---
name: video-watermark-removal
description: Use when removing a logo/stamp from video via ffmpeg delogo.
version: 1.0.0
author: Me
license: private
metadata:
  tags: [video, ffmpeg, delogo, watermark]
  related_skills: []
---
# Video Watermark Removal (ffmpeg delogo)

## When to Use
User drops a watermarked video (e.g. OpusClip output): locate the stamp, strip it with ffmpeg delogo, deliver clean file. Only for static stamps on a Timeline — moving logos/graphics need inpainting.

## Procedure
1. Extract 2-3 frames spread across timeline (first, mid, last):
   - `ffmpeg -i in.mp4 -ss 1 -frames:v 1 frame1.png`
   - `ffmpeg -i in.mp4 -ss (mid) -frames:v 1 frame2.png`
   - `ffmpeg -y -sseof -1 -i in.mp4 -frames:v 1 frame3.png`  # last frame from EOF
   (frame extraction prints an image2 no-pattern warning — noise, file still written)
2. Locate watermark in each frame by bright-pixel scan (PIL, convert('RGB'), threshold r>240):
   - scan full frame → bbox → crop around it → rescan for exact bbox
   - stamp MUST be same position on every frame; if it moves/animates, delogo can't fix — say so
3. Run delogo with bbox (origin top-left):
   `ffmpeg -y -i in.mp4 -vf "delogo=x=X:y=Y:w=W:h=H" -c:v libx264 -crf 20 -preset medium -c:a copy out.mp4`
   - always re-encode; crf 20, not 23 (delogo bands at low bitrate)
4. Verify: extract frames post-delogo at same timestamps, rescan bbox region, then vision_analyze to confirm stamp gone.

## Pitfalls
- `crop=w:h:x:y` does NOT erase — it extracts the watermark region as its own tiny frame (output size = stamp size). Use delogo. crop is only a pre-step for measurement, never the fix.
- delogo arg order is `x:y:w:h` (top-left origin), same as crop — NOT w:h:x:y. Check `ffmpeg -h filter=delogo` before writing.
- residual ~100-400 bright px in the stamp bbox post-delogo = normal video content, not watermark remnant. Count alone never proves removal — vision_analyze the region first.
- white logos scan clean at r>240; grey/anti-aliased stamps don't trigger threshold — find bbox by eye/PIL, delogo, verify visually.
- JPEG/opaque pixel data in: convert('RGB') before reading pixels or you get banding artifacts.

## Ceiling
delogo averages surrounding colors — fine on flat backgrounds, smears on detailed video. Upgrade: AI inpaint per-frame or regenerate a clean master. Native ffmpeg wins for static stamps on simple backgrounds.
