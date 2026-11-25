---
name: teammsg
description: E0-8 arm WITH the tool grant. Use when asked to run the brigade team-messaging routine. Lists live team sessions, identifies this session, and sends one reply.
allowed-tools: Bash(brigade:*)
---

# Brigade team-messaging routine

Run these three commands with the Bash tool, ONE tool call each, in this exact
order, and print each command's complete output verbatim before moving on:

1. `brigade sessions`
2. `brigade whoami`
3. `brigade send peer-9 hello-from-skill`

Run each command EXACTLY as written: no redirections, no pipes, no quoting
changes, no extra arguments. Do not combine them into one call. Do not run any
other command. Do not use any other tool. When the third command has been run, say `ROUTINE-COMPLETE` and stop.
