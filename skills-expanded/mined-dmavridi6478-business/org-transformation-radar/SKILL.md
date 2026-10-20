---
name: org-transformation-radar
description: Diagnostic tool based on McKinsey's 9 organizational shifts across three forces — Technology Disruption (AI readiness, human-AI collaboration, shared services), Economic Disruption (geopolitical adaptation, structural simplification, resource reallocation), and Workforce Shifts (performance ambition, D&I reinvestment, leadership adaptability). Use when auditing an organization's transformation readiness, stress-testing a strategic plan against real market forces, assessing AI adoption maturity, or identifying where an organization is lagging vs. leading peers. Source: McKinsey & Company "Nine Shifts Reshaping Organizations Today."
---

# Org Transformation Radar

Source: McKinsey & Company "Nine Shifts Reshaping Organizations Today."

> Nine specific, measurable shifts — mapped across three forces — that separate organizations building sustained productivity from those still chasing short-term resilience.

## The three forces and nine shifts

### Force 1 — Technology Disruption

| Shift | Market reality | What it means for your org |
|---|---|---|
| AI-enabled organizations | 86% not ready to adopt AI at scale | Most orgs are behind — the window to build AI infrastructure before competitors is closing |
| Human and AI collaboration | Only 1 in 4 expect AI agents as autonomous teammates | Underestimation of AI agents is the norm — orgs that design workflows around them now will have structural advantage |
| Rewriting shared services | 84% plan to expand shared services | Shared services are moving from cost center to capability platform; AI is the driver |

### Force 2 — Economic Disruption

| Shift | Market reality | What it means for your org |
|---|---|---|
| Geopolitical adaptation | 43% say they divested too late, or not at all | Portfolio inertia is the default — deliberate geopolitical scenario planning is rare and advantaged |
| From structure to flow | 2 in 3 say their organizations are overly complex and inefficient | Structural complexity is a tax on speed; simplification is a strategic decision, not just an ops cleanup |
| Focusing on the core | Only 30% reallocate resources enterprise-wide | Resource lock-in is nearly universal — active reallocation is a meaningful differentiator |

### Force 3 — Workforce Shifts

| Shift | Market reality | What it means for your org |
|---|---|---|
| Raising performance ambition | Only 20% see nonfinancial rewards as performance drivers | Most orgs over-index on financial incentives — nonfinancial motivation (autonomy, mastery, purpose) is underused and underpriced |
| Rethinking D&I | Nearly 50% plan to reinvest in D&I | After a period of pullback, D&I investment is returning as an organizational capability, not just a values statement |
| Reinventing leadership | 30% of reflective leaders see quick adaptability | Leadership adaptability is a minority trait — reflective leaders who model fast adaptation outperform |

---

## Copy-paste diagnostic prompt

```
You are an organizational transformation advisor. Use McKinsey's 9 shifts framework to audit the organization below and identify where it is leading, lagging, or absent on each shift.

ORGANIZATION CONTEXT:
- Industry: [FILL IN]
- Size: [FILL IN — headcount, revenue range, or both]
- Current strategic priorities: [FILL IN]
- Known challenges: [FILL IN]
- Any relevant context (recent restructuring, M&A, leadership change): [FILL IN]

Evaluate against each of the 9 shifts across three forces:

TECHNOLOGY DISRUPTION:
1. AI-enabled organizations — Is this org ready to adopt AI at scale? What's missing?
2. Human and AI collaboration — How is AI currently used? Are AI agents embedded in workflows?
3. Rewriting shared services — Are shared services being expanded? Is AI involved?

ECONOMIC DISRUPTION:
4. Geopolitical adaptation — Has the portfolio been deliberately shaped around geopolitical risk?
5. From structure to flow — Is the org overly complex? Where is structural friction highest?
6. Focusing on the core — Is resource reallocation happening deliberately or by inertia?

WORKFORCE SHIFTS:
7. Raising performance ambition — Are nonfinancial motivators actively designed into the culture?
8. Rethinking D&I — Is D&I framed as a capability investment, not compliance?
9. Reinventing leadership — Do leaders model adaptability, or do they protect the status quo?

For each shift, rate the organization: LEADING / ON TRACK / LAGGING / ABSENT
Then produce:
- The 3 shifts with the highest strategic urgency (where delay costs most)
- The 2 shifts where this org could build asymmetric advantage fastest
- One specific action for each of the top 3 urgent shifts
```

---

## Strategic pressure test prompt

```
I am [ROLE] at [COMPANY]. We are about to [STRATEGIC DECISION — e.g. expand into a new market / restructure our org / launch an AI initiative].

Pressure-test this decision against McKinsey's 9 organizational shifts. For each relevant shift, tell me:
1. Is our decision aligned with or against the direction this shift is moving?
2. What risk does this shift create for our plan?
3. What does the market data (e.g. "86% not AI-ready") imply about our competitive position post-decision?

Decision context:
[DESCRIBE THE DECISION IN 2-3 SENTENCES]
```

---

## Related skills

- **business-decision-frameworks**: Prioritization and scoring frameworks for the action planning step
- **multi-agent-debate**: Stress-test a transformation strategy before committing
- **analytical-prompts**: Use Prompt 03 (Hidden Assumptions) to surface what your transformation plan takes for granted
- **quarterly-okr-architect**: Translate shift-specific actions into quarterly OKRs
