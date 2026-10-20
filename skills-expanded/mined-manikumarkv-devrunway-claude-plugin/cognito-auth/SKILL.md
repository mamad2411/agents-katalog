---
name: cognito-auth
description: Scaffold a complete AWS Cognito authentication flow — frontend (Amplify, useAuth hook, LoginForm, API client with token refresh) and/or backend (JWT middleware, requireGroup).
argument-hint: [frontend|backend|fullstack]
user-invocable: true
stack: auth/cognito
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(ls *)
  - Bash(grep *)
  - Bash(npm *)
---

# Scaffold Cognito Auth

Type: `$ARGUMENTS` (default: `fullstack`).

First, detect context: look for `src/App.tsx` / `vite.config.ts` (frontend) and `express` in `package.json` / `src/app.ts` (backend). Scaffold accordingly, or use the explicit argument.

## Frontend Auth

Install if missing: `npm install aws-amplify`

**`src/config/aws.ts`**
```ts
import { Amplify } from 'aws-amplify';
// Legacy projects: import awsconfig from './aws-exports'; Amplify.configure(awsconfig);
// New projects: configure directly with env vars

Amplify.configure({
  Auth: {
    Cognito: {
      userPoolId: import.meta.env.VITE_COGNITO_USER_POOL_ID,
      userPoolClientId: import.meta.env.VITE_COGNITO_CLIENT_ID,
      loginWith: { email: true },
    },
  },
});
```

**`src/features/auth/types.ts`**
```ts
export interface AuthUser {
  sub: string;
  email: string;
  groups: string[];
}

export interface AuthState {
  user: AuthUser | null;
  isLoading: boolean;
  isAuthenticated: boolean;
}
```

**`src/features/auth/hooks/useAuth.ts`**
```ts
import { useState, useEffect, useCallback } from 'react';
import { signIn, signOut, getCurrentUser, fetchAuthSession, type SignInInput } from 'aws-amplify/auth';
import type { AuthUser, AuthState } from '../types';

export function useAuth() {
  const [state, setState] = useState<AuthState>({ user: null, isLoading: true, isAuthenticated: false });

  const loadUser = useCallback(async () => {
    try {
      const { username } = await getCurrentUser();
      const session = await fetchAuthSession();
      const payload = session.tokens?.accessToken.payload;
      setState({
        user: { sub: username, email: payload?.email as string ?? '', groups: (payload?.['cognito:groups'] as string[]) ?? [] },
        isLoading: false,
        isAuthenticated: true,
      });
    } catch {
      setState({ user: null, isLoading: false, isAuthenticated: false });
    }
  }, []);

  useEffect(() => { loadUser(); }, [loadUser]);

  const login = useCallback(async (input: SignInInput) => {
    await signIn(input);
    await loadUser();
  }, [loadUser]);

  const logout = useCallback(async () => {
    await signOut();
    setState({ user: null, isLoading: false, isAuthenticated: false });
  }, []);

  return { ...state, login, logout, refresh: loadUser };
}
```

**`src/features/auth/hooks/useRequireAuth.ts`**
```ts
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from './useAuth';

export function useRequireAuth(redirectTo = '/login') {
  const { isAuthenticated, isLoading } = useAuth();
  const navigate = useNavigate();
  useEffect(() => {
    if (!isLoading && !isAuthenticated) navigate(redirectTo, { replace: true });
  }, [isAuthenticated, isLoading, navigate, redirectTo]);
  return { isLoading };
}
```

**`src/services/api.ts`** (authenticated API client with refresh-and-retry)
```ts
import { fetchAuthSession } from 'aws-amplify/auth';

const BASE_URL = import.meta.env.VITE_API_BASE_URL;

async function getToken(forceRefresh = false) {
  const session = await fetchAuthSession({ forceRefresh });
  const token = session.tokens?.accessToken.toString();
  if (!token) throw new Error('Not authenticated');
  return token;
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const authHeaders = (token: string) => ({
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token}`,
    ...options.headers,
  });

  let res = await fetch(`${BASE_URL}${path}`, { ...options, headers: authHeaders(await getToken()) });

  if (res.status === 401) {
    res = await fetch(`${BASE_URL}${path}`, { ...options, headers: authHeaders(await getToken(true)) });
  }

  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json() as Promise<T>;
}

export const api = {
  get: <T>(path: string) => request<T>(path),
  post: <T>(path: string, body: unknown) => request<T>(path, { method: 'POST', body: JSON.stringify(body) }),
  patch: <T>(path: string, body: unknown) => request<T>(path, { method: 'PATCH', body: JSON.stringify(body) }),
  delete: <T>(path: string) => request<T>(path, { method: 'DELETE' }),
};
```

**`src/features/auth/components/LoginForm/LoginForm.tsx`**

The login form is the first screen every user meets and the one most often
screen-read, so it follows the universal `accessibility` skill exactly:

- Every field has a real `<label>` associated with `htmlFor` + `id`. A `placeholder`
  is not a label — it disappears the moment the user types, and it is the single most
  common accessibility defect in auth forms
- No `aria-label` on the fields: it would duplicate the visible label text, which the
  `accessibility` skill forbids
- The submit error is rendered with `role="alert"` **and** linked to both fields with
  `aria-describedby`, so a screen reader announces it when either field is focused
- `autoComplete` set so password managers can fill the form

```tsx
import { useState } from 'react';
import { useAuth } from '../../hooks/useAuth';

export function LoginForm() {
  const { login } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setIsLoading(true);
    try {
      await login({ username: email, password });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed');
    } finally {
      setIsLoading(false);
    }
  }

  const errorId = 'login-error';
  const describedBy = error ? errorId : undefined;

  return (
    <form onSubmit={handleSubmit} noValidate>
      <label htmlFor="login-email">Email</label>
      <input
        id="login-email"
        type="email"
        autoComplete="username"
        value={email}
        onChange={e => setEmail(e.target.value)}
        required
        aria-required="true"
        aria-invalid={!!error}
        aria-describedby={describedBy}
      />

      <label htmlFor="login-password">Password</label>
      <input
        id="login-password"
        type="password"
        autoComplete="current-password"
        value={password}
        onChange={e => setPassword(e.target.value)}
        required
        aria-required="true"
        aria-invalid={!!error}
        aria-describedby={describedBy}
      />

      {error && <p id={errorId} role="alert">{error}</p>}
      <button type="submit" disabled={isLoading}>{isLoading ? 'Signing in…' : 'Sign In'}</button>
    </form>
  );
}
```

**`src/features/auth/index.ts`**
```ts
export { LoginForm } from './components/LoginForm/LoginForm';
export { useAuth } from './hooks/useAuth';
export { useRequireAuth } from './hooks/useRequireAuth';
export type { AuthUser, AuthState } from './types';
```

Add to `.env.local` (remind user):
```
VITE_COGNITO_USER_POOL_ID=us-east-1_XXXXXXXXX
VITE_COGNITO_CLIENT_ID=XXXXXXXXXXXXXXXXXXXXXXXXXX
VITE_API_BASE_URL=https://api.yourdomain.com
```

---

## Backend Auth

Install if missing: `npm install aws-jwt-verify`

**`src/middleware/auth.ts`**
```ts
import { CognitoJwtVerifier } from 'aws-jwt-verify';
import type { Request, RequestHandler, Response, NextFunction } from 'express';

const verifier = CognitoJwtVerifier.create({
  userPoolId: process.env.COGNITO_USER_POOL_ID!,
  tokenUse: 'access',
  clientId: process.env.COGNITO_CLIENT_ID!,
});

export interface AuthenticatedRequest extends Request {
  user: { sub: string; email: string; groups: string[] };
}

export const authMiddleware: RequestHandler = async (req, res: Response, next: NextFunction) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ success: false, error: { code: 'MISSING_TOKEN', message: 'Authorization header required' } });
  try {
    const payload = await verifier.verify(token);
    (req as AuthenticatedRequest).user = {
      sub: payload.sub,
      email: payload.email as string,
      groups: (payload['cognito:groups'] as string[]) ?? [],
    };
    next();
  } catch {
    res.status(401).json({ success: false, error: { code: 'INVALID_TOKEN', message: 'Invalid or expired token' } });
  }
};
```

**`src/middleware/requireGroup.ts`**
```ts
import type { RequestHandler } from 'express';
import type { AuthenticatedRequest } from './auth';

export function requireGroup(...groups: string[]): RequestHandler {
  return (req, res, next) => {
    const user = (req as AuthenticatedRequest).user;
    if (!user) return res.status(401).json({ success: false, error: { code: 'UNAUTHENTICATED', message: 'Authentication required' } });
    if (!groups.some(g => user.groups.includes(g)))
      return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Insufficient permissions' } });
    next();
  };
}
// Usage: router.delete('/:id', authMiddleware, requireGroup('Admin'), controller.remove);
```

Add to `.env`:
```
COGNITO_USER_POOL_ID=us-east-1_XXXXXXXXX
COGNITO_CLIENT_ID=XXXXXXXXXXXXXXXXXXXXXXXXXX
```

---

## Summary

Print all created files and next steps:
```
Cognito Auth Scaffolded ✅
===========================
Files created:
  [list]

Next steps:
1. Set environment variables (see above)
2. Call Amplify.configure() in src/main.tsx before rendering <App />
3. Apply authMiddleware to protected routes
4. Use requireGroup('Admin') for admin-only endpoints
5. Test login flow end-to-end against your Cognito User Pool
```
