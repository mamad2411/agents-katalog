---
name: write-vitest-playwright-tests
description: >-
  Load this skill when writing Vitest, Testing Library, MSW, or Playwright tests for a web
  frontend. Auto-load when a .test.ts, .test.tsx, or .spec.ts file is created or modified.
disable-model-invocation: false
user-invocable: false
paths:
  - "**/*.test.{ts,tsx}"
  - "**/*.spec.{ts,tsx}"
  - "**/e2e/**"
  - "**/playwright.config.ts"
  - "**/mocks/**"
compatibility: >-
  Requires `bun` on PATH (or Node.js 20+) and network access on first install. Vitest, Testing
  Library, and MSW are project dev dependencies, not global installs. Playwright additionally
  needs its browser binaries, downloaded once by `bunx playwright install` - E2E tests will not
  run without them.
license: Apache-2.0
---

# Write Vitest and Playwright Tests

Frameworks: **Vitest** (unit + component), **Testing Library** (`@testing-library/svelte` or `@testing-library/react`), **MSW** (API mocking), **Playwright** (E2E)

> The examples below use Vitest APIs. If the project already uses Jest or Mocha instead, adapt the equivalent calls and match the runner in the repo — the `ceh-web-frontend:vitest-unit-tester` agent detects which one applies.

| Folder             | Contents                                           |
| ------------------ | -------------------------------------------------- |
| `tests/unit/`      | Pure function tests — no DOM, no fetch             |
| `tests/component/` | Component render and interaction tests             |
| `tests/e2e/`       | Full browser tests against the running application |

Naming: `<subject>.test.ts` for unit/component, `<scenario>.spec.ts` for E2E. One behavior per test.

Write each test at the lowest tier that can show the behavior. Done when each test asserts one
behavior and nothing reaches the real network outside E2E.

## Procedure

1. Choose the inputs and scenarios first (see Hands off to).
2. Put each test in `tests/unit/`, `tests/component/`, or `tests/e2e/` by what it needs.
3. Intercept the network with MSW, never by mocking `fetch`.
4. Run coverage and read the untested regions. Never add a test just to reach the floor.

## Rules

### Unit tests: no DOM, no network

```ts
import { describe, it, expect } from "vitest";
import { summarizeItems } from "$lib/items/summary";

describe("summarizeItems", () => {
  it("counts each open item", () => {
    const state = buildTestState({ items: [mockOpenItem()] });
    expect(summarizeItems(state).open).toBe(1);
  });
});
```

### Component tests: test what the user sees

Use `@testing-library/svelte` (SvelteKit) or `@testing-library/react` (React). Do not test implementation details. No snapshot tests — explicit assertions only, because a snapshot breaks on any markup change and gets re-approved unread.

```ts
import { render, screen } from "@testing-library/svelte";
import ItemPanel from "$lib/components/ItemPanel.svelte";

it("renders open items", () => {
  render(ItemPanel, {
    props: { state: buildTestState({ items: [mockOpenItem()] }) },
  });
  expect(screen.getByRole("status", { name: /open/i })).toBeInTheDocument();
});
```

The React form differs only in the render call, `render(<ItemPanel state={buildTestState({ items: [mockOpenItem()] })} />)`, imported from `@testing-library/react`. The queries and assertions are the same.

### API mocking with MSW: do not mock `fetch` directly

MSW intercepts at the network layer, so the real client code (URL, headers, parsing, errors) still
runs under test.

```ts
import { setupServer } from "msw/node";
import { http, HttpResponse } from "msw";

const server = setupServer(
  http.post("/sessions/:id/message", () =>
    HttpResponse.json({ message: "...", items: [] }),
  ),
);

beforeAll(() => server.listen({ onUnhandledRequest: "error" }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

### E2E with Playwright: critical paths only

```ts
import { test, expect } from "@playwright/test";

test("user can start a session and see the item list", async ({ page }) => {
  await page.goto("/");
  await page.fill('[data-testid="topic-input"]', "Weekly planning");
  await page.click('[data-testid="start-session"]');
  await expect(page.locator('[data-testid="item-panel"]')).toBeVisible();
});
```

Do not duplicate unit or component test coverage in E2E tests.

### Coverage floor

70% for `src/lib/`. A floor for finding blind spots, not a goal. Below it, look for the untested
regions. Reaching it proves nothing and is never a reason to add tests.

## Hands off to

This skill covers the **tooling** — runner, fixtures, mocking, coverage. It does not decide
_which_ inputs and cases a test should cover. Before writing the cases:

- Invoke the Skill tool with skill="ceh-testing:design-test-cases" to choose them. It supplies
  equivalence partitions, boundary values, decision tables, pairwise combinations, properties, and
  metamorphic relations — stack-agnostic technique that the sections above assume has already been
  applied.
