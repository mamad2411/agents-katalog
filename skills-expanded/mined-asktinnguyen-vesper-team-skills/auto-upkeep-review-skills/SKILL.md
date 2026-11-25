---
name: auto-upkeep-review-skills
description: "Use when setting up or running a weekly skill garden: audit Hermes/Codex/Vesper skill libraries, prune sediment, review quality standards, and report safe upkeep actions without deleting user work."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [skills, upkeep, curation, cron, quality-review]
    related_skills: [writing-great-skills, hermes-skill-lifecycle-management, hermes-skill-curation]
---

# Auto Upkeep Review Skills

## Overview

Use this skill as the weekly **skill garden** for Hermes and sibling agent skill libraries. The garden finds sediment, sprawl, duplication, broken support-file links, weak descriptions, and stale cross-harness copies before they become default context load or user-facing drift.

The default scheduled mode is **audit-first**: produce a concise report with recommended patches, disables, consolidations, and verification commands. Do not delete, archive, disable, or rewrite skills during an unattended cron run unless the cron prompt explicitly grants that scope.

## When to Use

- The user asks to schedule weekly skill upkeep, review skill quality, prune skills, or audit the active skill library.
- A cron job runs this skill to produce a recurring skills-quality report.
- Another skill-maintenance workflow needs a safe, repeatable checklist for pruning sediment and keeping descriptions sharp.

Don't use this for one-off external skill installation unless paired with `hermes-skill-lifecycle-management`.

## Operating Modes

### Weekly audit mode

Run when unattended or scheduled. Inspect, classify, and report. The completion criterion is a dated report that names every checked root, summarizes counts, and separates safe recommendations from actions requiring approval.

### Apply mode

Run only when the user explicitly asks to apply fixes. Make reversible edits first, use `skill_manage(action='patch')` for targeted changes, and verify the active registry afterward. The completion criterion is a list of exact paths changed plus verification output.

## Weekly Skill Garden Loop

1. **Load the quality bar.** Load `writing-great-skills`, `hermes-skill-lifecycle-management`, and `hermes-skill-curation` before reviewing content. Continue only after their rules are available.

2. **Inventory roots.** List active Hermes skills with `skills_list({})`, then inspect relevant on-disk roots when present:
   - `C:/Users/Admin/.hermes/skills`
   - `C:/Users/Admin/.agents/skills`
   - `C:/Users/Admin/.codex/skills`
   - `C:/Users/Admin/.codex/plugins/local/tin-global-skills/plugins/tin-workflow-skills/skills`
   - `C:/Users/Admin/.codex/plugins/cache/tin-global-skills/tin-workflow-skills/1.0.0/skills`
   - `C:/Users/Admin/.vesper/skills`

   Completion criterion: the report states which roots existed, which were skipped, and the skill count per existing root.

3. **Choose a review sample.** For a weekly run, inspect the highest-risk set instead of every file blindly:
   - newly added or recently modified skills;
   - skills with long `SKILL.md` files;
   - skills whose names/descriptions suggest overlap;
   - skills with support-file directories;
   - skills copied across multiple harnesses.

   Completion criterion: the report explains why each reviewed skill was selected.

4. **Apply the garden tests.** For each reviewed skill, check:
   - **Invocation:** description has distinct trigger branches and no synonym padding.
   - **Hierarchy:** always-needed steps are inline; bulky branch reference is behind pointers.
   - **Completion criteria:** ordered steps end with checkable done conditions.
   - **Single source:** duplicated rules are consolidated or flagged.
   - **No-op prose:** generic advice is deleted or replaced with a measurable criterion.
   - **Sediment:** stale session-specific detail is moved to reference, memory/session history, or removed.
   - **Cross-harness drift:** matching skill names across Hermes/Codex/Vesper have intentional differences or matching hashes.

   Completion criterion: each reviewed skill gets a pass/warn/fix-needed status with one-line rationale.

5. **Prefer reversible pruning.** Recommend config disablement or consolidation before deletion. For protected, bundled, or third-party skills, do not edit source directly; recommend a user-owned wrapper, disablement, or upstream sync.

   Completion criterion: every destructive or broad action is marked `requires approval`.

6. **Draft patch candidates.** When a fix is obvious, include a compact patch proposal: target path, old meaning, new meaning, and reason. Keep patch proposals class-level; do not encode one-off session outcomes.

   Completion criterion: proposed patches are small enough for a future `skill_manage(action='patch')` call or clearly labeled as a rewrite.

7. **Write the report.** Save longer findings to a dated local report under `C:/Users/Admin/.hermes/reports/skills-upkeep/` when filesystem access is available. Final chat output should be short: counts, top findings, proposed actions, and whether approval is needed.

   Completion criterion: the user can act from the final response without reading raw logs.

## Cron Recipe

Create a weekly audit job with this skill attached. Use a self-contained prompt because cron runs do not inherit chat context.

Suggested schedule: Monday 09:00 local time. Hermes cron accepts numeric weekdays, so use `1` for Monday.

```text
schedule: 0 9 * * 1
skills: [auto-upkeep-review-skills]
prompt: Run weekly audit mode for Tin's Hermes/Codex/Vesper skill libraries. Inspect active and on-disk skill roots, review recently modified/high-risk skills against writing-great-skills quality standards, save a dated report under C:/Users/Admin/.hermes/reports/skills-upkeep/, and send a concise summary with proposed safe upkeep actions. Do not delete, disable, archive, or rewrite skills unless explicitly approved in the prompt.
```

## Reporting Format

```markdown
## Weekly Skill Garden — YYYY-MM-DD

Roots checked:
- <root>: <count or skipped reason>

Reviewed:
- <skill>: <pass|warn|fix-needed> — <reason>

Top recommendations:
1. <action> — <why> — <safe now|requires approval>

Files written:
- <report path>
```

## Common Pitfalls

1. **Turning audit into unapproved cleanup.** Weekly cron should surface work, not surprise-delete or disable capabilities.
2. **Counting files as quality.** A large skill library can be healthy; judge by relevance, duplication, and process predictability.
3. **Creating narrow reminder skills.** Fold recurring maintenance lessons into this garden or a class-level umbrella.
4. **Ignoring support files.** Broken `references/`, `templates/`, `scripts/`, or `assets/` links make a skill fail at runtime even when `SKILL.md` looks fine.
5. **Letting cross-harness copies drift silently.** If Hermes, Codex, and Vesper copies intentionally differ, document why; otherwise sync from a reviewed source.

## Verification Checklist

- [ ] Required quality and lifecycle skills were loaded.
- [ ] Existing roots and skipped roots were both reported.
- [ ] Reviewed skills were selected by risk, recency, overlap, or size.
- [ ] Findings distinguish audit-only recommendations from approved edits.
- [ ] Destructive actions are marked `requires approval`.
- [ ] Any changed files are listed with exact paths and verified after the edit.
- [ ] Weekly report path is included when a report file is written.
