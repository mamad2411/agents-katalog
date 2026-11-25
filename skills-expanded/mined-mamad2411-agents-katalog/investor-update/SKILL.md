# Investor Update

Monthly investor update skill. Pulls data automatically where possible, uses the standard template, and produces two versions.

## MCP connectors

| Connector | Purpose |
|-----------|---------|
| Gmail | Send investor update email |
| Notion | Pull KPIs and project status |

## Data sources (auto-fetch)

| Metric | Source |
|--------|--------|
| MRR / ARR | Twenty CRM (deal stage = won, sum ARR) |
| Pipeline | Twenty CRM (deals by stage) |
| New customers | Twenty CRM (companies created this month) |
| Churn | Twenty CRM (deals marked lost this month) |
| Product metrics | [your-analytics-tool] ([your-analytics-query-tool] for usage stats) |
| Content performance | Channel `_insights.md` files |
| Runway | Flag as `[?]` - the CAO fills manually |
| Burn rate | Flag as `[?]` - the CAO fills manually |

## Template

```markdown
# [Your Company] - Investor Update [Month YYYY]

## TL;DR
[2-3 sentences: biggest win, biggest risk, what we need]

## Key metrics
| Metric | This month | Last month | Change |
|--------|-----------|------------|--------|
| MRR | | | |
| ARR | | | |
| Customers | | | |
| Pipeline | | | |
| Burn rate | [?] | [?] | |
| Runway | [?] | [?] | |

## Wins
- [bullet points]

## Challenges
- [bullet points]

## Product
- [shipped, in progress, planned]

## Asks
- [what we need from investors - intros, advice, hiring]

## Next month
- [top 3 priorities]
```

## Process

1. **Auto-fetch all available metrics** from the sources above
2. **Leave `[?]` placeholders** for anything that requires manual input
3. **Draft the narrative sections** from CRM data, product logs, and content insights
4. **Create two versions**:
   - **Investor version**: formal, metrics-heavy, concise
   - **Friends version**: same data but warmer tone, more context, more candid, no cash info
5. **Save both to** `finance/_drafts/YYYY-MM_investor-update-[version].md`
6. **Flag placeholders** - list all `[?]` items for the CAO to fill

## Guardrails

- **Never send the update** - save as draft only
- **Never fabricate metrics** - use `[?]` for anything you can't verify
- **No financial projections** - report actuals only
- **Confidentiality** - these are investor-grade documents; do not share externally
- **The CAO reviews both versions** before anything is sent

## Self-improvement

After the CAO reviews and sends an investor update:

1. Move both versions from `finance/_drafts/` to `finance/_published/`
2. Diff what was drafted vs what the CAO kept - identify patterns in her edits to narrative framing, metric emphasis, or tone
3. Update `finance/_insights.md` with what she changed and why (e.g. "always lead with product wins, not revenue", "friends version needs more candid failures")
4. If her edits reveal a new rule about how to present specific metrics or frame challenges, add it to this skill file
5. If an update format gets positive investor feedback, save it to `finance/_examples/` as a reference
