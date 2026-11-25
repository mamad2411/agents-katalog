---
name: react
description: "React frontend development skill with TypeScript, Vite, TanStack Query, and Tailwind CSS. Use when implementing React UI components and pages."
---

# React Frontend Development

## Purpose

This skill provides the complete knowledge base for building React frontends in a fullstack Golang + React application. It covers component architecture, state management, API integration, routing, styling, and form handling. The react-dev agent uses this skill to implement UI features that consume the Go backend API.

## Technology Stack

| Technology | Version | Purpose |
|---|---|---|
| React | 18+ | UI library (functional components only) |
| TypeScript | 5.x (strict mode) | Type safety |
| Vite | 5.x | Build tool and dev server |
| TanStack Query | v5 | Server state management |
| React Router | v6 | Client-side routing with lazy loading |
| Tailwind CSS | 3.x | Utility-first styling |
| React Hook Form | 7.x | Form state management |
| zod | 3.x | Schema validation (forms + API responses) |
| axios | 1.x | HTTP client |

## Project Structure

```
src/
├── api/                  # API client and typed endpoint functions
│   ├── client.ts         # Axios instance with interceptors
│   ├── auth.ts           # Auth-related API functions
│   └── [resource].ts     # Per-resource API functions
├── components/           # Reusable UI components
│   ├── ui/               # Primitive UI components (Button, Input, Modal, etc.)
│   ├── layout/           # Layout components (Header, Sidebar, Footer, PageWrapper)
│   └── [feature]/        # Feature-specific composed components
├── context/              # React Context providers
│   ├── AuthContext.tsx    # Auth state (user, token, login/logout)
│   └── [Name]Context.tsx # Feature-specific global state
├── hooks/                # Custom hooks
│   ├── useAuth.ts        # Auth hook (wraps AuthContext)
│   ├── useApi.ts         # Generic API hook patterns
│   └── use[Name].ts      # Feature-specific hooks
├── pages/                # Page-level components (1:1 with routes)
│   ├── HomePage.tsx
│   ├── LoginPage.tsx
│   └── [Feature]Page.tsx
├── routes/               # Route definitions
│   ├── index.tsx         # Route tree with lazy loading
│   └── ProtectedRoute.tsx # Auth guard wrapper
├── styles/               # Global styles
│   ├── globals.css       # Tailwind directives and global overrides
│   └── tailwind.css      # @tailwind base/components/utilities
├── types/                # Shared TypeScript types
│   ├── api.ts            # API request/response types (mirrors backend structs)
│   ├── models.ts         # Domain model types
│   └── common.ts         # Shared utility types
├── utils/                # Pure utility functions
│   ├── format.ts         # Date, currency, string formatters
│   ├── validation.ts     # Zod schemas shared across forms
│   └── constants.ts      # App-wide constants
├── App.tsx               # Root component with providers
├── main.tsx              # Entry point (ReactDOM.createRoot)
└── vite-env.d.ts         # Vite environment type declarations
```

## Key Patterns

### 1. Functional Components with TypeScript

Every component is a typed functional component. Never use class components (except ErrorBoundary). Always define a Props interface.

```tsx
interface UserCardProps {
  user: User;
  onSelect?: (userId: string) => void;
  variant?: "compact" | "full";
}

export function UserCard({ user, onSelect, variant = "full" }: UserCardProps) {
  return (
    <div className="rounded-lg border border-gray-200 p-4">
      <h3 className="text-lg font-semibold">{user.name}</h3>
      {variant === "full" && <p className="text-sm text-gray-600">{user.email}</p>}
      {onSelect && (
        <button
          onClick={() => onSelect(user.id)}
          className="mt-2 rounded bg-blue-600 px-4 py-2 text-sm text-white hover:bg-blue-700"
        >
          Select
        </button>
      )}
    </div>
  );
}
```

### 2. Custom Hooks for Logic Extraction

Extract any non-trivial logic (API calls, computed state, side effects) into custom hooks. Components should contain only rendering logic.

```tsx
// hooks/useUsers.ts
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getUsers, createUser } from "@/api/users";
import type { CreateUserRequest } from "@/types/api";

export function useUsers() {
  return useQuery({
    queryKey: ["users"],
    queryFn: getUsers,
  });
}

export function useCreateUser() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: CreateUserRequest) => createUser(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["users"] });
    },
  });
}
```

### 3. API Client with Typed Functions

The API client is a configured axios instance. Each resource gets its own file with typed functions that match the Go backend contracts exactly.

```tsx
// api/client.ts
import axios from "axios";

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "/api",
  headers: { "Content-Type": "application/json" },
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("token");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);
```

```tsx
// api/users.ts
import { apiClient } from "./client";
import type { User, CreateUserRequest, UpdateUserRequest, PaginatedResponse } from "@/types/api";

export async function getUsers(params?: { page?: number; limit?: number }): Promise<PaginatedResponse<User>> {
  const { data } = await apiClient.get("/users", { params });
  return data;
}

export async function getUserById(id: string): Promise<User> {
  const { data } = await apiClient.get(`/users/${id}`);
  return data;
}

export async function createUser(req: CreateUserRequest): Promise<User> {
  const { data } = await apiClient.post("/users", req);
  return data;
}

export async function updateUser(id: string, req: UpdateUserRequest): Promise<User> {
  const { data } = await apiClient.put(`/users/${id}`, req);
  return data;
}

export async function deleteUser(id: string): Promise<void> {
  await apiClient.delete(`/users/${id}`);
}
```

### 4. TypeScript Types Matching Backend Contracts

Types in `src/types/api.ts` must mirror the Go backend structs field-for-field. Use the PRD/design doc API contracts as the single source of truth. JSON field names from Go struct tags become TypeScript property names.

```tsx
// types/api.ts -- mirrors Go structs exactly
export interface User {
  id: string;
  email: string;
  name: string;
  role: "admin" | "user";
  created_at: string;   // ISO 8601 from Go time.Time
  updated_at: string;
}

export interface CreateUserRequest {
  email: string;
  name: string;
  password: string;
  role?: "admin" | "user";
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  limit: number;
}

export interface ApiError {
  error: string;
  code: string;
  details?: Record<string, string>;
}
```

### 5. State Management Strategy

| State Type | Solution | When to Use |
|---|---|---|
| Server state | TanStack Query | Data from API (lists, details, search results) |
| Global client state | React Context + useReducer | Auth, theme, UI preferences, notifications |
| Local component state | useState | Form inputs, toggles, modals, ephemeral UI state |
| URL state | React Router (useSearchParams) | Filters, pagination, active tabs |
| Form state | React Hook Form | Any form with validation |

Never use Redux, Zustand, or other external state libraries. TanStack Query handles server state; React Context handles the rest.

### 6. Routing with Lazy Loading

```tsx
// routes/index.tsx
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { lazy, Suspense } from "react";
import { ProtectedRoute } from "./ProtectedRoute";
import { AppLayout } from "@/components/layout/AppLayout";

const HomePage = lazy(() => import("@/pages/HomePage"));
const LoginPage = lazy(() => import("@/pages/LoginPage"));
const UsersPage = lazy(() => import("@/pages/UsersPage"));
const UserDetailPage = lazy(() => import("@/pages/UserDetailPage"));
const NotFoundPage = lazy(() => import("@/pages/NotFoundPage"));

function LazyPage({ children }: { children: React.ReactNode }) {
  return (
    <Suspense fallback={<div className="flex h-screen items-center justify-center">Loading...</div>}>
      {children}
    </Suspense>
  );
}

const router = createBrowserRouter([
  {
    path: "/login",
    element: <LazyPage><LoginPage /></LazyPage>,
  },
  {
    path: "/",
    element: <ProtectedRoute><AppLayout /></ProtectedRoute>,
    children: [
      { index: true, element: <LazyPage><HomePage /></LazyPage> },
      { path: "users", element: <LazyPage><UsersPage /></LazyPage> },
      { path: "users/:id", element: <LazyPage><UserDetailPage /></LazyPage> },
    ],
  },
  { path: "*", element: <LazyPage><NotFoundPage /></LazyPage> },
]);

export function AppRouter() {
  return <RouterProvider router={router} />;
}
```

### 7. Tailwind CSS Styling Conventions

- Mobile-first responsive design: start with base styles, add `sm:`, `md:`, `lg:` breakpoints
- Use Tailwind utility classes directly on elements; avoid `@apply` except in `globals.css` for base resets
- Group utilities logically: layout > spacing > sizing > typography > colors > effects
- Component variants via conditional classes with `clsx` or `cn` utility

```tsx
import { clsx } from "clsx";

interface ButtonProps {
  variant?: "primary" | "secondary" | "danger";
  size?: "sm" | "md" | "lg";
  children: React.ReactNode;
  onClick?: () => void;
  disabled?: boolean;
}

export function Button({ variant = "primary", size = "md", children, onClick, disabled }: ButtonProps) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={clsx(
        "inline-flex items-center justify-center rounded-md font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2",
        {
          "bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500": variant === "primary",
          "bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-500": variant === "secondary",
          "bg-red-600 text-white hover:bg-red-700 focus:ring-red-500": variant === "danger",
          "px-3 py-1.5 text-sm": size === "sm",
          "px-4 py-2 text-sm": size === "md",
          "px-6 py-3 text-base": size === "lg",
          "cursor-not-allowed opacity-50": disabled,
        }
      )}
    >
      {children}
    </button>
  );
}
```

### 8. Form Handling with React Hook Form + Zod

```tsx
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

const createUserSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters"),
  email: z.string().email("Invalid email address"),
  password: z.string().min(8, "Password must be at least 8 characters"),
  role: z.enum(["admin", "user"]).default("user"),
});

type CreateUserFormData = z.infer<typeof createUserSchema>;

export function CreateUserForm({ onSubmit }: { onSubmit: (data: CreateUserFormData) => void }) {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<CreateUserFormData>({
    resolver: zodResolver(createUserSchema),
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label htmlFor="name" className="block text-sm font-medium text-gray-700">Name</label>
        <input
          id="name"
          {...register("name")}
          className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
        />
        {errors.name && <p className="mt-1 text-sm text-red-600">{errors.name.message}</p>}
      </div>
      {/* Repeat pattern for email, password, role fields */}
      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 disabled:opacity-50"
      >
        {isSubmitting ? "Creating..." : "Create User"}
      </button>
    </form>
  );
}
```

### 9. Error Boundaries

Wrap page-level components in error boundaries. Provide a user-friendly fallback and a retry mechanism. This is the one allowed exception to the no class components rule.

```tsx
import { Component, type ErrorInfo, type ReactNode } from "react";

interface ErrorBoundaryProps {
  children: ReactNode;
  fallback?: ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("ErrorBoundary caught:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div className="flex min-h-[400px] flex-col items-center justify-center">
          <h2 className="text-xl font-semibold text-gray-900">Something went wrong</h2>
          <p className="mt-2 text-sm text-gray-600">{this.state.error?.message}</p>
          <button
            onClick={() => this.setState({ hasError: false, error: null })}
            className="mt-4 rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
          >
            Try Again
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}
```

### 10. Environment Variables

All environment variables are accessed via `import.meta.env` (Vite convention). Custom variables must be prefixed with `VITE_`.

```tsx
// vite-env.d.ts
/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_URL: string;
  readonly VITE_APP_TITLE: string;
  readonly VITE_ENABLE_MOCKS: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
```

```
# .env
VITE_API_URL=http://localhost:8080/api
VITE_APP_TITLE=MyApp
```

### 11. Responsive Design (Mobile-First)

Always start with mobile styles as the default, then layer on larger breakpoints:

```tsx
<div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
  {items.map((item) => (
    <Card key={item.id} item={item} />
  ))}
</div>
```

Breakpoint reference: `sm` (640px), `md` (768px), `lg` (1024px), `xl` (1280px), `2xl` (1536px).

### 12. Loading and Empty States

Every data-fetching component must handle four states: loading, error, empty, and success.

```tsx
export function UsersList() {
  const { data, isLoading, error } = useUsers();

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;
  if (!data?.data.length) return <EmptyState message="No users found" />;

  return (
    <div className="space-y-4">
      {data.data.map((user) => (
        <UserCard key={user.id} user={user} />
      ))}
    </div>
  );
}
```

## Conventions

1. **No `any` type** -- use `unknown` and narrow, or define proper types. The only acceptable `any` is in third-party library type workarounds (document with `// eslint-disable-next-line` comment).
2. **Named exports** for all components and hooks. Default exports only for page components (required for `React.lazy`).
3. **File naming**: PascalCase for components (`UserCard.tsx`), camelCase for hooks/utils (`useAuth.ts`, `format.ts`).
4. **One component per file** unless tightly coupled sub-components are small (< 30 lines).
5. **Props interface** must be defined directly above the component, named `[ComponentName]Props`.
6. **Barrel exports** (`index.ts`) only at the top level of `components/ui/`, `hooks/`, `utils/`. Not in feature directories.
7. **Absolute imports** using `@/` path alias configured in `vite.config.ts` and `tsconfig.json`.
8. **No inline styles**. Use Tailwind classes exclusively.
9. **Accessibility basics**: all `<img>` have `alt`, all interactive elements are focusable, form inputs have `<label>`, use semantic HTML (`<nav>`, `<main>`, `<section>`, `<article>`).
10. **Every API response type** must have a corresponding zod schema if used in form validation.

## Vite Configuration

```ts
// vite.config.ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    port: 3000,
    proxy: {
      "/api": {
        target: "http://localhost:8080",
        changeOrigin: true,
      },
    },
  },
});
```

## Knowledge Strategy

- **Patterns to capture:** Reusable component patterns (data tables, forms, modals), API integration patterns, complex TanStack Query configurations (optimistic updates, infinite scroll), auth flow patterns.
- **Examples to collect:** Successful component implementations, tricky TypeScript type patterns, responsive layout solutions, error handling patterns.
- **Update permission:** Agents may freely add/update files in `references/`. Changes to `SKILL.md` or `scripts/` require user approval.
