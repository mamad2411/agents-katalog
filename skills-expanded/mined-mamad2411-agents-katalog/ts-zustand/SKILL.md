---
name: ts-zustand
description: Use when building React state with Zustand — slice composition, selectors, middleware, TypeScript inference.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: language
  languages: [typescript]
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-17"
  related: [react, typescript, ts-zod]
---

# TS Zustand

**Iron Law: split stores into slices, colocate selectors with the store, NEVER call `useStore()` without a selector in render paths — that re-renders on every state change. NEVER store auth tokens or server-derived data in Zustand — tokens belong in httpOnly cookies; server data belongs in TanStack Query / SWR.**

**Version**: this skill targets Zustand v4 (v4.4+). Zustand v5 (2024) changed the `StateCreator` middleware signature and removed several internal APIs. The slice composition pattern shown below still works in v5 but the typing imports differ — when migrating, check the [v5 migration guide](https://zustand.docs.pmnd.rs/migrations/migrating-to-v5).

## Why Zustand (vs Redux / Context)

| Tool                     | Verdict                                                                                                     |
| ------------------------ | ----------------------------------------------------------------------------------------------------------- |
| **Zustand**              | ~3KB, no provider, hooks-native, selectors built-in — **default for most React apps**                       |
| **Redux Toolkit**        | heavier, DevTools/middleware ecosystem is unmatched; pick for very large teams or existing Redux investment |
| **Context + useReducer** | fine for ≤ 3 consumers in one subtree; re-renders the entire tree on any change — wrong at scale            |
| **Jotai / Recoil**       | atom-based; good for derived/dependent state graphs                                                         |

## Minimal store

```ts
import { create } from "zustand";

type CounterState = {
  count: number;
  inc: () => void;
  reset: () => void;
};

export const useCounter = create<CounterState>((set) => ({
  count: 0,
  inc: () => set((s) => ({ count: s.count + 1 })),
  reset: () => set({ count: 0 }),
}));
```

Always pass `set((s) => ...)` (function form) when the next state depends on the current — same reason as `setState` in React. `set({ ... })` (object) when independent.

## Selectors — non-negotiable

```ts
// WRONG — subscribes to the whole store, re-renders on every change
const state = useCounter();
return <span>{state.count}</span>;

// RIGHT — subscribes only to count
const count = useCounter((s) => s.count);
```

For derived state with multiple fields, use `useShallow` (zustand 4.4+):

```ts
import { useShallow } from "zustand/react/shallow";
const { count, inc } = useCounter(useShallow((s) => ({ count: s.count, inc: s.inc })));
```

Without `useShallow`, a new object each call → re-render every time.

## Slices — composition pattern

```ts
import { create, StateCreator } from "zustand";

type AuthSlice = { user: User | null; signIn: (u: User) => void; signOut: () => void };
type CartSlice = { items: Item[]; add: (i: Item) => void; clear: () => void };
type Store = AuthSlice & CartSlice;

const createAuthSlice: StateCreator<Store, [], [], AuthSlice> = (set) => ({
  user: null,
  signIn: (user) => set({ user }),
  signOut: () => set({ user: null, items: [] }), // can touch cart too
});

const createCartSlice: StateCreator<Store, [], [], CartSlice> = (set) => ({
  items: [],
  add: (i) => set((s) => ({ items: [...s.items, i] })),
  clear: () => set({ items: [] }),
});

export const useStore = create<Store>()((...a) => ({
  ...createAuthSlice(...a),
  ...createCartSlice(...a),
}));
// If you add `persist` to this composed store, `partialize` is MANDATORY — see the
// Middleware section below. AuthSlice's `user` field MUST be excluded (XSS-readable
// in localStorage). Default behavior without `partialize` persists the entire Store
// including every slice's state, which will land tokens in browser storage.
```

One file per slice (`auth.slice.ts`, `cart.slice.ts`), one barrel that composes them. Past ~150 lines in a single store file: split it.

## Middleware

| Middleware                | Use                                                                              |
| ------------------------- | -------------------------------------------------------------------------------- |
| **persist**               | sync to localStorage/sessionStorage/AsyncStorage; opt-in fields via `partialize` |
| **devtools**              | Redux DevTools integration; wrap in dev only                                     |
| **immer**                 | mutable-style updates (`set((s) => { s.items.push(x) })`); modest perf cost      |
| **subscribeWithSelector** | fine-grained `store.subscribe(selector, listener)` outside React                 |

```ts
import { devtools, persist } from "zustand/middleware";

export const useStore = create<Store>()(
  devtools(
    persist(
      (set) => ({ ... }),
      // partialize: include ONLY non-sensitive UI state — never auth tokens, never PII.
      // localStorage is XSS-readable: any script on the page can extract it.
      // If your User object contains a token field, exclude it explicitly:
      //   partialize: (s) => ({ user: { id: s.user?.id, displayName: s.user?.displayName } })
      // Tokens belong in httpOnly cookies (set by the server, unreadable by JS).
      { name: "myapp-store", partialize: (s) => ({ theme: s.theme, sidebarOpen: s.sidebarOpen }) },
    ),
    { name: "MyApp", enabled: import.meta.env.DEV },
  ),
);
```

Order matters: `devtools(persist(...))` — devtools wraps the persisted store. Reverse breaks DevTools.

## Outside-React access

```ts
useStore.getState().signOut(); // imperative read/dispatch (e.g., in API client)
const unsub = useStore.subscribe(
  (s) => s.user,
  (user, prev) => {
    /* react to user change */
  },
);
```

`getState`/`subscribe` are the escape hatches — fine for axios interceptors, event handlers, websocket adapters.

## Anti-patterns

- One monolithic store with 40 fields — split into slices
- `useStore()` without a selector — every render on every change
- Selectors that return new objects/arrays without `useShallow` — re-render storm
- Multiple parallel stores (`useUser`, `useUserSettings`, `useUserPrefs`) that always change together — should be one store
- Mutating state directly (`state.items.push(...)`) without immer middleware — React won't see it
- Storing derived state instead of computing in selector — drift
- Persisting non-serializable values (Maps, Sets, Class instances) without `storage:` custom serializer
- Storing UI ephemeral state (modal open/close) globally when component-local would do

## Red flags

| Thought                          | Reality                                                          |
| -------------------------------- | ---------------------------------------------------------------- |
| "Everything's re-rendering"      | Check selectors — `useStore()` bare is the cause 90% of the time |
| "I'll just use Context for this" | One re-render of 200 components later, you'll switch             |
| "Slice it later"                 | Two weeks later your store is 600 lines and everyone fears it    |
| "Persist the whole store"        | Token + cart on a public terminal — careful what you persist     |

## Hand-off

For component patterns + hooks rules: `Skill(react)`. For input validation at store boundaries: `Skill(ts-zod)`. For TS-level type design: `Skill(typescript)`.
