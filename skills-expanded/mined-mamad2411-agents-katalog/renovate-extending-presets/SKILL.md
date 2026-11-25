---
name: renovate-extending-presets
description: How to extend mmalyska/renovate-config presets in a repo's renovate.json5, including all available sub-presets and the local override pattern
---

# Extending mmalyska/renovate-config Presets

## When to Use

Use this skill when writing or auditing a `renovate.json5` (or `renovate.json`) that should inherit from the shared `mmalyska/renovate-config` preset. This skill covers the base preset, all sub-presets, and the local override pattern for per-repo customization.

---

## Available Presets

All presets live at `github.com/mmalyska/renovate-config`.

| Preset | Purpose |
|--------|---------|
| `github>mmalyska/renovate-config` | **Base** — extends config:base, enables dependency dashboard, disables rate limiting, enables Docker digest pinning and automerge, plus commit-message, pr-labels, semantic-commits, generic-regex-manager, devcontainer-regex-manager |
| `github>mmalyska/renovate-config:commit-message` | Commit format: `{{depName}}` topic, `to {{newVersion}}` extra, no suffix |
| `github>mmalyska/renovate-config:pr-labels` | Labels: dep/major, dep/minor, dep/patch + renovate/helm, renovate/container, renovate/ansible, renovate/terraform, renovate/github-action |
| `github>mmalyska/renovate-config:semantic-commits` | feat for minor, fix for patch, ci for github-actions; scoped by datasource (docker-image, helm-chart, terraform-provider, ansible-collection, ansible-role, github-action) |
| `github>mmalyska/renovate-config:automerge-docker-digest` | Automerge docker digest updates via branch |
| `github>mmalyska/renovate-config:automerge-github-actions` | Automerge minor/patch/digest for github-actions via branch, ignoreTests |
| `github>mmalyska/renovate-config:automerge-terraform-providers` | Automerge minor/patch for terraform-provider via branch |
| `github>mmalyska/renovate-config:automerge-galaxy-collections` | Automerge minor/patch for galaxy-collection via branch, ignoreTests |
| `github>mmalyska/renovate-config:automerge-galaxy-roles` | Automerge for Ansible Galaxy roles |
| `github>mmalyska/renovate-config:generic-regex-manager.json5` | Regex manager for comment-annotated versions in YAML/Dockerfile |
| `github>mmalyska/renovate-config:devcontainer-regex-manager.json5` | Regex manager for `"image":` in `.devcontainer/devcontainer.json` |

---

## Minimal Base Config

For a new repo, start with:

```json5
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": [
    "github>mmalyska/renovate-config"
  ],
  "timezone": "CET",
  "gitAuthor": "renovate-bot <renovate-bot@users.noreply.github.com>"
}
```

This pulls in: `config:base`, dependency dashboard, Docker digest pinning, commit message conventions, PR labels, and semantic commits.

---

## Adding Sub-Presets

Include individual presets to add automerge for specific datasources:

```json5
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": [
    "github>mmalyska/renovate-config",
    "github>mmalyska/renovate-config:automerge-github-actions",
    "github>mmalyska/renovate-config:automerge-terraform-providers"
  ]
}
```

---

## Local Override Pattern

For per-repo rules that don't belong in the shared preset, use local files in `.github/renovate/`:

```json5
// .github/renovate.json5
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": [
    "github>mmalyska/renovate-config",
    "github>mmalyska/renovate-config:automerge-github-actions",
    "local>OWNER/REPO//.github/renovate/autoMerge.json5",
    "local>OWNER/REPO//.github/renovate/groups.json5"
  ],
  "ignorePaths": [".archive/**"],
  "reviewers": ["username"]
}
```

The `local>` prefix references files in the same repo without a network round-trip.

---

## Full home-ops Pattern (Reference)

The `mmalyska/home-ops` repo is the canonical usage example:

```json5
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": [
    "github>mmalyska/renovate-config",
    "github>mmalyska/renovate-config:automerge-github-actions",
    "github>mmalyska/renovate-config:automerge-terraform-providers",
    "local>mmalyska/home-ops//.github/renovate/allowedVersions.json5",
    "local>mmalyska/home-ops//.github/renovate/autoMerge.json5",
    "local>mmalyska/home-ops//.github/renovate/disabledDatasources.json5",
    "local>mmalyska/home-ops//.github/renovate/groups.json5",
    "local>mmalyska/home-ops//.github/renovate/managers.json5",
    "local>mmalyska/home-ops//.github/renovate/customManagers.json5"
  ],
  "ignorePaths": [".archive/**", "charts/**"],
  "reviewers": ["mmalyska"]
}
```

---

## Dependency Dashboard

The base preset enables `":dependencyDashboard"`. This creates a GitHub issue titled "Renovate Dashboard" listing all pending updates. To disable:

```json5
{
  "dependencyDashboard": false
}
```

---

## Rate Limiting

The base preset disables rate limiting (`":disableRateLimiting"`). To re-enable for low-traffic repos:

```json5
{
  "prHourlyLimit": 2,
  "prConcurrentLimit": 5
}
```
