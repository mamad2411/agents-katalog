---
name: new-page
description: Generate a typed Playwright Page Object following Autoframe conventions. Use when the user runs /new-page or asks for a Page Object for a URL, page, or feature.
---

# /new-page — Generate a Page Object

**Type:** Functional
**Description:** Generates a typed Playwright Page Object for a given URL or feature, following Autoframe's Page Object Model conventions exactly.

---

## Input Format

The user provides one of:
- A page URL (e.g. `https://app.com/login`)
- A feature name (e.g. `login`, `checkout`)
- A description of the page and its key elements

If the page has elements you cannot infer, ask up to 3 clarifying questions about the key elements and actions on the page.

## Output Format

A single Page Object file at `pages/[feature-name]/[PageName]Page.ts` that follows the POM pattern in CLAUDE.md:
- `expect` imported from `@playwright/test`
- All locators declared `readonly` and assigned in the constructor
- `goto()` navigation method
- Verb-named action methods
- `expect`-prefixed assertion methods

## Step-by-Step Instructions

1. Read the POM conventions in CLAUDE.md.
2. Determine the feature folder (kebab-case) and the class name (`PascalCase` + `Page`).
3. Identify the page's key elements. Prefer `getByRole`, `getByLabel`, `getByPlaceholder` — never CSS selectors or `page.$()` unless no semantic locator exists.
4. Write the file:
   - Import `Page`, `Locator`, `expect` from `@playwright/test`.
   - Declare `readonly page: Page` and one `readonly` Locator per element.
   - Assign all locators in the constructor.
   - Add `goto()`.
   - Add one verb-named action method per user action (one responsibility each).
   - Add `expect`-prefixed assertion methods for key states.
5. Save to `pages/[feature-name]/[PageName]Page.ts`.
6. Suggest running `/new-spec` next to generate tests for this page, and offer to create a fixture.

## Rules

- Locators only in the constructor, never inline in methods.
- One action per method; methods named as verbs.
- Assertions prefixed with `expect`.
- Semantic locators over CSS, always.
