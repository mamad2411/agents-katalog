---
name: use-code-shape
description: >
  The SHAPE the code of this project must keep, and the eighteen build-time validators that enforce it
  instead of trusting anyone's memory. Load it before writing a route, an API door, a component that
  is growing, a database table, or anything that moves on screen — and whenever a gate refuses your
  work and you are about to "work around" it. The rules here are not style: each one is a limit that,
  when crossed, produces a defect nothing else reports — a page silently recomputed on every request,
  an API door open to guests, a table that exists on one machine, a crawler served an empty box. The
  central law: NO page in this project is dynamic, including the ones whose data is.
---

# use-code-shape

> Informational, not binding. **Know a better way for the case in front of you — do it your way and
> say so.** You are trusted with the creative work on this project.

**A limit is not advice.** When one is reached you stop and restructure — not later, not after this
feature. And a limit nobody can measure is a wish, so nearly every rule below has a validator that
refuses the build.

## 1. 🔒 The project has no dynamic pages — that is the target, and it is nearly reached

Not "public pages are static and the rest is free". A page whose DATA is dynamic still ships as a
**static shell**; the dynamic part wakes up inside it — an island, a fetch to `/api/*`, a widget under
`_widgets/dynamic/`. The shell is prerendered, the movement happens afterwards.

**Five** lines take a page — and with a layout, the whole subtree — out of the prerender, and each
is one line long:

| Line | Effect | Instead |
|---|---|---|
| `cookies()` in a page or layout | the entire subtree recomputes per request | an island asks after hydration; `/api/*` decides the right |
| `headers()` there | the same | the same |
| `export const dynamic = 'force-dynamic'` | the same, but out loud | `export const revalidate = N` when data ages |
| `export const revalidate = 0` | the same, written as a number | any `revalidate` **greater than zero** |
| `auth()` in a public page or layout | reading the session makes the route dynamic | the island asks `/api/me` after hydration |

Two more kill something worse than the route — they kill the CONTENT:

- **`"use client"` on `page.tsx`.** The browser owns the route; without JavaScript there is no page.
  Client components are fine anywhere else — a client component does not make a route dynamic.
- **`motion` imported into a server file.** It renders its `initial` state on the SERVER, so
  `initial={{opacity:0}}` ships `opacity:0` inside the prerendered HTML and the text exists only after
  hydration. Movement lives in a `*.client.tsx` island that swaps in over a printed static twin — see
  `ANTI-PATTERNS.md` №7 and `use-widgets`.

Under `sections/` both of the last two are refused outright: the section layer is server-side WHOLE, so
`"use client"` or `motion` anywhere in it fails the gate immediately.

`npm run check:static` refuses all seven, in `prebuild`. The second proof comes from another plane: the
route table after a build shows `●` for a static route and `ƒ` for a dynamic one. A gate reads causes;
the table reads the result — you want both.

**Whatever is not machine-checkable, say out loud instead of assuming.** Today the gate cannot tell an
expensive query from a cheap one, and it cannot prove a page works with JavaScript off. Those two are
checked by hand: read the served HTML for the content itself, and open the page with scripts disabled.

## 2. The validators, and what each one is actually for

Eighteen run inside `prebuild`, so a violation never reaches a deployment. Two do not run by themselves
and are the only thing standing between your edit and a failed build on the server, because you do not
build locally: **`npm run check:types` and `npm run check:i18n`**.

| Gate | Refuses |
|---|---|
| `check:static` | the seven above, plus a direct `@/lib/db` import from a public route folder — a subject has ONE reader in `lib/<subject>/`, shared by the page, the sitemap and the machine twin |
| `check:protected` | a protected layer that forgets `robots: { index: false }`; a session read in a layout; a permission group with no gate; an import from a sibling group; a `page.tsx` fatter than a thin entry; a widget outside `_widgets/{static,dynamic}/` |
| `check:api` | a route with no `// @api` name, or a name outside 6–12 words |
| `check:seo` · `check:aio` · `check:pwa` | the search, machine and installable surfaces — their own skills |
| `check:content` · `check:sections` · `check:links` | body rules, one specimen per section kind, dead links |
| `check:blocks-map` | a stale `BLOCKS.md` / `SECTIONS.json` — they are GENERATED (`npm run build:blocks-map`) and the panel reads the second one out of the slot |
| `check:project-types` | a project direction missing its words in a language of the corpus — `check:i18n` cannot read that shape, so it has its own guard |
| `check:i18n` | a missing interface string in an enabled language |
| `check:config-schemas` | a config key that exists in the type but not in the generated schema |
| `check:typography` · `check:layout` · `check:contrast` · `check:dialogs` | text through primitives, layout rules, contrast, one modal |
| `check:menu` | a menu entry pointing at a route the walk cannot reach |
| `check:encoding` | a control byte left where an accented letter was — the file still parses |
| `check:types` | what a local `npm run dev` will not tell you |

**Read `package.json` rather than trusting this table.** It is the authority: `prebuild` plus the
`check:*` scripts beside it. Two gates sat outside `prebuild` for weeks and were found only by
reading that file — a gate that has to be remembered is a gate that does not run.

🔒 **A red gate everybody has learned to ignore is worse than no gate.** `check:content` was red for six
routes and unnoticed because it was not in `prebuild`. If a gate is wrong, fix the gate in the same
change — never route around it.

## 3. Where things live

| Thing | Its only place | Why not elsewhere |
|---|---|---|
| middleware | `proxy.ts` — never `middleware.ts` | deliberate convention for Next 16/Turbopack; an empty `middleware-manifest.json` is not evidence of breakage |
| a guest-facing API door | its prefix in `PUBLIC_API_PREFIXES` (`proxy.ts`) | the gate closes `/api/*` whole; in bypass mode you cannot see it, so it breaks on the domain, at the customer |
| every table | the `SCHEMA` constant in `lib/db/index.ts` | both `makeLocalDb()` and `initRemoteSchema()` execute it, so local and server stay identical; there are no migration files and no button |
| segment values (`revalidate`, `dynamic`, `dynamicParams`) | literally in `page.tsx` / `route.ts` | Next parses them statically and refuses a re-export from an object |
| identity, SEO, branding, analytics | the configs, read at runtime (`npm run read:app-config`) | writing them into code is wrong twice: the app reads the file, and the file overwrites you |
| user-visible text | the translation layer, a key per string | a `lang === "ru" ? … : …` ternary cannot be translated, and it is found by the person least expecting it. Machine strings — ids, slugs, enum values — are never translated |

## 4. Names and size

- **250 lines** for a component or a function, then decomposition is mandatory — not "after this
  feature". Past that size state, rendering and side effects blur, and every later change touches what
  it did not mean to. Data does not count: a translation table or a country list is data.
  🔒 **This is the one limit with NO gate behind it** (checked 2026-08-22): nothing measures it, so it
  holds only while you stop and count. Everything longer than 250 lines in the project today is DATA —
  the specimen file, `SCHEMA`, the block catalogue, a page language cell — and data is exempt by the
  line above, not by an exception somebody granted it.
- `page.tsx` is a **thin entry**: declare the segment, re-export the entry from `./_components`.
- `.client.tsx` / `.server.tsx` suffixes say which side a file runs on, in its name.
- **Every `app/api/**/route.ts` opens with `// @api <verb first, 6–12 English words>`.** The address is
  a public contract and renaming it breaks browsers, logs and other people's integrations silently; the
  name in the header changes freely. At a hundred routes the question is never "what is this folder
  called" but "which one writes the presses" — only the name answers it. `npm run build:api-map`
  collects them into `development-docs/API-MAP.md`, which is **generated**: anything typed there by
  hand disappears at the next build.

## 5. Before you call it done

1. `npm run check:types` and `npm run check:i18n` — nobody runs them for you.
2. `npm run check:static` plus whichever gate covers the surface you touched.
3. On the server, after the build: your public routes are `●`. If one turned `ƒ`, look for one of the
   five lines in §1 — there is almost never another cause.
4. Open the page with JavaScript disabled and read it. Anything that must work without scripts, works;
   anything that degrades, degrades visibly rather than silently blanking.
5. 🔒 **Do not build locally on Windows.** The build belongs to the server; `npm run dev` is your
   local proof, and the exit code of a build is read from `npm`, never from the tail of a pipe.
