---
name: reddit-digest
description: Monitor relevant subreddits for questions, problems, and pain points that reveal content gaps on artstroy.net. Top questions with no good answer are article opportunities.
---

# Reddit Digest

Reddit's value as a content signal source is different from HN or RSS. It reveals **what questions practitioners are actually asking** — these make excellent article topics because demand is proven.

## Subreddits to Monitor

| Subreddit | Pillar | What to look for |
|---|---|---|
| `r/QualityAssurance` | QA | Unanswered questions, frustration posts |
| `r/softwaretesting` | QA | Common pain points, tool comparisons |
| `r/netsec` | Pentesting | Educational technique questions, CVE discussions |
| `r/hacking` (legal context) | Pentesting | Ethical hacking questions |
| `r/webdev` | Programming | Astro/React questions, performance issues |
| `r/typescript` | Programming | Type system problems, TS 5.x features |
| `r/node` | Programming | Bun/Node ecosystem shifts |

## API Access

Reddit provides a public JSON API (no auth required for read):
```
https://www.reddit.com/r/{subreddit}/top.json?t=week&limit=25
https://www.reddit.com/r/{subreddit}/hot.json?limit=25
```

Use `EXA_API_KEY` for deeper Reddit search if needed (Exa can search Reddit content semantically).

## What to Capture

**Best signals:**
- Questions with many upvotes but no accepted/highly-voted answer → content gap
- Posts describing a specific pain point with a tool artstroy.net covers
- "Is there a guide for X?" posts → explicit article request

**Skip:**
- Rant posts without a clear question
- Questions already answered in top comment
- Off-topic (job posts, memes)

## Scoring

Same rubric as other digest skills: Relevance + Timeliness + Uniqueness, 1–5 each. Threshold: ≥10/15.

**Bonus for Reddit**: if the same question appears in multiple subreddits or has appeared multiple times in the past month, add +1 to the Uniqueness score (proven demand).

## Output

```markdown
### {Thread Title}
- **Subreddit**: r/{name}
- **Link**: {url}
- **Signal type**: Unanswered question / Pain point / Explicit request
- **Score**: {R}/5 + {T}/5 + {U}/5 = {total}/15
- **Pillar**: QA / Pentesting / Programming
- **ArtStroy angle**: {how to answer the question better than the current top comments}
```

Pass qualifying candidates to `topic-brief` skill.
