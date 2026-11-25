---
name: micro-frontends
description: Decides whether micro-frontends are worth it and, if so, designs them - composition approach (separate apps per route, build-time packages, Module Federation, import maps, single-spa, Web Components, iframes, server or edge composition), shared dependencies and version skew, routing ownership, cross-app contracts, CSS isolation, auth, failure isolation, independent CI/CD and per-app observability. Use when splitting a large frontend across teams, adopting or debugging Module Federation or single-spa, migrating a legacy frontend incrementally, or reviewing a micro-frontend architecture. Not for small single-team apps.
license: MIT
---

# Micro-Frontends

Micro-frontends solve an organizational problem: many teams that must ship one product independently. They add runtime complexity, duplicated code and integration risk. Adopt them only when independent deployment is worth that cost, split by business domain, and keep the contracts between apps small, explicit and versioned.

## Decide first

| Signals for | Signals against |
|---|---|
| Several teams on one frontend block each other's releases | One team, or a handful of developers |
| Clear business areas with owners (search, checkout, account) | Most features cut across all areas |
| Incremental migration off a legacy framework (strangler pattern) | The real pain is slow builds or CI (fix with monorepo caching: Nx, Turborepo) |
| Areas need different release cadences or risk profiles | The goal is "let each team pick a framework" for preference |

The default alternative is a **modular monolith**: one deployable app with enforced module boundaries (lint rules, package `exports`, Nx module boundary rules), code ownership files, and a fast shared CI. If the user asks for micro-frontends without these signals, state the tradeoffs and confirm before building.

## Workflow

1. **Confirm the case** with the table above. Write down which teams own which areas.
2. **Split vertically by domain.** Each micro-frontend (MFE) owns a route or page area end to end, ideally with its own backend or BFF. Avoid horizontal splits ("header team", "button team"); the only shared horizontal pieces are the shell and the design system.
3. **Choose the simplest composition that works** (table below). Start with separate apps per route; add runtime composition only where one page must mix UI from several teams.
4. **Define the contracts**: routes each MFE owns, mount API (props in, events out), shared singleton dependencies and their version range, events and their payloads.
5. **Build the shell** (keep it thin), then one MFE end to end, including its independent pipeline, before adding the rest.
6. **Add resilience, observability and contract tests** before the second team goes live.

## Composition options

| Approach | Independent deploy | Isolation | Cost | Best for |
|---|---|---|---|---|
| Separate apps per route behind a reverse proxy or CDN path rules | Yes | Full (separate pages) | Full page loads between areas; shared header duplicated | The default first step; areas rarely share a page |
| Build-time packages (npm workspace packages) | No; host must rebuild | None | Simple | Shared libraries and design systems, not true MFEs |
| Runtime Module Federation (webpack, Rspack, Vite plugins) | Yes | Low (same JS realm and CSS) | Shared-dependency negotiation, version skew | Same-framework teams composing within one page |
| Import maps + native ES modules (often with single-spa) | Yes | Low | You manage shared deps via the import map | Framework-agnostic setups |
| single-spa (orchestrator with mount/unmount lifecycles) | Yes | Low | Extra framework and lifecycle wiring | Mixed frameworks during a migration |
| Web Components (custom elements, Shadow DOM) | Yes, if loaded at runtime | CSS isolation via Shadow DOM | SSR, forms and theming need care | Framework-neutral widgets embedded by many hosts |
| iframes | Yes | Strongest (security, CSS, JS) | Focus, accessibility, deep links, resizing and performance are harder | Third-party or untrusted content, legacy apps |
| Server or edge composition (SSI, ESI, fragment services) | Yes | Medium | Server infrastructure; client interactivity per fragment | Content-heavy, SEO-critical pages |

See [references/decision-matrix.md](references/decision-matrix.md) for a scored comparison and a strangler migration plan, and [references/module-federation.md](references/module-federation.md) for Module Federation setup.

## The shell (host)

Responsibilities: top-level routing, authentication bootstrap, global layout and navigation, loading and mounting MFEs, error boundaries and fallbacks, telemetry setup, feature flags. It holds no business logic. Changes to the shell should be rare, because every team depends on it.

## Shared dependencies and version skew

- Share only the framework runtime (for example `react` and `react-dom`) and the design system as singletons. Two copies of React on one page break hooks ("Invalid hook call").
- Publish a platform-wide supported version range for shared singletons. Upgrading a framework major version is a coordinated event, or the shell supports both through an adapter during the transition.
- Don't share business libraries or state libraries at runtime. Version them as packages; each MFE bundles its own copy.
- Track duplicate bytes per page; set a budget for them.

## Routing

- The shell owns top-level path prefixes (`/checkout/*`); each MFE owns everything under its prefix.
- There is one browser history. MFEs navigate through the shell's navigation API or standard links, never with their own competing top-level router instance.
- Deep links must work on reload: the server or CDN routes every prefix to the shell (or to the owning app).

## Communication contracts

In order of preference:

1. **The URL** (route and query params).
2. **Props or attributes** passed by the host at mount time.
3. **DOM `CustomEvent`s** with namespaced, versioned names and typed payloads.
4. **A small message bus owned by the shell**, only if the above are not enough.

```ts
// contracts package: versioned, types only, owned jointly
export const CART_ITEM_ADDED = "cart:item-added:v1";
export type CartItemAdded = { sku: string; quantity: number };

// producer (product MFE)
window.dispatchEvent(
  new CustomEvent<CartItemAdded>(CART_ITEM_ADDED, { detail: { sku, quantity: 1 } })
);

// consumer (cart MFE): subscribe on mount, unsubscribe on unmount
const onItemAdded = (event: Event) => {
  const { sku, quantity } = (event as CustomEvent<CartItemAdded>).detail;
  addToCart(sku, quantity);
};
window.addEventListener(CART_ITEM_ADDED, onItemAdded);
// on unmount: window.removeEventListener(CART_ITEM_ADDED, onItemAdded);
```

Never: a shared global mutable store across MFEs, reaching into another MFE's DOM or internals, or importing another MFE's source code.

## Styling and design system

- The design system is a versioned package; tokens are CSS custom properties set by the shell, so theming works everywhere.
- Only the shell sets global styles (resets, fonts, body). MFEs scope their CSS: CSS Modules, a per-MFE class prefix, cascade layers, or Shadow DOM.
- Avoid several runtime CSS-in-JS engines competing on one page.

## Auth and session

- The shell handles login; the session lives in an `httpOnly`, `Secure`, `SameSite` cookie on the shared site, so MFEs call APIs through the same origin or a BFF.
- Never pass tokens in URLs, `window` globals or `localStorage` shared across MFEs.
- MFEs handle `401` by calling the shell's API (redirect to login), not by each implementing its own login.

## Performance

- Lazy-load each MFE by route; preload the remote entry for likely next routes.
- Avoid waterfalls (shell → remote entry → chunks → data). Start data fetching in parallel with code loading.
- Set a per-MFE JavaScript budget and a total page budget; duplicated dependencies count against it.

## Resilience

- Wrap every remote load in a timeout, an error boundary and a fallback UI. The shell and the other MFEs must keep working when one remote is down.
- Deploy remotes as immutable versions and map MFE → URL in a runtime manifest per environment, so rolling back one MFE is a config change.

## Delivery

- Each MFE has its own pipeline: build, test, deploy and roll back alone.
- Hashed chunks are cached as `immutable`; the remote entry file or manifest is served with `no-cache` so hosts pick up new versions.
- Contract tests: the contracts package is type-checked by every consumer, and each MFE has tests for its mount API and events.
- Run an integrated end-to-end smoke test of the shell with the latest MFEs in staging before production, and canary releases per MFE.
- Ask before changing production routing, manifests or CDN rules; these affect every team.

## Observability

- Tag every error, log and RUM event with the MFE name and version (a release per MFE in the error tracker).
- Measure load time and failure rate per remote.
- Propagate trace IDs from the frontend to backend calls.

## Anti-patterns

- **Micro-frontends for one team**: all the costs, none of the benefits.
- **Horizontal splits** by component type instead of business domain.
- **Shared global store** coupling MFEs at runtime.
- **Multiple framework versions loaded on one page** by accident; no singleton policy.
- **A thick shell** full of business logic that every release depends on.
- **Mutable remote URLs with long cache times**, so users run mismatched versions.
- **No fallback** when a remote fails, so one team's outage blanks the whole page.
- **Integration only in production**: no staging composition test.

## Done when

- The decision is justified by team and domain signals, and recorded (an ADR).
- Each MFE owns its routes, builds and deploys independently, and can be rolled back alone.
- Shared singletons and their version range are documented and enforced.
- Contracts are versioned and type-checked by consumers.
- The shell degrades gracefully when any remote fails to load.
- Errors and performance are reported per MFE and version.

## References

- [references/decision-matrix.md](references/decision-matrix.md) — read when choosing between composition approaches, or planning an incremental migration from a legacy frontend.
- [references/module-federation.md](references/module-federation.md) — read when setting up or debugging Module Federation (host and remote config, shared singletons, async boundary, types, common errors).
