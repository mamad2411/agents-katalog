---
name: react-routing
description: "Routing en React con React Router v7 y TanStack Router. Cubre rutas declarativas, loaders/actions, type-safe search params, guards de autenticación, code splitting por ruta, layouts anidados, y cuándo usar cada router. Actívala al configurar navegación, proteger rutas, o migrar entre routers."
disable-model-invocation: true
---

# React Routing (2026)

Guía de routing en React. **React Router v7** para full-stack y ecosistema. **TanStack Router** para SPAs type-safe.

---

## Tabla de decisión

| Criterio | React Router v7 | TanStack Router |
|----------|-----------------|-----------------|
| **Full-stack (SSR)** | ✅ Nativo | ⚠️ Vía TanStack Start |
| **SPA (client-only)** | ✅ | ✅ |
| **Type safety** | Parcial (generics) | ✅ Total (search params, path params, loader data) |
| **Ecosistema** | ⭐⭐⭐⭐⭐ Enorme | ⭐⭐ Emergente |
| **Curva aprendizaje** | Baja | Media |

---

## React Router v7

### Configuración

```tsx
import { createBrowserRouter, RouterProvider } from 'react-router';

const router = createBrowserRouter([
  {
    path: '/',
    element: <RootLayout />,
    errorElement: <ErrorPage />,
    children: [
      { index: true, element: <DashboardPage /> },
      {
        path: 'orders',
        element: <OrdersLayout />,
        loader: ordersLoader,
        children: [
          { index: true, element: <OrderListPage /> },
          { path: ':id', element: <OrderDetailPage />, loader: orderLoader },
          { path: 'new', element: <CreateOrderPage /> },
        ],
      },
      { path: 'login', element: <LoginPage /> },
    ],
  },
]);

export function App() {
  return <RouterProvider router={router} />;
}
```

### Loaders y Actions

```tsx
// orders.loader.ts
export async function ordersLoader({ request }: LoaderFunctionArgs) {
  const url = new URL(request.url);
  const page = url.searchParams.get('page') ?? '1';
  const response = await fetch(`/api/orders?page=${page}`);
  return response.json() as Promise<PaginatedResponse<Order>>;
}

// Componente recibe datos del loader
export function OrderListPage() {
  const { data, pagination } = useLoaderData() as PaginatedResponse<Order>;
  const [searchParams, setSearchParams] = useSearchParams();

  return (
    <div>
      <ul>{data.map(order => <OrderCard key={order.id} order={order} />)}</ul>
      <button onClick={() => setSearchParams({ page: String(pagination.page + 1) })}>
        Next
      </button>
    </div>
  );
}
```

### Auth guard

```tsx
// Proteger rutas que requieren autenticación
export async function authLoader() {
  const user = await getCurrentUser();
  if (!user) throw redirect('/login');
  return user;
}

const router = createBrowserRouter([
  {
    path: '/',
    loader: authLoader,   // Todas las rutas hijas requieren auth
    element: <RootLayout />,
    children: [ /* ... */ ],
  },
  { path: '/login', element: <LoginPage /> },
]);
```

---

## TanStack Router (SPA type-safe)

```bash
npm install @tanstack/react-router
```

```tsx
// router.ts — TypeScript infiere tipos automáticamente
import { createFileRoute } from '@tanstack/react-router';

// File-based routing: src/routes/orders/$id.tsx
export const Route = createFileRoute('/orders/$id')({
  loader: async ({ params }) => {
    const order = await fetchOrder(params.id);
    return order; // Tipo inferido
  },
  component: OrderDetailPage,
});

function OrderDetailPage() {
  const order = Route.useLoaderData(); // Tipo Order, automático
  return <div>{order.customerId}</div>;
}

// Search params type-safe
export const Route = createFileRoute('/orders/')({
  validateSearch: (search: Record<string, unknown>) => ({
    page: z.coerce.number().default(1).parse(search.page ?? 1),
    status: z.enum(['pending', 'shipped']).optional().parse(search.status),
  }),
});
// En el componente:
const { page, status } = Route.useSearch(); // Tipado: { page: number; status?: string }
```

---

## Code splitting por ruta

```tsx
import { lazy, Suspense } from 'react';

// React Router v7 con lazy
const OrdersPage = lazy(() => import('./orders/page.js'));

const router = createBrowserRouter([
  {
    path: 'orders',
    lazy: async () => {
      const { OrdersLayout } = await import('./orders/layout.js');
      return { Component: OrdersLayout };
    },
    children: [
      {
        index: true,
        lazy: () => import('./orders/page.js'), // Se carga solo al visitar /orders
      },
    ],
  },
]);
```

---

## Layouts anidados

```tsx
// /app/layout.tsx — Root layout con sidebar
export function RootLayout() {
  return (
    <div className="flex h-screen">
      <Sidebar />
      <main className="flex-1 overflow-auto p-6">
        <Outlet /> {/* Renders child route */}
      </main>
    </div>
  );
}

// /app/orders/layout.tsx — Breadcrumb + tabs para orders
export function OrdersLayout() {
  const user = useLoaderData<User>();

  return (
    <div>
      <Breadcrumb items={[{ label: 'Home', href: '/' }, { label: 'Orders' }]} />
      <nav>
        <NavLink to="/orders">All</NavLink>
        <NavLink to="/orders?status=pending">Pending</NavLink>
      </nav>
      <Outlet />
    </div>
  );
}
```

---

## Navegación declarativa y programática

```tsx
// Declarativa
<Link to="/orders/123">Order #123</Link>
<NavLink to="/orders" className={({ isActive }) => isActive ? 'font-bold' : ''}>
  Orders
</NavLink>

// Programática
const navigate = useNavigate();
navigate('/orders/123');
navigate(-1); // Volver atrás

// Con search params
const [, setSearchParams] = useSearchParams();
setSearchParams({ page: '2', status: 'pending' });

// Redirect
import { redirect } from 'react-router';
export async function loader() {
  if (!authenticated) throw redirect('/login');
  return null;
}
```

---

## Checklist routing

- [ ] Router elegido según caso (React Router v7 full-stack, TanStack Router SPA type-safe)
- [ ] Layouts anidados con `<Outlet />` para UI compartida (sidebar, breadcrumbs)
- [ ] Loaders para data fetching (evitar useEffect + useState en rutas)
- [ ] Auth guard en loader del layout padre
- [ ] Code splitting por ruta con `lazy()`
- [ ] Search params tipados (TanStack Router) o validados con Zod (React Router)
- [ ] Error boundaries por ruta con `errorElement`
- [ ] `<Link>` y `<NavLink>` sobre `<a>` para SPA navigation
