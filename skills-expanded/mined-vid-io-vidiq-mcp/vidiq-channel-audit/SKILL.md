---
name: vidiq-channel-audit
description: Audit an authorized YouTube channel's last 30, 60, or 90 days with private vidIQ analytics (views, watch time, subscribers, format mix, top videos), then prioritize improvements. Use when asked 'analyze, audit, or review my YouTube channel', 'is my channel doing well', 'why are my views or subscribers dropping', or 'monthly channel report'. Whole-channel only; one new upload is vidiq-new-upload-review.
---

# vidIQ Channel Audit

Read [Live surface notes](references/live-surface-notes.md) first, even when using only supplied evidence.

Produce a private, read-only diagnosis of the authorized channel from its own evidence.
Do not generate assets, score packaging, or make state changes.

## Set comparable scope

Use the requested 30-, 60-, or 90-day window; propose 30 days in the research plan if unspecified.
Choose the latest completed calendar days, excluding today, and the immediately preceding equal
period. State both exact date ranges and date basis before querying.

Use a bounded analytics plan. Resolve the intended authorized channel with
`vidiq_user_channels`; stop private analysis if it is absent instead of substituting a similarly
named public channel. Request sensitive revenue, demographic, or geography breakdowns only when
the creator explicitly needs them.

## Gather relevant reports

- **Trajectory:** `vidiq_channel_analytics` with explicit dates and `dimensions: ["day"]`.
  Choose supported decision-relevant metrics, such as views, watch time, average duration/
  percentage, subscriber gains/losses, likes, and comments. Report latest observed date and
  gaps; a returned date is not proof of complete ingestion.
- **Format contribution:** use a separate `creatorContentType` report when the split matters.
  Keep long-form, Shorts, and live evidence distinct and use metrics valid for that report shape.
- **Portfolio:** a separate `video` report provides a bounded top-N view, not the full upload
  distribution. Use `vidiq_channel_videos` for recent titles/dates only when needed, with a
  required `videoFormat: long`, `short`, or `live` per call. Label that set a sample.
  Filter analytics to sampled IDs using `filters: "video==ID1,ID2"` in batches of at most 150;
  absent requested IDs remain unknown.
- **Public growth context:** `vidiq_channel_stats` with the `channelId` and the same `from`/`to`
  window gives public subscriber, view, and video-count growth for the channel or a comparison
  channel; keep it separate from private analytics.
- **Audience overlap or publishing windows:** use `vidiq_subscriber_insights` only when explicitly
  requested for the authorized channel. Its histogram is sampled public activity,
  not watch history or a live online-audience signal. Keep overlap data private.

## Interpret valid comparisons

Require equal-day coverage and comparable formats. If shifting bounds for ingestion lag, retain
equal full-length periods, disclose revised dates, and scope extra calls first. When an
inside-period change matters, compare equal-day halves (15/15, 30/30, or 45/45), showing observed
versus expected day counts. Missing values cannot be invented or unequal observed sums treated
as equal-day performance.

Sum additive metrics only. Weight rates/percentages using valid available denominators;
otherwise show rows separately. Compute net subscribers as gained minus lost, report both net
counts and the absolute delta, and add percent change only from a positive prior net. Counts
never change in percentage points.

Assess trajectory, watch efficiency, audience response, format contribution, and top-video
concentration against comparable channel history and the stated goal. Disclose cadence, upload
ages, sample size, and format-mix changes as competing explanations. Missing coverage or
nonpositive baselines leave relative decline unknown; show available absolute deltas.

Do not impose universal healthy-channel thresholds, unsupported peer benchmarks, or causal claims.
Thumbnail CTR/impressions are unavailable in this analytics schema; use supplied Studio data
when needed and label its source.

## Deliver

Give the authorized target, periods, relevant coverage/freshness limitations, and a compact health
summary separating observations, interpretations, and recommendations. Include an inside-period
comparison only when relevant, with its coverage or availability limit.

Prioritize up to three interventions, or the requested number, with evidence, competing explanation,
confidence, smallest action, success measure, and reassessment date. Report contradictions and
the next read that would most improve confidence. Route a focused launch question to
`vidiq-new-upload-review` and a single video's retention to `vidiq-retention-analysis`.
