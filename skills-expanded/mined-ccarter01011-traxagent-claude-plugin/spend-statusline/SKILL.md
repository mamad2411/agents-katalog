---
name: spend-statusline
description: Show session cost and Claude Code 5-hour and weekly limit use in the Claude Code status line. Use when the user wants to see what a session costs, how close they are to Claude Code limits, or their team's spend cap while they work.
---

# Spend in the status line

TraxAgent's free status line shows the model, this session's cost, and 5-hour and weekly limit use. With a TraxAgent account it also shows the person's spend cap and the day they'll reach it at their current pace. The script only reads Claude Code's status-line input; without an account, nothing is sent anywhere.

Don't run the installer yourself. Send the user to https://www.traxagent.io/statusline, where they can read the script and copy the one-line install command, and tell them to restart Claude Code after installing.
