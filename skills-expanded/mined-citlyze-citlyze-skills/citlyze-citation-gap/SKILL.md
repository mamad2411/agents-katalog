---
name: citlyze-citation-gap
description: Analyze which domains AI engines cite for your tracked prompts and find citation gaps to close. Use when asked "which domains get cited", "why are competitors cited and not us", "citation gap analysis", or to build an outreach/content target list from AI citation data. Requires the Citlyze MCP server.
license: MIT
metadata:
  author: Citlyze (https://www.citlyze.com)
---

# Citlyze citation gap analysis

Turn raw citation data into a classified gap map: who AI engines trust today, where your owned pages are missing, and which third-party surfaces are worth pursuing.

## Prerequisites

The [Citlyze](https://www.citlyze.com) MCP server must be connected ([setup guide](https://www.citlyze.com/docs/mcp/setup-clients)). Tools are read-only and default to the latest completed measurement window.

## Workflow

1. **Orient.** Call `get_workspace_overview` for the target brand and competitor list.
2. **Pull citations.** Call `list_citations`. Each entry in `domains` has `domain`, `citation_count`, and up to a few `sample_citations` (`url`, `title`). Use a higher `limit` (max 100) for fuller coverage.
3. **Classify every domain** into channels, using the brand's own domains and competitor names from step 1 plus the sample URLs/titles:
   - owned domains
   - competitor sites
   - peer companies
   - earned media (press, publishers, news)
   - user reviews and review platforms
   - user-generated content (forums, Q&A)
   - social platforms
   - affiliate sites
   - other third-party sources
   Also tag the apparent content type where the samples make it obvious: listicle/top list, comparison, blog or news, research or report, documentation, product page, wiki-style, social.
4. **Find the gaps.** Ask three questions of the classified table:
   - Where do competitors get cited on surfaces you are absent from (a listicle or review site citing them, not you)?
   - Which heavily cited third-party domains accept contributions, listings, or reviews you could legitimately pursue?
   - What share of citations is owned vs everything else, and is any owned page conspicuously missing for its topic?
5. **Deliver two artifacts:**
   - **Citation map table**: domain, channel, content type, citation count, one-line "why it gets cited".
   - **Target list**: top 5-10 actions, each with domain, action (pitch a listing, publish comparison page, earn a review, improve owned page), and expected difficulty.

## Interpretation rules

- A citation means the engine showed a link; it does not guarantee your brand was named in the answer. Keep citation, mention, and source consulted separate.
- Classification from domain names is approximate; mark uncertain rows rather than guessing confidently.
- High citation counts on one domain across many prompts usually matter more than one-off citations.

Learn more: [Citations in Citlyze](https://www.citlyze.com/docs/using-citlyze/citations) - [citlyze.com](https://www.citlyze.com)
