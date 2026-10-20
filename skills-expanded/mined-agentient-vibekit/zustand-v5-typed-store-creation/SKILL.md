---
name: zustand-v5-typed-store-creation
version: "1.0"
description: >
  Zustand v5 store creation with curried function syntax and TypeScript typing patterns.
  PROACTIVELY activate for: (1) creating typed Zustand stores with v5 syntax, (2) integrating persist and devtools middleware, (3) using useShallow for performance.
  Triggers: "zustand", "create store", "global state"
group: state-forms
core-integration:
  techniques:
    primary: ["structured_decomposition"]
    secondary: []
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# Zustand v5 Typed Store Creation

## Critical v5 Breaking Changes

Zustand v5 introduced significant API changes from v4. You **MUST** use v5 syntax:

### v5 Curried Function Syntax (MANDATORY)

```typescript
import { create } from 'zustand';

interface BearStore {
  bears: number;
  increase: (by: number) => void;
}

// CORRECT: v5 curried syntax - TWO function calls
const useBearStore = create<BearStore>()(  // Type on FIRST call
  (set) => ({
    bears: 0,
    increase: (by) => set((state) => ({ bears: state.bears + by })),
  })
);

// WRONG: v4 syntax - WILL NOT WORK IN V5
const useBearStore = create<BearStore>(
  (set) => ({ ... })
);
```

**Key Difference**: Notice the **double parentheses** `create<Type>()( ... )`. The type parameter goes on the **first** function call.

### v5 useShallow Hook (MANDATORY)

```typescript
import { useShallow } from 'zustand/shallow';

// CORRECT: v5 useShallow hook
const { bears, fish } = useBearStore(
  useShallow((state) => ({ bears: state.bears, fish: state.fish }))
);

// WRONG: v4 shallow function - REMOVED IN V5
const { bears, fish } = useBearStore(
  (state) => ({ bears: state.bears, fish: state.fish }),
  shallow  // This parameter doesn't exist in v5!
);
```

## Basic Store Creation Pattern

```typescript
import { create } from 'zustand';

// 1. Define TypeScript interface (MANDATORY)
interface CounterStore {
  // State
  count: number;

  // Actions
  increment: () => void;
  decrement: () => void;
  incrementBy: (amount: number) => void;
  reset: () => void;
}

// 2. Create store with v5 curried syntax
export const useCounterStore = create<CounterStore>()(
  (set) => ({
    // 3. Initial state
    count: 0,

    // 4. Actions using set()
    increment: () => set((state) => ({ count: state.count + 1 })),
    decrement: () => set((state) => ({ count: state.count - 1 })),
    incrementBy: (amount) => set((state) => ({ count: state.count + amount })),
    reset: () => set({ count: 0 }),
  })
);
```

## Middleware Integration

### Persist Middleware (localStorage/sessionStorage)

```typescript
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

interface UserStore {
  user: User | null;
  setUser: (user: User) => void;
  clearUser: () => void;
}

export const useUserStore = create<UserStore>()(
  persist(
    (set) => ({
      user: null,
      setUser: (user) => set({ user }),
      clearUser: () => set({ user: null }),
    }),
    {
      name: 'user-storage', // localStorage key
      storage: createJSONStorage(() => localStorage), // or sessionStorage

      // Persist only specific fields
      partialize: (state) => ({ user: state.user }),
    }
  )
);
```

### DevTools Middleware (Development Debugging)

```typescript
import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

interface TodoStore {
  todos: Todo[];
  addTodo: (todo: Todo) => void;
}

export const useTodoStore = create<TodoStore>()(
  devtools(
    (set) => ({
      todos: [],
      addTodo: (todo) => set((state) => ({ todos: [...state.todos, todo] })),
    }),
    {
      name: 'TodoStore', // Name in Redux DevTools
      enabled: process.env.NODE_ENV === 'development', // Only in dev
    }
  )
);
```

### Combined Middleware (Persist + DevTools)

```typescript
import { create } from 'zustand';
import { persist, devtools, createJSONStorage } from 'zustand/middleware';

interface SettingsStore {
  theme: 'light' | 'dark';
  setTheme: (theme: 'light' | 'dark') => void;
}

export const useSettingsStore = create<SettingsStore>()(
  devtools(
    persist(
      (set) => ({
        theme: 'light',
        setTheme: (theme) => set({ theme }),
      }),
      {
        name: 'settings-storage',
        storage: createJSONStorage(() => localStorage),
      }
    ),
    {
      name: 'SettingsStore',
      enabled: process.env.NODE_ENV === 'development',
    }
  )
);
```

## Async Actions Pattern

```typescript
interface DataStore {
  data: Item[];
  isLoading: boolean;
  error: string | null;
  fetchData: () => Promise<void>;
}

export const useDataStore = create<DataStore>()((set, get) => ({
  data: [],
  isLoading: false,
  error: null,

  // Async fetch pattern
  fetchData: async () => {
    set({ isLoading: true, error: null });

    try {
      const response = await fetch('/api/data');
      if (!response.ok) throw new Error('Fetch failed');

      const data = await response.json();
      set({ data, isLoading: false });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Unknown error',
        isLoading: false,
      });
    }
  },
}));
```

## Performance Optimization with useShallow

### Single Value Selection (Optimal)

```typescript
// BEST: Select single primitive
const count = useCounterStore((state) => state.count);

// Component re-renders ONLY when count changes
```

### Multiple Values with useShallow

```typescript
import { useShallow } from 'zustand/shallow';

// CORRECT: Use useShallow for multiple values
const { count, isActive } = useCounterStore(
  useShallow((state) => ({
    count: state.count,
    isActive: state.isActive,
  }))
);

// Component re-renders ONLY when count OR isActive change
// Without useShallow, this would re-render on ANY store change!
```

## Exporting Reusable Selectors

```typescript
interface UserStore {
  user: User | null;
  preferences: Preferences;
  isAuthenticated: boolean;
}

export const useUserStore = create<UserStore>()(/* ... */);

// Export typed selectors
export const selectUser = (state: UserStore) => state.user;
export const selectIsAuthenticated = (state: UserStore) => state.isAuthenticated;
export const selectUserRole = (state: UserStore) => state.user?.role;

// Usage in components
const user = useUserStore(selectUser);
const isAuthenticated = useUserStore(selectIsAuthenticated);
```

## Anti-Patterns (DO NOT DO)

### Using v4 Syntax

```typescript
// WRONG: v4 syntax
const useStore = create<StoreType>(
  (set) => ({ ... })
);

// CORRECT: v5 curried syntax
const useStore = create<StoreType>()(
  (set) => ({ ... })
);
```

### Direct State Mutation

```typescript
// WRONG: Mutating state directly
addItem: (item) => {
  get().items.push(item); // Mutation!
}

// CORRECT: Immutable update
addItem: (item) => set((state) => ({
  items: [...state.items, item]
}));
```

### Not Using useShallow for Multiple Values

```typescript
// WRONG: Creates new object reference on every render
const data = useStore((state) => ({
  a: state.a,
  b: state.b,
}));
// This will cause infinite render loops in v5!

// CORRECT: Use useShallow
const data = useStore(
  useShallow((state) => ({ a: state.a, b: state.b }))
);
```

## Summary

Zustand v5 requires:
- Curried function syntax: `create<Type>()()`
- TypeScript interface for full type safety
- `useShallow` hook for multiple value selection
- Immutable updates with `set()`
- `createJSONStorage` for persist middleware

---

**Related Skills**: `zustand-slices-pattern-for-scalability`, `zustand-rhf-state-synchronization`
