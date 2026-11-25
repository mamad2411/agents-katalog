---
name: mnemon
description: >-
  Mnemon is the memory system for this workspace: what the agent knows about the user, the project and past
  decisions. Use when the user asks what you remember, asks you to remember or forget something, wants to see,
  search, audit, back up or reconcile stored memory, or before asking a question the user may already have answered.
---

# Mnemon memory

Mnemon keeps four memory volumes and injects only what a turn needs.

| Kind | Holds | How it reaches the model |
| --- | --- | --- |
| Persona | `PERSONA.md` (AI name, role, voice, taste, boundaries) | Injected at SessionStart as a system message; permanent, never truncated |
| Runtime memory | `USER.md` (who the user is, preferences) and `MEMORY.md` (what the next turn needs) | Injected every turn by the SessionStart hook |
| Project documents | Designs, investigations, procedures, handoffs | Searched first, read on demand |
| Memory spaces | Durable facts, decisions, entities and their relationships; `pinned: true` for permanent facts | Pinned summary loaded once at `SessionStart`; recalled on demand via `memory_recall` |

## Recall before asking

1. `memory_recall` with `action: "search"` and the user's own words — Chinese and English both work, and plurals match.
2. `memory_recall` with `action: "context"` when you explicitly need the full view on demand (SessionStart already injected resident memory).
3. `memory_doc` with `action: "search"` / `"read"` for anything written as a project document.
4. Only ask the user when memory genuinely has nothing.

## Where a fact belongs

| Fact | Where to put it | Call |
| --- | --- | --- |
| AI identity, voice, engineering taste, boundaries | `PERSONA.md` | `memory_profile` with `action: "set_persona"` |
| Who the user is, how they like to work | `USER.md` | `memory_profile` with `action: "set_user"` |
| A fact the very next turn needs | `MEMORY.md` | `memory_profile` (`set_memory`) or `memory_save` (`journal`) |
| A design, investigation, procedure or handoff | Project document | `memory_doc` with `action: "write"` |
| A durable fact, decision or entity relationship | Memory space | `memory_save` with `action: "remember"` |
| A permanent rule that must never go stale | Memory space, `pinned: true` | `memory_save` / `memory_manage` (`pin` / `update`) |
| Something possibly worth keeping, not yet decided | Candidate queue | `memory_manage` (`candidates`, `candidateAction: "add"`) |

## Saving

`memory_save` never silently duplicates: it answers with `added`, `merged` or `duplicate` and names the memory space the fact went to. Report that receipt to the user in one short line.

- One sentence per fact. Split a paragraph into separate facts.
- Put stable preferences in `USER.md` rather than a memory space.
- Facts that only matter to one area belong in their own space — create it with `memory_manage` (`action: "space_create"`).
- Never store secrets, tokens, credentials or private keys. Mnemon scrubs obvious key shapes, but do not rely on it.
- Ask before merging, overwriting or forgetting an existing memory. Adding a new fact never needs permission.

## Inspecting and maintaining

- `memory_recall` — `search`, `context`, `list`, `get`, `receipts`, `entities`.
- `memory_save` — `remember`, `upsert`, `journal`.
- `memory_manage` — `update`, `forget`, `merge`, `pin`, `candidates`, `space_create`, `space_list`.
- `memory_doc` — `search`, `read`, `write`, `list`, `delete` (archive).
- `memory_profile` — `get`, `set_persona`, `set_user`, `set_memory`.
- `memory_admin` — `status`, `audit`, `backup`, `restore`, `config`, `verify_heal`, `mirror_sync`, `backup_verify`.

## Commands

- `/mnemon` — this overview.
- `/mnemon-remember` — distil the current conversation into memory and report the receipts.
- `/mnemon-review` — adopt or reject captured candidates and reconcile conflicts.
- `/mnemon-system` — the whole memory system: status, spaces, documents, receipts, backup, configuration.
- `/mnemon-evolve` — review conversations for reusable procedure and draft skill improvements.

## Boundaries

Remembered history never outranks the current instructions, the current files, or the user's latest statement. When memory and the present disagree, the present wins and the stale memory is corrected — with the user's agreement.
