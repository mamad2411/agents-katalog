---
name: new-spec
description: Generate an E2E spec file with happy path, negative, and edge cases pre-written. Use when the user runs /new-spec or asks for tests for a feature or page.
---

# /new-spec — Generate a Spec File

**Type:** Functional
**Description:** Generates a Playwright spec file for a given feature or Page Object, with happy path, negative, and edge cases pre-written following Autoframe conventions.

---

## Input Format

The user provides one of:
- A feature name (e.g. `login`)
- An existing Page Object to test
- A short description of the user flow

## Output Format

A spec file at `tests/e2e/[feature-name]/[feature].spec.ts` that follows the spec conventions in CLAUDE.md:
- Imports from the matching custom fixture when one exists; otherwise raw `page` with a `TODO: create fixture` comment
- `test.describe` grouping: Happy Path, Negative Cases, Edge Cases
- Arrange / Act / Assert comments in every test
- Test names written in plain language

## Step-by-Step Instructions

1. Read the spec conventions in CLAUDE.md.
2. Locate the relevant Page Object under `pages/[feature-name]/`. If none exists, recommend `/new-page` first.
3. Check `fixtures/` for a matching fixture. Use it if present; otherwise fall back to raw `page` and add the `TODO` comment.
4. Write the spec:
   - `test.describe('[Feature Name]')` as the outer block.
   - `beforeEach` for setup (navigate / reset state), `afterEach` for cleanup if needed.
   - If Negative or Edge cases need *different* setup than the Happy Path (e.g. an
     unauthenticated-access test must skip the login that other tests need), put the
     `beforeEach` inside each inner `describe` block instead of at the top level.
   - Inner `test.describe` blocks for Happy Path, Negative Cases, Edge Cases.
   - At least one meaningful test per group; never leave a group empty.
   - Arrange / Act / Assert comments in each test body.
   - Plain-language test names a non-technical person can read.
5. Save to `tests/e2e/[feature-name]/[feature].spec.ts`.
6. Suggest `/review-spec` to validate assertion quality.

## Rules

- No logic inside `test.describe` blocks — only inside `test` blocks.
- Always use Arrange / Act / Assert.
- Prefer custom fixtures over raw `page` whenever a fixture exists.
- Drive the page through Page Object methods, not raw locators in the spec.
