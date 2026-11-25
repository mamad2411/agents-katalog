---
name: git-personal-team-branch-workflow
description: Proactive session discipline for working on a team
    branch while keeping personal sandbox commits always at the
    tip of a personal/<purpose> branch — commit team work on
    the team branch, then immediately restack the personal
    branch onto the new team tip.
category: Git & Repository Management
---

# Git Personal Team Branch Workflow Skill (v1)

> **Skill ID:** `git-personal-team-branch-workflow`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

You maintain a `personal/<purpose>` branch (e.g., `personal/skills`) that is a **superset** of a team branch (e.g.,
`<author>-<ticket-id>`): it contains every team commit AND personal-only commits stacked at the tip. While actively
working on team tickets, you need to:

- Commit team work on the team branch (never mix personal files into team commits).
- Keep personal commits always at the tip of `personal/<purpose>` — never let them drift below new team commits.
- Verify that the personal branch is always restacked immediately after each team commit.
- At session end, push both branches to their respective remotes.

This skill provides the **session discipline** — the daily cadence of branch switching, incremental restack, and
verification — that keeps the invariant `personal/<purpose>` = `[team commits] + [personal commits at tip]` across an
entire work session.

**This is NOT a reactive extraction skill.** If you already have a mixed branch (team + personal commits interleaved),
use [`git-personal-content-extraction`](../git-personal-content-extraction/SKILL.md) to disentangle it first. This skill
prevents mixing from happening in the first place.

## Composition Rationale

This skill is a **composer** — it orchestrates the following primitives without reimplementing them:

| Composed Skill | Used for |
| --- | --- |
| [`git-personal-sandbox-remote`](../git-personal-sandbox-remote/SKILL.md) | **Prerequisite** — the dual-remote setup (`origin` + `personal`) and `personal/<purpose>` branch creation. This skill assumes that setup already exists. |
| [`git-personal-sandbox-restack`](../git-personal-sandbox-restack/SKILL.md) §3 | The six-axis equality audit that verifies no personal content is lost during the restack. This skill provides the incremental session cadence; the restack skill provides the verification rigour. |
| [`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md) | The team-commit discipline — each team ticket change is committed as an independent atomic unit on the team branch. |
| [`redaction-portability`](../redaction-portability/SKILL.md) | Sanitizing any conversation log / case study produced from this workflow. |

The composer **MUST NOT** reimplement dual-remote provisioning, restack verification, or atomic-commit mechanics — those
are the owners' jobs.

## Related Skills

- [`git-personal-content-extraction`](../git-personal-content-extraction/SKILL.md) — **sibling skill** for the
  *reactive* case: when team and personal commits are already mixed on a single branch, use extraction to purify the
  branch and move personal commits to the personal sandbox. This skill (the proactive discipline) and the extraction
  skill (the reactive cleanup) cover the complete personal-team branch lifecycle.
- [`git-dependent-branch-restack-cascade`](../git-dependent-branch-restack-cascade/SKILL.md) — the N-dependent
  generalization of `git-personal-sandbox-restack`. Use it when MORE THAN ONE branch (personal sandbox + diagnostics +
  feature stack) is stacked on a base that just moved.
- [`git-branch-promotion`](../git-branch-promotion/SKILL.md) — when you need to move a commit FROM the personal
  sandbox INTO the team branch (e.g., a personal experiment that should now go upstream).

## Source Rules

| Rule File | Scope Incorporated |
| --- | --- |
| [`ai-rule-standardization-rules.md`](../../../ai-agent-rules/ai-rule-standardization-rules.md) | Skill-First Architecture, Layered Composition Mandate |
| [`git-personal-sandbox-remote/SKILL.md`](../git-personal-sandbox-remote/SKILL.md) | Dual-remote setup and personal-branch creation (prerequisite contract) |
| [`git-personal-sandbox-restack/SKILL.md`](../git-personal-sandbox-restack/SKILL.md) §3 | Six-axis equality audit for restack verification |
| [`git-atomic-commit-construction/SKILL.md`](../git-atomic-commit-construction/SKILL.md) | Atomic commit discipline on the team branch |

***

## 1. When to Apply

Apply this skill when ALL of the following hold:

- A `personal/<purpose>` branch exists (created via [`git-personal-sandbox-remote`](../git-personal-sandbox-
  remote/SKILL.md)).
- `personal/<purpose>` is a **superset** of the team branch: it contains all team commits PLUS personal-only commits
  at the tip.
- The `personal` remote is configured and guardrails are in place (`remote.origin.push` negates
  `^refs/heads/personal/*`).
- You are actively working on team tickets, committing to the team branch.
- You want personal commits to remain at the tip of `personal/<purpose>` at all times — never mixed below new team
  commits.

Do NOT apply when:

- You do NOT have a dual-remote setup — first run [`git-personal-sandbox-remote`](../git-personal-sandbox-
  remote/SKILL.md).
- The `personal/<purpose>` branch has already drifted and is NOT a superset of the team branch — use [`git-personal-
  content-extraction`](../git-personal-content-extraction/SKILL.md) to repair first.
- The personal branch contains commits that were NOT replayed on top of the latest team commits — run [`git-personal-
  sandbox-restack`](../git-personal-sandbox-restack/SKILL.md) to realign first.

***

## 2. Prerequisites

| Requirement | Minimum |
| --- | --- |
| VCS | Git 2.23+ |
| Shell | Python 3.12+ (for the companion script) or POSIX shell |
| Remote | `personal` remote configured per [`git-personal-sandbox-remote`](../git-personal-sandbox-remote/SKILL.md) |
| Guardrails | `remote.origin.push` configured to negate `^refs/heads/personal/*` |
| Tags | Per-session backup tags (`backup/personal-pre-restack-<date>`) are created before each restack |

***

## 3. Session Workflow

### 3.1 Session Start

1. **Verify the invariant:**

   ```bash
   git merge-base <team-branch> <personal-branch>
   git log --oneline <team-branch>..<personal-branch>
   ```

   Confirm that every commit listed in the second output is a personal-only commit. The merge-base
   should be the team-branch tip. If `personal/<purpose>` contains commits that the team branch does
   NOT have and that are NOT personal, promote those first via
   [`git-branch-promotion`](../git-branch-promotion/SKILL.md).

2. **Ensure the working tree is clean:**

   ```bash
   git status --short   # MUST be empty
   ```

3. **Switch to the team branch:**

   ```bash
   git checkout <team-branch>
   ```

### 3.2 Team Work Cycle

This is the core loop — performed once per atomic team commit:

1. **Work on the team branch.** Make your changes. Stage and commit per [`git-atomic-commit-construction`](../git-
atomic-commit-construction/SKILL.md).

2. **Tag the commit** for traceability (optional but recommended):

   ```bash
   git tag <ticket-id>-<n>
   ```

3. **Restack the personal branch onto the new team tip** — immediately, before switching context:

   ```bash
   python3 .agents/skills/git-personal-team-branch-workflow/scripts/rebase-personal-on-team.py \
       --team-branch <team-branch> \
       --personal-branch <personal-branch> \
       --repo-path .
   ```

   This script (shipped with this skill) tags the pre-restack state, restacks, and verifies.

   **Manual equivalent** (when the script is unavailable):

   ```bash
   # 1. Remember the pre-restack tip
   PRE=$(git rev-parse <personal-branch>)
   git tag "backup/personal-pre-restack-$(date +%Y-%m-%d)" $PRE

   # 2. Restack
   BASE=$(git merge-base <team-branch> <personal-branch>)
   git rebase --onto <team-branch> $BASE <personal-branch>

   # 3. Quick verification
   echo "=== Personal commits at tip ==="
   git log --oneline <team-branch>..<personal-branch>
   ```

4. **Verify** that the personal commits are still at the tip:

   ```bash
   git log --oneline <team-branch>..<personal-branch>
   ```

   The output MUST contain only personal-only commits. If it contains team commits (meaning the
   restack failed or was incomplete), STOP and run
   [`git-personal-sandbox-restack`](../git-personal-sandbox-restack/SKILL.md) §3 (six-axis audit)
   before proceeding.

5. **Switch back to the team branch** for the next work cycle:

   ```bash
   git checkout <team-branch>
   ```

**Tagging convention** for commit messages:

- `[team]` prefix for team commits (e.g., `feat: [team] add density toggle`)
- `[personal]` prefix for personal-only commits (e.g., `feat(skills): [personal] add debug skill`)

### 3.3 Session End

1. **Push the team branch to `origin`:**

   ```bash
   git push origin <team-branch>
   ```

2. **Push `personal/<purpose>` to `personal`:**

   ```bash
   git push personal <personal-branch>
   ```

   Force-push is required when the personal branch history has been rewritten by the restacks. Always use `--force-with-lease`:

   ```bash
   git push --force-with-lease personal <personal-branch>
   ```

3. **Clean up per-session backup tags** (after external verification):

   ```bash
   git tag -d "backup/personal-pre-restack-$(date +%Y-%m-%d)"
   ```

4. **Verify both remotes:**

   ```bash
   git branch -vv | grep -E '^\*|personal|origin'
   ```

***

## 4. The `rebase-personal-on-team` Script

The companion script [`scripts/rebase-personal-on-team.py`](scripts/rebase-personal-on-team.py) automates the
incremental restack step (§3.2 step 3).

**Invocation:**

```bash
python3 scripts/rebase-personal-on-team.py \
    --team-branch <team-branch> \
    --personal-branch <personal-branch> \
    --repo-path <path>
```

**What it does:**

1. **Validates preconditions**: both branches exist, working tree is clean, `personal-branch` is a descendant of `team-
branch`.
2. **Tags** the personal-branch tip as `backup/personal-pre-restack-<date>-<timestamp>`.
3. **Discovers the merge-base** of `team-branch` and `personal-branch`.
4. **Restacks**: runs `git rebase --onto <team-branch> <merge-base> <personal-branch>`.
5. **Verifies**: confirms `personal-branch` HEAD differs from `team-branch` HEAD (personal commits are on top).
6. **Reports** the new commit list (`team-branch..personal-branch`) for manual review.

**Exit codes:**

| Code | Meaning |
| --- | --- |
| 0 | Restack succeeded, personal commits verified at tip |
| 1 | Precondition failure (branches missing, dirty tree, not a descendant) |
| 2 | Restack failed (rebase conflict or error) |
| 3 | Post-restack verification failed (no personal commits at tip or tip collapsed) |

***

## 5. Pitfalls & Recovery

### 5.1 Conflict during incremental restack

Symptom: `git rebase --onto` stops with a conflict.

Cause: The new team commit modified a file that the personal branch also modifies.

Resolution: Resolve the conflict manually, then:

```bash
git add <resolved-files>
git rebase --continue
```

Then run the six-axis audit per [`git-personal-sandbox-restack`](../git-personal-sandbox-restack/SKILL.md) §3 before
continuing.

### 5.2 Personal tip collapsed (no personal commits visible)

Symptom: After restack, `git log --oneline <team-branch>..<personal-branch>` is empty.

Cause: The personal commits were no-ops on the new base (the changes they introduced already exist in the new team
commit). This can happen when a team fix duplicates a personal workaround.

Resolution:

1. Reset to the backup tag: `git checkout -b recovery backup/personal-pre-restack-<date>`
2. Review the lost personal commits: `git log <personal-branch>..recovery`
3. Cherry-pick any that should be re-applied: `git checkout <personal-branch> && git cherry-pick <sha>`

### 5.3 Forget to restack before switching contexts

Symptom: You committed on the team branch, then started new work on the personal branch without restacking. Now personal
commits are below the new team commit.

Resolution: Run the restack immediately — it will reorder correctly as long as you haven't committed personal work on
top of the mixed state:

```bash
git checkout <personal-branch>
git rebase --onto <team-branch> <old-merge-base> <personal-branch>
```

If you HAVE committed personal work after the new team commit, use [`git-personal-content-extraction`](../git-personal-
content-extraction/SKILL.md) to reorder.

### 5.4 IDE file-lock prevents checkout

When VS Code / Eclipse / another editor is indexing, `git checkout` during step 3.1 can fail with `Deletion of directory
'<path>' failed.` Recover with `git reset --hard HEAD`, close the editor, then retry.

### 5.5 Guardrail not configured

If `git push` to `origin` threatens to push personal branches, configure the guardrail:

```bash
git config --local remote.origin.push '^refs/heads/personal/*'
```

***

## 6. Acceptance Criteria

The session workflow is complete when:

1. Every team commit was made on the team branch (not on `personal/<purpose>`).
2. After each team commit, `personal/<purpose>` was restacked onto the new team tip.
3. At session end, `personal/<purpose>` is a superset of the team branch tip with personal commits at the top.
4. `git push origin <team-branch>` succeeded without personal content.
5. `git push --force-with-lease personal <personal-branch>` succeeded.
6. Backup tags are cleaned up after external verification.

***

## 7. Related Conversations & Traceability

- Session 2026-05-31 (acers-web ticket AES-53): original derivation of the personal-team-branch-workflow discipline,
  including the incremental restack cycle, commit tagging convention (`[team]` / `[personal]`), and the guardrail
  configuration.

All session logs MUST be sanitized through [`redaction-portability`](../redaction-portability/SKILL.md) before commit.
