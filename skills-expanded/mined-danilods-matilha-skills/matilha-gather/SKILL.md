---
name: matilha-gather
description: Use when completed subprojects are ready to merge — validates SP-DONE.md strict gates, merges --no-ff in merge_order, runs per-SP regression, updates wave-NN-status.md.
category: matilha
version: "1.0.0"
optional_companions: []
---

## When this fires

After `/matilha-hunt` dispatched a wave and every SP has written a filled `SP-DONE.md`, the user wants to merge them back and verify regression. This skill is the inverse of `/matilha-hunt`: it consumes `wave-NN-status.md`, validates gates, merges in order, runs tests after each merge, and updates status.

## Preconditions

- `docs/matilha/waves/wave-NN-status.md` exists and validates against `waveSchema`.
- Current branch is the integration branch (not `wave-NN-sp-*`).
- Working tree clean.
- Every SP's `SP-DONE.md` passes strict gates.

## Execution Workflow

1. Read `docs/matilha/waves/wave-NN-status.md` via Read tool; validate against `waveSchema`.
2. Swiss Cheese pre-flight via Bash: verify current branch is not an SP branch (`git rev-parse --abbrev-ref HEAD`); verify clean tree (`git status --porcelain`).
3. For each SP in `merge_order` where status is not `completed`: validate `<worktree>/SP-DONE.md` strict gates (status=completed, tests.passed=true, non-empty commits[], non-null completed_at, tests.count>=1, sp_id/feature/wave match).
4. If `--dry-run`: emit merge plan preview and exit.
5. For each SP in merge_order: `git merge --no-ff <branch>` via Bash; on conflict, run `git merge --abort` and HALT (5-rule error with conflicting files).
6. After each successful merge: run test command (default `npm test` via Bash); on failure, HALT (5-rule error with `git reset --hard <pre-merge-sha>` recovery).
7. Update wave-status: mark SP merged (status: completed).
8. After all SPs merged: mark wave completed, regression_status: passed, ended: <iso>.
9. If `--cleanup`: for each completed SP, `git worktree remove --force <path>` + `git branch -d <branch>`.

## Rules: Do

- Validate SP-DONE gates BEFORE any merge (all-or-nothing pre-flight).
- Run `git merge --no-ff` (preserve merge commits as wave markers).
- Run test command after every merge (localize regressions).
- Commit wave-status.md after each mutation for atomicity.

## Rules: Don't

- Auto-rollback on failure (HALT preserves state for inspection).
- Force-merge or skip regression.
- Delete unmerged branches (safe `-d`, not `-D`).
- Advance project-status.md current_phase (attest owns that).

## Expected Behavior

On success, all SP branches merged into main in declared order + regression passed + wave-status updated. On failure, state preserved; 5-rule error with exact recovery commands.

## Quality Gates

- All SPs in wave-status have `status: completed`.
- Test suite passes after every merge.
- `wave-NN-status.md` always round-trips through `waveSchema` between updates.
- `.gitignore` unchanged by gather.
- `current_phase` unchanged by gather.

## Companion Integration

No companion integrations in Wave 4a. Review and quality delegation is Wave 3c's /matilha-review territory.

## Output Artifacts

- Updated `docs/matilha/waves/wave-NN-status.md` (status, regression_status, started, ended, per-SP status).
- N merge commits on integration branch.
- (With --cleanup) worktrees removed + branches deleted for completed SPs.

## Example Constraint Language

- Use "must" for: wave-status validates against waveSchema before any merge; current branch is not SP branch; working tree is clean; every SP-DONE.md passes strict gates.
- Use "should" for: run `--dry-run` first; commit wave-status after each gather; wait for wave to settle before `--cleanup`.
- Use "may" for: `--cleanup` (opt-in); reset failed SP entry to `pending` after manual recovery to resume.

## Troubleshooting

- **"wave-NN-status.md not found"**: Run `/matilha-hunt <slug> --wave N` first.
- **"SP-DONE.md has status=pending"**: SP author did not finish; ask them or re-dispatch via `matilha hunt --force --wave N`.
- **"merge conflict"**: Plan's intra-wave disjunction was bypassed; edit plan to move overlap to later wave, re-run `/matilha-hunt --force`.
- **"regression failed after merge"**: Revert via `git reset --hard <sha>` (SHA in error output); fix regression; re-run `/matilha-gather`.
- **"on SP branch"**: `git checkout main` before retrying.
- **"already gathered — no-op"**: Wave already at status: completed.
- **"uncommitted changes"**: Commit wave-status.md (or other edits) before resume.

## CLI shortcut (optional)

> If matilha CLI is installed (`matilha --version` succeeds), you can run
> `matilha gather <slug>` to execute this deterministically. The plugin path
> above works without any CLI installation.
