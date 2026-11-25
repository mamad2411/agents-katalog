---
name: harness-plan
description: Orchestrate the entire PLAN phase in one command — spec, research, plan, plan-check, and (if warranted) architecture. Use at the start of any non-trivial feature/change. Sequences the atomic skills, delegates to subagents, and pauses for your input at each decision gate.
---

# /harness-plan — run the Plan phase

A thin orchestrator. It does not re-implement the sub-skills; it sequences them,
enforces the gates, and stops for you at real decision points. Keep using the atomic
skills (`/harness-claude:spec`, `/harness-claude:plan`, ...) directly when you only want one step.

## Sequence

1. **`/harness-claude:spec`** — clarify the request into a spec with testable acceptance criteria.
   → **HALT** and ask the user any load-bearing clarifying questions. Do not proceed on
   guesses. Resume once the spec's open questions are resolved.

2. **`/harness-claude:research`** — reuse-first search (in-repo → context7 → registries/GitHub → web).
   Produce the build-vs-reuse decision; fold it into the spec.

3. **`/harness-claude:plan`** — **delegate to the `harness-claude:planner` agent** (pass it the spec + reuse decision +
   the *objective*, not just a query). Return a phased plan (tasks with write-sets +
   `depends_on` + the `AC-n` each addresses) with per-task exit checks.

4. **`/harness-claude:plan-check`** — gate the plan against the spec (criteria coverage, scope,
   parallel-task disjointness) before any code. **Delegate to the `harness-claude:planner` agent in a
   read-only check pass.** Loop ≤3 revisions with `/harness-claude:plan` on findings.
   → **HALT** and show the user the checked plan for approval before any code. A standing
   Critical finding blocks the phase.

5. **Design gate** — two independent, conditional siblings. A change can need one, both,
   or neither; run only what's relevant and **say which you skipped**.
   - **`/harness-claude:architect`** — **only if** the plan flagged a load-bearing *system*
     decision (new subsystem, public interface/data model, cross-cutting change, multi-shape
     refactor). Delegate to the `harness-claude:architect` agent and present the ADR.
   - **`/harness-claude:design`** — **only if** the change has a *user-facing surface* (page,
     screen, component, form, mobile, CLI/TUI presentation). Produce the design brief.
   → **HALT** for approval on whichever ran. If the work is routine and internal (no UI, no
   load-bearing design — like this CLI harness itself), **skip both** and say so.

## Rules
- Delegate the heavy steps (plan, architecture) to subagents; keep only their summaries
  in the main context to protect tokens.
- Never skip the HALTs — the Plan phase is interactive by design.
- Save artifacts (spec, plan, ADR, design brief) via `/harness-claude:save-session` for multi-session work.

## Output
A short phase summary: spec ✓, reuse decision, approved plan (phases), and the design gate —
architecture decision (or "skipped — routine") and design brief (or "skipped — no UI surface").
Then hand off to `/harness-claude:harness-implement`.
