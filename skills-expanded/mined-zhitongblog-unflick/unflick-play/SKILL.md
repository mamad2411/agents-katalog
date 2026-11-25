---
name: unflick-play
description: >-
  Open and control video playback with the unflick player — local files and
  30+ streaming-site URLs (YouTube, Bilibili, Twitch, Vimeo…). Use when the user
  asks to play, pause, resume, stop, seek, change volume or speed, check what's
  currently playing, put on a DVD or disc image, cast to a TV, or pick up where
  they left off. Requires the unflick MCP server (or CLI) installed.
license: MIT
---

# unflick: play & control video

You drive the [unflick](https://unflick.app) video player. Prefer the MCP tools
when the `unflick` MCP server is connected; otherwise shell out to the `unflick`
CLI (every tool has a 1:1 command).

## Core flow

1. **Open** — `play(file=<path-or-url>)`. `file` accepts a local path *or* a
   streaming URL (yt-dlp resolves YouTube/Bilibili/Twitch/Vimeo and 26 others).
   Optional `seek` (seconds), `volume` (0–100), `speed` (e.g. `1.5`).
2. **Control** — `pause`, `resume`, `stop`, `seek(seconds)`,
   `set_volume(level)`, `set_speed(rate)`.
3. **Inspect** — `get_status` returns `{state, file, position, duration, volume,
   speed}`. Read the `unflick://now-playing` resource for the same data when you
   just need a snapshot.

## CLI equivalents

```bash
unflick play "https://youtu.be/dQw4w9WgXcQ" --volume 80 --speed 1.25
unflick seek 120        # jump to 2:00
unflick pause
unflick status          # JSON to stdout
```

## Beyond a file path

- **Discs** — `disc_list()` reports optical drives and what is in them; `play`
  takes a `.iso`, a folder with `VIDEO_TS`, a drive path, or `dvd://3` for a
  specific title. Clipping and hover previews are refused on a disc, by design.
- **A television** — `cast(action="list")` finds DLNA renderers on the network,
  `cast(action="to", renderer=…)` sends what is playing, and pause/resume/seek/
  stop drive it from there.
- **The window** — `window_mode(mode="normal"|"pip"|"music")`. It answers "no window"
  when only the headless daemon is running, rather than pretending.
- **Getting back** — `session()` reports what was last watched and how far in;
  `session(action="restore")` reopens it. `recent_files()` is the list.
- **What is playing** — `now_playing()` gives title/artist/album and whether
  there is picture at all, which `get_status` (path, position, state) does not.

## Guidance

- To "skip ahead 30s", read `get_status.position`, then `seek(position + 30)`.
- Speed lives in `0.25`–`4.0` in practice; volume is `0`–`100`.
- If a URL fails, it's usually a missing/old `yt-dlp` — surface the error text
  rather than retrying blindly.
- Resume: before playing a file you've seen before, `get_position(path)` and
  pass it as `seek`; after stopping, `save_position(path, position)`.
