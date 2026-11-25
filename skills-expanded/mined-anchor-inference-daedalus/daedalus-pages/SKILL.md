---
name: daedalus-pages
description: Build the operator's own screens inside the Daedalus app (dashboards, tools, viewers, forms, embedded web apps, anything) with the Page tools, make them native on phone and desktop, check, publish and put them on the rail.
requires: pages, services
---
# Custom pages

A custom page is a screen of the operator's own inside the Daedalus app, at `/app/p/<slug>`. It can
sit in the rail and the phone drawer, follows the app's theme, and works on a phone and a desktop.
People bring into Daedalus what they would otherwise open in a separate browser tab or app: a view
of your results, a specialised client for some service, a calculator, a 3D or CAD viewer, a form,
an existing web app. **There is no limit on what a page contains.** Any framework, any library,
any CDN, WebAssembly, workers, WebSockets, the whole `/api` with the operator's session. The
templates, the kit and the bridge below are starting points and conveniences, never constraints.

A page is data, not app code: creating, changing, publishing or rolling one back never rebuilds the
app, restarts anything or interrupts a session. A broken page breaks only its own frame.

The tools are the `pages` group: `PageCreate`, `PageWrite`, `PageImport`, `PageRead`, `PageFiles`,
`PageDelete`, `PageCheck`, `PagePublish`, `PageRollback`, `PageList`, `PageRemove`, `PageShow`, and for
a page's own agent `PageBind`, `PageEmit`, `PageStorage`.

## The workflow

1. **Agree what it is for** in one or two sentences, and pick the kind (below). Ask only what you
   cannot decide yourself.
2. **`PageCreate`** with a slug (`orders`, `cad-viewer`), a title — per language when the operator
   reads more than one (`{"en": "Orders", "ru": "Заказы"}`) — an icon, and a template.
3. **Build it.** Small pages: `PageWrite` the files. Anything bigger: build it in your workspace with
   whatever toolchain fits (npm + Vite, a static site generator, a Python script that writes HTML)
   and `PageImport` the output folder with `replace=true`. Binary assets (models, fonts, images,
   data) go in with `PageImport` too.
4. **`PageCheck`**: screenshots at 390×844 and 1440×900 in the dark theme and the light scheme, what a
   vision model saw on each, console errors, failed requests, missing files, overflow at phone width,
   small tap targets, whether the bridge shook hands. Fix what it finds and check again. It is advice,
   not a gate: you decide when the page is ready.
5. **`PagePublish`** with a one-line note. Every open app shows the new version at once.
6. **Show it**: `PageShow(slug)` puts a card with an Open button in the chat; link it in your answer as
   `[Orders](/app/p/orders)`. If the operator is away from this chat, `Notify` with
   `link="/app/p/orders"`.
7. **Put it on the rail** when the operator wants it there (see the end of this file).

Later changes repeat 3–5: the draft is separate from the live version until you publish. A bad
publish is undone with `PageRollback(slug, version)`; `PageList` shows the versions kept.

## The three kinds

| Kind | What it is | Target |
|---|---|---|
| `static` | files you write or import, served at `/pages/<slug>/` | — |
| `service` | a web app you run, reverse-proxied at `/pages/<slug>/` (any method, streaming, WebSockets) | a port of the services range, or the name of a service from `ServiceStart` |
| `link` | another site in a full-size frame, with a way to open it in a tab when it refuses framing | its `https://` address |

For a **service** page: start the server with `ServiceStart` (it gives the server `$HOST` and `$PORT` to bind), then
`PageCreate(kind="service", target="<service name>")`. The server sees
`X-Forwarded-Prefix: /pages/<slug>`; an app that builds absolute links needs its base path set to
`/pages/<slug>/` (Jupyter `--ServerApp.base_url`, Vite `base`, many apps have a `BASE_URL` setting) or
must use relative links. Publish to make the target live; change the port later with a new draft and
publish, and roll back like any other change. To wrap an app in a toolbar of the page's own, make the
service page and then a static page from `embed-service` that frames `/pages/<service-slug>/`.

## Building anything

- **Static files are served as they are**, each with its content type (`.wasm`, `.glb`, `.mjs`, fonts,
  video …). An address with no extension that names no file is the entry, so a client-side router
  survives a reload on any of its addresses.
- **Paths.** The page lives under `/pages/<slug>/`. Use relative paths (`./app.js`, `assets/x.png`),
  or set the bundler's base: Vite `base: "/pages/<slug>/"`, Next export `basePath`, CRA `homepage`.
  An absolute `/assets/x.js` points at the app, not the page.
- **CDNs are fine**: `<script type="importmap">` with jsDelivr or unpkg, a stylesheet from Google Fonts,
  a library's UMD build. So are `fetch` to other sites (when they allow it), WebSockets, workers.
- **The whole API**: the page is on the app's origin behind the operator's sign-in, so
  `fetch("/api/…")` carries the session cookie — sessions, files, the page's storage, anything the app
  itself calls. `Daedalus.api(path, init)` is the same with JSON handling (see reference.md).
- **Durable data**: the page's own storage — `Daedalus.storage.get/set/delete/list`, any JSON, on the
  server, shared across the operator's devices (`/api/pages/<slug>/storage`). Not `localStorage`,
  which is per browser. Data you prepare can also ship as a file of the page (`fetch("data.json")`).
- **Files from your workspace**: the operator's files and your results can be copied in with
  `PageImport` and read by the page as its own files.

## Looking native

`<link rel="stylesheet" href="/pages/_kit/kit.css">` gives the app's design tokens and a small set of
`dk-` components (toolbar, buttons, fields, cards, lists, tabs, badges, empty state, split pane). Use
them for chrome and forms so the page looks like the rest of the app; use the tokens
(`var(--bg)`, `var(--surface-1)`, `var(--fg)`, `var(--fg-2)`, `var(--accent)`, `var(--line)`,
`var(--space-3)`, `var(--radius-md)`, `var(--ctl-h)` …) in the page's own styles instead of fixed
colours. Classes and tokens are listed in `reference.md`. A page with its own design system, or a
framework's components, is fine too.

**Follow the theme**: `<script src="/pages/_kit/daedalus.js"></script>`. Inside the app it receives
the computed value of every token whenever the operator's look changes (a theme picked in Appearance,
the system turning dark, the window crossing the phone width) and writes them onto the page's root,
with `data-scheme` (`dark`/`light`), `data-theme` and `lang`. Anything styled with the tokens follows
by itself; a canvas or a chart library re-reads them in `Daedalus.theme.onChange(fn)` (the `viewer`
template shows how). Without the bridge the page keeps the kit's default dark look.

## Phone rules

The app runs on phones; a page that only works at desktop width is broken there.

- `<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">`, always.
- No fixed widths wider than the screen: `max-width: 100%`, `minmax(0, 1fr)`, grids that wrap
  (`dk-grid`), tables inside a box with `overflow-x: auto`. `PageCheck` reports anything that sticks out
  at 390 px and where it starts.
- Touch targets at least 40 px on a phone; the kit's controls already are (`--ctl-h` grows below
  1024 px). Text fields at 16 px, or Safari zooms on focus (the kit does this).
- Safe areas when opened full screen: `padding-bottom: max(var(--space-4), env(safe-area-inset-bottom))`.
- Below 1024 px the app is in its phone layout and the bridge's context says `phone: true`; stack side
  panels (`dk-split` does), put the primary action where a thumb reaches it.
- Gestures: `touch-action: none` on a canvas you drive with pointers, so the page does not scroll
  under a drag.

## The page's own words

The app tells the page the operator's language (`Daedalus.ready()` → `context.lang`, and every theme
push). Keep every string the page shows in a dictionary per language and render from it; the
templates all do it with a `STRINGS` object, `data-i18n` attributes and a `t(key)` function. Write
English and every language the operator uses (Russian, usually). The title is per language in
`PageCreate`.

## The templates

`PageCreate(template=…)` copies one into the draft, with `{{title}}` and `{{slug}}` filled. Each is
one small file, kit-based, phone-correct, theme-following and bilingual. Change everything.

| Template | Starting point for |
|---|---|
| `blank` | anything: a toolbar and an empty state |
| `dashboard` | numbers and a chart from any source, refreshed on demand |
| `split` | a tool and its agent working together: `agent.ask`, the agent's answers and runs, state shared through the page's storage and `PageEmit` |
| `viewer` | a three.js 3D viewer loaded from a CDN, opening glTF/GLB/STL, colours from the theme |
| `embed-service` | a toolbar of the page's own around a framed web app |
| `form` | a validated form whose entries are kept in the page's storage |

## The page and its agent

A page may have an agent of its own: the session bound to it. The session that runs `PageCreate` is
bound at once, so if you made the page, **you are its agent** until the operator (or `PageBind`) binds
another. The operator sees your conversation beside the page (in its place on a phone) and talks to
you there while looking at the page; they can change the agent, make a new one for the page, or
unbind it from the page's header.

- **From the page to you.** A button or composer in the page calls `Daedalus.agent.ask(text,
  {attachments, silent})`. Such a message reaches you opening with "(Sent from the page «Title»
  (/app/p/<slug>) …)": the operator pressed something in the page. With `silent` it says the page
  reports this itself (a selection, a state, an error): context, not an order; act on it only when it
  asks for something or matters to what you are doing.
- **From you to the page.** `PageEmit(slug, event, data)` reaches every open instance of the page as
  `Daedalus.on(event, fn)`: "scene rebuilt, reload model.glb", "new results", "select part 12". It is
  live only and carries at most 64 KB, so lasting state goes in the page's storage with
  `PageStorage(slug, "set", key, value)` (the page reads it with `Daedalus.storage.get(key)`) and the
  event only says it changed. Big things (a model, a dataset) go in as files with `PageImport` and the
  event names the file.
- **Your answers** reach the page too: when your run ends, the page's `Daedalus.agent.on("message")`
  gets your reply and `agent.on("run")` your run's state, so a page can show "working…" and the
  result without the operator opening the chat.
- **Publishing never interrupts.** `PagePublish` while the operator has the page open shows them a
  quiet "Version N is out · Reload" chip; nothing reloads under them. Prefer `PageEmit` with data
  over a publish for anything that changes while they work (a scene, numbers): a publish is for the
  page's code.
- Design a page that has an agent around that loop: the tool, a place where the agent's answer and
  state appear, and actions that ask the agent in plain words. Start from the `split` template.

## Checking

`PageCheck(slug)` runs in your own throwaway browser against a copy of the page served without the
operator's sign-in: `/api` requests answer 401 there (the result says so) and work in the app. The
screenshots are saved under `.page-check/<slug>/` in your workspace: `ImageView` one with a precise
question, or `SendFile` it to the operator. A CDN that is slow from this machine shows up as "did not
finish loading". `draft=false` checks the live version.

## Publishing, rollback, removal

- `PagePublish(slug, note)` makes the draft a new numbered version; the newest are kept (`[pages] keep_versions`, 20 by default).
- `PageRollback(slug, version)` makes any kept version live again; the draft is untouched.
- `PageRemove(slug, confirm=true)` deletes the page, every version and its stored values, for good.
  For a page that was ever published, ask the operator with `AskUser` first unless they asked for
  the removal themselves. Taking a page off the rail is a navigation change, not a removal.

## Putting it on the rail

A published page is in the app's list of pages at once. Where it sits is the `[navigation]` setting:
`rail` (the desktop rail, in order), `drawer` (the phone's list), `more` (under More), `hidden`, and
`icons` (an icon per item). A page's item id is `page:<slug>`. Read the current value first and keep
what is there:

```
SettingsGet("navigation")
SettingsChange({"navigation": {"rail": ["agents", "projects", "...the items already there...", "page:orders"]}})
```

Navigation applies without asking. Put the page on the phone's `drawer` too when the operator uses a
phone. If these tools are not available in this installation, tell the operator the page is at
`/app/p/<slug>` and that Settings → Navigation places it.
