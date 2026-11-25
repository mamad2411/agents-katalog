---
name: trend-scan
description: "Scan a keyword or hashtag across platforms with ScrapeAtlas search and hashtag tools: retrieve one page of matching posts per platform, then summarize top posts, recurring angles and formats, and the accounts posting most. Use when the user asks what people are posting about a topic, how a hashtag is performing, trend research, social listening or topic discovery on TikTok, YouTube, Reddit, Threads, LinkedIn, Pinterest, Facebook, Tumblr or Mastodon."
---

# Trend scan

Search one keyword or hashtag on the platforms that support it and summarize what
is getting attention. Follow the `scrapeatlas` skill for connecting, reading status
and coverage, pagination and credits.

## Prompt

> Use ScrapeAtlas to scan [KEYWORD OR #HASHTAG] across [PLATFORMS, for example TikTok, YouTube, Reddit and Threads] for the last [TIME WINDOW, for example 7 days]. Use each platform's search or hashtag tool with its date filter where it has one, one page per platform. Summarize the top posts with URLs and engagement counts, the angles and formats that repeat, and the accounts that appear most. Tell me which requested platforms have no search tool, report each call's status and coverage with any failure codes, and tell me how many credits were used. Ask before fetching more pages.

## Inputs

- A keyword, phrase or hashtag, and the platforms to search. If none are given,
  propose TikTok, YouTube, Reddit and Threads and state the cost (about 1 credit
  per platform per page; LinkedIn search costs 2).
- Optional time window and region.

## Tools per platform

| Platform | Keyword search (CLI command) | Hashtag | Time filter |
| --- | --- | --- | --- |
| TikTok | `tiktokSearchKeyword` (`tiktok search-keyword`), `tiktokSearchTop` | `tiktokSearchHashtag` (`tiktok search-hashtag`) | `publish_time`, `sort_by`, `since`/`until` |
| YouTube | `youtubeSearch` (`youtube search`) | `youtubeSearchHashtag` (`youtube search-hashtag`) | `uploadDate`, `sortBy=popular`, `since`/`until` |
| Reddit | `redditGlobalSearch` (`reddit global-search`), `redditSubredditSearch` | none | `timeframe`, `sort`, `since`/`until` |
| Threads | `threadsSearch` (`threads search`) | `threadsSearchTags` finds tags | `recent`, `since`/`until` |
| LinkedIn | `linkedinSearchPosts` (`linkedin search-posts`), 2 credits | none | `date_posted` or `since`/`until` |
| Pinterest | `pinterestSearch` (`pinterest search`) | none | `since`/`until` |
| Facebook | none | `facebookHashtag` (`facebook hashtag`) | none |
| Tumblr | `tumblrSearch` (`tumblr search`) | `tumblrTag` (`tumblr tag`) | `sort=recent` |
| Mastodon | none for posts; `mastodonSearch` finds accounts and hashtags | `mastodonHashtag` (`mastodon hashtag`), with 7-day usage | `since`/`until` on the hashtag tool |

Also available: `tiktokTrending`, `youtubeTrendingShorts` and `mastodonTrends`
for what is trending without a keyword; `hackernewsSearch`, `mediumSearch`,
`substackSearch`, `quoraSearch` (2 credits) and `producthuntSearch` for topic
research outside social video.

Instagram, X and Bluesky have no keyword or hashtag search tool in ScrapeAtlas.
If the user asks for them, say so; do not replace them silently.

## Steps

1. Normalise the input: strip a leading `#` where a tool takes a bare hashtag
   (most accept either). Use a keyword tool for phrases and a hashtag tool for
   single tags.
2. Make one call per platform with the narrowest supported time filter. For an
   exact time window, use `since` / `until` where offered.
3. From the returned results, rank posts by the best available engagement metric
   and note the date range the page actually covers.
4. Group recurring angles, formats, sounds or titles, and count the accounts that
   appear more than once.

## Output

- Per platform: result count in the page, date range, top 3 to 5 posts with URL,
  author and metric values.
- Cross-platform themes, each with the posts that support it.
- Accounts that appear most, with platform and handle.
- A coverage line: calls made, status of each, pages covered, platforms skipped
  for lack of a search tool and credits charged.

Search results are a ranked sample chosen by each platform. Do not present result
counts as total volume or as a measure of the trend's size.
