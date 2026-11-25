---
name: use-static-pages
description: >
  Build or change a STATIC PUBLIC page — a blog post, a footer page, the home page, any page whose
  content somebody authored and every visitor sees the same. Use when the owner says "add an article",
  "write a page about X", "add a section to that page", "translate this post", or when you are about
  to create any folder under app/[lang]/(publicLayer). This is the FIRST of the three page models:
  a folder per item, prerendered, indexed. Data that grows without limit is the second model
  (use-dynamic-pages) and a user's own screen is the third — do not carry these rules there.
  Read this before writing the first file, because the two defects this area produces are invisible
  until late: a page nobody can find, and a page that ships one project's identity into another's.
---

# use-static-pages

> 🔒 **Superseded in one point (2026-09-25): a new page is a DATA folder read by one template, never a new**
> **`page.tsx`** — load `use-page-tree` first. Measured: 300 page files 1252 s against 98 s through one template. The
> per-folder `page.tsx` shape described below is how the existing pages were built — debt, not an example.

> Informational, not binding. **Know a better way for the case in front of you — do it your way and
> say so.** You are trusted with the creative work on this project.

**A page is a LIST OF BLOCKS in a language cell, not a laid-out file.** Everything below follows from
that. The engine's rule: everything a page needs lives in its own folder, everything shared lives once
in the engine, nothing in between.

---

## 1. Four layers

```
route shell   app/[lang]/(publicLayer)/<tab>/<slug>/page.tsx   3 lines, re-exports ./_components
per page      _components/  view      index.tsx — calls the factory
              _data/        data      meta.ts + one cell per enabled language + index.ts
              _lib/         functions resolve/list + type contracts   (a tab has one, a page rarely)
engine        lib/content/  factories create-content-page.tsx · create-content-post.tsx
                            resolve.ts (cell resolver, EN fallback) · blocks/{types,registry,inline,links}
              lib/parser-fs.mjs        generates _list.generated.ts on predev/prebuild — gitignored
sections      sections/blocks/<kind>.server.tsx   ONE kind, ONE file — the renderers
              sections/index.ts                   the full set · sections/contract.ts the contract
```

🔒 **A page folder sits TWO levels below the layer: `<tab>/<slug>/`, never directly under the group.**
`(publicLayer)/about/` looks natural and is wrong: the co-location gate derives the "tab" as
`_data/../..`, so a page one level down turns the WHOLE public layer into a tab of posts and applies
post rules to every neighbour — 27 failures on code you never touched, and nothing in the message
points at your folder. The tabs are `blog/`, `products/`, `(footerPages)/`; a page that belongs to
none of them needs a tab of its own, not a shortcut. This cost a rebuild during the skill's own trial
run.

🔒 **Localized UI strings are DATA** → `_data`, never `_lib`. Type contracts are CODE → `_lib/types.ts`.
🔒 **`lib/content/blocks/types.ts` has zero imports on purpose** — a leaf of the graph. Engine types are
imported, never extended.

**How many kinds exist — ask `sections/index.ts`, never this file.** The authoritative list is `sections/index.ts` (the `SECTIONS` object)
and it always equals the number of files in `sections/blocks/`; `npm run check:sections` prints the count. A number written into a skill is stale the week after it is written — this one said 28 while the gate answered 29. You cannot get this wrong silently:
`SectionSet` is a mapped type over every `Block["kind"]`, so a kind without a renderer does not compile.
Count them before you invent a new one — `p`, `h2`, `list`, `table`, `card`, `cards`, `callout`, `note`,
`quote`, `code`, `figure`, `columns`, `metrics`, `flow`, `panel`, `cta`, `badges`, `docref` and more are
already there.

## 2. Recipe: a new post

Six files, all inside one folder. "Copy an existing folder" beats "write from scratch" every time.

```
app/[lang]/(publicLayer)/blog/<slug>/
  page.tsx                 re-export of ./_components
  _components/index.tsx    createContentPost({ … })
  _data/meta.ts            non-translatable: slug, date, tags, hero, author
  _data/<lang>.ts          one cell per ENABLED language
  _data/index.ts           { meta, en, overrides: { … } }
  index.md/route.ts        markdownRoute('/blog/<slug>') — the machine twin
```

🔒 **The hero is OPTIONAL — every hero field is.** `heroImage`, `hero`, `heroVideo`, `heroPoster` are all
`?`. No video means no hero is drawn at all, and that is a legitimate post, not a half-finished one.
`heroPoster` still earns its place without a video: the blog list card draws it, and `ogImage` falls back
to the visible image (`post.ogImage ?? post.heroImage`) for social previews.

A footer page is the same shape with `createContentPage`, and needs three more edits **outside** the
folder — this is where the engine stops being self-contained:

| Also edit | Why |
|---|---|
| `lib/aio/surfaces.ts` | without the entry `/index.md` answers 404 and `llms.txt` never learns the page |
| `app/sitemap.ts` | groups in brackets are invisible to `check:seo`, so nothing will notice the miss |
| `lib/menu/nav-config.ts` → `DEFAULT_FOOTER` | the footer links of a FRESH project; the owner's own list lives in the panel |
| `_data/group.ts` — only for the TOP menu | the menu scanner finds a group by that file alone; without it the page is reachable by direct address only. Its label comes from `eyebrow` in each language cell, so it is translated — `DEFAULT_FOOTER` labels are not. Recipe and the two-sources trap: `place-page-in-menu` |

Posts need none of the three: `parser-fs` finds them, and the blog list feeds the sitemap.

🔒 **A whole NEW TAB is a folder plus FOUR edits outside it, and one of them is invisible.** Create
`app/[lang]/(publicLayer)/<tab>/` with its `_lib/{post,types}`, `_data`, `_components` and post folders,
then: (1) the tab into `COLLECTIONS` in `lib/parser-fs.mjs` — without it the list is never generated;
(2) the section into `app/sitemap.ts` — posts inside a KNOWN tab arrive by themselves, a new tab does
not; (3) the surface into `lib/aio/surfaces.ts`, or `/index.md` answers 404 for the whole tab; (4) the
entry into the menu, if people are meant to find it (`place-page-in-menu`).

✗ 2026-08-19: a whole section was written, translated and served 200 — and appeared in no map at all,
with every gate green. There is deliberately no central `posts.ts` to append to, but "no registry" was
never the same as "nothing outside the folder".

🔒 **Two factories exist, and the pair is CLOSED.** `createContentPost` for an item inside a
collection, `createContentPage` for everything else — the home page, privacy, terms, cookies. **A page
that needs less simply passes less:** breadcrumbs, the back link, tags, the hero, the FAQ and the
table of contents are all optional, and absent chrome renders nothing — the structured data drops
`BreadcrumbList` rather than emitting an empty one.

A third factory was proposed once for the home page, justified as *"a landing has a different anatomy
from a document"*. The claim was false: of the fifteen props, fourteen already degraded to nothing
when omitted, and the three that did not — `breadcrumbs`, `backHref`, `backLabel` — were `required`
**in our own code**. **Required-ness is a property of the code, not of the domain:** when a surface
looks like it needs its own machinery, ask what *physically* stops it from using what exists; if the
answer is a constraint you wrote yourself, remove the constraint. And the cost of a second factory is
not duplication — it is that a rule added to one never reaches the other, so the surfaces drift apart
with nothing red anywhere.

🔒 **The page is not finished when it renders.** A static page has three more surfaces, each with its
own skill and its own gate, and each invisible from the page itself: **`use-seo`** (canonical,
hreflang, structured data, the sitemap row, the card picture), **`use-aio`** (the markdown twin and
the map for models), **`use-links`** (the one form of an internal link, and why an outgoing one is the
owner's decision). `use-pwa` matters only when you touched the manifest or the worker. Skipping them
produces the two defects named at the top: a page nobody finds, and a page that carries another
project's identity.

## 3. Language cells

**One cell per ENABLED language** — the set is `NEXT_PUBLIC_SUPPORTED_LANGUAGES`, not the count your
neighbours happen to have. An enabled language with no cell is not a smaller post: it is the English
post at a foreign address, announcing itself as a translation. `resolve.ts` falls back to English key
by key, so a partial cell is legal and honest.

The slug is language-agnostic and chosen once from the English title. One post spans all languages.

## 4. 🔒 The law of the two links

Enforced by `check:content`, and every rule below is a defect that already shipped.

**External — always absolute.** It carries a host, opens in a new tab, and `lib/content/blocks/links.ts`
adds `rel="noopener noreferrer nofollow"` — omitting `nofollow` for **this project's own** domain, read
from `APP-CONFIG`. A relative external link is a bug: the post travels into projects that do not have
the page it points at.

**Internal — one form only:** `[%SITE%](/ru)` — the site root in the language of that cell. The label is
the literal token `%SITE%`, replaced at render time by the site's own name. **Every cell carries one.**
A name typed in by hand freezes one project's identity into content copied into every other project.

The same form is legal in an `href:` field — `cta`, a linked `figure`.

## 5. 🔒 Identity comes from settings

Author, site name, own domain, currency — from `APP-CONFIG`, never typed into `_data`. Leave
`meta.author` out and the byline comes from the project's settings; fill it only for a genuine guest.
Rule `brand-in-data` refuses the rest.

## 5a. Three more laws, each bought with a defect

**Images are referenced by NAME — `media:<file-name>` — never by id.** An id is born at upload and
differs on every server; a post must be identical everywhere. An id in `_data` renders a broken image on
every machine except the one it was written on.

**A missing canonical is harmless; a canonical pointing at ANOTHER domain hands the whole site away.**
Never write a host into `_data`. The address comes from `APP-CONFIG` and is derived from the server that
answers — see §5.

**A heading in a non-Latin script still needs an anchor.** Slugging that keeps only `[a-z0-9]` produces
`id=""` for every Cyrillic, Greek or CJK heading — and then the whole table of contents links to `#`.
It shipped exactly that way on `/ru`.

## 6. Need something that WORKS, not prose?

A calculator, a picker, a list that saves — **that is a kind of section, not a page of its own**:
a server renderer in `sections/blocks/<kind>.server.tsx` resolves data and dictionary and mounts an
island from `components/`. Pattern to copy: `project-type-marquee.server.tsx`.

🔒 **No file under `sections/` carries `"use client"`** — a property of the layer, not an accident.

A page of its own is for something that needs its OWN ADDRESS — searched for, linked to, in the sitemap.
Its body is still blocks.

## 6a. 🔒 The page ships without the part you could not make

Same law as everywhere: a missing piece is a branch with an exit, not a failed step. Finish the page,
say what is missing, open a step for it in `new-steps/`, close this one as a success.

**But the trap here is the opposite one.** On a page behind a role the temptation is to stall waiting
for data; on a page of prose the temptation is to **invent the content** — and that failure ships
looking finished, which is why it survives.

| Missing | Do NOT | Do |
|---|---|---|
| a fact, a number, a date about the owner's business | write a plausible one | leave the block out, or mark the text a sample in its own words, and ask |
| a source for a claim you are making | attach a link that looks authoritative | name the source in words and let the architect approve the link — `use-links` |
| a section kind the catalogue does not have | invent one for this page alone | ship without that block; a new kind is its own step, and a one-page thing is a widget |
| a widget or tool the page wanted | fake it with static markup pretending to work | ship the page, defer the widget — `use-dynamic-pages` §3c |
| a picture | ship a broken path | ship without it (every hero field is optional) or draw a placeholder that says so |
| a translation | machine-fill languages you cannot check | write the enabled set, record the debt — `use-multi-lang` |

🔒 **A sample page must say it is a sample, in the text a visitor reads.** The starter's own "About
us" carries that line about its invented team and history — remove it and the shipped example becomes
a claim about a real company, in every project that copies it.

## 🔒 Страница построена — спроси, где её найдут

Страница, на которую не ведёт ни одна ссылка, существует только для того, кто наберёт адрес руками.
Так уже было: страница менеджера жила с самого начала и не была связана ничем — он свою же таблицу не
находил.

Поэтому **закрывая страницу, спрашиваешь владельца о размещении**, а не решаешь за него:

| Какая страница | О чём спрашиваешь | Куда добавляется |
|---|---|---|
| за авторизацией — динамическая или защищённая | **в выдвижной ящик?** | `lib/menu/account-links.ts`, строка с `group` своего слоя |
| публичная | **в верхнее меню? в подвал?** | манифест `_data/group.ts` (шапка) или список подвала — `place-page-in-menu` |

Спрашиваешь **вопросом, а не утверждением**: «добавить её в ящик администрирования?» — потому что
ответ бывает «нет»: страница может быть шагом мастера, целью ссылки из письма или частью другой
страницы, и пункт меню ей не нужен.

🔒 **Ящик — вежливость, а не защита.** Замок стоит в `layout.tsx` группы и в дверях данных; пункт
лишь показывает дорогу тому, у кого доступ уже есть. Роли пункт НЕ перечисляет — он называет свою
группу (`group: "admin"`), а роли группы знает `lib/roles.ts`. Перечисли их копией — и однажды пункт
начнёт либо дразнить отказом, либо прятать доступное.

## 7. What the gate checks — `npm run check:content`

| Rule | Rejects |
|---|---|
| `link-not-absolute` | a relative link that is not the root form |
| `root-link-label` | a root link whose label is not `%SITE%` |
| `asset-missing` | `heroVideo` / `heroPoster` / `src` with no file in `public/` |
| `brand-in-data` | the site's name written into `_data` |
| `cell-missing` | `_data/index.ts` imports a language file that does not exist |
| `single-language` | a post with no translation at all |
| `no-root-link` | a cell with no link home — counted **per file** |
| `translation-coverage` | an ENABLED language with no cell — warning in build, refusal under `--strict` |

Also: `check:sections` (every kind has a specimen on the catalogue page), `check:aio` (markdown twin),
`check:seo` (metadata, alternates, `openGraph.url`). They read files, they do not build — run them.

## 8. Before you call it done

1. `npm run check:content`, `check:sections`, `check:aio`, `check:seo` — green. They were green BEFORE
   your change too, so green alone proves nothing.
2. Still static: no `force-dynamic`, no `cookies()` / `headers()` / `auth()`, no `"use client"` under
   the tab.
3. Open the page in every enabled language and read it.
4. Never hand-edit `_list.generated.ts`. It is regenerated by **`node lib/parser-fs.mjs`** — the same
   command `predev`/`prebuild` run for you. Added a post and the blog list does not show it? Run it.
5. Never introduce a dynamic `[slug]` here — that is the second model, and it has its own skill.
6. **Two proofs no gate can give you, and no cheaper substitute counts.** The build's route table must
   show `●` (not `ƒ`) for the index and every post — only the build knows what it prerendered. And the
   article's text must survive with every script stripped:
   `curl -s <url> | sed 's/<script[^>]*>.*<\/script>//g' | grep "<a phrase from the article>"`.
   "The code looks static" is not the first, and "it opens in my browser" is not the second — the
   browser runs the very JavaScript you are trying to prove unnecessary.

🔒 **An empty sitemap on your own machine is NORMAL, not a defect.** `app/sitemap.ts` opens with
`if (!site) return []`, and `site` comes from `APP-CONFIG/app-config.json`, which is `{}` until a server
fills it. Locally you will see `<urlset></urlset>` and nothing else. Judge the sitemap on a deployment
that has an address, never here.
