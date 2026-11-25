---
name: architecture
description: The four-layer frontend architecture — infrastructure → domain → view → routes — with its dependency rules, file layout, naming conventions, and the recurring patterns that hold it together (serialization boundary, initial-data hook ladder, flow state machines, typed domain errors). Use whenever adding or changing a feature, page, API call, hook, form, or component in a React app laid out as src/infrastructure + src/domain + src/view + src/pages; whenever deciding which layer a piece of code belongs in; whenever reviewing a diff for layering violations; and whenever structuring a greenfield React frontend that wants a proven shape. Reach for it even when a request sounds purely local — "add a field to this form", "call this new endpoint", "show a spinner here" — because those are precisely the changes that quietly leak business rules into components.
---

# Layered Frontend Architecture

## The one idea

**Everything the app _means_ lives in one layer that neither the network nor React can
corrupt.**

`domain/` holds the app's types, rules, and state transitions. It does not know it is
rendered by React, and it does not know the server speaks JSON over HTTP. Every other
layer is an adapter sitting on one side of it:

```
src/pages/            routes    URL → fetch → serialize → provider → view page   (thin)
       ↓
src/view/             React     components, hooks, providers, view models
       ↓
src/domain/           meaning   types, rules, transitions        ← no React, no URLs
       ↓
src/infrastructure/   world     HTTP clients, response schemas, cookies   ← no rules
```

This costs a few extra files per feature. What it buys:

- **The API's ugliness stops at one file.** `snake_case`, nullable-everything, an endpoint
  that returns a bare object where it swore it returned an array — all of it gets normalized
  in one domain function instead of being re-handled in nine components.
- **Components read as layout.** When a decision has a name (`checkIfCanProceedToPayment`)
  the JSX stops being a place where rules hide.
- **The rules are the cheapest thing in the app to test.** Pure functions, no DOM, no mocking
  a fetch. Colocate `thing.test.ts` beside `thing.ts`.

## What goes where

| Layer                 | Owns                                                                                                                                                                                                                                         | Never contains                                                                        |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `src/infrastructure/` | `httpClients/` (configured client instances), `endpoints/` (one function per API call plus its response schema), `models/` (schemas for shapes shared across endpoints), `cookies/`, `endpoints-helpers/` (parsing too large to inline)      | Business rules, React, decisions about what the app should do with the data           |
| `src/domain/`         | One folder per concept (`product/`, `auth/`, `checkout-flow/`). Types (`Product.ts`), actions (`getProduct.ts`, `login.ts`), pure helpers (`computeTotal.ts`), typed error classes                                                           | React, JSX, hooks, framework imports, URLs, header names, formatting meant for humans |
| `src/view/`           | One folder per feature, each with `components/`, `hooks/`, `pages/`, `providers/`, `views/`, plus `SerializedX.ts` and form schemas. Shared UI in `view/general/`, cross-cutting concerns in `view/styling/`, `view/routing/`, `view/utils/` | API URLs, response parsing, business rules that other surfaces would need             |
| `src/pages/`          | Routing only: the data fetch, the serialize call, the provider, the view page. Server-side auth redirects                                                                                                                                    | Anything a second route might also want to do                                         |

### Deciding where a piece of code goes

Ask, in order:

1. **Does it know a URL, a header, a cookie name, or the literal shape the server returns?**
   → `infrastructure/`.
2. **Would it still be true if this app were a CLI?** Is it a rule, a computation, a
   validation, a state transition, or a translation from API shape to app shape?
   → `domain/`.
3. **Does it need a React hook, JSX, viewport size, or human-facing copy?** → `view/`.
4. **Is it only about which URL renders what, and what has to happen on the server before
   the first render?** → `pages/`.

The most common mistake is answering 3 when the honest answer is 2. "Can the user check out
yet?" _feels_ like a view question because a button's `disabled` prop consumes it. It is a
domain question with a React consumer.

## Dependency rules

Imports point downward. Three refinements matter more than the arrow:

1. **Infrastructure may import domain _types_, never domain _behavior_.** An endpoint
   function legitimately takes an `AccessToken` or returns data typed by a shared model.
   The moment infrastructure _calls_ a domain action, the layering has inverted and the
   rule now depends on the transport.
2. **Domain imports nothing from view or React.** Not `useMemo`, not a formatter, not a
   constant that lives in `view/`. A domain function that needs a currency string is a
   domain function that has taken on a view concern — return the number and format it in
   the view.
3. **View reaches into infrastructure only for browser state that is not HTTP** — reading
   and writing the auth cookie, essentially. Anything network-shaped goes through a domain
   action, so that the view never sees a raw API response.

Routes may touch infrastructure directly for the same narrow reason: reading the auth cookie
server-side to guard a page.

## The patterns

Each has a reference file with full code. Read the one you need — do not read all four.

**`references/vertical-slice.md`** — how one feature is built end to end: the endpoint
function and its colocated response schema, the domain action that normalizes the response,
the serialization boundary (`SerializedX.ts`, because domain types carry real `Date` objects
while route props must be JSON), the initial-data hook ladder (`InitialXProvider` →
`useInitialX` → `useX` → `useGuaranteedX` → `useSelectedX`), and the thin route that ties
them together. Read this for almost any feature work.

**`references/state-and-flows.md`** — multi-step flows modeled as a discriminated union on
`step` with a type guard (`flowIsAtStep`) and a hook that throws when a component is mounted
at the wrong step (`useFlowAtStep`), so a step's components can assume the data that step
guarantees. Also: provider conventions, and where form schemas live so that one rule guards
a field, a payload, and a test.

**`references/errors.md`** — the error strategy end to end: infrastructure throws and does
not interpret, the domain captures the failures it expects and rethrows a typed error
carrying a machine-readable `reason`, and the view maps that `reason` to copy through an
exhaustive record. Also the deliberately non-blocking policy on response schemas.

**`references/helpers.md`** — copy-paste implementations of the generic helpers the other
files use (a typed selective `catch`, a typed error-class factory, two type utilities), so
adopting this architecture requires installing nothing.

## Naming and file conventions

- **One concept per file, file named after it.** `Product.ts` exports the `Product` type;
  `getProduct.ts` exports `getProduct`. Endpoint files additionally export their response
  schema and inferred response type, which is the same concept viewed three ways.
- **Named exports everywhere.** Default exports only where the framework requires them
  (route components, API handlers).
- **No barrel files.** Import from the defining module. Barrels obscure the dependency
  graph, which is the thing this architecture is trying to keep legible.
- **Hooks are `useX`, providers are `XProvider` in `providers/`, props types are `XProps`.**
- **Route params get their own hook** (`useProductIdFromSlug`) that throws if the param is
  missing or not a string, so every consumer downstream gets a plain `string`.
- **When a name needs to be re-exported across the layer boundary, alias it:**
  `import { getProduct as infraGetProduct }` inside `domain/product/getProduct.ts`. Keeping
  both names makes the delegation visible.

## Review checklist

Run through this on a diff before calling it done:

- [ ] No `fetch`, HTTP client call, or URL string outside `infrastructure/endpoints/`.
- [ ] No raw API field (`snake_case`, `image` where the app calls it `imageUrl`) reaching a
      component — the domain action normalizes it.
- [ ] No conditional in JSX that is really a rule. If it needs a comment to explain _why_,
      it wants a named domain function.
- [ ] Domain files import no React, no framework modules, nothing from `view/`.
- [ ] Infrastructure imports domain types only, never domain actions.
- [ ] New domain types containing `Date` (or any non-JSON value) have their `SerializedX`
      updated on both sides, and the route memoizes the deserialize.
- [ ] Errors surfaced to users go through a typed `reason`, mapped exhaustively — not
      `error.message` rendered raw, and not a stringly-typed `if (message.includes(...))`.
- [ ] New pure domain logic has a colocated test. This is the layer where tests are cheap;
      skipping them here is skipping them where they pay best.
- [ ] Route files stay thin: fetch, serialize, provide, render.
