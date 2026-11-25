---
name: vidiq-video-ideas
description: Find original YouTube video ideas from outlier videos overperforming right now in the creator's niche and adjacent niches. Use when asked for 'video ideas', 'content ideas', 'what's working in my niche', 'videos breaking out', or '10 ideas for a [niche] channel'. Returns concept cards for packaging. For a ranked choice based on the creator's own analytics use vidiq-next-video-planner.
---

# vidIQ Video Ideas

Read [Live surface notes](references/live-surface-notes.md) first, even when using only supplied evidence.

Find concepts in videos that overperform on their source channels. Use own-channel and competitor
context to discover title mechanisms across adjacent niches serving the same viewer motivation.
Hand off full packaging to `vidiq-packaging-studio`.

## Establish the scan

Read [Discovery evidence](references/discovery-evidence.md) before evaluating concept sources,
including supplied examples.

Reuse supplied channel, niche, viewer, format, language, and market context; ask only for gaps that
change the scan. Keep the scan bounded, e.g. one or two outlier calls per mechanism lane,
including the shared bounded correction.

Resolve canonical channel IDs from supplied context, `vidiq_user_channels`, or exact-handle
`vidiq_channel_search`. Authorized IDs do not supply niche classifications. Reuse a supplied
niche; otherwise search a known handle/title and verify the returned `channelId` before using
`niche` or `subNiches`. Use `vidiq_get_channels_by_ids` for a missing title only if necessary.
Missing classification stays unknown or needs creator input.

Keep these evidence lanes distinct:

- **Own channel:** use matching-format `vidiq_channel_videos` and authorized analytics when useful.
  Catalog calls require `videoFormat: long`, `short`, or `live`. For sampled per-video analytics,
  use `dimensions: ["video"]` and `filters: "video==ID1,ID2"` in batches of at most 150.
  Missing requested rows are unknown.
- **Exact niche:** use an existing `vidiq_list_competitors` result or `vidiq_similar_channels`.
  Canonical `channelId` mode permits optional `size`/`sort`; manual `niche` mode has separate
  filters and no `subNiches` input. Country may affect ranking rather than eligibility.
  Exclude self, known siblings, and unrelated channels from analysis; disclose uncertainty and
  leave the saved list unchanged.
- **Adjacent niches:** use audience-focused semantic `vidiq_channel_search` and known creators.
  Verify returned market fit. Shared viewer motivation, not topical similarity alone, supports
  transfer; a small scan cannot prove the creator's audience has never seen a concept.

## Discover and judge concepts

1. Search `vidiq_outliers` with mechanism-shaped `keyword` queries, such as “I analyzed 100…”.
   Use `requireAllTitleTerms: false` for semantic discovery and strict `true` phrases as support;
   verify exact wording locally. Reserve own/competitor `channelIds` scans for separate context
   (up to 50 IDs). Set recent `publishedWithin`, matching `contentType`, and `sort: breakoutScore`.
2. Check the format/language combination. Outliers rejects non-English Shorts and has no live-only
   lane. For non-English outliers, `all` narrows to long-form and discovery is capped at six months.
   Pass a supported `language` explicitly; omission means English. A supported
   `vidiq_trending_videos` alternative uses `videoFormat` and `videoTitleLanguage`, but measures
   absolute velocity rather than channel-relative breakout. Disclose unavailable coverage.
3. Use `vidiq_similar_videos` selectively for independent executions of a seed. Choose the live
   `matchOn`, set `excludeSeedChannel: true` when appropriate, and inspect `signalsUsed`,
   `signalsFailed`, and `matchedBy` before relying on matches.
4. Apply the shared relevance/independence rule to inspected titles and images. Test whether the
   promise survives adaptation, audience overlap is credible, and production is feasible.
   Exclude fame-dependent or unaffordable mechanisms from feasible adaptations.
5. Name each surviving mechanism and explain its transfer. Rank with an editorial rubric for
   audience fit, originality, truthful payoff, and feasibility; label the rubric result separately
   from evidence confidence. Consider views, channel size, publication age, baseline stability,
   and market. Nonpositive or tiny baselines cannot establish reliable relative uplift.
   Favor feasible small-channel examples without excluding larger sources.
   Parse outlier `videoPublishedAt` as epoch seconds before comparing ages with ISO dates.
   Validate adapted-topic demand with `vidiq_keyword_research`, `mode: research`, only if useful.

For recurring scans, exclude previously shown video IDs; persist lanes and the seen list in a
client file/project note only when the creator wants a standing workflow.

## Deliver

Return concept cards with source/link and lane, actual performance context, inspected thumbnail
evidence or its limitation, the adapted concept, mechanism/transfer reasoning, and a working title,
hook, and format direction. Include separate rubric judgments and evidence confidence.

Report coverage and exclusions once per scan. Use original wording and present concepts as
research candidates, not performance predictions. Generate no assets or tool-based scores.
