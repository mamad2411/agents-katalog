---
name: echolot-reflect
description: Look back at how the last echolot session went and propose changes to the tool — its commands, its texts, its config. For whoever maintains echolot, not for the app being profiled. Use when asked how a session went or what echolot should change.
---

# Reflect

Run `echolot guide reflect` and follow it. The installed echolot prints it,
so it matches the report `echolot reflect` writes.

In short: `echolot reflect --last` turns the newest session that used echolot
into facts and signals, and you read its json rather than the session itself.
You return proposals grouped by where each change lands, every one with its
evidence. Nothing is edited without asking: show the list, and the human picks.
