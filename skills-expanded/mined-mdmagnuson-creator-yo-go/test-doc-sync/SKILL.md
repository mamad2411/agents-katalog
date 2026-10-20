---
name: test-doc-sync
description: "Test documentation synchronization workflow. Use before committing behavior changes to ensure test comments/docstrings stay current. Triggers on: pre-commit, behavior changes, renamed functions, test documentation."
---

# Test Documentation Sync

> Load this skill when: committing behavior changes to ensure test comments and docstrings stay current.

> ⛔ **CRITICAL: Run test doc sync before EVERY commit that includes behavior changes.**
>
> **Trigger:** After implementation complete, before `git add`/`git commit`.
>
> **Failure behavior:** If stale test references remain after the sync process, do NOT commit. Fix the references first.

---

## Why This Exists

When code changes (renamed functions, changed behavior, updated strings), test comments and docstrings often become stale. This leaves misleading documentation that confuses future developers. Test doc sync catches and fixes these before they're committed.

---

## Step 1: Extract Keywords from Diff

Run `git diff --cached` (or `git diff` if not yet staged) and extract:

| Source | Keywords |
|--------|----------|
| Removed/renamed function names | `showQRCode`, `handlePayment` |
| Removed/renamed variable names | `isLoading`, `userData` |
| Changed string literals | `"Submit"`, `"Processing..."` |
| Removed/modified comments | `// handles QR display` |
| Removed class/type names | `PaymentForm`, `UserProfile` |

---

## Step 2: Semantic Expansion

Expand each keyword to catch variations:

| Original | Expanded to search |
|----------|-------------------|
| `showQRCode` | `showQRCode`, `QR code`, `QR-code`, `qrcode`, `QRCode` |
| `handlePayment` | `handlePayment`, `payment handler`, `payment handling` |
| `isLoading` | `isLoading`, `loading state`, `is loading` |

---

## Step 3: Search Test Files

```bash
# Search for stale references in test files
grep -rn "<keywords>" tests/ e2e/ --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" | grep -v node_modules
```

**Scope restrictions:**
- ✅ Search in: `tests/`, `e2e/`, `__tests__/`, `*.test.*`, `*.spec.*`
- ❌ Never search: `node_modules/`, `dist/`, `build/`, `.next/`
- ❌ Never modify files outside test directories

---

## Step 4: Handle Matches

| Match Count | Action |
|-------------|--------|
| 0 matches | Proceed to commit (no stale references) |
| 1-5 matches | Auto-update comments/docstrings, show changes |
| 6-15 matches | Show matches, ask user to confirm updates |
| 16+ matches | Narrow search (too broad), ask user to specify scope |

**Prioritization:** Files already touched in this change are updated first.

### Auto-update Behavior (1-5 matches)

1. Read each file with a match
2. Update the comment/docstring to reflect new behavior
3. Show the user what was changed
4. Include updated test files in the commit

**Example update:**
```typescript
// Before (stale)
/**
 * Tests the showQRCode function displays a QR code
 */

// After (updated)
/**
 * Tests the displayQRImage function renders a QR image
 */
```

---

## Step 5: Verification Grep

Before committing, verify no stale references remain:

```bash
# Final check - should return 0 matches
grep -rn "<original-keywords>" tests/ e2e/ --include="*.ts" --include="*.tsx" | grep -v node_modules | wc -l
```

If matches remain, either:
- Fix the remaining references
- Add to `docs/test-debt.json` with justification (explicit skip)

---

## When to Skip (Explicit Only)

Skip test doc sync ONLY when:
- Changes are purely infrastructure (CI, build config)
- Changes are documentation-only (README, CHANGELOG)
- User explicitly requests skip with justification

**Log skips to `docs/test-debt.json`:**
```json
{
  "testDocSkips": [{
    "commit": "abc123",
    "reason": "Infrastructure change only",
    "skippedAt": "2026-03-03T10:30:00Z"
  }]
}
```

---

## Integration with Developer

Developer agent handles the actual test doc sync. Builder ensures:
1. Developer runs sync before commit
2. Sync results are reported
3. Remaining stale references block commit
