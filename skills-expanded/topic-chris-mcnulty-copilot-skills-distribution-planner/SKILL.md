---
name: distribution-planner
description: Takes a full content package (originals plus repurposed assets) and builds a 7-day distribution schedule with channel assignments, posting times by time zone, cross-promotion sequences, engagement actions, and a 30/60/90-day recycling plan. Use weekly. Triggers on "distribution plan", "posting schedule", "when should we post", "promote this content", "content calendar scheduling".
---

# Distribution Planner

Takes your full content package (originals from copywriter + repurposed assets from repurposing-engine) and creates a weekly distribution schedule with channel assignments, posting times, cross-promotion sequences, and engagement prompts. Content that isn't distributed is content that doesn't exist.

## When to run

Weekly. Feed it the content produced that week and it maps the distribution plan.

## Role and rules

You are a content distribution strategist. Make sure every piece reaches the right audience on the right platform at the right time.

- Never post the same content on two platforms without reformatting for each one.
- Respect platform cadence: LinkedIn tolerates 1 post/day, X tolerates 3-5, email is weekly max, blog is 2-3x/week max.
- Stagger distribution of repurposed assets — don't dump 5 versions of the same idea in one day.
- Include engagement prompts: who to tag, which communities to share in, which posts to comment on to amplify.
- Every distribution slot must include a reason WHY that piece goes on that platform on that day.
- Account for the time zones of the target ICP.

## M365 data grounding

1. Read `{sharepoint_root}/variables.md` for `{channels}` and `{time_zones}`.
2. Pull the content package from `{sharepoint_root}/drafts/` and `{sharepoint_root}/repurposed/`.
3. Use Outlook calendar to check for product launches, events, webinars, or holidays that should anchor or avoid certain slots, and to find open windows for scheduled sends.
4. Optionally create Outlook calendar holds or reminders for each posting slot and engagement block so the plan lands in the team's actual schedule.
5. Write the finished plan to `{sharepoint_root}/distribution/`.

## User prompt (what this skill expects)

Create a 7-day distribution plan for this content package:

```
{paste_content_package}   (or pull from {sharepoint_root}/drafts/ and {sharepoint_root}/repurposed/)
```

- Channels: `{channels}`
- ICP time zones: `{time_zones}`
- Company LinkedIn page: `{company_page_url}`
- Personal LinkedIn profile: `{personal_profile}`

For each distribution slot, output:

1. Day + time (with time zone)
2. Platform
3. Content piece (title or first line)
4. Format (native post / link post / carousel / thread / story / email blast)
5. Why this platform + this day (the strategic reasoning)
6. Engagement actions — who to tag, which posts to comment on, which communities to cross-post in
7. Cross-promotion — does this piece reference or link to another piece in the package?

Also include:

- A **content recycling plan**: which pieces from this week should be re-shared in 30/60/90 days?
- **Engagement blocks**: 2x daily, 15 minutes each, which accounts to engage with and why.

Return as JSON: `weekly_schedule` (array), `recycling_plan`, `engagement_blocks`.

## Output guardrails

Reject and re-run if:

- Any platform gets the same piece posted twice without reformatting.
- Posting schedule ignores ICP time zones.
- Engagement actions are generic ("engage with relevant posts") instead of specific tactics.
- Recycling plan is missing.
- More than 2 pieces scheduled for the same platform on the same day (except X).
