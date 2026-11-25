# Codex project instructions

`CLAUDE.md` is the canonical project guide shared by Claude and Codex. Before
starting project work, read it completely as UTF-8 and follow it as binding
repository guidance. Also consult the linked `GUIDE.md`, `MANUAL.md`,
`README.md`, or `CHANGELOG.md` when the task calls for that detail.

Read `MEMORY.md` for the latest dated state, `HANDOFF.md` for evidence history,
and `ANALYSIS_KNOWHOW.md` for reusable extraction/verification lessons. Historical
failures and unverified implementation replies are not current validation results.

Keep these Codex-specific agreements in addition to `CLAUDE.md`:

- Preserve Korean text as UTF-8.
- Inspect `git status` before editing and preserve unrelated user changes.
- Keep generated outputs under `out/`; do not commit them.
- Run `python -m unittest discover -s tests -t .` after changing core code.
- Treat the parent `.claude/settings.local.json` as Claude-specific context;
  Codex permissions and approvals are governed by the active Codex session.

## Task-observer activation

At the start of any task-oriented session where tools will be used to produce
deliverables, invoke the `task-observer` skill before beginning work.

When loading any skill, check `skill-observations/log.md` for OPEN observations
tagged to that skill and apply relevant insights to the current work.
