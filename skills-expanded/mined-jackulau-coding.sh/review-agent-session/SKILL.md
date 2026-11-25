---
name: review-agent-session
description: "Reads a recorded agent session from coding.sh and explains what happened in it: the prompts, tool calls, failures, file changes, tests, subagents, tokens and cost. Use when the user asks what an agent did, why a run failed, went in circles or cost so much, wants a past session found, or asks you to review your own current session."
license: MIT
---

# Review an agent session

Uses the coding.sh MCP server's read tools. They read sessions recorded on this machine and change
nothing.

## Find the session

- This session: call `session_current`.
- A past one: call `sessions_list`. Narrow it with `since`, `agent`, `repo`, or `flagged: true` for
  sessions that went wrong.
- By something said or run in it: call `search` with `query` (the words), then open the session a
  hit names.

## Read it

1. Call `session_get` with `sessionId`. Read `session` first: turns, tool calls and errors,
   tokens, cost, `flags` and `derails`.
2. The timeline is paged. Pass `turn` for one turn, `cursor` for the next page, or `tail: true` for
   the end. Do not page through a long session from the start. Pick the turn from `turns`, the
   per-turn index: one with `toolErrors`, or the one running at a derail's `at`. A turn's `at` is
   milliseconds after `session.startedAt`.
3. A flag names a failure pattern for the whole session. A derail names the point where a long run
   went wrong, with a `detail`. Their meanings are in `references/flags.md`. Read it when a name is
   not clear.
4. For a session that spawned subagents, call `subagents` for the tree, or `session_tree` for cost
   and flags on every node. Open a child with `session_get` and its session id.
5. To see a file as it stood at one step, call `session_replay` with `sessionId` for the numbered
   step list, then again with `step` and `file`.

## Report

- Lead with the answer to what the user asked: what failed, where, and what the agent did next.
- Quote the tool call or error that shows it, with its turn number, so the user can check.
- Give tokens and cost from `session` when the user asks about cost. For totals over days, call
  `usage`.
- Keep causes you can see apart from guesses. A flag says what pattern occurred, not why.

## When data is missing

A result with `pending` was answered before every capture was indexed: call again shortly. If a
session the user expects is not there, call `status`. It reports each agent's last capture and the
last capture error.
