---
name: stickerforge
description: Turns one character image into hundreds of print-ready transparent PNG stickers. Plans concepts, checks duplicates, runs a pilot, batch-generates with Codex image generation or an OpenAI/Gemini key, gates alpha and fake-checkerboard backgrounds, retries failures twice, exports a contact sheet and die-cut notes. Use for sticker packs, character sticker sets, emoji or messenger stickers, print stickers, mascot sticker sheets. Korean triggers - 스티커 만들어, 스티커 팩, 캐릭터 스티커 대량 생성, 이모티콘 스티커, 인쇄용 스티커, 칼선, 스티커 시트, 투명 PNG 스티커, 컨셉 100개.
license: MIT
metadata:
  version: "0.1.0"
  repo: github.com/gongnyang/stickerforge
---

# stickerforge

One reference character in, a gated set of transparent PNG stickers out. Work in a project folder outside this skill folder. Scripts live in `scripts/` and are run, not read. Run `scripts/doctor.py` first; it detects the runtime and stops when image generation is unavailable.

## Invariants

1. Three human checks only: style (A), pilot (B), final (C). No batch run before B.
2. The reference is always the original character image. Generated images are never used as references.
3. Transparent output: ask for `transparent_background=true`, then clean alpha (12 and below to 0, 240 and above to 255). A checkerboard painted into pixels is a fail, not a transparent image.
4. Never add text on top of an image afterwards. A wrong glyph means regenerate.
5. Concepts are compared against the full concept list before generation. Duplicates are dropped.
6. Front model for the Codex path: gpt-6.1-terra at medium effort. Pass the prompt verbatim. No lighter model; quality drops in practice.
7. Collect images by the `thread_id` from `codex exec --json`, never by time window.
8. Resume from `manifest.jsonl`: append one row per state change, the last row for an id wins. Retry limit is 2 per sticker.
9. Concurrency default 8, hard cap 10. A quota or 429 error stops the run and saves the remaining list.
10. Never swap the model silently. Ask first.
11. Delete only your own thread's rollout and empty image folders under `~/.codex`.
12. Real people appear only with their own consent. No mocking of public figures. See `references/s0-intake.md`.

## Stages

| Stage | Output | Reads | Human |
|---|---|---|---|
| S0 Intake and style lock | `spec.json` | `references/s0-intake.md`, `styles/` | A: style and count (`--approve A`) |
| S1 Concepts and duplicate check | concept list | `references/s1-concepts.md` | none |
| S2 Pilot | `pilot_count` trial stickers (default 6) | `references/s2-pilot.md` | B: pilot (`--approve B`) |
| S3 Generate | `out/<id>.png`, manifest rows | `references/s3-generate.md` | none |
| S4 Gates | `passed` rows, `qc/rejected/` | `references/s4-gates.md` | none |
| S5 Retry failures, max 2 | new rows, `qc/failed.md` | `references/s5-retry.md` | report count at limit |
| S6 Final sheet and export | `qc/sheet.jpg`, `export/` | `references/s6-export.md`, `references/print-guide.md` | C: final (`--approve C`) |

Start each stage by reading only its own file. Entry point: `scripts/run.py <project>` runs from S0 and resumes; `--from S3` restarts at a stage; `--status` prints the ledger. It exits 3 at each human check. Exit codes: `run.py --help`. Gate list is whatever is in `scripts/gates/`; this file does not count them.

## When to read what

| Situation | Read |
|---|---|
| Which runtime works, missing key, nested Codex | `references/providers.md` |
| Refusal, quota, garbled glyphs, checkerboard, quality drop | `references/failure-playbook.md` |
| Picking a drawing style | `styles/` (six presets) |
| Writing spec or concept lines | `templates/` |
| Print size, die-cut line, white border, 300 dpi | `references/print-guide.md` |

## Runtime

| Environment | How to run |
|---|---|
| Codex only | Outer `codex exec` with full permission launches the runner (`setsid nohup ... &`) and keeps waiting until it exits; survival after the turn ends is unconfirmed. Or sequential: `run.py <project> --next` and `--ingest`. See `references/providers.md`. |
| Claude Code with Codex installed | Runner spawns `codex exec` per sticker. Claude does orchestration and visual review. |
| Claude Code with `OPENAI_API_KEY` or `GEMINI_API_KEY` | Script-based API provider. Transparency is post-processed and gated. |
| Claude Code, no key, no Codex | Unsupported. `doctor.py` stops with the fix. |

The built-in Codex tool has no size argument. Output is about 1254 to 1536 px. Tell the user the real print size from `references/print-guide.md`; never upscale silently.

## Output contract

Project folder holds `spec.json`, `manifest.jsonl`, `out/`, `qc/`, `export/`. Gates are exit-code scripts (`scripts/gates/README.md`) and are the full check. Visual review by a separate reviewer is a sample, not a guarantee.
