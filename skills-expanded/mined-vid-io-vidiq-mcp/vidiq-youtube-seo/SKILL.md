---
name: vidiq-youtube-seo
description: Research YouTube keywords and search demand with vidIQ, then draft tags, a description, and title angles. Use when asked 'youtube keyword research', 'search volume for [topic]', 'youtube seo', 'tags for my video', or 'write my video description'. Text output only; applying changes to a video belongs to vidiq-video-metadata.
---

# vidIQ YouTube SEO

Read [Live surface notes](references/live-surface-notes.md) first, even when using only supplied evidence.

Research search demand for a topic or video and draft SEO-ready keywords, tags, a description, and
title angles. Keep this workflow read-only: no generation tools and no YouTube changes.

## Establish the target

1. Use the supplied topic, draft title, script, or video URL plus audience, language, market, and
   format. Ask one compact question only when a gap changes the keyword inputs.
2. For a published video, fetch its current title, description, and tags with
   `vidiq_get_videos_by_ids` so drafts improve the existing metadata instead of replacing it blindly.
3. Resolve the creator's channel with `vidiq_user_channels` only when channel context, such as format
   mix or past topics, changes the recommendation.

## Research demand

Read [Discovery evidence](references/discovery-evidence.md) when judging recurring patterns in
competing titles, including supplied examples.

- **Seed keywords:** call `vidiq_keyword_research` with `mode: "research"`, one seed `keyword`, and
  an optional supported `country`. Capture search volume, competition, and related terms as returned.
  Run additional seeds only when the first set cannot cover the topic; keep the plan bounded.
- **Momentum:** use `mode: "rising"` with `period` and `language` only when timing matters. Discover
  `availableTopics` before supplying a `topic`. Rising mode ignores `keyword` and `country`; to test
  a specific phrase, pass it as `includeKeyword` where declared, which matches whole words or
  adjacent phrases only.
- **Competing results:** use `vidiq_youtube_search` with `type: ["video"]` for the top results on the
  chosen phrase. Note title patterns, publication ages, and channel sizes without copying wording.
- **Short-form demand:** when the creator makes Shorts, use `vidiq_trending_videos` with the phrase
  as `titleQuery`, `videoFormat: short`, and the matching `videoTitleLanguage` to check whether it
  appears in short-form at all. Velocity measures current interest, not search durability.

Keep measured demand, competition, and growth separate from scores or rank. Missing, stale, or
nonpositive baselines cannot establish growth, and search demand alone does not prove format fit.

## Draft the metadata

1. Shortlist up to five keywords, or the requested count, with the measured demand and competition
   for each and a note on why it fits the creator's audience and channel size.
2. Draft tags from the shortlist and natural variants within YouTube's 500-character tag limit.
3. Draft a description that leads with the primary phrase in the first two lines, reads naturally,
   and never repeats terms for their own sake. Include chapters or links only when supplied; for a
   chapter block from captions, `vidiq-video-metadata` runs `vidiq_generate_video_chapters`.
4. Suggest title angles that contain the primary phrase truthfully. Score candidates with
   `vidiq_score_title` using the confirmed `type: long` or `short` only when the creator wants scores;
   scores are directional, not predicted traffic.

## Deliver

Return the keyword shortlist with evidence, the draft tags, the draft description, title angles, and
the limitations of the sample (market, language, date). State what would change the recommendation.

Do not apply anything. To update a published video's title, description, or tags, hand the approved
drafts to `vidiq-video-metadata`. For trend timing use `vidiq-trend-radar`; for creative title and
thumbnail concepts use `vidiq-packaging-studio`.
