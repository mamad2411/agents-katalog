---
name: claim-receipts
description: Audits product writing (READMEs, launch pages, decks, case studies, resumes, PRDs, investor updates) for claims that are not backed by evidence, labels each claim, and rewrites unsupported ones. Use when the user asks to fact-check, review, tighten, or "make honest" any product or marketing copy, or before publishing anything with numbers or outcomes in it.
---

# Claim receipts

Every claim in product writing should be able to show its receipt: where it came from and what it covers. This skill finds the claims that cannot, and fixes the wording instead of inventing support.

## Workflow

1. **Extract claims.** List every sentence that states a fact, number, outcome, comparison, or capability. Skip opinions that are clearly framed as opinions.
2. **Find the receipt.** For each claim, look for support in the files, links, data, or notes the user provided. Do not search your own memory for support and do not assume.
3. **Label each claim** with exactly one label:

| Label | Meaning |
|---|---|
| `SOURCED` | A provided source states this directly. Cite it. |
| `MEASURED-WITH-SCOPE` | A measurement exists, but the claim needs its scope attached (sample, date, conditions). |
| `ASSUMPTION` | A plan, estimate, or belief. Fine to keep if worded as one. |
| `UNSUPPORTED` | No receipt found. Rewrite, ask for the source, or cut. |

4. **Rewrite** every `MEASURED-WITH-SCOPE`, `ASSUMPTION`, and `UNSUPPORTED` claim. Rewrites may only remove or narrow. Never add a number, customer, outcome, or adjective that was not in a source.
5. **Report** using the template below.

## Red flags to check first

- Outcomes stated as results when they come from a simulation, demo data, or a plan.
- Percentages without a denominator, or a denominator without a date.
- "Users", "customers", or "teams" when the source shows testers, a pilot, or one client.
- Process metrics presented as quality metrics (jobs completed is not answers correct).
- Superlatives: first, only, best, leading, revolutionary, 10x.
- Credit drift: "I built" when the source shows a team, or "we" hiding who did what.
- Model output presented as verified fact.

## Output template

```markdown
## Claim receipts: [document name]

| # | Claim (quoted) | Label | Receipt or gap | Suggested rewrite |
|---|---|---|---|---|
| 1 | "..." | SOURCED | [source, section] | keep |
| 2 | "..." | UNSUPPORTED | no source provided | "..." |

**Summary:** N claims checked. X sourced, Y need scope, Z assumptions, W unsupported.
**Questions for the author:** sources that would let an UNSUPPORTED claim stay.
```

## Example

Input sentence (a deliberately bad draft): "CrediClip analyzed 780 videos with 97% reliability."

Receipt available: a batch summary showing all 780 jobs completed (two after retry), and 759 of 780 results flagged as low evidence.

Output row:

| 1 | "analyzed 780 videos with 97% reliability" | MEASURED-WITH-SCOPE | Batch summary: 780 of 780 jobs completed; 759 of 780 flagged low evidence. "97%" matches no reported figure. | "In one 780-link YouTube batch, every job completed, but 759 of 780 results were flagged as low evidence." |

The rewrite is less flattering and more useful: it tells the reader what the system did and where it still falls short.
