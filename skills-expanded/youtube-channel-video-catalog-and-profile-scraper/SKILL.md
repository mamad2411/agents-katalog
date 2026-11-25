---
name: youtube-channel-video-catalog-and-profile-scraper
description: "Get a YouTube channel's profile details (subscribers, description, links, verification) together with its video, Shorts, playlist or live-stream catalog, for one channel or many at once. Output fields: title, viewCount, duration, publishedTimeText, url and more, as JSON rows. Use it for requests like \"YouTube channel video catalog scraper\", or a CSV/JSON export of public YouTube data."
---

# YouTube Channel Video Catalog & Profile Scraper

Get a YouTube channel's profile details (subscribers, description, links, verification) together with its video, Shorts, playlist or live-stream catalog, for one channel or many at once.

- Actor: https://apify.com/vexaloom-labs/youtube-channel-video-catalog-and-profile-scraper (ID `vexaloom-labs~youtube-channel-video-catalog-and-profile-scraper`)
- n8n workflow for the same Actor: https://github.com/bolvein-firex/scraping-n8n-workflows/blob/main/docs/youtube-channel-video-catalog-and-profile-scraper.md
- Example input: `references/example-input.json`
- Input schema: `references/input-schema.json`
- Output fields: `references/output-fields.json`

## When to use

Use this skill when the user wants:

- YouTube channel video catalog scraper
- a repeatable export of public YouTube data as CSV or JSON

Do not use it for private, login-protected or paywalled data.

## What it returns

One JSON row per result. Columns from the Actor's dataset schema:

- `title`: Title
- `videoId`: Video ID
- `viewCount`: Views
- `duration`: Duration
- `publishedTimeText`: Published
- `url`: URL
- `authorMetadata.channelName`: Channel
- `authorMetadata.subscriberCount`: Subscribers

All 49 declared fields: `references/output-fields.json`.

## Inputs

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `channelUrls` | array | yes |  | YouTube channel URLs, handles (@username), or channel IDs (UCxxx). Accepts any format. |
| `maxVideos` | integer | no | 50 | Maximum number of videos to scrape per channel. Set to 0 to get only channel info without videos. |
| `sortVideosBy` | string | no | newest | How to sort the channel's video listings. If YouTube does not offer the chosen sort for a channel, newest-first is used. |
| `sortShortsBy` | string | no | newest | How to sort the channel's Shorts listing (when includeShorts is enabled). Falls back to newest-first when the channel offers no Shorts sort. |
| `includeAbout` | boolean | no | true | Extract total views, join date, location, country, and external links from the channel About page. |
| `includeShorts` | boolean | no | false | Scrape the channel Shorts tab and include Shorts in the output. |
| `maxShorts` | integer | no | 20 | Maximum number of Shorts to return (when includeShorts is enabled). |
| `includeLiveVideos` | boolean | no | false | Scrape the channel Live/Streams tab and include live, upcoming, and past streams. |
| `maxLiveVideos` | integer | no | 20 | Maximum live/stream videos to return (when includeLiveVideos is enabled). |
| `includePlaylists` | boolean | no | false | Scrape the channel Playlists tab and include playlist metadata in the output. |
| `maxPlaylists` | integer | no | 20 | Maximum number of playlists to scrape (when includePlaylists is enabled). |
| `includePodcasts` | boolean | no | false | Scrape the channel Podcasts tab and include podcast shows (when the channel has one). |
| `maxPodcasts` | integer | no | 50 | Maximum number of podcast shows to return (when includePodcasts is enabled). |
| `includeCourses` | boolean | no | false | Scrape the channel Courses tab and include course playlists (when the channel has one). |

7 more optional fields on the Actor's Input tab.

Example (`references/example-input.json`):

```json
{
  "channelUrls": [
    "https://www.youtube.com/@Apify"
  ],
  "maxVideos": 25
}
```

The input passes the Actor's input schema (checked at every publish). First run: `maxVideos` = 25, small enough for the 300-second sync wait; raise it once the rows look right.

## Run it

Set `APIFY_TOKEN`, then call the synchronous endpoint for small and medium runs (it waits up to 300 seconds):

```bash
curl -s -X POST "https://api.apify.com/v2/acts/vexaloom-labs~youtube-channel-video-catalog-and-profile-scraper/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d @references/example-input.json > output.json
```

Or with Node 18+: `node scripts/run.mjs [input.json]`.

For large runs, start an async run and read its dataset when it finishes:

```bash
RUN=$(curl -s -X POST "https://api.apify.com/v2/acts/vexaloom-labs~youtube-channel-video-catalog-and-profile-scraper/runs" \
  -H "Authorization: Bearer $APIFY_TOKEN" -H "Content-Type: application/json" \
  -d @references/example-input.json)
RUN_ID=$(echo "$RUN" | jq -r '.data.id'); DATASET=$(echo "$RUN" | jq -r '.data.defaultDatasetId')
curl -s "https://api.apify.com/v2/actor-runs/$RUN_ID?waitForFinish=60" -H "Authorization: Bearer $APIFY_TOKEN" | jq -r '.data.status'
curl -s "https://api.apify.com/v2/datasets/$DATASET/items?format=json" -H "Authorization: Bearer $APIFY_TOKEN" > output.json
```

## Cost and limits

- Apify bills the Actor's usage on your account; the Actor's Pricing tab shows the current price.
- Keep the limit in the input small for a first run.

## Guardrails

- Public data only. Do not pass cookies, sessions or private account data.
- Do not use the output for spam, harassment or unlawful discrimination.
- Check the target site's terms and local law before running at scale.
