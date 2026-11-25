---
name: hacker-news-digest
description: Scan Hacker News for trending topics relevant to ArtStroy's content pillars (QA automation, pentesting, programming). Extracts article-worthy signals and scores them for topic brief creation.
---

# Hacker News Digest

Scan the Hacker News front page and "Ask HN / Show HN" sections for topics that could become ArtStroy articles.

## What to Scan

- HN front page (top ~30 stories)
- "Ask HN" posts with ≥50 points
- "Show HN" posts with ≥30 points
- Comments on highly-voted programming/security posts (sometimes the best signal is a problem people describe in comments)

Use the Algolia HN API for structured access:
```
https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=30
https://hn.algolia.com/api/v1/search?query=playwright+testing&tags=story&hitsPerPage=10
```

## ArtStroy Content Pillars

Filter for relevance to:

| Pillar | Categories |
|---|---|
| **QA Automation** | Playwright, Cypress, testing strategies, CI/CD quality gates, flaky tests, visual regression |
| **Pentesting** | OWASP findings, CVEs, security tooling, bug bounty write-ups, exploit techniques (educational) |
| **Programming** | TypeScript, Astro, React, Bun/Node, API design, developer tooling, performance patterns |

Discard: finance, crypto, hardware, politics, non-technical content.

## Scoring

For each candidate story, score on three dimensions (1–5 each):

| Dimension | 1 | 3 | 5 |
|---|---|---|---|
| **Relevance** | Tangentially related | Directly on a pillar | Core to a content gap on artstroy.net |
| **Timeliness** | Old news (>30 days) | Active discussion now | Trending today, article within 48h = first-mover |
| **Uniqueness** | Already covered on artstroy.net | Related but different angle | Not covered anywhere on site |

**Threshold**: score ≥10/15 to include in topic brief output.

## Output

For each qualifying story, produce a candidate entry:

```markdown
### {Story Title}
- **HN link**: {url}
- **Points / Comments**: {points} pts, {comments} comments
- **Score**: {relevance}/5 + {timeliness}/5 + {uniqueness}/5 = {total}/15
- **Pillar**: QA / Pentesting / Programming
- **Article angle**: {1–2 sentences on how artstroy.net would cover this differently/better}
```

Pass all candidates with score ≥10 to the `topic-brief` skill for formatting as a proper brief to EIC.
