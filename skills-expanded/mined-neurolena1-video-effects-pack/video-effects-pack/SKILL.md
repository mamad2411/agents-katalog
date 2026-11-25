---
name: video-effects-pack
description: Adds ready-made effects to a video, alone or stacked (47: glitch, zooms, magazine cover, chat/phone mockups, frames, transitions). Use to add, preview or list video effects, in any language.
license: MIT
compatibility: Needs a sandbox or terminal with Python 3.9+, ffmpeg, numpy, opencv-python and pillow. Works in Claude (claude.ai, Desktop, Claude Code), Codex and Antigravity.
metadata:
  author: NeuroLena
  version: "1.0"
---

# Video Effects Pack

47 video effects for short vertical (9:16) clips: edit presets (glitch, shake, zoom, pixelate, colour swings), intros and transitions, and "scene" effects (magazine cover, AI-chat card, phone mock-up, glowing frame, chart, checklist, headlines, orbiting icons). Everything is rendered locally by `scripts/fx.py` with ffmpeg; no cloud service and no API key.

The user normally talks to you in chat and does **not** use a terminal. You run the commands yourself and hand back the finished file. Command-line use by people is also supported (see README in the repository).

## Language

- Reply in the language the user writes in. Do not switch to English because this file is in English.
- Users may name an effect in any language, by number, or just describe the look ("make it glitchy"). Match it to the closest effect using `references/effects.md` (every effect has a one-line description). English ids and the Russian names shown by `--list` are accepted by `-e` directly; for any other language, translate the request to an id yourself.
- Default on-screen texts are English. `--lang ru` gives Russian defaults for the effects listed in the options table. For any other language, pass the texts explicitly with `--text`, `--items` or `--opt`.
- The bundled font (Inter) covers Latin, Cyrillic and Greek. It has no CJK, Arabic, Hebrew, Thai or Indic glyphs. For those scripts, warn the user that text-based scene effects will show empty boxes and offer the non-text effects instead.

## Workflow

1. **Find the skill folder.** It is the folder that contains this `SKILL.md`. All paths below are relative to it. Call it `$SKILL`.
2. **Check the environment once per session:** `python3 $SKILL/scripts/check_env.py` (on Windows try `python` or `py -3`). It prints OK/MISSING per item and ends with `READY` or `NOT READY`.
   - If everything is already installed it prints `READY`: do nothing more, do not reinstall anything.
   - Missing Python packages: `python3 -m pip install numpy opencv-python-headless pillow` (add `--break-system-packages` if pip refuses on a managed Python). Tell the user what you are installing.
   - Missing Python or ffmpeg on the user's own computer: do not install system software silently. Tell the user what is missing, propose the command for their system and wait for a yes: Windows `winget install Python.Python.3.12` / `winget install Gyan.FFmpeg` (a new terminal may be needed afterwards), macOS `brew install python ffmpeg`, Debian/Ubuntu `sudo apt install python3 python3-pip ffmpeg`. Then run `check_env.py` again.
   - In a sandbox where installing is impossible (no network or no permission), say so plainly and tell the user to run the pack on their own computer (README, "Before you start").
3. **Locate the input video.** Use the file the user attached or named. If you cannot see one, ask for it. Never edit the original: always write a new file.
4. **Choose the effect(s).** If the request is vague, propose 2-3 matching effects from `references/effects.md` in one short message, then continue. If the user wants to browse, show `python3 $SKILL/scripts/fx.py --list` (effects) or `--list-presets` (ready-made combinations). If the user wants several effects ("zoom at 2 s, glitch from 4 s, frame at the end") or a ready-made look, use a plan or a preset (section "Several effects in one render"), not several separate runs: a single pass encodes the video once, so there is no extra quality loss.
5. **Preview first** (fast, first seconds only):
   `python3 $SKILL/scripts/fx.py INPUT.mp4 OUT_preview.mp4 -e EFFECT --preview 3`
   Look at the result if you can (extract a frame with ffmpeg and view it) before the full render.
6. **Render in full** without `--preview`. Typical time is a few minutes for a 6 s 1080x1920 clip. If your tool has a time limit, run the command in the background, write the log to a file and poll it. The script prints `frame N` while working.
7. **Deliver.** Save the result next to the input as `<name>_<effect>.mp4` (or where the user asked) and give it to the user with whatever file-delivery mechanism your platform has (attach / present file / path in the workspace). State the file name and what you applied (effect, start time, duration). Do not paste long command output.
8. If the user wants changes (another moment, shorter, other texts), rerun with new parameters instead of re-explaining.

## Command

```
python3 $SKILL/scripts/fx.py INPUT OUTPUT -e EFFECT [options]
```

`EFFECT` is a number (1-47), an id (`glitch`...), a Russian name, or `all` (renders every effect into a folder; slow, only on request).

| Option | Meaning |
|---|---|
| `--start S` | second at which the effect begins (default 0) |
| `--end E` | second at which a *continuous* effect stops (default: end of the clip) |
| `--duration D` | length of an *intro* effect in seconds; the whole animation is stretched or squeezed proportionally. Recommended range per effect is in `--list`; outside it the script warns on stderr but still applies the value. Continuous effects ignore it |
| `--preview N` | render only the first N seconds |
| `--repeat P` | demo mode: an intro effect repeats with P seconds between plays |
| `--text T` | main text of a scene effect (see "Editable texts" below: what it means depends on the effect) |
| `--items "a,b,c"` | list for scene effects (use `\|` as separator when items contain commas) |
| `--opt key=value` | named setting or text of a scene (repeatable), e.g. `--opt issue="ISSUE 7" --opt barcode=off` |
| `--style S` | colour scheme of the scene effects: `minimal` (default), a name from `scripts/styles/`, or a path to a `.json` file |
| `--lang en\|ru` | language of the default on-screen texts of `magazine`, `growthchart`, `checklist2`, `headlinestorm2`, and of the `--list` descriptions. Other scenes have English defaults only |
| `--face x,y,w,h` | mosaic only: face box as fractions of the frame; default auto-detect |
| `--seed N` | another random pattern (sparkle, vglitch, cursed, formulas) |
| `--crf N` | x264 quality, lower is better (default 17) |

Two kinds of effects:

- **Intro / one-shot** (animation of fixed length, plays once at `--start`): e.g. `dropin`, `quickzoom`, `chat`, `magazine`, `phonemock`. Control length with `--duration`.
- **Continuous** (runs from `--start` to `--end`): e.g. `sparkle`, `vglitch`, `pulse`, `rainbow`. Control the span with `--start` / `--end`.

`--list` marks which is which, with default lengths and allowed ranges.

## Several effects in one render

All effects can be stacked in a single pass (one encode, so no quality loss). Two ways:

**Preset** (a ready-made combination; see `--list-presets`):
```
python3 $SKILL/scripts/fx.py IN.mp4 OUT.mp4 --preset hook
python3 $SKILL/scripts/fx.py IN.mp4 OUT.mp4 --preset cover-story --text "DAILY" --items "NEW|SEASON|10|TIPS"
```
Presets are JSON files in `scripts/presets/`: `hook` (hard push-in with a short glitch burst), `glow-up` (sparkles and a glowing frame), `cover-story` (black-and-white flash, then a magazine cover at 2.2 s), `ai-chat` (clip lands in an AI chat, then a checklist), `party` (colour swing, pulse and sparkles over the whole clip). Their timings are fixed in seconds from the start, so they suit clips of about 5 s or longer; for a different timing copy the file as a plan and edit it. The global `--text`, `--items`, `--opt`, `--style`, `--lang`, `--seed` apply to every effect of the preset.

**Plan** (your own list; write a JSON file and pass `--plan plan.json`):
```json
{"effects": [
  {"effect": "quickzoom", "start": 0.5, "duration": 1.5},
  {"effect": "vglitch", "start": 2, "end": 4},
  {"effect": "magazine", "start": 4, "duration": 2.2, "text": "DAILY",
   "items": ["NEW", "SEASON", "10", "TIPS"], "opt": {"barcode": "off"}}
]}
```
Each entry takes: `effect` (required), `start`, `end`, `duration`, `repeat`, `text`, `items` (string or list), `opt` (object), `style`, `lang`, `seed`, `face`. Anything not set inherits the global command-line `--text/--items/--opt/--style/--lang/--seed`. With `--plan` / `--preset`, the global `--start/--end/--duration/--repeat/--face` are ignored: set them inside the plan.

Rules for stacking:
- Effects are applied in list order, each one on the output of the previous. Put camera effects (zooms, shake, glitch, colour changes) first and overlays (frames, sparkles, scene effects) after them.
- Avoid overlapping two effects that take over the whole frame (for example `magazine` and `phonemock`, or any two scene effects that shrink the video): the second one works on the result of the first and the picture can look cluttered. This combination is not tested; preview it.
- Effects that show other moments of the clip (`pipdelay`, `griddive`, `colorswing`) use the original frames, not the output of earlier effects.
- Preview a plan first (`--preview 5`), then render in full.

## Editable texts of scene effects

Defaults are neutral placeholders. Ask the user for real wording when the effect shows text; do not invent claims about the user's product.

- `magazine` (38): `--text` = masthead. `--items` in order: `line1|line2|number|label|bottom1|bottom2|issue|date`. The same fields by name: `--opt head1=... head2=... big=... biglabel=... sub1=... sub2=... issue=... date=...`. A value of `-` hides that element; `--opt barcode=off` removes the barcode. Texts are upper-cased automatically and fitted to the free space; nothing overlaps the face.
- `chat` (22): `--text` = the user's request message, `--items` = up to 3 lines of the assistant's reply list, `--opt assistant="Name"` = chat title.
- `checklistpop` (24): `--items` = up to 4 entries. `checklist2` (45): `--items` = up to 5 entries, `--text` = card title.
- `headlinestorm` (25), `headlinestorm2` (46): `--items` = headlines (repeated if fewer than strips).
- `growthchart` (35): `--text` = chart title.
- `splitscreen` (37): `--text` = caption on the dividing line. `phonemock2` (47): `--text` = caption above the phone (shown only if given).
- `phonemock` (30): `--text` = the account name shown at the bottom of the phone screen (default `yourname`).

Example:
```
python3 $SKILL/scripts/fx.py in.mp4 out.mp4 -e magazine --start 1 --duration 3 \
  --text "DAILY" --items "NEW SEASON|IS HERE|10|TIPS|Inside: workflow|Gear guide|ISSUE 5|MARCH 2026"
```

## Own colour style

Scene effects use a neutral minimalist palette by default. To use brand colours, copy `scripts/styles/example-brand.json` to a new name, change the HEX values (`paper`, `card`, `ink`, `accent1-3`, `corners`) and pass `--style new-name` (or a full path). Only the fields you want to change are needed. Do not invent a user's brand colours; ask for them.

## Known limits (say them honestly when relevant)

- Designed and checked for vertical 9:16 clips (1080x1920 and scaled-down copies). Other sizes and orientations are accepted but were not tested; layouts of scene effects may not look right.
- Person-aware effects (`formulas`, `orbit`, `papercutout`, `iconsaround`, `greenbg`, `magazine`, ...) use a small bundled segmentation model: edges around hair can be rough, and a clip without a visible person gives weaker results.
- `mosaic` needs a detectable face; otherwise pass `--face`.
- Audio of the input is kept (re-encoded to AAC); effects do not add sound.
- Rendering is CPU-only and not instant; use `--preview` before a full render.
- These are look-alikes of common editor presets implemented from scratch. The pack is not affiliated with or endorsed by any video-editor vendor.

## Troubleshooting

- `NOT READY` from `check_env.py`: follow its MISSING lines (step 2).
- `ffmpeg: not found`: install ffmpeg; on Windows also make sure it is on PATH (new terminal after installing).
- Layout looks off: the input is probably not 9:16; tell the user.
- Effect name not recognised: run `--list` and choose by number.
- Text shows empty boxes: the script's font lacks that alphabet (see Language).
