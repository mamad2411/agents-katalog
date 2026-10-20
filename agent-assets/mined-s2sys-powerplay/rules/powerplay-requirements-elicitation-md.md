---
name: requirements-elicitation
description: Requirements engineering — user story format, acceptance criteria, INVEST principles, completeness checklist
alwaysApply: false
---

# Requirements Elicitation Standards

Applied when writing feature specifications, requirements documents, or user stories. Ensures every requirement is complete, unambiguous, and testable before development begins.

---

## User Story Format

**Template:**
```
As a [role], I want [feature], so that [benefit].
```

**ALWAYS:**
- Include all three parts: role, feature, and benefit (not optional)
- Role = specific persona ("registered customer", "system administrator", "API consumer"), not generic "user"
- Feature = a single coherent action, not a bundle of actions
- Benefit = measurable business value ("reduce data entry time", "prevent duplicate submissions", "comply with PCI-DSS")

**NEVER:**
- "As a user, I want the system to be faster" (vague role, no testable benefit)
- "As a user, I want to log in, view my dashboard, and export reports" (three stories bundled)
- Stories without an explicit benefit clause ("As a user, I want password reset" — but why?)

### GOOD Example
```
As a registered customer, I want to reset my password via email link,
so that I can regain access without contacting support.
```

### BAD Example
```
As a user, I want better account management.
(Generic role, no specific feature, no measurable benefit, not testable)
```

---

## INVEST Principles

Every user story before entering development must satisfy all six letters of INVEST:

| Letter | Principle | Test Question |
|--------|-----------|---------------|
| I | **Independent** | Can this be built without completing another story first? (no hard dependencies) |
| N | **Negotiable** | Can the implementation details be negotiated until sprint start? |
| V | **Valuable** | Does this deliver clear value to the role named? (avoid "technical debt cleanup") |
| E | **Estimable** | Can the team size this in story points? (if not, it's too vague) |
| S | **Small** | Can it be completed in one sprint (≤ 5 business days)? (XL stories get split) |
| T | **Testable** | Can acceptance criteria be verified by a test? (if not, rewrite the requirement) |

**ALWAYS:**
- Verify all six letters before moving a story to the sprint
- Split stories that fail Small or Testable (most common violations)
- Document why Independent is not achievable when stories have known dependencies (use "Depends on: Story-123" notation)
- REJECT stories that fail Estimable or Testable — do not move them to development

**NEVER:**
- Say "we'll figure out the details during development" for stories that fail INVEST
- Move a story that fails Testable to "In Progress" — if you cannot write a test, the requirement is ambiguous

---

## Acceptance Criteria Format

Use Gherkin (Given/When/Then) for every acceptance criterion. One criterion = one scenario.

**Template:**
```
Given [precondition — system state before action]
When  [action — what the user or system does]
Then  [outcome — what must be true afterward]
And   [additional outcomes, if any]
```

**ALWAYS:**
- Each criterion is a single scenario (no "or" in Given/When/Then)
- "Then" assertions must be observable (what can be verified in the UI/API/database/logs)
- Include happy path, at least two alternative paths, and at least one error scenario per story
- Be exhaustive in the Then clauses — every side effect (email sent, flag set, log entry) must be stated

**NEVER:**
- "Then the system works correctly" (not observable)
- "When the user does various things" (compound action)
- Criteria that depend on implementation details ("Then the database saves a row") — assert observable outcomes ("Then the record appears in the list")
- Mix multiple scenarios in one criterion

### GOOD Example
```
Given a registered customer with a valid email on the login page
When they submit their email and correct password
Then they are redirected to the dashboard
And a session cookie is set with a 24-hour expiry
And a login event is logged with timestamp and IP address
```

### BAD Example
```
Given the user is logged in, when they do stuff, then it works.
(Not observable, multiple scenarios bundled, no specific assertions)
```

---

## Completeness Checklist

Every requirements document must address all six dimensions before moving to development:

- [ ] **Functional requirements** — numbered list (REQ-F-###) of what the system must DO
- [ ] **Non-functional requirements** — performance (response time at Pxx), security (auth model, data classification), scalability (load estimate), availability (uptime SLA)
- [ ] **Edge cases** — boundary values, empty inputs, maximum limits, concurrent access, special characters
- [ ] **Error scenarios** — invalid input, external service unavailable, permission denied, session expired, rate limit exceeded
- [ ] **Security considerations** — who can access this? what data is sensitive (PII/payment/health)? what are authorization rules? what is data classification?
- [ ] **Performance expectations** — stated as measurable thresholds ("< 200ms at P95 under 500 concurrent users"), not feelings ("fast")

---

## Requirement Quality Rules

Write requirements that are:

**ALWAYS — five quality dimensions:**
- **Measurable** — includes a threshold ("< 200ms at P95"), not a feeling ("fast")
- **Testable** — can be verified by a test case; if you cannot write a test, rewrite the requirement
- **Unambiguous** — has exactly one interpretation; uses precise nouns and verbs
- **Atomic** — describes one behavior; split anything joined with "and/or" describing distinct behaviors
- **Traceable** — has a unique ID (REQ-F-001, REQ-NF-002) so it can be referenced in specs, tests, and tickets

**NEVER — these are ambiguity anti-patterns (replace with examples below):**

| Anti-Pattern | Example Bad | Example Good |
|---|---|---|
| "The system should be fast" | "API responses < 200ms at P95 under 500 concurrent users" |
| "The system should be easy to use" | "New users complete onboarding in < 5 minutes with zero support; measured by task completion rate" |
| "Users should be able to manage their data" | "Authenticated users can view, edit, delete their own profile records; users cannot access other users' records" |
| "The system should handle errors gracefully" | "When payment gateway is unavailable, user sees 'Payment service temporarily unavailable. Try again in 5 minutes.' No charge is made." |
| "The system must be scalable" | "System handles 10× current load (5,000 concurrent users) without architectural changes" |

**Ambiguity signal words** (replace with specific outcomes):
- "should" → state what WILL happen, not what's hoped for
- "might" → decide yes or no, document the decision
- "easy" / "user-friendly" → specify task completion time or error rate
- "fast" → specify milliseconds at percentile (P95, P99)
- "many" / "some" / "several" → specify a number or range
- "appropriate" / "reasonable" / "minimal" → define the metric and threshold
- "robust" / "reliable" → specify uptime SLA or error recovery time

---

## Non-Functional Requirements Template

**ALWAYS include all four NFR categories:**

| Category | Example Requirement |
|----------|---------------------|
| **Performance** | API responds in < 200ms at P95 under 500 concurrent users; dashboard loads in < 2 seconds at 256kbps connection |
| **Security** | All PII encrypted at rest (AES-256). All data in transit encrypted (TLS 1.2+). Authentication via OAuth 2.0. Role-based access control (Admin / Manager / ReadOnly). Password reset token expires in 1 hour. |
| **Scalability** | System handles 10× current load (5,000 concurrent users) without architectural changes. Horizontal scaling via load balancer and database replication. |
| **Availability** | 99.9% uptime SLA (< 8.7 hours downtime/year). Graceful degradation when auth service unavailable (read-only mode). RTO: 1 hour, RPO: 5 minutes. |

---

## Summary Checklist

Before handing a requirements document to engineering:

- [ ] All stories follow "As a [role], I want [feature], so that [benefit]" format
- [ ] All stories pass INVEST (split any that don't)
- [ ] All stories have Given/When/Then acceptance criteria (one criterion = one scenario)
- [ ] Each story covers: happy path, 2+ alternative paths, 1+ error scenarios
- [ ] All ambiguous words replaced with measurable thresholds
- [ ] NFRs defined: performance, security, scalability, availability
- [ ] Edge cases documented (empty/null, max limits, special chars, concurrent access)
- [ ] Each requirement has a unique ID (REQ-F-###, REQ-NF-###) for traceability
- [ ] Team has reviewed for completeness, clarity, testability
- [ ] All open questions raised and answers documented

---

**Last Updated**: 2026-04-09 | **SDLC Phase**: 1 of 6 (Requirements)
