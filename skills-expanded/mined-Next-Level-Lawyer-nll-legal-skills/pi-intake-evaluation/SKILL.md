---
name: pi-intake-evaluation
description: Evaluate personal injury intake submissions from the perspective of a PI attorney deciding whether to take the case, scoring on liability clarity, insurance coverage, damages severity, and statute of limitations risk. Use whenever the user asks to review, score, rank, or triage new PI leads or intake form submissions, or asks "is this case worth taking."
---

# PI Intake Evaluation

Screens personal injury leads the way an attorney would during intake: liability clarity, coverage, damages, and deadline risk — not a restatement of the incident narrative.

## Workflow

1. **Fetch or accept submissions** (Tally form, spreadsheet, or pasted intake notes).
2. **Check statute of limitations first, always.** Calculate or flag the SOL deadline based on incident date and jurisdiction (ask jurisdiction if not stated — SOL varies by state and claim type, don't guess). If it's close to expiring or already expired, flag this at the top in bold, regardless of how strong the rest of the case is.
3. **Assess liability clarity**: clear liability (rear-end collision, slip on documented hazard), disputed liability (comparative fault likely), or unclear (needs investigation).
4. **Assess coverage**: at-fault party insured, uninsured/underinsured, commercial vs. personal policy, policy limits if known.
5. **Assess damages severity**: injury type/permanence, medical treatment to date, lost wages, ongoing treatment needs.
6. **Flag red flags**: prior claims history, gaps in treatment, pre-existing condition overlap, recorded statement already given to the other insurer.
7. **Score and summarize** (format below).

## Summary format (per submission)

```
**[Name]** — incident date [date] | SOL deadline: [date] ⚠️ if <90 days out or expired

- **Liability:** [clear/disputed/unclear] — [why]
- **Coverage:** [insured/uninsured/commercial, limits if known]
- **Damages:** [injury severity, treatment status, wage loss]
- **Red flags:** [prior claims, treatment gaps, recorded statements — state "None" if none]
- **Score: X/10**
- **Take assessment:** [take / pass / needs more info, with reason]
```

## Scoring rubric (10 points)

| Factor | Points | What to check |
|---|---|---|
| Liability clarity | 3 | Clear liability = full points; disputed = partial; unclear = 0-1 |
| Coverage adequacy | 3 | Confirmed insured with reasonable limits = full; uninsured/unknown = low |
| Damages severity | 3 | Significant/permanent injury with documented treatment = full; minor/soft-tissue only = low |
| SOL/procedural risk | 1 | Full point only if well within deadline and no procedural traps (e.g., government entity notice requirements) |

**Do not average away an expiring SOL** — flag it prominently regardless of score.

## Notes

- Never estimate a settlement value — that requires case-specific legal judgment and is out of scope for this skill.
- Government/municipal defendants often have short notice-of-claim deadlines separate from the general SOL — flag if the fact pattern suggests one.
