---
name: anti-slop-fix
description: Runs the anti-slop audit on source code files and automatically applies fixes for detected issues. Invokes the anti-slop analysis first, then fixes each issue in-place. Use when the user wants to clean up AI slop automatically, fix slop patterns, or asks "fix slop", "clean up code", "auto-fix slop", "anti-slop fix".
metadata:
  author: b4r7x
  version: "1.0.0"
  argument-hint: <file-paths-or-globs>
---

# Anti-Slop Fix

Runs the anti-slop audit and automatically applies fixes to detected issues.

## Workflow

### Step 1 — Run the audit

Execute the full anti-slop analysis workflow (Steps 1-5 from the `anti-slop` skill) on the provided file paths or globs. Read `../anti-slop/references/slop-code-patterns.md` for the pattern catalog.

Store the results internally — do NOT output the full report yet.

### Step 2 — Classify fixability

For each issue found, classify it:

- **Auto-fixable** — the fix is mechanical and safe:
  - Deleting unnecessary comments (Cat 1a, 1b, 1c, 1d, 1e)
  - Removing redundant else-after-return (Cat 3c)
  - Removing `=== true` / `=== false` comparisons (Cat 7b)
  - Removing unnecessary `async`/`await` on return (Cat 7c)
  - Removing unused imports (Cat 5a)
  - Removing unreachable code (Cat 5c)
  - Replacing ternary with `??` (Cat 7a)
  - Removing `return condition ? true : false` → `return condition` (Cat 7b)

- **Semi-auto** — likely safe but needs a sanity check:
  - Inlining single-use helper functions (Cat 2a)
  - Removing fallback values on non-nullable types (Cat 3e)
  - Shortening verbose error messages (Cat 3d)
  - Removing type assertions on already-typed values (Cat 6c)
  - Renaming "enhanced/optimized" variables (Cat 4a)

- **Manual only** — too risky to auto-fix, report these instead:
  - Fixing `as any` casts — requires understanding the correct type (Cat 6a)
  - Removing `@ts-ignore` — need to verify the fix compiles (Cat 6b)
  - Deleting exported-but-unused symbols — other repos may depend on them (Cat 5d)
  - Cross-file refactors (inlining across files)

### Step 3 — Apply auto-fixes

Process fixes **bottom-up within each file** (highest line number first) to preserve line numbers for subsequent edits.

For each auto-fixable issue:
1. Use the Edit tool to apply the fix
2. Record what was changed

Do NOT apply semi-auto fixes without telling the user. List them separately.

### Step 4 — Apply semi-auto fixes (with disclosure)

For each semi-auto issue:
1. Briefly state what will change and why
2. Apply the fix
3. If the fix is wrong or unclear, skip it and move it to "manual review"

### Step 5 — Output summary

```
## Anti-Slop Fix Report

**Files processed:** N
**Issues found:** N
**Auto-fixed:** N
**Semi-auto fixed:** N
**Manual review needed:** N

---

### Changes Applied

#### `path/to/file.ts`
- L12: Deleted comment restating code (`// set the name`)
- L45-52: Inlined `formatDate()` — was called once at L78
- L89: Replaced `isActive === true` with `isActive`

#### `path/to/other-file.ts`
- L3: Removed unused imports: `useCallback`, `useMemo`
- L67: Removed redundant `else` after `return`

---

### Manual Review Needed

| File | Line | Issue | Why manual |
|------|------|-------|------------|
| `api.ts` | 34 | `as any` cast | Need to determine correct response type |
| `types.ts` | 12 | `UserDTO` exported but unused | May be consumed by external packages |

---

### Verify

Run your linter and tests to confirm nothing broke:

\`\`\`bash
npm run lint && npm test
\`\`\`
```

If there were no issues to fix:
```
## Anti-Slop Fix Report

**Files processed:** N
**Issues found:** 0

Clean. Nothing to fix.
```
