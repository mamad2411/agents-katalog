---
name: clerk-nextjs
description: Integrate Clerk into Next.js App Router with clerkMiddleware, ClerkProvider, prebuilt components, and server-side auth(). Use when the user adds or debugs Clerk in a Next.js app.
---

# Clerk + Next.js (App Router)

Current SDK: `@clerk/nextjs` (v7 line). Verify exact API shapes against
https://clerk.com/docs when precision matters; the hosted Clerk MCP server this
plugin connects also serves current snippets.

## Install and keys

```bash
npm install @clerk/nextjs
```

```bash
# .env.local
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...
```

Publishable key is public by design; the secret key is server-only, never in
client bundles or the repo (see `clerk-setup`).

## Middleware (required)

Next.js 16+: create `proxy.ts` at the root (or `/src`). Next.js 15 and
earlier: identical code in `middleware.ts`.

```ts
import { clerkMiddleware } from "@clerk/nextjs/server";

export default clerkMiddleware();

export const config = {
  matcher: [
    "/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)",
    "/(api|trpc)(.*)",
  ],
};
```

`clerkMiddleware()` protects nothing by default; it makes auth state available.
Protect at the resource (below), not only at the edge.

## Provider and components

```tsx
// app/layout.tsx
import { ClerkProvider, SignedIn, SignedOut, SignInButton, SignUpButton, UserButton } from "@clerk/nextjs";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <ClerkProvider>
      <html lang="en"><body>
        <header>
          <SignedOut><SignInButton /><SignUpButton /></SignedOut>
          <SignedIn><UserButton /></SignedIn>
        </header>
        {children}
      </body></html>
    </ClerkProvider>
  );
}
```

Prebuilt pages: `<SignIn />` at `app/sign-in/[[...sign-in]]/page.tsx` and
`<SignUp />` similarly; set `NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in`.

## Server-side auth (protect close to the data)

```ts
import { auth, currentUser } from "@clerk/nextjs/server";

// Server Component / Route Handler / Server Action
export default async function Page() {
  const { userId, has } = await auth();          // auth() is async
  if (!userId) return null;                      // or redirect("/sign-in")
  const user = await currentUser();              // full Backend User object
  ...
}
```

- `await auth.protect()` in a page/route throws to sign-in when signed out;
  pass `{ role: "org:admin" }` or `{ permission: "org:invoices:create" }` for
  authorization checks.
- Route groups in middleware when you do want edge gating:

```ts
import { clerkMiddleware, createRouteMatcher } from "@clerk/nextjs/server";
const isProtected = createRouteMatcher(["/dashboard(.*)", "/api/private(.*)"]);
export default clerkMiddleware(async (auth, req) => {
  if (isProtected(req)) await auth.protect();
});
```

- Client components: `useAuth()`, `useUser()` hooks.

## Security checklist

- Every mutation (Server Action, POST handler) re-checks `await auth()`
  itself; do not trust that middleware ran.
- Use `has({ permission })` for authorization; `userId` alone only proves
  authentication.
- Do not read role/permission claims client-side for enforcement; client
  state is presentation only.
- Data fetches keyed by `userId` from `auth()`, never by an id posted from
  the browser.
