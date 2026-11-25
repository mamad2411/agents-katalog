---
name: ci-cd-pipeline-builder
description: Generate CI/CD pipelines from detected project stack. Use when bootstrapping CI for a new repo, replacing brittle pipeline files, or auditing whether pipeline matches actual stack. Supports GitHub Actions and GitLab CI.
---

# CI/CD Pipeline Builder

**Category:** DevOps / Automation

## Overview

Generate pragmatic CI/CD pipelines based on actual project stack signals. Detects language, runtime, tooling from repo files, then generates appropriate GitHub Actions or GitLab CI configuration.

## When to Use

- Bootstrapping CI for a new repository
- Replacing copied/broken pipeline files
- Migrating between CI platforms
- Auditing whether pipeline matches actual stack

## Workflow

### Step 1: Detect Stack

Scan the repository for stack signals:

```bash
# Check for package managers
rtk ls package.json bun.lock package-lock.json yarn.lock pnpm-lock.yaml 2>/dev/null
rtk ls requirements.txt pyproject.toml Pipfile.lock poetry.lock 2>/dev/null
rtk ls go.mod go.sum 2>/dev/null
rtk ls Cargo.toml Cargo.lock 2>/dev/null

# Check for frameworks
rtk grep -l "next" package.json 2>/dev/null          # Next.js
rtk grep -l "react" package.json 2>/dev/null          # React
rtk grep -l "django" requirements.txt 2>/dev/null     # Django
rtk grep -l "fastapi" requirements.txt 2>/dev/null    # FastAPI

# Check for existing scripts
rtk read package.json | jq '.scripts' 2>/dev/null
```

**Detection heuristics:**
- Lockfiles determine package manager preference
- Language manifests determine runtime
- Script commands drive lint/test/build commands
- Missing scripts → conservative placeholders

### Step 2: Generate Pipeline

Start with minimal, reliable stages:

```
1. Checkout + setup runtime
2. Install dependencies (with cache)
3. Lint
4. Test
5. Build
6. (Optional) Deploy
```

### Step 3: GitHub Actions Template (Bun)

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  ci:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - uses: oven-sh/setup-bun@v2
        with:
          bun-version: latest
      
      - run: bun install --frozen-lockfile
      
      - name: Lint
        run: bun run lint
      
      - name: Test
        run: bun test
      
      - name: Build
        run: bun run build
```

### Step 4: GitLab CI Template

```yaml
stages:
  - install
  - quality
  - build

variables:
  NODE_VERSION: "20"

install:
  stage: install
  image: oven/bun:latest
  script:
    - bun install --frozen-lockfile
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/

lint:
  stage: quality
  script:
    - bun run lint

test:
  stage: quality
  script:
    - bun test
  coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)/'

build:
  stage: build
  script:
    - bun run build
  artifacts:
    paths:
      - dist/
```

### Step 5: Add Deployment (Safely)

Progressive deployment stages:

1. **CI-only first** — lint, test, build
2. **Staging deploy** — with explicit environment context
3. **Production deploy** — with manual gate/approval

```yaml
deploy-staging:
  stage: deploy
  needs: [build]
  environment:
    name: staging
    url: https://staging.example.com
  rules:
    - if: $CI_COMMIT_BRANCH == "main"

deploy-production:
  stage: deploy
  needs: [build]
  environment:
    name: production
    url: https://example.com
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      when: manual  # Manual gate
```

## Validation Checklist

```
□ Generated YAML parses successfully
□ All referenced commands exist in the repo
□ Cache strategy matches package manager
□ Required secrets are documented, not embedded
□ Branch rules match org policy
□ Deploy jobs gated by protected branches/environments
```

## Common Pitfalls

1. Copying a Node pipeline into Python/Go repos
2. Enabling deploy jobs before stable tests
3. Forgetting dependency cache keys
4. Running expensive matrix builds for trivial branches
5. Hardcoding secrets in YAML
6. Missing branch protections on prod deploy
