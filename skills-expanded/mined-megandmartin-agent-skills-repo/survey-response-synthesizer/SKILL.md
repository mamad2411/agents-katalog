---
name: survey-response-synthesizer
description: Cluster open-ended survey answers into named themes with counts and verbatim quotes, separating signal from noise. Use when the user says "synthesize these survey responses", "what are people saying", "theme these answers", "make sense of this feedback form", or pastes/points to a pile of free-text answers. Don't use for live interview transcripts and Mom Test discipline — that's user-interview-synthesis — or for numeric survey columns — that's csv-data-analyst.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Research & Analysis, Surveys, Qualitative, Customer Feedback]
    related_skills: [user-interview-synthesis, csv-data-analyst]
---

# Survey Response Synthesizer

Turns a pile of open-ended survey answers into a ranked theme table a founder can act on: theme name, count, share, and 1–2 verbatim quotes each. The standard: every quote is copy-pasted exactly (never paraphrased and passed off as a quote), every count is auditable (theme counts reconcile to total responses), and noise is quarantined — not silently deleted, not counted as signal.

## When to Use

- User has open-text answers from a survey, feedback form, NPS "why?", or exit poll and wants themes.
- User asks "what's the top complaint/request?" across many written responses.
- 10+ responses. Under 10, just read them aloud with the user — clustering adds ceremony, not insight.
- **Not for:** interview transcripts and commitment analysis (`user-interview-synthesis`); numeric ratings or multiple-choice columns (`csv-data-analyst`).

## Quick Reference

| Action | Command / Call |
|---|---|
| Load from CSV column | python heredoc, step 2 — extracts one text column, numbers each response |
| Noise filter | blank, "n/a"/"none"/"idk", <3 words, or off-question → quarantine list |
| Cluster | read every response; assign 1–2 themes each; merge themes until 4–8 remain |
| Count audit | sum of theme assignments ≥ signal responses; each response tagged ≥1 |
| Quote pick | verbatim, ≤30 words, with response # for traceability |

## Procedure

1. **Precheck** — confirm the source: a CSV file + column name, or pasted text (one response per line). Confirm what question the respondents were answering — themes are meaningless without the prompt. `command -v python3` if loading from CSV.
2. **Load and number** — every response gets an ID so quotes stay traceable:
   ```bash
   python3 - "$FILE" "$COLUMN" <<'PY'
   import csv, sys
   rows = list(csv.DictReader(open(sys.argv[1], newline='', encoding='utf-8-sig')))
   for i, r in enumerate(rows, 1):
       print(f"[{i}] {r[sys.argv[2]].strip()}")
   print(f"-- total: {len(rows)}")
   PY
   ```
3. **Split signal from noise** — quarantine: blanks, "n/a"-class answers, responses under 3 words with no content ("good", "nothing"), and answers to a different question. Record IDs and count. Noise is reported, never counted in themes.
4. **First-pass tagging** — read every signal response (all of them — no sampling under 500) and tag each with 1–2 candidate themes phrased as claims ("onboarding is confusing", not "onboarding"). Let themes emerge from the words used; don't force answers into a preset frame.
5. **Merge and name** — collapse overlapping candidates until 4–8 themes remain. A theme needs ≥3 responses (or ≥5% of signal); smaller ones go to "Long tail". Name each theme in the respondents' own vocabulary.
6. **Count and quote** — count responses per theme (a response tagged twice counts in both — say so in the table footer). Pick 1–2 verbatim quotes per theme with their `[#]` IDs. Quotes must be exact strings from step 2's output.
7. **Deliver** — fill the template. Rank themes by count. The "so what" per theme states what a founder should do or test next, labeled with confidence.

## Output Template

```
# Survey Synthesis — <survey/question> — <date>
Responses: N total | N signal | N noise (quarantined, listed below)

| # | Theme | Count | % of signal | Verbatim evidence |
|---|---|---|---|---|
| 1 | <claim-phrased theme> | 14 | 33% | "[7] <exact quote>" |
Footer: responses may carry 2 themes; tags total N.

## So what
1. <Theme 1> — <action/test to run> (confidence: high/med/low — <why>)
2. ...

## Long tail & noise
- Long tail (<3 mentions each): <one-line list>
- Noise quarantined: IDs <list> — <reason classes>
```

## Pitfalls

- **Paraphrase dressed as quote** — a cleaned-up "quote" that no respondent actually wrote destroys trust the first time someone checks. Recovery: quotes only via copy-paste from the numbered output; keep the `[#]` so anyone can verify; paraphrase goes in the theme name, not in quote marks.
- **Themes that mirror the founder's roadmap** — tagging answers into the categories the user hoped for. Recovery: do first-pass tagging in the respondents' vocabulary before looking at the user's feature list; if a theme has zero verbatim support, it isn't a theme.
- **Counts that don't reconcile** — theme counts sum to more than tagged responses can justify, or quarantined noise sneaks into percentages. Recovery: run the audit in Verification; percentages always use signal count as denominator and the footer discloses double-tagging.
- **One vivid quote outweighing twelve dull ones** — the memorable answer gets ranked above the frequent one. Recovery: rank strictly by count; vividness earns a quote slot, not a rank.
- **Sampling a big pile** — reading 50 of 300 and extrapolating. Recovery: read everything up to ~500; beyond that, say explicitly that responses were sampled, how many, and label all counts "estimated from sample".

## Verification

- [ ] Every quote string-matches a numbered response exactly (spot-check 3)
- [ ] signal + noise = total responses; theme % uses signal as denominator
- [ ] Every signal response carries ≥1 theme tag
- [ ] 4–8 themes, each ≥3 responses or ≥5% of signal
- [ ] Each "so what" has a confidence label with a reason
