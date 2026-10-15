---
name: legend-state
description: >
  Use Legend-State v3 for local and remote state management in React, React Native, or vanilla JS.
  Trigger this skill whenever the user mentions Legend-State, legend-state, @legendapp/state, observables,
  fine-grained reactivity, useValue, synced, syncedCrud, syncedFetch, syncedKeel, syncedSupabase,
  syncedQuery, For component, reactive components, or wants to set up state management with automatic
  persistence/sync. Also use when migrating from other state libraries to Legend-State, optimizing
  Legend-State performance, or debugging Legend-State reactivity issues. If the user is working with
  any state management that involves observables, signals, or fine-grained reactivity and Legend-State
  is installed or mentioned, use this skill.
---

# Legend-State v3 Skill

Legend-State is a fast all-in-one local and remote state library. It uses observables with fine-grained
reactivity so components re-render only when the specific state they care about changes.

## Quick Reference

### Core Concepts

- **Observables** wrap data with `get()`/`set()` access and automatic change tracking
- **Naming convention**: suffix observable variables with `$` (e.g., `state$`, `theme$`)
- **No boilerplate**: no reducers, actions, dispatchers, or immutability required
- **Two usage patterns**: one large global store OR multiple individual atoms — both work

### Creating Observables

```js
import { observable } from "@legendapp/state"

// Global store
const store$ = observable({
  todos: [],
  settings: { theme: 'dark' },
})

// Individual atoms
const theme$ = observable('dark')
const count$ = observable(0)

// Computed observable (function that auto-recomputes)
const name$ = observable(() => `${store$.first.get()} ${store$.last.get()}`)

// Async observable (Promise)
const data$ = observable(() => fetch('/api/data').then(r => r.json()))
```

### Reading and Writing

```js
// Get the raw value
const theme = store$.settings.theme.get()

// Set a value
store$.settings.theme.set('light')
store$.todos.push({ id: 1, text: 'Buy milk' })

// Peek (read without tracking)
const current = store$.settings.theme.peek()

// Assign multiple properties
store$.settings.assign({ theme: 'dark', fontSize: 14 })
```

### React Integration (v3 primary pattern)

**Use `useValue` — not `observer` with `.get()` — as the primary way to consume observables in React.**
This is required for React Compiler compatibility.

```jsx
import { useValue, useObservable } from "@legendapp/state/react"

function Component() {
  // Track a single observable
  const theme = useValue(store$.settings.theme)

  // Track a computation
  const completedCount = useValue(() =>
    store$.todos.get().filter(t => t.completed).length
  )

  // Local observable within a component
  const local$ = useObservable({ count: 0 })
  const count = useValue(local$.count)

  return <div>{theme} — {count}</div>
}
```

**`observer`** is now an optional optimization that merges multiple `useValue` calls into a single hook:

```jsx
import { observer, useValue } from "@legendapp/state/react"

const Component = observer(function Component() {
  const a = useValue(state$.a)
  const b = useValue(state$.b)
  const c = useValue(state$.c)
  // ... all tracked in one hook
})
```

### Fine-Grained Reactivity

Use these to minimize re-renders:

```jsx
import { Memo, For, Show, Switch } from "@legendapp/state/react"

// Memo: self-updating element, parent never re-renders
<Memo>{count$}</Memo>
<Memo>{() => <div>{state$.value.get()}</div>}</Memo>

// For: optimized array rendering
<For each={store$.todos} item={TodoItem} />
<For each={store$.todos} optimized item={TodoItem} />

// Show: conditional rendering without parent re-render
<Show if={state$.showModal}>
  {() => <Modal />}
</Show>

// Switch: render based on value
<Switch value={state$.page}>
  {{
    home: () => <Home />,
    settings: () => <Settings />,
    default: () => <NotFound />,
  }}
</Switch>
```

### Reactive Components

```jsx
// Web
import { $React } from "@legendapp/state/react-web"
<$React.div $className={() => state$.active.get() ? 'on' : 'off'} />
<$React.input $value={state$.name} />

// React Native
import { $TextInput, $View } from "@legendapp/state/react-native"
<$TextInput $value={state$.name} />
```

### Batching

```js
import { batch } from "@legendapp/state"

batch(() => {
  // Multiple changes, one notification
  store$.todos.push(item1)
  store$.todos.push(item2)
})
```

### Persistence and Sync

```js
import { syncObservable } from "@legendapp/state/sync"
import { ObservablePersistLocalStorage } from "@legendapp/state/persist-plugins/local-storage"

syncObservable(store$, {
  persist: {
    name: 'my-app',
    plugin: ObservablePersistLocalStorage,
  }
})
```

### Key Performance Tips

1. **Use `useValue`** instead of `.get()` inside components for automatic tracking
2. **Use `For` component** for arrays, with `optimized` prop for drag/drop or reordering
3. **Call `.get()` before iterating** large arrays to skip Proxy creation
4. **Batch multiple changes** to avoid excessive re-renders
5. **Arrays need unique `id` or `key`** fields for optimized rendering
6. **Use `peek()`** when you need a value but don't want to track it

## Reference Files

Read these for detailed guidance:

- [references/core.md](references/core.md) — Observable API, computed, async, linked, events, safety
- [references/react.md](references/react.md) — React hooks, fine-grained reactivity, reactive components, tracing
- [references/performance.md](references/performance.md) — Batching, array optimization, Proxy considerations
- [references/patterns.md](references/patterns.md) — Organizing state (global store vs atoms vs component state)
- [references/sync.md](references/sync.md) — Persistence, synced, syncedCrud, syncedFetch, Keel, Supabase, TanStack Query
- [references/helpers.md](references/helpers.md) — Helper functions, undo/redo, trackHistory, configuration

## Migration Notes (v2 → v3)

- `useSelector` / `use$` → `useValue`
- `observer` with `.get()` → `observer` with `useValue` (required for React Compiler)
- `computed()` → `observable(() => ...)`
- `persistObservable` → `syncObservable`
- Reactive props now use `$` prefix: `$value`, `$className`
- `Reactive` components → `$React` namespace (web) or `$Component` (React Native)

See [references/sync.md](references/sync.md) for full migration details.
