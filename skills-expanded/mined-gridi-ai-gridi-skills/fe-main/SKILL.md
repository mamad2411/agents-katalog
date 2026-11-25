---
name: fe-main
description: >
  A skill for developing frontends based on design specs (design-spec.md), Figma designs, and OpenAPI specs.
  Produces UI publishing, component development, and API integration code.
  Use this skill for frontend development, publishing, or UI implementation requests.
---

## 🌐 Language

> All output documents and user-facing messages must be written in the language specified
> by `crew-config.json → preferences.language`. If not set, default to English.

## 🔧 Project Configuration Reference

> **You must read `crew-config.json` first and operate according to the project settings.**
> - `frontend.framework`: Next.js, React+Vite, Vue, Svelte, etc.
> - `frontend.styling`: Tailwind, styled-components, CSS Modules, etc.
> - `frontend.stateManagement`: Zustand, Redux, etc.
> - `conventions.i18n`: Whether i18n is used (if false, hardcoded strings are allowed)
> - `integrations.figma`: Whether Figma MCP is used
>
> If `crew-config.json` does not exist, guide the user to run the `/project-init` skill first.

# Frontend Main Developer

Develops the frontend based on design specs (design-spec.md), Figma designs (if available), and OpenAPI specs.

## Use Generated API Clients

> **Required**: All API calls must use generated API clients instead of manual fetch/axios calls.
> Generate API clients from the OpenAPI spec using the project's configured tool (check `crew-config.json` or project documentation for the specific generator).

### Core Rules

1. **Direct axios/fetch calls prohibited**: Direct calls like `axios.get()`, `fetch()` are prohibited when a generated client exists
2. **Use only generated clients**: Use the generated API client methods for all API calls
3. **Do not modify generated code**: Do not directly edit auto-generated files
4. **Use generated types**: Import types from the generated API client instead of defining them manually

### Usage Example

```typescript
// ✅ GOOD: Using generated API client
import { usersApiClient } from './api/client';
import type { User } from './api/generated/models';

const { data } = await usersApiClient.getUser({ id });

// ❌ BAD: Direct fetch call
const res = await fetch(`/api/users/${id}`);

// ❌ BAD: Local interface definition (when generated type exists)
interface User { id: string; name: string; ... }
```

### When the OpenAPI Spec Changes

```bash
# Regenerate API client code (check your project's package.json for the exact script name)
npm run api:generate

# Check for broken imports with type check
npx tsc --noEmit
```

### Internationalization (i18n)

> Check `crew-config.json → conventions.i18n` to determine if i18n is required.

- If i18n is enabled: All UI text must use the project's translation mechanism
- If i18n is disabled: Hardcoded strings are allowed

---

## Workflow

### 1. Verify Input Documents

Receive the following documents as input:

#### Required Input
- **design-spec.md**: Design system, component specifications, screen layout definitions
- **OpenAPI spec**: API endpoints, request/response type definitions

#### Optional Input
- **Figma design**: Referenced when Figma links are included in design-spec.md
- **Wireframe**: For screen structure reference

```
Example inputs:
- "Implement the login page based on docs/{backlog-keyword}/design-spec.md"
- "Connect the API according to the OpenAPI spec"
- "Run npm run api:generate and connect the form using the generated hooks"
```

> **Important**: When the OpenAPI spec changes, you must run `npm run api:generate` to regenerate types and hooks.

### 1.1 Design Reference Priority

| Priority | Reference | Usage |
|----------|-----------|-------|
| 1 | **Figma design** (if available) | Actual UI implementation (colors, spacing, layout) |
| 2 | **design-spec.md** | Design tokens, component specs, state-specific behavior |
| 3 | **Wireframe** | Screen structure and flow reference |

> **Note**: When a Figma design is available, check the Figma links and component keys in design-spec.md and reference the actual design values. When Figma is unavailable, use the CSS/design token values from design-spec.md directly.

### 2. Project Analysis

1. Understand existing project structure
2. Identify the framework in use
3. Check UI library/design system
4. Understand state management approach

#### Supported Frameworks

| Framework | UI Library | API Client | Client State |
|-----------|-----------|------------|--------------|
| Next.js | Tailwind, shadcn/ui, Radix UI | Project-configured generator | Zustand |
| React | Tailwind, shadcn/ui, MUI | React Query (orval, openapi-generator-cli, etc.) | Zustand |
| Vue | Vuetify, Element Plus | Vue Query (orval, openapi-generator-cli, etc.) | Pinia |
| Svelte | Skeleton | Svelte Query (orval, openapi-generator-cli, etc.) | Svelte Store |

> Check `crew-config.json → frontend.framework` and project documentation to determine which API client generation tool is in use.

### 3. Code Structure

#### 3.1 Directory Structure (React/Next.js)

```
src/
├── app/                    # App Router (Next.js)
│   ├── (auth)/
│   │   ├── login/
│   │   │   └── page.tsx
│   │   └── signup/
│   │       └── page.tsx
│   ├── layout.tsx
│   └── providers.tsx       # React Query Provider, etc.
├── api/                    # API related (OpenAPI generated)
│   ├── custom-instance.ts  # Custom axios instance
│   ├── generated/          # Auto-generated by orval (do not modify)
│   │   ├── auth/
│   │   │   └── auth.ts
│   │   ├── users/
│   │   │   └── users.ts
│   │   └── index.ts
│   └── model/              # Auto-generated types (do not modify)
│       ├── index.ts
│       ├── loginRequest.ts
│       └── userResponse.ts
├── components/             # Components
│   ├── ui/                 # Base UI components
│   │   ├── button.tsx
│   │   └── input.tsx
│   ├── forms/              # Form components
│   │   └── login-form.tsx
│   └── layouts/            # Layout components
│       └── header.tsx
├── hooks/                  # Custom hooks (wrapping generated hooks)
│   ├── use-auth.ts
│   └── use-form.ts
├── lib/                    # Utilities
│   ├── schemas/            # Zod schemas (for form validation)
│   │   └── auth.ts
│   └── utils.ts
├── stores/                 # State management (Zustand)
│   └── auth-store.ts
└── styles/                 # Styles
    └── globals.css

# Root configuration files
├── orval.config.ts         # OpenAPI client generation config
└── docs/
    └── openapi.yaml        # OpenAPI spec file
```

#### 3.2 Page Component

```tsx
// app/(auth)/login/page.tsx
import { LoginForm } from '@/components/forms/login-form';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';

export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <Logo className="mx-auto mb-4" />
          <CardTitle>Log In</CardTitle>
        </CardHeader>
        <CardContent>
          <LoginForm />
        </CardContent>
      </Card>
    </div>
  );
}
```

#### 3.3 Form Component

```tsx
// components/forms/login-form.tsx
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { useAuth } from '@/hooks/use-auth';
import { loginSchema } from '@/lib/schemas/auth';

type LoginFormData = z.infer<typeof loginSchema>;

export function LoginForm() {
  const router = useRouter();
  const { login, isLoading } = useAuth();
  const [error, setError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (data: LoginFormData) => {
    try {
      setError(null);
      await login(data);
      router.push('/dashboard');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed.');
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      {error && (
        <div className="p-3 text-sm text-red-500 bg-red-50 rounded-md">
          {error}
        </div>
      )}

      <div className="space-y-2">
        <label htmlFor="email" className="text-sm font-medium">
          Email
        </label>
        <Input
          id="email"
          type="email"
          placeholder="email@example.com"
          {...register('email')}
          error={errors.email?.message}
        />
      </div>

      <div className="space-y-2">
        <label htmlFor="password" className="text-sm font-medium">
          Password
        </label>
        <Input
          id="password"
          type="password"
          placeholder="••••••••"
          {...register('password')}
          error={errors.password?.message}
        />
      </div>

      <Button type="submit" className="w-full" disabled={isLoading}>
        {isLoading ? 'Logging in...' : 'Log In'}
      </Button>

      <div className="text-center text-sm text-gray-500">
        <a href="/forgot-password" className="hover:underline">
          Forgot Password
        </a>
        {' | '}
        <a href="/signup" className="hover:underline">
          Sign Up
        </a>
      </div>
    </form>
  );
}
```

### 4. API Integration (OpenAPI Generated Client)

#### 4.1 OpenAPI Client Generation Setup

Use the project's configured API client generation tool to auto-generate types and API hooks/clients from the OpenAPI spec. Check `crew-config.json` or the project's `package.json` scripts for the specific tool in use.

##### Example: orval + React Query (when using React)

```bash
npm install @tanstack/react-query axios
npm install -D orval
```

```typescript
// orval.config.ts
import { defineConfig } from 'orval';

export default defineConfig({
  api: {
    input: {
      target: './docs/openapi.yaml',  // OpenAPI spec file path
    },
    output: {
      mode: 'tags-split',             // Split files by tag
      target: './src/api/generated',  // Generated file location
      schemas: './src/api/model',     // Type definition location
      client: 'react-query',          // Generate React Query hooks
      httpClient: 'axios',            // Use axios
      mock: false,
      override: {
        mutator: {
          path: './src/api/custom-instance.ts',  // Custom axios instance
          name: 'customInstance',
        },
        query: {
          useQuery: true,
          useMutation: true,
          signal: true,
        },
      },
    },
  },
});
```

```json
{
  "scripts": {
    "api:generate": "orval",
    "api:watch": "orval --watch"
  }
}
```

> Other common tools include **openapi-generator-cli** (typescript-axios, typescript-fetch), **swagger-codegen**, and **openapi-typescript**. Use whichever tool your project has configured.

#### 4.2 Custom Axios Instance

```typescript
// src/api/custom-instance.ts
import Axios, { AxiosRequestConfig, AxiosError } from 'axios';
import { useAuthStore } from '@/stores/auth-store';

export const AXIOS_INSTANCE = Axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3000/api/v1',
});

// Request interceptor: auto-attach token
AXIOS_INSTANCE.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor: handle token expiration
AXIOS_INSTANCE.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().clearToken();
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Custom instance function for orval
export const customInstance = <T>(config: AxiosRequestConfig): Promise<T> => {
  const source = Axios.CancelToken.source();
  const promise = AXIOS_INSTANCE({
    ...config,
    cancelToken: source.token,
  }).then(({ data }) => data);

  // @ts-expect-error cancel property for react-query
  promise.cancel = () => {
    source.cancel('Query was cancelled');
  };

  return promise;
};

export default customInstance;
```

#### 4.3 Generated Code Structure

Structure generated after running orval:

```
src/api/
├── custom-instance.ts          # Custom axios instance
├── generated/                  # Auto-generated files
│   ├── auth/
│   │   └── auth.ts            # Authentication-related hooks
│   ├── users/
│   │   └── users.ts           # User-related hooks
│   └── index.ts               # Full exports
└── model/                      # Auto-generated types
    ├── loginRequest.ts
    ├── signupRequest.ts
    ├── userResponse.ts
    ├── tokenResponse.ts
    └── index.ts
```

#### 4.4 Generated Hook Usage Example

```typescript
// Auto-generated hooks (src/api/generated/auth/auth.ts)
// This file is auto-generated by orval

import { useMutation, useQuery } from '@tanstack/react-query';
import type { LoginRequest, TokenResponse, UserResponse } from '../../model';
import { customInstance } from '../../custom-instance';

// POST /auth/login
export const useLogin = () => {
  return useMutation<TokenResponse, Error, LoginRequest>({
    mutationFn: (data) => customInstance({
      url: '/auth/login',
      method: 'POST',
      data,
    }),
  });
};

// POST /auth/signup
export const useSignup = () => {
  return useMutation<UserResponse, Error, SignupRequest>({
    mutationFn: (data) => customInstance({
      url: '/auth/signup',
      method: 'POST',
      data,
    }),
  });
};

// GET /auth/me
export const useGetMe = (options?: { enabled?: boolean }) => {
  return useQuery<UserResponse, Error>({
    queryKey: ['auth', 'me'],
    queryFn: () => customInstance({ url: '/auth/me', method: 'GET' }),
    ...options,
  });
};

// POST /auth/logout
export const useLogout = () => {
  return useMutation<void, Error>({
    mutationFn: () => customInstance({
      url: '/auth/logout',
      method: 'POST',
    }),
  });
};
```

#### 4.5 Using Generated Hooks in Components

```typescript
// hooks/use-auth.ts - Wrapping generated hooks to add business logic
import { useQueryClient } from '@tanstack/react-query';
import { useLogin, useLogout, useGetMe } from '@/api/generated/auth/auth';
import { useAuthStore } from '@/stores/auth-store';

export function useAuth() {
  const queryClient = useQueryClient();
  const { setToken, clearToken, token } = useAuthStore();

  // Using generated hooks
  const loginMutation = useLogin();
  const logoutMutation = useLogout();
  const { data: user, isLoading: isLoadingUser } = useGetMe({
    enabled: !!token,
  });

  const login = async (data: Parameters<typeof loginMutation.mutateAsync>[0]) => {
    const result = await loginMutation.mutateAsync(data);
    setToken(result.accessToken);
    queryClient.invalidateQueries({ queryKey: ['auth', 'me'] });
    return result;
  };

  const logout = async () => {
    await logoutMutation.mutateAsync();
    clearToken();
    queryClient.clear();
  };

  return {
    user: user?.data,
    isLoading: loginMutation.isPending,
    isLoadingUser,
    isAuthenticated: !!token,
    login,
    logout,
    error: loginMutation.error,
  };
}
```

#### 4.6 Using in Form Components

```tsx
// components/forms/login-form.tsx
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { useAuth } from '@/hooks/use-auth';
import type { LoginRequest } from '@/api/model';  // Using auto-generated types

const loginSchema = z.object({
  email: z.string().email('Please enter a valid email'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

export function LoginForm() {
  const router = useRouter();
  const { login, isLoading, error } = useAuth();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginRequest>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (data: LoginRequest) => {
    try {
      await login(data);
      router.push('/dashboard');
    } catch {
      // Error is handled via useAuth's error state
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      {error && (
        <div className="p-3 text-sm text-red-500 bg-red-50 rounded-md">
          {error.message}
        </div>
      )}

      <div className="space-y-2">
        <label htmlFor="email" className="text-sm font-medium">
          Email
        </label>
        <Input
          id="email"
          type="email"
          placeholder="email@example.com"
          {...register('email')}
          error={errors.email?.message}
        />
      </div>

      <div className="space-y-2">
        <label htmlFor="password" className="text-sm font-medium">
          Password
        </label>
        <Input
          id="password"
          type="password"
          placeholder="••••••••"
          {...register('password')}
          error={errors.password?.message}
        />
      </div>

      <Button type="submit" className="w-full" isLoading={isLoading}>
        Log In
      </Button>
    </form>
  );
}
```

#### 4.7 CRUD Example (Using Generated Hooks)

```tsx
// pages/users/index.tsx - List retrieval
import { useGetUsers } from '@/api/generated/users/users';

export function UserList() {
  const { data, isLoading, error } = useGetUsers({
    page: 1,
    limit: 10,
  });

  if (isLoading) return <Skeleton />;
  if (error) return <ErrorMessage error={error} />;

  return (
    <ul>
      {data?.data.map((user) => (
        <li key={user.id}>{user.email}</li>
      ))}
    </ul>
  );
}
```

```tsx
// pages/users/[id].tsx - Detail retrieval
import { useGetUser } from '@/api/generated/users/users';

export function UserDetail({ userId }: { userId: string }) {
  const { data, isLoading } = useGetUser(userId);

  if (isLoading) return <Skeleton />;

  return <div>{data?.data.email}</div>;
}
```

```tsx
// components/forms/user-form.tsx - Create/Update
import { useCreateUser, useUpdateUser } from '@/api/generated/users/users';
import type { CreateUserRequest, UpdateUserRequest } from '@/api/model';

export function UserForm({ userId }: { userId?: string }) {
  const createMutation = useCreateUser();
  const updateMutation = useUpdateUser();
  const queryClient = useQueryClient();

  const onSubmit = async (data: CreateUserRequest | UpdateUserRequest) => {
    if (userId) {
      await updateMutation.mutateAsync({ id: userId, data });
    } else {
      await createMutation.mutateAsync(data);
    }
    queryClient.invalidateQueries({ queryKey: ['users'] });
  };

  // ... form UI
}
```

#### 4.8 React Query Provider Setup

```tsx
// app/providers.tsx
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { useState } from 'react';

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 60 * 1000,        // Stay fresh for 1 minute
            gcTime: 5 * 60 * 1000,       // Keep cache for 5 minutes
            retry: 1,
            refetchOnWindowFocus: false,
          },
        },
      })
  );

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
```

```tsx
// app/layout.tsx
import { Providers } from './providers';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko">
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```

### 5. UI Components

#### 5.1 Button Component

```tsx
// components/ui/button.tsx
import { forwardRef } from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';
import { Loader2 } from 'lucide-react';

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-lg font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none',
  {
    variants: {
      variant: {
        primary: 'bg-primary text-white hover:bg-primary/90',
        secondary: 'border border-gray-300 bg-white hover:bg-gray-50',
        ghost: 'hover:bg-gray-100',
        danger: 'bg-red-500 text-white hover:bg-red-600',
      },
      size: {
        sm: 'h-8 px-3 text-sm',
        md: 'h-10 px-4',
        lg: 'h-12 px-6 text-lg',
      },
    },
    defaultVariants: {
      variant: 'primary',
      size: 'md',
    },
  }
);

interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  isLoading?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, isLoading, children, ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(buttonVariants({ variant, size }), className)}
        disabled={isLoading || props.disabled}
        {...props}
      >
        {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
        {children}
      </button>
    );
  }
);
```

#### 5.2 Input Component

```tsx
// components/ui/input.tsx
import { forwardRef } from 'react';
import { cn } from '@/lib/utils';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  error?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className, error, ...props }, ref) => {
    return (
      <div className="space-y-1">
        <input
          ref={ref}
          className={cn(
            'w-full h-11 px-4 rounded-lg border bg-white transition-colors',
            'focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary',
            error
              ? 'border-red-500 focus:ring-red-500/20 focus:border-red-500'
              : 'border-gray-300',
            className
          )}
          {...props}
        />
        {error && (
          <p className="text-sm text-red-500">{error}</p>
        )}
      </div>
    );
  }
);
```

### 6. State Management

```typescript
// stores/auth-store.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface AuthState {
  token: string | null;
  setToken: (token: string) => void;
  clearToken: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      setToken: (token) => set({ token }),
      clearToken: () => set({ token: null }),
    }),
    {
      name: 'auth-storage',
    }
  )
);
```

### 7. File Output

```
# Manually written files
src/
├── app/{route}/page.tsx           # Page components
├── app/providers.tsx               # React Query Provider
├── api/custom-instance.ts          # Custom axios instance
├── components/forms/{form}-form.tsx # Form components
├── components/ui/{component}.tsx   # UI components
├── hooks/use-{feature}.ts         # Custom hooks (wrapping generated hooks)
├── stores/{domain}-store.ts        # Zustand stores
└── lib/schemas/{domain}.ts         # Zod form validation schemas

# Auto-generated files (do not modify)
src/api/
├── generated/{tag}/{tag}.ts      # API hooks/clients
└── model/{type}.ts               # TypeScript types

# Configuration files
├── {api-generator-config}          # API client generation config (e.g., orval.config.ts, openapitools.json)
└── docs/openapi.yaml               # OpenAPI spec
```

## Lint Check Required

> **Warning**: After writing/modifying code, you must run the project's configured linter and fix all errors before finishing. Check `crew-config.json` for lint commands, or fall back to the defaults below.

### Required Execution Order

```
1. Code writing/modification complete
           │
           ▼
2. Run lint auto-fix (--fix)
           │
           ├── All errors fixed ──▶ Proceed to step 3
           │
           └── Unfixed errors remain ──▶ Fix manually, then re-run step 2
           │
           ▼
3. Lint check (confirm 0 errors)
           │
           ▼
4. Type check
           │
           ▼
5. Build verification (optional, recommended)
           │
           ▼
6. Task complete
```

### Lint Commands by Framework

| Framework | Lint Auto-Fix | Lint Check | Type Check |
|-----------|--------------|-----------|------------|
| Next.js | `npx next lint --fix` | `npx next lint` | `npx tsc --noEmit` |
| React (Vite) | `npm run lint -- --fix` | `npm run lint` | `npx tsc --noEmit` |
| Vue | `npm run lint -- --fix` | `npm run lint` | `npx vue-tsc --noEmit` |
| Svelte | `npm run lint -- --fix` | `npm run lint` | `npx svelte-check` |

### Handling Errors That Cannot Be Auto-Fixed

Errors not fixed by `--fix` must be **fixed manually**:

```typescript
// ❌ Cannot be auto-fixed: using any type
const data: any = fetchData();  // ESLint: Unexpected any

// ✅ Manual fix: specify correct type
interface UserData { id: string; name: string; }
const data: UserData = fetchData();
```

### Completion Criteria

- **Cannot complete task if lint errors remain**
- **Cannot complete task if type errors remain**
- Task is complete only when lint and type checks return 0 errors

---

## Development Principles

### 1. Lint Check Required
- Always run the project's lint auto-fix after writing code
- Manually fix errors that cannot be auto-fixed
- Also verify type errors with the appropriate type checker
- Task can only be completed with 0 lint/type errors

### 2. Generated API Client Must Be Used
- **Direct axios/fetch calls prohibited**: Use generated API client methods
- **Do not manually define types**: Use auto-generated types from the OpenAPI spec
- **Do not modify generated code**: Never edit auto-generated files
- **Regenerate when spec changes**: Run the project's API generation script when the OpenAPI spec changes

### 3. Component Separation
- Separate components by concern
- Reusable UI components

### 4. Import Path Conventions
- Follow the project's configured import path conventions (path aliases, relative paths, etc.)
- Prefer path aliases (e.g., `@/`, `~/`) when the project has them configured to avoid deep relative imports

### 5. Type Safety
- Use auto-generated types from the OpenAPI spec (`@/api/model`)
- Use Zod only for form input validation (separate from API types)
- Keep generated types and Zod schemas in sync

### 7. Server vs Client State Separation
- Manage server state with the project's data-fetching library (React Query, Vue Query, SWR, etc.)
- Manage client state with the project's state management tool (Zustand, Pinia, Svelte stores, etc.)
- Invalidate server-state caches after mutations

### 8. Accessibility
- Semantic HTML
- ARIA labels
- Keyboard navigation

### 9. Responsive Design
- Mobile-first approach
- Leverage the project's CSS framework breakpoints

> **Note**: Examples shown throughout this document are for React/Next.js with Tailwind CSS. Adapt to your framework per `crew-config.json → frontend.framework`.

## Framework-Specific References

Consult the reference that matches your project's `crew-config.json → frontend.framework`:

| Framework | Reference |
|-----------|-----------|
| Next.js | [references/nextjs-patterns.md](references/nextjs-patterns.md) |
| React + Vite | [references/react-vite-patterns.md](references/react-vite-patterns.md) |
| Vue 3 | [references/vue-patterns.md](references/vue-patterns.md) |
| Svelte/SvelteKit | [references/svelte-patterns.md](references/svelte-patterns.md) |
| Angular | [references/angular-patterns.md](references/angular-patterns.md) |

## References

- Component guide: [references/component-patterns.md](references/component-patterns.md)
- Styling guide: [references/styling-guide.md](references/styling-guide.md)
- TanStack Query official docs: https://tanstack.com/query/latest
- orval official docs: https://orval.dev/
- openapi-generator-cli docs: https://openapi-generator.tech/
