---
name: bulk-schedule-posts
description: "Bulk schedule many posts at once through WoopSocial from a spreadsheet, CSV, Notion table or a folder of photos and videos. Use when the user says \"schedule all of these\", \"upload this folder and spread it over the month\", \"import my content calendar sheet\", \"I have 30 clips to post\". Maps rows or files to accounts and dates, writes missing captions, uploads media, validates every post, shows the full queue for approval, then schedules it."
---

# Bulk schedule posts

Turn a content calendar or a pile of media into a full, validated queue in WoopSocial with one approval. The work is in the mapping and the checking: get every row right before anything is created.

The user's explicit instructions take priority over these guidelines, except that you never post, delete or change posts beyond what the user asked for.

## If WoopSocial isn't connected

If no WoopSocial tools are available, say the WoopSocial connector isn't set up. The user can create an account at https://app.woopsocial.com/signup?utm_source=claude-plugin&utm_medium=skill&utm_campaign=woop-plugin-v1&utm_content=bulk-schedule-posts and connect WoopSocial from the plugin's Connectors tab (in Claude Code, run `/mcp`), then retry. You can still clean up the sheet and build the queue table now, so offer that. Never pretend to post.

## 1. Read the input

Accept any of these:

- **CSV** or a **Google Sheet export** (File > Download > CSV)
- **Notion table export** (Export > Markdown & CSV) or a table pasted into chat
- **A folder of photos or videos**, with or without captions

If the user shares a Google Sheet or Notion link that you can't open, ask for the CSV export.

## 2. Map the columns

Find these columns, whatever they're called:

| Field | Typical headers | Needed |
|---|---|---|
| Date | date, day, publish date | Yes |
| Time | time, hour (or inside the date) | Yes, or a default the user sets |
| Platform | platform, channel, network | Yes, or one platform for all |
| Text | caption, copy, text, post | Yes, unless the user approves writing them |
| Media | file, image, media path, filename | When the platform needs it |
| Link, title | link, url, title | Optional (title is required for YouTube) |

Show the mapping in a few lines and ask about anything ambiguous: a date like 03/04 (March 4 or April 3?), a time without am/pm, "IG + FB" in one cell (one post to both), a platform name that matches two accounts, LinkedIn profile or company page. Ask the time zone once.

## 3. A folder of media

List the files, then propose a spread, for example "one post a day at 9:00, Monday to Friday, starting next Monday, in filename order". Ask which platforms and let the user adjust days, times and order. If they know their best posting times, use those. Don't claim to know them otherwise.

## 4. Missing captions

If rows have no text, ask before writing any. With approval, write each caption for its platform and the file it goes with (look at the image if you can). Never invent prices, results, reviews or claims. Use a `[placeholder]` and flag it.

## 5. Resolve accounts

Call projects_list (ask by name if there are several), then social_accounts_list. Every post in one call must use accounts from the same project. Match each row's platform to a CONNECTED account and show accounts by platform and username, never IDs. If a platform is missing or DISCONNECTED, offer to connect it with oauth_create_authorization before going on.

For Pinterest rows, call social_accounts_get_platform_inputs and map each row to a board by name. For TikTok rows, call it too and ask the user once for privacy (only from `privacyLevelOptions`), comments, duets and stitches (only where available), and whether the content is AI-generated or promotional. Apply those answers to every TikTok row unless the user says otherwise. YouTube rows need a title and a privacy choice. Instagram and Facebook rows need a post type: an image or carousel is POST (Instagram) or IMAGE (Facebook), and a vertical video is REEL. Show it in the Notes column. For TikTok photo rows, also ask whether TikTok should add music (`autoAddMusic`).

## 6. Show the queue

Show the whole queue as one table before uploading anything:

| # | Date and time (user's zone) | Platform | Account | Text (first line) | Media | Notes |
|---|---|---|---|---|---|---|

Flag rows now: missing media where it's required, past dates, duplicates, missing YouTube titles. Let the user fix or drop rows.

## 7. Upload all media

Upload every local file, one at a time, and keep a row-to-media-id map. Reuse the id when one file is in several rows.

1. Get the file size. Call media_uploads_create_session with projectId and fileSizeInBytes. Files over 5 GB are rejected, so flag them.
2. Split the file into `partCount` parts. Every part except the last is exactly `partSizeInBytes`. PUT each part's raw bytes to its `uploadUrl` (a short script works best for many files).
3. Call media_uploads_complete_session and record the media id. If the URLs expire (`expiresAt`), start a new session.

Uploads need code execution or a shell with network access. If they're blocked, ask the user to allow `*.r2.cloudflarestorage.com` (claude.ai or Claude Desktop: Settings > Capabilities > Create and edit files, turn on "Use the internet while making files" and add it under Allowed websites > Manage; Claude Code: the sandbox's allowed network domains). If you can't make HTTP requests at all, say so plainly. The fallback: the user uploads the files in the WoopSocial app, then you find them with media_list and match them to rows by filename. Text-only rows (X, Threads, Bluesky, LinkedIn, Facebook) can go ahead either way.

## 8. Validate every post

Build one payload per row: one content item (text, media), the target with its platform fields, `schedule` SCHEDULE_FOR_LATER with `scheduledFor` in UTC (or DRAFT if the user wants drafts), and `retryPolicy: {maxRetries: 2, delaySeconds: 300}` unless the user doesn't want retries, so short platform hiccups fix themselves.

Call posts_validate for every row, one row at a time. On a 429, wait and retry that row. It returns `isValid` and a list of `errors` (each with a `path` and a `message`); treat `isValid: false` as a failure even though the call succeeded. If an error names a field you don't recognize, schema_describe shows the tool's full input schema. List problems per row in plain words ("Row 7, Instagram: video aspect ratio not accepted"). Fix what you can, re-validate, and ask about anything that changes the user's content. posts_validate is the final check on text length and file format, so don't guess limits.

## 9. One confirmation, then create

Show the final queue table with every row valid, plus any rows dropped and why. Ask for one yes for the full queue. The yes covers exactly that table.

Then call posts_create for each row, one at a time, in date order. On a 429 (too many requests), wait a few seconds and retry that row. Don't fire calls in parallel.

## 10. Report per row

Give the table back with a status column: scheduled, or failed with the reason in plain words. Offer to retry the failed rows once the cause is fixed. Totals at the end: "28 scheduled, 2 failed."

## Good to know

- A scheduled post can't be edited in place. To change one, show the new version, get a yes, create it, then delete the old one. manage-post-queue handles moving or cancelling later.
- Planning the calendar from scratch, rather than importing one: content-calendar-generator can build it first.
- If a row fails after scheduling, fix-failed-posts can find and re-send it.
