---
name: follow-lib-solidjs-manage-state
description: SolidJS reactivity — createSignal, createStore, createMemo, createEffect, batch, untrack, context
argument-hint: "[primitive]"
related:
  - follow-lib-solidjs
  - run-test
  - resolve-errors
---

## Goal

Use SolidJS primitives fully — signals, stores, memos, effects, batching, context — with the fine-grained reactivity model

## Scope

state management — `createSignal`, `createStore`, `produce`/`reconcile`, `createMemo`, `createEffect`/`on`, `createRoot`, `createContext`, `untrack`/`batch`

## Execute

### 1. Signals

```ts
const [count, setCount] = createSignal(0)
setCount(c => c + 1)
setCount(5)            // replace
count()                // read — tracks in a reactive scope
```

- `createSignal(v, { equals: false })` — always notify; or a custom `equals` comparator
- Signals = Solid's atoms — tracking happens only when read inside a reactive scope (JSX/memo/effect)

### 2. Stores (Nested State)

```ts
const [state, setState] = createStore({ todos: [], filter: 'all' })
setState('todos', state.todos.length, newTodo)       // path-based update
setState(produce(s => s.todos.push(todo)))            // immer-style mutation
setState('filter', reconcile(newFilter))              // deep merge replace
```

- Store = proxy — reading nested values in JSX is fully reactive (`state.todos` tracks automatically)
- `produce` = mutation API; `reconcile` = diff-merge; `unwrap` = non-proxy snapshot

### 3. Derived Values

```ts
const doubled = createMemo(() => count() * 2)
const filtered = createMemo(() => todos().filter(t => !t.done))
```

- `createMemo` — cached derived value; `createComputed` — eager derived (pre-render)
- `createSelector` — selection reactivity (list item compare per item)

### 4. Effects And Control

```ts
createEffect(() => console.log(count()))                    // tracks deps automatically
createEffect(on(count, v => console.log(v)))                // explicit deps
onCleanup(() => sub.unsubscribe())                          // cleanup in an effect/root
batch(() => { setA(1); setB(2) })                           // single update flush
untrack(() => count())                                      // read without tracking
```

- `createRoot` — manual disposal scope; `createContext`+`useContext` — DI tree

### 5. Patterns

1. `createResource` for async → the `handle-async` workflow
2. Global state: create the signal/store at module top-level — no Provider requirement
3. Forms: controlled input = `value`/`onInput` — no re-render cost

## Rules

- Reading a signal outside a reactive scope = a static value — never cache `const v = count()` and use it in JSX
- `createEffect` is for side effects only — use `createMemo` for derived state
- Store updates go through path/`produce`/`reconcile` — never mutate `state.x = v` directly
- `untrack` when reading without subscribing; `batch` merges updates into one flush

## Expected Outcome

- Fine-grained reactivity correct — no stale reads / over-tracking
- Stores/signals/memos/effects used for the right purposes
