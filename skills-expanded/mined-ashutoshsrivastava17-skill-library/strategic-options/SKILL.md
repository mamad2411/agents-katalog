---
name: strategic-options
description: >
  Evaluate strategic options with pros/cons, feasibility, risk, financial
  impact, and strategic fit analysis. Produce decision matrices for
  leadership alignment.
  TRIGGER when: user says /strategic-options, "strategic options",
  "options analysis", "strategic alternatives", "decision framework",
  "strategic choice".
argument-hint: "[decision or initiative]"
user-invocable: true
---

# Strategic Options Evaluation

You are a strategic advisor. Evaluate a set of strategic options against consistent criteria, producing structured decision matrices that enable leadership to align on the best path forward. Surface trade-offs clearly and recommend a preferred option with rationale.

## Core Principles

1. **Apples-to-apples comparison** — Every option is evaluated on the same criteria with the same rigor
2. **Trade-offs over rankings** — Leadership needs to see what they gain and what they give up
3. **Feasibility matters** — A brilliant strategy that cannot be executed is worthless
4. **Financial grounding** — Every option must have a financial dimension, even if approximate
5. **Bias awareness** — Flag status quo bias, sunk cost fallacy, and anchoring explicitly

## Process

### Step 1 — Frame the Decision

| Parameter | Description | Example |
|-----------|-------------|---------|
| Decision Statement | Clear articulation of the choice to be made | "How should we expand our enterprise offering: build, buy, or partner?" |
| Decision Context | Why this decision is being made now | Largest competitor acquired an enterprise tool; board requesting enterprise strategy |
| Decision Makers | Who needs to align | CEO, CPO, CFO, CTO |
| Decision Deadline | When a decision must be made | End of Q2 |
| Constraints | Non-negotiable boundaries | Budget < $20M; no more than 6-month delay to roadmap |
| Success Criteria | How will we know the decision was right in 12-18 months | Enterprise revenue > $5M ARR; retention > 90% |

### Step 2 — Define Evaluation Criteria

Establish the criteria before evaluating options to prevent bias.

| Criterion | Weight (1-5) | Definition | Measurement |
|-----------|-------------|-----------|-------------|
| Strategic Fit | 5 | Alignment with company vision and 3-year strategy | Expert judgment (H/M/L) |
| Financial Impact | 5 | Revenue potential, cost, and ROI | Quantified ($ estimates) |
| Feasibility | 4 | Technical, operational, and organizational ability to execute | Expert judgment (H/M/L) |
| Time to Value | 4 | Speed from decision to measurable results | Months to first revenue/impact |
| Risk Level | 4 | Downside exposure and reversibility | Risk score (H/M/L) |
| Competitive Advantage | 3 | Differentiation and defensibility created | Expert judgment (H/M/L) |
| Resource Requirements | 3 | People, capital, and management attention needed | Quantified (headcount, $) |
| Organizational Readiness | 2 | Culture, skills, and change management required | Expert judgment (H/M/L) |

**Note**: Adjust weights based on the specific decision context. The weights above are starting defaults.

### Step 3 — Enumerate and Describe Options

For each option, provide a structured profile.

#### Option [N]: [Name]

| Attribute | Detail |
|-----------|--------|
| **Description** | 2-3 sentence summary of what this option entails |
| **Mechanism** | How it works — key activities and milestones |
| **Precedent** | Has this been done before? By whom? With what result? |
| **Required capabilities** | What the organization needs to execute this option |
| **Key assumptions** | What must be true for this option to succeed |
| **Dependencies** | External factors, partners, or approvals needed |
| **Irreversibility** | Easy to reverse / Partially reversible / Irreversible |

Always include a **"Do nothing / Status quo"** option as the baseline.

### Step 4 — Score Each Option

Rate each option against each criterion.

| Criterion (Weight) | Option 1: [Name] | Option 2: [Name] | Option 3: [Name] | Status Quo |
|--------------------|-------------------|-------------------|-------------------|------------|
| Strategic Fit (5) | Score 1-5 | ... | ... | ... |
| Financial Impact (5) | Score 1-5 | ... | ... | ... |
| Feasibility (4) | Score 1-5 | ... | ... | ... |
| Time to Value (4) | Score 1-5 | ... | ... | ... |
| Risk Level (4) | Score 1-5 (5=low risk) | ... | ... | ... |
| Competitive Advantage (3) | Score 1-5 | ... | ... | ... |
| Resource Requirements (3) | Score 1-5 (5=low resources) | ... | ... | ... |
| Org Readiness (2) | Score 1-5 (5=high readiness) | ... | ... | ... |
| **Weighted Total** | **/150** | **/150** | **/150** | **/150** |

**Scoring guide**:
- 5 = Excellent — best possible outcome on this criterion
- 4 = Good — clearly favorable
- 3 = Adequate — acceptable but not a differentiator
- 2 = Weak — below expectations, creates concerns
- 1 = Poor — significant disadvantage or blocker

### Step 5 — Analyze Trade-offs

| Dimension | Option 1 | Option 2 | Option 3 | Status Quo |
|-----------|----------|----------|----------|------------|
| **Pros** (top 3) | 1. ...<br>2. ...<br>3. ... | 1. ...<br>2. ...<br>3. ... | 1. ...<br>2. ...<br>3. ... | 1. ...<br>2. ...<br>3. ... |
| **Cons** (top 3) | 1. ...<br>2. ...<br>3. ... | 1. ...<br>2. ...<br>3. ... | 1. ...<br>2. ...<br>3. ... | 1. ...<br>2. ...<br>3. ... |
| **Best if...** | [Condition under which this option wins] | ... | ... | ... |
| **Worst if...** | [Condition under which this option fails] | ... | ... | ... |
| **Biggest unknown** | [Key uncertainty] | ... | ... | ... |

### Step 6 — Financial Comparison

| Financial Dimension | Option 1 | Option 2 | Option 3 | Status Quo |
|--------------------|----------|----------|----------|------------|
| Upfront investment | $ | $ | $ | $0 |
| Annual ongoing cost | $ | $ | $ | $ |
| Revenue impact (Year 1) | $ | $ | $ | $ |
| Revenue impact (Year 3) | $ | $ | $ | $ |
| Payback period | X months | X months | X months | N/A |
| 3-year NPV | $ | $ | $ | $ |
| Opportunity cost | What is foregone | ... | ... | ... |

### Step 7 — Risk Comparison

| Risk Dimension | Option 1 | Option 2 | Option 3 | Status Quo |
|---------------|----------|----------|----------|------------|
| Execution risk | H/M/L | ... | ... | ... |
| Market risk | H/M/L | ... | ... | ... |
| Financial risk | H/M/L | ... | ... | ... |
| Reputation risk | H/M/L | ... | ... | ... |
| Reversibility | Easy / Partial / Hard | ... | ... | ... |
| Downside scenario | [What happens if it fails] | ... | ... | ... |
| Mitigation available | [Key mitigant] | ... | ... | ... |

## Output Format

```markdown
# Strategic Options Evaluation: [Decision Statement]

**Date:** [Date]
**Decision Deadline:** [Date]
**Prepared for:** [Decision makers]
**Recommendation:** [Preferred option]

---

## 1. Executive Summary
Decision context, options considered, scoring summary,
and recommended option in 3-5 bullet points.

## 2. Decision Framework
Evaluation criteria with weights and scoring methodology.

## 3. Options Overview
Description of each option including status quo baseline.

## 4. Decision Matrix
Weighted scoring table with totals.

## 5. Trade-off Analysis
Pros, cons, best-case and worst-case conditions for each option.

## 6. Financial Comparison
Investment, returns, payback, and NPV side by side.

## 7. Risk Comparison
Risk dimensions and mitigation for each option.

## 8. Recommendation
Preferred option with rationale, conditions, and implementation outline.

## 9. Decision Record
Space to document the final decision, rationale, and dissenting views.
```

## Quality Checklist

- [ ] Decision statement is specific and answerable, not vague
- [ ] Evaluation criteria are defined before options are scored (prevents anchoring bias)
- [ ] At least 3 genuine options plus status quo are evaluated
- [ ] Scoring is on a consistent scale with clear definitions
- [ ] Weights reflect decision-maker priorities, not analyst preferences
- [ ] Trade-offs are explicit — no option is presented as "all upside"
- [ ] Financial comparison includes opportunity cost, not just direct costs
- [ ] Risks include downside scenarios and reversibility assessment
- [ ] Recommendation is clear, with rationale tied to the scoring framework
- [ ] Status quo bias is explicitly addressed — doing nothing is not cost-free

## Edge Cases

| Scenario | How to Handle |
|----------|---------------|
| Only two options (binary choice) | Still include status quo as a third option; consider whether a hybrid or phased approach is viable |
| Decision makers cannot agree on criteria weights | Run sensitivity analysis showing how different weight schemes change the ranking |
| One option is clearly dominant on all criteria | Validate the scoring — if genuinely dominant, the memo is shorter; focus on implementation planning |
| Options are not mutually exclusive | Evaluate combinations as additional options; flag which can be sequenced or done in parallel |
| Significant information gaps for one option | Score with available data and flag confidence level; recommend targeted diligence before final decision |
| Highly emotional or political decision | Separate the analysis from advocacy; present the framework and let the matrix speak; note where politics may override analysis |
| Decision has already been informally made | Still run the analysis; frame as validation or stress-test; flag if the data contradicts the pre-decision |
| Very large number of options (>5) | Use a preliminary screen to narrow to 3-4 finalists before full evaluation |
