---
name: inspect
description: Rebuild a clear picture of project state (active task, gaps, next step) before resuming or when things feel confusing.
---

# Inspect

Use this skill to show the current project state, not to write business code.

## Read

Start with the compact projections:

```bash
python .coderail/coderail.py inspect --no-write
python .coderail/coderail.py progress-view
python .coderail/coderail.py knowledge query "relevant term"
```

Only open the indexed source snippets needed to resolve a diagnostic. For a
full recovery audit, the underlying authorities remain:

- `docs/NORTH_STAR.md`
- `docs/TASKS.md`
- `docs/CONTRACTS.md`
- `docs/TRACELOG.jsonl`
- `docs/TRACE_INDEX.md`
- `docs/HANDOFF.md`
- `git status`

## Action

Run:

```bash
python .coderail/coderail.py inspect --no-write
```

This is the Agent Blackboard. If scripts are unavailable, reconstruct the same
agent-only sections:

- Current North Star
- Active Coordinate
- Active Tasks
- Draft Contracts
- Verification Gaps
- Trace Gaps
- Handoff State
- Recommended Next Action
- Auto Commit

For an owner-facing product summary, run the separate read-only command:

```bash
python .coderail/coderail.py owner-summary --locale zh-CN
```

## Rules

- `docs/CODERAIL_STATUS.md` is the generated Agent Blackboard.
- Do not treat inspect output as a new source of truth; it summarizes existing project files.
- Do not infer verified product capability from NORTH_STAR or render Inspect as an Owner Receipt.
- Preview projection changes with `sync-projections`; only explicit `--apply` writes them.
- Progress checkboxes are evidence projections: implementation, machine
  verification, and human acceptance stay separate, and stale evidence unchecks.
- `knowledge query` distinguishes source facts, confirmed decisions, drafts,
  stale regions, and missing sources without making ordinary staleness global.
- If inspect finds verification gaps, run `/coderail:done-gate` before marking done.
- If inspect finds orphan tasks or trace gaps, run `/coderail:link` or `/coderail:trace`.
