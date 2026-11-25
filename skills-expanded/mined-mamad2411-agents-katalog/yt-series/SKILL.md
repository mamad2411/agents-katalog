---
name: yt-series
description: >-
  Design a multi-video series or a playlist as an architecture - an order
  people binge, each video earning the next click, a shared package so the
  set reads as one thing. Use for "plan a series", "a playlist", "a
  course", "multi-part video", "how do I structure a season", or turning
  one big topic into several videos.
---

# yt-series

Read the [shared operating guide](../yt/references/operating-guide.md) for profile lookup, helper paths,
capability limits, and cross-skill routing before using this workflow.

A playlist is not a folder. A series that works is an architecture: an order that creates a binge,
each video ending on the question the next one answers, and a shared look so the set reads as one
thing in the sidebar. This designs that.

## Before you plan

1. Use the available voice profile or creator context (see the operating guide) and, if there is one, the channel's existing format - a series
   has to fit the cadence the creator can actually keep.
2. A series is a commitment. Size it to the uploads they will finish, not the ones they imagine.
   Four videos shipped beats a twelve-part plan abandoned at three.

## The architecture

1. **The spine.** One question big enough for the whole series, split into parts that each stand
   alone *and* lead on. Part 3 must be watchable by someone who found it first, and must make them
   want part 4.
2. **The binge seam.** Every video ends on the exact question the next one opens with. That seam is
   a reason to continue watching. Measure actual continuation instead of claiming an algorithmic reward.
3. **The shared package.** A title pattern (numbered or named), a thumbnail template that varies one
   element per part, and a playlist title that is itself a search query. Hand the per-video packaging
   to [$yt-package](../yt-package/SKILL.md) and [$yt-thumbnail](../yt-thumbnail/SKILL.md) so each one is still linted on its own.
4. **The entry point.** Decide which video a stranger lands on first - usually not part 1. Order the
   playlist so the strongest standalone is the front door and the spine still holds.

## The move

- Map the spine into N parts, N sized to real capacity.
- Write each part's one-line promise and its binge seam to the next.
- Define the title pattern and the thumbnail template (what stays, what changes per part).
- Set the playlist title as a query, and name the entry-point video.

## What to hand back

- the ordered series with each part's promise and its seam to the next
- the title + thumbnail pattern for the set
- the playlist title (as a search query) and the entry-point pick
- one line: the realistic cadence, and the first video to shoot
