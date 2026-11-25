---
name: saas-platform-builder
description: "Build full SaaS platforms: marketing site + auth-gated app + backend API + Stripe payments. Next.js 15 monorepo pattern with FastAPI backend, JWT auth, Vercel deployment."
version: 1.0.0
---

# SaaS Platform Builder

Build a complete SaaS platform in one go. Marketing site, auth-gated product, backend API, and Stripe checkout — all in a single Next.js monorepo with a Python/FastAPI backend.

## Architecture

```
curriculum-os-saas/
├── frontend/                # Next.js 15 monolith
│   └── src/app/
│       ├── page.tsx         # Marketing landing (public)
│       ├── features/        # Marketing page (public)
│       ├── pricing/         # Marketing + Stripe (public)
│       ├── how-it-works/    # Marketing page (public)
│       ├── about/           # Marketing page (public)
│       ├── login/           # Auth page (public)
│       ├── signup/          # Auth page (public)
│       ├── api/chat/        # LLM proxy (optional)
│       ├── api/stripe/      # Stripe checkout sessions
│       └── app/             # Auth-gated product
│           ├── layout.tsx   # Sidebar + auth guard
│           ├── page.tsx     # Dashboard
│           ├── chat/        # Main product feature
│           └── settings/    # User settings
├── backend/                 # FastAPI (separate deploy)
│   └── src/api/
│       ├── auth.py          # Register, login, me (JWT)
│       ├── routes.py        # Core product endpoints
│       ├── curriculum_store.py  # User data persistence
│       └── dependencies.py  # get_current_user, etc.
└── start.sh                 # Local dev launcher
```

## Page Inventory

### Public (7 pages — SEO, conversion)
| Route | Purpose |
|-------|---------|
| `/` | Hero, features grid, pricing preview, social proof, CTA |
| `/features` | Deep-dive on each feature with icons |
| `/pricing` | Free/Pro/Team tiers with Stripe or signup CTAs |
| `/how-it-works` | Numbered step-by-step with icons |
| `/about` | Mission, tech stack, team |
| `/login` | Email + password form |
| `/signup` | Name + email + password, plan-aware from query params |

### Product (4-5 pages — auth-gated)
| Route | Purpose |
|-------|---------|
| `/app` | Dashboard: stats, quick actions, recent items |
| `/app/chat` | Main product feature (chat UI) |
| `/app/curricula` | List saved items |
| `/app/curriculum/[id]` | Detail view of saved item |
| `/app/settings` | Profile, plan, sign out |

## Auth Pattern

### Supabase Signup: auto-detect email confirmation

Supabase `signUp()` returns a `session` object only when email confirmation is **disabled** in the project. When it's **enabled**, `data.session` is `null` and the user must click the email link. Detect this to avoid always showing a "check your email" screen:

```tsx
const { data, error } = await supabase.auth.signUp({ email, password });

if (data.session) {
  // Email confirmation is OFF — session available, redirect immediately
  router.push("/dashboard");
  return;
}

// Email confirmation is ON — show "check your email" UI
setConfirmNeeded(true);
```

To skip email confirmation entirely, disable it in Supabase Dashboard → Authentication → Settings → Email → uncheck "Confirm email."

### Frontend: AuthProvider context
```tsx
// src/lib/auth.tsx
"use client";
import { createContext, useContext, useState, useEffect } from "react";

const BACKEND = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const saved = localStorage.getItem("token");
    if (saved) {
      setToken(saved);
      fetch(`${BACKEND}/api/v1/auth/me`, {
        headers: { Authorization: `Bearer ${saved}` },
      }).then(r => r.ok ? r.json() : null)
        .then(data => { if (data?.id) setUser(data); })
        .finally(() => setLoading(false));
    } else setLoading(false);
  }, []);

  async function login(email, password) { /* POST /auth/login → store token */ }
  async function signup(email, password, name) { /* POST /auth/register → store token */ }
  function logout() { localStorage.removeItem("token"); setToken(null); setUser(null); }

  return <AuthContext.Provider value={{user,token,loading,login,signup,logout}}>{children}</AuthContext.Provider>;
}
```

### Root layout wraps with AuthProvider
```tsx
// src/app/layout.tsx
"use client";
import { AuthProvider } from "@/lib/auth";

export default function RootLayout({ children }) {
  return (
    <html lang="en" className="dark">
      <body><AuthProvider>{children}</AuthProvider></body>
    </html>
  );
}
```

### App layout guards with auth
```tsx
// src/app/app/layout.tsx
"use client";
import { useAuth } from "@/lib/auth";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function AppLayout({ children }) {
  const { user, loading } = useAuth();
  const router = useRouter();
  useEffect(() => { if (!loading && !user) router.push("/login"); }, [user, loading]);
  if (loading || !user) return <LoadingSpinner />;
  return <div className="flex"><Sidebar />{children}</div>;
}
```

### Backend: JWT auth with JSON file storage
```python
# Keep it simple for early-stage — JSON file, no DB needed
import hashlib, os, jwt, uuid

def _hash_password(password: str, salt: str) -> str:
    return hashlib.sha256((password + salt).encode()).hexdigest()

def _generate_token(user_id: str) -> str:
    payload = {"sub": user_id, "exp": datetime.now() + timedelta(days=7)}
    return jwt.encode(payload, config.JWT_SECRET, algorithm="HS256")

def get_current_user(credentials = Depends(bearer_scheme)):
    payload = jwt.decode(credentials.credentials, config.JWT_SECRET, algorithms=["HS256"])
    users = _load_users()  # from users.json
    for u in users:
        if u["id"] == payload["sub"]: return u
    raise HTTPException(401)
```

Key backend auth fields in responses:
- Register/login: `{ access_token: "...", token_type: "bearer", user: {...} }`
- GET /me: `{ id, email, name, plan, created_at }` (NOT wrapped in `{user: ...}`)

## Stripe Integration

See `references/plan-gating.md` for the full plan-gating architecture (tiered access, subscription management, Customer Portal, webhook handlers).

### No npm package needed — raw fetch to Stripe REST API

```tsx
// src/app/api/stripe/route.ts
export async function POST(req: NextRequest) {
  const { plan, email } = await req.json();
  const params = new URLSearchParams();
  params.append("line_items[0][price]", PRICE_IDS[plan]);
  params.append("mode", "subscription");
  params.append("success_url", `${req.nextUrl.origin}/app?checkout=success`);
  params.append("cancel_url", `${req.nextUrl.origin}/pricing`);

  const res = await fetch("https://api.stripe.com/v1/checkout/sessions", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${process.env.STRIPE_SECRET_KEY}`,
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: params.toString(),
  });
  return NextResponse.json({ url: (await res.json()).url });
}
```

### Pricing page buttons
```tsx
{t.plan === "free" ? (
  <Link href="/signup">Get Started</Link>
) : (
  <StripeCheckoutButton plan={t.plan} label={t.cta} />
)}
```

## Marketing Header Pattern

A persistent header used across all public pages:

```tsx
"use client";
// Fixed top header with logo, desktop nav, mobile hamburger
// Desktop: logo | Features Pricing HowItWorks | Sign In | CTA button
// Mobile: hamburger → slide-down menu
```

## Pitfalls

### `useSearchParams()` needs Suspense
Next.js 15 tries to SSG-prefetch pages using `useSearchParams()`. Extract the form into a child component and wrap the page's default export in `<Suspense>`. See `nextjs-app-router` skill for full fix pattern.

### `vercel.json` for Next.js
```json
{"framework": "nextjs"}
```
Never add `"public": true` — it breaks Next.js builds on Vercel.

### Frontend/backend field name mismatch
The backend returns `access_token` not `token`. The `/me` endpoint returns the user object directly, not `{user: {...}}`. Verify the exact response shape before wiring the frontend.

### Port conflicts on local dev
Before starting, check and free ports:
```bash
lsof -ti :3000 | xargs kill -9   # frontend
lsof -ti :8000 | xargs kill -9   # backend
```

### Runtime data in version control
JSON file storage (`users.json`, `curricula.json`) is runtime data — add `backend/data/` to `.gitignore`.

### Monorepo Vercel deploy
When deploying from a monorepo subdirectory (`frontend/`), run `vercel` from that directory. Vercel auto-detects Next.js and uses the correct build command.

### Mixing subscription and one-time products
If your SaaS has both subscription AND one-time payment products on the same Stripe account, use separate checkout session create calls with `mode: "subscription"` vs `mode: "payment"`. For one-time products where each purchase = one consumed unit (e.g., per-EPK pricing), use `payment_intent_data.metadata` instead of `subscription_data.metadata`, and check `status: "complete"` in webhooks instead of `status: "active"`. The `subscriptions` table CHECK constraint needs to allow both statuses (`'incomplete', 'active', 'past_due', 'canceled', 'complete'`).

### Lazy Stripe/Supabase initialization
In Next.js API routes, `new Stripe(key)` and `createClient(url, key)` at module level will execute during build even without env vars set, causing build failures. Wrap in lazy getters:
```typescript
let _stripe: Stripe | null = null;
function getStripe(): Stripe {
  if (!_stripe) _stripe = new Stripe(process.env.STRIPE_SECRET_KEY ?? "");
  return _stripe;
}
```

### `lucide-react` type errors in Next.js 16

If TypeScript complains `Could not find a declaration file for module 'lucide-react'`, add a declaration file instead of installing `@types/lucide-react` (which may not exist):

```ts
// types/lucide.d.ts
declare module "lucide-react";
```

### `new Stripe()` at module level crashes Next.js build
The Next.js build evaluates module-level code even for API routes. If `STRIPE_SECRET_KEY` isn't in the build environment, `new Stripe("")` throws. Always use lazy initialization:

```ts
// ❌ BAD — crashes build without env var
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY ?? "");

// ✅ GOOD — only created at request time
let _stripe: Stripe | null = null;
function getStripe(): Stripe {
  if (!_stripe) {
    _stripe = new Stripe(process.env.STRIPE_SECRET_KEY ?? "");
  }
  return _stripe;
}
// Usage: getStripe().checkout.sessions.create(...)
```

Same pattern applies to `createClient()` from `@supabase/supabase-js` in API routes — lazy-init with `any` type annotation to avoid TypeScript `never` type inference on the admin client.

### SWC binary corruption after low-disk-space npm installs
If `npm install` ran during low disk space, the `@next/swc-darwin-arm64` binary may be truncated. Symptom: `segment '__TEXT' load command content extends beyond end of file`. Fix:
```bash
rm -rf node_modules/@next/swc-darwin-arm64
npm rebuild @next/swc-darwin-arm64
```
If the native binary still fails, fall back to webpack: `next build --webpack`.

## Design System

Default dark theme for SaaS:
- Background: `hsl(240, 10%, 3.9%)` (near-black)
- Cards: `hsl(240, 10%, 5.9%)`
- Primary accent: `hsl(217, 91%, 60%)` (blue)
- Text: white/98% foreground
- Muted: `hsl(240, 5%, 64%)`
- Border: `hsl(240, 4%, 16%)`
- Radius: `0.75rem`
- Fonts: Inter (body), JetBrains Mono (code)

Lucide icons throughout — no heavy icon library needed.
