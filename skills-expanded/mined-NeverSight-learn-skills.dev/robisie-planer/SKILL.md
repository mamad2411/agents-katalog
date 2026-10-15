---
name: robisie-planer
description: "Connect to the Robisie Planer — an agent-readable kanban board exposed over MCP. Use when you (an AI agent) need to pick up delegated work on your own: read the board, take the next unblocked task by goal priority, do it, and report progress — without an operator translating tickets for you."
---
<!-- mirror of https://robisie.app/SKILL.md, fetched 2026-07-06T00:44:04.026Z — that URL is the live source of truth; this copy exists so `npx skills add` can install it -->

# Robisie Planer — self-onboarding skill for AI agents

You are reading this because someone handed you a URL. Good. This skill makes you self-sufficient on
the **Robisie Planer**: connect once, then read the board and take work **on your own**.

## What this is — and why it matters

The Robisie Planer is an **agent-readable kanban board** exposed over MCP (Model Context Protocol). A
human operator drops work onto the board; **you** read the board, pull the next task, do it, and report
back. The operator never has to translate a ticket into a prompt or babysit you between steps — you
**self-direct from the board**. That is the whole point: the lowest possible barrier between "there is
work" and "the agent is doing it", without asking a human what to do next. **You are the primary user
of this board** — the operator sets priorities, you execute.

## Step 1 — Get your key

Every call is authenticated with a Bearer key of the form `rob_` + 64 hex characters, scoped to **your
board only** (per-user isolation — you never see another tenant's work). Generate one at:

    https://robisie.app/dashboard/connect

(Log in once, generate the key, copy it. The key is shown a single time and is hashed at rest — store
it like a password. If you are an agent run by an operator, ask them for the `rob_` key.)

## Step 2 — Connect (one line)

Add the gateway as an MCP server. In **Claude Code**, paste this in your project directory (swap
`<KEY>` for your `rob_` key):

```bash
claude mcp add --transport http robisie-planer https://robisie.app/api/mcp --header "Authorization: Bearer <KEY>"
```

> **Use it in every project — add `-s user`.** By default `claude mcp add` binds the server to the
> **current directory** only, so the key would work in just that one project. Add `-s user`
> (`claude mcp add -s user --transport http …`) and the key works across **all your projects**.

The gateway lives at `https://robisie.app/api/mcp`. Using Cursor, Windsurf, Codex, the Python SDK or the Node
SDK instead? The exact copy-paste config for each is on the same page (`/dashboard/connect`).

## Securing your key

Your key is the **only** credential to your board. Never let it land somewhere it is stored or logged
in clear text:

- **Never paste it into an agent's chat.** A key dropped into a prompt is retained in the conversation
  log the agent (or its provider) keeps. If you are an operator handing a key to an agent, pass it
  through the environment, not the chat.
- **Keep it out of shell history.** Don't type the literal key inline in a command. Read it into an
  environment variable without echoing it — `read -rs ROBISIE_KEY` (paste the key, press enter) — then
  reference `$ROBISIE_KEY`. (A plain `export ROBISIE_KEY=...` works too, but writes the key to your
  history file unless your shell is set to ignore space-prefixed lines; `read -rs` avoids that entirely.)
- **Never commit it to git.** If your client reads a config file (`mcp.json`, `config.toml`), store a
  *placeholder* and let the client expand it from the environment at runtime, so the file you commit
  holds no secret:

  ```json
  "headers": { "Authorization": "Bearer ${ROBISIE_KEY}" }
  ```

  With the Claude Code CLI you don't edit a file by hand — by default `claude mcp add` keeps the key in
  your private Claude config, out of the project's committed files (use `-s user` to share it across all
  your projects). Avoid `-s project`, which instead writes the key into a shared `.mcp.json` at the repo
  root — the one scope that lands in git.
- **Rotate and revoke.** Manage your keys at `https://robisie.app/dashboard/connect`: revoke a key the
  moment you suspect it leaked — a revoked key starts returning `401` immediately — and rotate
  periodically (generate a fresh key, swap it in, then revoke the old one).

## The data model

```
Project
  └── Track (column / swim-lane)
        └── Task (card)
              ├── status      — spec | plan | w_pracy | do_akceptacji | wdrożone | zrobione | zablokowane
              ├── dependsOn    — [taskId, ...]  (blocks this card until those are done)
              ├── specRef      — pointer to a spec doc / ticket
              ├── assignee     — who/what is working it
              ├── rob          — free-text tag / notes
              └── details      — structured metadata (JSON object)
```

The `status` values stay **Polish in the API** (these are the literal strings you pass to
`update_task`). English glosses, if you don't read Polish: spec = draft · plan = ready ·
w_pracy = in progress · do_akceptacji = in review · wdrożone = deployed · zrobione = done ·
zablokowane = blocked.

A card is **unblocked** when every task in its `dependsOn` is finished. That is what `get_next_task`
uses to decide what you may pick up next.

Two fields drive **ordering** and **progress rollups**:

- `details.servesGoal` (`"#1"` | `"#2"` | `"#3"`) — the operator's goal priority; `get_next_task`
  serves #1 before #2 before #3. Cards without it sort last.
- `rob` — a free-text grouping tag (e.g. a workstream id); `get_board` rolls up progress per tag
  (`robProgress`).

## Step 3 — The workflow (this is the value)

Once connected you have the Planer tools. The loop that lets you work without being told what to do:

1. **`list_projects`** — list the boards you own. Grab the project id you want to work on. A fresh
   account already has its first project provisioned — `list_projects` will show it; `create_project`
   is only for additional boards.
2. **`get_board`** — the whole board in one call: tracks + a digest of every card (id, title, status,
   position, rob). Cheap situational awareness.
3. **`get_next_task`** — **the magic.** It hands you the *single next card you should pick up*: the
   next **unblocked** `plan` card (all its dependencies are done) in goal → track → position order,
   honouring the goal priority on the board. Drafts (`spec`) are never handed out — promote one with
   `update_task status:'plan'` when it's ready. You don't guess what's next — the board tells you.
   Returns `null` when nothing is ready to start (everything left is a draft, in progress, done, or
   blocked).
4. **`reserve_task`** — claim that card atomically (a single compare-and-set: sets `assignee` and flips
   it to `w_pracy` in one step). If another agent grabbed it a millisecond earlier you get `null`
   instead of a double-assignment. Reserve **before** you start so nobody collides with you.
5. **Do the work.**
6. **`update_task`** with `status: "do_akceptacji"` — hand the finished card to the acceptance bench.
7. **`append_detail`** — attach your proof (PR link, evidence, timestamp) to the card.
8. **Loop.** Go back to `get_next_task` and keep taking cards until it returns `null` — that endless
   loop, with no human telling you what is next, *is* the self-direction this skill exists for.

⚠️ **`update_task` with a `details` object OVERWRITES the entire `details` field** — earlier keys are
lost. To add or change a single field without losing the rest, use **`append_detail`** (a shallow
JSONB merge). Reach for `update_task.details` only when you mean to replace everything.

## Status flow

Cards move through these statuses (these are the literal `update_task` `status` values):

    spec → plan → w_pracy → do_akceptacji → wdrożone → zrobione

- `spec` — a draft; defined but not yet ready. Visible on the board, but `get_next_task` never
  returns it — promote it to `plan` when it's ready to be picked up.
- `plan` — ready to be picked up (what `get_next_task` draws from).
- `w_pracy` — in progress (`reserve_task` sets this for you).
- `do_akceptacji` — done by you, awaiting human/validator acceptance.
- `wdrożone` → `zrobione` — shipped, then confirmed live. Those last transitions belong to the
  operator / validator, not to you.
- `zablokowane` — parked / blocked; `get_next_task` skips these. If the board still has cards but
  `get_next_task` returns `null`, the rest are drafts (`spec`) or blocked. To return a blocked card
  to the queue, move it to `plan` (moving it to `spec` keeps it a draft — still not dispatched).

## All 19 tools

Every tool is scoped to your own board (RLS per-tenant) — you can only see and touch your own work.

**Board overview**
- `get_board(projectId)` — full board in one call: tracks + card digest (id, title, status, position,
  rob), plus a `robProgress` rollup. Excludes `zrobione` by default; pass `statuses: ["zrobione"]` for
  the archive. Start here.
- `get_next_task(projectId)` — the next unblocked `plan` card by goal → track → position (drafts in
  `spec` are not returned). `null` when nothing is ready to start.

**Projects**
- `list_projects()` — your boards (no args).
- `create_project(name)` — create a board; returns it with an id.
- `update_project(id, { name? })` — rename.
- `delete_project(id)` — delete the board and everything in it (cascades).

**Tracks (columns)**
- `list_tracks(projectId)` — tracks in position order.
- `create_track(projectId, name, color?)` — add a column at the end.
- `update_track(id, { name?, position?, color? })` — rename / reorder / recolour.
- `delete_track(id)` — fails if the track still has cards (move them first).

**Tasks (cards)**
- `list_tasks(projectId, { trackId?, statuses?, full? })` — cards in position order; omits `zrobione`
  unless you pass `statuses`. `full: true` adds every field plus a `depsReady` flag.
- `get_task(id)` — one card in full (all `details`, `assignee`, `dependsOn`).
- `create_task(projectId, trackId, title, {...})` — create a card; returns a slim echo plus a
  `similarOpenCards` anti-duplicate warning.
- `create_tasks(projectId, tasks[])` — batch-create up to 200 cards (`dependsOn` must reference cards
  that already exist — no intra-batch forward refs).
- `update_task(id, {...})` — change a card's fields (⚠️ `details` overwrites — see above).
- `move_task(id, { trackId?, afterId?, beforeId? })` — move to another track and/or reorder.
- `delete_task(id)` — delete a card.
- `reserve_task(id)` — atomically claim a card (sets `assignee` + `w_pracy` in one step); `null` if
  already taken.
- `append_detail(id, patch)` — shallow-merge a flat object into `details` without losing other keys;
  your proof goes here.

## Starting a brand-new board

```
create_project("My AI project")                 → projectId
create_track(projectId, "Backlog")              → trackId
create_track(projectId, "In progress")
create_track(projectId, "Done")
create_tasks(projectId, [
  { trackId, title: "Research the approach", status: "plan" },
  { trackId, title: "Build feature A",       status: "spec" },  // 'spec' = draft — get_next_task won't return it; promote with update_task status:'plan'
])
get_next_task(projectId) → reserve_task → work → update_task → loop   // returns the 'plan' card; after it, get_next_task is null until you promote the draft
```

## Troubleshooting

- **401 Unauthorized** — your key is invalid or revoked. Generate a new one at `/dashboard/connect`.
- **`get_next_task` returns `null`** — nothing is ready to start: everything left is a draft (`spec`),
  `w_pracy`, `do_akceptacji`, `wdrożone`, `zrobione`, or `zablokowane` (blocked). Promote a draft with
  `update_task status:'plan'`, or tell the operator.
- **`reserve_task` returns `null`** — three causes: (a) another agent claimed it first — call
  `get_next_task` again for the next card; (b) the card is a draft (`spec`) — only `plan` cards are
  reservable, so promote it with `update_task status:'plan'` (or ask the operator); (c) the id is
  wrong or not on your board — re-fetch it via `get_next_task`/`get_board`.
- **Tool errors in Polish?** — known gap, fix tracked. The MCP error strings are being localized to
  English; until then some domain/server errors surface in Polish.
- **A card you expected isn't there** — confirm the `projectId` with `list_projects()`.

## Why an operator delegates to you

Because once you are connected, you **self-direct from the board without asking**. The operator drops
work and watches it move `spec → … → do_akceptacji` — progress is visible on the board, no status
meetings, no per-task hand-holding. You find the next thing to do by yourself. That is the deal.

Bare kanbans give you CRUD; this board gives you the loop (get_next_task → reserve → report) plus
acceptance handoffs — the coordination layer you otherwise have to improvise.

Free tier runs one real project end-to-end (this whole loop, no card cap you'll realistically hit at
30); paid tiers add parallel projects and more connected agents.
