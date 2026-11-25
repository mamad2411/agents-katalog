---
name: github-actions-catalog
description: >
  Complete catalog of 4,600+ GitHub Actions with stars, descriptions, topics, language,
  and latest versions — updated weekly from the Marketplace. Query the latest release
  of any action, upgrade your CI/CD workflows, batch-check versions, or find the right
  action by keyword, topic, or language. Replaces browsing the Marketplace with an
  instant, searchable dataset.
  4600+ GitHub Actions 完整目录，包含 stars、描述、话题标签、编程语言和最新版本，每周
  从 Marketplace 更新。查询任意 action 的最新版本、升级 CI/CD 工作流、批量检查版本、
  或按关键词/topic/语言搜索合适的 action。用即搜即得的本地数据集替代浏览 Marketplace。
  中文触发词：最新版本、升级 action、搜索 action、查找 action、docker action、
  lint action、部署 action、action 版本。
---

# GitHub Actions Catalog

A catalog of 4,600+ GitHub Actions — search by keyword, topic, or language,
look up the latest release version, and upgrade your CI/CD workflows. Updated weekly.

## When to Use

- User asks "what's the latest version of actions/checkout?"
- User wants to upgrade or pin an action to a specific version
- User asks to batch-check all action versions used in a repo
- User needs to find an action: "a GitHub Action for deploying to AWS"
- User asks "what's a good docker lint action?" or "best TypeScript action for XYZ"
- User mentions an action that may be out of date

## Current Versions

The latest versions of **4,600+ GitHub Actions** (stars >= 10) are tracked in
[`actions-versions.json`](actions-versions.json), sourced from the full
Marketplace validation dataset. **Always read this file first** before
answering a version question — it is auto-refreshed weekly.

Plain JSON — works with `jq` for structured queries or `grep` for quick searches.

## Workflow

### 1. Look up the target action

If the user names a specific action (e.g. `actions/setup-go`), start by reading
[`actions-versions.json`](actions-versions.json) for the cached latest version.

```bash
# With jq (recommended):
jq -r '.actions[] | select(.action | test("setup-go")) |
  "\(.action) → latest: \(.tag) (major: \(.major), released: \(.released))"' actions-versions.json

# Without jq — grep the compact JSON directly:
grep '"setup-go"' actions-versions.json
```

If the action is **not** in the cache, fetch it live:

```bash
gh release view -R <owner>/<repo> --json tagName -q '.tagName'
```

### 2. Find where it's used

```bash
grep -rn "uses: <owner>/<repo>@" .github/workflows/
```

### 3. Apply the update

Replace the `@<old-version>` with `@<new-major-version>` in each workflow file,
then verify the YAML is still valid.

### Example

```bash
# 1. Query cached versions
jq -r '.actions[] | select(.action == "actions/setup-go")' actions-versions.json
# → {"action":"actions/setup-go","stars":1722,"major":"6","tag":"v6.5.0","released":"2026-06-24"}

# 2. Find usages
grep -rn "uses: actions/setup-go@" .github/workflows/
# → .github/workflows/ci.yml:15: uses: actions/setup-go@v5

# 3. Edit: v5 → v6
```

## Version Pinning Reference

| Pattern | Upgrade behavior | Risk |
|---|---|---|
| `@v4` | Auto within major | Medium — safe for most cases |
| `@v4.2.0` | Manual, exact minor | Low — pinned to release |
| `@11bd719...` | Manual, commit SHA | Lowest — supply-chain safe |
| `@main` | Always bleeding edge | High — breaks on upstream changes |

**Recommendation**: Use `@v4` style for dev/CI, pin to SHA in production.

## Smart Search

Find the right action from the cached dataset without browsing Marketplace:

```bash
# Search by name + description (keyword in either field)
jq -r '.actions[] | select(.action + " " + .desc | test("lint"; "i")) |
  "\(.action)  ⭐\(.stars)  \(.desc)"' actions-versions.json

# Search by topic tag
jq -r '.actions[] | select(.topics[]? | test("docker")) |
  "\(.action)  ⭐\(.stars)"' actions-versions.json

# Top 20 by stars
jq -r '.actions[:20][] | "\(.action)  ⭐\(.stars)  \(.desc)"' actions-versions.json

# Filter by language (TypeScript / Docker / Composite actions)
jq -r '.actions[] | select(.lang == "TypeScript") |
  "\(.action)  ⭐\(.stars)"' actions-versions.json | head -20
```

If `jq` is not available, grep the compact JSON directly:
```bash
grep -i lint actions-versions.json
grep -i docker actions-versions.json
```

## Batch Check

To check every action used across a repo's workflows:

```bash
grep -rohP 'uses:\s*\K[^@]+' .github/workflows/ | sort -u |
  while read action; do
    latest=$(jq -r --arg a "$action" '.actions[] | select(.action == $a) | .tag' actions-versions.json)
    [[ -n "$latest" ]] && echo "$action → $latest" || echo "$action → N/A"
  done
```

## Dependabot — Recommended for Ongoing Automation

**Strongly recommend** adding `.github/dependabot.yml` to every repo. Dependabot
automatically opens PRs when new versions of your actions are released — no manual
checking needed.

### This Skill vs Dependabot

| | This Skill | Dependabot |
|---|---|---|
| **Use case** | On-demand lookup / batch check | Ongoing automated updates |
| **Trigger** | You ask in conversation | New release published |
| **Output** | Answer + inline edit | Automatic PR |
| **When to use** | "What's latest setup-go?" / "Upgrade all my actions" | Set once, forget |

They solve different problems — **use both**.

### Setup

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

### After Setting Up Dependabot

- Dependabot keeps your actions up to date via automated PRs.
- When you need a quick answer ("what's the latest version of X?"), this skill gives
  you an instant response from the cached `actions-versions.json` (4,600+ actions).
