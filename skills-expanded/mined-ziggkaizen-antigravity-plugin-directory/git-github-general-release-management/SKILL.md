---
name: git-github-general-release-management
description: Plans Git/GitHub releases, hotfixes, tags, release notes, and rollback checks. Use when preparing a release, creating a tag, drafting release notes, triaging release risk, or planning a hotfix.
license: MIT
compatibility: Requires repository history access; optional GitHub CLI or GitHub MCP server for release metadata.
---

# Git/GitHub Release Management

This skill helps agents prepare releases and hotfixes with traceability and rollback awareness.

## When to Use This Skill

Use this skill for:

- release readiness checks;
- release note drafting;
- tag planning;
- hotfix branch planning;
- rollback planning;
- post-release verification.

## Release Principles

1. Verify the exact commit being released.
2. Ensure tests and required checks match repository policy.
3. Keep release notes accurate and user-oriented.
4. Tag only intentional release points.
5. Plan rollback before release.
6. Treat moved or deleted release tags as exceptional and approval-bound.
7. Separate release automation policy into a dedicated plugin when automation becomes tool-specific.

## Workflows

- `workflows/release-readiness-workflow.md`: Use before creating tags, publishing release notes, or merging release branches.
- `workflows/hotfix-workflow.md`: Use for urgent production fixes requiring branch isolation and post-release forward-porting.

## Resources

- `resources/release-checklist.md`
- `resources/rollback-plan-template.md`

## Examples

- `examples/release-notes-template.md`
- `examples/hotfix-branch-plan.md`
