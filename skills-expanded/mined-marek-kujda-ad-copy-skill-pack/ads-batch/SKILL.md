---
name: ads-batch
description: Bulk-generate RSAs for multiple ad groups at once. Use when the user wants to create ads for several ad groups or an entire campaign in one go.
allowed-tools: Read, Write, Bash
---

# /ads-batch — Bulk Generate RSAs for Multiple Ad Groups

## Input Required
Ask the user to provide a list of ad groups with their keywords, either as:
- A CSV/text file in the project directory
- Or inline in the conversation

Expected format per ad group:
```
Campaign: [name]
Ad Group: [name]
Keywords: [keyword1], [keyword2], [keyword3]
Landing Page: [URL]
USP: [unique selling point for this ad group]
```

## Execution
1. Parse all ad groups from input
2. For each ad group, run the full `/ads` workflow:
   - Load brand voice from `.claude/skills/brand-voice/SKILL.md`
   - Load ICP and persona from `.claude/skills/icp/SKILL.md`
   - Load platform rules from `.claude/skills/google-ads-rules/SKILL.md`
   - Generate 15 headlines + 4 descriptions
   - Validate character limits
   - Check keyword presence
3. Combine all ad groups into a SINGLE CSV file
4. Save to `output/rsa_batch_[campaign]_[date].csv`
5. Run `python .claude/skills/ads/validate.py` on the output
6. Present a summary table:

```
| Ad Group | Headlines | Descriptions | Keyword Coverage | Issues |
```

## Notes
- Maintain consistent brand voice across all ad groups
- Each ad group should have UNIQUE copy — no recycling between groups
- If >5 ad groups, suggest splitting into batches for quality review
