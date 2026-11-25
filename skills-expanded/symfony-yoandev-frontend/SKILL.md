---
name: symfony-yoandev-frontend
description: >-
  Build and debug the front end of a Symfony application with AssetMapper, Twig,
  Stimulus, Turbo and Symfony UX — no bundler, no Node build step. Use this skill
  whenever someone asks to make a page interactive, add a filter or a live search, add
  an autocomplete or a dropdown, add a JavaScript library, style a page or set up
  Tailwind, add an icon, build a reusable Twig component or a Live Component, add Turbo
  Drive, Frames or Streams, write a Stimulus controller, organise templates or
  translation keys, or set a form theme. Also use it for the failures: "my JavaScript
  does not run", "my JS stopped working after clicking a link", "the CSS did not
  update", "the page is slow to load", "the assets 404 in production", "the images are
  served by PHP", "importmap:audit is failing" — and whenever the question is *where* a
  piece of behaviour belongs, between a Stimulus controller, a Live Component and a
  Twig Component.
---

# Frontend

> **Tier: core the moment there is a front end** — AssetMapper, Stimulus and the no-bundler rule. Live Components, Mercure and every UX package are on demand — add them when the need appears, as the tables below say.

Twig, Stimulus, Turbo and Symfony UX, served by AssetMapper. No bundler.

```bash
symfony console importmap:require chart.js   # add a JS dependency
symfony console debug:asset-map              # what is actually mapped
symfony console importmap:audit              # vulnerable JS dependencies
symfony console asset-map:compile            # deploy step — see below
```

## The price of no bundler, stated once

AssetMapper serves your files as ES modules with an import map. There is no
compilation step, so there is **no JSX, no Vue or Svelte single-file components, no
TypeScript, no advanced transpilation**, and no tree-shaking of a dependency you only
use a corner of.

That is the deal, and it is not renegotiated per feature. If a request genuinely needs
a JavaScript framework with a build step, say it is out of scope rather than quietly
introducing a bundler — a bundler is a second toolchain, a second lockfile, a second CI
job and a second thing that breaks on a Node upgrade. (For orientation on an existing
project only: **Webpack Encore is now Symfony's legacy option** and **`symfony/reprise`**
is the official Vite/Rsbuild integration. Neither belongs in a project already on
AssetMapper.)

## The production trap

This is the part people get wrong, and it is why "AssetMapper is slow" is a widespread
belief. **AssetMapper concatenates nothing** — a page pulls dozens of small files. That
is fine, better than a bundle for cache granularity, under two conditions:

- **HTTP/2 or HTTP/3.** Over HTTP/1.1 the browser opens six connections and queues the
  rest; many small files then lose to one bundle, decisively. HTTP/2 is a
  **prerequisite, not an optimisation**. `symfony server:start` gives it locally,
  Caddy/FrankenPHP gives it in production; a naked HTTP/1.1 nginx does not.
- **Compression.** Each file is small; the wins come from brotli/zstd/gzip. Since
  Symfony 7.3, `framework.asset_mapper.precompress: true` writes `.br` / `.zst` / `.gz`
  next to each compiled asset for the web server to serve directly. On 6.4–7.2 there is
  no such option — compress at the web-server level. The rule does not change, only the
  means.

And the deploy step that decides whether any of this matters:

```bash
php bin/console asset-map:compile
```

Without it, `framework.asset_mapper.server` picks up the slack and serves every asset
**through the PHP process** — a full kernel boot per image, per stylesheet, per module.
The site works, which is exactly the problem: nobody notices until the traffic does.
(The rest of the deploy sequence belongs to `symfony-yoandev-deployment`.)

## Adding a JavaScript dependency

```bash
symfony console importmap:require chart.js   # pin it in importmap.php
symfony console importmap:install            # restore assets/vendor/ from it
symfony console importmap:outdated           # what has moved
symfony console importmap:audit              # known vulnerabilities
```

`importmap:audit` **belongs in CI**, next to `composer audit`. With no npm anywhere in
the loop, nothing else will ever report that a pinned JavaScript package has a
published advisory. It is the most-forgotten check on this stack.

## Where behaviour lives: follow the state

One question decides it, every time: **where does the state live?**

| State lives… | Use | Because |
|---|---|---|
| In the browser only | **Stimulus controller** | Nothing to ask the server: a dropdown open/closed, copy-to-clipboard, a character counter, drag-reorder before saving |
| On the server, **remembered from one interaction to the next** | **Live Component** | The server owns it and must re-render *with* it: a filtered book list, a search, a form validated as you type, a paginated table |
| On the server, with **nothing to remember** | **A controller returning a Turbo Stream** | One submission, several zones to refresh, no value carried between round trips — see the arbitration below |
| Nowhere — it is rendering | **Twig Component** | A function from props to HTML: a badge, a book card, a rating display, a modal shell |

The failure modes this prevents are specific: a Stimulus controller that filters in
JavaScript duplicates a rule that already lives in a repository, and the two drift; a
Live Component used for a visual toggle sends an HTTP request to open a menu; a Twig
Component given mutable state grows a re-render mechanism nobody asked for.

## Live Component, Stream response, pushed Stream

Three tools update part of a page from the server. **One question arbitrates, and it is
answerable without taste:**

> **Is there state to remember between two interactions?**
>
> - **Yes** → **Live Component.** The state *is* the component.
> - **No, and the user acted** → **a Turbo Stream returned as the response to that
>   submission.**
> - **No, and the user did not act** → **a Turbo Stream pushed** over Mercure.

| The interaction | Tool | Why that one |
|---|---|---|
| A filter that remembers what it is filtering on, a search refining as you type, a form validated field by field, a multi-step wizard | **Live Component** | The value must survive the round trip *and come back rendered*. That is exactly what a serialised `LiveProp` buys |
| A form POST after which several disjoint zones must change — the list gains a row, the counter goes up, a flash appears | **Turbo Stream response** (`text/vnd.turbo-stream.html`) | Nothing to remember: one submission, one response, several targets. No component class, no state in the DOM, one round trip |
| A notification, a change made by another user, progress on an async task | **Turbo Stream pushed** over Mercure | Nobody clicked. There is no request to answer, so the server has to open one |

The reasoning behind the first row: a Live Component round trip returns *the component's
own rendered state* — no target ids to name, no fragment template to keep in step with
the full-page render, props preserved between interactions. That machinery costs a
component class, a lifecycle to understand and an HTTP request per interaction, and it
only pays when there is state for it to carry. A component whose props are identical on
every render is a controller with extra steps.

The reasoning behind the second: answering a form submission with a stream is Turbo's own
documented primary usage, and it is stateless by construction. You name the targets and
you write the fragments — that is the price — but there is nothing to serialise into the
DOM, nothing to rehydrate and nothing to remount. Reach for it as the **default** as soon
as one submission must touch two zones that a single Drive navigation or a single frame
cannot cover together. The controller side is a request format and a template:
`references/turbo-and-stimulus.md` has the worked example.

The third row is the unchanged one, and the expensive one: **a Mercure hub is another
process to run, monitor and secure**, with its own JWT configuration and reachable from
the browser. "Add a live notification" is an infrastructure decision, not a template
change. Say so before proposing it.

Two warnings survive the arbitration, because they are about the tools rather than about
the choice between them:

- **A Live Component remounts on every interaction.** Constructor, `mount()`, prop
  rehydration, full render — per keystroke. An expensive `LiveProp`, or a render path
  that fans out into a dozen queries, does not make the page slow, it makes it unusable.
- **A `#[LiveAction]` is a publicly postable endpoint.** The route is
  `ux_live_component` and anyone can post to it; the fact that its button only renders
  for admins protects nothing. It needs `#[IsGranted]` exactly as a controller action
  does.

## Components take DTOs, never entities

```twig
<twig:BookCard :book="book" />   {# book is a BookCardView, not a Book entity #}
```

A Twig template holding a Doctrine entity triggers lazy loading from inside rendering:
`book.author.name` in a loop is an N+1 nobody sees in the code, and
`book.ratings|length` hydrates every rating row to count them. Those queries happen in a
template, far from any repository, invisible to a service-level test. Pass a DTO — a
read model built by the service, with exactly the fields the component renders. For a
Live Component it is doubly binding: a `LiveProp` is serialised into the DOM and
rehydrated on every interaction, so an entity there means an ORM round-trip per
keystroke.

**The Live Component trap:** every interaction is an HTTP request and the component is
re-instantiated — `mount()` runs again, props rehydrate, dependencies are re-injected,
anything held in a plain property is gone. Treat "how many queries does one keystroke
cost" as a real question. Details: `references/components.md`.

## Turbo

`ux-turbo` is three things with three different scopes:

- **Drive** — intercepts links and forms, fetches the page, swaps the `<body>`. On by
  default once installed.
- **Frames** — `<turbo-frame id="…">`; a link inside it replaces only it.
- **Streams** — fragments (`append`, `replace`, `remove`, …) applied to targets. They
  reach the page two ways: as the **response to a form submission** (Turbo asks for
  `text/vnd.turbo-stream.html` on every non-GET submission, so the controller only has
  to answer in that format), or **pushed** over Mercure with nobody interacting.

**Drive changes the page lifecycle, and that is what it breaks.** `DOMContentLoaded`
fires once, on the first load, and never again — any script assuming it runs per page
stops working after the first navigation. Turbo also compares `<head>` between
navigations, so anything in there that changes per request (a nonce, a timestamp) forces
a full reload. The fix is not a workaround, it is the rule below: behaviour lives in a
Stimulus controller, whose `connect()` runs on every insertion, Turbo swaps included.
See `references/turbo-and-stimulus.md`.

## Stimulus

- **One controller per behaviour**, named after what it does, not where it sits:
  `clipboard_controller.js`, `character_counter_controller.js` — not
  `book_page_controller.js`.
- **No inline `<script>` in a template.** It runs once, does not survive a Turbo
  navigation, cannot be reused, and is invisible to `importmap:audit`. The one
  exception is a `<script type="application/json">` data island read by a controller.
- **No business rule in JavaScript.** A threshold, a price, an eligibility check
  decided client-side *will* diverge from the server's — and the server's is the one
  that counts. JavaScript may display a rule; it may not own one.

## Tailwind, without Node

```bash
composer require symfonycasts/tailwind-bundle
symfony console tailwind:init
symfony console tailwind:build --watch      # during development
```

The bundle downloads the standalone Tailwind binary — no `npm`, no `node_modules` — and
registers an AssetMapper compiler, so `assets/styles/app.css` is processed on the fly in
dev and at `asset-map:compile` time in production. Pin `binary_version` in
`config/packages/symfonycasts_tailwind.yaml`: unpinned, a Tailwind major arrives on
whichever machine builds next. The form theme is declared **once**, globally:

```yaml
# config/packages/twig.yaml
twig:
    form_themes: ['tailwind_2_layout.html.twig']
```

Never `{% form_theme form '…' %}` in a template. Per-template themes are how a project
ends up with three form styles and no way to change all of them at once.

## Symfony UX packages: add when the need appears

| Package | The need it answers |
|---|---|
| `symfony/ux-icons` | `{{ ux_icon('tabler:book') }}` — any icon, inlined SVG, no icon font |
| `symfony/ux-autocomplete` | Essential the moment an `EntityType` passes a few dozen options: a `<select>` with 5 000 `<option>`s is a slow page and an unusable one |
| `symfony/ux-chartjs` | Chart.js from a PHP-built dataset |
| `symfony/ux-toggle-password` | The show/hide eye on a password field |
| `symfony/ux-lazy-image` | Blurhash placeholder plus native lazy loading |

Install none of them pre-emptively — each adds a bundle, a Stimulus controller and a
line in `importmap.php`. Production note for `ux-icons`: on-demand Iconify downloads are
**on by default**, so a missing icon is fetched from a third-party API at render time.
Run `ux:icons:lock` to import every icon used into `assets/icons/`, and disable
on-demand outside dev.

## Twig conventions

- **snake_case** template names and directories: `templates/book/show.html.twig`.
- **Fragments prefixed `_`**: `_book_row.html.twig`. The prefix says "not a page, not
  routable, included by something".
- **Three-level inheritance**: `base.html.twig` (document, `importmap()`, meta) →
  `layout/*.html.twig` (a section's chrome) → the page. Pages extending `base` directly
  duplicate chrome; four levels become unfollowable.
- **Translation keys name intent, not text**: `book.delete.confirm`, not
  `Are you sure?`. Format **XLIFF**, one file per domain and locale — a key that *is*
  the English sentence changes identity the day the wording changes.
- **`asset()` and `path()`, always.** A hardcoded `/assets/app.js` bypasses the digest
  and is served stale forever; a hardcoded `/books/12` breaks when the route moves.
- Twig filters and functions via **`Twig\Attribute\AsTwigFilter`** / `AsTwigFunction` /
  `AsTwigTest` — namespace `Twig\`, from `twig/twig` itself, not a Symfony one — rather
  than an `AbstractExtension` class. Twig 3.12+; below that, write the extension class.

## When the front end misbehaves

| Symptom | Cause |
|---|---|
| 404 on `/assets/…` in production | `asset-map:compile` was not run at deploy |
| Assets load but every request boots PHP | Same cause: `asset_mapper.server` is covering for it |
| Slower than the old bundle | HTTP/1.1, or no compression. Check the protocol before touching code |
| JS works, then stops after clicking a link | An inline `<script>` or a `DOMContentLoaded` listener; Turbo Drive swapped the body |
| A Stimulus controller never connects | File must be `name_controller.js` under `assets/controllers/`, element `data-controller="name"` |
| CSS changes do not appear | No `tailwind:build --watch` running, or a stale `public/assets/` from a previous compile |
| Full page reload on every Turbo navigation | Something in `<head>` differs per request |
| `importmap:audit` fails the build | Correct: a pinned JS package has an advisory. `importmap:update` it |
| A Live Component "loses" a value between clicks | The property is not a `LiveProp`, so it is not part of the serialised state |
| A list page issues hundreds of queries | An entity reached a template. Pass a DTO |
| A stream response is downloaded instead of applied | The response went out as `text/html` — `$request->setRequestFormat(TurboBundle::STREAM_FORMAT)` was not called |
| A stream response arrives but nothing moves | `targets` takes a **CSS selector**, so a bare id matches nothing. `targets="#book_list"`, or `target="book_list"` |

## Reference files

| File | When to read it |
|---|---|
| `references/assetmapper.md` | Adding a dependency, CSS and Tailwind, CSP, preloading, debugging a missing or stale asset, the production checklist |
| `references/components.md` | Writing a Twig or Live Component, props and DTOs, forms in a Live Component, testing components |
| `references/turbo-and-stimulus.md` | Turbo Drive/Frames/Streams, Mercure, the page lifecycle, writing and debugging a Stimulus controller |
