---
name: richdocs
description: "Generate and serve rich HTML companions to markdown discovery documents: paired markdown→HTML rendering (marked + mermaid + data-driven cytoscape/plotly fenced blocks), a vendored draw.io stencil library (~AWS/GCP/Azure/K8s SVG icons) for composing custom architecture diagrams, an injectable design-tokens brandpack, and a reliable localhost server for HTML that pulls pinned CDN libraries. Use when turning a review/architecture/cost markdown doc into an interactive HTML view, when a diagram needs real cloud provider icons, when serving local HTML that file:// breaks, or when building a data-driven graph/chart view. Skip when the deliverable is plain mermaid-in-markdown authoring with no HTML companion, or a Python-rendered architecture diagram image."
argument-hint: "[markdown-file | stencil-search-term]"
user-invocable: true
---

# richdocs — rich HTML companions for discovery docs

Markdown stays the source of truth. This skill generates an HTML *companion*
that renders the same `.md` with higher fidelity — interactive graphs, tinted
provider icons, branded theming — and serves it reliably on localhost.

## Route by intent

| Intent | Do this |
|--------|---------|
| "Make an HTML version of DOC.md" | `md2html.py DOC.md` then `serve.py` (multi-file, live-editable) |
| "One file I can open / attach" | `md2html.py DOC.md --inline` (self-contained, opens over `file://`) |
| "I need an AWS/GCP/Azure/K8s icon" | `stencil.py search TERM` → `stencil.py extract ID --color HEX` |
| "Build a custom SVG diagram with real icons" | read `resources/stencil-library.md` (registry + compose pattern) |
| "Interactive graph / chart in the doc" | fenced ` ```cytoscape ` / ` ```plotly ` block — see `resources/rich-blocks.md` |
| "3D scene, colour-space study, or a map" | fenced ` ```deckgl ` block — see `resources/rich-blocks.md` |
| "Why is my palette not the palette I designed?" | ` ```deckgl ` with `space: "oklch"`, `gamut: [L]` and `targetChroma` — draws the request against the sRGB gamut |
| "HTML looks broken opened from Finder" | `file://` blocks fetch — run `serve.py` (see `resources/serving.md`) |
| "Render it in a brand theme" | default is `osakanights`; `md2html.py DOC.md --theme NAME` for another (see `--help` for installed themes) |
| "Re-brand the output" | edit `<stem>.tokens.json` in the output dir, refresh — no rebuild |
| "Override a theme for this project" | drop `tmp/richdocs/theme/<name>/design-tokens.json` (+ optional `theme.css`) — shadows the built-in of that name |
| "Add a new brand theme" | `resources/themes/<name>/design-tokens.json` (+ optional `theme.css`) |
| "Is this theme readable?" | `themecheck.py` — contrast gate over every brandpack; part of `make ci` |
| "Show off / compare the themes" | `showcase.py` → gallery of all brands; `showcase.py --theme NAME` → that brand alone |
| "Upgrade one of this repo's root docs" | read `resources/discovery-docs.md` (per-archetype recipes) |

## Quickstart

```bash
# 1. Render a markdown doc into a rich HTML companion (multi-file, live mode)
uv run --no-project .claude/skills/richdocs/scripts/md2html.py TARGET_ARCHITECTURE.md

# 2. Serve it (no-store headers, CDN libs load fine over http://localhost)
uv run --no-project .claude/skills/richdocs/scripts/serve.py tmp/richdocs --open

# 3. Or produce one self-contained file (no server needed)
uv run --no-project .claude/skills/richdocs/scripts/md2html.py REVIEW.md --inline

# 3b. Render in a brand theme (default is osakanights; pass --theme for another)
uv run --no-project .claude/skills/richdocs/scripts/md2html.py DOC.md --theme v2ai

# 4. Grab a tinted provider icon
uv run --no-project .claude/skills/richdocs/scripts/stencil.py search lambda
uv run --no-project .claude/skills/richdocs/scripts/stencil.py extract "mxgraph.aws4/lambda" \
  --color '#ED7100' --out diagrams/lambda.svg
```

Run everything from the repo root. Never `cd`.

## Mermaid gate (mandatory before rendering)

Any doc containing ` ```mermaid ` fences MUST pass this skill's **vendored**
parse + contrast gates **on the source markdown, before `md2html.py`**:

```bash
bun run .claude/skills/richdocs/vendor/mermaidjs-diagrams/scripts/mermaid_complexity.ts SOURCE.md
bun run .claude/skills/richdocs/vendor/mermaidjs-diagrams/scripts/mermaid_contrast.ts SOURCE.md
```

First run only: `bun install --cwd
.claude/skills/richdocs/vendor/mermaidjs-diagrams/scripts --frozen-lockfile`.

Non-zero exit is a blocker — `ParserFailure … yielded 0 nodes` means the
fence is invalid mermaid and will render as a broken block in the companion.
`md2html.py` passes fences through verbatim; it cannot catch this for you.
The vendored `vendor/mermaidjs-diagrams/SKILL.md` documents both tools in
full (profiles, complexity presets, authoring pitfalls like quoted mindmap
labels and HTML entities). Prior adjudications on this class of failure live
in `resources/learned/` — treat them as already-decided, don't re-litigate.

## Command reference

### `showcase.py [--theme NAME] [--out DIR]`

Emits a theme showcase exercising the full brand surface: colour ramps, the glyph
disambiguation gate, type specimens, components, Plotly charts, a Cytoscape graph,
Mermaid, and architecture diagrams built from the stencil pack.

- **no `--theme`** — a **gallery**: every installed brand, with a brand switcher and a
  light/dark toggle. Each brand honours its own `defaultTheme` when selected.
- **`--theme NAME`** — that brand **alone**: no switcher, and no other brand's tokens
  or CSS anywhere in the file. Safe to hand to a client.

Architecture SVGs carry their `mxfile` source in a `content` attribute, so
"Download editable SVG" / "Download .drawio" re-open in diagrams.net as real AWS
shapes rather than a flat image.

```bash
uv run --no-project .claude/skills/richdocs/scripts/showcase.py                     # gallery
uv run --no-project .claude/skills/richdocs/scripts/showcase.py --theme osakanights # one brand
```

### `md2html.py DOC.md [--out DIR] [--inline] [--theme NAME] [--tokens FILE] [--title T]`

- **`--theme NAME`** — a named brand theme. Supplies both the brandpack
  (`design-tokens.json`) *and* its `theme.css` — which is the only place a webfont
  can actually be `@import`ed and a display face assigned to headings. A brandpack
  alone cannot do either. Overrides `--tokens`. An unknown name fails loudly and
  lists what is installed. Run `--help` to see the current set.
  - **Default theme is `osakanights`** — a plain `md2html.py DOC.md` renders branded,
    not neutral. Pass `--theme NAME` for a different brand, or `--tokens FILE` (with no
    `--theme`) for the raw-brandpack escape hatch.
  - **Themes resolve from two roots, project first**: `tmp/richdocs/theme/<name>/`
    (optional project overrides, run from repo root) then the skill's built-in
    `resources/themes/<name>/`. A project theme shadows the built-in of the same name
    and can add project-only themes. With no override dir the skill is the built-in set
    only — fully self-contained.

- **Multi-file (default, `--out` = `tmp/richdocs`)** — writes `<stem>.html`
  plus a copy of the `.md` and `design-tokens.json`. The HTML fetches the
  paired markdown at runtime (`?v=<BUILD_ID>`, `cache: no-store`) and renders
  client-side. Edit the copied `.md`, refresh the browser: live authoring
  loop. **Requires `serve.py`** — `file://` blocks fetch by design.
- **`--inline`** — one self-contained HTML with the markdown embedded on
  `window.__DOC_MD__` and tokens on `window.__DOC_TOKENS__`. Opens over
  `file://`. Network still needed for the pinned CDN libraries.
- **`--tokens FILE`** — raw-brandpack escape hatch (see schema in
  `resources/rich-blocks.md`). Applies only when passed **and** `--theme` is not;
  otherwise the default `osakanights` theme wins.

#### Reporting a generated doc (worktree-aware)

`md2html.py` ends every run with a `── richdoc output ──` block: the **slug**
(doc stem — use it as the shared shorthand), the **worktree dir** and **branch**
the output landed in (resolved from the output file, not the process cwd), the
**absolute** source `.md` and `.html` paths (so they cmd+click open in the editor
across worktrees), and two **serve commands** for the absolute output dir
(`serve.py` with no-store, and stdlib `python3 -m http.server <port> --directory
<abs-dir>`). When you report a generated doc back to the user, relay these
verbatim — absolute paths and the slug, never a bare relative path.

### `serve.py [DIR] [--port 8642] [--open]`

Serves DIR (default `tmp/richdocs`) on `127.0.0.1` with `Cache-Control:
no-store` on every response, so a browser refresh always re-fetches fresh
markdown/JSON. Busy port and missing dir fail loudly. `--open` launches the
browser. This is the answer to "reliably serve localhost HTML that pulls
Tailwind / Google Fonts / Cytoscape / deck.gl / plotly / mermaid" — third-party
CDNs load fine over `http://localhost`; only `file://` breaks fetch.

### `stencil.py packs | list | search | extract`

Vendored draw.io stencil library (`assets/stencils.json.zip`, thousands of
provider icons keyed `"<pack>/<name>"`, packs: `mxgraph.aws4`, `mxgraph.gcp2`,
`mxgraph.azure`, `mxgraph.mscae*`, `mxgraph.kubernetes*`).

```bash
stencil.py packs                       # pack prefixes + counts
stencil.py list --pack mxgraph.gcp2 --limit 40
stencil.py search "cloud run"
stencil.py extract "mxgraph.aws4/lambda" --color '#ED7100' --size 64 --out lambda.svg
```

Every stencil paints `currentColor`; `--color` tints by string-replace (works
in every renderer). Omit `--color` and the SVG inherits its parent's
`color` — ideal for inlining into themed HTML. Unknown ID exits 1 with
close-match suggestions.

## Fenced rich blocks (in the rendered markdown)

Beyond standard markdown + ` ```mermaid `, the HTML companion renders:

````markdown
```cytoscape
{ "elements": [ {"data": {"id": "a", "label": "API"}},
                {"data": {"id": "b", "label": "DB"}},
                {"data": {"source": "a", "target": "b"}} ],
  "height": 420 }
```

```plotly
{ "data": "cost_series.json" }
```
````

- Payload is either **inline JSON** or `{ "data": "relative/path.json" }` —
  the external file is fetched with cache-busting: the data-driven mode.
  Generate the `.json` from real sources (terraform plan, dbt manifest,
  pricing API) and the doc stays current on refresh.
- Canvas colours come from `design-tokens.json` (`canvas.cytoscape.*`,
  `canvas.plotly.*`), never CSS — canvases can't read CSS variables. Theme
  toggle re-feeds the palette and re-renders.
- Full block contract + token schema: `resources/rich-blocks.md`.

## Cross-cutting conventions

- **Escalators, not stairs**: a missing hard requirement (input file, busy
  port, unknown stencil id) crashes loudly with the reason. No silent skips.
- **Determinism**: same input → same output modulo `{{BUILD_ID}}`. Cache-bust
  every runtime fetch with `?v=<BUILD_ID>`.
- **Inline-embed safety**: anything embedded in a `<script>` escapes `</` as
  `<\/` — a stray `</script>` in doc content must not terminate the tag.
- **Brandpack is data, not code**: re-skin = edit `design-tokens.json` in the
  output dir and refresh. `FALLBACK_TOKENS` baked into the JS is a soft-fail
  net only, never the source of truth.
- Outputs land in project-local `tmp/richdocs/` (gitignored), never system
  `/tmp`.
- **Authored prose follows the global-audience standard**: when this skill
  writes prose (showcase copy, UI/error strings, its own docs, or a discovery
  doc it is asked to upgrade), apply [resources/prose-style.md](resources/prose-style.md):
  no em-dash, Australian English, short coherent clauses, inclusive language,
  standardised vocabulary. The user's canonical markdown is rendered as written,
  never silently corrected.

## Resources

| File | Content |
|------|---------|
| `resources/serving.md` | Localhost serving contract, pinned CDN table (Tailwind, fonts, cytoscape, deck.gl, plotly, mermaid), `file://` vs `http://` failure modes |
| `resources/stencil-library.md` | Stencil pack schema, tint mechanism, registry pattern, composing full custom SVG diagrams from icons |
| `resources/rich-blocks.md` | Fenced block contract, design-tokens schema, two-palette (chrome vs canvas) theming |
| `resources/discovery-docs.md` | Recipes for upgrading each discovery-doc archetype (diagram-driven, table-driven, prose review) to rich HTML |
| `resources/prose-style.md` | Global-audience standard for prose this skill authors: no em-dash, Australian English, short clauses, inclusive language, standardised vocabulary (self-contained copy) |
| `scripts/serve.py` | No-store localhost server |
| `scripts/stencil.py` | Stencil library query/extract CLI |
| `scripts/md2html.py` | Paired markdown → rich HTML generator |
| `assets/stencils.json.zip` | Vendored draw.io icon library (see `assets/NOTICE`) |
| `assets/design-tokens.json` | Default neutral brandpack |
| `vendor/mermaidjs-diagrams/` | Vendored mermaid toolchain: parse/complexity gate, WCAG contrast gate, color-theming references, render script |
| `resources/learned/` | Prior adjudications and self-taught facts — read before re-litigating |

richdocs is self-contained: every tool and reference it operates with lives
inside this skill directory. Never point runtime instructions at another
skill's files.
