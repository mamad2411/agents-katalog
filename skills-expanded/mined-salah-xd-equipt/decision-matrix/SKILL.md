---
name: decision-matrix
description: "Creates weighted decision matrices for business choices with criteria, scoring, and recommendation logic to remove emotion from decisions."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Decision Matrix

## When to Use This Skill

Use this skill when you need to:
- Compare multiple business options using objective, weighted criteria
- Make a hiring, vendor, tool, or strategy decision with clear reasoning
- Remove emotional bias from a business choice by scoring options systematically
- Document decision rationale for stakeholders or future reference

**DO NOT** use this skill for simple yes/no decisions, personal life choices, or decisions where one option is already clearly superior. This is for complex, multi-criteria business decisions.

---

## Core Principle

A DECISION MATRIX DOES NOT MAKE THE DECISION FOR YOU — IT MAKES YOUR THINKING VISIBLE SO YOU CAN SPOT WHERE INTUITION AND DATA AGREE OR CONFLICT.

---

## Phase 1: Frame the Decision

Define the decision clearly before building the matrix.

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Decision statement** | "What specific decision are you making? State it as a question." | No default — must be provided |
| **Options** | "What are your 2-5 options?" | No default — minimum 2 required |
| **Criteria** | "What factors matter most in this decision? (cost, speed, quality, risk, etc.)" | Suggest 5-7 based on decision type |
| **Stakeholders** | "Who is affected by or needs to approve this decision?" | Solopreneur (self) |
| **Timeline** | "When does this decision need to be made?" | This week |

### Decision Types and Suggested Criteria

| Decision Type | Suggested Criteria |
|--------------|-------------------|
| **Tool/Software** | Cost, ease of use, features, integrations, scalability, support |
| **Vendor/Partner** | Price, quality, reliability, communication, experience, terms |
| **Hire** | Skills match, culture fit, availability, rate, portfolio quality |
| **Strategy** | Revenue impact, effort, risk, time to results, alignment with goals |
| **Market/Product** | Market size, competition, margin potential, execution difficulty |

**GATE: Confirm the decision statement, options, and criteria before building the matrix.**

---

## Phase 2: Weight and Score

Build the matrix with weighted criteria and score each option.

### Weighting Criteria

Assign weights that total 100% across all criteria:

```
## Criteria Weights

| Criteria | Weight | Rationale |
|----------|--------|-----------|
| Revenue impact | 30% | Directly tied to business goal |
| Implementation effort | 25% | Limited resources as solopreneur |
| Risk level | 20% | Cannot afford major setbacks |
| Time to results | 15% | Need wins within 90 days |
| Scalability | 10% | Important but not urgent |
| **Total** | **100%** | |
```

### Scoring Options

Score each option 1-5 on every criterion with brief justification:

```
## Decision Matrix: [Decision Statement]

| Criteria | Weight | Option A | Score | Option B | Score | Option C | Score |
|----------|--------|----------|-------|----------|-------|----------|-------|
| Revenue impact | 30% | [rationale] | 4 | [rationale] | 3 | [rationale] | 5 |
| Effort | 25% | [rationale] | 3 | [rationale] | 5 | [rationale] | 2 |
| Risk | 20% | [rationale] | 4 | [rationale] | 4 | [rationale] | 3 |
| Time to results | 15% | [rationale] | 5 | [rationale] | 3 | [rationale] | 2 |
| Scalability | 10% | [rationale] | 3 | [rationale] | 4 | [rationale] | 5 |

## Weighted Scores

| Option | Weighted Score | Rank |
|--------|---------------|------|
| Option A | 3.80 | 1 |
| Option C | 3.40 | 2 |
| Option B | 3.85 | 1 |
```

**GATE: Present the scored matrix and get user validation on scores before delivering the recommendation.**

---

## Phase 3: Recommend

Deliver a clear recommendation with reasoning.

### Recommendation Format

```
## Recommendation

**Winner:** [Option] with a weighted score of [X.XX]

**Why this wins:** [2-3 sentences explaining the key differentiators]

**Key trade-off:** [What you give up by choosing this option vs. the runner-up]

**Gut check:** Does this match your intuition? If the matrix says Option A but your gut says Option B, examine which criteria might be underweighted.
```

### Sensitivity Analysis

Test whether the result holds if weights shift:
- "If you increased [criteria] weight by 10%, [Option X] would overtake [Option Y]"
- Flag any decision where the top two options are within 0.3 points — this means the decision is close and additional factors may matter

### Risk Flags

Note any option that scores below 2 on a high-weight criterion, even if the total score is high. A single critical weakness can sink an otherwise strong option.

---

## Phase 4: Document

Provide a decision record for future reference.

### Decision Record Template

```
## Decision Record

**Decision:** [Statement]
**Date:** [Date]
**Decision maker:** [Name]
**Chosen option:** [Option]
**Weighted score:** [X.XX]
**Key reasons:** [3 bullet points]
**Key risks:** [Known risks of the chosen option]
**Review date:** [When to evaluate if this was the right call]
```

---

## Anti-Patterns

- **Too many criteria** — more than 7 criteria dilutes the signal. Force-rank and keep the top 5-7.
- **Equal weights** — giving every criterion 20% means you have not thought about what matters most.
- **Scoring without justification** — a score of 4 means nothing without a one-line rationale.
- **Ignoring gut disagreement** — if the matrix says one thing and your instinct says another, the weights are probably wrong.
- **Using a matrix for obvious decisions** — if you already know the answer, do not build a matrix to justify it.

---

## Recovery

- **User cannot identify criteria:** Suggest 5 based on the decision type (see table above) and ask them to remove any that do not apply.
- **Options are too similar:** Add differentiating criteria or increase the scoring granularity to 1-10 instead of 1-5.
- **Scores are all 3s:** Challenge the user — "A 3 means average. Is this option truly average on [criteria], or is it actually a 2 or 4?" Push for honest differentiation.
- **User disagrees with the result:** Ask which score they would change. Often one re-scored criterion flips the result, revealing what they actually value most.
- **Stakeholders disagree on weights:** Have each stakeholder assign weights independently, then average them. Discuss any criteria where weights diverge by more than 15%.
