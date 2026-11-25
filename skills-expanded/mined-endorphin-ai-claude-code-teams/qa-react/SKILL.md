---
name: qa-react
description: "React testing skill with React Testing Library, Vitest, MSW, and Playwright. Use when writing or running React frontend tests."
---

# QA React

## Purpose

This skill equips the `tester-react` agent with everything needed to write, run, and maintain React frontend tests in a fullstack Golang + React codebase. It covers unit tests for components and hooks, integration tests for pages, API mocking with MSW, accessibility checks, and optional E2E flows with Playwright. The guiding philosophy: **test what the user experiences, not how the code is wired**.

## Core Testing Stack

| Tool | Role | Version Guidance |
|------|------|------------------|
| **Vitest** | Test runner | Vite-compatible, ESM-native, fast HMR-aware |
| **React Testing Library (RTL)** | Component rendering + queries | `@testing-library/react` |
| **user-event** | Realistic user interaction simulation | `@testing-library/user-event` v14+ |
| **MSW** | Network-level API mocking | `msw` v2+ — intercepts fetch/axios at Service Worker level |
| **jest-axe** | Automated accessibility assertions | `jest-axe` via `toHaveNoViolations` |
| **Playwright** | E2E browser tests (optional) | For critical user flows only |
| **@testing-library/react-hooks** | Hook testing (legacy) | Prefer `renderHook` from `@testing-library/react` v14+ |

## RTL Philosophy: Test Behavior, Not Implementation

The single most important principle: **tests should resemble how users interact with your app**. If a test breaks because you renamed an internal state variable but the UI behavior didn't change, the test is wrong.

### Forbidden Patterns
- **Never** query by CSS class name, tag name, or component internal state
- **Never** assert on `useState` / `useReducer` values directly
- **Never** use `container.querySelector` unless absolutely no RTL query works
- **Never** test implementation details (internal function calls, hook return values in isolation without rendering)
- **Never** use `act()` directly when RTL's `waitFor` / `findBy` handles it

### Encouraged Patterns
- Query by accessible role, label, placeholder, text — what the user sees
- Simulate real user actions (click, type, tab) with `userEvent`
- Assert on visible output: text content, element presence/absence, ARIA attributes
- Use `waitFor` and `findBy*` for async state transitions

## RTL Query Priority (strict order)

Use the highest-priority query that works for your case:

1. **`getByRole`** — Accessible role + name. Best for buttons, headings, links, form controls. Example: `getByRole('button', { name: /submit/i })`
2. **`getByLabelText`** — Form fields with associated `<label>`. Example: `getByLabelText(/email address/i)`
3. **`getByPlaceholderText`** — When label is absent (not ideal, but acceptable). Example: `getByPlaceholderText(/search/i)`
4. **`getByText`** — Visible text content. Example: `getByText(/welcome back/i)`
5. **`getByDisplayValue`** — Current value of input/textarea/select.
6. **`getByAltText`** — Images with alt text.
7. **`getByTitle`** — Elements with title attribute.
8. **`getByTestId`** — **Last resort only**. Use `data-testid` when no semantic query works. Example: `getByTestId('chart-container')`

### Query Variants

| Need | Prefix | Throws on miss? | Async? |
|------|--------|-----------------|--------|
| Element must exist | `getBy` | Yes | No |
| Element must NOT exist | `queryBy` | No (returns null) | No |
| Element will appear (async) | `findBy` | Yes (waits) | Yes |
| Multiple elements | `getAllBy` / `queryAllBy` / `findAllBy` | Respective behavior | Respective |

## User Event Simulation

Always use `@testing-library/user-event` over `fireEvent`. It simulates complete user interaction sequences (focus, keydown, keypress, keyup, input, change) rather than dispatching isolated synthetic events.

```typescript
import userEvent from '@testing-library/user-event';

// Setup — create a user instance per test
const user = userEvent.setup();

// Click
await user.click(screen.getByRole('button', { name: /save/i }));

// Type into input
await user.type(screen.getByLabelText(/username/i), 'john_doe');

// Clear and retype
await user.clear(screen.getByLabelText(/email/i));
await user.type(screen.getByLabelText(/email/i), 'new@email.com');

// Select option
await user.selectOptions(screen.getByRole('combobox', { name: /country/i }), 'US');

// Keyboard
await user.keyboard('{Enter}');
await user.tab();

// Upload file
const file = new File(['content'], 'doc.pdf', { type: 'application/pdf' });
await user.upload(screen.getByLabelText(/upload/i), file);
```

## Async Testing

### `waitFor` — poll until assertion passes
```typescript
await waitFor(() => {
  expect(screen.getByText(/data loaded/i)).toBeInTheDocument();
});
```

### `findBy` — shorthand for waitFor + getBy
```typescript
const heading = await screen.findByRole('heading', { name: /dashboard/i });
expect(heading).toBeInTheDocument();
```

### `waitForElementToBeRemoved` — wait for loading spinners to disappear
```typescript
await waitForElementToBeRemoved(() => screen.queryByText(/loading/i));
```

### Rules
- Default timeout is 1000ms. Increase for slow operations: `waitFor(() => ..., { timeout: 3000 })`
- Never use `setTimeout` or manual delays in tests
- If a `findBy` query is sufficient, prefer it over `waitFor` + `getBy`

## MSW (Mock Service Worker) — API Mocking

MSW intercepts HTTP requests at the network level. Tests hit the same fetch/axios calls as production — no mocking of modules.

### Server Setup (`src/test/setup.ts`)

```typescript
import { setupServer } from 'msw/node';
import { http, HttpResponse } from 'msw';

// Default handlers — shared across all tests
export const handlers = [
  http.get('/api/v1/user/me', () => {
    return HttpResponse.json({ id: 1, name: 'Test User', email: 'test@example.com' });
  }),
  http.get('/api/v1/health', () => {
    return HttpResponse.json({ status: 'ok' });
  }),
];

export const server = setupServer(...handlers);

// Vitest global setup
beforeAll(() => server.listen({ onUnhandledRequest: 'warn' }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

### Per-Test Handler Overrides

```typescript
import { server } from '@/test/setup';
import { http, HttpResponse } from 'msw';

test('shows error when API fails', async () => {
  server.use(
    http.get('/api/v1/user/me', () => {
      return HttpResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }),
  );

  render(<ProfilePage />);
  expect(await screen.findByText(/unauthorized/i)).toBeInTheDocument();
});
```

### MSW Handler Patterns

| Scenario | Pattern |
|----------|---------|
| Success response | `HttpResponse.json(data, { status: 200 })` |
| Error response | `HttpResponse.json({ error: msg }, { status: 4xx/5xx })` |
| Empty response | `HttpResponse.json(null, { status: 204 })` |
| Network error | `HttpResponse.error()` |
| Delayed response | `await delay(ms)` before returning |
| Request body validation | Read `await request.json()` and assert / branch |
| Paginated list | Read URL search params, return sliced data |

### MSW Convention
- Place default handlers in `src/test/handlers/` organized by API domain (e.g., `user.ts`, `projects.ts`, `auth.ts`)
- Export each handler array, compose into `server` in `setup.ts`
- Override in individual tests only for error/edge cases

## Component Testing Pattern

```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { LoginForm } from './LoginForm';

describe('LoginForm', () => {
  const user = userEvent.setup();
  const mockOnSubmit = vi.fn();

  beforeEach(() => {
    mockOnSubmit.mockClear();
  });

  it('renders email and password fields', () => {
    render(<LoginForm onSubmit={mockOnSubmit} />);

    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /sign in/i })).toBeInTheDocument();
  });

  it('calls onSubmit with credentials when form is filled and submitted', async () => {
    render(<LoginForm onSubmit={mockOnSubmit} />);

    await user.type(screen.getByLabelText(/email/i), 'user@test.com');
    await user.type(screen.getByLabelText(/password/i), 'secret123');
    await user.click(screen.getByRole('button', { name: /sign in/i }));

    expect(mockOnSubmit).toHaveBeenCalledWith({
      email: 'user@test.com',
      password: 'secret123',
    });
  });

  it('shows validation error when email is empty', async () => {
    render(<LoginForm onSubmit={mockOnSubmit} />);

    await user.click(screen.getByRole('button', { name: /sign in/i }));

    expect(await screen.findByText(/email is required/i)).toBeInTheDocument();
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });
});
```

## Hook Testing Pattern

Use `renderHook` from `@testing-library/react` (not the deprecated `@testing-library/react-hooks` package).

```typescript
import { renderHook, waitFor } from '@testing-library/react';
import { useCounter } from './useCounter';

describe('useCounter', () => {
  it('starts with initial value', () => {
    const { result } = renderHook(() => useCounter(5));
    expect(result.current.count).toBe(5);
  });

  it('increments count', () => {
    const { result } = renderHook(() => useCounter(0));
    act(() => result.current.increment());
    expect(result.current.count).toBe(1);
  });
});
```

### Hooks that need providers (React Query, Router, etc.)
```typescript
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

function createWrapper() {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
}

it('fetches user data', async () => {
  const { result } = renderHook(() => useUser(1), { wrapper: createWrapper() });

  await waitFor(() => expect(result.current.isSuccess).toBe(true));
  expect(result.current.data?.name).toBe('Test User');
});
```

## Page / Integration Testing Pattern

Page tests render a full page component with router context, mocked API, and all providers.

```typescript
import { render, screen } from '@/test/test-utils'; // custom render with providers
import { DashboardPage } from './DashboardPage';

describe('DashboardPage', () => {
  it('loads and displays project list', async () => {
    render(<DashboardPage />);

    // Wait for loading to complete
    await waitForElementToBeRemoved(() => screen.queryByText(/loading/i));

    // Assert data is rendered
    expect(screen.getByRole('heading', { name: /my projects/i })).toBeInTheDocument();
    expect(screen.getAllByRole('listitem')).toHaveLength(3);
  });

  it('navigates to project detail when clicked', async () => {
    render(<DashboardPage />);

    await waitForElementToBeRemoved(() => screen.queryByText(/loading/i));
    await user.click(screen.getByText(/project alpha/i));

    expect(await screen.findByRole('heading', { name: /project alpha/i })).toBeInTheDocument();
  });
});
```

### Custom Render (`src/test/test-utils.tsx`)

```typescript
import { render, RenderOptions } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

function AllProviders({ children }: { children: React.ReactNode }) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });

  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>{children}</BrowserRouter>
    </QueryClientProvider>
  );
}

const customRender = (ui: React.ReactElement, options?: Omit<RenderOptions, 'wrapper'>) =>
  render(ui, { wrapper: AllProviders, ...options });

export * from '@testing-library/react';
export { customRender as render };
```

## Snapshot Testing

Use snapshots **sparingly** and only for stable, presentational UI that changes rarely.

```typescript
it('matches snapshot for static footer', () => {
  const { container } = render(<Footer />);
  expect(container.firstChild).toMatchSnapshot();
});
```

### Snapshot Rules
- Never snapshot components with dynamic data (dates, IDs, random values)
- Never snapshot entire pages
- Prefer inline snapshots (`toMatchInlineSnapshot`) for small outputs
- When a snapshot update is needed, review the diff carefully before accepting with `--update`
- If a snapshot breaks frequently, replace it with explicit assertions

## Accessibility Testing

```typescript
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

it('has no accessibility violations', async () => {
  const { container } = render(<LoginForm onSubmit={vi.fn()} />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

### Accessibility Checks to Include
- Run `jest-axe` on every form component and every page-level component
- Verify focus management after modal open/close
- Verify keyboard navigation for custom interactive elements
- Check ARIA labels on icon-only buttons

## Coverage Targets

| Category | Target | Rationale |
|----------|--------|-----------|
| Business logic hooks (`use*`) | **80%+** | Core logic, high ROI |
| Form components | **80%+** | User input paths must be solid |
| Page components | **70%+** | Integration coverage, some paths are hard to reach |
| Presentational/layout components | **50%+** | Low logic, snapshot may suffice |
| Utility functions | **90%+** | Pure functions, easy to test exhaustively |
| E2E critical paths | **100% of defined flows** | If you write an E2E test, it must pass |

Run coverage: `npx vitest run --coverage`

## Playwright E2E (Optional — Critical Flows Only)

Use Playwright only for high-value end-to-end user flows that cannot be adequately tested with RTL + MSW. Examples: login flow, checkout, multi-step wizard.

```typescript
import { test, expect } from '@playwright/test';

test('user can log in and see dashboard', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel(/email/i).fill('user@test.com');
  await page.getByLabel(/password/i).fill('password123');
  await page.getByRole('button', { name: /sign in/i }).click();

  await expect(page.getByRole('heading', { name: /dashboard/i })).toBeVisible();
});
```

### Playwright Rules
- E2E tests live in `e2e/` at project root, not alongside components
- E2E tests run against a real dev server (or preview build), not mocked APIs
- Keep E2E suite small: 10-20 critical flows max
- Tag with `@critical` for CI gating

## Test Setup File (`src/test/setup.ts`)

This file is loaded by Vitest before every test file. It configures:

1. **MSW server** — starts, resets between tests, closes after suite
2. **jest-dom matchers** — extends `expect` with `.toBeInTheDocument()`, `.toHaveTextContent()`, etc.
3. **jest-axe matchers** — extends `expect` with `.toHaveNoViolations()`
4. **Global cleanup** — ensures no leaked state between tests

```typescript
import '@testing-library/jest-dom/vitest';
import { server } from './handlers';

beforeAll(() => server.listen({ onUnhandledRequest: 'warn' }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

Referenced in `vitest.config.ts`:
```typescript
export default defineConfig({
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    globals: true,
    css: false,
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      include: ['src/**/*.{ts,tsx}'],
      exclude: ['src/test/**', 'src/**/*.d.ts', 'src/main.tsx'],
    },
  },
});
```

## File Conventions

| Convention | Rule |
|-----------|------|
| Test file location | Same directory as source: `Button.tsx` -> `Button.test.tsx` |
| Test file naming | `ComponentName.test.tsx` for components, `useHook.test.ts` for hooks |
| Test utility location | `src/test/test-utils.tsx` for custom render, `src/test/handlers/` for MSW handlers |
| E2E test location | `e2e/` at project root |
| Describe blocks | `describe('ComponentName', () => { ... })` — one per file, named after component |
| Test names | Start with verb describing user action or state: "renders...", "shows...", "calls...", "navigates..." |

## Conventions

1. **One test file per source file** — never combine tests for multiple components
2. **Arrange-Act-Assert** — every test follows this structure clearly
3. **No test interdependence** — each test must work in isolation; no shared mutable state
4. **Mock at the network level** — use MSW, not `vi.mock()` for API calls. Reserve `vi.mock()` for non-HTTP dependencies (e.g., `window.matchMedia`, `IntersectionObserver`)
5. **Descriptive test names** — a failing test name should tell you what broke without reading the test body
6. **No magic numbers** — use named constants or factory functions for test data
7. **Test data factories** — create helper functions for generating test objects with sensible defaults
8. **Clean up** — if a test modifies global state (localStorage, cookies), restore it in `afterEach`

## Knowledge Strategy

- **Patterns to capture:** Reusable MSW handler configurations, custom render wrappers for project-specific providers, test data factory patterns, recurring accessibility violation fixes.
- **Examples to collect:** Successful test suites with high coverage, effective integration test patterns for complex pages, MSW handler compositions for multi-step API flows.
- **Update permission:** Agents may freely add/update files in `references/`. Changes to `SKILL.md` or `scripts/` require user approval.
