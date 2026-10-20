---
name: harmony-quality-review-team
description: HarmonyOS/OpenHarmony 三线质量评审工作流。Use when a user asks to statically review a Harmony project, test functionality and business flows, audit UI and accessibility, inspect interaction and motion, run a regression review, or produce a P0/P1/P2 quality report.
metadata:
  short-description: HarmonyOS functionality, UI, and interaction quality review
  source: WorkBuddy visible expert card, generalized for HarmonyOS projects
  child_entry_mode: internal-router-labels
---

# HarmonyOS 测试质量评审专家团

Use this skill as the standalone testing and quality-review entry for a generic HarmonyOS or OpenHarmony project. It generalizes the visible WorkBuddy "衣橱质量评审团" workflow: the product-specific wardrobe rules are removed, while the three independent review dimensions and lead-owned evidence synthesis are preserved. It is a separate expert team and is not a child route of `$harmony-expert-team`.

## When To Use

- The user asks to test or review a HarmonyOS project's functionality, flows, UI, interaction, or animation.
- The user asks for a static quality review, regression review, release-readiness review, or P0/P1/P2 fix list.
- The user wants to understand whether a HarmonyOS project has broken navigation, incomplete CRUD, data consistency risks, UI specification drift, missing state feedback, or interaction defects.

Do not use this entry as a substitute for implementing a fix. After the review, route implementation work to `$harmony-os-act`; route page generation to `$generate-ui-code`; route service-card work to `$service-widget`.

## Internal Review Roles

These are router-local labels, not standalone Skills and must not be invoked as `$label`:

- `harmony-quality-review-lead`: creates the review plan, coordinates independent tracks, de-duplicates findings, and owns the final report.
- `harmony-function-flow-reviewer`: checks feature reachability, CRUD completeness, navigation, repository contracts, migrations, media cleanup, and data consistency.
- `harmony-ui-visual-reviewer`: checks design tokens, color and typography usage, layout, component states, empty/error states, and accessibility basics.
- `harmony-interaction-motion-reviewer`: checks hit targets, duplicate-submit prevention, loading and error feedback, navigation and sheet transitions, list performance, and async races.

## Project-First Workflow

1. Inspect the project before judging it. Locate `module.json5`, `app.json5`, `build-profile.json5`, `hvigorfile.ts`, `oh-package.json5`, `main_pages.json`, source modules, resources, tests, and project design or architecture notes when present.
2. Record the target scope and evidence limits. Separate static code evidence from device, emulator, preview, build, or runtime evidence that was not available.
3. Run three independent review tracks in parallel when the request is a complete review. Each track reads the project's own conventions and reports only findings in its owned dimension.
4. Require every finding to include a repository-relative file path, line number when available, observed behavior, impact, and a concrete remediation.
5. Wait for all requested tracks before synthesis. The lead removes duplicates, keeps the strongest evidence, and records the responsible review dimension.
6. Classify the remaining findings:
   - `P0`: core workflow blocked, data can be lost or made false, or a serious accessibility or interaction defect prevents use.
   - `P1`: important correctness, consistency, architectural, feedback, or performance risk that should be fixed before release.
   - `P2`: lower-risk visual, motion, robustness, or maintainability issue.
7. Produce the final report and a remediation order. Only then suggest a follow-up implementation route.

## Review Track Guidance

### Function And Flow

- Trace the user-visible path from entry point to repository or service call.
- Compare domain operations with UI reachability and check that create, read, update, and delete behavior is complete where the product requires it.
- Verify that SQLite or the project's local source of truth, derived indexes, migrations, media references, and cleanup behavior remain consistent.
- Check that pages do not bypass the repository boundary, invent remote synchronization, or claim capabilities not present in the project.

### UI And Visual

- Read the project's design specification and theme tokens before checking screens.
- Search for hard-coded colors, copied token constants, inconsistent typography, spacing, radius, shadows, and component dimensions.
- Check loading, empty, error, disabled, selected, and long-text states, plus clear form labels and accessible names.
- Treat project-specific visual rules as higher priority than generic design advice and mark missing project guidance as an assumption.

### Interaction And Motion

- Check that interactive targets are large enough for the platform and that icons, tabs, list actions, sheets, and forms have an obvious state response.
- Check save and submit paths for loading, disabled, cancellation, error recovery, and duplicate-submit protection.
- Inspect navigation, sheets, overlays, transitions, and animation symmetry without claiming runtime behavior from static code alone.
- Check lazy rendering and asynchronous race risks in lists, media selection, refresh, and state transitions.

## Review Variants

- **Complete review**: run all three tracks in parallel, then synthesize one de-duplicated report.
- **Focused review**: run only the requested track and return its evidence without pretending the other dimensions were checked.
- **Regression review**: locate the previous report or baseline, run the relevant tracks, and label findings as new, fixed, persistent, or unverifiable.
- **Release review**: combine the three tracks with available build, test, lint, and device evidence; keep unavailable evidence explicit.

## Output Contract

Return a Chinese report unless the user requests another language. Include:

1. Scope, inspected project areas, and verification limits.
2. Overall conclusion and separate health scores for function/flow, UI/visual, and interaction/motion when enough evidence exists.
3. De-duplicated findings grouped by `P0`, `P1`, and `P2`.
4. For every finding: dimension, `file:line`, observed evidence, impact, and recommended fix.
5. A remediation roadmap ordered by severity and dependency.
6. Open questions, assumptions, and tests or runtime checks still required.

## Guardrails

- Review-only work must not modify project files, delete data, change permissions, or add dependencies.
- Do not claim that a build, test, animation, or device flow passed unless it was actually run and the evidence is available.
- Do not invent hidden WorkBuddy prompts, private APIs, product rules, or runtime capabilities.
- Prefer project-relative paths in reports and never commit local absolute paths, secrets, credentials, caches, or local-only reports.
- When formal multi-agent primitives are unavailable, describe the work as coordinated capability execution rather than claiming that a real team was spawned.

## References

- `references/guide.md`: source mapping, routing table, evidence checklist, and report template.
- `$harmony-os-ask`: diagnosis and technical explanation after the review identifies an unclear platform issue.
- `$harmony-os-act`: implementation and verification of approved fixes.

## Validation

- Confirm the project-specific paths and conventions were inspected before findings were written.
- Confirm every finding has evidence, severity, impact, and a fix recommendation.
- Confirm duplicate findings are merged and the three health dimensions are not silently conflated.
- Run the project's available static checks, tests, build, preview, or device checks when the user requests execution and the environment supports them.
- Report all unavailable checks and remaining risks explicitly.
