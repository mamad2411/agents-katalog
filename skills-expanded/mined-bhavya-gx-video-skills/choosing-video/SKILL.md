---
name: choosing-video
description: Reuse the saved Choosing landscape talking-head edit, with white Playfair headings behind the speaker, pale-yellow bottom subtitles, floating B-roll cards, natural camera colours and a gentle brighter-music transition. Use when the user asks for this saved video template or the Choosing style.
---

# Choosing Video

Recreate this specific **16:9 landscape** style. Its design canvas is 1920×1080 at 30 fps; preview at 960×540 and export from native sources up to 3840×2160. This is a standalone preset, separate from the repository's portrait editor and three portrait templates. Preserve the user's camera framing.

## Saved look

- White **Playfair Display, weight 600** for enlarged headings. Composite every enlarged heading behind a synchronized foreground subject matte, including hair and hands. Reuse the bundled OFL font.
- **Helvetica Neue Medium**, size 51 and tracking −0.752 px at 1080p, for body subtitles. Pale yellow **#FEF9D3**, no outline, black shadow alpha 55/255, 1.5 px downward offset and 1.5 px blur. Helvetica is not bundled; use a licensed local copy. Do not silently substitute it.
- Bottom subtitle baseline **967**, with left/centre/right anchors **143/960/1760**. Anchor each complete phrase once so the phrase does not drift as its words appear. The three columns align left, centre and right respectively.
- Floating rectangular B-roll cards in the saved positions and sizes; muted source audio and three-frame edge fades. No full-screen B-roll. Tie entrances to the new spoken words rather than copying the old timestamps.
- Original camera colours, with only technical HDR-to-SDR conversion where needed. No creative warm grade. Keep the full ending.

Use [assets/style.json](assets/style.json) for measured settings and [assets/card-layouts.json](assets/card-layouts.json) for the actual output card geometry. Geometry is in 1920×1080 design pixels; multiply by export width / 1920. Prefer these output measurements over rescaling the original reference screenshot again.

## Reproduce the saved edit

An installed personal copy may have `assets/local-reference.json`, which points to the retained project and separate voice/music stems. Read it when present. Copy the retained project to the current workspace before editing. Keep its original source/output mapping, word events, placements and audio unless the user requests a change. Use `start_frame` and `end_frame` as authoritative timing; older second-valued annotations can be stale after a trim.

Read any pending changes in the local reference manifest. An unresolved source choice is not a permanent template preference. Confirm a matching source before claiming a requested swap is complete.

## Apply to new footage

Inspect sources and align the actual recorded words. Select good takes, remove dead air without clipping quiet syllables, and use short quiet audio splice fades. Remap the picture, matte, words, cards and music together after every timeline cut. Avoid dissolves that produce a doubled face at talking-head joins.

Choose personal B-roll that shows the speaker and the activity described. Respect the user's prioritized source collections when relevant to the story. Verify the person, outfit, activity and location rather than relying on a filename. Keep raw footage unchanged.

Prepare the project described in [references/project-format.md](references/project-format.md). It contains a clean assembly, an aligned matte, premixed sound, prepared cards and frame-timed JSON. The renderer handles composition, not transcription, automatic source selection, segmentation or sound mixing. Read [references/audio.md](references/audio.md) before preparing a replacement mix.

For new headline copy, provide explicit `parts` with its text, size, tracking and position. The renderer also retains the original title phrases and measured layouts for exact reproduction. Centre the “so / pick / one” stack with clear vertical gaps; align “dream” and its support lines on their common right-side centre. Text is genuinely occluded by the person: inspect hair, hands and shoulders across the whole title interval. For new wording, adjust a layout if essential words become unreadable, while retaining the behind-subject treatment.

## Render and verify

Use Python 3.10+, Pillow and imageio-ffmpeg (the repository's `requirements.txt`). Use the repository virtual environment, or an equivalent environment for an installed personal copy. FFmpeg comes from imageio-ffmpeg.

```sh
python SKILL_DIR/scripts/render.py --project /path/to/prepared-project \
  --width 960 --output /path/to/preview.mp4

python SKILL_DIR/scripts/render.py --project /path/to/prepared-project \
  --width 3840 --output /path/to/master.mp4 \
  --quality-master /path/to/master-ProRes-HQ.mov
```

For frame review, add `--stills-only --still-frames 0 15 30`. Images go to the project's `review/` folder. On a system without the reference Helvetica collection, pass `--body-font /path/to/licensed-font.ttf --body-index 0`; disclose if this changes the face. An alternate Playfair file can be supplied with `--headline-font`.

Review representative frames, the full title/matte motion, card identity and orientation, every cut, audible joins and the music transition. Listen to the result; a decode check is not an audio review. The script rejects overwrites, checks geometry/timing and fully decodes exports before promotion. Measure mixed loudness separately against approximately −15.1 LUFS and a −1.5 dBTP ceiling. Export H.264 CRF12/AAC320k and, when requested, ProRes 422 HQ/PCM24. Do not upscale a smaller assembly and call it native 4K; rebuild from source media.

Deliver the export, editable project, source mapping and validation. Public packages retain instructions, code, geometry and the OFL font. Personal footage, mattes, previews, music and machine-specific paths stay in local storage. Invoking this skill does not authorize publishing media or modifying a GitHub repository.
