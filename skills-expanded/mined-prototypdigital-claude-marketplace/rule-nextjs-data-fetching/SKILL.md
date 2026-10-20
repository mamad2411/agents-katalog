---
name: nextjs-data-fetching
description: Prefer fetch with cache options in Server Components over useEffect + API calls
---

# Next.js Data Fetching

In App Router, data fetching belongs in Server Components using async/await with the extended `fetch` API. `useEffect` + client-side API calls add a waterfall (page load → render → fetch → render again) and send a round-trip that a Server Component can eliminate entirely.

## Rules

- **Fetch data in Server Components** by making the component `async` and using `await fetch(...)` or your ORM/DB client directly.
- **Use Next.js fetch cache options** to control revalidation:
  - `cache: 'force-cache'` — static, cached indefinitely (default for `fetch`)
  - `next: { revalidate: N }` — ISR, revalidate every N seconds
  - `cache: 'no-store'` — dynamic, never cached (equivalent to SSR on every request)
- **Prefer `generateStaticParams` + `force-cache`** for pages with a known set of params at build time.
- **Never reach for `useEffect` + `fetch`** for data that was available at render time — this creates a client-side waterfall and leaks API calls to the browser.
- **Avoid `getServerSideProps` / `getStaticProps`** — these are Pages Router patterns. In App Router, async Server Components replace them entirely.

## Examples

```tsx
// BAD — client-side waterfall
'use client'
export default function UserProfile({ userId }) {
  const [user, setUser] = useState(null)
  useEffect(() => {
    fetch(`/api/users/${userId}`).then(r => r.json()).then(setUser)
  }, [userId])
  if (!user) return <Spinner />
  return <h1>{user.name}</h1>
}

// GOOD — Server Component, zero client JS for this data
export default async function UserProfile({ params }) {
  const user = await db.user.findUnique({ where: { id: params.userId } })
  return <h1>{user.name}</h1>
}

// GOOD — fetch with revalidation
async function getPosts() {
  const res = await fetch('https://api.example.com/posts', {
    next: { revalidate: 60 }, // revalidate every 60 seconds
  })
  return res.json()
}
```
