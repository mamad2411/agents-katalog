---
name: user-story-writing
description: "Generates user stories with acceptance criteria, edge cases, and definition of done. Supports splitting epics into right-sized stories using the INVEST criteria. Based on Mike Cohn's user story methodology."
category: execution
default_depth: standard
---

# User Story Writing

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

Generates user stories with acceptance criteria, edge cases, and definition of done. Supports splitting epics into right-sized stories using the INVEST criteria. Based on Mike Cohn's user story methodology.

## When to Use

- Breaking down PRD requirements into implementable work items
- Sprint planning and backlog grooming
- Ensuring engineering, design, and QA share the same understanding of "done"
- Training teams on effective story writing

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | Trivial story with obvious behavior (e.g., copy change, config toggle) | Story Format, Acceptance Criteria (2 criteria minimum), Definition of Done |
| **Standard** | Typical feature story for sprint planning | All sections |
| **Deep** | High-complexity story with multiple personas, integrations, or compliance requirements | All sections + data contract specification, cross-persona impact matrix, regression test plan |

**Omit rules:** At Light depth, skip Edge Cases & Error States table and Story Splitting. Reduce acceptance criteria to 2 (happy path + one error path).

## Key Concepts

### INVEST Criteria

Every story should be:
- **I**ndependent, Can be built and delivered separately from other stories
- **N**egotiable, Details can be discussed; it's not a rigid contract
- **V**aluable, Delivers value to a user or stakeholder
- **E**stimable, Team can estimate the effort required
- **S**mall, Completable within one sprint
- **T**estable, Clear criteria to verify it works

## Framework

### Step 1: Story Format

```
As a [persona],
I want to [action/capability],
So that [benefit/outcome].
```

**Rules:**
- The persona should be specific (not "a user", use named personas)
- The action should describe a goal, not a UI interaction
- The benefit must be from the user's perspective

**Good:** "As a hiring manager, I want to filter candidates by years of experience, so that I can quickly find qualified applicants for senior roles."

**Bad:** "As a user, I want a dropdown, so that I can select things."

### Step 2: Acceptance Criteria

Use Given/When/Then format for testable criteria:

```markdown
### Acceptance Criteria

**AC1: [Scenario name]**
- Given [precondition]
- When [action]
- Then [expected result]

**AC2: [Scenario name]**
- Given [precondition]
- When [action]
- Then [expected result]

**AC3: [Negative / edge case]**
- Given [precondition]
- When [invalid action or edge condition]
- Then [expected error handling / graceful behavior]
```

**Rules:**
- Minimum 3 acceptance criteria per story (happy path, alternate path, error path)
- Each criterion must be independently testable
- Include data boundaries (max length, empty states, null values)
- Include permission/access scenarios if relevant

### Step 3: Edge Cases & Error States

```markdown
### Edge Cases
| Scenario | Expected Behavior |
|---|---|
| [Empty state, no data] | [What the user sees] |
| [Maximum data, 10,000 items] | [Performance expectation] |
| [Concurrent editing] | [Conflict resolution behavior] |
| [Network failure mid-action] | [Recovery behavior] |
| [Invalid input] | [Validation message] |
```

### Step 4: Definition of Done

```markdown
### Definition of Done
- [ ] All acceptance criteria pass
- [ ] Edge cases handled per specification
- [ ] Unit tests written and passing
- [ ] Integration tests updated
- [ ] Accessibility review complete (keyboard nav, screen reader)
- [ ] Performance within acceptable thresholds
- [ ] Code reviewed and approved
- [ ] Design review complete
- [ ] Documentation updated (if user-facing)
- [ ] Feature flag configured (if applicable)
```

### Step 5: Story Splitting (when stories are too large)

**Splitting strategies:**
1. **By workflow step**, Registration → Login → Profile setup
2. **By data variation**, Text input → File upload → Rich text
3. **By operation**, Create → Read → Update → Delete
4. **By role**, Admin view → Member view → Guest view
5. **By platform**, Web → Mobile → API
6. **By happy path vs. edge case**, Core flow → Error handling → Bulk operations

**Template for split stories:**
```markdown
## Original Epic: [Epic name]

### Story 1: [Core happy path]
As a [persona], I want to [simplest version], so that [core value].
Estimate: [S/M]

### Story 2: [Variation or extension]
As a [persona], I want to [additional capability], so that [additional value].
Estimate: [S/M]
Depends on: Story 1

### Story 3: [Edge cases and error handling]
As a [persona], I want [graceful handling of X], so that [I don't lose work / get confused].
Estimate: [S]
Depends on: Story 1
```

## Minimum Evidence Bar

**Required inputs:** A defined persona, a user need or job-to-be-done, and enough context to specify expected behavior (PRD, design spec, or documented user research).

**Acceptable evidence:** PRD requirements, design mockups, user interview notes, support ticket patterns, or an approved epic with scope definition.

**Insufficient evidence:** If the persona is undefined or the user need is assumed without evidence, produce a partial artifact with unanswered sections marked `[TBD, requires: user research or persona definition]` and flag the artifact as draft-only.

**Hypotheses vs. findings:**
- **Findings:** Persona definition, core acceptance criteria, and known system constraints must be grounded in evidence.
- **Hypotheses:** Edge case severity, performance thresholds, and effort estimates are hypotheses -- label them as such until validated by engineering and QA review.

## Output Format

For each user story, produce:
1. **Story statement**, As a / I want to / So that
2. **Acceptance criteria**, Given/When/Then for each scenario
3. **Edge cases**, table of scenarios and expected behaviors
4. **Definition of done**, checklist
5. **Estimation notes**, dependencies, risks, unknowns

**Shipwright Signature (required closing):**
6. **Decision Frame**, story readiness recommendation (ready for sprint / needs grooming / needs split), trade-off, confidence with evidence quality, owner, decision date, revisit trigger
7. **Unknowns & Evidence Gaps**, undefined edge case behaviors, missing design specs, unconfirmed performance thresholds
8. **Pass/Fail Readiness**, PASS if the story meets INVEST criteria, the acceptance criteria cover the intended behavior and material stated boundaries or error paths, and the persona is evidence-based. At Light depth, cover the main behavior and any material error path without inventing edge cases. FAIL if the persona is generic ("a user"), acceptance criteria are untestable, or the story is too large for one sprint.
9. **Recommended Next Artifact**, Which Shipwright skill to run next and why

## Common Mistakes to Avoid

- **Stories that are tasks**, "Set up database table" is a task, not a user story
- **Missing the "so that"**, Without the benefit, you can't evaluate trade-offs
- **Acceptance criteria that duplicate implementation**, Describe *what*, not *how*
- **Stories too large to estimate**, If it can't fit in a sprint, split it
- **Ignoring unhappy paths**, Error states and empty states are where UX quality lives

## Weak vs. Strong Output

**Weak:**
> AC1: User can upload a file. AC2: File is saved.

No preconditions, no boundaries, no error path -- QA cannot write a test from this.

**Strong:**
> AC1: **Happy path upload.** Given a logged-in hiring manager on the candidate profile page, when they upload a PDF or DOCX under 10MB, then the file appears in the Documents tab within 3 seconds and a confirmation toast displays. AC2: **Oversized file.** Given the same context, when they upload a file over 10MB, then the upload is rejected with the message "File must be under 10MB" and no partial file is saved.

Specifies persona, precondition, format constraints, performance expectation, and error behavior -- each criterion is independently testable.
