# Reddit Writer

```yaml
name: reddit-writer
description: >
  Creates Reddit posts across relevant subreddits. Covers benchmarks,
  postmortems, journey posts, Show posts, and AMAs. Optimized for
  community trust and authenticity.
triggers:
  - reddit post
  - post to reddit
  - reddit thread
```

---

## MCP connectors

| Connector | Purpose |
|-----------|---------|
| Reddit | Post and comment (via browser) |

## Format Library

### Benchmark Post
**When to use:** Sharing data, test results, or comparisons relevant to a subreddit.

```
Title: [Tool A] vs [Tool B] vs [Tool C]: I tested [what] across [scope]

Body:
[1-2 sentences on why you ran this benchmark]

## Setup
[What you tested, hardware/environment, methodology]

## Results
[Table or list of findings]

## Analysis
[What surprised you, caveats, limitations]

## My Take
[Brief, honest interpretation]

Happy to share the raw data if anyone wants to dig in.
```

### Postmortem
**When to use:** Sharing a failure, mistake, or hard lesson with enough detail to be useful.

```
Title: How we [broke/lost/wasted] [thing] and what we learned

Body:
[What happened in 2-3 sentences]

## Timeline
[Chronological account - what went wrong and when]

## Root Cause
[The actual cause, not just the symptom]

## What We Changed
[Specific fixes and process changes]

## Lessons
[2-3 transferable lessons]

Ask me anything about the details.
```

### Journey Post
**When to use:** Sharing progress, milestones, or the story of building something.

```
Title: [Time period] of building [thing]: what worked, what didn't

Body:
[One paragraph on what you're building and where you started]

## What Worked
- [Specific tactic + result]
- [Specific tactic + result]

## What Didn't Work
- [Specific failure + what you learned]
- [Specific failure + what you learned]

## Numbers
[Honest metrics - users, revenue, growth, whatever is relevant]

## What's Next
[Where you're headed]

Happy to answer questions about any of this.
```

### Show Post (Show HN, Show [Subreddit])
**When to use:** Launching or demoing something you built.

```
Title: Show [Subreddit]: [What it does in plain language]

Body:
[One sentence on what it is]
[One sentence on why you built it]
[One sentence on how it works]

[Link to demo/repo/site]

Looking for feedback on [specific thing]. What would you want to see?
```

### AMA / Open Q&A
**When to use:** Offering your expertise or experience for questions.

```
Title: I'm [role] who [relevant experience]. AMA about [topic].

Body:
[2-3 sentences establishing credibility without bragging]
[What you can speak to specifically]
[Time commitment - "I'll be answering questions for the next few hours"]
```

---

## Hard Rules

These are non-negotiable on Reddit. Breaking them destroys credibility.

1. **No marketing language.** Reddit detects and punishes corporate speak instantly. Write like a human, not a brand.
2. **Never hide your vendor identity.** If you work for the company you're posting about, say so upfront. "Full disclosure: I'm the CAO/engineer/etc." Astroturfing gets you banned.
3. **Karma thresholds.** Many subreddits require minimum karma to post. Check subreddit rules before posting. Build karma through genuine comments first.
4. **Read the room.** Every subreddit has a different culture. Lurk and read recent posts before contributing.
5. **Self-promotion limits.** Most subreddits follow a 90/10 rule: 90% of your contributions should be helpful comments, 10% can be your own content.
6. **No editorialized titles.** State what it is, not how people should feel about it.
7. **Respond to comments.** Posting and disappearing is a red flag. Budget time to engage.

---

## Subreddit Targeting Template

Before posting, fill this out:

```yaml
subreddit: r/[name]
subscribers: [number]
culture: [technical/casual/meme-heavy/strict-moderation]
self_promotion_rules: [link to rules or summary]
minimum_karma: [if any]
flair_required: [yes/no, which flair]
best_posting_time: [day/time based on subreddit activity]
recent_relevant_posts: [links to 2-3 similar posts that did well]
```

---

## What Gets Downvoted

- Anything that reads like an ad
- "We just launched [product]!" without substance
- Vague posts without specific details or data
- Refusing to answer hard questions in comments
- Posting the same content to 10 subreddits simultaneously
- Emoji-heavy posts (Reddit culture is text-first)
- Clickbait titles that oversell the content

## Self-improvement

After the CAO reviews and approves a Reddit post:

1. Move the final version from `content/reddit/_drafts/` to `content/reddit/_published/`
2. Diff what was drafted vs what the CAO kept - identify patterns in her edits to tone, format, or subreddit targeting
3. Update `content/reddit/_insights.md` with what worked, what she changed, and why (add upvote/comment metrics after 48 hours)
4. If her edits reveal a new rule (e.g. "always disclose vendor status in the first line", "never cross-post the same week"), add it to the Hard Rules section
5. If a post performs well, save it to `content/reddit/_examples/` with subreddit context and performance annotations
