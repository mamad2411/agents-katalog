---
name: "sveltekit"
description: "SvelteKit full-stack framework: file-based routing, server and universal load functions, form actions with progressive enhancement, hooks, route groups, adapters, and REST endpoints via +server.ts"
---

# SvelteKit Skill

## When to activate
- Building a full-stack SvelteKit application (not just Svelte components)
- Setting up file-based routing with `+page.svelte`, `+page.server.ts`, `+layout.svelte`
- Writing server load functions or universal load functions
- Implementing form actions (default or named) with `use:enhance`
- Writing `hooks.server.ts` (`handle`, `handleFetch`, `handleError`)
- Creating REST endpoints via `+server.ts`
- Protecting routes with route groups like `(auth)`
- Choosing and configuring an adapter (Vercel, Cloudflare, Node)
- Using `$app/stores` (`page`, `navigating`, `updated`)

## When NOT to use
- Pure Svelte component questions with no SvelteKit routing or server context — use the `svelte` skill
- React or Next.js projects — use the `nextjs` skill
- Static sites with no server-side data needs — use Astro
- Projects where the team is committed to React and switching is not an option

## Instructions

### Project setup

```bash
npm create svelte@latest my-app
# Choose: SvelteKit app (not library)
# TypeScript: Yes
# ESLint + Prettier: Yes
cd my-app && npm install && npm run dev
```

### File-based routing structure

```
src/
├── routes/
│   ├── +layout.svelte          # root layout — wraps all pages
│   ├── +layout.server.ts       # root server load — runs on every request
│   ├── +page.svelte            # / (home)
│   ├── +page.server.ts         # server load + actions for /
│   ├── (auth)/                 # route group — no URL segment added
│   │   ├── +layout.server.ts   # guard: redirect if not logged in
│   │   ├── dashboard/
│   │   │   └── +page.svelte
│   │   └── settings/
│   │       └── +page.svelte
│   ├── blog/
│   │   ├── +page.svelte        # /blog
│   │   └── [slug]/
│   │       ├── +page.svelte    # /blog/[slug]
│   │       └── +page.server.ts
│   └── api/
│       └── users/
│           └── +server.ts      # REST endpoint — not a page
├── lib/
│   ├── components/
│   ├── server/                 # server-only imports (never sent to client)
│   │   ├── db.ts
│   │   └── auth.ts
│   └── utils.ts
└── hooks.server.ts             # global server middleware
```

### Load functions: server vs universal

```typescript
// +page.server.ts — SERVER LOAD
// Runs only on the server. Can access DB, secrets, cookies.
// Return value is serialized and sent to the page.
import type { PageServerLoad } from './$types'
import { error } from '@sveltejs/kit'

export const load: PageServerLoad = async ({ params, locals, cookies }) => {
  if (!locals.user) error(401, 'Not authenticated')

  const post = await db.post.findUnique({ where: { slug: params.slug } })
  if (!post) error(404, 'Post not found')

  return { post }   // only serializable data — no class instances, no functions
}
```

```typescript
// +page.ts — UNIVERSAL LOAD
// Runs on server (initial request) AND client (navigation).
// Cannot access DB or secrets directly — must call an API.
import type { PageLoad } from './$types'

export const load: PageLoad = async ({ fetch, params }) => {
  const res = await fetch(`/api/posts/${params.slug}`)
  if (!res.ok) throw new Error('Post not found')
  return { post: await res.json() }
}
```

Rule: use `+page.server.ts` when you need DB or auth. Use `+page.ts` only when you have a public API and need client-side re-fetching on navigation.

```svelte
<!-- +page.svelte — consuming load data -->
<script lang="ts">
  import type { PageData } from './$types'
  let { data }: { data: PageData } = $props()
</script>

<h1>{data.post.title}</h1>
<p>{data.post.body}</p>
```

### Form actions

```typescript
// src/routes/posts/new/+page.server.ts
import type { Actions, PageServerLoad } from './$types'
import { fail, redirect } from '@sveltejs/kit'
import { z } from 'zod'

const PostSchema = z.object({
  title: z.string().min(1).max(200),
  body: z.string().min(10),
})

export const load: PageServerLoad = async ({ locals }) => {
  if (!locals.user) redirect(303, '/login')
  return {}
}

export const actions: Actions = {
  // Default action — called when the form has no `action` attribute
  default: async ({ request, locals }) => {
    if (!locals.user) return fail(401, { message: 'Not authenticated' })

    const data = Object.fromEntries(await request.formData())
    const parsed = PostSchema.safeParse(data)

    if (!parsed.success) {
      return fail(422, {
        errors: parsed.error.flatten().fieldErrors,
        values: data,      // return values so the form can repopulate
      })
    }

    const post = await db.post.create({
      data: { ...parsed.data, authorId: locals.user.id },
    })

    redirect(303, `/blog/${post.slug}`)
  },

  // Named action — <form action="?/draft">
  draft: async ({ request, locals }) => {
    const data = Object.fromEntries(await request.formData())
    await db.post.create({ data: { ...data, published: false, authorId: locals.user.id } })
    return { saved: true }
  },
}
```

```svelte
<!-- src/routes/posts/new/+page.svelte -->
<script lang="ts">
  import { enhance } from '$app/forms'
  let { form } = $props()
</script>

<!-- use:enhance — progressive enhancement: works without JS, upgrades with it -->
<form method="POST" use:enhance>
  <label>
    Title
    <input name="title" value={form?.values?.title ?? ''} />
    {#if form?.errors?.title}
      <span class="error">{form.errors.title[0]}</span>
    {/if}
  </label>

  <label>
    Body
    <textarea name="body">{form?.values?.body ?? ''}</textarea>
    {#if form?.errors?.body}
      <span class="error">{form.errors.body[0]}</span>
    {/if}
  </label>

  <button type="submit">Publish</button>
  <button type="submit" formaction="?/draft">Save draft</button>
</form>
```

`use:enhance` intercepts the form submit, handles the response via JavaScript, and updates the `form` prop — no full page reload. Falls back to native form submission if JS is unavailable.

### Hooks: hooks.server.ts

```typescript
// src/hooks.server.ts
import type { Handle, HandleFetch, HandleServerError } from '@sveltejs/kit'
import { sequence } from '@sveltejs/kit/hooks'

// handle — runs on every server request (like middleware)
const authHandle: Handle = async ({ event, resolve }) => {
  const token = event.cookies.get('session')

  if (token) {
    const user = await validateSession(token)
    event.locals.user = user ?? null
  } else {
    event.locals.user = null
  }

  return resolve(event)
}

const corsHandle: Handle = async ({ event, resolve }) => {
  const response = await resolve(event)
  // Add headers to all responses
  response.headers.set('X-Frame-Options', 'SAMEORIGIN')
  return response
}

// sequence() chains multiple handle functions
export const handle = sequence(authHandle, corsHandle)

// handleFetch — intercepts server-side fetch calls (e.g. in load functions)
export const handleFetch: HandleFetch = async ({ request, fetch }) => {
  // Attach auth to outgoing server-side fetch calls
  request.headers.set('Authorization', `Bearer ${process.env.INTERNAL_API_KEY}`)
  return fetch(request)
}

// handleError — called when an unexpected error reaches the server
export const handleServerError: HandleServerError = async ({ error, event }) => {
  console.error('Unhandled error:', error, event.url.pathname)
  return { message: 'An unexpected error occurred' }
}
```

Declare the `locals` type in `src/app.d.ts`:

```typescript
// src/app.d.ts
declare global {
  namespace App {
    interface Locals {
      user: { id: string; email: string; role: string } | null
    }
    interface Error {
      message: string
    }
  }
}
export {}
```

### Route groups: (auth) protected routes

```typescript
// src/routes/(auth)/+layout.server.ts
// Every route inside (auth)/ inherits this guard
import type { LayoutServerLoad } from './$types'
import { redirect } from '@sveltejs/kit'

export const load: LayoutServerLoad = async ({ locals }) => {
  if (!locals.user) redirect(303, '/login')
  return { user: locals.user }
}
```

The `(auth)` folder name does not appear in the URL. `/dashboard`, `/settings`, and `/profile` are all protected without any per-page boilerplate.

### REST endpoints: +server.ts

```typescript
// src/routes/api/users/+server.ts
import type { RequestHandler } from './$types'
import { json, error } from '@sveltejs/kit'

export const GET: RequestHandler = async ({ url, locals }) => {
  if (!locals.user) error(401, 'Unauthorized')

  const page = Number(url.searchParams.get('page') ?? 1)
  const users = await db.user.findMany({ skip: (page - 1) * 20, take: 20 })
  return json({ users, page })
}

export const POST: RequestHandler = async ({ request, locals }) => {
  if (locals.user?.role !== 'admin') error(403, 'Forbidden')

  const body = await request.json()
  const user = await db.user.create({ data: body })
  return json(user, { status: 201 })
}
```

### SvelteKit stores ($app/stores)

```svelte
<script lang="ts">
  import { page, navigating, updated } from '$app/stores'

  // page — current URL, route, params, data, status, form
  $: currentPath = $page.url.pathname
  $: user = $page.data.user          // data from root layout load
  $: routeId = $page.route.id        // e.g. '/blog/[slug]'

  // navigating — not null while a navigation is in progress
  $: isLoading = $navigating !== null

  // updated — true when a new app version is deployed
  // Poll: updated.check() — returns true if a new version exists
</script>

{#if $navigating}
  <div class="progress-bar" />
{/if}

<nav>
  <a href="/" class:active={currentPath === '/'}>Home</a>
  {#if $page.data.user}
    <a href="/dashboard">Dashboard</a>
  {:else}
    <a href="/login">Login</a>
  {/if}
</nav>
```

### Adapters

```bash
# Vercel (auto-detects SvelteKit projects)
npm install -D @sveltejs/adapter-vercel

# Cloudflare Pages
npm install -D @sveltejs/adapter-cloudflare

# Node.js (self-hosted, Docker)
npm install -D @sveltejs/adapter-node
```

```javascript
// svelte.config.js
import adapter from '@sveltejs/adapter-vercel'    // swap as needed
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte'

export default {
  preprocess: vitePreprocess(),
  kit: {
    adapter: adapter(),
    // Vercel: zero config
    // Cloudflare: adapter({ routes: { include: ['/*'], exclude: ['<all>'] } })
    // Node: adapter({ out: 'build' }) — then `node build`
  },
}
```

Cloudflare adapter gives access to Workers bindings:

```typescript
// src/hooks.server.ts (Cloudflare)
import type { Handle } from '@sveltejs/kit'

export const handle: Handle = async ({ event, resolve }) => {
  const { env } = event.platform ?? {}    // Cloudflare bindings
  event.locals.kv = env?.MY_KV
  event.locals.db = env?.MY_D1
  return resolve(event)
}
```

## Example

**User:** Build an authenticated blog CRUD app in SvelteKit. Users must log in to create or edit posts. The post list is public. Use form actions with validation, not a client-side fetch.

**Expected output:**

- `src/hooks.server.ts` — reads session cookie, sets `locals.user`
- `src/app.d.ts` — declares `App.Locals` with `user` type
- `src/routes/(auth)/+layout.server.ts` — redirects unauthenticated users to `/login`
- `src/routes/login/+page.server.ts` — default action: verify credentials, set cookie, redirect
- `src/routes/login/+page.svelte` — login form with `use:enhance`, shows errors from `form`
- `src/routes/blog/+page.server.ts` — server load returning all published posts (public)
- `src/routes/blog/+page.svelte` — renders post list, shows "New post" link if `$page.data.user`
- `src/routes/(auth)/blog/new/+page.server.ts` — load (auth guard inherited), `default` action with Zod validation + `fail()`, on success `redirect(303, '/blog')`
- `src/routes/(auth)/blog/new/+page.svelte` — form with `use:enhance`, repopulates values and shows field errors from `form`
- `src/routes/(auth)/blog/[id]/edit/+page.server.ts` — load fetches post and checks ownership, named actions `update` and `delete`
- `svelte.config.js` — adapter-vercel (or adapter-node for Docker)

---
