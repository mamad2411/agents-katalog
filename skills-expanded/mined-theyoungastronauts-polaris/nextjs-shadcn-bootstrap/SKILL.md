---
name: nextjs-shadcn-bootstrap
description: "Scaffold a Next.js app with ShadCN UI (Tailwind v4, next-themes)."
disable-model-invocation: true
---

# Next.js Bootstrap (ShadCN UI)

On-demand command for scaffolding a new Next.js application with Docker, App Router, ShadCN UI, Tailwind v4, and standard conventions.

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
│   │   ├── ui/                      # ShadCN components (auto-generated)
│   │   │   ├── button.tsx
│   │   │   ├── input.tsx
│   │   │   ├── label.tsx
│   │   │   ├── card.tsx
│   │   │   ├── dialog.tsx
│   │   │   ├── badge.tsx
│   │   │   └── sonner.tsx
│   │   └── <feature>/
│   ├── contexts/                  # Frontend-centric mode
│   │   └── UserContext.tsx
│   ├── lib/
│   │   ├── api.ts
│   │   ├── auth.ts                # Frontend-centric mode
│   │   ├── constants.ts
│   │   ├── utils.ts               # cn() utility
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
├── components.json                # ShadCN configuration
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
    "sonner": "^2",
    "class-variance-authority": "^0.7",
    "clsx": "^2",
    "tailwind-merge": "^3",
    "lucide-react": "^0.400",
    "next-themes": "^0.4"
  },
  "devDependencies": {
    "typescript": "^5",
    "tailwindcss": "^4",
    "@tailwindcss/postcss": "^4",
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

**Note**: Additional `@radix-ui/*` packages will be installed automatically when adding ShadCN components via the CLI (see Post-Bootstrap section).

### components.json

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "",
    "css": "src/app/globals.css",
    "baseColor": "zinc",
    "cssVariables": true
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui",
    "lib": "@/lib",
    "hooks": "@/lib/hooks"
  }
}
```

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

### src/lib/utils.ts

```typescript
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

### src/app/globals.css

```css
@import "tailwindcss";

@custom-variant dark (&:where(.dark, .dark *));

@theme {
  --color-background: oklch(100% 0 0);
  --color-foreground: oklch(14.5% 0.025 264);
  --color-card: oklch(100% 0 0);
  --color-card-foreground: oklch(14.5% 0.025 264);
  --color-popover: oklch(100% 0 0);
  --color-popover-foreground: oklch(14.5% 0.025 264);
  --color-primary: oklch(14.5% 0.025 264);
  --color-primary-foreground: oklch(98% 0.01 264);
  --color-secondary: oklch(96% 0.01 264);
  --color-secondary-foreground: oklch(14.5% 0.025 264);
  --color-muted: oklch(96% 0.01 264);
  --color-muted-foreground: oklch(46% 0.02 264);
  --color-accent: oklch(96% 0.01 264);
  --color-accent-foreground: oklch(14.5% 0.025 264);
  --color-destructive: oklch(53% 0.22 27);
  --color-destructive-foreground: oklch(98% 0.01 264);
  --color-border: oklch(91% 0.01 264);
  --color-input: oklch(91% 0.01 264);
  --color-ring: oklch(14.5% 0.025 264);
  --color-sidebar-background: oklch(98% 0.01 264);
  --color-sidebar-foreground: oklch(46% 0.02 264);
  --color-sidebar-primary: oklch(14.5% 0.025 264);
  --color-sidebar-primary-foreground: oklch(98% 0.01 264);
  --color-sidebar-accent: oklch(96% 0.01 264);
  --color-sidebar-accent-foreground: oklch(14.5% 0.025 264);
  --color-sidebar-border: oklch(91% 0.01 264);
  --color-sidebar-ring: oklch(14.5% 0.025 264);

  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-xl: 0.75rem;
}

.dark {
  --color-background: oklch(14.5% 0.025 264);
  --color-foreground: oklch(98% 0.01 264);
  --color-card: oklch(14.5% 0.025 264);
  --color-card-foreground: oklch(98% 0.01 264);
  --color-popover: oklch(14.5% 0.025 264);
  --color-popover-foreground: oklch(98% 0.01 264);
  --color-primary: oklch(98% 0.01 264);
  --color-primary-foreground: oklch(14.5% 0.025 264);
  --color-secondary: oklch(22% 0.02 264);
  --color-secondary-foreground: oklch(98% 0.01 264);
  --color-muted: oklch(22% 0.02 264);
  --color-muted-foreground: oklch(65% 0.02 264);
  --color-accent: oklch(22% 0.02 264);
  --color-accent-foreground: oklch(98% 0.01 264);
  --color-destructive: oklch(63% 0.22 25);
  --color-destructive-foreground: oklch(98% 0.01 264);
  --color-border: oklch(22% 0.02 264);
  --color-input: oklch(22% 0.02 264);
  --color-ring: oklch(83% 0.02 264);
  --color-sidebar-background: oklch(14.5% 0.025 264);
  --color-sidebar-foreground: oklch(65% 0.02 264);
  --color-sidebar-primary: oklch(98% 0.01 264);
  --color-sidebar-primary-foreground: oklch(14.5% 0.025 264);
  --color-sidebar-accent: oklch(22% 0.02 264);
  --color-sidebar-accent-foreground: oklch(98% 0.01 264);
  --color-sidebar-border: oklch(22% 0.02 264);
  --color-sidebar-ring: oklch(83% 0.02 264);
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground antialiased;
  }
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
    <html lang="en" suppressHydrationWarning>
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased`}>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```

**If Agentation enabled**: Add the import and component inside `<body>`, before the closing `</body>`:

```tsx
import { Agentation } from "agentation";

// Add after Providers, before </body>:
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
// ShadCN components are imported directly from @/components/ui/<component>
// Add custom shared components here:
// export { default as Breadcrumbs } from './Breadcrumbs';
```

### src/components/layout/Header.tsx

```typescript
'use client';

import Link from 'next/link';

export default function Header() {
  return (
    <header className="border-b border-border bg-background">
      <div className="container mx-auto flex h-14 max-w-5xl items-center px-4">
        <div className="flex-1">
          <Link href="/" className="text-xl font-bold text-primary">
            {app-title}
          </Link>
        </div>
        <div className="flex items-center gap-2">
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
import { ThemeProvider } from 'next-themes';
import { Toaster } from 'sonner';
import { UserProvider } from '@/contexts/UserContext';

export default function Providers({ children }: { children: ReactNode }) {
  return (
    <ThemeProvider attribute="class" defaultTheme="dark" enableSystem disableTransitionOnChange>
      <UserProvider>
        {children}
        <Toaster richColors position="top-right" />
      </UserProvider>
    </ThemeProvider>
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
import { Loader2 } from 'lucide-react';
import { useRequireAuth } from '@/lib/hooks';
import Header from './Header';

export default function AppLayout({ children }: { children: ReactNode }) {
  const { loading } = useRequireAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
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
import { toast } from 'sonner';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Loader2 } from 'lucide-react';

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
      <Card className="w-full max-w-sm">
        <CardHeader className="text-center">
          <CardTitle className="text-2xl">{app-title}</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : 'Sign In'}
            </Button>
          </form>
          <p className="text-center mt-4 text-sm text-muted-foreground">
            <Link href="/forgot-password" className="text-primary hover:underline">
              Forgot password?
            </Link>
          </p>
        </CardContent>
      </Card>
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
import { ThemeProvider } from 'next-themes';
import { Toaster } from 'sonner';

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
    <ThemeProvider attribute="class" defaultTheme="dark" enableSystem disableTransitionOnChange>
      <QueryClientProvider client={queryClient}>
        {children}
        <Toaster richColors position="top-right" />
      </QueryClientProvider>
    </ThemeProvider>
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

import { Button } from '@/components/ui/button';

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
      <p className="text-muted-foreground mb-6">{error.message}</p>
      <Button onClick={reset}>Try again</Button>
    </div>
  );
}
```

### loading.tsx pattern (SSR-Centric)

```typescript
import { Loader2 } from 'lucide-react';

export default function Loading() {
  return (
    <div className="flex justify-center py-16">
      <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
    </div>
  );
}
```

### Server Component data fetching (SSR-Centric)

```typescript
// src/app/items/page.tsx (Server Component)
import { itemsApi } from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export default async function ItemsPage() {
  const items = await itemsApi.list();

  return (
    <main className="container mx-auto px-4 py-8 max-w-5xl">
      <h1 className="text-2xl font-bold mb-8">Items</h1>
      <div className="grid gap-4 sm:grid-cols-2">
        {items.map((item) => (
          <Card key={item.uuid}>
            <CardHeader>
              <CardTitle className="text-lg">{item.title}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground text-sm">{item.description}</p>
            </CardContent>
          </Card>
        ))}
      </div>
    </main>
  );
}
```

---

## ShadCN UI Patterns Reference

### Semantic Colors

| Token | Usage |
|-------|-------|
| `bg-background` | Primary page background |
| `bg-card` | Card/section background |
| `bg-muted` | Subtle/elevated background |
| `text-foreground` | Primary text |
| `text-muted-foreground` | Secondary/muted text |
| `text-primary` | Accent color text |
| `border-border` | Default borders |
| `bg-primary text-primary-foreground` | Primary buttons/badges |
| `bg-destructive text-destructive-foreground` | Error/delete actions |
| `bg-secondary text-secondary-foreground` | Secondary actions |
| `bg-accent text-accent-foreground` | Hover/active states |

### Component Import Pattern

Always import ShadCN components from `@/components/ui/<component>`:

```typescript
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '@/components/ui/card';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter, DialogTrigger } from '@/components/ui/dialog';
import { Badge } from '@/components/ui/badge';
```

### Buttons

```tsx
<Button>Primary</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="outline">Outline</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="destructive">Destructive</Button>
<Button variant="link">Link</Button>
<Button size="sm">Small</Button>
<Button size="lg">Large</Button>
<Button size="icon"><Loader2 className="h-4 w-4" /></Button>
<Button disabled><Loader2 className="mr-2 h-4 w-4 animate-spin" />Loading</Button>
```

### Cards

```tsx
<Card>
  <CardHeader>
    <CardTitle className="text-lg">Title</CardTitle>
    <CardDescription>Description text</CardDescription>
  </CardHeader>
  <CardContent>
    <p className="text-muted-foreground text-sm">Content here</p>
  </CardContent>
  <CardFooter className="flex justify-end gap-2">
    <Button variant="ghost" size="sm">Cancel</Button>
    <Button size="sm">Action</Button>
  </CardFooter>
</Card>
```

### Badges

```typescript
const statusVariants: Record<string, "default" | "secondary" | "destructive" | "outline"> = {
  active: 'default',
  paused: 'secondary',
  completed: 'outline',
  failed: 'destructive',
};
<Badge variant={statusVariants[status]} className="capitalize">{status}</Badge>
```

### Forms

```tsx
<div className="space-y-2">
  <Label htmlFor="field">Field Name</Label>
  <Input id="field" type="text" placeholder="Enter value..." />
</div>
```

### Dialogs (Modals)

```tsx
<Dialog open={isOpen} onOpenChange={setIsOpen}>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Title</DialogTitle>
      <DialogDescription>Description text</DialogDescription>
    </DialogHeader>
    <div className="py-4">
      {/* Dialog body */}
    </div>
    <DialogFooter>
      <Button variant="ghost" onClick={() => setIsOpen(false)}>Cancel</Button>
      <Button onClick={onConfirm}>Confirm</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

### Loading Spinner

```tsx
import { Loader2 } from 'lucide-react';

<div className="flex justify-center py-16">
  <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
</div>
```

### Toast Notifications

```typescript
import { toast } from 'sonner';

toast.success('Item created!');
toast.error('Something went wrong');
toast.info('Processing...');
toast.warning('Are you sure?');
```

### Layout Patterns

```html
<!-- Page container -->
<main class="container mx-auto px-4 py-8 max-w-5xl">

<!-- Page header -->
<div class="flex items-center justify-between mb-8">
  <h1 class="text-2xl font-bold">Title</h1>
  <Button asChild><a href="/new">+ New</a></Button>
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

### Dark Mode Toggle

```tsx
'use client';

import { useTheme } from 'next-themes';
import { Button } from '@/components/ui/button';
import { Moon, Sun } from 'lucide-react';

export function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
    >
      <Sun className="h-4 w-4 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
      <Moon className="absolute h-4 w-4 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
      <span className="sr-only">Toggle theme</span>
    </Button>
  );
}
```

---

## Page Patterns

### Empty State

```typescript
<div className="text-center py-16">
  <div className="text-4xl mb-4 opacity-20">~</div>
  <h3 className="text-xl font-semibold mb-2">No items yet.</h3>
  <p className="text-muted-foreground mb-6 max-w-sm mx-auto">
    Descriptive text about what will appear here.
  </p>
  <Button asChild>
    <Link href="/items/new">Create Your First Item</Link>
  </Button>
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
# ShadCN UI
# ============================================================================

.PHONY: shadcn-add

shadcn-add:
	$(DOCKER_COMPOSE) exec web npx shadcn@latest add $(filter-out $@,$(MAKECMDGOALS))

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
6. Install ShadCN components inside the container:
   ```bash
   make shadcn-add button input label card dialog badge sonner
   ```
7. Verify page loads at `http://localhost:{host_port}`
8. `make lint` — should pass cleanly
9. `make typecheck` — should pass cleanly
10. For frontend-centric: verify login page renders at `/login`
11. If Agentation: verify `.mcp.json` exists at project root
12. Commit initial scaffold
