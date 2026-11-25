---
name: delegate
description: Live in-session delegation from Claude to Codex via the approval/delegation packet contract
type: shipping
version: v0.0
argument-hint: "[target-skill] [--allow-dirty <glob>] [--inline-fallback]"
---

# Delegate

Delegate the next step's execution to Codex **live, inside the current Claude session**. Produces an `approved` packet via the shared contract (same helpers `/handoff --target=codex` uses), then invokes Codex synchronously with `codex exec "<target-skill> --execute-approved"`. Claude stays the orchestrator; Codex executes; Claude resumes once Codex returns.

Unlike `/handoff --target=codex` (async — user resumes later), `/delegate` is live cross-CLI transport. The target skill defaults to `$run`; other executor skills (e.g. `$ship`) may be named but `$run` is the primary use case.

## Mode requirement

`/delegate` is **`hybrid`-only by design**. `claude-only` has no executor to delegate to; `codex-only` plans in Codex directly. In either non-hybrid mode, the skill exits non-zero with a `mode-mismatch:` reason and touches no packet state.

## Transport dependency

`/delegate` requires the `codex` binary on `PATH`. If missing (or auth-failed, or the start marker never prints), the skill falls cleanly into the **pre-start-failure** branch of the fallback matrix — it does not crash, and the packet stays at `approved`.

## Process

1. **Resolve agent mode** via `./scripts/agent-mode.sh`. If the effective mode is anything other than `hybrid`, exit non-zero with a `mode-mismatch:` message naming the resolved mode. Do not touch the packet.

2. **Parse arguments** from `$ARGUMENTS`:
   - First positional token (if any) is the target skill; defaults to `$run`.
   - Collect repeatable `--allow-dirty <glob>` flags (shell-glob semantics, same as `scripts/approved-plan.sh check`). Note: back-to-back hybrid cycles rewrite the `tasks/approved-plan.md` mirror on each `consume`; commit it between cycles, or pass `--allow-dirty tasks/approved-plan.md` so the next `draft` tolerates the uncommitted mirror.
   - `--inline-fallback` auto-selects inline Claude execution in the pre-start-failure branch without prompting.

3. **Derive `phase` / `step` / `title` from `tasks/todo.md`**, using the same rules as `/handoff --target=codex`:
   - First unchecked `- [ ]` under the `### Active Step Plan` block.
   - Fallback: first unchecked `- [ ]` under the current `## Phase N` header.
   - Parse `Phase N` and `Step N.X` tokens from the surrounding context; the checkbox text (stripped of `- [ ] **Step N.X** — `) becomes `title`.

4. **Produce the approval packet**:
   1. `./scripts/approved-plan.sh draft --phase "Phase N" --step "Step N.X" --title "<title>"` plus any `--allow-dirty <glob>` flags. Surface the helper's single-line failure reason verbatim if it fails.
   2. Pretty-print the drafted packet (`jq . .agents/approved-plan.json`).
   3. Ask exactly one concise question: *"Approve this packet for Codex execution via /delegate?"*
   4. On yes → `./scripts/approved-plan.sh approve`. On no → leave at `draft` and stop; the user can approve later or discard with `./scripts/approved-plan.sh supersede`.

5. **Invoke Codex synchronously**:
   - Record a start-marker timestamp (ISO-8601 UTC) before the exec call so the fallback matrix can classify outcomes.
   - Shell out to `codex exec "<target-skill> --execute-approved"`. Capture stdout, stderr, and the exit code.
   - The Step 4 consumer (`$run --execute-approved`) is what actually runs `scripts/approved-plan.sh check && consume` inside Codex. `/delegate` is transport only.

6. **Classify via the safe-fallback matrix — never blind-retry**:

   - **Pre-start failure** — `codex` binary not found, auth failure, or the start marker was never printed by Codex before exit:
     - Packet stays at `approved` (no writer ran).
     - Offer two options: (a) run inline in Claude (same session, no CLI boundary), or (b) keep the packet `approved` for later manual `$run --execute-approved` in Codex.
     - If `--inline-fallback` was passed, auto-select (a) without prompting.
     - Under an `agent-team` execution profile, inline fallback is a **downgrade** requiring explicit interactive confirmation unless `--inline-fallback` is already on the command line.

   - **Success** — Codex exited 0, printed `Approved packet consumed: …`, and `tasks/approved-plan.md` reports `lifecycle: consumed`:
     - Step 4's `consume` already flipped `approved → consumed`.
     - Read `tasks/approved-plan.md` to confirm `lifecycle: consumed`. If confirmed, report success and hand back to the user.
     - If the mirror does not report `consumed`, treat as the ambiguous case below.

   - **Ambiguous** — non-zero exit, timeout, or crash after the start marker printed (Codex may have started mutating state):
     - Call `./scripts/approved-plan.sh mark-uncertain`. The packet lifecycle becomes `uncertain`.
     - Prompt the user with three explicit options: *inspect repo state manually / discard the packet via `./scripts/approved-plan.sh supersede` / continue inline in Claude from the current repo state*.
     - **Never blind-retry `codex exec` on the same packet.** Re-executing against a packet whose consumer may have partially mutated state risks double-execution.

7. **Report** the classified outcome, the final lifecycle, and whatever the user chose from the fallback prompt.

## Constraints

- **Hybrid-only.** Non-hybrid modes exit with `mode-mismatch:` before any packet operation.
- **Never blind-retry cross-CLI.** The invariant. Ambiguous failures always go through `mark-uncertain` + explicit user prompt.
- **Contract is frozen.** Do not edit `docs/operating-modes.md`, `specs/approved-plan.schema.json`, or add new lifecycle states / freshness checks. `uncertain` is already in the schema enum; Step 6 is just its first writer.
- **`mark-uncertain` is only valid from `approved`.** The helper rejects `draft`, `consumed`, `stale`, `superseded`, and `uncertain` source states.
- **`codex` binary is a transport dependency.** Fall cleanly into pre-start-failure if missing; do not crash.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page at `alignment/delegate-{topic}.html`. Use a normalized topic slug derived from the app, feature, research subject, report subject, or output filename.

**Full content requirement.** The alignment page must contain the complete content of every proposed markdown deliverable -- every section, every finding, every detail, every list item. It is a thorough interactive review document, not a summary. Render the full deliverable content in clean, readable HTML with appropriate hierarchy, styling, and navigation. If the skill writes multiple scoped deliverables in one run, build one alignment page that contains all deliverables with anchor-linked navigation. Durable tracker artifacts, such as `research/assumption-tracker.md`, remain canonical markdown outputs but must also be fully rendered into the alignment page before approval.

**Dark-mode styling.** Use a dark color scheme by default. Base CSS variables: `--bg: #0d1117; --surface: #161b22; --border: #30363d; --text: #c9d1d9; --text-muted: #8b949e; --accent: #58a6ff; --green: #3fb950; --red: #f85149; --orange: #d29922; --purple: #bc8cff;`. Apply `background: var(--bg); color: var(--text);` on body. Use `--surface` for cards, nav, and table headers. Use `--border` for all borders. Use `--purple` for question blocks and gate headings. Use `--accent` for links and section headings. Keep headings `color: #fff` or `var(--accent)` for hierarchy. Question block backgrounds should use `#1c2333`.

**Alignment gates.** Treat gates as explicit review sections inside the HTML page. A gate blocks finalization until its required inline questions are answered and compiled into YAML. Include every gate that applies to the skill output, and include these gate types whenever relevant: evidence coverage, assumptions/confidence, scope/non-goals, candidate/verdict decisions, artifact destination, proposed file changes, coverage checkpoint, and post-approval route.

**Report-only research gates.** For report-only or pre-approval research skills, the alignment page must explicitly contain evidence coverage, assumptions/confidence, recommended path, proposed file changes, and approval gates before any canonical research, spec, or task file is created or updated.


**Required inline questions.** Each gate must contain at least one required inline question placed directly under the content it governs, inside a visually distinct question block. Each question must use radio-button inputs and include two standing options after the skill-generated choices: "Other / None of the above" backed by a multi-line text box for free-form input, and "Need clarification" backed by an optional notes box where the user can explain what is unclear. When any radio option other than "Other" or "Need clarification" is selected, show an optional "Additional notes" text box beneath it so the user can qualify their choice. Generate questions based on what genuinely needs user input -- do not add filler questions. Do not create a separate bottom "Decisions & Clarifications" section.

**Gate YAML contract.** At the bottom of the page, include a "Compile Answers" button that aggregates answers from all inline gate questions throughout the page, including free-text notes. The button remains disabled until every required question has a selection, shows a count of remaining unanswered questions, and scrolls to the first unanswered question if clicked early. When every question is answered, generate a structured YAML block with one item per gate answer using this stable shape: `section`, `gate_type`, `status` (`answered`, `other`, or `needs-clarification`), `answer`, optional `notes`, and optional `target_artifact` or `target_path` when the gate controls file output. After successful compilation, automatically attempt to copy the YAML to the clipboard with the Clipboard API, display copy status, and display the YAML in a read-only textarea with an explicit "Copy YAML" button. The copy button must retry clipboard copy when supported and fall back to selecting the textarea contents when clipboard access is unavailable or blocked.

**Pre-approval stop.** Before user approval, the next action is review of the HTML alignment page, not downstream routing. Ask the user to review the page and provide the compiled YAML answers. Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language until after compiled YAML has been provided and the approved artifacts have been written or updated.

**Diff highlighting on updates.** When the agent updates an existing alignment page after receiving compiled answers, highlight what changed since the previous version. The agent chooses inline annotation or side-by-side layout per situation.

**Archiving.** Before replacing an existing alignment page, archive it to `docs/history/archive/YYYY-MM-DD/HHMMSS/alignment/delegate-{topic}.html`.

**Browser open.** Attempt to open the resulting HTML page in the browser and report whether the open succeeded or was blocked. A blocked browser-open attempt does not make the skill fail when the files were written correctly.

## Default Shipping Contract

- **Default next-step routing:** when reporting completion, include either `Recommended next skill: <command>` or the two-line pair `**Next work:** <specific task or "none">` and `**Recommended next command:** <one command or route>` so the next operator has a concrete handoff.
- If this skill creates or modifies tracked repository files, finish by committing and pushing all intended changes to the repository primary branch (`main` when present, otherwise `master`) before stopping, even if the user did not explicitly ask for commit/push.
- Do not leave tracked changes or unpushed commits behind. If unrelated tracked work is already present, either include it in sensible commits too or stop and explain the blocker.
- This contract does not override stricter safety rules about secrets, destructive history changes, release publication/tag confirmation, or production deploy confirmation.
