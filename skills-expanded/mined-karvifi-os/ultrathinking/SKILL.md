---
name: ultrathinking
description: Deep requirement decomposition, contradiction detection, assumption elimination, risk-first reasoning
triggers: [ultrathinking, deep analysis, no assumptions, contradictions, requirements unclear, high stakes]
---

# SKILL: UltraThinking

## The Core Problem
Most projects fail before the first line of code because:
1. Requirements were assumed, not confirmed
2. Contradictions went undetected until too late
3. Unknowns were treated as knowns
4. Risk was identified too late to mitigate

UltraThinking eliminates all four.

## The Process (6 phases — never skip one)

### Phase 1: Intent Reconstruction

Extract what is ACTUALLY being asked:

**Step 1.1 — Explicit Requirements**
Write down every stated requirement in plain, unambiguous language.
Remove all vague language:
```
Vague:  "The system should be fast"
Precise: "API endpoints must respond in < 200ms at P95 under 1000 concurrent users"

Vague:  "Support many users"
Precise: "Handle 100,000 daily active users with < 1% error rate"

Vague:  "Good security"
Precise: "OWASP Top 10 compliance, GDPR-compliant data handling, SOC2 ready"
```

**Step 1.2 — Implicit Requirements**
What must be true that nobody said explicitly?
```
If building a payment system → PCI compliance implied
If handling user data → GDPR/CCPA implied
If building for mobile → offline capability likely needed
If replacing existing system → data migration implied
If for enterprise → SSO/SAML probably required
If consumer-facing → accessibility (WCAG) required by law in many jurisdictions
```

**Step 1.3 — Contradictions** (flag every one — do NOT resolve unilaterally)
```
Common contradiction types:
  Speed vs. Cost: "must be very fast" AND "minimal infrastructure cost"
  Security vs. Convenience: "maximum security" AND "frictionless user experience"
  Scope vs. Timeline: "comprehensive feature set" AND "ship in 6 weeks"
  Quality vs. Speed: "zero bugs" AND "ship this week"
  
For each contradiction:
  STATE IT: "Requirement A says X. Requirement B says Y. These conflict."
  ASK: "Which takes priority? What is the acceptable tradeoff?"
  DOCUMENT: The resolution and the reasoning
```

**Step 1.4 — Measurable Outcomes**
Every goal must become testable:
```
"Users should love it" → "SUS score > 75, NPS > 40 within 90 days"
"High availability" → "99.9% uptime SLA (< 8.7 hours downtime/year)"
"Scalable" → "Handle 10x current load with < 20% latency increase"
"Easy to use" → "New user completes core task without help within 5 minutes"
```

### Phase 2: Constraint Matrix

Create a complete constraints table:

```
HARD CONSTRAINTS (cannot be changed — violating = project fails):
┌────────────────────────┬─────────────────────────────────────┐
│ Constraint             │ Evidence / Source                   │
├────────────────────────┼─────────────────────────────────────┤
│ Budget: $50k total     │ Signed contract                     │
│ Launch: June 1         │ Investor commitment                 │
│ GDPR compliance        │ EU customers                        │
│ Python only            │ Existing team expertise             │
└────────────────────────┴─────────────────────────────────────┘

SOFT CONSTRAINTS (strong preferences — changing requires justification):
┌────────────────────────┬─────────────────────────────────────┐
│ Preference             │ Flexibility                         │
├────────────────────────┼─────────────────────────────────────┤
│ React frontend         │ Could change if compelling reason   │
│ AWS deployment         │ GCP acceptable                      │
│ Dark theme first       │ Both themes possible in MVP         │
└────────────────────────┴─────────────────────────────────────┘

UNKNOWNS (things we don't know — must become known before proceeding):
┌────────────────────────┬─────────────────────────────────────┐
│ Unknown                │ How to resolve                      │
├────────────────────────┼─────────────────────────────────────┤
│ Expected peak load     │ Ask product owner, analyze logs     │
│ Integration API format │ Schedule API review session         │
│ Data retention policy  │ Legal review needed                 │
└────────────────────────┴─────────────────────────────────────┘

ASSUMPTIONS (things we're treating as known but haven't confirmed):
┌────────────────────────┬─────────────────────────────────────┐
│ Assumption             │ Risk if wrong / How to verify       │
├────────────────────────┼─────────────────────────────────────┤
│ Users have smartphones │ High risk — validate with research  │
│ Single language (EN)   │ Medium — confirm no i18n needed     │
│ Admin creates accounts │ Low — confirm user self-service     │
└────────────────────────┴─────────────────────────────────────┘
```

### Phase 3: Failure-First Modeling

For EVERY major component, ask these questions before building it:

```
Component: [Name]

How can this FAIL?
  Technical: [specific technical failure modes]
  Human: [user error, misuse, edge cases]
  External: [third-party failure, network, data]
  Business: [assumption proves wrong, requirements change]

How LIKELY is failure?
  Critical risk (will definitely happen): [list]
  High risk (likely to happen): [list]
  Medium risk (might happen): [list]
  Low risk (unlikely but serious): [list]

What is the IMPACT if it fails?
  User impact: [who is affected and how]
  Business impact: [revenue, reputation, legal]
  Technical impact: [data loss, cascading failures]
  Recovery time: [how long to fix]

What PREVENTS or MITIGATES failure?
  Prevention: [design choices that prevent failure]
  Detection: [monitoring, tests, alerts that catch it fast]
  Recovery: [automated fallback, manual recovery process]
  Communication: [who to notify, how fast]
```

### Phase 4: Context Completeness Score

Rate each dimension 0-10, then calculate overall score:

```
Dimension                          Score  Notes
─────────────────────────────────────────────────────────────
Problem clarity (can state in 1 sentence)   __/10
User definition (specific personas)         __/10
Technical requirements (measurable)         __/10
Business requirements (measurable)          __/10
Stack / technology clarity                  __/10
Timeline realism                            __/10
Budget/resource clarity                     __/10
Integration requirements                   __/10
Security/compliance requirements           __/10
Definition of "done"                       __/10
─────────────────────────────────────────────────────────────
TOTAL SCORE:                               __/100

Threshold:
  0-60:  STOP — too many gaps. Ask questions before proceeding.
  61-84: CAUTION — proceed carefully, document assumptions.
  85-100: GO — safe to proceed to planning.
```

### Phase 5: Critical Questions

Generate the minimum set of questions that would unblock implementation:

```
Question format: "[BLOCKER/IMPORTANT/NICE-TO-HAVE] [specific question] — Impact if unknown: [specific consequence]"

Example:
BLOCKER: "What is the maximum acceptable response time for the search feature? 
         Impact if unknown: Cannot design database indexes or caching strategy."

IMPORTANT: "Should users be able to export their data? 
           Impact if unknown: May need to restructure data model retroactively."

NICE-TO-HAVE: "Is there a preferred color scheme?
              Impact if unknown: Will use default design system — easily changed."
```

### Phase 6: Decision Pack

Produce this before handing off to planning:

```markdown
# UltraThinking Decision Pack

## Project: [Name]

## Summary
One paragraph: what we're building, for whom, and why it matters.

## Confirmed Requirements (measurable)
1. [requirement]: measured by [metric]
2. [requirement]: measured by [metric]

## Contradictions Found and Resolved
| Contradiction | Resolution | Trade-off Accepted |
|--------------|-----------|-------------------|
| [conflict] | [resolution] | [what we gave up] |

## Assumptions Made (document explicitly)
| Assumption | Risk if Wrong | Verification Method |
|-----------|--------------|-------------------|
| [assumption] | [impact] | [how to verify] |

## Risk Register
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| [risk] | High/Med/Low | High/Med/Low | [action] |

## Open Questions (blocking)
1. [question] — blocking [phase] — need answer by [date]

## Context Completeness Score: [N]/100

## GO / NO-GO Recommendation
[GO — all gates passed, proceed to planning]
[NO-GO — [specific gaps that must be resolved first]]
```

## When to Run UltraThinking

```
ALWAYS run when:
  ✓ Requirements are described in vague terms
  ✓ Project involves multiple stakeholders
  ✓ Failure has high cost (financial, legal, safety)
  ✓ Timeline is tight (no room for rework)
  ✓ Technology choices are unclear
  ✓ Team has never built this type of system

SKIP only when:
  ✗ Tiny, well-understood change with clear spec
  ✗ Hotfix for known, confirmed bug
```

## Quality checks
- [ ] All explicit requirements converted to measurable outcomes
- [ ] Implicit requirements identified and documented
- [ ] Every contradiction flagged (not resolved unilaterally)
- [ ] Constraint matrix complete (hard / soft / unknown / assumed)
- [ ] Every major component has failure mode analysis
- [ ] Context completeness score ≥ 85 before proceeding
- [ ] Decision pack written and shared before planning starts
