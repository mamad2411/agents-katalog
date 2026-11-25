---
name: github-workflow-creation
description: Protocol for creating CI/CD workflows with atomic script separation,
    access control, and optimized deployment patterns.
category: CI/CD & DevOps
---

# GitHub Workflow Creation Skill

> **Skill ID:** `github-workflow-creation`<br>
> **Version:** 1.1.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

Automates creation of GitHub Actions workflows following industrial standards:
workflow organization, script separation, access control, checkout optimization,
and deployment via rsync/sshpass.

***

## 1. Workflow Organization

### 1.1 Directory Structure

Workflow files MUST be placed in `.github/workflows/` root for GitHub discovery.
Nested directories (e.g., `.github/workflows/deploy/`) are sometimes ignored by
GitHub Actions.

```text
.github/workflows/
  production.yml          # Target-specific workflow file
  staging.yml             # Future environments
  deploy-azure.yml        # Other deployment targets
  scripts/                # Shared scripts across workflows
    check-user.bash
    ...
```

### 1.2 File Naming

- Use environment/purpose names: `production.yml`, `staging.yml`, `ci.yml`
- Avoid generic names like `main.yml` when multiple workflows exist

***

## 2. Script Separation Mandate

### 2.1 No Inline Scripts

ALL shell logic MUST be extracted to separate `.bash` files under
`.github/workflows/scripts/`. Inline `run:` blocks are BLOCKED except for
single-line commands like `npm ci`.

This complements the broader **Template Extraction Mandate**
([`skill-factory` §2.2.1.1.6](../skill-factory/SKILL.md#2211-universal-script-mandates)):
just as shell logic must not be inlined in workflow files, file-content strings
(YAML, markdown, config) must not be inlined in scripts — use `.template` files
instead. The [`script-template-extraction`](../script-template-extraction/SKILL.md)
skill automates remediation of existing scripts that violate this rule.

### 2.2 Script Design

Each script MUST:

- Accept parameters via command-line arguments or environment variables
- NOT hardcode values like usernames, hosts, or paths
- Use `$GITHUB_ACTOR` for user context (built-in environment variable)
- Validate required arguments before execution
- Output `::error::` prefixed messages for GitHub Actions error reporting

### 2.3 Script Naming

- Use descriptive names: `check-user.bash`, `deploy-via-rsync.bash`
- Prefix with action verb: `check-`, `verify-`, `deploy-`, `install-`

***

## 3. Access Control

### 3.1 User Restriction

Workflows can be restricted to specific users:

```yaml
- name: Check Deploy Permission
  env:
    ALLOWED_USER: baneeishaque-ompventure
  run: bash .github/workflows/scripts/check-user.bash $ALLOWED_USER
```

### 3.2 Check Script Pattern

```bash
#!/bin/bash

ALLOWED="$1"

if [[ -z "$ALLOWED" ]]; then
  echo "::error::Allowed user argument is required."
  exit 1
fi

if [[ "$GITHUB_ACTOR" != "$ALLOWED" ]]; then
  echo "::error::Only authorized personnel can trigger this deployment. Current user: $GITHUB_ACTOR"
  exit 1
fi

echo "User check passed: $GITHUB_ACTOR"
```

***

## 4. Checkout Optimization

### 4.1 Production Branch Targeting

When building from a specific branch (e.g., production):

```yaml
- name: Checkout Production Branch
  uses: actions/checkout@v6.0.2
  with:
    ref: production
    fetch-depth: 1
    lfs: false
    persist-credentials: false
```

### 4.2 Flag Explanation

| Flag | Purpose |
|------|---------|
| `ref` | Target branch to checkout |
| `fetch-depth: 1` | Only fetch last commit (speed optimization) |
| `lfs: false` | Skip Git LFS objects if not used |
| `persist-credentials: false` | Skip credential setup when no git ops follow |

### 4.3 Version Pinning

ALWAYS use full version tags (e.g., `@v6.0.2`, not `@v6`) for reproducibility.

***

## 5. Build Configuration

### 5.1 Node.js Setup

Match the project's `mise.toml` or `.nvmrc` for version consistency:

```yaml
- name: Setup Node.js
  uses: actions/setup-node@v4
  with:
    node-version: "18.20.8"
    cache: "npm"
```

### 5.2 CI Mode Control

GitHub Actions automatically sets `CI=true`, which causes `react-scripts` to
treat ESLint warnings as fatal errors. For existing codebases with warnings:

```yaml
- name: Build Project
  env:
    CI: "false"
  run: npm run build
```

**When to use:**

- `CI: "false"` — Codebase has existing warnings that shouldn't block deployment
- Omit or `CI: "true"` — Fresh projects where zero warnings are enforced

### 5.3 Memory Management

Large React/Node projects require increased heap allocation:

```yaml
- name: Build Project
  env:
    NODE_OPTIONS: "--max-old-space-size=4096"
    CI: "false"
  run: npm run build
```

**Common combination:** Both `CI` and `NODE_OPTIONS` are typically needed together.

### 5.4 Dependency Installation

Use `npm ci` for deterministic, CI-optimized installs (reads only `package-lock.json`).

***

## 6. Deployment Patterns

### 6.1 Rsync via SSH Pass

For password-based SSH deployments:

```yaml
- name: Check SSH Pass
  run: bash .github/workflows/scripts/check-sshpass.bash

- name: Verify Runner Rsync
  run: bash .github/workflows/scripts/verify-runner-rsync.bash

- name: Verify Server Rsync
  env:
    VPS_PASSWORD: ${{ secrets.VPS_PASSWORD }}
    VPS_HOST: ${{ secrets.VPS_HOST }}
    VPS_USER: ${{ secrets.VPS_USER }}
  run: bash .github/workflows/scripts/verify-server-rsync.bash

- name: Deploy Static Build To Server
  env:
    VPS_PASSWORD: ${{ secrets.VPS_PASSWORD }}
    SOURCE: "build/"
    DEST: "${{ secrets.VPS_USER }}@${{ secrets.VPS_HOST }}:/var/www/acers/build/"
  run: bash .github/workflows/scripts/deploy-via-rsync.bash
```

### 6.2 Delta Sync Benefits

`rsync` only transfers changed files, unlike SCP which sends everything.
The `--delete` flag removes stale files from the target.

***

## 7. Step Naming Standards

All step names MUST use Title Case (capitalize first letter of each word):

- ✅ `Checkout Production Branch`
- ✅ `Check Deploy Permission`
- ✅ `Deploy Static Build To Server`
- ❌ `checkout production branch`
- ❌ `Check deploy permission`

***

## 8. Trigger Types

### 8.1 Manual Dispatch

For controlled deployments:

```yaml
on:
  workflow_dispatch:
```

### 8.2 Push Trigger

For automatic CI:

```yaml
on:
  push:
    branches: [main]
```

***

## 9. Runner Selection

### 9.1 Explicit Version

Use explicit OS versions instead of `latest`:

```yaml
runs-on: ubuntu-24.04
```

### 9.2 Available Runners

| Runner | Status |
|--------|--------|
| `ubuntu-24.04` | Current LTS |
| `ubuntu-22.04` | Legacy support |
| `ubuntu-latest` | Avoid (changes over time) |

***

## 10. Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Workflow not discovered by GitHub | Place `.yml` in `.github/workflows/` root, not subdirectories |
| Build fails with heap OOM | Add `NODE_OPTIONS: --max-old-space-size=4096` |
| Build fails with ESLint warnings as errors | Add `CI: "false"` to build step environment |
| SCP transfers all files every time | Use `rsync` with `--delete` for delta sync |
| Hardcoded values in scripts | Pass via arguments or environment variables |
| Using `@v6` instead of `@v6.0.2` | Always pin to full version for reproducibility |
| Inline scripts in workflow YAML | Extract to `.bash` files in `scripts/` folder |

***

## 11. Metadata Sync Workflows

### 11.1 Description Sync

Sync the repository description from a source of truth (e.g., `README.md` first line or `package.json`):

```yaml
name: Sync Repository Description
on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  sync-description:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4
      - name: Sync Description
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          DESCRIPTION=$(head -1 README.md | sed 's/^# //')
          gh repo edit "${{ github.repository }}" --description "$DESCRIPTION"
```

### 11.2 Topics Sync

Sync repository topics from a `.github/topics.txt` file (one topic per line):

```yaml
name: Sync Repository Topics
on:
  push:
    branches: [main]
    paths: ['.github/topics.txt']
  workflow_dispatch:

jobs:
  sync-topics:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4
      - name: Sync Topics
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          TOPICS=$(paste -sd, .github/topics.txt)
          gh repo edit "${{ github.repository }}" --add-topic "$TOPICS"
```

### 11.3 Combined Metadata Sync

For repositories that want both description and topics in a single workflow:

```yaml
name: Sync Repository Metadata
on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4
      - name: Sync Description
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          DESCRIPTION=$(head -1 README.md | sed 's/^# //')
          gh repo edit "${{ github.repository }}" --description "$DESCRIPTION"
      - name: Sync Topics
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          if [ -f .github/topics.txt ]; then
            TOPICS=$(paste -sd, .github/topics.txt)
            gh repo edit "${{ github.repository }}" --add-topic "$TOPICS"
          fi
```

***

## 12. PR Labeler Workflow

### 12.1 Labeler Configuration

Create `.github/labeler-config.yml` to define label rules based on changed paths:

```yaml
frontend:
  - changed-files:
      - any: ["src/frontend/**", "src/ui/**"]

backend:
  - changed-files:
      - any: ["src/backend/**", "src/api/**"]

documentation:
  - changed-files:
      - any: ["docs/**", "*.md"]

dependencies:
  - changed-files:
      - any: ["package.json", "requirements.txt", "go.mod"]

ci:
  - changed-files:
      - any: [".github/workflows/**", ".github/actions/**"]
```

### 12.2 Labeler Workflow

```yaml
name: PR Labeler
on:
  pull_request_target:
    types: [opened, synchronize, reopened]

jobs:
  label:
    runs-on: ubuntu-24.04
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: actions/labeler@v5
        with:
          configuration-path: .github/labeler-config.yml
```

### 12.3 Label Naming Convention

| Label | Prefix | Example |
|-------|--------|---------|
| Type | `type/` | `type/bug`, `type/feature` |
| Scope | `scope/` | `scope/frontend`, `scope/backend` |
| Priority | `priority/` | `priority/high`, `priority/low` |
| Status | `status/` | `status/needs-review`, `status/wip` |

***

## See Also

- [`github-actions-run-audit`](../github-actions-run-audit/SKILL.md) —
  observation-side counterpart. After authoring or modifying a workflow here,
  use that skill to verify it actually runs, succeeds, and (when applicable)
  produces / commits the expected artifact.
- [`github-actions-workflow-dispatch`](../github-actions-workflow-dispatch/SKILL.md) —
  trigger primitive. Required when the authored workflow includes
  `on: workflow_dispatch:` and the agent needs to fire it programmatically.
- [`github-ci-lint`](../github-ci-lint/SKILL.md) — C2 composer. Generates CI
  lint workflows (markdown + Python) that complement the patterns here.
- [`github-sync`](../github-sync/SKILL.md) — C3 composer. Generates metadata
  sync workflows for description/topics extracted from README.
- [`github-pr-labeler`](../github-pr-labeler/SKILL.md) — B9. Provides
  `pr-labeler.yml` + `labeler-config.yml` for automated PR labeling.
- [`github-workflows`](../github-workflows/SKILL.md) — C4 composer. Generates
  all GitHub Actions workflows (lint, PR labeler, sync) in one invocation.
- [`script-template-extraction`](../script-template-extraction/SKILL.md) —
  automation for the Template Extraction Mandate referenced in §2.1.
