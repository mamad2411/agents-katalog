---
name: harness-state
description: >-
  Pick up where the last session left off — feature list, progress log, and
  evidence on disk. Use when context is lost between sessions or long tasks
  need continuity across days.
---

# Harness State

## What this does for you

- **Memory that survives chat** — progress and status in files, not context window
- **Clear next step** — highest-priority unfinished feature is obvious
- **Proof of done** — evidence recorded before marking a feature passing

Long tasks lose continuity if state lives only in chat (Lesson 05). Persist progress on disk so the next session resumes exactly where the last one stopped.

## State artifacts

| File | Role | Update when |
|------|------|-------------|
| `feature_list.json` | Source of truth for features | Status changes or evidence is added |
| `progress.md` / `claude-progress.md` | Session log | At start (read) and close (write) |
| `session-handoff.md` | Compact handoff | When closing long sessions |
| Git log | Change history | Descriptive commits |

## feature_list.json rules

```json
{
  "rules": {
    "single_active_feature": true,
    "passing_requires_evidence": true,
    "do_not_skip_verification": true
  }
}
```

Valid statuses:

- `not_started` — no work yet
- `in_progress` — active feature (only one)
- `blocked` — blocker documented in `notes`
- `passing` — verification run + evidence in `evidence[]`

## Evidence format

```json
"evidence": [
  {
    "date": "2026-06-16",
    "verification_run": "npm test && npm run lint",
    "result": "pass",
    "notes": "42 tests passed, 0 lint errors"
  }
]
```

Do not mark `passing` without an entry in `evidence`.

## progress.md structure

```markdown
# Progress Log

## Current State
- Active feature: [id] — [title]
- Last verification: [command] — [pass/fail]
- Blockers: [none | description]

## Session History

### YYYY-MM-DD — [brief title]
- Worked on: ...
- Verification: ...
- Next: ...
```

## Multi-session flow

**Session start:**
1. Read `progress.md` → most recent verified state
2. Read `feature_list.json` → highest-priority unfinished feature
3. `git log --oneline -5` → recent changes
4. `./init.sh` → confirm healthy baseline

**Session end:**
1. Update `progress.md` with what was done and what remains
2. Update `feature_list.json` (status + evidence)
3. Optional: complete `session-handoff.md`
4. Commit if the repo is restartable

## Anti-patterns

- Relying on chat memory
- Marking features done without evidence
- Leaving multiple features as `in_progress`
- Aspirational progress ("almost done") vs verified

## Templates

- [templates/progress.md](../../templates/progress.md)
- [templates/session-handoff.md](../../templates/session-handoff.md)
- [templates/feature-list.json](../../templates/feature-list.json)

## Course reference

- Lesson 05: Why long tasks lose continuity
- Project 03: Continuity across sessions
