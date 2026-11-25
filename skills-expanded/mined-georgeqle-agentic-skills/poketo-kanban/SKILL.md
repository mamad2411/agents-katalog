---
name: poketo-kanban
description: Manage Poketo kanban boards — list boards, view board state, create/update/move cards, manage lists. Use when the user wants to track tasks, view project status, or manage work items.
type: ops
version: v0.0
argument-hint: "<subcommand> [options] [--archive]"
allowed-tools: Bash(poketo *)
---

# Poketo Kanban — Board & Task Management

Invoke as `$poketo-kanban`.

Manage Poketo Work kanban boards directly from any session. All operations go through the poketo CLI gateway.

## Prerequisites

- `poketo` CLI installed and on PATH
- Authenticated: `poketo auth login` or `POKETO_API_KEY` env var set

## Process

1. **Parse subcommand** from `$ARGUMENTS`:
   - `boards` — list all boards
   - `board <id>` — view a board's lists and cards
   - `search --query "<term>"` — search cards across all boards
   - `create-card`, `update-card`, `move-card`, `done` — card mutations
   - `create-board`, `create-list` — board/list mutations

2. **Execute via CLI:**
   - Run the appropriate command via `poketo kanban <command> [options]`

3. **Present results:**
   - Parse JSON output and display in human-readable format.
   - After mutations, re-fetch the board to show updated state.

## Output Format

- For `boards`: table of board names and IDs
- For `board <id>`: each list as a column header with cards as bullet points (include done status, due dates, starred)
- For mutations: confirmation with created/updated entity details

## Constraints

- If output contains `{ "error": "..." }`, report the error to the user with remediation steps.
- `"Not authenticated"` → tell user to run `poketo auth login`
- `"Could not reach the gateway"` → tell user to check that the gateway is running and reachable
- After any mutation, re-fetch and display the updated board state.

## Archive Mode (`--archive`)

When `$ARGUMENTS` contains `--archive` (or starts with `archive`), archive old Done and Punt cards. Use `--days <N>` to override the 30-day default.

### Setup

Run board resolution: check `tasks/.kanban-board` for stored ID, validate via `poketo kanban board <id>`. If missing, match board names against `basename $(pwd)`. If no match, ask the user. If setup fails, report the error and stop — this operation requires a working kanban connection.

### Process

1. **Parse arguments**: Extract `--days <N>` from `$ARGUMENTS`. Default to 30.
2. **Fetch board state**: Run `poketo kanban board <id>` to get all lists and cards.
3. **Find archivable cards**: Cards in Done/Punt lists where age (from `updatedAt` or `createdAt`) exceeds the threshold. If none qualify, report and stop.
4. **Display candidates**: Show each card with list name, last update date, and age.
5. **Confirm with user**: Ask "Archive these N cards? (y/n)". If declined, stop.
6. **Archive cards**: Run `poketo kanban archive-card --id <card-id>` for each. Continue on individual failures.
7. **Report**: "Archived N cards (X from Done, Y from Punt)."

### Constraints
- Never archive without explicit user confirmation.
- Process Done cards first, then Punt — oldest first within each list.
- Only archive from Done and Punt lists.
- The `poketo kanban archive-card` command handles auto-creating the Archive list.


## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page at `alignment/poketo-kanban-{topic}.html`. Use a normalized topic slug derived from the app, feature, research subject, report subject, or output filename.

**Full content requirement.** The alignment page must contain the complete content of every proposed markdown deliverable -- every section, every finding, every detail, every list item. It is a thorough interactive review document, not a summary. Render the full deliverable content in clean, readable HTML with appropriate hierarchy, styling, and navigation. If the skill writes multiple scoped deliverables in one run, build one alignment page that contains all deliverables with anchor-linked navigation. Durable tracker artifacts, such as `research/assumption-tracker.md`, remain canonical markdown outputs but must also be fully rendered into the alignment page before approval.

**Dark-mode styling.** Use a dark color scheme by default. Base CSS variables: `--bg: #0d1117; --surface: #161b22; --border: #30363d; --text: #c9d1d9; --text-muted: #8b949e; --accent: #58a6ff; --green: #3fb950; --red: #f85149; --orange: #d29922; --purple: #bc8cff;`. Apply `background: var(--bg); color: var(--text);` on body. Use `--surface` for cards, nav, and table headers. Use `--border` for all borders. Use `--purple` for question blocks and gate headings. Use `--accent` for links and section headings. Keep headings `color: #fff` or `var(--accent)` for hierarchy. Question block backgrounds should use `#1c2333`.

**Alignment gates.** Treat gates as explicit review sections inside the HTML page. A gate blocks finalization until its required inline questions are answered and compiled into YAML. Include every gate that applies to the skill output, and include these gate types whenever relevant: evidence coverage, assumptions/confidence, scope/non-goals, candidate/verdict decisions, artifact destination, proposed file changes, coverage checkpoint, and post-approval route.

**Report-only research gates.** For report-only or pre-approval research skills, the alignment page must explicitly contain evidence coverage, assumptions/confidence, recommended path, proposed file changes, and approval gates before any canonical research, spec, or task file is created or updated.


**Required inline questions.** Each gate must contain at least one required inline question placed directly under the content it governs, inside a visually distinct question block. Each question must use radio-button inputs and include two standing options after the skill-generated choices: "Other / None of the above" backed by a multi-line text box for free-form input, and "Need clarification" backed by an optional notes box where the user can explain what is unclear. When any radio option other than "Other" or "Need clarification" is selected, show an optional "Additional notes" text box beneath it so the user can qualify their choice. Generate questions based on what genuinely needs user input -- do not add filler questions. Do not create a separate bottom "Decisions & Clarifications" section.

**Gate YAML contract.** At the bottom of the page, include a "Compile Answers" button that aggregates answers from all inline gate questions throughout the page, including free-text notes. The button remains disabled until every required question has a selection, shows a count of remaining unanswered questions, and scrolls to the first unanswered question if clicked early. When every question is answered, generate a structured YAML block with one item per gate answer using this stable shape: `section`, `gate_type`, `status` (`answered`, `other`, or `needs-clarification`), `answer`, optional `notes`, and optional `target_artifact` or `target_path` when the gate controls file output. After successful compilation, automatically attempt to copy the YAML to the clipboard with the Clipboard API, display copy status, and display the YAML in a read-only textarea with an explicit "Copy YAML" button. The copy button must retry clipboard copy when supported and fall back to selecting the textarea contents when clipboard access is unavailable or blocked.

**Pre-approval stop.** Before user approval, the next action is review of the HTML alignment page, not downstream routing. Ask the user to review the page and provide the compiled YAML answers. Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language until after compiled YAML has been provided and the approved artifacts have been written or updated.

**Diff highlighting on updates.** When the agent updates an existing alignment page after receiving compiled answers, highlight what changed since the previous version. The agent chooses inline annotation or side-by-side layout per situation.

**Archiving.** Before replacing an existing alignment page, archive it to `docs/history/archive/YYYY-MM-DD/HHMMSS/alignment/poketo-kanban-{topic}.html`.

**Browser open.** Attempt to open the resulting HTML page in the browser and report whether the open succeeded or was blocked. A blocked browser-open attempt does not make the skill fail when the files were written correctly.

## Default Shipping Contract

- **Default next-step routing:** when reporting completion, include either `Recommended next skill: <command>` or the two-line pair `**Next work:** <specific task or "none">` and `**Recommended next command:** <one command or route>` so the next operator has a concrete handoff.
- If this skill creates or modifies tracked repository files, finish by committing and pushing all intended changes to the repository primary branch (`main` when present, otherwise `master`) before stopping, even if the user did not explicitly ask for commit/push.
- Do not leave tracked changes or unpushed commits behind. If unrelated tracked work is already present, either include it in sensible commits too or stop and explain the blocker.
- This contract does not override stricter safety rules about secrets, destructive history changes, release publication/tag confirmation, or production deploy confirmation.
