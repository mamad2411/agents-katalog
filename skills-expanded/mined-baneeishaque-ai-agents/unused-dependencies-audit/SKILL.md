---
name: unused-dependencies-audit
description: Comprehensively audit package.json dependencies, detect actual usage
    in codebase via import analysis, identify unused packages, and safely remove
    them one-by-one with validation.
category: Package Management & Dependencies
---

# Unused Dependencies Audit & Removal Skill

> **Skill ID:** `unused-dependencies-audit`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

Audit all npm/Yarn/pnpm dependencies to identify packages that are declared in
`package.json` but not actually imported in the codebase. This skill analyzes source
code for import/require statements, cross-references against declared dependencies,
and removes unused packages one-by-one while validating build integrity.

Unused dependencies increase install time, bloat node_modules, obscure true project
requirements, and create false upgrade obligations. This skill eliminates that waste.

## Source Rules

This skill operationalizes best practices for:

- **Codebase scanning**: Comprehensive import/require pattern matching
- **Dependency cross-reference**: Matching imports to package.json entries
- **One-by-one removal**: Testing each unused package with build validation
- **Atomic commits**: Individual removal commits with removal rationale
- **False-positive handling**: Manual review protocols for ambiguous packages

## Prerequisites

| Requirement | Minimum |
|---|---|
| Node.js | 14.0.0+ |
| Package Manager | npm 6+, Yarn 1.22+, or pnpm 6+ |
| VCS | Git 2.x+ |
| Shell | Bash 4+ or PowerShell 5.1+ |
| Build Command | `npm run build` or equivalent (for validation) |
| Source Files | TypeScript/JavaScript in standard directory (src/, lib/, etc.) |

## When to Apply

Apply this skill when:
- User asks: "find unused packages" or "remove unused dependencies"
- User specifies: "audit what packages are actually used"
- Project wants to reduce install size and build time
- Codebase cleanup and modernization is in progress
- Dependency drift has accumulated (many commits without dep maintenance)

Do NOT apply when:
- Project doesn't have a build step (pure static site)
- User explicitly protects certain packages from removal
- Project is actively refactoring (large uncommitted changes)
- Source code organization is non-standard (no clear root source dir)

## Operational Logic

### Phase 1: Environment & Codebase Discovery

1. **Locate source directories**:
   ```bash
   # Check for standard locations
   for dir in src src/ lib lib/ app app/ source; do
     if [ -d "$dir" ]; then
       source_dir="$dir"
       break
     fi
   done
   ```

2. **Identify file patterns**:
   - JavaScript: `*.js`
   - TypeScript: `*.ts`, `*.tsx`
   - React JSX: `*.jsx`

3. **Count analysis scope**:
   - Total source files to scan
   - Estimated import statements
   - Expected coverage percentage

4. **Verify build command exists**:
   ```bash
   # Check package.json scripts.build
   npm run build 2>&1 | head -5
   ```

### Phase 2: Import Statement Scanning

**Strategy**: Use multi-pattern regex to catch all common import styles

```bash
# Pattern examples
import X from 'pkg'
import * as X from 'pkg'
import { X } from 'pkg'
require('pkg')
from 'pkg'
require("pkg")
import('pkg')
```

**Implementation** (ripgrep or grep):

```bash
grep -r --include="*.{js,jsx,ts,tsx}" \
  -E "from\s+['\"]([^'\"]+)['\"]|require\(['\"]([^'\"]+)['\"]\)" \
  src/
```

**Extract package names**:
- For scoped packages: `@scope/package` → keep full name
- For paths: `lodash/fp` → extract `lodash`
- For file imports: `./components` → skip (local import)

### Phase 3: Package Classification

**For each package.json entry**:

| Category | Criterion | Action |
|----------|-----------|--------|
| **Used** | Import found in code | Keep |
| **Dev-only tool** | Build script, webpack plugin, babel preset | Inspect manually |
| **Indirect/Nested** | Listed but dependencies import it | Verify with `npm ls` |
| **Extraneous** | In node_modules but not in package.json | Flag for cleanup |
| **Type definitions** | `@types/*` with no base package | Investigate |
| **Unused candidate** | Zero import references | Mark for removal testing |

### Phase 4: Manual Review of Ambiguous Cases

**False-positive patterns** (require manual inspection):

1. **Dynamic imports**: `import(packageName)` - can't detect statically
2. **Webpack loaders**: Used in webpack config, not source code
3. **Babel plugins**: Used in `.babelrc` or `babel.config.js`
4. **PostCSS plugins**: Used in `postcss.config.js`
5. **Rollup plugins**: Used in `rollup.config.js`
6. **Vite plugins**: Used in `vite.config.js`
7. **Type definitions only**: `@types/*` packages used for TS types only
8. **CLI tools**: Packages invoked in npm scripts (e.g., `prettier`, `eslint`)

**Manual investigation**:
```bash
# Check webpack/rollup/vite config
grep -r "package-name" *.config.js

# Check babel config
grep -r "package-name" .babelrc babel.config.js

# Check postcss config
grep -r "package-name" postcss.config.js

# Check if in npm scripts
jq '.scripts' package.json
```

### Phase 5: One-by-One Removal Testing

**For each unused candidate**:

1. **Backup state**:
   ```bash
   cp package.json package.json.bak
   cp package-lock.json package-lock.json.bak
   git stash
   ```

2. **Remove from package.json**:
   ```json
   // Remove from: dependencies, devDependencies, optionalDependencies
   ```

3. **Clean and reinstall**:
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

4. **Run build validation**:
   ```bash
   npm run build 2>&1
   ```

5. **Evaluate result**:

   | Result | Interpretation | Action |
   |--------|---|---|
   | Build succeeds | Dependency truly unused | Commit removal |
   | Build fails with clear error | Dependency required | Restore, mark as required |
   | Build succeeds, then runtime error | Indirect dependency | Restore, investigate |
   | No build command | Manual verification | Use `npm ls package-name` |

6. **Commit decision**:
   - **If removable**: `deps: remove unused {package}`
   - **If required**: Restore from backup
   - **If ambiguous**: Mark for manual review

### Phase 6: Extraneous Packages Cleanup

**Extraneous packages** (in node_modules but not in package.json):

```bash
npm ls --depth=0 2>&1 | grep "extraneous"
```

These should be removed automatically:
```bash
npm prune
npm prune --production  # Only for prod, remove devDeps
```

### Phase 7: Final Report & Verification

1. **Summary statistics**:
   ```
   ✓ Unused Dependencies Audit Complete
   
   - Total packages scanned: N
   - Used packages: M
   - Unused candidates: K
   - Removed: R
   - Extraneous cleaned: E
   - Marked for manual review: F
   ```

2. **Build validation**:
   - Run full build command
   - Run test suite (if exists)
   - Verify no runtime errors

3. **Disk/Time savings**:
   - node_modules size before/after
   - npm install time before/after
   - Overall project size reduction

## Technical Specifications

### Import Pattern Matching

**Comprehensive regex for JavaScript/TypeScript**:

```regex
(?:
  from\s+['"]([^'"]+)['"]      # ES6 import
  |require\s*\(\s*['"]([^'"]+)['"]  # CommonJS require
  |import\s*\(\s*['"]([^'"]+)['"]   # Dynamic import
)
```

**Processing rules**:
- Ignore relative imports (`./`, `../`, `/`)
- Extract primary package name from paths (`lodash/fp` → `lodash`)
- Handle scoped packages (`@babel/core` → keep as-is)
- Deduplicate matches

### Validation Checkpoints

| Checkpoint | Success Criteria |
|---|---|
| **Source files found** | At least 10 files in standard directories |
| **Imports detected** | At least 20 import statements found |
| **Build command exists** | `npm run build` (or equivalent) succeeds pre-removal |
| **Each removal tested** | Lock file regenerates, build re-runs |
| **No unintended removals** | Removed packages match zero-import criteria |
| **Node modules clean** | `npm ls --depth=0` shows no extraneous |

## Error Handling

### Error Scenario: Removal Breaks Build

```
ERROR: Removing "package-x" causes build failure
Build output: Cannot find module "package-x"

ACTION: Restoring package-x from backup
        Marking as REQUIRED
        Investigating indirect dependency chain
```

### Error Scenario: No Build Command

```
WARNING: No build command found in package.json scripts

ACTION: Fall back to: npm ls {package}
        Manual verification required
        Document decision in audit report
```

## False Positive Mitigation

**High-risk packages that appear unused but are required**:

- Webpack loaders (check webpack.config.js)
- Babel plugins (check .babelrc)
- PostCSS plugins (check postcss.config.js)
- CLI tools in npm scripts (check scripts section)
- Type definitions (@types/* packages)
- Polyfills (explicitly side-effect imports)

**Pre-removal verification**:
```bash
# Comprehensive check
grep -r "package-name" src/ .*.js *.config.js
```

## Post-Execution Checklist

- [ ] All source directories scanned
- [ ] Import patterns matched and extracted
- [ ] Ambiguous packages manually reviewed
- [ ] Each unused candidate tested individually
- [ ] Build succeeds after each removal
- [ ] No runtime errors detected
- [ ] Extraneous packages cleaned
- [ ] node_modules size/install time verified
- [ ] Git history shows clear removal audit trail
- [ ] Final build validation passed

## Environmental Assumptions

- Working directory is JavaScript/TypeScript project root
- package.json is valid and contains all explicit dependencies
- Source code is in standard location (src/, lib/, app/, etc.)
- Build command exists and can be run repeatedly
- Git repository initialized with ability to stash/restore
- npm/yarn/pnpm installed and accessible in $PATH
- No concurrent npm processes (avoid lock conflicts)

## Related Conversations & Traceability

**Session**: `cfedcf46-1072-4430-b653-62041d45fcf1`
**Context**: After pinning 152 packages and removing overrides, questioned unused dependencies
**Motivating Statement**: "i suspect that so many packages are added without any code usage"
**Preliminary Investigation**: 
  - Found 1711 source files in codebase
  - Identified 40 extraneous packages already in node_modules
  - 152 packages in package.json requiring individual import analysis
  - Multi-pass import scanning needed for comprehensive detection
**Implementation Date**: 2026-04-15
