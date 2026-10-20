---
name: next-fast
description: Next.js App Router patterns and traps for rapid builds. Use when building with Next.js, React server components, route handlers, server actions, or debugging Next.js caching, env vars, or hydration issues.
---

# Next.js App Router Under Time Pressure

## Component discipline

- Server Components are the default. Add `"use client"` only at interaction leaves (forms,
  buttons, anything with hooks). A page that's 90% server-rendered with small client
  islands is both faster to build and reads as senior.
- Never import server-only code (db clients, secrets) into a client component — this is the late-session build
  error, 80% of the time.

## Data

- Read: fetch directly in async server components. No useEffect-fetch waterfalls.
- Write: server actions (`"use server"`) for form mutations, route handlers
  (`app/api/x/route.ts` exporting GET/POST) when an external client or clean REST shape is
  wanted. Call `revalidatePath("/")` after mutations or the UI will look broken when it isn't.

## The caching pressure valve

App Router caching surprises eat build time. Don't fight it: put
`export const dynamic = "force-dynamic"` on any page showing DB data that must be fresh.
Note it plainly: "trading cache optimization for correctness under the clock — I'd tune
revalidation properly given more time."

## Env vars

- Client-visible vars need the `NEXT_PUBLIC_` prefix; everything else is server-only.
- Vercel env additions require a redeploy to take effect. Add → deploy → verify, always.

## Fast traps list

- Hydration mismatch → almost always `Date`/`toLocaleString`/random values rendered on the
  server. Move to client component or render deterministic output.
- `params`/`searchParams` are async in current Next — `await` them in server components.
- Images: plain `<img>` is fine for a rapid build; skip next/image remote-domain config
  unless images are the assignment.
