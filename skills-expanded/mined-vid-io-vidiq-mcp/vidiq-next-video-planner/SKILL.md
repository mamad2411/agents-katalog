---
name: vidiq-next-video-planner
description: Rank what an authorized YouTube creator should publish next from their own analytics plus live search demand, audience requests, trends, and competitor gaps. Use when asked 'what should my next video be', 'what should I post on YouTube to grow', or 'rank these ideas for my channel'. Needs the creator's own channel; for ideas from breakout videos in any niche use vidiq-video-ideas.
---

# vidIQ Next Video Planner

Read [Live surface notes](references/live-surface-notes.md) first, even when using only supplied evidence.

Rank next-video opportunities from channel fit, competitors, demand, and timing. Keep this workflow
read-only: no generation, packaging scoring, refinement, or mutations. Switch to
`vidiq-video-ideas` for open-ended idea discovery and to `vidiq-packaging-studio` to package a
chosen idea.

## Scope and channel fit

1. Use supplied audience, format, language/market, horizon, constraints, and goal. Ask one compact
   question only for gaps affecting tool inputs or ranking.
2. Use a capped evidence plan: start with one call per relevant lane and expand only for facts
   that could change the decision.
3. Resolve the intended authorized channel with `vidiq_user_channels`. For recent channel fit,
   use `vidiq_channel_videos` with `popular: false` and matching `videoFormat: long`, `short`,
   or `live`.
4. Request `vidiq_channel_analytics` with explicit dates, `dimensions: ["video"]`, and
   `filters: "video==ID1,ID2"` for those IDs in batches of at most 150. Set `maxResults` to cover
   the batch within live limits and join by video ID. Missing rows are unknown; a mixed-format
   top-N report cannot define recent same-format fit. Compare sensible publication ages and
   label the upload set a sample. If private analytics are declined, disclose that missing lane.

## Research useful evidence lanes

Read [Discovery evidence](references/discovery-evidence.md) when discovering or evaluating
candidate opportunities, including supplied examples.

- **Competitors:** use `vidiq_list_competitors` when useful. Exclude self, known siblings, and
  unrelated channels from the analysis cohort; disclose uncertain ownership/fit and leave the
  saved list unchanged. Otherwise use `vidiq_similar_channels` with canonical `channelId` and
  optional `size`/`sort`. Manual `niche` mode has separate filters, no `subNiches` field, and
  ranking preferences that require checking returned fit.
- **Outliers:** gate the format/language combination before `vidiq_outliers`. Shorts are restricted
  to English; outliers and trending have no live-only lane. For non-English outliers, `all` narrows
  to long-form and discovery is capped at six months. Pass supported `contentType` and `language`;
  never silently substitute English or another format. Cluster premises, audience needs, and
  payoffs. Treat absent matches as a sampling limit, not proof of an unclaimed opportunity.
- **Search demand:** use `vidiq_keyword_research` with `mode: "research"`, seed `keyword`, and
  optional supported `country`. For momentum, `rising` uses `period` and `language`; discover
  `availableTopics` before supplying a `topic`. It ignores `keyword` and `country`; where declared,
  `includeKeyword` narrows results to a whole word or adjacent phrase.
  Keep measured demand/growth separate from scores or ranking; missing, stale, or
  nonpositive baselines cannot establish relative growth.
- **Audience requests:** `vidiq_comment_insights` with `mode: "discover"` and the `niche` returns
  recurring viewer requests and pain points across the niche as an asynchronous job; read
  [Job lifecycle](references/job-lifecycle.md) and poll `vidiq_job_poll`. `mode: "validate"` with
  `idea` tests a finalist. It is one lane, not a verdict, and the Claude.ai directory connector
  does not expose it.
- **Timing:** `vidiq_trending_videos` measures absolute velocity in the confirmed format and
  market. `vidiq_video_stats` on a finalist can test acceleration/decay; choose required
  `granularity: hourly`, `daily`, or `monthly` to match its age/window. Normalize epoch-second
  outlier dates and ISO timestamps before age comparisons. Do not equate velocity with
  channel-relative outlier performance.

Apply the shared relevance/independence rule to every discovery lane. For cross-niche mechanisms,
match viewer motivation and use semantic `requireAllTitleTerms: false`; strict matching is
supporting evidence only on tools declaring that field. Inspect actual images or mark visual
findings provisional.

## Decide and deliver

Compare up to three supported opportunities, or the requested count, on channel fit, competitive
opportunity, demand, timing, originality, and feasibility. Use ordinal judgments; do not sum
incompatible metrics. Prefer corroborating evidence types and state what could change the choice.

Return the shortlist and strongest supported brief with evidence scope/dates, confidence, and
counterevidence. Use original framing, examples, and expression. If evidence cannot support a
choice, state the gap; do not force a winner.
