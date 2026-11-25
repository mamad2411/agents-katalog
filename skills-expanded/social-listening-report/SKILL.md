---
name: social-listening-report
description: Weekly social-listening blueprint — scans the web for chosen keywords and brand mentions, ranks top mentions, reads sentiment, flags reply-worthy threads, and drafts (never posts) suggested replies. Use when the user asks to "monitor mentions", "social listening", "what are people saying about us", "track [keyword] this week", or wants the Friday listening report. Don't use for turning findings into publishable posts — that's content-repurposer or x-thread-builder.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Content & Marketing, Social Listening, Monitoring, Sentiment, Blueprint]
    related_skills: [content-repurposer, x-thread-builder, linkedin-content-pack, brand-voice-guardian, deep-research-brief]
    requires_toolsets: [web]
    blueprint:
      schedule: "0 9 * * 5"
      prompt: "Compile my weekly social listening report"
---

# Social Listening Report

Runs every Friday morning and answers three questions with evidence: what did people say about the brand and its keywords this week, how did it feel, and which conversations deserve a reply. Every mention links to its source, sentiment is judged from quoted text (not vibes), and replies ship as drafts for a human to post — this skill never speaks in public.

## When to Use

- The scheduled Friday run ("Compile my weekly social listening report").
- The user asks ad hoc: "what's the chatter about [brand/keyword]", "any threads I should jump into", "sentiment this week".
- A launch or incident needs a one-off mention sweep.
- **Not for:** turning findings into publishable content (`content-repurposer`, `x-thread-builder`), deep multi-source research on a question (`deep-research-brief`), or posting replies — drafts only, the human presses send.

## Quick Reference

| Action | Command / Call |
|---|---|
| Load watchlist | Read stored keywords/brand terms from memory or config; missing → ask once, save |
| Sweep | `web` search per term: `"[term]"` + site-scoped passes (reddit, x.com/twitter, news, forums), past-7-days framing |
| Fetch mention | `web_extract` the URL; capture quote, author, platform, date, engagement if shown |
| Sentiment | Label each mention + / – / neutral / mixed from its quoted text only |
| Rank | Top mentions by reach/engagement, then relevance; cap report at ~10 |
| Reply-worthy | Question about the product, correctable misinfo, high-visibility praise, fixable complaint |

## Procedure

1. **Precheck** — confirm the `web` toolset responds (one trivial search) and load the watchlist (brand names, product names, 3–8 keywords, founder handle if watched). No watchlist stored → ask the human once, then persist it for future runs. Note the window: last 7 days (or since the previous report).
2. **Sweep** — for each term, run general + platform-scoped searches (Reddit, X, LinkedIn, HN, news). Collect candidate URLs. Recency matters more than volume — an undated result gets fetched and date-checked or dropped.
3. **Extract & log** — `web_extract` each candidate. Log per mention: verbatim quote, platform, author, date, URL, engagement signal if visible. A mention without a working URL doesn't enter the report. Dedupe cross-posts to one entry.
4. **Sentiment + rank** — label each mention from its quoted text: positive / negative / neutral / mixed. Ambiguous or sarcastic → mixed, with a one-line note; never launder sarcasm into praise. Rank by visibility and relevance; keep the top ~10, tally the rest into counts.
5. **Flag reply-worthy threads** — apply the Quick Reference criteria; select 2–5. For each, write a suggested reply DRAFT in brand voice (per `brand-voice-guardian` if attached): helpful, specific, no corporate autopilot. Mark every one `DRAFT — do not auto-post`.
6. **Compare & deliver** — set week-over-week deltas against the previous report if available (volume, sentiment split). Assemble the Output Template and deliver to the human. Post nothing anywhere.

## Output Template

```
# Social Listening Report — week ending [date]
**Watchlist:** [terms] | **Mentions logged:** [n] ([+x/-y/~z/mixed m]) | **WoW:** [delta or "first run"]

## Top mentions
| # | Quote (trimmed) | Platform | Sentiment | Reach signal | Link |
|---|---|---|---|---|---|

## Sentiment read
[3–5 sentences: dominant themes, notable shifts, one surprise — each tied to a linked mention]

## Reply-worthy threads (drafts only)
### [thread title / author] — [why it qualifies]
Link: ... | Suggested reply (DRAFT — do not auto-post):
> [reply text]

## Watchlist health
[terms returning noise or nothing; suggested add/drop for human approval]
```

## Pitfalls

- **Stale results dressed as fresh** — search surfaces a viral 2024 thread and it headlines "this week". Recovery: date-check every logged mention in step 3; anything outside the window is dropped or moved to a clearly-labeled "resurfaced" note.
- **Sentiment from vibes** — a mention gets labeled positive because the summary sounded nice. Recovery: sentiment is assigned only against the verbatim quote in the log; no quote captured → fetch again or drop the mention.
- **Auto-posting a reply** — the reply draft is good, tooling can post, and the agent "saves a step". Recovery: hard rule — this skill has no posting step; if a reply was posted, tell the human immediately with the link. Public speech is human-only.
- **Watchlist drift** — a generic keyword floods the report with irrelevant noise week after week. Recovery: use the Watchlist health section; propose the add/drop, apply only after human approval.
- **Zero-mention panic padding** — a quiet week gets filled with barely-relevant results to look thorough. Recovery: a short honest report ("4 mentions, all neutral") is the correct output; note quietness as a data point, not a failure.

## Verification

- [ ] Every mention in the report has a verbatim quote, date inside the window, and a fetched (not invented) URL
- [ ] Sentiment labels trace to quoted text; sarcastic/ambiguous items marked mixed with a note
- [ ] 2–5 reply-worthy threads, each with criteria stated and a reply marked `DRAFT — do not auto-post`
- [ ] Nothing was posted, replied to, or liked by the agent anywhere
- [ ] WoW comparison present (or "first run" stated); watchlist health section included
