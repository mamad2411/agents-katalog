---
name: implement-plan
description: Execute implementation plans using a reviewer-led loop with one-task-per-agent delegation, iterative verification, and mandatory hardening passes. Use when the user asks to implement a plan, execute tasks, harden an implementation, or iterate on quality before final handoff.
---
<!-- Generated from .agents/ by scripts/sync-ai-workspace.mjs. Do not edit directly. -->


# Implement Plans

Reviewer-led workflow for turning plan files into production-ready code with repeated verification and hardening. The main agent owns architecture, quality gates, and final sign-off. Delegated agents execute tightly scoped tasks.

## When To Use

- User asks to implement a plan from `plans/{branch-name}/`
- User asks for phased delivery with multiple verification points
- User asks to harden an implementation before final handoff

## Critical Rules

1. **Plan before code**: for non-trivial work (3+ steps, cross-project changes, or architecture decisions), create a plan first using the `create-plan` skill.
2. **Re-plan on drift**: if assumptions break, tests fail repeatedly, or scope changes, stop and update the plan before continuing.
3. **Main agent is the reviewer**: keep global context, risk register, acceptance criteria, and final decisions in the main agent.
4. **One task per agent**: delegate exactly one task item per agent; no broad multi-task prompts.
5. **Evidence before completion**: no task is complete without code evidence plus verification evidence.
6. **Build/test constraints**: use `just` commands, never run apps, and run only affected test projects by default.
7. **Scope hygiene**: do not include unrelated generated or style-only changes.
8. **Behavior diff check**: for changed contracts/flows, verify old vs new behavior explicitly, not just compile success.
9. **Lessons loop (aggressive)**: add a lesson to `plans/_lessons.md` after any of these triggers — not just user corrections:
   - User corrects your approach or a delegated agent's output
   - A delegated agent makes a mistake that the review catches (pattern the review should have prevented)
   - A hardening pass finds a recurring issue type
   - A build/test failure reveals a non-obvious constraint
   Apply all existing lessons from `_lessons.md` at the start of every agent brief, not just at plan load time.
10. **Balanced elegance**: for non-trivial changes, run one elegance pass; simplify only when it reduces risk or complexity.
11. **Follow project conventions for cross-cutting machinery**: when a change touches scheduled jobs, message handlers, transactional consumers, or other cross-cutting infrastructure, follow the project's existing patterns (rule files, reference docs, architectural guides) rather than inventing a new shape. If a relevant `.agents/rules/*.md` or architecture doc exists, read it before implementing.
12. **Boundary validation**: clamp/validate externally supplied numeric controls (e.g., batch sizes) at handler boundaries before domain-service execution.
13. **No skipping or deferring without consent**: NEVER skip, defer, or simplify any task from the plan without explicit user approval. Every task in the plan must be implemented as specified. If a task seems too complex or edge-case-only, ask the user before deferring — do not decide unilaterally to skip it.
14. **Do not auto-commit**: never commit or push automatically. Leave changes (including plan file updates) in the working tree so that review skills (`/review`, `/review-codex`) can inspect them. The user will commit when ready using `/commit`.

## Step 1: Locate Plan and Build Task Graph

1. Get the current git branch: `git branch --show-current`
2. Find the plan at `plans/{branch-name}/plan.md`
   - If no plan exists, tell the user and suggest using the `create-plan` skill first
3. Extract for each task:
   - task id/title
   - dependencies
   - acceptance criteria
   - impacted files/projects
   - required verification (build/tests/docs)
4. Update the plan's Implementation Tasks table and Execution Log section as you progress. Use these status values:
   - `pending`, `in_progress`, `blocked`, `completed`, `deferred`
5. Load prior lessons from `plans/_lessons.md` (cross-feature lessons) and `.agents/rules/*.md` (rules matching impacted files from the plan). Apply relevant ones before coding and include them in agent briefs.
6. Check for a context file at `contexts/{branch-name}/context.md`:
   - If it exists, read it. This contains pre-curated research: critical path, must-read file manifest, external provider knowledge, internal architecture patterns, and test patterns.
   - The context file is the primary knowledge source for agent briefs — it prevents agents from wasting time on discovery and missing edge cases.

## Step 2: Reviewer-Driven Task Loop

Run this loop for each dependency-ready task:

1. Prepare implementation brief:
   - exact scope (single task id)
   - likely files touched
   - acceptance criteria
   - constraints from `AGENTS.md`
   - **context file preamble**: if a context file exists at `contexts/{branch-name}/context.md`, the agent prompt MUST start with: "First, read `contexts/{branch-name}/context.md` and then read all **critical** must-read files listed in it. This gives you the domain knowledge, patterns, and edge cases you need before writing any code." Include the context file path and the critical must-read file paths explicitly in the prompt so the agent reads them upfront — do not assume it will discover them on its own.
2. Delegate implementation to an agent.
   - Use a more capable model for risky logic or financial flows.
   - Use a faster model only for narrow mechanical edits.
3. Review the agent's output in two passes:

   **Spec compliance (first)** -- does it match the task, nothing more, nothing less?
   - All acceptance criteria from the plan are satisfied
   - No extra features, refactors, or "improvements" beyond scope were added
   - No acceptance criteria were partially implemented or skipped
   - If spec issues are found, fix them before proceeding to quality review

   **Code quality (second)** -- is it well-built?
   - architecture and pattern fit
   - invariants and edge-case handling
   - call-site propagation for contract changes
   - logging and observability quality
4. Run targeted verification and capture evidence:
   - run the project's targeted build and test commands for the affected modules
   - when a change touches cross-cutting infrastructure (scheduled jobs, message handlers, transactional consumers, etc.), verify it conforms to the patterns documented in the relevant `.agents/rules/*.md` or architecture docs.
5. **Rule check**: diff the task's changed files against matched rules from `.agents/rules/` (loaded at plan start). For each matched rule, verify the new code does not exhibit the anti-pattern. If a violation is found, send it back to the agent as focused feedback — do not mark the task complete until rule violations are resolved. Log: "Task {id}: checked against N rules — {pass/N violations}"
6. Check the plan's **Quality Gates** section (if present). If any gate can now be verified for this task's files, verify it. Update the gate checkbox.
7. Decide:
   - **Pass**: mark task completed in the plan with evidence
   - **Fail**: provide focused feedback (including rule violations) and rerun the same task
   - **Scope drift**: re-plan first, then continue
8. Update the plan file after each task completes:
   - Set task status to `completed` in the Implementation Tasks table
   - Fill in the Execution Log entry with evidence and notes
   - Do NOT commit or push — leave changes in the working tree for review

## Step 3: Mandatory Hardening Passes

Run after implementation reaches feature-complete state.

### Pass A: Functional Completeness

- Every plan task maps to concrete code changes
- No partially implemented interfaces/contracts remain
- All changed call sites compile and behave as intended

### Pass B: Bug Hunt and Failure Paths

Actively search for bugs in:

- edge conditions, null/empty/invalid inputs
- rollback/transaction semantics
- idempotency and concurrency risks
- fallback route correctness and observability

For domain-critical features (money handling, irreversible mutations, regulated flows), also verify:

- no magic strings or IDs in core domain logic
- deterministic routing/decision references are set consistently
- mutations align with documented invariants
- explicit handling of late events and terminal states
- warning/audit logging on fallback paths

### Pass C: Regression and Quality Gates

- Re-run affected build/test gates after hardening fixes
- Update docs when behavior or conventions changed
- Remove unrelated diff noise and confirm PR scope hygiene

## Step 4: Completion Report

Update the plan file with final status and produce a summary:

- Set top-level Status to `completed`
- All tasks have evidence in the Execution Log
- Deferred or blocked tasks have rationale and next actions
- Verification commands run and outcomes recorded
- Residual risks and monitoring recommendations noted
- Lessons added to `plans/_lessons.md` during this run (if any)
- Do NOT commit or push — leave changes in the working tree for review. The user will commit when ready using `/commit`.

## Step 4b: Knowledge Capture — Rule Check

Check if implementation revealed patterns, gotchas, or constraints worth codifying that are not already covered by existing `.agents/rules/` files. Sources include: recurring hardening findings, non-obvious constraints discovered during implementation, patterns from user corrections, or lessons added to `_lessons.md` during this run that have broader applicability.

If yes, delegate to `/create-rule`. Provide:
- The pattern (the convention or constraint discovered)
- The anti-pattern (the code that was wrong or the mistake that was made)
- The evidence (branch name, task ID, what happened during implementation)
- Suggested context tags (what kind of work this applies to)

**Do NOT write rule files directly** — `/create-rule` handles dedup, ID assignment, index update, and source tracking.

## Step 4c: Rule Harvest

After the completion report, check for patterns worth codifying as permanent rules:

- Tasks that required multiple iterations due to undocumented conventions
- Lessons added to `plans/_lessons.md` during this run that are generalizable
- Rule candidates listed in the plan's "Rule Candidates" table (if present) that were validated by implementation
- Recurring review findings from hardening passes that have no existing rule

If candidates found, suggest: "This implementation validated {N} patterns that could become permanent rules. Create them via `/create-rule`? {list with one-line descriptions}"

Rules are created only for validated patterns — not speculative ones.

## Step 5: PR Creation

After the completion report, ask the user if they want to create a pull request. If approved, follow the `create-pr` skill to create a PR with the issue number in the title and the plan summary as the body.

## Verification Checklist

- [ ] Plan located and task graph understood
- [ ] Context file loaded (if `contexts/{branch-name}/context.md` exists) and passed to agents
- [ ] Plan file updated throughout the run
- [ ] One-task-per-agent delegation used per task
- [ ] Spec compliance + code quality review passed for each completed task
- [ ] Hardening Pass A complete
- [ ] Hardening Pass B complete
- [ ] Hardening Pass C complete
- [ ] Build/test evidence recorded
- [ ] Docs/localization updates handled where needed
- [ ] Final report includes risks, deferrals, and lessons

## Reference

- `AGENTS.md` -- repository-wide constraints and implementation rules
- `.agents/skills/create-plan/SKILL.md` -- companion skill for creating plans
- `.agents/skills/create-pr/SKILL.md` -- PR creation with issue number in title
- `plans/_lessons.md` -- cross-feature lessons learned
