---
name: sessions
description: >-
  Show the team's sessions: `/brigade:sessions` runs `brigade sessions` and prints its output unchanged.
  `/brigade:sessions --all` includes the offline ones, `/brigade:sessions --here` shows only this repository's,
  and `/brigade:sessions --member <who>` only one member's. Use it whenever the roster is being SHOWN to the
  user, so they see what the command printed rather than a retelling of it; reading the roster to address a
  message is `brigade:team-messaging`.
user-invocable: true
argument-hint: "[--all] [--here] [--member <who>]"
allowed-tools: Bash(brigade sessions:*)
---

# Show the team's sessions

`$ARGUMENTS` is what came after the command name: typed by the user through `/brigade:sessions`, or passed by
you when you loaded this skill to show the roster — a flag only when the user asked for what it does, otherwise
nothing. Either way the steps below are the whole of it.

1. Build the command from `$ARGUMENTS`, ignoring surrounding whitespace. These are the only forms:

   | `$ARGUMENTS` | Run exactly |
   | --- | --- |
   | empty | `brigade sessions` |
   | `--all` | `brigade sessions --all` |
   | `--here` | `brigade sessions --here` |
   | `--member <who>` | `brigade sessions --member '<who>'` |

   `--all`, `--here` and `--member <who>` may be combined, in any order, each at most once:
   `brigade sessions --all --here --member '<who>'`.

   `<who>` is a member's label as the `MEMBER` column shows it, or the first 8 or more characters of their
   principal reference, or a bracketed `MEMBER` cell such as `[9f3c1a20]`. Put it in single quotes, as one
   argument. If it holds a single quote, a backslash or a line break, say that this skill cannot pass it, and
   stop.

   For anything else, say which forms this skill takes, and stop — never a flag the user did not ask for,
   never `--json`, never a second command.
2. If the command succeeded, print what it printed **verbatim**, inside a fenced block, and write nothing else.
   No table, no list, no counts, no summary, no "this session is …", no comparison with an earlier run, no remark
   about any session or its state. On the first use on a machine, a `brigade: first use: downloading …` line
   precedes the roster: print that too rather than editing the output. The command's output is the display;
   reformatting it is what this skill exists to stop. A table with a header and no rows is a complete answer:
   nobody matched.
3. If the command failed, print what it printed, verbatim, and stop. Do not run it again and do not offer
   another form of it.

Sending a message, reading the roster on your own initiative, and every other `brigade` verb belong to the
`brigade:team-messaging` skill. This one only shows what `brigade sessions` prints.

When your user asks for the digest or the report rather than the roster, the command is `brigade report show`
(a project with a state folder), printed verbatim the same way; it sends nothing.
