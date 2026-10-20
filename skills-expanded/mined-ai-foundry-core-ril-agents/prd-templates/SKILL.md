---
name: prd-templates
description: PRD structure, writing patterns, and success metric definition. Use when authoring a product requirements document, writing a PRFAQ, or defining success criteria for a development cycle.
---

# PRD Templates

A PRD (Product Requirements Document) is the contract between Product and Development for a cycle. A weak PRD produces ambiguous builds, rework, and missed metrics. A strong PRD makes clear what's being built, why, what done looks like, and what's explicitly out of scope.

## When to Use This Skill

- Writing a PRD for an upcoming development cycle
- Defining success metrics for a product initiative
- Scoping a cycle against engineering capacity
- Writing a PRFAQ (press release / FAQ) for a new product direction
- Reviewing a PRD for completeness before planning

## PRD Structure

### Minimal Viable PRD (for small cycles)

```markdown
# PRD: [Feature Name]

## Problem Statement
[1-2 sentences: what user problem are we solving? Who has this problem?]

## Proposed Solution
[What we're building. Not implementation details — the user-facing change.]

## Success Metrics
- Primary: [The one metric that determines if this worked]
- Secondary: [Supporting metrics to watch]
- Guardrails: [Metrics that must NOT get worse]

## Scope

### In Scope
- [Feature or behavior 1]
- [Feature or behavior 2]

### Out of Scope
- [Explicitly excluded items — especially things stakeholders might assume are included]

## Constraints
- Timeline: [Hard deadline if any]
- Technical: [Known technical constraints]
- Regulatory: [Compliance requirements if any]

## Open Questions
- [ ] [Question that needs answering before or during build]
```

### Full PRD (for large or high-stakes cycles)

```markdown
# PRD: [Feature or Initiative Name]

**Author:** [Name]
**Status:** Draft / In Review / Approved
**Cycle:** [Quarter / Sprint range]
**Last updated:** [Date]

---

## 1. Problem Statement

### User Problem
[Who is affected, what's the situation, what's the pain or unmet need]

### Business Problem
[Why this matters from a business perspective — revenue, retention, competitive position]

### Evidence
- [Research finding 1 — with source]
- [Data point 1 — with source]
- [Quote or observation from user research]

---

## 2. Goals and Non-Goals

### Goals
- [What this initiative is trying to achieve]

### Non-Goals
- [What this initiative explicitly does NOT address]

---

## 3. Proposed Solution

### Summary
[2-3 sentence description of what we're building]

### User Experience Overview
[High-level description of what the user will experience. Not a spec — a narrative.]

---

## 4. Success Metrics

| Metric | Baseline | Target | Measurement Method |
|--------|---------|--------|--------------------|
| [Primary metric] | [Current value] | [Target] | [How measured] |
| [Secondary metric] | [Current value] | [Target] | [How measured] |
| [Guardrail metric] | [Current value] | Must not decrease | [How measured] |

**Measurement window:** [How long after launch before evaluating?]

---

## 5. Feature Backlog

Stack-ranked list of features for this cycle. Each item has: description, user story, and priority tier.

### Must Have (blocks launch)
| # | Feature | User Story |
|---|---------|-----------|
| 1 | [Feature] | As a [user type], I want [capability] so that [outcome] |

### Should Have (strong preference, deprioritize if capacity is tight)
| # | Feature | User Story |
|---|---------|-----------|

### Could Have (nice to have, cut if needed)
| # | Feature | User Story |
|---|---------|-----------|

### Won't Have This Cycle (explicitly deferred)
| Feature | Reason for Deferral |
|---------|-------------------|

---

## 6. Constraints and Dependencies

### Technical Constraints
- [Constraint 1]

### External Dependencies
- [Team / Service / API we depend on]

### Timeline Constraints
- [Hard dates and why they're hard]

---

## 7. Assumptions

| Assumption | Validation Status | Risk if Wrong |
|-----------|------------------|---------------|
| [Assumption 1] | Validated / Unvalidated | [Impact] |
| [Assumption 2] | Validated / Unvalidated | [Impact] |

---

## 8. Open Questions

- [ ] [Question] — Owner: [Name] — Due: [Date]
```

## PRFAQ Format

The PRFAQ (Press Release / FAQ) is Amazon's method for defining a product by writing the announcement first. It forces clarity about customer benefit before diving into requirements.

```markdown
# Press Release: [Product/Feature Name]

**FOR IMMEDIATE RELEASE**

**[Company] Launches [Feature], Enabling [Customer Benefit]**

[City, Date] — [Company] today announced [Feature], a new capability that [one-sentence value proposition]. Starting today, [user type] can [key action], [outcome].

"[Quote from a hypothetical satisfied customer describing the benefit in their words]"

[Feature] addresses [the problem] that [affected users] have faced with [current state]. With [Feature], users can now [key capability 1] and [key capability 2], resulting in [measurable outcome].

[Feature] is available [to whom, when, how].

---

# Frequently Asked Questions

**Q: Who is this for?**
A: [Target user description]

**Q: What problem does it solve?**
A: [Problem statement in user language]

**Q: How does it work?**
A: [User-facing explanation, no technical jargon]

**Q: What does it NOT do?**
A: [Explicit scope limitations]

**Q: How will users find and start using it?**
A: [Discovery and activation path]

**Q: How will we know if it's working?**
A: [Success metrics in plain language]
```

## Success Metric Definition

### Metric Hierarchy

```
North Star Metric
└── Primary Success Metric (for this initiative)
    ├── Leading Indicator (early signal, visible within days/weeks)
    └── Lagging Indicator (confirms success, weeks/months)
        └── Guardrail Metrics (must not degrade)
```

### Metric Quality Checklist

A well-defined metric is:
- [ ] **Measurable:** Can be tracked with existing or addable instrumentation
- [ ] **Attributable:** Can be connected to this feature specifically (not confounded)
- [ ] **Time-bound:** Has a defined measurement window
- [ ] **Baselined:** Has a current value to compare against
- [ ] **Targeted:** Has an explicit success threshold

### Common Metric Mistakes

| Mistake | Example | Fix |
|---------|---------|-----|
| Vanity metric | "Increase page views" | Tie to a business outcome: "Increase checkout conversion" |
| Unmeasurable | "Improve user happiness" | Define: "Increase NPS from 32 to 40" |
| Too broad | "Improve retention" | Scope to cycle: "Increase 30-day retention for new users acquired via organic search" |
| No baseline | "Achieve 70% task completion" | Always document current baseline |

## Best Practices

1. **Write the out-of-scope section first** — it's the hardest and most important part
2. **Define guardrail metrics** — the things that must not get worse are as important as the success metrics
3. **Open questions are features too** — unresolved questions in the PRD become rework during the cycle
4. **PRD is a living document** — update it as decisions are made; it's the record of what was agreed
5. **Write for development agents as the audience** — if something would require a clarifying question during build, it's not specific enough
