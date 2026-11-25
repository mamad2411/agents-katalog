---
name: jev-lens
description: Legacy. Use only when images (photos, illustrations, screenshots) must reach TypeSafe's Jev (System One) model as text, because the request can't send the `TypeSafe-Danger-Zone-Images` header that lets Jev read images directly. Triggers on "turn this photo into a Jev state", "describe these images for Jev", "decode images for System One", or a Jev project whose decision depends on what a picture shows. Handles 1 to about 100 images; produces a neutral, complete decode and a JSON state, checked against Jev.
---

# Jev Lens

> **Legacy.** Since October 14, 2026, Jev 1.13 and 1.14 read images directly when a request sends the `TypeSafe-Danger-Zone-Images: true` header (TypeSafe's Images page, docs.typesafe.ai/images). Before anything else, ask whether the user's requests can send it. If they can, recommend sending the images to Jev directly and stop: that skips designing the state by description. Run Jev Lens only when they can't, or when they ask for it anyway.

Turns images into a JSON `state` for Jev. In priority order:
1. **An excellent decode:** a complete, accurate, unbiased record of what the image shows.
2. **A very good state:** the JSON object built from the decode.
3. **Questions, used only as instruments** to check that the decode and the state carry what's needed. Question design is out of scope.

The decode is done blind: fresh subagents that see only the cleaned images and a neutral brief, never the goal, the user's questions or their hypothesis. What a person hopes the image shows is the main source of bias, so it never reaches the decoder.

## Phases

| Images | Do | Open |
|---|---|---|
| 1 to 5 | Phase 1 on all of them; that is the whole job | `calibrate.md` |
| 6 to about 100 | Phase 1 on 1 to 3, then Phase 2 on the rest | `calibrate.md`, then `batch.md` |
| Over about 100 | Probably the wrong skill: say it isn't optimized for bulk extraction, and offer to calibrate on a sample so the package is ready for a bulk tool | |

Both phases use `decode-protocol.md` (how decoders are briefed and what they write) and `state-rules.md` (how the state is built). General rules for building with Jev, with their sources: `../shared/jev-rules.md` (shared with Jevaluate).

## Modes

- **Heavy:** 2 blind decoders per calibration image with agreement measured, up to 2 calibration rounds, then an agreement sample and a cascade in the batch.
- **Light:** 1 blind decoder, 1 round, no agreement sample.
- **Default:** Heavy the first time in a new kind of image or goal; Light when reusing a calibrated package that worked.
- With 5 images or fewer, use the default without asking. **With more than 5, always ask,** showing both costs.

## Cost

Each subagent carries a fixed overhead (about 55k tokens in Claude Code) before it reads anything. The figures below are Claude Code measurements; other harnesses differ. Guide for 10 images:

| | Light | Heavy |
|---|---|---|
| Calibration decodes (2 images) | ~60k | ~120k |
| Extra calibration round | none | ~120k |
| Main session (reviews, state, sketch, check) | ~20k | ~35k |
| Batch decode (8 images, 1 subagent) | ~75k | ~75k |
| Agreement sample (3 images) | none | ~65k |
| Cascade on flagged fields | none | ~30k |
| **Total** | **~155k** | **~445k** |

Scale the batch lines by images / 10 per decoder. The Jev API cost is under a cent either way; `jev_check.py` prints it before sending anything.

**Decoder model:** the strongest vision model for calibration and the cascade, a cheaper one for the batch. At intake, ask whether to use the strongest for everything, and show the difference: the batch line costs about the same in tokens but at the stronger model's price.

## Outputs

A run folder next to the images, `<name>-jev-lens/`:

| Path | What |
|---|---|
| `images/`, `manifest.json` | Cleaned copies (metadata stripped, renamed); the manifest maps them back and is never shown to a decoder |
| `package/` | `brief.md`, `template.json`, `decoder-prompt.md`, `examples/`: the calibrated package |
| `decodes/` | Each blind decode (`a/`, `b/`, `batch/`, `sample/`) |
| `agreement.md` | Field-by-field agreement between decoders |
| `inventory/` | The reviewed decode for each calibration image |
| `keep.json`, `left-out.md` | Which fields went into the state, and why the rest didn't |
| `state.json` or `states/` | The state, one per image |
| `questions.json`, `question-sketch.md` | The question sketch (a sketch, not final questions) |
| `jev-check.md` | The Jev check and the field-by-field ranking |
| `report.md` | One page: what was seen, what was uncertain, what was left out and why, the agreement rates, and what drives the answer |

## Requirements

- Python 3.9 or later. `prepare_images.py` and `jev_check.py` declare their packages inline (Pillow; `typesafe-sdk`), so `uv run` installs them; without uv, `pip install pillow typesafe-sdk` and use `python`. The other scripts use only the standard library.
- `TYPESAFE_API_KEY` for the Jev check. Without it, the skill skips the check, says so, and still delivers the decode and state.
- The model ID: `jev-1.13.0` by default; take the current one from https://docs.typesafe.ai/models.
- In Codex, the default sandbox blocks the network and writes outside the workspace: `uv run` installing packages, the Jev check, and a run folder outside the workspace need your approval.

Rating whether a finished Jev project uses Jev well is a different job: the Jevaluate skill. Jev Lens does not need it.
