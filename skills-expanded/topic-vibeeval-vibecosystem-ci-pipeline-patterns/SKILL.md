---
name: ci-pipeline-patterns
description: GitHub Actions workflow templates, matrix builds, caching, and monorepo CI strategies
---

# CI Pipeline Patterns

## GitHub Actions Workflow Template

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  lint-and-type:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: npm }
      - run: npm ci
      - run: npm run lint
      - run: npm run type-check

  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        shard: [1, 2, 3, 4]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: npm }
      - run: npm ci
      - run: npm test -- --shard=${{ matrix.shard }}/4

  build:
    needs: [lint-and-type, test]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: npm }
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-artifact@v4
        with: { name: build, path: dist/ }
```

## Caching Strategies

```yaml
# npm cache
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: npm-${{ hashFiles('**/package-lock.json') }}

# Docker layer cache
- uses: docker/build-push-action@v5
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max

# Turborepo remote cache
- run: npx turbo build --cache-dir=.turbo
```

## Monorepo CI (Affected Only)

```yaml
# Nx affected
- run: npx nx affected --target=test --base=origin/main

# Turborepo
- run: npx turbo run test --filter=...[origin/main]

# Manual path filter
- uses: dorny/paths-filter@v3
  id: changes
  with:
    filters: |
      api: ['packages/api/**']
      web: ['packages/web/**']
```

## Pipeline Security

```yaml
# Secret scanning
- uses: trufflesecurity/trufflehog@main
  with: { extra_args: --only-verified }

# Dependency audit
- run: npm audit --audit-level=high

# SAST
- uses: github/codeql-action/analyze@v3
```

## Checklist

- [ ] Concurrency: cancel-in-progress aktif
- [ ] Cache: npm/pip/go module cache
- [ ] Paralel: test shard veya matrix
- [ ] Security: secret scan + dependency audit
- [ ] Artifact: build output upload
- [ ] Branch protection: require status checks
- [ ] Monorepo: affected-only strategy
- [ ] Timeout: job timeout belirlenmiş

## Anti-Patterns

- Cache key'de sabit string (hash kullan)
- Her push'ta tüm testler (affected-only)
- Secret'ı log'a yazdırma (mask)
- Single job tüm adımlar (paralelize et)
- Manual deploy (CD otomatik olmalı)
