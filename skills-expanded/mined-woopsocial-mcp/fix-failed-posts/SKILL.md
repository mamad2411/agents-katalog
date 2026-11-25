---
name: fix-failed-posts
description: "Find and fix social media posts that failed to publish in WoopSocial. Use when the user says \"my post didn't go out\", \"Instagram post failed\", \"why did this fail\", \"TikTok upload error\", or wants failed posts re-sent. Lists failed deliveries, explains the platform error in plain words where it's clear, helps fix the cause (reconnect an account, shorten text, swap in a re-exported file), and re-sends with automatic retries switched on."
---

# Fix failed posts

Find what didn't go out, explain why in plain words, fix the cause, and re-send. Be honest about errors you can't read: show them rather than guess.

The user's explicit instructions take priority over these guidelines, except that you never post, delete or change posts beyond what the user asked for.

## If WoopSocial isn't connected

If no WoopSocial tools are available, say the WoopSocial connector isn't set up. The user can create an account at https://app.woopsocial.com/signup?utm_source=claude-plugin&utm_medium=skill&utm_campaign=woop-plugin-v1&utm_content=fix-failed-posts and connect WoopSocial from the plugin's Connectors tab (in Claude Code, run `/mcp`), then retry. Without it there are no delivery records to check. Never pretend to re-send anything.

## 1. Find the failures

1. Call projects_list. If there are several projects, ask which brand, or check them all if the user wants.
2. Call social_accounts_list for the project so you can name accounts by platform and username (never IDs) and see which are DISCONNECTED.
3. Call social_account_posts_list with `deliveryStatus: FAILED` and the projectIds. Narrow with `platform` or `socialAccountIds` if the user named one ("my Instagram post"). Follow `nextCursor` until there are no more pages. Default to failures from the last 30 days (`deliveryCompletedAt`) and say how many older ones exist.
4. If the user means one specific post and it isn't FAILED, check its status: NOT_STARTED means it's still scheduled, SENDING means it's going out now, PUBLISHED means it's live (share externalPostUrl). Tell them which.
5. For each failure, check whether an automatic retry already handled it: list posts for that account (PUBLISHED and NOT_STARTED) and look for the same text after the failure time. Published: tell the user it went out (externalPostUrl) and skip it. Waiting: tell the user and let it run, or, with a yes, cancel it (posts_delete) before re-sending, so the post doesn't go out twice.

If calls keep failing, call health_get to check whether WoopSocial itself is reachable.

## 2. Group by cause

Read each `errorMessage` and group the failures. Show a short table:

| Cause (plain words) | Posts | Platform(s) | Fix |
|---|---|---|---|

For each post, include the account, the scheduled time in the user's time zone (`schedule.scheduledFor`, or "publish now"), when it failed (`deliveryCompletedAt`) and the first line of its text.

## 3. Explain and fix each cause

- **Account disconnected or login expired.** The platform no longer accepts WoopSocial's access, often after a password change or expired permission. Fix: create a new sign-in link with oauth_create_authorization (projectId, platform), the user opens it and approves, then confirm the account is CONNECTED with social_accounts_list.
- **Media rejected** (wrong format, size, length or aspect ratio). Fix: the user re-exports the file in a format and shape the platform accepts (for example a vertical MP4 for Reels or TikTok), then re-upload it. posts_validate checks the request, but the platform only judges the file when it publishes, so say the new version could still fail if it breaks the same rule.
- **Text too long.** Fix: shorten it. Show the shorter version and get the user's OK before using it.
- **Duplicate content.** Some platforms reject a post that matches a recent one. Fix: change the text slightly (reword the first line, add a detail). Show the change first.
- **Platform outage or temporary error.** Nothing is wrong with the post. Fix: just retry.
- **Out of credits or plan limits.** The user needs to sort this in their WoopSocial account before re-sending.
- **Unclear error.** If the errorMessage doesn't clearly say what went wrong, say so and show the exact message. Don't invent a cause. Offer a plain retry if it might be temporary, or suggest the user checks the account on the platform itself.

## 4. Re-send

There is no edit endpoint. Re-sending means creating a new post with the fix applied:

1. Take the failed post's `content` (text and media). Reuse its media ids as `{type: MEDIA_LIBRARY, mediaId}` unless the media itself was the problem. For new or re-exported files, upload them:
   - Get the file size, call media_uploads_create_session (projectId, fileSizeInBytes, max 5 GB).
   - Split into `partCount` parts, every part except the last exactly `partSizeInBytes`, and PUT each to its `uploadUrl`.
   - Call media_uploads_complete_session and use the returned media id.
   If uploads are blocked, ask the user to allow `*.r2.cloudflarestorage.com` (claude.ai or Claude Desktop: Settings > Capabilities > Create and edit files, turn on "Use the internet while making files" and add it under Allowed websites > Manage; Claude Code: the sandbox's allowed network domains). If you can't make HTTP requests at all, say so and offer two options: the user uploads the file in the WoopSocial app and you find it with media_list, or a text-only post where the platform allows it.
   Upload links expire at `expiresAt`; if they do, start a new session.
2. Call posts_get on the failed post to copy every setting: platform fields (post type, privacy, board, title, link and so on), `contentOverride`, `retryPolicy` and `autoDeleteMediaAfterPublish`. After a reconnect, take the account from a fresh social_accounts_list.
3. Ask when: now (PUBLISH_NOW), or a new time (SCHEDULE_FOR_LATER with `scheduledFor` in UTC; if the original time has passed, it can't be reused). Ask the time zone once if unclear.
4. Keep the original `retryPolicy`. If it had none, add `retryPolicy: {maxRetries: 2, delaySeconds: 300}` so a short platform hiccup fixes itself, and mention it in the summary, or in the report when no summary is needed. Adding retries doesn't change what gets posted, so it doesn't count as a change for step 6.
5. Call posts_validate. It returns `isValid` and a list of `errors` (each with a `path` and a `message`); treat `isValid: false` as a failure even though the call succeeded. If an error names a field you don't recognize, schema_describe shows the tool's full input schema. Fix what it flags and validate again.
6. **Ask first, or go?** If the user asked to re-send one post unchanged (same text, media and settings, now or at a time they gave), that request is the go-ahead. Otherwise show the summary per post (account, the exact text, media, settings, time in the user's zone, and what changed from the failed version) and wait for a yes. That applies whenever you changed anything or there's more than one post. With several posts, one yes can cover the whole list shown.
7. Call posts_create for each, one at a time. On a 429, wait briefly and retry.

## 5. Clean up the failed record

After the re-send works, ask whether to delete the old failed copy so it stops showing up. Only on a yes, call social_account_posts_delete for that failed record. Never delete without asking.

## 6. Report back

Per post: re-sent and scheduled (time), published (externalPostUrl from social_account_posts_list once PUBLISHED), or still failing with the reason. For PUBLISH_NOW, check again after about 30 seconds; publishing takes a moment. Mention any failures you couldn't fix and what the user needs to do.

## Good to know

- Automatic retries are separate new posts, scheduled the retry delay after the failure, so the failed record stays FAILED even after a retry succeeds. That's why step 1.5 checks for them.
- Automatic retries (`retryPolicy`) don't cover failures that need the user, like a disconnected account or running out of credits. Those always need the fix first.
- Rarely, a retry can cause a duplicate: if the platform published the post but never sent a reply back, the retry posts it again. If the user sees a double, they can delete one on the platform.
- After reconnecting an account, check for other FAILED posts on it. They aren't re-sent on their own.
- To see or reschedule the rest of the queue, manage-post-queue covers that.
