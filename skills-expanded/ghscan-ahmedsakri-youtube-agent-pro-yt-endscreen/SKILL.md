---
name: yt-endscreen
description: >-
  Place end screens and cards where they keep the session going instead of
  ending it - the right next video, at the right second, read off the
  retention curve. Use for "end screen", "cards", "what plays next", "where
  do I put cards", "keep people on my channel", or routing viewers between
  videos.
---

# yt-endscreen

Read the [shared operating guide](../yt/references/operating-guide.md) for profile lookup, helper paths,
capability limits, and cross-skill routing before using this workflow.

An end screen can guide viewers to a relevant next video. Choose by continuity and observed
viewer behavior rather than assuming the newest upload is best. Verify current feature eligibility
before giving implementation steps. Shorts need a Shorts-appropriate related-video or spoken CTA
plan; do not assume long-form end screens/cards are available in the Shorts feed.

Pair it with [$yt-retention](../yt-retention/SKILL.md) - the retention curve says where the viewer still is at the end, and
whether a card mid-video would catch a leak or cause one.

## Before you place

1. Use the available voice profile or creator context (see the operating guide) for the close - the end screen has a spoken hand-off, and "one
   ask, not three" is the rule from [$yt-script](../yt-script/SKILL.md) applied here too.
2. If there is a retention export, read it first ([$yt-retention](../yt-retention/SKILL.md)). The end-screen timing is only as
   good as knowing how many viewers are left to see it.

## The rules

- **End screen: the last 5-20 seconds.** Point it at the video that continues the thought, not the
  newest upload. The best next video is the one a viewer who just finished *this* one would choose - a
  part 2, the thing this one referenced, the obvious next question.
- **Lead with watch, not subscribe.** One video element and one subscribe element is the ceiling. If the
  video did its job, the next-video click is worth more than the subscribe ask, and it earns the
  subscribe anyway.
- **Hold something back for it.** The last 20 seconds need a reason to stay - do not fully resolve
  before the end screen or there is nothing left to hold the viewer through it. A flat outro is where
  the final cliff is.
- **Cards: at a leak, not at a peak.** A card mid-video catches viewers who are about to leave anyway -
  place it just before a known drop-off from the retention curve, never over a peak where it only
  distracts a viewer who was staying.

## The move

- From the retention curve, find the end-screen window (how many viewers remain) and any mid-video
  leak a card could catch.
- Pick the next video by continuity, not recency.
- Write the spoken hand-off (one ask) and the end-screen layout.
- Place 0-2 cards, each at a leak, each pointing somewhere relevant.

## What to hand back

- the end-screen pick (which video, why), with the spoken hand-off line
- the end-screen layout (video + subscribe), and the seconds to place it
- the card placements (timecode + target), or "none - no leak worth a card"
- one line: the single routing change most likely to lift session time
