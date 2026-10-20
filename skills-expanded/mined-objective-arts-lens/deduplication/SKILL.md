---
name: deduplication
description: Find duplicated code and consolidate into shared utilities. Fixes all duplicates.
---

# /deduplication [path]

Find duplicated code patterns and consolidate them into shared utilities.

> **No arguments?** Describe this skill and stop. Do not execute.

## First: Activate Workflow

```bash
mkdir -p .claude && echo '{"skill":"deduplication","started":"'$(date -Iseconds)'"}' > .claude/active-workflow.json
```

## Craft Standards (MANDATORY)

**Consolidate toward code a master craftsperson would be proud of.**

Duplication is a form of technical debt. The consolidated code must look like it was written by a skilled human engineer.

### AI Antipatterns When Consolidating

- Don't create over-abstracted "utility frameworks"
- Don't add unnecessary configuration to consolidated functions
- Don't create deep inheritance hierarchies to share code
- Don't wrap simple functions in classes for no reason

### Human Craft When Consolidating

- Create focused, single-purpose utility functions
- Use clear names that describe what the function does
- Keep the consolidated code SIMPLER than the duplicates
- If consolidation makes code harder to understand, reconsider

**Test:** Is the consolidated version clearer than having the code inline? If not, maybe duplication was acceptable.

---

## Process

### Step 0: Load Expert Guidance

Before starting, read these canon skills and apply their principles throughout:

**Always load:**
1. `canon/composition/SKILL.md`
2. `canon/clarity/SKILL.md`
3. `canon/simplicity/SKILL.md`

**Auto-detect language canon (check files, load matches):**

| Check | If found, also read |
|-------|---------------------|
| `*.ts` or `*.js` files in target | `canon/javascript/typescript/SUMMARY.md`, `canon/javascript/js-safety/SUMMARY.md`, `canon/javascript/js-perf/SUMMARY.md`, `canon/javascript/js-internals/SUMMARY.md`, `canon/javascript/functional/SUMMARY.md` |
| `angular.json` in project root | `canon/angular/angular-arch/SUMMARY.md`, `canon/angular/angular-core/SUMMARY.md`, `canon/angular/angular-perf/SUMMARY.md`, `canon/angular/rxjs/SUMMARY.md` |
| `package.json` contains `"react"` | `canon/javascript/react-state/SUMMARY.md`, `canon/javascript/react-test/SUMMARY.md`, `canon/javascript/reactivity/SUMMARY.md` |
| `pom.xml` or `build.gradle` in project | `canon/java/SUMMARY.md` |
| `*.py` files in target | `canon/python/python-advanced/SUMMARY.md`, `canon/python/python-idioms/SUMMARY.md`, `canon/python/python-patterns/SUMMARY.md`, `canon/python/python-protocols/SUMMARY.md` |
| `*.cs` files or `*.csproj` in project | `canon/csharp/csharp-depth/SUMMARY.md`, `canon/csharp/type-systems/SUMMARY.md`, `canon/csharp/async/SUMMARY.md` |

If a skill file doesn't exist (not installed in this project), skip it and continue.
List loaded experts in EXPERTS_LOADED output.

### Step 0b: Check Known Pitfalls

Read `canon/pitfalls/SKILL.md` if it exists. Apply its patterns as you work:

- **Code Quality Traps** → search for duplicate patterns (same-name constants in different files)
- **Logic Traps** → when consolidating, ensure the shared version avoids known bug patterns (TOCTOU)

If the file doesn't exist, skip it and continue.

### Step 1: Find Duplicates

Search for duplicated patterns:

```bash
# Function definitions appearing in multiple files
grep -rn "function copy\|function hash\|execSync.*git" --include="*.ts" | grep -v test | grep -v node_modules

# Repeated utility patterns
grep -rn "createHash\|getGitCommit\|getGitRemote" --include="*.ts" | grep -v test | grep -v node_modules
```

### Step 2: Analyze Each Duplicate

For each pattern found in 2+ files:
1. Read all instances
2. Compare logic - are they truly identical?
3. If identical or nearly identical → consolidate
4. If intentionally different → document why and skip

### Step 3: Consolidate (MANDATORY)

For each TRUE duplicate:

1. **Create shared utility** in appropriate location:
   - `src/utils/` for general utilities
   - `src/shared/` for cross-module code
   - Module's own `helpers.ts` for module-specific

2. **Extract the function** to shared location:
   ```typescript
   // src/utils/fs.ts
   export function copyDirectoryRecursive(src: string, dest: string): void {
     // consolidated implementation
   }
   ```

3. **Update all usages** to import from shared:
   ```typescript
   import { copyDirectoryRecursive } from '../utils/fs.js';
   ```

4. **Delete duplicate code** from original locations

5. **Verify** - run build/tests:
   ```bash
   npm run build
   npm test
   ```

### Step 4: Report

Document what was consolidated.

## Output Format

```markdown
## Deduplication Fix: [path]

### Summary

| Metric | Value |
|--------|-------|
| Duplicates found | N |
| Consolidated | N |
| Kept separate | N |

### Consolidated

1. **copyDirectoryRecursive**
   - Extracted to: `src/utils/fs.ts`
   - Removed from: `src/canon/helpers.ts`, `src/workflow/index.ts`
   - Usages updated: 5 files

2. **getGitCommit**
   - Extracted to: `src/utils/git.ts`
   - Removed from: `src/canon/index.ts`, `src/profiles/apply.ts`
   - Usages updated: 3 files

### Kept Separate (with reason)

1. **hashDirectory** - Different algorithms for different manifest formats

### Verification

- Build: ✅ Pass
- Tests: ✅ Pass

EXPERTS_LOADED: [list of skill names actually read]

---
DUPLICATES_FOUND: N
CONSOLIDATED: N
KEPT_SEPARATE: N
DEDUPLICATION_COMPLETE: yes
```

## Pipeline Constraints

When running as part of a pipeline (called by `/build` or `/improve`):

**SCOPE CONSTRAINT:** Only consolidate true duplicates. Do not refactor, rename, or restructure code that is not duplicated.

**COMPLEXITY BUDGET:** The consolidated version must be simpler than the duplicates it replaces. Net-zero or net-negative files, functions, and lines. EXCEPTION: Security fixes are exempt.

**NO SILENT FAILURES:** Do not change a throw/crash to a log-and-continue. Fail-fast on misconfiguration is always correct.

## Rules

- **MUST CONSOLIDATE** - If it's truly duplicated, extract it
- **VERIFY** - Build and test after each consolidation
- **DOCUMENT** - If keeping separate, explain why
- **SINGLE SOURCE** - Each piece of logic should exist once

## Kept Separate Criteria

Only keep duplicates separate if:
- Intentionally different algorithms
- Different dependencies that can't be unified
- Performance-critical paths needing specialization

"Might diverge in the future" is NOT a valid reason.

## Comparison

| Skill | Finds | Fixes |
|-------|-------|-------|
| `/dedupe-scan` | ✓ | ✗ (read-only) |
| `/deduplication` | ✓ | ✓ (consolidates) |
