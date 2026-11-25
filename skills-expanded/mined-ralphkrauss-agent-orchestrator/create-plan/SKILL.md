---
name: create-plan
description: Create a feature implementation plan through structured discussion. Use when user says "create plan", "make a plan", "plan this feature", "let's plan", or wants to design an approach before coding.
---
<!-- Generated from .agents/ by scripts/sync-ai-workspace.mjs. Do not edit directly. -->


# Create Plan

Discussion-first workflow for designing feature implementation plans. Gather requirements through structured questions, resolve key decisions, then produce a written plan that tracks progress through implementation.

## Instructions

### Step 1: Determine Branch, Plan Paths, and Issue Context

1. Get the current git branch name: `git branch --show-current`
2. The plan root directory is `plans/{branch-name}/` (e.g., `plans/14-localization-infrastructure/`)
3. If the branch name starts with a number (e.g., `50-archive-dynamodb-event-store`), that number is a GitHub issue number. Fetch the issue details using the available GitHub tools (owner, repo, issue_number). Use this context to seed the discussion phase -- it often contains requirements, acceptance criteria, and design notes that inform the plan.
4. Derive a short feature slug for this plan (kebab-case, 3-8 words) from the user's requested scope. Examples: `import-timeout-retries`, `cache-expiration-audit`.
5. Use these paths:
   - Plan index (always): `plans/{branch-name}/plan.md`
   - Sub-plan file (this plan): `plans/{branch-name}/plans/{issue-number-if-present-}{feature-slug}.md`
     - If issue number exists, prefix the file name with it (e.g., `123-import-timeout-retries.md`)
     - If issue number does not exist, use `{feature-slug}.md`
6. Check whether the target sub-plan file already exists:
   - If it exists, ask whether to revise/continue it
   - If not, create a new sub-plan file
7. If index file `plans/{branch-name}/plan.md` does not exist, create it as a lightweight catalog of sub-plans.

### Step 1b: Load Review Rules

Before starting the discussion, load relevant rules that may inform the design:

1. Determine which areas of the codebase this feature will likely touch (from issue context, user description, or branch name)
2. Read `.agents/rules/*.md` files relevant to the anticipated paths
3. Keep these rules in context during the discussion phase. When a design decision intersects with a known rule (e.g., a handler that mutates money or shared state → an idempotency rule), proactively raise it:
   - *"The relevant rule requires idempotency checks before mutation. Let's make sure our plan accounts for that."*
4. Log: "Loaded rules from .agents/rules/ relevant to this feature area"

This prevents planning approaches that will fail the same review checks later.

### Step 2: Discussion Phase

Gather requirements and resolve design decisions before writing anything. Use two interaction styles and switch between them dynamically:

**Structured questions** (default) -- use the AskQuestion tool (Cursor) or AskUserQuestion tool (Claude Code) for:
- Clear multiple-choice decisions (approach A vs B vs C)
- Scope confirmation (include X? yes/no)
- Priority ordering
- Technology/pattern selection

**Freeform discussion** -- switch to natural conversation when:
- The user's response opens a broader topic that needs exploration
- A decision requires back-and-forth reasoning
- The user explicitly wants to discuss tradeoffs
- The question doesn't fit neatly into predefined options

After the freeform topic resolves, resume structured questions for the next decision point.

**After core decisions are resolved, probe for edge cases:**
- What are the failure modes? What happens when an external call fails mid-operation?
- Are there race conditions or concurrency risks? (concurrent writes, duplicate callbacks, out-of-order events)
- What about empty, null, or duplicate data? Boundary quantities?
- What if a dependency is down, slow, or returns unexpected data?
- Are there idempotency requirements? Late arrivals? Partial state risks?

Keep this conversational — 2-3 targeted questions based on the feature, not a checklist. Skip scenarios that clearly don't apply. Capture identified risks in the plan's Risks & Edge Cases section.

**Discussion guidelines:**
- Start by summarizing what you already know about the feature (from the branch name, any linked issues, existing code)
- Ask 1-2 questions at a time, not a wall of questions
- Focus on decisions that materially affect implementation: architecture, data model, API contracts, cross-cutting concerns
- Skip questions where the codebase conventions already dictate the answer (check `AGENTS.md`, `docs/ARCHITECTURE.md`)
- Capture each resolved decision as you go -- don't wait until the end
- **Surface alternatives for non-trivial decisions** -- when there are genuinely different implementation approaches (not just cosmetic variations), briefly present 2-3 options with tradeoffs and a recommendation before asking the user to choose. Keep it conversational — a few bullets per option, not a formal document. Note the rejected alternatives and why in the Decisions table so they don't get revisited later.

### Step 3: Write the Sub-Plan and Update Index

Create `plans/{branch-name}/plans/{issue-number-if-present-}{feature-slug}.md` with this structure:

```markdown
# {Feature Title}

Branch: `{branch-name}`
Plan Slug: `{feature-slug}`
Parent Issue: #{issue-number} (if detected)
Created: {date}
Status: planning | in-progress | completed

## Context

Brief description of the feature, why it's needed, and any relevant background.
Issue: #{issue-number} (if detected from branch name, link and summarize key points from the issue)

## Decisions

Resolved design decisions from the discussion phase.

| # | Decision | Choice | Rationale | Rejected Alternatives |
|---|----------|--------|-----------|----------------------|
| 1 | {question} | {chosen approach} | {why} | {brief note on what else was considered and why not, or - if obvious} |
| 2 | ... | ... | ... | ... |

## Scope

### In scope
- Item 1
- Item 2

### Out of scope
- Item 1

## Risks & Edge Cases

| # | Scenario | Mitigation | Task |
|---|----------|------------|------|
| 1 | {edge case or failure mode} | {how it's handled} | {task ID that covers it, or -} |

## Implementation Tasks

Ordered list of implementation tasks with dependencies and acceptance criteria.

| Task ID | Title | Depends On | Status | Acceptance Criteria |
|---------|-------|------------|--------|---------------------|
| {id} | {title} | {deps or -} | pending | {criteria} |

## Rule Candidates

New rules to create via `/create-rule` after implementation validates them. Identified during planning from:
- New patterns established by this feature that other features should follow
- Constraints discovered during discussion that aren't in AGENTS.md or `.agents/rules/` yet
- Edge cases that would prevent future bugs if codified as rules

| # | Rule description | Scope | Create after task |
|---|-----------------|-------|-------------------|
| {n} | {what the rule should enforce} | {project-wide, domain-specific, file-pattern} | {task ID that validates it} |

_Leave empty if no rule candidates identified. Rules are created AFTER implementation confirms they're correct, not before._

## Quality Gates

Derived from matched review rules (Step 1b). These must be true before the plan is considered done.

- [ ] {gate from matched rules, e.g., "All money-mutating handlers have idempotency checks before write"}
- [ ] {gate, e.g., "Domain events registered on every state transition with stable stream IDs"}
- [ ] {gate, e.g., "No hardcoded locale-specific values — use the configured abstraction"}
- [ ] Build passes with zero warnings on affected modules
- [ ] Tests pass for affected test suites

_Auto-populated from rules matched in Step 1b. Add feature-specific gates as needed._

## Execution Log

Updated during implementation. Each completed task gets an entry here.

### {task-id}: {title}
- **Status**: pending
- **Evidence**: (filled during implementation)
- **Notes**: (filled during implementation)
```

Then create or update `plans/{branch-name}/plan.md` as an index of all sub-plans for the branch/ticket:

```markdown
# Plan Index

Branch: `{branch-name}`
Issue: #{issue-number} (if detected)
Updated: {date}

## Sub-plans

| Plan | Scope | Status | File |
|------|-------|--------|------|
| {feature-slug} | {one-line scope} | planning | `plans/{branch-name}/plans/{issue-number-if-present-}{feature-slug}.md` |
```

### Step 3b: Plan Self-Review

Before presenting to the user, review the plan against these questions:

- **Is every task independently completable?** A subagent with no prior context should be able to execute each task from its description and acceptance criteria alone.
- **Are dependencies correct and complete?** No task should reference work from a task that isn't listed as a dependency.
- **Are acceptance criteria testable?** Each criterion should be verifiable via build, test, or observable behavior — not vague ("works correctly").
- **Are there gaps between the last task and "done"?** Check if wiring, registration, configuration, or documentation steps are missing.
- **Does any task try to do too much?** If a task touches 4+ files across multiple projects, consider splitting it.

Fix any issues found before proceeding. This is a quick internal check, not a separate discussion with the user.

### Step 4: Walk Through and Confirm

After writing the sub-plan file (and updating the index), present it to the user for review.

**In terminal environments (Claude Code):** the user can't easily read the plan file side-by-side, so walk through the plan interactively:
- Start with a one-sentence summary of the feature and its context
- Present each key decision as a bullet with the choice and rationale
- List the scope (in/out) as bullets
- Walk through implementation tasks in order, explaining each in one bullet: what it does, why it's needed, and what it depends on
- Ask for feedback after the walkthrough

**In IDE environments (Cursor):** the user can read the plan files in the editor, so keep the summary brief -- highlight any decisions or tasks that deserve extra attention and ask if anything needs revision.

Incorporate feedback and update the relevant sub-plan file (and index if needed). Do NOT commit or push — leave changes in the working tree so review skills can inspect them. The user will commit when ready using `/commit`.

### Step 4b: Knowledge Capture — Rule Check

Check if key design decisions or constraints discovered during planning are not already covered by existing `.agents/rules/` files. For example, a new cross-cutting convention, an edge case that applies beyond this feature, or a constraint that future plans should account for.

If yes, delegate to `/create-rule`. Provide:
- The pattern (the convention or constraint discovered)
- The anti-pattern (what would go wrong without this rule)
- The evidence (branch name, plan slug, the planning discussion that surfaced it)
- Suggested context tags (what kind of work this applies to)

**Do NOT write rule files directly** — `/create-rule` handles dedup, ID assignment, index update, and source tracking.

### Step 5: During Implementation

As tasks are implemented (via the `implement-plan` skill or manual work):

1. Update the task status in the sub-plan's Implementation Tasks table
2. Add evidence entries in that sub-plan's Execution Log section
3. Update the sub-plan top-level Status field when transitioning between phases
4. Keep `plans/{branch-name}/plan.md` index row status in sync for each sub-plan
5. Do NOT commit or push plan updates automatically — leave changes in the working tree for review.

## Lessons Integration

Before writing the plan, check `plans/_lessons.md` for any lessons from prior implementations that are relevant to this feature. Reference applicable lessons in the plan.

## Critical Rules

- **Never skip the discussion phase** -- always gather requirements before writing the plan
- **No mermaid diagrams** -- use tables and plain text for structure
- **Support multiple plans per branch/ticket** -- use one sub-plan file per feature slice and keep `plan.md` as index
- **No filename collisions** -- each sub-plan must have a unique feature slug; include issue prefix when available
- **Plans are living documents** -- they get updated as implementation progresses
- **Don't over-plan** -- keep tasks at a level where each is completable in one focused session
- **Check existing patterns** -- before proposing a new approach, search the codebase for how similar features were built
- **Do not auto-commit** -- never commit or push plan files automatically. Leave changes in the working tree so review skills (`/review`, `/review-codex`) can inspect them. The user will commit when ready using `/commit`.

## Reference

- `AGENTS.md` -- repository-wide constraints
- `docs/ARCHITECTURE.md` -- architecture and DDD boundaries
- `.agents/skills/implement-plan/SKILL.md` -- companion skill for executing plans
- `.agents/skills/create-pr/SKILL.md` -- PR creation with issue number in title
- `plans/_lessons.md` -- cross-feature lessons learned
