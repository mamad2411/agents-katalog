---
name: linkedin-posts
description: "Write and schedule LinkedIn posts for a personal profile or a company page through WoopSocial. Use when the user says \"write a LinkedIn post about this\", \"turn this into a LinkedIn post and schedule it\", \"post this to our company page Tuesday 8am\", \"queue my LinkedIn posts for the week\". Writes for LinkedIn (a hook that earns \"see more\", short lines, a real question, no engagement bait), attaches a link, image or video, picks profile or page, validates, shows the post for approval when it wrote or changed anything, then publishes or schedules."
---

# LinkedIn posts

Turn an idea, a draft, an article or a rough note into a LinkedIn post that reads well, then schedule or publish it through WoopSocial. Writing is half the job here, so take it seriously.

The user's explicit instructions take priority over these guidelines, except that you never post, delete or change posts beyond what the user asked for.

## If WoopSocial isn't connected

If no WoopSocial tools are available, say the WoopSocial connector isn't set up. The user can create an account at https://app.woopsocial.com/signup?utm_source=claude-plugin&utm_medium=skill&utm_campaign=woop-plugin-v1&utm_content=linkedin-posts and connect WoopSocial from the plugin's Connectors tab (in Claude Code, run `/mcp`), then retry. You can still write the post now, so offer that. Never pretend to post.

## 1. Profile or company page?

LinkedIn has two separate targets in WoopSocial, each its own connection:

- **Personal profile** (`LINKEDIN`): the user's own name and face. First person, opinions, lessons, stories.
- **Company page** (`LINKEDIN_PAGES`): the business. News, launches, hiring, customer stories, useful how-tos.

If the user didn't say which, ask. If they want both, write two versions, because a profile post and a page post should not read the same. Post them as one post with a contentOverride per target, or as two posts. Either way show both and get a yes.

## 2. Work out the post

Ask only for what's missing:

| What | Options |
|---|---|
| Topic or source | The idea, a draft, a link, notes, a transcript |
| Goal | Start a conversation, share a lesson, announce something, drive clicks |
| Link | A URL to share, or none |
| Media | One image or a video (local file or already in WoopSocial), or text only |
| When | Now, a date and time, or save as draft |

Don't promise PDF or document carousels. WoopSocial posts text, images and video to LinkedIn. If the user wants a document post, say it isn't supported here and offer an image or a text version instead.

## 3. Write it for LinkedIn

Skip this if the user gave final text and said to post it as is.

- **The first two lines must earn "see more".** Only about the first two or three lines show in the feed. Lead with the tension, the result, the surprising fact or the strong opinion. No warm-up, no "I'm excited to announce".
- **Short lines with white space.** One to two sentences per paragraph, a blank line between them. Easy to read on a phone.
- **One idea per post.** If there are three ideas, that's three posts. Offer to queue the others.
- **Be concrete.** Real numbers, names, steps and examples the user gave you. Never invent results, clients, quotes or figures. Ask, or leave a `[number]` placeholder and point it out.
- **End with a genuine question or a clear takeaway.** A question someone could actually answer from experience ("How do you handle X?"), or one line that sums up the lesson.
- **No engagement bait.** No "comment YES", "agree?", "like if", tag-a-friend asks, or fake cliffhangers.
- **No broetry.** Don't break every sentence onto its own line for drama. Normal paragraphs, kept short.
- **Hashtags:** 0 to 3, specific, at the end. None is fine.
- **Length:** LinkedIn allows up to 3,000 characters. Most good posts use far less. Count before validating.
- **Voice:** match the user's past posts if they shared some. Profile posts sound like a person. Page posts sound like the company, still human.

Show the draft and let the user edit before moving on.

## 4. Links

LinkedIn targets have a `link` field that publishes the URL as a link preview card. Links in a post can reduce reach on LinkedIn, so tell the user in one line and let them choose:

- **Link field:** set `link` on the target. Clean preview card under the post.
- **Link in the text:** paste the URL into the body.
- **No link:** keep the post native and mention where to find it ("search X", "on our site").

WoopSocial can't post a first comment, so "link in the first comment" has to be done by hand in LinkedIn after the post goes live. Say so if the user asks for it.

## 5. Find the account

Call projects_list (ask by name if there are several), then social_accounts_list. Pick the CONNECTED account on the platform chosen in step 1 (`LINKEDIN` or `LINKEDIN_PAGES`). Show it by name, never by ID. If it's missing or DISCONNECTED, offer to connect it now with oauth_create_authorization (projectId plus that platform). Give the user the link, tell them to pick the right page if the sign-in asks, wait for "done", then confirm with social_accounts_list.

## 6. Upload media (if any)

For each local image or video:

1. Get the file size. Call media_uploads_create_session with projectId and fileSizeInBytes (max 5 GB).
2. Split the file into `partCount` parts. Every part except the last must be exactly `partSizeInBytes`. PUT each part's raw bytes to its `uploadUrl` (curl or a short script).
3. Call media_uploads_complete_session and keep the returned media id.

Files already in WoopSocial: find them with media_list. If uploads are blocked by the network, ask the user to allow `*.r2.cloudflarestorage.com` (claude.ai or Claude Desktop: Settings > Capabilities > Create and edit files, turn on "Use the internet while making files" and add it under Allowed websites > Manage; Claude Code: the sandbox's allowed network domains). If you can't make HTTP requests at all, say so plainly. Offer to post it as text only (with the `link` field if there is one), or the user uploads the media in the WoopSocial app.

## 7. Validate, confirm, schedule

1. Build the payload: one content item with the text and any media, `schedule` (DRAFT, PUBLISH_NOW, or SCHEDULE_FOR_LATER with `scheduledFor` in UTC), and the target `{platform: LINKEDIN or LINKEDIN_PAGES, socialAccountId}` plus `link` if the user chose the link field. Add `retryPolicy: {maxRetries: 2, delaySeconds: 300}` unless the user doesn't want retries.
2. Call posts_validate. It returns `isValid` and a list of `errors` (each with a `path` and a `message`); treat `isValid: false` as a failure even though the call succeeded. If an error names a field you don't recognize, schema_describe shows the tool's full input schema. Fix what it flags and validate again. Ask before changing anything the user wrote.
3. **Ask first, or go?** If the user gave the final text and media, the account and the time, and you changed none of it, their request is the go-ahead: skip to step 4 without asking again. Show the summary below and wait for a yes when you wrote or changed any of the text, media or settings, when it's more than one post, or when the account, time or publish-versus-draft is unclear:
   - Account (profile or page, by name) and time in the user's time zone
   - Full post text, exactly as it will appear
   - Link handling and media
4. Call posts_create with the same payload.

If the time zone isn't clear, ask once. A time in the past isn't allowed, so ask for a new one. "Tuesday 8am" means the user's local time: convert to UTC.

## 8. Report back

- Scheduled: confirm the time and that it can be cancelled any time before it goes out.
- Published now: delivery often takes a minute or two, longer for video. Check social_account_posts_list for this post, and if it's still NOT_STARTED or SENDING, say it's on its way and check once more. If it's still not done, tell the user it's in progress and that they can ask you to check again later. When deliveryStatus is PUBLISHED, share externalPostUrl. If FAILED, explain errorMessage in plain words and offer to fix and re-send.

## Good to know

- A week of LinkedIn posts: write them all, show the list with dates, get one yes for the whole list, then create them one at a time. For a big batch from a sheet, bulk-schedule-posts fits better.
- The same post on X, Threads and others too: suggest cross-post-everywhere.
- A scheduled post can't be edited in place. To change it, show the new version, get a yes, create it, then delete the old one.
- On a 429 (too many requests), wait briefly and retry one call at a time.
- Results for posts sent through WoopSocial show up about a day later. Company pages also get an engagement rate. social-media-report covers that.
