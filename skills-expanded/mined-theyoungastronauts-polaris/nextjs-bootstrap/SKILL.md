---
name: nextjs-bootstrap
description: "Scaffold a Next.js app (App Router, Docker, DaisyUI + Tailwind v4, JWT auth)."
disable-model-invocation: true
---

# Next.js Bootstrap

On-demand command for scaffolding a new Next.js application with Docker, App Router, DaisyUI, Tailwind v4, and standard conventions.

> **MANDATORY: This project runs entirely in Docker.**
> Every Docker file below (Dockerfile.dev, docker-compose.yml, Makefile) MUST be generated.
> The Makefile is the sole interface — never run `npm` directly on the host.

## Before You Start

Ask the user for these values:

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{app-name}` | Project/directory name | `my-app` |
| `{compose-project}` | Docker Compose project name (kebab-case) | `my-app-web` |
| `{host_port}` | Host port for Next.js (default: `3000`) | `3001` |
| `{api-port}` | Backend API port (default: `8002`) | `8002` |
| `{domain}` | Production domain | `myapp.com` |
| `{app-title}` | Display name for metadata | `My App` |
| **Architecture mode** | See below | Frontend-centric / SSR-centric / Combination |
| **Include Agentation?** | Browser annotation tool for visual feedback | Yes / No |

### Architecture Modes

- **Frontend-centric**: SPA-like, client-first. JWT auth via localStorage, `useEffect`+`useState`, React Context, no middleware. Best for: apps with a separate Django/DRF backend.
- **SSR-centric**: Server-rendered, Next.js-native. Server Components, React Query, middleware auth, error.tsx/loading.tsx boundaries. Best for: content-heavy apps, SEO-critical pages.
- **Combination**: Both patterns available, choose per-route.

---

## Directory Structure

```
{app-name}/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── globals.css
│   │   ├── page.tsx
│   │   ├── login/page.tsx
│   │   ├── forgot-password/page.tsx
│   │   ├── reset-password/page.tsx
│   │   └── <feature>/
│   │       ├── page.tsx
│   │       ├── new/page.tsx
│   │       └── [id]/page.tsx
│   ├── components/
│   │   ├── Providers.tsx
│   │   ├── layout/
│   │   │   ├── Header.tsx
│   │   │   └── AppLayout.tsx
│   │   ├── landing/
│   │   │   └── LandingPage.tsx
│   │   ├── ui/
│   │   │   └── index.ts
│   │   └── <feature>/
│   ├── contexts/                  # Frontend-centric mode
│   │   └── UserContext.tsx
│   ├── lib/
│   │   ├── api.ts
│   │   ├── auth.ts                # Frontend-centric mode
│   │   ├── constants.ts
│   │   └── hooks/
│   │       ├── index.ts
│   │       └── useRequireAuth.ts
│   └── types/
│       └── api.ts
├── public/
│   ├── favicon.png
│   └── og.jpg
├── .husky/
│   └── pre-commit
├── package.json
├── tsconfig.json
├── next.config.ts
├── eslint.config.mjs
├── postcss.config.mjs
├── .nvmrc
├── .env.local
├── .gitignore
├── Dockerfile.dev
├── docker-compose.yml
├── Makefile
└── .mcp.json                 # If Agentation enabled
```

---

## Shared Templates (All Modes)

### package.json

```json
{
  "name": "{app-name}",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "eslint",
    "lint:fix": "eslint --fix",
    "typecheck": "tsc --noEmit",
    "prepare": "cd .. && husky {app-name}/.husky"
  },
  "dependencies": {
    "next": "^16",
    "react": "^19",
    "react-dom": "^19",
    "dayjs": "^1.11",
    "react-hot-toast": "^2.5"
  },
  "devDependencies": {
    "typescript": "^5",
    "tailwindcss": "^4",
    "@tailwindcss/postcss": "^4",
    "daisyui": "^5",
    "eslint": "^9",
    "eslint-config-next": "^16",
    "husky": "^9",
    "lint-staged": "^15",
    "@types/node": "^22",
    "@types/react": "^19",
    "@types/react-dom": "^19"
  },
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": ["eslint --fix"]
  }
}
```

**SSR-centric mode**: Also add `"@tanstack/react-query": "^5"` to dependencies.

**If Agentation enabled**: Also add `"agentation": "^0"` to devDependencies.

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "react-jsx",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts", ".next/dev/types/**/*.ts", "**/*.mts"],
  "exclude": ["node_modules"]
}
```

### next.config.ts

```typescript
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
};

export default nextConfig;
```

### eslint.config.mjs

```javascript
import { defineConfig, globalIgnores } from "eslint/config";
import nextVitals from "eslint-config-next/core-web-vitals";
import nextTs from "eslint-config-next/typescript";

const eslintConfig = defineConfig([
  ...nextVitals,
  ...nextTs,
  globalIgnores([
    ".next/**",
    "out/**",
    "build/**",
    "next-env.d.ts",
  ]),
]);

export default eslintConfig;
```

### postcss.config.mjs

```javascript
const config = {
  plugins: {
    "@tailwindcss/postcss": {},
  },
};

export default config;
```

### .nvmrc

```
22
```

### .env.local

```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:{api-port}
```

### .gitignore

```
# dependencies
/node_modules
/.pnp
.pnp.js

# testing
/coverage

# next.js
/.next/
/out/

# production
/build

# misc
.DS_Store
*.pem

# debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# local env files
.env*.local

# vercel
.vercel

# typescript
*.tsbuildinfo
next-env.d.ts

# docker
docker-compose.override.yml
```

### .husky/pre-commit

```bash
cd {app-name} && npx lint-staged
```

Make this file executable: `chmod +x .husky/pre-commit`

### .mcp.json (if Agentation enabled)

Only generate this file if the user opted into Agentation.

```json
{
  "mcpServers": {
    "agentation": {
      "command": "npx",
      "args": ["agentation-mcp", "server"]
    }
  }
}
```

### src/app/globals.css

```css
@import "tailwindcss";
@plugin "daisyui" {
  themes: light, dark;
}
```

### src/app/layout.tsx

```typescript
import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import Providers from "@/components/Providers";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  metadataBase: new URL("https://{domain}"),
  title: {
    default: "{app-title}",
    template: "%s | {app-title}",
  },
  description: "{app-title} description",
  icons: {
    icon: "/favicon.png",
    apple: "/favicon.png",
  },
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "https://{domain}",
    siteName: "{app-title}",
    title: "{app-title}",
    description: "{app-title} description",
    images: [{ url: "/og.jpg", width: 1200, height: 630, alt: "{app-title}" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "{app-title}",
    description: "{app-title} description",
    images: ["/og.jpg"],
  },
  robots: { index: true, follow: true },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" data-theme="dark">
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased`}>
        <div className="min-h-screen bg-base-100 text-base-content">
          <Providers>{children}</Providers>
        </div>
      </body>
    </html>
  );
}
```

**If Agentation enabled**: Add the import and component inside `<body>`, before the closing `</body>`:

```tsx
import { Agentation } from "agentation";

// Add after the content </div>, before </body>:
{process.env.NODE_ENV === "development" && <Agentation />}
```

### src/lib/api.ts

```typescript
import { getAccessToken } from '@/lib/auth';
import type { ApiErrorResponse } from '@/types/api';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:{api-port}';
const API_PATH = '/api/v1';

export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public statusText: string,
    public data?: ApiErrorResponse
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

async function apiFetch<T>(
  endpoint: string,
  options?: RequestInit & { skipAuth?: boolean }
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  const { skipAuth, ...fetchOptions } = options || {};

  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...fetchOptions?.headers,
  };

  if (!skipAuth) {
    const token = getAccessToken();
    if (token) {
      (headers as Record<string, string>)['Authorization'] = `Bearer ${token}`;
    }
  }

  try {
    const response = await fetch(url, { ...fetchOptions, headers });

    let data: Record<string, unknown>;
    try {
      data = await response.json();
    } catch {
      data = {};
    }

    if (!response.ok) {
      const errorMessage =
        (typeof data.detail === 'string' ? data.detail : null) ||
        (typeof data.error === 'string' ? data.error : null) ||
        (typeof data.message === 'string' ? data.message : null) ||
        `Request failed: ${response.statusText}`;
      throw new ApiError(errorMessage, response.status, response.statusText, data as unknown as ApiErrorResponse);
    }

    return data as T;
  } catch (error) {
    if (error instanceof ApiError) throw error;

    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new ApiError('Network error. Please check your connection.', 0, 'Network Error');
    }

    throw new ApiError(
      error instanceof Error ? error.message : 'An unknown error occurred',
      0,
      'Unknown Error'
    );
  }
}

export { apiFetch, API_PATH };
```

Add auth-specific API methods based on mode (see mode-specific sections below).

### src/lib/constants.ts

```typescript
export const APP_NAME = '{app-title}';
```

### src/types/api.ts

```typescript
// ============================================
// Auth & User
// ============================================

export interface User {
  uuid: string;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
}

export interface LoginResponse {
  access: string;
  refresh: string;
}

export interface RefreshResponse {
  access: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  first_name: string;
  last_name: string;
}

export interface RegisterResponse {
  user: User;
  tokens: { access: string; refresh: string };
}

export interface ApiErrorResponse {
  detail?: string;
  error?: string;
  message?: string;
  [key: string]: unknown;
}

// ============================================
// Add feature types below
// ============================================
```

### src/components/ui/index.ts

```typescript
// Barrel exports for shared UI components
// export { default as Breadcrumbs } from './Breadcrumbs';
```

### src/components/layout/Header.tsx

```typescript
'use client';

import Link from 'next/link';

export default function Header() {
  return (
    <header className="navbar bg-base-200 border-b border-base-300">
      <div className="container mx-auto max-w-5xl">
        <div className="flex-1">
          <Link href="/" className="text-xl font-bold text-primary">
            {app-title}
          </Link>
        </div>
        <div className="flex-none">
          {/* Navigation items */}
        </div>
      </div>
    </header>
  );
}
```

### src/app/page.tsx

```typescript
export default function HomePage() {
  return (
    <main className="container mx-auto px-4 py-16 max-w-5xl">
      <h1 className="text-4xl font-bold">{app-title}</h1>
    </main>
  );
}
```

---

## Frontend-Centric Mode Templates

Generate these files when the user selects **frontend-centric** or **combination** mode.

### src/lib/auth.ts

```typescript
const ACCESS_TOKEN_KEY = '{app-name}_access_token';
const REFRESH_TOKEN_KEY = '{app-name}_refresh_token';

export function getAccessToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem(ACCESS_TOKEN_KEY);
}

export function setAccessToken(token: string): void {
  localStorage.setItem(ACCESS_TOKEN_KEY, token);
}

export function getRefreshToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem(REFRESH_TOKEN_KEY);
}

export function setRefreshToken(token: string): void {
  localStorage.setItem(REFRESH_TOKEN_KEY, token);
}

export function setTokens(access: string, refresh: string): void {
  setAccessToken(access);
  setRefreshToken(refresh);
}

export function clearTokens(): void {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
}

export function isAuthenticated(): boolean {
  return getAccessToken() !== null;
}
```

### Auth API methods (add to src/lib/api.ts)

```typescript
import { setTokens, clearTokens, getRefreshToken } from '@/lib/auth';
import type {
  User, LoginResponse, RefreshResponse,
  RegisterRequest, RegisterResponse,
} from '@/types/api';

export const authApi = {
  login: async (email: string, password: string): Promise<LoginResponse> => {
    const response = await apiFetch<LoginResponse>(`${API_PATH}/auth/login/`, {
      method: 'POST',
      body: JSON.stringify({ email, password }),
      skipAuth: true,
    });
    setTokens(response.access, response.refresh);
    return response;
  },

  register: async (data: RegisterRequest): Promise<RegisterResponse> => {
    const response = await apiFetch<RegisterResponse>(`${API_PATH}/auth/register/`, {
      method: 'POST',
      body: JSON.stringify(data),
      skipAuth: true,
    });
    setTokens(response.tokens.access, response.tokens.refresh);
    return response;
  },

  logout: (): void => {
    clearTokens();
  },

  refresh: async (): Promise<string | null> => {
    const refreshToken = getRefreshToken();
    if (!refreshToken) return null;
    try {
      const response = await apiFetch<RefreshResponse>(`${API_PATH}/auth/refresh/`, {
        method: 'POST',
        body: JSON.stringify({ refresh: refreshToken }),
        skipAuth: true,
      });
      setTokens(response.access, refreshToken);
      return response.access;
    } catch {
      clearTokens();
      return null;
    }
  },

  me: () => apiFetch<User>(`${API_PATH}/auth/me/`),
};
```

### src/contexts/UserContext.tsx

```typescript
'use client';

import { createContext, useContext, useState, useEffect, useCallback, ReactNode } from 'react';
import type { User, RegisterRequest } from '@/types/api';
import { authApi, ApiError } from '@/lib/api';
import { isAuthenticated, clearTokens } from '@/lib/auth';

interface UserContextType {
  user: User | null;
  loading: boolean;
  isLoggedIn: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (data: RegisterRequest) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

export function UserProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const refreshUser = useCallback(async () => {
    if (!isAuthenticated()) {
      setUser(null);
      setLoading(false);
      return;
    }

    try {
      const userData = await authApi.me();
      setUser(userData);
    } catch (error) {
      if (error instanceof ApiError && error.status === 401) {
        const newToken = await authApi.refresh();
        if (newToken) {
          try {
            const userData = await authApi.me();
            setUser(userData);
            return;
          } catch {
            // Fall through to clear
          }
        }
      }
      clearTokens();
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refreshUser();
  }, [refreshUser]);

  const login = async (email: string, password: string) => {
    await authApi.login(email, password);
    const userData = await authApi.me();
    setUser(userData);
  };

  const register = async (data: RegisterRequest) => {
    const response = await authApi.register(data);
    setUser(response.user);
  };

  const logout = () => {
    authApi.logout();
    setUser(null);
  };

  return (
    <UserContext.Provider
      value={{ user, loading, isLoggedIn: user !== null, login, register, logout, refreshUser }}
    >
      {children}
    </UserContext.Provider>
  );
}

export function useUser() {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
}
```

### src/components/Providers.tsx (Frontend-Centric)

```typescript
'use client';

import { ReactNode } from 'react';
import { Toaster } from 'react-hot-toast';
import { UserProvider } from '@/contexts/UserContext';

export default function Providers({ children }: { children: ReactNode }) {
  return (
    <UserProvider>
      {children}
      <Toaster
        position="top-right"
        toastOptions={{
          style: {
            background: '#1a1a1a',
            color: '#fff',
            border: '1px solid #333',
          },
          success: {
            iconTheme: { primary: '#dca54c', secondary: '#1a1a1a' },
          },
          error: {
            iconTheme: { primary: '#ff6b6b', secondary: '#1a1a1a' },
          },
        }}
      />
    </UserProvider>
  );
}
```

### src/lib/hooks/useRequireAuth.ts

```typescript
'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useUser } from '@/contexts/UserContext';

export function useRequireAuth() {
  const { user, loading, isLoggedIn } = useUser();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !isLoggedIn) {
      router.replace('/login');
    }
  }, [loading, isLoggedIn, router]);

  return { user, loading, isAuthenticated: isLoggedIn };
}
```

### src/lib/hooks/index.ts

```typescript
export { useRequireAuth } from './useRequireAuth';
```

### src/components/layout/AppLayout.tsx (Frontend-Centric)

```typescript
'use client';

import { ReactNode } from 'react';
import { useRequireAuth } from '@/lib/hooks';
import Header from './Header';

export default function AppLayout({ children }: { children: ReactNode }) {
  const { loading } = useRequireAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <span className="loading loading-spinner loading-lg"></span>
      </div>
    );
  }

  return (
    <>
      <Header />
      <main className="container mx-auto px-4 py-8 max-w-5xl flex-1">
        {children}
      </main>
    </>
  );
}
```

### src/app/login/page.tsx (Frontend-Centric)

```typescript
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useUser } from '@/contexts/UserContext';
import { ApiError } from '@/lib/api';
import toast from 'react-hot-toast';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useUser();
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await login(email, password);
      toast.success('Welcome back!');
      router.push('/');
    } catch (error) {
      if (error instanceof ApiError) {
        toast.error(error.message);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4 py-16">
      <div className="w-full max-w-sm">
        <h1 className="text-2xl font-bold text-center mb-8">{app-title}</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="form-control">
            <label className="label">
              <span className="label-text">Email</span>
            </label>
            <input
              type="email"
              className="input input-bordered w-full"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="form-control">
            <label className="label">
              <span className="label-text">Password</span>
            </label>
            <input
              type="password"
              className="input input-bordered w-full"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button
            type="submit"
            className="btn btn-primary w-full"
            disabled={loading}
          >
            {loading ? <span className="loading loading-spinner loading-sm" /> : 'Sign In'}
          </button>
        </form>
        <p className="text-center mt-4 text-sm text-base-content/70">
          <Link href="/forgot-password" className="link link-primary">
            Forgot password?
          </Link>
        </p>
      </div>
    </div>
  );
}
```

---

## SSR-Centric Mode Templates

Generate these files when the user selects **SSR-centric** or **combination** mode.

### src/lib/auth.ts (SSR)

For SSR mode, provide a minimal stub that the user can extend with their preferred auth approach (cookies, NextAuth, etc.):

```typescript
// SSR auth — extend based on your auth strategy
// Options: NextAuth, cookie-based sessions, server-side JWT validation

export function getAccessToken(): string | null {
  if (typeof window === 'undefined') return null;
  // Implement based on auth strategy
  return null;
}
```

### src/components/Providers.tsx (SSR-Centric)

```typescript
'use client';

import { ReactNode, useState } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'react-hot-toast';

export default function Providers({ children }: { children: ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 60 * 1000,
            refetchOnWindowFocus: false,
          },
        },
      })
  );

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <Toaster
        position="top-right"
        toastOptions={{
          style: {
            background: '#1a1a1a',
            color: '#fff',
            border: '1px solid #333',
          },
          success: {
            iconTheme: { primary: '#dca54c', secondary: '#1a1a1a' },
          },
          error: {
            iconTheme: { primary: '#ff6b6b', secondary: '#1a1a1a' },
          },
        }}
      />
    </QueryClientProvider>
  );
}
```

### middleware.ts (SSR-Centric)

```typescript
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

const publicPaths = ['/login', '/forgot-password', '/reset-password'];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Allow public paths
  if (publicPaths.some((path) => pathname.startsWith(path))) {
    return NextResponse.next();
  }

  // Check for auth token (adjust based on your auth strategy)
  const token = request.cookies.get('session')?.value;
  if (!token) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.png|og.jpg).*)'],
};
```

### React Query hook pattern (SSR-Centric)

Create `src/lib/queries/` for domain-specific query hooks:

```typescript
// src/lib/queries/useItems.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { itemsApi } from '@/lib/api';
import type { Item, ItemCreateRequest } from '@/types/api';

export function useItems() {
  return useQuery<Item[]>({
    queryKey: ['items'],
    queryFn: () => itemsApi.list(),
  });
}

export function useItem(id: string) {
  return useQuery<Item>({
    queryKey: ['items', id],
    queryFn: () => itemsApi.get(id),
    enabled: !!id,
  });
}

export function useCreateItem() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: ItemCreateRequest) => itemsApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['items'] });
    },
  });
}
```

### error.tsx pattern (SSR-Centric)

```typescript
'use client';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div className="min-h-[50vh] flex flex-col items-center justify-center">
      <h2 className="text-xl font-bold mb-4">Something went wrong</h2>
      <p className="text-base-content/70 mb-6">{error.message}</p>
      <button className="btn btn-primary" onClick={reset}>
        Try again
      </button>
    </div>
  );
}
```

### loading.tsx pattern (SSR-Centric)

```typescript
export default function Loading() {
  return (
    <div className="flex justify-center py-16">
      <span className="loading loading-spinner loading-lg"></span>
    </div>
  );
}
```

### Server Component data fetching (SSR-Centric)

```typescript
// src/app/items/page.tsx (Server Component)
import { itemsApi } from '@/lib/api';

export default async function ItemsPage() {
  const items = await itemsApi.list();

  return (
    <main className="container mx-auto px-4 py-8 max-w-5xl">
      <h1 className="text-2xl font-bold mb-8">Items</h1>
      <div className="grid gap-4 sm:grid-cols-2">
        {items.map((item) => (
          <div key={item.uuid} className="card bg-base-200 shadow-md">
            <div className="card-body">
              <h3 className="card-title text-lg">{item.title}</h3>
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}
```

---

## DaisyUI + Tailwind Patterns Reference

### Semantic Colors

| Class | Usage |
|-------|-------|
| `bg-base-100` | Primary background |
| `bg-base-200` | Card/section background |
| `bg-base-300` | Elevated/nested background |
| `text-base-content` | Primary text |
| `text-base-content/70` | Secondary/muted text |
| `text-base-content/50` | Tertiary/hint text |
| `text-primary` | Accent color text |
| `border-base-300` | Borders |
| `bg-primary text-primary-content` | Primary buttons/badges |

### Component Classes

**Buttons:**
```html
<button class="btn btn-primary">Primary</button>
<button class="btn btn-ghost">Secondary</button>
<button class="btn btn-outline">Outline</button>
<button class="btn btn-error">Destructive</button>
<button class="btn btn-sm">Small</button>
```

**Cards:**
```html
<div class="card bg-base-200 shadow-md hover:shadow-lg transition-shadow">
  <div class="card-body">
    <h3 class="card-title text-lg">Title</h3>
    <p class="text-base-content/70 text-sm">Description</p>
    <div class="card-actions justify-end mt-4">
      <button class="btn btn-primary btn-sm">Action</button>
    </div>
  </div>
</div>
```

**Badges:**
```typescript
const statusColors: Record<string, string> = {
  active: 'badge-success',
  paused: 'badge-warning',
  completed: 'badge-neutral',
};
<span className={`badge ${statusColors[status]} capitalize`}>{status}</span>
```

**Forms:**
```html
<div class="form-control mb-4">
  <label class="label"><span class="label-text">Field</span></label>
  <input type="text" class="input input-bordered w-full" />
</div>
```

**Modals:**
```typescript
<dialog className={`modal ${isOpen ? 'modal-open' : ''}`}>
  <div className="modal-box">
    <h3 className="font-bold text-lg">Title</h3>
    <p className="py-4 text-base-content/70">Content</p>
    <div className="modal-action">
      <button className="btn btn-ghost" onClick={onClose}>Cancel</button>
      <button className="btn btn-primary" onClick={onConfirm}>Confirm</button>
    </div>
  </div>
  <form method="dialog" className="modal-backdrop"><button>close</button></form>
</dialog>
```

**Loading:**
```html
<div class="flex justify-center py-16">
  <span class="loading loading-spinner loading-lg"></span>
</div>
```

### Layout Patterns

```html
<!-- Page container -->
<main class="container mx-auto px-4 py-8 max-w-5xl">

<!-- Page header -->
<div class="flex items-center justify-between mb-8">
  <h1 class="text-2xl font-bold">Title</h1>
  <a href="/new" class="btn btn-primary">+ New</a>
</div>

<!-- Responsive grid -->
<div class="grid gap-4 sm:grid-cols-2 md:grid-cols-3">

<!-- Two-column detail -->
<div class="grid md:grid-cols-3 gap-6">
  <div class="md:col-span-2 space-y-6"><!-- Main --></div>
  <div class="space-y-6"><!-- Sidebar --></div>
</div>

<!-- Centered (auth pages) -->
<div class="min-h-screen flex flex-col items-center justify-center px-4 py-16">
```

---

## Page Patterns

### Empty State

```typescript
<div className="text-center py-16">
  <div className="text-4xl mb-4 opacity-20">~</div>
  <h3 className="text-xl font-semibold mb-2">No items yet.</h3>
  <p className="text-base-content/70 mb-6 max-w-sm mx-auto">
    Descriptive text about what will appear here.
  </p>
  <Link href="/items/new" className="btn btn-primary">
    Create Your First Item
  </Link>
</div>
```

### Error Handling Pattern

```typescript
try {
  const data = await itemsApi.create(formData);
  toast.success('Item created!');
  router.push(`/items/${data.uuid}`);
} catch (error) {
  if (error instanceof ApiError) {
    toast.error(error.message);
  }
} finally {
  setSubmitting(false);
}
```

### Image Pattern

```typescript
import Image from 'next/image';

<Image
  src="/images/logo.png"
  alt="Logo"
  width={574}
  height={177}
  className="h-9 w-auto"
  priority  // Only for above-the-fold
/>
```

---

## Docker (REQUIRED — do not skip)

### Dockerfile.dev

```dockerfile
FROM node:22-alpine

WORKDIR /app

# Install dependencies first for layer caching
COPY package.json package-lock.json* ./
RUN npm install

# Copy application code
COPY . .

EXPOSE 3000

ENV HOSTNAME=0.0.0.0
CMD ["npm", "run", "dev"]
```

### docker-compose.yml

```yaml
name: {compose-project}

services:
  web:
    build:
      context: .
      dockerfile: Dockerfile.dev
    volumes:
      - .:/app
      - /app/node_modules
      - /app/.next
    ports:
      - "{host_port}:3000"
    env_file:
      - .env.local
    environment:
      - WATCHPACK_POLLING=true
```

Key details:
- Anonymous volumes for `node_modules` and `.next` prevent host overwriting container installs
- `WATCHPACK_POLLING=true` enables hot reload inside Docker (required on macOS with bind mounts)
- Container always listens on port 3000; `{host_port}` maps the host side

### Makefile

```makefile
# {compose-project} - Makefile
PROJECT_NAME = {compose-project}
DOCKER_COMPOSE = docker compose --project-name $(PROJECT_NAME)

# ============================================================================
# Docker
# ============================================================================

.PHONY: build up down restart stop ps logs bash wipe

build:
	$(DOCKER_COMPOSE) build

up:
	$(DOCKER_COMPOSE) up --detach

down:
	$(DOCKER_COMPOSE) down

restart: down up

stop:
	$(DOCKER_COMPOSE) stop

ps:
	$(DOCKER_COMPOSE) ps

logs:
	$(DOCKER_COMPOSE) logs -f web

bash:
	$(DOCKER_COMPOSE) exec web sh

wipe:
	@echo "WARNING: This will delete all containers and volumes!"
	@read -p "Are you sure? [y/N] " confirm && [ "$$confirm" = "y" ]
	$(DOCKER_COMPOSE) down -v --remove-orphans

# ============================================================================
# Development
# ============================================================================

.PHONY: dev lint lint-fix typecheck

dev: up logs

lint:
	$(DOCKER_COMPOSE) exec web npm run lint

lint-fix:
	$(DOCKER_COMPOSE) exec web npm run lint:fix

typecheck:
	$(DOCKER_COMPOSE) exec web npm run typecheck

# ============================================================================
# Dependencies
# ============================================================================

.PHONY: install add

install:
	$(DOCKER_COMPOSE) exec web npm install

add:
	$(DOCKER_COMPOSE) exec web npm install $(filter-out $@,$(MAKECMDGOALS))

# ============================================================================
# Build
# ============================================================================

.PHONY: build-next

build-next:
	$(DOCKER_COMPOSE) exec web npm run build

# Catch-all for npm commands
%:
	@:
```

---

## Post-Bootstrap Checklist

1. Create project directory
2. Generate all files from templates above (replace placeholders)
3. Verify Docker files exist: `Dockerfile.dev`, `docker-compose.yml`, `Makefile`
4. Copy `.env.local` from template above
5. `make build && make up`
6. Verify page loads at `http://localhost:{host_port}`
7. `make lint` — should pass cleanly
8. `make typecheck` — should pass cleanly
9. For frontend-centric: verify login page renders at `/login`
10. If Agentation: verify `.mcp.json` exists at project root
11. Commit initial scaffold
