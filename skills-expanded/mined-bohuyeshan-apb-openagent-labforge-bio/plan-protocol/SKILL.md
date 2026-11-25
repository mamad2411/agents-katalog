---
name: plan-protocol
description: Guidelines for creating and managing implementation plans with citations
category: planning
exposure: standard
---

# Plan Protocol

> **Load this skill** when creating or updating implementation plans.

## TL;DR Checklist

When creating or updating a plan, ensure:

- [ ] YAML frontmatter with `status`, `phase`, `updated`
- [ ] `## Goal` section (one sentence)
- [ ] `## Context & Decisions` table with citations (`ref:delegation-id`)
- [ ] Phases with status markers: `[COMPLETE]`, `[IN PROGRESS]`, `[PENDING]`
- [ ] Tasks with hierarchical numbering (1.1, 1.2, 2.1)
- [ ] Only ONE task marked `← CURRENT`
- [ ] Citations for all research-based decisions

---

## When to Use

1. Starting a multi-step implementation
2. After receiving a complex user request
3. When tracking progress across phases
4. After research that informs architectural decisions

## When NOT to Use

1. Simple one-off tasks → use built-in todos instead
2. Pure research/exploration → use delegations only
3. Quick fixes that don't need tracking
4. Single-file changes with no dependencies

---

## Plan Format

Use `plan_save` with this exact markdown format:

```markdown
---
status: STATUS
phase: PHASE_NUMBER
updated: YYYY-MM-DD
---

# Implementation Plan

## Goal
ONE_SENTENCE_DESCRIBING_OUTCOME

## Context & Decisions
| Decision | Rationale | Source |
|----------|-----------|--------|
| CHOICE | WHY | `ref:DELEGATION_ID` |

## Phase 1: NAME [STATUS_MARKER]
- [x] 1.1 Completed task
- [x] 1.2 Another completed task → `ref:DELEGATION_ID`

## Phase 2: NAME [IN PROGRESS]
- [x] 2.1 Completed task
- [ ] **2.2 Current task** ← CURRENT
- [ ] 2.3 Pending task

## Phase 3: NAME [PENDING]
- [ ] 3.1 Future task
- [ ] 3.2 Another future task

## Notes
- YYYY-MM-DD: Observation or decision `ref:DELEGATION_ID`
```

### Frontmatter Fields

| Field | Values | Description |
|-------|--------|-------------|
| `status` | `not-started`, `in-progress`, `complete`, `blocked` | Overall plan status |
| `phase` | Number (1, 2, 3...) | Current phase number |
| `updated` | `YYYY-MM-DD` | Last update date |

### Phase Status Markers

| Marker | Meaning |
|--------|---------|
| `[PENDING]` | Not yet started |
| `[IN PROGRESS]` | Currently being worked on |
| `[COMPLETE]` | Finished successfully |
| `[BLOCKED]` | Waiting on dependencies |

---

## State Machine

### Plan Lifecycle
```
not-started → in-progress → complete
                         ↘ blocked
```

### Phase Lifecycle
```
[PENDING] → [IN PROGRESS] → [COMPLETE]
                         ↘ [BLOCKED]
```

### Task Lifecycle
```
[ ] unchecked → [x] checked
```

### Critical Rules

1. **Only ONE phase** may be `[IN PROGRESS]` at any time
2. **Only ONE task** may have `← CURRENT` marker at any time
3. **Move `← CURRENT`** immediately when starting a new task
4. **Mark tasks `[x]`** immediately after completing them

---

## Citations & Delegations

### Where Citations Come From

Citations reference delegation research. The flow is:

1. You delegate research: `delegate` to `researcher` or `explore`
2. Delegation completes with a readable ID (e.g., `swift-amber-falcon`)
3. You cite that research in the plan: `ref:swift-amber-falcon`

### When to Cite

| Situation | Action |
|-----------|--------|
| Architectural decision based on research | Add to Context & Decisions table |
| Task informed by research | Append `→ ref:id` to task line |
| Implementation detail from research | Inline citation in Notes |

### How to Find Delegation IDs

- Use `delegation_list()` to see all delegations
- Use `delegation_read("id")` to verify content before citing

### ❌ NEVER

- Make up delegation IDs
- Cite without actually reading the delegation
- Skip citations for research-based decisions

---

## Examples

### ✅ CORRECT: Well-formed plan

```markdown
---
status: in-progress
phase: 2
updated: 2026-01-02
---

# Implementation Plan

## Goal
Add JWT authentication with refresh token support

## Context & Decisions
| Decision | Rationale | Source |
|----------|-----------|--------|
| Use bcrypt (12 rounds) | Industry standard, balance of security/speed | `ref:swift-amber-falcon` |
| JWT with refresh tokens | Stateless auth, mobile-friendly | `ref:calm-jade-owl` |

## Phase 1: Research [COMPLETE]
- [x] 1.1 Research auth patterns → `ref:swift-amber-falcon`
- [x] 1.2 Evaluate token strategies → `ref:calm-jade-owl`

## Phase 2: Implementation [IN PROGRESS]
- [x] 2.1 Set up project structure
- [ ] **2.2 Add password hashing** ← CURRENT
- [ ] 2.3 Implement JWT generation

## Phase 3: Testing [PENDING]
- [ ] 3.1 Write unit tests
- [ ] 3.2 Integration tests

## Notes
- 2026-01-02: Chose bcrypt over argon2 for broader library support `ref:swift-amber-falcon`
```

### ❌ WRONG: Missing frontmatter

```markdown
# Implementation Plan

## Goal
Add authentication
```

**Error:** Plan must have YAML frontmatter with status, phase, updated.

### ❌ WRONG: Multiple CURRENT markers

```markdown
## Phase 2: Implementation [IN PROGRESS]
- [ ] **2.1 Task one** ← CURRENT
- [ ] **2.2 Task two** ← CURRENT
```

**Error:** Only one task may be marked CURRENT.

### ❌ WRONG: Decision without citation

```markdown
## Context & Decisions
| Decision | Rationale | Source |
|----------|-----------|--------|
| Use Redis | It's fast | - |
```

**Error:** Decisions must cite research with `ref:delegation-id`.

### ❌ WRONG: Invalid phase status

```markdown
## Phase 1: Research [DONE]
```

**Error:** Use `[COMPLETE]`, not `[DONE]`. Valid markers: `[PENDING]`, `[IN PROGRESS]`, `[COMPLETE]`, `[BLOCKED]`.

---

## Troubleshooting

| Error Message | Fix |
|---------------|-----|
| "Missing frontmatter" | Add `---\nstatus: in-progress\nphase: 1\nupdated: 2026-01-02\n---` at top |
| "Multiple CURRENT markers" | Remove `← CURRENT` from all but the active task |
| "Invalid citation format" | Use `ref:delegation-id` format (e.g., `ref:swift-amber-falcon`) |
| "Missing goal" | Add `## Goal` section with one-sentence description |
| "Empty phase" | Add at least one task to each phase |
| "Invalid phase status" | Use `[PENDING]`, `[IN PROGRESS]`, `[COMPLETE]`, or `[BLOCKED]` |

---

## Before Saving Checklist

Before calling `plan_save`, verify:

- [ ] **User Confirmation:** Has the user approved this plan?
- [ ] **Discussion Complete:** Have you discussed all key points with the user?
- [ ] **Frontmatter:** Has status, phase, and updated date?
- [ ] **Goal:** Is there a clear, one-sentence goal?
- [ ] **Citations:** Are all research-based decisions cited with `ref:id`?
- [ ] **Single CURRENT:** Is exactly one task marked `← CURRENT`?
- [ ] **Valid markers:** Do all phases use valid status markers?
- [ ] **Hierarchical IDs:** Are tasks numbered correctly (1.1, 1.2, 2.1)?

### User Confirmation Process

**REQUIRED before saving any plan:**

1. **Present the plan** — Show the full plan content to the user
2. **Ask for approval** — "Does this plan look good? Should I save it?"
3. **Wait for response** — Do NOT save until user says yes
4. **Save only after approval** — Call `plan_save` only after user confirms

**Example:**
```
Here's the plan I created:

[Plan content]

Should I save this plan? (yes/no)
```

If user says no, ask what to change and repeat the process.

---

## Task Granularity Standard

**Each task should be completable in 2-5 minutes.**

### Why This Matters

- Small tasks are easier to verify
- Small tasks reduce context switching
- Small tasks make progress visible
- Small tasks enable better error recovery

### How to Break Down Tasks

**Bad (too vague):**
```
- [ ] 2.1 Implement authentication
```

**Good (specific and actionable):**
```
- [ ] 2.1 Create src/auth/middleware.ts with validateToken() function
- [ ] 2.2 Add JWT verification logic to validateToken()
- [ ] 2.3 Write test for expired token rejection
- [ ] 2.4 Write test for invalid token format
- [ ] 2.5 Add middleware to router chain in src/app.ts
```

### Task Breakdown Checklist

Each task should specify:
- **What file** to create or modify
- **What function/component** to add
- **What behavior** to implement
- **How to verify** it works (test or manual check)

### Example: Feature Implementation

**Feature:** Add rate limiting to API

**Bad:**
```
- [ ] 3.1 Add rate limiting
```

**Good:**
```
- [ ] 3.1 Create src/middleware/rate-limiter.ts with sliding window algorithm
- [ ] 3.2 Add RateLimiter class with isAllowed(ip) method
- [ ] 3.3 Write test: verify 429 after 100 requests in 1 minute
- [ ] 3.4 Write test: verify X-RateLimit-Remaining header
- [ ] 3.5 Add rate-limiter middleware to src/app.ts router
- [ ] 3.6 Write integration test: verify rate limiting works end-to-end
```

### Task Breakdown Anti-Patterns

| Anti-Pattern | Problem |
|--------------|---------|
| "Implement feature X" | Too vague, unclear when done |
| "Fix the bug" | No verification step |
| "Update the code" | No specific file or function |
| "Add tests" | No specific test cases |

---

## Two Execution Modes

### Mode A: Self-Contained (Main Agent)

When the main agent (orchestrator/atlas) creates and executes its own plan:

1. Create plan using this protocol
2. Execute tasks sequentially
3. Mark tasks `[x]` as completed
4. Use `verification-before-completion` skill

### Mode B: Delegated (Plan Agent → Work Agent)

When using specialized agents:

1. **Plan Agent (prometheus)** creates the plan
2. **Work Agent (atlas)** executes via `/ol-start-work`
3. Plan file is the cross-session source of truth
4. Work agent updates checkboxes as tasks complete

### Which Mode to Use

| Scenario | Mode |
|----------|------|
| Simple feature, single session | A |
| Complex feature, multiple sessions | B |
| User explicitly asks for plan agent | B |
| Quick implementation | A |
| Need specialized planning | B |
