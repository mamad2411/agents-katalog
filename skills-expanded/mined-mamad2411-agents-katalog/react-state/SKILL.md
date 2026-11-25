---
name: react-state
description: "Manejo de estado en React 19 + TypeScript. Cubre server state vs client state, Zustand v5 (recomendado para nuevos proyectos), Redux Toolkit (enterprise), TanStack Query v5 (data fetching + cache), Context API (temas/auth), y cuándo elegir cada herramienta. Actívala al diseñar la estrategia de state management, migrar de Redux a Zustand, o implementar data fetching."
disable-model-invocation: true
---

# React State Management

Guía de state management en React 2026. La decisión clave: **server state vs client state.**

---

## Server State vs Client State

| Tipo | Dónde vive | Librería | Ejemplos |
|------|-----------|----------|----------|
| **Server State** | Backend (DB/API) | **TanStack Query v5** | Lista de órdenes, datos de cliente, catálogo |
| **Client State** | Solo en el navegador | **Zustand v5** o Context | UI mode (dark/light), filtros abiertos, carrito |

**Regla**: Si el dato viene del backend → TanStack Query. Si el dato solo existe en el frontend → Zustand.

---

## TanStack Query v5 (Server State)

### Setup

```tsx
// providers.tsx
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useState } from 'react';

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 30_000,           // 30s antes de considerar stale
        gcTime: 5 * 60 * 1000,        // 5min garbage collection
        retry: 2,
        refetchOnWindowFocus: false,
      },
    },
  }));

  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
}
```

### Queries

```tsx
// hooks/use-orders.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

export function useOrders(customerId: string, page: number) {
  return useQuery({
    queryKey: ['orders', customerId, page],
    queryFn: async ({ signal }) => {
      const res = await fetch(`/api/orders?customerId=${customerId}&page=${page}`, { signal });
      if (!res.ok) throw new Error('Failed to fetch orders');
      return res.json() as Promise<PaginatedResponse<Order>>;
    },
    placeholderData: keepPreviousData, // Muestra data anterior mientras carga la nueva página
  });
}

// Componente
export function OrderList({ customerId }: { customerId: string }) {
  const [page, setPage] = useState(1);
  const { data, isLoading, isError, error } = useOrders(customerId, page);

  if (isLoading) return <Spinner />;
  if (isError) return <Error message={error.message} />;

  return (
    <>
      <ul>{data.data.map(order => <OrderCard key={order.id} order={order} />)}</ul>
      <Pagination
        page={page}
        totalPages={data.pagination.totalPages}
        onPageChange={setPage}
      />
    </>
  );
}
```

### Mutations

```tsx
export function useCreateOrder() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (input: CreateOrderInput) => {
      const res = await fetch('/api/orders', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(input),
      });
      if (!res.ok) throw new Error('Failed to create order');
      return res.json() as Promise<Order>;
    },
    onSuccess: (newOrder) => {
      // Invalidar queries para refrescar la lista
      queryClient.invalidateQueries({ queryKey: ['orders'] });
      // O agregar directamente al cache (optimista)
      // queryClient.setQueryData(['orders', customerId, 1], (old) => ...);
    },
    onError: (error) => {
      toast.error(`Error: ${error.message}`);
    },
  });
}

export function CreateOrderForm() {
  const { mutate, isPending, error } = useCreateOrder();

  return (
    <form onSubmit={(e) => {
      e.preventDefault();
      const formData = new FormData(e.currentTarget);
      mutate({
        customerId: formData.get('customerId') as string,
        amount: Number(formData.get('amount')),
      });
      e.currentTarget.reset();
    }}>
      {/* ... */}
      <button disabled={isPending}>{isPending ? 'Creating...' : 'Create'}</button>
      {error && <p>{error.message}</p>}
    </form>
  );
}
```

---

## Zustand v5 (Client State)

```bash
npm install zustand
```

```tsx
// stores/use-cart-store.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface CartItem { sku: string; quantity: number; price: number; }

interface CartStore {
  items: CartItem[];
  addItem: (item: CartItem) => void;
  removeItem: (sku: string) => void;
  clear: () => void;
  total: () => number;
}

export const useCartStore = create<CartStore>()(
  persist(                               // Persiste en localStorage
    (set, get) => ({
      items: [],
      addItem: (item) => set((state) => {
        const existing = state.items.find(i => i.sku === item.sku);
        if (existing) {
          return {
            items: state.items.map(i =>
              i.sku === item.sku
                ? { ...i, quantity: i.quantity + item.quantity }
                : i
            ),
          };
        }
        return { items: [...state.items, item] };
      }),
      removeItem: (sku) => set((state) => ({
        items: state.items.filter(i => i.sku !== sku),
      })),
      clear: () => set({ items: [] }),
      total: () => get().items.reduce((sum, i) => sum + i.price * i.quantity, 0),
    }),
    { name: 'cart-storage' },
  ),
);

// Uso en componente
export function CartButton() {
  const items = useCartStore(s => s.items);
  const total = useCartStore(s => s.total);

  return (
    <button>
      Cart ({items.length}) — ${total().toFixed(2)}
    </button>
  );
}
```

### Zustand con selectores precisos

```tsx
// ❌ Re-render en cada cambio del store
const store = useCartStore();

// ✅ Solo re-render si items cambia
const items = useCartStore(s => s.items);

// ✅ Solo re-render si items.length cambia (con shallow)
import { useShallow } from 'zustand/react/shallow';
const count = useCartStore(s => s.items.length);
const { addItem, removeItem } = useCartStore(useShallow(s => ({
  addItem: s.addItem,
  removeItem: s.removeItem,
})));
```

---

## Redux Toolkit (Enterprise)

```bash
npm install @reduxjs/toolkit react-redux
```

```tsx
// store/orders-slice.ts
import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';

export const fetchOrders = createAsyncThunk(
  'orders/fetch',
  async (customerId: string) => {
    const res = await fetch(`/api/orders?customerId=${customerId}`);
    return res.json();
  },
);

const ordersSlice = createSlice({
  name: 'orders',
  initialState: { items: [] as Order[], status: 'idle' as 'idle' | 'loading' | 'error' },
  reducers: {
    addOptimisticOrder: (state, action: PayloadAction<Order>) => {
      state.items.unshift(action.payload);
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchOrders.pending, (state) => { state.status = 'loading'; })
      .addCase(fetchOrders.fulfilled, (state, action) => {
        state.items = action.payload;
        state.status = 'idle';
      })
      .addCase(fetchOrders.rejected, (state) => { state.status = 'error'; });
  },
});
```

**Regla 2026**: Usar Redux Toolkit solo si ya existe en el proyecto o es un app enterprise con mucha lógica de estado compleja. Para proyectos nuevos → Zustand + TanStack Query.

---

## Context API (temas, auth, i18n)

```tsx
// providers/theme-provider.tsx
import { createContext, useContext, useState, type ReactNode } from 'react';

type Theme = 'light' | 'dark';

const ThemeContext = createContext<{
  theme: Theme;
  toggleTheme: () => void;
} | null>(null);

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<Theme>('light');

  return (
    <ThemeContext value={{
      theme,
      toggleTheme: () => setTheme(t => t === 'light' ? 'dark' : 'light'),
    }}>
      <div className={theme}>{children}</div>
    </ThemeContext>
  );
}

export function useTheme() {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error('useTheme must be used within ThemeProvider');
  return ctx;
}
```

Context para datos que cambian muy poco (tema, locale, usuario autenticado). No para datos que cambian frecuentemente (cada re-render del provider re-renderea todos los consumers).

---

## Tabla de decisión

| Escenario | Herramienta | Razón |
|-----------|-------------|-------|
| Datos del servidor (fetch) | TanStack Query v5 | Caching, refetch, optimistic updates, pagination built-in |
| Estado UI (modal, sidebar) | `useState` | Suficiente para estado local |
| Estado global cliente (carrito, filtros) | Zustand v5 | Simple, ~2KB, hook-based |
| Proyecto enterprise existente | Redux Toolkit | No migrar si ya funciona; RTK Query cubre server state |
| Tema, auth, locale | Context API | Pocos updates, muchos consumers |
