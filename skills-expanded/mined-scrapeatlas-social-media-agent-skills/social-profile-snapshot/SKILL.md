---
name: social-profile-snapshot
description: "Build a snapshot of one person's or brand's public social accounts with ScrapeAtlas: retrieve the profile and one page of recent posts on each requested platform, then summarize audience size, bio and links, posting frequency and the best-performing recent posts. Use when the user asks for a profile overview, account audit, creator snapshot or 'what is @handle posting' across TikTok, Instagram, YouTube, X, Threads, Bluesky, LinkedIn, Facebook, Pinterest or Reddit."
---

# Social profile snapshot

Retrieve public profile data and recent posts for one handle or brand and summarize
them per platform. Follow the `scrapeatlas` skill for connecting, reading status
and coverage, pagination and credits.

## Prompt

> Use ScrapeAtlas to build a snapshot of the public accounts for [HANDLE OR BRAND] on [PLATFORMS, for example TikTok, Instagram, YouTube and X]. For each platform, retrieve the profile and one page of recent posts. Summarize follower count, bio and links, how often they post and their best-performing recent posts with URLs and engagement counts. Use only numbers the API returned. Report each call's status and coverage, list any platform that failed with its failure code, and tell me how many credits were used. Do not fetch more pages unless I ask.

## Inputs

- The handle or brand, and the platforms to check. If the user gives one handle
  for several platforms, confirm that it is the same account on each, or ask for
  the per-platform handles or URLs.
- If no platforms are given, ask, or propose TikTok, Instagram, YouTube and X and
  state the expected cost (about 2 credits per platform).

## Tools per platform

Use one profile call and one list call per platform. Operation IDs work as MCP tool
names and with `scrapeatlas call <id>`; CLI commands are shown in brackets.

| Platform | Profile | Recent posts | Identifier |
| --- | --- | --- | --- |
| TikTok | `tiktokProfile` (`tiktok profile`) | `tiktokProfileVideos` (`tiktok profile-videos`) | `handle` |
| Instagram | `instagramProfile` (`instagram profile`) | `instagramUserPosts` (`instagram user-posts`) or `instagramUserReels` | `handle` |
| YouTube | `youtubeChannel` (`youtube channel`) | `youtubeChannelVideos` (`youtube channel-videos`) or `youtubeChannelShorts` | `handle`, `channelId` or `url` |
| X | `twitterProfile` (`twitter profile`) | `twitterUserTweets` (`twitter user-tweets`) | `handle` |
| Threads | `threadsProfile` (`threads profile`) | `threadsUserPosts` (`threads user-posts`) | `handle` |
| Bluesky | `blueskyProfile` (`bluesky profile`) | `blueskyPosts` (`bluesky posts`) | `handle` (domain form, no @) |
| LinkedIn | `linkedinProfile` (`linkedin profile`) or `linkedinCompany` | `linkedinCompanyPosts` for companies; a person's profile includes recent posts | `url` |
| Facebook | `facebookProfile` (`facebook profile`) | `facebookProfilePosts` (`facebook profile-posts`) | `url` |
| Pinterest | `pinterestProfile` (`pinterest profile`) | `pinterestUserPins` (`pinterest user-pins`) | `handle` |
| Reddit | `redditProfile` (`reddit profile`) | `redditProfilePosts` (`reddit profile-posts`) | `handle` |

Other platforms (Twitch, Kick, Snapchat, Tumblr, Mastodon, Medium, Substack,
Telegram and more) have their own profile and post tools; discover them with
`scrapeatlas list <platform>` or the MCP tool list.

## Steps

1. Run the profile call for each platform. If it fails with `not_found`, report
   that and skip that platform's list call.
2. Run one page of the recent-posts call. Use the default sort (newest first).
3. From the returned records, compute only what the data supports: posts in the
   page, the date range they span, average and top engagement (views, likes,
   comments, shares as available). Name the fields you used.
4. Pick the top 3 posts per platform by the best available engagement metric and
   include their URLs.

## Output

- One short section per platform: followers, bio, links, verification, posts per
  week across the returned page, top posts with URLs and counts.
- A cross-platform line: where the account is largest and most active.
- A coverage line: calls made, status of each (`success`, `partial` or the failure
  code), pages covered and credits charged.

Do not compare platforms on metrics that only some return, and do not describe one
page of posts as the account's full history.
