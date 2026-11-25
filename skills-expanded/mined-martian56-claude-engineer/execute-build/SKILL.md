---
name: execute-build
description: Use after the plan is signed off, to drive the autonomous, plan-gated build to completion. Orchestrates per-task implementation, review, and verification in customer-experience-first order, stopping only on genuine blockers.
---

# Execute Build

**Announce at start:** "I'm using claude-engineer:execute-build to drive the autonomous build."

## Iron Law
**Only run after the user signed off on the plan** (`claude-engineer:plan-project`). If there is no
signed-off plan in `docs/plan/`, stop and go back.

## The drive loop
1. **Read state first** (`.claude-engineer/memory.md`, `progress.md`, `current-phase.txt`). Trust them over recollection.
2. **Isolate the workspace** via `superpowers:using-git-worktrees` before writing code.
3. **Work phases in CX-first order** (from the plan): Phase 0 scaffold → 1 design system → 2 frontend → 3 backend → 4 integration → 5 quality/CI/finish. Invoke the matching claude-engineer domain skill for each phase:
   - `project-conventions`, `monorepo-and-tooling`, `docker-dev-environment` (scaffold)
   - `design-system` → `frontend-development` → `backend-development`
   - `testing-and-quality`, `ci-cd-pipeline`
4. **Execute tasks with `superpowers:subagent-driven-development`** - a fresh implementer subagent per task; each task uses `superpowers:test-driven-development`. Use **`superpowers:dispatching-parallel-agents`** for independent workstreams. Fall back to `superpowers:executing-plans` only where subagents are unavailable.
5. **After each task:** update `.claude-engineer/progress.md`; record decisions in `memory.md`.
6. **When something breaks:** `superpowers:systematic-debugging` (root cause before fixes).
7. **Review gate per phase / major feature:** `superpowers:requesting-code-review` + `superpowers:receiving-code-review`.
8. **Before claiming any phase "done":** `superpowers:verification-before-completion` AND run the four gates via `claude-engineer:testing-and-quality`.
9. **Finish:** `claude-engineer:ci-cd-pipeline` then `superpowers:finishing-a-development-branch`.

## Autonomy & stopping
Plan-gated then autonomous: run to completion without check-ins. **Stop only on genuine blockers** -
ambiguous requirements not covered by the brief, a destructive/irreversible action, missing credentials,
or a decision that changes the agreed plan. Surface the blocker crisply with options.

## Red flags - STOP
- Building before reading the ledger → re-read it.
- Re-doing a task already marked done in `progress.md`.
- Marking a phase done without running the four gates.
- Changing the plan unilaterally → that's a blocker; ask.
