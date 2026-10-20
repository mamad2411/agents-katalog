---
name: research-gaps
description: Use when the user wants competitor content-gap analysis to identify keywords competitors rank for that this site does not.
---

# Research Gaps

Run the competitor gap analysis.

## Command

```bash
.venv/bin/python research_competitor_gaps.py
```

## Output

The script writes a report to `research/competitor-gaps-<date>.md`.

## Notes

- This workflow usually requires DataForSEO credentials and API spend.
- If credentials are unavailable, prefer `research-topics` or `priorities --skip-gaps`.
