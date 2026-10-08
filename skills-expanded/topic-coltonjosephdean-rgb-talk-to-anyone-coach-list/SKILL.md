---
name: coach-list
description: List all coach personas already built and cached on this machine.
disable-model-invocation: true
---

# /coach-list — saved coaches

Show the user every persona already built on this machine.

1. Resolve the personas directories the same way as /coach Step 0:
   `${CLAUDE_PLUGIN_DATA}/personas` if that substituted to a real path, AND the legacy
   location `~/.claude/talk-to-anyone/personas`. Check both, merge the results
   (primary wins on duplicate slugs).
2. List their subdirectories. For each one that contains a `persona.md`, pull the name
   and the "Built:" line from the top of the file, and count files in `transcripts/`.
3. Print a short table: coach name, built date, number of source videos. End with:
   `/coach <name>` loads instantly · `/coach-refresh <name>` rebuilds from fresh research.
4. If the directory is empty or missing, say no coaches are saved yet and that
   `/coach <name>` builds the first one.
