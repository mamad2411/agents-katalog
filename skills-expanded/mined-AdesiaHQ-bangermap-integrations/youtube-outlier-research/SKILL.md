---
name: youtube-outlier-research
description: Find which YouTube videos overperformed their own channel, and read the result correctly. Use when asked which of a channel's uploads did unusually well, whether a specific video is an outlier, what a channel's normal view count is, what is working in a niche, or what content idea to make next based on what already worked. Runs on the user's own free YouTube Data API key.
---

# YouTube outlier research

A video's view count says more about the channel it sits on than about the video. 500,000 views is unremarkable on a channel that always gets a million, and 60,000 views is a discovery on a channel that usually gets 4,000. The second is evidence that an idea worked without an audience carrying it, which is the only evidence worth copying.

So the unit of analysis is the multiple, meaning a video's views divided by its own channel's baseline. Report multiples. Never rank videos from different channels by raw views.

## The measurement

**Baseline.** The median views of the channel's 30 most recent settled uploads of the same format. Median rather than mean, because one runaway hit drags a mean upward and makes every other upload look like a failure against it.

**Settled** means published at least 7 days ago. Younger uploads are still accumulating views, so including them drags the baseline down and understates every multiple.

**Format** splits at 180 seconds. Shorts and long-form get separate baselines and are never compared to each other, since a 40-second video judged against 20-minute numbers is flattered or punished by nothing but its length.

**Typical range** is the 25th to 75th percentile of the same pool. A video inside that range is the channel doing what it always does, whatever its raw views.

**Not enough data.** Fewer than 5 settled uploads in a format means no baseline for that format. Say so rather than computing one from three videos.

## Reading a result

- Below 1x is under the channel's own normal, whatever the view count looks like.
- 3x is the common bar for calling something an outlier.
- 10x and above reshapes a niche, and is rare enough to be worth checking for a cause, a collaboration, an external link, or a video that got picked up somewhere.

Two things change the reading and are the most common analysis errors.

**Age.** A 12x from two years ago has already been absorbed, every serious competitor made their version. A 12x from last month is still open. Always report how old an outlier is next to its multiple.

**One channel is an anecdote.** One outlier can be luck, a thumbnail, a good day. The same idea overperforming on three channels in a niche within a month is a pattern, and that is the point at which it is worth acting on. When the user wants to know what to make next, compare across channels before recommending anything.

A video under 7 days old can be scored, but say that it is still climbing and its multiple will move.

## Running it

The measurement is implemented in the `bangermap-mcp` MCP server, which runs locally over stdio on the user's own free YouTube Data API key. Nothing is metered and no data leaves their machine except the API call to Google.

Add it to the MCP client config, with the key in `YOUTUBE_API_KEY`:

```json
{
  "mcpServers": {
    "bangermap": {
      "command": "npx",
      "args": ["-y", "bangermap-mcp"],
      "env": { "YOUTUBE_API_KEY": "the user's key" }
    }
  }
}
```

Four tools, each taking a channel URL, an @handle, a channel id, or the URL of any video on the channel.

- `find_outliers` ranks one channel's recent uploads by multiple. About 5 quota units.
- `channel_baseline` reports what normal looks like for a channel, with subscriber count and cadence. Use it before judging whether a view count is good. About 5 units.
- `compare_channels` scans several channels and merges the results, each scored against its own baseline. About 5 units per channel.
- `sweep_niche` expands from a seed channel through the channels it features, then ranks across all of them. Use it when the user wants channels they do not already know. About 5 units per channel found.

If the server is not available, the same measurement runs free in a browser at https://bangermap.com/tools, one channel at a time and no signup.

## Quota

A Google account gets 10,000 free Data API units a day, which is roughly 1,100 channel scans. Keyword search costs 100 units a call, so it is capped near 100 searches a day and is a burst tool. Seeding from a channel and expanding through the channel graph is the cheap path and is what `sweep_niche` does.

If a call fails on quota, say so plainly and give the reset time, which is midnight Pacific. Do not retry in a loop.

## Reporting

Lead with the multiple, then views, then age, then the title. Group by channel when several are in play, since each channel's baseline is different and a merged list without channel names cannot be checked. State the baseline you measured against, per format, so the arithmetic can be verified.

The multiple and the baseline are computed by this method, not by YouTube. View counts come from the YouTube Data API. Say so when presenting results anywhere they might be mistaken for platform figures.
