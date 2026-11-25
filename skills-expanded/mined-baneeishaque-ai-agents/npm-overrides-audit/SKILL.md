---
name: npm-overrides-audit
description: Audit package.json overrides field, test each override's necessity,
    remove unnecessary ones, and clean up the configuration for simpler dependency
    resolution.
category: Package Management & Dependencies
---

# NPM Overrides Audit & Correction Skill

> **Skill ID:** `npm-overrides-audit`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

Audit npm's `overrides` field to identify unnecessary version constraints, test their
necessity one-by-one, and remove those that don't contribute to build stability. This
skill helps simplify dependency resolution and reduces hidden constraints that can
hinder future upgrades.

The `overrides` field (npm 8.3+) forces specific versions across the entire dependency
tree. While powerful for resolving conflicts, unnecessary overrides reduce flexibility
and create implicit project assumptions that aren't documented.

## Source Rules

This skill operationalizes best practices for:

- **Override necessity assessment**: Testing each override's requirement
- **Lock file validation**: Regenerating and verifying compatibility
- **Atomic override removal**: Individual testing + commit per override
- **Configuration cleanup**: Removing empty or redundant sections

## Prerequisites

| Requirement | Minimum |
|---|---|
| Node.js | 14.0.0+ |
| npm | 8.3.0+ (overrides support) |
| VCS | Git 2.x+ |
| Shell | Bash 4+ or PowerShell 5.1+ |
| Node Modules | node_modules/ present or regeneratable via `npm install` |

## When to Apply

Apply this skill when:
- User asks: "audit overrides" or "are these overrides needed?"
- User specifies: "remove unnecessary overrides" or "test overrides"
- `package.json` contains an `overrides` field with one or more entries
- Project maintains lock file (package-lock.json, yarn.lock, pnpm-lock.yaml)
- Build reproducibility and dependency resolution clarity are priorities

Do NOT apply when:
- `package.json` has no `overrides` field
- User explicitly states overrides are required (production compatibility mandate)
- Project is a library (libraries should minimize overrides to avoid imposing constraints)
- Lock file is missing or corrupted

## Operational Logic

### Phase 1: Environment Validation

1. **Verify package manager state**:
   ```bash
   if [ ! -f "package.json" ]; then
     echo "ERROR: package.json not found"
     exit 1
   fi
   
   # Determine package manager
   if [ -f "package-lock.json" ]; then pm="npm"
   elif [ -f "yarn.lock" ]; then pm="yarn"
   elif [ -f "pnpm-lock.yaml" ]; then pm="pnpm"
   else
     echo "ERROR: No lock file found. Run 'npm install' first."
     exit 1
   fi
   ```

2. **Check for overrides field**:
   ```bash
   jq '.overrides' package.json
   # If null or empty: "No overrides found. Exiting."
   ```

3. **Validate lock file integrity**:
   - Check file size (> 1KB)
   - Verify valid JSON/YAML syntax
   - Confirm recent modification timestamp

4. **Git repository check**:
   - Verify `.git/` directory exists
   - Ensure working tree is clean (or allow staging)
   - Document current HEAD commit for rollback

### Phase 2: Override Inventory & Analysis

1. **Parse package.json overrides**:
   ```python
   import json
   with open('package.json') as f:
       pkg = json.load(f)
   
   overrides = pkg.get('overrides', {})
   total = len(overrides)
   ```

2. **Categorize each override**:
   - **Dependency type**: Is it in dependencies, devDependencies, or not installed?
   - **Direct vs. nested**: Does it override a direct dependency or nested one?
   - **Reason documentation**: Look for comments in git history (if any)

3. **Log initial state**:
   ```
   Found N overrides to audit:
   1. package-a: version-x
   2. package-b: version-y
   ...
   ```

### Phase 3: Individual Override Testing (One-by-One)

**For each override:**

1. **Preserve original state**:
   ```bash
   cp package.json package.json.bak
   cp package-lock.json package-lock.json.bak
   ```

2. **Remove the override**:
   ```python
   del pkg['overrides'][package_name]
   with open('package.json', 'w') as f:
       json.dump(pkg, f, indent=2)
   ```

3. **Regenerate lock file**:
   ```bash
   # npm
   npm install --package-lock-only
   
   # yarn
   yarn install --frozen-lockfile
   
   # pnpm
   pnpm install --frozen-lockfile
   ```

4. **Evaluate lock file regeneration result**:

   | Result | Interpretation | Action |
   |--------|---|---|
   | Lock file regenerates cleanly | Override not needed | Mark for removal |
   | Lock file conflicts/errors | Override is necessary | Restore original, mark as "REQUIRED" |
   | New packages added | Override prevents conflicts | Restore original, mark as "REQUIRED" |
   | Lock file unchanged | Override is redundant | Mark for removal |

5. **Commit decision**:
   - **If removable**: Commit with message: `deps(overrides): remove unnecessary {package} override`
   - **If required**: Restore original, log reason, skip

### Phase 4: Cleanup & Consolidation

1. **Remove empty overrides section** (if all removed):
   ```python
   if 'overrides' in pkg and not pkg['overrides']:
       del pkg['overrides']
   ```

2. **Commit cleanup**:
   ```
   chore: remove empty overrides section
   
   All unnecessary overrides have been tested and removed.
   Remaining state documented in prior commits.
   ```

### Phase 5: Final Report & Verification

1. **Summary Report**:
   ```
   ✓ Override Audit Complete
   
   Statistics:
   - Overrides tested: N
   - Removed (unnecessary): M
   - Retained (necessary): K
   - Lock file validation: PASSED
   
   Commits created: M + 1 (cleanup)
   ```

2. **Verification output**:
   - Current `overrides` field (if any remain)
   - Rationale for retained overrides
   - Link to removal commits

3. **Next steps guidance**:
   - If all removed: "All unnecessary constraints eliminated. Dependency resolution simplified."
   - If some retained: "Document retained overrides in ARCHITECTURE.md or similar"

## Technical Specifications

### Override Test Protocol

**Test Independence**: Each override is tested in isolation:
```
Iteration N:
1. Save current package.json + lock file
2. Remove override[N]
3. Run: npm install --package-lock-only
4. Evaluate result
5. Commit or restore based on result
6. Move to override[N+1]
```

**Lock File Comparison Logic**:
- Compare size and line count (> 5% change = significant)
- Parse and compare package tree structure
- Check for new packages or version conflicts

### Validation Checkpoints

| Checkpoint | Success Criteria |
|---|---|
| **Override identified** | Field exists and contains entries |
| **Test isolation** | Lock file regenerates independently for each override |
| **Removal success** | npm ls (or equivalent) shows no errors |
| **Cleanup complete** | Empty overrides section removed if applicable |
| **Git history** | Each removal is individually committed |

## Error Handling

### Error Scenario: Override Breaks Build

```
ERROR: Removing override "package-x" causes lock file conflicts
Reason: package-x version incompatible with transitive dependency tree

ACTION: Restoring original override
        Marking override as REQUIRED
        Document incompatibility in code comments
```

### Error Scenario: Lock File Corruption

```
WARNING: Lock file regeneration produced invalid syntax
Reason: npm/yarn/pnpm version incompatibility or corrupted state

ACTION: Restore backup files
        Clear node_modules/ (if needed)
        Retry with: npm ci
```

## Post-Execution Checklist

- [ ] All overrides tested individually
- [ ] Each removal or retention decision committed atomically
- [ ] Empty overrides section removed (if applicable)
- [ ] Lock file valid and regenerated
- [ ] No uncommitted changes remain
- [ ] Git log shows clear audit trail
- [ ] Rationale for retained overrides documented

## Environmental Assumptions

- Working directory is Node.js project root
- package.json is valid JSON with potential `overrides` field
- Lock file matches current package.json state (or can be regenerated)
- Git repository initialized with clean or stageable working tree
- npm/yarn/pnpm installed and accessible in $PATH
- No concurrent npm/yarn/pnpm processes (avoid lock conflicts)

## Related Conversations & Traceability

**Session**: `cfedcf46-1072-4430-b653-62041d45fcf1`
**Context**: After pinning 152 packages to exact versions, tested 2 unnecessary overrides
**Motivating Statement**: "sounds like overrides may cause problems"
**Motivating Work**: Audited resolve-url-loader and css-select overrides
  - Both tested and found to be unnecessary
  - Both successfully removed via individual lock file regeneration
  - Project dependency resolution simplified
**Implementation Date**: 2026-04-15
