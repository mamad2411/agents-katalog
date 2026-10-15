---
name: privacy-policy-diff-summarizer
description: Diff two privacy policy texts and produce a vendor-neutral summary of materially changed sections and risk flags.
---

## When to invoke
- You have an updated privacy policy and need a quick summary of changes.
- You need to flag potentially material changes (data collected, sharing, retention, user rights).
- You want an evidence-backed diff that can be reviewed by legal/compliance.

## Inputs needed
- `--old` path to the previous policy text (UTF-8)
- `--new` path to the updated policy text (UTF-8)

## Workflow
1. Normalize whitespace and split into paragraphs.
2. Compute a paragraph-level diff.
3. Extract:
   - added and removed paragraphs
   - most-changed paragraphs (by similarity)
4. Apply heuristic risk flags (keyword rules), e.g.:
   - new data categories: location, biometrics, health, children
   - new sharing: advertisers, partners, affiliates
   - retention expansion
   - cross-border transfers
5. Emit a JSON report with:
   - change summary
   - top changes (with old/new snippets)
   - triggered risk flags

## Output format
JSON to stdout:
- `material_change_score` (0-100)
- `added_paragraphs`, `removed_paragraphs`
- `changed_paragraph_pairs`
- `risk_flags`

## Guardrails
- Vendor-neutral: operates on plain text and heuristic rules only.
- Not legal advice; always route to counsel for final review.
- Avoid overconfident conclusions: report evidence (snippets) for each flag.

## Reference code
- `privacy_policy_diff_summarizer.py`
