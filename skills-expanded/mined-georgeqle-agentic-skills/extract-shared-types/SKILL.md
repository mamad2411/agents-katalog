---
name: extract-shared-types
description: Extract shared type definitions into a dedicated types directory without runtime behavior changes
type: execution
version: v0.0
argument-hint: "[optional: package, app, directory, or domain to refactor]"
---

# Extract Shared Types

Invoke as `$extract-shared-types`.

Use this skill for type hoisting, type barreling, shared `types/` directories, import honesty, and circular-dependency prevention when the requested change is explicitly structural and behavior-preserving.

## Process

1. **Establish scope.**
   - Read `$ARGUMENTS` for a package, app, directory, or domain.
   - If no scope is provided, inspect the repo and choose the smallest coherent area with shared exported types.
   - Read project instructions, package manifests, TypeScript config, path aliases, lint rules, package export maps, and existing `types/` or barrel conventions.

2. **Classify declarations before editing.**
   - Candidate moves: exported `type` aliases, `interface` declarations, ambient declarations, generic helper shapes, DTO/result shapes, props/state shapes, and domain data shapes.
   - Do not move runtime values: functions, constants, classes, runtime enums, schemas, validators, database/API clients, React components, business logic, or anything imported as a value.
   - Treat TypeScript `enum` as runtime unless the project already uses `const enum` safely and the compiler settings make the move clearly type-only.

3. **Design the target type layout.**
   - Create or reuse a dedicated `types/` directory at the nearest appropriate boundary.
   - Organize files by domain, feature, or package convention rather than by source file name when a domain boundary is clear.
   - Prefer direct imports from domain type files. Add `types/index.ts` only if the project already uses barrels or repeated type imports would otherwise become noisy.

4. **Move type declarations.**
   - Move only the approved type declarations.
   - Preserve exported names, generic parameters, comments that explain shape semantics, and public visibility.
   - Keep runtime implementation files focused on runtime logic, importing moved declarations with `import type` where supported.

5. **Update imports and compatibility.**
   - Update internal imports to the new type files.
   - Use `import type` for type-only imports and avoid creating new value imports from `types/`.
   - If old import paths are part of a public API or package boundary, leave type-only re-exports from the original module rather than forcing a breaking migration.
   - Avoid widening public barrels unless the repo already exposes that type surface intentionally.

6. **Verify behavior preservation.**
   - Run the narrowest relevant typecheck, tests, lint/import checks, and dependency-cycle checks available.
   - Inspect the diff for runtime changes: implementation logic, emitted values, schema definitions, package exports, route behavior, and component behavior should not change.
   - If verification fails, fix import/type issues without changing runtime behavior.

## Output Format

When reporting completion, include:

- Scope refactored.
- Type files created or reused.
- Compatibility re-exports left in place, if any.
- Verification commands run and their results.
- Any skipped candidates with the reason they were runtime-coupled or public-API-sensitive.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page at `alignment/extract-shared-types-{topic}.html`. Use a normalized topic slug derived from the app, feature, research subject, report subject, or output filename.

**Full content requirement.** The alignment page must contain the complete content of every proposed markdown deliverable -- every section, every finding, every detail, every list item. It is a thorough interactive review document, not a summary. Render the full deliverable content in clean, readable HTML with appropriate hierarchy, styling, and navigation. If the skill writes multiple scoped deliverables in one run, build one alignment page that contains all deliverables with anchor-linked navigation. Durable tracker artifacts, such as `research/assumption-tracker.md`, remain canonical markdown outputs but must also be fully rendered into the alignment page before approval.

**Dark-mode styling.** Use a dark color scheme by default. Base CSS variables: `--bg: #0d1117; --surface: #161b22; --border: #30363d; --text: #c9d1d9; --text-muted: #8b949e; --accent: #58a6ff; --green: #3fb950; --red: #f85149; --orange: #d29922; --purple: #bc8cff;`. Apply `background: var(--bg); color: var(--text);` on body. Use `--surface` for cards, nav, and table headers. Use `--border` for all borders. Use `--purple` for question blocks and gate headings. Use `--accent` for links and section headings. Keep headings `color: #fff` or `var(--accent)` for hierarchy. Question block backgrounds should use `#1c2333`.

**Alignment gates.** Treat gates as explicit review sections inside the HTML page. A gate blocks finalization until its required inline questions are answered and compiled into YAML. Include every gate that applies to the skill output, and include these gate types whenever relevant: evidence coverage, assumptions/confidence, scope/non-goals, candidate/verdict decisions, artifact destination, proposed file changes, coverage checkpoint, and post-approval route.

**Report-only research gates.** For report-only or pre-approval research skills, the alignment page must explicitly contain evidence coverage, assumptions/confidence, recommended path, proposed file changes, and approval gates before any canonical research, spec, or task file is created or updated.


**Required inline questions.** Each gate must contain at least one required inline question placed directly under the content it governs, inside a visually distinct question block. Each question must use radio-button inputs and include two standing options after the skill-generated choices: "Other / None of the above" backed by a multi-line text box for free-form input, and "Need clarification" backed by an optional notes box where the user can explain what is unclear. When any radio option other than "Other" or "Need clarification" is selected, show an optional "Additional notes" text box beneath it so the user can qualify their choice. Generate questions based on what genuinely needs user input -- do not add filler questions. Do not create a separate bottom "Decisions & Clarifications" section.

**Gate YAML contract.** At the bottom of the page, include a "Compile Answers" button that aggregates answers from all inline gate questions throughout the page, including free-text notes. The button remains disabled until every required question has a selection, shows a count of remaining unanswered questions, and scrolls to the first unanswered question if clicked early. When every question is answered, generate a structured YAML block with one item per gate answer using this stable shape: `section`, `gate_type`, `status` (`answered`, `other`, or `needs-clarification`), `answer`, optional `notes`, and optional `target_artifact` or `target_path` when the gate controls file output. After successful compilation, automatically attempt to copy the YAML to the clipboard with the Clipboard API, display copy status, and display the YAML in a read-only textarea with an explicit "Copy YAML" button. The copy button must retry clipboard copy when supported and fall back to selecting the textarea contents when clipboard access is unavailable or blocked.

**Pre-approval stop.** Before user approval, the next action is review of the HTML alignment page, not downstream routing. Ask the user to review the page and provide the compiled YAML answers. Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language until after compiled YAML has been provided and the approved artifacts have been written or updated.

**Diff highlighting on updates.** When the agent updates an existing alignment page after receiving compiled answers, highlight what changed since the previous version. The agent chooses inline annotation or side-by-side layout per situation.

**Archiving.** Before replacing an existing alignment page, archive it to `docs/history/archive/YYYY-MM-DD/HHMMSS/alignment/extract-shared-types-{topic}.html`.

**Browser open.** Attempt to open the resulting HTML page in the browser and report whether the open succeeded or was blocked. A blocked browser-open attempt does not make the skill fail when the files were written correctly.

## Next-Skill Routing

In the final response, include `Recommended next skill: <command>` using these rules:

- Audit-only results with type/module coupling as the top finding: recommend `$extract-shared-types`.
- Audit-only results with safe mechanical cleanup available: recommend `$quality-sweep fix`.
- Any mutation or broad refactor completion: recommend `$regression-check`.
- Validation complete with changes ready to ship: recommend `$ship`.

Default recommendation: `$regression-check after mutation, or $quality-sweep fix/full when broader cleanup remains`.

## Constraints

- Zero runtime behavior changes.
- Do not move declarations unless they are type-only.
- Do not introduce dependency upgrades, schema redesigns, or broad module restructuring.
- Do not remove public import paths unless the user explicitly requests a breaking change.
- Preserve unrelated user changes in the working tree.
