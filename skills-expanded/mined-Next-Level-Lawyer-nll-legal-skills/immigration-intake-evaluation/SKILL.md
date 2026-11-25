---
name: immigration-intake-evaluation
description: Evaluate marriage-based green card intake form submissions (Tally) from the perspective of an immigration attorney deciding whether to take on the case. Produces a per-submission summary, red-flag callouts, and a 0-10 viability score. Use this whenever the user asks to review, summarize, score, or rank submissions for the "Marriage-based Green Card Intake" form, asks "is this case worth taking," or wants a case-viability assessment of intake responses. Also use for any request to re-score, re-rank, or bulk-triage a batch of these submissions.
---

# Intake Evaluation (Marriage-Based Green Card)

Evaluates Tally form submissions for the "Marriage-based Green Card Intake" form the way an immigration attorney would during initial case screening: not just restating the answers, but flagging what matters for take-or-pass decisions.

## Workflow

1. **Fetch or accept submissions.** If a compatible Tally integration is available, fetch the relevant form submissions and filter to completed responses unless the user wants partials too. Otherwise, accept a Tally export, spreadsheet, uploaded file, or pasted intake responses.
2. **Detect test/junk submissions first.** Before evaluating, scan for:
   - Placeholder text ("test", "asdf", "sdf", "n/a" used everywhere, repeated single characters)
   - Email domains matching the reviewing firm itself (e.g., an `@[immigration-firm].com` address filling out its own client intake form)
   - Nonsensical or clearly fabricated data (future marriage dates entered as if historical, garbage strings in every field)
   Flag these explicitly as **likely test/internal data** and exclude them from scoring — don't silently score them, and don't silently drop them either. Say why they're excluded.
3. **Check internal consistency.** Cross-reference related answers before writing the summary. Common contradictions to check for in this form:
   - "Currently living together: Yes" vs. "Immigrant spouse currently: Abroad"
   - "First marriage for both" vs. "divorce decree: No/incomplete" (implies a prior marriage exists)
   - "Entered with a visa" vs. "Yes" to unlawful presence/overstay/entry without inspection
   Any contradiction found should be called out explicitly in the summary — don't resolve it silently in either direction, and don't average it away in the score.
4. **Write the per-submission summary** (see format below).
5. **Score each valid (non-test) submission out of 10** using the rubric below.
6. **Close with a one-line pipeline takeaway** if there are multiple submissions (e.g., which ones are ready to move forward, which need a clarifying call, which to pass on).

## Summary format (per submission)

For each submission, use this structure:

```
**[Name]** ([email]) — submitted [timestamp]

- **Setup:** [USC/LPR status of sponsoring spouse, immigrant spouse's location, marriage date/place, how they met, how long before marrying]
- **Red flags:** [explicitly list: fraud/denial history, unlawful presence/overstay/EWI, sham marriage findings, criminal history, removal proceedings — state "None" if genuinely none]
- **Concerns:** [documentation gaps, weak evidence of bona fide marriage, incomplete answers — non-disqualifying but worth resolving]
- **Contradictions:** [any internal inconsistency found in step 3 — omit this line only if none found]
- **Score: X/10**
- **Take assessment:** [1-2 sentence recommendation: take, pass, or needs-clarifying-call, with the specific reason]
```

## Scoring rubric (10 points)

| Factor | Points | What to check |
|---|---|---|
| No red flags | 4 | Fraud/denial history, unlawful presence/overstay/EWI, sham marriage findings, criminal history, removal proceedings. Any single red flag caps this at 0-1 of the 4 points, even if everything else is clean — red flags don't average out. |
| Consistency | 2 | No contradictions between related answers (see step 3 checklist above). Any contradiction found = 0 of these 2 points until clarified. |
| Documentation readiness | 2 | Marriage certificate in hand; divorce decrees finalized and documented if applicable. |
| Bona fide marriage evidence | 1 | Strength of "shared life" evidence (joint lease/accounts/insurance, photos, communication history) and cohabitation status. |
| Completeness | 1 | No blank/skipped fields. Partial credit for minor gaps; 0 if substantial fields are missing. |

**Do not assign a score to submissions flagged as test/junk data in step 2.** Mark them "N/A (test data)" instead. If asked to score one anyway for illustration, label it clearly as hypothetical/face-value only.

## Notes on tone

Write like an attorney doing initial triage, not like a form summarizer — lead with what determines viability (red flags, contradictions), not with a restatement of every field. Keep it scannable; use the structure above rather than prose paragraphs. Be direct about recommending a pass or a clarifying call when the data warrants it — don't soften a real red flag into a "concern."
