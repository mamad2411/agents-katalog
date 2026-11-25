---
name: eliteforge-git-feature-oriented-spec
description: Git specification for feature-oriented development with full branch types, including non multi-agent, multi-agent base, and subagent branch and worktree tree naming.
metadata:
  version: 1.0.1
---

# EliteForge Git Feature-Oriented Spec

## Environment Variables

- `ELITEFORGE_SKILL_GIT_WORKTREE_ROOT` [optional] Root directory for generated git worktrees; defaults to `${CODEX_HOME:-$HOME/.codex}/worktrees`.

## Branch Spec

> main and master are equivalent

Follow the feature-oriented branching model. Continuously develop and test features.

Release-flow branches keep their project convention, such as `nightly`, `qa/<version>`, and `release/<version>`. Working branches only use `feature`, `bugfix`, or `hotfix` as `<type>`.

Non multi-agent branch name follows template: `<type>/<version>/<developer>[/<taskId>]/<taskName>`.

Multi-agent base branch name follows template: `<type>/<version>/<developer>[/<taskId>]/<taskName>/base`.

Codex subagent branch name follows template: `<type>/<version>/<developer>[/<taskId>]/<taskName>/<agentId>/<subtaskName>`.

- the `type` attribute only belongs to:
  - feature: new requirements
  - bugfix: bugs does not stuck the main process
  - hotfix: serious bugs requiring urgent fix
- the `version` attribute follows SemVer Spec `x.y.z`
- `developer` is the name of the developer from git config, use email prefix if the name is not set.
- `agentId` is not used in non multi-agent branches and is required for Codex subagents or parallel agents.
- Subagent `agentId` must use the role name only, for example `backend`, `frontend`, `test`, `review`, or `docs`.
- Put scope and target details in `taskName` or `subtaskName`, not in `agentId`.
- Do not use pure numbers, weak semantic names, numbered variants, or role-plus-target names such as `agent-01`, `backend-01`, `frontend-02`, `worker-a`, `tmp`, `work`, `backend-login-api`, `frontend-login-page`, or `test-auth-flow`.
- `taskId` is optional, only used for non multi-agent branches when the project has task management system and the task can be easily linked to the branch name.
- `taskName` and `subtaskName` should be concise and descriptive, use hyphen to separate words, avoid using special characters.
- Normalize each branch segment to lowercase filesystem-safe text using only `a-z`, `0-9`, `.`, `_`, and `-`.
- Do not use `/base` for non multi-agent workflows. Use `/base` only as the integration branch leaf after a task enters multi-agent workflow.
- If a task starts on a non multi-agent branch and later needs subagents, rename the existing branch to the matching `/base` branch before creating subagent branches. Do not keep both forms for the same task.

| origin branch | target branch | ops | notes |
| :--- | :--- | :--- | :--- |
| `master` | `feature/<version>/<developer>[/<taskId>]/<taskName>`、`feature/<version>/<developer>[/<taskId>]/<taskName>/base`、`qa/<version>`、`release/<version>` | create from `master` | development and unit testing |
| `master` | `feature/<version>/...`、`qa/<version>`、`release/<version>` | `git rebase` | always rebase `master` latest commits |
| `<type>/<version>/<developer>[/<taskId>]/<taskName>/base` | `<type>/<version>/<developer>[/<taskId>]/<taskName>/<agentId>/<subtaskName>` | create from multi-agent base branch | subtask implementation in isolated worktree |
| `<type>/<version>/<developer>[/<taskId>]/<taskName>/<agentId>/<subtaskName>` | `<type>/<version>/<developer>[/<taskId>]/<taskName>/base` | git merge | subtask branch must merge back to its corresponding multi-agent base branch after completion |
| `feature` | `nightly` | git merge | coding complete,no compilation errors |
| `feature` | `qa` | create merge request  | submit to testing, ensure version consistency |
| `feature` | `feature` | git rebase -i (squash commits) && git push -f  | squash mutiple commits of one feature |
| `feature`（squashed） | `release` | git merge | ensure completed testing |
| `release` | `release` | `git tag <version>` | ensure no snapshot/dev dependencies |
| `release` | `master` | Fast-forward only merge | after merge completed,ensure all other branches for the current version are cleaned up  |

## Worktree Spec

When using `git worktree`, the worktree path must mirror the branch tree and have a one-to-one relationship with the checked-out branch.

Worktree root is resolved dynamically:

```bash
worktree_root="${ELITEFORGE_SKILL_GIT_WORKTREE_ROOT:-${CODEX_HOME:-$HOME/.codex}/worktrees}"
```

- One worktree checks out exactly one spec-compliant branch.
- One spec-compliant branch must not be reused by multiple worktrees at the same time.
- Non multi-agent worktrees follow the non multi-agent branch tree: `<root>/<repo>/<type>/<version>/<developer>[/<taskId>]/<taskName>`.
- Multi-agent base worktree path follows template: `<root>/<repo>/<type>/<version>/<developer>[/<taskId>]/<taskName>/base`.
- Subagent worktree path follows template: `<root>/<repo>/<type>/<version>/<developer>[/<taskId>]/<taskName>/<agentId>/<subtaskName>`.
- Use the same semantic fields as the branch name; do not flatten path separators into a basename.
- Do not use project-ambiguous or weak worktree names such as `temp`, `new`, `work`, `scratch`, or `feature-clouds3n-add-login`.
- If converting an existing non multi-agent worktree to multi-agent mode, move or recreate the worktree at the `/base` path before adding subagent worktrees. Do not create subagent worktrees inside an existing non multi-agent worktree.

Examples:

- non multi-agent branch `feature/1.2.0/clouds3n/add-login` uses worktree `<root>/<repo>/feature/1.2.0/clouds3n/add-login`.
- multi-agent base branch `feature/1.2.0/clouds3n/add-login/base` uses worktree `<root>/<repo>/feature/1.2.0/clouds3n/add-login/base`.
- subagent branch `feature/1.2.0/clouds3n/add-login/backend/session-token` uses worktree `<root>/<repo>/feature/1.2.0/clouds3n/add-login/backend/session-token`.

## Subagent Merge Spec

- The multi-agent `/base` branch is the integration branch for the task.
- A subagent branch must merge back into its corresponding `/base` branch after the subtask is complete.
- A subagent branch must not bypass the `/base` branch and merge directly into default, `nightly`, `qa`, `release`, or another release-flow branch.
- The coordinating agent owns conflict resolution, final acceptance, and release-flow promotion.

## Commit Spce

Follow `Conventional Commits` specification.

## Merge Request Spce

Always use the default MR/PR template from current project.


## Useful CLI Commands

> Learn more from the `scripts/` directory in this skil

- `auto_merge`: Merge the current version branches into the current branch
- `check_merge`: Check all branches for the current version are merged into the current branch
- `delete_local_branches`: Delete all branches except the main/master.ensure all branches are pushed
- `rename_git_branch`: Rename the branch both locally and remotely

## Quality Gates

- Check branch before coding. **DO NOT** develop directly on `master`,`main`,`nightly`,`qa`,`release` branch
- Non multi-agent branch name follows template: `<type>/<version>/<developer>[/<taskId>]/<taskName>`
- Multi-agent base branch name follows template: `<type>/<version>/<developer>[/<taskId>]/<taskName>/base`
- Subagent branch name follows template: `<type>/<version>/<developer>[/<taskId>]/<taskName>/<agentId>/<subtaskName>`
- Worktree path must mirror the branch tree under `${ELITEFORGE_SKILL_GIT_WORKTREE_ROOT:-${CODEX_HOME:-$HOME/.codex}/worktrees}`
- Worktree and branch must have a one-to-one relationship
- Subagent branches must merge back to the corresponding `/base` branch
- Subagent `agentId` must use a role name and must not include numeric suffixes, scope, or target details
- Version follows `SemVer`
- Commit message follows `Conventional Commits`
