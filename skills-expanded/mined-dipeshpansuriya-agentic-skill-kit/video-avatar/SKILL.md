---
name: video-avatar
description: "Use when the user wants a cartoon talking-head avatar (hoodie, glasses, teaching pose) and a local screen-record/edit for a video. Not for store preview clips (use goldie) or HeyGen unless he names it."
user-invocable: true
---

# Video avatar (local, no git)

This file is the whole skill. Do not fetch an avatar GitHub tree. Recorder: a **release** binary already on disk, or the OS tool; cut with `ffmpeg`.

Approved video path remains **local ffmpeg**. Hosted talking-head vendors wait for a fresh go.

## 1. Still — lock this look

Match the house avatar: flat vector illustration, not photo, not 3D, not cinematic.

- Short black hair, black rectangular glasses, light stubble, friendly smile
- Light-grey hoodie, drawstrings with a small cyan tip
- One hand raised, index finger up (explaining)
- Cream background with a faint grey dot grid
- Head-and-shoulders, centred, even lighting, no text, no logo, no watermark

Generate the still **outside the repo** (a scratch working tree or the project's asset folder). Git stays text-only: no media files committed. Same character every video: reuse the file; do not invent a new face.

Prompt to reuse (any image tool the user has):

```
Flat vector illustration of a young South Asian man, short black hair,
black rectangular glasses, light stubble, warm smile, light-grey hoodie
with cyan-tipped drawstrings, right index finger raised, cream background
with subtle grey polka dots, even lighting, no text, no watermark.
```

## 2. Record and edit

Prefer the **Recordly release binary** (Windows `.exe` from its GitHub **Releases** page), not a source clone. Features we use: zoom, cursor, webcam overlay, trim, speed, MP4/GIF.

If Recordly is not installed, record with the OS tool already on the machine, then cut with `ffmpeg` on PATH:

```
ffmpeg -i take.mp4 -ss 00:00:01 -t 00:00:21 -c:v libx264 -pix_fmt yuv420p -an out/clip.mp4
```

Keep cuts short (about 20 s works well). Nothing published, nothing uploaded, until the user says go.

## 3. Assemble

1. Avatar still (step 1)
2. Screen recording of the product (step 2)
3. Optional picture-in-picture: avatar in a corner — Recordly overlay, or ffmpeg overlay. No new SaaS without go.

Personal content and product demos follow the same steps; a product demo is recorded from its code root. Output stays in a scratch working tree or a reports folder as a **path**, never a committed media file.
