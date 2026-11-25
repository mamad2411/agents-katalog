---
name: tanstack-start-ssr
description: Use when adding or changing a screen, route, loader, server function or data read in apps/web or apps/admin. Covers which half of the application a piece of work belongs to, hydration versus seeding an atom, why every server function is a GET, the one boundary at the root, createServerOnlyFn, and the trap where a control looks live and does nothing.
---

# A GET is rendered on the server; a write happens on the client

A dashboard that fetches after hydration shows a spinner for work the server could already
have done. So a read a route can name is a **route loader**, and what stays in the browser
is what a person asks for: creating, editing, deleting, and the refetch that follows.

It is one query either way. `contactsAtom` is still what the screen reads, still what a
write invalidates, and still what `apps/mobile` renders with no server behind it — the
loader only arranges for it to arrive already full.

## Three pieces

1. **`server/rpc.ts`** — the RPC client as the server uses it. The cookie is **read inside
   `serverRpc`**, never passed in: it was a parameter at every call site once, which made
   the one thing that must never be forgotten into one somebody could pass wrong. Only the
   cookie goes; a whole header set sends `host` and `content-length`, which describe the
   request rather than the caller.
2. **`server/reads/`** — one file per concern. `apps/admin/src/server/` splits the same
   way, because one file holding the authentication _and_ every read is the one that grows
   a procedure somebody forgot to put `requireStaff` in front of.
3. **The atom** — `Atom.serializable({ key, schema })` declared in `packages/core` beside
   the atom, because the server needs the same pair to encode and a pair kept twice drifts
   into hydrating nothing while the page quietly fetches again.

## Server functions are GET only

`tooling/test/server-functions.test.ts` enforces it. The rule is invisible at the call
site — `createServerFn({ method: "POST" })` reads perfectly well and says nothing about
which half of the application it belongs to. A write is a form on the client, and the RPC
behind it is already authenticated by `AuthMiddleware`.

## Hydration, not seeding

`useAtomInitialValues` looks like the tool and is not: it marks the node **valid**, so the
atom never builds a lifecycle and a mutation that invalidates its reactivity key has
nothing to refresh. The table showed the server's rows and then ignored every write,
intermittently, because which of the seed and the first fetch won was a race.

`Hydration` _preloads_ the encoded value through `registry.setSerializable`; the node
collects it when it builds. The atom has the server's data and is still live.

## One boundary, at the root, above the shell

`HydrationBoundary` applies a value immediately only for an atom with **no node yet**; for
one that already exists it defers to an effect, and an effect never runs during SSR. The
app shell reads atoms of its own and renders before the child route, so a boundary inside a
route arrived too late for exactly those. `useHydratedMatches` collects every matched
route's data above the shell.

A loader may return one dehydrated read or a list of them.

## The traps, all three of which shipped once

- **A server-rendered control that only runs a handler is dead until React attaches.** It
  looks live in the markup and does nothing, silently. `useHydrated` disables it until
  hydration — which is also the one signal a browser test can wait on. Forms do not need
  this: effect-form does not render its fields during SSR at all.
- **A signal that works by coincidence stops working.** The Upload button encoded
  "not hydrated" _by accident_ because it was disabled until permissions arrived; server
  rendering the identity made it enabled from the first byte and the suite went red.
- **A server-only import pulls a module toward the client.** `currentStaff` was a plain
  function reaching `pg`, and TanStack Start's import protection refused the admin bundle —
  correctly; a Postgres driver in a browser bundle is a connection string looking for
  somewhere to leak. `createServerOnlyFn` says to the bundler what was previously
  convention.

## Testing a server-rendered read

The router serialises every loader's result into the document, so the data is in the HTML
whether or not anything rendered it. A test that asserts on raw text passes while the
server emits the empty state. **Strip `<script>` blocks first** — and HTML comments too,
because React separates adjacent text nodes with `<!-- -->`, so `1<!-- --> of <!-- -->3`
does not contain `1 of 3`.

## Where to look

- `apps/web/src/server/` — `rpc.ts`, `hydration.ts`, `reads/README.md`
- `apps/web/src/routes/__root.tsx` — the single boundary
- `packages/core/src/atoms/` — one file per feature, each with its serial pair
