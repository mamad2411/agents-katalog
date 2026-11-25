---
name: gabito-memoria
description: Queries and saves project memory with the memory_* tools, for Engram and team-server projects alike. Trigger: before starting work on a topic, after a decision, fix, discovery or convention, before saying done, or after context compaction.
license: Apache-2.0
metadata:
  author: gabitotl
  version: "1.0"
---

# Gabito memory: query first, save what matters

Memory keeps what the code cannot say: why, what was tried, what was decided. It is the lowest rung of the
truth order: current code > `.gabitotl/` > Git > memory > imported docs. If memory contradicts the code,
the code wins and you fix the memory.

## Which provider

Read `.gabitotl/memory.md` once. It names the provider for this project: `engram` or `memory-mcp` (the team
server). Never ask again what it already says. Both providers answer the same bridge tools, registered as the
`gabitotl memory mcp` MCP entry:

| Tool | Use |
|---|---|
| `memory_current_project` | Project key and your actor. Call first if unsure. |
| `memory_search` | Query by relevance: `text`, optional `type`, `limit` (default 8, max 20), `match_any`. |
| `memory_save` | Save one entry. Reusing a `topic_key` revises that entry instead of duplicating it. |
| `memory_update` | Patch an entry by `id` (optionally `expected_revision`). |
| `memory_session_summary` | Close a session: goal, discoveries, accomplished, next steps, files. |
| `memory_doctor` | Diagnose the provider when a call fails. |
| `memory_active_work` | Team server only: what others are doing now. |

If a runtime also exposes Engram's own tools (`mem_search`, `mem_save`, `mem_context`, `mem_session_summary`,
...), they work on the same Engram store; prefer the `memory_*` bridge so one entry serves both providers.
A tool that says it is "only available with team memory" is not an error in your call: use `gabitotl who`
instead. If a call fails, run `memory_doctor` or `gabitotl memory doctor` and report the exact message.
Memory failing never blocks the work or replaces the answer.

## Query before working

- Query by relevance with 2-4 specific terms: the module, the feature, the error. Never load everything.
- First step: `gabitotl memory context --task "<what you will do>"` returns a capped bundle (about 1500 tokens:
  most relevant entries, bodies cut). Read the full entry with `memory_search` only when a cut body matters.
- Then `memory_search`; use `type` (`decision`, `bugfix`, `convention`, `pending`, `risk`) to narrow.
- Also search after context compaction or when resuming, then read the full entry you need.
- Entries flagged `needs_review` (or otherwise marked pending review) are stale context: use them as a hint
  to check the code, never as fact. Revise them with `memory_update` once you verified the truth.
- Read-only work still queries memory; it just does not save.
- Searches full of old progress entries: suggest `gabitotl memory compact` (dry run; the user decides to `--apply`).

## Save after

Save immediately, without waiting to be asked, after: a decision, a bugfix, a discovery, a new convention,
a config change, a risk found, or a commit that closes a task.

Do not save: secrets, tokens, passwords, connection strings, raw logs, whole files, or what the code already shows.

## Format

`memory_save` fields: `type`, `title` (short, searchable), `content`, `topic_key`, and when known `task`,
`branch`, `commit`, `files`, `validation`, `next_step`, `ojo`. Write `content` as four lines:

- **What:** the change or fact, in one or two sentences.
- **Why:** the reason or the problem it solved.
- **Where:** files, modules, branch and commit.
- **Learned:** the gotcha or rule for next time. Omit if none.

Use English unless the project documents in another language. No AI branding or attribution in memory.

## Stable topic keys

A `topic_key` identifies one evolving subject, so later saves revise instead of piling up. Use
`area/subject` in lowercase: `decision/delivery-settings`, `bugfix/login-refresh`, `convention/error-wrapping`,
`progress/<feature>`. Reuse the same key for the same subject; use a new key for a different one.
Never overwrite an unrelated entry.

## Session summary and compaction

- Before saying "done", call `memory_session_summary` with goal, discoveries, accomplished, next steps, files.
- Around 75% of the context budget, save progress and the summary, then give the user the long-chat TIP.
- After compaction: `memory_current_project`, then `memory_search` for the active task, then read the project
  files. Reconcile what you remember with the current code before continuing.

## Rules

- Saving is bookkeeping, never the reply. Save first, then give the user the full answer as the last message.
- Memory is shared in team mode: write for the next person, not for yourself.
- Never send an `actor` other than your own; the server attributes writes to you.
- Conflicting memory: do not delete it. Save the new decision with the same `topic_key` and say it supersedes.
