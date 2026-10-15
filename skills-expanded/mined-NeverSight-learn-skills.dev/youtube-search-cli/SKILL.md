---
name: youtube-search-cli
description: Use the local YouTube Search CLI standalone binary to search YouTube videos and playlists, list videos from a playlist, or fetch video metadata through YouTube Data API v3 with JSON output. Trigger for API-based YouTube discovery and metadata tasks, especially from automation, CI, headless systems, or cloud networks where scraping tools such as yt-dlp are blocked or unreliable.
---

# YouTube Search CLI

Use the `youtube-search-cli` binary for structured YouTube search and metadata retrieval through YouTube Data API v3.

## Requirements

- Treat this as a standalone binary tool, not a library or source package.
- Expect `youtube-search-cli` or `youtube-search-cli.exe` to be available on `PATH`, unless the user provides an explicit executable path.
- Never ask the user to paste the API key into the prompt or include it in a command.
- Expect successful commands to emit indented JSON on stdout.
- Pass a playlist ID or video ID to ID-based commands, not a YouTube URL.

## Arguments

```bash
youtube-search-cli <SUBCOMMAND> [OPTIONS] [QUERY_OR_ID]
```

Place named options before the positional query or ID.

### Search

```bash
youtube-search-cli search [--filter video|playlist|channel|mixed] [--max-results N] [--next-page-token TOKEN] "QUERY"
```

- `QUERY`: Required search text. Quote it when it contains spaces.
- `--filter`: Optional result type. Accept `video`, `playlist`, `channel` or `mixed` (video and playlist); default `mixed`.
- `--max-results`: Optional results per page from 1 to 50; default 10.
- `--next-page-token`: Optional token from a previous response for the next result page.
- `--compact`: Optional flag to output deindented and stripped JSON in single line with only including necessary fields for each result, excluding thumbnails.


Examples:

```bash
youtube-search-cli search "Never Gonna Give You Up"
youtube-search-cli search --filter video --max-results 25 "TypeScript tutorials"
youtube-search-cli search --max-results 50 --next-page-token TOKEN "travel vlogs"
youtube-search-cli search --filter channel --max-results 5 "News"
```

This endpoint returns a `youtube#searchListResponse` kind, with `id` and `snippet` parts.

Performing this operation costs 100 units.

### Playlist

```bash
youtube-search-cli playlist [--max-results N] [--next-page-token TOKEN] PLAYLIST_ID
```

- `PLAYLIST_ID`: Required playlist ID.
- `--max-results`: Optional results per page from 1 to 50; default 10.
- `--next-page-token`: Optional token from a previous response for the next playlist page.
- `--compact`: Optional flag to output deindented and stripped JSON in single line with only including necessary fields for each result, excluding thumbnails.

Example:

```bash
youtube-search-cli playlist --max-results 50 PLxxxxxxxxxxxxxxxx
```

This endpoint returns a `youtube#playlistListResponse` kind, with `id`, `snippet`, and `contentDetails` parts.

Performing this operation costs 1 unit.


### Channel

```bash
youtube-search-cli channel [--query-type id|username|handle] [--max-results N] [--next-page-token TOKEN] QUERY_CHANNEL_NAME_OR_ID
```

- `QUERY_CHANNEL_NAME_OR_ID`: Required channel ID, legacy username, or handle.
- `--query-type`: Optional query type; default `handle`. Accepts `id`, `username`, or `handle`.
- `--max-results`: Optional results per page from 1 to 50; default 10.
- `--next-page-token`: Optional token from a previous response for the next playlist page.
- `--compact`: Optional flag to output deindented and stripped JSON in single line with only including necessary fields for each result, excluding thumbnails.

If the `--query-type` parameter isn't specified, it uses `handle` by default and the query can start with or without `@` and must be used if the user provides a username or handle if the user provides a channel URL or username.

The `id` query type should be preferrably used after using the `search` and `playlist` subcommand as its responses provides the list of videos with its associated channel name and ID. 

The `username` should only be used if the user is sure that the channel is still using the legacy username system, otherwise, it should be avoided as Google rolled out the username with handle system in 2022 for all channels, using `handle` is much more preferred if possible and use this as a fallback.

This endpoint returns a `youtube#playlistListResponse` kind, with `id`, `snippet`, and `contentDetails` parts, as it calls playlist endpoint to list videos from the channel.

Performing this operation costs 2 units - one for the channel query and one for the playlist query which lists videos from the queried channel, pagination with `--next-page-token` will cost the same 2 units.

### Video

```bash
youtube-search-cli video VIDEO_ID
```

- `VIDEO_ID`: Required YouTube video ID.
- This subcommand has no data options.

Example:

```bash
youtube-search-cli video dQw4w9WgXcQ
```

This endpoint returns a `youtube#videoListResponse` kind, with `id`, `snippet`, and `contentDetails` parts.  

Performing this operation costs 1 units.

### Utility arguments

- `--help` or `-h`: Show top-level help.
- `--version` or `-v`: Print the binary version.
- `<subcommand> --help`: Show subcommand help.

## Cost recommendations

Assume the standard YouTube Data API allocation is 10,000 quota units per project per day unless the user states otherwise.

- Treat each `search` request as 100 units. This permits about 100 search requests if no other operations consume quota.
- Treat each `playlist`, `channel` or `video` request as 1 unit. Prefer these commands when an ID is already known.
- Try `yt-dlp` or web search first for discovery when they work in the current environment. Use this binary when API reliability, structured results, cloud-network access, or YouTube Terms of Service compliance matters.
- Start discovery with `--filter mixed` so one 100-unit request can expose both videos, associated channel, and useful playlists. See Combinations section below for ways to stretch the 10,000-unit daily quota.
- Follow relevant playlists with the 1-unit `playlist` command before buying more 100-unit search pages.
- Choose `--max-results` deliberately. A larger page does not increase the quota cost of that request and can reduce follow-up calls. If using `--compact`, use max results value higher than its defaults (10) to stretch the quota.
- Treat every `--next-page-token` use as a new API request: another 100 units for `search`, another 1 unit for `playlist`, or 2 units for `channel`.
- Always use `--compact` for `search`, `playlist`, and `channel` operations which reduces the JSON size and context usage. This only excludes thumbnails and other unnecessary fields, and returns in unindented JSON. 
- If deciding not to use `--compact` due to either user request or in rare cases may not be able to properly obtain necessary results due to errors, save large JSON responses to a file and inspect only relevant fields with tools such as `jq` or `rg`/`grep` instead of loading the entire JSON response into context.

### Combinations

To make the most of the 10,000-unit daily quota and to stretch it while discovering videos from various playlists or channels, consider these combinations:

- Run two calls with `search --filter mixed` and `search --filter playlist` if there's a relevant playlist and is worth looking for, this search combination costs 200 units. Followed by further `playlist` calls for each relevant playlist found and paginate as needed which costs additional 1 or more units per playlist list.
- Run `search --filter mixed` and then `channel --query-type id [ID]` if the associated search results from videos have channel name and its ID that is worth looking for to discover possible relevant videos, this combination costs 100 units for search and 2 units for channel video listing as described above. This is much more cheaper than the playlist workflow.

Keep in mind that this depends on the results shown so these combinations are not guaranteed to be the most efficient for every search query, but they are a good starting point for cost optimization.

## Workflow

1. Determine whether the task needs discovery, playlist enumeration, or known-video metadata.
2. Confirm that the binary is available and that `YOUTUBE_DATA_API_KEY` is configured without exposing its value.
3. Select the lowest-cost subcommand that can answer the task.
4. Run the command with named arguments before the positional query or ID.
5. Parse the JSON response and report only the relevant results when necessary. Preserve `nextPageToken` when another page may be needed.
6. Stop paging once the task is answered; do not spend quota collecting unused results.

## Failure handling

- If `YOUTUBE_DATA_API_KEY` is missing after running the executables first-pass, ask the user to set the environment variable first before continuing, and discourage putting the API key within the current agent context. The user can also set an environment variable to a file, refer the user to this documentation: https://github.com/zavocc/youtube-cli#usage-and-installation. In addition, do not set or source any environment variable yourself and you must halt first and explicitly ask the user to set it up first before continuing or perform alternatives.
- If the binary is missing from `PATH`, ask for its executable path or direct the user to install the release binary.
- If given a YouTube URL for `video`, extract its video ID. If given a playlist URL for `playlist`, extract its `list` parameter. If given a channel URL that has a username or handle in the URL, extract the username or handle.
- If the API reports quota exhaustion, stop retrying and explain which operation consumed quota. Suggest waiting for quota reset or using a non-API discovery method.
- If the API rejects `--max-results`, keep it between 1 and 50.
- If the command returns malformed or mixed output, preserve stderr separately and parse stdout as JSON.
