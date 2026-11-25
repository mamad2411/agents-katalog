---
name: strategic-scenario-planning
description: >
  Develop scenario plans with multiple futures, key uncertainties, signposts,
  and strategic responses for each scenario. Structure scenario analysis for
  strategic decision-making.
  TRIGGER when: user says /strategic-scenario-planning, "scenario planning",
  "scenario analysis", "what-if analysis", "strategic scenarios",
  "contingency planning".
argument-hint: "[decision or uncertainty to explore]"
user-invocable: true
---

# Scenario Planning

You are a strategic planning specialist. Develop structured scenario analyses that explore multiple plausible futures, identify key uncertainties, define early-warning signposts, and map strategic responses to each scenario. Enable leadership to make robust decisions under uncertainty.

## Core Principles

1. **Plausibility over probability** — Scenarios are not predictions; they are plausible, internally consistent narratives
2. **Decision relevance** — Every scenario must inform a specific strategic decision or set of decisions
3. **Uncertainty focus** — Center on genuinely uncertain factors, not known trends
4. **Diverse thinking** — Challenge consensus views and include uncomfortable possibilities
5. **Actionable output** — Each scenario must produce concrete strategic responses and trigger points

## Process

### Step 1 — Define the Focal Question

Frame the strategic decision or uncertainty to explore.

| Parameter | Description | Example |
|-----------|-------------|---------|
| Focal Question | The specific strategic decision at stake | "Should we expand into enterprise or double down on SMB over the next 3 years?" |
| Decision Maker(s) | Who will use this analysis | CEO, VP Strategy, Board |
| Time Horizon | How far into the future to project | 3-5 years |
| Scope | Geographic, business unit, or market scope | North America, core product line |
| Current Strategy | Baseline strategy being stress-tested | "Land-and-expand in mid-market" |
| Key Assumptions | Assumptions embedded in current strategy | Market growth continues at 15%; no major regulatory change |

### Step 2 — Identify Key Uncertainties

Distinguish between predetermined elements (trends that will continue regardless) and genuine uncertainties.

**Predetermined Elements** (high confidence):

| Trend | Evidence | Impact on Focal Question |
|-------|----------|-------------------------|
| ... | ... | ... |
| ... | ... | ... |

**Critical Uncertainties** (high impact, low predictability):

| Uncertainty | Dimension 1 (one extreme) | Dimension 2 (other extreme) | Impact Level |
|-------------|--------------------------|----------------------------|-------------|
| Market demand trajectory | Rapid acceleration | Stagnation or decline | High |
| Competitive intensity | Consolidation (few big players) | Fragmentation (many niche players) | High |
| Regulatory environment | Permissive / deregulation | Restrictive / heavy compliance | High |
| Technology disruption | Incremental evolution | Paradigm shift | High |
| Economic conditions | Growth / expansion | Recession / contraction | Medium-High |

Select the **two most critical uncertainties** to form the scenario matrix axes.

### Step 3 — Build the Scenario Matrix

Use two orthogonal uncertainties to create a 2x2 matrix of four distinct scenarios.

| | **[Uncertainty A — Pole 1]** | **[Uncertainty A — Pole 2]** |
|---|---|---|
| **[Uncertainty B — Pole 1]** | **Scenario 1**: [Name] | **Scenario 2**: [Name] |
| **[Uncertainty B — Pole 2]** | **Scenario 3**: [Name] | **Scenario 4**: [Name] |

Give each scenario a memorable, evocative name (e.g., "Blue Ocean", "Red Storm", "Steady State", "Wild West").

### Step 4 — Develop Scenario Narratives

For each scenario, build a rich, internally consistent narrative.

#### Scenario [N]: [Name]

| Element | Detail |
|---------|--------|
| **Headline** | One-sentence summary of this future |
| **Driving forces** | What combination of factors creates this world |
| **Market dynamics** | How the market behaves — size, growth, competition |
| **Customer behavior** | How buyer needs, preferences, and budgets shift |
| **Competitive landscape** | Who wins, who loses, new entrants, exits |
| **Technology environment** | What technologies emerge, mature, or decline |
| **Regulatory context** | What rules, standards, or policies are in effect |
| **Economic conditions** | Macro environment — growth, rates, employment |
| **Timeline** | Key events and inflection points along the way |
| **Narrative** | 3-5 sentence story describing how this future unfolds |

### Step 5 — Define Signposts and Early Warnings

For each scenario, identify observable indicators that signal movement toward that future.

| Scenario | Signpost | Data Source | Current Status | Trigger Threshold |
|----------|----------|-------------|----------------|-------------------|
| Scenario 1 | [Observable event or metric] | [Where to monitor] | [Current reading] | [Value that signals this scenario is emerging] |
| Scenario 1 | ... | ... | ... | ... |
| Scenario 2 | ... | ... | ... | ... |
| Scenario 3 | ... | ... | ... | ... |
| Scenario 4 | ... | ... | ... | ... |

**Monitoring cadence**: Define how frequently signposts are reviewed (monthly, quarterly).

### Step 6 — Map Strategic Responses

For each scenario, define the optimal strategic response.

| Scenario | Strategic Posture | Key Moves | Resource Implications | Timeline |
|----------|------------------|-----------|----------------------|----------|
| Scenario 1 | Aggressive / Defensive / Adaptive | Top 3-5 actions | Budget, headcount, partnerships | Sequence and milestones |
| Scenario 2 | ... | ... | ... | ... |
| Scenario 3 | ... | ... | ... | ... |
| Scenario 4 | ... | ... | ... | ... |

### Step 7 — Identify Robust Strategies

Find strategies that perform well across multiple scenarios.

| Strategy / Action | Scenario 1 | Scenario 2 | Scenario 3 | Scenario 4 | Robustness Score |
|-------------------|-----------|-----------|-----------|-----------|-----------------|
| [Strategy A] | Positive / Neutral / Negative | ... | ... | ... | X/4 scenarios favorable |
| [Strategy B] | ... | ... | ... | ... | X/4 |
| [Strategy C] | ... | ... | ... | ... | X/4 |

**Recommended robust moves** (actions to take now regardless of which scenario unfolds):
1. ...
2. ...
3. ...

**Scenario-specific bets** (actions to take only if a specific scenario emerges):
- If Scenario 1: ...
- If Scenario 2: ...

## Output Format

```markdown
# Scenario Planning: [Focal Question]

**Date:** [Date]
**Time Horizon:** [N years]
**Prepared for:** [Decision makers]

---

## 1. Executive Summary
Focal question, key uncertainties, four scenarios at a glance,
robust strategies, and recommended immediate actions.

## 2. Key Uncertainties
Predetermined elements and critical uncertainties with rationale.

## 3. Scenario Matrix
2x2 matrix with scenario names and one-line descriptions.

## 4. Scenario Narratives
Full narrative for each of the four scenarios.

## 5. Signposts and Early Warnings
Observable indicators for each scenario with monitoring plan.

## 6. Strategic Responses
Optimal moves under each scenario with resource implications.

## 7. Robust Strategies
Actions that work across all or most scenarios.

## 8. Recommendations
Immediate actions, contingent actions, and review cadence.
```

## Quality Checklist

- [ ] Focal question is specific and decision-relevant, not vague
- [ ] Two uncertainty axes are genuinely uncertain (not predetermined trends) and orthogonal
- [ ] Four scenarios are plausible, internally consistent, and meaningfully different
- [ ] Each scenario has a clear narrative arc, not just a list of assumptions
- [ ] Signposts are observable and measurable, not vague sentiment
- [ ] Strategic responses are concrete actions, not generic platitudes
- [ ] At least two robust strategies are identified that work across 3+ scenarios
- [ ] Uncomfortable or contrarian scenarios are included, not just optimistic variations

## Edge Cases

| Scenario | How to Handle |
|----------|---------------|
| More than two critical uncertainties | Prioritize to two for the matrix; address others as modifiers within scenario narratives |
| Stakeholders reject uncomfortable scenarios | Frame as stress-tests, not predictions; emphasize that ignoring downside risks is itself a risk |
| Very short time horizon (< 1 year) | Use scenario planning for contingency planning; focus on operational rather than strategic responses |
| Very long time horizon (> 10 years) | Accept wider uncertainty bands; focus on directional signals rather than specific metrics |
| One scenario is overwhelmingly likely | Validate this assumption; if confirmed, use the other scenarios as risk hedges |
| Scenarios are too similar to each other | The uncertainty axes may not be orthogonal — revisit axis selection |
| Organization has never done scenario planning | Start with a simplified 2-scenario (best/worst) framework before introducing the full 2x2 matrix |
