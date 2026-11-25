---
name: release-management
description: Coordinate end-to-end software releases with semantic versioning, automated changelogs, tag verification, and rollbacks.
category: development
aliases:
- release-workflow
- release-coordinator
- semantic-release
- cut-release
triggers:
- cut a new release
- manage release workflow
- generate release notes and tag
- prepare semantic version bump
- coordinate production release
keywords:
- release
- semver
- version
- tag
- changelog
- publish
- rollout
- rollback
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
lifecycle: enabled
capabilities:
- semantic-versioning
- changelog-generation
- release-orchestration
- rollback-readiness
inputs:
- commits
- current_version
- release_type
outputs:
- new_version
- changelog_entry
- git_tag_command
- release_checklist
permissions:
  filesystem: none
  network: none
  shell: none
  secrets: none
author: Mr-Nobody-Anonymous
tags:
- development
- management
- release
- semver
- tag
- version
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Release Management

## Purpose
Orchestrates disciplined, repeatable software release lifecycles. Automates semantic version calculation, changelog generation, release tagging, artifact verification, and deployment rollback checklists.

## When to Use
- Cutting patch, minor, or major releases for libraries, CLIs, or production services.
- Generating user-facing release notes grouped by features, fixes, and breaking changes.
- Enforcing pre-release gate checks (passing CI, clean test suites, updated lockfiles).
- Auditing release readiness and deployment canary health.

## When NOT to Use
- Routine feature development before reaching release candidate status.
- Ad-hoc unversioned hotfixing in sandbox environments.

## Capabilities
- **Semantic Version Bump**: Calculate patch, minor, or major version bumps based on conventional commits.
- **Changelog Synthesis**: Compile clean, human-readable release notes with commit links and contributor credits.
- **Release Verification**: Run comprehensive pre-release checklists (`validate`, `test`, license audits).
- **Rollback Planning**: Define explicit rollback triggers, backup verification, and revert procedures.

## Inputs
- `current_version` (required) — Current semantic version string (e.g., `1.2.0`).
- `commit_log` (required) — Commits since the last release tag.
- `release_type` (optional) — `major`, `minor`, `patch`, or `auto`.

## Workflow
1. Inspect commits since the previous release tag for breaking changes, features, and fixes.
2. Compute the new semantic version according to SemVer 2.0 specifications.
3. Verify that all automated tests, security scans, and build gates pass 100%.
4. Generate the changelog entry and update project metadata files (`pyproject.toml`, `package.json`).
5. Create the annotated git tag and publish the release draft with assets.
6. Verify deployment health metrics and confirm rollback readiness.

## Tools
- `git` for tagging and commit extraction; project build systems.

## Examples
- "Cut a new patch release with updated changelogs."
- "Prepare semantic version bump from 1.2.0 based on recent conventional commits."
- "Coordinate our release workflow and confirm pre-flight checks."

## Safety
- Require explicit confirmation before pushing release tags or publishing packages to external registries (PyPI, npm).
- Never publish a release when CI or security test suites report failures.

## Source
Custom skill maintained in this library adhering to SemVer and release engineering standards.

## Notes
Pairs with `development.ci-cd-pipeline` and `development.verification-before-completion`.
