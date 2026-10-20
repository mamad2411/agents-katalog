---
name: landing-write
description: Use when the user wants a conversion-focused landing page rather than a blog article. This skill writes SEO or PPC landing pages and then recommends running the landing audit script.
---

# Landing Write

Create a landing page optimized for either SEO intent or PPC message match.

## Inputs

- Topic or research brief
- `--type seo|ppc`
- `--goal trial|demo|lead`

## Read First

- `context/cro-best-practices.md`
- `context/brand-voice.md`
- `context/features.md`
- Any landing research brief already saved in `research/`

## Output

Save to:

`landing-pages/<topic-slug>-<YYYY-MM-DD>.md`

The file should include at least:

- `Meta Title`
- `Meta Description`
- `Target Keyword`
- `Page Type`
- `Conversion Goal`
- `URL Slug`

## After Saving

```bash
.venv/bin/python scripts/run_landing_audit.py landing-pages/<page-file>.md --type <seo|ppc> --goal <trial|demo|lead>
```
