---
name: acceptance-criteria-patterns
description: Given/When/Then format, BDD patterns, quality gates, and definition of done templates. Use when writing acceptance criteria for features, defining quality gates, or specifying what "done" means for a development cycle.
---

# Acceptance Criteria Patterns

Acceptance criteria (AC) are the contract between Product and Development. They define what must be true for a feature to be considered complete. Weak AC produces features that technically function but miss the user need. Strong AC produces testable, unambiguous conditions that Development can implement and QA can verify without guessing.

## When to Use This Skill

- Writing acceptance criteria from feature specs and journey maps
- Defining the definition of done for a cycle or feature
- Setting quality gates between pipeline phases
- Reviewing AC for completeness (edge cases, non-functional requirements)
- Translating vague requirements ("it should be fast") into testable conditions

## Core Concepts

### 1. If You Can't Test It, It's Not an AC

Every acceptance criterion must be independently verifiable. "The checkout flow should feel smooth" is not an AC — it's a wish. "The checkout flow completes in under 3 seconds on a 4G connection for 95% of sessions" is an AC.

### 2. AC Covers All States

A feature is not just its happy path. Acceptance criteria must cover:
- Happy path (everything works)
- Unhappy paths (user makes mistakes)
- Edge cases (boundary conditions)
- Error states (system or third-party failures)
- Non-functional requirements (performance, accessibility, security)

### 3. One Condition Per Criterion

Compound acceptance criteria fail silently. "The form validates input AND shows an error message AND allows resubmission" should be three separate criteria. When a criterion has multiple conditions, partial pass/fail is ambiguous.

## Given/When/Then Format

The standard format for writing testable AC:

```
Given [a precondition or context],
When [a user action or event occurs],
Then [the expected outcome].
```

### Examples

**Functional — Happy Path:**
```
Given a user has items in their cart and a valid payment method saved,
When they tap "Place Order",
Then an order is created, a confirmation screen is shown with order ID,
  and a confirmation email is sent within 60 seconds.
```

**Functional — Unhappy Path:**
```
Given a user has items in their cart,
When they submit payment with an expired card,
Then the order is NOT created, an error message is shown identifying the card as expired,
  and the cart contents are preserved.
```

**Edge Case:**
```
Given a user is on the checkout screen,
When they tap "Place Order" twice in rapid succession (within 500ms),
Then only one order is created.
```

**Performance:**
```
Given a user navigates to the product listing page,
When the page loads on a 4G connection,
Then the page reaches First Contentful Paint within 2 seconds for the 95th percentile of sessions.
```

**Accessibility:**
```
Given a user is navigating with a screen reader,
When they reach the checkout form,
Then all form fields have descriptive labels readable by the screen reader,
  and focus order follows the visual layout.
```

## Definition of Done Template

The DoD applies to every feature unless explicitly overridden. It defines the bar every feature must clear before it can ship.

```markdown
# Definition of Done

A feature is DONE when ALL of the following are true:

## Functional Completeness
- [ ] All Must Have acceptance criteria pass
- [ ] All edge cases specified in the edge case registry have defined behavior
- [ ] All error states show user-facing messages (no raw error codes or stack traces)

## Non-Functional Requirements
- [ ] Page load time meets the defined performance criteria
- [ ] All new UI meets WCAG 2.1 AA accessibility standards
- [ ] No new security vulnerabilities introduced (verified by security review)
- [ ] Feature functions correctly across target browsers / devices

## Test Coverage
- [ ] Unit tests written for all new business logic
- [ ] Integration tests written for all new API endpoints
- [ ] E2E test written for the primary happy path
- [ ] Test coverage for the feature is ≥ 80%

## Documentation and Instrumentation
- [ ] Tracking events instrumented per the measurement plan
- [ ] API documentation updated if new endpoints added
- [ ] Feature flags configured if progressive rollout is required

## Review Gates
- [ ] Code review approved by at least one other engineer
- [ ] QA sign-off on all AC
- [ ] Product sign-off that behavior matches spec
```

## Quality Gates

Quality gates are checkpoints between pipeline phases. They prevent defects from propagating downstream where they're more expensive to fix.

### Gate Definitions

```markdown
## Gate: Design → Development

PASS criteria:
- [ ] Feature spec reviewed and approved by engineering
- [ ] Edge case registry complete
- [ ] Acceptance criteria written and reviewed
- [ ] Design briefs delivered for all UI components

FAIL actions:
- Return to Product phase with specific gaps documented
- Development does NOT begin until gate passes

---

## Gate: Development → QA

PASS criteria:
- [ ] All unit and integration tests pass in CI
- [ ] No Critical or High severity lint/security warnings
- [ ] Feature deployed to staging environment
- [ ] Developer self-tested the primary happy path

FAIL actions:
- Return to Development with specific issues
- QA does NOT begin formal testing until gate passes

---

## Gate: QA → Launch

PASS criteria:
- [ ] All Must Have AC verified ✓
- [ ] No Critical or High severity bugs open
- [ ] Performance criteria verified on staging
- [ ] Accessibility audit passed

FAIL actions:
- Return to Development for fixes
- Partial launch (shadow mode / feature flag) if appropriate for severity
```

## AC Review Checklist

When reviewing acceptance criteria for completeness:

- [ ] Does the AC cover the happy path?
- [ ] Does the AC cover the most common unhappy path?
- [ ] Are all edge cases from the edge case registry covered?
- [ ] Are all error states specified with user-facing copy?
- [ ] Are performance requirements included (not just functional)?
- [ ] Are accessibility requirements included?
- [ ] Is each criterion independently testable?
- [ ] Does each criterion have exactly one condition (not compound)?
- [ ] Are all terms in the AC unambiguous? ("fast" vs. "< 2 seconds")

## Common AC Mistakes

| Mistake | Example | Fix |
|---------|---------|-----|
| Not testable | "The UI should be intuitive" | Define: "New users complete onboarding in under 5 minutes without help documentation" |
| Compound criterion | "Validates AND saves AND shows confirmation" | Split into three separate criteria |
| Missing error states | Only specifies success behavior | Add: what happens when each step fails? |
| No performance criteria | Specifies function but not speed | Add latency/throughput/load targets |
| Scope creep in AC | AC describes behavior not in the feature spec | Flag and discuss; don't silently expand scope |

## Best Practices

1. **Write AC before implementation begins** — AC written after the fact justifies what was built, not what was needed
2. **Review AC with Engineering before the cycle starts** — engineers often spot edge cases that Product missed
3. **Keep AC atomic** — one condition per criterion makes test case generation straightforward
4. **Non-functional AC are mandatory, not optional** — performance and accessibility criteria belong in every feature's AC
5. **AC and test cases are not the same thing** — AC defines what must be true; test cases define how to verify it (QA's job)
