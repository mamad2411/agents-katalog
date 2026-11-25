---
name: runsheet-plan
description: "Plans the creator's next weeks of YouTube videos from their own channel with Runsheet: reads what the channel makes and what worked, finds rivals' breakouts, picks ideas for the open days, writes a script for each, and saves them as ideas in Runsheet. Use when the user asks to plan their month or week, what to film next, or for video ideas for their channel."
---

# Plan the next weeks from the channel itself

Your own model does the thinking and the writing. Runsheet gives you the channel's data and saves the
result. Nothing is uploaded or published by this skill.

## Steps

1. **Read.**
   - `runsheet_get_channel`.
   - `runsheet_get_library` with limit 50: the topics, the formats, and which videos beat the
     channel's own usual numbers. Compare against the channel itself, never against other channels.
   - `runsheet_get_watchlist`: breakouts on the channels it watches.
   - `runsheet_get_schedule` with 30 days: what is already planned.
2. **Find the gaps.** List the days in the period with nothing planned. If the user named a pace, use
   it. Otherwise use the channel's own recent pace from the library.
3. **Choose ideas.** One per open day.
   - Each one builds on something that worked on this channel, or takes a different angle on a
     watched channel's breakout.
   - Mix Shorts and long videos the way the channel already does.
   - Each idea has a working title, one sentence on the promise, and the format.
   - **Working titles follow YouTube's rules:** under 60 characters with the phrase a viewer would search in
     the first 40 (20 to 40 for a Short), no hashtags, at most one word in capitals, and only a promise the
     video can keep. Searchable for a how-to, a real question or problem for a story. No two share a pattern.
   - For a breakout, `runsheet_break_down_breakout` returns a brief. Write the read and the angles
     from it yourself.
4. **Script the first ones.** For the next three, call `runsheet_write_script` with the title and what
   the video is about. It returns Runsheet's brief, the rules and the format, and you write the script
   from it.
   - The hook: the first fifteen seconds.
   - The beats: in filming order.
   - The outro.
   Where a fact only the creator knows is needed, leave a [bracketed blank] rather than guessing.
5. **Save.** `runsheet_create_idea` for each idea, with the title, the promise and the format. Put the
   script in its notes when there is one.
6. **Report.** A short calendar: date, format, working title. Then the three scripts.

## Rules

- No invented numbers, results or stories. Opinions and advice are fine.
- Never promise views or growth.
- No em dashes and no emojis.
- US English unless the channel speaks another language.
- If the library is nearly empty (a new channel), plan from what the creator says the channel is about
  and say that this is what the plan rests on.
