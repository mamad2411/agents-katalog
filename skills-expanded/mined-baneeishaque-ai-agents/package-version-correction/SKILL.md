---
name: package-version-correction
description: Audit package.json version specifications, extract exact versions from
    package-lock.json or yarn.lock, and replace range specifications with pinned
    exact versions for reproducible builds.
category: Package Management & Dependencies
---

# Package Version Correction Skill

> **Skill ID:** `package-version-correction`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

Replace loose version ranges in `package.json` with exact, pinned versions extracted
from lock files. This skill ensures build reproducibility by enforcing precise version
control across dependency specifications.

When developers specify version ranges (e.g., `^1.16.0`, `~2.5.3`), upgrades between
builds create non-deterministic environments. This skill identifies range-based
specifications and replaces them with exact versions locked in the repository's package
manager state file (`package-lock.json` for npm, `yarn.lock` for Yarn, `pnpm-lock.yaml`
for pnpm).

## Source Rules

This skill operationalizes best practices for:

- **Reproducible builds**: Exact versions prevent environment drift
- **Lock file synchronization**: Versions extracted from authoritative lock files
- **Dependency audit**: Comprehensive package scanning with configurable scope
- **Post-correction validation**: Linting after lock file regeneration

## Prerequisites

| Requirement | Minimum |
|---|---|
| Node.js | 14.0.0+ (or latest supported) |
| Package Manager | npm 6+, Yarn 1.22+, or pnpm 6+ |
| VCS | Git 2.x+ (for validating lock files) |
| Shell | Bash 4+ or PowerShell 5.1+ |

## When to Apply

Apply this skill when:
- User asks: "use exact versions" or "pin package versions"
- User specifies: "replace `^` and `~` with exact versions"
- `package.json` contains range specifiers (`^`, `~`, `>=`, `||`) in devDependencies or dependencies
- Lock file exists and is authoritative (committed to repository)
- Post-dependency-installation validation is required

Do NOT apply when:
- Lock file is missing or out-of-sync (run `npm install` / `yarn install` / `pnpm install` first)
- Project uses library-mode semver ranges intentionally (e.g., published npm packages)
- User explicitly requests preserving ranges for compatibility
- Environment uses git-based or URL-based dependency specifications

## Operational Logic

### Phase 1: Environment Validation

1. **Package Manager Detection**
   ```bash
   # Determine primary package manager
   if [ -f "package-lock.json" ]; then pm="npm"
   elif [ -f "yarn.lock" ]; then pm="yarn"
   elif [ -f "pnpm-lock.yaml" ]; then pm="pnpm"
   else
     echo "ERROR: No lock file found. Run '${pm} install' first."
     exit 1
   fi
   ```

2. **Lock File Validation**
   - Verify lock file exists and is valid JSON/YAML
   - Check lock file is not empty (indicates corrupted state)
   - Confirm lock file timestamp is recent (within last installation)

3. **Git State Check**
   - Ensure repository is clean or changes are staged
   - Verify ability to run `npm install`/lock file regeneration
   - Document current HEAD commit for rollback

### Phase 2: Package.json Audit

1. **Scan all dependency sections**:
   - `dependencies`
   - `devDependencies`
   - `peerDependencies` (advisory only, do not modify)
   - `optionalDependencies`

2. **Identify version specifiers**:
   ```
   ^1.16.0    → Caret (allows minor/patch)
   ~2.5.3     → Tilde (allows patch only)
   >=1.0.0    → Greater-than-or-equal
   1.0.0 - 2.0.0 → Range
   ||         → OR operator
   *          → Wildcard
   ```

3. **Categorize packages**:
   - **To-Fix**: Packages with range specifiers requiring pinning
   - **Already-Exact**: Packages with exact versions (e.g., `1.16.0`)
   - **Git/URL-Based**: Packages with git URLs or local paths (skip)
   - **Workspace/Local**: Packages referencing `workspace:*` or `file:` (skip)

### Phase 3: Version Extraction from Lock Files

#### For npm (package-lock.json)

```bash
# Extract exact version for a package
jq '.dependencies["PACKAGE_NAME"].version' package-lock.json
# Output: "1.16.0"
```

#### For Yarn (yarn.lock)

```bash
# Parse yarn.lock (text-based format)
grep -A 5 "^PACKAGE_NAME@" yarn.lock | grep "version" | head -1
# Example: version "1.16.0"
```

#### For pnpm (pnpm-lock.yaml)

```bash
# Extract from YAML lock file
grep -A 3 "PACKAGE_NAME:" pnpm-lock.yaml | grep "version" | head -1
```

### Phase 4: Version Replacement

1. **Read current package.json**
2. **For each to-fix package**:
   - Lookup exact version in lock file
   - Replace version specifier with exact version
   - Preserve all other metadata (patch, tarball, integrity)

3. **Example transformation**:
   ```json
   // Before
   "oxlint": "^1.16.0"
   
   // After
   "oxlint": "1.16.0"
   ```

### Phase 5: Lock File Regeneration & Validation

1. **Run lock file update** (without installing packages):
   ```bash
   # npm
   npm install --package-lock-only
   
   # yarn
   yarn install --frozen-lockfile
   
   # pnpm
   pnpm install --frozen-lockfile
   ```

2. **Verify lock file integrity**:
   - Check for syntax errors in lock file
   - Verify no new packages were added
   - Confirm all existing packages remain locked

3. **Run optional linting** (if linter is available):
   - Execute `npm run lint` or `yarn lint` if defined in scripts
   - Report warnings/errors (informational only)

### Phase 6: Completion & User Communication

1. **Summary Report**:
   ```
   ✓ Package Version Correction Complete
   
   Statistics:
   - Packages corrected: N
   - Packages already exact: M
   - Packages skipped (git/url): K
   - Lock file regenerated: Yes
   - Linting status: Passed/Warnings/Failed
   ```

2. **Commit Readiness**:
   - Stage `package.json` and lock file
   - Provide commit message template (see below)

3. **Git Commit** (if user authorizes):
   ```
   deps(npm): pin all dependencies to exact versions
   
   - Replace version ranges with exact pinned versions
   - Extract versions from package-lock.json (authoritative)
   - Regenerate lock file to ensure consistency
   - Verify all dependencies remain in locked state
   
   This ensures reproducible builds across all environments.
   ```

## Technical Specifications

### Package Manager Auto-Detection

```bash
if   [ -f "package-lock.json" ]; then pm="npm"
elif [ -f "yarn.lock" ]; then pm="yarn"
elif [ -f "pnpm-lock.yaml" ]; then pm="pnpm"
else echo "ERROR: No lock file found"
fi
```

### Version Extraction Logic

All extraction queries MUST handle:
- **Missing packages** (return error, skip)
- **Multiple versions** (use first/highest, document decision)
- **Non-semver formats** (preserve as-is, log warning)
- **Git SHAs in lock files** (skip, preserve git reference)

### Validation Checkpoints

| Checkpoint | Success Criteria |
|---|---|
| **Lock file exists** | File size > 1KB, valid JSON/YAML syntax |
| **Versions extracted** | All required packages found in lock file |
| **JSON updated** | All replaced versions are exact semver |
| **Lock regenerated** | Lock file modified, no new packages added |
| **Syntax valid** | `npm ls` / `yarn check` returns no errors |

## Error Handling

### Error Scenario: Missing Lock File

```
ERROR: No lock file found in current directory.
ACTION: Run 'npm install' first to generate package-lock.json.
```

### Error Scenario: Package Not in Lock File

```
WARNING: Package "PACKAGE_NAME" not found in lock file.
ACTION: Run 'npm install' to add missing entry, then retry.
```

### Error Scenario: Invalid Version in Lock File

```
WARNING: Package "PACKAGE_NAME" has non-semver version: "next"
ACTION: Skipping this package. Manually update if needed.
```

## Post-Execution Checklist

- [ ] All `package.json` dependencies with ranges are now exact versions
- [ ] Lock file regenerated with `npm install --package-lock-only`
- [ ] No new packages added during lock file regeneration
- [ ] Linting (if enabled) reports acceptable results
- [ ] Git status shows modified `package.json` and lock file
- [ ] User has reviewed changes before committing

## Environmental Assumptions

- Working directory is a Node.js project root (contains `package.json`)
- Package manager is installed and accessible in $PATH
- Lock file matches current `package.json` state
- Git repository is initialized (for rollback capability)
- No active npm/yarn/pnpm processes (avoid lock conflicts)

## Related Conversations & Traceability

**Session**: `cfedcf46-1072-4430-b653-62041d45fcf1`
**Context**: User requested exact versions for oxlint dependency in `/Users/dk/lab-data/acers-web/`
**Motivating Statement**: "i always want exact dependency version instead of range of versions"
**Implementation Date**: 2026-04-15
