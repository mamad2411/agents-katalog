---
name: mascot-video
description: Build a talking mascot from the user's picture as-is (one pose, engine-drawn mouth and blinks) and turn a script into a lip-synced vertical video with this repo. Use when the user wants to create a mascot, add art or a voice to one, fix its mouth position, or make a mascot video from text or audio. For a full redraw with poses from reference images use draw-mascot.
---

# Mascot video

## New mascot from a picture

If `ANTHROPIC_API_KEY` is set, `python make.py create <name> --image <path>` does steps 1-4 itself; then read the
model sheet and go to step 5. Inside Claude Code without a key, do it by hand:

1. `python make.py new <name> --from-image <path>` (lowercase-dash name).
2. `python make.py check <name>`, then read `out/<name>/check/grid.png`. Find the mouth centre and both eye centres
   in the grid's pixel coordinates; sample the skin colour next to the mouth (PIL `getpixel`).
3. Edit `mascots/<name>/mascot.py`: `MOUTH = dict(at=..., width=..., cover=dict(color=<skin>, size=(w, h)))` when the
   picture already has a mouth, `EYES = dict(left=..., right=..., size=(rx, ry), lid=<skin>)` for blinking. Width is
   roughly the drawn mouth's width x 1.1.
4. `python make.py check <name>` again and read `model_sheet.png`: the 9 mouths must sit on the face and fully hide the
   original mouth. Adjust and repeat until they do.
5. Voice: ask which provider (macOS `say` is zero setup; ElevenLabs needs `ELEVENLABS_API_KEY` in `.env`;
   Voicebox / own recording = `VOICE = {"provider": "file"}` + `--audio`). For a new ElevenLabs voice use
   `design-voice`, let the user listen, then `save-voice`.
6. `python make.py video <name> --text "..."`, then `python make.py sheet <name> <take dir> 0.5 2 4` and read the
   sheet before reporting.

## Existing mascot

`python make.py video <name> --text "..."` (or `--script file.txt`, or `--audio file.wav --text "same words"`).
More poses or hand-drawn mouths: see `mascots/_template/README.md` for file names; trigger words live in `TRIGGERS`.

## Fixes

- Mouth too big/small or off-centre: `MOUTH.width` / `MOUTH.at`.
- Old mouth showing through: grow `cover.size` or fix `cover.color`.
- Lip sync feels loose: `bash scripts/install_rhubarb.sh` (the fallback is loudness-only), and pass `--text` with audio.
- Captions wrong words: `pip install openai-whisper`.
