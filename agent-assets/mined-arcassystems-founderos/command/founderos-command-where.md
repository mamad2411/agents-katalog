---
description: Find work you cannot find. Say "where is my work", "where did that go", "where did you save it", or run /founder-os:where. Answers with the project and folder in your own words instead of a list of paths, says plainly whether a second copy exists anywhere, and names any folder that would be gone tomorrow if this laptop died. Read-only - it opens nothing and moves nothing.
argument-hint: "[what you are looking for]"
---

Run the `where` skill.

Looking for: $ARGUMENTS

Run `python scripts/where.py --days 14 $ARGUMENTS` first (the words they gave you surface matching folders first), then answer in two or three plain sentences leading with the work, not the location. Widen the window if nothing looks familiar. If any folder comes back NOT BACKED UP, say so even though they did not ask - that is the more urgent finding. Close by offering to open the folder; on a yes, open it with `python scripts/open_folder.py "<folder>"`, never with a raw explorer / open / xdg-open command.

Never explain the folder architecture to someone who has just told you they cannot find their work.
