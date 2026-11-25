---
name: content-stack
description: Database-backed content + i18n stack, `ContentPage` / `ContentString` Prisma models on MongoDB, `StringRole` enum, `Languages` embedded type, a public `getPageStrings` server fn cached forever in TanStack Query, a `useTranslation(pageSlug)` hook resolving by `(fallback, role, section)`, store-driven active locale (Redux / Zustand / etc.), an opt-in locale switcher, a `seed-translations` script as the source of truth, and a gated admin editor for live patches. Use when adding/editing copy on a page, wiring `useTranslation` into a new route, adding a new content page, enabling a new language, changing `StringRole`, touching `Languages`, persisting a per-user locale preference, or working on the translations admin UI.
---

# Content + i18n stack

All user-facing copy lives in MongoDB as `ContentString` rows grouped under `ContentPage` slugs. Every string carries one mandatory base-language value and optional translations; resolution falls back to the base language so the system runs **single-locale-first** and lights up additional locales as translations are filled in. The seed file is the source of truth, the admin UI exists to patch it, not to replace it.

> **Stack assumed.** Prisma + MongoDB (`relationMode = "prisma"`), TanStack Query v5, TanStack Start (or any framework that supports server functions), a client store for active locale (Redux / Zustand / Context, the patterns here use Redux as the example), and **the `auth-stack` skill** for `requireAuthenticatedUser` and the role predicate. Authoring runs through a TS script (any of `tsx` / `bun`/`ts-node` works).

> **Notation.** `<server>/lib/i18n/`, `<server>/lib/admin/`, `<server>/lib/queries/`, `<client>/hooks/`, `<client>/store/`, `<client>/components/`, `<routes>/`, `prisma/seed-translations.ts` are placeholders. Resolve to the project's actual paths and aliases. Helper names (`useTranslation`, `i18nQueries`, `i18nMutations`, `adminQueries`, `LocaleSelect`, `setLocale`, `selectLocale`, `requireAuthenticatedUser`, `isAdmin`) are suggested conventions, rename to match your project's style.

> **Precedence.** Project rules (ESLint / Biome / `tsconfig` / `CLAUDE.md` / `AGENTS.md` / contributing guides) win over this skill. Defer and note the deviation.

---

## Stack at a glance

| Concern              | Implementation                                                                   | Topic                                              |
| -------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------- |
| Data model           | `ContentPage` / `ContentString` + `StringRole` enum + `Languages` type           | [schema-and-server.md](schema-and-server.md)       |
| Read path (server)   | `getPageStrings` server fn, flattens `Languages` to `ResolvedString[]`          | [schema-and-server.md](schema-and-server.md)       |
| Read path (client)   | `i18nQueries.pageStrings({ pageSlug })` with `staleTime: Infinity`               | [client-and-locale.md](client-and-locale.md)       |
| Translate API        | `useTranslation(pageSlug)` → `t({ text, role, section })` or positional          | [client-and-locale.md](client-and-locale.md)       |
| Active locale        | Client store slice (`selectLocale`, `setLocale`)                                 | [client-and-locale.md](client-and-locale.md)       |
| Locale init          | App provider reads `authSession.user.preferredLocale` on mount                   | [client-and-locale.md](client-and-locale.md)       |
| Locale switcher      | `LocaleSelect` UI atom (store-only; doesn't persist)                             | [client-and-locale.md](client-and-locale.md)       |
| Persist preference   | `updateUserLocale` server fn → `User.preferredLocale`                            | [schema-and-server.md](schema-and-server.md)       |
| Authoring            | `prisma/seed-translations.ts`, declarative `pages` array, run via the TS runner | [workflows.md](workflows.md)                       |
| Admin editing        | Gated `/admin/translations` route, `upsertContentString` + `listContentPages`    | [workflows.md](workflows.md)                       |
| Adding a new locale  | 4 coordinated edits (Prisma type, locale list, resolver, switcher)               | [workflows.md](workflows.md)                       |

This skill assumes the [auth-stack](../auth-stack/SKILL.md) skill is in place, `requireAuthenticatedUser` and role narrowing come from there.

---

## Core principles

These are the **nine rules that span more than one topic file**. Topic-specific rules live in their respective files; this list is the cross-cutting contract.

### 1. The `fallback` field is both the base-language copy AND the lookup key

In JSX you write `t({ text: "Start your project", role: "action", section: "hero" })`. That literal string `"Start your project"` is the `fallback` column in the DB and the lookup key for the unique index `(pageId, fallback, role, section)`. Renaming the JSX string without updating the seed silently breaks the lookup, the resolver returns `args.text` (the new base copy) but loses every translation associated with the old key.

**Implication:** treat copy changes as schema-adjacent. Update the seed, re-seed, then update the JSX in the same change.

### 2. The base language is mandatory; every other language is optional and falls back

`Languages` in Prisma is `{ <base>: String, <other>: String?, <other>: String?, … }`. The resolver returns `match.<base>` whenever the requested locale's value is `null`. This is the seam that makes single-locale-first viable, you ship with the base language filled and translations land incrementally without breaking the UI.

In this doc, examples use `en` as the base language. Any language can play that role; pick one and make it the only non-nullable column in `Languages`.

### 3. The composite unique key is `(pageId, fallback, role, section)`, all four matter

You can have the same base-language string in two `section`s (`hero` vs `nav`) or two `role`s (`headline` vs `body`) and they're distinct rows. Use this on purpose: `section` is the visual region, `role` is the typographic intent. Don't bypass the constraint by appending markers to `fallback` (`"Submit (form)"`), split on `section` or `role` instead.

### 4. `i18nQueries.pageStrings` has `staleTime: Infinity`, content is treated as immutable

Once a page is fetched, TanStack Query never refetches automatically. After `upsertContentString` succeeds, the **admin** page invalidates `adminQueries.contentPages().queryKey`, but the **public** `i18nQueries` cache for that page slug stays warm for the session. Do not assume edits propagate live; a refresh is required outside the admin tab.

### 5. One server fn per read path; admin gate on writes

`getPageStrings` is public (no auth, anonymous landing-page visitors hit it). `updateUserLocale` requires `requireAuthenticatedUser` (from the auth-stack skill). `listContentPages` and `upsertContentString` require `requireAuthenticatedUser` **plus** an admin role check (`isAdmin(user.role)`). Never expose `upsertContentString` from a non-admin route, and never read raw `prisma.contentString` from a route module; go through the server fn.

### 6. Locale lives in the client store, persists via the User row, never in the URL

There are no `/en/...` / `/es/...` routes. The active locale is a single field in the client store, seeded from `authSession.user.preferredLocale` on mount and otherwise `DEFAULT_LOCALE`. The locale switcher dispatches the store action only; it does **not** call `updateUserLocale`. If a feature needs the choice to survive logout/refresh for a logged-in user, call the mutation explicitly.

This is opinionated, if your project needs URL-driven locales (for SEO, shareable links per locale), this stack is not for you; use a routing-driven i18n library instead.

### 7. The seed file is the source of truth, not the database

`prisma/seed-translations.ts` deletes every `ContentString` and `ContentPage`, then re-creates from the `pages` array. Edits made through the admin UI survive only until the next seed run. Treat the admin UI as a **hot-patch tool**; commit final copy back into the seed.

### 8. `StringRole` is metadata, not behavior

The role values exist for the admin UI's organisation and as part of the composite key. The translation engine **never branches on role**, it's just metadata. Adding a new role is a Prisma migration **plus** an entry in the runtime `VALID_STRING_ROLES` set, **plus** the TS string union, three places, must stay in sync.

### 9. Resolution is synchronous and client-side

`getPageStrings` returns all locales' values flattened (`{ en, es, … }`). The client picks one based on store state. Switching locale is a single store dispatch, no refetch, no flicker, no SSR roundtrip. **Don't** try to filter by locale on the server; the round-trip would defeat the cache and break instant locale switches.

---

## Workflow checklist

Before merging changes that touch this stack:

- [ ] Every new visible string is in `prisma/seed-translations.ts` under the right `pageSlug`.
- [ ] Every new string has a non-empty base-language value; other languages either filled or omitted (null).
- [ ] `(pageSlug, fallback, role, section)` tuples are unique within their page.
- [ ] Component calls `useTranslation(pageSlug)` once, near the top of the component.
- [ ] JSX uses `t({ text, role, section })`; the `text` argument matches `fallback` verbatim.
- [ ] No new `prisma.contentString` calls outside `<server>/lib/i18n/` and `<server>/lib/admin/`.
- [ ] If adding a `StringRole` value: Prisma enum, TS union, `VALID_STRING_ROLES` set, `prisma db push`, `prisma generate`, restart dev.
- [ ] If adding a new locale: see [workflows.md § Adding a language](workflows.md), 4+ coordinated edits.
- [ ] Seed runs cleanly against your dev DB.
- [ ] Admin route still loads (gated to admin role).
- [ ] Lint, typecheck, and tests clean.

---

## Reference files

- [schema-and-server.md](schema-and-server.md), Prisma `ContentPage` / `ContentString` / `StringRole` / `Languages`, the four server fns (`getPageStrings`, `updateUserLocale`, `listContentPages`, `upsertContentString`), and how each enforces (or skips) auth.
- [client-and-locale.md](client-and-locale.md), `i18nQueries.pageStrings`, `useTranslation` resolution algorithm, the locale store slice, app-provider locale init, `LocaleSelect` semantics, `i18nMutations.updateUserLocale`.
- [workflows.md](workflows.md), Adding a string, adding a page, editing via admin UI, re-seeding safely, and the recipe to enable a new language.
