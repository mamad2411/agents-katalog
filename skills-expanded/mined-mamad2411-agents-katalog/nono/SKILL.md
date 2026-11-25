---
name: nono
description: Authoring this Nono (.nono) site — the spite-driven static site generator's SwiftUI/Elm-flavoured DSL. Use when writing or editing .nono files in this project, adding pages/layouts/content, working with slots, optional params, fn functions, the standard library, head { } hoists, or nono.toml build steps.
---

# Nono

This project is a **Nono** site. Nono is a static site generator with its own
DSL: you write `.nono` files (markup components) plus Markdown, and `nono build`
compiles them to static HTML. It ships **nothing** to the browser: no JS, no
runtime, no hydration. Everything resolves at build time. The pipeline is
parse → evaluate → emit HTML.

If you scaffolded this with `nono new`, you already have a working blog: a home
page with an about blurb and a linked post list, an about page, a posts layout,
shared chrome in `lib/` (a `Shell` with `Header`/`Footer`, plus `Prose` and
`PostCard`), several posts in `content/posts/`, and a Vercel deploy workflow.

Styling is **Tailwind** (v4): `assets/app.css` is compiled to `static/styles.css`
by the build step in `nono.toml`, and `SiteHead` links it. So: run `npm install`
once, then `nono dev` to preview. Components use Tailwind utility classes; the
build step re-runs Tailwind on every reload, so new classes appear on refresh.

## The shape of a project

```
your-site/
  pages/      .nono files, one component each, routed to HTML
  layouts/    .nono files, one component each, wrap markdown pages
  lib/        shared components + stylesheet, loaded into every page
  content/    .md files, each routed to HTML in its own right
  static/     copied verbatim into the output
  nono.toml   optional config (build steps)
```

The filesystem is the router, and it routes two things:
- `pages/about.nono` → `about/index.html` (vanity URLs); `pages/index.nono` → `index.html`.
- `content/posts/x.md` → `posts/x/index.html`, wrapped in a layout.
- Path segments must match `[a-z0-9-]` or it's a hard build error.

## CLI

```sh
nono new   --path path/to/site   # scaffold from the blog template
nono build path/to/site --out out
nono dev   path/to/site          # http://127.0.0.1:6969, rebuilds per request
nono parse file.nono             # dump the AST (debugging)
```

## Language

### Components and elements

```nono
component Post(title: string, date: string) {
  article {
    h1 { "{title}" }
    time(datetime = date) { "{date}" }
    Slot()
  }
}
```

- **Capitalised name = component** (must be defined). **lowercase = HTML element**
  (must be a known tag). The allowlist covers most of HTML5 — structure, text,
  tables, forms, media, `details`/`summary`/`dialog`, and a basic SVG set — so an
  unknown lowercase name is treated as a typo and errors loudly.
- Attributes are named args: `p(class = "Prose")`, `a(href = "/x")`. Attribute
  names may contain hyphens (`data-level`, `aria-label`); plain identifiers may
  not (so `a-b` is subtraction).
- Text is a string literal `"..."`. Interpolate with `{expr}`: `"{title}"`,
  `"{track.artist["#text"]} - {track.name}"`.

### `=` binds, `:` types

`title = "x"` is an argument; `title: string` is a type. They never collide.
Types are decorative (not enforced); use `string`, `number`, `list`, etc.

### Optional params

`name?: type` marks a param optional. Omit it at the call site and it binds
`nil`; branch on it with `if`. This is how you do conditional/layout composition
without a portal system.

```nono
component Hero(title: string, subtitle?: string) {
  h1 { "{title}" }
  if subtitle != nil {
    p(class = "subtitle") { "{subtitle}" }
  }
}

Hero(title = "Nono")                          // subtitle is nil, <p> skipped
Hero(title = "Nono", subtitle = "spite SSG")  // <p> renders
```

A param without `?` is required; omitting it is a hard error. `nil` is falsy, so
`if subtitle { ... }` works too; `== nil` / `!= nil` are explicit.

### Slots (content passed down into a component)

```nono
component Layout(heading: string) {
  main  { h1 { "{heading}" } Slot() }              // default (unnamed) slot
  aside { Slot(named = "sidebar", or = nil) }      // named, optional
}

// filling it:
Layout(heading = "Home") {
  sidebar = { h2 { "Links" } }   // fills the named slot
  Prose { "the body" }           // unnamed content fills Slot()
}
```

- `Slot()` is the default hole; `Slot(named = "x")` a named one.
- `name = { ... }` inside an invocation fills a named slot; trailing content
  fills the default. `or = nil` makes a slot render nothing when unfilled.
- A named slot is filled at most once (filling twice is an error). Fills flow
  **down** from caller to callee and capture the caller's environment, so a fill
  referencing an enclosing `for` binding resolves correctly.

### `const` and `fn`

```nono
const posts = glob("content/posts/*.md")        // bind-time; data sources run here
fn greeting(name: string) = "hello, {name}"     // value-returning function
```

`const` is bind-time (top-level or block-local; there is no `var`). `fn` returns
a value (distinct from a component, which returns markup).

### Control flow

```nono
for post in posts { Prose { "{post.title}" } }

if post.draft { p { "draft" } } else { p { "live" } }

match post.kind {
  Note  => Prose { "{post.title}" }
  Essay => Post(title = post.title, date = post.date) { Slot() }
  _     => nil
}
```

### Expressions

Literals `number`, `true`/`false`, `nil`, `string`. Paths `a.b.c`. Calls
`f(x = 1)`. Field access `post.title`. Bracket indexing `x["#text"]` (string key,
for JSON keys that aren't identifiers) and `xs[0]` (list index). Operators
`== != < <= > >= + - * /`.

Collection literals let you author data inline (no data source needed):

```nono
const nav = [
  { label = "Home",  href = "/" },
  { label = "About", href = "/about/" },
]
```

`[ ... ]` is a list, `{ key = value }` a map (keys are plain idents; values are
any expression, so lists and maps nest). Literals can carry accessors:
`[10, 20][1]` is `20`, `{ a = 1 }.a` is `1`. Note: a bare `{ ... }` after `name =`
in a component invocation is a slot fill (a block), not a map — wrap a map in
parens there, `name = ({ a = 1 })`, or bind it to a `const` first.

**No operator precedence** — expressions are strictly left to right, so
`1 + 2 * 3` is 9, not 7. Parenthesise or reorder if it matters.

### Stylesheet block

```nono
stylesheet {
  Prose { max-width = 65ch; line-height = 1.6 }
}
```

Compiles to an inline `<style>` in every page's head. For external CSS, see
`head { }` below.

## Builtins and the standard library

Builtins are deliberately generic: `glob("content/**.md")`, `markdown(file = ...)`,
`http_get("https://...")` (returns parsed JSON as a value), `env("NAME")` (errors
if unset). There are no service-specific builtins.

The standard library (`src/std.nono`, compiled into the binary, loaded into every
project) is plain Nono built on those:
- `lastfm_recent(user, limit)` — recent scrobbles (reads `NONO_LASTFM_KEY`).
- `TableOfContents(headings = ...)` — a `<nav class="toc">` of anchor links.

Shadow any of them by defining your own with the same name.

## Markdown values

`glob(...)` and `markdown(...)` return a Map per file with: `title`, `date`,
`kind` (defaults `Essay`), `draft` (defaults `false`), `path`, `slug`, `html`
(rendered body, raw), and `headings` — a list of `{level, text, id}`, with a
matching slug `id` on each heading in the body. `draft: true` keeps a file out of
the build entirely (no page, and it drops from `glob` listings too).

## Layouts (the markdown half)

A `.md` page picks its layout: a `layout:` frontmatter field (resolved by
filename), else the parent directory name (`content/posts/` → `layouts/posts.nono`),
else `layouts/default.nono`, else a loud error. The layout's params are filled
from frontmatter; the rendered body lands in its `Slot()`. That `Slot()` can be
handed down through another component, e.g. `Post(...) { Slot() }`.

## `head { }` — contribute to the document head

```nono
component SiteHead {
  head {
    link(rel = "stylesheet", href = "/styles.css")
  }
}
```

A `head { }` block is lifted into the document `<head>` from wherever it renders,
and blocks from across the whole component tree are combined. So a shared
`SiteHead` dropped into each top-level page component links your CSS once, in the
head. Put it only in once-per-page roots (not in a reused component, or you get
duplicates).

## nono.toml (the build stage)

```toml
[build]
# Shell commands run in order before each build (including every `nono dev`
# reload). Use them for Tailwind, esbuild, a sass compile, etc. Keep them quick;
# do `npm install` by hand. Two path tokens are substituted first:
#   <rootDir>    the project root
#   <publicDir>  the static/ directory (its contents become the site root)
steps = ["npx @tailwindcss/cli -i assets/app.css -o <publicDir>/styles.css --minify"]
```

nono links nothing for you — the build stage just produces static assets; you
link them with a `head { }` block. Config is optional; no `nono.toml` means no
build steps.

## Hard rules and gotchas

- **A page or layout file is exactly one component.** Helpers go in `lib/` (which
  may define as many as you like). Two components in a `pages/` or `layouts/`
  file is a hard error.
- Capitalised = component, lowercase = HTML element. An unknown lowercase tag is
  an error.
- No operator precedence (left to right).
- `=` binds, `:` types; identifiers can't contain hyphens, attribute names can.
- Data source failures (a bad `http_get`, an unset `env`) abort the build loudly,
  by design. Pair flaky sources with `or =` on a slot or a periodic rebuild.

## A minimal page

```nono
// pages/index.nono
const posts = glob("content/posts/*.md")

component IndexPage {
  SiteHead()
  main {
    h1 { "Posts" }
    for post in posts {
      article { h2 { "{post.title}" } }
    }
  }
}
```
