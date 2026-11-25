---
name: steering-push-vs-point
description: >-
  use this when deciding what belongs in always-on AGENTS.md versus on-demand
  skills or docs — push-vs-point rule, prune tests, pointer discipline,
  auto-compact danger
license: MIT
metadata:
  portability: portable
---
# steering push-vs-point

Steer agents across sessions without overloading the context window.
Default: **point**; push only what must apply every turn.

## When

- Writing or pruning a repo's AGENTS.md / CLAUDE.md.
- A rule fires on the wrong tasks, or a needed rule never fires.
- Asking whether something must be always-on or reachable on demand.

## Context load (two costs)
Anything loaded up front is resent on **every model provider request**. You pay (1) tokens and (2) **attention** — extra rules quiet every other rule and nudge toward the dumb zone.

## Push vs point
| | Push | Point |
|---|---|---|
| What | Full rule always in window (AGENTS.md / CLAUDE.md) | Tiny pointer; full text in docs/skill |
| Cost | High every request | Minimal most turns |
| Risk | Rules fire on wrong tasks | Must be discoverable when needed |

## Steps
1. **Push** only short rules that are both factually true of the repo **and** binding across tasks — true-but-rarely-relevant trivia gets pointed, not pushed.
2. **Point** for situational playbooks: one line in AGENTS.md → `docs/...` or a skill. Write those pointers well; **test after a clear**.
3. Package repeated pointers as **skills** (portable; model-invoked or user-invoked with `disable-model-invocation` for zero description load).
4. Add **navigation pointers** near code; watch staleness.
5. **Prune** with three tests — delete if it fails: **single source of truth**, **sediment** (once-true now-false), **no-ops** (change nothing). Method: delete-then-see.
   - Examples: "This file provides guidance…" preamble = **no-op**; generic "write unit tests" / formatting rules the model already knows = **assumed-knowledge no-op**; full `app/routes|services|components` directory listing or every npm script table = **sediment/SSOT** (filesystem/`package.json` already owns it) — keep only non-obvious highways (e.g. `scripts/seed.ts` outside `app/`).
6. Audit automatic memory like AGENTS.md.

## Anti-patterns
- Novel essays in AGENTS.md
- Duplicate rules in three places
- Secrets in steering files
- A pointer that names no discoverable target
- Pushing rules the model already knows (assumed-knowledge no-ops)

## User vs project
Personal taste (tone, formatting, pet habits) belongs in **user-level** skills, loaded everywhere. Team conventions (repo norms, stack rules) belong in **project skills**, committed in the repo.

## Auto-compaction
Do **not** believe auto-compaction makes phase discipline unnecessary. Mid-phase auto-compact is **dangerous**. Keep explicit clear/compact/handoff/subagent boundaries.

## Related
session-hygiene · kill-context-bloat · handoff
