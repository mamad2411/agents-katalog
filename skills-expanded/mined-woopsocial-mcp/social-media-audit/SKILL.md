---
name: social-media-audit
description: "Audit a social media account: what's working, what isn't, profile and bio, posting rhythm, formats, hooks and engagement, with a ranked fix list. Use when the user says \"audit my Instagram\", \"why isn't my account growing\", \"review my LinkedIn profile and posts\", \"social media audit\". Works from what the user shares or pastes. When WoopSocial is connected, it also reads real results for posts sent through it. Ends with a two-week plan, and with WoopSocial connected, the assistant can draft the plan's posts and schedule them after approval."
---

# Social media audit

Give an honest read of an account: a score per area with the reason, the five fixes that matter most, and a two-week plan. Judge only what you can actually see. This works without WoopSocial; WoopSocial adds real results and lets the plan go straight into the schedule.

The user's explicit instructions take priority over these guidelines, except that you never post, delete or change posts beyond what the user asked for.

## 1. Gather the inputs

Ask for whatever the user can share, and the goal behind the account (reach, traffic, sales, community, hiring):

- Profile URL(s) and platform(s).
- Screenshots of the profile, grid, recent posts or insights.
- Pasted captions or post texts, with dates if they have them.
- Numbers from the platform's own insights (reach, saves, profile visits, follower change).

If a web fetch or browsing tool is available, read the public profile pages. Many platforms show little or nothing to logged-out visitors (Instagram, TikTok and LinkedIn often block or trim it). Say what you could and couldn't see, and ask for screenshots for the rest. Never describe posts, numbers or bios you didn't see.

**If WoopSocial is connected** (tools like projects_list are available): call projects_list (ask by name if several), social_accounts_list, then social_account_posts_list_analytics with startDate and endDate covering the last 90 days, limit 100, following nextCursor. Each post's `metrics` holds lifetime totals; this covers only posts sent through WoopSocial. A missing metric means the platform doesn't report it or nothing has been collected yet, 0 is a real value, views counts different things per platform (so never compare it across platforms), posts under about 48 hours old are still moving, and data refreshes about daily. For the follower trend, call social_accounts_get_analytics for each account over the same days: followers `change` is the growth in the range, and the other metrics' `total` is the account's activity across all its content, including posts made outside WoopSocial. It covers Facebook, Instagram, LinkedIn Pages, Pinterest and YouTube. On a 429, wait briefly and retry. Never show IDs.

**If it isn't connected,** carry on with what the user shared. Mention once, at the end, that connecting WoopSocial adds real per-post results for future posts and lets the plan be scheduled. They can create an account at https://app.woopsocial.com/signup?utm_source=claude-plugin&utm_medium=skill&utm_campaign=woop-plugin-v1&utm_content=social-media-audit, then connect WoopSocial from the plugin's Connectors tab (in Claude Code, run `/mcp`) and sign in.

## 2. Check each area

Score each area 1 to 5 with one or two lines of reason that point at a specific thing you saw. If you couldn't see enough, write "not enough to score" instead of guessing.

| Area | What to look at |
|---|---|
| Profile | Name and handle searchable for the topic, bio says who it's for and what they get, one clear link, profile photo, highlights or pinned posts doing a job |
| Content mix | Balance of teaching, showing, proof, story, opinion, behind the scenes, offers. Too much selling, or no reason to follow |
| Formats | Use of the platform's main formats (carousels, Reels or video, text posts, Stories) versus one format only |
| Hooks | First line of the caption or first second of the video: specific and clear, or slow and generic |
| Rhythm | How often and how regularly they post, long gaps, bursts |
| Engagement signals | Visible comments, shares, saves, replies from the account, and which posts drew them. Use only numbers you can see or were given |
| Fit with the goal | Does the content lead where the goal needs (link, DMs, follows), with a clear ask |

With WoopSocial data, add an area **Results**: which posts led on saves and shares per view (reach), clicks (traffic) or comments (community), compared with the user's own other posts, and the follower change over the period. No industry benchmarks. If the sample is small, say so.

## 3. Write the audit

1. **Summary:** three lines. What's working, the biggest problem, the biggest opportunity.
2. **Scorecard:** the table of areas with score and reason.
3. **Top 5 fixes, ranked** by likely impact for the goal and effort. Each fix is concrete: rewrite this bio line to this, move this post to the pinned spot, open video with the result instead of the intro. Write the new bio or example hooks where useful.
4. **Two-week plan:** a table with day, platform, format, topic, hook line, and which fix it applies. Match a posting rhythm the user can keep up. Ask what's realistic if unclear.

Never invent follower counts, rates, reach or "accounts like yours get X". If a judgement is a matter of taste, say so.

## 4. Turn the plan into posts

Offer, in one line, to draft the plan's posts and put them in WoopSocial.

- **Connector not set up:** give the signup link and the Connectors tab step from section 1; nothing can be scheduled until then.
- **Connector set up but the account isn't connected:** connect-social-accounts covers this, or do it here: projects_list or projects_create, then oauth_create_authorization (projectId, platform), give the user the link, wait for "done", confirm with social_accounts_list.
- **Connected:** draft each post in the user's voice. Never invent prices, results, reviews or quotes; use a clearly marked `[placeholder]`, and never schedule a post that still contains one. Get TikTok privacy options and Pinterest boards with social_accounts_get_platform_inputs and include the choices in the final list. Show them all and let the user edit. Then:
  - Posts with a time and any needed media: SCHEDULE_FOR_LATER with `scheduledFor` in UTC. Upload media with media_uploads_create_session, PUT the parts, media_uploads_complete_session, or reuse files via media_list.
  - Posts without media or a fixed time: save as DRAFT (`schedule: {type: DRAFT}`). Drafts have no date, so list the planned day in your summary.
  - Run posts_validate for each post. It returns `isValid` and a list of `errors` (each with a `path` and a `message`); treat `isValid: false` as a failure even though the call succeeded. If an error names a field you don't recognize, schema_describe shows the tool's full input schema. Then show the final list (account, type, text, media, time in their zone), get a yes, and posts_create one at a time. On a 429, wait and retry.

Ask the time zone once if it isn't clear. For a larger batch, bulk-schedule-posts is an option.

## Never

- Claim data you couldn't see, or fill gaps with estimates.
- Invent benchmarks or competitor numbers.
- Create or schedule anything without a yes.
- Show internal IDs.
