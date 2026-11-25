---
name: pwrl-refresh-learnings
description: Review and update existing learnings to keep knowledge current
argument-hint: "[scope like category, tag, date range, or file:path]"
---

# PWRL Refresh Learnings

Review existing learnings for staleness, consolidation opportunities, or needed updates.

## Interaction Method

- Use platform's `ask_user_question`, `ask_user`, `ask_user_input`, `vscode/askQuestions` or any available extension/tool for user interaction for all decisions
- Ask one question at a time
- Use multiple-choice questions when possible
- If input is empty, ask: "What learnings would you like to refresh? Provide a category, tag, file path, or scope to review."
- Provide clear recovery suggestions when errors occur

## Purpose

- Keep `docs/learnings/` accurate, current, and non-duplicative
- Decide what to update/consolidate/archive, then execute with user approval
- Sync `docs/learnings/INDEX.md` so descriptions stay current

## Usage

```bash
/pwrl-refresh-learnings
/pwrl-refresh-learnings authentication
/pwrl-refresh-learnings technical-fix
/pwrl-refresh-learnings file:docs/learnings/pattern/example.md
```

## Support Files

- `references/assessment-criteria.md` — Assessment methodology and update procedures
- `docs/learnings/INDEX.md` — Canonical index to audit and sync

## Workflow

### Phase 1: Select Scope

1. If no scope is provided, ask the user what to review (file, category, tag/keyword, date range).
2. Load `docs/learnings/INDEX.md` first and use it as the candidate list when possible.
3. Limit scope to a small batch (target 3-10 docs). If it’s broader, ask the user to narrow.

### Phase 2: Assess and Propose Actions

1. Read each candidate learning end-to-end.
2. Assess freshness, duplication, and gaps (use `references/assessment-criteria.md`).
3. Propose one action per doc:
   - **Current** (no change)
   - **Update** (improve or extend)
   - **Superseded** (link to newer doc)
   - **Consolidate** (merge duplicates)
   - **Archive** (move to `docs/learnings/archive/`)
4. Present the proposed action list and ask the user what to execute.

### Phase 3: Execute and Sync Index

1. Apply the selected updates (preserve intent; don’t delete without archiving).
2. After changes, sync `docs/learnings/INDEX.md` (or run `/pwrl-update-learnings` if available).
3. Report what changed and what was intentionally left unchanged.

## Acceptance Criteria

- Scope is clearly defined and candidates are identified from `docs/learnings/INDEX.md` when possible
- Each reviewed doc has an explicit proposed action (Current/Update/Superseded/Consolidate/Archive)
- If updates are executed, `docs/learnings/INDEX.md` is updated to match the new state

## When to Use

- After major refactors, migrations, or dependency upgrades
- When you notice duplicates or contradictions in `docs/learnings/`
- Periodically for high-churn areas (auth, CI, infra, build tooling)

## Best Practices

- Ask before archiving or consolidating; prefer reversible changes
- Preserve the original learning’s intent; add context rather than rewriting history
- Keep scope small (3-10 docs) to avoid turning refresh into a multi-day project

## Rules

- Never delete learnings; archive instead when removing from active use.
- When consolidating, keep one canonical doc and update incoming links.
- After executing updates, sync `docs/learnings/INDEX.md` (or run `/pwrl-update-learnings`).
- If anything is ambiguous, stop and ask the user before applying changes.
