---
name: tweet-digest
description: Monitor Twitter/X for trending discussions in QA, security, and programming communities. Captures practitioner sentiment and emerging technique discussions as article signals.
---

# Tweet Digest

Twitter/X reveals real-time practitioner conversation — what developers and security engineers are actively discussing, debating, or frustrated about. High-signal topics here often become articles.

## How to Search

Use the Exa API (`EXA_API_KEY`) for semantic search across Twitter content, or the Twitter/X API if credentials are configured:

```
Search queries to run:
- "playwright testing" site:twitter.com past:7days
- "OWASP vulnerability" site:twitter.com past:7days
- "astro.js performance" site:twitter.com past:7days
- "typescript pattern" site:twitter.com past:7days
- "bun vs node" site:twitter.com past:7days
- "pentesting technique" site:twitter.com past:7days
```

Focus on tweets with ≥50 likes or threads with visible engagement (replies, quotes).

## Key Accounts to Monitor

These accounts consistently publish content aligned with ArtStroy's pillars:

**QA / Testing:**
- Playwright team announcements
- Known Playwright contributors
- QA engineering thought leaders

**Security:**
- OWASP official
- Known pentesters with public write-ups
- CVE disclosure threads

**Programming:**
- Astro core team
- TypeScript team
- Bun team announcements

When a tweet from a verified key account announces a new feature or breaking change, that's a ≥4 timeliness score automatically — ArtStroy covering it within 48h has first-mover value.

## What to Capture

**High-value signals:**
- A practitioner thread explaining a technique or problem
- Debate about two approaches where artstroy.net could be the authoritative reference
- A new release announcement that warrants a "how to use X" article
- A common misconception thread → "the correct answer" article

**Low-value signals:**
- Hot takes without substance
- Vendor marketing
- Job posts

## Scoring

Same rubric: Relevance + Timeliness + Uniqueness, 1–5 each. Threshold: ≥10/15.

**Twitter-specific**: a tweet thread going viral (>500 engagement) on a topic artstroy.net hasn't covered is an automatic ≥13/15 — prioritize immediately.

## Output

```markdown
### {Thread topic or tweet summary}
- **Source**: @{handle} | {url}
- **Engagement**: {likes}, {reposts}
- **Score**: {R}/5 + {T}/5 + {U}/5 = {total}/15
- **Pillar**: QA / Pentesting / Programming
- **ArtStroy angle**: {what the article would add that the thread doesn't cover}
```

Pass qualifying candidates to `topic-brief` skill.
