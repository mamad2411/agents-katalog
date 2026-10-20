---
description: Global project context for MercFlow. Always apply this rule.
globs: ["**/*"]
alwaysApply: true
---

# MercFlow — Project Context

## What is MercFlow?

MercFlow is an opinionated Medusa v2 distribution. It is a fork of the Medusa admin UI and a set of Medusa modules that together deliver:

- A redesigned admin UI (Shopify-inspired: light, clean, spacious)
- Page-based navigation replacing modal-heavy flows
- Native content fields (rich text, SEO, media gallery) on Product and Category entities
- An intuitive i18n editing flow for multilingual catalogs
- Improved list views across the admin panel

MercFlow is built with Guapo (guapo.store) as the first use case, but is designed from day one to be used by other Medusa-based shops.

**MercFlow is not:**
- A Shopify clone
- A headless CMS replacement (it brings CMS capabilities into Medusa, not the other way around)
- A plugin — it is a distribution (fork + modules)

---

## Repository Structure

```
mercflow/
├── packages/
│   ├── admin-ui/          ← Forked and redesigned Medusa admin
│   ├── content-module/    ← Native content fields as a Medusa module
│   └── design-tokens/     ← Shared design token system (CSS vars + Tailwind config)
├── apps/
│   └── backend/           ← Medusa v2 backend with MercFlow modules registered
├── docs/
│   ├── PRD.md
│   └── ARCHITECTURE.md
└── .cursor/
    ├── rules/
    └── agents/
```

### Package responsibilities

| Package | Responsibility |
|---|---|
| `packages/admin-ui` | All admin UI components, pages, routing, and styling |
| `packages/content-module` | Medusa module: content fields, migrations, service, API routes |
| `packages/design-tokens` | Single source of truth for colors, spacing, typography, radius |
| `apps/backend` | Medusa backend — registers MercFlow modules, no custom logic here |

---

## Technology Stack

| Layer | Technology |
|---|---|
| Backend runtime | Node.js + Medusa v2 |
| Database | PostgreSQL (via MikroORM) |
| Admin UI framework | React 18 + Vite |
| Component primitives | Radix UI |
| Styling | Tailwind CSS (token-driven) |
| Rich text editor | TipTap v2 |
| Language | TypeScript (strict mode throughout) |

---

## Hard Rules — Never Violate These

These are non-negotiable. Stop and ask the user before proceeding if any of these applies.

1. **Never modify Medusa core packages directly.** All changes go into MercFlow packages. If a core behavior needs to change, extend or override it — never edit files inside `node_modules` or Medusa's own source files.

2. **Never create a database migration without an explicit instruction.** Migrations are irreversible in production. Always confirm the field definitions are final before generating a migration file.

3. **Never use `any` in TypeScript.** If a type is unknown, use `unknown` and narrow it. If a third-party type is missing, extend it properly.

4. **Never hardcode design values.** Colors, spacing, font sizes, border radii — always use design tokens from `packages/design-tokens`. No inline hex values, no arbitrary Tailwind values unless explicitly approved.

5. **Never delete or overwrite a file you did not create in the current task.** If an existing file needs to change, edit it in place and explain the change in the commit message.

6. **Never touch Guapo production config, credentials, or environment variables.** MercFlow is a separate project. Guapo-specific configuration lives in a separate repo.

---

## When to Stop and Ask

Stop immediately and ask the user for clarification when:

- You are about to make a decision that affects the public API contract (field names, route paths, response shapes)
- You are unsure whether a new component belongs in `admin-ui` or should be a shared primitive in `design-tokens`
- A task requires a database migration and the field definitions have not been explicitly confirmed
- You encounter a conflict between two existing patterns in the codebase and cannot determine which is canonical
- A task is underspecified and two reasonable interpretations would lead to meaningfully different implementations

When in doubt: stop, describe what you found, propose two options, and ask which to proceed with.
