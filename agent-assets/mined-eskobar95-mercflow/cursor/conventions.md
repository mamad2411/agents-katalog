---
description: Code conventions, commit discipline, and PR workflow for MercFlow. Always apply this rule.
globs: ["**/*"]
alwaysApply: true
---

# Conventions — Code, Commits, and Pull Requests

---

## Code Conventions

### TypeScript

- Strict mode is enabled. No exceptions.
- Never use `any`. Use `unknown` + type narrowing, or extend types properly.
- Prefer `type` over `interface` for data shapes. Use `interface` only when extension via `extends` is the intent.
- All functions must have explicit return types unless the type is trivially inferred (e.g., a one-liner arrow function returning a primitive).
- No barrel re-exports at the top level of a package unless explicitly needed for the public API (`index.ts`).

### Imports

Order imports in this sequence, separated by a blank line:

```ts
// 1. Node built-ins
import path from "path"

// 2. Third-party packages
import { useState } from "react"
import { MedusaError } from "@medusajs/utils"

// 3. Internal packages (workspace)
import { tokens } from "@mercflow/design-tokens"

// 4. Local imports (relative)
import { ProductContentTab } from "./ProductContentTab"
import type { ProductContentFields } from "./types"
```

Use path aliases over deep relative imports:

```ts
// ❌ Avoid
import { Button } from "../../../components/ui/Button"

// ✅ Prefer
import { Button } from "@/components/ui/Button"
```

### Naming

| Thing | Convention | Example |
|---|---|---|
| Files: components | PascalCase | `ProductContentTab.tsx` |
| Files: utilities/hooks | camelCase | `useProductContent.ts` |
| Files: types | PascalCase | `ProductContentFields.ts` |
| Variables / functions | camelCase | `const seoTitle` |
| Constants | SCREAMING_SNAKE | `const MAX_SEO_DESCRIPTION_LENGTH = 160` |
| React components | PascalCase | `function ProductContentTab()` |
| Database columns | snake_case | `seo_description` |
| API route params | snake_case | `/products/:product_id` |

### Error handling

Use Medusa's `MedusaError` in service layer. Never throw raw `Error` objects from services.

```ts
// ✅ Correct
throw new MedusaError(MedusaError.Types.NOT_FOUND, `Product content not found for product ${productId}`)

// ❌ Wrong
throw new Error("Not found")
```

In the UI, always handle loading and error states explicitly. Never render nothing silently on error.

---

## Commit Discipline

### Commit format

MercFlow uses [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <short description>

[optional body]

[optional footer]
```

**Types:**

| Type | When to use |
|---|---|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `style` | Formatting, whitespace, token changes (no logic change) |
| `test` | Adding or updating tests |
| `chore` | Build process, dependency updates, config changes |
| `docs` | Documentation only |
| `migration` | Database migration (always use this type, never hide migrations in `feat`) |

**Scopes** (use the package or domain name):

```
feat(admin-ui): add SEO preview component to product content tab
fix(content-module): clamp seo_description to 160 characters in service
migration(content-module): add product_content table
chore(design-tokens): add surface-subtle token
```

### Commit size — the golden rule

**One commit = one logical change.**

A logical change is the smallest unit of work that leaves the codebase in a working, consistent state. Ask yourself: "If I had to revert only this commit, would the codebase still make sense?" If yes, the commit size is right.

**Examples of correct commit granularity:**

```
feat(design-tokens): add initial token system (colors, spacing, radius)
feat(admin-ui): add PageTransition wrapper component
feat(admin-ui): replace product modal with dedicated product page
feat(admin-ui): add product list view with sortable columns
migration(content-module): create product_content table
feat(content-module): add ProductContent model and repository
feat(content-module): add content service with upsert and fetch methods
feat(admin-ui): add content tab to product detail page
feat(admin-ui): integrate TipTap editor into product content tab
```

**Examples of commits that are too large — split these:**

```
❌ feat: add product content system
   (this touches migrations, service, UI, and types — split into 6+ commits)

❌ feat(admin-ui): redesign admin
   (this is an entire feature area — split by component/page)
```

### When to commit

Commit when:
- A component renders correctly and is self-contained (even if not yet wired up)
- A service method is implemented and has passing unit tests
- A migration file is created and verified locally
- A refactor is complete and tests still pass
- A bug is fixed and the fix is isolated

Do not commit:
- Broken code (TypeScript errors, failing tests)
- Half-implemented features mixed with unrelated cleanup
- Console.log statements left in for debugging

---

## Pull Request Workflow

### PR size — the golden rule

**One PR = one feature, one module, or one clearly scoped piece of work.**

A PR should be reviewable in under 30 minutes. If a PR takes longer than that to understand, it is too large.

**Target:** 200–400 lines changed per PR. Hard limit: 600 lines. If you are approaching 600 lines, stop and split.

### Branch naming

```
feat/product-content-model
feat/admin-product-content-tab
feat/page-transitions
fix/seo-description-length-validation
migration/add-product-content-table
chore/update-design-tokens
```

### When to open a PR

Open a PR when:
- A full vertical slice of a feature is complete (e.g., model + migration + service for product content — but not the UI yet)
- A standalone UI component is complete and documented
- A bug fix is isolated and tested
- A refactor of a single module or component area is complete

Do not wait until an entire feature (e.g., "the full content system") is done before opening a PR. Split by layer:

```
PR 1: feat/content-module-model-and-migration
PR 2: feat/content-module-service-and-routes
PR 3: feat/admin-product-content-tab
PR 4: feat/admin-category-content-tab
```

### PR description template

Every PR must include:

```markdown
## What
Short description of what this PR does.

## Why
Why this change is needed (link to PRD section if relevant).

## How
Brief explanation of the approach taken.

## Testing
How to verify this works locally.

## Notes
Anything the reviewer should be aware of (edge cases, follow-up work, known limitations).
```

### PR checklist before opening

- [ ] TypeScript compiles with no errors (`pnpm tsc --noEmit`)
- [ ] No `console.log` or debug statements left in
- [ ] Commit messages follow conventional commits format
- [ ] PR description filled out
- [ ] No unrelated changes included (if you found something to fix, make a separate PR)
- [ ] Migration files (if any) have been tested locally with `pnpm migration:run`

---

## Documentation Rules

### README placement — the golden rule

**A README belongs in the directory it describes.** Never aggregate package documentation into a central location.

```
mercflow/
├── README.md                    ← Project entry point only
├── packages/
│   ├── admin-ui/
│   │   └── README.md            ← admin-ui docs live here
│   ├── content-module/
│   │   └── README.md            ← content-module docs live here
│   └── design-tokens/
│       └── README.md            ← design-tokens docs live here
├── apps/
│   └── backend/
│       └── README.md            ← backend docs live here
└── docs/
    ├── PRD.md                   ← Non-technical project docs only
    └── ARCHITECTURE.md          ← Architecture decision records only
```

**`docs/` is strictly for:**
- PRD and product requirements
- Architecture decision records (ADRs)
- Roadmap

**`docs/` is never for:**
- Package-specific documentation
- API references
- Setup guides for individual packages

### When to create a README

When creating a new package or app directory, always create its `README.md` immediately — before writing any code. The README is part of the deliverable, not an afterthought.

### What each README must contain

**Root `README.md`:**
- What MercFlow is (2–3 sentences)
- Monorepo structure overview
- Prerequisites and getting started (install + run locally)
- Links to individual package READMEs

**Package READMEs** (`packages/*/README.md` and `apps/*/README.md`):
- Package responsibility (one paragraph)
- How to run and test in isolation
- Key conventions specific to this package
- What explicitly does NOT belong in this package (prevents scope creep)

**`packages/content-module/README.md`** must additionally include:
- All field definitions (kept in sync with the model files)
- API route reference
- Migration workflow (how to create, run, and roll back locally)

### Keeping READMEs up to date

If you add significant new functionality to a package, update that package's README in the same PR — not as a separate follow-up. A PR that adds a new feature without updating the README is incomplete.

Never create additional `.md` files inside a package directory unless they are explicitly needed (e.g., a `CHANGELOG.md`). All package documentation goes into the single `README.md`.

---

## Migration Environment Rules

Migrations behave differently depending on the environment. The agent must apply the correct rule for the current context.

### Local development (default context)

The agent operates freely. It may:
- Create new migration files based on the current task and PRD field definitions
- Run migrations (`pnpm migration:run`)
- Roll back migrations (`pnpm migration:revert`) if something needs to change
- Iterate on schema as needed

**Every migration file must include a decision log comment at the top:**

```ts
/**
 * MIGRATION DECISION LOG
 * Reason: <why this migration exists, with reference to PRD section>
 * Changes: <list of tables/columns added, modified, or removed>
 * Reversible: Yes — down() <describe what it does>
 * Fields derived from: content-module.mdc field definitions
 */
```

**Every migration commit must follow this format:**

```
migration(content-module): add product_content table

Fields: description_rich (jsonb), seo_title (varchar 255),
seo_description (varchar 160), seo_og_image_id (uuid nullable).
Reversible via down(). Decision log in migration file.
```

This provides full traceability without requiring the agent to stop and ask for approval on every field.

### Production / staging

Never run or generate migrations targeting a production or staging database without explicit written instruction from the user in the current task. If the agent is unsure which environment it is targeting, it must stop and ask before proceeding.

---

## Agent-specific Workflow

When the Cursor agent is running a task autonomously, it follows this commit rhythm:

1. **Complete one logical unit of work** (e.g., one component, one service method, one migration)
2. **Verify it compiles and tests pass**
3. **Commit immediately** with a conventional commit message
4. **Continue to the next logical unit**

The agent **never** accumulates multiple logical units before committing. Each commit should be usable as a safe restore point.

The agent **opens a PR** when it has completed a full layer of a feature (e.g., all service methods for the content module). It does not wait for the entire feature to be done.

If the agent is unsure whether something constitutes a PR boundary, it should stop and ask.
