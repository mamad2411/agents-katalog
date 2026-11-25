---
name: spec-driven-development
description: Mandates writing a comprehensive PRD/spec before ANY code is written. Spec must cover objectives, commands, structure, code style, testing strategy, boundaries, success criteria, and be reviewed via spec review gates before implementation begins.
---

# Spec-Driven Development

## Overview

The most expensive bug is the one found during implementation that requires a requirement change. The second most expensive is implementing the wrong thing perfectly.

Spec-driven development eliminates both by enforcing a **single mandatory gate: spec before code.** No branch is created, no file is opened, no function is written until a written specification has been reviewed and approved.

The spec is not a suggestion — it is the contract between intent and implementation. It must be precise enough that a different engineer (or a future you) could implement it without asking questions. It must be bounded enough that scope creep is visible the moment it happens.

## When to Use

| Trigger | Description |
|---------|-------------|
| Any new feature | Anything that changes behavior, adds capability, or modifies existing logic |
| Bug fix with design implications | Fix requires choosing between multiple valid approaches |
| Refactoring | Structural changes that affect interfaces or data flow |
| Architecture decision | Choosing between frameworks, patterns, or infrastructure |
| Public API change | Any modification to a consumer-facing contract |
| Cross-team dependency | Work that another team or system depends on |
| User cannot articulate what they want | Spec process forces clarity | |

**Do NOT use** when: trivial rename, dead code removal, dependency version bump with no behavior change, typo fix in a comment, or any change completable in < 5 minutes with zero ambiguity.

## Spec Structure

Every spec must follow this template. Deviations require explicit justification.

```markdown
# PRD: [Title]

## Objectives
[3-5 measurable objectives. Not features — outcomes.]

## Context
- Problem being solved
- User stories (As [persona], I want [capability] so that [benefit])
- Prior art / existing behavior
- Relevant links (docs, designs, issues)

## Commands & Interface
[How users or systems interact with this. CLI commands, API routes, UI flows.]
- Command signatures
- Input/output schemas
- Error conditions and responses
- Example invocations

## Implementation Approach
### High-Level Design
[Architecture diagram or textual description. Components, data flow, key algorithms.]

### Structure
[File tree of new/modified files.]
```
src/
  features/
    new-feature/
      index.ts
      service.ts
      types.ts
  tests/
    new-feature.test.ts
```

### Data Model
[Schema changes, new types, interfaces. Inline or linked.]

## Code Style & Conventions
[Project-specific conventions this code must follow.]
- Naming conventions (camelCase, PascalCase, kebab-case for files)
- File organization pattern
- Error handling pattern
- Async/await or Promise style
- Import ordering
- Documentation expectations (JSDoc, comments, or nothing)
- Maximum function length, file length, cyclomatic complexity

## Testing Strategy
| Type | Coverage | Framework | Key Scenarios |
|------|----------|-----------|---------------|
| Unit | Core logic, edge cases | Vitest | [list 5-10] |
| Integration | API endpoints, data flow | Supertest | [list 3-5] |
| E2E | Critical user paths | Playwright | [list 1-3] |

- Mocking policy: what can be mocked, what must be real
- Test data strategy: fixtures, factories, or seed data
- Performance threshold: max response time, max memory

## Boundaries & Constraints
- Explicit in-scope
- Explicit out-of-scope
- Performance requirements
- Security requirements
- Accessibility requirements
- Browser/environment support
- Backward compatibility guarantees
- Deprecation plan (if removing something)

## Success Criteria
[Completion checklist. Each item must be verifiable (pass/fail, not subjective).]
- [ ] All acceptance criteria from user stories pass
- [ ] Test coverage >= 90% for new code
- [ ] All existing tests pass
- [ ] Lint passes with no warnings
- [ ] TypeScript strict mode, no errors
- [ ] Bundle size increases by < 5KB
- [ ] Page load time increases by < 50ms
- [ ] Accessibility score >= 95
- [ ] API docs updated
- [ ] CHANGELOG entry added

## Risks & Mitigations
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Risk description | H/M/L | H/M/L | Mitigation strategy |

## Open Questions
- [ ] Question 1 — assigned to: [person]
- [ ] Question 2 — assigned to: [person]
```

## Spec Writing Process

### Step 1: Gather (Collect inputs)
- Interview user (see interview-me skill)
- Review existing code and docs
- Collect any designs, mockups, or references
- List all known constraints upfront

### Step 2: Draft (Write the spec)
- Start with **Objectives** — if you can't write 3-5 measurable objectives, you don't understand the problem
- Fill **Context** next — this is the "why" that justifies everything else
- Write **Boundaries** early — scope control starts here
- Define **Success Criteria** as you write — if you can't define success, don't proceed
- Confirm **Testing Strategy** is adequate for the risk level

Time estimate: 15-60 minutes depending on feature size.

### Step 3: Self-Review

Before presenting to anyone, self-review against these questions:

1. Could a junior engineer implement this without asking me a question?
2. Are all terms defined? No jargon, no ambiguity, no "etc."
3. Is every success criterion pass/fail? No "make it fast" — use "API responds in < 200ms p95."
4. Are the boundaries explicit? "Out of scope" is as important as "in scope."
5. Are the trade-offs documented? Every decision has alternatives listed.

If any answer is no, revise before proceeding.

### Step 4: Review Gate

The spec MUST be reviewed before any code is written. Review types:

| Gate | Who | What They Check | Pass Condition |
|------|-----|-----------------|----------------|
| Design review | Peer or senior engineer | Technical approach, architecture, trade-offs | Approach is sound, no major gaps |
| Product review | Stakeholder or user | Objectives, success criteria, scope | Aligns with intent, no surprises |
| Security review | Security team (if sensitive) | Auth, data handling, exposure | No new vulnerabilities |

**Gate rules:**
- All "Open Questions" must be resolved before code begins
- If any reviewer says "I don't understand X", the spec is not clear enough
- If a reviewer identifies a missing success criterion, add it
- If the review reveals a fundamentally different approach, kill the spec and restart

### Step 5: Spec Freeze

Once approved:
- Spec is committed to `/specs/` in the project repository
- Changes to the spec during implementation require a **spec amendment** (diff review)
- Scope additions trigger a **spec revision** (+1 version number)
- Spec is the source of truth; code must match it

## Anti-Rationalization Table

| Temptation | Why It Happens | Why It's Dangerous | What To Do Instead |
|------------|----------------|--------------------|--------------------|
| "I'll write the spec as I code" | Impatience, excitement to start | Spec becomes after-the-fact documentation, not a guide | Write the spec first. The 30 minutes saves 3 hours of rework. |
| "The change is too small for a spec" | Laziness disguised as efficiency | Small changes compound into architecture erosion | If it modifies behavior, it needs a spec. 10 lines minimum. |
| "I already know what to build" | Overconfidence | You skip the review that catches blind spots | Write it down. The act of writing reveals gaps. |
| "The user will change their mind anyway" | Cynicism from past trauma | Spec still provides a baseline to measure change against | Write the spec as a contract. Track changes. |
| "Specs take too long" | Time pressure | 10x more time spent debugging wrong implementation | Spec time is investment. 3:1 ROI on any non-trivial feature. |
| "We use agile, specs are waterfall" | Misunderstanding of agile | Agile needs a definition of done; spec provides it | A spec is the story acceptance criteria, detailed. |
| "I'll add tests later" | Delivery pressure | Tests never get added; regression risk | Write tests as part of spec commitment |
| "This is exploratory, can't spec it" | Genuine uncertainty | Exploration without scope becomes infinite | Spec the exploration: "I will spend X time investigating Y and report Z" |

## Red Flags

1. Objectives are features, not outcomes — "Add a login page" instead of "Users can authenticate"
2. Success criteria are subjective — "Fast" instead of "< 200ms", "Clean" instead of "No lint errors"
3. Boundaries section is empty — everything is in scope, nothing is excluded
4. Testing strategy is "manual testing" — no automated verification
5. No open questions — the first draft was perfect (it wasn't)
6. Code style section is missing — everyone assumes different conventions
7. Risks are all "Low" — no honest assessment
8. Spec is longer than 5 pages for a simple feature — over-analysis
9. No one reviews it — spec is written, approved, and implemented by same person without feedback
10. Spec is updated silently during implementation — no trace of changes

## Verification

- [ ] **Objectives** written as measurable outcomes, not features
- [ ] **Context** defines the problem, user, and prior art
- [ ] **Commands/Interface** fully specified with examples
- [ ] **Implementation approach** documented with structure, data model, and design
- [ ] **Code style** section captures project conventions
- [ ] **Testing strategy** covers unit, integration, and e2e with key scenarios
- [ ] **Boundaries** include explicit in-scope and out-of-scope
- [ ] **Success criteria** are all pass/fail, timebound, measurable
- [ ] **Risks** assessed with mitigations
- [ ] **Open questions** resolved before code begins
- [ ] **Review gate** passed — at least one other person has reviewed the spec
- [ ] **Spec frozen** — committed, versioned, changes tracked
- [ ] **Spec amendment process** defined for changes during implementation

### Spec Execution Order

```
┌─────────────┐
│ 1. Gather   │ ← Interview, collect inputs
└──────┬──────┘
       ↓
┌─────────────┐
│ 2. Draft    │ ← Write full spec with all sections
└──────┬──────┘
       ↓
┌─────────────┐
│ 3. Self-Review│ ← Against clarity, completeness, testability
└──────┬──────┘
       ↓
┌─────────────┐
│ 4. Review Gate│ ← Design review + product review
└──────┬──────┘
       ↓
┌─────────────┐
│ 5. Freeze   │ ← Commit spec, begin implementation
└─────────────┘
       ↓
┌─────────────┐
│ Implementation │ ← Code must match spec exactly
└─────────────┘
       ↓
┌─────────────┐
│ Verification  │ ← Test against success criteria
└─────────────┘
```
