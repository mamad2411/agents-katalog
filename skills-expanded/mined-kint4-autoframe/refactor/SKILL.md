---
name: refactor
description: Restructure messy Playwright tests to follow Autoframe conventions, extracting Page Objects and fixtures. Use when the user runs /refactor or asks to clean up existing tests.
---

# /refactor — Refactor to Autoframe Conventions

**Type:** Maintenance
**Description:** Takes existing, messy Playwright tests and restructures them to follow Autoframe conventions — extracting Page Objects, applying AAA, grouping tests, and replacing brittle selectors.

---

## Input Format

- A path to an existing spec or test file (or a pasted snippet)
- Optionally, a target feature name

## Output Format

The refactored file(s) following Autoframe conventions, plus a short changelog of what was changed and why. May produce a new Page Object and/or fixture as part of the refactor.

## Step-by-Step Instructions

1. Read the target file and any related Page Objects/fixtures.
2. Read the POM, spec, and fixture conventions in CLAUDE.md.
3. Diagnose convention violations:
   - Raw locators / `page.$()` / CSS selectors in tests → extract into a Page Object using semantic locators.
   - Inline locators in Page Object methods → move to the constructor.
   - Missing AAA structure → add Arrange / Act / Assert.
   - Ungrouped tests → wrap in Happy Path / Negative / Edge `describe` blocks.
   - Technical test names → rewrite in plain language.
   - Raw `page` where a fixture exists → switch to the custom fixture.
4. Apply the refactor incrementally, preserving the original test intent and assertions.
5. Extract a Page Object and fixture if the logic belongs there.
6. Save files to their correct locations per the folder structure.
7. Output a changelog: what moved, what was renamed, what was replaced.

## Rules

- Preserve test behavior — never silently drop assertions.
- Preserving scope may leave Negative/Edge `describe` groups empty — do not invent
  coverage the original didn't have. Instead, note the gap in the changelog and hand
  off to `/new-spec` to fill it.
- Never introduce `waitForTimeout` or CSS selectors during a refactor.
- Place all new files in their conventional locations.
