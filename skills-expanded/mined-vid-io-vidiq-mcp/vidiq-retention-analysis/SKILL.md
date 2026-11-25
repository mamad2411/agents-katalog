---
name: vidiq-retention-analysis
description: Find where and why viewers leave an authorized YouTube video using vidIQ audience-retention analytics, the transcript, watched scenes when available, and comments. Use when asked about 'audience retention', 'watch time', 'where people drop off', 'my intro or hook loses viewers', or 'average view duration is low', or for pacing and structure advice on one video.
---

# vidIQ Retention Analysis

Read [Live surface notes](references/live-surface-notes.md) first, even when using only supplied evidence.

Investigate retention changes with private analytics and relevant content evidence.
Treat explanations as hypotheses, not proof of why every viewer left.

## Establish authorized evidence

1. Identify video, format, and review dates; keep analysis and optional watch/poll work within scope.
2. Resolve authorized IDs with `vidiq_user_channels`. If no video is supplied, discover candidates
   with `vidiq_channel_videos`, `popular: false`, and confirmed `videoFormat: long`, `short`,
   or `live`, or with `vidiq_user_videos` and the owning `channelId` when the video is unlisted
   or private; confirm the candidate. Use `vidiq_get_videos_by_ids` and require its `channelId`
   to match an authorized ID before private analytics. Otherwise offer a public-content critique
   with retention evidence unavailable, or hand the video to `vidiq-video-breakdown`.
3. Request `vidiq_channel_analytics` with explicit dates, `report: "audience_retention"`,
   `filters: "video==VIDEO_ID"`, `metrics: ["audienceWatchRatio", "relativeRetentionPerformance"]`,
   and `maxResults: 100`. The equivalent `dimensions: ["elapsedVideoTimeRatio"]` still requires
   that video filter. Read `columnHeaders` before interpreting the 100-point curve.

## Interpret the curve

`audienceWatchRatio` is segment watches relative to video views; repeat viewing can exceed 1
(100%). `relativeRetentionPerformance` compares videos of similar length on a 0–1 scale:
0.5 is the median, with higher values above it and lower values below it. This is comparative
rank, not the percentage of this video's viewers; see [YouTube's metric definition](https://developers.google.com/youtube/analytics/metrics#relativeRetentionPerformance).
If requested, `totalSegmentImpressions` counts segment watches, not unique viewers or thumbnail
impressions. Report available sample/denominator context; scope any extra read needed for missing counts.

Identify material drops, recoveries, or sustained changes against surrounding observations and
relative-retention context. Use actual non-null endpoints; percentage-point change is 100 times
the ratio difference. Record endpoints, interval, magnitude, and why it warrants attention.
Do not impose universal editing cutoffs or interpolate gaps into evidence. Sparse curves, small/unknown
samples, and near-end drops lower confidence without establishing an editing fault.

## Align content only with appropriate evidence

`vidiq_video_transcript` returns untimed `transcription`. Use it for spoken themes.
For scene alignment within the requested analysis, verify the source before watching:
`vidiq_video_watch` serves long-form; `vidiq_watch_shortform_content` serves Shorts.
Verify eligibility separately for live streams or recordings. Before a watch call, read
[Job lifecycle](references/job-lifecycle.md) for submission, bounded polling, and recovery.

Elapsed ratio times known duration gives an approximate analytics position, not an observed
scene timestamp. Attach scenes or timed hypotheses only when completed watch evidence supports
the alignment; scene ranges are not frame-accurate ground truth. Never attach a transcript quote
to a time range without evidence at that precision.

Without watch evidence, separate numeric zones from untimed content hypotheses. Use
`vidiq_video_comments` only for useful corroboration, preferring deidentified paraphrases;
comments are not representative of every viewer.

## Deliver

Report the scoped retention findings with actual metric values/deltas, approximate analytics
positions, watched scenes when available, hypotheses, confidence, and material sample limits.
Include requested watch job status and distinguish missing visual evidence.

When the creator requests editing advice, prioritize supported structural changes and the next
experiment; preserve what worked. Rewrite the opening or section order only when requested.
