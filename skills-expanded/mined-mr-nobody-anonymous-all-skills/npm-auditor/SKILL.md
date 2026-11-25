---
name: npm-auditor
description: Audit npm dependencies for vulnerabilities, staleness, licenses, and supply-chain risk.
category: security
aliases:
- npm
- audit
- pnpm
- yarn
- dependency
- vulnerabilities
triggers:
- Audit my dependencies
- Run npm audit
- Check for CVEs
- Are my packages up to date
- License check
keywords:
- npm
- pnpm
- yarn
- audit
- dependency
- vulnerability
- cve
- license
- supply
- chain
dependencies:
- optional:npm
risk: medium
version: 1.0.0
source: custom
enabled: true
capabilities:
- npm-auditor
- security
inputs:
- task
- context
outputs:
- result
- report
lifecycle: enabled
author: Mr-Nobody-Anonymous
tags:
- audit
- auditor
- npm
- pnpm
- security
- yarn
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Npm Auditor

## Purpose
Run a layered audit of a Node.js project's dependencies — **vulnerabilities** (CVEs),
**outdated packages**, **license risks**, and **supply-chain red flags** (typosquats,
unmaintained packages, postinstall scripts) — and turn the result into a single,
actionable fix plan.

## When to Use
- A new dependency is being added
- A routine security check is requested
- After a major version bump or lockfile change
- Before a release

## When NOT to Use
- The project has no `package.json`
- The user is offline and the lockfile cannot be validated against the registry
- The user wants a license *enforcement* rule (this skill only reports)

## Capabilities
- `npm audit --json` (or pnpm/yarn equivalent), grouped by severity
- `npm outdated --json`, grouped by major/minor/patch
- License scan: list of SPDX expressions, flag unknown / GPL / AGPL
- Postinstall scan: list packages with `scripts.postinstall`
- Typosquat / maintenance check against a curated list
- Suggest a fix plan: `npm audit fix`, then a list of manual bumps

## Inputs
- `mode`: `cves` | `outdated` | `licenses` | `all` (default `all`)
- `severity`: `low|moderate|high|critical` filter (default `moderate+`)
- `prod-only`: include only production dependencies (default false)
- `apply`: actually run `npm audit fix` (default false — report only)

## Workflow
1. **Detect** package manager (`package-lock.json` â†’ npm, `pnpm-lock.yaml` â†’ pnpm, `yarn.lock` â†’ yarn).
2. **Run audit** in the chosen mode; parse JSON.
3. **Group** findings by severity and by package.
4. **Cross-check** postinstall scripts and license expressions.
5. **Compose the fix plan** — small, ordered, with the exact command per step.
6. **Print** a table: package | current | target | severity | license | action.
7. **Optionally apply** `npm audit fix` (non-breaking) if `--apply`.

## Tools
- `npm` / `pnpm` / `yarn` (whichever the project uses)
- `jq` for JSON shaping
- Optional: `license-checker` for richer license reports

## Examples
**User:** "Audit my project for CVEs."
**Response:**

| package | severity | via | fix |
|---|---|---|---|
| `lodash` | high | `^4.17.20` | `npm audit fix` |
| `axios` | moderate | `^0.27.0` | bump to `^1.7.0` (manual) |

**User:** "What packages are out of date?"
**Response:** 3 majors behind (breaking), 7 minors, 12 patches. List grouped.

## Safety
- Never run `npm audit fix --force` automatically
- Never modify the lockfile without a dry-run preview first
- Surface postinstall scripts to the user; require approval to install
- Skip `optionalDependencies` and `devDependencies` unless asked

## Source
Auto-generated from openclawskills.net description.

## Notes
Maintained as part of canonical security category.
