---
name: dependency-auditor
description: Dependency health scanner covering vulnerabilities, license compliance, outdated packages, and upgrade planning. Use when auditing dependencies, checking licenses, planning upgrades, or assessing supply chain risk.
---

# Dependency Auditor

**Category:** Dependency Management & Security

## Overview

Comprehensive dependency analysis covering security vulnerabilities, license compliance, outdated packages, bloat detection, and upgrade planning. Supports JavaScript, Python, Go, Rust, Ruby, Java, PHP, and .NET ecosystems.

## When to Use

- Before releasing to production
- When adding new dependencies
- Quarterly dependency health checks
- License compliance audits
- Planning major dependency upgrades

## Supported Ecosystems

| Language | Manifest | Lockfile |
|----------|----------|----------|
| JavaScript | `package.json` | `bun.lock`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml` |
| Python | `requirements.txt`, `pyproject.toml` | `Pipfile.lock`, `poetry.lock` |
| Go | `go.mod` | `go.sum` |
| Rust | `Cargo.toml` | `Cargo.lock` |
| Ruby | `Gemfile` | `Gemfile.lock` |
| Java | `pom.xml` | `gradle.lockfile` |
| PHP | `composer.json` | `composer.lock` |
| .NET | `packages.config` | `project.assets.json` |

## Audit Workflow

### Step 1: Vulnerability Scan

```bash
# JavaScript/Node.js
# JavaScript/Node.js (prefer bun)
rtk bun audit

# Alternative: npm audit
# npm audit --json > audit-results.json

# Python
pip audit
pip audit --format=json > audit-results.json

# Go
go list -m -json all | go-mod-vulncheck

# General (if available)
grype .
```

### Step 2: License Compliance

#### License Classification

| Category | Licenses | Risk Level |
|----------|----------|-----------|
| Permissive | MIT, Apache 2.0, BSD, ISC | ✅ Low risk |
| Weak copyleft | LGPL, MPL 2.0 | ⚠️ Medium — check distribution model |
| Strong copyleft | GPL v2/v3, AGPL v3 | 🔴 High — may require source disclosure |
| Proprietary | Commercial, custom | 🔴 Review terms carefully |
| Unknown | Missing or ambiguous | ⚠️ Investigate before using |

#### Conflict Detection
- GPL + MIT in same binary → GPL takes over
- AGPL in server code → may require open-sourcing your server
- No license = all rights reserved (cannot use legally)

```bash
# JavaScript - check licenses
rtk bunx license-checker --summary
rtk bunx license-checker --failOn "GPL-2.0;GPL-3.0;AGPL-3.0"

# Python
pip-licenses --format=table
```

### Step 3: Outdated Detection

```bash
# JavaScript
# JavaScript (prefer bun)
rtk bun outdated
rtk bunx npm-check-updates

# Python
pip list --outdated

# Go
go list -m -u all
```

**Categorize updates:**
- 🟢 Patch (1.2.3 → 1.2.4) — Safe, auto-update
- 🟡 Minor (1.2.3 → 1.3.0) — Review changelog
- 🔴 Major (1.2.3 → 2.0.0) — Plan migration

### Step 4: Bloat Analysis

Check for:
- Dependencies not actually imported/used in code
- Multiple packages providing same functionality
- Oversized packages for simple use cases (e.g., `moment.js` for date formatting)

```bash
# JavaScript - find unused deps
rtk bunx depcheck

# Bundle size impact
rtk bunx bundlephobia-cli <package-name>
```

### Step 5: Supply Chain Assessment

- Are packages maintained? (last release date, open issues)
- Any recent maintainer changes?
- Download counts reasonable for the package?
- Are lockfiles committed and up-to-date?

## Upgrade Priority Matrix

| Priority | Criteria | Action |
|----------|----------|--------|
| 🔴 Critical | Known CVE, actively exploited | Patch immediately |
| 🟡 High | Known CVE, no exploit, or EOL dependency | Patch within sprint |
| 🟢 Medium | Major version behind, no security issue | Plan for next quarter |
| ⚪ Low | Minor/patch behind, well-maintained | Update on next dependency sweep |

## Report Format

```markdown
## Dependency Audit Report

**Project:** [name]
**Date:** [date]
**Total Dependencies:** N direct, M transitive

### 🔴 Vulnerabilities
| Package | Version | CVE | Severity | Fix Version |
|---------|---------|-----|----------|-------------|

### ⚖️ License Compliance
| Package | License | Risk | Action Needed |
|---------|---------|------|--------------|

### 📦 Outdated
| Package | Current | Latest | Type | Priority |
|---------|---------|--------|------|----------|

### 🗑️ Unused/Bloat
| Package | Size | Alternative |
|---------|------|-------------|

### ✅ Summary
- Vulnerabilities: N critical, N high
- License conflicts: N
- Outdated packages: N major, N minor
- Unused packages: N
```
