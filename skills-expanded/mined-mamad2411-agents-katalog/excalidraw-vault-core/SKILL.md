---
name: excalidraw-vault-core
description: Runner protocol for generating Excalidraw diagrams directly into the MoxyWolf Vault in the zsviczian Obsidian-Excalidraw plugin's native .excalidraw.md format. Single source of truth for the wrapping format, element schema, depth assessment, and routing used by /excalidraw and /excalidraw-here.
---

# excalidraw-vault-core

The canonical runner protocol for emitting Excalidraw diagrams into the MoxyWolf Vault. Both `/excalidraw` and `/excalidraw-here` delegate here. Future plugins that need to generate diagrams (board-deck, saas-frontend-designer, github-repo-analyzer) should reference this skill rather than reinventing the wrapping.

## Why a vault-native format

The Obsidian Excalidraw plugin (zsviczian) treats `.excalidraw.md` as the preferred storage format — a markdown file with `excalidraw-plugin: parsed` frontmatter and a fenced JSON block. Storing diagrams this way means:

- They render natively when opened in Obsidian (no separate canvas server, no external link).
- They embed in any note via `![[<name>.excalidraw]]` and render inline as a PNG.
- They version in the git-backed vault alongside the notes that reference them.
- They cross-link with the rest of the vault (graphify-vault picks up their backlinks if any text content is added between frontmatter and the `# Text Elements` heading).

The headless Excalidraw MCP servers (mcp.excalidraw.com, yctimlin/mcp_excalidraw-canvas) do **not** write to this format — they live outside the vault. This skill replaces them for MoxyWolf's "everything in the vault" pattern.

## Obsidian wrapping format

Every diagram written to the vault MUST follow this structure exactly:

```
---
excalidraw-plugin: parsed
tags: [excalidraw]
---

==⚠ Switch to EXCALIDRAW VIEW in the MORE OPTIONS menu of this document. ⚠== You can decompress Drawing data with the command palette: 'Decompress current Excalidraw file'. For more info check in plugin settings under 'Saving'

# Excalidraw Data

## Text Elements

%%
## Drawing
```json
{ ...Excalidraw JSON... }
```
%%
```

Critical rules:

- Frontmatter MUST include `excalidraw-plugin: parsed` AND `tags: [excalidraw]`.
- The warning banner line is preserved verbatim — the plugin keys on it.
- `## Text Elements` stays empty (just `%%` on the next line). The plugin auto-fills it from the JSON.
- The JSON block is fenced with ```json (not ```excalidraw, not ```compressed-json — we do not compress).
- The closing `%%` must be present (it closes the embed wrapper).

See `references/obsidian-format.md` for a copy-pasteable template.

## JSON root structure

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://github.com/zsviczian/obsidian-excalidraw-plugin",
  "elements": [ /* ... */ ],
  "appState": {
    "gridSize": null,
    "viewBackgroundColor": "#ffffff"
  },
  "files": {}
}
```

The `source` field MUST be the zsviczian GitHub URL when writing to the vault — that's what the Obsidian plugin checks. Setting it to `https://excalidraw.com` will make the file open in compatibility (read-only) mode.

## Element schema

Every element requires these fields (do not add extras like `frameId`, `index`, `versionNonce`, `rawText` — they cause issues on excalidraw.com round-trips):

```json
{
  "id": "unique-id-string",
  "type": "rectangle | ellipse | diamond | text | arrow | line | freedraw",
  "x": 100,
  "y": 100,
  "width": 200,
  "height": 50,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "groupIds": [],
  "roundness": { "type": 3 },
  "seed": 123456789,
  "version": 1,
  "isDeleted": false,
  "boundElements": null,
  "updated": 1,
  "link": null,
  "locked": false
}
```

- `boundElements` is `null`, not `[]`.
- `updated` is `1`, not a real timestamp (real timestamps cause noisy git diffs on no-op opens).
- Text elements additionally need `text`, `fontSize` (16/20/24/32), `fontFamily: 5` (Excalifont), `textAlign`, `verticalAlign`.
- Arrow elements need `points: [[0,0],[dx,dy]]` (relative) and optionally `startBinding`/`endBinding` to attach to nodes.

See `references/element-templates.md` for ready-to-use templates per element type.

## Depth assessment

Before generating JSON, classify the diagram by element count and structure:

| Tier | Elements | Approach |
|---|---|---|
| Simple | ≤ 10 | Generate in one pass. |
| Medium | 11–25 | Generate in two passes: layout skeleton (positions only) → fill content. |
| Complex | 26+ | Generate section-by-section: title bar → primary nodes → connectors → annotations. Validate after each section. |

For Medium and Complex, after generating the JSON, mentally walk the layout: do positions overlap? Are arrows attached to the right nodes? Are groups visually distinct? Adjust before writing.

## Routing

| Scope | Destination |
|---|---|
| `--shared` or default (no scope) | `_Shared Knowledge/Diagrams/<name>.excalidraw.md` |
| `--scope Projects/<project>` | `Projects/<project>/06-Engineering/diagrams/<name>.excalidraw.md` |
| `/excalidraw-here` (sibling to source note) | Same folder as source note, or `<source-folder>/diagrams/<name>.excalidraw.md` if `diagrams/` exists or is preferred |

Vault root resolves from `$MW_VAULT_PATH` if set, otherwise the canonical mount: `/Users/doriancougias/Library/CloudStorage/GoogleDrive-dorianc@moxywolf.com/Shared drives/MoxyWolf Shared Files/MoxyWolf Vault`.

Filenames are kebab-case with a `.excalidraw.md` extension. Examples: `uber-brain-architecture.excalidraw.md`, `dr-routing-flow.excalidraw.md`.

## Writing path

The vault is cloud-synced Google Drive. From the sandbox, write via Desktop Commander / `pc files write` — never via raw filesystem APIs that would create local-only copies.

## Embedding into notes

Once written, any note can embed the diagram as a rendered image:

```markdown
![[uber-brain-architecture.excalidraw]]
```

Obsidian resolves `.excalidraw` from the basename (ignoring `.md`) and renders the diagram as a PNG. To embed a specific size: `![[uber-brain-architecture.excalidraw|600]]`.

## Repo-backed mode

Use this mode whenever the thing being drawn is code: the source `/excalidraw` or `/excalidraw-here` is given is a path inside a git repository. The drawing then makes claims about that code, and every claim has to point at the lines that prove it. The rules come from Archify (`tt-a1i/archify` at `d5a1333`, MIT). We took the ideas and wrote them in our own words. No code was copied. We didn't take its typed JSON IR and schemas, its interactive viewer, or its PNG, video and share-card export.

**1. Pin the commit before you read anything.** Add three keys to the note's frontmatter, under `tags`:

```yaml
repo_head: <git rev-parse HEAD, all 40 characters>
repo_origin: <git remote get-url origin, with any user:password@ or token removed>
repo_dirty: [<paths from git status --short>]   # [] when clean; information only
```

**2. Read only the pinned commit.** Evidence counts at `repo_head` and nowhere else. Read every cited file with `git show <repo_head>:<path>`, whether it's dirty or clean. Never cite working-tree bytes.

**3. Trace to where the work happens.** Read a small connected slice. Follow calls from the entry point until the behavior you're drawing reaches its real input, output or side effect.
- A connection to a store names the code that actually reads or writes it. A sentence saying a module "maintains" something doesn't prove I/O.
- Code that's configured or exported but never called on the normal path is optional. Label it that way, not as a runtime edge.
- Stop when the responsibilities you were asked to draw are covered. There's no node or arrow count to hit.

**4. Every claim gets exactly one Sources row.** Put a `## Sources` table after the warning banner and before `# Excalidraw Data`:

```markdown
## Sources

| element | claim | source |
|---|---|---|
| `api` | serves /orders | `src/api/orders.py:12-48` |
| `e-api-db` | api writes orders | `src/api/orders.py:40-44` |
| `cache` | eviction policy | `unknown` |
```

- `element` is the Excalidraw element `id`.
- Every non-deleted rectangle, ellipse, diamond, arrow and line is a claim and needs exactly one row. Titles, legends and frames opt out with `"customData": {"claim": false}`.
- `source` is `path:start-end` at `repo_head`, or `unknown`. An `unknown` element is drawn with `"strokeStyle": "dashed"` and its claim says what is unresolved.

**5. Check it before you report it.**

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_repo_diagram.py <note> --repo <repo path>
```

It fails on:
- a claim element with no row, a row for an element that isn't in the drawing, or two rows for one element;
- a path missing at `repo_head`, or a line range outside the file;
- a bad or missing `repo_head`;
- an origin that carries credentials or doesn't match `--repo`'s;
- a compressed drawing;
- having nothing to examine.

It validates the note as history, not freshness. When the repo has moved past `repo_head`, it prints the cited files that changed as drift. Drift doesn't change the exit code. Report both lines to the user, along with what the check didn't cover: whether the cited lines actually prove each claim is a judgment the check doesn't make.

## What NOT to do

- Don't use `compressed-json` fences — we keep diagrams readable and diffable.
- Don't put `excalidraw-plugin: raw` in frontmatter — that disables most plugin features.
- Don't add text content between the frontmatter and the warning banner — the plugin tolerates it but it makes diffs noisy.
- Don't write through the sandbox filesystem — the vault is cloud-synced; use Desktop Commander.
- Don't have obsidian-update or vault-code-learn ingest these files — they're derived artifacts. (They're already covered by the `_Templates/`, `99 – Archive/`, etc. exclusions in those skills; diagrams in `diagrams/` subfolders should be added to the ignore lists going forward.)
