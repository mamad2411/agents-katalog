---
name: landing-audit
description: Use when the user wants a CRO and landing-page quality audit on a local landing page draft. This skill runs the landing audit script and then applies the highest-priority fixes.
---

# Landing Audit

Audit a local landing page draft with the dedicated landing-page analyzers.

## Command

```bash
.venv/bin/python scripts/run_landing_audit.py landing-pages/<page-file>.md --type seo --goal trial
```

## What The Script Covers

- Landing page scoring
- Above-the-fold analysis
- CTA analysis
- Trust signal analysis
- CRO checklist review

## What Codex Should Add

- Turn the report into an editing plan
- Fix the page directly if requested
- Re-run the audit after meaningful changes
