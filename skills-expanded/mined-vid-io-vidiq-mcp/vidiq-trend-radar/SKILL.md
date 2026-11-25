---
name: vidiq-trend-radar
description: Judge YouTube trends by urgency, durability, saturation, and accessibility to smaller channels using live vidIQ data. Use when asked 'what's trending on YouTube today', 'trending topics in [niche] this week', 'is this trend worth a video', or 'should I jump on this now or is it too late'. Classifies topics as urgent, durable, mature, or misleading.
---

# vidIQ Trend Radar

Read [Live surface notes](references/live-surface-notes.md) first, even when using only supplied evidence.

Separate current velocity, channel-relative breakout, durable demand, and creator accessibility.
Recommend timing from evidence and production lead time. Switch to `vidiq-youtube-seo` for keyword
volume and tags, and to `vidiq-next-video-planner` for a ranked next-video choice.

## Gather a bounded evidence set

Read [Discovery evidence](references/discovery-evidence.md) before evaluating trend examples,
including supplied results.

1. Define niche, audience, region/language, format, and horizon; use a bounded research
   plan. Before a saved-watchlist scan, exclude self, known siblings, and unrelated channels from
   analysis, disclose uncertainty, and leave the list unchanged.
2. Use `vidiq_trend_categories` only when its taxonomy can narrow outliers through
   `trendCategories`; those slugs are not inputs to `vidiq_trending_videos`.
3. Use `vidiq_trending_videos` for absolute velocity with required `videoFormat: long` or
   `short`, `videoTitleLanguage`, and a relevant `channelCountry`. Creator country is not
   audience geography. Use `vidiq_outliers` separately for channel-relative performance, with
   explicit supported `contentType`/`language`; omission defaults to English. Outliers rejects
   non-English Shorts, narrows non-English `all` to long-form, and caps non-English discovery at
   six months. Neither discovery tool provides a live-only lane; disclose unsupported coverage.
4. Apply the shared relevance/independence rule to inspected titles and images. Match transferable
   viewer motivation for cross-niche searches. Use semantic `requireAllTitleTerms: false` where
   declared, with strict matching as supporting evidence.
5. Use `vidiq_keyword_research` for search durability. Seed `research` gives demand context;
   `rising` accepts supported trend windows/categories and ignores `keyword`; narrow it to a phrase
   only with `includeKeyword` where declared (whole words or adjacent phrases).
   Search demand alone does not prove format fit.
6. Use `vidiq_video_stats` on finalists with required age-appropriate `granularity`; prefer
   `hourly` for recent trends and explicit ISO `from`/`to` bounds. Analyze historical `vph`,
   not cumulative views. Use comparable windows, allowing younger videos less than a full day
   of history. Normalize outlier epoch seconds and other ISO dates to a common timezone.
7. When accessibility matters, use `vidiq_channel_search` with `breakoutChannel: true`.
   Apply `subscriberCountMin` only for a requested or justified cohort boundary; disclose the
   reason and flag tiny-base growth as uncertain instead of excluding new creators by default.

## Classify from evidence

The labels are reporting aids, not fixed thresholds or deadlines. Leave unsupported cases
unclassified and state what observation could change the recommendation.

| Class | Evidence and response |
| --- | --- |
| **Urgent** | Relevant independent examples exceed positive comparable baselines with measured rising velocity. Act soon only if production fits the opportunity window. |
| **Durable** | Recurring need supported by relevant content over time and search demand; normal production timing can fit. |
| **Mature** | Measured plateau or decay across relevant examples with established demand. Differentiate or pass; age alone is insufficient. |
| **Misleading** | Evidence on relevance, independence, or sustained demand contradicts the apparent opportunity. State the contradiction; the topic itself need not be worthless. |

For urgency, use at least two timestamped non-null historical VPH observations per qualifying
example. Report baseline source, comparable format/age scope, window, and contrary movement.
One VPH snapshot, total views, or age cannot establish acceleration. Missing historical VPH or
positive comparable baselines leaves urgency unconfirmed.

Claim measured search-demand growth only for the same keyword with current value, positive
baseline, comparable market/window, and usable freshness timestamp. Prefer returned
`searchDemandGrowthPct` with that context; related keywords, upstream ranking, or raw growth are
not substitutes. Stable demand may support durable fit without positive growth.

High channel concentration plus declining VPH is a warning, not proof of a misleading trend.
Show cohort size, concentration denominator, sampling limits, and corroborating contradictions.

## Deliver

Return relevant opportunities with velocity, relative breakout, search durability, accessibility,
class, timing, production fit, and confidence. State the evidence date, actual filters, strongest
counterevidence, and next reassessment signal. Offer an original format/angle; keep timing a
reasoned estimate rather than a guaranteed trend half-life.
