---
name: promote-handover-test
description: |
  Promotes a handover test to the regression or smoke test suite. Renames the file to remove the ticket prefix, moves it to the target directory, and updates the test.describe block. Use when asked to promote, graduate, or move a handover test to regression or smoke.
user-invocable: true
argument-hint: "[TICKET or file-path]"
disable-model-invocation: true
---

# Promote Handover Test

Move a completed handover test from `tests/handover/` to `tests/regression/` or `tests/smoke/`.

---

## Workflow

1. **Locate the handover test** — search `e2e/tests/handover/` for the ticket key or file path
2. **Determine the target suite** — regression (default) or smoke (if user specifies)
3. **Check for an existing spec** in the target directory for the same feature
   - If one exists, merge the tests into the existing `test.describe` block
   - If not, create a new spec file
4. **Apply the promotion changes** (see checklist below)
5. **Delete the original handover spec** from `tests/handover/`
6. **Run the test** in its new location:
   ```bash
   npx playwright test --project="chromium:regression" {feature}.spec.ts
   ```

---

## Promotion Checklist

### 1. Rename the File

Remove the ticket key prefix:

```
BEFORE: e2e/tests/handover/PROJ-456-bulk-export.spec.ts
AFTER:  e2e/tests/regression/bulk-export.spec.ts
```

If the feature already has a regression spec (e.g., `vault.spec.ts`), merge the tests into that file instead of creating a new one.

### 2. Update `test.describe`

Remove the ticket key from the describe block:

```typescript
// BEFORE
test.describe('PROJ-456: Bulk Export', () => {

// AFTER
test.describe('Bulk Export', () => {
```

If merging into an existing spec, add the tests inside the existing `test.describe` block (or create a nested `test.describe` if the feature area is distinct).

### 3. Verify POM JSDoc

Ensure all POM methods added for this ticket have complete JSDoc:
- Summary line
- Steps block (numbered)
- @param tags for all parameters

### 4. Run Tests

Verify the tests pass in their new location:

```bash
# For regression
npx playwright test --project="chromium:regression" {feature}.spec.ts

# For smoke
npx playwright test --project="chromium:smoke" {feature}.spec.ts

# Across all browsers
npx playwright test --project="*:regression" {feature}.spec.ts
```

### 5. Delete the Original

Remove the handover spec from `tests/handover/` after confirming the promoted version passes.

---

## Decision: Promote, Merge, or Delete?

| Scenario | Action |
| -------- | ------ |
| Feature is permanent, no existing regression spec | Promote to `tests/regression/{feature}.spec.ts` |
| Feature is permanent, regression spec already exists | Merge tests into the existing regression spec |
| Feature is on the critical path | Promote to `tests/smoke/{feature}.spec.ts` |
| Feature is fully covered by existing tests | Delete the handover spec |
| Feature was reverted | Delete the handover spec |

---

## Example: Full Promotion

### Before (handover)

File: `e2e/tests/handover/MANT-123-vault-bulk-delete.spec.ts`

```typescript
import { test } from '../../fixtures/base';
import { getAuthFilePath } from '../../helpers/env-config';
import { VaultPage } from '../../poms/vault.page';

const authFile = getAuthFilePath();

test.describe('MANT-123: Vault Bulk Delete', () => {
    test.beforeAll(async ({ browser }) => {
        const context = await browser.newContext({
            storageState: authFile,
        });
        const page = await context.newPage();
        const vault = new VaultPage(page);
        await vault.setUp();
        await page.close();
        await context.close();
    });

    test('should select and delete multiple items', async ({ page, testData }) => {
        // ...
    });
});
```

### After (regression)

File: `e2e/tests/regression/vault.spec.ts` (merged into existing spec, or new file)

```typescript
import { test } from '../../fixtures/base';
import { getAuthFilePath } from '../../helpers/env-config';
import { VaultPage } from '../../poms/vault.page';

const authFile = getAuthFilePath();

test.describe('Vault Tests', () => {
    test.beforeAll(async ({ browser }) => {
        const context = await browser.newContext({
            storageState: authFile,
        });
        const page = await context.newPage();
        const vault = new VaultPage(page);
        await vault.setUp();
        await page.close();
        await context.close();
    });

    // ... existing tests ...

    test('should select and delete multiple items', async ({ page, testData }) => {
        // ... (promoted from MANT-123)
    });
});
```

Original file `e2e/tests/handover/MANT-123-vault-bulk-delete.spec.ts` is deleted.
