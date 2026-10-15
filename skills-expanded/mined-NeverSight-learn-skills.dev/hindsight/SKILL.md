---
name: hindsight
description: Use the Hindsight tool to retain, recall, and reflect on persistent memory across sessions. Load when Hindsight tools are available and the task involves remembering, recalling, correcting, or managing long-term memory.
---

# Hindsight Memory

Use the Hindsight tools to persist what matters across sessions and retrieve it when it changes behavior. Memory that is never recalled is wasted. Memory that is never corrected goes stale and corrupts reasoning.

## When to Retain

Call `sync_retain` when the user shares any of the following:

- A preference, correction, or stated goal
- A technical decision, architectural choice, or trade-off
- A fact about their environment or project
- An error and its resolution

Do not retain greetings, small talk, or reasoning that does not affect future behavior.

Always use `sync_retain`, not `retain`.

## How to Retain

Set these fields on every `sync_retain` call:

- **content**: The raw conversation text or document. Do not summarize first.
- **context**: A short description of what the data is (e.g., "architecture review for the payments service", "user preference for error handling style").
- **document_id**: A slug identifying the session or topic (e.g., `session-payments-refactor`, `ticket-1234`). Pick this slug at the start of a session and reuse it on every retain in that session. Each retain with the same slug upserts, replacing the prior version.
- **tags**: See Tag Conventions below.
- **timestamp**: The current time in ISO 8601 format (e.g., `2026-07-31T10:30:00Z`).

## Tag Conventions

Tags filter which memories `recall` and `reflect` return. Pass `tags` with a filter to scope results - omit `tags` to search all memories.

Allowed tags:

- `repo:<git repo name>`: The repo name of the current git repo (or the base git repo name if in a working tree). Use a command like `basename "$(dirname "$(cd "$(git rev-parse --git-common-dir)" && pwd)")"` to determine the repo folder name at the start of a session and reuse this tag on every retain. Note that when working within a working tree, the base repo name should be used. When recalling, decide whether the query is specific to the current repo or general. Pass `tags=["repo:<name>"]` to filter to the current repo. Omit `tags` to search across all repos.

The `repo:` tag is required on every `sync_retain` call. Do not skip it by defaulting to "no evidence of a git repo" - run `git rev-parse --show-toplevel` to check. If the command fails (no git repo), omit the tag.

## When to Recall

Call `recall` at the start of a session or when a task would benefit from past context. Pass a query describing what is needed. Set `budget` to `mid`.

Call `reflect` instead of `recall` when the question requires synthesizing across multiple memories into a single answer. Pass `response_schema` when structured output is needed.

## How to Retrieve

- Call `recall` or `reflect` once. Read the result. If it answers the question, stop.
- If the result is insufficient, change the query or tags and call once more. Do not call a third time.
- Set `budget` to `low` for simple fact lookups. Set `budget` to `mid` for everything else.

Do not call `sync_retain` and `recall` in the same turn. Retain at the end of a turn. Recall at the start of the next.

## Correcting Memories

When the user corrects or contradicts something previously stated:

1. Call `invalidate_memory` on the old memory ID to retire it.
2. Call `sync_retain` with the corrected information.

Use `update_memory` to fix a detail in a memory without retiring it. Use `invalidate_memory` with `restore=true` if a memory was retired by mistake.

## Mental Models

Create a mental model for repeated queries that should return consistent answers (e.g., user preferences, technical stack, current projects). Create one model per topic. Do not create a single model covering everything. Call `refresh_mental_model` after significant data updates.

## Session Continuity

Call `sync_retain` at the start of each turn with the prior turn's key decisions, discoveries, and corrections. Use the same `document_id` slug across all retains in a session (e.g., `session-payments-refactor`). Each retain upserts, replacing the prior version. Include `timestamp` and tags.

Call `recall` at the start of a turn when a task would benefit from past context, with a query like "recent decisions and current project state".

## Gotchas

- **Do not retain then recall in the same turn.** Retained memories are not indexed yet. The recall will not find them.
- **Do not use random UUIDs for document_id.** Reuse the same slug when re-retaining the same conversation. Random IDs create duplicate documents.
- **Always set the context field.** Without it, extraction quality drops significantly.
- **Use tags for filtering, not metadata.** Metadata is not filterable at recall time.
- **Do not pre-summarize content before retaining.** Pass the raw conversation text. Summaries lose entity relationships and temporal markers.
- **Do not create one mental model for everything.** One model per topic. A single model covering everything has low accuracy and slow refresh.
- **Do not use budget="high" by default.** Use `mid`. Use `low` for simple lookups.
- **Invalidate stale memories when they change.** A corrected fact and its old version rank equally in retrieval. Retire the old one.
