---
name: daily-news-report
description: Research current news and create concise sourced daily briefings, market updates, AI news reports, Thailand news summaries, or scheduled news digests. Use when the user asks for daily news, current events, latest updates, recurring news reports, or news monitoring.
---

# Daily News Report

Create a high-signal Markdown briefing from current, sourced information.

## Workflow

1. Define scope
   - Use the user's requested topic, geography, industry, audience, and time window.
   - If no scope is provided, cover world headlines, Thailand, markets, business, technology, AI, and policy items with broad practical impact.
   - Use the current date explicitly in the report title.

2. Gather sources
   - Use recent reputable sources.
   - Prefer primary reporting, official statements, regulator pages, company announcements, and established newsrooms.
   - Prioritize the last 24 hours unless the user requests a broader window.
   - Cross-check major claims when possible — see [research-methodology](../research-methodology/SKILL.md) for source-tiering and telling real corroboration apart from several outlets repeating one wire story.

3. Filter and rank
   - Keep only items that are significant, new, and useful.
   - Rank by public impact, market impact, policy impact, technology impact, novelty, and urgency.
   - Avoid duplicate stories and low-impact viral items.

4. Write the report
   - Respond in the user's language.
   - Keep code, source names, URLs, company names, model names, and structured keys in English when appropriate.
   - Use concise paragraphs and clear bullets.
   - Include links for every major item.

5. Verify
   - Confirm every major claim has a source.
   - Mark uncertain or developing items clearly.
   - Separate fact from inference.
   - Run [claim-citation-check](../claim-citation-check/SKILL.md) before finalizing — it catches uncited factual sentences that slipped through.

## Output Format

```markdown
# Daily News Report - YYYY-MM-DD

## Summary

## Top Stories

### 1. [Headline]
- Summary:
- Why it matters:
- Possible impact:
- Sources:

## Markets And Business

## Technology And AI

## Thailand

## Watch Next

## Sources
```

## Rules

- Never present unverified rumors as fact.
- State uncertainty clearly when a story is developing.
- If asked to write a file, use `news-report-YYYY-MM-DD.md`.
- Browse or use current-source tools for any latest, today, market, legal, political, product, or rapidly changing topic.
