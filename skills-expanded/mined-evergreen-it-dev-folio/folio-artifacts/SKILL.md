---
name: Folio Artifacts
description: Build and publish interactive pages (kind artifact) with publish_artifact — dashboards, calculators, filterable reports, charts; the HTML rules, the CDN allowlist, state with window.storage, replacing an artifact.
version: "1.0.0"
tags: [folio, artifacts, html]
---

# Folio artifacts (`kind: artifact`)

An artifact is an interactive page: HTML + JS (+ files) that runs in a
sandboxed frame inside Folio. Use it when the user wants something a markdown
page cannot do: a dashboard, a calculator, a filter or a chart that reacts to
input, a small tool. A document never holds `<script>`/`<iframe>` — the
sanitizer removes them — so interactive content always goes into an artifact.
An artifact is in the tree, search, trash and Git like any page, but it is not
edited in place: you replace it whole.

Only in `AGENT` mode (`publish_artifact` is a write tool).

## `publish_artifact`

| Input | Meaning |
|---|---|
| `space` | Space slug (required) |
| `id` | Replace this artifact (its page id). Omit to create a new one |
| `parentPath` | New artifact only: folder from the space root (`""` = root), e.g. the folder of the current page |
| `title`, `icon` | Page title (default: the HTML `<title>`) and an emoji |
| `html` | The entry page: ONE complete, self-contained HTML document |
| `text` + `type` | Raw `svg` / `markdown` / `mermaid` text instead of `html`; Folio wraps it into a page |
| `files` | Extra files next to the entry (`path`, `content`, `encoding`: `utf8` or `base64`), referenced from the HTML by relative path |
| `entry` | Entry file when it is not `index.html` |
| `sourceCode`, `sourceFileName` | The original JSX/TSX, kept verbatim next to the page (with `type: react` or `canvas-tsx`) |
| `type` | `html` (default), `react`, `svg`, `markdown`, `mermaid`, `canvas-tsx` |
| `origin`, `capabilities`, `properties` | Where it came from (`other` for something you built), what it needs from its host besides storage, page properties |

The `url` and `embedCode` inputs of the public MCP tool are not available in
the built-in chat: write the page yourself.

The reply has `id`, `space`, `path`, `title`, `created`, `url` and `warnings`.
Tell the user about the warnings. End the answer with the link
`[<title>](/s/<space>/p/<id>)`.

## Rules for the HTML

- One file that runs with no build step and no server. Inline the CSS, the JS
  and the DATA (the numbers the page shows come from what you read with the
  tools; paste them into the page as JSON).
- No `fetch` of any API, including Folio's own: the frame has an opaque origin
  and a strict security policy. Whatever the page needs must be inside it.
- Scripts, styles and fonts may load only from `cdnjs.cloudflare.com`,
  `cdn.jsdelivr.net`, `unpkg.com`, `cdn.tailwindcss.com`, `code.jquery.com`,
  `esm.sh` (and Google Fonts). Pin a version in the URL, for example
  `https://cdnjs.cloudflare.com/ajax/libs/react/18.3.1/umd/react.production.min.js`.
- React: load React + ReactDOM (+ `@babel/standalone` for a
  `<script type="text/babel">`), or use `<script type="module">` with imports
  from `https://esm.sh/react@18`. Plain HTML + vanilla JS is simpler and
  enough for most pages — prefer it.
- Make it readable on its own: a title, a short note on what the data is and
  as of when, labels on charts and inputs. Work in a narrow frame too.
- State: `window.storage` (async `get`, `set`, `delete`, `list`; string
  values; `shared: true` is seen by every reader) and `localStorage` persist
  per reader. `window.claude.complete` does not work.

## Order of work

1. Read what the page shows (`read_page`, `folio_table_query`, `search_pages`)
   before writing it, so the data in the page is real.
2. Create it with `publish_artifact` (`space`, `parentPath` from the current
   context unless the user said otherwise).
3. To change an artifact: `read_page` it — you get `artifact.manifest`, the
   file list and `entryHtml` (cut at 60 000 characters; `entryTruncated` says
   so) — then `publish_artifact` with its `id` and the WHOLE new HTML. Title,
   icon and properties are kept unless you send new ones. Do not replace an
   artifact whose entry you could only read partly, unless the user asked for
   a rewrite.
4. Confirm with the link; say that the data is a snapshot (it is not live)
   when the page shows numbers read from Folio.

## Not an artifact

Text, tables of figures, lists, diagrams that do not need interaction: a
document (`folio-content`, Mermaid in a fenced block), a data table
(`folio-tables`), a whiteboard (`folio-boards`).
