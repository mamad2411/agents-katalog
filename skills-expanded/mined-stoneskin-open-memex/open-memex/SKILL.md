---
name: open-memex
description: Persistent local-first memory for the user and their projects. Use when the user shares facts, preferences, or decisions worth remembering across sessions, or when you need to recall past context before answering.
---

# open-memex — local memory

open-memex gives you persistent memory across sessions. Memories live in local
markdown files (SQLite FTS index); the `personal` scope never leaves this machine.

If `open-memex` MCP tools (`memory_add`, `memory_search`, …) are available in
this session, prefer them. Otherwise use the CLI below. If `open-memex` is not
on PATH, prefix commands with `npx -y open-memex@latest`.

## Session start - the wake ritual

Start the session from what memory already holds, not from questions to the
user:

- Read the `[OPEN-MEMEX]` block injected at session start (opencode plugin) or
  the equivalent guidance in the MCP handshake instructions. It carries the top
  project memories, the user's preferences, the working-state note from a
  previous session (if any), and the compiled memory map.
- If the block is empty or doesn't cover the current task, call `memory_search`
  once with the task's keywords - try 2-3 phrasings and check both scopes -
  before concluding anything is missing.
- Do not ask the user to re-explain what memory already holds; repeated
  "didn't we decide X?" questions are the failure open-memex exists to prevent.
  Ask only about what neither the block nor search can answer.

## Save — be proactive

When the user shares something worth remembering — a fact, preference,
decision, convention, or error fix — save it without being asked:

```sh
open-memex add "standup is at 9:30"                        # current project scope
open-memex add "I prefer concise diffs" --scope personal   # applies everywhere
```

Keep each memory one self-contained statement. Scope routing: facts about the
user ("I"/"me") → `personal`; everything else → the current project.

One thing the user said is one memory. When their own wording triggered keyword
capture (`remember …`, `记住…`), that sentence is already stored — do not save it
again in any rewording. Save only what the stored text does not contain, as its
own statement; if your version replaces it, use `memory_supersede`. `memory_add`
refuses the echo and hands you the stored id.

Worth saving: decisions and their reasons, preferences, conventions, gotchas,
approaches tried and abandoned. Not worth saving: one-off task details or
anything re-derivable from the code.

Attach alternate phrasings when saving — synonyms, another way the question
might be worded, equivalents in the user's other language — so reworded
questions still find the memory:

```sh
open-memex add "Public holidays are listed in the HR portal" --aliases "holidays;time off;节假日"
```

(Aliases are stored only when the install has capture aliases enabled — the
init default.)

## At task checkpoints — propose, don't just save

For conclusions you infer yourself (the user never stated them): when you
finish a task the user would describe in one sentence, propose 1–3 short
memories capturing the useful conclusion (what was learned or decided, how an
issue was resolved, what to avoid, where the authoritative doc lives — not the
raw transcript). Save nothing the user did not approve; on approval, save it —
with the `memory_add` tool pass `source: "inference"` so the capture is marked
as agent-proposed. Don't interrupt mid-task, and don't re-propose something
the user already declined.

## At wrap-up — refresh the working-state note

When the user signals the session or task is wrapping up (and the
`memory_workingstate` tool is available), write a short scratch note so an
interrupted task can resume in a fresh session: task summary (one paragraph),
open files, last commands, where the work stands, next step. It is **scratch
state, not knowledge** — never save it as a memory; anything here that
deserves to outlive the task goes through the propose flow above. The note
expires after 7 days; `open-memex wstate` shows it (`--clear` deletes it).

## Recall

```sh
open-memex search "deployment steps"   # keyword search across scopes
open-memex list                       # recent memories in the current project
```

Search before asking the user about past decisions or preferences they may
have told you before. Search well: break the question into its concepts and
try 2–3 phrasings per concept — synonyms, the user's other language, shorter
keyword forms — and check the other scope too, before concluding nothing is
stored.

## Record what paid off (D77)

When a person explicitly confirms a memory helped (or accepts work that
visibly relied on one), mark it: the `memory_useful` tool if available, else
`open-memex useful <id>`. Never mark a memory just because it appeared in
search results, a listing, or the session-start block — passive exposure is
counted automatically as `retrieved_count` and is not usefulness. Superseding
a memory or a human approving it at review already records a useful signal.

## Seeing and removing what is remembered

When the user asks "what do you remember about me?" (or wants to check or
clean up), show them the inventory:

```sh
open-memex inventory              # everything remembered, read-only
```

In chat, present the memories conversationally — turn the fields into
plain words (who the words came from, when it was saved, project or
personal) instead of reading raw ids. If the user asks to remove one,
read the entry back in full and get a confirmation before deleting —
deletion is permanent, there is no undo. If they hesitate, offer hiding
instead (`--soft`): it disappears from lists and search, but the file
survives. Either way, if the memory lives in the repo, the change is only
yours until you commit and push it.

```sh
open-memex forget <id>          # delete (permanent)
open-memex forget <id> --soft   # hide (retracted, one-way)
```

## Structure: the knowledge graph

The project's memories form a derived graph (D91) — what is connected to
what, without searching. Use it when the user asks how memories relate, what
an entry links to, or what is orphaned:

```sh
open-memex graph outline                 # topics + titles (also injected at session start)
open-memex graph neighbours <id>         # what links to / from this memory, with provenance
open-memex graph path <a> <b>            # how two memories connect
open-memex graph lint                    # orphans, dangling edges, near-stale pairs (reports only)
```

Edges are `EXTRACTED` (structural fact) or `INFERRED` (heuristic) — quote
that distinction when reporting. `lint` never fixes anything; a human decides.
The graph is rebuilt automatically on writes; `graph build` forces it.

## Project outbox → repo (the sync flow)

New project memories land in a local outbox (not in git). Review and publish:

```sh
open-memex sync-status     # drafts waiting, repo review state, uncommitted files
open-memex submit <id>     # publish drafts to .ai/open-memex/ + local commit
```

`sync-status` also ends with the D77 reuse report — per-scope retrieved/useful
rates, the most-reused memories, and "zombies" (retrieved but never confirmed
useful). Show it when the user asks what memory is actually pulling its weight.

If any command output reports drafts waiting in the project outbox, run
`open-memex sync-status` and ask the user which drafts to sync. The user may
also trigger this flow by saying "sync memory".

Run `open-memex <command> --help` for full usage of any command.
