---
name: planning-and-task-breakdown
description: Breaks work into ordered tasks. Use when you have a spec or clear requirements and need to break work into implementable tasks. Use when a task feels too large to start, when you need to estimate scope, or when parallel work is possible. For refactor, debugging, lifecycle/status, or system-design plans, require source grounding plus a bounded zoom-out across callers, consumers, sibling flows, ownership, state/status cohorts, and verification before approving tasks.
---

# Planning and Task Breakdown

## Overview

Decompose work into small, verifiable tasks with explicit acceptance criteria. Good task breakdown is the difference between an agent that completes work reliably and one that produces a tangled mess. Every task should be small enough to implement, test, and verify in a single focused session.

For substantive plans, run Deep Think first or inline its plan-review standard. A plan is not
ready just because the task list is tidy; it must prove the objective, source truth, ownership,
blast radius, edge cases, and proof path. Use a bounded zoom-out: first ring by default, one
more ring only when root cause, lifecycle/status coverage, ownership, or verification remains
unclear.

## When to Use

- You have a spec and need to break it into implementable units
- A task feels too large or vague to start
- Work needs to be parallelized across multiple agents or sessions
- You need to communicate scope to a human
- The implementation order isn't obvious

**When NOT to use:** Single-file changes with obvious scope, or when the spec already contains well-defined tasks.

## The Planning Process

### Step 1: Enter Plan Mode

Before writing any code, operate in read-only mode:

- Read the spec and relevant codebase sections
- Identify existing patterns and conventions
- Map dependencies between components
- Read the real source of truth for the work: entrypoints, owners, contracts, configs, tests, and current consumers
- Zoom out from the proposed change: callers, consumers, sibling modules or workflows, state/status cohorts, terminal/excluded states, and operator workflow
- Cite which files or symbols the plan is grounded in
- If source access is incomplete, label assumptions and unknowns instead of inventing certainty
- Note risks and unknowns

For PR-producing or review-sensitive work, add a front-loaded review-prevention checklist before tasking. Decide which recent-review classes apply: branch/reason coverage, async state-machine recovery, request/response/config field drift, SQL cast/index/migration safety, runtime-to-proof parity, proof-lane selection, tenant/owner scoping, external fallback/idempotent retry, security/log redaction, public seam/consumer drift, accessibility for custom controls, performance/bounded work, artifact hygiene, and test integrity. Each applicable class needs a planned proof command or becomes a blocking question.

For multi-file, refactor, or architecture-sensitive work, add an `Architecture Ratchet Matrix` before tasking. It must lock the current boundary, intended boundary, public seam, owner layer, allowed dependency direction, forbidden imports, architecture test, and future regression that should fail fast. Prefer thin vertical tracer bullets that move one observable behavior through the seam; avoid horizontal file churn, deep private modules without a public seam, or new helper layers that are not protected by a consumer/startup/module-graph test.

For schema/query/data-sensitive work, add a `Local Full-Schema Proof Plan`. Prefer a local Postgres clone or restored snapshot that matches the migrated schema before PR submission. Use sanitized or approved least-privilege data; never point tests at production, commit dumps, print credentials, or let proof depend on machine-local paths. If full-schema local proof is unavailable, the plan must mark it as a blocking question or explicitly narrow the claim away from schema/query behavior.

Do not infer architecture, ownership, or blast radius from folder names or common patterns alone. Read the actual implementation first.
Do not approve lifecycle-driven plans until the relevant state/status cohort is enumerated and
each included or excluded state has a source-grounded reason.

**Do NOT write code during planning.** The output is a plan document, not implementation.

### Step 2: Identify the Dependency Graph

Map what depends on what:

```
Database schema
    │
    ├── API models/types
    │       │
    │       ├── API endpoints
    │       │       │
    │       │       └── Frontend API client
    │       │               │
    │       │               └── UI components
    │       │
    │       └── Validation logic
    │
    └── Seed data / migrations
```

Implementation order follows the dependency graph bottom-up: build foundations first.

### Step 3: Slice Vertically With Tracer Bullets

Instead of building all the database, then all the API, then all the UI — build one complete feature path at a time:

**Bad (horizontal slicing):**
```
Task 1: Build entire database schema
Task 2: Build all API endpoints
Task 3: Build all UI components
Task 4: Connect everything
```

**Good (vertical slicing):**
```
Task 1: User can create an account (schema + API + UI for registration)
Task 2: User can log in (auth schema + API + UI for login)
Task 3: User can create a task (task schema + API + UI for creation)
Task 4: User can view task list (query + API + UI for list view)
```

Each vertical slice delivers working, testable functionality.

A good slice is a tracer bullet:

- It passes through every integration layer needed for one observable outcome.
- It is demoable or verifiable by itself.
- It has its own acceptance criteria and proof command.
- It can be implemented without depending on unfinished sibling slices, except for explicitly named prerequisites.
- It leaves the system in a working state when complete.

Mark slices as `AFK` when an agent can execute them from the written task without fresh human decisions. Mark them as `HITL` when they need human product, design, access, or architecture input before execution.

### Step 4: Write Tasks

Each task follows this structure:

```markdown
## Task [N]: [Short descriptive title]

**Description:** One paragraph explaining what this task accomplishes.

**Acceptance criteria:**
- [ ] [Specific, testable condition]
- [ ] [Specific, testable condition]

**Slice type:** [AFK | HITL]

**Execution proof:**
- [ ] Focused command passes: `npm test -- --grep "feature-name"`
- [ ] Build/gate command passes: `npm run build`
- [ ] Runtime or headless proof command passes: `...`
- [ ] Manual/HITL observation, if any: [supporting context only; not completion evidence unless this task is explicitly human-only]

**Dependencies:** [Task numbers this depends on, or "None"]

**Grounded in current source:**
- `src/path/to/current-entrypoint.ts`
- `src/path/to/current-consumer.ts`

**Zoom-out / lifecycle coverage:**
- Callers and consumers checked: [...]
- Sibling flows or filters checked: [...]
- Included states/statuses: [...]
- Excluded terminal states/statuses: [...]

**Review-prevention coverage:**
- Applicable recent-review classes: [...]
- Planned proof commands or blocking questions: [...]
- Artifact/proof-lane/test-integrity gates: [...]

**Architecture ratchet coverage:**
- Boundary preserved or introduced: [...]
- Public seam and owner layer: [...]
- Forbidden import/coupling regression: [...]
- Architecture proof command: [...]

**Local full-schema proof, if DB/schema-sensitive:**
- Local Postgres source: [sanitized clone | approved snapshot | schema-only | unavailable/blocking]
- Restore/migration command: [...]
- Proof command and cleanup: [...]

**Files likely touched:**
- `src/path/to/file.ts`
- `tests/path/to/test.ts`

**Estimated scope:** [Small: 1-2 files | Medium: 3-5 files | Large: 5+ files]
```

### Step 5: Order and Checkpoint

Arrange tasks so that:

1. Dependencies are satisfied (build foundation first)
2. Each task leaves the system in a working state
3. Verification checkpoints occur after every 2-3 tasks
4. High-risk tasks are early (fail fast)

Add explicit checkpoints:

```markdown
## Checkpoint: After Tasks 1-3
- [ ] All tests pass
- [ ] Application builds without errors
- [ ] Core user flow works end-to-end
- [ ] Review with human before proceeding
```

## Task Sizing Guidelines

| Size | Files | Scope | Example |
|------|-------|-------|---------|
| **XS** | 1 | Single function or config change | Add a validation rule |
| **S** | 1-2 | One component or endpoint | Add a new API endpoint |
| **M** | 3-5 | One feature slice | User registration flow |
| **L** | 5-8 | Multi-component feature | Search with filtering and pagination |
| **XL** | 8+ | **Too large — break it down further** | — |

If a task is L or larger, it should be broken into smaller tasks. An agent performs best on S and M tasks.

**When to break a task down further:**
- It would take more than one focused session (roughly 2+ hours of agent work)
- You cannot describe the acceptance criteria in 3 or fewer bullet points
- It touches two or more independent subsystems (e.g., auth and billing)
- You find yourself writing "and" in the task title (a sign it is two tasks)

## Plan Document Template

```markdown
# Implementation Plan: [Feature/Project Name]

## Overview
[One paragraph summary of what we're building]

## Architecture Decisions
- [Key decision 1 and rationale]
- [Key decision 2 and rationale]

## Architecture Ratchet Matrix
| Boundary | Current Source | Target Shape | Public Seam | Owner Layer | Allowed Dependency Direction | Forbidden Regression | Architecture Test |
|----------|----------------|--------------|-------------|-------------|------------------------------|----------------------|-------------------|
| [Boundary] | [file/symbol read] | [thin vertical slice/deep module rationale] | [export/route/component] | [layer] | [allowed import/call direction] | [import/coupling/state leak that must fail] | [command] |

## Local Full-Schema Proof Plan

- Applies: yes/no
- DB source: sanitized local clone, approved snapshot, schema-only, or N/A
- Safety controls: no production writes and no secret output
- Restore/migration command: `...`
- Proof command: `...`
- Cleanup: `...`

## Task List

### Phase 1: Foundation
- [ ] Task 1: ...
- [ ] Task 2: ...

### Checkpoint: Foundation
- [ ] Tests pass, builds clean

### Phase 2: Core Features
- [ ] Task 3: ...
- [ ] Task 4: ...

### Checkpoint: Core Features
- [ ] End-to-end flow works

### Phase 3: Polish
- [ ] Task 5: ...
- [ ] Task 6: ...

### Checkpoint: Complete
- [ ] All acceptance criteria met
- [ ] Ready for review

## Risks and Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk] | [High/Med/Low] | [Strategy] |

## Open Questions
- [Question needing human input]
```

## Parallelization Opportunities

When multiple agents or sessions are available:

- **Safe to parallelize:** Independent feature slices, tests for already-implemented features, documentation
- **Must be sequential:** Database migrations, shared state changes, dependency chains
- **Needs coordination:** Features that share an API contract (define the contract first, then parallelize)

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll figure it out as I go" | That's how you end up with a tangled mess and rework. 10 minutes of planning saves hours. |
| "The tasks are obvious" | Write them down anyway. Explicit tasks surface hidden dependencies and forgotten edge cases. |
| "Planning is overhead" | Planning is the task. Implementation without a plan is just typing. |
| "I can hold it all in my head" | Context windows are finite. Written plans survive session boundaries and compaction. |

## Red Flags

- Starting implementation without a written task list
- Tasks that say "implement the feature" without acceptance criteria
- No verification steps in the plan
- All tasks are XL-sized
- No checkpoints between tasks
- Dependency order isn't considered
- Exact paths, dependencies, or ownership claims that were never grounded in code actually read
- Deep modules or extracted helpers without a named public seam and architecture ratchet test
- DB/schema claims without local full-schema proof or an explicit blocker/narrowed claim

## Verification

Before starting implementation, confirm:

- [ ] Every task has acceptance criteria
- [ ] Every task has a verification step
- [ ] Task dependencies are identified and ordered correctly
- [ ] The plan is grounded in real files or symbols that were actually read
- [ ] The plan includes a bounded zoom-out map for debugging, refactor, lifecycle/status, or confusing system work
- [ ] Architecture Ratchet Matrix locks public seams, owner layers, allowed dependency direction, forbidden imports, and architecture tests for multi-file work
- [ ] Tasks are thin vertical tracer bullets unless a horizontal foundation task is explicitly justified and independently verifiable
- [ ] Schema/query/data-sensitive plans include a local full-schema Postgres proof plan or a blocking/narrowing decision
- [ ] Lifecycle/status plans enumerate included and excluded states before changing filters, totals, guards, or transitions
- [ ] No task touches more than ~5 files
- [ ] Tasks are vertical tracer bullets, not horizontal layer batches
- [ ] Any HITL task names the exact decision or access it needs
- [ ] Checkpoints exist between major phases
- [ ] The human has reviewed and approved the plan
