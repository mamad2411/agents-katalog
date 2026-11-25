---
name: dev-audit
description: >-
  Post-mortem on what the user has already published on dev.to - which posts
  actually worked, why, and what to stop doing. Uses the user's own analytics
  plus ~/.claude/devto/log.md history.
---

# dev-audit

The only honest source of what works for a dev.to account is that account.
Every rule in every dev.to guide is a prior. The user's own last 30 posts are
the evidence.

## Input

Ask for whichever the user has:

- The dev.to analytics export (Dashboard -> article stats). Or API via
  `GET https://dev.to/api/analytics/...` with `api-key` + `accept`
  headers (`totals`, `historical`, `past_day`, `referrers`, `dashboard`).
- Or per-post screenshots with views, reactions, comments, reading time.
- Or just the posts and their reaction counts, which is enough for a first
  pass.
- Also read `~/.claude/devto/log.md` if it exists, since it records which
  title formula and tags each post used.

## What to actually measure

Raw impressions/views are the least useful number, because they are mostly a
function of how many followers the user already has. Compute these instead,
and show the working:

| metric | how | what it tells you |
|---|---|---|
| **Engagement rate** | (reactions + comments + bookmarks) / views | whether the post earned its reach |
| **Comment ratio** | comments / reactions | whether it started something or just got a nod |
| **Reach multiple** | views / follower count | whether it travelled past the existing audience |
| **Save/send rate** | bookmarks / views | strongest single predictor of future reach |

Rank by engagement rate and reach multiple, not views. A post with 900 views
and 40 comments beats the one with 12,000 views and 6.

## Analytics caveats (warn honestly)

- **Average read time** is precomputed server-side and internally inconsistent
  (totals vs daily rows can disagree 1.7–6.1x). Treat as directional only.
- **Historical data degrades** for old posts (~15% coverage for 2017, 95% for
  2019, 100% for 2026). Gate computations on coverage — track posts with
  ≥80% of lifetime views covered.
- **Follower count is not readership.** Reciprocal-follow farming inflates it;
  ~37% of usernames look auto-generated. Don't weight reach multiple too
  heavily if follower growth looks suspicious.
- **Median post half-life is ~4 days.** Most views land in the first week.

## Then find the pattern

With the top 5 and bottom 5 side by side, look for what actually separates
them, and be willing to conclude something the user will not like:

- Title formula. Which numbers from `title-formulas.json` are in the top 5?
- Format. Tutorial, listicle, discussion, opinion, announcement, series.
- Length. 1–3 min vs 4–7 min vs 8–13 min reads.
- Tags. Which tag stacks appear in the top 5? Which are absent?
- Cover image. Do top posts have covers? Do bottom posts lack them?
- Canonical URL. Do syndicated posts underperform native ones?
- Day and time — check this **last**, and only if the other four show
  nothing. It is almost never the cause.
- First-hour comments. Posts the user replied to inside an hour vs not.

State the finding as a claim with the evidence attached, and say how
confident it is. With 30 posts you can see a pattern; with 6 you cannot, and
you should say that instead of inventing one.

## Output

```
AUDIT  ·  31 posts  ·  Jun 12 - Sep 5

TOP 5 BY ENGAGEMENT RATE
  8.1%  #12 Comparison   "I cut proposal time from 5h to 20m"      1,940 views
  6.4%  #4  Story        "I Passed The Google Interviews"          2,210 views
  ...

BOTTOM 5
  0.4%  #1 Listicle      "7 tools every dev needs"                11,400 views
  ...

WHAT THE DATA SAYS
1. Posts where you were the one who looked bad: mean 6.2% vs 1.1% for
   everything else. n=6. Strongest signal, not close.
2. Tool listicles get views and nothing else. High reach, no comments.
   Three of your bottom five.
3. Cover image present: mean 4.1% vs 1.8% without. n=14.
4. Day of week shows nothing. Your Tuesday mean and your Friday mean are
   inside the noise. Stop optimising it.

STOP: listicles about tools.
DO MORE: the ones with a cost you paid, and a number.
```

Then hand the conclusions to a planning step so next week's posts are built on
the user's own evidence rather than on defaults.

## Self-improvement: learn()

After every audit, run `python3 ~/.config/opencode/skills/dev-learn.py audit --apply`.
This reads `~/.claude/devto/log.md`, computes per-post engagement metrics, and:

- **dev-post**: promotes title formulas and tags in the top-5 engagement rate
  (weight += 0.1), demotes bottom-5 (weight -= 0.1), archives formulas/tags
  whose weight drops to 0. Requires ≥10 audited posts before any change.
- **dev-profile**: flags rubric items for manual re-weighting based on which
  fixes users actually apply.
- **dev-human**: no automatic slop changes (voice-specific); user reviews
  recurring slop words from `humanize.py --report` output.

Never deletes formulas/tags/items — demotes weight to 0 and moves to `archive`.
Re-run `dev-post` after learning to see updated suggestions.

## Skipped (ponytail)

- No auto-fetch of analytics API (requires DEVTO_API_KEY + manual setup).
- No unfollow/follow automation (Forem API exposes follow-add only).
- No schedule optimization beyond "Tue/Wed/Thu ~9–10am ET" prior.
