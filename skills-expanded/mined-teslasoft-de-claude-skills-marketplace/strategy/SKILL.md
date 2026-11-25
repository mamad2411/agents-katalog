---
name: strategy
description: |
  Develop UX strategy, metrics, and organizational alignment. Use for UX vision, roadmaps,
  maturity assessment, DesignOps, HEART/CASTLE metrics, north star metric, experience canvas,
  UX OKRs, UX ROI calculation, stakeholder alignment, agentic UX, and delegative UI patterns.
version: 1.0.0
last_updated: 2026-04-29
---

# UX Strategy

A systematic approach to aligning user experience with business objectives, measuring UX value, and building organizational design capability.

## When to Use

- Defining UX vision and North Star metrics
- Creating experience roadmaps aligned with business goals
- Assessing and improving UX maturity
- Establishing DesignOps practices
- Measuring UX impact with HEART/CASTLE frameworks
- Communicating UX ROI to stakeholders
- Building stakeholder alignment for UX initiatives

## When NOT to Use

- Creating wireframes or prototypes (use UX Design skills)
- Conducting usability testing sessions (use UX Research skills)
- Designing UI components (use UI Design skills)
- Building design systems (use Design System skills)

---

## Quick Start (Happy Path)

1. **Assess current state** - Use UX Maturity Model to baseline organizational capability
2. **Define UX vision** - Create aspirational experience statement aligned with business goals
3. **Establish North Star metric** - Select single metric capturing core user value
4. **Select measurement framework** - HEART for products, CASTLE for enterprise apps
5. **Create experience roadmap** - Sequence initiatives by business impact
6. **Build stakeholder alignment** - Present ROI case to executives
7. **Implement DesignOps** - Scale through process and tool optimization

---

## Core Procedure

### Step 1: UX Maturity Assessment

Evaluate organizational design capability using the 6-level maturity model.

**Maturity Levels:**

| Level | Name | Characteristics |
|-------|------|-----------------|
| 1 | Absent | No recognized UX function |
| 2 | Limited | Sporadic UX involvement |
| 3 | Emergent | Dedicated UX resources |
| 4 | Structured | Established research processes |
| 5 | Integrated | UX in leadership decisions |
| 6 | User-Driven | UX drives business strategy |

**Checkpoint:** Document current level and target level with timeline.

See [Maturity Model Details](references/maturity.md) for advancement strategies.

### Step 2: Define UX Vision and North Star

Create an aspirational statement describing the ideal future experience.

**UX Vision Characteristics:**
- Inspirational yet achievable
- User-centered, not feature-focused
- Aligned with business strategy
- Time-bound (typically 2-5 years)

**Example:** "Within 3 years, our platform will anticipate user needs before they arise, reducing cognitive load by 60% and making complex tasks feel effortless."

**North Star Metric by Product Type:**

| Product Type | North Star Metric |
|--------------|-------------------|
| E-commerce | Weekly purchasing customers |
| SaaS | Weekly active teams |
| Media | Total watch time |
| Marketplace | Transactions per week |
| Productivity | Weekly active documents |

**Checkpoint:** Vision statement reviewed by stakeholders; North Star approved by leadership.

See [Frameworks Reference](references/frameworks.md) for OKRs and roadmapping.

### Step 3: Select Measurement Framework

Choose the appropriate metrics framework based on context.

**HEART Framework** (Google) - For products with user choice:

```
+-------------+------------------+------------------------+
|  Category   |     Signal       |        Metric          |
+-------------+------------------+------------------------+
| Happiness   | Survey responses | NPS, CSAT, SUS score   |
| Engagement  | Feature usage    | DAU/MAU, sessions/user |
| Adoption    | Onboarding       | Activation rate        |
| Retention   | Return visits    | Weekly retention, churn|
| Task Success| Completions      | Success rate, time     |
+-------------+------------------+------------------------+
```

**CASTLE Framework** (NN/g) - For mandatory-use enterprise apps:

```
+----------------+--------------------------------+
|   Dimension    |         Measures               |
+----------------+--------------------------------+
| Cognitive Load | Mental effort for tasks        |
| Actionability  | Ability to take efficient action|
| Satisfaction   | User contentment               |
| Trust          | Confidence in system reliability|
| Learnability   | Ease of acquiring new skills   |
| Efficiency     | Speed and resource optimization|
+----------------+--------------------------------+
```

**Checkpoint:** Metrics framework selected; Goals-Signals-Metrics documented for each category.

See [Metrics Reference](references/metrics.md) for detailed implementation.

### Step 4: Create Experience Roadmap

Build strategic design roadmap connecting UX initiatives to business outcomes.

**Roadmap Components:**
1. **User Segments** - Who are we designing for?
2. **Key Journeys** - Critical user flows to optimize
3. **Initiative Prioritization** - Impact vs. effort matrix
4. **Quarterly Themes** - Focus areas per quarter
5. **Dependency Mapping** - Technical and research dependencies

**Prioritization Framework:**

```
           High Impact
               |
    Quick Wins | Strategic Bets
               |
  Low Effort --+-- High Effort
               |
    Fill-ins   | Big Rocks (defer)
               |
           Low Impact
```

**Checkpoint:** Roadmap reviewed with Product and Engineering; dependencies identified.

### Step 5: Build Stakeholder Alignment

Communicate UX value in business language to executives.

**ROI Communication Framework:**

```
UX Improvement        Business Translation       Outcome
-----------------------------------------------------------------
Reduced time-on-task  Lower support costs        Cost savings
Higher completion     Higher conversion          Revenue impact
Fewer errors          Reduced rework             Efficiency gains
Better NPS/CSAT       Improved retention         Customer value
```

**Key Statistics for Executive Presentations:**
- Forrester: 351% ROI from UX optimization
- McKinsey: 32% faster revenue growth for design leaders
- Every $1 on UX returns up to $100 in revenue

**Checkpoint:** Executive presentation delivered; budget/resources approved.

See [Stakeholder Communication](references/stakeholders.md) for presentation strategies.

### Step 6: Implement DesignOps

Scale UX organization through operational excellence.

**DesignOps Quick Wins:**
1. Organize what is messy (file structure, asset management)
2. Build simple rituals (design reviews, critique sessions)
3. Create visibility into design work (dashboards, status tracking)
4. Standardize design-dev handoff (specs, documentation)
5. Implement design system governance (contribution, review)

**DesignOps Value:** Organizations with mature DesignOps report 228% higher ROI (NN/g).

**Checkpoint:** DesignOps pilot initiative launched; initial metrics established.

See [Maturity Reference](references/maturity.md) for DesignOps maturity levels.

---

## UX Strategy Framework

The following diagram illustrates how UX Strategy connects business objectives to user outcomes.

```
                    +-------------------+
                    |   Business Layer  |
                    +-------------------+
                    | Business Vision   |
                    | Business Objectives|
                    | KPIs              |
                    +---------+---------+
                              |
                              v
                    +-------------------+
                    | UX Strategy Layer |
                    +-------------------+
                    | UX Vision         |
                    | North Star Metric |
                    | Experience Roadmap|
                    +---------+---------+
                              |
                              v
                    +-------------------+
                    |  Execution Layer  |
                    +-------------------+
                    | Design System     |
                    | User Research     |
                    | Prototyping       |
                    +---------+---------+
                              |
                              v
                    +-------------------+
                    | Measurement Layer |
                    +-------------------+
                    | HEART/CASTLE      |
                    | NPS/CSAT          |
                    | Task Completion   |
                    +---------+---------+
                              |
              Feedback Loop   |
                    +---------+
                    |
                    v
            [Back to Business Layer]
```

---

## HEART Framework Detail

Google's HEART framework with Goals-Signals-Metrics approach:

```
+===========================================================+
|                    HEART FRAMEWORK                        |
+===========================================================+
|                                                           |
|   H A P P I N E S S                                       |
|   +-------------------------------------------------+     |
|   | Goal: Users find the product delightful         |     |
|   | Signal: Survey responses, sentiment             |     |
|   | Metrics: NPS, CSAT, SUS score                   |     |
|   +-------------------------------------------------+     |
|                                                           |
|   E N G A G E M E N T                                     |
|   +-------------------------------------------------+     |
|   | Goal: Users actively use core features          |     |
|   | Signal: Feature usage frequency                 |     |
|   | Metrics: DAU/MAU ratio, sessions per user       |     |
|   +-------------------------------------------------+     |
|                                                           |
|   A D O P T I O N                                         |
|   +-------------------------------------------------+     |
|   | Goal: New users successfully onboard            |     |
|   | Signal: Completing setup flow                   |     |
|   | Metrics: Activation rate, feature adoption %    |     |
|   +-------------------------------------------------+     |
|                                                           |
|   R E T E N T I O N                                       |
|   +-------------------------------------------------+     |
|   | Goal: Users continue using the product          |     |
|   | Signal: Return visits over time                 |     |
|   | Metrics: Weekly retention, churn rate           |     |
|   +-------------------------------------------------+     |
|                                                           |
|   T A S K   S U C C E S S                                 |
|   +-------------------------------------------------+     |
|   | Goal: Users complete key workflows              |     |
|   | Signal: Successful task completion              |     |
|   | Metrics: Success rate, time-on-task, errors     |     |
|   +-------------------------------------------------+     |
|                                                           |
+===========================================================+
```

---

## Definition of Done

A UX Strategy engagement is complete when:

- [ ] UX maturity level documented with improvement roadmap
- [ ] UX vision statement approved by stakeholders
- [ ] North Star metric defined and measurement in place
- [ ] HEART or CASTLE metrics framework implemented
- [ ] Experience roadmap aligned with product roadmap
- [ ] Executive presentation on UX ROI delivered
- [ ] DesignOps pilot initiative launched

---

## Guardrails

### Security & Permissions

- **Required tools:** Read (for strategy documents), Write (for deliverables)
- **Confirmations:** Before sharing sensitive competitive analysis externally
- **Trust model:** Treat user research data as confidential

### Forbidden Actions

- Do not execute usability tests (that's UX Research scope)
- Do not design wireframes or prototypes (that's UX Design scope)
- Do not implement design system components (that's UI/Design scope)
- Do not skip stakeholder alignment before major initiatives

### Quality Gates

- Vision statements must reference specific business goals
- Metrics must have baseline and target values
- Roadmaps must show dependencies and owners
- ROI calculations must cite sources for statistics

---

## Failure Modes & Recovery

| Failure | Recovery |
|---------|----------|
| Stakeholder misalignment | Schedule alignment workshop; document agreements |
| Metrics not improving | Audit implementation; check leading vs. lagging indicators |
| Low UX maturity progress | Identify blockers; secure executive sponsorship |
| DesignOps resistance | Start with quick wins; demonstrate value incrementally |

---

## 2026 Strategic Context

### AI & Agentic UX

The shift from Conversational UI to **Delegative UI** is the defining paradigm change:

```
Traditional:  User --> [Commands] --> System --> [Response] --> User

Agentic:      User --> [Intent] --> AI Agent --> [Plans & Executes] --> System
                  \                    |
                   \<-- [Oversight] --/
```

**Design Patterns for Agentic AI:**
- Intent Canvases replace traditional forms
- Negotiation Dialogs for human-agent co-creation
- Interruptibility for user override
- Explainability for transparency

### Trust as Core Design Challenge

In 2026, trust is the defining UX challenge for AI experiences:
- **Visibility** - Users understand what the AI is doing
- **Predictability** - Consistent behavior builds confidence
- **Reassurance** - Clear communication about limitations

**Key principle:** "Do-it-for-me" cannot become "do-it-without-me."

---

## References

- [Metrics Reference](references/metrics.md) - HEART, CASTLE, ROI calculation
- [Maturity Reference](references/maturity.md) - UX maturity model, DesignOps
- [Frameworks Reference](references/frameworks.md) - North Star, OKRs, roadmapping
- [Stakeholders Reference](references/stakeholders.md) - Communication, alignment
