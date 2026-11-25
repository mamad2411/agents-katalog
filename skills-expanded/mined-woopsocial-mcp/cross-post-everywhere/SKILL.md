---
name: cross-post-everywhere
description: "Cross-post one piece of content to Instagram, TikTok, LinkedIn, X, Threads, Bluesky, Facebook, Pinterest and YouTube in one go through WoopSocial. Use when the user says \"post this everywhere\", \"cross-post this\", \"share this on all my accounts\", \"same post to LinkedIn and X\", \"turn this video into posts for every platform\". Writes a native version per platform, validates every account in one check so nothing is created until every version passes, shows the versions for approval, then publishes or schedules. Reddit and Mastodon are not supported."
---

# Cross-post everywhere

One piece of content, one WoopSocial post, a native version on every platform. The point is not to paste the same caption everywhere: each platform gets text written for how people read it there.

The user's explicit instructions take priority over these guidelines, except that you never post, delete or change posts beyond what the user asked for.

## If WoopSocial isn't connected

If no WoopSocial tools are available, say the WoopSocial connector isn't set up. The user can create an account at https://app.woopsocial.com/signup?utm_source=claude-plugin&utm_medium=skill&utm_campaign=woop-plugin-v1&utm_content=cross-post-everywhere and connect WoopSocial from the plugin's Connectors tab (in Claude Code, run `/mcp`), then retry. You can still write every platform version now, so offer that. Never pretend to post.

## 1. Find the accounts

Call projects_list. If there are several projects, ask which brand by name. All accounts in one post must belong to the same project, so one cross-post covers one brand or client. Then call social_accounts_list and show the CONNECTED accounts by platform and username (never IDs).

"Everywhere" means every connected account in that project, unless the user names a subset. Mention any DISCONNECTED account and offer to reconnect it with oauth_create_authorization before going on. Reddit and Mastodon aren't supported. If the user asks for them, say so in one line.

## 2. Check what each platform needs

Get the content (text, link, image, video) and check each platform against it:

| Platform | Needs | Target fields |
|---|---|---|
| Instagram | An image or video | `postType` POST (image, carousel) or REEL (vertical video); `isAiGeneratedContent` true if the content is AI-generated |
| TikTok | A video, or images for a photo post | Settings from social_accounts_get_platform_inputs (below) |
| YouTube | A video and a title | `title`, `privacy` (public, private, unlisted), optional `tags`, `madeForKids` |
| Pinterest | An image or video, a board, ideally a link | `pinterestBoardId`, `title`, `link` |
| Facebook | Text only is fine | `postType` TEXT_ONLY, IMAGE, VIDEO or REEL; optional `link` |
| LinkedIn (profile or page) | Text only is fine | optional `link` |
| X, Threads, Bluesky | Text only is fine | none |

If a platform can't take this content (text only for Instagram, an image for YouTube), say which ones drop out and why, and ask whether to continue without them or add the missing media.

- **Pinterest:** call social_accounts_get_platform_inputs for the account and let the user pick a board by name.
- **TikTok:** call social_accounts_get_platform_inputs. The user must choose privacy from `privacyLevelOptions`. Never default it. Only allow comments, duets and stitches where the flags say they're available (duets and stitches are video only). The API needs `allowComment`, `allowDuet`, `allowStitch`, `isYourBrand`, `isBrandedContent` and `autoAddMusic` as true or false. Ask whether the content is AI-generated (`isAiGeneratedContent`) and whether it promotes their own business (`isYourBrand`) or is a paid partnership (`isBrandedContent`). For a photo post, ask whether TikTok should add music (`autoAddMusic`). The video must be within `maxVideoPostDurationSec`. For more TikTok detail, tiktok-posts covers it.
- **YouTube:** ask for or write the title, and ask the privacy and whether it's made for kids (`madeForKids`).
- **Media aspect ratios:** a horizontal video can go to YouTube but may fail as a Reel or TikTok. posts_validate is the final check, so don't guess limits.

## 3. Write a native version per platform

Start from the user's core message and write each one for its platform. Never invent facts, prices or results. Ask, or leave a `[placeholder]`.

- **X:** short and punchy, one idea, aim for under 280 characters. One or no hashtag.
- **Threads:** conversational, like talking to a friend. A question works well.
- **Bluesky:** 300 characters max, plain and conversational, no hashtag stuffing. Put a link in the text if there is one.
- **LinkedIn:** professional and specific. First two lines earn "see more", short paragraphs, end on a takeaway or real question, 0 to 3 hashtags. No engagement bait.
- **Facebook:** friendly and plain, a little context, the link if there is one.
- **Instagram:** hook in the first line, value, one clear ask, 3 to 5 specific hashtags.
- **TikTok:** a hook that matches the video's first second, short, 3 to 5 hashtags.
- **YouTube:** a searchable title plus a description with the key words.
- **Pinterest:** a keyword-rich title and description of what the pin shows, plus the link.

Single post per platform: WoopSocial doesn't post X, Threads or Bluesky thread chains. If the content is long, cut it to one strong post and offer a link.

## 4. Upload media once

Upload each local file once and reuse the media id on every platform:

1. Get the file size. Call media_uploads_create_session with projectId and fileSizeInBytes (max 5 GB).
2. Split into `partCount` parts. Every part except the last is exactly `partSizeInBytes`. PUT each part's raw bytes to its `uploadUrl`.
3. Call media_uploads_complete_session and keep the media id.

Files already in WoopSocial: media_list. If uploads are blocked, ask the user to allow `*.r2.cloudflarestorage.com` (claude.ai or Claude Desktop: Settings > Capabilities > Create and edit files, turn on "Use the internet while making files" and add it under Allowed websites > Manage; Claude Code: the sandbox's allowed network domains). If you can't make HTTP requests at all, say so. Offer to cross-post text only to X, Threads, Bluesky, LinkedIn and Facebook, or the user uploads the media in the WoopSocial app.

## 5. Build one post with overrides

One posts_create call for all platforms:

- `content`: one item with the base text and media.
- `socialAccounts`: one target per account, with its platform fields. Give each target a `contentOverride` (same one-item shape: text plus media) holding that platform's own version. Use the override for media too, for example a different image on Pinterest, or no media on X.
- `schedule`: DRAFT, PUBLISH_NOW, or SCHEDULE_FOR_LATER with `scheduledFor` in UTC. Ask the time zone once if unclear. Past times aren't allowed.
- `retryPolicy: {maxRetries: 2, delaySeconds: 300}` unless the user doesn't want retries.

## 6. Validate together

Call posts_validate with the full payload. It returns `isValid` and a list of `errors` (each with a `path` and a `message`); treat `isValid: false` as a failure even though the call succeeded. If an error names a field you don't recognize, schema_describe shows the tool's full input schema. Validation is atomic: if one platform fails, nothing is created. For each error, say which platform and why in plain words. Fix it (shorten text, swap media, add a title) and validate again. If a platform can't be fixed, ask the user before dropping it. Never drop one silently.

## 7. Preview and confirm

Show a preview table, one row per account:

| Platform | Account | Text (full) | Media | Settings |
|---|---|---|---|---|

Settings include post type, link, board, title, privacy and TikTok labels. Add the time in the user's time zone. Ask for a yes, because you wrote the per-platform versions and the user hasn't seen them yet. Skip the question only if the user supplied the exact text for every platform, the accounts, the time and every required setting, and you changed none of it. A yes covers exactly what was shown. On yes, call posts_create with the validated payload. On a 429, wait briefly and retry once.

## 8. Report back

Per platform: scheduled (with time) or published. For PUBLISH_NOW, check social_account_posts_list for this post and list each externalPostUrl once PUBLISHED. If one platform FAILED while others went out, explain its errorMessage in plain words and offer to re-send just that one. fix-failed-posts can help with that.

## Good to know

- A scheduled cross-post can't be edited in place. To change one platform, show the new version, get a yes, create it as a new post, then delete the old platform copy with social_account_posts_delete. If that delete is refused, delete the whole post with posts_delete and recreate the rest.
- Several pieces of content across all platforms over weeks: bulk-schedule-posts fits better.
