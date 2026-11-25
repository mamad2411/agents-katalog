---
name: dependabot-janitor
description: "Triage open Dependabot pull requests and carry out the safe remediations: merge-ready reports, lockstep combines, and dependabot ignore rules. Use when given a GitHub pull queue URL, a list of PRs, or a Dependabot backlog. Does not cover Renovate or other update bots, and does not merge major bumps."
---

# Dependabot Janitor

Triage and clean up open Dependabot pull requests. Auto-merging a dependency PR is safe only when the repository can prove the bump is boring. This skill applies deterministic guards, separates routine patch bumps from breaking changes, diagnoses failing checks honestly, and executes multi-package combinations and configuration exclusions.

## Tools

Use stock `git` and stock `gh` only. Every command in this skill is upstream git or GitHub CLI. Do not call shell aliases, wrapper scripts, or any other CLI.

`gh` must already be authenticated for the host that owns the pull requests. This includes GitHub Enterprise hosts, not only `github.com`.

## Supported Inputs

Accept a dependency queue in any of these forms:

1. **GitHub URLs** on `github.com` or on a GitHub Enterprise host `gh` is already authenticated for:
   - Queue URLs: `https://<host>/pulls/assigned`, `https://<host>/pulls`, `https://<host>/orgs/<org>/pulls`, or `https://<host>/<owner>/<repo>/pulls`
   - Individual PR URLs: `https://<host>/<owner>/<repo>/pull/<number>`
2. **Pasted lists** of markdown links: `- [repo#123](https://<host>/<owner>/<repo>/pull/123)`
3. **Implicit discovery**, when no URL or list is given. The default `--limit` is 30. Raise it until the number of results comes back smaller than the limit you asked for:
   ```bash
   gh search prs --state open --assignee @me --limit 100 --json repository,number,title,author,url
   ```

## Core Principles

- **Absence of information beats instructions.** Do not merge a major version bump unattended. Major bumps carry breaking-change risk; the merge stays with the maintainer.
- **Diagnose failing checks honestly.** A failing check is not automatically a broken dependency. Look for peers bumped apart, a stale workflow, or a failure already present on the base branch before calling it a regression.
- **Demand protective test gates.** A green check that does not exercise the bumped surface is not permission to merge.
- **Close with receipts.** When excluding an update or closing a PR, say why the bump is wrong now and when it becomes appropriate.

## Step 1: Ingestion and Metadata Gathering

For each PR:

1. **Pass the pull request URL through.** That URL is the `gh` argument. Do not split it into owner, repository, and number.
2. **Keep Dependabot, set the rest aside.** The author login is `dependabot[bot]` (app slug `dependabot`). A PR from a person or from any other bot is **Manual / Operational**. Do not run dependency triage on it.
3. **Read state, checks, and the diff.**
   ```bash
   gh pr view <url> --json number,title,author,mergeable,statusCheckRollup,headRefName,baseRefName,files
   ```
   ```bash
   gh pr diff <url>
   ```
4. **Classify the bump** from the manifest diff: `patch`, `minor`, or `major`, and runtime versus development. The manifest is whatever that ecosystem uses (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Gemfile`, `pom.xml`, and their lockfiles).

## Step 2: Evaluation and Disposition Rubric

Assign every candidate to exactly one disposition.

### 1. Merge Ready

Criteria:

- The bump is a `patch` or `minor` inside the range that repository already accepts.
- Required status checks completed successfully.
- Those checks exercise the surface this bump touches (tests, typecheck, lint, or the repository's equivalent).
- The PR merges cleanly.

Action: report it as ready for the maintainer to merge. Do not merge it.

### 2. Combine

Criteria:

- Two or more open Dependabot PRs in one repository bump packages that must move together. Examples: `vitest` with `@vitest/coverage-v8` and `@vitest/ui`, or `react` with `react-dom`. The same shape exists in every ecosystem that versions a family together.
- Each PR alone fails install or resolution because a peer is missing. npm's `ERESOLVE` is one such failure; treat the equivalent resolver error in any other package manager the same way.

Action: plan one lockstep change on a new branch from the shared base (`baseRefName`). If the PRs do not share a base branch, use Caution instead. Plan to close the split PRs with a pointer to the combined PR.

### 3. Exclude and Close

Criteria:

- A major bump breaks the architecture, compiler, or tooling this repository actually uses.
- Or a types or platform package moves past the runtime this repository declares (engine field, runtime version file, or an explicit pin).
- Or the dependency is pinned on purpose to match an external platform.

Action: plan an `ignore` rule in the existing Dependabot config, and a close comment that states why and when.

### 4. Caution and Manual Review

Criteria:

- A major bump is green on honest checks, and still changes packaging, credentials, security-sensitive behavior, or a public API other repositories consume.
- Or the bump raises a support floor the maintainer has not agreed to.

Action: flag it for the maintainer. State what changed, what CI proved, and what CI did not prove.

### 5. Hold and Blocked

Criteria:

- Tests caught a real regression.
- Or a downstream tool does not yet support the new version.

Action: comment with the blocker. Do not merge.

## Step 3: Presenting the Disposition Index

Print the full index before any write: branch, config edit, push, or close. Group by disposition. The package names in the template are shape examples; substitute the PR's real ecosystem.

~~~markdown
# Dependabot PR Triage Index

## Summary
- **Merge Ready**: N PRs
- **Combine**: N PRs
- **Exclude & Close**: N PRs
- **Caution / Manual Review**: N PRs
- **Hold / Blocked**: N PRs
- **Manual / Operational**: N PRs

## 1. Merge Ready
- **[owner/repo#123](url)**: `fix(deps-dev): bump pkg from 1.0.0 to 1.0.1`
  - **Verdict**: Ready for the maintainer to merge. Patch bump, required checks passed, and those checks exercise this package.

## 2. Bumps Requiring Combination
- **[owner/repo#124](url)**: `fix(deps-dev): bump vitest from 4.1.0 to 5.0.0`
- **[owner/repo#125](url)**: `fix(deps-dev): bump @vitest/coverage-v8 from 4.1.0 to 5.0.0`
  - **Diagnosis**: Install failed because the peers were bumped apart.
  - **Action**: One lockstep PR from the shared base branch, then close #124 and #125.

## 3. Major Version Bumps to Exclude & Close
- **[owner/repo#126](url)**: `chore(deps-dev): bump typescript from 6.0.0 to 7.0.0`
  - **Diagnosis**: The new compiler breaks the documentation build this repository runs in CI.
  - **Action**: Ignore `typescript` versions `>=7.0.0` in the existing Dependabot config, then close #126 with why and when.

## 4. Bumps to Review with Caution
- **[owner/repo#127](url)**: `chore(deps-dev): bump tool from 3.0.0 to 4.0.0`
  - **Diagnosis**: Checks passed. The bump also raises the runtime floor and changes credential handling.

## 5. Hold / Blocked
- **[owner/repo#128](url)**: `fix(deps): bump pkg from 1.2.3 to 2.0.0`
  - **Diagnosis**: Tests failed on a real regression. <the blocker>
  - **Action**: Leave the PR open. Comment the blocker. Do not merge.

## 6. Non-Dependabot / Operational PRs
- **[owner/repo#129](url)**: `fix(rc): internal feature branch` (not Dependabot; left out of dependency triage).
~~~

## Step 4: Execution

When you are explicitly asked to execute, read `references/execute.md` and follow it. Do not checkout, commit, edit config, push, or close pull requests from this file.
