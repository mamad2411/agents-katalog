---
name: "remix"
description: "Remix full-stack React: file-based routing, loaders, actions, progressive enhancement, session management, resource routes, error boundaries, and production deployment patterns"
---

# Remix Skill

## When to activate
- Building or extending a Remix application (`app/routes/`, `app/root.tsx`)
- Implementing data fetching with loaders or mutations with actions
- Setting up session-based auth, cookie management, or form handling in Remix
- Wiring up resource routes for APIs or webhooks in a Remix project
- Any task referencing `useLoaderData`, `useActionData`, `Form`, `redirect`, or `@remix-run/*`

## When NOT to use
- The user wants a pure React SPA without server-side rendering — use the react skill
- The user is on Next.js — use the nextjs skill
- Server-only API (no UI) — use the express or fastify skill

## Instructions

### Project setup and structure

```
Set up a production-ready Remix 2.x project with TypeScript and Vite.

Runtime: [Node.js / Cloudflare Pages / Fly.io]
Auth: [session cookie / none]
Database: [Prisma + PostgreSQL / Drizzle / none]
Styling: [Tailwind / plain CSS]

Directory structure:
app/
  root.tsx              ← root layout, global error boundary, meta
  entry.client.tsx      ← browser hydration (rarely edited)
  entry.server.tsx      ← server rendering (rarely edited)
  routes/
    _index.tsx          ← renders at /
    dashboard.tsx       ← renders at /dashboard (layout route)
    dashboard._index.tsx← renders at /dashboard (index child)
    users.$id.tsx       ← renders at /users/:id
    api.webhook.tsx     ← resource route at /api/webhook (no UI export)
  lib/
    session.server.ts   ← cookie session factory (server-only)
    db.server.ts        ← Prisma/Drizzle client singleton
    auth.server.ts      ← login/logout helpers
  components/
    ui/                 ← shared presentational components
  styles/
    tailwind.css

// vite.config.ts
import { vitePlugin as remix } from '@remix-run/dev'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [
    remix({
      future: {
        v3_fetcherPersist: true,
        v3_relativeSplatPath: true,
        v3_throwAbortReason: true,
      },
    }),
  ],
})
```

### Loaders — server data fetching

```
Implement a loader for [route] that fetches [data] and handles auth/errors.

Loaders run server-side on every GET request (navigation + data refresh).
They never run in the browser. Return anything serializable.

// app/routes/users.$id.tsx
import { json, LoaderFunctionArgs } from '@remix-run/node'
import { useLoaderData } from '@remix-run/react'
import { requireUser } from '~/lib/auth.server'
import { db } from '~/lib/db.server'

export async function loader({ request, params }: LoaderFunctionArgs) {
  // Auth gate — throws redirect to /login if no session
  const currentUser = await requireUser(request)

  const user = await db.user.findUnique({ where: { id: params.id } })

  // Throw Response to trigger the nearest ErrorBoundary
  if (!user) throw new Response('User not found', { status: 404 })

  // Authorization check
  if (currentUser.role !== 'admin' && currentUser.id !== user.id) {
    throw new Response('Forbidden', { status: 403 })
  }

  // Serialize — dates become strings, never pass class instances
  return json({
    user: {
      id: user.id,
      name: user.name,
      email: user.email,
      createdAt: user.createdAt.toISOString(),
    },
    isOwner: currentUser.id === user.id,
  })
}

export default function UserProfile() {
  // Fully typed — TypeScript infers from loader return
  const { user, isOwner } = useLoaderData<typeof loader>()

  return (
    <article>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
      {isOwner && <a href="/settings">Edit profile</a>}
    </article>
  )
}
```

### Actions — mutations and form handling

```
Implement an action for [route] that handles [create / update / delete] with validation.

Actions run server-side on POST/PUT/PATCH/DELETE. They are the only way
to mutate data in Remix. Return json() with errors or redirect() on success.

// app/routes/users.new.tsx
import { json, redirect, ActionFunctionArgs } from '@remix-run/node'
import { Form, useActionData, useNavigation } from '@remix-run/react'
import { requireUser } from '~/lib/auth.server'
import { db } from '~/lib/db.server'
import { z } from 'zod'

const CreateUserSchema = z.object({
  name: z.string().min(1, 'Name is required').max(100),
  email: z.string().email('Invalid email'),
  role: z.enum(['admin', 'user']),
})

export async function action({ request }: ActionFunctionArgs) {
  await requireUser(request)

  const formData = await request.formData()
  const raw = Object.fromEntries(formData)

  const result = CreateUserSchema.safeParse(raw)
  if (!result.success) {
    // Return errors — useActionData picks these up without a page reload
    return json(
      { errors: result.error.flatten().fieldErrors, values: raw },
      { status: 422 }
    )
  }

  const { name, email, role } = result.data

  try {
    const user = await db.user.create({ data: { name, email, role } })
    // Redirect to the new resource — triggers a GET to clear the form
    return redirect(`/users/${user.id}`)
  } catch (err: any) {
    if (err.code === 'P2002') {  // Prisma unique constraint
      return json({ errors: { email: ['Email already registered'] }, values: raw }, { status: 409 })
    }
    throw err  // unhandled — triggers ErrorBoundary
  }
}

export default function NewUser() {
  const data = useActionData<typeof action>()
  const nav = useNavigation()
  const isSubmitting = nav.state === 'submitting'

  return (
    // Remix Form submits to the same route's action by default
    <Form method="post">
      <div>
        <label htmlFor="name">Name</label>
        <input id="name" name="name" defaultValue={data?.values?.name as string} />
        {data?.errors?.name && <p className="error">{data.errors.name[0]}</p>}
      </div>

      <div>
        <label htmlFor="email">Email</label>
        <input id="email" name="email" type="email" defaultValue={data?.values?.email as string} />
        {data?.errors?.email && <p className="error">{data.errors.email[0]}</p>}
      </div>

      <select name="role" defaultValue="user">
        <option value="user">User</option>
        <option value="admin">Admin</option>
      </select>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Creating...' : 'Create user'}
      </button>
    </Form>
  )
}
```

### Session management and authentication

```
Implement cookie-based session auth in Remix.

// app/lib/session.server.ts
import { createCookieSessionStorage, redirect } from '@remix-run/node'

type SessionData = { userId: string; role: string }
type SessionFlashData = { error: string }

const { getSession, commitSession, destroySession } =
  createCookieSessionStorage<SessionData, SessionFlashData>({
    cookie: {
      name: '__session',
      httpOnly: true,
      maxAge: 60 * 60 * 24 * 30,  // 30 days
      path: '/',
      sameSite: 'lax',
      secrets: [process.env.SESSION_SECRET!],
      secure: process.env.NODE_ENV === 'production',
    },
  })

export { getSession, commitSession, destroySession }

// app/lib/auth.server.ts
import { getSession, commitSession, destroySession } from './session.server'
import { db } from './db.server'
import bcrypt from 'bcryptjs'

export async function requireUser(request: Request) {
  const session = await getSession(request.headers.get('Cookie'))
  const userId = session.get('userId')
  if (!userId) throw redirect('/login')

  const user = await db.user.findUnique({ where: { id: userId } })
  if (!user) throw redirect('/login')

  return user
}

export async function login(email: string, password: string) {
  const user = await db.user.findUnique({ where: { email } })
  if (!user || !(await bcrypt.compare(password, user.passwordHash))) {
    return null
  }
  return user
}

// app/routes/login.tsx — login action
export async function action({ request }: ActionFunctionArgs) {
  const formData = await request.formData()
  const email = formData.get('email') as string
  const password = formData.get('password') as string

  const user = await login(email, password)
  if (!user) {
    return json({ error: 'Invalid credentials' }, { status: 401 })
  }

  const session = await getSession(request.headers.get('Cookie'))
  session.set('userId', user.id)
  session.set('role', user.role)

  return redirect('/dashboard', {
    headers: { 'Set-Cookie': await commitSession(session) },
  })
}

// app/routes/logout.tsx — logout action (no UI needed)
export async function action({ request }: ActionFunctionArgs) {
  const session = await getSession(request.headers.get('Cookie'))
  return redirect('/login', {
    headers: { 'Set-Cookie': await destroySession(session) },
  })
}
```

### Resource routes

```
Create a resource route for [webhook / API endpoint / file download].

Resource routes have no default export (no UI). They respond with arbitrary
Response objects — JSON, binary, redirects, or webhooks.

// app/routes/api.users.ts — REST endpoint at /api/users
import { json, LoaderFunctionArgs, ActionFunctionArgs } from '@remix-run/node'

export async function loader({ request }: LoaderFunctionArgs) {
  // Can be called from fetch() in browser or external services
  const users = await db.user.findMany({ select: { id: true, name: true, email: true } })
  return json(users)
}

export async function action({ request }: ActionFunctionArgs) {
  if (request.method !== 'POST') {
    return new Response('Method Not Allowed', { status: 405 })
  }
  const body = await request.json()
  // ... handle POST
  return json({ created: true }, { status: 201 })
}

// app/routes/api.webhook.stripe.ts — webhook at /api/webhook/stripe
import Stripe from 'stripe'

export async function action({ request }: ActionFunctionArgs) {
  const sig = request.headers.get('stripe-signature')!
  const body = await request.text()  // raw text for signature verification

  let event: Stripe.Event
  try {
    event = stripe.webhooks.constructEvent(body, sig, process.env.STRIPE_WEBHOOK_SECRET!)
  } catch {
    return new Response('Webhook signature invalid', { status: 400 })
  }

  switch (event.type) {
    case 'checkout.session.completed':
      await handleCheckoutComplete(event.data.object)
      break
  }

  return new Response('ok', { status: 200 })
}

// app/routes/files.$key.ts — file download at /files/:key
export async function loader({ params }: LoaderFunctionArgs) {
  const file = await storage.get(params.key)
  if (!file) return new Response('Not found', { status: 404 })

  return new Response(file.stream(), {
    headers: {
      'Content-Type': file.contentType,
      'Content-Disposition': `attachment; filename="${file.name}"`,
    },
  })
}
```

### Error boundaries

```
Add error boundaries at the route level for [route].

// Route-level error boundary — catches loader/action errors for this route only
// Parent layout stays mounted (no full-page crash)
export function ErrorBoundary() {
  const error = useRouteError()

  if (isRouteErrorResponse(error)) {
    // Thrown Response — structured HTTP error from loader/action
    return (
      <div className="error-container">
        <h1>{error.status} {error.statusText}</h1>
        <p>{error.data}</p>
        <a href="/">Go home</a>
      </div>
    )
  }

  // Unhandled JS error — error is an Error instance
  const message = error instanceof Error ? error.message : 'Unknown error'
  return (
    <div className="error-container">
      <h1>Something went wrong</h1>
      <p>{message}</p>
    </div>
  )
}

// app/root.tsx — catches everything not caught by a route boundary
export function ErrorBoundary() {
  const error = useRouteError()
  return (
    <html lang="en">
      <head><title>Error</title></head>
      <body>
        <h1>Application error</h1>
        {isRouteErrorResponse(error) ? (
          <p>{error.status}: {error.data}</p>
        ) : (
          <p>An unexpected error occurred</p>
        )}
      </body>
    </html>
  )
}
```

### Nested routes and layouts

```
Set up nested routes with shared layout and outlet for [feature area].

// app/routes/dashboard.tsx — layout route (renders shell + Outlet)
import { Outlet, NavLink, useLoaderData } from '@remix-run/react'

export async function loader({ request }: LoaderFunctionArgs) {
  const user = await requireUser(request)
  return json({ user: { name: user.name, role: user.role } })
}

export default function DashboardLayout() {
  const { user } = useLoaderData<typeof loader>()
  return (
    <div className="dashboard">
      <nav>
        <span>{user.name}</span>
        <NavLink to="/dashboard">Overview</NavLink>
        <NavLink to="/dashboard/users">Users</NavLink>
        {user.role === 'admin' && <NavLink to="/dashboard/settings">Settings</NavLink>}
      </nav>
      <main>
        <Outlet />  {/* child routes render here */}
      </main>
    </div>
  )
}

// Route files that render inside this layout:
// app/routes/dashboard._index.tsx   → /dashboard
// app/routes/dashboard.users.tsx    → /dashboard/users
// app/routes/dashboard.settings.tsx → /dashboard/settings

// The layout loader (requireUser) runs on EVERY child route navigation —
// no prop drilling, each route fetches exactly what it needs.
```

## Example

**User:** Build a Remix CRUD app for a contacts list. Needs: list all contacts, create new contact, edit existing, delete. Auth is out of scope.

**Implementation — four route files:**

```typescript
// app/routes/contacts._index.tsx — list + delete
import { json, ActionFunctionArgs } from '@remix-run/node'
import { useLoaderData, Form, Link } from '@remix-run/react'
import { db } from '~/lib/db.server'

export async function loader() {
  const contacts = await db.contact.findMany({ orderBy: { name: 'asc' } })
  return json({ contacts })
}

export async function action({ request }: ActionFunctionArgs) {
  const formData = await request.formData()
  const intent = formData.get('intent')
  const id = formData.get('id') as string

  if (intent === 'delete') {
    await db.contact.delete({ where: { id } })
  }
  return json({ ok: true })
}

export default function ContactsList() {
  const { contacts } = useLoaderData<typeof loader>()
  return (
    <div>
      <h1>Contacts</h1>
      <Link to="new">Add contact</Link>
      <ul>
        {contacts.map((c) => (
          <li key={c.id}>
            <Link to={c.id}>{c.name}</Link> — {c.email}
            <Form method="post" style={{ display: 'inline' }}>
              <input type="hidden" name="id" value={c.id} />
              <button name="intent" value="delete" type="submit">Delete</button>
            </Form>
          </li>
        ))}
      </ul>
    </div>
  )
}

// app/routes/contacts.new.tsx — create
export async function action({ request }: ActionFunctionArgs) {
  const formData = await request.formData()
  const name = formData.get('name') as string
  const email = formData.get('email') as string

  if (!name || !email) return json({ error: 'Name and email required' }, { status: 422 })

  const contact = await db.contact.create({ data: { name, email } })
  return redirect(`/contacts/${contact.id}`)
}

export default function NewContact() {
  const data = useActionData<typeof action>()
  return (
    <Form method="post">
      {data?.error && <p>{data.error}</p>}
      <input name="name" placeholder="Name" required />
      <input name="email" type="email" placeholder="Email" required />
      <button type="submit">Save</button>
    </Form>
  )
}

// app/routes/contacts.$id.tsx — view + edit
export async function loader({ params }: LoaderFunctionArgs) {
  const contact = await db.contact.findUnique({ where: { id: params.id } })
  if (!contact) throw new Response('Not found', { status: 404 })
  return json({ contact })
}

export async function action({ request, params }: ActionFunctionArgs) {
  const formData = await request.formData()
  const name = formData.get('name') as string
  const email = formData.get('email') as string

  await db.contact.update({ where: { id: params.id }, data: { name, email } })
  return redirect(`/contacts/${params.id}`)
}

export default function ContactDetail() {
  const { contact } = useLoaderData<typeof loader>()
  const nav = useNavigation()

  return (
    <Form method="post">
      <input name="name" defaultValue={contact.name} required />
      <input name="email" type="email" defaultValue={contact.email} required />
      <button type="submit" disabled={nav.state === 'submitting'}>
        {nav.state === 'submitting' ? 'Saving...' : 'Save changes'}
      </button>
    </Form>
  )
}

export { ErrorBoundary } from '~/components/RouteErrorBoundary'
```

This works without JavaScript enabled (progressive enhancement). With JS, Remix intercepts the form submit, runs the action via `fetch`, and revalidates the loader data — no full page reload.
