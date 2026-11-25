---
name: react-conventions
description: Use when writing or reviewing React code — adding a feature beside existing ones, placing a sub-component's hook, helper or constant inside a feature, importing from another feature or layer, letting one feature use another, registering a reducer, route or provider, holding a request's loading, error and data in a component, putting two requests in one component (loading its options and creating an option), reading a value from useRef or writing usePrevious, setting up the app's layout or routes, an error boundary, a white screen after a render error.
---

# React conventions

Before you add a file or an import to a feature, look at how this feature and
the others do it. When they consistently place files or import each other
otherwise than the sections below, their way wins: match it, and say so in the
reply. With files grouped by kind, as `components/` and `hooks/`, a new hook
goes into `hooks/` and a new component into `components/`. With deep imports
and no `index.ts`, an import stays a deep import, and no `index.ts` is added.
The direction does not yield: an upward import, or a second direction between
two features, is debt, not a precedent.

## Layers import downward only

Top to bottom: `app → features → shared → ui → core`. A layer imports only the
layers below it. Inside `features`, the next section says when one feature may
use another.

An upward import that already exists is debt, not a precedent. Do not add
another one beside it. Report each existing one as a finding outside the
change.

```ts
// core/store.ts
import { offersReducer } from '../features/offers/offers-slice';   // no: core imports a feature
```

When a lower layer must know a feature — a store, a router, a list of
providers — the feature registers itself through an extension point that the
lower layer owns, or `app` wires the two together:

```ts
// core/store.ts: the extension point, no feature imports
import { combineSlices } from '@reduxjs/toolkit';

import { sessionSlice } from './session-slice';

// interface: declaration merging, each feature adds its slice
export interface LazyLoadedSlices {}

export const rootReducer = combineSlices(sessionSlice).withLazyLoadedSlices<LazyLoadedSlices>();
```

```ts
// features/offers/offers-slice.ts: the feature registers itself
import { createSlice, type WithSlice } from '@reduxjs/toolkit';

import { rootReducer } from '../../core/store';

const offersSlice = createSlice({ /* … */ });

declare module '../../core/store' {
  // interface: module augmentation
  interface LazyLoadedSlices extends WithSlice<typeof offersSlice> {}
}

export const injectedOffersSlice = offersSlice.injectInto(rootReducer);
```

## A feature uses another only through its index, one way

By default a feature imports no other feature. When a page needs two features,
the page or `app` composes them, and neither knows about the other:

```tsx
<OffersList toolbar={<SearchBox scope="offers" />} />
```

When feature A needs something feature B owns — a component, hook or API of B's
domain — A imports it through `features/b/index.ts`, and only in one direction:
with `offers → search`, `search → offers` is forbidden. Two features that need
each other share a part that belongs on a lower layer.

```ts
import { useSearch } from '../search';                 // offers → search, through the index
import { useSearch } from '../search/use-search';      // no: a deep import
import { abortPrevious } from '../reports';            // no: a generic helper
```

Before you add an import from another feature, search the files of that
feature for imports from this one, deep imports too. Search also the features
that it imports, and the features that they import. When an import leads back
to this feature, do not add yours, not even through the index. A file that may
import both composes them: a file of the other feature that already renders a
part of this one, or else `app`. It gives this feature what it needs from the
other one as a prop: a value, an element or a callback.

```tsx
// app/search-route.tsx: offers already imports search, so search gets the count from app
import { useOffers } from '../features/offers';
import { SearchPage } from '../features/search';

export function SearchRoute() {
  const { countMatching } = useOffers();

  return <SearchPage countOffers={countMatching} />;
}
```

A generic helper — abort logic, a formatter, a fetch wrapper — is never part of
a feature's API, even through its `index.ts`. It moves down to `shared` before
the second feature imports it. A move leaves one copy: in the same change, the
body goes to `shared` unchanged, and the old place becomes one line,
`export { abortPrevious } from '../../shared/abort-previous';`, or loses the
helper. Show that one-line file in the change. A copy in the second feature,
even one marked to move later, is the failure this rule prevents: two copies
drift apart.

## A part's own files live in its folder

A sub-component with a hook, helper or constant file of its own is a folder:
its component and the files that only it uses. A file that two parts use goes
to their nearest common folder. A shared type goes into `models/` and a schema
into `schemas/` of its area, the nearest folder that holds every file that uses
it, as typescript-conventions says. The page is the feature's top part, so its
own files sit at the feature root.

```
features/orders/
├── index.ts
├── orders-page.tsx        composes the parts
├── fetch-orders.ts        the page's request
├── models/order.ts        the type that the page and the table use
├── schemas/order.ts       the schema that fetch-orders.ts parses with
└── orders-table/
    ├── orders-table.tsx   ROWS_PER_PAGE stays in it, below the export
    └── use-table-sort.ts  only the table uses it
```

A flat `features/orders/use-table-sort.ts`, beside a flat `orders-table.tsx`,
would say that the page uses the hook, or more than one part does. A
sub-component with no file of its own stays one file next to its parent.

## A request's state is one union

```tsx
// no: three flags that can disagree
const [isLoading, setIsLoading] = useState(false);
const [error, setError] = useState<Error | null>(null);
const [results, setResults] = useState<SearchResult[]>([]);
```

```tsx
type SearchState =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'failed'; error: Error }
  | { status: 'done'; results: SearchResult[] };

const [search, setSearch] = useState<SearchState>({ status: 'idle' });
```

Three flags allow eight combinations, and only four of them are real. Every
transition then resets the other two by hand, and one missed reset shows an
error over fresh results. With one union, each transition is one `setSearch`,
and the render branches on `status`. If the project already has a data library
(TanStack Query, RTK Query), it holds this state instead.

## A component with two jobs gives each one a hook

A job is a request and its state: loading the options, creating an item,
sending a form. When one component body holds two jobs or more, each with its
own state and its own async call, each job moves into a custom hook of its
own. The component calls the hooks, connects them to each other and to its
callback props, as `onChange`, and renders.

```tsx
// no: two requests and their state in one body
export function GroupSelect({ type, onChange }: GroupSelectProps) {
  const [name, setName] = useState('');
  const [options, setOptions] = useState<OptionsState>({ status: 'loading' });
  const [creation, setCreation] = useState<CreationState>({ status: 'idle' });

  useEffect(() => {
    // fetch the options, setOptions at each step
  }, [type]);

  async function handleCreate() {
    // post, setCreation, add to the options, onChange
  }

  return <div>…</div>;
}
```

```tsx
export function GroupSelect({ type, onChange }: GroupSelectProps) {
  const [name, setName] = useState('');
  const { options, addOption } = useGroupOptions(type);
  const { creation, createGroup } = useCreateGroup(type, (group) => {
    addOption(group);
    onChange(group);
  });

  function handleCreate() {
    createGroup(name);
  }

  return <div>…</div>;
}
```

Count the jobs, not the lines. A short body with two requests has two jobs. A
long form with one submit has one job, and its request can stay in the
component. Without a data library, each job's hook holds one union, as *A
request's state is one union* says. If the project already has a data
library, each job's hook holds the library's call, as `useQuery` or
`useMutation`, and the library holds the state. A query and a mutation in one
body are two jobs, and so are two queries or two mutations. The hooks are the
component's own files, and *A part's own files live in its folder* places
them: `group-select/use-group-options.ts` next to
`group-select/group-select.tsx`, and a page's hooks sit at the feature root.

The text of an input is not kept in a job's hook. In the example, the
component holds it as `name` and gives it to `createGroup(name)`.

## Render reads props, state and context — not refs

A ref change schedules no render. A value read from `ref.current` in the
component body can be stale, and the UI does not update when it changes. The
common `usePrevious` — `useRef`, an effect that writes it,
`return ref.current` — does exactly this: an arrow next to a changed price
disappears on the next unrelated render.

```ts
export function usePrevious<T>(value: T): T | undefined {
  const [state, setState] = useState<{ value: T; previous: T | undefined }>({ value, previous: undefined });

  if (!Object.is(state.value, value)) {
    setState({ value, previous: state.value });
  }

  return state.previous;
}
```

It returns the previous *different* value: A → B → B gives
`undefined → A → A`. Pass a primitive or a value with a stable identity: an
object literal made in the same render is new every time and loops.

Read and write refs in effects and event handlers. A value that the UI shows is
state. The one exception is lazy initialisation:

```ts
if (playerRef.current === null) {
  playerRef.current = new Player();
}
```

## The app root and each route have an error boundary

When a render throws and no error boundary catches it, React removes the whole
tree: the user sees a white page. So each time you write or change the app's
root (`main.tsx`, `App`), its layout or its routes, check the two levels below,
and add each one that is missing in the same change, even when the task does
not name it:

1. **App level**, always: around the layout. Its fallback uses nothing that can
   fail with the app — no request, no store, no context of a feature — and
   offers a reload.
2. **Route level**, when the app has routes: inside the layout, around the
   content of each route. An error on one page shows its fallback in the
   content area. The header, the navigation and the other routes keep working,
   and the boundary resets when the route changes.

In an app with routes, one boundary around the whole app is the failure that
this rule prevents: one broken page takes every page down. An app without
routes has the app level only:

```tsx
// main.tsx: an app without routes
createRoot(document.getElementById('root')!).render(
  <ErrorBoundary fallback={<AppError />} onError={reportError}>
    <App />
  </ErrorBoundary>,
);
```

With routes:

```tsx
// app/router.tsx
export const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    errorElement: <AppError />,        // app level: in place of the layout
    children: [
      {
        errorElement: <PageError />,   // route level: in the layout's <Outlet />
        children: [
          { index: true, element: <HomePage /> },
          { path: 'orders', element: <OrdersPage /> },
        ],
      },
    ],
  },
]);
```

Use the router's own mechanism when the project has one: `errorElement` or
`ErrorBoundary` of a React Router route made with `createBrowserRouter` or in
framework mode, `errorComponent` of TanStack Router, `error.tsx` under the root
layout and `global-error.tsx` in Next.js. A `<Route>` inside `<BrowserRouter>`
ignores `errorElement`. Without such a mechanism, use `react-error-boundary` if
the project has it, or one `ErrorBoundary` class: React has no boundary as a
function component. Such a boundary resets only when told, so the route-level
one gets `key={location.pathname}`. The fallbacks are generic code on a lower
layer, and `app` wires both levels. Each boundary reports the error that it
catches.

A boundary catches an error that a render throws, not one in an event handler
or a `setTimeout` callback. A request's error is state, as *A request's state
is one union* says.
