---
name: guide
description: "Click-by-click instructions for manual blockers — DNS, OAuth, signups, and other GUI-dependent tasks"
type: analysis
version: v0.0
---

# Guide

Invoke as `$guide`.

Produce detailed, click-by-click instructions for human-only manual tasks that block automated progress — service signups, DNS configuration, OAuth credential creation with no authenticated CLI/API path, dashboard settings that cannot be scripted, production smoke checks needing a real account/device or human sign-off, and anything else that requires a third-party portal or subjective human judgment.

This skill is not for development-document bookkeeping. If the requested task is
auditing, reconciling, checking off, moving, or classifying entries in
`tasks/manual-todo.md`, `tasks/todo.md`, `tasks/record-todo.md`, or history
against repo reality, stop and route to `$reconcile-dev-docs fix tasks` or a
direct dev-doc audit instead.

This skill is also not for agent-executable work. If the task is repo edits,
SDK wiring, generated assets, local commands, tests, audits, or CLI/API work
with available authentication, stop and route it to `$run`, `$ship`, or the
specific implementation skill instead of producing click instructions.

## Workflow

1. **Find the blocker:**
   - If `$ARGUMENTS` is non-empty, use the provided text as the task description.
   - If `$ARGUMENTS` is empty, read `tasks/manual-todo.md` and find the first unchecked item (prefer items with `_(blocks: ...)_` annotations).
   - If `$ARGUMENTS` explicitly references `tasks/record-todo.md`, use that record item as the task description and produce instructions for satisfying its condition or collecting its evidence. Do not use record items by default.
   - If no task is found, ask the user what they need help with.

2. **Gather project context:**
   - Read `tasks/todo.md`, `tasks/roadmap.md`, and `CLAUDE.md` to understand what the manual task is for.
   - Search the codebase for references to the service or credentials (env var names, config keys) to identify exact values and output destinations.

3. **Research current instructions:**
   - Use web search to find up-to-date instructions for the specific service or platform.
   - Service UIs change frequently — always search rather than relying on prior knowledge.

4. **Produce click-by-click guide:**
   - Numbered steps with exact UI elements, fields, and project-specific values.
   - Group into logical phases. Note wait times (DNS propagation, approval queues).

5. **Show where to put results:**
   - For each output (API keys, tokens, URLs), specify the exact file path, variable name, and expected format.

6. **Offer to check off:**
   - When the user confirms completion, mark the item done in `tasks/manual-todo.md`.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page at `alignment/guide-{topic}.html`. Use a normalized topic slug derived from the app, feature, research subject, report subject, or output filename.

**Full content requirement.** The alignment page must contain the complete content of every proposed markdown deliverable -- every section, every finding, every detail, every list item. It is a thorough interactive review document, not a summary. Render the full deliverable content in clean, readable HTML with appropriate hierarchy, styling, and navigation. If the skill writes multiple scoped deliverables in one run, build one alignment page that contains all deliverables with anchor-linked navigation. Durable tracker artifacts, such as `research/assumption-tracker.md`, remain canonical markdown outputs but must also be fully rendered into the alignment page before approval.

**Dark-mode styling.** Use a dark color scheme by default. Base CSS variables: `--bg: #0d1117; --surface: #161b22; --border: #30363d; --text: #c9d1d9; --text-muted: #8b949e; --accent: #58a6ff; --green: #3fb950; --red: #f85149; --orange: #d29922; --purple: #bc8cff;`. Apply `background: var(--bg); color: var(--text);` on body. Use `--surface` for cards, nav, and table headers. Use `--border` for all borders. Use `--purple` for question blocks and gate headings. Use `--accent` for links and section headings. Keep headings `color: #fff` or `var(--accent)` for hierarchy. Question block backgrounds should use `#1c2333`.

**Alignment gates.** Treat gates as explicit review sections inside the HTML page. A gate blocks finalization until its required inline questions are answered and compiled into YAML. Include every gate that applies to the skill output, and include these gate types whenever relevant: evidence coverage, assumptions/confidence, scope/non-goals, candidate/verdict decisions, artifact destination, proposed file changes, coverage checkpoint, and post-approval route.

**Report-only research gates.** For report-only or pre-approval research skills, the alignment page must explicitly contain evidence coverage, assumptions/confidence, recommended path, proposed file changes, and approval gates before any canonical research, spec, or task file is created or updated.


**Required inline questions.** Each gate must contain at least one required inline question placed directly under the content it governs, inside a visually distinct question block. Each question must use radio-button inputs and include two standing options after the skill-generated choices: "Other / None of the above" backed by a multi-line text box for free-form input, and "Need clarification" backed by an optional notes box where the user can explain what is unclear. When any radio option other than "Other" or "Need clarification" is selected, show an optional "Additional notes" text box beneath it so the user can qualify their choice. Generate questions based on what genuinely needs user input -- do not add filler questions. Do not create a separate bottom "Decisions & Clarifications" section.

**Gate YAML contract.** At the bottom of the page, include a "Compile Answers" button that aggregates answers from all inline gate questions throughout the page, including free-text notes. The button remains disabled until every required question has a selection, shows a count of remaining unanswered questions, and scrolls to the first unanswered question if clicked early. When every question is answered, generate a structured YAML block with one item per gate answer using this stable shape: `section`, `gate_type`, `status` (`answered`, `other`, or `needs-clarification`), `answer`, optional `notes`, and optional `target_artifact` or `target_path` when the gate controls file output. After successful compilation, automatically attempt to copy the YAML to the clipboard with the Clipboard API, display copy status, and display the YAML in a read-only textarea with an explicit "Copy YAML" button. The copy button must retry clipboard copy when supported and fall back to selecting the textarea contents when clipboard access is unavailable or blocked.

**Pre-approval stop.** Before user approval, the next action is review of the HTML alignment page, not downstream routing. Ask the user to review the page and provide the compiled YAML answers. Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language until after compiled YAML has been provided and the approved artifacts have been written or updated.

**Diff highlighting on updates.** When the agent updates an existing alignment page after receiving compiled answers, highlight what changed since the previous version. The agent chooses inline annotation or side-by-side layout per situation.

**Archiving.** Before replacing an existing alignment page, archive it to `docs/history/archive/YYYY-MM-DD/HHMMSS/alignment/guide-{topic}.html`.

**Browser open.** Attempt to open the resulting HTML page in the browser and report whether the open succeeded or was blocked. A blocked browser-open attempt does not make the skill fail when the files were written correctly.

## Constraints

- Always web search — never produce instructions from memory alone.
- Use project-specific values, not generic placeholders.
- Read-only except for checking off items in `tasks/manual-todo.md`.
- Do not check off or modify `tasks/record-todo.md`; record items are advisory unless a separate workflow updates them.
- One task at a time.
- No task-ledger reconciliation — do not produce a guide for requests such as
  "reconcile manual-todo", "audit stale manual tasks", or "check off completed
  todo items". Route those to `$reconcile-dev-docs fix tasks` or a direct
  dev-doc audit.
- No agent-executable work — do not produce a guide for repo edits, local
  commands, SDK adoption, generated assets, test runs, Lighthouse/Playwright
  checks, or authenticated CLI/API operations.
- Don't execute the task — produce instructions for the user to follow.
