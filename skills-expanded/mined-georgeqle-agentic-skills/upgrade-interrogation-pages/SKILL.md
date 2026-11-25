---
name: upgrade-interrogation-pages
description: Audit and explicitly upgrade generated interrogation/*.html round pages to the current local interrogation-page standard while preserving page-specific context
type: ops
version: v0.1
argument-hint: "[--repo <path>] [--apply] [interrogation/*.html...]"
---

# Upgrade Interrogation Pages

Invoke as `$upgrade-interrogation-pages`.

Use this skill when a repository already has generated `interrogation/*.html` round pages and the user wants to audit or update them against the current local interrogation-page convention. This skill targets generated interrogation HTML artifacts only.

## Inputs

- Default target repository: current working directory.
- Optional `--repo <path>` to target another repository.
- Optional explicit page paths under the target repository's `interrogation/` directory.
- Optional `--apply`, or clear user wording such as "apply the upgrade" or "upgrade these pages", to allow page rewrites.

## Mode

- Default mode is audit/dry-run.
- The skill name alone is not apply intent; do not modify files unless the visible user request explicitly asks to apply or upgrade existing pages.
- In audit/dry-run mode, inspect pages and report drift without creating, editing, moving, or deleting any files.

## Process

1. Resolve scope:
   - Locate the project-root `interrogation/` directory; stop if absent.
   - Enumerate `interrogation/*.html` round pages.
   - If the user provided page paths, include only those paths after confirming they are inside the project-root `interrogation/` directory.

2. Load local standards:
   - Read applicable local convention sources from `AGENTS.md`, `CLAUDE.md`, and active bundled `INTERROGATION-PAGE.md` files found under `base/`, `packs/`, `.claude/skills/`, and `.codex/skills/`.
   - Treat those local files as read-only standards. Do not fetch external standards.
   - Extract the current required HTML behaviors: the five open-question markers (`data-open-input`, `data-recommended-answer`, `data-agent-confidence` with a value in `{high, medium, low}`, a `data-clarify-copy` button, and a `data-apply-recommended` button on every `data-open-question` block), the ≥1 open input per round rule, the page-metadata attributes (`data-visual-tier`, `data-interrogation-status`, `data-interrogation-round`, `data-interrogation-gate`), round-file naming (`{skill}-r{N}-{branch}.html`), the `data-answer-sidecar` reference, the Brief Me TTS include, dark-mode styling, responsive layout, the embed prohibition, and archive-before-replace behavior.

3. Audit every selected page:
   - Read the whole HTML file before judging it.
   - Identify page-specific substance: title, meta/context, assumptions manifest, open questions, recommended answers, confidence badges, apply-recommended controls/scripts, gate controls, coverage summaries, prior context, and any page-specific scripts.
   - Report missing or stale standard features per page.
   - Classify each page as `current`, `upgrade-needed`, or `blocked-content-loss-risk`.

4. Stop on content-loss risk:
   - If a page's structure is too ambiguous to upgrade while preserving substantive content, do not rewrite it.
   - Report exactly what content could not be mapped and what human decision is needed.

4b. Batch-mode handoff (apply mode only):
   - Count pages classified as `upgrade-needed` (excluding `blocked-content-loss-risk`).
   - If count > 2:
     - Generate a phase in `tasks/todo.md` titled "## Phase: Upgrade Interrogation Pages" with:
       - Execution Profile: serial
       - A Context block listing the standards sources discovered in step 2 and the archive timestamp path (`docs/history/archive/YYYY-MM-DD/HHMMSS/`)
       - One checklist step per upgrade-needed page: `- [ ] Upgrade interrogation/<filename>.html — archive original, rewrite to current standard preserving all content, verify content preservation`
       - A final step: `- [ ] Run node scripts/audit-interrogation-pages.mjs and verify all archives; commit and push`
       - Acceptance criteria matching the audit findings
     - If `tasks/todo.md` already has unchecked items, append the phase at the bottom with a separator (`---`) and warn the user about pre-existing items.
     - Output the full audit report.
     - Report: "Generated exec-loop task plan with N steps. Recommended next route: approved task artifact"
     - Stop. Do not modify any HTML files.
   - If count <= 2: proceed to step 5 (inline apply).

5. Apply only when explicit:
   - Before replacing each page, archive the original to `docs/history/archive/YYYY-MM-DD/HHMMSS/interrogation/<filename>.html`.
   - Rewrite the page contextually from the original, preserving page-specific assumptions, questions, gates, coverage context, and prior answers.
   - Preserve the round filename, the `r{N}` round number, and the `data-answer-sidecar` path on rewrite.
   - Author the now-required helpers — `data-recommended-answer`, `data-agent-confidence`, and `data-apply-recommended` — for each open question from the page's own elicitation context.
   - Ensure each `data-apply-recommended` button is labeled `Apply recommended`, fills the nearest `data-open-input` from the nearest `data-recommended-answer`, confirms before replacing non-empty input, dispatches `input` and `change` events after setting the value, supports textarea and text input controls, and does not use clipboard APIs.
   - Add or modernize missing standard markers without replacing the page with a generic template.
   - Preserve relative links and keep the page self-contained unless the original already used explicit external resources.
   - Highlight upgrade changes where useful with inline notes, a change summary section, or scoped diff styling.

6. Verify after apply:
   - Confirm every changed page has a matching archive copy.
   - Re-open each changed page textually and confirm the preserved title, assumptions, questions, recommended answers, apply-recommended controls/scripts, and gates still exist.
   - Run `node scripts/audit-interrogation-pages.mjs` to confirm the changed pages now conform to the convention.

## Audit Report

Include:

- Target repository and mode.
- Standards sources read.
- Pages inspected and pages excluded.
- Per-page status with missing standard features.
- Content preservation risks or blockers.
- In apply mode, archive paths and changed page paths.
- Verification performed.
- Next action: usually `node scripts/audit-interrogation-pages.mjs` after successful apply, or no mutation needed when all pages are current.
- In batch mode: the generated `tasks/todo.md` phase with execution steps and the approved-artifact route.

## Constraints

- Do not edit `CLAUDE.md`, `AGENTS.md`, any `SKILL.md`, or any bundled `INTERROGATION-PAGE.md` file.
- Do not modify non-interrogation HTML files.
- Do not rewrite pages in audit/dry-run mode.
- Do not replace page-specific content with a generic template.
- Stop and report when an upgrade is likely to lose assumptions, questions, recommended answers, apply-recommended controls/scripts, gates, or coverage context.
- Do not create or modify GitHub Actions workflows.

## Default Shipping Contract

- **Audit mode:** no file mutations; no commit or push.
- **Apply mode (inline, ≤2 pages):** modified generated interrogation pages and archive copies are normal repo artifacts. Follow the target repository's shipping rules after verification.
- **Apply mode (batch, >2 pages):** generates `tasks/todo.md` phase only; does not modify any HTML files. Commit the task plan, then stop; the approved task artifact records the next executable step.
- **Default next-step routing:** after successful inline apply, `Recommended next command: node scripts/audit-interrogation-pages.mjs`; after batch-mode handoff, `Recommended next route: approved task artifact`; otherwise report the audit result and recommend no follow-up skill when no upgrades are needed.
