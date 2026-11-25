---
name: git-workflow-and-versioning
description: >-
  Trunk-based development with atomic commits, disciplined versioning, and
  a forensic bisect workflow. Covers commit granularity, branch naming,
  conventional commits, semver, merge strategies, and the `git bisect`
  workflow for finding regressions. Designed to make `git log` a reliable
  audit trail and `git bisect` a reliable tool.
---

# Git Workflow & Versioning

## Overview

Git is the most widely used tool in software engineering and the most
misused. Most teams treat it as a dumpster — large, unstructured commits
on long-lived branches merged with incomprehensible messages. This skill
treats Git as a forensic tool. Every commit is a save point with a
verifiable hypothesis. Every merge records intent. Every tag corresponds
to a deployable artifact.

**Core principle: trunk-based development.** The `main` (or `master`)
branch is always deployable. Branches are short-lived (hours to days, not
weeks). The typical change is approximately 100 lines, fitting in a single
commit. Larger changes are split into a sequence of atomic commits on a
short branch, each passing CI.

## When to Use

- Starting a new project or repository
- Creating a branch for any change
- Committing work-in-progress or complete changes
- Writing commit messages
- Reviewing or merging a pull request
- Choosing a version number for a release
- Rebasing, squashing, or resolving merge conflicts
- Running `git bisect` to find a regression
- Setting up CI/CD triggers and branch protection rules
- Onboarding new team members to the project's Git conventions

## Process

### Step 1: Choose the Right Branch Strategy

For most teams, the optimal strategy is **short-lived feature branches
merged to trunk**.

**Branch types:**

| Branch | Purpose | Lifespan | Base |
|--------|---------|----------|------|
| `main` | Production-ready, always deployable | Permanent | — |
| `feat/<name>` | A single feature or bug fix | Hours to 2 days max | `main` |
| `fix/<name>` | Bug fix (separated from features for release tracking) | Hours to 2 days max | `main` |
| `chore/<name>` | Refactoring, deps, tooling, docs | Hours to 1 day | `main` |
| `release/v<major>.<minor>` | Release stabilization (rare — for coordinated releases) | Days, not weeks | `main` |
| `hotfix/<name>` | Emergency fix from a release branch or tag | Hours | `main` or release tag |

**Naming conventions:**
- Lowercase with hyphens: `feat/user-authentication`
- Include issue/ ticket number: `feat/PROJ-1234-user-auth`
- Descriptive but concise: `fix/null-pointer-login` not `fix/bug`
- Use `/` separators: `feat/`, `fix/`, `chore/`, `release/`, `hotfix/`

**Anti-patterns:**
- Long-lived branches (more than 2 days without merging to trunk)
- `dev` or `develop` branches that lag behind `main` by weeks
- Branches named after people (`alexs-feature`) — anonymity enables
  collective ownership
- Branches named `temp` or `test` — they never get deleted

**Exit criteria:** A branch with a valid name, based on the latest `main`,
expected to live <48 hours.

### Step 2: Make Atomic Commits

A commit is a save point: it should compile, pass tests, and represent one
logical change. The ideal commit changes approximately 100 lines (+/- 50).
If a change exceeds 200 lines, split it.

**Commit granularity rules:**
1. One commit = one logical change. A feature might be 3-5 commits:
   (1) add data model, (2) add API endpoint, (3) add frontend component,
   (4) wire them together.
2. If you can describe the change in a sentence, it is atomic enough. If you
   need "and", split it.
3. Refactoring and behavior changes must never share a commit. If you refactor
   and add a feature in the same commit, bisect cannot distinguish them.
4. Formatting changes are either the only change in a commit or they are
   committed separately before the logic change.
5. Every commit passes the project's lint and test suite locally. If CI would
   fail on this commit, refine it before pushing.

**Commit message format (Conventional Commits):**

```
<type>(<scope>): <short summary> (≤72 chars)

<optional body — wrap at 72 chars>
- Explain *why* the change was made, not *what* (the diff shows what)
- Include trade-offs, alternatives considered, reasoning

<optional footer>
- BREAKING CHANGE: <description>
- Closes: #123
- Co-authored-by: Name <email>
```

**Types:**
| Type | Meaning | Version Impact |
|------|---------|---------------|
| `feat` | A new feature | MINOR |
| `fix` | A bug fix | PATCH |
| `refactor` | Code change with no behavior change | PATCH |
| `perf` | Performance improvement | PATCH |
| `test` | Adding or fixing tests | PATCH |
| `docs` | Documentation changes | PATCH |
| `chore` | Tooling, dependencies, CI, config | PATCH |
| `style` | Formatting, linting | PATCH |
| `BREAKING CHANGE` | Incompatible API change | MAJOR |

**Exit criteria:** A commit that compiles, passes tests, has a conventional
commit message, and changes ~100 lines.

### Step 3: Merge with Intent

**Merge strategies (in order of preference):**

| Strategy | When to Use | Impact on History |
|----------|-------------|-------------------|
| **Squash merge** | Merging a branch with multiple small commits into trunk. The entire branch becomes one commit on `main`. | Linear history, clean bisect, loses individual commit context. |
| **Rebase + merge (linear)** | You want a linear history with the benefit of individual commits. Rebase the branch onto `main`, then fast-forward merge. | Linear history, preserves individual commits, requires force-push. |
| **Merge commit** | When the branch's individual commits are meaningful and rebasing would be impractical (many conflicts, long-running branch). | Non-linear history, preserves all commits and topology, readable merge point. |

**Branch protection rules (GitHub/GitLab):**
- `main` is protected: no direct pushes, only PRs/MRs
- Required status checks: lint, test, build, security audit, coverage threshold
- Required reviews: at least one approval, blocking comments resolved
- Linear history required (squash or rebase)
- Branch must be up to date with `main` before merging

**Exit criteria:** A clean merge to `main` with an appropriate strategy,
passing status checks, and a meaningful merge/squash message.

### Step 4: Version with Semver

Semantic Versioning (semver): `MAJOR.MINOR.PATCH`

| Component | Increment When | Example |
|-----------|---------------|---------|
| **MAJOR** | Breaking change (API contract changed, backward-incompatible) | 2.0.0 |
| **MINOR** | New feature (backward-compatible) | 1.3.0 |
| **PATCH** | Bug fix, refactor, performance (backward-compatible) | 1.2.4 |

**Pre-release tags:** `1.0.0-alpha.1`, `1.0.0-beta.2`, `1.0.0-rc.3`

**Versioning rules:**
- Every merge to `main` that is deployable produces a version decision:
  maintainers determine if the cumulative unreleased changes since the last
  tag are MAJOR, MINOR, or PATCH.
- Tag every release: `git tag v1.2.3` and push tags.
- Versions are immutable. If a release is bad, tag the fix as a PATCH bump.
- Maintain a `CHANGELOG.md` (keep a changelog convention) that documents
  every version change with links to PRs/issues.
- For libraries/packages: version the published artifact, not just the
  repository tag.

**Exit criteria:** Every deployable version has a semver tag, a changelog
entry, and an artifact that can be reproduced from the tag.

### Step 5: Git Bisect Workflow

When a regression is found, `git bisect` identifies the exact commit that
introduced it. This is only possible if commits are atomic (Step 2).

**Bisect workflow:**
```bash
# Start bisect
git bisect start

# Mark the current commit as bad (contains the bug)
git bisect bad

# Mark a known-good commit (from a tag, a date, or a known-good SHA)
git bisect good v1.2.0

# Git checks out a commit halfway between good and bad.
# For each checked-out commit:
#   1. Build the project
#   2. Run the reproduction test
#   3. If the test passes:   git bisect good
#   4. If the test fails:    git bisect bad
# Repeat until the first bad commit is identified.

# When done:
git bisect reset
```

**Automated bisect:**
```bash
git bisect start HEAD v1.2.0 --   # bad=HEAD, good=v1.2.0
git bisect run npm test            # any command that exits 0 (good) or non-0 (bad)
```

**Bisect prerequisites (how commits enable bisect):**
- Every commit compiles. If a commit does not compile, bisect cannot use it.
- Every commit passes tests. If unrelated tests are broken, bisect cannot
  distinguish the regression.
- Refactoring and behavior change are in separate commits. If they are
  combined, the bisect output is ambiguous.
- Formatting changes are in separate commits. A bisect should never point
  to a formatting commit as the "first bad commit."

**Exit criteria:** A `git bisect` session that identifies the exact commit
introducing a regression, with an automated script (optional but ideal).

---

## Anti-Rationalization Table

| Excuse | Rebuttal |
|--------|----------|
| "I'll write the commit message after I finish coding." | Write the message before you commit. If you cannot summarize it in one sentence, the change is not atomic. A TODO commit is not a commit. |
| "My branch is only 3 days old, that's not long-lived." | After 48 hours, `main` has likely moved significantly. The merge becomes painful and bisect becomes imprecise. Short branches are the single best predictor of team velocity. |
| "I'll squash everything on merge, so individual commit quality doesn't matter." | Squashing discards the intermediate state that bisect needs. If you plan to squash, make sure each commit is still atomic and compiles — bisect runs on the final result anyway. But this still makes review harder. |
| "We don't need semver — we ship everything continuously." | Semver communicates compatibility to consumers. Even if you deploy continuously, your API consumers (other services, mobile apps, open-source users) need to know when to expect breakage. |
| "Rebasing rewrites history, which is dangerous." | Rebasing shared branches is dangerous. Rebasing your own feature branch onto `main` is safe and produces cleaner history. Follow the rule: never rebase `main`, never rebase shared branches. |
| "The merge conflict was small, so I resolved it without checking with the author." | Every merge conflict represents a communication gap. At minimum, the resolution should be reviewed. If the conflict touched business logic, the original author should verify the resolution. |
| "We don't need branch protection rules because we trust each other." | Trust prevents malice, not mistakes. Branch protection prevents the CI from being bypassed when someone forgets to run tests, a dependency audit fails, or a linter rule is violated. Protection is for process, not people. |

## Red Flags

- Commits with messages like "fix", "update", "wip", "asdf", or "."
- Commits that change 500+ files or 10,000+ lines
- Branches that live longer than 1 week
- Merge commits that contain no actual merge (just a fast-forward with a message)
- `git bisect` that lands on a "merge branch" or "fix formatting" commit
- Version tags that do not match semver (e.g., `v1.2.3.4` or `v1.02.03`)
- No tags at all — no way to identify deployable reference points
- Committing `.env`, `node_modules`, `vendor/`, `build/`, or other generated
  files
- `main` branch broken for more than 30 minutes
- Force-push to shared branches (including `main`)
- Commit that combines formatting, refactoring, and a feature in one diff

## Verification

1. Check `git log --oneline -20`. Does every message follow conventional
   commits format?
2. Check `git diff --stat` for the last commit. Is it approximately 100 lines?
3. Check `git bisect` capability: pick a known regression from the last month
   and verify that `git bisect` lands on an atomic commit, not a merge or
   formatting commit.
4. Check branch list: `git branch -a`. Any branches older than 2 days?
5. Check tags: `git tag -l`. Do they follow semver? Is the latest tag
   deployable?
6. Check branch protection settings: are `main` protections configured?
   Required checks? Required reviews?
7. Check CHANGELOG.md: is it up to date? Does it link to PRs/issues?
8. Check lockfiles: are `package-lock.json`, `poetry.lock`, `Cargo.lock`,
   etc. committed?
9. Check `.gitignore`: are secrets, build artifacts, and OS files ignored?
10. Test a commit reverts cleanly: `git revert HEAD`. Does CI pass?
