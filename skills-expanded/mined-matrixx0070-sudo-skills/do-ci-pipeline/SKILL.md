---
name: do-ci-pipeline
version: 1.0.0
description: Design or repair a CI/CD pipeline with well-ordered parallel stages, lockfile-keyed caching, quality gates, and build-once artifact promotion.
author: matrixx0070
tags: [ci, cd, devops, automation, pipeline, gates]
capabilities: []
---

# do-ci-pipeline

## When to use

You need to build a CI/CD pipeline from scratch, diagnose a slow or flaky one, or add gates before a risky change ships. Works for GitHub Actions, GitLab CI, CircleCI, Jenkins, or Buildkite.

**Not for:** application code changes, local build scripts, one-off deploy commands, or infra provisioning (use do-terraform), container image authoring (use do-dockerfile), or the release runbook itself (use do-release-checklist).

## Method

1. Map the delivery graph: list triggers (push, PR, tag, schedule), what must pass before merge, and what promotes to each environment.
2. Split work into ordered stages — lint/typecheck, unit test, build, integration test, package, deploy. Decision: if two stages share no inputs, run them in parallel to cut wall-clock time; if one consumes another's output, chain them.
3. Add caching keyed on lockfile hashes (deps, build layers, fixtures) with a documented cache-bust path. Decision: cache only deterministic, non-secret, non-environment-specific output — never credentials or per-env config.
4. Define gates: required status checks, coverage threshold, security scan (SAST + dependency audit), and manual approval before prod. Decision: block merge on gates that protect correctness; warn-only on advisory ones.
5. Build the artifact once, version it immutably, and promote the same artifact across environments. Decision: never rebuild per stage — rebuilding breaks the "tested == shipped" guarantee.
6. Instrument the pipeline: surface duration, flake rate, and failure cause; fail fast and report clearly.

## Example

```yaml
# .github/workflows/ci.yml (excerpt)
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: npm }   # key: package-lock.json
      - run: npm ci
      - run: npm test -- --coverage
  build:
    needs: test          # gate: tests must pass first
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm run build
      - uses: actions/upload-artifact@v4   # build once, promote later
        with: { name: dist, path: dist/ }
```

## Pitfalls

- Rebuilding the artifact in the deploy stage — you then ship something CI never tested.
- Caching on a branch name or timestamp instead of a lockfile hash, so the cache never invalidates correctly (stale deps) or never hits (slow).
- Treating flaky tests as "retry until green" — retries hide real races and erode trust in the gate.
- Baking secrets into cached layers or logs; anything cached or echoed is effectively public.

## Output format

```
Pipeline: <platform> config file (valid syntax)

Stage table:
| stage | depends-on | cache key | gate | artifact |
|-------|-----------|-----------|------|----------|

Top 3 risks:
1. <flake source>      -> mitigation
2. <cache staleness>   -> mitigation
3. <secret exposure>   -> mitigation
```
