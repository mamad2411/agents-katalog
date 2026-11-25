---
name: reddit-seo
description: >
  Check whether a Reddit post or comment is publicly live and marked robot-indexable — or silently
  held in the AutoMod queue. Use this whenever someone asks
  about Reddit SEO, Reddit GEO, generative engine optimisation on Reddit, whether their Reddit post
  is indexed, why a Reddit post gets no traffic, whether a post was shadowbanned, removed, filtered,
  or "posted fine but nobody sees it". Also use it before posting, to check a subreddit's posting
  requirements, flair rules, and karma or account-age gates, and after posting, to confirm the
  submission survived moderation. Reach for it when a Reddit write returned HTTP 200 but the post
  is missing from listings, when auditing which of your Reddit posts are indexable, or when
  planning where Reddit content can realistically rank. Not a keyword-research or content-writing
  tool — this measures visibility that already exists.
---

# Reddit SEO: is your post live and robot-indexable?

Reddit ranks well in Google and is heavily cited by AI answer engines, which is why people post
there for visibility. The problem is that **a Reddit post can look completely successful while it
is absent from public listings and ineligible for robot indexing.** Large subreddits route new
submissions through AutoMod, where they remain reachable by direct link but are marked
non-indexable. The write returns HTTP 200. The post still loads when you open it directly.

This skill measures that difference. It does not write content and does not do keyword research —
it tells you whether content you already have can be seen.

## Verify the installed runtime without Reddit

Run `node scripts/verify-synthetic.mjs` with no arguments. It passes four fabricated moderation
shapes through the production visibility classifier and checks `live`, `automod_filtered`,
`not_indexable`, and `removed` without Chrome or Reddit. A pass proves classification behavior
only; it says nothing about the current state of a real permalink.
Overall `passed` is the AND of all five shared checks; inspect `functional.reddit_seo` for this
skill's evidence.

An independent tester can submit the exact named verifier result through the
[structured installed-run report](https://github.com/L4A-ai/reddit-skills/issues/new?template=reddit-skill-installed-run.yml).
Select the `reddit-seo` zero-input synthetic option only after running the installed copy. This
proves installation and classification contracts, not the live state of a permalink.

Live checks require Node.js 18+, `agent-browser`, and the user's own logged-in Chrome profile; see
`references/browser-session.md`. The synthetic verifier needs only Node.js 18+.

## The signal that matters

Two fields expose that state:

| field | meaning |
|---|---|
| `removed_by_category` | `null` = not removed. `automod_filtered` = sitting in the mod queue. Anything else = removed. |
| `is_robot_indexable` | `false` = Reddit marks the post ineligible for robot indexing; do not treat it as a searchable or answer-engine-visible page. |

Measured on a real post minutes apart, before and after a moderator approved it:

```
removed_by_category: "automod_filtered"   →   null
is_robot_indexable:  false                →   true
```

Nothing about the post changed. A human approved it. Before that moment Reddit marked it
non-indexable; after approval the field changed to `true`. If you are posting to Reddit for SEO or
GEO, this is the state worth tracking.

## Check a post

```bash
node scripts/rdtx.mjs read <permalink>
```

Returns a `visibility` block:

```json
"visibility": {
  "state": "automod_filtered",
  "public": false,
  "indexable": false,
  "detail": "held in the mod queue by AutoMod — reachable by direct link, but not
             indexable and not in public listings until a mod approves it"
}
```

States: `live`, `automod_filtered`, `not_indexable`, `removed`.

**Only `live` proves the page is both public and marked robot-indexable.** Treat everything else as
unpublished for SEO/GEO measurement.

## Check before you post

Most visibility is lost at submission time, not after. Before writing, check what the subreddit
actually requires:

```bash
node scripts/rdtx.mjs requirements <subreddit>
```

```json
{
  "subreddit": "ClaudeAI",
  "subscribers": 1048530,
  "flair_required": true,
  "flairs": ["Skills", "Built with Claude", "Coding", "..."],
  "allowed_post_types": "any",
  "rules": [{ "short_name": "Showcase your project…", "kind": "submission" }]
}
```

A post that violates a rule gets removed, and a removed post is worth less than no post — it costs
account standing too. `flair_required` in particular is silent: Reddit rejects an unflaired
submission rather than posting it.

## What actually earns visibility

The mechanics above are necessary but not sufficient. Three things decide whether Reddit content
ranks, and only the first is technical:

**Indexability.** Covered above. A filtered post is not eligible for public robot indexing; check it
rather than assuming.

**Subreddit choice.** Subreddits differ enormously in how well they rank and how aggressively they
filter. A large subreddit with strict AutoMod may deliver less indexable content than a smaller
permissive one. `requirements` tells you the gates; the filtered-vs-live rate over your own posts
tells you the reality.

**Being worth citing.** AI answer engines cite Reddit threads that genuinely answer a question.
Content written to rank rather than to answer tends to get filtered, downvoted, or removed — all
three of which destroy the visibility it was chasing. The measurable version of this is simple: a
post that stays `live` and accumulates real comments is working; one that is repeatedly filtered
is not, and posting more of the same accelerates the problem.

## What this skill will not do

It will not post the same content across many subreddits to manufacture ranking signal. That
pattern is what AutoMod and Reddit's spam detection are built to catch — you will watch posts go
from `live` to `automod_filtered` to removed, and eventually take the account with them. If you
need reach, the lever is fewer, better-targeted posts that survive moderation, and this skill's
job is to tell you which ones did.

Reposting to escape a filter is the specific mistake to avoid: it converts one filtered post into
a spam pattern across the account.

## Setup

Needs a logged-in Chrome the human launched, attached over CDP:

```bash
node scripts/rdtx.mjs launch    # Chrome with a debug port, no automation flags
node scripts/rdtx.mjs login     # you log in by hand
node scripts/rdtx.mjs doctor    # confirms the session
```

`rdtx` never handles your password. See `references/browser-session.md` for why this attach model
is used and why Puppeteer/Playwright get flagged where this does not.

## Related

- `reddit-post` — write posts and comments, with the same visibility verification built into the write
- `reddit-archive` — capture a post and its media for analysis
