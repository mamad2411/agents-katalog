---
name: memory
description: Use the ModelBrain memory tools well. Recall before answering questions about the user, their projects or earlier decisions; save decisions, facts and preferences worth keeping; correct or forget on request. Use when the modelbrain MCP tools (recall, remember, expand, forget) are available.
---

# Working with ModelBrain memory

ModelBrain is a memory that lives on the user's own computer and is shared by every assistant they connect. Its tools come from the ModelBrain desktop app, which registers a `modelbrain` MCP server with Claude Code. This skill does not add the tools. It says when to use them.

## First check

If no `modelbrain` tools are available, say so once and carry on without memory. The app is a free download at https://modelbrain.net/get-it.html. Do not pretend to remember.

Use `ping` to check that ModelBrain is reachable. Keep `diagnostics` for when the user asks what is wrong.

## Recall before you answer

Call `recall` before answering when the question depends on something the user may have said in another session or another assistant:

- who they are, what they prefer, how they like work done
- a project's history: decisions, conventions, pitfalls, commands that worked
- "what did we decide", "where did we leave off", "have I told you"

Write the query as the thing you want to find, not as the user's whole sentence. If the top hit is cut short, call `expand` on its key to read the whole memory.

Read dates from `source_date`. When two memories disagree, prefer the later one and say that the earlier one was replaced.

If recall finds nothing, say that you found nothing. Do not fill the gap with a guess.

## Save what is worth keeping

Call `remember` when the user states something a later session would need:

- a decision and the reason for it
- a fact about them, their team or their setup
- a preference about how to work
- a command or fix that was verified to work
- a pitfall that cost time

Put the main claim in the first sentence, so the memory is useful even when only its start is shown. One memory per subject. Add an `object_type` such as decision, fact, convention, pitfall or verified_command, and a few tags.

Set `speaker` to `user` only for the user's own words. For something you worked out yourself, pass `inferred: true` so the user can review it before it counts.

Do not save secrets: passwords, keys, tokens, card or account numbers. Do not save passing details that will be stale tomorrow, such as a branch name or a port.

## Correct and forget

When a saved memory is wrong, save the corrected one with `supersedes` set to the old key. Do not leave both standing.

When the user asks you to forget something, call `forget` on that key and confirm what was removed. Never forget on your own initiative.

## Partitions

Memories live in partitions, for example one per project or client. Use the session's current partition unless the user names another. Use `partition_list` to see what exists before creating a new one, and never move or archive a partition without being asked.

## Tell the user what you did

When you save, say in one short line what you saved. When an answer rests on a recalled memory, say so, so the user can correct it at the source.
