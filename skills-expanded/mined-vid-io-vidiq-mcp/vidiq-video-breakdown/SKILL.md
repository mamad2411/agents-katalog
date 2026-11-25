---
name: vidiq-video-breakdown
description: Analyze any public YouTube video from a URL or ID, covering view history and velocity, title and thumbnail changes, transcript hooks and structure, comment themes, similar videos, and estimated earnings. Use when asked 'analyze this video', 'why did this video go viral', 'break down this competitor's video', 'summarize this YouTube video', or 'how much did this video earn'. No channel authorization needed.
---

# vidIQ Video Breakdown

Read [Live surface notes](references/live-surface-notes.md) first, even when using only supplied evidence.

Explain how a public YouTube video performed and why, from its own evidence. Any video qualifies;
private analytics are neither required nor assumed.

## Identify the video

1. Resolve the video ID from the supplied URL or ID. Fetch title, channel, publication date, duration,
   format, and current stats with `vidiq_get_videos_by_ids`. Without a resolvable video, stop and ask.
2. Use a bounded evidence plan: start with one call per lane below and add calls only when a finding
   could change the conclusion.

## Gather the lanes

- **Performance:** `vidiq_video_stats` with a required `granularity` matching the video's age
  (`hourly` for recent uploads, `daily` or `monthly` otherwise) and explicit ISO `from`/`to`
  bounds. Read historical `vph` for acceleration or decay; cumulative views are not velocity.
  Compare against the channel's typical results with `vidiq_channel_videos` (`popular: false`,
  matching `videoFormat`) as a sample, never as the full catalog. `vidiq_channel_stats` with the
  `channelId` and an optional `from`/`to` window adds subscriber, view, and video-count growth for
  size context.
- **Packaging history:** `vidiq_video_change_history` accepts a video ID or a watch, youtu.be,
  Shorts, or live URL and returns observed title and thumbnail `changes`, with archived snapshots,
  plus thumbnail `abTests`. Align them with the stats timeline; an empty history means no change
  was observed, not that none happened.
- **Content:** `vidiq_video_transcript` returns untimed `transcription`; use it for the hook,
  promise, structure, and payoff. Read [Discovery evidence](references/discovery-evidence.md) before
  claiming a pattern from the transcript or from similar videos.
- **Audience response:** sample `vidiq_video_comments` with explicit `order` and singular
  `maxResult`. Summarize themes with paraphrases; never reproduce usernames or full comments. Hand a
  deeper language bank to `vidiq-comment-insights`.
- **Independent executions:** `vidiq_similar_videos` with the live `matchOn` and
  `excludeSeedChannel: true` shows whether the premise works for other channels; inspect
  `signalsUsed`, `signalsFailed`, and `matchedBy` first.
- **Packaging quality:** `vidiq_score_title` with confirmed `type` and `vidiq_score_thumbnail` with
  the real `videoId`, current `title`, and thumbnail `image` give directional scores, not verdicts.
- **Earnings:** when asked what the video earned, `vidiq_video_earnings_estimate` with the
  `videoId` gives a low, mid, and high USD range from vidIQ's RPM model; label it an estimate that
  assumes a monetized channel and ad-serving views. For "what would X views earn" scenarios use
  `vidiq_earnings_calculate` with `subject`, `monthlyViews`, `category`, and `format`.
- **Moving image:** only when pacing or on-screen structure changes the conclusion, read
  [Job lifecycle](references/job-lifecycle.md), then submit `vidiq_video_watch` for long-form or
  `vidiq_watch_shortform_content` for Shorts. Transcripts and thumbnails cannot establish scene
  timing.

## Explain the result

Separate observations from hypotheses. Attribute performance to demand, packaging, distribution,
retention, or timing only with corroborating evidence, and state the strongest competing explanation.
Views and channel size give context; a breakout on a large channel is not a transferable mechanism
for a small one.

## Deliver

Report the video, evidence window and gaps, performance trajectory, packaging and content findings,
audience themes, transferable lessons, confidence, and the next read that would most improve it.
Keep adaptations original.

For the creator's own fresh upload use `vidiq-new-upload-review`; for an authorized channel's
retention curve use `vidiq-retention-analysis`; to repackage the video use `vidiq-packaging-studio`.
