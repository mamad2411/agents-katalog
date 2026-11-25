---
name: planning-and-task-breakdown
description: Decomposes spec-driven specifications into small, independently verifiable tasks with explicit dependency ordering, acceptance criteria, effort estimation, and clear ownership. Ensures no task is larger than one day and every task has a definition of done.
---

# Planning and Task Breakdown

## Overview

A spec tells you WHAT to build. Task breakdown tells you HOW to sequence the work. Without it, you get: missed dependencies (built the UI before the API), oversized tasks (takes 2 weeks, status is always "80% done"), and invisible blockers (blocked on design that hasn't started).

This skill decomposes any spec into a directed graph of small, independently verifiable tasks. Each task has:
- A clear **owner**
- An **effort estimate** (1-8 hours, never more than one day)
- **Acceptance criteria** (pass/fail, no subjectivity)
- **Dependencies** (what must be done first)
- **Artifacts** (what is produced: code, test, doc, config)

The golden rule: **If a task takes longer than one day, it's not a task — it's a project.**

## When to Use

| Trigger | Description |
|---------|-------------|
| After spec is approved | Before any implementation begins |
| Sprint/iteration planning | Breaking user stories into workable units |
| Onboarding new team member | Giving someone a clear, bounded first task |
| Unblocking stalled work | Finding the smallest next step |
| Estimating delivery date | Summing task estimates with dependency paths |
| Parallel work opportunities | Identifying tasks that can happen simultaneously |

**Do NOT use** when: the task is trivial (< 1 hour, single person, no dependencies), or when the spec already includes a perfect task breakdown.

## Process

### Step 1: Extract Tasks from Spec

Read the spec section by section and extract candidate tasks.

Each task candidate should answer:
- What is the specific piece of work?
- What file(s) will be created or modified?
- How do we verify it's done?

**Granularity rules:**
- A task is **too large** if it touches more than 3 files
- A task is **too large** if it would take longer than 8 hours for an experienced engineer
- A task is **too small** if it's less than 15 minutes (combine with adjacent tasks)
- A task is **just right** if an engineer can complete it and verify it independently

### Step 2: Define Acceptance Criteria

For each task, write 2-5 pass/fail criteria.

Good acceptance criteria:
- "All fields validate correctly" — NO
- "Email field rejects invalid formats. Password field requires 8+ characters." — YES
- "API works" — NO
- "GET /users returns 200 with user list. GET /users/:id returns 404 for nonexistent user." — YES

### Step 3: Identify Dependencies

For each task, ask: "What must be true before this task can be completed?"

Common dependency types:
| Type | Example |
|------|---------|
| Data dependency | API schema must be defined before UI can consume it |
| Interface dependency | Interface must be agreed before both sides implemented |
| Infrastructure dependency | Database must be provisioned before migrations run |
| Knowledge dependency | Must research X before implementing Y |
| Review dependency | Design must be approved before frontend work |

### Step 4: Estimate Effort

Use **T-shirt sizing with hourly ranges:**

| Size | Hours | Confidence | Action |
|------|-------|------------|--------|
| XS | 0.5-1 | Certain | Do it now |
| S | 1-3 | High | Normal task |
| M | 3-5 | Medium | Break down if > 5 |
| L | 5-8 | Low | Break down. Must not exceed 8. |
| XL | 8+ | Very Low | Must decompose into smaller tasks |

**Estimation rule:** The person doing the work provides the estimate. Never estimate for someone else.

### Step 5: Order the Work

Create a dependency graph.

**Dependency graph patterns:**

```
Pattern 1: Sequential (A → B → C)
  Task A (API schema) → Task B (Backend logic) → Task C (Frontend UI)
  Risk: Blocked if A is delayed.
  Mitigation: Start A early, or build a mock for B/C.

Pattern 2: Parallel (A, B → C)
  Task A (Auth) ──┐
                   ├──→ Task C (Protected route)
  Task B (DB) ────┘
  Risk: Merge conflicts on C.
  Mitigation: Clear interface contract between A, B, and C.

Pattern 3: Fan-in (A → B, C)
  Task A (Shared utility) → Task B (Feature 1)
                           → Task C (Feature 2)
  Risk: A becomes a bottleneck.
  Mitigation: Validate A early, freeze its interface.

Pattern 4: Fan-out (A, B → C, D)
  Task A (API) ──→ Task C (Web UI)
  Task B (Auth) ─→ Task D (Mobile UI)
  Risk: C and D diverge.
  Mitigation: Shared types between C and D.
```

### Step 6: Assign Ownership

Every task must have exactly one owner. Shared ownership is no ownership.

If a task truly requires multiple people, it's too large. Break it into sub-tasks.

### Step 7: Create the Plan

Output a structured task list with all the above.

## Task Template

```markdown
## Task: [Short, verb-first name]

**ID:** T-001
**Owner:** [name]
**Effort:** [XS/S/M/L] (~[hours]h)
**Depends on:** [T-XXX, T-YYY]
**Blocking:** [T-XXX, T-YYY] (tasks that depend on this)

### Description
[2-3 sentence description of the work]

### Acceptance Criteria
- [ ] Criterion 1 (pass/fail, observable)
- [ ] Criterion 2
- [ ] Criterion 3

### Files
- `src/path/to/file.ts` (create)
- `src/path/to/another.ts` (modify)

### Artifacts
- Code changes
- Tests
- Documentation update (if applicable)
```

## Anti-Rationalization Table

| Temptation | Why It Happens | Why It's Dangerous | What To Do Instead |
|------------|----------------|--------------------|--------------------|
| "This task is too complex to estimate" | Genuine uncertainty | Task becomes a black hole | Break it down until you can estimate each piece |
| "I'll just start and figure it out" | Action bias | You miss dependencies, cause rework | List top 3 unknowns as separate research tasks first |
| "This is obvious, no need to write it down" | Laziness | Team can't see progress, can't parallelize | Write one line per task. 10 minutes saves hours. |
| "Let's estimate in story points" | Process cargo-culting | Points are relative, hours are absolute | Use hours. They map to real calendar time. |
| "All tasks are independent" | Wishful thinking | You discover mid-sprint you're blocked | Check: "Can I deliver task B without task A being done?" |
| "This task will take 2 weeks" | Crunch thinking | No one can see progress | Break into 8-hour chunks with milestones |
| "I'll own everything" | Control issues | Bottleneck — no parallel work | Delegate bounded sub-tasks |
| "We can estimate as a team" | Collaboration theater | Group estimate is the loudest voice, not the most accurate | Each person estimates their own work |

## Red Flags

1. Any task estimated > 8 hours — must be decomposed
2. Dependency chain is longer than 5 tasks deep — risk of serial blocking
3. No tasks have dependencies listed — you missed something
4. Acceptance criteria include "works properly" or "looks good" — not measurable
5. All tasks assigned to one person — bottleneck
6. Task descriptions are features, not actions — "Authentication" instead of "Implement login endpoint"
7. Estimates are all the same size — no real thinking happened
8. Milestone named but no tasks attached — placeholder, not a plan
9. No explicit "done" state for any task — can't verify completion
10. Plan doesn't include testing tasks — tests are treated as afterthought

## Verification

- [ ] **Every task has an ID** — T-001, T-002, etc.
- [ ] **Every task has an owner** — exactly one person
- [ ] **No task exceeds 8 hours** — if it does, decompose it
- [ ] **Acceptance criteria are pass/fail** — no subjective language
- [ ] **Dependencies are explicit** — what must be done first
- [ ] **Dependency graph is acyclic** — no circular dependencies
- [ ] **Critical path identified** — longest dependency chain
- [ ] **Parallel tasks exist** — work can be distributed
- [ ] **Testing tasks are included** — not implicit
- [ ] **Total effort estimated** — sum of all task hours
- [ ] **Milestones defined** — checkpoints with clear outputs
- [ ] **Risks identified** — what could delay each milestone

### Plan Output Template

```markdown
# Implementation Plan: [Feature Name]

## Summary
- **Total tasks:** 12
- **Total effort:** 32 hours (estimated)
- **Critical path:** T-001 → T-003 → T-007 → T-010 → T-012 (18 hours)
- **Parallel tracks:** 3 maximum
- **Estimated calendar time:** 3-4 days (with 2 engineers)

## Dependency Graph
```
T-001 (Auth schema)
  ├──→ T-002 (Auth service) ──→ T-005 (Session middleware)
  │                             └──→ T-007 (Protected routes)
  │
T-003 (DB migrations)
  ├──→ T-004 (User model) ──→ T-006 (User API)
  │                             └──→ T-008 (User UI)
  │
T-009 (E2E test setup)
  └──→ T-010 (Auth E2E tests) ──→ T-011 (User E2E tests)
                                   └──→ T-012 (Integration tests)
```

## Milestones
| Milestone | Tasks | Estimated | Verifiable Outcome |
|-----------|-------|-----------|--------------------|
| M1: Auth foundation | T-001, T-002, T-003 | 8h | Users can register and log in |
| M2: Core API | T-004, T-005, T-006 | 10h | CRUD operations working |
| M3: User interface | T-007, T-008 | 8h | UI connected to API |
| M4: Tests | T-009, T-010, T-011, T-012 | 6h | All scenarios automated |

## Task List

### T-001: Define Auth API schema
**Owner:** Alice
**Effort:** S (~2h)
**Depends on:** None
**Blocking:** T-002, T-005

**AC:**
- [ ] POST /auth/register accepts email + password
- [ ] POST /auth/login returns JWT token
- [ ] Schema validated with Zod
- [ ] OpenAPI spec updated

### T-002: Implement auth service
...
```
