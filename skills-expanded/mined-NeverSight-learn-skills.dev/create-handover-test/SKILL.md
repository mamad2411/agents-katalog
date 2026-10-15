---
name: create-handover-test
description: |
  Creates a ticket-driven handover test for a Playwright E2E test suite. Names the test with the ticket prefix, places it in the handover test directory, and follows the promotion lifecycle. Use when asked to write a handover test, ticket test, functional test, or test for a specific ticket number.
user-invocable: true
argument-hint: "[TICKET] [description]"
disable-model-invocation: true
---

# Create Handover Test

Generate a ticket-driven handover test that validates specific acceptance criteria.

---

## Workflow

1. **Parse the ticket key and description** from the user's request (e.g., `PROJ-456 bulk export`)
2. **Check if a POM exists** for the page under test in `e2e/poms/`
   - If yes, read it and add any new methods needed for this ticket's acceptance criteria
   - If no, create one first using the `create-pom` skill
3. **Check if test data exists** — create or update as needed
4. **Create the spec file** in `e2e/tests/handover/`
5. **Run the test** to verify it passes:
   ```bash
   npx playwright test --project="chromium:handover" {TICKET}-{description}.spec.ts
   ```

---

## Naming Convention

### Filename

```
{TICKET}-{short-description}.spec.ts
```

- `{TICKET}` — The ticket key exactly as it appears in the tracker (e.g., `PROJ-456`, `MANT-123`)
- `{short-description}` — Brief kebab-case summary (NOT the full ticket title)

Examples:
- `PROJ-456-bulk-export.spec.ts`
- `MANT-123-vault-bulk-delete.spec.ts`
- `FEAT-789-user-avatar-upload.spec.ts`

### `test.describe` Block

The outer `test.describe` **must** include the ticket key for traceability:

```typescript
test.describe('PROJ-456: Bulk Export', () => {
```

---

## Spec Structure

```typescript
import { test } from '../../fixtures/base';
import { getAuthFilePath } from '../../helpers/env-config';
import { FeaturePage } from '../../poms/feature.page';

const authFile = getAuthFilePath();

test.describe('PROJ-456: Bulk Export', () => {
    test.beforeAll(async ({ browser }) => {
        const context = await browser.newContext({
            storageState: authFile,
        });
        const page = await context.newPage();
        const pom = new FeaturePage(page);
        await pom.setUp();
        await page.close();
        await context.close();
    });

    test('should export selected items as CSV', async ({ page, testData }) => {
        const pom = new FeaturePage(page);
        const items = testData.feature.items;

        await pom.navigateToPage();
        // ... validate acceptance criteria from ticket
    });

    test('should show error when no items selected', async ({ page }) => {
        const pom = new FeaturePage(page);

        await pom.navigateToPage();
        // ... validate error handling criteria
    });
});
```

See [references/handover-spec-template.md](references/handover-spec-template.md) for the full template.

---

## POM Rules

Handover tests follow **all** the same POM rules as regression/smoke tests:

- **Use the existing POM** for the page under test
- If the ticket requires new interactions, **add methods to the existing POM** — do NOT create a second POM for the same page
- Only create a **new POM** if the ticket introduces an entirely new page
- All new POM methods must have full JSDoc with Steps and @param tags

---

## All Standard Rules Apply

- Import `test` from custom fixtures, not from `@playwright/test`
- No raw `page` calls in specs — all interaction through POMs
- Every test is independent — creates its own data, navigates independently
- No hardcoded test data — use external JSON via the testData fixture
- beforeAll uses manual browser context with storageState for cleanup

---

## Promotion Lifecycle

Handover tests are **temporary by design**. After the ticket is Done:

| Action | When |
| ------ | ---- |
| **Promote to regression** | Feature is permanent, should run on every build |
| **Promote to smoke** | Feature is on the critical path |
| **Delete** | Already covered by existing tests, or feature was reverted |

Use the `promote-handover-test` skill when ready to promote.

### Staleness Policy

- Review `tests/handover/` after every sprint/release
- Any spec whose ticket is Done/Closed should be promoted or deleted
- Never leave handover tests running indefinitely

---

## File Checklist

- [ ] `e2e/poms/{feature}.page.ts` — POM updated with new methods (or new POM created)
- [ ] `e2e/test-data/{feature}.json` — Test data (created or updated)
- [ ] `e2e/tests/handover/{TICKET}-{description}.spec.ts` — Spec file
- [ ] Filename includes ticket key prefix
- [ ] `test.describe` includes ticket key
- [ ] All POM methods have JSDoc
- [ ] Tests pass: `npx playwright test --project="chromium:handover" {TICKET}-{description}.spec.ts`
