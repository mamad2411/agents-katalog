---
name: last30days
description: Researches a topic from the last 30 days on Reddit, X, and the web to surface community sentiment and actionable insights.
allowed-tools:
- Bash
- Read
- Write
- AskUserQuestion
- WebSearch
- mcp__exa__web_search_exa
metadata:
  version: 0.2.0
  category: trail-of-bits
---
# last30days: Research Any Topic from the Last 30 Days

## Quick Start
```bash
python3 "../scripts/last30days.py" "$TOPIC" --emit=compact 2>&1
```

## Workflow
1. **Parse Intent**: Extract TOPIC, TARGET_TOOL, and QUERY_TYPE (PROMPTING, RECOMMENDATIONS, NEWS, or GENERAL).
2. **Execute Research**: Run the research script and supplement with targeted WebSearches in parallel.
3. **Synthesize Findings**: Weight Reddit/X higher than web sources and extract top 3-5 patterns/insights.
4. **Present Results**: Show "What I learned", list patterns/recommendations with citations, and provide a stats summary.
5. **Invite Vision**: Offer to answer follow-up questions or generate a perfect, tailored prompt based on the research.
6. **Execute Follow-up**: Write a prompt or answer questions using the expert knowledge gained during research.

## Rules & Constraints
- **CITE-1**: Cite sources sparingly using `@handle` (X) or `r/sub` (Reddit). Prioritize people over publications.
- **URL-1**: NEVER include raw URLs in output. Use publication names or social handles.
- **FORMAT-1**: When writing prompts, match the EXACT format (JSON, structured, etc.) recommended by the research.
- **GND-1**: Ground all synthesis in actual research content; avoid using pre-existing knowledge.

## When to Use
- Researching recent community sentiment, recommendations, or trending discussions.
- Understanding "what's new" or "best X" before making a decision.
- Generating copy-paste prompts using the latest community-discovered techniques.

## When NOT to Use
- Historical data older than 30 days is required.
- Official documentation or API references are needed (use specialized tools).
- Factual questions that do not benefit from community sentiment.

## References
- [Skill Manual](references/last30days-manual.md)
- [Reddit Official API](https://www.reddit.com/dev/api/)
- [X API Documentation](https://developer.x.com/en/docs)
