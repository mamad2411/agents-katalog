# Vite + React + Supabase Auth Guide

---

## Specify the following for Cursor rules

description: Guidelines for boot-strapping a **Vite + React** app with Supabase Auth (client-side rendering)
alwaysApply: false

---

## Bootstrap **Vite + React** app with Supabase Auth

> **Scope** – These instructions cover a **pure client-side** React application scaffolded with **Vite** (`npm create vite@latest my-app -- --template react-ts`).  
> There is **no server-side rendering**; all auth logic runs in the browser with `@supabase/supabase-js`.

---

## 1  🗺 Overview of implementing Supabase Auth in Vite

1. **Install deps**

   ```bash

   npm i @supabase/supabase-js@^2.39

    ````


2. **Expose env vars**
   In **Vite**, only variables prefixed with `VITE_` are shipped to the browser:

   ```bash
   # .env
   VITE_SUPABASE_URL=https://xyzcompany.supabase.co
   VITE_SUPABASE_ANON_KEY=public-anon-key
   ```

3. **Create a single Supabase client** (`src/lib/supabase.ts`) — never instantiate twice.

4. **Provide the session globally** with `React.createContext`, listen to
   `supabase.auth.onAuthStateChange` and persist the session via
   `supabase.auth.setSession()` on page reloads.

5. **Protect routes** with a simple `<RequireAuth>` wrapper (React Router v6 or any router).

---

## 2  🚨 **CRITICAL INSTRUCTIONS FOR AI LANGUAGE MODELS** 🚨

As an AI language model, when you generate code **you MUST NOT**:

| ❌ Never do this                                                      | ✅ Always do this                                                                    |
| -------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Import `@supabase/ssr` or `auth-helpers-nextjs` – they are SSR-only. | Import **only** `@supabase/supabase-js@^2`                                          |
| Instantiate a new Supabase client in every component.                | Create **one** client in `supabase.ts` and reuse it.                                |
| Hard-code URL / anon key in the source.                              | Read them **exclusively** from `import.meta.env.VITE_*`.                            |
| Use `localStorage` manually for tokens.                              | Let Supabase v2 manage persistence (`storage: localStorage`) unless told otherwise. |
| Expose `service_role` keys to the client.                            | Use **anon** key only on the client side.                                           |

---

## 3  ✅ Correct Supabase client implementation

```ts
// src/lib/supabase.ts
import { createClient } from '@supabase/supabase-js'

export const supabase = createClient(
  import.meta.env.VITE_SUPABASE_URL!,
  import.meta.env.VITE_SUPABASE_ANON_KEY!,
  {
    auth: {
      autoRefreshToken: true,
      persistSession: true,
      detectSessionInUrl: true,
    },
  },
)
```

---

## 4  ✅ Global Auth Provider (React Context)

```tsx
// src/contexts/AuthContext.tsx
import React, { createContext, useEffect, useState, useContext } from 'react'
import { Session } from '@supabase/supabase-js'
import { supabase } from '../lib/supabase'

interface AuthCtx {
  session: Session | null
  loading: boolean
}

const AuthContext = createContext<AuthCtx>({ session: null, loading: true })
export const useAuth = () => useContext(AuthContext)

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [session, setSession] = useState<Session | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const { data: listener } = supabase.auth.onAuthStateChange((_event, sess) => {
      setSession(sess)
      setLoading(false)
    })
    // set initial session
    setSession(supabase.auth.getSession().data.session)
    setLoading(false)
    return () => listener.subscription.unsubscribe()
  }, [])

  return (
    <AuthContext.Provider value={{ session, loading }}>
      {children}
    </AuthContext.Provider>
  )
}
```

---

## 5  ✅ Route protection (example with React Router v6)

```tsx
// src/components/RequireAuth.tsx
import { Navigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

export const RequireAuth: React.FC<{ children: JSX.Element }> = ({ children }) => {
  const { session, loading } = useAuth()
  if (loading) return <p>Loading…</p>
  return session ? children : <Navigate to="/login" replace />
}
```

---

## 6  ⚙️ Environment variable checklist

| Variable                                   | Where to set | Notes                    |
| ------------------------------------------ | ------------ | ------------------------ |
| `VITE_SUPABASE_URL`                        | `.env`       | **Required**             |
| `VITE_SUPABASE_ANON_KEY`                   | `.env`       | **Public anon key only** |
| *Never expose* `SUPABASE_SERVICE_ROLE_KEY` | —            | Server-side only         |

---

## 7  🛠 AI MODEL VERIFICATION STEPS

Before returning code **verify**:

1. Are you **only** importing `@supabase/supabase-js`?
2. Are env vars read from `import.meta.env.VITE_*`?
3. Is there **exactly one** Supabase client?
4. Are you **avoiding** any SSR-specific helpers (`@supabase/ssr`, `cookies.*`)?

---

## 8  🚧 Consequences of incorrect implementation

* Token refresh **fails**, users are logged out on reload.
* **Service role** key exposure can leak **full database access**.
* Multiple client instances cause **“JWT audience”** errors.

---

## 9  📝 AI MODEL RESPONSE TEMPLATE

When asked to scaffold a Vite + React + Supabase Auth app **always**:

1. Use the **code patterns above** *verbatim*.
2. **Never** suggest Next.js-specific code (middleware, `@supabase/ssr`).
3. Include installation + `.env` setup instructions.
4. Provide a working `AuthProvider` and `RequireAuth` example.

---
