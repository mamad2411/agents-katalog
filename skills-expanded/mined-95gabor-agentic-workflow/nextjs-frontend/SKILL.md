---
name: nextjs-frontend
description: >-
  Optional stack skill: Next.js App Router UI (pages, forms, Tailwind, API
  client). Use when working in the Next.js app path from project-context.
---

# Next.js Frontend (optional)

Enable this skill when the project uses Next.js. Paths and package filters come from `.agents/skills/project-context/SKILL.md`.

Also read `.agents/skills/typescript/SKILL.md` and `.agents/skills/clean-code/SKILL.md`.
For landing metadata, sitemap, GTM, and Lighthouse: `.agents/skills/seo/SKILL.md`.

## Stack (typical)

- Next.js App Router, TypeScript, Tailwind CSS
- Common location: `apps/web/`
- Package filter example: `@your-scope/web`

## UI language

- **End users:** language from `project-context`.
- **Developers:** English code, comments, and docs.

## Conventions

1. **Data-driven UI** — Prefer API/catalog-driven forms over hardcoding option lists when content is domain data.
2. **Forms** — Multi-step wizards with partial save where product requires; validation messages in UI language.
3. **Server vs client** — Prefer Server Components for static content; Client Components for interactive flows.
4. **API client** — Centralize fetch in `lib/`; typed responses where possible.
5. **Admin** — Protected routes; auth flow only for authorized users.
6. **Test IDs** — Add `data-testid` to key interactive and assertion targets for E2E.

## Test IDs (`data-testid`)

Stable test hooks for Playwright and component tests. **English kebab-case** — not translated.

### When to add

| Add `data-testid`                        | Skip                               |
| ---------------------------------------- | ---------------------------------- |
| Primary/secondary CTAs, submit/next/back | Decorative wrappers                |
| Form inputs and field groups             | Every list item unless asserted    |
| Wizard step containers, progress         | Framework internals unless exposed |
| Error/empty/loading states               | Static marketing paragraphs        |

**Naming:** `{area}-{context}-{element}` (e.g. `landing-hero-cta`, `wizard-profile-next-button`).

Recommend a central registry (e.g. `src/lib/test-ids.ts`) shared conceptually with E2E page objects.

### Implementation rules

1. One test id per logical target in a view.
2. Put on the interactive or assertable node.
3. Do not use test ids for styling.
4. Do not remove existing test ids without updating E2E in the same change.

## Checklist before finishing

- [ ] User-facing strings match UI language from `project-context`
- [ ] Loading and empty states for data tables/lists
- [ ] Environment-based API base URL for local vs Docker
- [ ] Landing/public routes: metadata per `seo/SKILL.md` when touched
- [ ] Key interactives have `data-testid` (new/changed flows)
- [ ] Lint passes for the web package
- [ ] Tests added; all pass (see `developer-quality`)
