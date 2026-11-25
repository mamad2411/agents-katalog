---
name: formax-dev-loop-workflow
description: "Use when working on Formax code changes and you need a disciplined dev loop: keep a single mainline task, avoid scope drift, run only targeted tests (no coverage), avoid partial staging (MM), run mandatory review before commit, include an incremental optimization check, and keep commits small and reviewable."
---

# Formax Dev Loop (Mainline Discipline)

## Default loop (repeat per TODO item)

1) **Pick one mainline item** and finish it end-to-end before starting another.
   - If a new idea appears mid-flight, write it down in a backlog note and continue the mainline.

2) **Write/adjust tests first** to lock behavior (when feasible).

3) **Implement** the smallest change that satisfies the item.

4) **Incremental optimization check (required)**
   - After implementation, do a quick pass:
     - Is there newly-dead/unused logic introduced by this increment?
     - Is there a low-risk simplification that reduces branching/duplication?
   - If yes, include a **small** optimization in the same item (no scope drift, no behavior change).
   - If no, explicitly proceed without optimization.

5) **Run only targeted tests** (never `bun run test:coverage` unless explicitly asked).
   - Preferred: `bun run test -- <changed-test-files...>`
   - Helper (repo): `bun run test:changed`
     - Use default (staged only) for the commit you are about to make.
     - Use `bun run test:changed -- --all` only when you intentionally want staged + unstaged + untracked.

6) **Pre-commit hygiene**
   - Avoid partial staging (“MM” state). If needed, check with:
     - `bun run check:partial-stage`
   - Run review before every commit using `AGENTS.md` -> `Review Profile (Single Source of Truth)`.
   - If review returns findings: fix -> re-run targeted tests -> re-run review.

7) **Commit**
   - Keep it small (2–4 files ideally, unless refactor forces more).
   - Prefer one concern per commit (tests + implementation together for that concern).

## Guardrails (Formax-specific)

- Do not fix unrelated failures mid-loop unless they block the mainline.
- If a command would usually be run with pipes/redirections for convenience, prefer running it plain and rely on Formax’s own output truncation/Expand UI.
- Don’t “clean up” formatting/copy/colors/spacing unless explicitly requested or required for parity.

## Quick commands

```bash
# Detect partial staging (“MM”)
bun run check:partial-stage

# Run related tests for staged changes
bun run test:changed -- --dry-run
bun run test:changed

# Include unstaged + untracked (when explicitly intended)
bun run test:changed -- --all

# Required before commit (review profile)
# See AGENTS.md -> "Review Profile (Single Source of Truth)"
```
