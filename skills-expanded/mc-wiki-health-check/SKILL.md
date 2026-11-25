---
name: mc-wiki-health-check
description: Periodically run the wiki lint and report findings — broken page links, missing image / file refs, orphan pages, tag drift. Read-only (never modifies the wiki). Use when the user asks to "check the wiki", "lint the wiki", or runs on the bundled weekly schedule below to surface drift before it accumulates. (#1491 Phase D, Karpathy "lint" operation.)
schedule: interval 168h
---

# Wiki Health Check

A bundled MulmoClaude preset skill (`mc-` prefix = launcher-managed; do not edit
this file in the workspace, it is overwritten on every server boot).

This is the **lint** operation from the LLM-Wiki pattern: a periodic, fully
**read-only** sweep that flags drift in `data/wiki/` (broken links, orphan
pages, tag mismatches, missing image / file refs) so the user can fix it
before it compounds. Findings only — this skill never writes to the wiki.

## What to do

1. Invoke `manageWiki` with `{ "action": "lint_report" }`. The server returns
   the structured report (re-uses the same lint helpers that power the
   on-demand "Wiki Lint" button).
2. **Healthy wiki** (zero findings): reply with one line — "Wiki is healthy
   (N pages checked)." — and stop. Do not page the user; the value of a
   weekly run is the silence on healthy weeks.
3. **Findings present**: render a short, grouped report:
   - Broken `[[page]]` / `![](path)` links — list `source slug → target` with
     the file path so the user can jump straight to the offending page.
   - Missing image / file refs — same shape.
   - Orphan pages (no incoming links) — list slugs; suggest either linking
     from `index.md` / a hub page, or archiving if obsolete.
   - Tag drift (tag in `index.md` ≠ tag in page frontmatter) — list the
     mismatches.
   Keep the prose minimal. The lint report's own `formatLintReport` output is
   already terse and well-grouped; prefer pasting it over re-narrating.
4. **Do not auto-fix.** Each finding is a decision the user must make
   (rename vs delete, add a backlink vs archive, fix the tag in which
   place). Offer to fix any specific one if the user picks it up, but never
   write to the wiki as part of this scheduled run.

## Rules

- **Read-only**: this skill never calls `manageWiki` with `action` other than
  `lint_report`. Any "fix" the user agrees to should be a follow-up turn so
  the boundary stays clear.
- **Quiet on success**: a healthy wiki run ends in one line. Don't expand the
  report when there's nothing to report — the schedule's value is catching
  drift, not generating weekly noise.
- **Don't open files unless asked**: the lint output already names the
  offending slugs and paths. The user reads and decides; they'll ask to open
  a specific page if they want detail.
- **Cadence**: bundled schedule is `interval 168h` (≈ weekly). The user can
  star this preset to opt in, or change the cadence by editing the
  re-registered task in `/automations` after activation.

## Out of scope (RFC #1491 follow-ups)

- LLM-driven lint extensions: contradiction detection across pages, stale
  claims (date-aware), missing-concepts gap analysis. Tracked as Phase B of
  the RFC; this preset deliberately covers only the structural lint that's
  already in the codebase.
- Auto-fix / promote-answer-to-page workflows: Phases A / C of the RFC.
