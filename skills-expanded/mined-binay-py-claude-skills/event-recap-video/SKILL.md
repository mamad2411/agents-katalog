---
name: event-recap-video
description: Turn a pile of phone photos/videos from an event (conference, trip, retreat, wedding) into a hooky recap video with ffmpeg — a 16:9 main cut, a 9:16 version, and a ~45 s beat-synced reel. Use when the user wants a recap/highlight/montage video from their own footage.
---

# Event recap video

Tested end to end on a 780-item event library. Requires `ffmpeg`/`ffprobe` on PATH and Python 3.10+ with `pip install pillow pillow-heif numpy`.

Scripts live next to this file. Copy into the project:
- `scripts/analyze.py`, `build.py`, `reel.py`, `motion.py`, `fonts.py` → project root
- `scripts/work/*.py` → `<project>/work/`
- `examples/*.json` → project root, then edit them

Project layout: `raw/` (untouched originals), `music/`, `work/` (cache), `output/`, `edit.json` (the whole edit).
Fonts are found automatically on Windows/macOS/Linux; override with `FONT_SERIF`, `FONT_SERIF_BOLD`, `FONT_SANS_BOLD`, `FONT_BLACK`, `FONT_EMOJI`, `FONT_DEVANAGARI`.
Title, label and reel lines with Nepali/Hindi (alone or mixed with English) are shaped by ffmpeg one word at a time and overlaid as PNGs with the same fades and outline, because drawtext shapes a whole line in its first letter's script; motion.py stickers and the shortlist use the same helper. Emoji only work in motion.py stickers; build.py and reel.py drop them because ffmpeg draws them as boxes.

## 1. Get media
- Put each export/zip in its own folder under `raw/`. Never modify originals.
- Google Photos has no API for an existing library: drive the user's own logged-in browser over CDP (see the `brave-cdp` skill in this repo). Grid items are `a[href*="/photo/"]`; day headers are `[role=checkbox][aria-label^="Select all photos from"]`.
- Select day headers with REAL mouse events (`Input.dispatchMouseEvent`), verify the `"N selected"` text, press Shift+D. The tab must be in front (`Page.bringToFront`) or the grid stays grey.
- Google clears the selection after a download and header `aria-checked` can go stale; reload before reselecting.
- `Browser.setDownloadBehavior` with `allowAndName` saves the zip under its GUID with no extension; watch `Browser.downloadProgress` for `completed`.

## 2. Analyze and pick
- `python analyze.py` → `work/media.json` (capture time from EXIF / video `creation_time` in local tz, blur, brightness, duplicates, loudness) + per-day contact sheets in `work/sheets/`.
- `python work/vsheets.py` → 3-frame strips per video. LOOK at every sheet. Skip clips that rotate mid-recording, pocket shots and dark night clips.
- `python work/loudest.py ID:seconds ...` finds the loudest window (singing, speech, cheering). Verify with a 1 fps frame strip before trimming.
- Shared/forwarded files have no capture date (falls back to file mtime) — place them by eye.

## 3. Edit (what audiences liked)
- Lead with VIDEO (~90% clips); photos only for strong group shots. Photo-heavy cuts feel slow.
- Cold open hook: 8–10 clips of 1.2–1.8 s, `hook_xf` 0.1 near-hard cuts, then the title card. Then days in order with a small `"label": "Day N · date"` on each day's first clip, 3–4 s cuts, and a few 9–12 s moments flagged `"speech": true` (music ducks under them).
- Music makes or breaks the hook. Chain 2 tracks of similar tempo (`"music": [a, b]`, 3 s crossfade) instead of looping one. `python work/bpm.py file.mp3` estimates tempo.
- `edit.json` keys: `title, subtitle, closing, closing_sub, title_bg / closing_bg` (+ `_bg_at` for video ids), `music` / `vertical_music`, `music_volume, duck_volume, ambient_volume, photo_seconds, hook_xf, closing_seconds, horizontal_hook, horizontal, vertical_hook, vertical`. Segment: `{"id", "at" (0–1 centre) | "start", "dur", "speech", "label", "xf"}`.
- `python work/shortlist.py` → `output/shortlist.jpg` (a frame at every cut). Show it to the user before rendering.

## Make it perform (defaults from docs/video-playbook.md)
- **Hook in the first 1.5 s:** frame 0 already shows the subject plus 3-7 words of hook text (never a black or logo-only first frame). Show the real thing (people, product, the moment) by 3 s.
- **Pace:** something changes on screen at least every 3 s; add a fresh visual + sound at ~40% and ~70% of the runtime. Shorts/Reels: keep it under 45 s unless the content truly holds.
- **Text:** burned-in captions (most people watch muted), 1-3 words per chunk, ≥72 px, heavy weight, 6 px outline. On 9:16 keep all text inside x 65-890, y 250-1440 so the platform's buttons and captions don't cover it.
- **Ending:** one call to action in the last 3 s, end within 1 s of it, and make the last frame match the first so replays loop (YouTube counts replays as views).
- **Audio:** music ducked 18-24 dB under voice; final mix `loudnorm=I=-14:TP=-1:LRA=11`. Only royalty-free music; a Short over 60 s with any Content ID claim is blocked.
- **Export:** H.264 high, yuv420p, CRF 18, keyframe every 0.5 s (`-g fps/2`), `-movflags +faststart`, AAC 48 kHz. Fiverr gig videos: ≤ 75 s, ≤ 50 MB, no contact details.

## Keep it cheap (tokens)
- Review a render with ONE small contact sheet (`ffmpeg -i out.mp4 -vf "fps=10/DURATION,scale=216:-1,tile=5x2" -frames:v 1 sheet.png`), not individual frames.
- Check length, size, fps and loudness with numbers (`ffprobe`, `ebur128`) instead of looking.
- Change the edit/storyboard JSON and re-render; don't rewrite scripts. Don't print ffmpeg logs (`-loglevel error`).

## 4. Render and QC
- `python build.py [horizontal|vertical|vertical-full]` — per-segment cache in `work/seg`, xfade chain, loudnorm −14 LUFS, x264.
- `EDIT=other.json OUT_SUFFIX=-v2 python build.py` renders an alternative edit without touching the main one.
- QC every render: `nb_frames == duration*30` (xfade chains can drop frames), `blackdetect` count 0, ebur128 ≈ −14 LUFS, and a tile sheet of frames (`fps=1/5,tile=8x6`) to eyeball rotation and cut-off titles.
- ffmpeg 7+ prefers `-/filter_complex file` over the deprecated `-filter_complex_script`.

## 5. Beat-synced reel (IG / TikTok / FB) — `reel.py` + `reel.json`
- `python reel.py` → `output/reel.mp4` (~45 s), built on build.py's segment renderer.
- Cuts land exactly on the beat grid (`bpm` hint, auto phase, frame-rounded cut times). Double-check tempo: naive estimators often return half/double (85 vs 154).
- First second = the most surprising moment, with a "POV: …" line. 4-beat cuts, 6–8 beats on hero moments, slow push-in on every clip, white flash on section starts.
- Text: heavy sans, white with thick black outline, ~24% from the top (clear of TikTok/IG buttons), slide-up fade. 5–7 short lines total; the last one is the event name.

## 6. Meme / motion cut — `motion.py` + `motion.json` (only when the user asks for memes/stickers)
- Many people find this style too much for a heartfelt event. Default to sections 3–5.
- One long, steady track (~3 min) instead of chaining; beat grid via comb-filter search.
- Per clip: `beats`, `speed` (0.5 slow-mo / 2 fast-forward), `freeze` (beats; tape-stop + silence + desaturate), `cap` sticker (rounded box, tilt, elastic pop, colour emoji), `day` slam titles + whoosh, `title`, `verse`, `shake`, `punch`, `flash`, `zoom`.
- If a render is killed, delete clip files that fail ffprobe before re-running (the cache would reuse them).

## 7. Vertical and social delivery
- When someone approves the 16:9 edit and asks for 9:16, give them the SAME edit vertical (`python build.py vertical-full`). Don't restyle an approved edit; "make it more attractive" means polish only.
- Platforms (especially Facebook) mute posts with unlicensed music. Offer an original-sound version (an edit with `"music": null`) and/or a silent copy (`ffmpeg -i in.mp4 -an -c copy out.mp4`) so music can be added from the platform's licensed library.
- Final polish: `eq=contrast=1.07:saturation=1.2:gamma=0.97,colorbalance=rm=0.03:bm=-0.03:rh=0.02:bh=-0.02,unsharp=5:5:0.45,vignette=angle=PI/5.5` + audio `highpass=80,dynaudnorm,acompressor,loudnorm=I=-14`.
