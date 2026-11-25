---
name: cz
description: 'Commitizen version introspection. Show current version and predicted next version based on conventional commits. Triggers on: "cz version", "what version will this be", "commitizen version", "cz bump preview".'
license: MIT
compatibility: 'Works on Claude Code and any platform with git available. cz CLI optional — falls back to git tag analysis.'
argument-hint: '[--dry-run]'
---

# cz

Show the current project version and predicted next version using commitizen conventions.

## Critical Rules

- **Read-only** — never run `cz bump`, never write files, never commit
- **Always fall back** — if commitizen is not installed, use git tags + conventional commits
- **One answer** — print current version and next version, then stop
- **Markdown output: soft-wrap prose, never hard-wrap** — when writing markdown, write each paragraph as one continuous line; do not insert manual newlines to wrap prose at a fixed column width. Newlines still separate paragraphs, list items, headings, and code fences.

## Step 0: Detect config

```bash
# Priority order for commitizen config
CZ_CONFIG=""
[ -f ".cz.toml" ]                                                          && CZ_CONFIG=".cz.toml"
[ -f "pyproject.toml" ] && grep -q "\[tool.commitizen\]" pyproject.toml   && CZ_CONFIG="pyproject.toml"
[ -f ".commitizen.json" ]                                                   && CZ_CONFIG=".commitizen.json"
[ -f "package.json" ] && grep -q '"commitizen"' package.json               && CZ_CONFIG="package.json"
```

## Step 1: Get current version

If `CZ_CONFIG` is set and `cz` CLI is available:
```bash
cz version --project 2>/dev/null
```

Otherwise: `git describe --tags --abbrev=0 2>/dev/null | sed 's/^v//'` or `0.0.0`.

## Step 2: Predict next version

If `cz` CLI is available:
```bash
cz bump --dry-run 2>/dev/null
```
Parse the output for the bumped version line.

Otherwise: use the same conventional commit parsing as `changelog preview`:
- Get commits since last tag
- Apply semver bump rules (breaking → major, feat → minor, fix → patch)

## Step 3: Report

```
commitizen version introspection
  Config:   {CZ_CONFIG or "(none — using git tags)"}
  Current:  {current version}
  Next:     {next version}  ({Major|Minor|Patch|None} bump)
  Reason:   {N breaking | M features | P fixes since {last tag}}
```

If `cz` CLI is not installed: note "commitizen not installed — using git tag + conventional commit fallback".
