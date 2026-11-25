---
name: use-app-config
description: >
  Everything about APP-CONFIG — what the application IS: name, description, brand, logo and
  images, icons and PWA, author, SEO and OpenGraph, structured data, analytics, currency, the
  `nav` branch, and the open list of social networks (`seo.socialLinks`). Use when the owner
  says "change the site name", "put my logo in", "add my Instagram", "the footer shows the
  wrong Telegram", "set the description for search", "our Twitter is stale", or anything about
  the site's identity or its accounts. ALSO use BEFORE hard-coding any name, address, handle,
  brand string or profile URL into a component — every one of them already has a home here,
  and a hard-coded copy is invisible to the panel and to the owner.
---

# use-app-config

> Informational, not binding. **Know a better way for the case in front of you — do it your way and
> say so.** You are trusted with the creative work on this project.

The file is `APP-CONFIG/app-config.json` in the project root. **The panel (`:3002`) writes it,
this application (`:3000`) reads it — per request.** A saved change shows on the next page load:
no rebuild, no redeploy.

```ts
import { getAppConfig } from "@/config/app-config"   // server only — it touches fs
```

Reading a file does not make a route dynamic. Pages stay static; `force-dynamic` would break that
and is not used here.

🔒 **This layer only READS. It never writes.** The panel owns the file. A helper here once created
it from the defaults on first read — two writers, and the panel stopped being the single answer to
"what is this app called".

🔒 **A missing file is normal**, and so is a partial one. The JSON holds only the owner's
decisions; `config/app-config.defaults.ts` answers for everything else, deep-merged underneath.
Seeing `{}` and concluding "empty, so it cannot be working" cost a whole session on 2026-08-18.

## 1. APP-CONFIG or PLATFORM-CONFIG — decide before you touch anything

The split is the owner's, and it is sharp:

| Question | Config | Example |
|---|---|---|
| Does this capability EXIST at all? | `PLATFORM-CONFIG` | "I don't want to see socials" → switch `socials` |
| WHAT is in it? | `APP-CONFIG` | "my Telegram is @aifa_dev" → `seo.socialLinks` |

Get this backwards and you offer the owner the wrong tool. Before the `socials` switch existed,
the icon row appeared merely because records existed — the only way to hide it was to delete the
data, which is not what "hide it" means. See `use-platform-config`.

## 2. A field lives in FOUR places

Changing a VALUE is ordinary work. Adding a FIELD is not: three of the four omissions are silent.

| # | Where | Miss it and |
|---|---|---|
| 1 | `config/app-config.defaults.ts` — the type | the build fails, loudly. The only honest failure. |
| 2 | `config/app-config.defaults.ts` — the default | an owner who never spoke gets `undefined` |
| 3 | **`config/app-config.schema.ts`** | **validation strips the unknown key on save — silently** |
| 4 | `APP-CONFIG/{schema,defaults}.json` | `check:config-schemas` fails the build on the server |

Number four is generated, never hand-written: `npm run build:config-schemas`. The fifth place —
the form in the panel (`bridges/app/app/[lang]/app-settings/_lib/fields.ts`) — is in another
repository, and a field absent there exists but cannot be edited by the owner.

## 3. Social networks — a record carries its RULE, not just a value

```ts
{ id: "telegram", name: "Telegram", urlTemplate: "https://t.me/{value}", value: "aifa_dev", icon: "/api/media/…/file" }
```

The address is **computed, not guessed**. That is the whole point: every network spells its
profile differently — `t.me/<handle>`, `wa.me/<number>`, and a LinkedIn PERSONAL profile is
`/in/`, not `/company/`. A free text field knows none of this and silently builds a dead link.

```ts
import { resolveSocialLinks, socialHref, socialUrls, twitterHandle } from "@/config/app-config.defaults"
```

`resolveSocialLinks(cfg.seo)` is the **single** place that decides what to show. Pass it `cfg.seo`,
never `cfg.seo.social`:

🔒 **`socialUrls(cfg.seo.social)` compiles, runs, and is wrong.** The function keeps a
compatibility path for that older call shape, so it answers with the four legacy keys only and the
open list never reaches the caller. That is exactly how `sameAs` came to tell machines
`twitter.com/fractera` — a starter default belonging to nobody — while the footer correctly showed
the owner's Telegram. Nothing throws. It is found only by reading the rendered `sameAs`.

🔒 **"No branch" and "empty branch" are different states.** `socialLinks` absent means the owner
never opened the constructor, and the four legacy `seo.social` keys still answer. `socialLinks: []`
means he removed every record on purpose, and resurrecting the legacy four would overrule a human
decision. The resolver tests `Array.isArray`, not `.length` — do not "simplify" that back.

🔒 **The legacy four are read VERBATIM, bugs included.** `linkedin` builds `/company/`, which is
wrong for a personal profile. Fixing the rule retroactively is forbidden: live servers hold values
entered *under that rule*, and changing the template would silently point a working link somewhere
else. New records get their rule from the model and inherit none of this.

**Icons are copied INTO the project**, never linked from a foreign CDN. The panel downloads the
SVG once (`api/config/social-icon`, source `cdn.simpleicons.org`, licence CC0-1.0 verified at the
source) and stores it in the media library; the record keeps `/api/media/<id>/file`. A CDN link
would put every visitor of every page on someone else's host and leave holes when
`offlineCache` serves the page offline. lucide carries almost no brand marks — that is why
`BrandX` in the footer is drawn by hand.

**`sameAs` is not gated by the `socials` switch, and that is deliberate.** Hiding the row is a
layout decision; `sameAs` is the site's claim to machines that these accounts are its own.

## 4. Language: which fields are translated, and how

Five fields are per-language — `name`, `description`, `seo.titleTemplate`, `seo.keywords`,
`og.siteName`. The main value is the field itself; other languages live in `i18n.<path>.<lang>`.
Everything else (logo, colours, coordinates, analytics ids, handles) does not depend on language,
and giving it a translation would be work with no reader.

Machine values are never translated: ids, slugs, enum values, `urlTemplate`.

## 5. Making a change visible

- Saving from the panel purges the app's ISR cache — the change shows on the next load.
- Editing the file **by hand purges nothing**: the page keeps its old HTML until the ISR window
  expires, up to ten minutes. That is the entire content of "I changed it and nothing happened".

```bash
curl -X POST http://127.0.0.1:3000/api/revalidate \
  -H "Content-Type: application/json" -H "x-agent-identity: agent" -d '{}'
```

A browser tab can also hold a page from *before* the purge. Fetch with `cache: 'reload'`, or hard
reload, before declaring anything broken — a stale tab has produced more than one false verdict.

Never suggest a redeploy to make a config change take effect.

## 6. Do not hard-code identity

Every site name, support address, brand string, profile URL or handle written into a component is
invisible to the panel: the owner edits the setting, nothing moves, and the value rots where no
one looks for it. The Twitter card read `seo.social.twitter` directly for exactly this reason and
lost the author for every owner who used the constructor.

If a value genuinely has no home here, add the field (section 2) — do not inline it.

## 7. Before you call it done

1. Change the value **in the panel**, not in the file, and confirm it in a browser.
2. Check the **markup**, not only the pixels: `sameAs`, OpenGraph, the Twitter card and the
   manifest all read this config, and each can go stale on its own.
3. Count **elements, not words**. Grepping the HTML for `twitter` proves nothing — the word lives
   in `sameAs`, in class names, in comments. Count `<a href=…>`. Measuring by words once produced
   the confident verdict "the socials gate is broken" about a gate that worked.
4. `npm run check:types`, and `check:config-schemas` if you touched a type or a default.
