---
name: follow-tool-renovate-config-renovate
description: Configure `renovate.json` — extends presets, packageRules, automerge, schedule
argument-hint: "[scope]"
related:
  - follow-tool-github-actions
  - run-install
  - improve
---

## Goal

Configure `renovate.json` to match the update policy — `extends` presets, `packageRules`, `automerge`, `schedule` — merging with the existing config

## Scope

Use when editing an existing Renovate config — install/token/workflow are in `workflows/setup-renovate/SKILL.md`

## Execute

### 1. Read Current Config

> Goal: read the existing config before editing

1. Find the config: `renovate.json`, `.github/renovate.json`, `renovate.json5`, or the `"renovate"` field in `package.json`
2. Record the current keys — run `/deep-review-codebase` domain `review-config` if the config looks suspicious
3. If no config exists → run `workflows/setup-renovate/SKILL.md` first

### 2. Base Config And Presets

> Goal: set the base and `extends`

1. Use `"$schema": "https://docs.renovatebot.com/renovate-schema.json"`
2. `extends` — `["config:base"]` as the starting point; see official docs for other presets (`config:recommended` may add unwanted checks)
3. `schedule` — e.g. `["every day"]` or an explicit time window
4. `"platform": "github"` for self-hosted; `repositories: ["owner/repo"]` when running multiple repos
5. `docker: false` if Docker updates aren't wanted

### 3. Package Rules

> Goal: define per-package/group policies with `packageRules`

1. Group related packages — `matchPackagePatterns`/`matchPackageNames` to combine into one PR (e.g. the eslint ecosystem, framework + plugins)
2. Use `matchUpdateTypes` (`patch`, `minor`, `major`) to split policy by bump severity
3. `enabled: false` for packages you keep frozen
4. Matchers must be exact — a wrong one silently stops the rule from matching

### 4. Automerge

> Goal: set the automerge policy

1. `automerge: true` in `packageRules` for low-risk updates (e.g. devDependencies patch/minor)
2. Use `automergeType`/`platformAutomerge` per repo settings — check official docs for uncertain option names
3. Never automerge major bumps or production-critical dependencies without review
4. Check branch protection — automerge must pass the required checks

### 5. Validate And Monitor

> Goal: validate the config and follow up

1. Run `bunx -- renovate-config-validator <config-path>` — it must pass
2. After merge → monitor the PRs Renovate creates: does automerge pass, do the rules match correctly
3. Adjust `packageRules` when you find deps you don't want auto-updated
4. Report before/after with `/report-before-after`

## Rules

### 1. Config Discipline

- Use `config:base` as the base; merge only the necessary keys, never overwrite the whole file
- Validate with `renovate-config-validator` after every change

### 2. Automerge Safety

- Automerge only low-risk updates — major/critical deps need review
- Branch protection required checks must be set before enabling automerge

### 3. Common Mistakes

- `config:recommended` may add unwanted checks — know what a preset does before extending it
- Wrong matchers = the rule silently doesn't fire — verify against real PRs after editing

- Use /deep-review-codebase review-config if needed

## Expected Outcome

- `renovate.json` passes the validator
- `packageRules`/automerge match the update policy
- PRs are created and automerged as intended
