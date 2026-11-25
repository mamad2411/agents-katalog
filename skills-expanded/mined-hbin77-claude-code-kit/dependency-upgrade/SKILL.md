---
name: dependency-upgrade
description: Safely upgrade project dependencies with minimal risk.
---

# Dependency Upgrade Skill

Safely upgrade project dependencies with minimal risk.

## Process

### 1. Audit Current State
```bash
# Node.js
npx npm-check-updates
npm audit

# Python
pip list --outdated
pip-audit
```

### 2. Categorize Updates
- **Patch** (1.0.x): Usually safe, bug fixes only
- **Minor** (1.x.0): New features, should be backwards compatible
- **Major** (x.0.0): Breaking changes, needs careful review

### 3. Upgrade Strategy

**Safe batch**: Upgrade all patch versions at once
```bash
npx npm-check-updates -t patch -u && npm install
```

**Minor versions**: Upgrade one at a time, test between each
```bash
npx npm-check-updates -f [package] -t minor -u && npm install
```

**Major versions**:
1. Read the changelog/migration guide
2. Upgrade one package at a time
3. Fix breaking changes
4. Run full test suite

### 4. Verification After Each Upgrade
1. `npm install` (clean install)
2. `npm run build` (no build errors)
3. `npm test` (all tests pass)
4. Quick manual smoke test

### 5. Commit Strategy
- One commit per logical group of upgrades
- Include "chore(deps):" prefix
- Note any breaking changes in commit body
