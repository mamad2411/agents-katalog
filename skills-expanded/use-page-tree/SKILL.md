---
name: use-page-tree
description: >
  How a page is added in a Fractera WEB4 ITEM — as a FOLDER OF DATA read by one route template, never as a
  new `page.tsx`. Load it before creating anything under `app/`, when the owner asks for "a new page",
  "a section", "an article", "a tab with N pages", "the same page in every language", and whenever a
  build is slow and you are about to look for the cause. The thing you cannot guess: every route file is
  compiled and type-checked on its own with everything it imports, so a site built as one `page.tsx`
  per page gets slower with every page and ends at many minutes per build — measured here as 1252 s for
  300 page files against 98 s for the same 300 pages through one template. The build succeeds either
  way; nothing warns you until the owner waits an hour.
---

# use-page-tree

> COPY. The master of this skill lives in the element templates (`Fractera/fractera-custom-item-starter`, `.claude/skills/build-skills/
> skills/use-page-tree`, `lib/page-tree.ts`). Change it there first, then copy here.
> Paths below are an element's; in the core the same shape applies to `app/[lang]/(architectLayer)/`.

> Informational, not binding. **Know a better way for the case in front of you — do it your way and
> say so.** The one thing that is not optional: a new page never arrives as a new route file.

## 0. The rule, in one line

**A page is a folder in `presentation/content/`. The route is one template for all of them.** Creating a
`page.tsx` (or `route.ts`) for a new page is forbidden; `scripts/check-routes.mjs` fails the build on any
route file that is not in its closed list, and names this skill.

## 1. Why — measured, not believed (this service, Next 16.2, Cache Components on, 2026-09-25)

| built | total | compile | types | prerender |
|---|---|---|---|---|
| the service as it was (40 pages) | 103 s | 60 s | 21 s | 3.6 s |
| + 100 pages as separate `page.tsx` | 183 s | 114 s | 50 s | 7.7 s |
| + 300 pages as separate `page.tsx` | **1252 s** | 7 min | 83 s | 63 s |
| + 300 pages through ONE template | **98 s** | 53 s | 22 s | 13 s |
| + 300 page FOLDERS × 2 languages, one template, only `en` prerendered | **73 s** | 34.5 s | 19 s | 12.5 s |

Also measured: editing ONE page of 100 rebuilds everything (164 s of 172). The Turbopack build cache
(`experimental.turbopackFileSystemCacheForBuild`) crashed on Windows (`kill EPERM`) both times.
`next build --debug-build-paths` builds one route but its output lacks every other page — it is for
debugging and must never be released. **A production build is always the whole app; the only lever is
how many route files the app has.**

The core of the node reached 126 near-identical `page.tsx` files (each one differs from its neighbour only
by a comment) and 5–7 minutes of compile. That is the failure this skill exists to prevent.

## 2. Where things are (the reference implementation lives in this repository)

| What | Where |
|---|---|
| the only template | `presentation/app/[lang]/[collection]/[[...slug]]/page.tsx` — a page, and the collection index when `slug` is empty |
| reading the tree | `presentation/lib/page-tree.ts` — `pageTree()`, `pageWords()`, `prerenderSlice()`, tag `PAGE_TREE_TAG` |
| the content | `presentation/content/<collection>/` |
| the folder root at runtime | `server.js` sets `PAGE_TREE_DIR` |
| the sitemap | `presentation/app/sitemap.ts` — from the same tree, no second list |
| the guard | `scripts/check-routes.mjs`, first command of `npm run build` |

`presentation/pages/` must never exist: it is the Pages Router of Next and every folder in it would become
a route. That is why the content root is called `content`.

## 3. Adding a page — three files, no code

```
content/<collection>/_collection.json   { "titles": { "en": "Guide", "ru": "Руководство" }, "index": true }
content/<collection>/<slug>/meta.json   { "order": 10 }                       ("index": false hides one page)
content/<collection>/<slug>/en.json     { "title": "…", "lead": "…", "blocks": [ … ] }
content/<collection>/<slug>/ru.json     (one file per language the page exists in)
```

- The address is the folder path: `/<lang>/<collection>/<slug>`; nested folders give nested addresses.
- `blocks` are blocks of the catalogue (`registry/src/lib/content/blocks/types.ts`, kinds such as `h2`, `p`,
  `list`, `quote`, `code`, `figure`, `cta`) — the page is COMPOSED, not coded.
- **There is no registry.** Add the folder and the page has an address, a line in the collection index and
  a line in the sitemap; delete it and it is gone from all three. There is no list to forget.
- A language the page has no file for is a real 404, and hreflang lists only the languages that exist:
  a link to a translation that does not exist is a lie to the search engine.
- A new collection is a new folder with `_collection.json`. **It is not a new route.**

## 4. Texts are DATA, never modules

`<lang>.json` is read at render time inside `'use cache'`. **Never import page texts as TypeScript modules**
(`_data/en.ts`, `words.i18n.ts` per page): the compiler then carries every language of every page, and
600 pages × 82 languages inflate the build exactly the way 600 route files do.

## 5. Prerender a slice, the rest on the first visit

`PRERENDER_LANGS=en,ru` limits what the build draws. Every other address is drawn on its first visit and
saved to disk — Next 16.2 docs, `dynamic-routes.md`, "With Cache Components": *"pages rendered with runtime
params are saved to disk after a successful first request"*. Measured: a page outside the slice answered
the first visit in 0.67 s and every later one in 0.008 s. The page stays **static**: its own address, its
own HTML, canonical and hreflang. Only the address segment is dynamic, never the rendering — the static
standard of the project is kept.

With Cache Components `generateStaticParams` must return at least one param; an empty tree returns a
placeholder that answers 404. The collection index needs `slug: []` in the slice — without it the index
was not prerendered (found and fixed on 2026-09-25).

## 6. The real exception

A page whose behaviour cannot be composed from its sections (a live tool, a form with its own logic)
may have its own route file. It goes into `ALLOWED` in `scripts/check-routes.mjs` **with its reason** —
a decision the owner can read, not a habit. If a second page needs the same behaviour, the behaviour
becomes a block kind and both pages become data.

## 7. Search visibility is the owner's decision

A new collection starts with `"index": false`: public, indexable text is published only with the owner's
word (the federal law about public texts). Switching to `true` puts the pages into the sitemap and lets
search see them.

## 8. What this skill replaces

`use-routes` (row "public, authored, finite → a folder per item") and `use-static-pages` ("a folder per
item") carried the right half — one folder per page — together with the wrong half — one `page.tsx` per
folder. The folder stays; the route file per page is gone. Pages that already exist as separate files in
the core are **debt**, not examples: move them into a tree when their area is touched, one collection at a
time.

## 9. Proof this skill is true

Break it and watch the guard: add `presentation/app/x/page.tsx` → `npm run build` stops with
`===ROUTES_FAILED===` (checked 2026-09-25, exit 1). Remove the file → `===ROUTES_OK===`.
