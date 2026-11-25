---
name: prioritization-advisor
description: "Applies structured prioritization frameworks (RICE, ICE, Kano, MoSCoW, Weighted Scoring) to a feature backlog or initiative list. Helps PMs make transparent, defensible prioritization decisions by making trade-offs explicit."
category: strategy
default_depth: standard
---

# Prioritization Advisor

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

Applies structured prioritization frameworks (RICE, ICE, Kano, MoSCoW, Weighted Scoring) to a feature backlog or initiative list. Helps PMs make transparent, defensible prioritization decisions by making trade-offs explicit.

## When to Use

- Backlog grooming when there are too many competing requests
- Sprint or quarterly planning when tough trade-offs must be made
- Stakeholder alignment when multiple teams want different things prioritized
- Any time the PM needs to justify "why X before Y"

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | Quick gut-check on 3-5 items, single framework obvious | Ask, Score, Rank |
| **Standard** | Backlog triage or quarterly planning with competing inputs | All sections |
| **Deep** | Cross-org prioritization with multiple stakeholder groups | All sections + multi-framework comparison, stakeholder-specific scoring weights, sensitivity analysis per assumption |

**Omit rules:** At Light depth, skip Challenge, Surface Trade-Offs, Sensitivity Notes, and Trade-Off Analysis. Produce only a scored and ranked list with the chosen framework.

## Framework

### Available Frameworks

### 1. RICE Scoring

Best for: Comparing initiatives of varying scope when you have reach data.

```markdown
| Initiative | Reach (users/qtr) | Impact (0.25-3) | Confidence (%) | Effort (person-wks) | RICE |
|---|---|---|---|---|---|
| [Item] | [N] | [score] | [%] | [N] | [calc] |
```

RICE = (Reach × Impact × Confidence) / Effort

**Impact Scale:**
- 3 = Massive, step-change improvement
- 2 = High, significant improvement
- 1 = Medium, noticeable improvement
- 0.5 = Low, minor improvement
- 0.25 = Minimal, barely noticeable

### 2. ICE Scoring

Best for: Quick-and-dirty prioritization when you lack reach data.

```markdown
| Initiative | Impact (1-10) | Confidence (1-10) | Ease (1-10) | ICE |
|---|---|---|---|---|
| [Item] | [score] | [score] | [score] | [calc] |
```

ICE = Impact × Confidence × Ease

### 3. Kano Model

Best for: Understanding which features delight vs. which are table stakes.

**Categories:**
- **Must-Be (Basic):** Expected. Absence causes dissatisfaction. Presence doesn't delight. (e.g., login, data export)
- **One-Dimensional (Performance):** More is better. Linear relationship to satisfaction. (e.g., speed, storage)
- **Attractive (Delight):** Unexpected. Absence doesn't disappoint, but presence delights. (e.g., AI suggestions)
- **Indifferent:** Customer doesn't care either way.
- **Reverse:** Some customers actively don't want this.

```markdown
| Feature | Category | Rationale | Priority Implication |
|---|---|---|---|
| [Feature] | Must-Be | [Evidence] | Ship first, absence is a deal-breaker |
| [Feature] | Attractive | [Evidence] | Invest selectively, high differentiation potential |
```

### 4. MoSCoW

Best for: Timeboxed releases when you need to negotiate scope.

```markdown
## Must Have (release is broken without these)
- [Item], Reason: [why it's non-negotiable]

## Should Have (important but not critical)
- [Item], Reason: [significant value, workaround exists]

## Could Have (nice to include if time permits)
- [Item], Reason: [incremental value]

## Won't Have (explicitly out of scope for this release)
- [Item], Reason: [why it's deferred]
```

### 5. Weighted Scoring

Best for: When different stakeholders value different criteria.

```markdown
## Scoring Criteria
| Criterion | Weight | Description |
|---|---|---|
| Revenue impact | 30% | Expected contribution to revenue |
| User satisfaction | 25% | Impact on NPS/CSAT |
| Strategic alignment | 25% | Supports current strategic bets |
| Technical debt reduction | 20% | Reduces maintenance burden |

## Scoring Matrix
| Initiative | Revenue (1-5) | Satisfaction (1-5) | Strategy (1-5) | Tech Debt (1-5) | Weighted Score |
|---|---|---|---|---|---|
| [Item] | [score] | [score] | [score] | [score] | [calc] |
```

## Advisor Workflow

1. **Ask** the PM which framework fits their context (offer recommendation)
2. **Gather** the list of items to prioritize
3. **Score** each item using the chosen framework
4. **Rank** by score, then review for sanity
5. **Challenge** any scoring that seems off, "You rated confidence at 90% but mentioned you haven't validated demand. Should this be lower?"
6. **Surface trade-offs**, "Items A and B are close in score but very different in risk profile. Here's what changes if assumptions shift."

## Minimum Evidence Bar

**Required inputs:** At least two items to compare and evidence or explicitly labeled estimates for the chosen scoring dimensions.

**Acceptable evidence:** Usage analytics, customer feedback, stakeholder requests with business rationale, engineering estimates, prior experiment results.

**Insufficient evidence:** If fewer than 2 items are provided or no context exists for any scoring dimension, stop and recommend gathering usage data or stakeholder input before attempting this skill. Do not produce a prioritized list without scorable context.

**Hypotheses vs. findings:**
- **Findings:** Final ranked order, scores backed by data (reach from analytics, effort from engineering estimates)
- **Hypotheses:** Confidence percentages and impact ratings without direct validation, must be labeled with evidence source or "assumption"

## Output Format

Produce a Prioritization Report with:
1. **Framework Used**, which method and why
2. **Scored Backlog**, all items with scores, sorted by priority
3. **Trade-Off Analysis**, close calls and what would change the ranking
4. **Recommendation**, top 3-5 items to invest in, with rationale
5. **Sensitivity Notes**, which scores are most uncertain

**Shipwright Signature (required closing):**
6. **Decision Frame**, Top recommended investment with trade-off (speed vs. certainty, breadth vs. depth), confidence with evidence quality, owner, decision date, revisit trigger
7. **Unknowns & Evidence Gaps**, Items scored with <50% confidence, assumptions that would change the ranking if wrong
8. **Pass/Fail Readiness**, PASS if scores state their evidence or assumptions, uncertainty is honest, and the recommendation explains tradeoffs. Low confidence must lead to a provisional ranking and a targeted validation step, never inflated scores; FAIL if unsupported estimates are presented as facts.
9. **Recommended Next Artifact**, Which Shipwright skill to run next and why

## Common Mistakes to Avoid

- **Precision theater**, Don't debate whether something is a 7 or an 8; focus on the big gaps
- **Ignoring confidence**, A high-impact, low-confidence item needs validation, not commitment
- **Using one framework for everything**, RICE for roadmap planning, MoSCoW for release scoping, Kano for feature strategy
- **Scoring in isolation**, Score as a team, not solo, to reduce individual bias
- **Forgetting to re-prioritize**, Priorities change as you learn; rescore at least quarterly

## Weak vs. Strong Output

**Weak:**
> "Impact: High. Confidence: High. This is a top priority."

No evidence behind the scores, just adjectives restating the rating scale.

**Strong:**
> "Impact: 2 (High), based on 1,200 support tickets/month citing this workflow gap. Confidence: 70%, validated via 3 customer interviews but no quantitative A/B test yet."

Scores are anchored to specific evidence with explicit gaps called out.
