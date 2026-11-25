---
name: harness-verification
description: >-
  No more "done" without running tests — mandatory checks before marking
  complete. Use when the agent declares victory too early or init.sh /
  verification commands need setup.
---

# Harness Verification

## What this does for you

- **Done means verified** — tests, lint, and smoke run before marking passing
- **Evidence on record** — commands and results saved in feature list or progress
- **Fix the baseline first** — if `init.sh` fails, no new feature work

Confidence ≠ correctness (Lesson 09). Only a full pipeline run counts as real evidence (Lesson 10).

## Core principle

The agent **cannot** mark a feature as `passing` until:

1. Documented verification commands were executed
2. All passed (or known failures documented as `blocked`)
3. Evidence recorded in `feature_list.json` or `progress.md`

## Verification hierarchy

```
1. Unit tests        → isolated logic
2. Lint / format     → style and static errors
3. Type-check        → type contracts
4. Integration       → connected modules
5. Smoke / E2E       → observable end-to-end flow
```

Document all applicable levels in AGENTS.md. Minimum viable path is `./init.sh`.

## init.sh contract

```bash
#!/usr/bin/env bash
set -euo pipefail
# 1. Install dependencies
# 2. Run baseline verification
# 3. Show startup command (do not launch by default)
```

Rule: **if init.sh fails, do not start new features**. Fix the baseline first.

## Commands in AGENTS.md

Explicit, copy-pasteable format:

```markdown
## Verification

| Level | Command |
|-------|---------|
| Tests | `npm test` |
| Lint | `npm run lint` |
| Types | `npm run typecheck` |
| Full | `./init.sh` |
| Smoke | `npm run test:e2e` |
```

## Correction loop

```
Implement → Run verification → Pass?
  ├── Yes → Record evidence → Mark passing
  └── No → Read error → Fix → Re-run (do not declare done)
```

## Role separation (Project 05)

For critical tasks, separate implementer from verifier:

- Agent A implements
- Agent B (or readonly subagent) reviews against `verification[]` in feature_list
- Use [evaluator-rubric](../../templates/evaluator-rubric.md) as a guide

## Minimum evidence

```json
{
  "evidence": [{
    "date": "2026-06-16",
    "commands": ["npm test", "npm run lint"],
    "result": "pass",
    "output_summary": "42/42 tests, 0 lint errors"
  }]
}
```

## Anti-patterns

- "Looks good" without running tests
- Marking passing with tests skipped
- Changing verification thresholds to force a pass
- Unit tests only when the feature is user-visible (missing smoke/e2e)

## Related skills

- `harness-e2e` — mandatory E2E for user-visible features
- `harness-evaluator` — independent review before marking passing
- `harness-diagnose` — when verification keeps failing

## Templates

- [templates/init.sh](../../templates/init.sh)
- [templates/evaluator-rubric.md](../../templates/evaluator-rubric.md)

## Course reference

- Lesson 09: Why agents declare victory too early
- Lesson 10: Why end-to-end testing changes outcomes
- Project 05: Self-verification and evidence-based Q&A
