---
name: use-platform-config
description: >
  Everything about PLATFORM-CONFIG — the eleven switches that decide which capabilities the site
  offers: top menu, footer pages, cookie banner, sign-in, breadcrumbs, FAQ, theme toggle, width
  toggle, language switcher, socials row, offline cache. Use when the owner says "turn off the
  menu", "remove the cookie notice", "hide the login button", "we don't need breadcrumbs", "hide
  the social icons", "add a header", "the switch does nothing", or anything about a capability
  being present or absent. ALSO use
  BEFORE building any header, footer, consent strip, theme or language control of your own —
  they already exist, they are switched, and a hand-rolled copy answers to nobody.
---

# use-platform-config

> Informational, not binding. **Know a better way for the case in front of you — do it your way and
> say so.** You are trusted with the creative work on this project.

The file is `PLATFORM-CONFIG/platform-config.json` in the project root. The panel writes it, the
app reads it on every render, and a change needs **no rebuild**.

## 1. What the file holds — and what it deliberately does not

```json
{ "features": { "topMenu": true, "auth": false }, "developmentMode": "cases" }
```

🔒 **Only the owner's DECISIONS live on disk.** A key that is absent means "the owner never spoke",
not "off". `{}` is a normal, healthy file — a project nobody has configured yet.

The reader returns the full picture, and the difference is load-bearing:

```ts
import { featureOn, featureDecided } from "@/config/platform-config"

featureOn("topMenu")      // the VALUE: stored decision, or the code default
featureDecided("topMenu") // did the owner ever speak about it
```

`featureOn` is the only question worth asking in ordinary code. `featureDecided` exists for the rare
case where "never chosen" must behave differently from "chosen false" — use it only with a reason
written next to it. It was used once to let a build-time variable override the switch, and the result
was a panel that said OFF while the site showed the feature. That is gone; do not rebuild it.

🔒 **Server only.** The reader touches `fs` and is marked `server-only`. Resolve in a server
component and hand the boolean to an island as a prop. Importing it from a client component is a
build error, and that is the correct answer.

## 2. The eleven switches and where each is read

Measured in a browser on a live server, 2026-08-20 — not inferred from the code.

| Switch | Default | Read in |
|---|---|---|
| `topMenu` | on | `components/menu/top/top-menu.server.tsx` |
| `footerPages` | on | `components/menu/footer/footer-menu.server.tsx` |
| `cookieBanner` | off | `app/[lang]/layout.tsx`, footer menu (the "Cookie settings" button) |
| `auth` | on | `components/menu/account/account-config.ts` |
| `offlineCache` | on | `app/[lang]/layout.tsx` |
| `themeToggle` | on | footer menu — **both clusters**, desktop and mobile |
| `widthToggle` | on | footer menu, desktop cluster |
| `languageSwitcher` | on | footer menu — **both clusters** |
| `socials` | on | footer menu — the row of network icons |
| `breadcrumbs` | off | `components/content-page/page-header.server.tsx` |
| `faq` | off | `lib/content/create-content-post.tsx`, `create-content-page.tsx` |

🔒 **A switch is wired in ONE place, at the source.** `faq` gates the array itself, not the two
consumers (the visible block and the `FAQPage` structured data) — gate consumers separately and the
third one somebody adds later will be ungated, promising a machine what the page does not show. Same
reason breadcrumbs are gated where the component is mounted: `BreadcrumbList` markup lives inside it.

🔒 **The footer draws its buttons TWICE** — a desktop cluster and a mobile one. Gate one and the
feature stays alive on half the devices, producing a bug report that does not reproduce.

## 3. What each switch does NOT control

- **`footerPages`** hides the LINKS. The pages themselves keep answering: `/privacy` returns 200 with
  the switch off. Removing a page is a different job — see `use-static-pages`.
- **`languageSwitcher`** hides the BUTTON. The language set is `NEXT_PUBLIC_SUPPORTED_LANGUAGES`, and
  it decides the shape of every URL. Confuse the two and you break addresses, not a control.
- **`auth`** decides whether the public sign-in element renders. Which side the account drawer slides
  from is `nav.authSide` in `APP-CONFIG`.
- **`cookieBanner`** is a setting, never a deletion. Deleting the component to "turn it off" takes the
  switch away from every project built afterwards.
- **`socials`** hides the ROW. Which networks and which profiles is `seo.socialLinks` in
  `APP-CONFIG` — see `use-app-config`. The split is the owner's and it is right: "I don't want to
  see socials" is a question of the capability EXISTING, "which accounts are mine" is content.
  Before the switch existed, the row appeared merely because records existed, and the only way to
  remove it was to delete the data. The switch does **not** gate `sameAs`: hiding the row is a
  layout decision, while `sameAs` is the site's claim to machines that these accounts are its own.

## 4. Making a change visible

The app reads the file at render, but public pages are static with ISR. So:

- the panel purges the cache on save — the change shows on the next load;
- editing the file by hand does **not** purge anything: without a purge the page keeps its old HTML
  until the ISR window expires, up to ten minutes. That is the whole content of "I toggled it and
  nothing happened".

```bash
curl -X POST http://127.0.0.1:3000/api/revalidate \
  -H "Content-Type: application/json" -H "x-agent-identity: agent" -d '{}'
```

Never suggest a redeploy to make a switch take effect.

## 5. Do not build your own header, footer or consent strip

Both failures look like nothing until a human opens the page.

**Two stacked bars.** Yours answers to nobody: it is not in the config, so the panel cannot touch it,
and the owner's edits appear to do nothing.

**Static generation quietly lost.** A hand-rolled menu reaches for the current path to highlight the
active link, which pulls a client component that owns the route — and the page stops being
prerendered. The platform header avoids this deliberately: everything resolves on the server and
finished strings go to small islands as props.

```bash
npm run check:menu   # fails on a second sticky header carrying links
```

Facts that bite: menu labels are capped at 12 characters (`lib/menu/nav-config.ts`); nesting is
exactly one level; "menu on, zero buttons" is a valid state, not a defect; the account button and the
cart are always on the right.

## 6. A new switch lives in FOUR places, plus the panel

Adding a switch and finding it dead is the most common way to lose a day here. Only one of the four
omissions tells you anything.

| # | Where | Miss it and |
|---|---|---|
| 1 | `config/platform-config.defaults.ts` — the key in the union | the build fails, loudly. The only honest failure of the four. |
| 2 | `config/platform-config.defaults.ts` — the default value | an owner who never spoke gets `undefined` instead of a decision |
| 3 | **`config/platform-config.schema.ts`** | **validation strips the unknown key on save — silently.** The file on disk looks right, the reader falls back to the default, the switch looks broken. |
| 4 | `PLATFORM-CONFIG/{schema,defaults}.json` | `check:config-schemas` fails the build on the server |

Number three cost three separate detours in one day. Number four is generated, never hand-written:
`npm run build:config-schemas`. The fifth place — the form in the panel — is in another repository.

## 7. Defaults live in TWO repositories

`config/platform-config.defaults.ts` here, and `bridges/app/lib/platform-features.shared.ts` in the
panel. Duplicated on purpose — the panel is a foreign repository to this project — so **any change to
a default goes into both**, and the generated `PLATFORM-CONFIG/defaults.json` is rebuilt:

```bash
npm run build:config-schemas && npm run check:config-schemas
```

Skip that and the build fails on the server, not here.

🔒 `offlineCache` is deliberately absent from `FEATURE_ORDER` in the panel: the capabilities editor
writes only the keys listed there and carries the rest over from the existing config. Put it back into
that list and saving from one page starts wiping the choice made on another.

## 8. Before you call it done

1. Set the switch **off**, purge the cache, open the page in a browser, confirm the thing is gone.
2. Set it **on**, purge, confirm it is back. One direction proves nothing: a feature can be absent for
   its own reasons.
3. For anything with structured data (breadcrumbs, FAQ, socials), check the markup too — not only
   the pixels.

🔒 **Count ELEMENTS, not words.** Searching the HTML for `twitter` says nothing: the word also lives
in `sameAs`, in a class name, in a comment. Count `<a href=…>` in the footer instead. Measuring by
words once produced the confident verdict "the socials gate does not work" about a gate that worked.
4. `npm run check:menu`, `check:types`, and `check:config-schemas` if you touched a default.

🔒 Green gates are not proof. Four of these ten switches shipped dead for months with every gate
green: the panel offered them, the config stored them, and nothing read them. Only a browser told the
truth.
