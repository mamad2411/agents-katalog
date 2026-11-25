---
name: instagram-posts
description: "Write and schedule Instagram posts, carousels, Reels and Stories through WoopSocial. Use when the user says \"post this to Instagram\", \"write a caption and schedule it\", \"schedule this Reel for Friday\", \"post a Story\", \"post this carousel\", or wants a Trial Reel shown to non-followers first. Writes or tightens the caption and hashtags if needed, uploads the media, sets post type and cover, validates, shows the post for approval when it wrote or changed anything, then publishes or schedules. For designing carousel slides from scratch, use instagram-carousel-maker."
---

# Instagram posts

Take what the user has (a photo, slides, a video, a rough caption) and turn it into a scheduled or published Instagram post through WoopSocial. Writing the caption is part of the job. Designing slides from scratch is not: point to instagram-carousel-maker for that.

The user's explicit instructions take priority over these guidelines, except that you never post, delete or change posts beyond what the user asked for.

## If WoopSocial isn't connected

If no WoopSocial tools are available, say the WoopSocial connector isn't set up. The user can create an account at https://app.woopsocial.com/signup?utm_source=claude-plugin&utm_medium=skill&utm_campaign=woop-plugin-v1&utm_content=instagram-posts and connect WoopSocial from the plugin's Connectors tab (in Claude Code, run `/mcp`), then retry. You can still write the caption now, so offer that. Never pretend to post.

## 1. Work out the post

Get these, asking only for what's missing:

| What | Options |
|---|---|
| Type | Feed post (one image or video), carousel (2 or more images/videos in one post), Reel (vertical video), Story |
| Media | Local file paths, files already in WoopSocial, or files the user will attach |
| Caption | User's text, or write one |
| When | Now, a date and time, or save as draft |
| Account | Which Instagram account, if more than one |

Map the type to WoopSocial: feed post and carousel are `postType: POST` (a carousel is one content item with several media). A Reel is `REEL`. A Story is `STORY`. Stories don't show captions, so don't write one, and tell the user any text must be on the image itself.

## 2. Write or tighten the caption

Skip this if the user gave final text and said to post it as is.

- **First line is the hook.** Only about the first 125 characters show before "more". Make it specific: a result, a question, a surprising detail. No "Hey guys!".
- **Then the value or story,** in short paragraphs.
- **One clear ask** that fits the goal: save it, share it, comment a word, tap the link in bio. Never "like and follow for more".
- **Hashtags:** 3 to 5 specific ones that real people search for (niche plus topic plus location if local), at the end. Instagram treats hashtags as topic signals now, so piling them on doesn't help.
- **Keywords in the caption** help Instagram search. Name the topic in plain words.
- Match the user's voice. If they shared past posts, copy their tone, emoji habits and length.
- Never invent prices, results, reviews or claims. Ask, or leave `[price]`-style placeholders and point them out.

Show the caption so the user can edit it now. The summary in step 6 covers the final yes.

## 3. Reel, Trial Reel and AI settings

- **Cover:** if the user has a cover image, upload it and set it as `cover`. Otherwise Instagram picks a frame. Mention that a cover with clear text helps the profile grid.
- **Trial Reel:** if the user wants to test a Reel with non-followers first, set `trialParams.graduationStrategy`:
  - `MANUAL`: the user decides in Instagram whether to share it with followers.
  - `SS_PERFORMANCE`: Instagram shares it with followers automatically if it performs well.
  Explain the choice in one line each and let them pick. Some accounts can't use Trial Reels. If validation rejects it, say so and offer a normal Reel.
- **AI-generated content** (any post type): set `isAiGeneratedContent: true` when the image or video was made or heavily changed with AI, including an AI voiceover. Instagram then shows its "AI info" label. It can only be set when the post is created, not added later. If unsure, ask.

## 4. Find the account

Call projects_list (ask by name if there are several), then social_accounts_list. Use the CONNECTED Instagram account. If there's none, or it's DISCONNECTED, offer to connect it now with oauth_create_authorization (projectId, platform INSTAGRAM). Give the user the link, wait for "done", then confirm with social_accounts_list. Instagram needs a Business or Creator account.

## 5. Upload the media

For each local file (slides in the right order for a carousel):

1. Get the file size. Call media_uploads_create_session with projectId and fileSizeInBytes.
2. Split the file into `partCount` parts. Every part except the last must be exactly `partSizeInBytes`. PUT each part's raw bytes to its `uploadUrl` (curl or a short script).
3. Call media_uploads_complete_session and keep the returned media id.

If the user says the files are already in WoopSocial, find them with media_list. If uploads are blocked by the network, ask the user to allow `*.r2.cloudflarestorage.com` (claude.ai or Claude Desktop: Settings > Capabilities > Create and edit files, turn on "Use the internet while making files" and add it under Allowed websites > Manage; Claude Code: the sandbox's allowed network domains). If you can't make HTTP requests here at all, say so plainly. The user can upload the media in the WoopSocial app, and you can still prepare the caption.

## 6. Validate, confirm, schedule

1. Build the payload: one content item with the caption and media (in order), `schedule` (DRAFT, PUBLISH_NOW, or SCHEDULE_FOR_LATER with `scheduledFor` in UTC), and the Instagram target with `postType`, plus `cover`, `trialParams` and `isAiGeneratedContent` when used. Add `retryPolicy: {maxRetries: 2, delaySeconds: 300}` unless the user doesn't want retries.
2. Call posts_validate with that payload. It returns `isValid` and a list of `errors` (each with a `path` and a `message`); treat `isValid: false` as a failure even though the call succeeded. If an error names a field you don't recognize, schema_describe shows the tool's full input schema. Fix what it flags (caption length, unsupported file, aspect ratio) and validate again. Ask before changing anything the user wrote.
3. **Ask first, or go?** If the user gave the final text and media, the account and the time, and you changed none of it, their request is the go-ahead: skip to step 4 without asking again. Show the summary below and wait for a yes when you wrote or changed any of the text, media or settings, when it's more than one post, or when the account, time or publish-versus-draft is unclear:
   - Account (username), post type, time in the user's time zone
   - Full caption
   - Media list in order, cover, Trial Reel setting, AI label
4. Call posts_create with the same payload.

If the time zone isn't clear, ask once. A time in the past isn't allowed, so ask for a new one.

## 7. Report back

- Scheduled: confirm the time and that it can be moved or cancelled any time before it goes out.
- Published now: delivery often takes a minute or two, longer for video. Check social_account_posts_list for this post, and if it's still NOT_STARTED or SENDING, say it's on its way and check once more. If it's still not done, tell the user it's in progress and that they can ask you to check again later. When deliveryStatus is PUBLISHED, share externalPostUrl. If FAILED, explain errorMessage in plain words and offer to fix and re-send.

## Good to know

- Posting several Instagram posts at once (a week of posts, a folder of photos) is a batch. Show the whole list, get one yes for all of it, then create the posts one at a time, or suggest bulk-schedule-posts.
- To post the same thing to other platforms too, suggest cross-post-everywhere.
- A scheduled post can't be edited in place. To change it, show the new version, get a yes, create it, then delete the old one.
- On a 429 (too many requests), wait briefly and retry one call at a time.
- Results (views, saves, shares) for posts sent through WoopSocial show up about a day later. social-media-report covers that.
