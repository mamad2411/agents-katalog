---
name: select-shots
description: Review every clip in a footage folder and pick the most cinematic moments — sample stills from each clip, score sharpness, shake, exposure and colour, find each clip's steadiest window, judge framing (keeping heads in when portrait footage fills a landscape frame) and make sure every clip gets used. Use it before cutting any montage, recap, highlight or travel video from a folder of clips, whenever the user says "use the best shots", "make it cinematic", "you missed some of my videos", or complains a shot is shaky, blurry, too dark or too close.
---

# Selecting shots

People remember their own footage. Two complaints come up again and again: "my best clip isn't in
it" and "why that moment?" (shaky, blurry, head cut off, a selfie blown up to fill the screen). Review
all the footage, every time, before planning the cut. Scripts need Pillow and
`FILMCRAFT_CLI="${user_config.filmcraft_cli}"`.

## 1. Sample every clip

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/sample_clips.py <clips folder> work/samples --every 0.5 --skip recap
```
Stills every 0.5 s (long clips sparser), plus `clips.json` with each clip's length, size, fps and
whether it's portrait. Re-run it when the user adds clips — then diff against what the plan uses.

## 2. Score

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/score_frames.py work/samples --window 1.0
```
Per clip: steadiest+sharpest window for a shot of `--window` seconds, median sharpness, motion
(high = shake or fast pan), brightness, and flags: dark, washed, shaky, soft, grey. Treat these as
pointers, not verdicts — a dark cave with a shaft of light, or a fast bike ride, can be the best shot.

## 3. Look

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/review_sheets.py work/samples work/review --aspect 16:9
```
One block per clip, every still labelled with its time; on clips of a different shape a magenta box
shows the slice that fills the frame when centred. Read every sheet. For each clip note:
- best moment(s) and why (light, gesture, action peak — a smash, a jump, arms opening at sunset)
- for portrait clips in a landscape edit: the **focus height** that keeps the subject in the slice
  (people: usually 0.3–0.45 so heads stay in; render a frame to confirm)
- whether it can fill the frame at all: selfies, tight close-ups and low-res (720p) portrait clips look
  "very zoomed" full-frame — plan them as whole pictures in an overlay section instead
- low light that will need denoising, 24 fps clips that need frame blending
- clips filmed upside down / sideways (rotate them)

For a promising moment, look closer at 0.1 s steps with `export_frames(item, times)` — e.g. to land
exactly on a smash or a jump.

## 4. Choose

- Holds (2–3.5 s) get the most cinematic, steadiest shots; half-beat bursts (0.35–0.45 s) can take
  busier moments; one hero shot per section.
- Use every clip at least once; repeat only long clips, at clearly different moments.
- Prefer wide/medium shots full-frame; save close-ups for overlays.
- Keep a table: clip → moment → slot → focus → look. It becomes the plan.
