---
name: ui-stack-react
description: "Building interfaces in React 19: file layout by feature, typed function components, composition and slots, variants with cva, native props and refs passed through, where state lives and derived values, effects only for outside systems, keys, context split by concern, server data with TanStack Query, forms with actions or react-hook-form, Suspense and error boundaries, transitions and deferred values, portals and headless accessible primitives, the React Compiler and memo, Testing Library, and the traps (stale closures, racing effects, props copied into state, index keys, giant components). Read when the project uses React."
---

# React

The generated React component is one 400-line file with a boolean prop per
variation, an effect that copies props into state and another that fetches,
`key={index}`, `useMemo` on everything, a clickable `div`, and one context
holding the whole app. This is React 19 (19.3 in September 2026) as
experienced teams write it: small typed components that compose, state where
it belongs, effects only at the edges. Next.js is in `ui-stack-next`;
app-wide state and data in `frontend-state` and `frontend-data`.

## 1. Project layout

```text
src/main.tsx  src/App.tsx     entry, providers, router
src/routes/                   one file per screen (or the router's layout)
src/components/ui/            primitives: Button, Input, Field, Dialog
src/features/orders/          OrderTable.tsx, OrderFilters.tsx, useOrders.ts,
                              orders.api.ts, OrderTable.test.tsx
src/lib/                      the API client, formatting, cn
```

- Files by feature, not by kind: everything about orders sits together, and
  removing a feature removes a folder. Primitives in `components/ui/`,
  composed parts in `features/<feature>/` (or `components/<feature>/`), or
  the project's own layout.
- A new app: Vite (`npm create vite@latest app -- --template react-ts`), a
  router (React Router or TanStack Router) and TanStack Query; Next.js when
  pages need server rendering or search traffic (`ui-stack-next`).

## 2. Components

- Function components, one per file named for it, props typed (a `type` or
  `interface`); match the project's export style.
- Composition over configuration: `children` and named slots (`icon`,
  `actions` props that take elements) rather than a boolean per variation
  (`showIcon`, `isCompact`). Variants as a `variant` and a `size` prop.
- A primitive passes native props and the `ref` through, so it stays a real
  button to forms and screen readers. In 19 `ref` is an ordinary prop;
  `forwardRef` only before 19.

```tsx
import type { ComponentProps } from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/cn";

const button = cva(
  "inline-flex items-center justify-center gap-2 rounded-md font-medium disabled:opacity-50",
  {
    variants: {
      variant: { primary: "bg-accent text-on-accent", quiet: "text-ink hover:bg-surface-2" },
      size: { sm: "h-8 px-3 text-sm", md: "h-10 px-4" },
    },
    defaultVariants: { variant: "primary", size: "md" },
  },
);
type ButtonProps = ComponentProps<"button"> & VariantProps<typeof button>;
export function Button({ variant, size, className, type = "button", ...props }: ButtonProps) {
  return <button type={type} className={cn(button({ variant, size }), className)} {...props} />;
}
```

- `type="button"` by default: a button inside a form otherwise submits it.
  Without Tailwind, the same shape with a class map from a CSS Module.
- Never define a component inside another's render: it remounts every time
  and loses its state and focus.
- A component past about 200 lines or doing two jobs splits: its data into
  a hook, each region into its own component.

## 3. State

- State in the lowest component that needs it; lift it when two need it;
  context for what many parts read (theme, the signed-in user), not for
  everything.
- Derive values during render instead of copying them into state and
  syncing with an effect: a filtered list is `items.filter(...)` in render.
- State that should reset when a record changes: `key={record.id}` on the
  component, not an effect that clears it.
- Context split by concern (the user, the theme, one per compound
  component), its value stable; in 19 the context is the provider
  (`<ThemeContext value={theme}>`). A value that changes often (form input,
  the pointer) re-renders every reader: keep it local, or in a store with
  selectors (Zustand, `useSyncExternalStore`).
- Filters, tabs and the page number live in the URL through the router, so
  reload and share keep them.

## 4. Effects and events

- Effects only to synchronise with something outside React (a
  subscription, a socket, a third-party widget, the document title), with a
  cleanup. Strict Mode runs them twice in development to prove the cleanup.
- What a click causes belongs in the click handler, not in an effect
  watching state the handler set.
- An effect that needs the latest props without re-running reads them
  through `useEffectEvent` (19.2):

```tsx
const onMessage = useEffectEvent((message: Message) => {
  if (!muted) notify(message); // always the current `muted`
});
useEffect(() => {
  const socket = connect(roomId);
  socket.on("message", onMessage);
  return () => socket.disconnect();
}, [roomId]); // reconnects only when the room changes
```

## 5. Server data

- Through the project's library (TanStack Query, SWR) or the framework's
  loaders; never a hand-written fetch in an effect when one of those is
  there. Loading, error and empty are three branches in the markup, each
  saying what to do:

```tsx
const orders = useQuery({
  queryKey: ["orders", filters],
  queryFn: ({ signal }) => api.listOrders(filters, { signal }),
});
if (orders.isPending) return <OrdersSkeleton />;
if (orders.isError) return <LoadError what="orders" onRetry={() => orders.refetch()} />;
if (orders.data.length === 0) return <NoOrders />;
return <OrderTable orders={orders.data} />;
```

- The key holds every input, so a filter change refetches and caches;
  after a mutation, `queryClient.invalidateQueries({ queryKey: ["orders"] })`.
- Without a library, a fetch in an effect aborts in its cleanup
  (`AbortController`), or the slower of two responses lands last and wins.

## 6. Lists and forms

- Keys are stable ids from the data, never the index for a list that
  changes: with index keys, row state and focus stay at the position while
  the data moves. Hundreds of rows are virtualised (TanStack Virtual) or
  paginated.
- Labels tied to fields with `htmlFor` and an id from `useId`; the error in
  words under the field with `aria-describedby`; the submit button disabled
  and showing progress while pending (`frontend-forms`).
- Use the project's form library (react-hook-form, with zod when it is
  there) for large forms and validation as the user types:

```tsx
const form = useForm<Invite>({ resolver: zodResolver(inviteSchema), defaultValues: { email: "" } });
const id = useId();
const error = form.formState.errors.email;
return (
  <form onSubmit={form.handleSubmit(sendInvite)} noValidate>
    <label htmlFor={id}>Work email</label>
    <input id={id} type="email" autoComplete="email" {...form.register("email")}
      aria-invalid={!!error} aria-describedby={`${id}-error`} />
    <p id={`${id}-error`}>{error?.message}</p>
    <button type="submit" disabled={form.formState.isSubmitting}>Send invite</button>
  </form>
);
```

- A form that posts can use React 19 actions: `<form action={fn}>`,
  `useActionState` for the result and a pending flag, `useFormStatus` in a
  child of the form, `useOptimistic` for a list that updates at once. React
  resets an uncontrolled form after its action: on a failure, return the
  submitted values and use them as `defaultValue`.

## 7. Suspense, errors and transitions

- `<Suspense fallback={<Skeleton />}>` around the part that waits (a lazy
  component, `use(promise)`, a suspense query), where the layout should
  hold, not around the whole app.
- Error boundaries around regions that can fail alone (a chart, a panel),
  with a retry: `react-error-boundary`'s `<ErrorBoundary>`, since a
  boundary is otherwise a class component (`frontend-errors`).
- `useTransition` for an update that renders a lot (a tab switch, a filter
  on a big table): the old screen stays usable and `isPending` dims it.
  `useDeferredValue` for a fast-typed value feeding something slow:
  `<Results query={deferredQuery} dimmed={query !== deferredQuery} />`.
- `<Activity mode="hidden">` (19.2) keeps a hidden tab's state and pauses
  its effects instead of unmounting it.

## 8. Accessibility and overlays

- Semantic elements, never a clickable `div`. Dialogs, menus, tabs,
  popovers, tooltips and comboboxes from the project's primitives (Radix,
  Base UI, React Aria, or shadcn/ui built on one), which handle focus, keys
  and ARIA, rather than hand-rolled.
- Overlays render in a portal (`createPortal(node, document.body)`, which
  the libraries do) or the native top layer (`<dialog>`, `popover`), so no
  `overflow: hidden` parent clips them and no `z-index` war starts.
- Focus moves into a dialog and back to its trigger on close; after a route
  change, focus goes to the new page's `h1` (`frontend-accessibility`).
- `<title>` and `<meta>` rendered in a component are hoisted to `<head>` in
  19: a title per screen without a helmet library.

## 9. Performance

- Memoise after measuring, not by habit. With the React Compiler (1.0) on,
  components and values are memoised for you: add no `useMemo`,
  `useCallback` or `memo` by habit, and keep existing ones until a test
  shows they can go.
- Turning the compiler on: with `@vitejs/plugin-react` 6, add
  `babel({ presets: [reactCompilerPreset()] })` beside `react()` (`babel`
  from `@rolldown/plugin-babel`, the preset from `@vitejs/plugin-react`);
  earlier versions take `react({ babel: { plugins:
  ["babel-plugin-react-compiler"] } })`; Next.js has `reactCompiler: true`.
  Its lint rules come with the latest `eslint-plugin-react-hooks`.
- Split heavy routes and components with `lazy` and a Suspense fallback;
  import one function, not a library's barrel. Images with sizes set
  (`frontend-performance`).

## 10. Testing

Behaviour as a user meets it: Vitest with Testing Library
(`@testing-library/react`, `user-event`, `jest-dom`), queries by role and
name, never by class or test id first (`frontend-testing`).

```tsx
test("filters orders by status", async () => {
  const user = userEvent.setup();
  render(<Orders initial={orders} />);
  await user.click(screen.getByRole("button", { name: "Paid" }));
  expect(screen.getAllByRole("row")).toHaveLength(3); // the header and two paid
});
```

## 11. Traps

- Stale closures: an interval or handler reading state from the render that
  made it. Use the updater (`setCount((c) => c + 1)`), a ref, or
  `useEffectEvent`.
- Racing effects: two requests for two ids, the older landing last. Abort
  in the cleanup, or let the data library handle it.
- Props copied into state (`useState(props.user)`) never update: derive,
  or reset with `key`.
- `{count && <Badge />}` renders `0`: write `count > 0 &&`.
- Ten `useState`s that change together: one `useReducer`, or split the
  component.
- Prop drilling answered with a context for everything: pass `children`
  and elements instead, so the middle layers never see the data.

## Check it

- `npm run build` (a Vite template runs `tsc -b && vite build`), `npm run
  lint` when there is one, `npx vitest run`.
- With Vite, look at the result with the `preview` tool: `url`
  `http://localhost:5173/` and `start` `npm run dev -- --port 5173
  --strictPort`. With Next, see `ui-stack-next`.
- The console in the `preview` report: key warnings, hydration errors and
  failed requests are bugs, not noise.

## Avoid

A boolean prop per variation; components defined inside components; state
copied from props; effects for derived values or for events; fetch in an
effect beside a data library; index keys on changing lists; `useMemo` by
habit; a context for everything; a clickable `div`; a hand-rolled dialog,
menu or combobox; overlays clipped by a parent; `{count && ...}`.
