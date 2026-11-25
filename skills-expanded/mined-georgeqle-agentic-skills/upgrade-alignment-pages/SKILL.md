---
name: upgrade-alignment-pages
description: Audit and explicitly upgrade generated alignment/*.html review pages to the current local alignment-page standard while preserving page-specific context
type: ops
version: v0.2
argument-hint: "[--repo <path>] [--apply] [alignment/*.html...]"
---

# Upgrade Alignment Pages

Invoke as `$upgrade-alignment-pages`.

Use this skill when a repository already has generated `alignment/*.html` review pages and the user wants to audit or update them against the current local alignment-page convention. This skill targets generated alignment HTML artifacts only.

## Inputs

- Default target repository: current working directory.
- Optional `--repo <path>` to target another repository.
- Optional explicit page paths under the target repository's `alignment/` directory.
- Optional `--apply`, or clear user wording such as "apply the upgrade" or "upgrade these pages", to allow page rewrites.

## Mode

- Default mode is audit/dry-run.
- The skill name alone is not apply intent; do not modify files unless the visible user request explicitly asks to apply or upgrade existing pages.
- In audit/dry-run mode, inspect pages and report drift without creating, editing, moving, or deleting any files.

## Process

1. Resolve scope:
   - Locate the project-root `alignment/` directory; stop if absent.
   - Enumerate `alignment/*.html`, excluding `alignment/index.html`.
   - If the user provided page paths, include only those paths after confirming they are inside the project-root `alignment/` directory.

2. Load local standards:
   - Read applicable local convention sources from `AGENTS.md`, `CLAUDE.md`, and active bundled `ALIGNMENT-PAGE.md` files found under `global/`, `packs/`, `.claude/skills/`, and `.codex/skills/`.
   - Treat those local files as read-only standards. Do not fetch external standards.
   - Extract the current required HTML behaviors: dark-mode styling, inline approval gates, section feedback controls, local section feedback YAML, unified response YAML, copy fallback behavior, unanswered-question handling, archive-before-replace behavior, and diff/change highlighting for updates.

3. Audit every selected page:
   - Read the whole HTML file before judging it.
   - Identify page-specific substance: title, meta/context, research findings, evidence/source matrices, assumptions, decisions, open questions, approval gates, review notes, proposed file changes, prior user feedback, and any page-specific scripts.
   - Report missing or stale standard features per page.
   - Classify each page as `current`, `upgrade-needed`, or `blocked-content-loss-risk`.

4. Stop on content-loss risk:
   - If a page's structure is too ambiguous to upgrade while preserving substantive content, do not rewrite it.
   - Report exactly what content could not be mapped and what human decision is needed.

4b. Batch-mode handoff (apply mode only):
   - Count pages classified as `upgrade-needed` (excluding `blocked-content-loss-risk`).
   - If count > 2:
     - Generate a phase in `tasks/todo.md` titled "## Phase: Upgrade Alignment Pages" with:
       - Execution Profile: serial
       - A Context block listing the standards sources discovered in step 2 and the archive timestamp path (`docs/history/archive/YYYY-MM-DD/HHMMSS/`)
       - One checklist step per upgrade-needed page: `- [ ] Upgrade alignment/<filename>.html — archive original, rewrite to current standard preserving all content, verify content preservation`
       - A final step: `- [ ] Run $compile-central-alignment and verify all archives; commit and push`
       - Acceptance criteria matching the audit findings
     - If `tasks/todo.md` already has unchecked items, append the phase at the bottom with a separator (`---`) and warn the user about pre-existing items.
     - Output the full audit report.
     - Report: "Generated exec-loop task plan with N steps. Recommended next command: $exec"
     - Stop. Do not modify any HTML files.
   - If count <= 2: proceed to step 5 (inline apply).

5. Apply only when explicit:
   - Before replacing each page, archive the original to `docs/history/archive/YYYY-MM-DD/HHMMSS/alignment/<filename>.html`.
   - Rewrite the page contextually from the original, preserving page-specific research, decisions, questions, gates, review context, and user feedback.
   - Add or modernize missing standard elements without replacing the page with a generic template.
   - Preserve relative links and keep the page self-contained unless the original already used explicit external resources.
   - Highlight upgrade changes where useful with inline notes, a change summary section, or scoped diff styling.

6. Verify after apply:
   - Confirm every changed page has a matching archive copy.
   - Re-open each changed page textually and confirm the preserved title, decisions/findings, questions, and gates still exist.
   - Run or recommend `$compile-central-alignment` so `alignment/index.html` reflects updated page metadata.

## Audit Report

Include:

- Target repository and mode.
- Standards sources read.
- Pages inspected and pages excluded.
- Per-page status with missing standard features.
- Content preservation risks or blockers.
- In apply mode, archive paths and changed page paths.
- Verification performed.
- Next action: usually `$compile-central-alignment` after successful apply, or no mutation needed when all pages are current.
- In batch mode: the generated `tasks/todo.md` phase with exec-loop steps and the recommended `$exec` command.

## Constraints

- Do not edit `CLAUDE.md`, `AGENTS.md`, any `SKILL.md`, or any bundled `ALIGNMENT-PAGE.md` file.
- Do not modify non-alignment HTML files.
- Do not modify `alignment/index.html`; leave index regeneration to `$compile-central-alignment`.
- Do not rewrite pages in audit/dry-run mode.
- Do not replace page-specific content with a generic template.
- Stop and report when an upgrade is likely to lose research, decisions, questions, gates, or review context.
- Do not create or modify GitHub Actions workflows.

## Default Shipping Contract

- **Audit mode:** no file mutations; no commit or push.
- **Apply mode (inline, ≤2 pages):** modified generated alignment pages and archive copies are normal repo artifacts. Follow the target repository's shipping rules after verification.
- **Apply mode (batch, >2 pages):** generates `tasks/todo.md` phase only; does not modify any HTML files. Commit the task plan, then hand off to `$exec`.
- **Default next-step routing:** after successful inline apply, `Recommended next command: $compile-central-alignment`; after batch-mode handoff, `Recommended next command: $exec`; otherwise report the audit result and recommend no follow-up skill when no upgrades are needed.
