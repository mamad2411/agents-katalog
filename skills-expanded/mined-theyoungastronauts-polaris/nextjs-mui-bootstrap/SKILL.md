---
name: nextjs-mui-bootstrap
description: "Scaffold a Next.js app with Material UI (Emotion SSR, MUI v7)."
disable-model-invocation: true
---

# Next.js Bootstrap (Material UI)

On-demand command for scaffolding a new Next.js application with Docker, App Router, Material UI (MUI v7), Emotion, and standard conventions.

> **MANDATORY: This project runs entirely in Docker.**
> Every Docker file below (Dockerfile.dev, docker-compose.yml, Makefile) MUST be generated.
> The Makefile is the sole interface — never run `npm` directly on the host.

> **MUI component reference**: For detailed component APIs, props, and usage patterns, see https://mui.com/material-ui/llms.txt

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
│   ├── theme.ts                   # MUI theme configuration
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
├── .nvmrc
├── .env.local
├── .gitignore
├── Dockerfile.dev
├── docker-compose.yml
├── Makefile
└── .mcp.json                 # If Agentation enabled
```

**Note**: No `postcss.config.mjs` or `globals.css` — MUI handles all styling via Emotion. No Tailwind.

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
    "@mui/material": "^7",
    "@mui/icons-material": "^7",
    "@mui/material-nextjs": "^7",
    "@emotion/react": "^11",
    "@emotion/styled": "^11",
    "dayjs": "^1.11",
    "sonner": "^2"
  },
  "devDependencies": {
    "typescript": "^5",
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

### src/theme.ts

```typescript
'use client';

import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  cssVariables: {
    colorSchemeSelector: 'data',
  },
  colorSchemes: {
    light: {
      palette: {
        primary: {
          main: '#1976d2',
        },
        secondary: {
          main: '#9c27b0',
        },
        background: {
          default: '#fafafa',
          paper: '#ffffff',
        },
      },
    },
    dark: {
      palette: {
        primary: {
          main: '#90caf9',
        },
        secondary: {
          main: '#ce93d8',
        },
        background: {
          default: '#121212',
          paper: '#1e1e1e',
        },
      },
    },
  },
  typography: {
    fontFamily: 'var(--font-roboto)',
  },
  shape: {
    borderRadius: 8,
  },
});

export default theme;
```

### src/app/layout.tsx

```typescript
import type { Metadata } from "next";
import { Roboto } from "next/font/google";
import InitColorSchemeScript from "@mui/material/InitColorSchemeScript";
import { AppRouterCacheProvider } from "@mui/material-nextjs/v16-appRouter";
import { ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import theme from "@/theme";
import Providers from "@/components/Providers";

const roboto = Roboto({
  weight: ["300", "400", "500", "700"],
  subsets: ["latin"],
  display: "swap",
  variable: "--font-roboto",
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
      <body className={roboto.variable}>
        <InitColorSchemeScript attribute="data-mui-color-scheme" />
        <AppRouterCacheProvider options={{ enableCssLayer: true }}>
          <ThemeProvider theme={theme}>
            <CssBaseline enableColorScheme />
            <Providers>{children}</Providers>
          </ThemeProvider>
        </AppRouterCacheProvider>
      </body>
    </html>
  );
}
```

**If Agentation enabled**: Add the import and component inside `<body>`, before the closing `</body>`:

```tsx
import { Agentation } from "agentation";

// Add after AppRouterCacheProvider closing tag, before </body>:
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

### src/components/layout/Header.tsx

```typescript
'use client';

import Link from 'next/link';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';

export default function Header() {
  return (
    <AppBar position="static" color="default" elevation={0} sx={{ borderBottom: 1, borderColor: 'divider' }}>
      <Container maxWidth="md">
        <Toolbar disableGutters>
          <Typography
            variant="h6"
            component={Link}
            href="/"
            sx={{ flexGrow: 1, textDecoration: 'none', color: 'primary.main', fontWeight: 700 }}
          >
            {app-title}
          </Typography>
          {/* Navigation items */}
        </Toolbar>
      </Container>
    </AppBar>
  );
}
```

### src/app/page.tsx

```typescript
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';

export default function HomePage() {
  return (
    <Container maxWidth="md" sx={{ py: 8 }}>
      <Typography variant="h3" component="h1" fontWeight="bold">
        {app-title}
      </Typography>
    </Container>
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
import { Toaster } from 'sonner';
import { UserProvider } from '@/contexts/UserContext';

export default function Providers({ children }: { children: ReactNode }) {
  return (
    <UserProvider>
      {children}
      <Toaster richColors position="top-right" />
    </UserProvider>
  );
}
```

**Note**: `ThemeProvider`, `CssBaseline`, and `AppRouterCacheProvider` are already in `layout.tsx`. Providers only handles app-level context (auth, toasts).

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
import Box from '@mui/material/Box';
import CircularProgress from '@mui/material/CircularProgress';
import Container from '@mui/material/Container';
import { useRequireAuth } from '@/lib/hooks';
import Header from './Header';

export default function AppLayout({ children }: { children: ReactNode }) {
  const { loading } = useRequireAuth();

  if (loading) {
    return (
      <Box sx={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <>
      <Header />
      <Container component="main" maxWidth="md" sx={{ py: 4, flex: 1 }}>
        {children}
      </Container>
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
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import CircularProgress from '@mui/material/CircularProgress';
import MuiLink from '@mui/material/Link';
import { useUser } from '@/contexts/UserContext';
import { ApiError } from '@/lib/api';
import { toast } from 'sonner';

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
    <Box sx={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', px: 2, py: 8 }}>
      <Card sx={{ width: '100%', maxWidth: 400 }}>
        <CardContent sx={{ p: 4 }}>
          <Typography variant="h5" component="h1" align="center" fontWeight="bold" gutterBottom>
            {app-title}
          </Typography>
          <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2, display: 'flex', flexDirection: 'column', gap: 2.5 }}>
            <TextField
              label="Email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              fullWidth
              size="small"
            />
            <TextField
              label="Password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              fullWidth
              size="small"
            />
            <Button
              type="submit"
              variant="contained"
              fullWidth
              disabled={loading}
              sx={{ mt: 1 }}
            >
              {loading ? <CircularProgress size={24} color="inherit" /> : 'Sign In'}
            </Button>
          </Box>
          <Typography variant="body2" align="center" sx={{ mt: 2, color: 'text.secondary' }}>
            <MuiLink component={Link} href="/forgot-password" color="primary">
              Forgot password?
            </MuiLink>
          </Typography>
        </CardContent>
      </Card>
    </Box>
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
    <QueryClientProvider client={queryClient}>
      {children}
      <Toaster richColors position="top-right" />
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

  if (publicPaths.some((path) => pathname.startsWith(path))) {
    return NextResponse.next();
  }

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

import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <Box sx={{ minHeight: '50vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
      <Typography variant="h5" fontWeight="bold" gutterBottom>
        Something went wrong
      </Typography>
      <Typography color="text.secondary" sx={{ mb: 3 }}>
        {error.message}
      </Typography>
      <Button variant="contained" onClick={reset}>
        Try again
      </Button>
    </Box>
  );
}
```

### loading.tsx pattern (SSR-Centric)

```typescript
import Box from '@mui/material/Box';
import CircularProgress from '@mui/material/CircularProgress';

export default function Loading() {
  return (
    <Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}>
      <CircularProgress />
    </Box>
  );
}
```

### Server Component data fetching (SSR-Centric)

```typescript
// src/app/items/page.tsx (Server Component)
import { itemsApi } from '@/lib/api';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';

export default async function ItemsPage() {
  const items = await itemsApi.list();

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" fontWeight="bold" sx={{ mb: 4 }}>
        Items
      </Typography>
      <Grid container spacing={2}>
        {items.map((item) => (
          <Grid key={item.uuid} size={{ xs: 12, sm: 6 }}>
            <Card variant="outlined">
              <CardContent>
                <Typography variant="subtitle1" fontWeight="bold">
                  {item.title}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {item.description}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
}
```

---

## MUI Patterns Reference

### Styling with the `sx` Prop

The `sx` prop is the primary styling API. It accepts theme-aware values:

```tsx
// Theme spacing — 1 unit = 8px by default
<Box sx={{ p: 2, mt: 4 }}>  {/* padding: 16px, margin-top: 32px */}

// Theme palette colors
<Box sx={{ color: 'primary.main', bgcolor: 'background.paper' }}>

// Responsive values
<Box sx={{ width: { xs: '100%', sm: '50%', md: '33%' } }}>

// Pseudo-selectors
<Box sx={{ '&:hover': { bgcolor: 'action.hover' } }}>
```

### Component Import Pattern

Import each component individually for optimal tree-shaking:

```typescript
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardActions from '@mui/material/CardActions';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';
import Chip from '@mui/material/Chip';
import CircularProgress from '@mui/material/CircularProgress';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Grid from '@mui/material/Grid';
import Stack from '@mui/material/Stack';
```

### Icons

```typescript
import AddIcon from '@mui/icons-material/Add';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import SearchIcon from '@mui/icons-material/Search';
import MenuIcon from '@mui/icons-material/Menu';
import CloseIcon from '@mui/icons-material/Close';
import DarkModeIcon from '@mui/icons-material/DarkMode';
import LightModeIcon from '@mui/icons-material/LightMode';
```

### Buttons

```tsx
<Button variant="contained">Primary</Button>
<Button variant="outlined">Outlined</Button>
<Button variant="text">Text</Button>
<Button variant="contained" color="error">Destructive</Button>
<Button variant="contained" color="secondary">Secondary</Button>
<Button size="small">Small</Button>
<Button size="large">Large</Button>
<Button variant="contained" startIcon={<AddIcon />}>Create</Button>
<Button disabled><CircularProgress size={20} sx={{ mr: 1 }} />Loading</Button>
```

### Cards

```tsx
<Card variant="outlined">
  <CardContent>
    <Typography variant="subtitle1" fontWeight="bold">
      Title
    </Typography>
    <Typography variant="body2" color="text.secondary">
      Description text
    </Typography>
  </CardContent>
  <CardActions sx={{ justifyContent: 'flex-end', px: 2, pb: 2 }}>
    <Button size="small">Cancel</Button>
    <Button size="small" variant="contained">Action</Button>
  </CardActions>
</Card>
```

### Chips (Badges)

```typescript
const statusColors: Record<string, 'success' | 'warning' | 'default' | 'error'> = {
  active: 'success',
  paused: 'warning',
  completed: 'default',
  failed: 'error',
};
<Chip label={status} color={statusColors[status]} size="small" sx={{ textTransform: 'capitalize' }} />
```

### Form Fields

```tsx
<TextField
  label="Field Name"
  type="text"
  value={value}
  onChange={(e) => setValue(e.target.value)}
  fullWidth
  size="small"
  required
  helperText="Optional helper text"
  error={!!fieldError}
/>
```

### Dialogs (Modals)

```tsx
<Dialog open={isOpen} onClose={() => setIsOpen(false)} maxWidth="sm" fullWidth>
  <DialogTitle>Title</DialogTitle>
  <DialogContent>
    <Typography color="text.secondary">Description text</Typography>
  </DialogContent>
  <DialogActions>
    <Button onClick={() => setIsOpen(false)}>Cancel</Button>
    <Button variant="contained" onClick={onConfirm}>Confirm</Button>
  </DialogActions>
</Dialog>
```

### Loading Spinner

```tsx
import CircularProgress from '@mui/material/CircularProgress';

<Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}>
  <CircularProgress />
</Box>
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

```tsx
{/* Page container */}
<Container maxWidth="md" sx={{ py: 4 }}>

{/* Page header */}
<Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 4 }}>
  <Typography variant="h4" fontWeight="bold">Title</Typography>
  <Button variant="contained" startIcon={<AddIcon />}>New</Button>
</Box>

{/* Responsive grid */}
<Grid container spacing={2}>
  <Grid size={{ xs: 12, sm: 6, md: 4 }}>...</Grid>
</Grid>

{/* Two-column detail */}
<Grid container spacing={3}>
  <Grid size={{ xs: 12, md: 8 }}>
    <Stack spacing={3}>{/* Main */}</Stack>
  </Grid>
  <Grid size={{ xs: 12, md: 4 }}>
    <Stack spacing={3}>{/* Sidebar */}</Stack>
  </Grid>
</Grid>

{/* Centered (auth pages) */}
<Box sx={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', px: 2, py: 8 }}>
```

### Dark Mode Toggle

```tsx
'use client';

import { useColorScheme } from '@mui/material/styles';
import IconButton from '@mui/material/IconButton';
import DarkModeIcon from '@mui/icons-material/DarkMode';
import LightModeIcon from '@mui/icons-material/LightMode';

export function ThemeToggle() {
  const { mode, setMode } = useColorScheme();

  return (
    <IconButton
      onClick={() => setMode(mode === 'dark' ? 'light' : 'dark')}
      color="inherit"
    >
      {mode === 'dark' ? <LightModeIcon /> : <DarkModeIcon />}
    </IconButton>
  );
}
```

---

## Page Patterns

### Empty State

```tsx
<Box sx={{ textAlign: 'center', py: 8 }}>
  <Typography variant="h4" sx={{ mb: 2, opacity: 0.2 }}>~</Typography>
  <Typography variant="h6" fontWeight="bold" gutterBottom>
    No items yet.
  </Typography>
  <Typography color="text.secondary" sx={{ mb: 3, maxWidth: 360, mx: 'auto' }}>
    Descriptive text about what will appear here.
  </Typography>
  <Button variant="contained" component={Link} href="/items/new">
    Create Your First Item
  </Button>
</Box>
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
  style={{ height: 36, width: 'auto' }}
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
