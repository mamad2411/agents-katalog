---
name: polytropos-execute
description: Run a polytropos execution kit (PLAN.md + TASKS.md) from Cursor through the headless CLI driver — one task per invocation, verified by the task's own command, recorded in the attempt ledger. Use when the user asks to execute, continue, or resume a kit from Cursor. Not for planning a kit.
---

# polytropos-execute (Cursor)

polytropos lives at `{{POLYTROPOS_ROOT}}` (resolved when this skill was installed; if the
path below does not exist, reinstall with `python3 bin/cursor_adapter.py install --project .`
from the polytropos checkout).

The driver is `python3 {{POLYTROPOS_ROOT}}/bin/cursor_execute.py`. It runs one task of a kit
through `agent -p`, runs the task's verify command itself inside the execution boundary,
writes the task's status and NOTES.md outcome line, and records every dispatch before and
after it runs in the attempt ledger. It never plans a kit; that is the architect skill of
whichever harness planned it.

```bash
python3 {{POLYTROPOS_ROOT}}/bin/cursor_execute.py probe                       # is `agent` Cursor? read-only
python3 {{POLYTROPOS_ROOT}}/bin/cursor_execute.py status --kit .claude/kits/<slug>
python3 {{POLYTROPOS_ROOT}}/bin/cursor_execute.py run --kit .claude/kits/<slug> --dry-run
python3 {{POLYTROPOS_ROOT}}/bin/cursor_execute.py run --kit .claude/kits/<slug> [--task <id>] [--model <id>]
python3 {{POLYTROPOS_ROOT}}/bin/cursor_execute.py review --kit .claude/kits/<slug> --phase <N>
```

Rules the driver enforces, so state them rather than working around them:

- **Identity first.** `agent` is a generic name; the driver asks it `--version` (then
  `about --format json`) and dispatches only when the answer names Cursor. Anything else
  exits 2 with nothing written. Point `--cursor-bin` at the real CLI if it is not on PATH.
- **A real run spends.** `--dry-run` prints the exact `agent -p` argv and spawns nothing.
  Without it the task's brief is sent to Cursor under your account; there is no cost figure,
  because the CLI reports none — the outcome line says `usd: null`.
- **The model is yours to name or leave.** `--model <id>` passes `--model`; a task's own
  `model:` pin is passed as written; neither resolves through a price list, because
  `data/pricing.cursor.json` records none. `agent models` lists what your account offers.
- **Verification is the driver's.** The verify command runs through polytropos's execution
  boundary, never through Cursor; a pass marks the task `done`, a failure `blocked`.
- **Review is read-only.** `review` dispatches with `--mode ask`, never `--force`.
- **Kits declare rosters.** A `roles:` line naming a role this driver cannot sequence stops
  the run and says so (`--roster-gap disclose` to proceed with the gap recorded).

Cursor also discovers `.claude/agents` and `.claude/skills` in this project. Those files may
carry another harness's commands; `python3 {{POLYTROPOS_ROOT}}/bin/cursor_adapter.py doctor
--project .` names them. Do not run a command from one of those files as if it were yours.
