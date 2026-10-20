---
name: deep-review-ship
description: Pre-ship deep review — fan out subagents per part, fix findings, re-verify, report ship readiness
argument-hint: "[scope] [--diff]"
triggers:
  - user
  - model
related:
  - deep-thinking
  - deep-analyze
  - use-subagents
  - deep-review-codebase
  - deep-review-codebase-then-fix
  - follow-parallel
  - report-review
  - deep-validate
  - run-check
  - ship
  - suggest-next-action
---

## Goal

Review the changed scope the way it will actually ship: split it into parts (workspace/module/layer), send one review subagent per part via `/use-subagents`, aggregate the findings, route the fixes, re-verify until clean, and hand over a ship-ready scope to `/ship`

## Scope

- Use before any ship when the change spans several workspaces/modules/layers — one deep review pass per part in parallel instead of a single serial sweep
- Thin pre-ship orchestrator: this skill reviews and fixes; it never commits, pushes, opens PRs, or merges — `/ship` owns every ship gate
- Called from `/ship` step 2 → stop at the ship-readiness report and return control to `/ship` (never re-enter `/ship`)
- Standalone use → finish with `/ship` when the verdict is `ready-for-ship`
- One dimension only, no per-part fan-out → `/deep-review-codebase` directly; no findings to fix → skip step 5

## Execute

### 1. Think

> Goal: know what is being shipped and which parts exist

1. Run `/deep-thinking` on the change — what artifact types are in scope (code, docs, config, skills), which risks apply to each
2. Resolve the scope: `[scope]` argument limits it; default = files changed in this session / `git diff` (+ untracked new files); `--diff` forces diff-only scope
3. Run `/deep-analyze` for structure/dependency evidence over the scope — which workspaces/modules the changes actually touch

### 2. Partition Into Parts

> Goal: disjoint parts that review in parallel without collisions

1. Split the scope into parts — one part per workspace, module, or layer (a part may be one folder or one logical change set)
2. Partition per `/use-subagents` step 2: file sets disjoint (`∪Sᵢ = scope`, `Sᵢ ∩ Sⱼ = ∅`); inter-part dependencies form a DAG → waves; cycle → merge those parts
3. Budget: ≤ 10 parts per run; over budget → highest-risk parts first, record `skipped (budget)` with the reason in the report
4. Track every part with a todo — part, file set, status — from spawn to done

### 3. Fan Out Review Subagents

> Goal: one reviewer per part, full coverage, disjoint context

1. Use `/use-subagents` — spawn the `part-reviewer` profile (see `## Subagents`) per part in parallel (`is_background=true`), one wave at a time per the DAG; independent batches ≤ 10 via `/follow-parallel`
2. Each subagent runs `/deep-review-codebase` limited to its own file set with `--diff` — report-only contract, never edits code
3. Pass complete context in the prompt: part path, in-scope files, project `AGENTS.md` conventions, step 1 evidence
4. A part with ≤ 2 changed files → the parent reviews it itself instead of spawning — mark it `covered-manually`
5. Subagent timeout/error → `/resolve-errors`, retry once; still failing → mark the part `failed` and carry it into the report — never silently drop a part

### 4. Aggregate Findings

> Goal: one deduplicated, severity-ordered picture across all parts

1. Collect every part-reviewer output; dedup by `file + rule` keeping the highest severity with combined evidence
2. No findings in any part → jump to step 6
3. Present the findings with `/report-review` — one table: `No. | Finding | Evidence (file:line) | Severity | Part | Owner skill`

### 5. Fix Per Part

> Goal: findings are fixed by the canonical fixer, part by part

1. Ask the user to confirm the fix list (`/ask-me`), except `dont-ask-me` mode → fix all Critical/High by safe default
2. Run `/deep-review-codebase-then-fix` per part with the confirmed findings; parts with disjoint file sets → parallel `fix-worker` subagents via `/use-subagents`
3. Mechanically enforceable or convention findings → persist per `/deep-review-codebase` step 5 (`/update-devin-project-rules`, `/update-astgrep-rules`) so they cannot silently recur

### 6. Re-Verify

> Goal: the fixed scope is provably clean

1. Re-run step 3 for the fixed parts only (`--diff`, never a full rescan); loop ≤ 3 rounds — still failing → stop and report `blocked` with the surviving findings
2. Run `/run-check` and `/deep-validate` across the whole scope — both must pass

### 7. Report Ship Readiness

> Goal: a verifiable verdict — ship or not

1. Run `/report` — table: `Part | Files | Findings | Fixed | Status (done/skipped/failed)` + verdict `ready-for-ship` / `blocked (reasons)` + coverage note (every part reviewed, manually covered, failed, or skipped with reason)
2. Called from `/ship` → return the verdict to the `/ship` flow and stop — this skill never pushes or merges
3. Standalone use → if `ready-for-ship`, run `/ship` to take it to production
4. Run `/suggest-next-action`

## Subagents

### part-reviewer

- Inputs: `part-path`, `files-in-scope` (disjoint list), `findings-slice?`, `conventions` (workspace `AGENTS.md` paths), `scope-mode` (`--diff` default)
- Tools: read, grep, glob, exec (read-only commands), skill
- Execute: run `/deep-review-codebase` limited to `files-in-scope` — read the slice and every evidence file named; never rerun the CLI outside the part, never sweep the codebase, never edit anything
- Output: findings table (`No. | Finding | Severity | Evidence file:line | Action | Owner skill`) + a one-paragraph part summary + `part-status` (`clean` / `findings` / `failed (reason)`)
- Constraints: report-only; read only its own file set + evidence-named files; one part per subagent, no shared mutable state

## Rules

- `/ship` owns commit/push/PR/merge — this skill never performs them; when invoked from `/ship`, return the verdict instead of chaining back (no recursion)
- Review subagents are report-only; every fix routes through `/deep-review-codebase-then-fix` — the canonical fixer
- File sets stay disjoint across parts; dependent parts run in DAG waves, never together
- Evidence first — every finding cites `file:line`; no severity from intuition
- Hard limits: ≤ 10 parts, retry ×1 per subagent, fix/re-verify loop ≤ 3 rounds → then stop and report `blocked`
- A part is never dropped silently — `skipped`/`failed`/`covered-manually` all appear in the coverage note with a reason

## Expected Outcome

- Every part of the changed scope reviewed in parallel by its own subagent with a proven coverage note — no part silently dropped
- Findings aggregated, deduped, confirmed, fixed via the canonical fixer, and persisted as rules where mechanical
- `/run-check` + `/deep-validate` green on the whole scope after ≤ 3 re-verify rounds
- A ship-readiness report with verdict `ready-for-ship` or `blocked (reasons)` — `/ship` continues from there
