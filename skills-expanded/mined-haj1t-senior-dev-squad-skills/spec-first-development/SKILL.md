---
name: spec-first-development
description: "Turns ideas into product specs with user stories, acceptance criteria, and edge cases. Use when writing a spec before starting implementation."
---

# Spec First Development

## Overview

Transform rough ideas into structured product specifications before any code is written. A spec is the single source of truth for implementation, testing, and review. Code written without a spec is technical debt waiting to happen.

**Core principle:** NO CODE WITHOUT A SPEC. Writing code is the last step, not the first.

## The Iron Law

```
NO IMPLEMENTATION WITHOUT AN APPROVED SPEC
```

If you haven't completed all 6 phases below, you cannot write code. Not a single line.

## When to Use

**Use this when:**
- A new feature or component is requested
- A bug report needs root cause analysis before fix
- Before any architecture or implementation work begins
- Requirements are ambiguous or incomplete

**Use this ESPECIALLY when:**
- Someone says "just make it work, we'll spec later" (spec-first prevents 10x rework)
- The feature seems "simple" (simple features have complex edge cases)
- The requester is vague about what they want (spec forces clarity)

**Don't skip when:**
- Under time pressure (a 15-minute spec beats 3 days of wrong implementation)
- Feature seems trivial (trivial features still need acceptance criteria)

## Project Context

Before significant work, check for a project glossary and decision log:
- If `CONTEXT.md` exists, use its ubiquitous-language glossary for all naming, and respect the decisions recorded in `docs/adr/`.
- If they are missing and the work is non-trivial, consider `/senior-dev-squad:grill` (alignment + glossary/ADR capture) or `/senior-dev-squad:setup-senior-dev-squad` first.

## The Six Phases

You MUST complete each phase before proceeding to the next.

### Phase 1: Clarify the Goal

**BEFORE writing anything:**

1. **Identify Target User**
   - Who uses this? What is their context? Expertise level?
   - What device/browser/network are they on?

2. **Define the Problem**
   - What specific problem does this solve? (not the solution)
   - What happens if we don't build this?
   - What's the current workaround?

3. **Establish Success Metrics**
   - How do we objectively know it works?
   - Quantitative: "Load time < 2s", "Success rate > 99%"
   - Qualitative: "Users can complete task without help"

4. **Understand Constraints**
   - Time, budget, tech stack, team size
   - Compliance requirements (GDPR, HIPAA, SOC2)
   - Backward compatibility needs

**Output:** Problem statement with target user, success criteria, and constraints.

### Phase 2: Define Scope

| Section | What to Include |
|---------|----------------|
| **Goals** | What this feature MUST achieve (3-5 items max) |
| **Non-Goals** | Explicitly what this feature will NOT do (prevents scope creep) |
| **User Stories** | "As a [role], I want [goal] so that [reason]" |
| **Acceptance Criteria** | Given/When/Then — independently testable |
| **Edge Cases** | Empty states, error states, boundary values |

```markdown
### Goals
- Users can create a project with a name and optional description
- Users can view a list of their projects

### Non-Goals
- This feature does NOT include project sharing or team collaboration
- This feature does NOT include project deletion (will be separate)
```

### Phase 3: Write Acceptance Criteria

Every criterion MUST be in Given/When/Then format and independently testable:

```gherkin
Scenario: User creates a new project with valid data
  Given user is authenticated
  When user submits the "New Project" form with name "My Project" and description "Test"
  Then a new project is created in the database with name "My Project"
  And user is redirected to the project dashboard
  And a success message "Project created" appears

Scenario: User submits form with empty name
  Given user is on the "New Project" form
  When user submits with an empty name
  Then the form is NOT submitted
  And an error message "Project name is required" appears
  And the name field is highlighted in red
```

**Rule:** Every user story MUST have at least one happy-path scenario AND one error scenario.

### Phase 4: Map All States

Every UI component that fetches data MUST document four states:

```
┌─────────────────────────────────────┐
│  Loading State                      │
│  - What user sees first (skeleton)  │
│  - Timing: show immediately         │
├─────────────────────────────────────┤
│  Empty State                        │
│  - What user sees with no data      │
│  - Clear message + next action CTA  │
├─────────────────────────────────────┤
│  Error State                        │
│  - What user sees on failure        │
│  - Human-readable error + retry CTA │
├─────────────────────────────────────┤
│  Success State                      │
│  - The actual data view             │
│  - Every visual element described   │
└─────────────────────────────────────┘
```

### Phase 5: Data & Security Impact

Document:
- **New models/tables** needed (with fields and types)
- **Existing model changes** (additive only when possible)
- **Migration considerations** (zero-downtime?)
- **Security implications** (new auth checks, PII, audit events)
- **Rate limits** needed

### Phase 6: Dependencies & Risks

```markdown
### Dependencies
- External APIs: [which services must be available?]
- Internal modules: [which code paths are affected?]
- Third-party: [new libraries, SaaS, licenses]
- Team: [frontend, backend, design, QA]

### Risks
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| API rate limit exceeded | Medium | High | Implement retry with backoff |
| Auth provider downtime | Low | Critical | Cached tokens + fallback |
```

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "We'll figure out the details during implementation"
- "The spec is obvious, let's just start coding"
- "I'll write the spec while I code"
- "This feature is too small for a spec"
- "I know what the user wants, no need to document it"
- "Let me code a quick prototype first, spec later"
- No non-goals section written
- Acceptance criteria are vague ("should work", "should be fast")

**ALL of these mean: STOP. Return to the relevant phase.**

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "Can you write that down?" — You didn't document the spec
- "That's not what I meant" — You didn't validate the spec before proceeding
- "What about X?" — You missed an edge case
- "Let's not over-engineer this" — Your spec is too complex, simplify

**When you see these:** STOP. Return to Phase 1.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Small change, no spec needed" | Small changes break production too. A 5-minute spec saves hours. |
| "We'll spec during implementation" | You'll forget edge cases and miss requirements. |
| "I understand what's needed" | Written specs reveal gaps that mental models hide. |
| "Time is tight, skip the spec" | Wrong implementation takes 3x longer to fix. |
| "Specs are for PMs, not engineers" | Engineers who write specs ship faster with fewer bugs. |

## Recommended Chaining

**When complete, recommended next (invoke manually or wire via hooks):**
- `architecture-planner` — transition to architecture after spec is completed
- `edge-case-hunter` — extract edge cases from scenarios in the spec
- `grill` — start automatic discovery if scope is ambiguous

## Related Skills

- **architecture-planner** — use AFTER spec is approved, before implementation
- **test-engineer** — use spec's acceptance criteria as test cases
- **edge-case-hunter** — use to verify spec covers all failure modes

## Verification (Before Proceeding to Architecture)

- [ ] Every user story has at least one acceptance criterion
- [ ] Every acceptance criterion is in Given/When/Then format
- [ ] All four states documented (loading, empty, error, success)
- [ ] Edge cases documented (empty, error, boundary, concurrent)
- [ ] Non-goals are explicitly listed
- [ ] Data model changes identified
- [ ] Security implications assessed
- [ ] Dependencies listed
- [ ] Open questions documented (not hidden)
- [ ] Human partner has reviewed and approved
