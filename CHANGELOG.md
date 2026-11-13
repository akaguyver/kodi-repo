# Sortovia (formerly Kodi Sorter) – version history

Newest first. Each line says what the update changed for you.

## 1.60 – The phone's download queue keeps moving
- **1.60.0**
  - The phone downloads **8 at a time** instead of 2, so one slow torrent can't hold up the queue.
  - A torrent with no data for **5 minutes** goes to the back of the queue. After its first go and 3 more, it moves to a new **Failed - tried 3x** list in **Downloads**, where **Try again** (one or all) puts it back on the queue later, carrying on from what it has.
  - Torrents find peers faster: 12 of the steadiest free public trackers are added to every one, along with peers on your own network.
  - Search results sent to the phone always try **Real-Debrid first** when you're signed in; the phone downloads as a torrent only what Real-Debrid can't get.
  - Needs the phone helper updated: run the phone installer again (Downloads tells you if it's older).

## 1.59 – Downloads you can sort, resume and retry
- **1.59.0**
  - **Downloads** has buttons for each kind: **Waiting for peers**, **Downloading**, **Queued**, **Paused**, **Failed** and **Done**, each with how many. "Waiting" was the queue: the phone runs two at a time, and a torrent with no peers kept its place forever. Now one with no peers for 5 minutes moves to the back, so the others get going.
  - **Try again** on any failed download, and **Retry all failed**. Downloads that failed because the connection dropped are tried again by themselves, up to 3 times.
  - **Real-Debrid on the Xbox** keeps what it has downloaded when the connection or the phone's share goes down, and carries on from there. Downloads cut off by Kodi closing come back when you next open Sortovia.
  - A Real-Debrid download that finishes smaller than Real-Debrid said shows as **Failed**, so you can get it again.
  - **Packed albums** (one archive with a whole album) sent to the phone are unpacked into their folder before sorting. .rar needs Kodi's Archive support add-on; the screen says so if it's missing.
  - **Real-Debrid**: a whole album packed into one archive now says **packed: all N files** and downloads all of it, instead of showing as one song. When picking files, choose **Download all**, **Pick the ones I want** or **Pick the ones I don't want**, then one OK. Each torrent is checked right after sending, so a dead one is reported at once.
  - On the phone, run **kodi-share stop**, then **kodi-share**, once to get the new helper.

## 1.58 – File-host links, and torrents on the phone or your own client
- **1.58.5**
  - Moving music off the phone now offers **Also keep a copy in the phone's Music folder** for albums that came packed in an archive (.rar or .zip) too. Before, it only asked for plain files, so a packed album never asked. The Xbox unpacks the songs and sends them to Music/Artist/Album on the phone. On the phone, run **kodi-share stop**, then **kodi-share**, once to get this.
  - In the phone app, **Copy music from the Xbox** now puts songs straight into Music/Artist, with no From the Xbox folder. **Tidy up From the Xbox** moves copies you already have there (including a From the Xbox inside From the Xbox) up to their artist's folder and keeps their analysis.
- **1.58.4**
  - **Downloads on the phone** now says which folder a finished download is in: Download/Real-Debrid or Download/Torrents. Before, it always said Torrents.
  - **Sort the finished downloads** sorts whichever folder has something in it, and asks only when both do.
  - A torrent that's still finding peers to get its details now reads that way, instead of "[METADATA]...".
- **1.58.3**
  - Sending torrents to **the phone** now tries **Real-Debrid first**: what Real-Debrid can get, the phone downloads through Real-Debrid, and only the ones it can't get are downloaded as torrents on the phone. You can still pick **This Xbox through Real-Debrid**, **Torrent only** on the phone, or one of your own torrent clients.
  - When Real-Debrid can't get a torrent, it now goes straight to the phone by default, with no question. **Indexes and categories > Torrent clients** can change that.
- **1.58.2**
  - **Downloads on the phone > Sort the finished downloads** now says when nothing has finished downloading yet. Before, it said it couldn't reach the phone.
- **1.58.1**
  - **Pause a Real-Debrid download** on the Xbox and carry on later. While one runs, Sortovia's menu has **pause** (or **carry on**) next to **Stop**. The half-done file is kept and it carries on from where it got to.
  - **Real-Debrid > Download on**: choose whether the phone or this Xbox downloads what Real-Debrid unlocks. It starts on the phone, which is faster here, and you can also choose each time. On the phone, files go to Download/Real-Debrid.
  - **Downloads on the phone** (it was Torrents on the phone) shows torrents and Real-Debrid files together, and sorts either folder when they're done.
- **1.58.0**
  - **Real-Debrid > Get links from a web page**: give it a forum post, blog or release page, and it finds every Rapidgator, Nitroflare or other file-host link Real-Debrid can unlock. Tick them and they download to the drive. It uses Real-Debrid's own list of supported hosts, so new hosts work by themselves.
  - Download sites' **RSS feeds** work in **Search torrents** too. Add one under **Indexes and categories**; its posts show as "file-host links", and ticking one unlocks the links in the post, or on the page it links to.
  - **Torrents on the phone** (Downloads): when Real-Debrid can't get a torrent, the phone can download it, using aria2 in Termux. It's saved into Download/Torrents. Kodi shows progress, lets you pause, carry on or remove each one, and sorts the finished ones into your library. The phone needs aria2 once: in Termux type **pkg install aria2**.
  - **Your own torrent client**: add Transmission, qBittorrent, aria2, or BiglyBT or Vuze (they use the Transmission-style remote) on the phone or your network, under **Indexes and categories > Torrent clients**.
  - Search results can now go to Real-Debrid, the phone, or any client you added.
  - When Real-Debrid can't get a torrent, Sortovia asks where to download it instead. You can make it send it by itself to the phone or a client, or do nothing. Torrents it couldn't get in the background wait under **Real-Debrid > Couldn't get on Real-Debrid**.

## 1.57 – Torrent search, folders from your searches, and the TV library fixed for good
- **1.57.1**
  - **Indexes and categories > Add an index: a site's RSS feed** now takes a site's ordinary feed address. Sortovia reads the whole feed and keeps the items whose titles have your search words. A search feed with {q} where the words go still works too.
  - The feeds you added under **Real-Debrid > Add a feed** are searched too: in **Everything**, and in their own category, **My feeds**.
- **1.57.0**
  - **Search torrents** (Downloads, and in Real-Debrid): search many indexes at once by category, such as Music, Music videos, Movies, TV or Anime. Built in: Knaben, which searches many trackers at once, plus The Pirate Bay, Nyaa, Torrents-CSV and YTS. Tick results and Real-Debrid fetches them; then they download by themselves.
  - **Indexes and categories**: turn any index off, and add your own: Jackett or Prowlarr (Torznab), which reach almost any tracker, private ones too, or a tracker's search RSS address. Make your own categories (such as **My releases**) and choose which indexes each one searches.
  - **Download new torrents by themselves** (Real-Debrid): anything added to your account, from the phone, the website or another app, downloads as soon as Real-Debrid has it.
  - The phone app can now take **magnet links**: tap one anywhere on the phone, choose Sortovia, and it goes to Real-Debrid.
  - **Download from YouTube** is now always in Downloads. Before, it only showed when the welcome screen's phone question had been answered yes.
  - **Music and DJing** is now a folder inside **Tutorials**.
  - YouTube videos you download from a search go into a folder named after the search: "how to build a house" goes to **Tutorials/House building**. If a folder that means the same is already there, it's used instead, and a video Sortovia already recognises (a program, or a kind of music video) goes where it always did.
  - YouTube's **Downloads** list now shows the one downloading first, then the waiting ones in order, then the finished ones, newest first.
  - **TV library**: when Kodi scans your TV folder twice under two spellings (such as D:\\TV and D:/TV), every episode is listed twice and the whole folder can become one show with a wrong name, such as "TV Animal Farm". **Clean the library > TV** now stops the second scan, so this doesn't come back, and takes the wrong show out by itself. Sortovia also checks for this each time it opens. Only library entries change, never your files.
  - When you sort music from the phone, Sortovia asks whether to keep a copy in the phone's **Music** folder too (Music/Artist/Album).
  - **Library > Get tags from the phone** now asks which parts to write (key, tempo, genre, energy), and for each one whether to keep what a track's tag already has or replace it. It then lists every change before anything is written.

## 1.56 – Quicker library backups, and YouTube videos sorted by what they are
- **1.56.0**
  - **Library backups** now save only what changed: each movie, show and episode that was added, changed (such as a watched mark) or removed, plus a copy of Kodi's library database. That takes seconds. Kodi's own full export, which is slow, now runs once a week, or when you choose **Kodi library backup > Full backup now**. When nothing in the library changed, no backup is made at all.
  - A backup's progress now shows in the **top-right corner**, and **Back up the library now** runs in the background, so you can keep using Kodi. Cleaning the library says that Kodi's own progress is in the corner too.
  - **YouTube downloads about music and DJing** (beatmatching, beat grids, rekordbox, Serato, Mixed In Key, song structure, Ableton and so on) now go to a new **Music and DJing** folder, in **DJing**, **Making music**, **Music videos** or **DJ sets and mixes**. Add that folder in Kodi as a source to see it.
  - Many more YouTube lessons are now recognised ("How to...", "Explained", "Tips", reviews and demos), with new **Claude** and **Closet design** folders in Tutorials.
  - Before sorting YouTube downloads, the videos that still don't look like lessons or music are listed: tick any to sort anyway, and choose where they go (a Tutorials program, a Music and DJing kind, or **YouTube videos**).
  - New YouTube downloads keep their **channel, upload date and link**, inside the file and in Sortovia. **Download from YouTube > Look up channel and upload date for videos already downloaded** finds them for the videos you already have, and writes a small .nfo next to each one.
  - **Hold down a video in Tutorials or Music and DJing > YouTube video (Sortovia)** shows its channel and upload date, lists **more from that channel** to download, and finds **the rest of its series** (its playlist, or the channel's videos named the same way, such as "Step 1" to "Step 6"). Restart Kodi once if the option doesn't appear. The phone's YouTube service needs a restart too: stop kodi-share and start it again.
  - Fixed: sorting could stop with an error on a separate audio track (such as an .mka) whose language Sortovia couldn't read.

## 1.55 – Every genre in a tag, and clearer DJ tools
- **1.55.2**
  - **Library > Clean the library > TV** now finds a show Kodi made out of your whole TV folder (its episodes repeat your real shows') and offers to take just that entry out of the library. Your files and your other shows stay as they are.
- **1.55.1**
  - An opening or ending credits clip whose name doesn't say which show it's from (such as "NCOP One Reason.mkv") is now left where it is. Before, a clip in a download folder like **Videos** became a new show called "Videos", and Kodi's look-up turned that into a show you don't have.
- **1.55.0**
  - **Find genres** now reads every genre in a track's tag. A track tagged "Dubstep" and "Trap" shows both, at the start of the screen, and the screen's top line says what each artist or track is tagged with now.
  - The genre screen's colour key now names every source: release info from Discogs, Apple Music and Deezer, and tags from Last.fm and Audius.
  - After a look-up, the summary says how many tracks each source found, so a source that knew none of them (Audius often doesn't) is easy to see.
  - **Crossfade between songs** now also turns on crossfading between songs from the same album, and says that Kodi crossfades as a song ends on its own.
  - **Play a playlist in mixing order** now puts songs within 6% of each other's tempo next to each other before it looks at the key, counting half and double time (75 and 150 BPM match).
  - Where a song has no key, Sortovia now says the phone app can work it out: **Analyse the Xbox's music**, then **Send tags to the Xbox**, then **Library > Get tags from the phone**.

## 1.54 – Write your genres, playlists that show, and tags from the phone
- **1.54.0**
  - **Find genres** now writes the genres you chose into your MP3s, after you've seen what each track would get and said yes. Several genres go in as one text, such as "Dubstep / Riddim": Kodi lists each genre, and rekordbox and Serato show the whole text. Each file's old tag is saved first, so **File > Undo the last music tag fix** puts them back. Other formats, such as FLAC, aren't written yet.
  - **Playlists** that Sortovia makes are now saved as .m3u, which Kodi's **Music > Playlists** shows. Ones saved before as .m3u8 are renamed.
  - **Hold down a song or an album > Add to a playlist (Sortovia)** adds it to one of your playlists, or a new one. Restart Kodi once if the option doesn't appear.
  - **Library > Get tags from the phone** writes the keys, tempos, energy and genres the Sortovia phone app worked out into your MP3s. Kodi on the Xbox can't listen to music itself, so the phone does it over Wi-Fi. It only fills in what's missing unless you choose to replace, and the old tags can be put back.
  - In **DJ and playlists**, mixing order is better at finding the sections of a track.

## 1.53 – Genres for each track
- **1.53.0**
  - **Find genres** by **Album** now shows a screen for **each track**, so a crossover track can have different genres from its artist. Choosing by Artist works as before, with **Change one track** for single tracks.
  - Genres found that **aren't on your list** now show on the screen too, after yours. When you choose any, Sortovia offers to add them to your list.
  - Genres already in a track's tags start **ticked**.
  - Tracks with a featured or collaborating artist ("A feat. B", "A & B") also suggest the genres you chose for that artist, and start with them ticked.
  - Genres are now also looked up on **Apple Music**, **Deezer** and **Audius**, with no keys needed. Apple Music allows about 20 searches a minute, so a first look-up takes longer. Lookups are remembered, so repeat runs are quick.
  - **DJ and playlists** has two new orders: **Live set** (warms up, peaks about three quarters of the way through, then cools down) and **Peaks and valleys** (harder, then softer, again and again).

## 1.52 – DJ tools on the Xbox
- **1.52.0**
  - **DJ and playlists**, in *Library*, is a new menu.
  - **Play a playlist in mixing order** puts a saved playlist, or the music playing now, in **Key order**, **Build up** (softest first) or **Wind down**. Each song is in a key that mixes into the next. It can play the result now, save it as a new playlist, or both.
  - **What mixes after the song playing now** lists songs in a key next to it and within 6% of its tempo. Pick one and it plays next. **Hold down a song** in the music library for the same list. Restart Kodi once if the option doesn't appear.
  - **Crossfade between songs** switches Kodi's own crossfade on or off. Kodi can't match beats; the phone app's DJ mix can.
  - **Make a Kodi playlist from another playlist** reads a CSV export (Spotify through Exportify or TuneMyMusic), an M3U, a typed list or a Deezer link. It uses the songs you have, can put them in mixing order, and lists the ones you don't have.
  - Keys, tempos and energy come from the tags Mixed In Key (or rekordbox, Serato, Traktor) wrote. Sortovia reads them once. After retagging, use **Read keys and tempos again**.

## 1.51 – Play this music on your phone
- **1.51.0**
  - **Play this music on your phone**, in *Library*, lets the Sortovia phone app play and mix the songs in this music library over Wi-Fi. It turns on Kodi's web server with your phone share's password, then shows what to type in the app. If the web server is already on, its settings stay as they are.

## 1.50 – Choose genres for your music
- **1.50.0**
  - **Find genres (dry run)**, in *File*, looks up the tracks you pick on Discogs and Last.fm, then shows a screen of your genres for each artist. Orange came from Discogs, teal from Last.fm, and half of each from both. Genres found on both start on. A filled genre is on, and an outline is off.
  - Your choices are saved, and **Change one track** gives a single track its own genres. The report then shows what each track would get. **This version doesn't change your music files.**
  - Add your Discogs token, Last.fm key and genre list in *Settings > Music genres*.

## 1.49 – Every setting in one place
- **1.49.0**
  - **Every setting is now on Kodi's settings page for Sortovia.** **Settings** in Sortovia's menu opens it. Restart Kodi once if its labels look blank.
  - **Fix music tags** asks whether to choose by **Artist** or **Album**. A quick scan starts from Kodi's own list and reads only what you pick, so a big library doesn't slow it down.
  - Holding down an artist now reads only that artist's music. A new setting in *Music* skips the question.
  - **Set artist art from folders**, in *Library*, uses pictures such as `Music\Artist\artist.jpg` and `fanart.jpg`.
  - If Kodi's picture cache is set to a folder on your drive that doesn't exist, Sortovia creates it.

## 1.48 – Downloads and quicker tag fixes
- **1.48.0**
  - **Downloads** now holds **Transfer and sort**, YouTube and Real-Debrid.
  - **Fix music tags** moves to **File**, because it changes your files, and you can pick whole artists as well as single albums.
  - **Quick scan** doesn't ask your drive about files it already knows, so repeat runs are much faster. **Full scan** checks every file.
  - **Hold down an artist in Kodi's music library** to fix that artist's tags. Restart Kodi once if the option doesn't appear.
  - **Clean the library**, in *Library*, lets you pick TV, Movies or Music.

## 1.47 – A tidier menu
- **1.47.0**
  - **The menu is reorganised:** Sort my downloads, YouTube, Real-Debrid, File, Library, Settings, Help. **File** works on your files, and **Library** works on what Kodi lists.
  - **Organise my folders**, in *File*, replaces the separate tidy items. Tick TV, Movies, Music or Comics.
  - **Library** is split into Video, Music and Backups.
  - **Settings and Help are now separate,** and every setting is in Settings.

## 1.46 – Faster music fixes
- **1.46.0**
  - **Fix music tags** now asks once at the start, then runs tags, rescan, clean-up and album art on one progress bar.
  - **Files that haven't changed aren't read again,** so later runs are faster.
  - **Fixed songs appearing twice after a tag fix.**
  - A track with no year, or a year of 0000, takes its album's year.

## 1.45 – Music tags
- **1.45.5** After a music update, Sortovia checks art only on the albums that need it and shows progress, so the result appears much sooner.
- **1.45.4** **Rescan one album**, in *Kodi library*, brings one album's tag changes into the library without a full scan. **Set album art from folders** now shows progress while it checks your albums.
- **1.45.3** Safer music updates: Sortovia saves a copy of the music library before a rescan, and notices if Kodi can no longer show songs that are still in its database.
- **1.45.1**
  - **Restore the music library**, in *Kodi library*. It puts back a saved copy of Kodi's music library. No music files change.
  - After **Fix music tags**, Sortovia can update Kodi's library for you. It rescans only the folders that changed, removes songs whose files are gone, and sets album art from folders. It stops before removing anything if the library shrank.
  - **Fix music tags** shows progress while it finds your files, and **Check music art** also reports how much is in Kodi's music library.
- **1.45.0**
  - **Fix music tags (MP3)**, in *Kodi library*. It updates tags to ID3v2.4, joins albums Kodi shows as several, and links collaborations to each artist. You see every change first and pick the albums, the audio stays the same, and files stay where they are. You can undo it.
  - **Set album art from folders.** It uses the picture in an album's folder when Kodi shows no art, whatever the picture is called.
  - **Check music art** now shows progress, and clicking twice no longer starts it twice. It also lists albums Kodi shows as more than one.
  - The menu now stays on screen during an update, with no blank flash.

## 1.44 – Music
- **1.44.4** Better artist folders: a song credited to several artists goes under the first one, and an album with a guest on each track stays under its main artist instead of Various Artists. **Check music art** now names any image it finds in an album's folder.
- **1.44.3**
  - **Music already in folders under an artist now stays where it is,** such as `Music\Artist\Singles\2014 - Title\`. Dates at the start of a folder name are no longer mistaken for an artist.
  - **Check music art**, in *Kodi library*. It lists albums with no cover art and compares them with your backup from before a drive letter switch. It changes nothing.
- **1.44.2**
  - **Clean music library**, in *Kodi library*. It removes songs whose files are gone, and won't run while your drive looks missing.
  - The menu now comes back by itself after an update, instead of a blank screen.
  - The drive letter fix says when an up-to-date backup already exists, and doesn't make another. On an Xbox it now tells you how to restart Kodi from the Xbox menu.
- **1.44.1** Better music folders: a folder named after an artist now counts as the artist, not an album, and collaborations stay in that artist's folder.
- **1.44.0**
  - **Sortovia now sorts music.** Songs go to `Music\Artist\Album\03 - Title.mp3`, using the file's own tags, then its folders. Albums by several artists stay together under Various Artists, and cover art goes with the album. Podcasts, audiobooks, recordings and songs with no artist are left where they are. *Tidy my Music folder* sorts music you already have.
  - **The drive letter fix now includes your music library.** If you ran it on 1.43, run it again to bring your music over.

## 1.43 – Drive letter changes
- **1.43.0** **Drive letter changed? Fix the library**, in *Kodi library*. If your drive's letter changes, for example from E: to D:, Sortovia checks your files are on the new letter, saves a library backup for each letter, and points Kodi and Sortovia at the new one. Your shows, watched marks and resume points stay, and no videos are moved. Run it again whenever the letter changes.

## 1.42 – A new look
- **1.42.1** Sortovia's source code is now public at github.com/sortovia/sortovia, and bug reports go there too.
- **1.42.0** **Sortovia has its logo:** on its icon and Kodi backdrop, and in its full-window screens and web pages. Restart Kodi if the old icon still shows.

## 1.41 – YouTube test
- **1.41.0**
  - **The guide now points to the right cookie extension,** cookies.txt 1.0, which is marked for Firefox on Android.

## 1.40 – Easier to read, more options
- **1.40.0**
  - **A full window for messages, and a guide that scrolls slowly by itself**, one line at a time, so you never lose your place. OK pauses, Up and Down move, and Left and Right change the speed. The guide is now split into topics.
  - **Send a problem report to the developer.** Sortovia removes private details from Kodi's log, shows you what's in it, and only uploads it if you agree.
  - **Protect saved passwords and keys with a passcode**, in Settings.
  - **New options in Settings:** sort videos under 50 MB instead of skipping them, and turn renaming movie titles to your language on or off.
  - **Your phone is now a download source,** with steps in the guide for the Android app, Termux and iPhone (experimental).
  - **xbox-share is now kodi-share,** because not everyone has an Xbox. The old command still works.
  - **New folder names:** `SortoviaLogs` and `SortoviaBackups` on the phone, and `_Sortovia temp` on your drive. Earlier logs and phone backups stay in their old folders.
  - Messages say your language instead of English.

## 1.39 – Sortovia
- **1.39.1** **The daily library backup is skipped when nothing has changed**, which saves time and space. *Back up now* always runs.
- **1.39.0**
  - **Sortovia is now called Sortovia.** Your folders, settings and updates carry on as before.
  - **Real-Debrid downloads by itself.** Anything you send to Real-Debrid downloads automatically once it's ready, in the background. If Kodi closes, it carries on the next time you open Sortovia.
  - **My releases.** Add the feed of your own uploads from any site you use, tick releases, and they go to Real-Debrid. No sites are built in.

## 1.38 – Ready for everyone
- **1.38.1** **Settings you can read.** The settings page showed blank labels on the Xbox, so *Help & settings → Settings* is now a plain list in Sortovia's own menu. Select a line to turn it on or off.
- **1.38.0**
  - **A settings page.** Open it from *Help & settings → Settings* or Kodi's *Configure* button. You can turn update checks, the daily library backup, the phone helper and log copying on or off, and set your TMDb key.
  - **The phone is now optional.** The welcome screen asks whether you want to use one, and answering No hides the phone and YouTube options.
  - **No more network searches for a phone you haven't set up.** Sortovia used to look for a phone every time it opened. Now it only looks after you've set one up or when you ask it to.
  - **Messages fit any device**, not just an Xbox, and mention the companion app.
  - **A new guide and web page**, with install steps, a troubleshooting section and a list of what Sortovia connects to. The add-on also has an icon and an MIT licence file.

## 1.37 – Your device, QR sign-in
- **1.37.3** **Copies from the phone are no longer thrown away as "size mismatch (0 vs …)".** When the phone's share was busy, the check of the original's size failed and came back as 0, so a good copy was deleted (the originals were always kept). The size is now asked again after the copy. The companion app's own cause is fixed in app 0.1.5.
- **1.37.2** **Picking a folder on the phone opens the phone's Download folder.** Kodi's folder browser can't open a place that isn't a Kodi source, so it showed the Xbox's list instead. Sortovia now lists the phone's folders itself: pick one to go into it, *Use this folder* to choose it, and Back to go up. This works with kodi-share and the companion app.
- **1.37.1** **An Xbox is detected as an Xbox** (1.37.0 said Windows PC). Kodi's system info on the Xbox only says Windows, so the device model is now read from the top of Kodi's log ("Running on Microsoft Xbox One S"), with the Xbox's network name as a backup check. If you confirmed Windows PC before, it asks once more.
- **1.37.0**
  - **Your device:** Sortovia detects what Kodi runs on (Xbox, Windows, Android, Raspberry Pi/Linux, Mac, Apple TV, LG TV) and asks you to confirm it once, on the welcome screen or at the next start. Steps are fitted to it.
    - New in *Help & settings*: **How to add your folders to Kodi** (on the Xbox, typing the `win-lib://` path; elsewhere, Browse) and **Your device**.
    - On an Xbox, moves don't try to rename first, which never works there.
  - **Real-Debrid sign-in shows a QR code.** Scan it with your phone's camera, and Real-Debrid opens for this sign-in, so you just tap Allow. The code to type at real-debrid.com/device is still shown. The QR code is drawn on the device itself, and nothing is sent to a website.
  - **Free up space** (was "on the Xbox") works on any device.
    - Kodi's own temporary folders are explained: add-on install leftovers, the scraper's cache.
    - The list title says which backup is the newest, and that it's kept.

## 1.36 – One menu entry, backups on the drive
- **1.36.0**
  - **Sortovia shows once in Program add-ons** again (1.34 and 1.35 showed it twice). Opening it still checks for updates and backs up the library first, at most once every 10 minutes.
  - **Library backups are saved on the library drive** (`_Kodi library backups`) and the phone only, not on the Xbox's own storage. Old ones on the Xbox are cleared after the next backup.
    - *Restore a backup* gets the one you pick ready in Kodi's Home folder, because Kodi's Import library can't see the external drive.
    - *Remove old library backups* frees space, always keeping the newest.
  - **Convert .cbr comics:** choose which ones (all are ticked to start). **Cancel stops after the comic being done**, and the menu then offers to carry on with the rest later. Turning pages also lets you choose the comics.

## 1.35 – Real-Debrid, and the Xbox's storage
- **1.35.0**
  - **Real-Debrid:** a new menu category.
    - Sign in with a code on your phone (real-debrid.com/device), then pick from *My torrents*, add a magnet link, unlock a file-host link, or get a recent download again.
    - Files download straight to `E:\Downloads\Real-Debrid` in the background, with progress and Stop at the top of the menu. Then *Sort the Real-Debrid downloads*.
  - **Big temporary files go on the library drive** (`E:\_Sortovia temp`), not the Xbox's own small storage. This covers building .cbz comics and the library backup's export, which also writes every poster and fan art.
    - Turning comic pages failed with "no space left on device" because of this.
  - **Free up space on the Xbox** (*Help & settings*) shows what's using the Xbox's storage and clears leftovers: temporary files, old add-on downloads and older backups. Kodi's artwork cache is shown but kept.
  - Shorter folder-picker titles, so they aren't cut off.

## 1.34 – A tidier menu
- **1.34.1** Fixes and a new clean-up:
  - **Converting .cbr to .cbz works on the Xbox.** The pages were read fine, but copying the finished .cbz onto the drive failed ("copying the .cbz failed"). It now copies through Kodi's own temp folder path.
  - **Clean TV library** (in *Kodi library*) removes episode entries that aren't TV episodes: files in Movies, Tutorials or a set-aside folder (`_Replaced`, `_Unpacked`, `_No English`), or ones also listed as movies. Then Kodi removes entries whose files are gone. Files are never deleted, and a backup is made first.
  - "Remove wrong movie entries" is now **Clean movie library**, and it also lets Kodi remove entries whose files are gone.
- **1.34.0** **The menu is now a Kodi folder list, sorted into categories**, like other add-ons: *Sort my downloads*, *YouTube*, *Tidy my library folders*, *Kodi library* and *Help & settings*. Each entry has a short description. Opening Sortovia still checks for updates and backs up the library first. A sort that's running, or one to resume, shows at the top.
  - **Pause YouTube downloads:** pause one download or all of them in *Downloads*, and carry on later from where they got to.
  - **Tidy my TV folder / Tidy my Movies folder:** puts what's already there into the folders and names Kodi expects. You see the full list first, and nothing is replaced without asking.

## 1.33 – Comics
- **1.33.1** **Remove wrong movie entries:** under *Kodi library* on the start menu. It finds movies that are really TV episodes, for example "Cesium Hollow" left behind after the whole drive was scanned as Movies. It shows the list and removes them all at once. Only the library entries are removed, never the files, and a library backup is made first. The start menu item is now called "Kodi library: back up, restore, remove wrong movies".
  - The Comics "tidy the folder" line no longer names Ironclad. It only ever moves what's out of place.
- **1.33.0** New start menu item: **Comics: tidy folders, convert .cbr to .cbz, turn pages**.
  - **Tidy the folder:** loose comics go into their series folder, and near-duplicate folders like "Ironclad (2)" are merged into "Ironclad". PDFs that an old version filed in Comics (bills, manuals) can be moved to a Documents folder. You see the list first.
  - **Convert .cbr to .cbz:** Kodi opens a .cbz by itself, page by page. A .cbr needs the Archive support add-on to unpack it first, which is slow and sometimes fails. The .cbr is deleted only after the new .cbz checks out. New .cbr comics are converted while sorting (you can turn this off).
  - **Turn pages for a monitor on its side:** each JPEG page gets an orientation tag, so Kodi shows it turned. Nothing is re-encoded, and "Upright" undoes it. Try one comic first.

## 1.32 – Library backup
- **1.32.0** **Back up / restore my Kodi library** on the start menu.
  - A backup holds Kodi's own library export (shows, episodes, movies, watched marks and resume points) plus a copy of Kodi's database file.
  - It's saved on the Xbox (Home folder → Kodi library backups), on your library drive (`_Kodi library backups`) and on the phone (`Download/KodiSorterBackups`). The newest 5 are kept on the Xbox and the drive.
  - It **backs up by itself once a day** when Sortovia opens, in the background. An empty library is never backed up, so a good backup is never pushed out.
  - If the library **suddenly loses half its episodes or movies**, for example after changing a source's content type, it warns you and shows how to put the backup back (Kodi: Settings → Media → Library → Import library).
  - **YouTube search** shows when each video came out and how many views it has. A new menu item, **Search results order**, sorts by best match, newest, most viewed, longest or shortest. Search is also quicker, because it asks YouTube directly.

## 1.31 – YouTube download quality
- **1.31.4** **Downloads and search results fit on screen.** Each entry has two short lines: the title, then its progress or its length and channel. Nothing scrolls, so pressing down moves to the next entry straight away. A failed download has **Show the whole error**.
  - Search asks YouTube for 20 results instead of 25, which saves one slow request. If the phone's internet is very slow, it says so plainly instead of showing a long command.
- **1.31.3** **Opens faster, with a start-up screen.** It shows "Starting... Checking for updates" straight away instead of nothing. The logs go to the phone in the background while it checks for updates, so it's ready a few seconds sooner. **Cancel** skips the update check, and a second click while it's opening is ignored.
- **1.31.2**
  - **Sorting YouTube downloads goes straight to your default folder.** You choose it once, and change it under "Where sorted videos go" in the YouTube menu. Before, it asked every time, because it ignored Xbox drive paths.
  - **No library rescan** when a run only moved tutorials or comics. They aren't in Kodi's library.
  - Titles in the Downloads list no longer show boxes, and "｜｜" becomes " - " instead of "--".
- **1.31.1** Better at YouTube titles:
  - "walkthrough", "webinar", "quick start" and "getting started" count as tutorials.
  - Producer Pal goes to Ableton Live, Claude Desktop to Claude, and "20⧸20" or "2020 software" to 2020 Design.
  - Emoji and the downloader's look-alike characters (⧸ ｜ ：), which show as boxes on the Xbox, are removed from file names.
  - The preview shows names without %20 codes, and a skipped YouTube video gives the real reason instead of "too small".
- **1.31.0** **Download quality** in the YouTube menu: best up to 4K, 1080p (the default), 720p, 480p, or sound only (.m4a). Lower quality makes smaller files and uses less mobile data. The setting is kept on the phone, and each queued video remembers the quality it was queued with.

## 1.30 – Your language
- **1.30.1** Fixes:
  - **Scans crashed** in 1.30.0 (a mistake in the movie-title lookup). Fixed, and a new test now loads every add-on file.
  - **Import cookies now** in the YouTube menu, with a plain message: imported, already have them, or no file found. A note also pops up whenever new cookies are picked up.
  - Downloads YouTube sends in pieces show progress (pieces done, MB) instead of 0%.
  - Hidden folders (like `.adblocker_1dm`) are skipped when scanning.
- **1.30.0** Choose **your language** on the welcome screen or under Help → Your language. You can pick one or use **Kodi's language**.
  - Sortovia keeps videos with audio in that language. Ones without go to `_No Spanish` and so on, or are skipped or deleted as you choose.
  - It keeps subtitles in that language, and names movies by their title in that language (TMDb).
  - Untagged audio tracks only count as English when English is your language.
  - The YouTube cookie guide now explains how to add an extension from its file when **Add to Firefox** is greyed out.

## 1.29 – Companion app ready
- **1.29.1** Fixes from the first run on the Xbox:
  - **Library folders** show where the standard folders are (for example `E:\Movies`).
  - **The guide** no longer breaks sentences across lines.
  - A folder whose videos are already in Kodi's library is no longer reported as "not a Kodi video source".
- **1.29.0** Sortovia also finds the phone when it runs the new **Sortovia companion** Android app instead of kodi-share in Termux.

## Phone setup
- **YouTube helper (Nov 3):** dropped connections ("Did not get any data blocks") retry by themselves, up to 3 times per video, keeping what was already downloaded. Pieces are retried 30 times before that.

- **One-step install for the phone (Nov 2026):** paste one line into Termux. Ubuntu isn't needed any more. It installs the Wi-Fi share, the YouTube downloader and the `kodi-share` command, and keeps the password from an older setup. See the README, section 3.

## 1.28 – Can Kodi read your folder?
- **1.28.1** **Search & download from YouTube** and **Help** are on the start menu from the very first run, so you don't need to sort something first.
- **1.28.0** When you pick an existing TV or Movies folder, Sortovia checks it against Kodi's library:
  - how many videos Kodi already has,
  - whether the folder is a video source with the right content type,
  - which files have names Kodi can't read.

  If anything's wrong, it explains how to fix it and offers to **reorganize the folder into Kodi-style folders**, in place. It shows how many files would move and roughly how long that takes, and the usual preview comes first. Safe choices are used: it asks before replacing anything, skips the audio check, leaves NFOs and subtitles alone, and doesn't change "Same as last time".

## 1.27 – Use your existing library folders
- **1.27.0** Each kind (TV, Movies, Comics, Tutorials) can go into **a folder you already have**, with any name on any drive. You choose them on the welcome screen or under Help → My library folders. Nothing already in them is moved.
  - New files reuse your **existing show, season and movie folders**: *Sams Sandwiches* → your *Sam's Sandwiches*, *Season 01* → your *Season 1*, *Matrix 1999* → your *The Matrix (1999)*.
  - Years must agree, so *Doctor Who (2005)* never lands in *Doctor Who (1963)*.

## 1.26 – Welcome screen and Help
- **1.26.0** First run shows a **welcome screen**:
  - Choose **what to sort** (TV, Movies, Comics, Tutorials). Kinds you leave unticked are skipped and listed in the preview.
  - It offers to show **the guide** (this README) on the TV.
  - New **Help** menu item: the guide, the version history and "what to sort".
  - After each update, a short **what's new** note.

## 1.25 – Download from YouTube
- **1.25.0** New menu item, **Download from YouTube**:
  - Search YouTube or type a link (a video or a playlist) on the Xbox. The phone downloads it into `Download/YouTube` (up to 1080p, in a format the Xbox plays).
  - Uses a `cookies.txt` exported from your signed-in browser.
  - The queue shows live progress. You can stop or retry a download, then sort the finished videos straight into your library.

## 1.23 – 1.24 – Tutorials
- **1.24.0** You can sort straight from a YouTube download folder (NewPipe, Seal and others). A video there that names a known program is filed as a tutorial even without the word "tutorial". Anything else in that folder is left alone instead of being guessed as a movie.
- **1.23.1** Tutorial folders for Ableton Live, Claude Code, OpenClaw and 20/20 Design.
- **1.23.0** Tutorials go to `Tutorials\<program>\` (AutoCAD, Revit, SketchUp, Blender …) with their original names. Short tutorial videos are no longer skipped as samples.

## 1.22 – Quality tags, credits clips, separate audio
- **1.22.4** A separate audio track is only brought along when the video has no English audio of its own.
- **1.22.3** Separate audio tracks (`.mka/.ac3/.eac3/.dts`) go next to their video, so Kodi offers them as an extra track.
- **1.22.2** Opening/ending credits clips with a show name go to Season 00 instead of being skipped.
- **1.22.1** Checks that `.nomedia` files were really written.
- **1.22.0** New NFO choice: movie `.nfo` files with **quality tags** (codec, 10-bit, source, bit rate).

## 1.21 – Cleaner leftovers, English titles
- **1.21.3** `.nomedia` in `_Unpacked`, `_Replaced` and `_No English`, so Kodi's library scan skips them.
- **1.21.2** Exact duplicates of library files and junk files are cleared. URL-style names (`%5b…`) are decoded. Every action is counted in the report.
- **1.21.1** English titles for Russian movie names written in Latin letters (e.g. *Bolshoi Gorod 3* → *Road Deputies 3*).
- **1.21.0** Option to remove empty folders from the source. It now says when movie titles weren't checked, and offers to set up the TMDb key.

## 1.20 – Subtitle languages
- **1.20.1** Shows progress for the steps after the scan (matching subtitles, checking the library).
- **1.20.0** Keep only the subtitle languages you choose. The others are deleted or parked.

## 1.19 – Destination folders
- **1.19.1** Much faster when moving many small files (subtitles).
- **1.19.0** The destination can be the Movies or TV folder itself. The other kinds go to the folders next to it.

## 1.18 – Comics and movie titles
- **1.18.0** Comics go into series folders. Movies named in another language get their English title (TMDb).

## 1.17 – Subtitles
- **1.17.0** Subtitles go to `Subs\` next to their video. Subtitles named only by language are matched to the right video. Release folders that were sorted earlier get tidied up.

## 1.15 – 1.16 – NFO files
- **1.16.1** Clearer warning when the destination is the Movies or TV folder.
- **1.16.0** Release `.nfo` files are used to tell a video's audio language when the file itself doesn't say.
- **1.15.0** Release NFOs become Kodi `.nfo` files (IMDb links). Leftovers are tidied and empty folders removed.

## 1.13 – 1.14 – Library tools
- **1.14.1** View any text or NFO file (old DOS art shows correctly).
- **1.14.0** **Where to watch**: per season, whether a show is on your services, free, or available to buy or rent (TMDb, free key).
- **1.13.0** **Find missing episodes** in your Kodi TV library (TVmaze). The report is saved to the phone.

## 1.12 – Phone and Xbox fixes
- **1.12.10** PDFs and EPUBs only count as comics inside a Comics or Manga folder (no more bills filed as comics).
- **1.12.9** Updates download as soon as they're released.
- **1.12.8** Sends the log when opened during a background move.
- **1.12.7** Guards against picking the TV folder as the destination. Files already in place are left alone.
- **1.12.6** Resume never deletes a finished copy.
- **1.12.5** Sort a drive in place (source = destination).
- **1.12.4** Finds the phone on the hotspot by itself.
- **1.12.3** Asks for the kodi-share password at start-up.
- **1.12.2** Choose **Stop now** or **Stop after this file**.
- **1.12.1** Works with the Xbox's drives, which can't rename files: copies go straight to the final name.
- **1.12.0** Kodi's logs are sent to the phone automatically.

## 1.9 – 1.11 – Background moves and the phone
- **1.11.1** Shows each step after a copy, so a hang can be traced.
- **1.11.0** Progress bar for each file (GB done, speed, time left). You can stop in the middle of a file.
- **1.10.0** Read downloads from the phone over Wi-Fi (kodi-share), or from a USB drive on the phone (FTP).
- **1.9.0** Moves run in the background while Kodi stays usable.

## 1.4 – 1.8 – Self-update, archives, resume
- **1.8.0** Full run report in Kodi's log.
- **1.7.x** OVAs and specials go to Season 00. Videos inside `.zip/.rar/.7z` are unpacked. An unfinished run can be resumed. The last settings are remembered. More reliable update checks. Clearer scan counts.
- **1.5.x** **Checks for updates** on every start and installs them. Notes are listed once per show. Textless openings are skipped.
- **1.4.0** "Scan finished" menu, scan progress, and scans that can be stopped and carried on.

## 1.0 – 1.3 – First versions
- **1.3.1** Version number shown in the dialog titles.
- **1.3.0** Fansub anime names (*Tinman Meadow*, *Paragon*) sort correctly. The add-on and the command-line tool share the same naming rules.
- **1.2.1** First Kodi add-on for the Xbox: TV, Movies and Comics with a preview, English-audio check and duplicate handling.
- Command-line `kodi_sort.py` with tests.
