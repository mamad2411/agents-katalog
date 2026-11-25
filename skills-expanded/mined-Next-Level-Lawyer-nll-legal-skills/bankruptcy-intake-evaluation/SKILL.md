---
name: bankruptcy-intake-evaluation
description: Evaluate new bankruptcy intake submissions for Chapter 7 vs. Chapter 13 fit, overall viability, and urgency (garnishment, foreclosure, repossession deadlines). Use whenever the user asks to review, score, or triage new bankruptcy leads/intake, or asks whether a case is a good Chapter 7 or Chapter 13 fit.
---

# Bankruptcy Intake Evaluation

Screens new bankruptcy leads for chapter fit and urgency — the two things that determine both viability and how fast the firm needs to move.

## Workflow

1. **Check urgency first.** Flag prominently: active wage garnishment, imminent foreclosure sale date, repossession scheduled, utility shutoff, or a lawsuit judgment about to be entered. These often require an emergency filing, not standard-timeline intake.
2. **Assess rough chapter fit**: income relative to household size (a rough means test read, not a final calculation — flag that the actual means test calculator should run before confirming), whether the client has non-exempt assets that would be at risk in a Chapter 7, and whether they have secured debt they want to catch up on (favors Chapter 13, e.g., saving a house from foreclosure).
3. **Flag red flags**: recent large purchases/transfers (preference and fraudulent transfer exposure), prior bankruptcy filing (check timing against re-filing eligibility windows), unfiled tax returns (required before filing in most cases), business ownership (adds complexity).
4. **Score and summarize** (format below).

## Summary format (per submission)

```
**[Name]** — Total debt: $[amount] | Household size: [X] | Monthly income: $[amount]

- **Urgency:** [routine / time-sensitive ⚠️ — garnishment/foreclosure/repo date if any]
- **Likely chapter fit:** [Chapter 7 / Chapter 13 / unclear — needs full means test]
- **Red flags:** [recent transfers, prior filing timing, unfiled returns, business ownership — "None" if none]
- **Score: X/10**
- **Take assessment:** [take / pass / needs more info, with reason]
```

## Scoring rubric (10 points)

| Factor | Points | What to check |
|---|---|---|
| Chapter fit clarity | 4 | Clear Ch 7 or Ch 13 candidate = full; genuinely borderline = partial, needs full means test |
| Urgency handled | 2 | Full if urgency is clear and firm can move on the timeline needed |
| Red flags | 3 | No recent transfers, no re-filing timing issue, returns filed = full; any flag present = reduced, not disqualifying by itself |
| Completeness | 1 | Enough info to scope the engagement |

## Notes

- Never run or assert a final means test result here — this is a rough fit read only; use the means-test-calculator skill for the actual calculation.
- Prior bankruptcy filing timing (re-filing eligibility for discharge) is a hard rule-based cutoff — flag it explicitly if a prior filing is mentioned, rather than treating it as a soft factor.
