---
name: react-testing-workflows
description: Testing strategy and execution for React applications. Covers Vitest configuration, React Testing Library patterns, custom hook testing, Playwright E2E, Storybook stories and play functions, and coverage reporting. Keywords: test, vitest, testing library, playwright, storybook, coverage, unit test, integration test, e2e, renderHook, userEvent
---

# React Testing Workflows

## Overview

This skill provides a complete testing strategy for React applications built with TypeScript. It covers every layer of the testing pyramid: unit tests with Vitest, component integration tests with React Testing Library, visual and interaction tests with Storybook, and end-to-end tests with Playwright.

**Testing Pyramid Target Ratios:**

| Layer | Proportion | Tool | Speed |
|-------|-----------|------|-------|
| Unit (functions, hooks) | 50% | Vitest | < 5ms each |
| Integration (components) | 30% | Vitest + React Testing Library | < 50ms each |
| E2E (full user flows) | 15% | Playwright | < 5s each |
| Visual (screenshot comparison) | 5% | Storybook + Chromatic or Playwright | Varies |

## When to Use

Use this skill when:
- Setting up testing infrastructure for a React project
- Writing tests for React components or custom hooks
- Creating Storybook stories with play functions
- Writing E2E tests with Playwright
- Configuring test coverage reporting
- Debugging failing tests

**Trigger phrases:**
- "Write tests for this component"
- "Set up Vitest"
- "Test this custom hook"
- "Create a Storybook story"
- "Write an E2E test"
- "Check test coverage"
- "Why is this test failing"

## Vitest Configuration

### Setup

```bash
pnpm add -D vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom @vitejs/plugin-react
```

### vitest.config.ts

```typescript
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: ["./src/test/setup.ts"],
    include: ["src/**/*.{test,spec}.{ts,tsx}"],
    coverage: {
      provider: "v8",
      reporter: ["text", "html", "lcov"],
      include: ["src/**/*.{ts,tsx}"],
      exclude: [
        "src/**/*.test.{ts,tsx}",
        "src/**/*.stories.{ts,tsx}",
        "src/test/**",
        "src/types/**",
        "src/**/*.d.ts",
      ],
      thresholds: {
        branches: 80,
        functions: 80,
        lines: 80,
        statements: 80,
      },
    },
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
```

### Test Setup File

```typescript
// src/test/setup.ts
import "@testing-library/jest-dom/vitest";
import { cleanup } from "@testing-library/react";
import { afterEach, vi } from "vitest";

// Automatic cleanup after each test
afterEach(() => {
  cleanup();
});

// Mock IntersectionObserver
class MockIntersectionObserver {
  observe = vi.fn();
  disconnect = vi.fn();
  unobserve = vi.fn();
}
Object.defineProperty(window, "IntersectionObserver", {
  writable: true,
  value: MockIntersectionObserver,
});

// Mock matchMedia
Object.defineProperty(window, "matchMedia", {
  writable: true,
  value: vi.fn().mockImplementation((query: string) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

// Mock ResizeObserver
class MockResizeObserver {
  observe = vi.fn();
  disconnect = vi.fn();
  unobserve = vi.fn();
}
Object.defineProperty(window, "ResizeObserver", {
  writable: true,
  value: MockResizeObserver,
});
```

## React Testing Library Patterns

### Rendering and Querying

```typescript
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi } from "vitest";
import { Button } from "@/components/ui/button";

describe("Button", () => {
  it("renders with text content", () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole("button", { name: "Click me" })).toBeInTheDocument();
  });

  it("calls onClick when clicked", async () => {
    const user = userEvent.setup();
    const handleClick = vi.fn();

    render(<Button onClick={handleClick}>Click me</Button>);
    await user.click(screen.getByRole("button", { name: "Click me" }));

    expect(handleClick).toHaveBeenCalledOnce();
  });

  it("is disabled when disabled prop is true", () => {
    render(<Button disabled>Click me</Button>);
    expect(screen.getByRole("button")).toBeDisabled();
  });

  it("applies variant classes", () => {
    render(<Button variant="secondary">Secondary</Button>);
    expect(screen.getByRole("button")).toHaveClass("bg-secondary");
  });
});
```

### Query Priority

Always use queries in this order of preference (most accessible first):

1. `getByRole` -- ARIA role (button, heading, textbox, link, etc.)
2. `getByLabelText` -- Form inputs with labels
3. `getByPlaceholderText` -- Inputs with placeholders (less preferred than label)
4. `getByText` -- Non-interactive elements with visible text
5. `getByDisplayValue` -- Current value of form elements
6. `getByAltText` -- Images
7. `getByTitle` -- Title attribute (last resort for visible)
8. `getByTestId` -- `data-testid` attribute (escape hatch only)

### Async Testing

```typescript
import { render, screen, waitFor } from "@testing-library/react";

describe("UserProfile", () => {
  it("loads and displays user data", async () => {
    render(<UserProfile userId="123" />);

    // Wait for loading to finish
    expect(screen.getByText("Loading...")).toBeInTheDocument();

    // Wait for content to appear
    await waitFor(() => {
      expect(screen.getByRole("heading", { name: "Jane Doe" })).toBeInTheDocument();
    });

    expect(screen.queryByText("Loading...")).not.toBeInTheDocument();
  });

  it("displays error state on fetch failure", async () => {
    server.use(
      http.get("/api/users/123", () => {
        return HttpResponse.json({ error: "Not found" }, { status: 404 });
      })
    );

    render(<UserProfile userId="123" />);

    await waitFor(() => {
      expect(screen.getByRole("alert")).toHaveTextContent("Failed to load user");
    });
  });
});
```

### Testing Forms

```typescript
describe("ContactForm", () => {
  it("submits valid form data", async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();

    render(<ContactForm onSubmit={onSubmit} />);

    await user.type(screen.getByLabelText("Name"), "Jane Doe");
    await user.type(screen.getByLabelText("Email"), "jane@example.com");
    await user.type(screen.getByLabelText("Message"), "Hello there, this is a test message");
    await user.click(screen.getByRole("button", { name: "Send" }));

    expect(onSubmit).toHaveBeenCalledWith({
      name: "Jane Doe",
      email: "jane@example.com",
      message: "Hello there, this is a test message",
    });
  });

  it("shows validation errors for empty required fields", async () => {
    const user = userEvent.setup();
    render(<ContactForm onSubmit={vi.fn()} />);

    await user.click(screen.getByRole("button", { name: "Send" }));

    expect(screen.getByText("Name is required")).toBeInTheDocument();
    expect(screen.getByText("Valid email required")).toBeInTheDocument();
  });
});
```

### Rendering with Providers

```typescript
// src/test/utils.tsx
import { render, type RenderOptions } from "@testing-library/react";
import { type ReactElement, type ReactNode } from "react";
import { ThemeProvider } from "@/components/providers/theme-provider";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  });
}

function AllProviders({ children }: { children: ReactNode }) {
  const queryClient = createTestQueryClient();
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider defaultTheme="light">
        {children}
      </ThemeProvider>
    </QueryClientProvider>
  );
}

function renderWithProviders(ui: ReactElement, options?: Omit<RenderOptions, "wrapper">) {
  return render(ui, { wrapper: AllProviders, ...options });
}

export { renderWithProviders as render };
```

## Testing Custom Hooks

```typescript
import { renderHook, act } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { useCounter } from "@/hooks/use-counter";

describe("useCounter", () => {
  it("initializes with default value", () => {
    const { result } = renderHook(() => useCounter());
    expect(result.current.count).toBe(0);
  });

  it("initializes with provided value", () => {
    const { result } = renderHook(() => useCounter(10));
    expect(result.current.count).toBe(10);
  });

  it("increments the count", () => {
    const { result } = renderHook(() => useCounter());

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(1);
  });

  it("respects max value", () => {
    const { result } = renderHook(() => useCounter(9, { max: 10 }));

    act(() => {
      result.current.increment();
      result.current.increment(); // should not go past 10
    });

    expect(result.current.count).toBe(10);
  });
});

// Testing hooks that depend on context
describe("useAuth", () => {
  it("returns current user from auth context", () => {
    const mockUser = { id: "1", name: "Jane" };

    const { result } = renderHook(() => useAuth(), {
      wrapper: ({ children }) => (
        <AuthProvider initialUser={mockUser}>{children}</AuthProvider>
      ),
    });

    expect(result.current.user).toEqual(mockUser);
  });
});
```

## API Mocking with MSW

```typescript
// src/test/mocks/handlers.ts
import { http, HttpResponse } from "msw";

export const handlers = [
  http.get("/api/users", () => {
    return HttpResponse.json([
      { id: "1", name: "Jane Doe", email: "jane@example.com" },
      { id: "2", name: "John Smith", email: "john@example.com" },
    ]);
  }),

  http.post("/api/users", async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json({ id: "3", ...body }, { status: 201 });
  }),

  http.get("/api/users/:id", ({ params }) => {
    return HttpResponse.json({
      id: params.id,
      name: "Jane Doe",
      email: "jane@example.com",
    });
  }),
];

// src/test/mocks/server.ts
import { setupServer } from "msw/node";
import { handlers } from "./handlers";

export const server = setupServer(...handlers);

// Add to src/test/setup.ts
import { server } from "./mocks/server";

beforeAll(() => server.listen({ onUnhandledRequest: "error" }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

## Storybook Stories

### Story Configuration

```typescript
// src/components/ui/button.stories.tsx
import type { Meta, StoryObj } from "@storybook/react";
import { within, userEvent, expect } from "@storybook/test";
import { Button } from "./button";

const meta = {
  title: "UI/Button",
  component: Button,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
  argTypes: {
    variant: {
      control: "select",
      options: ["primary", "secondary", "outline", "ghost"],
    },
    size: {
      control: "select",
      options: ["sm", "md", "lg"],
    },
  },
} satisfies Meta<typeof Button>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Primary: Story = {
  args: {
    children: "Primary Button",
    variant: "primary",
  },
};

export const Secondary: Story = {
  args: {
    children: "Secondary Button",
    variant: "secondary",
  },
};

export const AllVariants: Story = {
  render: () => (
    <div className="flex gap-4">
      <Button variant="primary">Primary</Button>
      <Button variant="secondary">Secondary</Button>
      <Button variant="outline">Outline</Button>
      <Button variant="ghost">Ghost</Button>
    </div>
  ),
};

export const AllSizes: Story = {
  render: () => (
    <div className="flex items-center gap-4">
      <Button size="sm">Small</Button>
      <Button size="md">Medium</Button>
      <Button size="lg">Large</Button>
    </div>
  ),
};
```

### Play Functions (Interaction Tests)

```typescript
export const ClickInteraction: Story = {
  args: {
    children: "Click me",
  },
  play: async ({ canvasElement, args }) => {
    const canvas = within(canvasElement);
    const button = canvas.getByRole("button", { name: "Click me" });

    // Verify initial state
    await expect(button).toBeEnabled();

    // Simulate click
    await userEvent.click(button);

    // Verify callback was invoked (if args.onClick is a spy)
    if (args.onClick) {
      await expect(args.onClick).toHaveBeenCalledOnce();
    }
  },
};

export const FormSubmission: Story = {
  render: () => <ContactForm />,
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    await userEvent.type(canvas.getByLabelText("Name"), "Jane Doe");
    await userEvent.type(canvas.getByLabelText("Email"), "jane@example.com");
    await userEvent.type(canvas.getByLabelText("Message"), "Hello from Storybook");
    await userEvent.click(canvas.getByRole("button", { name: "Send" }));

    // Verify success state
    await expect(canvas.getByText("Message sent!")).toBeInTheDocument();
  },
};
```

## Playwright E2E Testing

### Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [["html"], ["list"]],
  use: {
    baseURL: "http://localhost:3000",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
  },
  projects: [
    { name: "chromium", use: { ...devices["Desktop Chrome"] } },
    { name: "firefox", use: { ...devices["Desktop Firefox"] } },
    { name: "webkit", use: { ...devices["Desktop Safari"] } },
    { name: "mobile-chrome", use: { ...devices["Pixel 5"] } },
    { name: "mobile-safari", use: { ...devices["iPhone 13"] } },
  ],
  webServer: {
    command: "pnpm dev",
    url: "http://localhost:3000",
    reuseExistingServer: !process.env.CI,
  },
});
```

### E2E Test Patterns

```typescript
// e2e/auth.spec.ts
import { test, expect } from "@playwright/test";

test.describe("Authentication", () => {
  test("user can sign up with valid credentials", async ({ page }) => {
    await page.goto("/signup");

    await page.getByLabel("Full name").fill("Jane Doe");
    await page.getByLabel("Email").fill("jane@example.com");
    await page.getByLabel("Password").fill("SecureP@ss123");
    await page.getByRole("button", { name: "Create account" }).click();

    // Wait for redirect to dashboard
    await expect(page).toHaveURL("/dashboard");
    await expect(page.getByRole("heading", { name: "Welcome, Jane" })).toBeVisible();
  });

  test("shows validation errors for invalid email", async ({ page }) => {
    await page.goto("/signup");

    await page.getByLabel("Email").fill("not-an-email");
    await page.getByRole("button", { name: "Create account" }).click();

    await expect(page.getByText("Valid email required")).toBeVisible();
  });
});

// e2e/navigation.spec.ts
test.describe("Navigation", () => {
  test("navigates between pages via header links", async ({ page }) => {
    await page.goto("/");

    await page.getByRole("link", { name: "About" }).click();
    await expect(page).toHaveURL("/about");
    await expect(page.getByRole("heading", { level: 1 })).toHaveText("About Us");

    await page.getByRole("link", { name: "Contact" }).click();
    await expect(page).toHaveURL("/contact");
  });

  test("mobile menu toggles correctly", async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto("/");

    const menuButton = page.getByRole("button", { name: "Open menu" });
    await expect(menuButton).toBeVisible();

    await menuButton.click();
    await expect(page.getByRole("navigation")).toBeVisible();

    await page.getByRole("button", { name: "Close menu" }).click();
    await expect(page.getByRole("navigation")).toBeHidden();
  });
});
```

### Visual Regression with Playwright

```typescript
// e2e/visual.spec.ts
test.describe("Visual regression", () => {
  test("homepage matches screenshot", async ({ page }) => {
    await page.goto("/");
    await page.waitForLoadState("networkidle");
    await expect(page).toHaveScreenshot("homepage.png", {
      fullPage: true,
      maxDiffPixelRatio: 0.01,
    });
  });

  test("responsive screenshots", async ({ page }) => {
    const breakpoints = [
      { name: "mobile", width: 375, height: 812 },
      { name: "tablet", width: 768, height: 1024 },
      { name: "desktop", width: 1280, height: 720 },
    ];

    for (const bp of breakpoints) {
      await page.setViewportSize({ width: bp.width, height: bp.height });
      await page.goto("/");
      await page.waitForLoadState("networkidle");
      await expect(page).toHaveScreenshot(`homepage-${bp.name}.png`, {
        fullPage: true,
      });
    }
  });
});
```

## Coverage Reporting

### Running Coverage

```bash
# Run all tests with coverage
pnpm vitest run --coverage

# Run specific file/directory with coverage
pnpm vitest run src/components/ --coverage

# Watch mode with coverage
pnpm vitest --coverage
```

### Coverage Thresholds

Set in `vitest.config.ts` under `test.coverage.thresholds`:

| Metric | Minimum | Target |
|--------|---------|--------|
| Statements | 80% | 90%+ |
| Branches | 80% | 85%+ |
| Functions | 80% | 90%+ |
| Lines | 80% | 90%+ |

### What to Test vs. What to Skip

**Always test:**
- Component rendering with different prop combinations
- User interactions (clicks, typing, form submissions)
- Conditional rendering (loading, error, empty states)
- Custom hooks (state transitions, side effects)
- Utility functions (pure logic)
- Accessibility (roles, labels, keyboard navigation)

**Skip or minimize:**
- Third-party library internals
- Static content with no logic
- CSS class names (test behavior, not implementation)
- Implementation details (internal state variables, method names)

## Running Tests

```bash
# All unit/integration tests
pnpm vitest run

# Watch mode
pnpm vitest

# Specific file
pnpm vitest run src/components/ui/button.test.tsx

# Pattern match
pnpm vitest run --testNamePattern "submits valid form"

# E2E tests
pnpm exec playwright test

# E2E with UI
pnpm exec playwright test --ui

# Storybook interaction tests
pnpm storybook --ci && pnpm test-storybook

# Full test suite (CI)
pnpm vitest run --coverage && pnpm exec playwright test
```

## Common Test Debugging

### Test Fails with "Unable to find role"

The element's ARIA role does not match. Use `screen.logTestingPlaygroundURL()` or `screen.debug()` to inspect the rendered DOM.

### Test Fails with Act Warning

Wrap state updates in `act()`, or use `await waitFor()` for async updates. `userEvent.setup()` handles most act-wrapping automatically.

### Flaky Async Tests

Replace arbitrary `waitFor` timeouts with specific assertions:

```typescript
// Bad - flaky
await new Promise((r) => setTimeout(r, 1000));

// Good - deterministic
await waitFor(() => {
  expect(screen.getByText("Loaded")).toBeInTheDocument();
});
```

### Playwright Test Times Out

Check that the dev server is running and accessible. Increase the `timeout` in the test or configure `webServer.timeout` in `playwright.config.ts`.

---

**Skill Version:** 1.0.0
**Last Updated:** 2026-03-11
