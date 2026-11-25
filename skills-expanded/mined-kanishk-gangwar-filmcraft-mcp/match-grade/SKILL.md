---
name: match-grade
description: Colour-grade an edit to match a reference video's look by measuring it — shadow neutrality, highlight warmth, brightness, saturation — and tuning Lumetri until the numbers line up, plus per-shot corrections by kind of light and gentle handling of noisy night shots. Use it whenever the user says the reference "has a warmth/vibe/filter ours doesn't", asks for a cinematic or film look, a specific colour feel, or complains about grain, washed-out or grey footage in an edit.
---

# Matching a grade

Eyeballing a look ("warm", "teal-orange") usually lands in the wrong place — e.g. a teal preset
when the reference is actually neutral shadows with creamy yellow highlights. Measure both, compare,
adjust, measure again. Two layers: a per-shot correction (balances each clip's light) and one overall
look on an adjustment layer above everything.

`color_stats.py` reports mean RGB in shadows / midtones / highlights, overall brightness and
saturation; with `--ref` and `--ours` it prints which way to move.

## 1. Measure the reference

Use frames of the body (not the intro, not black bars or captions):
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/color_stats.py work/ref --crop 0,112,180,208 --every 6
```
Read it as: shadows R≈G≈B → neutral shadows; highlights with B well below R → warm/creamy; overall
mean → exposure; saturation → how punchy.

## 2. Per-shot correction (by light)

Give each shot a look that fixes its own light before the overall grade (plan `look` field;
presets in recap-edit's build script):
- **haze** (grey sea/sky, overcast): +contrast, lower blacks, -highlights, +vibrance, slightly warm
- **golden** (sunset, sun in frame): -highlights to hold the sun, lift shadows a little
- **green** (forests, tea, waterfalls): +contrast, +vibrance
- **stage / indoor**: moderate contrast; indoor sports +exposure
- **night**: no contrast boost and no shadow lift — they amplify sensor noise; pull blacks down instead,
  add `vr_denoise` 40–50 on the worst shots only. Heavy denoise or a median filter softens the image;
  users notice blur more than grain.
Denoise goes before Lumetri in the effect order.

## 3. Overall look on an adjustment layer

Start from the measurements, e.g. for "neutral shadows, warm creamy highlights, slightly darker":
```json
{"temperature": 2, "contrast": 18, "exposure": -0.2, "blacks": -16, "whites": 18,
 "curve_red": [[0,0],[0.15,0.13],[0.8,0.83],[1,1]],
 "curve_blue": [[0,0.01],[0.15,0.17],[0.45,0.45],[1,0.84]], "vignette_amount": -0.7}
```
Curves let you warm highlights while keeping shadows neutral — temperature alone warms everything.
Skip film grain on footage that is already noisy.

## 4. Compare and iterate

Render frames of the edit (`export_frames(every: 0.2)` or check-render `--keep`), then:
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/color_stats.py --ref work/ref --ref-crop 0,112,180,208 --ours work/edit_frames
```
Apply the advice, re-render frames, compare again. Two or three rounds usually get every zone within a
few levels. Then look at the night shots, faces and skies by eye — numbers can match while skin goes
orange.
