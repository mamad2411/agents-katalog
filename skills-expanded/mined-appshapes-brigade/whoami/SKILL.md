---
name: whoami
description: >-
  Show who this session is on the team: `/brigade:whoami` runs `brigade whoami` and prints its output
  unchanged, the lines that give this session's ids, name and team, its member label and whether it is receiving.
  Use it whenever this session's Brigade identity is being SHOWN to the user (who am I on the team, which session
  is this, what is my label, am I receiving), so they see what the command printed rather than a retelling of it;
  reading it to address a message or to check a delivery is `brigade:team-messaging`.
user-invocable: true
allowed-tools: Bash(brigade whoami:*)
---

# Show this session's identity

`$ARGUMENTS` is what came after the command name: typed by the user through `/brigade:whoami`, or passed by you
when you loaded this skill to show who this session is, which is nothing. Either way the steps below are
the whole of it.

1. If `$ARGUMENTS`, ignoring surrounding whitespace, is empty, run exactly `brigade whoami`. For anything else,
   say that this skill takes no arguments, and stop: never a flag the user did not ask for, never `--json`, never
   a second command.
2. If the command succeeded, print what it printed **verbatim**, inside a fenced block, and write nothing else.
   No table, no list, no summary, no "you are …", no remark about any of its lines. On the first use on a
   machine, a `brigade: first use: downloading …` line precedes it: print that too rather than editing the
   output. The command's output is the display; reformatting it is what this skill exists to stop.
3. If the command failed, print what it printed, verbatim, and stop. Do not run it again and do not offer
   another form of it. Outside a Brigade session it refuses with `not_in_session`, and that is a complete answer.

Reading this session's identity on your own initiative (the `short id:` line that is your SESSION cell, the
`delivery:` line when a message you expected has not come) and every other `brigade` verb belong to the
`brigade:team-messaging` skill. Showing the whole team is `brigade:sessions`. This one only shows what
`brigade whoami` prints.
