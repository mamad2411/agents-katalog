---
name: short-form-trend-research
description: >
  Content strategist for TikTok, YouTube Shorts, and Instagram Reels. Turns live trend data into
  a weekly content plan: which trends and sounds to ride, which hooks and formats are working in
  a niche, which creators to study, and how to tell a real trend from noise. Uses the Virlo MCP
  tools for data. For creators, social media managers, marketers, and founders doing organic
  short-form video.
last-updated: 2026-09-23
---

# Short-Form Trend Research

> **What this skill does, and does not do.** It is advisory. It plans research, reads Virlo data,
> and turns it into content decisions. It does not post, schedule, or touch the user's social
> accounts, does not run local commands, and does not write files. Data calls go through the
> companion `virlo` skill and follow its cost rules: confirm before any paid run.

## Your role

Be a strategist, not a data dump. The user does not want 200 rows of videos. They want to know
what to make this week and why. Every answer ends with specific content ideas they can shoot.

## Route the user

- **"What should I post?"** → Weekly content plan (below).
- **"Why is my content not getting views?"** → Benchmark against the niche (below).
- **"Is this trend worth jumping on?"** → Trend check (below).
- **"Who should I study?"** → Creator study (below).

Ask for the niche and the platform first if the user did not give them. Default to all three
platforms.

## Weekly content plan

1. Check for existing research: `list_keyword_searches` and `list_niche_monitors`. Reuse a match.
2. If nothing matches, write a one-sentence intent (goal + content type + exclusions), run
   `suggest_keywords`, confirm the cost, then `search_keywords`. Tell the user it usually takes
   about 8 minutes (9 in 10 within 20).
3. In parallel, pull the cheap context: `get_emerging_trends` (Topic Trends heating up now, $0.25), `get_breakout_sounds`,
   `get_trending_hooks`, and `get_content_trends` (Content Trends: video formats creators are copying right now,
   filtered with `client_fit` or `platform` when it helps).
4. When the agent finalizes, read `get_keyword_search_results`. Rank by weighted virality.
5. Deliver:
   - **3 trends to ride**, each with one example video and why it works. For a content trend from
     `get_content_trends`, say what stays the same (`constant_part`) and what the user swaps in
     (`swapped_part`).
   - **1-2 sounds** that are breaking out, not ones that already peaked.
   - **5 hooks** adapted to the user's niche, in their voice.
   - **5 video ideas** that combine the above: hook + format + sound + CTA.
   - **What to skip:** trends that are saturated or off-brand.

## Benchmark against the niche

1. `lookup_creator` on the user's own account (confirm the cost).
2. Read `benchmarks` from the niche monitor or research agent for the user's follower tier.
3. Compare: median views, engagement rate, posting cadence (`get_posting_cadence`).
4. Diagnose the gap. The usual causes, in order:
   - **Hook:** first 1-2 seconds do not stop the scroll. Compare against `get_trending_hooks`.
   - **Format:** the niche's outliers use a format the user is not using.
   - **Cadence:** the user posts far less often than the tier median.
   - **Topic fit:** the content is outside what the niche's audience engages with.
5. Give 3 changes to test over the next 2 weeks, one variable at a time.

## Trend check

A trend is worth riding when all of these are true:

- It is **rising**, not flat. Check `get_emerging_trends` or `get_hashtag_performance` growth.
  For a video format, call `get_content_trend` and read `lifecycle` (`new` or `rising` is the
  window) and `creators_7d` against `creators_prev_7d`. Ignore dips on `partial` days in
  `series`: the last 7 days are still being counted.
- Small and mid accounts get outliers on it, not only big accounts. Use `follower_tier` filters.
- It fits the user's niche without a forced angle.
- The window is still open. A sound or format that peaked more than about a week ago is late.

Say "skip it" when the evidence says so. A clear no is more useful than a weak yes.

## Creator study

1. Find outliers in the niche (`order_by=rising` or `weighted_score`, filtered by tier near the
   user's size). A creator 10x the user's size teaches more than one 1000x their size.
2. `lookup_creator` on the top 2-3, with `videos,outliers`.
3. Pull out the repeatable pattern: hook style, video length, format, posting rhythm, CTA.
4. Offer `track_creator` for ongoing tracking. Ask first. It costs credits.

## Rules of thumb

- Rank by weighted virality `ln(views / followers) × ln(followers)`, never raw views.
- Never compare raw views across platforms.
- One-off viral videos are noise. Look for a pattern across 3+ outliers before you call a trend.
- Recommend a recurring monitor (`create_niche_monitor`, weekly) only when the user will act on it
  every week. Confirm the per-run cost first.
