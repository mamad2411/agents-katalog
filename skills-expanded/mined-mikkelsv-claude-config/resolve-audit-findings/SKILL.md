---
name: resolve-audit-findings
description: "Triage the judgment-only audit findings that /audit-branch deferred — research each, apply inline when the fix is clearly better, and defer substantial or architectural findings to a post-audit plan. Use after /audit-branch, or whenever you're handed a structured findings list to work through."
---

# Resolve Audit Findings

Per-finding triage. Every item gets researched first — even ones that look like easy applies — then applied inline or deferred based on what the research surfaced. The skill's value is informed confidence, not reflexive disposition.

**Apply by default — defer is the exception, not the path.** Defer only when:

- Scope is substantial (multi-file restructure, public API change, framework-level decision)
- The fix needs deep consideration (architectural choice with multiple defensible paths)
- Research reveals the finding is stale or wrong → skip with a one-line reason

## Input

Structured findings list — the **judgment-only set** that upstream agents chose not to apply themselves. Mechanical findings (typos, unused imports, stale comments, trivial dead code) are already inlined by `/audit-branch` Phase 3 and don't reach here. Each item has `**File:**`, `**Description:**`, `**Recommended fix:**`. Caller passes the list and a slug for deferral (current branch name, sans `implement/` prefix, or a short feature name).

## Step 1: Research per finding (Sonnet agents in parallel)

Spawn one Sonnet sub-agent per finding (per `wf-agents-on-sonnet` + `wf-delegate-large-reads`). Batch all spawns into a single message so they run in parallel — research is fully delegated, orchestrator does no file reads.

Each agent's prompt:

1. The single finding (file, description, recommended fix).
2. Investigate before deciding:
   - Read the affected file + immediate consumers/callers.
   - Grep for the pattern elsewhere — codebase precedent usually decides.
   - Check `.claude/rules/` and `CLAUDE.md` for constraints touching the finding.
   - Cross-module / framework-API / unclear cases: deeper multi-file exploration, external doc fetch (per `wf-verify-api-before-using`), git history check on the affected files.
3. Classify and return structured:
   - `bucket`: **Apply** (right answer clear, scope contained) / **Defer** (substantial: multi-file restructure, public API, architectural with multiple defensible paths) / **Skip** (stale / wrong / already addressed)
   - `research_summary`: what was checked + what was found (1-3 sentences)
   - `recommended_edit`: precise edit for Apply, task `**Context:**` paragraph for Defer, or reason for Skip
   - `confidence`: 0-1

## Step 2: Apply

For each `Apply` return with high confidence, execute the agent's `recommended_edit` via Edit/Write. Apply minimally — don't expand scope. Build verification runs upstream (`/audit-branch` Phase 6).

For `Apply` returns with low/moderate confidence, downgrade to `Defer` — the agent wasn't sure enough; the user should review.

## Step 3: Defer

For each `Defer` (and downgraded-Apply) finding, write to `plans/post-audit-{slug}.md` using `plan-template.md` from the implement skill directory. Each = one Task with `**Files:**`, `**Acceptance:**`, and `recommended_edit` as `**Context:**`. Append if the file exists.

## Step 3.5: Deferred doc gaps actually close

Before a plan is treated as closed, grep every task's notes for deferral language about documentation — "doc update deferred", "will document in", "note this in `docs/…`", "follow-up doc" — and confirm the named content landed. A deferred doc gap has no build error, no failing test, and no reviewer: the task ticks complete on the code, and the doc sentence quietly never arrives.

## Step 4: Report

Concise summary:

- **Applied inline** — one line per finding (`file:line — what changed`)
- **Deferred** — titles only, with the plan path
- **Skipped** — one-line reason per finding

If the deferred set is unusually large (8+ tasks), mention: *"consider `/plan-optimizer plans/post-audit-{slug}.md` for an extra refinement pass."*
