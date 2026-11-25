---
name: forge-setup
description: Set up the forge dev environment from a fresh clone and verify it with forge doctor. Use when the repo was just cloned, the venv is missing, or tests/lint must be validated before work.
---

# forge-setup: dev environment + verification

1. Check prerequisites: `python3 --version` (need 3.13+) and `uv --version`.
   If missing, install uv via the official installer; use the system Python
   3.13+ (pyenv/homebrew acceptable).
2. `uv sync` from the repository root.
3. Verify: `set -o pipefail && .venv/bin/python -m pytest -q` — expect ~815
   passed, 1 skipped, 3 xfailed (xfails are pinned upstream defects; never
   unpin them casually).
4. Lint: `.venv/bin/ruff format . && .venv/bin/ruff check src tests`.
5. Final gate: `uv run python -m forge.doctor` — exit code 0. Without a
   `.env`, the service checks (gitlab/redis/database/litellm) may WARN or
   FAIL; that is expected for a pure-dev clone. What must pass: unit suite
   and lint. If the user provides a `.env`, `forge doctor` should go fully
   green (`--project <id>` adds target-project checks).

Report: test counts, lint status, doctor output. Do not commit anything.
