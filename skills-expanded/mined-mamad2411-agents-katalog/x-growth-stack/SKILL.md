---
name: x-growth-stack
description: >-
  Grow a following on X (Twitter) using a proven playbook: shape the profile
  into a landing page, define a consistent IP/theme, get seen by commenting
  under others, ride trends on-identity, post frequently with images, and
  leverage real relationships. Reads the user's OWN logged-in X via browser
  automation to learn native style, find trends to ride, and surface accounts
  to engage. Use when the user wants to grow on X/Twitter, plan a posting or
  engagement sprint, rewrite their X bio, draft native-style X posts, find
  trending topics to post about, or find accounts/posts to reply to. Triggers:
  "grow my X", "grow on Twitter", "get more X followers", "X growth", "plan my
  tweets", "rewrite my X bio", "what should I post on X", "who should I reply
  to on X".
---

# X Growth Stack (executable playbook)

A field-tested playbook for growing an X following fast (the author added ~1,000
followers in 2 weeks). This skill does two things: it **teaches the principles**
and it **executes the repeatable actions** by driving the user's own logged-in X
in the browser.

Read `references/playbook.md` for the full reasoning behind each pillar. This
file is the operating manual.

## Prerequisites (check first, tell the user if missing)

- **Browser automation.** Either the Claude-in-Chrome extension (preferred — it
  uses the user's real, logged-in Chrome) or the Playwright MCP. If neither is
  available, say so and offer to run the non-live parts (profile, IP, drafting,
  planning) without reading X.
- **The user is logged into X** in that browser.
- Never hardcode a handle or niche — always operate on *this* user's account and
  *their* niche. Ask for their niche/positioning if it isn't obvious.

## How to read X (the mechanism)

Everything "live" works by driving the user's own session — this is reading
their own authenticated feed, the same as scrolling it themselves. Keep it
**human-paced and personal-use**; never mass-scrape (violates X ToS and gets
accounts flagged).

1. Start a browser session (see `claude-in-chrome` skill / tools). Check current
   tabs first; open a new tab to `https://x.com` rather than hijacking one.
2. To learn style / find reply targets: scroll the home feed or a niche
   search/list, read ~10–20 posts, extract patterns. NOTE: `get_page_text`
   only returns one article block on X — to read many posts/bios, use
   `read_page` or scroll + screenshot repeatedly, don't rely on `get_page_text`.
3. To find trends: read `https://x.com/explore/tabs/trending` plus the user's
   feed, then filter to what's relevant to their IP.
4. To read their own performance: open their profile / analytics.

## The playbook — six pillars + one engine

Split into **craft** (online execution) and **network** (relationships). The
biggest wins usually come from where the two overlap (e.g. a personal-connection
moment that is also on-trend).

### Foundation — do this BEFORE chasing followers
1. **The profile is the deciding surface.** The follow decision happens on the
   profile, not the post — the bio must convey *who are you* and *why follow you*
   at a glance. (This is a goal, not a copywriting style: the rewrite should read
   as a natural, native bio modeled on strong accounts in the user's space — not
   as landing-page marketing. See Task A.)
2. **Purpose / IP.** One consistent through-line; every main post ladders up to
   it. Consistency is what makes a follow feel worth it.

### Get seen
3. **Comment under others** so their audience sees you — but two separate jobs:
   the comment must be genuinely interesting (earns the click) AND the profile
   must already convert the click. A great comment on an empty profile is wasted.

### Ride trends
4. **Match trends, don't manufacture them.** Point content at what people
   already discuss (model releases, big conferences, hot company news). Timely
   relevance = free exposure — but only in a way that fits your IP.

### The engine
5. **Post frequently.** Cadence is the real driver.
6. **Images > text — especially images of yourself.** A face reads as a real
   person and stops the scroll.

### Native style (format layer)
7. **Sound *of* X, not visiting it.** Lowercase, minimal punctuation, short
   lines, native signs. Getting format wrong (title case, marketing polish,
   hashtag soup) instantly reads as outsider. See `references/native-style.md`.

### Network layer (relationships — earned, not free)
- **Reposts / tags from people in the field** extend reach and boost the
  algorithm. This comes from real connection.
- **IRL → online.** Meet people (esp. in a hub like SF), add them on X.

## Tasks this skill performs

Pick the task that matches the request; run the numbered steps.

### A. Rewrite the profile description (learn from real examples first)
The output is a natural, native bio description — NOT landing-page marketing
copy. The way to write a good one is to study how strong accounts in the user's
own space write theirs, then model the rewrite on those patterns.
1. Open the user's profile; read their current bio, pinned post, header, handle.
2. **Read other people's profiles for reference.** Pull the bios of 5–10
   relevant accounts — ones in the user's niche, ones they admire, or accounts
   at the size they're aiming for (ask the user to name some, or find them by
   searching the niche). Read each bio.
3. **Extract what works:** how they open, length, how they convey who-they-are
   and why-follow without sounding like an ad, use of specifics/credentials,
   line breaks, signs, tone. Note the recurring patterns.
4. Rewrite the user's bio in that idiom — natural and native, keeping their real
   identity/IP. Offer 2–3 variants. Optionally suggest a pinned post that states
   the IP. Keep it in native style, not marketing voice.

### B. Define / sharpen the IP
1. Ask (or infer from recent posts) the one through-line.
2. Propose 3–5 content lanes that all ladder to it. Flag off-brand posts.

### C. Find trends to ride
1. Read trending + the user's feed (see "How to read X").
2. Return only trends that fit the IP, each with a concrete on-brand angle.

### D. Find accounts / posts to comment under
1. Scroll the niche (search terms, lists, or accounts the user names).
2. Surface high-value reply targets: post link, why it's a good target, and a
   drafted interesting reply in native style.

### E. Draft posts
1. Take an idea (or generate from the IP + a live trend).
2. Draft in native style, with an image suggestion — prefer a photo of the user
   where natural. Offer 2–3 variants.

### F. Plan a 2-week sprint
1. Combine cadence + comment targets + trend-watching into a daily checklist.
2. Concrete: N posts/day, M replies/day, which accounts, what to watch for.

## Guardrails
- Personal-use, human-paced browsing only. No automation of mass following,
  mass replying, or scraping at scale.
- Draft, don't auto-post, unless the user explicitly asks to post.
- Keep every suggestion on-identity; refuse trend-chasing that breaks the IP.
