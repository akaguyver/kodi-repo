#!/usr/bin/env bash
# kodi-share (older name: xbox-share): let Sortovia read the phone's downloads over the
# hotspot Wi-Fi (no mobile data used). Runs a password-protected WebDAV server.
#   kodi-share                      share /storage/emulated/0/Download
#   kodi-share /storage/emulated/0/Movies   share another folder
#   kodi-share password             just show the password (e.g. to type it into the companion app)
#   kodi-share stop                 stop a share that's running (in any Termux session)
# Stop it with Ctrl+C (or close Termux).
# Saved settings stay in ~/.config/xbox-share, so existing passwords keep working.
DIR="${1:-/storage/emulated/0/Download}"
PORT=8080
CONF="$HOME/.config/xbox-share"
mkdir -p "$CONF"
if [ ! -s "$CONF/password" ]; then
  # letters + digits only, so it can be typed with the Xbox controller
  tr -dc 'a-z0-9' </dev/urandom | head -c 8 >"$CONF/password"
fi
PASS=$(cat "$CONF/password")
if [ "$1" = "password" ] || [ "$1" = "pass" ]; then
  echo "kodi-share password: $PASS   (user name: kodi)"
  exit 0
fi
if [ "$1" = "log" ]; then
  tail -n 40 "$CONF/share.log" 2>/dev/null || echo "No log yet."
  exit 0
fi
if [ "$1" = "restart" ]; then
  bash "$0" stop
  sleep 1
  exec bash "$0"
fi
if [ "$1" = "stop" ]; then
  # only the share itself (anchored, so it can't match this script); the YouTube helper
  # keeps running, so Sortovia's YouTube downloads still work with the companion app
  if pkill -f "^rclone serve webdav" 2>/dev/null; then
    echo "kodi-share stopped. (The companion app can share now.)"
  else
    echo "kodi-share wasn't running."
  fi
  exit 0
fi

if ! command -v rclone >/dev/null; then
  echo "rclone is missing: in Termux run  pkg install rclone  (or run the Sortovia installer again)"; exit 1
fi
if [ ! -d "$DIR" ]; then
  echo "Folder not found: $DIR"; exit 1
fi

# Phone's addresses on Wi-Fi/hotspot (not mobile data or the VPN)
IPS=$(ifconfig 2>/dev/null | awk '/^[a-z]/{i=$1} /inet /{print i, $2}' \
      | grep -Ev '^(lo|rmnet|tun|dummy|ccmni|ppp)' | awk '{print $2}')

echo "================ KODI SHARE ================"
echo " Sharing : $DIR"
echo " User    : kodi"
echo " Password: $PASS"
if [ -n "$IPS" ]; then
  for ip in $IPS; do echo " Address : $ip   (port $PORT)"; done
else
  echo " Address : none found - is the Mobile Hotspot ON?"
  echo "           (Sortovia finds the phone by itself anyway)"
fi
echo
echo " In Kodi: Sortovia > Sort my downloads > Choose folders >"
echo "   My phone over Wi-Fi - phone storage"
echo " It runs in the background, so you can keep typing here."
echo "   kodi-share stop     stop sharing"
echo "   kodi-share restart  stop and start again (after an update)"
echo "   kodi-share log      see what it's doing"
echo " Keep Termux running (it can be in the background) while files copy."
echo " YouTube downloads: Sortovia > Download from YouTube (port 8081)."
echo "============================================"
if (exec 3<>/dev/tcp/127.0.0.1/$PORT) 2>/dev/null; then
  echo
  echo " Port $PORT is already in use: kodi-share is already running (maybe in another Termux"
  echo " session), or the companion app is sharing. Kodi can already reach the phone."
  echo " To restart it: type  kodi-share stop  then  kodi-share"
  exit 1
fi
# YouTube and torrent downloads for the add-on (port 8081, same password): see yt_helper.py.
# A helper left over from before (an older copy, or one started elsewhere) is replaced, so it can't hold the port.
HELPER="$(dirname "$(readlink -f "$0")")/yt_helper.py"
if [ -f "$HELPER" ] && [ "$DIR" = "/storage/emulated/0/Download" ]; then
  pkill -f "python3? .*yt_helper\.py$" 2>/dev/null && sleep 1
  YT_SHARE="$DIR" nohup python3 "$HELPER" >>"$CONF/helper.log" 2>&1 </dev/null &
fi
# In the background (with its own log), so the terminal stays free to type in.
nohup rclone serve webdav "$DIR" --addr ":$PORT" --user kodi --pass "$PASS" --realm rclone \
  --dir-cache-time 5s --poll-interval 0 --log-level NOTICE >"$CONF/share.log" 2>&1 </dev/null &
SPID=$!
command -v termux-wake-lock >/dev/null && termux-wake-lock 2>/dev/null
sleep 2
if kill -0 $SPID 2>/dev/null; then
  echo " Sharing now. Type  kodi-share stop  to stop."
else
  echo " Sharing didn't start:"; tail -n 5 "$CONF/share.log"; exit 1
fi
