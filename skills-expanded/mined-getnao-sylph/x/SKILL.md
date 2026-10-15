# X/Twitter Writer

```yaml
name: x-writer
description: >
  Creates X/Twitter content - single tweets, threads, quote-tweets,
  and demo clips. Optimized for the algorithm and leadership audiences.
triggers:
  - tweet
  - x post
  - twitter thread
  - write a tweet
```

---

## MCP connectors

| Connector | Purpose |
|-----------|---------|
| X/Twitter | Post tweets, read engagement (via browser) |

## Format Library

### Contrarian Thread (3-8 tweets)
**When to use:** Challenging conventional wisdom with evidence.

```
Tweet 1: [Bold claim that stops the scroll]

Tweet 2: Here's why everyone says [opposite]: [1-2 sentences]

Tweet 3-6: [Your counter-evidence, one point per tweet]

Tweet 7: The nuance: [when the conventional wisdom IS right]

Tweet 8: TL;DR: [one sentence summary + CTA]
```

### Demo Clip
**When to use:** Showing your product doing something impressive.

```
[One sentence describing what you're about to show]

[Attach video/GIF - 30-60 seconds max]

[Optional: one sentence on what to notice]
```

Keep text minimal. The clip does the work.

### Ship Log
**When to use:** Quick announcement of something you shipped today.

```
Shipped: [feature name]

[One sentence on what it does]

[One sentence on why it matters]

[Screenshot or GIF]
```

### Quote-Tweet
**When to use:** Adding your perspective to someone else's post.

```
[Your take - not just "This" or "100%"]

[1-2 sentences adding context, disagreement, or a personal angle]
```

Never quote-tweet just to agree. Add value or don't QT.

### Leadership POV
**When to use:** Sharing a personal insight, lesson, or observation.

```
[The insight in one sentence]

[The story behind it in 2-3 sentences]

[Optional: what you're doing differently now]
```

---

## Hook Patterns

The first line must work in a timeline of noise. Patterns that work:

- **Specific number**: "We went from 200ms to 12ms query time"
- **Contrarian claim**: "Your data warehouse is a liability, not an asset"
- **Before/after**: "Before: 3 dashboards nobody used. After: one question anyone can ask."
- **Confession**: "I spent 6 months building the wrong thing"
- **Observation**: "Every data team I talk to has the same problem"

Patterns that don't work:
- "Thread:" (don't announce it, just write it)
- "Hot take:" (let the take speak for itself)
- "Unpopular opinion:" (usually a popular opinion)

---

## Cadence

- **Singles**: 3-5 per week, spread across mornings (weekdays)
- **Threads**: 1-2 per week max. Threads that aren't worth 5+ tweets aren't worth threading.
- **Demo clips**: Whenever you ship. These have the highest save/share ratio.
- **Quote-tweets**: Opportunistic. Only when you have a genuine addition.

---

## What Doesn't Work on X

- Long corporate announcements (save for LinkedIn)
- Hashtag stuffing
- "We're hiring!" without context
- Engagement bait ("Like if you agree")
- Threads that should have been a blog post
- Tweeting at brands hoping for a RT
- Self-congratulatory milestone posts without substance

---

## Voice Rules

- Maximum 280 characters for singles (obvious, but enforce it)
- Lowercase is fine for casual tone
- No em dashes. Use hyphens or just break into two sentences.
- Abbreviations are fine (b/c, w/, etc.) - this is X, not a blog
- Tag people sparingly and only when they'd genuinely want to see it
- Never use "Excited to announce" - just announce

## Self-improvement

After the CAO reviews and approves X posts:

1. Move the final version from `content/x/_drafts/` to `content/x/_published/`
2. Diff what was drafted vs what the CAO kept - identify patterns in her edits to hooks, tone, or format choices
3. Update `content/x/_insights.md` with what worked, what she changed, and why
4. If her edits reveal a new rule (e.g. "never start with a question on X", "demo clips need zero intro text"), add it to the Voice Rules or Hook Patterns sections above
5. If a post performs well (high impressions, saves, or replies), promote it to `content/x/_examples/` with performance annotations
