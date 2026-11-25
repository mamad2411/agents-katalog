---
name: draw-mascot
description: Redraw a character from reference images as a fully code-drawn mascot (draw.py -> complete sprite pack with poses, 9 lip-sync mouths, eyes and swinging parts). Use when the user uploads or points at character images and wants Claude to create the mascot from them, wants more poses or hand-quality mouths than `make.py create` gives, or wants a new original character designed.
---

# Draw a mascot from reference images

`python make.py create` uses the picture as-is (one pose, engine-drawn mouth). This skill is the full build: you
study the references and write `mascots/<name>/draw.py`, which paints every layer in code, the way
`mascots/sparky/draw.py` (Skia) and `rigs/doodle_rig.py` (PIL rig, baked by `engine/bake.py`) were made.

## 1. Set up

- `python make.py new <name> --refs <image> [<image> ...]` copies the references into `mascots/<name>/refs/`.
  If the user already dropped images there, skip this.
- Read every reference image. Write down: silhouette and proportions (head-to-body ratio), palette as hex codes
  (base, shadow, highlight per material), line weight and colour, eye style, signature features (ears, tail, hair,
  accessories, logo), and what makes it recognisable at phone size.
- Rights: if the references are a character the user owns or made, match it faithfully. If they are someone else's
  trademarked character, design an original mascot inspired by it (different name, colours, details) and say so.

## 2. Pick the approach

- **Skia sprite pack** (`pip install skia-python`), copy the structure of `mascots/sparky/draw.py`: smooth paths,
  gradients, cel shading. Best for creatures, blobs, mascots with simple bodies.
- **PIL rig + bake**: copy the structure of `rigs/bake_doodle.py`: one `render(pose, mouth, eyes)` function and
  `engine.bake.bake()` cuts the mouth and eye layers out by diffing. Best for humanoid characters with arms that move.

## 3. The sprite contract (all layers one canvas, same registration)

- `pose_idle`, `pose_excited`, `pose_point`, `pose_wave_a`, `pose_wave_b`, `pose_shrug`, `pose_think`: body + arms,
  no eyes and no mouth (unless baking, where bake.py handles it).
- `mouth_X` (rest), `mouth_A` (M/B/P closed), `mouth_B` (teeth, K/S/T), `mouth_C` (EH), `mouth_D` (wide AH), `mouth_E`
  (round AO), `mouth_F` (pucker OO), `mouth_G` (teeth on lip F/V), `mouth_H` (tongue up L), optional `mouth_smile`.
- `eyes_open`, `eyes_half`, `eyes_closed`, `eyes_happy`, `eyes_wide`.
- Parts that should swing (ears, tail, antennae) as their own layers, listed in `PARTS` with their pivot.
- Never draw both hands raised over the head in one pose. It reads badly.

## 4. Settings + verify

- Write `mascots/<name>/mascot.py` (copy `mascots/sparky/mascot.py`): CANVAS, FEET, FACE, SCALE, PLACE, PARTS, VOICE,
  STYLE with a saturated dark backdrop that contrasts with the character.
- `python make.py draw <name>` then `python make.py check <name>` and READ `out/<name>/check/model_sheet.png`.
  Compare it side by side with the references and fix proportions, colours, mouths. Repeat until it matches. Do not
  report done before you have looked at the sheet.
- `python make.py video <name> --text "..."`, then `python make.py sheet <name> <take dir> 0.5 2 4` and read it.

## 5. Voice

Suggest a voice that fits: ElevenLabs Voice Design (`python make.py design-voice <name> "<description>"`), Voicebox
(free, local, export a wav and pass `--audio`), or macOS `say` with a `pitch` for testing.
