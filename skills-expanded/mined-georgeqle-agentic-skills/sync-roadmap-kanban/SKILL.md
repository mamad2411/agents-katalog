---
name: sync-roadmap-kanban
description: Reconcile kanban board state with roadmap docs and codebase reality — sync cards, steps, and git history so they agree.
type: ops
version: v0.0
allowed-tools: Bash(poketo *), Bash(git *)
---

# Sync Roadmap ↔ Kanban

Reconcile the kanban board, roadmap docs, and codebase state so all three reflect the same reality.

## Process

### 1. Pull latest

Run `/sync` first. If there are merge conflicts, **stop** and report them — do not proceed with reconciliation on a dirty tree.

### 2. Read kanban state

```bash
poketo kanban boards
```

**Board auto-detection:**

1. Run `boards` to get the list of all boards (JSON with `id` and `name` fields).
2. If `tasks/.kanban-board` exists, read it (single line containing a board ID). Check that the ID appears in the boards list. If valid, use it. If stale (ID not found), delete the file and continue to step 3.
3. If no mapping file: compare each board name against `basename $(pwd)` — case-insensitive substring match.
4. If exactly one board matches → use it. Save the board ID to `tasks/.kanban-board`.
5. If zero or multiple matches → list the boards and ask the user to pick one. Save their choice to `tasks/.kanban-board`.
6. Run `poketo kanban board <id>` to get the full board state (all lists and cards).

`tasks/.kanban-board` should be committed to git so all devices share the mapping.

### 3. Read roadmap docs

- Read `tasks/roadmap.md` (full phased plan).
- Read `tasks/todo.md` (current phase steps).
- Read `tasks/manual-todo.md` (if it exists — manual tasks for the current phase).
- Read `tasks/record-todo.md` and `tasks/recurring-todo.md` only for advisory counts. Do not create ordinary Todo cards from these files unless an item has already been promoted into `tasks/todo.md`.
- Build a list of all roadmap items with their status (checked/unchecked).

### 4. Read codebase reality

- Run `git log --oneline -30` to see recent commits.
- For each roadmap item that claims to be done (checked) or has a "done" kanban card, verify the deliverable exists:
  - If the item references a file or directory, check it exists.
  - If the item references a feature, grep for key identifiers.
  - If verification is ambiguous, flag it rather than assuming.

### 5. Reconcile

Apply these rules in order:

**Rule 1 — Kanban done + code confirms → mark roadmap complete**
Cards in a "Done" list whose deliverables are verified in the codebase → check off the corresponding roadmap/todo item if not already checked.

**Rule 2 — Roadmap done + code confirms → move kanban card to Done**
Roadmap items that are checked off and verified in code, but their kanban card is not in "Done" → move the card to the Done list.

**Rule 3 — New roadmap items with no card → create cards**
Roadmap steps or phases that have no matching kanban card → create a card in the appropriate list:
- Unchecked items → "Backlog" or first non-Done list
- Items in the current phase's todo → "In Progress" list (if one exists)

**Rule 4 — Orphaned kanban cards → flag**
Cards on the board that don't correspond to any roadmap item → report as orphaned. Do NOT delete them — the user may want to add them to the roadmap or archive them.

**Rule 5 — Claimed done but code doesn't support → flag as discrepancy**
Items marked done (in roadmap or kanban) but whose deliverables cannot be verified in the codebase → report as discrepancies. Do NOT uncheck or move them — let the user decide.

### 6. Apply changes

- **Kanban mutations:** Use the poketo CLI to create cards, move cards, or mark cards done.
  ```bash
  poketo kanban create-card --board <id> --list <list-id> --name "Step name" --description "Details"
  poketo kanban move-card --id <card-id> --list <done-list-id>
  poketo kanban done --id <card-id>
  ```
- **Roadmap doc edits:** Use Edit to check off completed items in `tasks/roadmap.md` and `tasks/todo.md`.
- After all mutations, re-fetch the board to confirm the final state.

### 7. Report

Output a summary with these sections:

**Synced:**
- Items checked off in roadmap (list them)
- Cards moved to Done (list them)
- Cards created (list them)

**Discrepancies (needs human judgment):**
- Items claimed done but not verified in code
- Orphaned kanban cards with no roadmap match

**Board state:** Show the updated board (lists and cards).

**Roadmap state:** Show current phase progress (e.g., "Phase 1: 2/3 steps complete"). If `tasks/manual-todo.md` exists, include manual task status (e.g., "Manual tasks: 1/3 complete"). If advisory task files exist, include record/recurring counts separately.

## Constraints

- Do NOT auto-resolve discrepancies — always report and let the user decide.
- Do NOT delete kanban cards. Move or flag only.
- Do NOT force-push or rewrite git history.
- Do NOT modify code — this skill only syncs metadata (docs and board state).
- Do NOT proceed if the working tree has merge conflicts from the sync step.
- Card-to-roadmap matching is by name similarity. Use fuzzy matching (the card name should contain key words from the roadmap step). When ambiguous, ask rather than guess.
- If the poketo CLI is not available or fails, report the error and stop.


## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page at `alignment/sync-roadmap-kanban-{topic}.html`. Use a normalized topic slug derived from the app, feature, research subject, report subject, or output filename.

**Full content requirement.** The alignment page must contain the complete content of every proposed markdown deliverable -- every section, every finding, every detail, every list item. It is a thorough interactive review document, not a summary. Render the full deliverable content in clean, readable HTML with appropriate hierarchy, styling, and navigation. If the skill writes multiple scoped deliverables in one run, build one alignment page that contains all deliverables with anchor-linked navigation. Durable tracker artifacts, such as `research/assumption-tracker.md`, remain canonical markdown outputs but must also be fully rendered into the alignment page before approval.

**Dark-mode styling.** Use a dark color scheme by default. Base CSS variables: `--bg: #0d1117; --surface: #161b22; --border: #30363d; --text: #c9d1d9; --text-muted: #8b949e; --accent: #58a6ff; --green: #3fb950; --red: #f85149; --orange: #d29922; --purple: #bc8cff;`. Apply `background: var(--bg); color: var(--text);` on body. Use `--surface` for cards, nav, and table headers. Use `--border` for all borders. Use `--purple` for question blocks and gate headings. Use `--accent` for links and section headings. Keep headings `color: #fff` or `var(--accent)` for hierarchy. Question block backgrounds should use `#1c2333`.

**Alignment gates.** Treat gates as explicit review sections inside the HTML page. A gate blocks finalization until its required inline questions are answered and compiled into YAML. Include every gate that applies to the skill output, and include these gate types whenever relevant: evidence coverage, assumptions/confidence, scope/non-goals, candidate/verdict decisions, artifact destination, proposed file changes, coverage checkpoint, and post-approval route.

**Report-only research gates.** For report-only or pre-approval research skills, the alignment page must explicitly contain evidence coverage, assumptions/confidence, recommended path, proposed file changes, and approval gates before any canonical research, spec, or task file is created or updated.


**Required inline questions.** Each gate must contain at least one required inline question placed directly under the content it governs, inside a visually distinct question block. Each question must use radio-button inputs and include two standing options after the skill-generated choices: "Other / None of the above" backed by a multi-line text box for free-form input, and "Need clarification" backed by an optional notes box where the user can explain what is unclear. When any radio option other than "Other" or "Need clarification" is selected, show an optional "Additional notes" text box beneath it so the user can qualify their choice. Generate questions based on what genuinely needs user input -- do not add filler questions. Do not create a separate bottom "Decisions & Clarifications" section.

**Gate YAML contract.** At the bottom of the page, include a "Compile Answers" button that aggregates answers from all inline gate questions throughout the page, including free-text notes. The button remains disabled until every required question has a selection, shows a count of remaining unanswered questions, and scrolls to the first unanswered question if clicked early. When every question is answered, generate a structured YAML block with one item per gate answer using this stable shape: `section`, `gate_type`, `status` (`answered`, `other`, or `needs-clarification`), `answer`, optional `notes`, and optional `target_artifact` or `target_path` when the gate controls file output. After successful compilation, automatically attempt to copy the YAML to the clipboard with the Clipboard API, display copy status, and display the YAML in a read-only textarea with an explicit "Copy YAML" button. The copy button must retry clipboard copy when supported and fall back to selecting the textarea contents when clipboard access is unavailable or blocked.

**Pre-approval stop.** Before user approval, the next action is review of the HTML alignment page, not downstream routing. Ask the user to review the page and provide the compiled YAML answers. Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language until after compiled YAML has been provided and the approved artifacts have been written or updated.

**Diff highlighting on updates.** When the agent updates an existing alignment page after receiving compiled answers, highlight what changed since the previous version. The agent chooses inline annotation or side-by-side layout per situation.

**Archiving.** Before replacing an existing alignment page, archive it to `docs/history/archive/YYYY-MM-DD/HHMMSS/alignment/sync-roadmap-kanban-{topic}.html`.

**Browser open.** Attempt to open the resulting HTML page in the browser and report whether the open succeeded or was blocked. A blocked browser-open attempt does not make the skill fail when the files were written correctly.

## Default Shipping Contract

- **Default next-step routing:** when reporting completion, include either `Recommended next skill: <command>` or the two-line pair `**Next work:** <specific task or "none">` and `**Recommended next command:** <one command or route>` so the next operator has a concrete handoff.
- If this skill creates or modifies tracked repository files, finish by committing and pushing all intended changes to the repository primary branch (`main` when present, otherwise `master`) before stopping, even if the user did not explicitly ask for commit/push.
- Do not leave tracked changes or unpushed commits behind. If unrelated tracked work is already present, either include it in sensible commits too or stop and explain the blocker.
- This contract does not override stricter safety rules about secrets, destructive history changes, release publication/tag confirmation, or production deploy confirmation.
