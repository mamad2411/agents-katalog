---
name: runsheet-review
description: "A weekly review of the creator's YouTube channel with Runsheet: which recent videos beat the channel's own usual numbers and which fell short, what the difference was, what rivals broke out with, and the three things to do next week, saved as ideas. Use when the user asks how their channel is doing, for a weekly or monthly review, what worked, or what to change."
---

# The weekly review: measured first, then your read

## Steps

1. **Measure.**
   - `runsheet_get_library` with limit 50. Split the videos into Shorts and long videos, and compare
     each recent video (the last 14 days) with the median of its own format on this channel. The
     median, not the average: one viral video must not move the bar.
   - Runsheet's view counts come from its own snapshots, taken twice a day. Say so when a number
     matters.
2. **Name the pattern.** Look at what the videos above the median share and what the ones below
   share. Compare title shape, topic, length, day and format. This is your read, not a measurement,
   so call it that.
3. **Rivals.** `runsheet_get_watchlist`: any new breakouts. For the most relevant one,
   `runsheet_break_down_breakout` returns a brief, and you write the read and three angles for this
   channel.
4. **Next week.** Three actions, each concrete and small. For example:
   - "retitle X" (use `runsheet_generate_titles` and `runsheet_update_metadata`), only for a video well
     under its format's median, and only one change at a time (the title or the thumbnail) so the creator can
     tell what helped. YouTube does not penalize the edit itself. If the creator might be running a Test &
     Compare test on it in Studio, ask first: a change through the API ends the test,
   - "make two more Shorts like Y",
   - "move the upload from Monday to Thursday".
   Save any new video idea with `runsheet_create_idea`.
5. **Report.** Under ten lines:
   - the measured table (title, format, views, versus median),
   - the pattern,
   - the three actions.

## Rules

- **Measured numbers:** only from Runsheet. Your read is labelled as yours.
- **Small samples:** with fewer than five videos in a format, say the sample is too small to call
  a pattern.
- **Promises:** never promise views or growth.
- **Style:** no em dashes and no emojis.
