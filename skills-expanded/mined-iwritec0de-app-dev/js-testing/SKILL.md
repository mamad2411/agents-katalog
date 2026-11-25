---
name: js-testing
description: >-
  This skill should be used when the user asks to 'write tests', 'add test
  coverage', 'test a component', 'test an API route', 'test a hook',
  'set up Vitest', 'use React Testing Library', 'mock an API', or mentions
  'component testing', 'integration tests', 'vitest', 'RTL', 'msw',
  'testing library'. Provides JavaScript/TypeScript testing patterns using
  Vitest and React Testing Library for Next.js applications.
license: MIT
metadata:
  author: Chris Kelley (hello@iwritecode.io)
  version: 1.0.0
---

# JS Testing Skill — Vitest + React Testing Library for Next.js

## Critical Rules

1. **Vitest is the test runner.** Do not use Jest. All configuration, mocking, and assertions use the Vitest API (`vi.fn()`, `vi.mock()`, `vi.spyOn()`, etc.).
2. **React Testing Library (RTL) for component tests.** Query elements the way a user would find them — by role, label, text, or placeholder. Never reach for `getByTestId` unless no semantic query is possible.
3. **Test user behavior, not implementation.** Assert what the user sees and can interact with. Do not assert on component state, refs, internal variables, or hook return values directly (except when using `renderHook`).
4. **Never test React internals.** Do not mock `useState`, `useEffect`, `useRef`, or any React built-in. If you need to control what a hook returns, extract the logic into a custom hook and test it with `renderHook`.
5. **Use MSW for API mocking.** Mock at the network layer with Mock Service Worker, not by stubbing `fetch` or `axios` directly. This gives realistic request/response cycles and catches serialization issues.
6. **Prefer `userEvent` over `fireEvent`.** `userEvent` simulates real browser behavior (focus, blur, keystrokes). `fireEvent` dispatches synthetic DOM events and should only be used for events `userEvent` does not support.
7. **Every test file must be self-contained.** Shared setup belongs in `vitest.setup.ts` or a dedicated test utility file, not scattered across tests via implicit globals.

---

## Component Testing

### Basic Render Test

```tsx
// components/greeting.tsx
export function Greeting({ name }: { name: string }) {
  return <h1>Hello, {name}!</h1>;
}
```

```tsx
// components/greeting.test.tsx
import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { Greeting } from "./greeting";

describe("Greeting", () => {
  it("renders the user name", () => {
    render(<Greeting name="Kelley" />);

    expect(
      screen.getByRole("heading", { name: /hello, kelley/i })
    ).toBeInTheDocument();
  });
});
```

### User Interaction Test (Click)

```tsx
// components/counter.tsx
"use client";

import { useState } from "react";

export function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount((c) => c + 1)}>Increment</button>
    </div>
  );
}
```

```tsx
// components/counter.test.tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect } from "vitest";
import { Counter } from "./counter";

describe("Counter", () => {
  it("increments the count when the button is clicked", async () => {
    const user = userEvent.setup();
    render(<Counter />);

    expect(screen.getByText("Count: 0")).toBeInTheDocument();

    await user.click(screen.getByRole("button", { name: /increment/i }));

    expect(screen.getByText("Count: 1")).toBeInTheDocument();
  });
});
```

### User Interaction Test (Typing)

```tsx
// components/search-input.tsx
"use client";

import { useState } from "react";

export function SearchInput({ onSearch }: { onSearch: (query: string) => void }) {
  const [query, setQuery] = useState("");

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        onSearch(query);
      }}
    >
      <label htmlFor="search">Search</label>
      <input
        id="search"
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button type="submit">Go</button>
    </form>
  );
}
```

```tsx
// components/search-input.test.tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi } from "vitest";
import { SearchInput } from "./search-input";

describe("SearchInput", () => {
  it("calls onSearch with the typed query on submit", async () => {
    const user = userEvent.setup();
    const handleSearch = vi.fn();

    render(<SearchInput onSearch={handleSearch} />);

    await user.type(screen.getByLabelText(/search/i), "vitest");
    await user.click(screen.getByRole("button", { name: /go/i }));

    expect(handleSearch).toHaveBeenCalledWith("vitest");
    expect(handleSearch).toHaveBeenCalledTimes(1);
  });
});
```

### Async Data Loading Test

```tsx
// components/user-profile.tsx
"use client";

import { useEffect, useState } from "react";

interface User {
  id: number;
  name: string;
  email: string;
}

export function UserProfile({ userId }: { userId: number }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`/api/users/${userId}`)
      .then((res) => res.json())
      .then((data) => {
        setUser(data);
        setLoading(false);
      });
  }, [userId]);

  if (loading) return <p>Loading profile...</p>;
  if (!user) return <p>User not found</p>;

  return (
    <article>
      <h2>{user.name}</h2>
      <p>{user.email}</p>
    </article>
  );
}
```

```tsx
// components/user-profile.test.tsx
import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { http, HttpResponse } from "msw";
import { server } from "@/test/msw-server";
import { UserProfile } from "./user-profile";

describe("UserProfile", () => {
  it("shows loading state then renders user data", async () => {
    server.use(
      http.get("/api/users/1", () => {
        return HttpResponse.json({
          id: 1,
          name: "Kelley",
          email: "kelley@example.com",
        });
      })
    );

    render(<UserProfile userId={1} />);

    expect(screen.getByText(/loading profile/i)).toBeInTheDocument();

    expect(
      await screen.findByRole("heading", { name: /kelley/i })
    ).toBeInTheDocument();
    expect(screen.getByText("kelley@example.com")).toBeInTheDocument();
  });
});
```

### Form Submission Test

```tsx
// components/contact-form.tsx
"use client";

import { useState } from "react";

export function ContactForm() {
  const [submitted, setSubmitted] = useState(false);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);

    const res = await fetch("/api/contact", {
      method: "POST",
      body: JSON.stringify({
        name: formData.get("name"),
        message: formData.get("message"),
      }),
      headers: { "Content-Type": "application/json" },
    });

    if (res.ok) setSubmitted(true);
  }

  if (submitted) return <p>Thank you for your message!</p>;

  return (
    <form onSubmit={handleSubmit}>
      <label htmlFor="name">Name</label>
      <input id="name" name="name" required />

      <label htmlFor="message">Message</label>
      <textarea id="message" name="message" required />

      <button type="submit">Send</button>
    </form>
  );
}
```

```tsx
// components/contact-form.test.tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect } from "vitest";
import { http, HttpResponse } from "msw";
import { server } from "@/test/msw-server";
import { ContactForm } from "./contact-form";

describe("ContactForm", () => {
  it("submits the form and shows a success message", async () => {
    const user = userEvent.setup();

    server.use(
      http.post("/api/contact", () => {
        return HttpResponse.json({ success: true });
      })
    );

    render(<ContactForm />);

    await user.type(screen.getByLabelText(/name/i), "Kelley");
    await user.type(screen.getByLabelText(/message/i), "Hello there");
    await user.click(screen.getByRole("button", { name: /send/i }));

    expect(
      await screen.findByText(/thank you for your message/i)
    ).toBeInTheDocument();
  });
});
```

### Error State Test

```tsx
// components/contact-form.test.tsx (additional test)
describe("ContactForm", () => {
  // ... success test above ...

  it("shows an error message when submission fails", async () => {
    const user = userEvent.setup();

    server.use(
      http.post("/api/contact", () => {
        return HttpResponse.json(
          { error: "Server error" },
          { status: 500 }
        );
      })
    );

    render(<ContactForm />);

    await user.type(screen.getByLabelText(/name/i), "Kelley");
    await user.type(screen.getByLabelText(/message/i), "Hello");
    await user.click(screen.getByRole("button", { name: /send/i }));

    // The form should still be visible (not replaced by success message)
    expect(
      await screen.findByText(/something went wrong/i)
    ).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /send/i })).toBeInTheDocument();
  });
});
```

---

## API Route Testing (Next.js App Router)

### Testing a GET Route Handler

```ts
// app/api/users/route.ts
import { NextResponse } from "next/server";
import { db } from "@/lib/db";

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const role = searchParams.get("role");

  const users = role
    ? await db.user.findMany({ where: { role } })
    : await db.user.findMany();

  return NextResponse.json(users);
}
```

```ts
// app/api/users/route.test.ts
import { describe, it, expect, vi, beforeEach } from "vitest";
import { GET } from "./route";

vi.mock("@/lib/db", () => ({
  db: {
    user: {
      findMany: vi.fn(),
    },
  },
}));

import { db } from "@/lib/db";

const mockFindMany = vi.mocked(db.user.findMany);

describe("GET /api/users", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("returns all users when no role filter is provided", async () => {
    const users = [
      { id: 1, name: "Alice", role: "admin" },
      { id: 2, name: "Bob", role: "user" },
    ];
    mockFindMany.mockResolvedValue(users);

    const request = new Request("http://localhost/api/users");
    const response = await GET(request);
    const data = await response.json();

    expect(response.status).toBe(200);
    expect(data).toEqual(users);
    expect(mockFindMany).toHaveBeenCalledWith();
  });

  it("filters users by role when query param is provided", async () => {
    const admins = [{ id: 1, name: "Alice", role: "admin" }];
    mockFindMany.mockResolvedValue(admins);

    const request = new Request("http://localhost/api/users?role=admin");
    const response = await GET(request);
    const data = await response.json();

    expect(data).toEqual(admins);
    expect(mockFindMany).toHaveBeenCalledWith({ where: { role: "admin" } });
  });
});
```

### Testing a POST Route Handler

```ts
// app/api/posts/route.ts
import { NextResponse } from "next/server";
import { db } from "@/lib/db";
import { getServerSession } from "@/lib/auth";

export async function POST(request: Request) {
  const session = await getServerSession();

  if (!session?.user) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const body = await request.json();

  if (!body.title || !body.content) {
    return NextResponse.json(
      { error: "Title and content are required" },
      { status: 400 }
    );
  }

  const post = await db.post.create({
    data: {
      title: body.title,
      content: body.content,
      authorId: session.user.id,
    },
  });

  return NextResponse.json(post, { status: 201 });
}
```

```ts
// app/api/posts/route.test.ts
import { describe, it, expect, vi, beforeEach } from "vitest";
import { POST } from "./route";

vi.mock("@/lib/db", () => ({
  db: {
    post: {
      create: vi.fn(),
    },
  },
}));

vi.mock("@/lib/auth", () => ({
  getServerSession: vi.fn(),
}));

import { db } from "@/lib/db";
import { getServerSession } from "@/lib/auth";

const mockCreate = vi.mocked(db.post.create);
const mockGetSession = vi.mocked(getServerSession);

function jsonRequest(body: unknown): Request {
  return new Request("http://localhost/api/posts", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
}

describe("POST /api/posts", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("returns 401 when the user is not authenticated", async () => {
    mockGetSession.mockResolvedValue(null);

    const response = await POST(jsonRequest({ title: "Hi", content: "Body" }));

    expect(response.status).toBe(401);
    expect(await response.json()).toEqual({ error: "Unauthorized" });
  });

  it("returns 400 when required fields are missing", async () => {
    mockGetSession.mockResolvedValue({ user: { id: "u1", name: "Alice" } });

    const response = await POST(jsonRequest({ title: "" }));

    expect(response.status).toBe(400);
  });

  it("creates a post and returns 201", async () => {
    mockGetSession.mockResolvedValue({ user: { id: "u1", name: "Alice" } });
    mockCreate.mockResolvedValue({
      id: "p1",
      title: "My Post",
      content: "Content here",
      authorId: "u1",
    } as any);

    const response = await POST(
      jsonRequest({ title: "My Post", content: "Content here" })
    );
    const data = await response.json();

    expect(response.status).toBe(201);
    expect(data.title).toBe("My Post");
    expect(mockCreate).toHaveBeenCalledWith({
      data: {
        title: "My Post",
        content: "Content here",
        authorId: "u1",
      },
    });
  });
});
```

---

## Hook Testing

### Testing a Custom Hook

```ts
// hooks/use-debounce.ts
import { useState, useEffect } from "react";

export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}
```

```ts
// hooks/use-debounce.test.ts
import { renderHook, act } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { useDebounce } from "./use-debounce";

describe("useDebounce", () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it("returns the initial value immediately", () => {
    const { result } = renderHook(() => useDebounce("hello", 500));
    expect(result.current).toBe("hello");
  });

  it("updates the value after the delay", () => {
    const { result, rerender } = renderHook(
      ({ value, delay }) => useDebounce(value, delay),
      { initialProps: { value: "hello", delay: 500 } }
    );

    rerender({ value: "world", delay: 500 });

    // Value should not have changed yet
    expect(result.current).toBe("hello");

    act(() => {
      vi.advanceTimersByTime(500);
    });

    expect(result.current).toBe("world");
  });
});
```

### Testing an Async Hook with Providers

```tsx
// hooks/use-current-user.ts
"use client";

import { useEffect, useState } from "react";

interface User {
  id: string;
  name: string;
}

export function useCurrentUser() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("/api/me")
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch user");
        return res.json();
      })
      .then(setUser)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  return { user, loading, error };
}
```

```tsx
// hooks/use-current-user.test.ts
import { renderHook, waitFor } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { http, HttpResponse } from "msw";
import { server } from "@/test/msw-server";
import { useCurrentUser } from "./use-current-user";

describe("useCurrentUser", () => {
  it("returns the current user after loading", async () => {
    server.use(
      http.get("/api/me", () => {
        return HttpResponse.json({ id: "u1", name: "Kelley" });
      })
    );

    const { result } = renderHook(() => useCurrentUser());

    expect(result.current.loading).toBe(true);

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    expect(result.current.user).toEqual({ id: "u1", name: "Kelley" });
    expect(result.current.error).toBeNull();
  });

  it("returns an error when the API fails", async () => {
    server.use(
      http.get("/api/me", () => {
        return HttpResponse.json(null, { status: 500 });
      })
    );

    const { result } = renderHook(() => useCurrentUser());

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    expect(result.current.user).toBeNull();
    expect(result.current.error).toBe("Failed to fetch user");
  });
});
```

### Wrapping a Hook with Providers

```tsx
// hooks/use-theme.test.tsx
import { renderHook } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { ThemeProvider } from "@/components/theme-provider";
import { useTheme } from "./use-theme";

function wrapper({ children }: { children: React.ReactNode }) {
  return <ThemeProvider defaultTheme="dark">{children}</ThemeProvider>;
}

describe("useTheme", () => {
  it("returns the theme from the provider", () => {
    const { result } = renderHook(() => useTheme(), { wrapper });
    expect(result.current.theme).toBe("dark");
  });
});
```

---

## What to Mock and How

### External APIs — Use MSW

```ts
// test/msw-server.ts
import { setupServer } from "msw/node";

export const server = setupServer();
// Handlers are added per-test with server.use(...)
```

```ts
// vitest.setup.ts (excerpt)
import { server } from "@/test/msw-server";
import { beforeAll, afterEach, afterAll } from "vitest";

beforeAll(() => server.listen({ onUnhandledRequest: "error" }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

### Database — Prefer a Test Database, Not a Mock ORM

For integration tests, use a real database (SQLite in-memory, or a test Postgres instance). Only mock the database module for unit tests of API route handlers where you want to isolate the handler logic:

```ts
vi.mock("@/lib/db", () => ({
  db: {
    user: {
      findMany: vi.fn(),
      findUnique: vi.fn(),
      create: vi.fn(),
    },
  },
}));
```

### Auth — Mock the Session

```ts
vi.mock("@/lib/auth", () => ({
  getServerSession: vi.fn(),
}));

// In a specific test:
vi.mocked(getServerSession).mockResolvedValue({
  user: { id: "u1", name: "Alice", role: "admin" },
});
```

### Time — Use Fake Timers

```ts
import { vi, beforeEach, afterEach } from "vitest";

beforeEach(() => {
  vi.useFakeTimers();
  vi.setSystemTime(new Date("2026-01-15T10:00:00Z"));
});

afterEach(() => {
  vi.useRealTimers();
});

// In a test:
vi.advanceTimersByTime(5000); // advance 5 seconds
```

### Environment Variables — Use `vi.stubEnv`

```ts
import { vi, beforeEach, afterEach } from "vitest";

beforeEach(() => {
  vi.stubEnv("DATABASE_URL", "postgresql://test:test@localhost/testdb");
  vi.stubEnv("NODE_ENV", "test");
});

afterEach(() => {
  vi.unstubAllEnvs();
});
```

---

## Anti-Patterns (JS-Specific)

### 1. Using `getByTestId` When a Semantic Query Exists

```tsx
// BAD — requires adding data-testid to the component for no reason
screen.getByTestId("submit-button");

// GOOD — queries the way a user would find the button
screen.getByRole("button", { name: /submit/i });
```

### 2. Snapshot Tests for Complex Components

Snapshot tests on large component trees are brittle and produce meaningless diffs. Test specific behavior instead.

```tsx
// BAD
expect(container).toMatchSnapshot();

// GOOD
expect(screen.getByRole("heading", { name: /dashboard/i })).toBeInTheDocument();
expect(screen.getByText(/3 new notifications/i)).toBeInTheDocument();
```

### 3. Mocking `useState` or `useEffect`

Never mock React internals. If a component's behavior depends on state, test the behavior through user interactions.

```tsx
// BAD — fragile, breaks on refactors, tests nothing useful
vi.spyOn(React, "useState").mockReturnValue([true, vi.fn()]);

// GOOD — interact with the component as a user would
await user.click(screen.getByRole("button", { name: /toggle/i }));
expect(screen.getByText(/panel is open/i)).toBeInTheDocument();
```

### 4. Using `vi.mock` at Module Level for Everything

Only mock what you must. Over-mocking makes tests pass even when the real integration is broken.

```tsx
// BAD — mocking everything, test proves nothing
vi.mock("@/lib/utils");
vi.mock("@/lib/format");
vi.mock("@/components/button");

// GOOD — mock only the boundary (network, database)
// Let utils, formatters, and child components run with real code
```

### 5. Testing CSS Classes or Styles

```tsx
// BAD — breaks when you change Tailwind classes
expect(element).toHaveClass("bg-red-500 text-white");

// GOOD — test the accessible semantics or visible outcome
expect(screen.getByRole("alert")).toBeInTheDocument();
expect(screen.getByRole("alert")).toHaveTextContent(/error/i);
```

---

## Test File Organization

### Co-Located Tests (Preferred)

Place test files next to the code they test:

```
components/
  button.tsx
  button.test.tsx
  user-profile.tsx
  user-profile.test.tsx
hooks/
  use-debounce.ts
  use-debounce.test.ts
app/
  api/
    users/
      route.ts
      route.test.ts
```

### Shared Test Utilities

```
test/
  msw-server.ts          # MSW server instance
  handlers.ts            # Default/shared MSW handlers
  render.tsx             # Custom render with providers
  factories.ts           # Test data factories
```

### Custom Render with Providers

```tsx
// test/render.tsx
import { render, type RenderOptions } from "@testing-library/react";
import { ThemeProvider } from "@/components/theme-provider";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

function AllProviders({ children }: { children: React.ReactNode }) {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
    },
  });

  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider defaultTheme="light">{children}</ThemeProvider>
    </QueryClientProvider>
  );
}

export function renderWithProviders(
  ui: React.ReactElement,
  options?: Omit<RenderOptions, "wrapper">
) {
  return render(ui, { wrapper: AllProviders, ...options });
}
```

### Setup Files

```ts
// vitest.setup.ts
import "@testing-library/jest-dom/vitest";
import { cleanup } from "@testing-library/react";
import { afterEach, beforeAll, afterAll } from "vitest";
import { server } from "@/test/msw-server";

// RTL cleanup after each test
afterEach(() => {
  cleanup();
});

// MSW server lifecycle
beforeAll(() => server.listen({ onUnhandledRequest: "error" }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```
