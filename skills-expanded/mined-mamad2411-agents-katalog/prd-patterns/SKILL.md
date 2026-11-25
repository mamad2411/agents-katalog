---
name: prd-patterns
description: "When to activate: PRD, product requirements document, feature spec, functional spec, requirements writing, acceptance criteria, edge cases"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: business
  domain: product
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# PRD Patterns

## PRD Structure Template

```markdown
# [Feature Name] PRD

**Status**: Draft | In Review | Approved | Shipped
**Author**: [Name]
**Reviewers**: [Engineering Lead], [Design Lead], [Data], [Legal if needed]
**Last Updated**: YYYY-MM-DD
**Target Release**: Q[X] YYYY

---

## 1. Problem Statement
One paragraph. What user pain exists? What evidence supports it?

## 2. Goals & Success Metrics
- Goal 1: [Outcome, not output]
- Success metric: [Specific measurable target with baseline]

## 3. Non-Goals
- Explicitly exclude scope to prevent creep

## 4. User Stories
[See user-stories.md for format]

## 5. Functional Requirements
FR-001: [Requirement]
FR-002: [Requirement]

## 6. Non-Functional Requirements
NFR-001: Latency < 200ms at p95
NFR-002: Availability 99.9%

## 7. UX/Design
[Figma link] [Key screens described]

## 8. Technical Considerations
[Architecture notes, dependencies, risks]

## 9. Edge Cases & Error States
[Table of edge cases]

## 10. Analytics Plan
[Events to instrument]

## 11. Launch Plan
[Phased rollout, feature flags, comms]

## 12. Open Questions
| Question | Owner | Due |
|----------|-------|-----|
```

## Acceptance Criteria Writing

### GIVEN / WHEN / THEN Format
```
GIVEN [context/precondition]
WHEN [action taken]
THEN [expected outcome]
AND [additional assertion]

Example:
GIVEN a user is logged in with a free plan
WHEN they click "Export to CSV"
THEN they see an upgrade modal
AND the modal shows Pro plan features
AND clicking "Upgrade" redirects to /billing
```

### Checklist Format (simpler features)
```
AC-001: User can filter by date range
  - [ ] Start date defaults to 30 days ago
  - [ ] End date defaults to today
  - [ ] Invalid range (start > end) shows inline error
  - [ ] Maximum range: 365 days; exceeding shows error message
  - [ ] Empty result set shows empty state with CTA
```

## Edge Cases Documentation

### Edge Case Table
| Scenario | Input | Expected Behavior | Priority |
|----------|-------|-------------------|----------|
| Empty state | No data returned | Show empty state UI with CTA | P0 |
| Network error | API timeout > 5s | Show retry toast, do not lose data | P0 |
| Concurrent edit | Two users edit same record | Last-write-wins with timestamp | P1 |
| Invalid characters | SQL injection attempt | Sanitize input, reject gracefully | P0 |
| Max payload | File > 10MB upload | Show size limit error before upload | P1 |
| Session expired | Token expires mid-flow | Redirect to login, preserve intent | P0 |

### Error States Checklist
- [ ] 400 Bad Request: show user-friendly validation message
- [ ] 401 Unauthorized: redirect to login
- [ ] 403 Forbidden: show "you don't have access" message
- [ ] 404 Not Found: show 404 page with navigation
- [ ] 429 Rate Limited: show "too many requests, try again in X seconds"
- [ ] 500 Server Error: show generic error with support link
- [ ] Network offline: show offline banner, queue actions if feasible

## Requirement Writing Rules

### DO
- Use "the system SHALL" for mandatory requirements
- Use "the system SHOULD" for recommended
- Use "the system MAY" for optional
- Reference exact UI element names from design
- Include specific numbers (thresholds, limits, timeouts)
- Attach Figma links to specific frames

### DON'T
- Write vague requirements: "the page should load fast" → "p95 < 2s"
- Combine multiple behaviors in one requirement
- Leave decisions open: "TBD" in approved PRDs is a blocker
- Describe implementation, only describe behavior

## Stakeholder Sign-Off Process

### Review Stages
```
1. Author Draft (Day 0)
   → Self-review against checklist below

2. Design Review (Day 1-2)
   → UX completeness, design feasibility

3. Engineering Review (Day 3-5)
   → Technical feasibility, estimates, NFRs

4. Data Review (Day 5-6)
   → Analytics plan completeness, metric definitions

5. Legal/Compliance (if needed, Day 5-7)
   → Privacy, regulatory requirements

6. PM/Leadership Approval (Day 7-10)
   → Priority alignment, resource commitment

7. Kickoff Meeting
   → All stakeholders aligned, questions resolved
```

### PRD Self-Review Checklist
- [ ] Problem clearly stated with supporting evidence (qualitative + quantitative)
- [ ] Goals are outcomes, not outputs
- [ ] Success metrics have baseline and target values
- [ ] Non-goals explicitly listed
- [ ] All user roles/personas addressed
- [ ] Every functional requirement has at least one acceptance criterion
- [ ] All edge cases documented
- [ ] Error states defined
- [ ] NFRs specified (performance, availability, security)
- [ ] Analytics instrumentation plan included
- [ ] Dependencies on other teams identified
- [ ] Rollout plan defined (flag? % rollout? which segments?)
- [ ] Open questions resolved or assigned owners

## PRD Status Definitions

| Status | Meaning |
|--------|---------|
| `Draft` | Author working, not ready for review |
| `In Review` | Circulating to stakeholders |
| `Revision Needed` | Feedback received, author updating |
| `Approved` | All required sign-offs obtained |
| `In Progress` | Engineering actively building |
| `Shipped` | Feature live in production |
| `Deprecated` | Feature killed or superseded |

## Minimal PRD (for small features)

For < 2 sprint features, use this lighter format:
```markdown
## What
[1-2 sentence description]

## Why
[Problem + evidence]

## How (Behavior)
- [Bullet list of user-visible behaviors]

## Acceptance Criteria
- [ ] AC1
- [ ] AC2

## Not included
- [Explicit scope exclusions]

## Metrics
- Primary: [metric]
- Secondary: [metric]
```
