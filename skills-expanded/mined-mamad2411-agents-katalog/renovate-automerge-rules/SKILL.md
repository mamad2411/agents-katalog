---
name: renovate-automerge-rules
description: Datasource-specific automerge rules — shared presets from mmalyska/renovate-config and per-repo scoping patterns from mmalyska/home-ops
---

# Renovate Automerge Rules

## When to Use

Use this skill when configuring automerge in a `renovate.json5`. It covers the shared presets (extend them directly), how to scope automerge to specific files or packages, and when to use `branch` vs `pr` automerge type.

---

## Shared Automerge Presets

These are provided by `mmalyska/renovate-config`. Extend the ones you need:

### `automerge-docker-digest`
Automerge digest-only updates for all docker images:
```json
{
  "packageRules": [{
    "matchDatasources": ["docker"],
    "automerge": true,
    "automergeType": "branch",
    "matchUpdateTypes": ["digest"],
    "ignoreTests": false
  }]
}
```
Use when: you pin all Docker images to digests and want them to stay current automatically.

### `automerge-github-actions`
Automerge minor/patch/digest for GitHub Actions:
```json
{
  "packageRules": [{
    "matchManagers": ["github-actions"],
    "automerge": true,
    "automergeType": "branch",
    "matchUpdateTypes": ["minor", "patch", "digest"],
    "ignoreTests": true
  }]
}
```
`ignoreTests: true` means Renovate merges directly without waiting for CI — appropriate for Actions where the update itself doesn't affect your code.

### `automerge-terraform-providers`
Automerge minor/patch for Terraform providers:
```json
{
  "packageRules": [{
    "matchDatasources": ["terraform-provider"],
    "automerge": true,
    "automergeType": "branch",
    "matchUpdateTypes": ["minor", "patch"],
    "ignoreTests": false
  }]
}
```

### `automerge-galaxy-collections` / `automerge-galaxy-roles`
Automerge minor/patch for Ansible Galaxy collections and roles:
```json
{
  "packageRules": [{
    "matchDatasources": ["galaxy-collection"],
    "automerge": true,
    "automergeType": "branch",
    "matchUpdateTypes": ["minor", "patch"],
    "ignoreTests": true
  }]
}
```

---

## `automergeType: "branch"` vs `"pr"`

| Type | Behavior | Use when |
|------|----------|---------|
| `"branch"` | Renovate merges directly to base branch if CI passes (or ignoreTests) | Low-risk updates; CI is reliable; prefer fewer PRs |
| `"pr"` | Creates a PR that auto-merges after approval/CI | Higher-risk updates; want review trail; GitHub branch protection required |

For most automerge rules in home-ops-style repos, `"branch"` is preferred.

---

## Per-Repo Scoping Patterns

Use `matchFileNames` to limit automerge to specific directories:

```json5
// .github/renovate/autoMerge.json5
{
  "packageRules": [
    {
      "description": "Auto merge cluster apps (not core)",
      "matchDatasources": ["github-releases", "github-tags", "helm", "docker"],
      "automerge": true,
      "automergeType": "pr",
      "matchUpdateTypes": ["minor", "patch", "digest"],
      "matchFileNames": ["cluster/**", "!cluster/core/**"],
      "ignoreTests": false
    },
    {
      "description": "Auto merge devcontainer digest",
      "matchDatasources": ["docker"],
      "automerge": true,
      "automergeType": "branch",
      "matchUpdateTypes": ["digest"],
      "matchFileNames": [".devcontainer/devcontainer.json"],
      "ignoreTests": true
    }
  ]
}
```

Use `matchPackageNames` to limit to specific packages:

```json5
{
  "packageRules": [
    {
      "description": "Auto merge pre-commit hooks",
      "matchDatasources": ["github-releases", "github-tags"],
      "automerge": true,
      "automergeType": "branch",
      "matchUpdateTypes": ["minor", "patch"],
      "matchPackageNames": [
        "pre-commit/pre-commit-hooks",
        "adrienverge/yamllint"
      ],
      "ignoreTests": true
    }
  ]
}
```

---

## `automergeSchedule` requires `platformAutomerge: false`

`platformAutomerge` defaults to `true`. When enabled, Renovate hands the PR to the platform's native auto-merge (e.g. GitHub's "Enable auto-merge") **at PR-creation time**, and the platform merges it as soon as CI passes — with no awareness of `automergeSchedule`. The schedule is silently ignored; PRs merge any hour, any day.

If a packageRule needs `automergeSchedule` to actually restrict merge timing, you must also set `platformAutomerge: false` so Renovate performs the merge itself (Renovate re-checks the schedule on each run before merging):

```json5
{
  "description": "Weekly-only digest updates (e.g. a noisy upstream `:main` tag)",
  "matchDatasources": ["docker"],
  "matchPackageNames": ["some/noisy-image"],
  "matchUpdateTypes": ["digest"],
  "automergeSchedule": ["before 5am on monday"],
  "platformAutomerge": false
}
```

Symptom if you miss this: the rule looks correct, but PRs keep merging outside the schedule window — because it's GitHub merging them, not Renovate. Confirmed in home-ops: a first attempt at scheduling hermes-agent digest automerge (added `automergeSchedule` alone) kept merging multiple times a day for over a month before `platformAutomerge: false` was added.

---

## Safety: `minimumReleaseAge`

Add a minimum age before automerging to avoid immediately pulling in a botched release:

```json5
{
  "packageRules": [{
    "matchDatasources": ["github-releases"],
    "automerge": true,
    "automergeType": "branch",
    "matchUpdateTypes": ["minor", "patch"],
    "minimumReleaseAge": "3 days"
  }]
}
```

---

## Never Automerge Major Versions

The base preset does not automerge major versions for any datasource. To explicitly block a datasource from major automerge:

```json5
{
  "packageRules": [{
    "matchDatasources": ["helm"],
    "matchUpdateTypes": ["major"],
    "automerge": false
  }]
}
```
