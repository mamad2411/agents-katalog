---
name: zustand-slices-pattern-for-scalability
version: "1.0"
description: >
  Slice pattern for organizing large Zustand stores with separation of concerns.
  PROACTIVELY activate for: (1) splitting large stores into feature slices, (2) composing multiple slices into a root store, (3) implementing cross-slice actions.
  Triggers: "zustand slice", "large store", "modular state"
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

# Zustand Slices Pattern for Scalability

## When to Use Slices

Use the slice pattern when:
- Store exceeds **150 lines** of code
- Store has more than **10 actions**
- Related features should be co-located
- Multiple developers work on different parts of state
- You need better code organization and maintainability

## Slice Definition Pattern

A **slice** is a function that accepts `set` and `get` and returns a portion of the store:

```typescript
import { StateCreator } from 'zustand';

// Define slice interface
export interface AuthSlice {
  user: User | null;
  isAuthenticated: boolean;
  login: (credentials: Credentials) => Promise<void>;
  logout: () => void;
}

// Create slice function
export const createAuthSlice: StateCreator<AuthSlice> = (set, get) => ({
  user: null,
  isAuthenticated: false,

  login: async (credentials) => {
    const user = await authAPI.login(credentials);
    set({ user, isAuthenticated: true });
  },

  logout: () => set({ user: null, isAuthenticated: false }),
});
```

## Combining Slices

```typescript
import { create } from 'zustand';
import { createAuthSlice, AuthSlice } from './slices/auth-slice';
import { createSettingsSlice, SettingsSlice } from './slices/settings-slice';

// Combine slice types
type RootStore = AuthSlice & SettingsSlice;

// Combine slices with spread syntax
export const useRootStore = create<RootStore>()(
  (...args) => ({
    ...createAuthSlice(...args),
    ...createSettingsSlice(...args),
  })
);
```

## Complete Multi-Slice Example

**File: `lib/stores/slices/auth-slice.ts`**
```typescript
import { StateCreator } from 'zustand';

export interface AuthSlice {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

export const createAuthSlice: StateCreator<AuthSlice> = (set, get) => ({
  user: null,
  token: null,

  login: async (email, password) => {
    const { user, token } = await authAPI.login(email, password);
    set({ user, token });
  },

  logout: () => {
    set({ user: null, token: null });
  },
});
```

**File: `lib/stores/slices/settings-slice.ts`**
```typescript
import { StateCreator } from 'zustand';

export interface SettingsSlice {
  theme: 'light' | 'dark';
  language: string;
  notifications: boolean;
  setTheme: (theme: 'light' | 'dark') => void;
  setLanguage: (language: string) => void;
  toggleNotifications: () => void;
}

export const createSettingsSlice: StateCreator<SettingsSlice> = (set) => ({
  theme: 'light',
  language: 'en',
  notifications: true,

  setTheme: (theme) => set({ theme }),
  setLanguage: (language) => set({ language }),
  toggleNotifications: () => set((state) => ({ notifications: !state.notifications })),
});
```

**File: `lib/stores/root-store.ts`**
```typescript
import { create } from 'zustand';
import { persist, devtools, createJSONStorage } from 'zustand/middleware';
import { createAuthSlice, AuthSlice } from './slices/auth-slice';
import { createSettingsSlice, SettingsSlice } from './slices/settings-slice';

// Combine all slice types
type RootStore = AuthSlice & SettingsSlice;

export const useRootStore = create<RootStore>()(
  devtools(
    persist(
      (...args) => ({
        // Spread all slices
        ...createAuthSlice(...args),
        ...createSettingsSlice(...args),
      }),
      {
        name: 'root-storage',
        // Persist only specific slices
        partialize: (state) => ({
          user: state.user,
          token: state.token,
          theme: state.theme,
          language: state.language,
        }),
      }
    ),
    {
      name: 'RootStore',
    }
  )
);
```

## Cross-Slice Actions

Slices can access other slices via `get()`:

```typescript
import { StateCreator } from 'zustand';
import { AuthSlice } from './auth-slice';
import { SettingsSlice } from './settings-slice';

// This slice needs types from other slices
type ProfileSliceWithDeps = ProfileSlice & AuthSlice & SettingsSlice;

export const createProfileSlice: StateCreator<
  ProfileSliceWithDeps,
  [],
  [],
  ProfileSlice
> = (set, get) => ({
  profile: null,

  updateProfileWithAuth: async (updates) => {
    // Access auth slice via get()
    const { token, user } = get();

    if (!token || !user) {
      throw new Error('Not authenticated');
    }

    // Access settings slice
    const { language } = get();

    const updated = await profileAPI.update(user.id, {
      ...updates,
      language, // Include language from settings
    });

    set({ profile: updated });
  },
});
```

## Selective Slice Usage in Components

```typescript
import { useShallow } from 'zustand/shallow';
import { useRootStore } from '@/lib/stores/root-store';

function AuthComponent() {
  // Select only auth slice
  const { user, login, logout } = useRootStore(
    useShallow((state) => ({
      user: state.user,
      login: state.login,
      logout: state.logout,
    }))
  );

  // Component re-renders only when auth slice changes
  return <div>{user?.name}</div>;
}

function SettingsComponent() {
  // Select only settings slice
  const { theme, setTheme } = useRootStore(
    useShallow((state) => ({
      theme: state.theme,
      setTheme: state.setTheme,
    }))
  );

  // Component re-renders only when settings slice changes
  return <button onClick={() => setTheme('dark')}>{theme}</button>;
}
```

## Anti-Patterns

### Circular Dependencies

```typescript
// WRONG: auth-slice imports profile-slice, profile-slice imports auth-slice
// This creates circular dependency!

// Avoid this by using get() to access other slices at runtime
```

### Typeless Slices

```typescript
// WRONG: No interface defined
export const createMySlice = (set) => ({
  data: null,
  setData: (data) => set({ data }),
});

// CORRECT: With TypeScript interface
export interface MySlice {
  data: Data | null;
  setData: (data: Data) => void;
}

export const createMySlice: StateCreator<MySlice> = (set) => ({
  data: null,
  setData: (data) => set({ data }),
});
```

## Summary

The slice pattern provides:
- Better code organization for large stores
- Separation of concerns by feature domain
- Easier collaboration (different devs work on different slices)
- Selective persistence per slice
- Type-safe slice composition
- Co-location of related state and actions

---

**Related Skills**: `zustand-v5-typed-store-creation`, `zustand-rhf-state-synchronization`
