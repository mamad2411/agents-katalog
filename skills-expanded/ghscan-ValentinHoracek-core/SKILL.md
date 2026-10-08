---
name: dotnet-solution-architect
type: hero
description: Use when translating a raw .NET/C# feature requirement, including dictated stream-of-consciousness text, all the way through to a merged, tested, reviewed implementation
---

# dotnet-solution-architect

## Overview

Orchestrates a 6-stage pipeline that turns a raw requirement into a merged, tested, reviewed .NET 10/C# feature. Holds pipeline state on disk so an interrupted session can resume without repeating completed stages. Never takes a destructive action (e.g. deleting a worktree) automatically — every failure path pauses and returns control to the user.

## When to Use

- You have a raw requirement (possibly a dictated, unstructured markdown dump) for a .NET/C# feature and want it carried through spec, plan, implementation, verification, and review as one pipeline.
- Not for quick one-off fixes — this is the full pipeline; for something small, use the underlying skills (`superpowers:test-driven-development`, etc.) directly instead.

## Pipeline State

State is tracked in `docs/dotnet-solution-architect/<date>-<slug>-.das-state.json` in the target repo, where `<date>` is `YYYY-MM-DD` (the date Stage 1 started) and `<slug>` is a kebab-case, lowercased slug derived once at Stage 1 from the Goal line of the restructured draft, truncated to 5-6 words. Every other pipeline artifact (`SPEC.md`, `PLAN.md`, `DECISIONS.md`, the three `REVIEW_*.json` files) uses the same `<date>-<slug>-` prefix in the same folder, so distinct feature runs never collide.

```json
{
  "stage": 3,
  "mode": "with-user",
  "slug": "add-refund-api",
  "artifacts": {
    "spec": "docs/dotnet-solution-architect/2026-08-24-add-refund-api-SPEC.md",
    "plan": "docs/dotnet-solution-architect/2026-08-24-add-refund-api-PLAN.md",
    "decisions": "docs/dotnet-solution-architect/2026-08-24-add-refund-api-DECISIONS.md"
  },
  "worktree": "../agent-worktree"
}
```

At the start of every invocation, check `docs/dotnet-solution-architect/` for an existing `*-.das-state.json`. If present, resume from `stage` rather than starting at Stage 1 — the recorded `mode` and `slug` carry forward unchanged; a resumed session never re-asks for mode. If absent, this is a new run: derive `slug` and set `mode` during Stage 1 (see below), then create the state file.

## The 6 Stages

### Stage 1 — Requirements

Determine `mode`: `"automatic"` only if the invocation explicitly asked for automatic/unattended execution (e.g. "...run this automatically", "...don't stop to ask me"); otherwise `"with-user"`. Derive `slug` from the raw input's likely Goal (kebab-case, lowercased, 5-6 words) — refine it once the restructured draft's actual Goal line exists in step below, if it differs materially. Create the state file with `mode`, `slug`, `stage: 1`.

**REQUIRED SUB-SKILL:** Use `core-agentic:dictation-spec-writer` on the raw dictation input, passing `mode` through to it. `dictation-spec-writer` itself hands off to `superpowers:brainstorming` for clarification and confirmation — that inner clarification loop and `brainstorming`'s own hard gate are unaffected by `mode`; only `dictation-spec-writer`'s own confirmation step (see that skill) is mode-conditional.

**Output:** `docs/dotnet-solution-architect/<date>-<slug>-SPEC.md`. Update state: `stage: 2`, `artifacts.spec` to that path.

### Stage 2 — Architecture & Decisions

1. **REQUIRED SUB-SKILL:** Use `superpowers:writing-plans` against the run's `docs/dotnet-solution-architect/<date>-<slug>-SPEC.md` to draft the run's `PLAN.md`.
2. **REQUIRED SUB-SKILL:** Use `core-agentic:decision-recorder` for each significant decision made while drafting the plan, appending to the run's `DECISIONS.md`.
3. **REQUIRED SUB-SKILL:** Use `core-agentic:replan` against the run's `SPEC.md`, `DECISIONS.md`, and the draft `PLAN.md` to do the final review pass and finalize the plan.

**Output:** the run's `PLAN.md`, `DECISIONS.md`. Update state: `stage: 3`, `artifacts.plan` and `artifacts.decisions` to their respective run-prefixed paths.

### Stage 3 — Isolated TDD Implementation

1. **REQUIRED SUB-SKILL:** Use `superpowers:using-git-worktrees` to ensure an isolated worktree exists for this feature — if `worktree` is already recorded in the state file, verify and reuse it, do not create a new one. Record its path in `worktree`.
2. **REQUIRED SUB-SKILL:** Use `superpowers:executing-plans` to walk the run's `PLAN.md` task-by-task inside that worktree, applying `superpowers:test-driven-development`'s red-green-refactor cycle for each task.

**Output:** compiling source and passing tests in the worktree. Update state: `stage: 4`.

### Stage 4 — Hard Verification Gate

**REQUIRED SUB-SKILL:** Use `core-agentic:hard-verification-gate` against the worktree.

- If it reports PASS: stage the full worktree diff (`git add -A` in the worktree) — Stage 5's reviewer skills all read `git diff --staged` and produce nothing meaningful against an empty staging area. Then update state to `stage: 5` and continue.
- If it reports a paused pipeline (its own report of what's still broken): STOP here. Leave `stage: 4` in the state file. Present the report to the user and wait — do not proceed to Stage 5 and do not touch the worktree.

### Stage 5 — Triple Parallel Audit

**REQUIRED SUB-SKILL:** Use `superpowers:dispatching-parallel-agents` to run three concurrent, read-only agents against `git diff --staged` in the worktree (each capped to roughly 2,000 tokens of context: the diff plus the run's `SPEC.md`). Since `SPEC.md` lives in the target repo root, not inside the worktree, the orchestrator passes each dispatched agent the run's `SPEC.md`'s resolved content directly in its prompt rather than a bare filename; the three `REVIEW_*.json` outputs are written alongside the other pipeline artifacts using the run's `<date>-<slug>-` prefix (not inside the worktree):
- One running `core-agentic:reviewer-micro` → `docs/dotnet-solution-architect/<date>-<slug>-REVIEW_MICRO.json`
- One running `core-agentic:reviewer-macro` → `docs/dotnet-solution-architect/<date>-<slug>-REVIEW_MACRO.json`
- One running `core-agentic:reviewer-ops` → `docs/dotnet-solution-architect/<date>-<slug>-REVIEW_OPS.json`

**Output:** the three JSON files. Update state: `stage: 6`.

### Stage 6 — Human Arbitration

1. **REQUIRED SUB-SKILL:** Use `superpowers:receiving-code-review` to consolidate the three run-prefixed `REVIEW_*.json` files into a triage matrix (finding, source reviewer, severity) for the user.
2. If `mode` is `"with-user"`, or any reviewer verdict is `concerns`/`fail`: present the matrix and ask the user to decide per finding (or overall): **Approve & Merge**, or **Fix & Loop**.
3. If `mode` is `"automatic"` and all three reviewer verdicts are `pass`: skip the question, proceed directly to Approve & Merge — but still ask the local/remote/PR merge-method question inside `superpowers:finishing-a-development-branch` either way, since that's an environment/mechanics question, not a safety judgment call.
4. On Approve & Merge (asked or automatic): **REQUIRED SUB-SKILL:** use `superpowers:finishing-a-development-branch` to merge. Delete the `docs/dotnet-solution-architect/<date>-<slug>-.das-state.json` file — the pipeline is complete.
5. If **Fix & Loop**: set `stage: 3` in the state file (same `worktree`, do not re-provision it), pass the specific findings as targeted refactor instructions into Stage 3, and re-enter the pipeline at Stage 3.

## Quick Reference

| Stage | Entry skill(s) | Output |
|---|---|---|
| 1 | `core-agentic:dictation-spec-writer` → `superpowers:brainstorming` | `docs/dotnet-solution-architect/<date>-<slug>-SPEC.md` |
| 2 | `superpowers:writing-plans` → `core-agentic:decision-recorder` → `core-agentic:replan` | run's `PLAN.md`, `DECISIONS.md` (run-prefixed) |
| 3 | `superpowers:using-git-worktrees` → `superpowers:executing-plans` (+ `superpowers:test-driven-development`) | passing tests in worktree |
| 4 | `core-agentic:hard-verification-gate` (→ `superpowers:systematic-debugging` on failure) | PASS + staged diff, or paused report |
| 5 | `superpowers:dispatching-parallel-agents` (`core-agentic:reviewer-micro`, `core-agentic:reviewer-macro`, `core-agentic:reviewer-ops`) | 3× run-prefixed `REVIEW_*.json` |
| 6 | `superpowers:receiving-code-review` → `superpowers:finishing-a-development-branch` | merge, or loop to Stage 3 |

## Common Mistakes

- **Skipping the state file.** Without it, an interrupted session restarts the whole pipeline from Stage 1 instead of resuming.
- **Re-provisioning the worktree on a Stage 3 re-entry from Fix & Loop.** Reuse the existing one recorded in state.
- **Letting Stage 5 run against a failing build.** Stage 4 PASS is a hard prerequisite — never dispatch reviewers otherwise.
- **Forgetting to stage the diff after Stage 4 PASS.** `git diff --staged` is empty until something runs `git add`; no sub-skill in Stages 3–4 does this on its own, so the orchestrator must do it directly as part of Stage 4's PASS path before entering Stage 5.
- **Auto-resolving Stage 6.** The merge-vs-loop decision is only automatic when mode is `"automatic"` and all verdicts pass; in `"with-user"` mode or with any concerns/fails, the user always decides.
