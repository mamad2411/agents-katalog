---
name: use-seo
description: >
  The SEARCH surface of a public page — the part a visitor never sees and a search engine judges the
  site by. Load it whenever you create a public route, change an address, touch metadata, add a
  section to the sitemap, or the owner says "the page is not in Google", "the wrong text shows up in
  the preview", "the picture is missing when I paste the link", "add hreflang", "set up robots".
  Every rule here was bought with a defect that looked like nothing: the page opens, the build is
  green, the gate passes — and whole languages are missing from results, or the page exists for
  nobody because no sitemap names it. Read it BEFORE the first file: a canonical address chosen
  wrong is not a cosmetic mistake, it is the page asking not to be indexed.
---

# use-seo

> Informational, not binding. **Know a better way for the case in front of you — do it your way and
> say so.** You are trusted with the creative work on this project.

**One builder per signal, and the page declares itself.** Everything below follows from those two.

| Signal | The only builder | Never |
|---|---|---|
| canonical + `hreflang` + the markdown twin link | `buildAlternates(lang, subPath)` — `lib/seo/alternates.ts` | a canonical written by hand, or inherited from the layout |
| the whole metadata object (title, description, OG, X card, robots, verification, icons) | `constructMetadata()` — `lib/construct-metadata.ts` | a hand-assembled `Metadata` |
| any address of our own page — in metadata, in a sitemap, anywhere | `urlFor(lang, subPath)` | a template string glueing site, language and path |
| structured data | three printers, §4 | a fourth printer of the same type |

A page built through `createContentPage` / `createContentPost` gets all four for free — that is what
the factory is for. A page written by hand owns all four itself.

## 1. 🔒 A page that does not declare itself gets the layout's declaration

Metadata in Next is **inherited**. `[lang]/layout.tsx` calls `constructMetadata()` with no `pathname`,
and that is deliberate: while it defaulted to `/`, every page that forgot its own `alternates`
announced the site root as its canonical — `/ru` literally said "index him, not me".

Which is why `check:seo` refuses a layout that declares `alternates` or `pathname` at all, and refuses
a page with no `generateMetadata`. **A missing canonical is harmless** (the page is read as its own
original); **a canonical pointing elsewhere hands the page away**, and one pointing at another domain
hands away the site. Never write a host into page data — the origin comes from `APP-CONFIG`.

## 2. One language means no language in the address

`SINGLE_LANG_MODE` turns on by itself when `NEXT_PUBLIC_SUPPORTED_LANGUAGES` holds one entry, and then
`proxy.ts` strips the segment from every public address: `/en/blog` answers 301 and the page lives at
`/blog`. That is the whole reason for the `urlFor` rule — a hand-glued address is a second source of
truth that disagrees with the first **only in that mode**, so it ships looking correct and turns every
canonical and every sitemap row into a redirect.

With two or more languages `buildAlternates` also emits `x-default` plus one entry per language. A
translation that does not name its siblings is not read as a translation but as a copy, and a set of
copies where nobody claims the original is what a search engine calls a doorway. The cost is not a
lower position — it is entire languages absent from results while the site looks perfect to its owner.

## 3. The snippet is not the first paragraph

`description` is cut to **160 characters** (`MAX_DESCRIPTION_LENGTH`, then `truncate` adds an ellipsis).
It travels into the result page and into the social card, and that is a different job from the opening
paragraph, which explains the product to a human and takes the room it needs. Feed one field to both
and you get either a snippet cut mid-word or a hero of one line — the home page carries that reasoning
in its own `_data/index.ts`; do not undo it.

The five language-sensitive values (name, description, title template, keywords, site name) resolve
through `configValueForLang`. Without `lang` a Spanish page introduces itself in English.

## 4. Structured data has exactly three printers

| Who prints | What | Where |
|---|---|---|
| `[lang]/layout.tsx` | `WebSite`, `Organization`, `LocalBusiness` — each behind its own `cfg.jsonLd.*` switch | builders in `lib/jsonld.ts` |
| the page factory | `Article` / `NewsArticle`, `author` = **`Person`** (`@id`, `sameAs`), `publisher` = `Organization`, and `FAQPage` | inline in `lib/content/create-content-page.tsx` |
| `components/nav/breadcrumbs.server.tsx` | `BreadcrumbList` | beside the trail a human sees |

🔒 **Breadcrumb markup lives where the drawn path lives, and nowhere else.** The factory used to print
a second `BreadcrumbList`; two declarations of one path drift apart at the first edit, and silently,
because nobody opens the second one in a browser.

🔒 **A switch can hide markup you correctly wrote.** `breadcrumbs` in `PLATFORM-CONFIG` gates the
trail AND its `BreadcrumbList` together; `faq` does the same for the questions and `FAQPage`. Both
default to on, but an owner who turned one off has a site where your structured data is simply
absent — and it looks exactly like a page you built wrong. Before hunting your own mistake, read the
switch: `npm run read:app-config` and the platform config beside it. A requested feature that is
switched off is a sentence to the owner, not a bug to fix.

🔒 **A switch is honoured at the SOURCE, not at each consumer.** `featureOn("faq")` blanks the array
once, so the visible block and the `FAQPage` node cannot disagree. Gating only the visible half
promises a machine something the page does not contain.

**Author and brand are read, never typed** — `lib/author.ts`, `lib/brand.ts`, both from `APP-CONFIG`.
`sameAs` is what consolidates a person into one entity; two spellings split that entity in half. An
empty author is a legitimate state: no byline, no `Person` node. Better no attribution than a false one.

## 5. 🔒 A section named by no sitemap does not exist

Everything above guards the QUALITY of a page's signals and says nothing about a page nobody can find
— and that error costs more. It shipped twice: the blog answered 200 with two translated posts while
no map knew it, then all five footer pages, for a reason worth memorising —

> **`check:seo` counts a section as a first-level folder of `app/[lang]` holding a `page.tsx`. Bracket
> groups (`(publicLayer)`, `(footerPages)`) are transparent to it.** Transparency for the URL is not
> transparency for the map. A page inside a group is guarded by nobody — name it yourself.

| Set | Map | Why |
|---|---|---|
| finite, authored — home, sections, posts, footer pages | `app/sitemap.ts` | posts arrive from `_list.generated.ts`, so a new post enters the map by existing; footer pages are a **literal list**, so a private page cannot walk in on its own |
| grows at runtime — products | `app/products/sitemap.ts`, chunked | the limit is 50 000 URLs per file and exceeding it makes an engine drop the file **whole**; addresses here are rows × languages |
| behind a role | never | it does not exist at build, and a crawler would be handed the login form |

`robots.ts` is config-driven (`seo.indexing`, `seo.disallowPaths`, plus the service paths) and must list
**every** map, product chunks included: the storefront lazy-loads its rows, so the map is the only door
an engine has to them.

🔒 **A sitemap that throws takes the whole build with it** — map generation runs inside the page-data
phase. The product map wraps its query in `try/catch` and ships empty on failure; a deployment already
died this way.

## 6. The picture in the card

`og:image` must be **absolute** — Telegram, Facebook and LinkedIn ignore a relative path — and the file
must exist. Nothing checks the second half: `check:content` verifies assets named in blocks, never in
`meta`. Five footer pages shipped pointing at `/og-default.png`, a file absent from the repository, and
the preview card of every one of them was empty. Request the URL before you believe it.

Keep the page's own illustration and its card picture the same value; two different ones mean the human
and the machine are looking at different pages. **One file, three roles** — `heroImage` under the
title, `og:image` + `twitter:image`, and `Article.image` — declared once in `_data/meta.ts`.

**Where that file lives:** `public/page-media/<slug>.jpg`, 1200×630. Posts keep theirs in
`public/blog-media/`, and `public/placeholders/` belongs to the settings slots — do not park a page
picture in either. No text inside the picture: a word baked into pixels is not translated, and the
site has more than one language.

**When the owner has no picture at all**, `/og-default.png` answers — it is a ROUTE
(`app/og-default.png/route.ts`), not a file: a card drawn at build from the project's own identity,
shapes seeded by the site name, the owner's logo composited when he uploaded one. Never our mark,
never a letter of text. That address exists because five pages pointed at a file nobody had created.

## 7. What the gates say, and what they cannot

| Command | Refuses |
|---|---|
| `check:seo` | a page with no `generateMetadata`; no `alternates`; `openGraph` without `url`; an address glued by hand inside a sitemap; a layout claiming a canonical; a first-level section present in no map |
| `check:aio` | a public page with no markdown twin — see `use-aio` |
| `check:content` | the link and asset rules of the body — **`use-links`** owns them, and they are part of this surface: an outgoing link spends the weight this page earned |
| `npm run build` | the honest answer to "is it still static": `●`, never `ƒ` |

All of them were green before your change too. Green proves the tree is well-formed, never that the
page is findable.

## 8. Before you call it done

- Fetch the built page and read its head: one `canonical`, one `og:url`, `hreflang` for every enabled
  language plus `x-default`, the `alternate` of type `text/markdown`, and the `ld+json` blocks —
  **count** them, a duplicated `BreadcrumbList` is invisible any other way.
- Request the `og:image` URL itself. Empty card, missing file, same thing.
- Read `/sitemap.xml` and `/robots.txt` on a deployment that has an address, and find your page there.
- 🔒 **An empty sitemap on your own machine is NORMAL, not a defect.** `app/sitemap.ts` opens with
  `if (!site) return []`, and `site` comes from `APP-CONFIG`, which stays `{}` until a server fills it.
  Judge the map where there is an address, never here.
