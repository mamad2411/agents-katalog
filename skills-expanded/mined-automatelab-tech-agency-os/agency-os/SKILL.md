---
name: agency-os
description: "Notion-as-source-of-truth dispatch board. Status flow Suggestion→Discussion→To-Do→In Progress→Done with subtasks, recurring tasks, deps, batch agent execution. Trigger: 'suggest X', 'discuss X', 'approve', 'start X', 'run todo', 'mark X done', 'kill X', 'next', 'capture this to Notion', 'agency-os status'."
---

# agency-os

Notion-as-source-of-truth dispatch board. One Tasks database, one Hub page, one page per Corpus, one page each for General Guidance and Resources. The skill mutates Notion via the Notion MCP (`mcp__*__notion-*` tools); only `references/notion-pointers.json` is committed to git.

**Skill name decision:** the skill is named `agency-os` (matching the repo). All commands are `/agency-os <cmd>`. This is the single plugin entry point; there is no `agency-os/notion` sub-namespace. If you embed this plugin alongside others, prefix commands with `agency-os` to avoid collisions.

## Positioning when writing user-facing copy (READ FIRST)

This is the canonical positioning brief. Apply it to any user-facing copy you draft for agency-os — README sections, blog posts, X threads, LinkedIn posts, Reddit submissions, plugin-directory entries, awesome-list PR bodies, social cards, launch surfaces, anything operators or audiences will read.

**Lead with these, in this order:**

1. **Structures the work.** Turns AI ideas into a visual workflow board so the user doesn't drown in suggestions. The board is the source of truth; work has shape and status.
2. **Streamlines agent-human interaction.** Discuss → scope → approve → run. The human is in the loop on every shipping decision.
3. **Control over execution.** Every run is operator-gated. Nothing dispatches autonomously. `Exec=Agent` is opt-in per row.
4. **Visual workflow.** One Notion board, one status flow (Suggestion → Discussion → To-Do → In Progress → Done), subtasks, dependencies, recurring cadences.

**Demote — mention later in the piece, never in the hook, headline, or opening tweet:**

- Token savings, "cheaper than running on Opus", Haiku-subagent dispatch — phrase as a side benefit, not the headline.
- Model-per-task routing — a consequence of the design, not the reason to adopt.

The product's first value is structuring AI-assisted work and keeping the human in control of what ships. Cost efficiency is a happy consequence of doing that well, not the pitch.

This section is mechanics-neutral: how the Sonnet/Haiku dispatch works is documented below under "Execution model" — that's how, not why. Don't conflate the two when writing copy.

## Harness compatibility

This SKILL.md is the authoritative spec and is harness-agnostic. The slash-command interface (`/agency-os ...`), the status flow, the schema, the workspace layout, and every command's behavior are the same everywhere.

Per-harness wrappers only differ in two things:

- **How commands are triggered.** Claude Code exposes them as real slash commands via the plugin manifest. Cursor / Cline / generic MCP harnesses load this file as instructions and rely on the user typing `/agency-os ...` (or the natural-language equivalent) into chat. Either way, the parser is the same.
- **Whether mutations are delegated to a subagent.** The "Execution model" section below describes Claude Code's Sonnet subagent dispatch. Other harnesses run mutations directly on the main agent. The Notion MCP calls underneath are identical; only the indirection changes.

See `docs/harnesses/` for per-harness setup. If you're reading this in a non-Claude-Code harness, treat the subagent dispatch instructions as optional: execute commands inline instead.

## Execution model — model selection by harness

### Claude Code: delegate to Sonnet (medium reasoning)

Every `/agency-os <command>` invocation runs on **Sonnet at medium reasoning effort** via a subagent. Sonnet at medium is the right balance for ID resolution, dedup, and brief assembly. The orchestrator stays free for conversation.

```
Agent({
  description: "Run /agency-os <command>",
  subagent_type: "general-purpose",
  model: "sonnet",
  prompt: "Run /agency-os <command> <args>.\n\nRead .claude/skills/agency-os/SKILL.md AND .claude/skills/agency-os/references/commands/<command>.md for the specific command spec. Execute end-to-end: sync preflight (run `python .claude/skills/agency-os/scripts/sync-tasks.py` via Bash — this incrementally refreshes the local mirror at `state/tasks.json`; do NOT call notion-fetch on the full data source as a default read path), resolve IDs against the local mirror, mutate Notion via the Notion MCP, write-through patch the mirror with the MCP response in the same step, and return the exact output format the command file specifies. All task/result links must be formatted as CommonMark markdown links — `[title](url)` — never HTML `<a>` tags and never a bare URL. If anything fails (sync, MCP, ID resolution), stop and report — do not guess.\n\nSTRUCTURE CHECK (for `suggest` without `--parent`, and for any batch suggest): Before creating any row, read `.claude/skills/agency-os/state/task-tree.json` for the current active task hierarchy. If the file is absent, call `/agency-os tree` first. Scan In-Progress and To-Do rows for an obvious umbrella parent. If a candidate exists with high confidence, surface it and require the orchestrator to confirm before proceeding. Never silently create a top-level row when an obvious parent exists. Full rules: `references/structuring-work.md`.\n\nALWAYS PRODUCE OUTPUT. On success: the skill's standard output. On failure: one paragraph naming what failed and what state Notion was left in. Returning nothing is not an option."
})
```

**Orchestrator MUST relay subagent output verbatim.** If output is empty: say `subagent returned no output; check Notion directly.` Never re-run, never absorb silently.

**Natural-language driving stays on the orchestrator.** Parsing "let's discuss the X task" into `/agency-os discuss <id>`, asking clarifying questions during a discussion, deciding `log` vs `add-subtask` — that runs on the orchestrator so thread context survives. Only discrete mutations dispatch to Sonnet.

Rule of thumb: touches Notion via MCP → Sonnet subagent. Deciding *what* to touch → orchestrator.

### Non-Claude harnesses: read models from config.json

On Cursor, Cline, Continue, and generic MCP harnesses, the skill can't spawn subagents. Instead:

1. **Before first use:** run `/agency-os init` to store your preferred models in `.claude/skills/agency-os/config.json`.
2. **Mutations (suggest, discuss, log, etc.):** run inline on the main agent.
3. **Batch execution (`/agency-os run`):** read `config.json` and use the stored models' constraints when evaluating task complexity.

The config file has this shape:
```json
{
  "harness": "cursor",
  "models": {
    "haiku": "claude-haiku-4-5-20251001",
    "sonnet": "claude-sonnet-4-6",
    "opus": "claude-opus-4-7"
  }
}
```

The `/agency-os run` command still uses the same picker heuristic (Haiku for mechanical work, Sonnet default, Opus for strategic) — but on non-Claude harnesses, you need to ensure your harness has an API or SDK integration with those models. If your harness only supports one model, set all three to that model.

---

## Authorization gates — no auto-promotion, no auto-execution

Three transitions require **explicit user authorization** every time. The skill must never make these moves on its own initiative.

**Gate 1 — Promoting to To-Do.** Any transition into `To-Do` (via `approve`, `move --to todo`, or direct Status write) is a scheduling commitment. MUST NOT promote unless the user named that row or an explicit batch the row clearly belongs to. "Cascade-approve discussion descendants because the user wants the parent executed" is **forbidden** — that's auto-promotion. Recurring-loop auto-flip on `done` is the only exception (the operator authorized it when marking Type=recurring).

**Gate 2 — Marking Exec=Agent.** Operator-owned. Skill MUST NOT set `Exec=Agent` on any row unless the user explicitly named that row and asked for it. Bulk-flipping across a subtree because "these look agent-runnable" is forbidden. `Exec=Human` and `Exec=none` are safe defaults; only `Exec=Agent` requires the gate.

**Gate 3 — Firing the queue.** `/agency-os run` is dry-run by default; `--go` is the user's explicit dispatch authorization. Orchestrator never adds `--go` to a `run` call the user did not type.

**Worked failure mode.** User says "execute all todo tasks under OS-XXX" → dispatch rows that are *already* `Status=To-Do AND Exec=Agent` under OS-XXX. Does NOT authorize flipping Discussion descendants to To-Do, flipping leaves to Exec=Agent, or any prep step. If literal scope yields zero runnable rows, say so and ask — do not invent prep.

**When in doubt — ask.** List candidates, wait for selection, then act. Never guess the set.

---

## What lives where (hybrid contract)

- **Local, source-of-truth:** every skill spec under `.claude/skills/`, every doc under `docs/`, the `notion-pointers.json` binding, and `references/general-guidance.md` (the canonical General Guidance text — Notion's page is a one-way mirror).
- **In Notion, source-of-truth:** task rows (Title / Status / Corpus / Priority / Impact / Type / Cadence / Effort / Parent Task), discussion logs, done logs, corpus pages, the Hub itself.
- **One-way mirror:** `references/general-guidance.md` → Notion General Guidance. Edit locally, push to Notion. Never reverse-sync.

Briefs pull **task state** from Notion (via the local mirror) and **stable spec** from local files. The brief contains pointers to local files, not copies.

```
# setup
/agency-os scaffold [--parent=<page-id-or-url>] [--corpora="<n1>,<n2>,..."]
/agency-os init [--harness ...] [--haiku=...] [--sonnet=...] [--opus=...]
/agency-os sync
/agency-os tree [--depth N] [--corpus=<s>] [--status=<s>]

# suggestions
/agency-os suggest "<title>" [--corpus=<s>] [--type one-time|recurring]
                              [--cadence ...] [--notes "..."] [--effort S|M|L|XL]
                              [--parent=<id>] [--force-top-level]

# clarification & subtasks
/agency-os discuss <id>
/agency-os log <id> "<entry>"
/agency-os add-subtask <parent-id> "<title>" [--effort=<e>] [--notes "..."] [--deps=...]
/agency-os approve <id>

# execution
/agency-os start <id>
/agency-os refresh
/agency-os run [--go]
/agency-os done <id> [--result-link <url>] [--note "..."]
/agency-os kill <id> [--reason "..."]

# read
/agency-os next [N] [--corpus=<s>]
/agency-os status
/agency-os list <suggestion|discussion|todo|inprogress|done|killed|recurring|all> [--corpus=<s>]
/agency-os show <id> [--section description|discussion|donelog|all] [--entry <date>]

# escape hatches
/agency-os update <id> [--title="..."] [--notes="..."] [--priority=1|2|3|4]
                       [--effort=...] [--type=...] [--cadence=...] [--corpus=<s>]
                       [--deps=<id1>,<id2>,...|none] [--parent=<id>|none]
/agency-os move <id> --to <status>
/agency-os add-corpus "<name>" [--goal "..."]
```

**Natural language is also a trigger** — see the "Natural-language driving" table below.

**Command specs** live in `references/commands/<name>.md`. The subagent loads SKILL.md + the one command file for the dispatched command.

---

## Status flow — the dedup gate

```
Suggestion --discuss--> Discussion --approve--> To-Do --start--> In Progress --done--> Done
                                                                             ^
   any  --kill-->  Killed  (terminal)                                        |
                              Recurring tasks: done logs + loops to To-Do ---+
```

| Status | Meaning | Set by |
|---|---|---|
| `Suggestion` | Idea in the inbox; not yet discussed | `suggest`, manual |
| `Discussion` | Under clarification | `discuss` |
| `To-Do` | Approved; scheduled | `approve`, recurring loop |
| `In Progress` | Agent actively working | `start` |
| `Done` | Closed (one-time) | `done` |
| `Killed` | Intentionally dropped | `kill` |

`next` filters `Status == "To-Do"` sorted by Priority asc then Created asc. `run` requires `Status == "To-Do" AND Exec == "Agent"`. `suggest` refuses dupes via Title-Jaccard ≥ 0.8 against any non-terminal status. If `start` crashes, manual recovery: `/agency-os move <id> --to todo`.

---

## Sync — local mirror is the read path

Every command reads from a **local JSON mirror** at `state/tasks.json`, not from live Notion. The mirror is kept fresh by an incremental delta sync that only fetches pages whose `last_edited_time` advanced since the last sync — typically a handful of rows per command, often zero. Live `notion-fetch` of the full data source is the escape hatch, not the default. Token cost per command drops by roughly an order of magnitude after the first bootstrap.

**Preflight (every command).** Run:

```bash
python .claude/skills/agency-os/scripts/sync-tasks.py
```

via the Bash tool. The script reads `NOTION_KEY` from `.env`, pulls the data source ID from `notion-pointers.json`, queries Notion with a `last_edited_time` filter, parses each changed page's body (Description / Discussion log / Done log toggleable H2 sections), and upserts into `state/tasks.json`. On first run (no mirror file) it does a full bootstrap. Then resolve `<id-or-substring>` against `state/tasks.json`.

**Write-through on mutations.** Every command that mutates Notion (via the Notion MCP — `notion-create-pages`, `notion-update-page`, etc.) MUST patch the corresponding row in `state/tasks.json` in the same step, using the response payload from the MCP call. This keeps the mirror authoritative across the same session and prevents the next command from re-syncing the row we just wrote. The shape of each row is what `sync-tasks.py` produces (see schema below).

**Escape hatches.**
- `python scripts/sync-tasks.py --full` — full rebuild (e.g. after schema changes or suspected drift).
- `notion-fetch <data_source_id>` directly — only when you need a property the mirror doesn't carry, or when verifying the mirror against live data. Do not make this the default; the whole point is to stop dragging the full DB into LLM context on every command.

**Tree snapshot side-effect.** After every successful sync, also write `state/task-tree.json` — a compact nested representation of all non-terminal tasks (Suggestion / Discussion / To-Do / In Progress), structured as a tree via `Parent Task`. This is the free structure reference for `suggest` preflight and orchestrator planning. Both files are gitignored.

```json
{
  "snapshot_at": "<iso>",
  "tree": [
    {
      "id": "OS-12", "notion_id": "<uuid>", "url": "<url>",
      "title": "Top-level initiative", "status": "In Progress",
      "corpus": "General", "effort": "L", "depth": 0,
      "children": [
        { "id": "OS-13", "notion_id": "...", "url": "...",
          "title": "Container subtask", "status": "To-Do",
          "corpus": "General", "effort": "M", "depth": 1,
          "children": [] }
      ]
    }
  ]
}
```

**Mirror schema (`state/tasks.json`).**

```json
{
  "synced_at": "<iso>",
  "previous_synced_at": "<iso|null>",
  "tasks": [
    {
      "notion_id": "<uuid>", "task_id": "OS-12", "url": "<url>",
      "title": "...", "status": "To-Do",
      "type": "one-time", "cadence": null,
      "corpus": "General", "priority": "2", "impact": "high",
      "effort": "M", "exec": "Agent", "tags": [],
      "parent_task_id": "<uuid|null>", "dependency_ids": ["<uuid>"],
      "last_done": null, "done_at": null, "result_link": null,
      "created_time": "<iso>", "last_edited_time": "<iso>",
      "description": "<first 600 chars of Description section>",
      "latest_discussion_entry": "<most recent ### entry, truncated>",
      "last_done_log_entry": "<most recent ### entry, truncated>"
    }
  ]
}
```

If `sync-tasks.py` fails (Notion API down, OAuth expired, network error), print `sync failed: <reason>` and abort the command — do not fall back to a stale mirror for mutations. Read-only commands (`list`, `next`, `show`, `status`, `tree`) MAY proceed against the existing mirror with a `sync failed; reading stale mirror` warning; mutations (`suggest`, `discuss`, `approve`, `start`, `done`, `kill`, `update`, `move`, `log`, `add-subtask`) MUST abort.

---

## Workspace structure

```
Hub  (page)
+-- intro: what this board is for
+-- General Guidance  -> page
+-- General Plan      -> table; one row per Corpus, linked to its page
+-- Suggestions Inbox  (linked DB view: Status=Suggestion, sort Created desc)
+-- In Discussion      (linked DB view: Status=Discussion, sort Created desc)
+-- To-Do (Scheduled)  (linked DB view: Status=To-Do, sort Priority asc, group by Corpus)
+-- Recurring          (linked DB view: Type=recurring, sort Last Done asc)
+-- In Progress        (linked DB view: Status=In Progress)
+-- Recently Done      (linked DB view: Status=Done, sort Done At desc, limit 25)
+-- Resources          -> page

Tasks  (database)
+-- one row per task, of any status, including subtasks
```

### Tasks database schema

| Property | Type | Notes |
|---|---|---|
| `Title` | title | Imperative phrase, <=80 chars |
| `Status` | status | `Suggestion`, `Discussion`, `To-Do`, `In Progress`, `Done`, `Killed`. Default `Suggestion` |
| `Type` | select | `one-time` (default), `recurring` |
| `Cadence` | select | `daily`, `weekly`, `biweekly`, `monthly`, `quarterly`, `yearly`. Empty for `one-time` |
| `Last Done` | date | Set on `done` for recurring |
| `Corpus` | select | One of the configured corpora |
| `Priority` | select | `1`–`4` — **urgency** (1 = this week / 4 = nice to have). Default `4` |
| `Impact` | select | `low`, `medium`, `high`, `outsized` — outcome size within corpus. Default `medium` |
| `Effort` | select | `S`, `M`, `L`, `XL`. Default `M` |
| `Exec` | select | `none` (default), `Agent`, `Human`. Operator-set gate for `run` |
| `Parent Task` | relation (self) | Subtask linkage; empty for top-level |
| `Subtasks` | rollup | Inverse of Parent Task |
| `Created` | created_time | Automatic |
| `Done At` | date | Set on terminal `Done` |
| `Result Link` | url | Live link, post URL, PR URL |
| `Tags` | multi_select | Cross-cutting |
| `Dependencies` | relation (self) | Must reach `Done` before this row is dispatchable by `run`. Ignored by `start`, `next`, `list` |

### Task page body

Every task page uses **toggleable H2 sections** (`is_toggleable: true`). If the MCP can't set the flag, fall back to plain H2.

```
> Launch this task
> Paste in Claude Code: `/agency-os start <id>`

Description     <- starts expanded
   <freeform: what to do, why, acceptance criteria, links>

Subtasks        <- expanded if any exist
   (linked DB view: Parent Task = this)

Discussion log  <- collapsed
   ### 2026-01-10 — initial clarification
   ...

Done log        <- collapsed; mainly for recurring
   ### 2026-01-12: completed by agent — link <url>

Related         <- expanded; one-line each
   Corpus: [-> <corpus>](<corpus-url>)
   General guidance: [-> Guidance](<guidance-url>)
   Parent: [-> <parent-title>](<parent-url>)
```

### Corpus pages

```
# Corpus: <name>
## Goal
1-3 sentences on what "done" looks like.
## Local guidance
Conventions, owners, references.
## Tasks
(linked DB view: Corpus = this, group by Status)
```

### General Guidance page

Project-wide rules. Kept short. Links into `docs/` and `.claude/skills/`. Links beat duplication. Seeded from `references/general-guidance.md` — edit the local file, push the mirror.

---

## Pointer + cache files

`.claude/skills/agency-os/references/notion-pointers.json` (committed):

```json
{
  "hub": { "page_id": "<uuid>", "url": "...", "title": "..." },
  "tasks_database": {
    "database_id": "<uuid>",
    "data_source_id": "<uuid>",
    "url": "...",
    "task_id_prefix": "OS"
  },
  "guidance": { "page_id": "<uuid>", "url": "...", "title": "..." },
  "resources": { "page_id": "<uuid>", "url": "...", "title": "..." },
  "corpora": {
    "General": { "page_id": "<uuid>", "url": "...", "title": "General" }
  },
  "hub_views": { "Suggestions Inbox": "view://<uuid>", "...": "..." },
  "corpus_views": { "General": "view://<uuid>" },
  "schema_summary": { }
}
```

---

## Commands

Each command's full spec lives in its own file. The dispatch subagent loads this SKILL.md plus the one relevant file.

| Command | Spec file |
|---|---|
| `init` | `references/commands/init.md` |
| `scaffold`, `add-corpus` | `references/commands/scaffold.md` |
| `suggest` | `references/commands/suggest.md` |
| `discuss` | `references/commands/discuss.md` |
| `log` | `references/commands/log.md` |
| `add-subtask` | `references/commands/add-subtask.md` |
| `approve` | `references/commands/approve.md` |
| `start` (alias `launch`) | `references/commands/start.md` |
| `refresh` | `references/commands/refresh.md` |
| `run` | `references/commands/run.md` |
| `done` | `references/commands/done.md` |
| `kill` | `references/commands/kill.md` |
| `next` | `references/commands/next.md` |
| `status` | `references/commands/status.md` |
| `list` | `references/commands/list.md` |
| `tree` | `references/commands/tree.md` |
| `show` | `references/commands/show.md` |
| `update` | `references/commands/update.md` |
| `move` | `references/commands/move.md` |

Shared rules: parent-vs-subtask-vs-log decisions, structure preflight protocol, "move this chat to Notion" workflow, and a worked example → `references/structuring-work.md`. The `suggest` and `add-subtask` specs reference this file.

---

## Natural-language driving

When the user says these things in chat, the skill translates to commands:

| User says | Skill calls |
|---|---|
| "what's the structure" / "show me the hierarchy" / "how is this organized" / "what tasks are active" | `tree` |
| "add a suggestion: <title>" / "new idea: <title>" | `suggest "<title>"` — structure preflight runs inside; if an obvious parent exists the subagent will surface it and wait for confirmation before creating the row |
| "create N tasks for X, Y, Z" / "batch add: ..." / "set up tasks for <multi-part work>" | orchestrator reads `state/task-tree.json` (or runs `tree` if absent), proposes the full planned tree in chat (existing umbrella? container needed?), waits for user confirmation, THEN dispatches `suggest --parent=<id>` per item |
| "reorganize <X>" / "restructure under <parent>" / "move <task> under <other-task>" / "group these tasks" | `update <id> --parent=<parent-id>` per row (or `--parent=none` to demote) |
| "let's discuss X" / "open X for discussion" | `discuss <id>` |
| "log: <thing>" / "note that <thing>" (during discuss) | `log <id> "<thing>"` |
| "add a subtask: <title>" / "we'll also need to <thing>" | `add-subtask <parent-id> "<title>"` |
| "approve" / "approve it" / "ship it" / "go ahead" | `approve <id>` (Gate-1 — user must name the row or explicit batch; never auto-cascade beyond what the user said) |
| "start X" / "launch X" / "let's do X now" | `start <id>` |
| "run todo" / "run all" / "execute the queue" | `run` (dry-run) -> user reviews -> `run --go`. Gate-3 — `--go` is added ONLY when the user explicitly says go/fire/yes. NEVER cascade-approve or flip Exec=Agent as a "prep step" — execute only rows that already meet `Status=To-Do AND Exec=Agent` literally |
| "X is done [link <url>]" / "mark X done" | `done <id> [--result-link <url>]` |
| "kill X" / "drop X" / "X is no longer relevant" | `kill <id>` |
| "make X recurring weekly" / "X is recurring monthly" | `update <id> --type=recurring --cadence=weekly` |
| "what's next" / "what should I work on" | `next [N]` |
| "show me X" / "details on X" | `show <id>` |
| "what's the status" / "where are we" | `status` |
| "save this to Notion" / "capture this conversation" | "move this chat to Notion" workflow — see `references/structuring-work.md` |

**The skill is the user's hands.** When in doubt, the agent asks: "Should I `<command equivalent>` for that?" before mutating. Trivial appends (a `log` entry during an open `discuss`, an `add-subtask` from an explicit "we'll need to") can proceed without asking each time.

---

## Bootstrapping

Fresh setup and migration from a prior hub: see `references/bootstrapping.md`.

---

## What this skill does NOT do

- **Does not auto-execute To-Do items.** `next` shows; only `start` flips status and loads brief.
- **Does not auto-promote rows to To-Do.** Every To-Do transition requires explicit user authorization (Gate 1).
- **Does not mark rows `Exec=Agent` without explicit authorization** (Gate 2).
- **Does not append `--go` to a `run` the user didn't write** (Gate 3).
- **Does not write content, deploy, or run any other skill.** The brief may point at another skill.
- **Does not delete content.** `kill` is archival; the row remains.
- **Does not commit or push to git** beyond `notion-pointers.json` (which scaffold writes).
- **Does not enforce subtask completion before parent done.** Surfaces a nudge, not a refusal.
- **Does not de-dup beyond Title-Jaccard 0.8 on `suggest`.** Manual Notion-UI rows bypass.
- **Does not auto-archive old discussion entries.** Brief assembler bounds agent context (latest entry only).
- **Does not run more than one `start` per task at a time.** `In Progress` is the lock.

---

## One-command summary

```
/agency-os suggest -> discuss -> log/add-subtask (clarify) -> approve -> start -> done
                                                                          ^       |
                                                                          |recur  |
                                                                          +-------+
```

Sync runs as preflight via `scripts/sync-tasks.py`, refreshing the local mirror at `state/tasks.json` incrementally. Notion is canonical; the mirror is the read path; the pointer file is the only repo binding. The DB grid stays clean; details fold; briefs stay bounded.
