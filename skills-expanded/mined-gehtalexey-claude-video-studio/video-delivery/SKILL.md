---
name: video-delivery
description: Render, finish and verify the final files of a code-made HyperFrames video — wide 1920×1080, square 1080×1080, 4K 3840×2160 — with CRF 16 picture, AAC 320k audio, ffprobe pass conditions, loudness printout, contact sheets, the phone-size check, upload limits and when to post on LinkedIn. Use when a video is final and needs exporting, re-exporting, checking or preparing for LinkedIn / X / Facebook. Creative work is in video-studio.
---

# Deliver a code-made video

Mechanical work: a small, cheap model can run this without the creative context. Scripts are in
`example/tools/` of this repo.

## Before rendering
- Close other apps (on a 16 GB laptop renders slowed down ~2× when memory was short).
- `npx --yes hyperframes@<version> lint` and `check` must pass for every composition you render
  (`check` silently skips layout audits while lint has errors).
- If music or SFX times changed in `settings.js`: `node tools/sync-audio.mjs` and
  `node tools/sync-audio.mjs square.html`.

## Render (picture at CRF 16), then finish the audio
HyperFrames has no audio-bitrate flag, so each render gets one audio-only pass (picture copied
untouched, AAC 320k 48 kHz stereo, faststart). Never re-encode the picture a second time.
```bash
# wide
npx --yes hyperframes@<version> render --crf 16 --workers 4 --output renders/_wide.mp4
bash tools/finish-audio.sh renders/_wide.mp4 renders/<name>-wide.mp4
# square (its own re-laid-out composition, never a crop)
npx --yes hyperframes@<version> render -c square.html --crf 16 --workers 4 --output renders/_square.mp4
bash tools/finish-audio.sh renders/_square.mp4 renders/<name>-square.mp4
# 4K master of the wide version (2× supersampled; run alone)
npx --yes hyperframes@<version> render --resolution landscape-4k --crf 16 --workers 4 --output renders/_4k.mp4
bash tools/finish-audio.sh renders/_4k.mp4 renders/<name>-4k.mp4
```
Measured on a 45 s, 30 fps video (Intel i5 laptop, 16 GB, `--workers 4`, other apps closed):
square 5m19, 4K 17m57 (217 MB). With 1 worker and a busy machine the wide render took ~15 min.
Closing your normal browser mid-render is safe: HyperFrames uses its own headless Chrome.

## Pass conditions (run, don't assume)
```bash
ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate,pix_fmt,color_space,bit_rate,sample_rate,channels -show_entries format=duration -of compact renders/<file>.mp4
```
- Size 1920×1080 / 1080×1080 / 3840×2160; `r_frame_rate=30/1`; the intended duration ±1 s;
  h264, yuv420p, bt709; exactly one audio stream, aac 48000 Hz stereo, ~300k (AAC at a 320k
  target averages ~300k).
- Loudness printout (per 0.25 s RMS) around deliberate silences, drops and the fade: silence must
  read below about −75 dB, the fade must fall steadily.
- Contact sheet, one frame every 1.5 s, labels matching real frame times:
  `bash tools/contact-sheet.sh renders/<file>.mp4 renders/<file>-contact.jpg`. Look at it:
  nothing cut off at the edges, every scene present.
- Full-size frames at each scene change (+0.15 s): only one scene visible.
- Phone check: watch muted at ~400 px wide. The big words alone must tell the story.
- Compare the final against the approved draft (mean frame difference < ~1 grey level) to prove
  nothing changed between review and render.

## Upload notes (checked October 2026)
- LinkedIn (official): MP4, ≤10 min, ≤5 GB, 192 kbps–30 Mbps, max 4096×2304. Upload natively.
  Square or 4:5 (1080×1350) fills more of the feed than 16:9. Burned-in words; don't rely on sound.
- X: 16:9 or 1:1, under 60 s; keep key text away from the bottom edge.
- Facebook: square or vertical; keep text inside the centre safe zone.
- Never upload the 4K master to social; it is the archive copy.
- When to post (Buffer 4.8M posts, Social Champ 2.6M, Sprout Social): Tue–Thu, 10:00–12:00 in your
  audience's time zone, Wednesday strongest; newer data also favours 15:00–17:00. Where the work
  week is Sunday–Thursday (e.g. Israel), Tuesday or Wednesday morning is mid-week both at home and
  abroad. Your own analytics after 2–3 posts beat any study.
- Posting is the owner's job. An agent never posts on their behalf.
