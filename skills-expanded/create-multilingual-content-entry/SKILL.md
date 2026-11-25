---
name: create-multilingual-content-entry
description: >
  Create a multilingual content document (news, blog, docs, any page copy) the
  scalable, co-located way: one route folder per document, a full base-language
  file, partial per-language override files — auto-discovered (no registry), with
  zero language branching in page code. Use whenever you add or translate content
  that must work in more than one language. Self-sufficient: pure file edits, no
  any external service.
---

# create-multilingual-content-entry

> Informational, not binding. **Know a better way for the case in front of you — do it your way and
> say so.** You are trusted with the creative work on this project.

Add a piece of multilingual content so it scales to many languages **by construction** —
a new language is a new file, a partial translation is fine, and no page ever says
`if language == X`. The full engine standard — architecture, every component, how it scales, the law of
the two links and what the gate rejects — is the skill `use-static-pages`; this skill is its
operational entry.

This skill is **self-sufficient**: it is plain file editing. It does NOT depend on any service,
on memory, or on any other agent. If you are the only agent in the project, you can still
create a correct multilingual document.

## When to use

- You are adding a content item (a news post, a blog post, a doc, a landing section) that
  must exist in more than one language — now or later.
- You are translating an existing item into a new language.
- You catch a `lang === 'xx' ? A : B` ternary in page code and need to move it into the
  data layer (`_data`) or a data discriminator.

## The shape — document = co-located route folder (NO registry, NO `[slug]`)

```
app/[lang]/<tab>/<slug>/        # one document = one co-located route folder
  page.tsx                      # thin: re-export Entry + generateMetadata from ./_components
  _components/index.tsx         # createContentPost / createContentPage({ resolve, chrome, … })
  _data/
    meta.ts                     # non-translatable: slug, date, tags, author, images
    en.ts                       # the FULL base body (required): translatable fields + blocks + FAQ
    <lang>.ts                   # a PARTIAL override: only the keys that differ from the base
    index.ts                    # export const data = { meta, en, overrides: { <lang> } }
```

**There is no registry and no dynamic `[slug]`.** The tab's post list is auto-discovered:
`lib/parser-fs.mjs` scans the tab folder at build (`npm run gen:lists`, also `predev`/`prebuild`)
and regenerates `app/[lang]/<tab>/_list.generated.ts` (gitignored). Adding a document =
adding a folder; **zero existing files are edited**. Deleting the document = deleting the
folder (zero orphans).

The per-tab plumbing already exists once in the tab folder and is reused by every document:
- `app/[lang]/<tab>/_lib/post.ts(x)` — FUNCTIONS: the `resolveEntry`-based resolver +
  list helper (`<tab>Post` / `<tab>List`) and `<tab>/_lib/types.ts` — the type contracts.
- `app/[lang]/<tab>/_data/{en,ru,index}.ts` — DATA: the tab's localized UI chrome
  (`get<Tab>Ui(lang)`). UI strings are data → never hardcode them in `_components`.
- Shared engine (reused, never copied into a tab): `lib/content` (neutral block catalog,
  `resolveEntry`, `createContentPost`/`createContentPage`) + `components/content-page`
  (`StandardContentPage`, `PostBody`). A new tab = one line in `lib/parser-fs.mjs`
  `COLLECTIONS` with `typeModule: './_lib/post'`.

## 🔒 One post spans ALL languages — the slug is a language-agnostic identifier

A content item is **ONE post that spans every language**, never one post per language. Its
`<slug>` is a **stable, language-agnostic identifier chosen ONCE from the base (English) title**
and reused for every language: `/en/<tab>/<slug>` and `/es/<tab>/<slug>` share the SAME `<slug>` —
only the language prefix differs. A translation is a `<lang>.ts` cell in the SAME folder — **never
a second post**. Therefore:
- **Never slugify a translated title** (a Spanish title must NOT become a second `hemos-…` post).
- **Never create a post once per language** — one create yields all language cells at once.
- Creation is always keyed by the **English identifier**; translating is a SEPARATE path (the
  `expand-site-language` and its translation runner) that writes INTO the cell, it
  does not create a post.

## The five rules (do not skip)

1. **`en` is the full base, required.** Every other language is a partial override; any key
   it omits falls back to `en` per key (not the whole object) — done by `resolveEntry`.
2. **Arrays replace wholesale, never merge element-wise.** A partial list translation means
   "translate the whole list or inherit the base one".
3. **No language branching in pages.** A UI label → a key in the tab's `_data` chrome
   (`get<Tab>Ui`). A different component per language → a discriminator field in the data,
   not a ternary in `_components`.
4. **Dates via `toLocaleDateString(lang, …)`** — pass `lang` straight through; never map
   `'ru' → 'ru-RU'` by hand.
5. **SEO/GEO per language — SAME slug, different prefix.** Every language is served at the SAME
   `<slug>` under its language prefix (`/en/<slug>`, `/es/<slug>`) with correct `hreflang`; each
   gets its own SEO surface (title/description/keywords) from its own angle (not a word-for-word
   copy). This is NEVER a separate post or a translated slug. If the project keeps `llms.txt` /
   `llms-full.txt` / sitemap, update them in the same change.

## Confirm before creating (mandatory)

Before writing files, restate to the architect exactly what you will create: the `<tab>`,
the `<slug>`, the base language, and which languages get an override now. Create only after
explicit confirmation. Never silently scaffold a content tree.

## Steps

1. Pick the `<tab>` (e.g. `news`, `blog`, `documentation`) and a kebab `<slug>`. If the tab
   does not exist yet, create it first (its `_lib/{post,types}`, `_data/{en,ru,index}`,
   `_components/index.tsx`, thin `page.tsx`) and add one `COLLECTIONS` line in
   `lib/parser-fs.mjs` — see `content-engine.md` §7.
2. Create `app/[lang]/<tab>/<slug>/_data/meta.ts` — non-translatable fields only.
3. Create `_data/en.ts` — the complete base body (all translatable fields + blocks + FAQ).
4. For each language you can translate now, create `_data/<lang>.ts` — only the keys that
   differ. Leave the rest; `resolveEntry` fills them from `en` per key.
5. Create `_data/index.ts` — `export const data = { meta, en, overrides: { <lang> } }`.
6. Create the thin `page.tsx` (re-export from `./_components`) and `_components/index.tsx`
   (the `createContentPost`/`createContentPage` composition, chrome via `get<Tab>Ui`).
7. **Do NOT edit any list/registry** — run `npm run gen:lists` to regenerate
   `_list.generated.ts`; the index picks the new document up automatically.
8. Verify: `npx tsc --noEmit` passes, and a grep for `=== '<lang>'` in `_components` is clean.
   (Windows: never `npm run build`.)
9. If the project has `llms.txt` / `llms-full.txt` / sitemap — add the new item.

## After creating

Report to the architect:
> Created multilingual <tab> document «<slug>» — co-located route folder with full `en`
> base + <N> language override(s); auto-discovered (no registry edit). No language
> branching; dates/SEO per the standard. Ready to add another language later as a single
> new `_data/<lang>.ts` file.

The document is content, not a feature. Adding the 81st language stays a one-file change,
and deleting the document is deleting one folder — that is the whole point of the co-located
shape (full rationale in `content-engine.md`).
