---
name: mindmaply-cursor
description: Create mind maps, concept maps, org charts, and flowcharts as polished SVG with Mindmaply. Use when the user asks for a mindmap, a diagram of ideas or topics, a visual outline or summary, an org chart, a process flow, or a shareable diagram link. Writes a Markdown outline, validates it, renders SVG locally with the mindmaply CLI (npx mindmaply-core), and returns a mindmaply.app link.
---

# Mindmaply: text to beautiful mind maps

Turn a topic into a **Markdown outline first**, then render it as a polished SVG with the
[Mindmaply](https://mindmaply.app) CLI. Everything runs on the user's machine through one command:

```bash
npx -y mindmaply-core@latest <command> [file] [options]
```

Commands: `validate`, `render`, `share`, `convert`. Source comes from a file argument or stdin.

## Requirements

- **Node.js 18+** so `npx` can run the CLI. The first run downloads the package; after that,
  validation and rendering are fully offline.
- **`mindmaply-core` 0.3.0 or newer**, which `@latest` resolves to. Releases before 0.3.0 have
  no `mindmaply` binary; if `npx` ever prints `could not determine executable to run`, pin
  `mindmaply-core@^0.3` explicitly.

## Output locations (defaults)

- Workspace root folder: **`mindmaps/`**
- Files: `mindmaps/<topic-slug>.md` (source) and `mindmaps/<topic-slug>.svg` (rendered)
- If the user specifies another path, follow their preference

Use a **slug**: lowercase, hyphens, no spaces (e.g. `auth-service-architecture`).

## Workflow

1. **Clarify** only if needed (scope, depth, audience). If the request is specific, skip questions.

2. **Write the Markdown outline** to `mindmaps/<slug>.md` using the grammar below.

3. **Validate** before rendering. Invalid source exits 1 and prints `line N: message` for every
   bad line; fix those lines and re-validate until it passes.

```bash
npx -y mindmaply-core@latest validate "mindmaps/<slug>.md"
```

4. **Render** the SVG. Success prints `Wrote mindmaps/<slug>.svg`.

```bash
npx -y mindmaply-core@latest render "mindmaps/<slug>.md" -o "mindmaps/<slug>.svg"
```

5. **Share link** (always include it). This is computed locally: the outline is compressed into
   the URL, nothing is uploaded. Opening the link at mindmaply.app gives the user pan, zoom, and
   editing.

```bash
npx -y mindmaply-core@latest share "mindmaps/<slug>.md"
```

   It prints JSON. Give the user `sharePageUrl` (paste anywhere, unfurls with a preview) and
   `editorUrl` (opens the map in the editor). `embedCode` is an iframe for docs/wikis. Do not
   pass `--short`; it contacts a server.

6. **Confirm** the `.svg` exists, then hand back: the SVG path, `sharePageUrl`, and `editorUrl`.
   Tell the user the SVG is a static image; the live, interactive version is the link.

7. **Edits**: change the `.md`, then re-run `validate`, `render`, and `share`.

## Source format 1: Markdown outline (default)

Use for notes, topics, lists, summaries, anything hierarchical.

```markdown
# Service architecture
- Edge
  - CDN
  - WAF
- Application
  - API
  - Workers
- Data
  - Primary DB
  - Cache
- Cross-cutting
  - Auth
  - Observability
```

Rules, all of them enforced by `validate` or by the renderer:

- The first line is exactly **one** `# Title`. A second `#` heading is not an error; it and its
  whole subtree are **silently left out** of the map. One root per file.
- `##` and `###` headings may add levels. Every other line is a `- ` bullet.
- Nest bullets with **exactly 2 spaces** per level. Four-space indents jump two levels with no
  error and produce a wrong tree.
- **Plain text labels only.** Links, bold, backticks, and other inline Markdown pass validation
  but render as literal characters in the node. Write `Run the CLI`, not `` Run `mindmaply` ``.
- Nothing else: no paragraphs, numbered lists, code fences, quotes, or tables. They fail validation.
- Optional leading frontmatter (`--- ... ---` on the first lines) can set `direction: TD|LR`,
  `edgeStyle: curved|straight`, `diagram: mindmap|flowchart`, and `theme.*` keys. Use
  `direction: TD` for org charts.

## Source format 2: Mermaid flowchart (for processes and flows)

Use only when the content clearly describes a process with steps and arrows.

```
flowchart LR
a[Start] --> b[Review the draft]
b --> c["Approved?"]
c --> d((Done))
```

First line `flowchart LR` or `flowchart TD`. Node ids are single words. Labels go in `id[Label]`,
`id["Label with punctuation"]`, or `id((Circle))`. Edges are exactly `id --> id`, one per line:
no chaining, no arrow labels, no subgraphs, no dashed arrows, no semicolons. At least one node
must have no incoming arrow. Most full-Mermaid documents will not validate.

## Quality rules for generated maps

- Stay faithful to the input: use its wording, never invent topics.
- Condense long sentences into short labels (under about 8 words). No em dashes in labels.
- Be thorough. For substantial inputs (articles, transcripts, codebases) aim for 25-70 nodes and
  3-4 levels: main themes as branches, sub-topics beneath, concrete specifics as leaves.
- Only very short inputs deserve small maps.
- Keep source under 20,000 characters so the share link stays usable.

## CLI reference

```
mindmaply validate [file] [--format markdown|mermaid]        # exit 1 + line errors if invalid
mindmaply render   [file] [--format ...] [--direction LR|TD]
                          [--edge-style curved|straight] [-o out.svg]
mindmaply share    [file] [--format ...] [--direction LR|TD] [--edge-style ...]
mindmaply convert  [file] --to markdown|mermaid
```

`--format` is auto-detected when omitted. Default direction is LR. Mind maps default to curved
edges, flowcharts to straight. Unknown flags exit 2; there is no `--offline` or `--no-open`.

## Failure handling

- Show CLI errors verbatim. `line N:` errors point at the exact source line to fix.
- Never claim the SVG was generated until the command succeeds and the file is present.
- If `npx` itself fails, suggest installing Node.js LTS and retrying.

## Privacy

Nothing leaves the machine. Validation and rendering are local, and `share` builds its URLs
locally by encoding the outline into the link. The user decides whether to open that link.
