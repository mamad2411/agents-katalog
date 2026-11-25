---
name: social-media-report
description: "Social media performance report for posts published through WoopSocial: views, impressions, likes, comments, shares, saves and clicks (where each platform reports them) per post, per platform and by publish week, plus follower growth and account totals, and what to post more of next. Use when the user asks \"how did my posts do\", \"weekly social report\", \"which post performed best\", \"what's working on my accounts\". Per-post results only cover posts sent through WoopSocial, not older native posts; numbers refresh about daily."
---

# Social media report

Turn the results of posts sent through WoopSocial, and of the accounts they went to, into a short, honest report and three things to do next. Compare the user with their own past posts, never with made-up industry numbers.

The user's explicit instructions take priority over these guidelines, except that you never post, delete or change posts beyond what the user asked for.

## If WoopSocial isn't connected

If no WoopSocial tools (projects_list, social_account_posts_list and so on) are available, the connector isn't set up. Say so in one line. The user can create an account at https://app.woopsocial.com/signup?utm_source=claude-plugin&utm_medium=skill&utm_campaign=woop-plugin-v1&utm_content=social-media-report, connect WoopSocial from the plugin's Connectors tab (in Claude Code, run `/mcp`), and retry. If they paste numbers from their native insights instead, you can read those, but say they came from the user. Never invent results.

## 1. Scope the report

Ask only for what's missing:

| What | Default |
|---|---|
| Period | Last 7 days or last 28 days. Ask which. |
| Brand | The only project, or ask by name if there are several |
| Platforms or accounts | All connected ones |
| Goal | Reach, traffic, or community. Ask once; it decides the ranking. |

Ask the time zone once if it isn't clear, and show dates in it.

## 2. Collect the numbers

1. Call projects_list, then social_accounts_list for the project, so you can show accounts by platform and username. Never show IDs.
2. Call social_account_posts_list_analytics with startDate and endDate set to the UTC days that cover the period, projectId, and platform or socialAccountId if the user narrowed it. Use limit 100 and keep calling with nextCursor until it's gone. Make the same calls for the period before, for comparison.
3. The range is in UTC days, so drop the posts whose deliveryCompletedAt (the publish time) falls outside the period in the user's time zone.
4. For each account, call social_accounts_get_analytics with the same startDate and endDate.
5. On a 429, wait briefly and retry, one call at a time.

**If no posts come back,** explain why: per-post results only cover posts published through WoopSocial, and none went out in this period (or ever, for this project). Posts made directly in the Instagram or TikTok app don't show here. Still report the account numbers if there are any. Offer to schedule the first posts, for example with instagram-posts, linkedin-posts, tiktok-posts or cross-post-everywhere, so the next report has data.

## 3. Read the numbers

Each post's `metrics` holds lifetime totals since it was published: views, impressions, uniqueImpressions, likes, reactions, comments, shares, saves, clicks, and engagementRate for LinkedIn Pages only. `metricsCollectedAt` says how fresh they are.

- A metric that's missing means the platform doesn't report it for that post, or nothing has been collected yet. Show "not available", never 0.
- A 0 is a real recorded value. Show it as 0.
- views counts different things per platform: times the post was shown on Instagram, Facebook and Threads, video plays on TikTok and YouTube, and video views on Pinterest. LinkedIn Pages reports impressions instead. Never compare views across platforms.
- engagementRate is a ratio: 0.03 means 3 percent. It exists only for LinkedIn Pages, so don't compute a fake one for other platforms.
- Mark posts published less than about 48 hours ago as "still moving". Their numbers will grow.
- Reading doesn't refresh anything. Data is collected about daily, so the newest numbers may be a day old.

Account numbers from social_accounts_get_analytics cover everything on the account, including posts made outside WoopSocial. They exist for Facebook, Instagram, LinkedIn Pages, Pinterest and YouTube; other platforms return empty `metrics`.

- followers: `latest` is the most recent count and `change` is the latest minus the earliest count in the range.
- Every other metric counts activity per UTC day: `total` adds up the collected days and `points` holds one value per day. A day without a point has nothing collected, and the latest day or two are often missing.
- An empty `points` means nothing has been collected for that range yet. Show "not collected yet", never 0.

## 4. Build the report

Keep it short and scannable.

1. **Headline:** posts published in the period, per platform, and when the numbers were last collected.
2. **Accounts:** follower change and the account's total views or impressions and engagements in the period, per account. These include posts made outside WoopSocial; say so once.
3. **Per platform:** totals for each reported metric. Don't add metrics across platforms that measure different things (views on TikTok are not impressions on LinkedIn); show them per platform.
4. **Per week:** group posts by the week they were published (deliveryCompletedAt). Totals are lifetime numbers for those posts, not engagement that happened that week. Say so once.
5. **Top and bottom posts:** rank by what matters for the goal:
   - Reach: saves and shares.
   - Traffic: clicks.
   - Community: comments.
   Where views or impressions exist, rank by rate per view (saves per 1,000 views, for example) so a post with more views doesn't win just by size. Show the raw counts next to the rate. Give each post a text preview (first line), the platform, the publish date and externalPostUrl.
6. **Against themselves:** if there's enough history (the previous period of the same length, from the same list), compare with that. If not, say there isn't enough history yet. No industry benchmarks.

Use a table per platform when there are more than a few posts. Never fill a gap with an estimate.

## 5. What to do next

End with exactly three concrete actions, each tied to evidence from this report:

- "Post more of X": name the post or pattern (format, topic, hook style, time of day) that led on the goal metric.
- "Post less of Y": name what trailed, with the numbers.
- One test for next period, for example the winning topic in a different format.

If the sample is small (a handful of posts), say the signal is weak and frame the actions as tests.

Then offer the next step in one line: draft and schedule the next posts in that direction. Platform skills (instagram-posts, linkedin-posts, tiktok-posts), cross-post-everywhere, or weekly-social-autopilot for a weekly routine are optional routes. Nothing gets created without a yes.

## Caveats to state in the report

Put these in a short footer, only the ones that apply:

- Per-post results only include posts sent through WoopSocial; account totals include everything on the account.
- Numbers are collected about daily; latest collection date shown.
- Posts under about 48 hours old are still moving.
- "Not available" means the platform doesn't provide that metric, or it hasn't been collected yet.

## Never

- Invent numbers, benchmarks or "average engagement rates".
- Show 0 for a metric that isn't available.
- Show internal IDs.
- Claim posts made outside WoopSocial are missing because of an error.
