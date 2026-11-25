---
name: github-master
description: Default GitHub governance skill for repository work, pull requests, branch safety, merges, releases, versioning, CODEOWNERS, protected branches, rulesets, CI checks, and collaboration conflict prevention. Use whenever the user mentions GitHub, git, branches, pull requests, merges, release impact, changelog, version bumps, CODEOWNERS, branch protection, rulesets, or version conflicts.
---

# GitHub Master

Use this skill as the default operating model for GitHub-related work.

This skill is optimized for small teams, usually two to four people, that deploy from a live `main` branch and use other branches only for temporary work. The default recommendation is a strict GitHub Flow model with a protected `main`, short-lived topic branches, pull-request-only integration, and no shared-history rewrites.

## Default posture

- Never commit directly to `main`, `master`, or release branches.
- Never force-push a shared branch.
- Never rewrite shared history.
- Never push without an explicit `yes`.
- Prefer short-lived topic branches and squash merges into `main`.
- Treat merge conflicts as a signal to sync early, reduce branch lifetime, or split work into smaller pull requests.

## Required first checks

Before editing, detect and report:

- current branch
- target base branch
- current version
- version source(s)
- release workflow in repo: `release-please`, `semantic-release`, `changesets`, `manual`, or `unknown`
- changelog file(s), version file(s), CI workflow(s)
- whether the task changes API, schema, CLI, config contract, or user-visible behavior

Run the bundled preflight script first when possible:

```bash
python3 scripts/repo_preflight.py --path /absolute/path/to/repo --task "user request summary"
```

If a repository is empty or not yet initialized, report that explicitly and mark missing items as `not present` or `assumed`.

## Mandatory workflow

### 1. RESEARCHER

Use official GitHub documentation first for workflow, policy, and merge-governance questions.

Output:

`Research Brief {facts, risks, assumptions, sources}`

Read [references/github-small-team-best-practices.md](references/github-small-team-best-practices.md) when you need the current baseline.

### 2. ARCHITECT

Propose the smallest viable design.

If the task is trivial, output exactly:

`No architectural change required.`

Output:

`Architecture Spec {decision, impacted files, interfaces, migrations, rollback risk}`

### 3. BUILDER

Implement the smallest safe change.

- Add or update tests for changed behavior.
- Update docs only when behavior, config, setup, or operations change.
- Never change unrelated files.

Output:

`Build Report {changed files, tests added, commands run, assumptions}`

### 4. VALIDATOR

Run the checks that match the scope.

- lint
- typecheck
- tests
- security sanity checks
- repo-specific validation

If implementation issues appear, return to `BUILDER`.
If design issues appear, return to `ARCHITECT`.

Output:

`Validation Report {commands, results, failures, reproduction}`

### 5. RELEASE MANAGER

Always classify release impact:

- `major` = breaking API, schema, CLI, or config contract
- `minor` = backward-compatible feature
- `patch` = backward-compatible fix
- `none` = docs, tests, chores, or internal-only work

Always output:

- `release_impact`
- `candidate_next_version`
- `build_id = <branch>-<shortsha>`

If the repo uses `release-please`, `semantic-release`, or `changesets`, do not invent manual version bumps unless the repo already requires them.

If the repo is manual, update `CHANGELOG.md` using Keep a Changelog and add or maintain `[Unreleased]`.

## Branch and merge policy

### Branches

- Use short topic branches: `feat/<slug>`, `fix/<slug>`, `chore/<slug>`, `refactor/<slug>`.
- If the host tool imposes a prefix, keep the topic suffix intact, for example `codex/feat/<slug>`.
- One unrelated change set per branch.
- Keep branches short-lived. If a branch becomes long-running, split it or re-plan.

### Pull requests

- Open a pull request early if feedback is needed.
- Use draft pull requests for incomplete work.
- Include a clear summary, the problem being solved, linked issues, validation commands, and release impact.
- Keep pull requests small enough that another person can review them quickly.

### Sync policy

- If the base branch moves, update the head branch before merge when strict checks or conflicts require it.
- Resolve conflicts before merge; do not push conflict resolution blindly.
- Prefer the platform's `Update branch` flow or a carefully executed local sync over ad hoc merge commits into `main`.

### Merge policy

For small teams with a live `main` branch, the default recommendation is:

- protect `main`
- require pull requests
- require at least one approval from someone other than the author
- dismiss stale approvals
- require conversation resolution
- require required status checks
- require branches to be up to date before merging
- require linear history
- allow squash merge only
- enable automatic deletion of merged branches

This recommendation is an inference from GitHub's official guidance plus the small-team, short-lived-branch context. Read [references/recommended-github-settings.md](references/recommended-github-settings.md) before changing this default.

## CODEOWNERS and rulesets

- Add `CODEOWNERS` when review ownership should be explicit.
- Prefer a code owner for `.github/`, workflow files, and release or deployment files.
- Use protected branches as the minimum baseline.
- Use rulesets when visibility, layering, or org-wide governance matter.
- Respect CODEOWNERS, required checks, protected branches, and rulesets.

## Push gate

After validation and local commit preparation, stop and ask exactly:

`Ready to push to GitHub? (yes/no)`

Never push before the user answers `yes`.

## Resources

Use these files instead of recreating them:

- guidance: [references/github-small-team-best-practices.md](references/github-small-team-best-practices.md)
- exact settings: [references/recommended-github-settings.md](references/recommended-github-settings.md)
- reusable PR template: [assets/pull_request_template.md](assets/pull_request_template.md)
- reusable CODEOWNERS example: [assets/CODEOWNERS.example](assets/CODEOWNERS.example)

## Final output contract

For GitHub tasks, the final response should include:

- current branch
- target base branch
- release impact
- candidate next version
- build id
- changed files
- checks run
- remaining risks
- push gate question
