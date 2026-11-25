---
name: follow-lib-solidjs-build-components
description: Write SolidJS components — props, children, control flow (<For>/<Show>/<Switch>), refs, portals
argument-hint: "[scope]"
related:
  - follow-lib-solidjs
  - run-test
  - resolve-errors
---

## Goal

Write SolidJS components with the correct mental model — render-once, props destructuring pitfalls, control flow components, refs/portals

## Scope

component authoring — JSX in Solid renders once (unlike React re-rendering); state primitives → `manage-state`

## Execute

### 1. Component Basics

```tsx
function Card(props: { title: string; children?: JSX.Element }) {
  return <section><h2>{props.title}</h2>{props.children}</section>
}
```

- **Render-once**: the component body runs once — only reactive expressions in JSX update
- **Never destructure props immediately** — `const { title } = props` destroys reactivity; use `props.title` in JSX or `mergeProps`/`splitProps`

```ts
const [local, rest] = splitProps(props, ['title', 'variant'])
const merged = mergeProps({ variant: 'default' }, props)
```

### 2. Control Flow Components

```tsx
<Show when={user()} fallback={<Login />}>{u => <Profile user={u()} />}</Show>
<For each={items()} fallback={<Empty />}>{item => <Row item={item} />}</For>
<Switch><Match when={a()}>...</Match><Match when={b()}>...</Match></Switch>
<ErrorBoundary fallback={err => <Oops err={err} />}>...</ErrorBoundary>
```

- `<For>` = keyed (identity tracking); `<Index>` = index-based (for primitives whose values change)
- `<Dynamic component={Comp()} />` — dynamic component; `<Portal>` — render across the DOM tree

### 3. Refs And Directives

```tsx
let inputRef!: HTMLInputElement
<input ref={inputRef} />           // or ref={el => el.focus()}
```

- `ref` = the real element, not a wrapper
- Directives: `use:directiveName` (custom `directives/`), `classList={{ active: isActive() }}`
- Event handlers: `onClick`, `on:input` — auto-delegated; `onClick={[handler, data]}` bound args

### 4. Patterns

1. Context: `createContext` + `useContext` — works across every component tree (no memo needed)
2. Lazy: `lazy(() => import('./Heavy'))` — code split
3. `children` — `props.children` evaluates once; `children(() => props.children)` for helpers

## Rules

- Props destructuring → reactivity loss — use `splitProps`/`mergeProps` only
- `<For>` keys by item identity — don't use plain map+index for lists that reorder
- JSX is not a template string — `{...}` expressions evaluate lazily within the JSX scope only
- The component body does not re-run — logic in the body = runs once; reactive logic lives in JSX/effects

## Expected Outcome

- Components correctly reactive (reactivity not broken via destructuring)
- Control flow uses the right components
