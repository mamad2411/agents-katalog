---
description: Show what's on for today. Say "what's on for today?" (or run /today). 20-line view: anchor, open decisions, active flags, last 3 log entries, next calendar event.
---

# Today

One-screen view of what matters today. No scrolling. No prose. Read-only.

## Procedure (in order)

1. Read `cadence/daily-anchors.md`. Extract the `## Today:` section: anchor line + top 3 tasks.

2. Read `context/decisions.md`. Extract the top 3 Pending decisions by deadline proximity.

3. Read `brain/flags.md`. Extract active flags. Top 3.

4. Read `brain/log.md`. Extract the first line of the last 3 entries (newest on top).

5. If a calendar MCP is available (Google Calendar, Outlook), fetch the next scheduled event within the next 24 hours. Otherwise skip that line.

6. Render the output as a single fenced block, exactly this structure. No commentary before, after, or around it.

   ```
   TODAY - <YYYY-MM-DD>
   Anchor: <anchor line from daily-anchors>

   OPEN DECISIONS (top 3 by deadline)
   - <title> - <deadline>
   - <title> - <deadline>
   - <title> - <deadline>

   ACTIVE FLAGS
   - <flag name>
   - <flag name>
   - <flag name>

   LAST 3 SESSIONS
   - <first line of session entry 1>
   - <first line of session entry 2>
   - <first line of session entry 3>

   NEXT: <calendar event title at HH:MM> | <"no scheduled event next 24h">
   ```

7. If a section has nothing, write the header and one line: `none open.` Do not skip the section.
8. Day-one exception: if the anchor is `[NOT SET]` and the log holds one entry or fewer, do NOT render the fenced block. Reply instead, outside any block: `Nothing on today yet - that is normal on day one. Tell me the one thing you have to get done and I will make it today's anchor.` Placeholders rendered as a dashboard read as broken; a question reads as a start.

## What counts as progress here

Two behavior rules on what this brief reports. They change what the founder sees on a busy day, so they are not stylistic.

**Read back what moved, not what got closed.** The LAST 3 SESSIONS lines name outcomes: a reply that came in, a decision that got made, a thing that shipped, a payment that landed. Not "three items closed". Closing items is motion, and motion is easy to generate and easy to mistake for progress. If a day genuinely moved nothing, the honest line is that nothing moved. A brief that always looks productive is a brief nobody believes by the second week.

**Work that needs the founder's own hands surfaces as an action, not as another thing on a list.** If the anchor requires them to make a call, send a message, or decide something, write it as the action in their words ("call the supplier back about the delivery date"), not as a queue reference. Never answer a full plate by adding to it. When the plate is genuinely full, say which one thing matters today and that the rest can wait.

## Rules

- Read-only. Do not write to any file.
- Do not invoke other skills.
- No commentary outside the fenced block.
- If the daily anchor is stale (current date past `## Today:`), prepend a top line: `Yesterday's plan (<X>) is still showing. Say "roll my day" and I will carry it forward and ask for today's one thing.`
- Keep total under 20 lines.
- No em dashes or en dashes. Hyphens only.
- This command works only inside a Founder OS install. If the `cadence/` folder is missing, reply: `Founder OS not installed here. Say "set up Founder OS" first.`
