---
name: todos
description: Own the To-Do Protocol - user tasks in vault tasks.md files, optional Notion Kanban mirror, status reporting. Actions - new (create a task, user confirmation required), sync, push, pull, board (Notion mode only), status, overview. Fully functional without Notion (vault-only mode).
---

# Task

Execute the requested action: $ARGUMENTS

Calling rule: `/todos <action> <arguments>`.

**Module check:** read `axiom-config.md`. If M3-todos is inactive, reply in one line that the module is inactive and offer `/axiom activate M3` — execute nothing. Note the mode: **vault-only** or **notion**.

If the requested action is ambiguous or contradictory, do NOT guess: flag the ambiguity and ask for clarification before executing.

Core principles (To-Do Protocol, root CLAUDE.md):

- **The task list is the user's to-do list** — only tasks the user acts on become task lines/cards.
- **Confirmation gate: never create a task for the user without explicit approval.** Propose short name + description, wait for OK, only then allocate the ID and write the line.
- **Agent tasks** (my own work items) live under a `## Agent` heading at the end of the WP's `tasks.md` — IDs like any task, never mirrored externally.
- **One task may bundle several items.** A task is one line with an ID and a short name; the individual points go into the description, not into separate tasks. Bundle vs. split: see the format section.
- **Reference, don't restate.** Where the detail already lives in a deliverable or vault page, the description summarises each point in a line or two and points at the document.
- **Notion mode only: board wins status, vault wins wording.** Card descriptions are write-once at creation. Sync is on-demand only. Cards mirror task lines in WP `tasks.md` files only — never structural pages.

## Mode behavior

| Action | vault-only | notion |
| :--- | :--- | :--- |
| `new`, `status` | Full function | Full function |
| `sync`, `push`, `pull`, `board` | One-line reply: needs the Notion mirror — offer to check for the connector and switch modes | Full function |

If the mode is vault-only but a Notion connector is detected during any action, mention once that the Kanban mirror is available (`/axiom activate M3` handles the switch); do not switch silently.

---

## If action is empty

Describe this skill: its purpose and the actions table from "overview". Do not execute anything.

## If action is "overview" (or unknown)

| Argument | Action |
| :--- | :--- |
| `new <wp> <task>` | Draft short name + description (bundling related items) → user confirmation → ID, task line, card if Notion mode |
| `sync [project]` | Notion mode: full sync — pull, then push. No project named → every project with a board |
| `push [project]` | Notion mode: vault → board — create cards for new user tasks, update card titles from vault wording |
| `pull [project]` | Notion mode: board → vault — update task status from the board (per-card, see Notes) |
| `board <project>` | Notion mode: create the project's Kanban board + its registry page |
| `status [project or topic]` | Status report — no argument = full report, argument = narrow answer |
| `overview` | This table |

If the action was unknown, say so first, then show the table.

---

## Board registry (Notion mode)

Each synced project has `vault/projects/<project>/board.md` holding its board URL, database ID, and data source ID. A project without `board.md` has no board — suggest `/todos board <project>` instead of guessing.

## Task line format (in WP tasks.md)

| Vault line | Status |
| :--- | :--- |
| `- [ ] Task text` | Not started |
| `- [/] Task text` | In progress |
| `- [x] Task text (YYYY-MM-DD)` | Done (date = completion) |

- Task line: `- [ ] XX-WW-TT — <short name, 3–6 words>` (Task ID Protocol, root CLAUDE.md). The short name carries no context.
- Description: indented sub-bullet directly under the task line — full context, acceptance criteria, references. Never parsed as a task line. In Notion mode it becomes the card body at creation — write-once, never synced afterwards; the vault copy stays the source of truth.
- Optional due date inside the text: `(due YYYY-MM-DD)` → card Due property in Notion mode.
- Card reference (Notion mode): HTML comment at line end — `<!-- notion:<page-id> -->`. A task without it has no card yet.
- Tasks under a `## Agent` heading are agent tasks: skipped by push and sync, no card reference ever added.

### Bundling

A set of related items becomes **one task**, not one task per item — the line stays a short name with its ID, and the items are enumerated in the description.

| Bundle when | Split when |
| :--- | :--- |
| The items share one owner | An item has its own owner |
| They would plausibly be worked in one sitting | An item needs its own due date |
| They came out of one analysis and share its context | An item blocks something else, or something else waits on it |

In the description, give each item a number, a one-line statement of what it is, and the concrete next action. Where an item is already written up elsewhere, add the section reference rather than copying the reasoning across.

---

## If action is "new"

1. Check $ARGUMENTS (after "new"): a WP (folder name or unambiguous fragment) and the task intent. No WP identifiable → ask which WP, never guess. No suitable WP exists → suggest creating one first (`/project new WP`), per the hierarchy protocol.
2. Draft the task: short name (3-6 words) + description (full context, acceptance criteria, references). Decide who acts: the user → user task; me → `## Agent` section. **Decide bundle or split here** — if the intent covers several related items, draft one task enumerating them.
3. **Present the draft and STOP — wait for explicit approval.** No ID is allocated, nothing is written before the OK.
4. On approval: allocate the task number from `ids.md` (the WP's `Next task`, then bump it), write the task line + indented description sub-bullet to the WP's `tasks.md` (user tasks above `## Agent`, agent tasks below it), bump the file's `updated:` date.
5. Notion mode, user task, board exists: create the card (see push, steps 3-4) with the description as card body. **If the WP's select option does not exist on the board yet, create it first** (see Notes). Vault-only mode, agent task, or no board: done after the vault write.

## If action is "push" (Notion mode)

1. Resolve projects (given or all registered) and read each `board.md` for IDs.
2. Collect every WP `tasks.md` under `vault/projects/<project>/`. The card's WP select value is the WP folder name **with the `WW-` prefix stripped** (folder `04-market-analysis` → option `market-analysis`); the number already rides in the card Name via the ID prefix. **Skip everything under a `## Agent` heading.** Skip indented sub-bullets.
3. For each user task **without** a card reference: create a card (`notion-create-pages`, parent = data source ID) with Name (task text without HTML comments — keep the `XX-WW-TT` ID prefix), Status per the checkbox, WP, and Due if given. The indented description sub-bullet becomes the card body — write-once at creation. WP options missing from the board must be added before the card is created (see Notes).
4. Write the returned page ID back into the task line as `<!-- notion:<id> -->`.
5. For each task **with** a reference whose wording differs from the card Name: update the card Name (vault wins wording). Never change card status on push.
6. Report per WP: cards created / retitled / unchanged.

## If action is "pull" (Notion mode)

1. Resolve projects and IDs as in "push".
2. Collect every task line with a `<!-- notion:<id> -->` reference; fetch each card individually (`notion-fetch` on the page ID — bulk queries may be plan-gated, see Notes).
3. For each card: set the checkbox to the card's status (`[ ]` / `[/]` / `[x]`); a newly Done task gets a completion date. Board wins status; wording stays untouched.
4. A fetch that returns a deleted/inaccessible card: flag it, never delete the vault task silently.
5. If bulk queries are unavailable on the user's Notion plan, cards created directly on the board cannot be detected — remind the user to name them for a manual carry: WP set → append as a new task line with reference and a freshly allocated ID; no WP → ask where to file.
6. Bump the `updated:` frontmatter date of every changed `tasks.md`; report the changes.

## If action is "sync" (Notion mode)

1. Run "pull", then "push" — status changes land first, then new cards and retitles.

## If action is "board" (Notion mode)

1. Requires a project name; verify `vault/projects/<project>/` exists. If `board.md` already exists: stop and report.
2. Ask the user for (or create) a parent Notion page to hold the boards; store its ID in the registry. Create a database titled `<project>` under it: `"Name" TITLE, "Status" STATUS, "Due" DATE, "WP" SELECT(<one option per existing WP>), "URL" URL`.
3. Create views: Kanban (board, `GROUP BY "Status"`), open-tasks table, finished-tasks table, Calendar (`CALENDAR BY "Due"`), Timeline (`TIMELINE BY "Due"`).
4. Write the registry page `vault/projects/<project>/board.md` (board URL, database ID, data source ID, parent page ID) and update `vault/index.md`.
5. Tell the user which settings need a one-time manual click (see MCP limits in Notes).

## If action is "status"

1. No argument → full report:
   1. Read `vault/index.md`, then `vault/log.md` (last 20 entries or since the user's last session).
   2. For each active project, read `vault/projects/<name>/status.md` and the `tasks.md` of its WPs.
   3. Notion mode with boards: offer to pull current board states first (`/todos pull`).
   4. Report, in this order and briefly: **Active projects** (one line each: state, blocker if any) · **Recent activity** (notable log entries, grouped) · **Open items** (tasks open/doing, decisions waiting on the user) · **Suggested next steps** (max 3, most impactful first).
2. With argument → quick: read only the relevant vault pages and answer the narrow question. No full report.

---

## After any action

- Append to `vault/log.md`; update `vault/index.md` if pages were added or removed. Exception: status reports are read-only — do not log them.
- Update the `updated:` date in every changed vault page.

## Notes — Notion MCP specifics (Notion mode only)

- Card properties: `"Name"` (title); `"Status"` one of `"Not started"` / `"In progress"` / `"Done"`; `"WP"` (select — WP folder name **without** its `WW-` prefix); `"userDefined:URL"` (url); due date via expanded columns `"date:Due:start"` (ISO `YYYY-MM-DD`) with `"date:Due:is_datetime": 0`.
- Vocabulary: vault "To-Do" = board "Not started" — treat as the same state.
- MCP limits: status option names are not settable via DDL (a new STATUS column always starts with "Not started"); view filters on status properties are silently dropped by the view DSL. Both are one-time manual clicks in the Notion UI.
- **Select options ARE settable via API**: `notion-update-data-source` with `ALTER COLUMN "WP" SET SELECT('opt':color, ...)`. **Restate every existing option in the statement** — `SET` replaces the option list wholesale, so any option left out is dropped from the property and from the cards using it. Fetch the data source first, copy the current options with their colours, append the new one.
- Plan gate: `notion-query-data-sources` (bulk board query) may require a paid Notion plan with Notion AI. Where unavailable, pull works **per-card** via `notion-fetch` on the stored `<!-- notion:id -->`; board-only cards and cards deleted on the board go undetected until a manual carry. Verify once per workspace and note the result in the first `board.md`.
- Conflict rules: board wins status; vault wins wording; card descriptions are write-once at creation.
