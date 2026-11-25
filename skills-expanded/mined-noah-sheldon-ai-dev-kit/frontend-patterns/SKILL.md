---
name: frontend-patterns
description: React 19 and Next.js patterns including component architecture, state management, performance, styling, forms, testing, Chrome extension parity, DX tooling, micro-frontends, UI state machines, and AI chat surface composition.
origin: AI Dev Kit
---

# Frontend Patterns

Production-grade React 19 and Next.js patterns: component architecture (hooks vs server
components), state management (React Query, Zustand, signals), performance optimization
(memoization, useTransition, streaming SSR, bundle splitting), styling (Tailwind, CSS
Modules, design tokens), forms (React Hook Form + Zod), testing (RTL + Vitest + Storybook),
Chrome extension parity, DX tooling, micro-frontends, UI state machines, and AI chat
surface composition with streaming UX heuristics.

## When to Use

- Building or refactoring React/Next.js applications with modern patterns.
- Choosing between server components, client components, hooks, and context boundaries.
- Implementing state management with React Query (server state) or Zustand (UI state).
- Optimizing performance with memoization, transitions, streaming, and code splitting.
- Styling with Tailwind CSS, CSS Modules, design tokens, and responsive grids.
- Building forms with React Hook Form, Zod validation, and accessibility.
- Testing components with React Testing Library, Vitest, and Storybook.
- Sharing component libraries between web apps and WXT Chrome extensions.
- Designing AI chat surfaces with streaming conversations and heuristic-driven UX.
- Setting up DX tooling: ESLint, TypeScript, turborepo, shadcn/ui integration.

## Core Concepts

### 1. Component Architecture

**Server Components vs Client Components:**

```tsx
// app/dashboard/page.tsx — Server Component (default)
// Runs on server, zero JS sent to client
import { Suspense } from "react";
import { getDashboardData } from "@/lib/api";
import { RevenueChart } from "@/components/charts/revenue-chart";
import { UserTable } from "@/components/users/user-table";
import { DashboardSkeleton } from "@/components/ui/skeleton";

export default async function DashboardPage() {
  // Direct database/API call on the server — no useEffect, no useState
  const data = await getDashboardData();

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Dashboard</h1>

      {/* Streaming: chart loads independently */}
      <Suspense fallback={<DashboardSkeleton />}>
        <RevenueChart initialData={data.revenue} />
      </Suspense>

      <UserTable users={data.users} />
    </div>
  );
}
```

```tsx
// app/dashboard/revenue-chart.tsx — "use client" directive
// Only this component + its imports go to the client
"use client";

import { LineChart, Line, XAxis, YAxis, Tooltip } from "recharts";
import { useState } from "react";

interface RevenueChartProps {
  initialData: Array<{ month: string; revenue: number }>;
}

export function RevenueChart({ initialData }: RevenueChartProps) {
  const [hoveredMonth, setHoveredMonth] = useState<string | null>(null);

  return (
    <div className="rounded-lg border p-4">
      <LineChart data={initialData}>
        <XAxis dataKey="month" />
        <YAxis />
        <Tooltip
          formatter={(value: number) => [`$${value.toLocaleString()}`, "Revenue"]}
          labelFormatter={(label) => `Month: ${label}`}
        />
        <Line
          type="monotone"
          dataKey="revenue"
          stroke="#3b82f6"
          strokeWidth={2}
          dot={false}
          activeDot={{ r: 6 }}
          onMouseEnter={(_, index) => setHoveredMonth(initialData[index]?.month)}
        />
      </LineChart>
      {hoveredMonth && (
        <p className="mt-2 text-sm text-muted-foreground">Viewing: {hoveredMonth}</p>
      )}
    </div>
  );
}
```

**Co-Location Pattern:**

```
components/
├── dashboard/
│   ├── dashboard-page.tsx        # Server component entry
│   ├── dashboard-chart.tsx       # Client component (co-located)
│   ├── dashboard-stats.tsx
│   ├── dashboard-skeleton.tsx
│   └── index.ts                  # Barrel export (optional)
├── users/
│   ├── user-table.tsx
│   ├── user-row.tsx
│   ├── user-actions.tsx
│   └── use-user-actions.ts       # Hook co-located with consumers
└── ui/                           # Shared primitive components
    ├── button.tsx
    ├── dialog.tsx
    ├── input.tsx
    └── skeleton.tsx
```

**Context Boundaries — Minimize Re-renders:**

```tsx
// DON'T — one context causes re-render of entire app
const AppContext = createContext<{ user: User; theme: string; lang: string }>(...);

// DO — split contexts by concern
const UserContext = createContext<User | null>(null);
const ThemeContext = createContext<Theme>("light");
const LocaleContext = createContext<string>("en");

// Even better — use Zustand for frequently-changing UI state
import { create } from "zustand";

interface UIStore {
  sidebarOpen: boolean;
  toggleSidebar: () => void;
  selectedItems: Set<string>;
  selectItem: (id: string) => void;
  clearSelection: () => void;
}

const useUIStore = create<UIStore>((set) => ({
  sidebarOpen: false,
  toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),
  selectedItems: new Set(),
  selectItem: (id) =>
    set((s) => {
      const next = new Set(s.selectedItems);
      next.has(id) ? next.delete(id) : next.add(id);
      return { selectedItems: next };
    }),
  clearSelection: () => set({ selectedItems: new Set() }),
}));

// Select only what you need — no unnecessary re-renders
function SidebarToggle() {
  const toggle = useUIStore((s) => s.toggleSidebar); // Only re-renders if toggle changes (never)
  return <button onClick={toggle}>Toggle</button>;
}
```

### 2. State Management

**React Query — Server State:**

```tsx
// lib/query-keys.ts
export const queryKeys = {
  users: {
    all: ["users"] as const,
    lists: () => [...queryKeys.users.all, "list"] as const,
    list: (filters: UserFilters) => [...queryKeys.users.lists(), filters] as const,
    details: () => [...queryKeys.users.all, "detail"] as const,
    detail: (id: string) => [...queryKeys.users.details(), id] as const,
  },
} as const;

// hooks/use-users.ts
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { queryKeys } from "@/lib/query-keys";
import { fetchUsers, createUser, type User, type UserFilters } from "@/lib/api";

export function useUsers(filters: UserFilters) {
  return useQuery({
    queryKey: queryKeys.users.list(filters),
    queryFn: () => fetchUsers(filters),
    staleTime: 1000 * 60 * 5, // 5 minutes
    gcTime: 1000 * 60 * 30,   // 30 minutes (formerly cacheTime)
  });
}

export function useCreateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createUser,
    onMutate: async (newUser) => {
      // Optimistic update
      await queryClient.cancelQueries({ queryKey: queryKeys.users.lists() });
      const previous = queryClient.getQueryData(queryKeys.users.lists());

      queryClient.setQueryData(queryKeys.users.lists(), (old: User[] | undefined) => [
        ...(old ?? []),
        { ...newUser, id: crypto.randomUUID(), createdAt: new Date().toISOString() },
      ]);

      return { previous };
    },
    onError: (_err, _newUser, context) => {
      // Rollback on failure
      queryClient.setQueryData(queryKeys.users.lists(), context?.previous);
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.users.lists() });
    },
  });
}
```

**Zustand — UI State:**

```tsx
// stores/chat-store.ts
import { create } from "zustand";
import { persist } from "zustand/middleware";

export interface ChatMessage {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  streaming?: boolean;
  timestamp: Date;
}

interface ChatStore {
  messages: ChatMessage[];
  isStreaming: boolean;
  currentConversationId: string | null;
  addMessage: (message: Omit<ChatMessage, "id" | "timestamp">) => void;
  updateStreamingMessage: (id: string, content: string, done: boolean) => void;
  clearMessages: () => void;
  setConversationId: (id: string) => void;
}

export const useChatStore = create<ChatStore>()(
  persist(
    (set) => ({
      messages: [],
      isStreaming: false,
      currentConversationId: null,

      addMessage: (msg) =>
        set((s) => ({
          messages: [
            ...s.messages,
            { ...msg, id: crypto.randomUUID(), timestamp: new Date() },
          ],
        })),

      updateStreamingMessage: (id, content, done) =>
        set((s) => ({
          messages: s.messages.map((m) =>
            m.id === id ? { ...m, content, streaming: !done } : m,
          ),
          isStreaming: !done,
        })),

      clearMessages: () => set({ messages: [], isStreaming: false }),
      setConversationId: (id) => set({ currentConversationId: id }),
    }),
    {
      name: "chat-storage",
      partialize: (s) => ({
        messages: s.messages.slice(-50), // Only persist last 50 messages
        currentConversationId: s.currentConversationId,
      }),
    },
  ),
);
```

### 3. Performance Optimization

**Memoization — When and When Not To:**

```tsx
import { memo, useMemo, useCallback, useTransition } from "react";

// GOOD — memo when component re-renders often with same props
const ExpensiveRow = memo(function ExpensiveRow({ data }: { data: RowData }) {
  // This component is expensive to render — memo prevents wasted work
  return <tr>{/* ... */}</tr>;
});

// BAD — memo on trivial components
const Label = memo(({ text }: { text: string }) => <span>{text}</span>); // Overhead > benefit

// useMemo for expensive computations
const sortedUsers = useMemo(
  () => [...users].sort((a, b) => a.name.localeCompare(b.name)),
  [users], // Only re-sort when users array changes
);

// useCallback for stable references (passed to memo children or deps arrays)
const handleDelete = useCallback(
  (id: string) => {
    deleteUser(id);
    queryClient.invalidateQueries({ queryKey: queryKeys.users.lists() });
  },
  [queryClient],
);

// useTransition — keep UI responsive during expensive updates
function SearchResults({ query }: { query: string }) {
  const [results, setResults] = useState<Result[]>([]);
  const [isPending, startTransition] = useTransition();

  const handleSearch = (value: string) => {
    startTransition(() => {
      // Expensive filter — won't block typing
      const filtered = heavyFilter(allItems, value);
      setResults(filtered);
    });
  };

  return (
    <div>
      <input onChange={(e) => handleSearch(e.target.value)} />
      {isPending && <Spinner />}
      <ResultsList results={results} />
    </div>
  );
}
```

**Bundle Splitting:**

```tsx
// Dynamic import for route-level code splitting
import dynamic from "next/dynamic";

// Heavy chart component — loaded on demand
const RevenueChart = dynamic(
  () => import("@/components/charts/revenue-chart").then((m) => m.RevenueChart),
  {
    loading: () => <ChartSkeleton />,
    ssr: false, // Charts don't need server rendering
  },
);

// Admin panel — only loaded when user navigates to /admin
const AdminPanel = dynamic(() => import("@/components/admin/admin-panel"), {
  loading: () => <PanelSkeleton />,
});

// Next.js automatic route-level splitting
// app/admin/page.tsx — automatically split from main bundle
```

**Streaming SSR:**

```tsx
// app/layout.tsx
import { Suspense } from "react";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        {/* Shell renders immediately */}
        <Header />
        <Suspense fallback={<SidebarSkeleton />}>
          <Sidebar /> {/* Suspended until data fetches */}
        </Suspense>
        <main>{children}</main>
        <Suspense fallback={null}>
          <Analytics /> {/* Non-blocking — renders when ready */}
        </Suspense>
      </body>
    </html>
  );
}
```

### 4. Styling — Tailwind, CSS Modules, Design Tokens

**Tailwind Best Practices:**

```tsx
// Use Tailwind utility classes with design token aliases
// tailwind.config.ts
import type { Config } from "tailwindcss";

export default {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--color-border))",
        background: "hsl(var(--color-background))",
        foreground: "hsl(var(--color-foreground))",
        primary: {
          DEFAULT: "hsl(var(--color-primary))",
          foreground: "hsl(var(--color-primary-foreground))",
          muted: "hsl(var(--color-primary-muted))",
        },
        destructive: {
          DEFAULT: "hsl(var(--color-destructive))",
          foreground: "hsl(var(--color-destructive-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
    },
  },
  plugins: [require("tailwindcss-animate"), require("@tailwindcss/forms")],
} satisfies Config;
```

```tsx
// components/ui/card.tsx — Reusable card with Tailwind
import { cn } from "@/lib/utils";

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "elevated" | "outline";
}

export function Card({ className, variant = "default", ...props }: CardProps) {
  return (
    <div
      className={cn(
        "rounded-lg border bg-card text-card-foreground shadow-sm",
        {
          "border-border bg-card": variant === "default",
          "border-border bg-card shadow-lg": variant === "elevated",
          "border-2 border-primary bg-transparent shadow-none": variant === "outline",
        },
        className,
      )}
      {...props}
    />
  );
}

// Responsive grid with Tailwind
<div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
  {items.map((item) => (
    <Card key={item.id}>
      <ItemCard item={item} />
    </Card>
  ))}
</div>
```

**CSS Modules for Component-Specific Styles:**

```tsx
// components/hero/hero.module.css
.hero {
  position: relative;
  min-height: 60vh;
  display: grid;
  place-items: center;
  overflow: hidden;
}

.hero::before {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, var(--color-primary) 0%, transparent 60%);
  opacity: 0.1;
}

.title {
  font-size: clamp(2rem, 5vw, 4rem);
  font-weight: 800;
  letter-spacing: -0.02em;
  line-height: 1.1;
}
```

```tsx
// components/hero/hero.tsx
import styles from "./hero.module.css";

export function Hero({ title, subtitle }: HeroProps) {
  return (
    <section className={styles.hero}>
      <div className="text-center">
        <h1 className={styles.title}>{title}</h1>
        <p className="mt-4 text-lg text-muted-foreground">{subtitle}</p>
      </div>
    </section>
  );
}
```

### 5. Forms — React Hook Form + Zod

```tsx
// schemas/user-schema.ts
import { z } from "zod";

export const userFormSchema = z.object({
  email: z.string().email("Invalid email address").min(1).max(255),
  name: z.string().min(1, "Name is required").max(150),
  password: z
    .string()
    .min(8, "Password must be at least 8 characters")
    .max(128)
    .regex(/[A-Z]/, "Password must contain an uppercase letter")
    .regex(/\d/, "Password must contain a number"),
  role: z.enum(["user", "admin", "viewer"]).default("user"),
  notifications: z.boolean().default(true),
});

export type UserFormValues = z.infer<typeof userFormSchema>;

// components/users/user-form.tsx
"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { userFormSchema, type UserFormValues } from "@/schemas/user-schema";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { useCreateUser } from "@/hooks/use-users";

export function UserForm() {
  const form = useForm<UserFormValues>({
    resolver: zodResolver(userFormSchema),
    defaultValues: {
      email: "",
      name: "",
      password: "",
      role: "user",
      notifications: true,
    },
    mode: "onChange", // Validate on every change (progressive enhancement)
  });

  const mutation = useCreateUser();

  const onSubmit = async (values: UserFormValues) => {
    await mutation.mutateAsync(values);
    form.reset();
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input
                  type="email"
                  placeholder="user @example.com"
                  autoComplete="email"
                  aria-describedby="email-error"
                  {...field}
                />
              </FormControl>
              <FormMessage id="email-error" />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Name</FormLabel>
              <FormControl>
                <Input placeholder="Jane Doe" autoComplete="name" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <Button type="submit" disabled={mutation.isPending || !form.formState.isValid}>
          {mutation.isPending ? "Creating..." : "Create User"}
        </Button>

        {mutation.error && (
          <p role="alert" className="text-sm text-destructive">
            {mutation.error.message}
          </p>
        )}
      </form>
    </Form>
  );
}
```

### 6. Testing — RTL + Vitest + Storybook

**React Testing Library + Vitest:**

```tsx
// components/users/__tests__/user-table.test.tsx
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { http, HttpResponse } from "msw";
import { setupServer } from "msw/node";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { UserTable } from "../user-table";

const server = setupServer(
  http.get("/api/v1/users", () =>
    HttpResponse.json({
      success: true,
      data: {
        items: [
          { id: "1", email: "a @x.com", name: "Alice", isActive: true },
          { id: "2", email: "b @x.com", name: "Bob", isActive: false },
        ],
        meta: { total: 2, page: 1, pageSize: 20, pages: 1 },
      },
    }),
  ),
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

function renderWithProviders(ui: React.ReactElement) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false, gcTime: 0 } },
  });
  return render(
    <QueryClientProvider client={queryClient}>{ui}</QueryClientProvider>,
  );
}

describe("UserTable", () => {
  it("renders user list from API", async () => {
    renderWithProviders(<UserTable />);

    // Loading state
    expect(screen.getByText(/loading/i)).toBeInTheDocument();

    // Data loaded
    await waitFor(() => {
      expect(screen.getByText("Alice")).toBeInTheDocument();
      expect(screen.getByText("Bob")).toBeInTheDocument();
    });

    expect(screen.getByText("a @x.com")).toBeInTheDocument();
  });

  it("shows deactivation confirmation", async () => {
    const user = userEvent.setup();
    renderWithProviders(<UserTable />);

    await waitFor(() => expect(screen.getByText("Bob")).toBeInTheDocument());

    const deactivateBtn = screen.getByRole("button", { name: /deactivate bob/i });
    await user.click(deactivateBtn);

    expect(screen.getByText(/confirm deactivation/i)).toBeInTheDocument();
  });

  it("handles empty state gracefully", async () => {
    server.use(
      http.get("/api/v1/users", () =>
        HttpResponse.json({ success: true, data: { items: [], meta: { total: 0 } } }),
      ),
    );

    renderWithProviders(<UserTable />);
    await waitFor(() => {
      expect(screen.getByText(/no users found/i)).toBeInTheDocument();
    });
  });
});
```

**Storybook — Story-Driven Development:**

```tsx
// components/ui/button.stories.tsx
import type { Meta, StoryObj } from "@storybook/react";
import { Button } from "./button";

const meta: Meta<typeof Button> = {
  title: "UI/Button",
  component: Button,
  tags: ["autodocs"],
  argTypes: {
    variant: {
      control: "select",
      options: ["default", "destructive", "outline", "secondary", "ghost", "link"],
    },
    size: {
      control: "select",
      options: ["default", "sm", "lg", "icon"],
    },
  },
  args: {
    children: "Button",
    disabled: false,
  },
};

export default meta;
type Story = StoryObj<typeof Button>;

export const Default: Story = {};

export const Destructive: Story = {
  args: { variant: "destructive", children: "Delete" },
};

export const Loading: Story = {
  args: { disabled: true, children: "Loading..." },
};

export const WithIcon: Story = {
  args: {
    children: (
      <>
        <PlusIcon className="h-4 w-4" />
        Add User
      </>
    ),
  },
};
```

### 7. Chrome Extension Parity — Shared Component Libraries

```
packages/
├── ui/                          # Shared component library
│   ├── src/
│   │   ├── components/
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── dialog.tsx
│   │   │   ├── input.tsx
│   │   │   └── toast.tsx
│   │   ├── hooks/
│   │   │   ├── use-toast.ts
│   │   │   └── use-media-query.ts
│   │   ├── styles/
│   │   │   ├── globals.css      # Tailwind + design tokens
│   │   │   └── tokens.css       # CSS custom properties
│   │   └── index.ts             # Public API
│   ├── package.json
│   └── tsconfig.json
│
apps/
├── web/                         # Next.js web app
│   ├── app/
│   └── components/              # Web-specific wrappers
│       └── uses @ai-dev-kit/ui
│
└── extension/                   # WXT Chrome extension
    ├── entrypoints/
    │   ├── popup/               # Uses @ai-dev-kit/ui components
    │   ├── options/
    │   └── content/
    └── components/              # Extension-specific UI
        └── uses @ai-dev-kit/ui
```

```json
// packages/ui/package.json
{
  "name": "@ai-dev-kit/ui",
  "version": "1.0.0",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": "./dist/index.js",
      "types": "./dist/index.d.ts"
    },
    "./styles.css": "./dist/styles.css"
  },
  "peerDependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0"
  }
}
```

### 8. DX — ESLint, TypeScript, Turborepo, shadcn/ui

**ESLint Config (React 19):**

```js
// eslint.config.js
import js from "@eslint/js";
import tseslint from "typescript-eslint";
import react from "eslint-plugin-react";
import reactHooks from "eslint-plugin-react-hooks";
import nextPlugin from "@next/eslint-plugin-next";

export default tseslint.config(
  js.configs.recommended,
  ...tseslint.configs.recommendedTypeChecked,
  {
    files: ["**/*.{ts,tsx}"],
    languageOptions: {
      parserOptions: {
        project: true,
        tsconfigRootDir: import.meta.dirname,
      },
    },
    plugins: {
      react,
      "react-hooks": reactHooks,
      "@next/next": nextPlugin,
    },
    rules: {
      ...reactHooks.configs.recommended.rules,
      "@next/next/no-html-link-for-pages": "error",
      "react/react-in-jsx-scope": "off", // React 17+ JSX transform
      "@typescript-eslint/no-unused-vars": ["warn", { argsIgnorePattern: "^_" }],
      "@typescript-eslint/consistent-type-imports": "error",
      "@typescript-eslint/no-misused-promises": ["error", { checksVoidReturn: false }],
    },
  },
  {
    ignores: ["node_modules", ".next", "dist", "build"],
  },
);
```

**Turborepo Cache Configuration:**

```js
// turbo.json
{
  "$schema": "https://turbo.build/schema.json",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": [".next/**", "!.next/cache/**", "dist/**"],
      "cache": true
    },
    "lint": {
      "cache": true
    },
    "type-check": {
      "cache": true
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": ["coverage/**"],
      "cache": true
    },
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

**shadcn/ui Integration:**

```bash
# Initialize shadcn/ui in monorepo
npx shadcn@latest init

# Add components (goes to packages/ui or apps/web/components/ui)
npx shadcn@latest add button dialog input form toast

# Configure for shared package
# components.json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.ts",
    "css": "packages/ui/src/styles/globals.css",
    "baseColor": "slate",
    "cssVariables": true
  },
  "aliases": {
    "components": "@ai-dev-kit/ui/components",
    "utils": "@ai-dev-kit/ui/lib/utils"
  }
}
```

### 9. Architecture Patterns

**Micro-Frontends vs Modules:**

```
// Module Federation (micro-frontend) — use when:
// - Independent teams deploy independently
// - Different release cycles per feature area
// - Cross-app component sharing is needed

// Module-based monorepo (turborepo) — use when:
// - Single team or closely coordinated teams
// - Shared design system + utilities
// - Consistent release cycle
// RECOMMENDED for most teams — simpler, less operational overhead
```

**UI State Machines:**

```tsx
// use-request-state.ts — Finite state machine for async operations
type RequestState<D> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: D }
  | { status: "error"; error: Error };

function useRequestState<D>(): [RequestState<D>, (action: Action<D>) => void] {
  const [state, dispatch] = useReducer(requestReducer, { status: "idle" });

  const request = useCallback(async (fn: () => Promise<D>) => {
    dispatch({ type: "START" });
    try {
      const data = await fn();
      dispatch({ type: "SUCCESS", data });
    } catch (error) {
      dispatch({ type: "ERROR", error: error as Error });
    }
  }, []);

  const reset = useCallback(() => dispatch({ type: "RESET" }), []);

  return [state, { request, reset }];
}

// Usage
function UserProfile({ userId }: { userId: string }) {
  const [state, actions] = useRequestState<User>();

  useEffect(() => {
    actions.request(() => fetchUser(userId));
  }, [userId, actions.request]);

  switch (state.status) {
    case "idle":
    case "loading":
      return <UserSkeleton />;
    case "error":
      return <ErrorBanner message={state.error.message} onRetry={actions.request} />;
    case "success":
      return <UserCard user={state.data} />;
  }
}
```

**AI Chat Surface Composition:**

```tsx
// components/chat/chat-surface.tsx
"use client";

import { useRef, useEffect } from "react";
import { useChatStore } from "@/stores/chat-store";
import { ChatMessage } from "./chat-message";
import { ChatInput } from "./chat-input";
import { StreamingIndicator } from "./streaming-indicator";
import { useStreamingCompletion } from "./use-streaming-completion";

export function ChatSurface() {
  const { messages, isStreaming } = useChatStore();
  const bottomRef = useRef<HTMLDivElement>(null);
  const { completeStream } = useStreamingCompletion();

  // Auto-scroll on new messages
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages.length, messages[messages.length - 1]?.content]);

  return (
    <div className="flex h-full flex-col">
      {/* Message list */}
      <div className="flex-1 overflow-y-auto px-4 py-6" role="log" aria-live="polite">
        {messages.length === 0 ? (
          <EmptyState />
        ) : (
          messages.map((msg) => <ChatMessage key={msg.id} message={msg} />)
        )}
        {isStreaming && <StreamingIndicator />}
        <div ref={bottomRef} />
      </div>

      {/* Input — always visible */}
      <div className="border-t bg-background p-4">
        <ChatInput
          onSubmit={completeStream}
          disabled={isStreaming}
        />
      </div>
    </div>
  );
}
```

**UX Heuristics for Streaming Conversations:**

```tsx
// 1. Stream tokens as they arrive — no waiting for full response
// 2. Show typing indicator within 300ms if no tokens received
// 3. Provide cancel/stop button during streaming
// 4. Preserve scroll position at bottom during streaming
// 5. Show partial content with syntax highlighting as it arrives
// 6. Distinguish streaming from complete (e.g., cursor blink)
// 7. Handle errors gracefully — show retry option
// 8. Rate-limit DOM updates — batch token renders at 60fps

// components/chat/use-streaming-completion.ts
export function useStreamingCompletion() {
  const { addMessage, updateStreamingMessage } = useChatStore();
  const abortControllerRef = useRef<AbortController | null>(null);

  const completeStream = useCallback(async (prompt: string) => {
    // Add user message immediately
    addMessage({ role: "user", content: prompt });

    // Create placeholder for assistant response
    const assistantId = crypto.randomUUID();
    addMessage({ role: "assistant", content: "", streaming: true });

    abortControllerRef.current = new AbortController();

    try {
      const response = await fetch("/api/v1/chat/completions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt, stream: true }),
        signal: abortControllerRef.current.signal,
      });

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      let accumulated = "";

      while (true) {
        const { done, value } = await reader!.read();
        if (done) break;

        const chunk = decoder.decode(value);
        // Parse SSE stream
        const lines = chunk.split("\n");
        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const data = JSON.parse(line.slice(6));
            if (data.content) {
              accumulated += data.content;
              updateStreamingMessage(assistantId, accumulated, false);
            }
          }
        }
      }

      // Mark complete
      updateStreamingMessage(assistantId, accumulated, true);
    } catch (error) {
      if (error instanceof DOMException && error.name === "AbortError") {
        // User cancelled — leave partial content
        updateStreamingMessage(assistantId, "", true);
      } else {
        // Error state
        updateStreamingMessage(assistantId, "Error generating response.", true);
      }
    }
  }, [addMessage, updateStreamingMessage]);

  const cancelStream = useCallback(() => {
    abortControllerRef.current?.abort();
  }, []);

  return { completeStream, cancelStream };
}
```

## Anti-Patterns

- **Overusing `useContext` for frequently-changing state** — causes full-tree re-renders; use Zustand selectors.
- **Passing props deeper than 3 levels** — compose components or use context/Zustand.
- **`useEffect` for data fetching in client components** — use React Query or server components instead.
- **`memo()` on every component** — profiling shows most components don't need it; adds overhead.
- **Inline object/array props** — `{...{a: 1}}` creates new reference every render, breaks `memo`.
- **Not using `"use client"` boundary explicitly** — Next.js App Router defaults to server; mark client components at the leaf.
- **Tailwind class soup in large components** — extract to sub-components or use `cn()` utility.
- **Uncontrolled forms in complex UIs** — React Hook Form + Zod gives validation, types, and accessibility.
- **Testing implementation details** — test what the user sees and does, not internal state.
- **Duplicating UI between web and extension** — extract shared components to a monorepo package.
- **Not setting `gcTime` (cacheTime) on React Query** — causes memory leaks with unlimited cache growth.
- **Missing `aria-live` on streaming regions** — screen readers won't announce new content.
- **Blocking main thread with heavy computations** — use Web Workers or `useTransition`.

## Best Practices

1. **Server components by default** — only add `"use client"` when you need interactivity.
2. **React Query for server state** — caching, deduping, optimistic updates, background refetch.
3. **Zustand for UI state** — lightweight, selector-based, no provider needed.
4. **Co-locate files with consumers** — keep components, hooks, tests, and stories together.
5. **Tailwind with CSS variables** — design tokens for theming, dark mode, and consistency.
6. **`cn()` utility for conditional classes** — `clsx` + `tailwind-merge` for conflict resolution.
7. **React Hook Form + Zod** — type-safe validation with progressive enhancement.
8. **RTL queries by role/text** — `getByRole`, `getByText`, not `getByTestId` unless necessary.
9. **MSW for API mocking** — intercept at network layer, works with RTL and E2E.
10. **Storybook for component catalog** — every UI primitive gets a story with variants.
11. **Dynamic imports for heavy components** — charts, editors, maps behind `Suspense`.
12. **useTransition for expensive renders** — keep input responsive during list filtering.
13. **Stream SSE responses for AI chat** — token-by-token rendering with abort support.
14. **`aria-live="polite"` on streaming regions** — accessible screen reader announcements.
15. **Turborepo for monorepos** — cached builds, parallel dev, consistent tooling.
16. **shadcn/ui as component baseline** — copy (not install) for full customization control.
17. **State machines for async flows** — explicit `idle → loading → success/error` eliminates edge cases.
18. **Scroll anchoring for chat** — `scrollIntoView({ behavior: "smooth" })` on new messages.
19. **Cancel streaming on unmount** — abort controller in `useEffect` cleanup.
20. **Design tokens as CSS custom properties** — single source of truth for colors, spacing, radii.

## Related Skills

- `backend-patterns` — FastAPI architecture, API design, error contracts
- `python-testing` — Pytest patterns, coverage, AI regression testing
- `wxt-chrome-extension` — WXT framework, Manifest V3, extension-specific UI
- `frontend-design` — Design quality, visual hierarchy, modern minimal UI
- `tdd-workflow` — Test-driven development, RED-GREEN-REFACTOR
- `e2e-testing` — Playwright end-to-end patterns
- `api-design` — API contracts, versioning, OpenAPI schemas
- `coding-standards` — Code style, linting, formatting conventions
