---
name: react-patterns
description: Writes and reviews idiomatic React - minimal state with derived values, effects only for external systems, server state through a data library or framework loaders, correct keys, composition over prop drilling, measured memoization, error boundaries, Suspense, forms and actions, and the Server/Client Component boundary. Use when building or reviewing React components or hooks, fixing re-render, stale state or useEffect bugs, structuring state, data fetching and forms, or testing components in React, Next.js, React Router/Remix or Vite apps.
license: MIT
---

# React Patterns

UI is a function of state. Keep the minimum state, compute everything else during render, and use effects only to synchronize with systems outside React. Most React bugs come from duplicated state and effects that should not exist.

## When to use

- Writing or reviewing components, custom hooks or a React diff.
- Bugs: stale values, infinite re-render loops, flicker, "state is one step behind", lost input focus, slow typing.
- Deciding where state, data fetching or form handling should live.

Not for: React Native platform APIs, or styling questions.

## Workflow

1. **Check the versions.** Read `package.json` for the `react` version and the framework (Next.js App Router or Pages Router, React Router v7 / Remix, Vite SPA, Expo). React 19 APIs (actions, `use`, ref as a prop, `<Context value>`) need `react` 19+. Server Components need a framework that supports them.
2. **Check for React Compiler** (`babel-plugin-react-compiler`, or the framework's compiler option). If it is on, don't add manual `useMemo`/`useCallback`/`memo` unless profiling shows a need. Check the installed version's docs for what it covers.
3. **Classify every piece of data** using the table below before writing state.
4. **Audit every `useEffect`** against [references/effects.md](references/effects.md). Delete the ones that don't sync with an external system.
5. **Lint with `eslint-plugin-react-hooks`.** Fix `exhaustive-deps` warnings by restructuring code; never suppress them.
6. **Test behavior** with Testing Library (see Testing).

## Where state lives

| Kind | Example | Put it in |
|---|---|---|
| Server data | users, orders | A data library (TanStack Query, SWR, RTK Query, Apollo, Relay) or framework loaders / Server Components. Never copy it into `useState` |
| URL state | filters, sort, tab, page | Search params or route params, so it survives reload and can be shared |
| Form state | inputs before submit | Uncontrolled inputs plus `FormData`, or a form library for complex validation |
| Local UI state | open/closed, hover | `useState` in the lowest component that needs it |
| Shared client state | theme, current user, cart | Context for low-frequency values; a store with selectors (Zustand, Redux Toolkit, Jotai) for frequently changing ones |
| Derived values | filtered list, totals, validity | Compute during render; `useMemo` only if measured as expensive |

Lift state to the closest common parent of the components that need it, and no higher.

## Rules

### Derive, don't sync

```tsx
// Bad: duplicated state kept in sync by an effect (extra render, can drift)
const [fullName, setFullName] = useState("");
useEffect(() => { setFullName(`${first} ${last}`); }, [first, last]);

// Good
const fullName = `${first} ${last}`;
```

Store IDs, not copies of objects: keep `selectedId` and look up the item, so edits to the list are never shadowed by a stale copy.

### Effects are for external systems

Valid uses: subscriptions (WebSocket, browser events, `matchMedia`), third-party widgets and manual DOM integration, timers, and fetching data when no library or framework loader is available. Everything else (transforming data, reacting to a click, resetting state on a prop change, notifying a parent) belongs in render or in an event handler. See [references/effects.md](references/effects.md).

Every effect that starts something must stop it:

```tsx
useEffect(() => {
  const socket = connect(roomId);
  socket.on("message", onMessage);
  return () => socket.disconnect();
}, [roomId]);
```

Strict Mode runs effects twice in development to expose missing cleanup. Fix the cleanup; don't remove Strict Mode.

### Reset state with a key

```tsx
// Remounts the form, clearing its state, whenever the user changes
<ProfileForm key={user.id} user={user} />
```

### Keys in lists

- Use a stable, unique ID from the data.
- Don't use the array index for lists that can reorder, insert or delete; state and focus attach to the wrong row.
- Never generate keys during render (`Math.random()`, `crypto.randomUUID()`); every render remounts every row.

### Controlled vs uncontrolled inputs

| Use | When |
|---|---|
| Uncontrolled (`defaultValue`, read with `FormData` or a ref) | Most forms: values are only needed on submit |
| Controlled (`value` + `onChange`) | The UI must react to every keystroke: live validation, formatting, dependent fields |

Never switch one input between controlled and uncontrolled (`value={undefined}` then a string). Initialize with `""`.

### Composition before context

Pass components as `children` or slot props instead of threading props through layers that don't use them.

```tsx
<Layout sidebar={<UserMenu user={user} />}>
  <Dashboard user={user} />
</Layout>
```

When context is right:

- Split contexts by how often they change (theme vs live cursor position). Every consumer re-renders when the value changes.
- Memoize object values so consumers don't re-render on every provider render:

```tsx
const value = useMemo(() => ({ user, signOut }), [user, signOut]);
return <AuthContext value={value}>{children}</AuthContext>; // React 18: AuthContext.Provider
```

- For high-frequency shared state, use a store with selectors instead of context.

### Memoize only what you measured

Profile first with the React DevTools Profiler. Reach for `useMemo`, `useCallback` or `memo` when:

- a computation is measurably slow (filtering or sorting thousands of items on every keystroke),
- a memoized child or an effect dependency needs a stable reference.

Wrapping everything adds noise and hides real problems. For slow typing, try `useDeferredValue` or `startTransition` for the expensive part, and virtualize long lists.

### Error boundaries and Suspense

- Put an error boundary at each route and around independent widgets so one failure doesn't blank the page. Boundaries are class components (`getDerivedStateFromError`, `componentDidCatch`) or the `react-error-boundary` package.
- Boundaries do not catch errors in event handlers, `setTimeout` or other async code; handle those with `try/catch` and show state.
- Use `<Suspense fallback={...}>` with data sources that support it (framework loaders, `useSuspenseQuery`, `use(promise)` in React 19). A promise passed to `use` must come from a cache, a loader or a parent; one created during render is recreated on every render.
- Place Suspense boundaries where a loading state makes sense to the user, not around every component.

### Server and Client Components

Only applies in frameworks with React Server Components (for example the Next.js App Router).

- Components are Server Components by default. `"use client"` at the top of a file makes it and everything it imports client code. Put the directive on small leaf components (a button, a chart), not on layouts.
- Server Components cannot use state, effects, event handlers or browser APIs.
- Props passed from server to client must be serializable. Pass Server Components into Client Components as `children`.
- Import the `server-only` package in modules with secrets or DB access so they fail the build if imported into client code.
- Functions marked `"use server"` are public HTTP endpoints. Validate their input and check authorization inside every one.

### Forms and actions (React 19)

```tsx
import { useActionState } from "react";

async function subscribe(prevState: { error: string | null }, formData: FormData) {
  const email = String(formData.get("email") ?? "");
  if (!email.includes("@")) return { error: "Enter a valid email address." };
  await api.subscribe(email);
  return { error: null };
}

export function SubscribeForm() {
  const [state, formAction, isPending] = useActionState(subscribe, { error: null });
  return (
    <form action={formAction}>
      <label htmlFor="email">Email</label>
      <input id="email" name="email" type="email" required />
      <button type="submit" disabled={isPending}>Subscribe</button>
      {state.error && <p role="alert">{state.error}</p>}
    </form>
  );
}
```

- `useFormStatus` (from `react-dom`) only works in a component rendered inside the `<form>`.
- `useOptimistic` shows an expected result while the action runs and reverts on failure.
- Validate on the server too; client checks are only for user experience.

### Custom hooks

Extract a hook to share logic, not state: each call gets its own state. Name it `useSomething`, call hooks unconditionally at the top level, and return the smallest useful API.

## Testing

```tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

test("adds a todo", async () => {
  const user = userEvent.setup();
  render(<Todos />);
  await user.type(screen.getByRole("textbox", { name: /new todo/i }), "Buy milk");
  await user.click(screen.getByRole("button", { name: /add/i }));
  expect(screen.getByRole("listitem")).toHaveTextContent("Buy milk");
});
```

- Query in this order: `getByRole` (with `name`), `getByLabelText`, `getByText`, and `getByTestId` only as a last resort. Role queries also catch accessibility bugs.
- Use `findBy*` for content that appears asynchronously; don't add manual waits.
- Mock the network at the boundary (for example MSW), not the component's own hooks.
- Test what the user sees and does, not state variables or hook internals.

## Anti-patterns

- **Effect chains**: one effect sets state that triggers another. Compute in render or do it all in the event handler.
- **Fetching in `useEffect` without cleanup**: race conditions show stale results. Use a data library, or handle races as shown in the reference.
- **Server data copied into `useState`**: it goes stale. Read it from the cache.
- **Objects or functions created in render used as effect dependencies**: the effect runs every render. Move them inside the effect or outside the component.
- **Index or random keys** on dynamic lists.
- **Defining a component inside another component**: it remounts on every render and loses state and focus.
- **One giant context** holding everything.
- **`"use client"` at the root layout**: it turns the whole tree into client code.
- **Suppressing `exhaustive-deps`**: it hides stale closures.

## Done when

- No effect exists that only transforms data or responds to a user event.
- Every effect that subscribes, connects or starts a timer has cleanup.
- Server state lives in a data library or framework loader, URL state lives in the URL.
- Hooks lint passes with no suppressed warnings; tests query by role.
- Any memoization added is backed by a profile or a stable-reference requirement.

## References

- [references/effects.md](references/effects.md) — read when writing, reviewing or debugging any `useEffect`, or deciding between an effect, an event handler, render-time computation or `useSyncExternalStore`.
