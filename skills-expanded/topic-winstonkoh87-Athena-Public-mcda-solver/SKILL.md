---
name: Decision Matrix (MCDA)
description: Multi-Criteria Decision Analysis calculator. Breaks complex decisions into weighted criteria with explicit scoring.
created: 2026-02-27
auto-invoke: false
model: default
context_trigger: "decision matrix, multi-criteria, MCDA, weighted scoring, trade-off analysis, alternatives, prioritization"
---

# ⚖️ Decision Matrix (MCDA / EEV)

> **Philosophy**: Complex decisions fail because people optimize for one variable while ignoring five others.

## 1. When to Use

- Choosing between 2+ options with multiple trade-offs
- Any decision where "it depends" is the current answer
- When stakeholders disagree on priorities

## 2. Execution Workflow

```
STEP 1: LIST OPTIONS
  └─ Must have ≥2 distinct options (no straw men)

STEP 2: DEFINE CRITERIA
  └─ List 3-7 evaluation criteria
  └─ Each criterion must be measurable or scorable (1-10)

STEP 3: WEIGHT CRITERIA
  └─ Assign percentage weights (must sum to 100%)
  └─ Force-rank: "If you could only optimize for ONE criterion, which?"

STEP 4: SCORE EACH OPTION
  └─ Score 1-10 per criterion per option
  └─ Justify each score in one sentence

STEP 5: COMPUTE EEV
  └─ EEV = Σ (Score × Weight) for each option
  └─ Rank options by total EEV

STEP 6: SANITY CHECK
  └─ Does the winner "feel" right?
  └─ If not, a hidden criterion exists — surface it and re-run
```

## 3. Output Format

```markdown
# Decision: [Question]

## Criteria & Weights
| # | Criterion | Weight |
|---|-----------|--------|
| 1 | [Name]    | [X]%   |
| 2 | [Name]    | [X]%   |

## Scoring Matrix
| Option | C1 | C2 | C3 | **EEV** |
|--------|----|----|-----|---------|
| A      | 8  | 6  | 7   | **7.1** |
| B      | 5  | 9  | 4   | **6.2** |

## Recommendation
[Winner] with EEV of [X]. Key differentiator: [criterion].

## Sensitivity Analysis
If [criterion weight] changed by ±10%, would the winner change? [Yes/No]
```

## 4. Rules

- Never let one criterion dominate (max weight 40%)
- If an option scores 0 on a criterion, flag it as a potential dealbreaker
- Always run sensitivity analysis on the top weight

---

# skill #decision-making #analysis #framework
