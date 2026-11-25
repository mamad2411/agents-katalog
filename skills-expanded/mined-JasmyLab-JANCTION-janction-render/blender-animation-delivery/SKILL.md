---
name: blender-animation-delivery
description: Gets a Blender animation delivered complete and intact - a 10-frame contiguous test through the final settings, checks for black, corrupt, missing and duplicated frames, re-estimating time from the test, encoding frames to video, and verifying the decoded frame count, resolution, FPS and duration with ffprobe. Use before and after rendering any animation, a turntable or an image sequence, locally or on a render farm.
license: MIT
metadata:
  author: JasmyLab Inc. (https://render.janction.jp)
  version: "0.1.0"
  related-skills: blender-scene-preflight, blender-render-settings, blender-turntable
---

# Blender Animation Delivery

A finished job is not a finished animation. Frames can come back black, half-written, duplicated or missing while every
status says "done". Test a short contiguous run first, verify every frame after, and report numbers.

## Before: a 10-frame contiguous test

1. Preflight the scene (blender-scene-preflight): real frame range, FPS, camera, engine, samples, compositor, motion blur.
2. Render 10 contiguous frames (for example 1-10, or 10 frames around the most complex moment) with the final engine,
   samples, resolution and output path. Not a low-sample preview: problems such as intermittent black frames often
   appear only on the final path.
3. Check the 10 frames with the script below and look at them.
4. Estimate the full render from the measured time per frame, tell the user, and wait for a yes.

A case from production: a Cycles animation came back with intermittent black frames. Switching it to EEVEE removed the
black frames but washed the look out: the wrong trade. The fix that kept the look was to keep Cycles and the original
lighting and materials, turn off motion blur, and bypass the compositor's Glare and Lens Distortion nodes by linking
Render Layers straight to the output. Change one suspected subsystem at a time and re-run the 10-frame test after each.

## After: check every frame (PNG or EXR sequence)

```python
# python check_frames.py <folder> <first> <last>   (needs Pillow: pip install pillow)
import hashlib, re, sys
from pathlib import Path
from PIL import Image, ImageStat

folder, first, last = Path(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
files = {int(m.group(1)): p for p in folder.iterdir() if (m := re.search(r"(\d+)\.(png|jpg|exr)$", p.name, re.I))}
want = range(first, last + 1)
missing = [f for f in want if f not in files]
rows, sizes, hashes = [], set(), {}
for f in want:
    if f not in files:
        continue
    try:
        with Image.open(files[f]) as im:
            im.load()
            sizes.add(im.size)
            luma = ImageStat.Stat(im.convert("L")).mean[0]
    except Exception as exc:
        rows.append((f, None, f"corrupt: {exc}"))
        continue
    h = hashlib.sha1(files[f].read_bytes()).hexdigest()
    rows.append((f, luma, "duplicate of %d" % hashes[h] if h in hashes else ""))
    hashes.setdefault(h, f)

lumas = [l for _, l, _ in rows if l is not None]
median = sorted(lumas)[len(lumas) // 2] if lumas else 0
black = [f for f, l, _ in rows if l is not None and l < 3 and median > 12]   # dark frame in a visible sequence
print(f"expected {len(want)}, found {len(want) - len(missing)}, missing {missing[:20]}")
print(f"sizes {sizes}, median luma {median:.1f}")
print(f"black {black[:20]}")
print("problems", [(f, note) for f, _, note in rows if note][:20])
```

A sequence that is dark on purpose (a fade to black, a night shot) has a low median, so it is not flagged; an isolated
near-black frame inside a visible sequence is. Identical files are flagged as duplicates: fine for a held frame, a bug
if the camera was moving. EXR needs an EXR-capable reader; check those in Blender or convert with ffmpeg.

## Encode frames to video

```bash
ffmpeg -framerate 30 -start_number 1 -i frame_%04d.png -c:v libx264 -pix_fmt yuv420p -crf 18 -movflags +faststart out.mp4
```

Encode from frames rather than rendering straight to MP4: a crash then costs frames, not the whole video. Use the
scene's FPS (`fps / fps_base`), not a default. Odd widths or heights fail with `yuv420p`; scale to even numbers.

## Verify the video

```bash
ffprobe -v error -select_streams v:0 -count_frames \
  -show_entries stream=width,height,r_frame_rate,nb_read_frames -show_entries format=duration -of json out.mp4
ffmpeg -v info -i out.mp4 -vf "blackdetect=d=0:pix_th=0.10" -an -f null - 2>&1 | grep blackdetect
```

`nb_read_frames` is the decoded count (count the frames, do not trust the header). Duration should be frames / FPS.
`blackdetect` lists black stretches with times; any inside a visible shot is a defect.

## Report

```
Asked:      240 frames at 1080p
Scene:      frames 1-200 at 30 fps (told the user before rendering)
Delivered:  200/200 frames, contiguous 1-200, 0 missing, 0 corrupt, 0 black, 0 unexpected duplicates
Video:      1920x1080, 30 fps, 200 decoded frames, 6.667 s
Time:       measured 41 s/frame on the 10-frame test; full render took 2 h 18 min
```

Do not say "done" until fidelity (looks like the approved preview), stability (no black or corrupt frames),
completeness (every frame once), and delivery (decoded properties) all pass.

## With JANCTION Render

Run the 10-frame test as a short `render_final` (frames 1-10) once the user has agreed, then call `render_estimate`
again: the measured time replaces the first guess. Every final carries a delivery check (`report.json`,
`report_sheet.png`); read its verdict, then still verify the downloaded files as above.
