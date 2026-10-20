---
name: state-management
description: |
  Client and server state management patterns for React apps. Apply when managing global state,
  server data, real-time updates, or complex UI state. Covers Zustand store design,
  TanStack Query caching strategy, optimistic updates, and when to use which tool.
---

# State Management

## Rule: What Goes Where
```
Local state (useState):    Form inputs, modal open/close, hover, toggle
Context:                   Theme, locale, current user (auth)
Zustand:                   Global UI state, user preferences, cart, notifications
TanStack Query:            All server data — fetching, caching, mutations, invalidation
```

## Zustand Store Design
```typescript
// stores/cartStore.ts
import { create } from 'zustand';
import { persist, devtools } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';

interface CartItem {
  productId: string;
  name: string;
  price: number;
  quantity: number;
}

interface CartStore {
  items: CartItem[];
  addItem: (item: CartItem) => void;
  removeItem: (productId: string) => void;
  updateQuantity: (productId: string, qty: number) => void;
  clear: () => void;
  total: () => number;
  itemCount: () => number;
}

export const useCartStore = create<CartStore>()(
  devtools(
    persist(
      immer((set, get) => ({
        items: [],

        addItem: (item) => set((state) => {
          const existing = state.items.find(i => i.productId === item.productId);
          if (existing) {
            existing.quantity += item.quantity;
          } else {
            state.items.push(item);
          }
        }),

        removeItem: (productId) => set((state) => {
          state.items = state.items.filter(i => i.productId !== productId);
        }),

        updateQuantity: (productId, qty) => set((state) => {
          const item = state.items.find(i => i.productId === productId);
          if (item) item.quantity = Math.max(0, qty);
          state.items = state.items.filter(i => i.quantity > 0);
        }),

        clear: () => set({ items: [] }),
        total: () => get().items.reduce((sum, i) => sum + i.price * i.quantity, 0),
        itemCount: () => get().items.reduce((sum, i) => sum + i.quantity, 0),
      })),
      { name: 'cart-storage' }
    )
  )
);

// Slice selectors to prevent unnecessary re-renders
export const useCartTotal = () => useCartStore((s) => s.total());
export const useCartCount = () => useCartStore((s) => s.itemCount());
```

## TanStack Query Patterns
```typescript
// lib/queryKeys.ts — centralized key factory
export const queryKeys = {
  products: {
    all: ['products'] as const,
    lists: () => [...queryKeys.products.all, 'list'] as const,
    list: (filters: ProductFilters) => [...queryKeys.products.lists(), filters] as const,
    detail: (id: string) => [...queryKeys.products.all, 'detail', id] as const,
  },
  orders: {
    all: ['orders'] as const,
    mine: () => [...queryKeys.orders.all, 'mine'] as const,
    detail: (id: string) => [...queryKeys.orders.all, 'detail', id] as const,
  },
};

// hooks/useProducts.ts
export function useProducts(filters: ProductFilters) {
  return useQuery({
    queryKey: queryKeys.products.list(filters),
    queryFn: () => api.products.list(filters),
    staleTime: 5 * 60 * 1000,    // 5 min — products don't change that often
    gcTime: 30 * 60 * 1000,      // 30 min cache
    placeholderData: keepPreviousData,  // No loading flash on filter change
  });
}

// Optimistic update for mutations
export function useUpdateProduct() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: api.products.update,

    onMutate: async (updated) => {
      // Cancel in-flight queries
      await queryClient.cancelQueries({ queryKey: queryKeys.products.detail(updated.id) });
      // Snapshot previous value
      const previous = queryClient.getQueryData(queryKeys.products.detail(updated.id));
      // Optimistically update
      queryClient.setQueryData(queryKeys.products.detail(updated.id), updated);
      return { previous };
    },

    onError: (err, updated, context) => {
      // Rollback on error
      queryClient.setQueryData(queryKeys.products.detail(updated.id), context?.previous);
      toast.error('Update failed — changes reverted');
    },

    onSettled: (_, __, updated) => {
      // Always refetch to sync with server
      queryClient.invalidateQueries({ queryKey: queryKeys.products.detail(updated.id) });
      queryClient.invalidateQueries({ queryKey: queryKeys.products.lists() });
    },
  });
}
```
