---
name: tax-intake-evaluation
description: Evaluate tax debt-relief and resolution intake submissions (offer in compromise, installment agreement, penalty abatement candidates) from the perspective of a tax resolution attorney deciding whether to take the case, scoring on collectibility and viability. Use whenever the user asks to review, score, or triage new tax resolution leads/intake, or asks whether an OIC or resolution case is worth taking.
---

# Tax Resolution Intake Evaluation

Screens tax debt-relief leads the way a resolution attorney would: collectibility and program fit drive viability more than the size of the debt itself.

## Workflow

1. **Establish the debt picture**: total owed, tax years involved, whether returns are filed for all years (unfiled returns must generally be resolved before any resolution program applies — flag prominently if any are missing).
2. **Check collection status/urgency**: active levy/garnishment, lien filed, CP504/Final Notice already issued, or no active enforcement yet. Active enforcement changes urgency significantly.
3. **Assess income/asset picture for collectibility**: income relative to allowable expenses (reasonable collection potential), equity in assets, so the client's realistic program fit (OIC vs. installment agreement vs. currently-not-collectible) can be roughly identified — not to calculate an exact offer amount, just to flag likely direction.
4. **Flag red flags**: prior OIC rejections, unfiled returns, active criminal referral risk (rare but flag if suggested), assets that would defeat an OIC (significant equity).
5. **Score and summarize** (format below).

## Summary format (per submission)

```
**[Name]** — Total owed: $[amount] | Years: [list] | Unfiled returns: [yes/no — which years]

- **Collection status:** [none yet / notices issued / active levy-garnishment ⚠️]
- **Likely program fit:** [OIC / installment agreement / currently-not-collectible / unclear — needs full financial analysis]
- **Red flags:** [unfiled returns, prior rejection, asset equity issues — "None" if none]
- **Score: X/10**
- **Take assessment:** [take / pass / needs more info, with reason]
```

## Scoring rubric (10 points)

| Factor | Points | What to check |
|---|---|---|
| Filing compliance | 3 | All years filed = full; unfiled returns = 0-1, since this must be resolved first |
| Collectibility fit | 4 | Clear mismatch between income/assets and debt (good OIC candidate) or clear ability to pay via installment = full; ambiguous = partial |
| Urgency/enforcement | 2 | Active levy/garnishment = still a "take" but flag urgency; no enforcement yet = standard |
| Red flags | 1 | No prior rejections or disqualifying asset equity = full point |

## Notes

- Never estimate an actual offer amount or reasonable collection potential figure — that requires full financial analysis (Form 433 equivalent) and is out of scope here.
- Unfiled returns are the single most common reason a resolution case stalls — flag this before anything else.
