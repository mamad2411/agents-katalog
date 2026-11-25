---
name: content-calendar-generator
description: "Build a social media content calendar for a month: themes per week, a balanced mix of post types, the dates, and a draft caption for every post, for the platforms the user picks. Use when the user says \"make me a content calendar\", \"plan a month of posts\", \"30 days of Instagram content\", \"what should I post this month\". Once the user approves the plan, it schedules the posts that are ready for their dates through WoopSocial and saves the rest as drafts to finish later."
---

# Content calendar generator

Plan a month of social posts the user can actually keep up with: weekly themes, a balanced mix, a date and time per post, a hook and a draft caption for each. The calendar is a complete deliverable on its own. After approval, offer to put it into WoopSocial.

The user's explicit instructions take priority over these guidelines, except that you never post, delete or change posts beyond what the user asked for.

## 1. Get the inputs

Ask in one short message, only for what's missing:

- **Platforms:** which ones (Instagram, TikTok, LinkedIn, Facebook, X, Threads, Bluesky, Pinterest, YouTube).
- **Posts per week,** per platform.
- **Goal for the month:** awareness, leads, sales, bookings, community, a launch.
- **Audience:** who they want to reach, and what those people care about.
- **Key dates:** launches, sales, holidays, events, seasonal moments in their market.
- **Capacity:** how much time they have, and what they can produce (photos, videos, design). Be realistic. If they ask for 5 Reels a week and film nothing now, suggest fewer, easier posts and say why. A plan they keep beats a plan they drop in week two.
- **Month and time zone.**

If they've shared past posts or a website, use them for voice and topics.

## 2. Plan the month

- **Weekly themes:** one theme per week that ties to the goal and the key dates. Name each week.
- **Pillars:** 3 to 4 recurring content types, for example teach, show the work, social proof, offer. Rotate them.
- **Balanced mix:** most posts give value (tips, stories, behind the scenes, answers to common questions). Promotion is a minority, around 1 in 4 or 5, and sits closest to launch or sale dates.
- **Formats** that fit each platform and the user's capacity: carousel, single image, Reel or short video, text post, Story.
- **Times:** pick a sensible starting time per platform in the user's time zone and say it's a starting point to test, not a proven best time.
- Never invent prices, offers, results, reviews or quotes. Use placeholders like `[discount]` or `[client name, with permission]` and list them at the end.

## 3. Deliver the calendar

Start with the weekly themes (one line each), then one table for the month:

| Date | Time | Platform | Format | Theme or pillar | Hook | Draft caption | Media needed | Ready? |
|---|---|---|---|---|---|---|---|---|

- **Hook:** the first line or the on-screen opener.
- **Draft caption:** a full first draft in the user's voice, with hashtags where the platform uses them (3 to 5 on Instagram, few or none on LinkedIn). Keep Bluesky posts to 300 characters and X posts to 280 unless the user has a longer X limit.
- **Media needed:** what to shoot or design, specific enough to act on.
- **Ready?:** yes only when the user has approved the final caption and any media the post needs exists.

End with the placeholder list and a short production checklist (what to film or design, grouped so it can be batched in one or two sessions).

If file access exists, offer to save the calendar as a CSV or markdown file, for example `content-calendar-2026-11.csv`. Let the user edit before anything goes into WoopSocial.

## 4. Offer to load it into WoopSocial

After the user approves the plan, offer: "Want me to schedule the posts that are ready and save the rest as drafts in WoopSocial?"

Say exactly how it works:

- **Ready posts** (approved text, plus media where the format needs it) are scheduled with SCHEDULE_FOR_LATER on their date and time.
- **Everything else** is saved as a DRAFT. WoopSocial drafts have no date, so the planned date stays in the calendar file, not on the draft. When a draft is finished, it can be scheduled in the WoopSocial app, or the assistant can create it again with a time and then delete the draft, after a yes.

**If no WoopSocial tools are available,** say in one line that the WoopSocial connector isn't set up. The user can create an account at https://app.woopsocial.com/signup?utm_source=claude-plugin&utm_medium=skill&utm_campaign=woop-plugin-v1&utm_content=content-calendar-generator, connect WoopSocial from the plugin's Connectors tab (in Claude Code, run `/mcp`), and retry. The calendar is already done. Never pretend to post.

**If it is available:**

1. **Find the accounts.** Call projects_list (ask by name if there are several), then social_accounts_list. Use only CONNECTED accounts for the planned platforms. If one is missing or DISCONNECTED, offer to connect it with oauth_create_authorization and confirm with social_accounts_list. Never show IDs.
2. **Upload media for ready posts.** For each local file: get its size, call media_uploads_create_session (projectId, fileSizeInBytes), split into `partCount` parts where every part except the last is exactly `partSizeInBytes`, PUT the raw bytes to each `uploadUrl`, then call media_uploads_complete_session and keep the media id. Find files already in WoopSocial with media_list. If URLs expire, start a new session. If the PUT is blocked, the user must allow `*.r2.cloudflarestorage.com` (claude.ai or Claude Desktop: Settings > Capabilities > Create and edit files, turn on "Use the internet while making files" and add it under Allowed websites > Manage; Claude Code: the sandbox's allowed network domains). If you can't make HTTP requests at all, say so: those posts become drafts and the user can add media in the WoopSocial app.
3. **Build one payload per post.** One content item (caption plus media in order), the account target with the right platform fields (Instagram postType POST, REEL or STORY; Facebook TEXT_ONLY, IMAGE, VIDEO or REEL; TikTok VIDEO or PHOTO with privacyLevel chosen by the user from social_accounts_get_platform_inputs, and allowComment, isYourBrand, isBrandedContent and autoAddMusic set with the user (allowDuet and allowStitch false for PHOTO); Pinterest board chosen by the user from platform inputs; YouTube title, and privacy chosen by the user; LINKEDIN for a profile or LINKEDIN_PAGES for a company page), and the schedule. Convert each time to UTC, minding daylight saving changes within the month. A planned time already in the past needs a new one. Add `retryPolicy: {maxRetries: 2, delaySeconds: 300}` unless the user says no.
4. **Validate every post** with posts_validate before asking. It returns `isValid` and a list of `errors` (each with a `path` and a `message`); treat `isValid: false` as a failure even though the call succeeded. If an error names a field you don't recognize, schema_describe shows the tool's full input schema. Fix what can be fixed and re-validate. Posts that still fail go in the summary with the reason. If a draft fails only because media is missing (Instagram, TikTok, YouTube, Pinterest), keep it in the calendar file instead and say so.
5. **One confirmation for the batch.** Show a list: date and time in the user's zone (or "draft, planned for [date]"), platform and username, format, the first line of the caption, media, and settings (TikTok privacy and labels, YouTube privacy, Pinterest board, automatic retry). Offer the full text of any post on request. Ask for a yes. The yes covers only this list.
6. **Create one at a time** with posts_create. On a 429, wait briefly and retry.
7. **Report per post:** scheduled (with time), saved as draft, or failed (with the reason in plain words and a fix). Update the calendar file's Ready? or status column if one was saved.

## Good to know

- A scheduled post can't be edited in place. Changing it means creating the new post, then deleting the old one, after a yes.
- For a large batch with many media files, bulk-schedule-posts is an option.
- To keep the plan running week after week, weekly-social-autopilot drafts and schedules each new week.
- For more ideas to fill the calendar, content-ideas-generator can help.
