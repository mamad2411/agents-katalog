---
name: version-control-workflows
description: Apply Git workflows (trunk-based, GitFlow, release-train), branching strategies, monorepo tooling (Nx/Turborepo/Bazel), commit hygiene, and PR practices. Use when picking a branching model, structuring a monorepo, or improving review velocity.
source: self
date_added: 2026-04-30
---

# Version Control Workflows

Pick the lightest branching model that meets your release needs and keep `main` always shippable.

## When to Use

- Setting up a repo or restructuring an existing one.
- Choosing between polyrepo and monorepo, and selecting tooling.
- Defining branching, merging, and release conventions.
- Reducing PR cycle time and merge conflicts.

## Branching Model Decision

| Context | Model |
| --- | --- |
| SaaS, CI/CD multiple times/day, small-to-mid teams | **Trunk-based** with short-lived branches (<1-2 days) and feature flags |
| Multiple supported versions of installable software | **Release branches** off trunk; cherry-pick fixes |
| Large coordinated train releases (mobile app stores) | **Release-train** with a soft cutoff date |
| Open source, contributor PRs | **Trunk-based** with fork+PR; protected branches |

Avoid GitFlow for SaaS — it overinvests in branches you don't need.

## Trunk-Based Defaults

- Single long-lived branch: `main` (always green, always deployable).
- Branches < 400 LOC, < 24-48 hrs old before merging.
- Feature flags for unfinished work merged behind a switch.
- Required: PR review, CI green, linear or squash merge.
- Tag releases (`v1.4.2`) on `main`; deploy artifacts from tags or commit SHAs.
- Hotfixes: branch from the release tag, fix, tag, deploy, merge back to `main`.

## Commit & PR Hygiene

- **Conventional Commits** (`feat:`, `fix:`, `chore:`, `refactor:`, `BREAKING CHANGE:`) — enables changelog automation and semver.
- Commit message: imperative subject ≤ 72 chars; body explains *why*; footer references issue/ADR.
- Squash-merge by default; keep merge commits only for true integrations.
- PR title follows commit convention; description includes: what, why, how to test, screenshots/recordings, risk.
- Small PRs win — average diff under 300 lines correlates with faster review and fewer defects.
- Draft PRs early for feedback; convert to ready when CI passes.

## Code Review Norms

- First response within 1 business day; full review same/next day.
- Reviewer focuses on correctness, design, test coverage, security, and naming — not style (lint/format does that).
- Authors respond to every comment (resolve, fix, or discuss).
- "Approved with comments" is fine for non-blocking suggestions.
- Pair-review or async-review for senior context, never solo merge of risky changes.
- CODEOWNERS for security-sensitive paths and shared libs; require their approval.

## Monorepo vs Polyrepo

| Choose monorepo if | Choose polyrepo if |
| --- | --- |
| Many shared libraries with rapid co-evolution | Independent release cadences with no shared code |
| Want atomic cross-cutting refactors | Strict org/security boundaries between teams |
| Have tooling investment for build graph (Nx/Turbo/Bazel) | Small teams, few services, no shared deps |

## Monorepo Tooling

| Tool | Best for |
| --- | --- |
| **Nx** | TS/JS-heavy apps; rich generators, affected graph, remote cache |
| **Turborepo** | Lightweight TS/JS pipelines; minimal config |
| **pnpm workspaces** | Pure JS without an orchestrator |
| **Bazel** | Polyglot at scale (Go/Java/Python/JS); hermetic builds |
| **Pants / Buck2** | Polyglot mid-scale; modern alternatives |
| **Gradle / Maven multi-module** | JVM-only |

Defaults regardless of tool:
- **Build graph + affected** detection so PRs only build/test what changed.
- **Remote cache** (Nx Cloud, Turbo Remote, BuildBuddy, Bazel Remote) — biggest CI speedup.
- **CODEOWNERS** per package.
- **Versioning policy** documented (single version vs independent; Changesets for independent npm packages).
- Path-based CI triggers; merge queue (GitHub Merge Queue) to keep main green at scale.

## Release Strategy

- **Continuous deployment** to prod on green main (with feature flags + canary) — preferred default.
- **Continuous delivery** with manual prod gate when regulated.
- **Semantic versioning** for libraries; date-based for SaaS where users don't see versions.
- **Changelogs** auto-generated from Conventional Commits (release-please, semantic-release, Changesets).
- **Release artifacts** are immutable and signed (Sigstore/cosign).

## Anti-Patterns

- Long-lived feature branches that diverge for weeks.
- Force-push to shared branches without coordination.
- "Fix typo" commits left unsquashed flooding history.
- Branch protection bypassed via admin merge.
- Monorepo without affected-build tooling — CI time explodes.
- Polyrepo with copy-pasted shared code drifting silently.
- Commits containing secrets (use `git-secrets`, `trufflehog`, pre-commit hooks).
- Rebasing public/shared branches.

## Tooling Baseline

- `pre-commit` hooks: format, lint, secret scan, conventional-commit check.
- Branch protection: required checks, required reviews, dismiss stale reviews on push, no force-push.
- Merge queue when PR throughput is high.
- Signed commits/tags (`gpg` or Sigstore `gitsign`) for release tags.
- Renovate or Dependabot for dependency PRs with auto-merge on green for patches.

## Quality Gates

- `main` is green; broken main pages the on-call.
- Average PR age in review < 1 day; p95 < 3 days.
- 95% of PRs merge within a week of opening.
- Zero secrets in history (continuous scanning).
- Release process documented and reproducible from tag.

## References

- "Trunk Based Development" — https://trunkbaseddevelopment.com/
- Conventional Commits — https://www.conventionalcommits.org/
- Google Engineering Practices (eng-practices)
- Accelerate (Forsgren, Humble, Kim)
- monorepo.tools
