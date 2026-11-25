---
name: estimate-task
description: Break down a feature or task into subtasks with time estimates, risk flags, and dependency ordering. Trigger when the user asks to estimate a task, break down a feature, plan implementation, or says things like "how long would this take", "break this down for me", "estimate this feature", "/estimate-task", "help me scope this", "write a task breakdown", or "how should I approach building this". Also trigger when the user describes a feature and asks about complexity or implementation order.
---

# Estimate Task

Transform a feature description into a structured implementation plan with subtasks, time estimates, risk assessments, and dependency ordering. Thinks like a senior engineer scoping work for a sprint — practical, honest about unknowns, and aware of where surprises hide.

## Trigger Examples

- "/estimate-task"
- "How long would it take to build [feature]?"
- "Break down this feature into tasks"
- "Help me scope this work"
- "Estimate this: [description]"
- "How should I approach building [feature]?"
- "I need to write a ticket for [feature], help me break it down"

## Inputs

- **Feature description** (required) — what needs to be built, as detailed as available
- **Codebase context** (optional) — existing code, tech stack, or architecture constraints
- **Team size** (optional, default: `1`) — how many engineers will work on this
- **Experience level** (optional, default: `mid-senior`) — adjusts estimates:
  - `junior` — 1.5x multiplier, flag more unknowns
  - `mid-senior` — baseline estimates
  - `senior` — 0.8x multiplier, fewer unknowns
- **Include testing** (optional, default: `true`) — whether to include test-writing in estimates

---

## Workflow

### Step 1: Understand the Feature

Before estimating, Claude should:

1. **Clarify ambiguity** — If the description is vague, ask 2-3 targeted questions before proceeding. Don't estimate what you don't understand.
2. **Identify the layers** — What parts of the stack does this touch? (frontend, backend, database, infrastructure, third-party integrations)
3. **Find the edges** — What are the boundary conditions? What happens on error? What about concurrent access? Permissions?
4. **Spot the unknowns** — What does the engineer need to research or prototype before they can estimate confidently?

### Step 2: Decompose into Subtasks

Break the feature into the smallest tasks that can be independently completed and verified. Each subtask should:

- Be completable in ≤ 4 hours (if longer, break it down further)
- Have a clear "done" condition
- Be assignable to one person
- Have its dependencies explicitly listed

**Standard decomposition layers:**

1. **Data model changes** — schema migrations, new models, relationships
2. **Backend logic** — services, business rules, validation
3. **API endpoints** — routes, request/response contracts, error handling
4. **Frontend components** — UI elements, forms, displays
5. **Frontend integration** — API calls, state management, error states
6. **Testing** — unit tests, integration tests, edge case coverage
7. **Infrastructure** — environment variables, deployment config, permissions
8. **Documentation** — API docs, README updates, inline comments for complex logic

### Step 3: Estimate Each Subtask

For each subtask, provide:

- **Time estimate** as a range: `[optimistic] — [likely] — [pessimistic]`
  - Optimistic: everything goes smoothly, no surprises
  - Likely: normal friction, one minor issue
  - Pessimistic: unexpected complexity, debugging, refactoring
- **Confidence level**: High (done this before) / Medium (understand the approach) / Low (need to research)
- **Risk factors**: what could make this take longer than expected

**Estimation heuristics:**
- Simple CRUD endpoint: 1-2 hours
- Complex business logic with edge cases: 2-4 hours
- New UI component from scratch: 2-4 hours
- Third-party API integration: 3-6 hours (API docs are always worse than expected)
- Database migration on existing data: 2-4 hours (includes testing migration)
- Auth/permissions logic: 3-6 hours (security review needed)
- Real-time features (WebSocket/SSE): 4-8 hours
- File upload/processing: 3-6 hours

### Step 4: Generate the Breakdown

```markdown
# Task Breakdown: [Feature Name]

## Overview
**Feature:** [one-sentence description]
**Layers touched:** [Frontend, Backend, Database, Infrastructure]
**Total estimate:** [sum of likely estimates] ([optimistic] — [pessimistic])
**Confidence:** [overall confidence assessment]

---

## Assumptions
- [Assumption 1 — e.g., "Auth system already exists"]
- [Assumption 2 — e.g., "PostgreSQL, no need to set up new DB"]
- [Assumption 3 — e.g., "Design mockups are provided"]

## Open Questions
- [ ] [Question that could significantly change scope]
- [ ] [Question that needs stakeholder input]

---

## Subtasks

### Phase 1: Foundation
_These tasks have no dependencies and should be done first._

#### 1. [Task name]
- **Description:** [What to do and what "done" looks like]
- **Estimate:** [optimistic] — **[likely]** — [pessimistic]
- **Confidence:** [High/Medium/Low]
- **Depends on:** None
- **Risk:** [What could go wrong]

#### 2. [Task name]
- **Description:** [...]
- **Estimate:** [...]
- **Confidence:** [...]
- **Depends on:** None
- **Risk:** [...]

---

### Phase 2: Core Implementation
_These tasks depend on Phase 1 being complete._

#### 3. [Task name]
- **Description:** [...]
- **Estimate:** [...]
- **Confidence:** [...]
- **Depends on:** Task 1, Task 2
- **Risk:** [...]

---

### Phase 3: Integration & Polish
_Connect the pieces and handle edge cases._

#### 4. [Task name]
- **Description:** [...]
- **Estimate:** [...]
- **Confidence:** [...]
- **Depends on:** Task 3
- **Risk:** [...]

---

### Phase 4: Testing & Review
_Verify everything works end-to-end._

#### 5. [Task name]
- **Description:** [...]
- **Estimate:** [...]
- **Confidence:** [...]
- **Depends on:** All previous tasks
- **Risk:** [...]

---

## Summary

| Phase | Tasks | Optimistic | Likely | Pessimistic |
|-------|-------|-----------|--------|-------------|
| Foundation | [n] | [time] | [time] | [time] |
| Core | [n] | [time] | [time] | [time] |
| Integration | [n] | [time] | [time] | [time] |
| Testing | [n] | [time] | [time] | [time] |
| **Total** | **[n]** | **[time]** | **[time]** | **[time]** |

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| [risk] | [H/M/L] | [H/M/L] | [what to do] |

## Dependency Graph

[Text-based DAG showing task dependencies]

```
Task 1 ──┐
          ├──▶ Task 3 ──▶ Task 5 ──▶ Task 7
Task 2 ──┘                  │
                             ▼
Task 4 ──────────▶ Task 6 ──┘
```

## Recommendations

- **Critical path:** [Tasks X → Y → Z are on the critical path. 
  Delay in any of these delays the entire feature.]
- **Parallelize:** [Tasks A and B can be done simultaneously by different engineers]
- **Spike first:** [Task C has low confidence — consider a 2-hour 
  research spike before committing to the estimate]
- **Cut if tight:** [Task D is nice-to-have and can be deferred 
  without blocking the feature]
```

---

## Output Format

- Default: Render in chat as structured markdown
- For complex features (8+ subtasks), also write to `/mnt/user-data/outputs/`
- If codebase context is available, reference specific files and functions in task descriptions

---

## Notes for Claude

- **Honest > precise.** A wide range with a note saying "I'd spike this first" is more useful than a fake-precise number. Software estimation is hard — acknowledge it.
- **Include the boring stuff.** PR review, deployment, environment setup, writing tests — these take real time and are always forgotten in estimates.
- **Flag the traps.** Third-party APIs, file upload, permissions, data migration, timezone handling, email delivery — these are the things that always take 3x longer than expected. Call them out.
- **Decomposition is the skill.** The value isn't the hour counts — it's identifying all the subtasks. A task list that's complete is more valuable than one with precise estimates but missing work.
- **Adjust for context.** If the user says "we have an existing auth system," don't include auth setup. If they say "greenfield project," include infrastructure setup.
- **Think in PRs.** Each phase should roughly correspond to a shippable PR. This helps with code review and incremental delivery.
- **Call out scope creep.** If the feature description implies multiple features, say so. "This is actually 3 features: X, Y, and Z. Here's the breakdown for X. Want me to estimate Y and Z separately?"
