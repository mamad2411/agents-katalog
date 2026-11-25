---
name: content-ideas-generator
description: "Generate social media post ideas that fit the user's niche, audience and platforms, each with a hook and a format (carousel, Reel, text post, Story). Use when the user says \"give me content ideas\", \"what should I post\", \"I'm out of ideas\", \"post ideas for my bakery\". When WoopSocial is connected, it starts from the user's best-performing posts sent through WoopSocial. Ideas the user picks can be saved in WoopSocial as drafts or scheduled."
---

# Content ideas generator

Give the user up to 20 specific post ideas they could make this week, not a list of generic topics. When WoopSocial is connected, build on what already works for them. Ideas they pick can become drafts or scheduled posts.

The user's explicit instructions take priority over these guidelines, except that you never post, delete or change posts beyond what the user asked for.

## 1. Know the account

Ask only for what's missing, in one message:

- **Niche:** what they do or sell, and where (local business, online, B2B).
- **Audience:** who they want to reach and what that person cares about.
- **Goal:** reach, traffic, sales, community.
- **Platforms** they post to.
- Anything they can or can't produce (no face on camera, no time for video, product photos only).

If they shared past posts or a website, use the specifics in them: product names, places, customer questions, recurring events.

## 2. Start from their best posts (if WoopSocial is connected)

If WoopSocial tools are available:

1. projects_list (ask by name if several), then social_accounts_list. Never show IDs.
2. social_account_posts_list_analytics with projectId and startDate and endDate covering the last 90 days, limit 100, following nextCursor.
3. Each post's `metrics` holds its lifetime totals. Rank by (saves + shares) divided by views where views exist. Where there are no views, use saves and shares, or comments or clicks if those fit the goal better.
4. Take the top few and work out why they worked: topic, format, hook, angle.

Only posts sent through WoopSocial are included, and metrics refresh about once a day. A missing metric means the platform doesn't report it or nothing has been collected yet; a 0 is a real zero. Leave out posts younger than about 48 hours, which are still collecting numbers. If there are no published posts yet, say so and generate from the niche alone.

If WoopSocial isn't connected, skip this step and generate from what the user told you.

## 3. Generate the ideas

Give up to 20 ideas, usually 10 to 15, in a table. Fewer strong ideas beat a padded list.

| # | Hook (first line or first second) | Format | Platform | Type | Why it should work |
|---|---|---|---|---|---|

- **Format:** carousel, Reel, text post, Story, photo, or video.
- **Type:** mix teach, show, prove, story, opinion and behind the scenes. No more than a third of one type, and few direct sales posts.
- **Hook:** written out, specific, in their voice. Not "5 tips for success" but "The 3 questions every bride asks us about buttercream in October".
- **Why:** one line. When an idea builds on one of their posts, name it ("builds on your 'oven at 4am' Reel, your most saved post").
- Name real specifics: their products, places, seasons, customer questions. Leave a `[placeholder]` for anything you don't know.
- Never invent results, reviews, prices or claims in a hook. "Our customers love it" only if they said so.

Avoid ideas any account in the niche could post unchanged. If an idea is generic, sharpen it or drop it.

## 4. From ideas to posts

Ask which ideas they want to use. Then:

1. Draft each picked idea as a ready post for its platform: the hook, the body, one clear ask, and hashtags where the platform uses them. For carousels, outline the slides. For video, give a short shot list. Show the drafts and let them edit.
2. **Not connected:** stop here, or offer to connect so they can save the drafts. They can create an account at https://app.woopsocial.com/signup?utm_source=claude-plugin&utm_medium=skill&utm_campaign=woop-plugin-v1&utm_content=content-ideas-generator, then connect WoopSocial from the plugin's Connectors tab (in Claude Code, run `/mcp`) and sign in. connect-social-accounts can walk them through it. Never pretend to save or post.
3. **Connected:** use CONNECTED accounts only. Offer to connect a missing platform with oauth_create_authorization, and confirm with social_accounts_list after the user says done.
   - Default: save each as a DRAFT (`schedule: {type: DRAFT}`). Drafts have no date; they wait in WoopSocial until the user schedules them.
   - Set the fields each target needs: postType for Instagram and Facebook; for TikTok, privacyLevel and labels chosen by the user; YouTube title and privacy; Pinterest board. A draft for a platform that needs media (Instagram, TikTok, YouTube, Pinterest) may fail validation without a file. If so, say why and keep the draft in chat.
   - If the user gives times and the needed media: schedule with SCHEDULE_FOR_LATER and `scheduledFor` in UTC. Ask the time zone once if unclear; a past time isn't allowed. Upload local files with media_uploads_create_session, PUT each part to its uploadUrl (every part but the last exactly partSizeInBytes), then media_uploads_complete_session. Reuse uploaded files via media_list. If uploads are blocked, ask the user to allow `*.r2.cloudflarestorage.com`. Text-only drafts need no upload. Add `retryPolicy: {maxRetries: 2, delaySeconds: 300}` for scheduled posts unless the user says no.
   - Run posts_validate for each. It returns `isValid` and a list of `errors` (each with a `path` and a `message`); treat `isValid: false` as a failure even though the call succeeded. If an error names a field you don't recognize, schema_describe shows the tool's full input schema. Fix and re-validate.
   - Show the list (account, type, text, media, settings including automatic retry, draft or time in their zone) and get a yes. Then posts_create one at a time. On a 429, wait and retry.
4. Report what was saved as drafts and what was scheduled, per platform.

For a whole month of posts, content-calendar-generator is an option. For carousel slide design, instagram-carousel-maker.

## Never

- Pad the list with generic ideas to reach a number.
- Say an idea "will go viral" or quote made-up numbers.
- Create anything in WoopSocial without a yes.
- Show internal IDs.
