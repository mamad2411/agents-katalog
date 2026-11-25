---
name: warm-vlog-intro
description: Make a four-second landscape vlog intro with a centered cutout, expanding background montage, reference music and changing vlog fonts. Use for the Warm Vlog Intro preset or this expanding-strip intro style.
---

# Warm Vlog Intro

Create a **16:9 landscape, 30 fps, four-second** intro. The design canvas is 1920×1080; default exports are 3840×2160 and previews are 1280×720. This is a standalone intro preset, separate from the portrait editor and its three talking-head templates.

## Saved look

- A centered moving cutout stays in front of the lettering. Its visible silhouette is 908 px tall at 1080p and touches the bottom edge. Scale uniformly; preserve the requested orientation.
- A thin horizontal montage strip expands vertically and fills all four edges for frames 115–119. Preserve the supplied geometry and rapid cut rhythm. Black outside the growing strip is intentional.
- Lowercase white **vlog** starts at frame 0 behind the subject. Fonts change every **0.3 seconds / 9 frames**: Playfair Display 600, Didot Regular, Helvetica Neue Regular, Didot Italic, Playfair Display 400. The last change is at frame 117.
- Use the user's four-second reference music mix. Mute camera audio. For a new mix, close with a short 40 ms fade rather than an abrupt audio cut.
- Apply `colortemperature=temperature=4160:mix=1:pl=1` once to the entire ungraded composition. This is the saved warm look, not a request to compound the grade each time the preset is reused.
- End at exactly four seconds, before any title card, emojis or talking ending.

## Prepare a local project

Use the project virtual environment. Rendering requires the base requirements plus NumPy; automatic matte preparation additionally requires ONNX Runtime. Install the optional preparation dependencies with:

```sh
.venv/bin/python -m pip install -r requirements-portrait.txt
```

FFmpeg is supplied by `imageio-ffmpeg`; `REELKIT_FFMPEG` can select another build. FFprobe is not required. The renderer also works as an installed personal skill with equivalent Python packages.

```sh
.venv/bin/python SKILL_DIR/scripts/create_project.py .local/my-intro
```

The public package contains code, design geometry, a fill-in project and the OFL Playfair font. It contains no personal footage, reference music, exact reference export, matte caches, model weights or proprietary fonts. Keep those in the ignored project directory.

Fill the new project's `options.json` and `backgrounds.json` with local source paths and selects. Supply:

- `sound.wav`: four seconds, stereo, 48 kHz, ready-mixed music.
- `style.json` → `model_path`: a local MODNet ONNX model if generating new mattes. The repository's existing MODNet cache can be reused; weights are not bundled.
- `style.json` → `font_paths` and `font_indices`: licensed Didot and Helvetica Neue collections. On macOS these may be in `/System/Library/Fonts/`; on other systems provide licensed font files and correct collection indices. Disclose and obtain the user's agreement for a visual substitution; do not silently change the typefaces.

Paths may be absolute or relative to the new project. The placeholder source paths are examples, not included media. See [references/project.md](references/project.md) for source replacement, prepared-cache input and timing details.

```sh
.venv/bin/python SKILL_DIR/scripts/prepare.py --project .local/my-intro
.venv/bin/python SKILL_DIR/scripts/render.py --project .local/my-intro --check
.venv/bin/python SKILL_DIR/scripts/render.py --project .local/my-intro --draft
```

Inspect the actual clips before choosing selects. Review the matte across hair, hands and shoulders; not every selfie or scene separates cleanly. If a prepared cache is supplied, unchanged caches are reused without a model download or inference pass. A personal installation may retain a local reference manifest or approved export; inspect those only when they exist.

## Review and export

For a quick graded composition check:

```sh
.venv/bin/python SKILL_DIR/scripts/render.py --project .local/my-intro \
  --draft --stills --frames 0,30,60,90,119 --name composition-check
```

After reviewing the full draft and listening to its audio:

```sh
.venv/bin/python SKILL_DIR/scripts/render.py --project .local/my-intro
```

`renders/master/` contains H.264 CRF 10/AAC 320k MP4 and ProRes 4444 XQ qscale 1/PCM 24-bit MOV, with stereo 48 kHz audio. `--width` accepts other 16:9 sizes divisible by 32, at least 320. Do not label upscaled smaller footage native 4K.

The renderer checks dimensions, frame count, duration, audio rate and full decoding, writes checksums, and extracts review frames from the encoded video. Existing render folders are not overwritten; use `--name revision-2` for another pass. Deliver the video, editable project and validation. Invoking this skill does not authorize publishing the user's media.
