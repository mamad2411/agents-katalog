---
name: writing-plans-for-teams
description: Use when you have a spec or requirements for a multi-step task that may benefit from parallel team execution, before touching code. Runs a fitness check and either produces a team-format plan or hands off to writing-plans.
---

# Writing Plans for Teams

## Overview

Write implementation plans designed for parallel execution by a team of persistent specialist agents coordinated by a Lead through Claude Code's Agent Teams feature. Before drafting task content, run a fitness check; if the plan doesn't benefit from team execution, hand off to `writing-plans` immediately.

Assume implementers are skilled developers with zero codebase context. Document everything: which files to touch, complete code, testing commands, dependency relationships, and what each task produces for later tasks. DRY. YAGNI. TDD. Frequent commits.

**Announce at start:** "I'm using the writing-plans-for-teams skill to create the implementation plan."

**Context:** This should be run in a dedicated worktree (created by brainstorming skill).

**Save plans to:** `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`
- (User preferences for plan location override this default)

## The Process

Companion-skill names in this skill (`writing-plans`, `subagent-driven-development`) are unprefixed: resolve each to your local skill of that name, or its superpowers-plugin equivalent (`superpowers:<name>`) if that is where yours lives.

1. Draft the task list and dependency graph (no code or file paths yet — just what are the tasks and what depends on what)
2. Run the fitness check
3. If it fails, hand off to `writing-plans` immediately
4. If it passes, write the full team-format plan

## Fitness Check

**Scope of this gate (read first).** The four-criterion check below is the **build-team** gate: it decides whether a multi-task, multi-wave *build* should run as a persistent specialist team versus a serial subagent chain. It is NOT the gate for a **deliberation team** (2+ conflicting expert lenses cross-challenging to converge on one contested decision). A deliberation team is count-free, needs no spec and no written plan (the deliberation IS the design work), and is reached at intake time per the `task-routing` skill's deliberation track. It never arrives here. If you find yourself failing a decision/design question against the >=4-task / >=2-wave thresholds, STOP: you are applying the build gate to a deliberation, which is the documented mis-route. Send it back to the deliberation track, do not hand it to `writing-plans`.

**Pre-check (shape):** before the four-criterion gate, ask one question. Is this mechanical fan-out over independent units with no cross-task deliberation (apply the same transform to N files, score N candidates against one rubric, run parallel verifiers, extract structured data from N documents)? If yes, this is **Workflow-shaped**, not team-shaped: a persistent specialist team adds coordination overhead it cannot repay when the units never talk to each other, and a serial subagent chain wastes the parallelism. Recommend the `Workflow` tool instead (and note that under ultracode the session will tend to author one by default). This stays advisory: surface the recommendation in your announce text, do not hand off to a third skill. A genuine team-shaped BUILD plan (specialists carrying context across waves, reconciling module boundaries) proceeds to the four-criterion gate below.

All four criteria must hold. If ANY fails, hand off.

| Criterion | Threshold |
|---|---|
| Total tasks | ≥ 4 |
| Waves with ≥2 tasks | ≥ 2 |
| Distinct specialist roles | ≥ 2 |
| No pervasive shared state across tasks | judgment |

**If any fail:**

Announce to user: *"After analyzing dependencies, this plan is [reason: e.g., only 3 tasks / a serial chain / single specialist / heavy shared state]. Team overhead wouldn't pay off. Switching to writing-plans with subagent-driven execution."*

Then invoke `writing-plans` as the sub-skill. Do not attempt to draft a team-format plan and convert.

## Plan Document Header

Every team-format plan MUST start with this header. It references `agent-team-driven-development` (user-level skill; not namespaced). The square-bracketed text is template syntax you fill in:

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use agent-team-driven-development to implement this plan in parallel with a specialist team. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

---
```

`agent-team-driven-development` greps for `agent-team-driven-development` in the blockquote at boot; the exact string matters.

## Wave Analysis

Immediately after the header. Four subsections: Specialists, Waves, Dependency Graph, Lifetime Plan.

```markdown
## Wave Analysis

### Specialists

| Role | Expertise | Tasks |
|------|-----------|-------|
| backend-engineer | API design, DB conventions, server patterns | Tasks 1, 2 |
| docs-writer | Technical writing, API docs | Task 5 |

### Waves

**Wave 1: Foundation** — schema + types everything else needs
- Task 1 (backend-engineer) — Zod schemas

  *Parallel-safe because:* only one task in wave

**Wave 2: Independent consumers** — both need Wave 1 types, different modules
- Task 2 (backend-engineer) — DB migration
- Task 5 (docs-writer) — iOS model docs

  *Parallel-safe because:* different directories, no import relationship
  *Depends on Wave 1:* Task 1's schemas at `packages/shared/src/schemas/`

### Dependency Graph

```
Task 1 → Task 2
Task 1 → Task 5
```

### Lifetime Plan

| Specialist | Waves | Lifetime strategy |
|---|---|---|
| backend-engineer | 1, 2 | Full-session (2+ waves of work) |
| docs-writer | 2 | Spawn-per-wave, shut down after Wave 2 |
```

**Rules for wave grouping:**
- Max 3 tasks per wave (max 3 simultaneous implementers)
- Tasks in the same wave MUST NOT touch the same files
- Tasks in the same wave MUST NOT have an import relationship
- When unsure about independence → serialize into separate waves
- Earlier waves produce foundations (types, schemas, configs); later waves consume them

**Rules for specialists:**
- Max 3 distinct specialist roles (beyond that, diminishing returns)
- Every task's `Specialist:` field must match exactly one Specialists table row
- Use descriptive role names, not numbers (`backend-engineer`, not `engineer-1`)

## Task Structure

Every task has three mandatory metadata fields plus the standard superpowers task body. The `subject` that gets used for `TaskCreate` is the task heading with a role prefix — `agent-team-driven-development` uses this prefix for self-claim filtering.

```markdown
### [backend-engineer] Task N: Zod schemas

**Specialist:** backend-engineer
**Depends on:** None
**Produces:** `packages/shared/src/schemas/user-preferences.ts` with `UserPreferencesSchema` exported

**Files:**
- Create: `packages/shared/src/schemas/user-preferences.ts`
- Test: `packages/shared/src/schemas/user-preferences.test.ts`

- [ ] **Step 1: Write the failing test**

```ts
import { UserPreferencesSchema } from './user-preferences';

test('validates theme enum', () => {
  const result = UserPreferencesSchema.safeParse({ theme: 'dark' });
  expect(result.success).toBe(true);
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `bun test packages/shared/src/schemas/user-preferences.test.ts`
Expected: FAIL with "Cannot find module './user-preferences'"

- [ ] **Step 3: Write minimal implementation**

[... real code, complete, not "TBD" ...]

- [ ] **Step 4: Run test to verify it passes**

Run: `bun test packages/shared/src/schemas/user-preferences.test.ts`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add packages/shared/src/schemas/
git commit -m "feat(shared): add UserPreferencesSchema"
```
```

**Task metadata fields:**

- **`Specialist:`** — role name. Must match a Specialists table row exactly.
- **`Depends on:`** — either `None` or explicit task references with what's produced. Example: `Task 1 (Zod schemas at packages/shared/src/schemas/)`. Lead reads these to set `addBlockedBy` on `TaskCreate`.
- **`Produces:`** — what this task creates that later tasks consume. Goes into the teammate's journal entry on completion.
- **`Plan approval required:`** — `true` or `false` (omit if false). Set `true` when the task touches schema migrations, destructive operations, auth/session logic, or refactors >5 files. The lead spawns these teammates in plan-approval mode; they must propose an approach via `plan_approval_request` before writing code. See `agent-team-driven-development` § Plan Approval for Risky Tasks.

## Bite-Sized Task Granularity

Same as `writing-plans`; each step is one action (2-5 minutes). Write failing test, verify fails, minimal implementation, verify passes, commit.

## No Placeholders

Every step must contain actual content. These are plan failures:
- "TBD", "TODO", "implement later"
- "Add appropriate error handling" / "add validation" / "handle edge cases"
- "Similar to Task N" (repeat the code)
- Steps that describe without showing (code blocks required for code steps)

## Remember

- Exact file paths always
- Complete code in every step
- Exact commands with expected output
- DRY, YAGNI, TDD, frequent commits
- Max 3 tasks per wave
- Same-wave tasks must not touch the same files
- Same-wave tasks must not have an import relationship
- Max 3 distinct specialist roles total
- Dependency graph must be acyclic

## Self-Review

After writing the complete plan, run the standard `writing-plans` self-review checklist (spec coverage, placeholder scan, type consistency) plus three team-specific checks:

1. **Wave grouping safety** — for each same-wave pair, confirm no file overlap and no import relationship
2. **Task metadata completeness** — every task has Specialist, Depends on, and Produces fields
3. **Specialist role consistency** — every `Specialist:` reference matches a row in the Specialists table; no orphaned roles; no two rows with overlapping responsibilities

If you find issues, fix inline. If you find a spec requirement with no task, add the task.

## Execution Handoff

After saving the plan, present:

**"Plan complete and saved to `docs/superpowers/plans/<filename>.md`. Two execution options:**

**1. Agent Team-Driven (recommended for this plan)** — Parallel specialist team via Agent Teams, wave-based execution, two-stage review per task

**2. Subagent-Driven** — Serial, simpler, no team overhead. Better if you want to re-check whether team execution is worth it.

**Which approach?"**

**If Agent Team-Driven chosen:**
- **REQUIRED SUB-SKILL:** Use `agent-team-driven-development`
- Stay in this session
- Lead spawns specialists, orchestrates waves, runs reviews

**If Subagent-Driven chosen:**
- **REQUIRED SUB-SKILL:** Use `subagent-driven-development`
- Fresh subagent per task, serial execution
