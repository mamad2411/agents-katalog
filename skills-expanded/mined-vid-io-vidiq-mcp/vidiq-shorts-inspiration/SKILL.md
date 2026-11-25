---
name: vidiq-shorts-inspiration
description: Find original YouTube Shorts ideas by studying what is breaking out on Instagram Reels and TikTok, then adapting the hook, pacing, format, and payoff. Use when asked for 'Shorts ideas', 'how to go viral on Shorts', 'viral TikTok or Reels formats I can use', 'what's working on TikTok in [niche]', or 'how are my Reels doing'.
---

# vidIQ Shorts Inspiration

Read [Live surface notes](references/live-surface-notes.md) first, even when using only supplied evidence.

Study Instagram Reels or TikTok examples and adapt their abstract mechanisms into original
YouTube Shorts concepts. Transfer hypotheses need evidence from the target platform. For
long-form YouTube ideas switch to `vidiq-video-ideas`.

## Research a bounded sample

1. Establish the source platform, target audience, niche, region, and production constraints.
2. Search with `vidiq_instagram_tiktok_outlier_search`, building `audienceQuery` from the supplied
   audience. Ask when context is vague rather than inferring sensitive traits. Set `embeddingType`
   (`concept`, `hook`, or `format`) and `query`. Date bounds require full ISO 8601 datetimes with
   timezone, not date-only strings.
3. Read [Discovery evidence](references/discovery-evidence.md) when evaluating source examples,
   including supplied results. Search only relevant concept, hook, or format lanes. Apply its
   minimum separately per platform before claiming a recurring pattern.
4. Use `vidiq_watch_shortform_content` on strong examples within scope. Verify the source and
   pass full public URLs, expanding Instagram shortcodes into full reel
   URLs; bare IDs, shortcodes, and TikTok short links are invalid. Preserve, poll, and recover
   jobs using [Job lifecycle](references/job-lifecycle.md); read it before a watch call.
5. Compare hook, pacing, on-screen text, reveal, payoff, duration, and production complexity
   from actually watched content or completed watch results. Covers, captions, URLs, and pending
   or failed watches cannot establish moving-image details. Mark missing visual evidence;
   use caption/title-only findings when that is all available.
6. For needed Instagram creator context or shortcode verification, selectively use
   `vidiq_instagram_account_discovery`, `vidiq_ig_profile`, or `vidiq_ig_profile_reels`.
   Match the target shortcode in returned reels; never assume the first result is the target.
7. For the creator's own Instagram results, call `vidiq_social_account_list` with
   `platform: "INSTAGRAM"`; a platform in `partial` has unknown connection state. Use the chosen
   account's exact `platformAccountId` with `vidiq_instagram_owner_insights` for shares, saves,
   watch time, and skip rate. Publishing eligibility does not establish insights access.
   If insights are unavailable, report the returned reason; public Reel data from
   `vidiq_ig_profile_reels` can supplement the review when labeled as public.
   To publish the resulting content, switch to `vidiq-publishing` when available; it
   prepares regular Reels as drafts and handles the separate Trial Reel and AI-label path.

## Verify transfer to Shorts

Use `vidiq_outliers` with `contentType: short` or `vidiq_trending_videos` with
`videoFormat: short` where the requested language is supported. Outliers rejects non-English
Shorts; use a supported alternative or disclose the gap. YouTube search with
`type: ["video"]` and `videoDuration: short` means under four minutes, not verified Shorts.
Check actual format before counting candidates; `vidiq_channel_videos` requires
`videoFormat: short`.

Use semantic mechanism searches primarily (`requireAllTitleTerms: false` when declared), with
strict phrases as supporting evidence. Apply the same relevance gate to YouTube results; a
bounded search cannot establish that nobody has adopted a mechanism.

Explain which viewer motivation transfers and how opening, reveal, and payoff need adapting.
Check dependencies on platform-specific audio, trends, interface, and audience context against
relevant watched target examples. Without that evidence, label transfer a hypothesis.

## Deliver original adaptations

Return the requested patterns/adaptations with source evidence grouped by platform, target-platform
support, production notes, confidence, and contradictions. Keep incomparable platform scores
separate. State actual watch status and material coverage limits.

Change subject, wording, examples, visuals, and payoff; use original or appropriately licensed
footage/audio, preserving required attribution. Do not copy or reupload source clips. Additional
generation requires a request and relevant source and likeness rights. Voice cloning also
requires explicit speaker consent.
