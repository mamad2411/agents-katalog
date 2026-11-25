---
name: redditlens
description: Find real pain points on Reddit for any product, niche, or audience, then draft value-first replies the user can post. Interactive Q&A drives the search; outputs a pain-point report with reply drafts.
user-invocable: true
---

# redditlens

Find real pain points on Reddit and draft replies that a founder, indie hacker, or marketer could actually post without getting downvoted into oblivion.

## When to use

- User asks to "find pain points on Reddit" for a product, niche, or audience
- User wants market research before building a feature or landing page
- User wants to find Reddit threads where they can genuinely help and mention their product
- User says "find me customers on Reddit" or "what are people complaining about in X"

## How to use

This skill drives a 5-question interactive flow, runs searches via the `redditlens` CLI, and produces a structured pain-points report.

### Step 1 — Ask the five questions

Ask these one at a time (not as a dump). Wait for each answer before the next.

1. **What are you researching?** (product, niche, or topic — one sentence)
2. **Who is your target user?** (e.g., solo devs, SaaS founders, parents, remote workers)
3. **Any specific subreddits in mind, or should I discover them?** (comma-separated, or "discover")
4. **Time window?** (day / week / month / year — default: month for pain points)
5. **Reply tone?** (helpful, casual, professional, technical)

### Step 2 — Discover subreddits (if needed)

If the user said "discover", run:

```bash
redditlens subreddits "<niche from Q1+Q2>"
```

Pick 3-5 most relevant subreddits from the result.

### Step 3 — Search for pain-point language

Don't search for the product name. Search for the **pain** in the user's own words. Run 2-3 searches with phrases like:

- `"I hate" <topic>`
- `"looking for alternative" <topic>`
- `"is there a better way" <topic>`
- `"anyone else" <topic> "frustrated"`
- `"why does <topic>" OR "problem with <topic>"`

Example:

```bash
redditlens search "I hate notion" --subreddits productivity,ObsidianMD,PKMS --period month --limit 15 --comments
redditlens search "notion alternatives" --period month --limit 15 --comments
```

Always pass `--comments` for pain-points research — the top comments carry the actual complaints.

### Step 4 — Cluster pain points

Read the posts and top comments. Group them into 3-6 distinct pain clusters. For each cluster, extract:

- **The pain** (in the user's own words, 1 sentence)
- **How often it appears** (count of posts/comments)
- **Representative quote** (direct from a comment, with the subreddit)
- **Who feels it** (what kind of user is complaining)

### Step 5 — Pick reply opportunities

From the search results, select the top 3-5 posts where:

- The post is a genuine question or frustration (not a rant, not a meme)
- The pain aligns with the user's product/niche
- The post is recent enough that a reply would still be seen
- The existing replies don't already solve the problem perfectly

### Step 6 — Draft replies

For each picked post, draft a reply that:

- **Starts with empathy**, not a pitch ("I had the same issue when..." not "Check out my product!")
- **Gives real value first** — a concrete tip, workflow, or insight the user can apply even without the product
- **Mentions the product ONCE, softly**, at the end, only if truly relevant ("I ended up building X to solve this for myself — happy to share if useful")
- **Matches the tone the user picked** in Q5
- **Is short** — 3-5 sentences max. Long replies on Reddit get ignored.
- **Never uses AI tells** — no "I hope this helps!", no "Great question!", no em dashes as pauses

If the user said the reply should NOT mention their product, skip the soft mention entirely and just give value.

### Step 7 — Output the report

Produce a single markdown report with these sections:

```markdown
# Pain Points Report: <topic>

## Summary
<2-3 sentences — the biggest finding>

## Pain Clusters

### 1. <Pain in plain language>
- **Frequency**: <N posts, M comments>
- **Who**: <user type>
- **Quote**: "<direct quote>" — r/<subreddit>

<repeat for each cluster>

## Reply Opportunities

### Post 1: <title>
- **URL**: <reddit url>
- **Subreddit**: r/<sub>
- **Score**: <score> · **Comments**: <n>
- **Why this one**: <1 sentence>

**Draft reply**:
> <the draft>

<repeat for each pick>

## Recommended Next Steps
<3 bullets: things the user should do with this report>
```

## CLI reference

```bash
redditlens search "<query>" [--subreddits a,b] [--period day|week|month|year] [--limit N] [--comments]
redditlens post <reddit-url> [--comments]
redditlens subreddits "<niche>"
```

Environment:
- `SERPER_API_KEY` — required. Free 2500 queries at https://serper.dev
- `PROXIES_FILE` — optional. Path to `ip:port:user:pass` list (one per line). If unset, runs in polite-throttle mode (1 request/second, exponential backoff on 429).

## Guidelines

- **Never hallucinate Reddit content.** Only use data returned by the CLI.
- **Always pass `--comments`** when searching for pain points.
- **Don't search for brand names** in Step 3 — search for the pain language.
- **Never draft spammy replies.** If a post isn't a good fit, skip it. Better 2 great replies than 5 mediocre ones.
- **Respect the rate limit** when running without proxies. The CLI handles throttling, but don't fire 10 commands in parallel.
- If `SERPER_API_KEY` is missing, tell the user exactly how to get one: sign up at https://serper.dev, free plan gives 2500 queries, then `export SERPER_API_KEY=...`.
