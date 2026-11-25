---
name: git-flow
description: Use when branching, opening an MR, cutting a release, or shipping a hotfix — the develop→staging→master branching & release flow, tagging, semantic versioning, hotfix path. Tool-agnostic (plain git).
metadata:
  last-updated: 2026-06-20
  author: Ken Nguyễn <ntnpro@gmail.com>
---

## When to use

Reach for this when you start a feature branch, open a merge request, promote code between
environments, tag a release, or ship an urgent production fix. It is the **branching & release**
workflow; for commit-message rules and the "never target main for feature work" guard see the global
*Git Commit Rules* / *Branch & PR Target Rules* in `CLAUDE.md`.

> Branch **names** vary by project — some teams use `staging`, others `RC`, for the pre-production
> branch. What matters is the **role** each branch plays, not its literal name. Map the names below
> to your project's. This is plain git, so it applies to a repo in any language.

## Branch roles

| Branch | Role |
|---|---|
| `master` (or `main`) | Production. Only thoroughly tested code. Tagged per production release. |
| `staging` (or `RC`) *(optional)* | Pre-production / demo. Tagged per staging release. Optional if you have strong feature flags. |
| `develop` | Integration branch for active development; deploys to the Dev environment. |
| `feature/*` | One per task/feature. Branches from `develop`. |
| `hotfix/*` | Critical production-bug fixes. Branches from `master`. |

## Steps

### 1. Feature development

```bash
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name      # always branch from fresh develop
# ...commit focused work...
```
Open a merge request **into `develop`**. After review, merge (`--no-ff`) — this triggers the Dev
deployment. Keep one feature branch to one concern (see *SRP per MR* in
[code-conventions](./code-conventions.md) §5).

### 2. Promote to staging (selective)

Not every feature in `develop` ships at once. When the selected changes are ready:

```bash
git checkout staging
git merge --no-ff develop                       # or cherry-pick specific feature merges:
# git cherry-pick -m 1 <feature-merge-commit>   # for selective promotion
git push origin staging

git tag -a v1.0.0-staging -m "Staging release v1.0.0"
git push origin v1.0.0-staging                  # tag → deploys to staging; test there
```
Any bug fix found on staging is committed on `staging`, then merged back into `develop`.

### 3. Production release

Promote the **exact code that was tagged for staging** — don't re-merge a moving `develop`.

```bash
git checkout v1.0.0-staging
git checkout -b release/v1.0.0
# MR release/v1.0.0 → master, get approval, then:
git checkout master
git merge --no-ff release/v1.0.0

git tag -a v1.0.0 -m "Production release v1.0.0"
git push origin master
git push origin v1.0.0                           # tag → deploys to production
git branch -d release/v1.0.0                      # clean up
```

### 4. Hotfix (urgent production fix) — default path

```bash
git checkout master
git checkout -b hotfix/critical-fix
# ...fix + test thoroughly...

# verify in staging FIRST
git checkout staging && git merge --no-ff hotfix/critical-fix && git push origin staging
git tag -a v1.0.1-staging -m "Hotfix staging v1.0.1" && git push origin v1.0.1-staging

# then release to production
git checkout master && git merge --no-ff hotfix/critical-fix && git push origin master
git tag -a v1.0.1 -m "Hotfix v1.0.1" && git push origin v1.0.1

# propagate back so develop doesn't regress the fix
git checkout develop && git merge --no-ff hotfix/critical-fix && git push origin develop
```

**Merging a hotfix straight to `master` (skipping staging)** is allowed **only** for
critical/blocker cases with high confidence: production is broken (login down, payments failing), no
time for a full UAT round (still test locally / on an emergency env), the fix is very small and
low-risk (revert a bad commit, fix a config typo), and only trusted engineers deploy. Even then,
**propagate the fix back to `develop`** (and `staging`) afterward.

## Versioning & CI/CD

- **Semantic versioning** `vMAJOR.MINOR.PATCH`: MAJOR = incompatible API change, MINOR = new
  backward-compatible functionality, PATCH = backward-compatible bug fix.
- **Staging tags mirror their production counterpart** except for the `-staging` suffix:
  `v1.2.3-staging` → `v1.2.3`.
- **CI/CD by trigger:** Dev deploys automatically when changes merge to `develop`; Staging deploys
  from tags on `staging` (`v1.0.0-staging`); Production deploys from tags on `master` (`v1.0.0`).

## Verification

A release/hotfix followed the flow when:
- The feature was branched from a freshly pulled `develop` and merged via MR (not committed to
  `master`/`develop` directly).
- Production shipped the **same commit** that was tagged on staging (staging tag ↔ prod tag differ
  only by `-staging`).
- A hotfix that touched `master` was also merged back into `develop` (and `staging`) — verify with
  `git branch --contains <hotfix-commit>`.
- The deploy you expected fired (Dev on `develop` merge; Staging/Prod on the new tag).

## Related

- `CLAUDE.md` — *Git Commit Rules* (no AI attribution), *Branch & PR Target Rules*,
  *Release Safety Rules* (backward compat, rollback plan, post-release verification).
- [code-conventions](./code-conventions.md) — one responsibility per MR.
