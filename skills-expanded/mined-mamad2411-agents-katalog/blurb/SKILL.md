---
name: blurb
description: >
  Create rich, shareable artifacts (reports, analyses, plans, itineraries) with inline charts,
  Mermaid diagrams, maps, timelines, calendars, and more. Publish as shareable URLs. Use when:
  "create a report", "create an artifact", "publish a report", "make a plan", "generate a report",
  "share this analysis", "publish to blurb", "/blurb", or when the user wants to create a
  shareable markdown document with embedded data visualizations.
---

# Create Blurb

Create rich markdown artifacts with inline widgets — charts, diagrams, maps, timelines, calendars, tables, math, embeds, sketches — published as shareable URLs.

## API

**Base URL:** `https://blurb.md`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/~/public` | Create a folder with files |
| GET | `/~/public/:slug` | Get folder with all files + comments |
| GET | `/~/public/:slug/:path` | Read a single file |
| PUT | `/~/public/:slug/:path` | Create or replace a file (upsert) |
| PATCH | `/~/public/:slug/:path` | Edit file (old_str/new_str diffs) |
| DELETE | `/~/public/:slug/:path` | Delete file + its comments |
| POST | `/~/public/:slug/:path/@comments` | Add a comment to a file |
| DELETE | `/~/public/:slug/:path/@comments/:id` | Delete a comment |
| POST | `/~/public/:slug/:path/@comments/:id/replies` | Add a reply to a comment |

### Create a folder

```bash
curl -X POST https://blurb.md/~/public \
  -H "Content-Type: application/json" \
  -d '{"title":"Report Title","files":[{"path":"report.md","content":"...markdown..."}]}'
```

Returns `{"id":"...","slug":"adj-animal-NNNN"}`. The report is viewable at `https://blurb.md/~/public/{slug}`.

**Files use paths** — organize with folders:
```json
{
  "title": "Experiment Results",
  "files": [
    {"path": "overview.md", "content": "# Overview\n..."},
    {"path": "experiments/baseline.md", "content": "# Baseline\n..."},
    {"path": "experiments/with-cache.md", "content": "# With Cache\n..."}
  ]
}
```

Allowed file extensions: `.md`, `.mdx`, `.json`, `.ts`, `.tsx`, `.js`, `.jsx`, `.py`, `.rs`, `.go`, `.java`, `.css`, `.html`, `.yaml`, `.yml`, `.toml`, `.sql`, and more. Markdown files render in preview mode; code files render with syntax highlighting.

### Read a file

```bash
curl https://blurb.md/~/public/:slug/:path \
  -H "Accept: application/json"
```

Always read before editing — you need the current content to produce correct diffs.

### Create or replace a file (idempotent PUT)

```bash
curl -X PUT https://blurb.md/~/public/:slug/:path \
  -H "Content-Type: application/json" \
  -d '{"content":"# New Page\n..."}'
```

### Edit a file (diff-based)

```bash
curl -X PATCH https://blurb.md/~/public/:slug/:path \
  -H "Content-Type: application/json" \
  -d '{"updates":[{"old_str":"exact text to find","new_str":"replacement text"}]}'
```

### Delete a file

```bash
curl -X DELETE https://blurb.md/~/public/:slug/:path
```

## Workflow

### 1. Write the markdown

Write a markdown document with embedded widgets. See [references/widget-spec.md](references/widget-spec.md) for full widget specs.

### 2. Publish via API

```bash
curl -s -X POST https://blurb.md/~/public \
  -H "Content-Type: application/json" \
  -d "$(cat <<'ENDJSON'
{"title":"My Report","files":[{"path":"report.md","content":"# Title\n\nContent here..."}]}
ENDJSON
)"
```

### 3. Share the URL

The response contains a `slug`. The report is live at:
```
https://blurb.md/~/public/{slug}
```

## Available Widgets

### Charts (`widget` code block)

Bar, line, pie, doughnut, radar, polar area, scatter, bubble — powered by Chart.js.

````markdown
```widget
{"widgetId":"rev","type":"chart","config":{"type":"bar","data":{"labels":["Q1","Q2","Q3"],"datasets":[{"label":"Revenue","data":[2.4,3.1,3.8]}]}}}
```
````

### Mermaid Diagrams (`mermaid` code block)

Flowcharts, sequence diagrams, ER diagrams, Gantt charts, etc.

````markdown
```mermaid
graph TD
    A[Client] --> B[API]
    B --> C[(Database)]
```
````

### Math / LaTeX (`math` code block)

KaTeX-rendered math expressions.

````markdown
```math
E = mc^2
```
````

### Tables (`table` code block)

Sortable tables from JSON. Click headers to sort.

````markdown
```table
{"caption":"Team Stats","columns":["Name","Score"],"rows":[{"Name":"Alice","Score":95},{"Name":"Bob","Score":88}]}
```
````

### Maps (`map` code block)

MapLibre GL vector maps with markers. Dark Matter (dark) / Voyager (light) tiles.

````markdown
```map
{"zoom":4,"center":[20,110],"markers":[{"location":[1.35,103.82],"label":"Singapore"},{"location":[39.90,116.41],"label":"Beijing"}]}
```
````

Spec: `center` is `[lat, lng]`, `markers[].location` is `[lat, lng]`. Set `controls: true` to show zoom buttons.

### Timeline (`timeline` code block)

Vertical chronological timeline with colored dots.

````markdown
```timeline
{"events":[{"date":"2025-01-15","title":"Kickoff","description":"Project started"},{"date":"2025-03-01","title":"Launch","description":"v1.0 released"}]}
```
````

### Calendar (`calendar` code block)

Month grid with colored event ranges.

````markdown
```calendar
{"month":"2025-03","events":[{"start":"2025-03-01","end":"2025-03-03","title":"Sprint 1","color":"#6a8ac0"},{"start":"2025-03-08","end":"2025-03-10","title":"Sprint 2","color":"#7aa874"}]}
```
````

If `month` is omitted, it's inferred from the earliest event.

### Embeds (`embed` code block)

Sanitized iframes for YouTube, Vimeo, Loom, Figma, CodeSandbox, StackBlitz, etc. Share URLs auto-convert to embed URLs.

````markdown
```embed
https://www.youtube.com/watch?v=dQw4w9WgXcQ
```
````

### Diffs (`diff` code block)

Syntax-highlighted code diffs.

````markdown
```diff
{"language":"typescript","filename":"api.ts","old":"const x = 1","new":"const x = 2"}
```
````

### Sketches (`sketch` code block)

Hand-drawn diagrams via Rough.js. Elements: `rect`, `ellipse`, `line`, `arrow`, `text`.

````markdown
```sketch
{"width":500,"height":200,"elements":[{"type":"rect","x":30,"y":60,"width":130,"height":70,"fill":"#a5d8ff","color":"#1971c2","label":"Client"},{"type":"arrow","x1":160,"y1":95,"x2":280,"y2":95,"color":"#868e96","label":"REST"},{"type":"rect","x":280,"y":60,"width":130,"height":70,"fill":"#b2f2bb","color":"#2f9e44","label":"API"}]}
```
````

### Globe (`globe` code block)

Interactive WebGL globe with markers (COBE).

````markdown
```globe
{"markers":[{"location":[37.77,-122.42],"size":0.1},{"location":[51.51,-0.13],"size":0.08}]}
```
````

## Citations

Use `[^key]` markers inline and `[^key]: text` definitions. Hover shows rich tooltips.

```markdown
Vector search is standard[^1]. Hybrid methods outperform[^2].

[^1]: Karpukhin et al., 2020. "Dense Passage Retrieval." EMNLP.
[^2]: Ma et al., 2023. "Hybrid Search Revisited." SIGIR.
```

## Tips

- **Inter-file links**: `[Results](results.md)` navigates between files
- Markdown files render in preview; code files get syntax highlighting
- Multi-file artifacts show a collapsible tree sidebar
- Keep `widgetId` unique within a document (for chart widgets)
- Colors auto-assign from the engei palette — only specify when needed
- **Chart widget uses `widget` code blocks** — NOT `json:widget` or `chart`. Other widgets use their own lang: `mermaid`, `math`, `table`, `map`, `timeline`, `calendar`, `embed`, `sketch`, `globe`, `diff`
- **Pie/doughnut charts need explicit `backgroundColor`** on datasets or all slices render the same color
- **Map `center` is respected** — if you set `center` and `zoom`, the map won't auto-fit to markers. Omit `center` to auto-fit
- **Mermaid gotchas**: No backticks in labels, no special chars (`→`) in messages, no curly braces `{}` in message labels (breaks v11 parser), use `#quot;` for quotes
- **Sketch elements need absolute coordinates** — plan your layout on a grid (e.g., 700x200) before writing the spec

## Validating mermaid (optional)

Mermaid renders client-side — `curl` can't tell you if syntax is broken. Validate locally before publishing:

```bash
echo 'sequenceDiagram
    A->>B: hello' | npx -y @mermaid-js/mermaid-cli -i - -o /tmp/test.svg 2>&1
```

Non-zero exit = broken syntax. Fix before curling.
