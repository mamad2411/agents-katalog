---
name: yt-funnel
description: >-
  Fix the channel page and the subscriber conversion - the trailer, the
  above-the-fold, the sections, and the one video that converts browsers
  into subscribers. Use for "my channel page", "people watch but don't
  subscribe", "channel trailer", "subscriber conversion", or "optimise my
  homepage".
---

# yt-funnel

Read the [shared operating guide](../yt/references/operating-guide.md) for profile lookup, helper paths,
capability limits, and cross-skill routing before using this workflow.

Views are not the funnel. A viewer lands on one video, and whether they become a subscriber is
decided on the channel page in the next ten seconds. Most creators never touch it. This does.

For the per-video numbers (impressions, CTR, retention), that is [$yt-analytics](../yt-analytics/SKILL.md). This skill is the
layer above: what happens to a viewer *between* videos, and on the channel page itself.

## Before you work

1. Use the available voice profile or creator context (see the operating guide) - the trailer and the channel description are the channel's
   first sentence, in the creator's voice.
2. Get the conversion reality: Studio -> Analytics -> Audience shows returning vs new viewers, and
   Content -> a video -> Analytics shows subscribers gained per video. Subscribers-per-view is the
   number this skill moves.

## The four surfaces

1. **The channel trailer** (shown to non-subscribers). Not a highlight reel - a 30-60s answer to "why
   subscribe": who it is for, what they get, how often. Treat its first 5 seconds like any hook and
   run it through [$yt-script](../yt-script/SKILL.md)'s hook logic.
2. **Above the fold.** The banner, the handle, the one-line description. A stranger reads these before
   a single video plays. They must say who the channel is for in one line.
3. **The sections.** Order the channel homepage so the entry-point video (the one strangers find
   first) is top, a playlist that creates a binge is second, and the rest supports. Pair with
   [$yt-series](../yt-series/SKILL.md) for the binge path.
4. **The conversion video.** Find the one video with the best subscribers-per-view and treat it as the
   front door - link it, pin it, feature it. Make more like it.

## The move

- Audit each of the four surfaces against "does a stranger know who this is for in ten seconds".
- Rewrite the trailer script and the above-the-fold line.
- Name the conversion video and the entry-point ordering.
- Give one change per surface, ranked - not a redesign.

## What to hand back

- the rewritten trailer script (hook-first) and the above-the-fold line
- the section order, with the entry-point and binge playlist named
- the conversion video to feature, from the data
- one line: the single highest-leverage change of the four
