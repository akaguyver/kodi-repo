#!/usr/bin/env python3
"""YouTube downloads for Sortovia, run on the phone next to kodi-share.

The Xbox can't run yt-dlp (Kodi's sandboxed Python has no ffmpeg or JavaScript
runtime), so the add-on asks this helper to do it. Videos are saved to
Download/YouTube, where Sortovia picks them up (tutorials -> Tutorials/<program>).

YouTube asks for a signed-in browser's cookies ("Sign in to confirm you're not a
bot"). Android won't let other apps read a browser's cookies, so export them once
as a cookies.txt file into Download; this helper moves it out of the shared
folder into ~/.config/xbox-share/youtube-cookies.txt and uses it from there.

HTTP on port 8081, same user/password as kodi-share (Basic auth):
  GET  /yt/ping              helper + cookies status
  GET  /yt/search?q=..&n=15&order=best|newest|views|longest|shortest  search results
  POST /yt/add   {"url", "title"}   queue a download
  GET  /yt/jobs              queue with progress
  POST /yt/cancel {"id"}     stop / remove one
  POST /yt/pause  {"id"} or {"all": true}   pause (the part downloaded is kept)
  POST /yt/resume {"id"} or {"all": true}   carry on
  POST /yt/clear             remove finished and failed
"""
import base64
import glob
import json
import urllib.request
import os
import re
import shutil
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

PORT = int(os.environ.get("YT_HELPER_PORT", "8081"))
CONF = os.path.expanduser("~/.config/xbox-share")
SHARE = os.environ.get("YT_SHARE", "/storage/emulated/0/Download")
OUT = os.path.join(SHARE, "YouTube")
TMP = os.path.expanduser("~/.cache/xbox-share/yt")  # half-done files stay out of the share
COOKIES = os.path.join(CONF, "youtube-cookies.txt")
JOBS_FILE = os.path.join(CONF, "yt-jobs.json")
SETTINGS_FILE = os.path.join(CONF, "yt-settings.json")
META_FILE = os.path.join(CONF, "yt-meta.json")  # channel, upload date ... of each downloaded video, by file name

# Download quality (Sortovia > YouTube > Download quality). Each is "the best up to this",
# preferring H.264/AAC in .mp4, which every Kodi plays; 4K on YouTube is VP9/AV1 only.
QUALITIES = {
    "2160": ("Best, up to 4K (big files)", ["-S", "res:2160,vcodec:h264,acodec:aac,ext:mp4:m4a", "--merge-output-format", "mp4"]),
    "1080": ("Full HD 1080p (recommended)", ["-S", "res:1080,vcodec:h264,acodec:aac,ext:mp4:m4a", "--merge-output-format", "mp4"]),
    "720": ("HD 720p (smaller, saves data)", ["-S", "res:720,vcodec:h264,acodec:aac,ext:mp4:m4a", "--merge-output-format", "mp4"]),
    "480": ("SD 480p (smallest video)", ["-S", "res:480,vcodec:h264,acodec:aac,ext:mp4:m4a", "--merge-output-format", "mp4"]),
    "audio": ("Sound only (.m4a - not sorted into the library)", ["-f", "bestaudio[ext=m4a]/bestaudio", "-x", "--audio-format", "m4a"]),
}
DEFAULT_QUALITY = "1080"


def settings():
    try:
        with open(SETTINGS_FILE) as f:
            s = json.load(f)
    except (OSError, ValueError):
        s = {}
    if s.get("quality") not in QUALITIES:
        s["quality"] = DEFAULT_QUALITY
    return s


def save_settings(s):
    os.makedirs(CONF, exist_ok=True)
    with open(SETTINGS_FILE, "w") as f:
        json.dump(s, f)
TERMUX_BIN = "/data/data/com.termux/files/usr/bin"


def tool(name):
    return shutil.which(name) or (os.path.join(TERMUX_BIN, name) if os.path.exists(os.path.join(TERMUX_BIN, name)) else None)


def password():
    with open(os.path.join(CONF, "password")) as f:
        return f.read().strip()


def log(msg):
    print(time.strftime("%H:%M:%S"), "[youtube]", msg, flush=True)


# ---------- cookies ----------
def import_cookies():
    """Move the newest exported cookies file (with YouTube cookies) out of Download."""
    found = []
    for pat in ("*cookie*.txt", "*Cookie*.txt", "*.cookies"):
        found += glob.glob(os.path.join(SHARE, pat))
    for path in sorted(set(found), key=os.path.getmtime, reverse=True):
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                text = f.read()
        except OSError:
            continue
        if "youtube.com" not in text:
            continue
        if not text.lstrip().startswith("# Netscape") and "\tTRUE\t" not in text and "\tFALSE\t" not in text:
            continue  # not a cookies.txt (Netscape format) file
        os.makedirs(CONF, exist_ok=True)
        with open(COOKIES, "w", encoding="utf-8") as f:
            f.write(text)
        os.chmod(COOKIES, 0o600)
        try:
            os.remove(path)  # don't leave sign-in cookies in the shared folder
        except OSError:
            pass
        log("cookies imported from %s" % os.path.basename(path))
        LAST_IMPORT["name"], LAST_IMPORT["when"] = os.path.basename(path), time.time()
        return os.path.basename(path)
    return None


LAST_IMPORT = {"name": None, "when": 0}


def cookies_status():
    just = import_cookies()
    if not os.path.exists(COOKIES):
        return {"present": False, "imported": None}
    age = (time.time() - os.path.getmtime(COOKIES)) / 86400
    signed_in = False
    try:
        with open(COOKIES, encoding="utf-8", errors="replace") as f:
            signed_in = any(n in f.read() for n in ("\tSAPISID\t", "\tLOGIN_INFO\t", "\t__Secure-3PSID\t"))
    except OSError:
        pass
    return {"present": True, "age_days": round(age, 1), "signed_in": signed_in, "imported": just,
            "last_import": LAST_IMPORT["name"], "last_import_ago_s": int(time.time() - LAST_IMPORT["when"]) if LAST_IMPORT["when"] else None}


def base_cmd():
    cmd = [tool("yt-dlp") or "yt-dlp", "--no-warnings"]
    node = tool("node")
    if node:
        cmd += ["--js-runtimes", "node:" + node]
    ff = tool("ffmpeg")
    if ff:
        cmd += ["--ffmpeg-location", ff]  # joins the video and sound tracks
    if os.path.exists(COOKIES):
        cmd += ["--cookies", COOKIES]
    return cmd


def explain(err):
    """yt-dlp's error, said plainly."""
    if "not a bot" in err or "Sign in to confirm" in err:
        return "YouTube wants a signed-in browser's cookies - export a new cookies.txt into Download"
    if "Private video" in err or "members-only" in err or "Join this channel" in err:
        return "private or members-only video (needs cookies from an account that can watch it)"
    if "Video unavailable" in err:
        return "video unavailable"
    if "No space left" in err:
        return "the phone is full"
    m = re.findall(r"ERROR: (.*)", err)
    return (m[-1] if m else err.strip().splitlines()[-1] if err.strip() else "failed")[:300]


# ---------- search ----------
# YouTube's own search API: one request, and unlike yt-dlp's search it says when
# each video came out ("4 years ago") and how many views it has. yt-dlp is the
# fallback (links, playlists, or if YouTube changes this reply).
ORDERS = [["best", "Best match"], ["newest", "Newest first"], ["views", "Most viewed"],
          ["longest", "Longest first"], ["shortest", "Shortest first"]]
API_SORT = {"views": "CAM="}  # YouTube sorts these itself; the rest are sorted here
AGE_RE = re.compile(r"(\d+)\s+(second|minute|hour|day|week|month|year)", re.I)
AGE_DAYS = {"second": 1 / 86400., "minute": 1 / 1440., "hour": 1 / 24., "day": 1, "week": 7, "month": 30.4, "year": 365.25}


def age_days(text):
    """'4 years ago' -> about 1461 (days); unknown -> None."""
    m = AGE_RE.search(text or "")
    return int(m.group(1)) * AGE_DAYS[m.group(2).lower()] if m else None


def _text(o):
    o = o or {}
    return o.get("simpleText") or "".join(r.get("text", "") for r in o.get("runs", []))


def _seconds(text):
    secs = 0
    for part in (text or "").split(":"):
        if not part.strip().isdigit():
            return 0
        secs = secs * 60 + int(part)
    return secs


def _video_renderers(o, out):
    if isinstance(o, dict):
        if "videoRenderer" in o:
            out.append(o["videoRenderer"])
        for v in o.values():
            _video_renderers(v, out)
    elif isinstance(o, list):
        for v in o:
            _video_renderers(v, out)
    return out


def parse_api_results(data):
    out = []
    for v in _video_renderers(data, []):
        vid = v.get("videoId")
        if not vid:
            continue
        views = re.sub(r"[^0-9]", "", _text(v.get("viewCountText")).split(" ")[0])
        out.append({"id": vid, "url": "https://www.youtube.com/watch?v=%s" % vid,
                    "title": _text(v.get("title")) or vid,
                    "channel": _text(v.get("ownerText") or v.get("longBylineText")),
                    "duration": _seconds(_text(v.get("lengthText"))),
                    "published": _text(v.get("publishedTimeText")),
                    "views": int(views) if views else None})
    return out


def api_search(q, order):
    from urllib.request import Request, urlopen
    body = {"context": {"client": {"clientName": "WEB", "clientVersion": "2.20250101.00.00", "hl": "en", "gl": "US"}},
            "query": q}
    if API_SORT.get(order):
        body["params"] = API_SORT[order]
    req = Request("https://www.youtube.com/youtubei/v1/search?prettyPrint=false", data=json.dumps(body).encode(),
                  headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
    resp = urlopen(req, timeout=170)
    try:
        return parse_api_results(json.loads(resp.read().decode("utf-8")))
    finally:
        resp.close()


def sort_results(res, order):
    big = float("inf")
    if order == "newest":
        res.sort(key=lambda r: age_days(r.get("published")) if age_days(r.get("published")) is not None else big)
    elif order == "longest":
        res.sort(key=lambda r: -(r.get("duration") or 0))
    elif order == "shortest":
        res.sort(key=lambda r: r.get("duration") or big)
    return res


def search(q, n, order="best"):
    if not re.match(r"https?://", q):
        try:
            res = api_search(q, order)
            if res:
                return sort_results(res[:max(n, 20)], order)
        except Exception as e:
            log("YouTube search API failed (%s), using yt-dlp" % e)
        return sort_results(ytdlp_search(q, n), order)
    return ytdlp_search(q, n)


def ytdlp_search(q, n):
    cmd = base_cmd() + ["--flat-playlist", "-J", "ytsearch%d:%s" % (n, q)]
    if re.match(r"https?://", q):
        cmd = base_cmd() + ["--flat-playlist", "-J", q]  # a link: list it (or a playlist's videos)
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    except subprocess.TimeoutExpired:
        raise RuntimeError("YouTube didn't answer within 3 minutes. The phone's internet is very slow right now "
                           "(a download or Kodi's library scan may be using it). Try again in a while.")
    if p.returncode != 0:
        raise RuntimeError(explain(p.stderr))
    data = json.loads(p.stdout)
    entries = data.get("entries") or [data]
    out = []
    for e in entries:
        vid = e.get("id")
        if not vid:
            continue
        url = e.get("url") or e.get("webpage_url") or "https://www.youtube.com/watch?v=%s" % vid
        if not url.startswith("http"):
            url = "https://www.youtube.com/watch?v=%s" % vid
        out.append({"id": vid, "url": url, "title": e.get("title") or vid,
                    "channel": e.get("channel") or e.get("uploader") or "",
                    "duration": e.get("duration") or 0})
    return out


# ---------- queue ----------
LOCK = threading.Lock()
WAKE = threading.Event()
JOBS = []
CURRENT = {"proc": None, "id": None}


def save_jobs():
    os.makedirs(CONF, exist_ok=True)
    tmp = JOBS_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(JOBS, f, indent=1)
    os.replace(tmp, JOBS_FILE)


def load_jobs():
    try:
        with open(JOBS_FILE) as f:
            JOBS.extend(json.load(f))
    except (OSError, ValueError):
        return
    for j in JOBS:
        if j["state"] in ("downloading", "copying"):
            j["state"] = "queued"  # helper was stopped part way: start that one again


def add_job(url, title="", quality=None):
    with LOCK:
        for j in JOBS:
            if j["url"] == url and j["state"] in ("queued", "downloading", "paused"):
                return j
        job = {"id": "%d%03d" % (time.time(), len(JOBS) % 1000), "url": url, "title": title or url,
               "state": "queued", "pct": 0.0, "speed": "", "eta": "", "file": "", "error": "",
               "quality": quality if quality in QUALITIES else settings()["quality"],
               "added": time.strftime("%Y-%m-%d %H:%M")}
        JOBS.append(job)
        save_jobs()
    WAKE.set()
    return job


TRANSIENT_RE = re.compile(r"Did not get any data blocks|timed out|Connection reset|Connection aborted|"
                          r"Temporary failure|Network is unreachable|IncompleteRead|HTTP Error 5\d\d|"
                          r"Remote end closed|EOF occurred", re.I)
PROG_RE = re.compile(r"^KSPROG\s*(.*)$")


def parse_progress(line):
    """KSPROG percent|speed|eta|fragment|fragments|bytes -> (pct or None, speed, eta, bytes).
    Videos YouTube sends in pieces (HLS) often have no percent: it comes from the pieces then."""
    f = (line.split(" ", 1)[1] if " " in line else "").split("|")
    f += [""] * (6 - len(f))
    num = lambda x: float(x) if re.match(r"^\d+(\.\d+)?$", (x or "").strip()) else None
    pct = num(f[0].strip().rstrip("%"))
    idx, cnt = num(f[3]), num(f[4])
    if pct is None and idx and cnt:
        pct = min(100.0, 100.0 * idx / cnt)
    clean = lambda x: "" if x.strip() in ("NA", "N/A", "Unknown", "None") else x.strip()
    return pct, clean(f[1]), clean(f[2]), num(f[5])


def run_job(job):
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(TMP, exist_ok=True)
    cmd = base_cmd() + [
        "--no-playlist", "--newline", "--quiet", "--progress", "--no-simulate",
    ] + QUALITIES[job.get("quality") if job.get("quality") in QUALITIES else DEFAULT_QUALITY][1] + [
        "--windows-filenames", "--trim-filenames", "180", "--no-mtime",
        # The hotspot / mobile data drops out now and then ("Did not get any data blocks"):
        # keep retrying pieces instead of failing the whole video.
        "--retries", "15", "--fragment-retries", "30", "--retry-sleep", "fragment:exp=1:30",
        "--socket-timeout", "30",
        # Whole download (and the final merge) happens in TMP, outside the share; publish() then
        # copies it in under a hidden name and renames it, so Sortovia never sees half a file.
        "-P", TMP, "-o", "%(title)s.%(ext)s",
        "--progress-template", "download:KSPROG %(progress._percent_str)s|%(progress._speed_str)s|%(progress._eta_str)s"
                               "|%(progress.fragment_index)s|%(progress.fragment_count)s|%(progress.downloaded_bytes)s",
        "--print", "before_dl:KSTITLE %(title)s",
        "--print", "after_move:KSFILE %(filepath)s",
        "--print", "after_move:KSMETA %(.{" + ",".join(META_FIELDS) + "})j",
        "--embed-metadata",  # channel, upload date and link go into the file itself too
        job["url"],
    ]
    log("downloading %s" % job["url"])
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)
    CURRENT["proc"], CURRENT["id"] = proc, job["id"]
    err_lines = []
    t = threading.Thread(target=lambda: err_lines.extend(proc.stderr), daemon=True)
    t.start()
    part = 0
    last_pct = -1.0
    for line in proc.stdout:
        line = line.strip()
        m = PROG_RE.match(line)
        with LOCK:
            if m:
                pct, speed, eta, got = parse_progress(line)
                if pct is not None:
                    if pct < last_pct - 50:
                        part += 1  # video done, now the sound track
                    last_pct = pct
                    job["pct"] = pct
                job["speed"], job["eta"] = speed, eta
                if got:
                    job["mb"] = round(got / 1e6, 1)
                job["part"] = part + 1
            elif line.startswith("KSTITLE "):
                job["title"] = line[8:]
            elif line.startswith("KSFILE "):
                job["file"] = line[7:]
            elif line.startswith("KSMETA "):
                try:
                    job["meta"] = trim_meta(json.loads(line[7:]))
                except ValueError:
                    pass
    proc.wait()
    t.join(5)
    with LOCK:
        CURRENT["proc"] = CURRENT["id"] = None
        if job["state"] in ("cancelled", "paused"):
            pass
        elif proc.returncode == 0 and job["file"]:
            job["state"], job["eta"], job["speed"] = "copying", "", ""
    if job["state"] == "copying":
        try:
            name = publish(job["file"])
            with LOCK:
                job["state"], job["pct"], job["file"] = "done", 100.0, name
                if job.get("meta"):
                    remember_meta(name, job["meta"])
            log("done: %s" % name)
        except OSError as e:
            with LOCK:
                job["state"], job["error"] = "failed", explain(str(e)) or "couldn't copy into Download/YouTube"
    with LOCK:
        if job["state"] in ("done", "failed", "cancelled", "paused"):
            pass
        else:
            err = "".join(err_lines)
            if TRANSIENT_RE.search(err) and job.get("tries", 0) < 3:
                # a dropped connection: try again by itself (the part already downloaded is kept)
                job["tries"] = job.get("tries", 0) + 1
                job["state"], job["error"] = "queued", ""
                log("connection dropped, trying again (%d of 3): %s" % (job["tries"], job["url"]))
                WAKE.set()
            else:
                job["state"], job["error"] = "failed", explain(err)
                log("failed: %s - %s" % (job["url"], job["error"]))
        save_jobs()


def publish(path):
    """Copy a finished download from TMP into Download/YouTube: hidden .part name first
    (Sortovia skips hidden files), then renamed. Returns the final file name."""
    name = os.path.basename(path)
    stem, ext = os.path.splitext(name)
    final, n = os.path.join(OUT, name), 2
    while os.path.exists(final):
        final = os.path.join(OUT, "%s (%d)%s" % (stem, n, ext))
        n += 1
    part = os.path.join(OUT, "." + os.path.basename(final) + ".part")
    shutil.copyfile(path, part)
    if os.path.getsize(part) != os.path.getsize(path):
        os.remove(part)
        raise OSError("copy into Download/YouTube came out short")
    os.replace(part, final)
    os.remove(path)
    return os.path.basename(final)


def worker():
    while True:
        with LOCK:
            job = next((j for j in JOBS if j["state"] == "queued"), None)
            if job:
                job["state"] = "downloading"
                save_jobs()
        if not job:
            WAKE.wait(30)
            WAKE.clear()
            continue
        try:
            run_job(job)
        except Exception as e:
            with LOCK:
                job["state"], job["error"] = "failed", str(e)[:300]
                save_jobs()


# ---------- what's known about each video (channel, upload date, series) ----------
META_FIELDS = ["id", "webpage_url", "title", "uploader", "channel", "channel_url", "uploader_url", "upload_date",
               "playlist_title", "playlist_id", "playlist_index", "playlist_count", "categories", "duration"]
META = {}
META_STATE = {"busy": False, "left": 0, "done": 0, "failed": 0}


def trim_meta(m):
    out = dict((k, m.get(k)) for k in META_FIELDS if m.get(k) not in (None, "", [], "NA"))
    if out.get("playlist_id") and out.get("playlist_id") == out.get("id"):
        for k in ("playlist_title", "playlist_id", "playlist_index", "playlist_count"):
            out.pop(k, None)  # a single video "playlist" isn't a series
    return out


def load_meta():
    try:
        with open(META_FILE) as f:
            META.update(json.load(f))
    except (OSError, ValueError):
        pass


def remember_meta(name, meta):
    META[name] = meta
    os.makedirs(CONF, exist_ok=True)
    tmp = META_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(META, f, indent=1, sort_keys=True)
    os.replace(tmp, META_FILE)


def _key(name):
    stem = re.sub(r"\.(mp4|mkv|webm|m4a|mp3)$", "", name, flags=re.I)
    stem = re.sub(r" \(\d+\)$", "", stem)
    return re.sub(r"[\W_]+", "", stem, flags=re.U).lower()


def fetch_meta(url):
    p = subprocess.run(base_cmd() + ["-j", "--skip-download", "--no-playlist", url],
                       capture_output=True, text=True, timeout=180)
    if p.returncode != 0:
        raise RuntimeError(explain(p.stderr))
    return trim_meta(json.loads(p.stdout))


def find_url(name):
    """The YouTube link of a downloaded video, from the download list or else a search for its title."""
    k = _key(name)
    for j in JOBS:
        if j.get("url") and k in (_key(j.get("file") or ""), _key(j.get("title") or "")):
            return j["url"]
    title = re.sub(r"\.(mp4|mkv|webm)$", "", name, flags=re.I)
    title = re.sub(r" \(\d+\)$", "", title)
    for r in search(title, 5):
        if _key(r.get("title") or "") == k:
            return r["url"]
    return None


def look_up(names):
    """Fill in what's known for files that don't have it yet (a few seconds each)."""
    todo = [n for n in names if not any(_key(n) == _key(have) for have in META)]
    META_STATE.update(busy=True, left=len(todo), done=0, failed=0)
    for n in todo:
        try:
            url = find_url(n)
            if not url:
                raise RuntimeError("not found on YouTube")
            remember_meta(n, fetch_meta(url))
            META_STATE["done"] += 1
        except Exception as e:
            log("no details for %s: %s" % (n, e))
            META_STATE["failed"] += 1
        META_STATE["left"] -= 1
    META_STATE["busy"] = False
    log("video details: %d found, %d not found" % (META_STATE["done"], META_STATE["failed"]))


# ---------- torrents on the phone (aria2), for what Real-Debrid can't get ----------
TOR_WORK = os.path.expanduser("~/.cache/xbox-share/torrents")  # half-done downloads stay out of the share
TOR_OUT = os.path.join(SHARE, "Torrents")  # (and Download/Real-Debrid for unlocked links)
TOR_SESSION = os.path.join(CONF, "aria2-session.txt")
TOR_PORT = 6801
TOR = {"proc": None, "moved": set()}


def aria(method, *params):
    """One call to the phone's own aria2 (localhost only, with the kodi-share password as its secret)."""
    body = json.dumps({"jsonrpc": "2.0", "id": "s", "method": method,
                       "params": ["token:" + password()] + list(params)}).encode()
    req = urllib.request.Request("http://127.0.0.1:%d/jsonrpc" % TOR_PORT, data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        out = json.loads(r.read().decode("utf-8"))
    if out.get("error"):
        raise RuntimeError(out["error"].get("message") or "aria2 said no")
    return out.get("result")


def aria_start():
    """aria2 running in the background, started the first time it's needed. False when it isn't installed."""
    if TOR["proc"] and TOR["proc"].poll() is None:
        return True
    exe = tool("aria2c")
    if not exe:
        return False
    os.makedirs(TOR_WORK, exist_ok=True)
    os.makedirs(CONF, exist_ok=True)
    if not os.path.exists(TOR_SESSION):
        open(TOR_SESSION, "a").close()
    TOR["proc"] = subprocess.Popen([
        exe, "--enable-rpc", "--rpc-listen-all=false", "--rpc-listen-port=%d" % TOR_PORT,
        "--rpc-secret=" + password(), "--dir=" + TOR_WORK, "--seed-time=0", "--continue=true",
        "--max-concurrent-downloads=2", "--bt-save-metadata=false", "--follow-torrent=mem",
        "--input-file=" + TOR_SESSION, "--save-session=" + TOR_SESSION, "--save-session-interval=20",
        "--force-save=false", "--quiet=true"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(30):
        try:
            aria("aria2.getVersion")
            log("torrent downloads ready (aria2), saving into %s" % TOR_OUT)
            return True
        except Exception:
            time.sleep(0.3)
    return False


def _tor_name(d):
    bt = (d.get("bittorrent") or {}).get("info") or {}
    files = d.get("files") or []
    path = files[0].get("path") if files else ""
    return bt.get("name") or (os.path.basename(path) if path else "") or "Getting the torrent's details..."


KINDS = ("Torrents", "Real-Debrid")  # Download/Torrents for torrents, Download/Real-Debrid for unlocked links


def _tor_rel(d):
    """[kind, ...path] of a download's first file, relative to TOR_WORK."""
    files = d.get("files") or []
    if not files or not files[0].get("path"):
        return None
    rel = os.path.relpath(files[0]["path"], TOR_WORK).split(os.sep)
    return rel if rel[0] in KINDS and len(rel) > 1 else ["Torrents"] + rel


def _into_share(src, final):
    """Move src to final through a hidden name, so Sortovia never sees half of it. Returns the name used."""
    base, n = final, 2
    stem, ext = os.path.splitext(base)
    while os.path.exists(final):
        final = "%s (%d)%s" % (stem, n, ext)
        n += 1
    os.makedirs(os.path.dirname(final), exist_ok=True)
    hidden = os.path.join(os.path.dirname(final), "." + os.path.basename(final) + ".part")
    shutil.move(src, hidden)
    os.replace(hidden, final)
    return final


def tor_publish(d):
    """A finished torrent goes into Download/Torrents whole; an unlocked file into Download/Real-Debrid/<group>."""
    rel = _tor_rel(d)
    if not rel:
        return
    kind = rel[0]
    if kind == "Torrents":
        src = os.path.join(TOR_WORK, *rel[:2]) if os.path.exists(os.path.join(TOR_WORK, *rel[:2])) else os.path.join(TOR_WORK, rel[1])
        final = os.path.join(SHARE, "Torrents", os.path.basename(src))
    else:
        src = os.path.join(TOR_WORK, *rel)
        final = os.path.join(SHARE, *rel)
    if os.path.exists(src):
        log("download done: %s" % os.path.basename(_into_share(src, final)))


FIELDS = ["gid", "status", "totalLength", "completedLength", "downloadSpeed", "files", "bittorrent", "dir",
          "errorMessage", "followedBy", "numSeeders", "connections"]


def tor_jobs():
    if not aria_start():
        return []
    out = []
    for d in (aria("aria2.tellActive", FIELDS) + aria("aria2.tellWaiting", 0, 100, FIELDS) +
              aria("aria2.tellStopped", 0, 100, FIELDS)):
        if d.get("followedBy"):
            continue  # a magnet's first step (its details); the real download follows it
        total, done = int(d.get("totalLength") or 0), int(d.get("completedLength") or 0)
        speed = int(d.get("downloadSpeed") or 0)
        state = d["status"]
        if state == "complete" and d["gid"] not in TOR["moved"]:
            TOR["moved"].add(d["gid"])
            try:
                tor_publish(d)
            except OSError as e:
                log("couldn't move a finished torrent into Download/Torrents: %s" % e)
        rel = _tor_rel(d)
        out.append({"id": d["gid"], "name": _tor_name(d), "kind": rel[0] if rel else "Torrents", "state": state, "size": total,
                    "pct": round(100.0 * done / total, 1) if total else 0.0, "speed": speed,
                    "eta": int((total - done) / speed) if speed and total else 0,
                    "seeds": int(d.get("numSeeders") or 0), "peers": int(d.get("connections") or 0),
                    "error": d.get("errorMessage") or ""})
    return out


def tor_watch():
    """Moves finished torrents into the share even when nobody is looking."""
    while True:
        time.sleep(15)
        if TOR["proc"] and TOR["proc"].poll() is None:
            try:
                tor_jobs()
            except Exception:
                pass


# ---------- copies into the phone's Music folder ----------
MUSIC_DIR = os.environ.get("PHONE_MUSIC", "/storage/emulated/0/Music")


def _inside(base, rel):
    """base/rel, or None when rel would leave base (.. or an absolute path)."""
    if not isinstance(rel, str) or not rel or rel.startswith(("/", "\\")):
        return None
    path = os.path.realpath(os.path.join(base, rel))
    return path if path.startswith(os.path.realpath(base) + os.sep) else None


def copy_to_music(files):
    """[{"from": path in the shared folder, "to": "Artist/Album/03 - Title.mp3"}]: each copied into Music,
    unless the same file is already there. Done before Sortovia moves them, so it replies when finished."""
    copied, same, failed = 0, 0, []
    for f in files:
        src, dst = _inside(SHARE, f.get("from")), _inside(MUSIC_DIR, f.get("to"))
        if not src or not dst or not os.path.isfile(src):
            failed.append(f.get("from") or "?")
            continue
        try:
            if os.path.exists(dst) and os.path.getsize(dst) == os.path.getsize(src):
                same += 1
                continue
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(src, dst + ".part")
            os.replace(dst + ".part", dst)
            copied += 1
        except OSError as e:
            log("music copy failed: %s (%s)" % (f.get("from"), e))
            failed.append(f.get("from") or "?")
    log("copied %d music file(s) into the phone's Music folder (%d already there)" % (copied, same))
    return {"copied": copied, "already": same, "failed": failed}


# ---------- HTTP ----------
class Handler(BaseHTTPRequestHandler):
    server_version = "SortoviaYT/1"

    def log_message(self, fmt, *args):
        pass

    def _authed(self):
        h = self.headers.get("Authorization", "")
        try:
            user, _, pw = base64.b64decode(h.split(" ", 1)[1]).decode().partition(":")
        except Exception:
            user = pw = None
        if user == "kodi" and pw == password():
            return True
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="kodisorter-youtube"')
        self.end_headers()
        return False

    def _send(self, obj, code=200):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _body(self):
        n = int(self.headers.get("Content-Length") or 0)
        try:
            return json.loads(self.rfile.read(n) or b"{}")
        except ValueError:
            return {}

    def do_GET(self):
        if not self._authed():
            return
        u = urlparse(self.path)
        q = parse_qs(u.query)
        if u.path == "/yt/ping":
            ver = subprocess.run([tool("yt-dlp") or "yt-dlp", "--version"], capture_output=True, text=True).stdout.strip()
            return self._send({"ok": True, "cookies": cookies_status(), "yt_dlp": ver,
                               "node": bool(tool("node")), "folder": OUT})
        if u.path == "/yt/search":
            cookies_status()
            try:
                return self._send({"results": search(q.get("q", [""])[0], min(int(q.get("n", ["15"])[0]), 40),
                                                     q.get("order", ["best"])[0]), "orders": ORDERS})
            except Exception as e:
                return self._send({"error": str(e)}, 502)
        if u.path == "/yt/jobs":
            with LOCK:
                return self._send({"jobs": JOBS})
        if u.path == "/yt/meta":
            return self._send(dict(META_STATE, meta=META))
        if u.path == "/tor/jobs":
            try:
                return self._send({"installed": bool(tool("aria2c")), "jobs": tor_jobs(), "folder": TOR_OUT})
            except Exception as e:
                return self._send({"installed": bool(tool("aria2c")), "jobs": [], "error": str(e)})
        self._send({"error": "not found"}, 404)

    def do_POST(self):
        if not self._authed():
            return
        u = urlparse(self.path)
        b = self._body()
        if u.path == "/yt/add":
            url = (b.get("url") or "").strip()
            if not re.match(r"https?://", url):
                url = "https://www.youtube.com/watch?v=" + url if re.match(r"^[\w-]{11}$", url) else ""
            if not url:
                return self._send({"error": "that isn't a YouTube link"}, 400)
            cookies_status()
            return self._send({"job": add_job(url, b.get("title", ""), b.get("quality"))})
        if u.path in ("/yt/pause", "/yt/resume"):
            pause = u.path == "/yt/pause"
            with LOCK:
                hit = [j for j in JOBS if (b.get("all") or j["id"] == b.get("id")) and
                       j["state"] in (("queued", "downloading") if pause else ("paused",))]
                for j in hit:
                    if pause and j["state"] == "downloading" and CURRENT["id"] == j["id"] and CURRENT["proc"]:
                        CURRENT["proc"].terminate()  # yt-dlp keeps the part file and carries on from it later
                    j["state"] = "paused" if pause else "queued"
                    j["speed"] = j["eta"] = ""
                save_jobs()
            if hit:
                log("%s %d download(s)" % ("paused" if pause else "resumed", len(hit)))
                WAKE.set()
            return self._send({"ok": bool(hit), "count": len(hit)})
        if u.path == "/yt/cancel":
            with LOCK:
                job = next((j for j in JOBS if j["id"] == b.get("id")), None)
                if job and job["state"] == "downloading" and CURRENT["id"] == job["id"] and CURRENT["proc"]:
                    job["state"] = "cancelled"
                    CURRENT["proc"].terminate()
                elif job:
                    JOBS.remove(job)
                save_jobs()
            return self._send({"ok": bool(job)})
        if u.path == "/yt/settings":
            s = settings()
            if b.get("quality") in QUALITIES:
                s["quality"] = b["quality"]
                save_settings(s)
                log("download quality: %s" % QUALITIES[s["quality"]][0])
            if b.get("order") in dict(ORDERS):
                s["order"] = b["order"]
                save_settings(s)
            s.setdefault("order", "best")
            return self._send({"settings": s, "qualities": [[k, v[0]] for k, v in QUALITIES.items()],
                               "orders": ORDERS})
        if u.path == "/yt/cookies":
            # "Import cookies now": look in Download right away and say what happened
            st = cookies_status()
            return self._send({"cookies": st})
        if u.path == "/yt/meta":
            # look up the channel and upload date of videos downloaded before this was saved
            names = [n for n in (b.get("files") or []) if isinstance(n, str)]
            if b.get("all"):
                names += [f for f in os.listdir(OUT) if re.search(r"\.(mp4|mkv|webm)$", f, re.I)] if os.path.isdir(OUT) else []
                names += [j["file"] for j in JOBS if j.get("state") == "done" and j.get("file")]
            if not META_STATE["busy"]:
                threading.Thread(target=look_up, args=(sorted(set(names)),), daemon=True).start()
                META_STATE["busy"] = True
            return self._send(dict(META_STATE, meta=META))
        if u.path.startswith("/tor/"):
            if not aria_start():
                return self._send({"error": "aria2 isn't installed on the phone: in Termux type  pkg install aria2"}, 400)
            try:
                if u.path == "/tor/add":
                    uri = (b.get("uri") or "").strip()
                    if not re.match(r"^(magnet:\?|https?://)", uri):
                        return self._send({"error": "that isn't a magnet link or a torrent address"}, 400)
                    kind = "Real-Debrid" if b.get("kind") == "Real-Debrid" else "Torrents"
                    sub = re.sub(r'[\\/:*?"<>|]+', " ", b.get("group") or "").strip()
                    opts = {"dir": os.path.join(TOR_WORK, kind, sub) if sub else os.path.join(TOR_WORK, kind)}
                    if b.get("out"):
                        opts["out"] = re.sub(r'[\\/:*?"<>|]+', " ", b["out"]).strip()
                    gid = aria("aria2.addUri", [uri], opts)
                    log("torrent added: %s" % (b.get("name") or uri[:60]))
                    return self._send({"id": gid})
                gids = [j["id"] for j in tor_jobs()] if b.get("all") else [b.get("id")]
                method = {"/tor/pause": "aria2.forcePause", "/tor/resume": "aria2.unpause",
                          "/tor/remove": "aria2.forceRemove"}.get(u.path)
                if not method:
                    return self._send({"error": "not found"}, 404)
                done = 0
                for g in gids:
                    try:
                        aria(method, g)
                        done += 1
                    except Exception:
                        try:
                            aria("aria2.removeDownloadResult", g)  # finished or failed: just off the list
                            done += 1
                        except Exception:
                            pass
                return self._send({"ok": done})
            except Exception as e:
                return self._send({"error": str(e)}, 502)
        if u.path == "/phone/music":
            # Sortovia moving music off the phone: keep a copy in the phone's own Music folder first
            return self._send(copy_to_music(b.get("files") or []))
        if u.path == "/yt/clear":
            with LOCK:
                JOBS[:] = [j for j in JOBS if j["state"] in ("queued", "downloading", "paused")]
                save_jobs()
            return self._send({"ok": True})
        self._send({"error": "not found"}, 404)


def main():
    if not os.path.exists(os.path.join(CONF, "password")):
        sys.exit("no kodi-share password yet - start kodi-share once first")
    if not tool("yt-dlp"):
        log("yt-dlp is missing: in plain Termux run  pkg install yt-dlp ffmpeg nodejs")
    load_jobs()
    load_meta()
    st = cookies_status()
    log("YouTube downloads on port %d -> %s (cookies: %s)" % (
        PORT, OUT, "OK" if st.get("present") else "none yet - export cookies.txt into Download"))
    threading.Thread(target=worker, daemon=True).start()
    if os.path.getsize(TOR_SESSION) if os.path.exists(TOR_SESSION) else 0:
        aria_start()  # torrents that were going when the phone stopped carry on
    threading.Thread(target=tor_watch, daemon=True).start()
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
