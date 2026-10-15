---
name: skillsman-branch
description: Create, inspect, sync, and govern GitHub/Git branches using a main/develop/release branching model. Use when the user asks to create or choose a branch, name a feature/bugfix/hotfix/release branch, check branch safety, sync a base branch, prepare a pull request, protect main/develop/release branches, or decide whether staging/UAT/test should be a branch or deployment environment.
---

# Skillsman Branch

## Overview

Use this skill to turn natural-language branch requests into safe Git/GitHub branch plans and, when requested, execute the branch operations. Prefer Pull Requests for integration and enforce the team's protected-branch rules.

## Branch Model

Long-lived branches:

- `main`: production branch; only stable released or releasable code.
- `develop`: development integration branch; daily feature work branches from and merges back here.

Temporary branches:

- `release/<version>`: release candidate branch, for example `release/1.9.0`.
- `feature/<yyyymmdd>-<short-name>`: new feature work.
- `bugfix/<yyyymmdd>-<short-name>`: normal defects.
- `hotfix/<yyyymmdd>-<short-name>`: urgent production fixes.

Do not default to `staging`, `uat`, `test`, or `preprod` branches. Treat Staging, UAT, Test, SIT, and Pre-prod as deployment environments. If the user insists and gives a reason, use `env/<environment>` such as `env/staging`; never create bare `staging`, `uat`, `test`, or `preprod`.

## Classification

Classify the request before naming the branch:

- `feature`: new feature, new requirement, new page, new module, new API, "开发某功能", "add feature", "new module".
- `bugfix`: normal bug, test/SIT/UAT/release-stage issue, "fix bug".
- `hotfix`: production issue, incident, prod issue, online outage, emergency repair, "hotfix".
- `release`: release preparation, version freeze, pre-release validation, "发版", "release 1.9.0".

Ask a focused question when classification affects safety:

- Missing release version for a `release` branch: ask for the version.
- Ambiguous bugfix vs hotfix: ask whether the issue is in production.
- Ambiguous bugfix base: ask whether it belongs to daily development or a specific pending release.
- Unclear short name: propose a concise English slug and ask for confirmation only if the generated name would be misleading.

## Naming

Use today's branch-creation date in `yyyymmdd` format. Do not use a date as the whole branch name.

Allowed formats:

- `feature/<yyyymmdd>-<short-name>`
- `bugfix/<yyyymmdd>-<short-name>`
- `hotfix/<yyyymmdd>-<short-name>`
- `release/<version>`

Naming constraints:

- Use lowercase English letters, digits, and hyphens.
- Do not use Chinese, spaces, personal names, or date-only names.
- Keep `short-name` clear and brief, usually 2 to 6 English words.
- Prefer branch names under 60 characters.
- Use semantic-looking versions for release branches, for example `release/1.9.0`.

Generate `short-name` from the user's description:

- Translate Chinese into concise English.
- Convert to lowercase kebab-case.
- Remove filler words like `create`, `update`, `new`, and `fix` when they add no meaning.
- Keep business module and problem terms.
- Compress long descriptions to the essential 2 to 6 words.

Examples:

- "Admin dashboard 新 homepage" -> `admin-dashboard-homepage`
- "Occasion Notification 功能" -> `occasion-notification`
- "KPI 计算错误" -> `kpi-calculation-error`
- "用户角色同步失败" -> `user-role-sync-failed`
- "生产登录超时" -> `login-timeout`
- "API 调用失败" -> `api-call-failed`

## Base And Target

Choose base branch and target merge branch:

- `feature/*`: base `develop`, PR target `develop`.
- Daily `bugfix/*`: base `develop`, PR target `develop`.
- Release bugfix: base `release/<version>`, PR target `release/<version>`; remind the user to sync back to `develop` after merge.
- `hotfix/*`: base `main`, PR target `main`; after merge to `main`, remind the user to sync back to `develop` and evaluate active `release/*` branches.
- `release/<version>`: base `develop`, PR target `main`; after merge to `main`, recommend tag `v<version>`.

## Preflight

Before creating or pushing a branch:

1. Verify the current directory is a Git repository.
2. Check the working tree is clean. If dirty, stop and ask the user to handle or explicitly approve how to proceed.
3. Run `git fetch origin`.
4. Verify the base branch exists locally or on `origin`.
5. Check whether the target branch already exists locally or on `origin`.
6. If the branch exists, stop; suggest checking it out or choosing a new name.
7. Update the base branch from origin before creating the new branch.

Recommended command sequence:

```bash
git fetch origin
git checkout <base-branch>
git pull origin <base-branch>
git checkout -b <new-branch>
git push -u origin <new-branch>
```

If using a GitHub API or MCP tool, get the latest base branch commit SHA, create `refs/heads/<new-branch>`, and return the branch link.

## Protected Rules

Enforce these rules unless the user explicitly asks for a risk exception and the exception is not destructive:

- Do not push directly to `main`.
- Do not directly merge `feature/*` into `main`.
- Do not directly merge ordinary `bugfix/*` into `main` unless the user explicitly confirms the risk.
- Do not add unrelated new features to `release/*`.
- Do not develop directly on `develop`.
- Do not delete unmerged branches.
- Do not force-push `main`, `develop`, or `release/*`.
- Do not use `git push --force` on `main`, `develop`, or `release/*`.
- Require PRs for merges into `main`, `develop`, and `release/*`.

Temporary branches may be deleted only after confirming they have been merged.

## Pull Requests

Default PR targets:

- `feature/*` -> `develop`
- `bugfix/*` -> its source branch, either `develop` or `release/<version>`
- `hotfix/*` -> `main`
- `release/*` -> `main`

After PR guidance:

- For `hotfix/*` merged to `main`, remind the user to sync into `develop` and assess active `release/*`.
- For `release/*` merged to `main`, recommend a tag such as `v1.9.0`.
- For `bugfix/*` merged to `release/*`, remind the user to sync back to `develop`.
- After temporary branch merge, suggest deleting the remote branch only after merged status is confirmed.

## Output Format

For every plan, recommendation, or execution summary, include:

1. Branch type
2. Generated branch name
3. Base branch
4. Target merge branch
5. Recommended commands or actions to execute
6. Risk reminders
7. Next step

Keep responses concise and operational. If executing commands, report the exact checks performed and where execution stopped if a guard failed.
