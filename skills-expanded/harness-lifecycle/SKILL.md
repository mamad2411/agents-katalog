---
name: harness-lifecycle
description: >-
  Clean start and handoff every session — init.sh, progress updates, and a
  restart path. Use when sessions feel chaotic, the next agent can't pick up,
  or init.sh / handoff files need design.
---

# Harness Lifecycle

## What this does for you

- **Every session starts the same way** — read state, run `init.sh`, pick one feature
- **Every session ends cleanly** — progress updated, safe to commit, easy to resume
- **No "where were we?"** — handoff captures blockers, files, and next step

Initialization needs its own phase (Lesson 06). Every session must leave clean state (Lesson 12).

## Full session cycle

```
START
  1. Read AGENTS.md / CLAUDE.md
  2. Run ./init.sh (install + verify + health check)
  3. Read progress.md (what happened last time)
  4. Read feature_list.json (what is next)
  5. git log --oneline -5

SELECT
  6. Pick ONE unfinished feature
  7. status → in_progress

EXECUTE
  8. Implement
  9. Verify (tests, lint, type-check)
  10. If fail → fix → re-verify
  11. If pass → record evidence

WRAP UP
  12. Update progress.md
  13. Update feature_list.json
  14. Document risks/blockers
  15. Commit (only if safe to resume)
  16. Leave a clean restart path
```

## init.sh

Separate initialization phase from feature work:

```bash
#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

echo "==> Syncing dependencies"
npm install  # adapt to project package manager

echo "==> Running baseline verification"
npm test     # adapt commands

echo "==> Startup: npm run dev"
echo "Set RUN_START_COMMAND=1 to launch directly."
```

If init.sh fails → **fix environment, do not implement features**.

## session-handoff.md

Complete when closing long sessions or before switching agents:

```markdown
## Verified now
- What works:
- Verification run:

## Changed this session
- Code:
- Harness/infra:

## Broken or unverified
- Known defects:
- Risks for next session:

## Best next step
- Feature: [id] — [title]
- Done criteria:
- What NOT to change:

## Commands
- Start: ./init.sh
- Verification: ...
- Debug: ...
```

## Clean-state checklist

Before finishing, verify [clean-state-checklist.md](../../templates/clean-state-checklist.md):

- [ ] init.sh works
- [ ] Baseline verification passes
- [ ] Progress updated
- [ ] feature_list reflects reality
- [ ] No half-finished steps left undocumented
- [ ] Next session can continue without manual repair

## Commit rules

Commit when:

- Verification passes (or blocker documented)
- Progress and feature_list updated
- No forgotten temp/debug files

Do not commit when:

- Broken tests undocumented
- Half-finished feature without notes
- init.sh would fail on fresh checkout

## Anti-patterns

- Starting to code without init.sh
- Closing session without updating progress
- Commit with broken baseline
- Generic handoff ("made good progress")

## Templates

- [templates/init.sh](../../templates/init.sh)
- [templates/session-handoff.md](../../templates/session-handoff.md)
- [templates/clean-state-checklist.md](../../templates/clean-state-checklist.md)

## Course reference

- Lesson 06: Why initialization needs its own phase
- Lesson 12: Why every session must leave clean state
- Project 03: Continuity across sessions
