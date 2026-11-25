---
name: clock
description: Clock.app heuristics for background-computer-use. Use when the user asks you to set an alarm, start a timer, run a stopwatch, or manage world clocks.
---

# Driving Clock with background computer use

1. Always call `get_app_state app="Clock"` before interacting.
2. Clock has four tabs (World Clock, Alarms, Stopwatch, Timers); after
   switching tabs, the tree changes completely — re-call `get_app_state`.
3. When adding a world-clock city from the search sheet, `click` the result
   row rather than pressing Return.
4. Alarm toggles are `switch` elements embedded in each row — click the
   switch, not the row.
5. Time pickers are usually `settable=true`; prefer `set_value` with a
   numeric string. If the picker is not settable, use `scroll` against the
   picker element's index.
6. In Stopwatch, Start/Stop is a single button whose title toggles; re-read
   state after each press.

Extended notes live in `server/app-hints/Clock.md`; the MCP server injects
them on every `get_app_state` call for Clock.
