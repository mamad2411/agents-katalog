---
name: react-component-development
description: Component patterns and best practices for React with TypeScript. Covers functional components, custom hooks, state management, composition patterns, error boundaries, server components, and form handling. Keywords: React component, hooks, state management, TypeScript component, custom hooks, Zustand, useReducer, compound components, render props, server components
---

# React Component Development

## Overview

This skill provides patterns, conventions, and best practices for building React components with TypeScript. It covers the full spectrum from primitive UI components to complex composed layouts, custom hooks, state management integration, and React 19 server components.

All patterns assume:
- React 18+ or React 19 (server components)
- TypeScript in strict mode
- Tailwind CSS for styling
- ESLint with `@typescript-eslint` and `eslint-plugin-react-hooks`

## When to Use

Use this skill when:
- Creating new React components
- Refactoring existing components for better patterns
- Implementing custom hooks
- Setting up state management (local or global)
- Building compound component APIs
- Working with React 19 server components
- Implementing form handling logic

**Trigger phrases:**
- "Create a React component"
- "Build a custom hook"
- "Set up state management"
- "TypeScript component pattern"
- "Compound component"
- "Server component"
- "Form handling in React"

## Component Patterns

### Functional Component with TypeScript

The standard pattern for all components:

```typescript
import { type HTMLAttributes, forwardRef } from "react";
import { cn } from "@/lib/utils";

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "outlined" | "elevated";
  padding?: "none" | "sm" | "md" | "lg";
}

const Card = forwardRef<HTMLDivElement, CardProps>(
  ({ className, variant = "default", padding = "md", children, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          "rounded-lg",
          {
            "bg-card text-card-foreground": variant === "default",
            "border border-border bg-transparent": variant === "outlined",
            "bg-card text-card-foreground shadow-lg": variant === "elevated",
          },
          {
            "p-0": padding === "none",
            "p-4": padding === "sm",
            "p-6": padding === "md",
            "p-8": padding === "lg",
          },
          className
        )}
        {...props}
      >
        {children}
      </div>
    );
  }
);
Card.displayName = "Card";

export { Card, type CardProps };
```

**Rules:**
1. Always use explicit `interface` for props (not inline types)
2. Extend the appropriate HTML element attributes
3. Use `forwardRef` for any component that wraps a DOM element
4. Accept and merge `className` via `cn()` (clsx + tailwind-merge)
5. Spread remaining props onto the root element
6. Set `displayName` when using `forwardRef`
7. Export the props type alongside the component

### Discriminated Union Props

Use when a component has mutually exclusive configurations:

```typescript
interface LinkButtonProps {
  as: "link";
  href: string;
  target?: "_blank" | "_self";
}

interface ActionButtonProps {
  as?: "button";
  onClick: () => void;
  disabled?: boolean;
}

type ButtonProps = (LinkButtonProps | ActionButtonProps) & {
  variant?: "primary" | "secondary";
  size?: "sm" | "md" | "lg";
  children: React.ReactNode;
};

function Button(props: ButtonProps) {
  const { variant = "primary", size = "md", children, ...rest } = props;
  const classes = cn(/* ... */);

  if (props.as === "link") {
    return (
      <a href={props.href} target={props.target} className={classes}>
        {children}
      </a>
    );
  }

  return (
    <button onClick={props.onClick} disabled={props.disabled} className={classes}>
      {children}
    </button>
  );
}
```

### Children Patterns

```typescript
// String children only
interface BadgeProps {
  children: string;
}

// ReactNode (any renderable)
interface ContainerProps {
  children: React.ReactNode;
}

// Render function (render props)
interface DataListProps<T> {
  items: T[];
  children: (item: T, index: number) => React.ReactNode;
}

// Named slots via props
interface DialogProps {
  trigger: React.ReactNode;
  title: React.ReactNode;
  description?: React.ReactNode;
  children: React.ReactNode;
  footer?: React.ReactNode;
}
```

## Custom Hooks

### Pattern: useLocalStorage

```typescript
import { useState, useEffect, useCallback } from "react";

function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    if (typeof window === "undefined") return initialValue;
    try {
      const item = window.localStorage.getItem(key);
      return item ? (JSON.parse(item) as T) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setValue = useCallback(
    (value: T | ((prev: T) => T)) => {
      setStoredValue((prev) => {
        const nextValue = value instanceof Function ? value(prev) : value;
        window.localStorage.setItem(key, JSON.stringify(nextValue));
        return nextValue;
      });
    },
    [key]
  );

  const removeValue = useCallback(() => {
    window.localStorage.removeItem(key);
    setStoredValue(initialValue);
  }, [key, initialValue]);

  return [storedValue, setValue, removeValue] as const;
}
```

### Pattern: useDebounce

```typescript
import { useState, useEffect } from "react";

function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}
```

### Pattern: useFetch

```typescript
import { useState, useEffect, useRef } from "react";

interface UseFetchResult<T> {
  data: T | null;
  error: Error | null;
  isLoading: boolean;
}

function useFetch<T>(url: string, options?: RequestInit): UseFetchResult<T> {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const abortControllerRef = useRef<AbortController | null>(null);

  useEffect(() => {
    const abortController = new AbortController();
    abortControllerRef.current = abortController;
    setIsLoading(true);

    fetch(url, { ...options, signal: abortController.signal })
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);
        return res.json() as Promise<T>;
      })
      .then((json) => {
        if (!abortController.signal.aborted) {
          setData(json);
          setError(null);
        }
      })
      .catch((err: unknown) => {
        if (err instanceof Error && err.name !== "AbortError") {
          setError(err);
        }
      })
      .finally(() => {
        if (!abortController.signal.aborted) {
          setIsLoading(false);
        }
      });

    return () => abortController.abort();
  }, [url]); // eslint-disable-line react-hooks/exhaustive-deps

  return { data, error, isLoading };
}
```

### Pattern: useMediaQuery

```typescript
import { useState, useEffect } from "react";

function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    const media = window.matchMedia(query);
    setMatches(media.matches);

    const listener = (event: MediaQueryListEvent) => setMatches(event.matches);
    media.addEventListener("change", listener);
    return () => media.removeEventListener("change", listener);
  }, [query]);

  return matches;
}

// Usage
const isMobile = useMediaQuery("(max-width: 768px)");
const prefersDark = useMediaQuery("(prefers-color-scheme: dark)");
```

### Hook Rules

1. Always prefix with `use`
2. Only call hooks at the top level (never inside conditions or loops)
3. Return a tuple `as const` for positional returns, or an object for named returns
4. Include cleanup in `useEffect` return (abort controllers, event listeners, timers)
5. Explicitly type the return value for complex hooks
6. Document the hook purpose with a JSDoc comment

## State Management Patterns

### Local State: useState

Use for simple, component-scoped state:

```typescript
const [count, setCount] = useState(0);
const [user, setUser] = useState<User | null>(null);
const [items, setItems] = useState<Item[]>([]);
```

### Complex Local State: useReducer

Use when state transitions are complex or interdependent:

```typescript
interface FormState {
  values: Record<string, string>;
  errors: Record<string, string>;
  isSubmitting: boolean;
  isValid: boolean;
}

type FormAction =
  | { type: "SET_FIELD"; field: string; value: string }
  | { type: "SET_ERROR"; field: string; error: string }
  | { type: "CLEAR_ERRORS" }
  | { type: "SUBMIT_START" }
  | { type: "SUBMIT_SUCCESS" }
  | { type: "SUBMIT_FAILURE"; errors: Record<string, string> };

function formReducer(state: FormState, action: FormAction): FormState {
  switch (action.type) {
    case "SET_FIELD":
      return {
        ...state,
        values: { ...state.values, [action.field]: action.value },
        errors: { ...state.errors, [action.field]: "" },
      };
    case "SET_ERROR":
      return {
        ...state,
        errors: { ...state.errors, [action.field]: action.error },
        isValid: false,
      };
    case "CLEAR_ERRORS":
      return { ...state, errors: {}, isValid: true };
    case "SUBMIT_START":
      return { ...state, isSubmitting: true };
    case "SUBMIT_SUCCESS":
      return { ...state, isSubmitting: false };
    case "SUBMIT_FAILURE":
      return { ...state, isSubmitting: false, errors: action.errors, isValid: false };
  }
}
```

### Global State: Zustand

Use for shared state across unrelated components:

```typescript
import { create } from "zustand";
import { persist } from "zustand/middleware";

interface AuthStore {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const useAuthStore = create<AuthStore>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      login: async (email, password) => {
        const res = await fetch("/api/auth/login", {
          method: "POST",
          body: JSON.stringify({ email, password }),
          headers: { "Content-Type": "application/json" },
        });
        const data = await res.json();
        set({ user: data.user, token: data.token });
      },
      logout: () => set({ user: null, token: null }),
    }),
    { name: "auth-storage" }
  )
);

// Usage in components
function UserMenu() {
  const user = useAuthStore((state) => state.user);
  const logout = useAuthStore((state) => state.logout);
  // Select individual fields to avoid unnecessary re-renders
}
```

### Atomic State: Jotai

Use for fine-grained, composable state atoms:

```typescript
import { atom, useAtom, useAtomValue, useSetAtom } from "jotai";

// Primitive atoms
const countAtom = atom(0);
const nameAtom = atom("");

// Derived atom (read-only)
const doubleCountAtom = atom((get) => get(countAtom) * 2);

// Async derived atom
const userAtom = atom(async (get) => {
  const id = get(userIdAtom);
  const res = await fetch(`/api/users/${id}`);
  return res.json() as Promise<User>;
});

// Write-only atom (action)
const incrementAtom = atom(null, (get, set) => {
  set(countAtom, get(countAtom) + 1);
});
```

### When to Use What

| Scenario | Solution |
|----------|----------|
| Toggle, simple counter, form field | `useState` |
| Complex form with validation | `useReducer` |
| Theme, auth, cart (shared across app) | Zustand |
| Many independent atoms, derived state | Jotai |
| Server data (fetching, caching) | TanStack Query |
| URL state | `useSearchParams` (router) |

## Composition Patterns

### Compound Components

Components that share implicit state through context:

```typescript
import { createContext, useContext, useState, type ReactNode } from "react";

interface AccordionContextValue {
  openItems: Set<string>;
  toggle: (id: string) => void;
}

const AccordionContext = createContext<AccordionContextValue | null>(null);

function useAccordion() {
  const context = useContext(AccordionContext);
  if (!context) throw new Error("useAccordion must be used within <Accordion>");
  return context;
}

function Accordion({ children, multiple = false }: { children: ReactNode; multiple?: boolean }) {
  const [openItems, setOpenItems] = useState<Set<string>>(new Set());

  const toggle = (id: string) => {
    setOpenItems((prev) => {
      const next = new Set(multiple ? prev : []);
      if (prev.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  };

  return (
    <AccordionContext.Provider value={{ openItems, toggle }}>
      <div role="region">{children}</div>
    </AccordionContext.Provider>
  );
}

function AccordionItem({ id, trigger, children }: { id: string; trigger: ReactNode; children: ReactNode }) {
  const { openItems, toggle } = useAccordion();
  const isOpen = openItems.has(id);

  return (
    <div>
      <button
        onClick={() => toggle(id)}
        aria-expanded={isOpen}
        aria-controls={`accordion-panel-${id}`}
      >
        {trigger}
      </button>
      {isOpen && (
        <div id={`accordion-panel-${id}`} role="region">
          {children}
        </div>
      )}
    </div>
  );
}

Accordion.Item = AccordionItem;
export { Accordion };
```

### Render Props

Expose internal logic to parent for flexible rendering:

```typescript
interface VirtualListProps<T> {
  items: T[];
  itemHeight: number;
  containerHeight: number;
  children: (item: T, style: React.CSSProperties) => React.ReactNode;
}

function VirtualList<T>({ items, itemHeight, containerHeight, children }: VirtualListProps<T>) {
  const [scrollTop, setScrollTop] = useState(0);
  const startIndex = Math.floor(scrollTop / itemHeight);
  const endIndex = Math.min(startIndex + Math.ceil(containerHeight / itemHeight) + 1, items.length);
  const visibleItems = items.slice(startIndex, endIndex);

  return (
    <div style={{ height: containerHeight, overflow: "auto" }} onScroll={(e) => setScrollTop(e.currentTarget.scrollTop)}>
      <div style={{ height: items.length * itemHeight, position: "relative" }}>
        {visibleItems.map((item, i) =>
          children(item, {
            position: "absolute",
            top: (startIndex + i) * itemHeight,
            height: itemHeight,
            width: "100%",
          })
        )}
      </div>
    </div>
  );
}
```

### Slots via Props

Named content areas without compound component complexity:

```typescript
interface PageLayoutProps {
  header: React.ReactNode;
  sidebar?: React.ReactNode;
  children: React.ReactNode;
  footer?: React.ReactNode;
}

function PageLayout({ header, sidebar, children, footer }: PageLayoutProps) {
  return (
    <div className="flex min-h-screen flex-col">
      <header>{header}</header>
      <div className="flex flex-1">
        {sidebar && <aside className="w-64 border-r">{sidebar}</aside>}
        <main className="flex-1 p-6">{children}</main>
      </div>
      {footer && <footer>{footer}</footer>}
    </div>
  );
}
```

## Error Boundaries

```typescript
import { Component, type ErrorInfo, type ReactNode } from "react";

interface ErrorBoundaryProps {
  children: ReactNode;
  fallback: ReactNode | ((error: Error, reset: () => void) => ReactNode);
}

interface ErrorBoundaryState {
  error: Error | null;
}

class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  state: ErrorBoundaryState = { error: null };

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { error };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error("ErrorBoundary caught:", error, info.componentStack);
  }

  reset = () => this.setState({ error: null });

  render() {
    if (this.state.error) {
      return typeof this.props.fallback === "function"
        ? this.props.fallback(this.state.error, this.reset)
        : this.props.fallback;
    }
    return this.props.children;
  }
}

// Usage
<ErrorBoundary fallback={(error, reset) => (
  <div role="alert">
    <p>Something went wrong: {error.message}</p>
    <button onClick={reset}>Try again</button>
  </div>
)}>
  <MyComponent />
</ErrorBoundary>
```

## Server Components (React 19 / Next.js App Router)

### Server vs. Client Components

```
// Server Component (default in app/ directory) — NO "use client" directive
// Can: fetch data, access backend, read files, use async/await
// Cannot: useState, useEffect, event handlers, browser APIs

// app/users/page.tsx (server component)
async function UsersPage() {
  const users = await db.user.findMany();     // Direct DB access
  return <UserList users={users} />;
}

// Client Component — must have "use client" directive
// Can: useState, useEffect, event handlers, browser APIs
// Cannot: async component, direct DB/filesystem access

// components/user-search.tsx
"use client";
import { useState } from "react";

function UserSearch({ onSearch }: { onSearch: (query: string) => void }) {
  const [query, setQuery] = useState("");
  return <input value={query} onChange={(e) => setQuery(e.target.value)} />;
}
```

### Server Component Patterns

```typescript
// Pass server data to client components via props
// app/dashboard/page.tsx (server)
import { DashboardChart } from "@/components/dashboard-chart"; // client component

async function DashboardPage() {
  const stats = await getStats(); // server-side fetch
  return <DashboardChart data={stats} />;
}

// Streaming with Suspense
import { Suspense } from "react";

async function Page() {
  return (
    <div>
      <h1>Dashboard</h1>
      <Suspense fallback={<ChartSkeleton />}>
        <SlowChart />
      </Suspense>
    </div>
  );
}
```

### When to Use "use client"

Add `"use client"` only when the component needs:
- `useState`, `useReducer`, `useEffect`, `useRef`, `useContext`
- Event handlers (`onClick`, `onChange`, etc.)
- Browser APIs (`window`, `document`, `localStorage`)
- Third-party libraries that use any of the above

**Push "use client" as far down the tree as possible.** Keep layouts and pages as server components; extract interactive pieces into small client components.

## Form Handling

### Controlled Form Pattern

```typescript
"use client";
import { useState, type FormEvent } from "react";

interface ContactForm {
  name: string;
  email: string;
  message: string;
}

function ContactForm() {
  const [values, setValues] = useState<ContactForm>({ name: "", email: "", message: "" });
  const [errors, setErrors] = useState<Partial<ContactForm>>({});

  const validate = (): boolean => {
    const newErrors: Partial<ContactForm> = {};
    if (!values.name.trim()) newErrors.name = "Name is required";
    if (!values.email.includes("@")) newErrors.email = "Valid email required";
    if (!values.message.trim()) newErrors.message = "Message is required";
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!validate()) return;
    await fetch("/api/contact", {
      method: "POST",
      body: JSON.stringify(values),
      headers: { "Content-Type": "application/json" },
    });
  };

  return (
    <form onSubmit={handleSubmit} noValidate>
      <label htmlFor="name">Name</label>
      <input
        id="name"
        value={values.name}
        onChange={(e) => setValues((v) => ({ ...v, name: e.target.value }))}
        aria-invalid={!!errors.name}
        aria-describedby={errors.name ? "name-error" : undefined}
      />
      {errors.name && <p id="name-error" role="alert">{errors.name}</p>}
      {/* ... other fields ... */}
      <button type="submit">Send</button>
    </form>
  );
}
```

### react-hook-form Pattern

```typescript
"use client";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

const contactSchema = z.object({
  name: z.string().min(1, "Name is required"),
  email: z.string().email("Valid email required"),
  message: z.string().min(10, "Message must be at least 10 characters"),
});

type ContactFormValues = z.infer<typeof contactSchema>;

function ContactForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<ContactFormValues>({
    resolver: zodResolver(contactSchema),
  });

  const onSubmit = async (data: ContactFormValues) => {
    await fetch("/api/contact", {
      method: "POST",
      body: JSON.stringify(data),
      headers: { "Content-Type": "application/json" },
    });
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} noValidate>
      <label htmlFor="name">Name</label>
      <input id="name" {...register("name")} aria-invalid={!!errors.name} />
      {errors.name && <p role="alert">{errors.name.message}</p>}

      <label htmlFor="email">Email</label>
      <input id="email" type="email" {...register("email")} aria-invalid={!!errors.email} />
      {errors.email && <p role="alert">{errors.email.message}</p>}

      <label htmlFor="message">Message</label>
      <textarea id="message" {...register("message")} aria-invalid={!!errors.message} />
      {errors.message && <p role="alert">{errors.message.message}</p>}

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? "Sending..." : "Send"}
      </button>
    </form>
  );
}
```

## File Organization

```
src/
├── components/
│   ├── ui/                  # Primitive, reusable UI components
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   ├── card.tsx
│   │   └── index.ts         # Barrel export
│   ├── layout/              # Layout structure components
│   │   ├── header.tsx
│   │   ├── footer.tsx
│   │   └── page-layout.tsx
│   ├── sections/            # Page-level content sections
│   │   ├── hero-section.tsx
│   │   └── features-grid.tsx
│   └── providers/           # Context providers
│       ├── theme-provider.tsx
│       └── auth-provider.tsx
├── hooks/                   # Custom hooks
│   ├── use-local-storage.ts
│   ├── use-debounce.ts
│   └── use-media-query.ts
├── stores/                  # Zustand / Jotai stores
│   ├── auth-store.ts
│   └── cart-store.ts
├── lib/                     # Utilities
│   ├── utils.ts             # cn(), formatters
│   └── validators.ts        # Zod schemas
└── types/                   # Shared TypeScript types
    ├── api.ts
    └── models.ts
```

## Common Mistakes to Avoid

1. **Overusing `useEffect`** -- Derive state during render instead of syncing with effects. If you can calculate it from existing state/props, do so inline.
2. **Missing dependency arrays** -- Always include all dependencies in `useEffect`/`useMemo`/`useCallback`. Use the ESLint rule.
3. **Premature memoization** -- Don't wrap everything in `React.memo`, `useMemo`, or `useCallback`. Only optimize when you have measured a performance problem.
4. **Prop drilling past 2-3 levels** -- Use context or a state library instead.
5. **Putting "use client" on layout components** -- Keep layouts as server components. Extract interactive parts into small client child components.
6. **Inline object/array props** -- `<Comp style={{ color: "red" }} />` creates a new object every render. Hoist to a constant or use `useMemo` if in a hot path.
7. **Not handling loading and error states** -- Every async operation needs loading, success, and error UI.

---

**Skill Version:** 1.0.0
**Last Updated:** 2026-03-11
