---
name: tanstack-router-patterns
description: "When to activate: TanStack Router, React Router v6, file-based routing, route loaders, search params, type-safe navigation"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: typescript
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# React Router & TanStack Router Patterns

## React Router v6

### Setup
```tsx
import { createBrowserRouter, RouterProvider, Outlet } from 'react-router-dom'

const router = createBrowserRouter([
  {
    path: '/',
    element: <RootLayout />,
    errorElement: <ErrorPage />,
    children: [
      { index: true, element: <Home /> },
      {
        path: 'users',
        children: [
          { index: true, element: <UserList />, loader: usersLoader },
          { path: ':id', element: <UserDetail />, loader: userLoader },
          { path: 'new', element: <CreateUser />, action: createUserAction },
        ],
      },
    ],
  },
])

function App() { return <RouterProvider router={router} /> }
```

### Loaders & Actions
```tsx
// Loader — runs before render
export async function userLoader({ params }: LoaderFunctionArgs) {
  const user = await api.users.getById(params.id!)
  if (!user) throw new Response('Not Found', { status: 404 })
  return json(user)
}

// Usage in component
function UserDetail() {
  const user = useLoaderData() as User
  return <div>{user.name}</div>
}

// Action — handles form submission
export async function createUserAction({ request }: ActionFunctionArgs) {
  const formData = await request.formData()
  const name  = String(formData.get('name'))
  const email = String(formData.get('email'))
  const user  = await api.users.create({ name, email })
  return redirect(`/users/${user.id}`)
}
```

### Navigation
```tsx
import { useNavigate, Link, NavLink, useParams, useSearchParams } from 'react-router-dom'

// Imperative navigation
const navigate = useNavigate()
navigate('/users/123', { replace: true, state: { from: 'dashboard' } })
navigate(-1)  // back

// Declarative
<Link to="/users/123">View user</Link>
<NavLink to="/dashboard" className={({ isActive }) => isActive ? 'active' : ''}>
  Dashboard
</NavLink>

// Params & search
const { id } = useParams<{ id: string }>()
const [searchParams, setSearchParams] = useSearchParams()
const page = Number(searchParams.get('page') ?? '1')
```

### Lazy Routes
```tsx
const router = createBrowserRouter([
  {
    path: '/dashboard',
    lazy: async () => {
      const { Dashboard } = await import('./pages/Dashboard')
      return { Component: Dashboard }
    },
  },
])
```

## TanStack Router (fully type-safe)

### Setup
```tsx
import { createRouter, createRoute, createRootRoute } from '@tanstack/react-router'

const rootRoute = createRootRoute({ component: RootLayout })

const indexRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/',
  component: Home,
})

const usersRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/users',
})

const userDetailRoute = createRoute({
  getParentRoute: () => usersRoute,
  path: '$userId',
  loader: ({ params }) => fetchUser(params.userId),
  component: UserDetail,
})

const router = createRouter({
  routeTree: rootRoute.addChildren([
    indexRoute,
    usersRoute.addChildren([userDetailRoute]),
  ]),
})

// Type registration
declare module '@tanstack/react-router' {
  interface Register { router: typeof router }
}
```

### Type-Safe Search Params
```tsx
import { z } from 'zod'
import { zodValidator } from '@tanstack/zod-adapter'

const usersSearchSchema = z.object({
  page:  z.number().default(1),
  limit: z.number().default(20),
  q:     z.string().optional(),
})

const usersRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/users',
  validateSearch: zodValidator(usersSearchSchema),
  component: UserList,
})

// In component — fully typed
function UserList() {
  const { page, limit, q } = usersRoute.useSearch()
  const navigate = useNavigate()

  const setPage = (p: number) =>
    navigate({ to: '/users', search: prev => ({ ...prev, page: p }) })
}
```

### Navigation (type-safe)
```tsx
import { Link, useNavigate } from '@tanstack/react-router'

// All paths and params are type-checked
<Link to="/users/$userId" params={{ userId: user.id }}>
  {user.name}
</Link>

const navigate = useNavigate()
navigate({ to: '/users/$userId', params: { userId: '123' } })
```
