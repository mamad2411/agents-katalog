---
name: manage-post-queue
description: "See and manage scheduled social posts in WoopSocial: what's going out this week, gaps in the calendar, moving a post to a new time, cancelling posts, or pausing everything during a crisis or bad news and resuming later. Use when the user asks \"what's scheduled\", \"move Thursday's post\", \"cancel that post\", \"pause all my posts\", \"hold the queue\"."
---

# Manage the post queue

Show the user what's scheduled, and move, cancel, pause or resume posts safely. WoopSocial can't edit a scheduled post, so moving, pausing and resuming work by recreating it and deleting the original. Say this in one line before any of those.

The user's explicit instructions take priority over these guidelines, except that you never post, delete or change posts beyond what the user asked for.

## If WoopSocial isn't connected

If no WoopSocial tools are available, say the WoopSocial connector isn't set up. The user can create an account at https://app.woopsocial.com/signup?utm_source=claude-plugin&utm_medium=skill&utm_campaign=woop-plugin-v1&utm_content=manage-post-queue, connect WoopSocial from the plugin's Connectors tab (in Claude Code, run `/mcp`), sign in and retry. There's no queue to show until then. Never pretend to change anything.

## 1. Load the queue

1. Call projects_list (ask by name if there are several), then social_accounts_list so you can show platform and username. Never show IDs.
2. Call social_account_posts_list with projectIds and deliveryStatus NOT_STARTED,SENDING, limit 100. Keep calling with nextCursor until it's gone.
3. Split the results: `schedule.type` SCHEDULE_FOR_LATER are scheduled (they have `scheduledFor`). DRAFT items are drafts and have no date, so list them separately as "undated drafts".
4. Group items by postId. One post can go to several platforms; each platform copy is its own item.

Ask the time zone once if it isn't clear. Show the next 7 days unless the user asks for another range, and say how many posts are scheduled after that.

## 2. Show it

By day, in the user's time zone, sorted by time:

```
Tue 4 Nov
  08:00  Instagram (@shop), LinkedIn page  "First line of the text..."  [2 images]
  17:30  TikTok (@shop)                    "First line..."              [video]
```

Then point out, briefly:

- **Gaps:** days in the shown period with nothing on an account that has posts on other days.
- **Clusters:** several posts on the same account within a few hours, or the same text on the same day.
- **Retries:** an automatic retry of a failed post is its own new post, scheduled the retry delay after the failure, with the same text and account. To label retries, also list FAILED posts from the last few days and mark matching text on the same account as a retry.
- Anything that looks off: a post more than a few minutes in the past that's still NOT_STARTED, a DISCONNECTED account with posts waiting (those won't go out; offer to reconnect with oauth_create_authorization).

Items in SENDING are going out right now and can't be stopped or changed. Say so if the user asks about one.

## 3. Cancel

1. Identify the post with the user (day, time, platform, preview). Ask: all platforms, or just one?
2. Show what will be removed and ask for a yes.
3. All platforms: posts_delete on the parent post. It only works while every platform copy is still NOT_STARTED. If it returns `POST_NOT_DELETABLE`, one copy is already sending, published or failed; explain and offer to remove the remaining copies one by one.
   One platform: social_account_posts_delete for that platform's copy only.
4. Reload the list and confirm it's gone.

## 4. Move to a new time

There's no edit, so a move is recreate then delete. Say this in one line first.

1. Ask: all platforms, or just one? For one platform, the new post targets only that account and you delete only that copy (social_account_posts_delete).
2. Get the new time and convert to UTC. If the time is in the past, ask for another.
3. Call posts_get on the post to copy every setting: the same text and media ids (`type: MEDIA_LIBRARY`, `mediaId`, in order), each account with its platform fields (postType, privacyLevel, pinterestBoardId, title, link and so on), `contentOverride` where a platform differs, `retryPolicy` and `autoDeleteMediaAfterPublish`. Only change `schedule` to SCHEDULE_FOR_LATER with the new `scheduledFor`.
4. Call posts_validate. It returns `isValid` and a list of `errors` (each with a `path` and a `message`); treat `isValid: false` as a failure even though the call succeeded. If an error names a field you don't recognize, schema_describe shows the tool's full input schema. Fix and re-validate if needed.
5. Show old time, new time, accounts and text preview. Ask for a yes.
6. posts_create. Only after it confirms the new post was created, delete the old one (posts_delete, or social_account_posts_delete if only one platform moves).
7. Reload and show the new slot. If the delete fails, tell the user both copies exist right now and offer to retry the delete.

Moving several posts: show the full list of old and new times, get one yes, then do them one at a time.

## 5. Pause everything (crisis or bad news)

Goal: nothing goes out, and nothing is lost.

1. List every SCHEDULE_FOR_LATER item that's NOT_STARTED for the project (or the accounts the user names).
2. Write a recovery list, one row per post: platforms and usernames, original time in the user's zone, and the first line of the text. If you can write files, save it (for example `queue-recovery-<date>.md`) and say where. Always show it in chat as well. The drafts keep the full text, media and settings.
3. Explain the plan once: each post is recreated as an undated DRAFT in WoopSocial, then the scheduled original is deleted. Ask for one yes for the whole list.
4. Work soonest first, one post at a time: posts_get the original, posts_validate and posts_create the same payload with `schedule: {type: DRAFT}`, confirm it was created, then posts_delete the original. If the delete returns `POST_NOT_DELETABLE`, the post is already going out: tell the user and delete the new draft (the yes above covers this). On a 429, wait and retry that call.
5. Reload the queue and report: how many paused, any that couldn't be (for example already SENDING), and that the recovery list holds the original times.

## 6. Resume

1. List the drafts (social_account_posts_list, NOT_STARTED, `schedule.type` DRAFT) and match them to the recovery list (ask the user to paste it, or read the saved file) for the original times. If there's no recovery list, show the drafts and ask for times.
2. Ask for new times: the original ones where they're still in the future, and new ones for anything whose time has passed. Past times must move forward. Offer to spread them out rather than release everything at once.
3. Show the new schedule, say each draft is deleted once its scheduled copy exists, and ask for one yes.
4. One post at a time: posts_get the draft, posts_validate and posts_create the same payload with SCHEDULE_FOR_LATER and the new time, then posts_delete the draft once the new post is confirmed.
5. Reload and show the queue by day.

## Good to know

- Go one call at a time. On a 429, wait briefly and retry.
- If a call fails mid-batch, stop, report what was done and what's left, and ask before continuing.
- To fill gaps with new posts, instagram-posts, linkedin-posts, tiktok-posts, cross-post-everywhere or bulk-schedule-posts can help. Failed posts belong in fix-failed-posts.

## Never

- Delete anything without a yes for exactly what was shown.
- Delete an original before its replacement is confirmed created.
- Show internal IDs.
- Say a draft is "on" a date. Drafts are undated.
