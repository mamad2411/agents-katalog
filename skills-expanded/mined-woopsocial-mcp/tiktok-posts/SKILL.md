---
name: tiktok-posts
description: "Write captions for and schedule TikTok videos and photo carousels through WoopSocial. Use when the user has the video or images ready and says \"post this to TikTok\", \"schedule my TikTok for 7pm\", \"upload this slideshow to TikTok\", \"write a TikTok caption and post it\", or asks how to set privacy, duets, stitches, branded-content or AI-generated labels. Writes the caption and hashtags, uploads, applies the TikTok settings, validates, shows the post for approval when it wrote or changed anything, then publishes or schedules."
---

# TikTok posts

Take a finished video or a set of images and get it onto TikTok through WoopSocial, with a caption that works and the right TikTok settings. TikTok has more required settings than other platforms, and some must come from the user, so don't skip them.

The user's explicit instructions take priority over these guidelines, except that you never post, delete or change posts beyond what the user asked for.

## If WoopSocial isn't connected

If no WoopSocial tools are available, say the WoopSocial connector isn't set up. The user can create an account at https://app.woopsocial.com/signup?utm_source=claude-plugin&utm_medium=skill&utm_campaign=woop-plugin-v1&utm_content=tiktok-posts and connect WoopSocial from the plugin's Connectors tab (in Claude Code, run `/mcp`), then retry. You can still write the caption now, so offer that. Never pretend to post.

## 1. Find the account and its options

Call projects_list (ask by name if there are several), then social_accounts_list. Use the CONNECTED TikTok account and show it by username, never by ID. If it's missing or DISCONNECTED, offer to connect it now with oauth_create_authorization (projectId, platform TIKTOK), wait for "done", then confirm with social_accounts_list.

Then call **social_accounts_get_platform_inputs** for that account before anything else. It returns what this account may use right now:

- `privacyLevelOptions`: the only privacy values you may offer
- `commentAvailable`, `duetAvailable`, `stitchAvailable`: whether each can be turned on
- `maxVideoPostDurationSec`: the longest video this account may post

## 2. Work out the post

| What | Options |
|---|---|
| Type | Video (`postType: VIDEO`) or photo carousel (`postType: PHOTO`, several images swiped like a slideshow) |
| Media | Local files, or files already in WoopSocial |
| Caption | User's text, or write one |
| When | Now, a date and time, or save as draft |

For a video, check its length (for example with ffprobe if a shell is available). If it's longer than `maxVideoPostDurationSec`, say so and ask the user to trim it. Don't upload a video that will be rejected.

## 3. Posting mode

Explain both in one line each and let the user pick:

- **Post directly** (`postMode: DIRECT_POST`): it goes live on TikTok at the scheduled time.
- **Send to TikTok inbox** (`postMode: MEDIA_UPLOAD`): the video lands in the user's TikTok inbox and they finish and publish it in the app. Best when they want to add a trending sound, text or effects in TikTok itself.

## 4. TikTok settings (ask, never assume)

- **Privacy** (direct post only): offer only the values in `privacyLevelOptions`, in plain words: everyone (`PUBLIC_TO_EVERYONE`), followers (`FOLLOWER_OF_CREATOR`), friends who follow back (`MUTUAL_FOLLOW_FRIENDS`), only me (`SELF_ONLY`). The user must choose. Never pick one silently, not even "everyone".
- **Comments, duets, stitches:** ask which to allow. Only offer one if its `...Available` flag is true, otherwise send false. Duets and stitches only apply to videos. For photo posts send them as false.
- **Music on photo posts:** for `PHOTO`, ask whether TikTok should add music automatically (`autoAddMusic`). For video send false.
- **AI-generated content** (video): set `isAiGeneratedContent: true` when the video was made or heavily changed with AI. If unsure, ask. TikTok expects this label. For photo posts send false.
- **Promotion labels**, explained plainly:
  - `isYourBrand`: the post promotes the user's own business, product or service.
  - `isBrandedContent`: someone paid them or gave them something to post it (a paid partnership).
  Ask if the post promotes anything. Both can be false for ordinary posts.
- **Cover** (video only, optional): WoopSocial adds the user's image as a single frame at the very start of the video. Tell the user this before using it. Without one, they can pick the cover in TikTok.

The API needs `allowComment`, `allowDuet`, `allowStitch`, `isYourBrand`, `isBrandedContent` and `autoAddMusic` on every TikTok target, so always send all six as true or false.

## 5. Write the caption

Skip if the user gave final text and said to post it as is.

- **Open with a hook** that matches the first second of the video: the payoff, a question, a bold claim the video backs up.
- **Keep it short.** One or two lines of context, plain words people search for (TikTok search reads captions).
- **3 to 5 hashtags:** a mix of topic and niche ones that fit the content. No #fyp padding.
- Match the user's voice. Never invent prices, results or claims. Ask, or leave a `[placeholder]` and point it out.

Show the caption and let the user edit before moving on.

## 6. Upload the media

For each file (images in swipe order for a photo post):

1. Get the file size. Call media_uploads_create_session with projectId and fileSizeInBytes (max 5 GB).
2. Split the file into `partCount` parts. Every part except the last must be exactly `partSizeInBytes`. PUT each part's raw bytes to its `uploadUrl` (curl or a short script).
3. Call media_uploads_complete_session and keep the returned media id.

Files already in WoopSocial: find them with media_list. If uploads are blocked by the network, ask the user to allow `*.r2.cloudflarestorage.com` (claude.ai or Claude Desktop: Settings > Capabilities > Create and edit files, turn on "Use the internet while making files" and add it under Allowed websites > Manage; Claude Code: the sandbox's allowed network domains). If you can't make HTTP requests at all, say so plainly. TikTok always needs media, so the user would upload it in the WoopSocial app. You can still prepare the caption and settings.

## 7. Validate, confirm, schedule

1. Build the payload: one content item with caption and media, `schedule` (DRAFT, PUBLISH_NOW, or SCHEDULE_FOR_LATER with `scheduledFor` in UTC), and the TikTok target with `postType`, `postMode`, `privacyLevel` (direct post), the six booleans, `isAiGeneratedContent`, and `cover` if used. Add `retryPolicy: {maxRetries: 2, delaySeconds: 300}` unless the user doesn't want retries.
2. Call posts_validate. It returns `isValid` and a list of `errors` (each with a `path` and a `message`); treat `isValid: false` as a failure even though the call succeeded. If an error names a field you don't recognize, schema_describe shows the tool's full input schema. Fix what it flags and validate again. Ask before changing anything the user wrote or chose. posts_validate is the final check on format and size.
3. **Ask first, or go?** If the user gave the final text and media, the account, the time and every TikTok setting in section 4, and you changed none of it, their request is the go-ahead: skip to step 4 without asking again. Show the summary below and wait for a yes when you wrote or changed any of the text, media or settings, when it's more than one post, or when the account, time or publish-versus-draft is unclear:
   - Account (username), type, posting mode, time in the user's time zone
   - Full caption
   - Media in order, cover
   - Privacy, comments, duets, stitches, music, AI label, promotion labels
4. Call posts_create with the same payload.

If the time zone isn't clear, ask once. "7pm" means the user's local time: convert to UTC. A time in the past isn't allowed.

## 8. Report back

- Scheduled: confirm the time and that it can be cancelled before it goes out.
- Inbox mode: once delivered, the post waits in the user's TikTok inbox. Tell them to open TikTok and finish it from the notification. It isn't public until they do.
- Published now: delivery often takes a minute or two, longer for video. Check social_account_posts_list for this post, and if it's still NOT_STARTED or SENDING, say it's on its way and check once more. If it's still not done, tell the user it's in progress and that they can ask you to check again later. When PUBLISHED, share externalPostUrl. If FAILED, explain errorMessage in plain words and offer to fix and re-send.

## Good to know

- Many TikToks at once: one confirmation for the whole list, then create them one at a time, or suggest bulk-schedule-posts.
- On a 429 (too many requests), wait briefly and retry one call at a time.
- The same video on Reels and Shorts too: suggest cross-post-everywhere.
- A scheduled post can't be edited in place. To change it, show the new version, get a yes, create it, then delete the old one.
- Designing the slides for a photo carousel from scratch: instagram-carousel-maker can help, then come back here to post.
