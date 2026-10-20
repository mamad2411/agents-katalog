# Project: ClipForge
AI pipeline that turns long streams/podcasts into captioned vertical clips, plus a local review website (FastAPI + one static page) where Diego approves clips. Used to sell clipping retainers to small creators; also a resume project, so code quality and git history matter.

## Commands
<!-- Agents copy these exactly. -->
- Install: `pip install -r requirements.txt` (needs ffmpeg on PATH; OpenCV must stay < 5)
- Dev server (review website): `CLIPFORGE_ASR=mock CLIPFORGE_HL=mock CLIPFORGE_DETECTOR=haar python -m clipforge.cli serve` → http://localhost:8000
- Tests: `python -m pytest tests/ -q` (offline, mock engines, ~4 min)
- Browser tests (after any server/ or static/ change): `CLIPFORGE_BROWSER_TESTS=1 python -m pytest tests/test_ui_browser.py -q` (~10–15 min)
- Quick tests for one area: `python -m pytest tests/test_server.py -q`
- Lint: `python -m pyflakes clipforge tests`

## Architecture (don't break these)
- `clipforge/<stage>/` = the 7 pipeline modules. Stages talk ONLY through JSON files in the job dir; `manifest.json` is the state machine.
- Every stage is idempotent (re-running a finished stage is a no-op) and verifies its own outputs.
- Engines (ASR / LLM / face detector) are swappable with mock implementations. Tests must never call the real Claude API or download models.
- Website: `clipforge/server/app.py` (API) + `clipforge/server/static/index.html` (UI, vanilla JS, no build step).

## Rules for every agent
- Source of truth: `docs/SPEC.md` (what to build), `docs/features.json` (status), `docs/progress.md` (log). Read the top of progress.md before starting.
- One feature at a time. Stay inside the files your task names.
- A feature is done when its acceptance criteria pass — not when the code "looks right."
- Never edit a test just to make it pass. If a test is wrong, say so and explain why.
- Never read or print secrets (`.env`, `client_secret*.json`, keys, tokens). Never commit video files. Never push, deploy, or publish.
- Only use footage we have rights to; nothing posts to social platforms automatically.
- Keep command output short: pipe long output through `tail -40` or `grep`.
- Search for an existing helper before writing a new one.
- Commit small, with descriptive messages.

## Lessons learned (curated by /retro — max 40 lines)
@docs/LESSONS.md

# Compact instructions
When compacting, keep: current feature id, files changed, failing tests, open review findings, next step.
Drop: full file contents, old command output, exploration that led nowhere.
