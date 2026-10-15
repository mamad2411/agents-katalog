---
name: fp-audit
description: Analyze the gap between E2E specifications and existing test implementations
---

# Audit E2E Test Coverage

Analyze the gap between E2E specifications and existing test implementations. This is a read-only command — it reports findings but does not modify any files.

Additional instructions from the user: "$ARGUMENTS". Ignore if empty.

## Phase 1: Discover

1. Find all `E2E_TESTS.md` files by searching recursively from the project root.
2. Read the root-level spec first (`docs/E2E_TESTS.md` or `E2E_TESTS.md`) to understand project-wide testing constraints.
3. Read each package-level `E2E_TESTS.md` and extract:
   - All suites (H2 headings)
   - All features within each suite (H4 headings)
   - Category metadata (`<!-- category: ... -->`)
   - Skip metadata (`<!-- skip: ... -->`)
4. Find all existing E2E test files:
   - Files matching `**/*.e2e.test.*`
   - Files inside `**/e2e/**/*.test.*`
5. Read existing test files and extract:
   - Suite/group blocks — the framework's grouping construct (e.g., `describe()` in vitest/jest, `mod tests` in Rust, `class` in pytest) — map to suites
   - Individual test cases — the framework's test declaration (e.g., `it()` / `test()` in vitest/jest, `#[test]` in Rust, `def test_` in pytest) — map to features
   - Skip/conditional-skip markers — the framework's mechanism for skipping tests (e.g., `skip` / `skipIf` in vitest/jest, `#[ignore]` in Rust, `@pytest.mark.skip` in pytest)

## Phase 2: Map

Build a coverage matrix:

| Spec Suite    | Spec Feature          | Category | Test File        | Test Case           | Status  |
|---------------|-----------------------|----------|------------------|---------------------|---------|
| Task Creation | Create basic task     | core     | task.e2e.test.ts | "Create basic task" | Covered |
| Task Creation | Create with long name | edge     | —                | —                   | Missing |
| Push          | Push to remote        | core     | push.e2e.test.ts | "push to remote"    | Covered |

For each spec feature, determine:
- **Covered**: A corresponding test case exists and its assertions match the spec
- **Missing**: No corresponding test case
- **Stale**: Test exists but assertions don't match current spec
- **Skipped**: Test exists with a skip marker (expected for `<!-- skip: ... -->` features)

## Phase 3: Report

Present findings in this format:

```
E2E Test Coverage Audit
========================

Specs found: N files
Test files found: N files

Overall coverage: X/Y features (Z%)

By category:
  core:        X/Y (Z%)
  edge:        X/Y (Z%)
  error:       X/Y (Z%)
  side-effect: X/Y (Z%)
  idempotency: X/Y (Z%)

Gaps by suite:
  ## Task Creation (3/5 features covered)
    MISSING  [edge]        Create with very long name
    MISSING  [idempotency] Re-create after deletion

  ## Push (4/4 features covered)
    (fully covered)

Stale tests:
  push.e2e.test.ts: "push with pending changes"
    Spec says: Exits with non-zero code
    Test asserts: Exits with code 0

Structural issues:
  - task.e2e.test.ts: Tests share mutable state at suite level
  - init.e2e.test.ts: Missing afterEach cleanup for env.HOME
```

Do NOT suggest fixes or modifications. This command is purely diagnostic.
