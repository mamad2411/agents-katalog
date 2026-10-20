---
name: git-workflow-conventions
description: >
  Team Git workflow conventions: branching models (trunk-based, GitHub Flow),
  commit hygiene, PR size, rebase vs merge, protected branches, release tags, and
  hotfix paths. Use when standardizing repository collaboration — not for force-
  pushing shared history without agreement.
---

# Git Workflow Conventions

## Scope And Authorization

- **In scope:** Repositories your team owns; establishing or documenting collaboration rules.
- **Out of scope:** Force-pushing shared branches without coordination; rewriting published
  release history casually; accessing repos without permission.
- Prefer conventions encoded in `CONTRIBUTING.md`, branch protection, and CI over tribal knowledge.
- Pair commit message format with `commit-message-conventions` when present.

## When To Use

- Bootstrapping a new team repo or reconciling conflicting Git habits.
- Choosing trunk-based vs release-branch models.
- Defining PR requirements, reviewers, and merge strategy.
- Training engineers on rebase etiquette and hotfix flow.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Commit message format only | `commit-message-conventions` |
| CODEOWNERS enforcement | `github-codeowners-enforcement` |
| GitHub Actions CI design | GHA skills |
| Changelog/release notes | `changelog-and-release-notes` |
| Implementation quality | `code-quality-standards` |

## Concepts

| Model | Summary |
| --- | --- |
| Trunk-based | Short-lived branches; frequent merge to `main`; feature flags |
| GitHub Flow | Branch → PR → review → merge to `main` → deploy |
| Git Flow | `develop` + `release/*` + `hotfix/*` (heavier) |
| Protected branch | No direct push; required checks + reviews |
| FF merge / merge commit / squash | History shape tradeoffs |
| Immutable release tags | `vX.Y.Z` on production artifacts |

## Workflow

### 1. Choose a default model

| Team signal | Prefer |
| --- | --- |
| Continuous deploy, good CI | Trunk-based / GitHub Flow |
| Versioned products, long QA | Release branches (disciplined) |
| Multiple versions supported | Explicit LTS branches + backports |

Document **one** primary model in `CONTRIBUTING.md`.

### 2. Branch naming

```text
feature/TICKET-123-short-slug
fix/TICKET-456-short-slug
chore/deps-2026-07
hotfix/TICKET-789-short-slug
release/1.4.0
```

Rules:

- Branch from latest `main` (or agreed trunk).
- Delete remote branch after merge.
- No unbounded `wip` branches older than team SLA (e.g. 14 days).

### 3. Commit hygiene

1. Atomic commits preferred; squash on merge acceptable if team chooses squash-only.
2. Do not commit secrets, large binaries, or `node_modules`.
3. Use signed commits if org requires (`git config commit.gpgsign true`).
4. Follow `commit-message-conventions` (Conventional Commits often).

```bash
git status
git diff
git add -p
git commit -m "feat(api): add health check endpoint"
```

### 4. Keep branches current

```bash
git fetch origin
git rebase origin/main
# or: git merge origin/main
git push --force-with-lease   # ONLY on your feature branch, never on main
```

| Do | Don't |
| --- | --- |
| `--force-with-lease` on personal branch | `git push --force` on `main` |
| Rebase feature before review | Rewrite already-shared feature history mid-review without notice |

### 5. Pull requests

| Convention | Guidance |
| --- | --- |
| Size | Prefer &lt; ~400 lines meaningful diff; split otherwise |
| Description | Why, how, risk, test plan |
| CI | Must be green before merge |
| Reviewers | CODEOWNERS + domain expert |
| Draft | Use for early feedback without review clock |

### 6. Merge strategy

Pick and document one default:

| Strategy | Pros | Cons |
| --- | --- | --- |
| Squash | Clean main | Loses fine-grained commits |
| Merge commit | Preserves branch topology | Noisier history |
| Rebase+FF | Linear | Needs discipline |

Enable branch protection: required checks, linear history if FF, dismiss stale reviews.

### 7. Releases and hotfixes

```bash
# Tag after CI green on main (example)
git checkout main
git pull
git tag -a v1.4.0 -m "v1.4.0"
git push origin v1.4.0
```

Hotfix:

1. Branch `hotfix/...` from the production tag or `main` per model.
2. Minimal fix + test.
3. PR with expedited review; deploy; back-merge to trunk if needed.
4. Patch version tag.

### 8. Break-glass

- Temporary admin bypass of protection: ticketed, time-limited, audited.
- Never disable protection permanently for convenience.

## CONTRIBUTING.md skeleton

```markdown
## Branching
- Trunk: main
- Branch names: feature|fix|chore|hotfix/...
## Commits
- Conventional Commits
## PRs
- Template required; 1 approval + CI
## Merge
- Squash merge
## Releases
- Annotated tags vX.Y.Z
```

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Branches | Short-lived | Months-old feature branch |
| Secrets | Pre-commit secret scan | API keys in git history |
| Force push | Lease on feature only | Force main |
| PRs | Focused + test plan | 50-file unrelated drive-by |
| Tags | Annotated release tags | Moving tags after release |

## Output Checklist

- [ ] Model chosen and documented
- [ ] Branch naming published
- [ ] Commit/PR conventions linked
- [ ] Protection rules applied on default branch
- [ ] Merge strategy consistent in UI settings
- [ ] Release/hotfix path documented
- [ ] Break-glass process defined
- [ ] Team trained / FAQ updated

## Rules

- No force-push to shared protected branches.
- History of public release tags is immutable.
- Encode workflow in tooling (protection, templates), not only wiki.
- Pair with CODEOWNERS and CI skills for enforcement.
- Keep this skill about collaboration workflow, not app code style.
