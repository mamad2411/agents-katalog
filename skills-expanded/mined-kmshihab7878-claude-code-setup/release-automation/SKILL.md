---
name: release-automation
description: Automated releases with Release Please, Renovate, conventional commits, semantic versioning, and CHANGELOG generation
triggers:
  - release
  - changelog
  - version bump
  - semantic version
  - conventional commits
  - renovate
  - release please
  - dependency update
---

# Release Automation

Automated versioning, changelogs, and dependency updates using Release Please + Renovate + Conventional Commits.

## Conventional Commits

Format: `type(scope): description`

| Type | Version Bump | Example |
|------|-------------|---------|
| `feat` | MINOR | `feat(agents): add delegation engine` |
| `fix` | PATCH | `fix(api): handle null response body` |
| `feat!` / `BREAKING CHANGE` | MAJOR | `feat!: redesign agent protocol` |
| `docs` | None | `docs: update API reference` |
| `chore` | None | `chore: update dependencies` |
| `refactor` | None | `refactor(core): simplify task queue` |
| `test` | None | `test: add integration tests for auth` |
| `ci` | None | `ci: add security scanning step` |

## Release Please Setup

```yaml
# .github/workflows/release.yml
name: Release
on:
  push:
    branches: [main]

permissions:
  contents: write
  pull-requests: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: googleapis/release-please-action@v4
        with:
          release-type: python
          package-name: coremind-fresh
```

```json
// release-please-config.json
{
  "packages": {
    ".": {
      "release-type": "python",
      "package-name": "coremind-fresh",
      "bump-minor-pre-major": true,
      "changelog-sections": [
        {"type": "feat", "section": "Features"},
        {"type": "fix", "section": "Bug Fixes"},
        {"type": "perf", "section": "Performance"},
        {"type": "refactor", "section": "Code Refactoring"},
        {"type": "docs", "section": "Documentation"},
        {"type": "chore", "section": "Miscellaneous", "hidden": true}
      ]
    }
  }
}
```

## Renovate (Automated Dependency Updates)

```json
// renovate.json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["config:recommended", ":automergeMinor", ":automergeDigest"],
  "packageRules": [
    {
      "matchUpdateTypes": ["minor", "patch"],
      "automerge": true,
      "automergeType": "pr"
    },
    {
      "matchUpdateTypes": ["major"],
      "automerge": false,
      "labels": ["major-update"]
    },
    {
      "matchPackagePatterns": ["*"],
      "groupName": "all-deps",
      "groupSlug": "all",
      "schedule": ["before 6am on monday"]
    }
  ],
  "vulnerabilityAlerts": { "enabled": true, "labels": ["security"] }
}
```
