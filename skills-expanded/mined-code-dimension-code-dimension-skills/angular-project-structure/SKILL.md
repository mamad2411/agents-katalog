---
name: angular-project-structure
description: "Project folder and file structure conventions. USE WHEN creating any new resource (component, service, directive, pipe, guard, interceptor, module, layout, util, etc.), deciding where a file belongs, creating feature modules or wiring lazy-loaded routes, importing across layers, or asked 'where do I put X?' / 'how should this be structured?'."
metadata:
  author: code-dimension
  version: 1.0
---

# Angular Project Structure

A mold for organizing every resource in the project: three layers, one naming pattern. Apply it to **any** kind of resource — the pattern is not limited to components, services, or directives.

## The mold

Every file lives at:

```
<layer>/<resource-name>/<slice>/<name>.<type>.{ts|html|css|scss}
```

- `<layer>` — `core/`, `features/`, or `shared/`. These are the only root-level folders for application code.
- `<resource-name>` — the resource being built (e.g. `checkout`, `http`, `ui`).
- `<slice>` — a sub-domain of the resource that groups related files (e.g. `cart/`, `payment/`, `interceptors/`).
- `<name>.<type>` — file name is `<name>.<type>.<ext>`. `<type>` is free-form: component, service, directive, pipe, guard, interceptor, resolver, layout, util, anything. `.ts` is always present; add `.html` / `.css` / `.scss` for templates and styles.

Examples of the mold in practice:

```
features/checkout/cart/cart.component.ts|html|scss
features/checkout/payment/payment-form.component.ts
features/checkout/payment/payment.service.ts
core/http/interceptors/auth.interceptor.ts
core/layout/base/base-layout.component.ts|html|scss
shared/ui/pipes/currency.pipe.ts
```

The single documented exception: a feature's route file sits at the feature root — `features/<feature-name>/routes.ts` — not inside a slice. See [routing.md](./references/routing.md).

## Layers

| Layer | Purpose |
|---|---|
| `core/` | Resources used at bootstrap or in `app.{ts\|html}`: HTTP interceptors, app initializers, global error handlers, base/root layouts, app config. Nothing URL-addressable lives here. |
| `features/` | Pages and modules of the application. Each module owns its routes (`routes.ts`) and sub-routes. Modules are the unit of scope. |
| `shared/` | Resources reused across features: UI widgets, pipes, generic services, helpers. |

### features/ — modules and scoping

- An app has many modules (e.g. customers, payments, reports), each with its own sub-routes.
- Every URL-accessible component inside a module gets a route **within that module's `routes.ts`** — never a new root-level folder in `features/`.
- When a resource escapes the scope of its module, create **another module** that fits that scope — do not widen the current module and do not add a root folder.

### shared/ — reuse with care

- Shared resources are consumed by features. A shared resource may occasionally use another shared resource, but avoid it: chained shared-to-shared imports are how circular dependencies start. If two shared resources are entangled, they are probably one resource.

## Dependency rules

| From | May import | Must not import |
|---|---|---|
| `core/` | other `core/` resources | `features/`, `shared/` |
| `shared/` | `core/`; other `shared/` resources (avoid) | `features/` |
| `features/` | `core/`, `shared/` | other `features/` modules |

```
features ──▶ shared ──▶ core
   │                      ▲
   └──────────────────────┘
   core imports nothing outside core
```

- `features → features` is forbidden. If two features need the same resource, move it to `shared/` or extract a new module (see [routing.md](./references/routing.md)).
- `core` is self-contained: it may depend on other core resources, but never on `shared/` or `features/`.

## Decision checklist — "where do I put X?"

1. Used at bootstrap or rendered by `app.{ts|html}`? → `core/`
2. Reachable via URL, or a page/module of the app? → `features/` (create a module if none fits)
3. Used by two or more features (or plausibly reusable)? → `shared/`
4. Inside a feature but needed outside its scope? → new module in `features/` (behavior/route) or `shared/` (generic piece)
5. Never invent new root-level folders; never place files outside `resource/slice/`.

## References

- [structure.md](./references/structure.md) — full example trees, naming details, correct vs incorrect layouts.
- [routing.md](./references/routing.md) — `routes.ts` patterns, lazy loading, sub-routes, and module extraction rules.