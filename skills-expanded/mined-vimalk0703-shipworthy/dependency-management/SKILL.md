---
name: dependency-management
description: Vet packages before adoption, audit for vulnerabilities, pin versions, and prevent dependency bloat.
invoke_when: Use when adding a new dependency, reviewing package.json/requirements.txt, auditing for vulnerabilities, or when the post-tool-use hook detects a package installation.
---

# Dependency Management

## Before Adding a Dependency

### 1. Is it necessary?
- Can this be done in <50 lines without the dependency?
- Does the standard library already provide this?

### 2. Is it trustworthy?
- Downloads: >10K weekly (npm) or >1K stars (GitHub)
- Maintenance: updated within last 6 months
- License: MIT, Apache 2.0, BSD are safe
- Security: no open critical/high CVEs

### 3. What's the cost?
- Bundle size impact (for frontend)
- Transitive dependency count
- Lock-in risk

## When Adding
1. Install with exact version: `npm install package@1.2.3 --save-exact`
2. Run `npm audit` immediately after
3. Review lock file diff
4. Document WHY this dependency was chosen

## Red Flags
- Package with <100 weekly downloads
- Single maintainer with no org backing (for critical deps)
- No test suite in the package source
- Excessive transitive dependencies for a simple task
- Not updated in 2+ years (unless genuinely complete)
- Copyleft license (GPL) when your project isn't
