---
name: spin-off
description: Extract a bounded part of the invoking codebase into a new GitHub repository with private and public-OSS readiness gates
type: execution
version: v0.0
argument-hint: "<target-path-or-symbol> --name <repo-name> [--visibility private|public-oss] [--owner <github-owner>]"
---

# Spin Off

Invoke as `$spin-off`.

Use this skill when the user wants to extract a package, app, component family, library, harness, or subsystem from the current repository into a new standalone codebase and GitHub repository.

The workflow is one skill with a visibility gate, not separate closed-source and OSS skills. Private and public-OSS spin-offs share the same extraction mechanics; visibility changes the legal, naming, licensing, documentation, and scrub requirements.

## Workflow

1. **Resolve intent and mode.**
   - Parse the target path, symbol, feature name, desired repo name, GitHub owner, and `--visibility private|public-oss`.
   - Default visibility to `private` when omitted.
   - If the target is ambiguous, inspect the repo first and present 2-4 candidate boundaries before asking the user to choose.
   - Treat `oss`, `open source`, `public`, or `publishable` as `--visibility public-oss`.

2. **Enter planning for non-trivial extraction.**
   - Use `update_plan` in Codex Default mode.
   - Write the extraction plan to the source repo's `tasks/roadmap.md` and current work to `tasks/todo.md` only when the source repo already uses those files or the user asks to track the work there.
   - Do not start mutating source or target files until the boundary, visibility mode, and repo destination are clear.

3. **Audit the candidate boundary.**
   - List source files, tests, styles/assets, package manifests, exports, examples, and docs in scope.
   - Trace internal imports and classify each as:
     - `core`: belongs in the new repo.
     - `adapter`: should become a host integration layer or example.
     - `fixture`: should become fake/demo data.
     - `host-only`: stays in the source repo.
     - `blocked`: cannot move without a policy or dependency decision.
   - Check secrets, environment variables, local paths, private URLs, proprietary assets, generated files, licenses, package names, and trademark/brand coupling.
   - Inspect git status in the source repo and do not include unrelated dirty work.

4. **Choose the extraction shape.**
   - Prefer the smallest standalone product boundary that can build and run independently.
   - For UI/devtool spin-offs, extract reusable components, public contracts, CSS tokens, fixtures, and a tiny demo harness; keep app-specific routing, auth, telemetry, and product data as adapters.
   - For library spin-offs, extract public APIs, tests, fixtures, and docs; replace monorepo-only imports with package-local contracts.
   - For app spin-offs, extract runtime code, config, and deployment docs, but rebuild secrets and environment setup from templates.

5. **Apply visibility gates.**
   - `private`:
     - GitHub repo stays private by default.
     - Internal roadmap context may be copied only if it helps the new repo and contains no secrets or unrelated proprietary details.
     - Brand-specific fixtures are allowed if the repo remains private.
     - License is optional unless the user asks for one.
   - `public-oss`:
     - Add or confirm a license before publishing.
     - Remove private roadmap/history, private URLs, local machine paths, internal task names, proprietary assets, customer/user data, and unreleased business strategy.
     - Rename packages, docs, examples, and README language so the project stands alone.
     - Add attribution/provenance notes when code originated in another owned repo.
     - Avoid third-party trademarks in repo name, package name, branding, screenshots, and marketing copy unless nominative reference is necessary and clearly non-affiliating.
     - Do not publish until the scrub checklist, dependency license review, and build/test verification pass.

6. **Scaffold the target repository.**
   - Create the new repo locally outside the source repo unless the user explicitly asks for a nested staging directory.
   - Initialize git on the repository primary branch (`main` unless the target ecosystem strongly expects otherwise).
   - Add `README.md`, `AGENTS.md`, package/app manifests, source directories, tests, examples, and minimal task docs appropriate for the target.
   - If the target is a devtool, use or recommend the `devtool` project-local pack after repo creation.
   - Do not create or modify GitHub Actions workflows unless the user explicitly overrides a project policy that allows them.

7. **Move code deliberately.**
   - Copy only audited files.
   - Rename namespaces and package scopes.
   - Replace source-repo contracts with target-local types or documented peer dependencies.
   - Preserve behavior with focused tests before broad cleanup.
   - Do not delete source-repo files unless the user explicitly asked for a hard extraction rather than a copy/spin-off.

8. **Verify independence.**
   - Run the narrowest useful checks first: typecheck, unit tests, component tests, package build, import smoke, demo harness smoke.
   - Run dependency/license/security checks when publishing public OSS.
   - Confirm no source-repo absolute paths, private package imports, secrets, or unrelated brand references remain.
   - For UI spin-offs, run or recommend browser/screenshot verification for the demo harness.

9. **Publish intentionally.**
   - Create the GitHub repo only after local verification passes or after clearly reporting any blocker the user accepts.
   - Use private visibility unless `--visibility public-oss` is explicit.
   - Commit only intended target-repo files.
   - Push the primary branch.
   - For public OSS, stop before public release if license, naming, provenance, dependency license review, or scrub checks are incomplete.

10. **Report the result.**
    - Summarize source boundary, target repo path, GitHub URL if created, visibility, files moved, host adapters left behind, verification commands, and unresolved publication gates.
    - Include next-step routing:
      - `Recommended next skill: $pack` when the target repo needs project-local skill packs.
      - `Recommended next skill: $ship` when the target repo has local changes ready to ship.
      - `Recommended next skill: $roadmap` when the new repo needs a build plan.

## Output

- **Boundary**: extracted target, source files, and excluded host-only files
- **Visibility**: `private` or `public-oss`, with completed and remaining gates
- **Target Repo**: local path, package/app name, GitHub owner/repo when created
- **Verification**: commands run and results
- **Next Work**: exact next task and recommended command

## Bismarck Top Bar Example

For a Bismarck v5 top-bar harness spin-off, prefer extracting `packages/game-ui` shell components and a fixture-backed demo harness, not `apps/game` wholesale.

Core candidates:
- `ExperimentToolbar`
- `VariantSelector`
- `ObservationChecklist`
- `AgentStatus`
- `PerformanceOverlay`
- `SessionInspector`
- `QuickActions`
- `ShellErrorBanner`
- `ShellErrorOverlay`
- `HelpOverlay`
- shell token CSS

Treat these as adapters or fixtures:
- `apps/game/src/layouts/ExperimentLayout.tsx`
- Bismarck `ExperimentId` values
- Bismarck agent-client hooks
- route loaders, game hypotheses, and session telemetry naming

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page at `alignment/spin-off-{topic}.html`. Use a normalized topic slug derived from the app, feature, research subject, report subject, or output filename.

**Full content requirement.** The alignment page must contain the complete content of every proposed markdown deliverable -- every section, every finding, every detail, every list item. It is a thorough interactive review document, not a summary. Render the full deliverable content in clean, readable HTML with appropriate hierarchy, styling, and navigation. If the skill writes multiple scoped deliverables in one run, build one alignment page that contains all deliverables with anchor-linked navigation. Durable tracker artifacts, such as `research/assumption-tracker.md`, remain canonical markdown outputs but must also be fully rendered into the alignment page before approval.

**Dark-mode styling.** Use a dark color scheme by default. Base CSS variables: `--bg: #0d1117; --surface: #161b22; --border: #30363d; --text: #c9d1d9; --text-muted: #8b949e; --accent: #58a6ff; --green: #3fb950; --red: #f85149; --orange: #d29922; --purple: #bc8cff;`. Apply `background: var(--bg); color: var(--text);` on body. Use `--surface` for cards, nav, and table headers. Use `--border` for all borders. Use `--purple` for question blocks and gate headings. Use `--accent` for links and section headings. Keep headings `color: #fff` or `var(--accent)` for hierarchy. Question block backgrounds should use `#1c2333`.

**Alignment gates.** Treat gates as explicit review sections inside the HTML page. A gate blocks finalization until its required inline questions are answered and compiled into YAML. Include every gate that applies to the skill output, and include these gate types whenever relevant: evidence coverage, assumptions/confidence, scope/non-goals, candidate/verdict decisions, artifact destination, proposed file changes, coverage checkpoint, and post-approval route.

**Report-only research gates.** For report-only or pre-approval research skills, the alignment page must explicitly contain evidence coverage, assumptions/confidence, recommended path, proposed file changes, and approval gates before any canonical research, spec, or task file is created or updated.


**Required inline questions.** Each gate must contain at least one required inline question placed directly under the content it governs, inside a visually distinct question block. Each question must use radio-button inputs and include two standing options after the skill-generated choices: "Other / None of the above" backed by a multi-line text box for free-form input, and "Need clarification" backed by an optional notes box where the user can explain what is unclear. When any radio option other than "Other" or "Need clarification" is selected, show an optional "Additional notes" text box beneath it so the user can qualify their choice. Generate questions based on what genuinely needs user input -- do not add filler questions. Do not create a separate bottom "Decisions & Clarifications" section.

**Gate YAML contract.** At the bottom of the page, include a "Compile Answers" button that aggregates answers from all inline gate questions throughout the page, including free-text notes. The button remains disabled until every required question has a selection, shows a count of remaining unanswered questions, and scrolls to the first unanswered question if clicked early. When every question is answered, generate a structured YAML block with one item per gate answer using this stable shape: `section`, `gate_type`, `status` (`answered`, `other`, or `needs-clarification`), `answer`, optional `notes`, and optional `target_artifact` or `target_path` when the gate controls file output. After successful compilation, automatically attempt to copy the YAML to the clipboard with the Clipboard API, display copy status, and display the YAML in a read-only textarea with an explicit "Copy YAML" button. The copy button must retry clipboard copy when supported and fall back to selecting the textarea contents when clipboard access is unavailable or blocked.

**Pre-approval stop.** Before user approval, the next action is review of the HTML alignment page, not downstream routing. Ask the user to review the page and provide the compiled YAML answers. Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language until after compiled YAML has been provided and the approved artifacts have been written or updated.

**Diff highlighting on updates.** When the agent updates an existing alignment page after receiving compiled answers, highlight what changed since the previous version. The agent chooses inline annotation or side-by-side layout per situation.

**Archiving.** Before replacing an existing alignment page, archive it to `docs/history/archive/YYYY-MM-DD/HHMMSS/alignment/spin-off-{topic}.html`.

**Browser open.** Attempt to open the resulting HTML page in the browser and report whether the open succeeded or was blocked. A blocked browser-open attempt does not make the skill fail when the files were written correctly.

## Constraints

- Never assume OSS readiness from ownership alone; run the public-OSS gate.
- Never publish secrets, private URLs, local absolute paths, proprietary assets, customer data, or unrelated roadmap/history.
- Never mutate shared source lockfiles during parallel monorepo work.
- Never delete the source implementation unless the user explicitly asks for a move instead of a copy.
- Do not leave the target repo half-created without reporting the exact path, status, and cleanup or continuation step.
