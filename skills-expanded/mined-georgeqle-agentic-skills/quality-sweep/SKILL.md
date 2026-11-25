---
name: quality-sweep
description: Audit and implement behavior-preserving cleanup across types, dead code, dependencies, errors, and comments
type: execution
version: v0.0
argument-hint: "[audit|fix|full] [optional: package, app, directory, or domain]"
---

# Quality Sweep

Invoke as `$quality-sweep`.

Use this skill when a project needs a behavior-preserving code quality cleanup campaign across duplication, type hygiene, dead code, dependency boundaries, defensive error handling, legacy paths, and comments. This skill orchestrates cleanup work; use narrower skills like `extract-shared-types`, `dead-code`, `slim-audit`, `hygiene`, `spec-drift`, and `regression-check` when the user asks for only one of those concerns.

## Process

1. **Select mode and scope.**
   - Parse `$ARGUMENTS` for mode: `audit`, `fix`, or `full`.
   - Default to `audit` when no mode is provided.
   - Treat remaining arguments as the target scope: package, app, directory, or domain.
   - If no scope is provided, inspect the repository and choose the smallest coherent scope before broadening.

2. **Establish baseline and context.**
   - Read project instructions, manifests, package configs, path aliases, lint/typecheck/test/build scripts, and relevant docs.
   - Read specs, roadmap/todo/history, changelogs, ADRs, or design notes when present.
   - In `fix` or `full`, run or record the narrowest relevant baseline checks available before edits.
   - Respect documented trade-offs and intentional architecture. Do not report documented decisions as cleanup targets.

3. **Run audit lanes.**
   - **Duplication:** find duplicate or near-duplicate code where consolidation reduces coupling, maintenance cost, or complexity.
   - **Shared types:** find type definitions that should move to a shared boundary; follow `extract-shared-types` rules for any implementation.
   - **Unused code:** use code search and available tools such as `knip` to find unused exports, orphaned files, stale dependencies, and unreachable branches.
   - **Circular dependencies:** use code search and available tools such as `madge` to identify dependency cycles and import-boundary issues.
   - **Weak types:** find unsafe `any` and unjustified weak typing. Preserve `unknown` at trust boundaries unless a stronger validated type exists.
   - **Error handling:** audit `try`/`catch` and defensive patterns. Preserve boundary handling, parsing, cleanup, rollback, external-service handling, and error translation.
   - **Legacy paths:** find deprecated, migration, compatibility, fallback, and alternate code paths that may now be obsolete.
   - **Comments and stubs:** remove or rewrite AI slop, stale comments, in-motion notes, stubs, larp, and comments that describe previous work instead of current behavior.

4. **Triage every finding.**
   - `Safe to Fix`: behavior-preserving, statically supported, verified by code search, not public-API-sensitive, and independently revertible.
   - `Needs Investigation`: plausible but ambiguous, migration-sensitive, weakly covered, or dependent on product intent.
   - `Do Not Change`: documented decision, necessary fallback, valid boundary handling, or readability-preserving duplication.
   - Re-read the relevant source before finalizing a finding. Drop findings that cannot be reconfirmed.

5. **Use subagents only for audit-first lanes.**
   - If the user explicitly requests subagents, or the mode is `full` and the active environment permits subagents, assign lanes as research tasks first.
   - Subagents should report findings and recommendations before edits.
   - The main agent owns final triage, integration, edits, and verification.
   - Direct subagent edits are allowed only when the main agent assigns disjoint file or path ownership.

6. **Implement only approved safe cleanup in `fix` or `full`.**
   - Do not modify files in `audit` mode.
   - Batch changes by lane or subsystem.
   - Avoid broad abstractions unless they reduce real complexity or coupling.
   - Do not remove public import paths, compatibility shims, migrations, or fallbacks unless evidence shows they are obsolete.
   - Do not replace `unknown` with weaker or speculative types.
   - Do not remove error handling that defines a clear boundary, adds actionable context, performs cleanup, or preserves system integrity.
   - Re-run the narrowest relevant validation after each meaningful batch.

7. **Verify and report.**
   - Run relevant typecheck, lint, tests, build, dead-code checks, and circular-dependency checks when available.
   - Distinguish new failures from pre-existing baseline failures.
   - If validation fails in `fix` or `full`, fix the regression or stop and report the blocker.

## Output Format

- **Summary:** mode, scope, tools/checks used, and overall cleanup potential.
- **Safe to Fix:** concrete items with file references, evidence, proposed change, and validation path.
- **Implemented:** for `fix` or `full` only; grouped by batch with files changed.
- **Needs Investigation:** skipped items and why they need more evidence or product input.
- **Do Not Change:** suspicious-looking patterns intentionally preserved.
- **Verification:** commands run, pass/fail status, and pre-existing failures if any.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page at `alignment/quality-sweep-{topic}.html`. Use a normalized topic slug derived from the app, feature, research subject, report subject, or output filename.

**Full content requirement.** The alignment page must contain the complete content of every proposed markdown deliverable -- every section, every finding, every detail, every list item. It is a thorough interactive review document, not a summary. Render the full deliverable content in clean, readable HTML with appropriate hierarchy, styling, and navigation. If the skill writes multiple scoped deliverables in one run, build one alignment page that contains all deliverables with anchor-linked navigation. Durable tracker artifacts, such as `research/assumption-tracker.md`, remain canonical markdown outputs but must also be fully rendered into the alignment page before approval.

**Dark-mode styling.** Use a dark color scheme by default. Base CSS variables: `--bg: #0d1117; --surface: #161b22; --border: #30363d; --text: #c9d1d9; --text-muted: #8b949e; --accent: #58a6ff; --green: #3fb950; --red: #f85149; --orange: #d29922; --purple: #bc8cff;`. Apply `background: var(--bg); color: var(--text);` on body. Use `--surface` for cards, nav, and table headers. Use `--border` for all borders. Use `--purple` for question blocks and gate headings. Use `--accent` for links and section headings. Keep headings `color: #fff` or `var(--accent)` for hierarchy. Question block backgrounds should use `#1c2333`.

**Alignment gates.** Treat gates as explicit review sections inside the HTML page. A gate blocks finalization until its required inline questions are answered and compiled into YAML. Include every gate that applies to the skill output, and include these gate types whenever relevant: evidence coverage, assumptions/confidence, scope/non-goals, candidate/verdict decisions, artifact destination, proposed file changes, coverage checkpoint, and post-approval route.

**Report-only research gates.** For report-only or pre-approval research skills, the alignment page must explicitly contain evidence coverage, assumptions/confidence, recommended path, proposed file changes, and approval gates before any canonical research, spec, or task file is created or updated.


**Required inline questions.** Each gate must contain at least one required inline question placed directly under the content it governs, inside a visually distinct question block. Each question must use radio-button inputs and include two standing options after the skill-generated choices: "Other / None of the above" backed by a multi-line text box for free-form input, and "Need clarification" backed by an optional notes box where the user can explain what is unclear. When any radio option other than "Other" or "Need clarification" is selected, show an optional "Additional notes" text box beneath it so the user can qualify their choice. Generate questions based on what genuinely needs user input -- do not add filler questions. Do not create a separate bottom "Decisions & Clarifications" section.

**Gate YAML contract.** At the bottom of the page, include a "Compile Answers" button that aggregates answers from all inline gate questions throughout the page, including free-text notes. The button remains disabled until every required question has a selection, shows a count of remaining unanswered questions, and scrolls to the first unanswered question if clicked early. When every question is answered, generate a structured YAML block with one item per gate answer using this stable shape: `section`, `gate_type`, `status` (`answered`, `other`, or `needs-clarification`), `answer`, optional `notes`, and optional `target_artifact` or `target_path` when the gate controls file output. After successful compilation, automatically attempt to copy the YAML to the clipboard with the Clipboard API, display copy status, and display the YAML in a read-only textarea with an explicit "Copy YAML" button. The copy button must retry clipboard copy when supported and fall back to selecting the textarea contents when clipboard access is unavailable or blocked.

**Pre-approval stop.** Before user approval, the next action is review of the HTML alignment page, not downstream routing. Ask the user to review the page and provide the compiled YAML answers. Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language until after compiled YAML has been provided and the approved artifacts have been written or updated.

**Diff highlighting on updates.** When the agent updates an existing alignment page after receiving compiled answers, highlight what changed since the previous version. The agent chooses inline annotation or side-by-side layout per situation.

**Archiving.** Before replacing an existing alignment page, archive it to `docs/history/archive/YYYY-MM-DD/HHMMSS/alignment/quality-sweep-{topic}.html`.

**Browser open.** Attempt to open the resulting HTML page in the browser and report whether the open succeeded or was blocked. A blocked browser-open attempt does not make the skill fail when the files were written correctly.

## Next-Skill Routing

In the final response, include `Recommended next skill: <command>` using these rules:

- Audit-only results with type/module coupling as the top finding: recommend `$extract-shared-types`.
- Audit-only results with safe mechanical cleanup available: recommend `$quality-sweep fix`.
- Any mutation or broad refactor completion: recommend `$regression-check`.
- Validation complete with changes ready to ship: recommend `$ship`.

Default recommendation: `$extract-shared-types when type/module coupling is the top finding, $quality-sweep fix when safe fixes are identified, or $regression-check after mutation`.

## Constraints

- Audit-only by default. Never edit files unless mode is `fix` or `full`.
- Behavior preservation is the default. Treat public APIs, package exports, migrations, database/data compatibility, and external contracts as high risk.
- Prefer repository-native tooling and existing dependencies. Do not add cleanup tools unless the user explicitly approves.
- Be conservative with deletion. Static analysis findings must be verified with code search and source inspection.
- Do not use DRY as a blanket rule. Consolidate only when it reduces real maintenance burden without hiding distinct reasons to change.
- Keep comments only when they explain intent, constraints, invariants, or non-obvious behavior for a future maintainer.
