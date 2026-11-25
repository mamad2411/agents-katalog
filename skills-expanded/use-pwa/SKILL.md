---
name: use-pwa
description: >
  The INSTALLABLE side of the site — per-language manifest, icons, iOS splash screens, the service
  worker and the install prompt. Load it when the owner says "make it installable", "add it to the
  home screen", "the icon is wrong", "it opens white when I launch it", "add offline", or when you
  touch `app/manifest.ts`, `app/[lang]/manifest.webmanifest`, `public/sw.js`, the register island, or
  the icon and splash generators. Two defects here are invisible from code: an app that cannot be
  installed at all because the manifest has no icons, and — the expensive one — a service worker
  serving yesterday's page, which also makes every measurement you take in the browser a lie.
---

# use-pwa

> Informational, not binding. **Know a better way for the case in front of you — do it your way and
> say so.** You are trusted with the creative work on this project.

**It is the same site, installed.** No store, no separate build, no second codebase — a manifest, a
worker and a browser that agrees the site is installable.

## 1. A manifest per language, not one per site

Every language links its own `/<lang>/manifest.webmanifest`; the root one stays for the default
language. They are all built by `lib/pwa/manifest.ts` — `check:pwa` refuses a manifest assembled
anywhere else.

An installed app is labelled on the home screen with the manifest's `name` and opens at its
`start_url`. One manifest for the whole site meant a Spanish visitor installed an English-named app
opening on the English home page, with no way to rename it afterwards.

- **`id` is mandatory** — ours is the language's start address. Without it the system identifies an
  installation by `start_url`, so connecting a domain later creates a SECOND app beside the first
  instead of updating it: two identical icons on the user's screen.
- **`name` is the site name, not the page title.** The title runs through the `%s | Site` template and
  reaches the home screen as "Shop | Ivanov's Shop". Found by reading a live manifest, not by thinking.
- **`themeColor` is declared for both colour schemes** in `generateViewport`, or the status bar on a
  dark phone is painted the wrong colour and the app looks foreign.

## 2. Icons and splash screens are files, and the gate checks the files

The owner uploads one image and the panel cuts the set (192, 512, **maskable**, `apple-touch-icon`,
favicons including `.ico`) into `iconSet`, which overrides everything else. Until then the project
ships neutral starter icons in `public/icons/` from `npm run icons:default` — because a manifest
without icons means exactly one thing: **the app cannot be installed**, and all the rest of this work
is unreachable.

- **`maskable` is a separate file**, not the same picture declared twice: Android crops the icon to its
  shell's shape (circle, squircle, teardrop) and an icon without margin loses its edges.
- **iOS splash screens are mandatory** — `apple-touch-startup-image` per resolution, portrait and
  landscape, declared once in `components/pwa/ios-splash.tsx` and drawn by the same generator. Android
  takes the background colour from the manifest and needs no raster; iOS picks a bitmap by media query
  and, finding none, paints a **white screen** on launch. On a dark theme that reads as a flash and a
  fault, and it is the first thing a person sees after installing.
- `check:pwa` compares what is declared against what is on disk. A declaration without a file is
  invisible otherwise — only the owner of that particular phone ever sees it.

## 3. 🔒 The worker never serves a document from cache first

`public/sw.js`, and this is the law of the file:

| Request | Strategy |
|---|---|
| documents (HTML) | **network first**; cache only when there is no network |
| hashed static (`/_next/static/…`) | cache — the address changes with every build, so it cannot go stale |
| everything else (api, images) | the worker does not touch it at all |

The reason is doubled here: the control panel changes texts and settings **without a rebuild**, so a
cached page diverges from the real one the same minute. `check:pwa` fails a worker that serves
documents from cache, and that rule was verified with a negative control.

Two details that were bought with a real half hour:

- **The first-visit page is cached on `activate`.** The worker is born AFTER the page it was born on,
  so that page passes it by; a visitor who lost the network on it got a browser error on something they
  saw a second ago. On activation the worker asks `clients.matchAll()` which pages are open right now
  and stores exactly those — no guessing about the future, the page is already on screen.
- **The offline branch reads the cache twice** — by request object and by URL string — because that
  first-visit entry was written under a string key and a match by object is not obliged to find it.

**Offline covers pages already seen, and nothing else.** There is no offline page for unvisited
addresses, deliberately: it would need words in every language. That absence is named, not forgotten.

**No worker outside a secure context.** `localhost` and https addresses (the temporary one, the own
domain) are secure, so the worker registers there; any other plain-http address gets none. The app
works fully; only offline is missing. Never report a worker as broken on such an address.

## 4. 🔒 The worker also makes your browser measurements lie

A registered worker serves the previous build's document from cache in exactly the situation where you
are checking whether your change arrived. The half hour it cost on 2026-08-21 is the reason this
paragraph exists.

Before measuring anything in a browser: unregister the worker **and** clear `caches` — caches outlive
`unregister` on their own, so doing one of the two proves nothing. A hard reload alone is not enough.
The register island (`components/pwa/register-sw.client.tsx`) can unregister as well as register.

## 5. The install button waits for the browser

It appears only after `beforeinstallprompt`, and a dismissal is remembered for 30 days. A button drawn
earlier either does nothing or nags: only the browser can open the install dialog, and it sends that
event only when the site is genuinely installable (manifest with icons, https, worker) and the visitor
showed interest. We draw our own because the browser hides its offer in a menu, where only someone who
already knew about it will look.

Its two strings live in `components/pwa/install-prompt.i18n.ts` in **82 languages** — a reusable part
of the product appears in any language the owner switches on, the same minute. The dictionary resolves
on the SERVER and travels as a prop; 82 languages have no right to reach the browser.

## 6. Before you call it done

- `npm run check:pwa` — manifest through the shared builder, per-language manifest present and linked
  from the layout, required fields, `maskable`, every declared icon and splash present on disk, the
  register island wired in, and no document-from-cache.
- `curl /ru/manifest.webmanifest` — `lang`, `name`, `start_url` and shortcuts in that language.
- In a browser, on HTTPS: install it, launch it from the home screen, and look at the launch screen
  and the label. Clear the worker and caches FIRST, or you are grading the previous build.
- 🔒 **Proving network-first WITHOUT a phone — plant a stale copy** (done live 2026-08-22). Comparing
  the cached page with the network one proves nothing: a successful fetch has just rewritten the
  cache, so both agree whichever strategy is in force. Instead put a KNOWN-FALSE document into
  `pages-v1` under a real page address, then request that address with an `accept: text/html` header
  (the worker treats it as a document — see its `isDocument`). The planted copy must NOT come back.
  The test cleans up after itself: the successful network response overwrites what you planted.
  A check that cannot fail proves nothing — this one can, and that is the whole point of it.
- Say plainly which half you proved. "Built and served" is honest; "PWA works" requires a phone.
