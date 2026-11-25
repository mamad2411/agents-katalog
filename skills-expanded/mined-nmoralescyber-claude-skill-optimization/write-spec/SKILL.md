---
name: write-spec
description: Writes a feature spec or PRD from a problem statement, idea, or user request — turns vague intent into a structured document with goals, non-goals, success metrics, acceptance criteria, and phased scope. Make sure to use this skill whenever the user says write a spec, PRD for [feature], document this feature, scope this work, write a feature brief, build a one-pager spec, or describes wanting to formalize a feature decision into a buildable document. Includes scoping discipline (what's in / out), success metrics that aren't vanity, and phased breakdowns for too-big features. Do NOT use for: brainstorming whether to build something (use product-management:product-brainstorming first), updating the roadmap with the spec'd feature (use product-management:roadmap-update), generating user-facing documentation after build (different scope), or sprint planning for the team (use product-management:sprint-planning). Defining characteristic: "convergence on a defined feature, with crisp scope and acceptance criteria."
---

# Write Spec

Feature specifications and PRDs — vague intent → structured, buildable document.

## When to use vs. adjacent product skills

| Use this skill when... | Use a different skill when... |
|---|---|
| Converting a decided idea into a spec | Exploring whether to build it → `product-management:product-brainstorming` |
| Defining scope, success metrics, acceptance criteria | Adding the spec'd feature to roadmap → `product-management:roadmap-update` |
| Writing a PRD for engineering kickoff | Planning the next sprint's stories → `product-management:sprint-planning` |
| Documenting decision made in spec form | Writing customer-facing docs after build → handle directly |

## Standard spec structure

Every spec produced includes ALL of these sections:

```markdown
# Spec: [Feature name]

## Status
[Draft / In review / Approved / Building / Shipped]
**Owner:** [PM]
**Engineering lead:** [Name]
**Design lead:** [Name]
**Last updated:** YYYY-MM-DD

## TL;DR
[One paragraph. What we're building, for whom, why now.]

## Problem
[Specific user problem in their language. Evidence: tickets, interviews, data.]

## Goals
[What success looks like. 2-4 bullet points.]

## Non-goals
[What this is NOT. Bounds the scope explicitly.]

## Success metrics
[Quantifiable. Leading + lagging. Targets where possible.]
| Metric | Today | 30-day target | 90-day target |
|---|---|---|---|
| ... | | | |

## User stories
- As a [persona], I can [capability] so I can [outcome]
- As a [persona], I can [capability] so I can [outcome]

## Acceptance criteria
- [ ] [Specific, testable condition]
- [ ] [Specific, testable condition]

## Out of scope (this iteration)
- [Things explicitly deferred]

## Design notes
[Link to mockups; key UX decisions; states to handle (loading/empty/error/success)]

## Technical notes
[Architecture decisions; API surface; data model changes; performance considerations; security implications]

## Dependencies
[Other teams, services, third-party]

## Risks
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| ... | | | |

## Phased scope (if too big for one ship)
**Phase 1 (week 1-3):** [Minimum lovable version]
**Phase 2 (week 4-6):** [Next-most-valuable additions]
**Phase 3 (week 7+):** [Nice-to-haves]

## Open questions
- [ ] [Question needing decision before build]
- [ ] [Question for engineering to weigh in on]

## Decisions log
| Date | Decision | Why | Decided by |
|---|---|---|---|

## Communication plan
- Engineering kickoff: [date]
- Design review: [date]
- Beta cohort identified: [yes/no]
- Launch comms drafted by: [date]
```

## Goals vs. non-goals (the most important section)

Most specs fail by being too expansive. The non-goals section is where this skill enforces discipline.

For every goal, ask: "What's the OPPOSITE thing we're explicitly NOT doing?"

Examples:
- Goal: Reduce time-to-onboarding for new admin users
- Non-goal: Redesign the admin onboarding for existing users

- Goal: Enable customers to export audit logs in CEF format
- Non-goal: Build a full SIEM integration; build other format exports

- Goal: Support SSO via Okta for enterprise customers
- Non-goal: Support every SAML provider; build SCIM provisioning

A spec without non-goals will scope-creep. Force the section.

## Success metrics that aren't vanity

Bad metric: "Increase engagement"
Good metric: "% of new admin users who complete first useful action within 7 days, measured by [specific event]"

Bad metric: "Better security posture"
Good metric: "Time from credential exposure detection to credential revocation, measured in seconds"

Every metric needs:
- A current baseline (or "to be measured at launch")
- A target with timeframe
- The event/source that will measure it
- A leading indicator and a lagging indicator (where possible)

## Acceptance criteria discipline

Every criterion must be:
- **Specific:** "Page loads in under 2 seconds at 95th percentile" not "fast"
- **Testable:** Either you can write a test for it or it's a UX subjective judgment that needs a different gating mechanism
- **User-observable:** What the user can see/do, not internal implementation

Bad: "API is performant"
Good: "API responds in under 200ms at p99 under 1000 req/sec sustained load"

Bad: "Login works"
Good: "Valid credentials log in within 3 seconds; invalid credentials show error within 1 second"

## Phased scope (when feature is too big)

Most "big" features should ship in phases. The phased breakdown forces:
- **Phase 1 = minimum lovable version** (NOT minimum viable — minimum lovable. Users delight, not tolerate.)
- **Phase 2** = next-most-valuable additions based on Phase 1 learning
- **Phase 3+** = nice-to-haves

If the feature can't be phased, that's a yellow flag for over-scoping.

## Cybersecurity feature spec considerations

For security/cybersec product features, also include:

- **Threat model:** what attacks does this feature enable, defend against, or change the surface for?
- **Compliance impact:** does this affect SOC 2 / ISO / HIPAA / PCI scope?
- **Audit trail:** what user actions need to be logged?
- **RBAC:** who can use this feature? Default permissions?
- **Data classification:** what data does this touch? PII / PHI / PCI / customer data?
- **Failure mode:** what happens if this feature fails? Open or closed?
- **Customer-side trust:** does this require customer to extend trust to us in new ways? If so, document.
- **Disclosure:** does this require customer notification? Updates to security pages, sub-processor list, DPA?

## Risks section discipline

Use likelihood × impact:

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| API breaking change for existing customers | High | High | Deprecation period 6 months + parallel old/new endpoints |
| Performance degradation under high load | Medium | High | Load testing at 2x expected peak before launch |
| Sub-processor change requires customer DPA notification | Certain | Medium | Notification flow built; 30-day notice complies with DPA |

Risks without mitigation aren't risks; they're hopes.

## Anti-patterns

- **Spec as wish-list** — every PM-favorite feature without scope discipline
- **Vague success metrics** — "improve engagement" doesn't define done
- **Missing non-goals** — guarantees scope creep
- **Hand-wavy acceptance criteria** — "works well" isn't testable
- **No phasing on a 6-month feature** — ships late or never
- **Risks ignored** — known risks not in the spec become surprises in build
- **Stakeholder list as audience** — spec for everyone is for no one
- **Spec that contradicts the brainstorm** — convergence should align with exploration; if it doesn't, surface why

## Output

Produces:
1. The full spec in the structure above
2. Open questions surfaced for resolution before build
3. Suggested chain: after spec is approved, chain to `product-management:roadmap-update` (place on roadmap) then `product-management:sprint-planning` (start building)
4. Communication plan with kickoff dates
5. Reviewer signoff fields
