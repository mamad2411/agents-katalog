---
name: mono-detect
description: Detect pnpm workspace structure, optional Turborepo overlay, package metadata, and internal dependency graph for monorepo-aware skills
type: analysis
version: v0.0
argument-hint: "[optional: repository root]"
---

# Mono Detect

Invoke as `$mono-detect`.

Use this skill to detect a pnpm workspace monorepo and generate the `.agents/monorepo.json` artifact consumed by the monorepo pack.

`mono-detect` is the foundation skill for `mono-run`, `mono-ship`, and `mono-guard`. Those skills use its output to inject monorepo-aware pre/post steps into the standard `$run` and `$ship` contracts without duplicating the global workflow.

## Augmentation Injection Pattern

`mono-detect` is the pack's detection foundation for the augmentation injection pattern. It does not replace `$run`, `$ship`, or global monorepo planning skills; it supplies `.agents/monorepo.json` so `mono-run`, `mono-ship`, and `mono-guard` can inject monorepo-aware pre-flight and post-integration checks around those existing workflows.

## Workflow

1. Resolve the target repository root.
   - Use `$ARGUMENTS` as the root when provided.
   - Otherwise use the current working directory.
2. Locate the pack script relative to this skill: `../../scripts/mono-detect.sh` from the monorepo pack root.
3. Check whether `.agents/monorepo.json` is fresh:
   - Run `packs/monorepo/scripts/mono-detect.sh <root> --check-stale`.
   - If it prints `fresh: .agents/monorepo.json`, keep the existing artifact.
   - If the file is missing, stale, or the check does not report fresh, run `packs/monorepo/scripts/mono-detect.sh <root>` to regenerate it.
4. If detection fails because `pnpm-workspace.yaml` is missing:
   - Report that the project is not a detected pnpm monorepo.
   - Suggest `$mono-migrate` as a future V2 migration route when the user wants to convert a single-app project.
   - Do not create `.agents/monorepo.json` by hand.
5. Read `.agents/monorepo.json` and summarize:
   - Workspace manager.
   - Build orchestrator (`turborepo` when `turbo.json` is present, otherwise none).
   - Package count and package paths.
   - Internal dependency graph edges.
   - Turborepo pipeline names.
6. Report staleness behavior:
   - Mention that the artifact is regenerated when `pnpm-workspace.yaml`, `turbo.json`, or workspace `package.json` files are newer than `.agents/monorepo.json`.
7. Route the next step:
   - If detection passed and the user is preparing execution, recommend `$mono-run`.
   - If detection passed and the user is checking lane safety, recommend `$mono-guard`.
   - If detection failed because this is not a pnpm monorepo, recommend `$mono-migrate` as the V2 advisory route.

## Output Format

- **Detection:** detected, fresh, regenerated, or not detected.
- **Workspace:** manager, build orchestrator, root path.
- **Packages:** count plus package name/path list.
- **Dependency graph:** internal dependency edges; say `none` when no internal edges exist.
- **Turbo pipelines:** pipeline names when present; say `none` when Turborepo is absent.
- **Artifact:** `.agents/monorepo.json` path and whether it was reused or regenerated.
- **Next work:** concrete follow-up.
- **Recommended next command:** one command.

## Constraints

- Do not edit task files.
- Do not run package manager install/add commands.
- Do not infer non-pnpm workspace managers in V1.
- Do not modify `.agents/monorepo.json` manually; use `mono-detect.sh`.
- Treat `mono-detect` as an augmentation foundation for `mono-run`, `mono-ship`, and `mono-guard`, not as a replacement for `$run`, `$ship`, or global monorepo planning skills.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page at `alignment/mono-detect-{topic}.html`. Use a normalized topic slug derived from the app, feature, research subject, report subject, or output filename.

**Full content requirement.** The alignment page must contain the complete content of every proposed markdown deliverable -- every section, every finding, every detail, every list item. It is a thorough interactive review document, not a summary. Render the full deliverable content in clean, readable HTML with appropriate hierarchy, styling, and navigation. If the skill writes multiple scoped deliverables in one run, build one alignment page that contains all deliverables with anchor-linked navigation. Durable tracker artifacts, such as `research/assumption-tracker.md`, remain canonical markdown outputs but must also be fully rendered into the alignment page before approval.

**Dark-mode styling.** Use a dark color scheme by default. Base CSS variables: `--bg: #0d1117; --surface: #161b22; --border: #30363d; --text: #c9d1d9; --text-muted: #8b949e; --accent: #58a6ff; --green: #3fb950; --red: #f85149; --orange: #d29922; --purple: #bc8cff;`. Apply `background: var(--bg); color: var(--text);` on body. Use `--surface` for cards, nav, and table headers. Use `--border` for all borders. Use `--purple` for question blocks and gate headings. Use `--accent` for links and section headings. Keep headings `color: #fff` or `var(--accent)` for hierarchy. Question block backgrounds should use `#1c2333`.

**Alignment gates.** Treat gates as explicit review sections inside the HTML page. A gate blocks finalization until its required inline questions are answered and compiled into YAML. Include every gate that applies to the skill output, and include these gate types whenever relevant: evidence coverage, assumptions/confidence, scope/non-goals, candidate/verdict decisions, artifact destination, proposed file changes, coverage checkpoint, and post-approval route.

**Report-only research gates.** For report-only or pre-approval research skills, the alignment page must explicitly contain evidence coverage, assumptions/confidence, recommended path, proposed file changes, and approval gates before any canonical research, spec, or task file is created or updated.


**Required inline questions.** Each gate must contain at least one required inline question placed directly under the content it governs, inside a visually distinct question block. Each question must use radio-button inputs and include two standing options after the skill-generated choices: "Other / None of the above" backed by a multi-line text box for free-form input, and "Need clarification" backed by an optional notes box where the user can explain what is unclear. When any radio option other than "Other" or "Need clarification" is selected, show an optional "Additional notes" text box beneath it so the user can qualify their choice. Generate questions based on what genuinely needs user input -- do not add filler questions. Do not create a separate bottom "Decisions & Clarifications" section.

**Gate YAML contract.** At the bottom of the page, include a "Compile Answers" button that aggregates answers from all inline gate questions throughout the page, including free-text notes. The button remains disabled until every required question has a selection, shows a count of remaining unanswered questions, and scrolls to the first unanswered question if clicked early. When every question is answered, generate a structured YAML block with one item per gate answer using this stable shape: `section`, `gate_type`, `status` (`answered`, `other`, or `needs-clarification`), `answer`, optional `notes`, and optional `target_artifact` or `target_path` when the gate controls file output. After successful compilation, automatically attempt to copy the YAML to the clipboard with the Clipboard API, display copy status, and display the YAML in a read-only textarea with an explicit "Copy YAML" button. The copy button must retry clipboard copy when supported and fall back to selecting the textarea contents when clipboard access is unavailable or blocked.

**Pre-approval stop.** Before user approval, the next action is review of the HTML alignment page, not downstream routing. Ask the user to review the page and provide the compiled YAML answers. Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language until after compiled YAML has been provided and the approved artifacts have been written or updated.

**Diff highlighting on updates.** When the agent updates an existing alignment page after receiving compiled answers, highlight what changed since the previous version. The agent chooses inline annotation or side-by-side layout per situation.

**Archiving.** Before replacing an existing alignment page, archive it to `docs/history/archive/YYYY-MM-DD/HHMMSS/alignment/mono-detect-{topic}.html`.

**Browser open.** Attempt to open the resulting HTML page in the browser and report whether the open succeeded or was blocked. A blocked browser-open attempt does not make the skill fail when the files were written correctly.

## Default Shipping Contract

- **Default next-step routing:** when reporting completion, include the two-line pair `**Next work:** <specific task, blocker, or follow-up>` and `**Recommended next command:** <one command or route>` so the next operator has a concrete handoff.
- If this skill creates or modifies tracked repository files, finish by committing and pushing all intended changes to the repository primary branch (`main` when present, otherwise `master`) before stopping, even if the user did not explicitly ask for commit/push.
- Do not leave tracked changes or unpushed commits behind. If unrelated tracked work is already present, either include it in sensible commits too or stop and explain the blocker.
- This contract does not override stricter safety rules about secrets, destructive history changes, release publication/tag confirmation, or production deploy confirmation.
