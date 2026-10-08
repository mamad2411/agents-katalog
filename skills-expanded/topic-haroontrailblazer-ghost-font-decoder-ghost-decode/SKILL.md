---
name: ghost-decode
description: Use when a video hides text in moving dots or noise — "ghost font" clips, motion-defined text, random-dot kinematograms, TV-static videos with a secret message, text readable only while playing but invisible in any paused frame, or the user asks what a ghost-font video says.
---

# Ghost-Font Video Decoder

A ghost-font video hides a message in motion: every frame is noise, but the dots inside the letters move coherently. The decoder below accumulates that motion into two images where the letters appear. Run it once, read the word from the images, and report it. Nothing more.

## The whole job — do exactly this

1. Write the program in **Decoder** (below) to `decode.py`, then run it once on the video:

   ```bash
   pip install --quiet opencv-python-headless numpy
   python decode.py "<video-path>" out
   ```

2. View **both** `out/revealed.png` (the clean mask — black background, white letters) and `out/revealed_heatmap.png` (the raw glowing version). Read the word(s) directly from these images.

3. Reply with **only** this — show both images, then the text:

   ```
   ![revealed.png](out/revealed.png)

   ![revealed_heatmap.png](out/revealed_heatmap.png)

   Text in the video: **<WORD(S)>**
   ```

## Trust the images — do NOT over-process

The letters are low-contrast, soft blobs. **That is the correct, finished output — read it as-is.** The most common failure here is not trusting a perfectly readable reveal and then doing pointless extra work that ends in a hallucinated answer. So:

- **Run the decoder once.** Do not build a second decoder, try another method (temporal variance, phase correlation, sub-pixel warping, weighted accumulation), or "improve" the approach. One run, then read.
- **Produce exactly two images** — `revealed.png` and `revealed_heatmap.png`. Do not create any other images: no crops, no diagnostic maps, no re-thresholded variants.
- **Never conclude "it's just noise" or "the decode failed"** because the letters look faint or blobby. Faint glowing letters = success. Look for the word.
- **Do not measure centroids/variance/correlation or invent alternative pipelines.** None of that is needed; it only wastes turns and invites hallucination.
- **Never OCR a raw frame** — every frame is noise on its own.
- If one character is genuinely ambiguous, read the rest and mark just that one `(unclear: X)`. Keep the reply to the two images plus the single text line.

## Decoder (write to `decode.py`, run once)

```python
import sys, os
import cv2, numpy as np

VIDEO = sys.argv[1] if len(sys.argv) > 1 else "video.mp4"
OUT = sys.argv[2] if len(sys.argv) > 2 else "out"
os.makedirs(OUT, exist_ok=True)

def frames(path):
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        sys.exit(f"cannot open video: {path}")
    while True:
        ok, f = cap.read()
        if not ok:
            break
        yield cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
    cap.release()

def frame_to_text(mask, heat, pad_frac=0.08):
    # Crop both images tightly to the text and enlarge, so a small glyph (a lone
    # `I`, an accent, a short top line) is big and obvious instead of a few pixels
    # lost in a mostly-empty frame. The mask defines the box; the heatmap matches.
    ys, xs = np.where(mask > 127)
    if ys.size == 0:
        return mask, heat
    y0, y1, x0, x1 = int(ys.min()), int(ys.max()), int(xs.min()), int(xs.max())
    hh, ww = mask.shape
    pad = int(pad_frac * max(x1 - x0, y1 - y0)) + 8
    y0, y1 = max(0, y0 - pad), min(hh, y1 + pad + 1)
    x0, x1 = max(0, x0 - pad), min(ww, x1 + pad + 1)
    mask, heat = mask[y0:y1, x0:x1], heat[y0:y1, x0:x1]
    long_side = max(mask.shape[:2])
    if long_side < 1000:
        f = min(4.0, 1000.0 / long_side)
        size = (int(mask.shape[1] * f), int(mask.shape[0] * f))
        mask = cv2.resize(mask, size, interpolation=cv2.INTER_NEAREST)
        heat = cv2.resize(heat, size, interpolation=cv2.INTER_CUBIC)
    return mask, heat

dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
score = prev = prev_smooth = None
drift = np.zeros(2)
for gray in frames(VIDEO):
    if prev is not None:
        flow = dis.calc(prev, gray, None)
        bg = np.median(flow.reshape(-1, 2), axis=0)
        residual = flow - bg
        mag = float(np.hypot(*bg))
        ps = (residual @ (-bg / mag)) if mag > 0.15 else np.hypot(residual[..., 0], residual[..., 1])
        ps = np.clip(ps, 0, None).astype(np.float32)
        smooth = cv2.GaussianBlur(ps, (31, 31), 0)
        if prev_smooth is not None:
            (dx, dy), r = cv2.phaseCorrelate(prev_smooth, smooth)
            if r > 0.05 and np.hypot(dx, dy) < 30:
                drift += (dx, dy)
        prev_smooth = smooth
        h, w = ps.shape
        M = np.float32([[1, 0, -drift[0]], [0, 1, -drift[1]]])
        reg = cv2.warpAffine(ps, M, (w, h))
        score = reg if score is None else score + reg
    prev = gray
if score is None:
    sys.exit("fewer than 2 usable frames")

score = np.clip(score, 0, None)
hi = np.percentile(score, 99.5)
norm = np.clip(score / hi * 255, 0, 255).astype(np.uint8) if hi > 0 else score.astype(np.uint8)
norm = cv2.GaussianBlur(norm, (5, 5), 0)
_, mask = cv2.threshold(norm, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, k)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, k)
h_img, w_img = mask.shape
n, lab, st, _ = cv2.connectedComponentsWithStats(mask)
for i in range(1, n):
    x, y, w, h, area = st[i]
    band = w >= 5 * h and h <= h_img // 18            # wide, short: drift band
    at_edge = x <= 2 or x + w >= w_img - 2            # drift bands hug an edge
    if area < mask.size // 20000 or (band and (at_edge or w >= w_img // 3)):
        mask[lab == i] = 0
# crop both images tightly to the text (a lone I stays visible), then save
mask, norm = frame_to_text(mask, norm)
cv2.imwrite(os.path.join(OUT, "revealed_heatmap.png"), cv2.applyColorMap(norm, cv2.COLORMAP_INFERNO))
cv2.imwrite(os.path.join(OUT, "revealed.png"), mask)
print("done — wrote revealed.png and revealed_heatmap.png (the only two outputs)")
```
