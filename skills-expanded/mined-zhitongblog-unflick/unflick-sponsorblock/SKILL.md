---
name: unflick-sponsorblock
description: >-
  Inspect SponsorBlock skip segments for a YouTube video with the unflick player
  — find sponsor reads, intros, self-promos, and other community-marked segments,
  and report or skip past them. Use when the user asks "where are the ads/sponsors
  in this video", to skip sponsor segments, or about SponsorBlock. Requires the
  unflick MCP server (or CLI).
license: MIT
---

# unflick: SponsorBlock segments

unflick auto-skips YouTube sponsor segments during playback via SponsorBlock.
The `sponsor_segments` tool lets you inspect those segments programmatically.

## Tool

`sponsor_segments(url)` — `url` is any YouTube form (watch / shorts / youtu.be /
embed). Returns the configured categories plus a list of segments:
`{start, end, category, action_type, uuid}` (seconds). An **empty list** means
none are marked (HTTP 404 upstream). It errors only on network/parse failure or
a non-YouTube URL.

## Flows

- **"Where are the sponsors in this video?"** → `sponsor_segments(url=…)` →
  summarize each as `category mm:ss–mm:ss` (e.g. `sponsor 1:12–2:05`).
- **"Play it and skip the sponsors"** → `play(file=url)` (auto-skip already
  happens during playback); use `sponsor_segments` to *tell the user* what will
  be skipped, or to manually `seek()` past a segment if auto-skip is off.
- **"How much ad time?"** → sum `(end - start)` across `category == "sponsor"`.

## Guidance

- Categories include `sponsor`, `selfpromo`, `intro`, `outro`, `interaction`,
  `music_offtopic`, etc. — name them plainly for the user.
- Empty list is a normal result (no data), not an error — say "none marked".
- Only works for YouTube URLs; for other sites, say so rather than guessing.
