---
name: mono-guard
description: Validate monorepo lane specs before dispatch and verify integrated changes stay inside declared lane boundaries
type: analysis
version: v0.0
argument-hint: "[--post-integration] [optional: lane-specs.json]"
---

# Mono Guard

Invoke as `$mono-guard`.

Use this skill to validate monorepo pack lane artifacts before parallel dispatch and to audit integrated lane changes after dispatch.

This pack-local `mono-guard` consumes `.agents/lane-specs.json` and `.agents/monorepo.json`. It preserves behavioral compatibility with the global `$mono-guard` contract while using the monorepo pack's JSON artifacts and scripts as the project-local enforcement surface.

## Augmentation Injection Pattern

`mono-guard` is the pack's safety gate for the augmentation injection pattern. `mono-run` injects it before package-scoped dispatch, and `mono-ship` relies on its post-integration boundary checks before delegating to `$ship`. The skill augments existing run/ship workflows with monorepo lane enforcement rather than replacing their task selection, validation, history, commit, push, or deploy responsibilities.

## Modes

- **Pre-flight (default):** Validate `.agents/lane-specs.json` before `mono-run` dispatches package-scoped lanes.
- **Post-integration (`--post-integration`):** Verify actual changed files from the integrated diff stay inside declared lane ownership and do not include unsafe shared files.

## Inputs

- `.agents/lane-specs.json`: generated lane plan with lifecycle, cross-cutting steps, lanes, `owns`, `must_not_edit`, `depends_on`, mode, and branch.
- `.agents/monorepo.json`: workspace detection output from `mono-detect`, including packages and internal dependency graph.
- `packs/monorepo/scripts/lane-spec-validate.sh`: schema and boundary validator for lane specs.

If `.agents/monorepo.json` is missing or stale, run `mono-detect` first. If `.agents/lane-specs.json` is missing, stop and recommend generating lane specs through `mono-run`.

## Pre-Flight Workflow

1. Resolve the lane-spec file:
   - Use the path in `$ARGUMENTS` when provided.
   - Otherwise use `.agents/lane-specs.json`.
2. Run `packs/monorepo/scripts/lane-spec-validate.sh <lane-specs.json>`.
   - This verifies required fields, lifecycle state, disjoint `owns`, required root `must_not_edit` entries, valid `depends_on` references, unique non-primary branches, and duplicate step protection.
   - On failure, report `FAIL` and do not dispatch.
3. Read `.agents/monorepo.json`.
   - If missing, run or recommend `mono-detect`.
   - Use its `packages` and `dependency_graph` to evaluate package-aware safety.
4. Verify every lane's `owns` paths map to declared workspace package paths or clearly root-only serial work.
5. Verify every lane's `must_not_edit` includes lockfiles and shared root config files:
   - `pnpm-lock.yaml`
   - `package.json`
   - `pnpm-workspace.yaml`
   - `turbo.json`
6. Verify dependency ordering:
   - If package X depends on package Y and both packages are owned by different lanes, the lane for X must depend on the lane for Y directly or transitively.
   - Use `.agents/monorepo.json.dependency_graph` for dependency edges.
7. Verify lane dependency graph validity:
   - All `depends_on` references resolve to known cross-cutting step IDs or lane step IDs.
   - No lane dependency cycle exists.
8. Verify branch isolation:
   - Every write lane has a unique non-primary GitHub branch.
   - No lane branch is `main` or `master`.
   - If PR review is required by the execution profile but branch/PR evidence is missing after dispatch, report `FAIL`.
9. Scan lane descriptions, scopes, and modes when present for install/add intent.
   - Fail non-serial package lanes that instruct `pnpm install`, `pnpm add`, `npm install`, `yarn add`, or equivalent lockfile-modifying commands.
   - Warn on natural-language dependency changes such as "add dependency" or "install package".

## Post-Integration Workflow

1. Read `.agents/lane-specs.json` and `.agents/monorepo.json`.
2. Inspect the integrated diff with `git diff --name-only` unless the user supplied a different reviewed diff range.
3. For each changed file:
   - Flag any lockfile modification from a parallel lane as `FAIL`.
   - Flag root config changes as `WARN` unless they are declared in a serial cross-cutting step.
   - Verify the path is inside at least one declared lane `owns` path or an allowed serial cross-cutting/root scope.
   - Flag files outside declared ownership as boundary violations.
4. Verify consolidation/PR review evidence when lane specs record branch-backed dispatch:
   - Every integrated lane must have branch, commit SHA, and PR URL evidence recorded in `tasks/lane-specs.md` or the dispatch report.
   - Missing PR review evidence is `FAIL` because package lanes must not bypass consolidation review.
5. Report violations without reverting, fixing, or editing task files.

## Output Format

```markdown
### Mono Guard Report

**Mode:** pre-flight | post-integration
**Lane spec:** .agents/lane-specs.json
**Monorepo artifact:** .agents/monorepo.json
**Verdict:** PASS | WARN | FAIL

#### Results

| Check | Verdict | Details |
|---|---|---|
| Lane-spec schema | PASS | lane-spec-validate.sh passed |
| Owns disjointness | PASS | all lane owns paths are disjoint |
| Shared file exclusions | PASS | lockfile and root config paths are in must_not_edit |
| Branch isolation | PASS | each write lane has a unique non-primary GitHub branch |
| Dependency ordering | PASS | package dependency lanes are ordered |
| Integrated diff boundaries | WARN | one root config changed in serial integration |

#### Failures

- List blocking issues with lane IDs, step IDs, paths, and specific fixes.

#### Warnings

- List advisory issues with recommended follow-up.
```

## Verdicts

- **PASS:** Safe to dispatch or ship.
- **WARN:** Advisory issues found; review before proceeding.
- **FAIL:** Dispatch or shipping is blocked until the lane specs or integrated changes are corrected.

## Constraints

- Do not edit task files.
- Do not run package manager install/add commands.
- Do not modify `.agents/lane-specs.json` or `.agents/monorepo.json` except by invoking the designated generation/detection skills when appropriate.
- Do not revert or repair post-integration changes; report violations only.
- Keep behavior compatible with the global `$mono-guard` safety contract.

## Next-Step Routing

- **PASS pre-flight:** `$mono-run` to dispatch the validated lanes.
- **WARN pre-flight:** Review warnings, then `$mono-run` if accepted.
- **FAIL pre-flight:** Fix or regenerate `.agents/lane-specs.json`, then rerun `$mono-guard`.
- **PASS post-integration:** `$mono-ship` for package-scoped validation and shipping.
- **WARN/FAIL post-integration:** Resolve boundary issues, then rerun `$mono-guard --post-integration`.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page at `alignment/mono-guard-{topic}.html`. Use a normalized topic slug derived from the app, feature, research subject, report subject, or output filename.

**Full content requirement.** The alignment page must contain the complete content of every proposed markdown deliverable -- every section, every finding, every detail, every list item. It is a thorough interactive review document, not a summary. Render the full deliverable content in clean, readable HTML with appropriate hierarchy, styling, and navigation. If the skill writes multiple scoped deliverables in one run, build one alignment page that contains all deliverables with anchor-linked navigation. Durable tracker artifacts, such as `research/assumption-tracker.md`, remain canonical markdown outputs but must also be fully rendered into the alignment page before approval.

**Dark-mode styling.** Use a dark color scheme by default. Base CSS variables: `--bg: #0d1117; --surface: #161b22; --border: #30363d; --text: #c9d1d9; --text-muted: #8b949e; --accent: #58a6ff; --green: #3fb950; --red: #f85149; --orange: #d29922; --purple: #bc8cff;`. Apply `background: var(--bg); color: var(--text);` on body. Use `--surface` for cards, nav, and table headers. Use `--border` for all borders. Use `--purple` for question blocks and gate headings. Use `--accent` for links and section headings. Keep headings `color: #fff` or `var(--accent)` for hierarchy. Question block backgrounds should use `#1c2333`.

**Alignment gates.** Treat gates as explicit review sections inside the HTML page. A gate blocks finalization until its required inline questions are answered and compiled into YAML. Include every gate that applies to the skill output, and include these gate types whenever relevant: evidence coverage, assumptions/confidence, scope/non-goals, candidate/verdict decisions, artifact destination, proposed file changes, coverage checkpoint, and post-approval route.

**Report-only research gates.** For report-only or pre-approval research skills, the alignment page must explicitly contain evidence coverage, assumptions/confidence, recommended path, proposed file changes, and approval gates before any canonical research, spec, or task file is created or updated.


**Required inline questions.** Each gate must contain at least one required inline question placed directly under the content it governs, inside a visually distinct question block. Each question must use radio-button inputs and include two standing options after the skill-generated choices: "Other / None of the above" backed by a multi-line text box for free-form input, and "Need clarification" backed by an optional notes box where the user can explain what is unclear. When any radio option other than "Other" or "Need clarification" is selected, show an optional "Additional notes" text box beneath it so the user can qualify their choice. Generate questions based on what genuinely needs user input -- do not add filler questions. Do not create a separate bottom "Decisions & Clarifications" section.

**Gate YAML contract.** At the bottom of the page, include a "Compile Answers" button that aggregates answers from all inline gate questions throughout the page, including free-text notes. The button remains disabled until every required question has a selection, shows a count of remaining unanswered questions, and scrolls to the first unanswered question if clicked early. When every question is answered, generate a structured YAML block with one item per gate answer using this stable shape: `section`, `gate_type`, `status` (`answered`, `other`, or `needs-clarification`), `answer`, optional `notes`, and optional `target_artifact` or `target_path` when the gate controls file output. After successful compilation, automatically attempt to copy the YAML to the clipboard with the Clipboard API, display copy status, and display the YAML in a read-only textarea with an explicit "Copy YAML" button. The copy button must retry clipboard copy when supported and fall back to selecting the textarea contents when clipboard access is unavailable or blocked.

**Pre-approval stop.** Before user approval, the next action is review of the HTML alignment page, not downstream routing. Ask the user to review the page and provide the compiled YAML answers. Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language until after compiled YAML has been provided and the approved artifacts have been written or updated.

**Diff highlighting on updates.** When the agent updates an existing alignment page after receiving compiled answers, highlight what changed since the previous version. The agent chooses inline annotation or side-by-side layout per situation.

**Archiving.** Before replacing an existing alignment page, archive it to `docs/history/archive/YYYY-MM-DD/HHMMSS/alignment/mono-guard-{topic}.html`.

**Browser open.** Attempt to open the resulting HTML page in the browser and report whether the open succeeded or was blocked. A blocked browser-open attempt does not make the skill fail when the files were written correctly.

## Default Shipping Contract

- **Default next-step routing:** when reporting completion, include the two-line pair `**Next work:** <specific task, blocker, or follow-up>` and `**Recommended next command:** <one command or route>` so the next operator has a concrete handoff.
- If this skill creates or modifies tracked repository files, finish by committing and pushing all intended changes to the repository primary branch (`main` when present, otherwise `master`) before stopping, even if the user did not explicitly ask for commit/push.
- Do not leave tracked changes or unpushed commits behind. If unrelated tracked work is already present, either include it in sensible commits too or stop and explain the blocker.
- This contract does not override stricter safety rules about secrets, destructive history changes, release publication/tag confirmation, or production deploy confirmation.
