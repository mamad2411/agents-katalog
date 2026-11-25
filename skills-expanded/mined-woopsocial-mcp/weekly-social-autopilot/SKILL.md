---
name: weekly-social-autopilot
description: "Weekly social media autopilot through WoopSocial: each week read how last week's posts did, draft next week's posts in the user's voice, get approval, then schedule them. Use when the user says \"run my social media on autopilot\", \"be my social media manager\", \"do my posts every week\", \"set up a weekly content routine\". Nothing is scheduled without approval; as a recurring task, unattended runs only save drafts for review."
---

# Weekly social autopilot

Run the same loop every week: look at last week, plan next week, draft in the user's voice, get approval, schedule. The assistant does the planning and writing; the user supplies media and approves. Nothing is scheduled without a person's yes.

The user's explicit instructions take priority over these guidelines, except that you never post, delete or change posts beyond what the user asked for.

## If WoopSocial isn't connected

If no WoopSocial tools are available, say the WoopSocial connector isn't set up. The user can create an account at https://app.woopsocial.com/signup?utm_source=claude-plugin&utm_medium=skill&utm_campaign=woop-plugin-v1&utm_content=weekly-social-autopilot, connect WoopSocial from the plugin's Connectors tab (in Claude Code, run `/mcp`), sign in and retry. You can still do onboarding and draft a first week now, so offer that. Never pretend to schedule.

## First run: onboarding

Resolve accounts first: projects_list (ask by name if several), then social_accounts_list. Use CONNECTED accounts only. Offer to connect a missing or DISCONNECTED one with oauth_create_authorization. Never show IDs.

Then ask, in one short message, only what you don't know:

1. **Accounts:** which of the connected accounts to post to (show them by platform and username).
2. **Goal:** reach, traffic (clicks to a site or shop), or community (comments, DMs).
3. **Posts per week** per platform, and preferred days and times. Be realistic about what they can supply media for.
4. **Mix:** the kinds of posts they want (for example tips, behind the scenes, product, customer stories, opinions) and anything off limits.
5. **Voice samples:** 3 to 5 past posts or texts they like.
6. Time zone.

Then write a short **voice and brand notes** block (10 to 20 lines): who they are, audience, tone, words and emoji they use or avoid, recurring hashtags, links, claims never to make, the weekly plan. Show it and get it approved. If you can write files, save it as `social-autopilot-notes.md` and read it at the start of every run. If you can't, ask the user to keep it and paste it next time.

Get TikTok privacy options and Pinterest boards with social_accounts_get_platform_inputs, ask once, save the choices in the notes, and show them in the approval list.

## The weekly loop

### 1. Review last week (brief)

Call social_account_posts_list_analytics with projectId and startDate and endDate covering the last 7 days in UTC, limit 100, following nextCursor. Each post's `metrics` holds its lifetime totals. Name the top one or two posts for the goal (saves and shares for reach, clicks for traffic, comments for community; per view where views exist) and one that trailed. Three to five lines, no more.

Honesty: only posts sent through WoopSocial count. Missing metrics mean the platform doesn't report them or nothing has been collected yet, 0 is real, posts under about 48 hours old are still moving, and data refreshes about daily. If there's no data yet, say so and plan from the notes alone. For a full breakdown, social-media-report is an option.

Also list NOT_STARTED posts with social_account_posts_list: SCHEDULE_FOR_LATER ones fill slots already, so don't double-book them. DRAFT ones may come from an unattended run; start the plan from them instead of drafting again.

### 2. Plan next week

Make a table: day, time (user's zone), platform, post type, topic, which part of the mix, and the media it needs. Follow the posts-per-week and mix from the notes. Lean towards what worked last week, and keep one slot for a test.

### 3. Draft every post

Write each post in the voice from the notes, adapted per platform (a strong first line, the platform's length and style, one clear ask that fits the goal). Never invent prices, results, reviews, quotes or claims; use a clearly marked `[placeholder]` and list them. Never schedule a post that still contains a placeholder. Ask for the fact, or save the post as a draft and flag it.

### 4. Approve

Show the week post by post: day and time, account, post type, full text, media needed or attached. The user can approve, edit, swap or drop each post. Apply edits and show the changed posts again. Say which posts will be saved as drafts because their media is missing. Ask for one clear yes on the final list.

### 5. Schedule

For each approved post, one at a time:

1. **Media:** for local files, upload them (media_uploads_create_session with projectId and fileSizeInBytes, PUT each part to its uploadUrl, every part but the last exactly partSizeInBytes, then media_uploads_complete_session). Files already in WoopSocial: find them with media_list. If uploads are blocked, ask the user to allow `*.r2.cloudflarestorage.com` (claude.ai or Claude Desktop: Settings > Capabilities > Create and edit files, turn on "Use the internet while making files" and add it under Allowed websites > Manage; Claude Code: the sandbox's allowed network domains). If you can't make HTTP requests at all, say so: the user can upload in the WoopSocial app (then find it with media_list), and posts that still lack media are saved as drafts (step 3).
2. **Build the payload:** one content item, `schedule: {type: SCHEDULE_FOR_LATER, scheduledFor: <UTC>}`, the account targets with their platform fields, and `retryPolicy: {maxRetries: 2, delaySeconds: 300}` unless they don't want retries.
3. **No media on a platform that needs it** (Instagram, TikTok, YouTube, Pinterest): don't schedule it. Save it as a DRAFT (`schedule: {type: DRAFT}`, no date) and flag it in the summary so the user can add media in the WoopSocial app or send the file next time. If posts_validate rejects even the draft, keep the post in the summary as text to add later, and don't create it.
4. posts_validate, fix and re-validate, then posts_create. It returns `isValid` and a list of `errors` (each with a `path` and a `message`); treat `isValid: false` as a failure even though the call succeeded. If an error names a field you don't recognize, schema_describe shows the tool's full input schema. If a fix changes the text, media or settings the user approved, show the change and get a yes before posts_create. On a 429, wait briefly and retry.

Then report: scheduled posts by day and platform, drafts waiting for media, and anything that failed validation and why.

## Making it weekly

Suggest running it as a recurring task where the client supports it: scheduled tasks or routines in Claude Code, or scheduled tasks in Cowork. A good slot is a fixed day before the week starts. The task prompt should say: read `social-autopilot-notes.md`, review last week, plan and draft next week.

**Unattended runs** (no person in the conversation): only create DRAFT posts and write a summary of what was drafted and why. Never schedule or publish. If `social-autopilot-notes.md` can't be read, stop and write a note saying so instead of drafting. The user reviews the drafts later, in WoopSocial or in a follow-up conversation, and approves scheduling then. In an attended run, the normal approval in step 4 applies.

To schedule approved drafts later: posts_get each draft, posts_create the same payload with SCHEDULE_FOR_LATER and the approved time (validate first), then delete the draft (posts_delete) once the new post is confirmed. The approval covers these deletes.

## Never

- Schedule or publish without a person's explicit yes in this conversation.
- Say a draft is set for a date. Drafts are undated; put the planned day in the summary instead.
- Invent results, benchmarks or claims.
- Show internal IDs.
