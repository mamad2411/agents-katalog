# f-import — Figma Import Orchestrator

Entry point for all Figma work. Detects input mode, extracts Figma data,
generates a semantic manifest, then invokes `f-ui-kit` and/or `f-page`.

Supports three input modes:
- **MCP** — Figma file/frame URL, extracts via `mcp__figma__*` tools
- **Export** — local folder of AI-generated code (Figma Make / ZIP export)
- **Hybrid** — MCP for classification + export folder for code files (best accuracy)

---

## Input

```
/f-import <figma-url>                             → MCP mode
/f-import auth:<figma-url>                        → MCP mode, auth module
/f-import --export src/exports/auth-export        → export folder mode
/f-import auth:--export src/exports/auth-export
/f-import --hybrid <figma-url> <folder-path>      → hybrid mode
/f-import auth:--hybrid <figma-url> <folder-path>
/f-import                                         → interactive: ask for input
```

URL detection: argument starts with `https://figma.com/` or `https://www.figma.com/`.

---

## Step 0 — Validate

Read `.claude/figma.yaml` (error if missing → "Run /f-setup first").

Parse `$ARGUMENTS`:
- Extract module scope from prefix (text before `:` if present)
- Extract mode flag (`--export`, `--hybrid`) and remaining args
- If no args: ask user interactively

```
How would you like to import from Figma?
[1] MCP — paste a Figma file or frame URL
[2] Export folder — provide path to an extracted Figma export
[3] Hybrid — MCP for classification + export folder for code
```

For MCP mode: verify `cfg.mcp_available == true`. If false:
```
MCP is not configured (mcp_available: false in .claude/figma.yaml).
Options:
  [1] Switch to export folder mode
  [2] Configure MCP first (run: claude mcp add figma -- npx -y @figma/mcp)
```

---

## Step 1 — Extract data by mode

### Mode: MCP

Parse Figma URL to extract `file_key` and optional `node_id`.

```
https://figma.com/design/<file_key>/...?node-id=<node_id>
```

Call Figma MCP tools:

```
mcp__figma__get_file(file_key)
  → file name, pages, full node tree

mcp__figma__get_file_components(file_key)
  → list of published components with id, name, description, containing_frame

mcp__figma__get_local_variables(file_key)
  → variable collections (colors, spacing, typography, etc.)
```

If `node_id` provided: focus extraction on that frame and its children only.

Map each node:
- `type == "COMPONENT"` → `figma_type: COMPONENT`
- `type == "COMPONENT_SET"` → expand variants, each variant is a shared-component
- `type == "FRAME"` at top level of a page → `figma_type: FRAME`

Apply role resolution:

```
COMPONENT / COMPONENT_SET → role: shared-component
FRAME:
  name matches /layout|shell|appshell|wrapper/i → role: layout
  name matches /playground|demo|gallery/i       → role: playground
  otherwise                                     → role: page
```

Map variables to token list:
- Variable type `COLOR` → category: color, css_var: `--<kebab-case-name>`
- Variable type `FLOAT` with name containing `spacing`/`size`/`radius` → category: spacing
- Variable type `FLOAT` with name containing `font`/`text` → category: typography

### Mode: Export folder

Read all files in `$ARGUMENTS` folder recursively (skip `node_modules`, `.git`).

For each `.tsx`/`.jsx`/`.ts`/`.js`/`.html` file:

1. Read content.
2. Content analysis:
   - Multiple named exports with props → `shared-component`
   - Large single JSX tree with no variant props → `page`
3. Filename heuristics (if ambiguous):
   - `/layout|shell|appshell/i` → `layout`
   - `/playground|demo|gallery/i` → `playground`
   - `/button|input|badge|card|chip|avatar|tag|icon|select|checkbox|radio|toggle|tooltip|modal|dialog|spinner|loader/i` → `shared-component`
   - Otherwise → `page`
4. Folder position:
   - In `layout/` subfolder → `layout`
   - In `playground/` subfolder → `playground`

No `figma_id`, no `figma_type` — set both to `null`.

CSS/SCSS files: collect for token extraction if they define CSS custom properties (`--`).

### Mode: Hybrid

1. Run MCP extraction (as above) — gets classification + token values + variant/prop info.
2. Read export folder — gets actual code files.
3. Correlate: match MCP component name to export filename (case-insensitive, strip path).
   - Matched: use MCP metadata + export file path
   - MCP only (no file): note in manifest, MCP code generation may be needed
   - File only (no MCP match): fall back to export classification

---

## Step 2 — Build manifest

Create manifest directory: `.figma-import/<module-or-root>/<YYYY-MM-DDTHH-MM>/`.

Write `manifest.yaml`:

```yaml
version: 1
source: mcp | export | hybrid
timestamp: "<ISO-8601>"
module: <module or null>
figma_file_key: <key or null>
figma_url: <url or null>
export_folder: <path or null>

components:
  - name: <Name>
    figma_id: <id or null>
    figma_type: <COMPONENT|FRAME|null>
    role: <shared-component|layout|playground|page>
    variants: []       # from MCP; [] if export-only
    props: []          # from MCP; [] if export-only
    export_path: <path or null>
    installed_path: null

tokens:
  - name: <name>
    css_var: --<kebab-name>
    value: <value>
    category: <color|spacing|typography|other>
```

Print manifest summary:

```
Manifest written: .figma-import/auth/2026-05-13T10-00/manifest.yaml

Components found:
  Shared components (5): Button, Input, Badge, Card, Checkbox
  Layout (1):            AuthLayout
  Playground (1):        Playground
  Pages (3):             SignIn, SignUp, ForgotPassword

Tokens: 24  (12 color, 8 spacing, 4 typography)
```

---

## Step 3 — Confirm what to build

```
What would you like to integrate?
[1] UI kit + pages  (recommended)
[2] UI kit only     (shared components, layout, playground)
[3] Pages only      (requires UI kit already installed)
[4] Tokens only     (update tokens.css, skip components)
[5] Cancel
```

Wait for selection.

---

## Step 4 — Write tokens (if tokens present + cfg.design_tokens.write == true)

Read existing `cfg.design_tokens.path` if it exists.

Show diff:
```
Token changes:
  NEW    --color-primary: #3B82F6
  NEW    --color-secondary: #64748B
  CHANGE --spacing-4: 16px → 14px   (was 16px)
  SAME   --color-white: #FFFFFF      (skip)

Apply token changes? [y/n]
```

If yes: write new/changed vars to the token file. Append at end; preserve existing comments.

If `cfg.design_tokens.write == false`: show diff only, do not write.

---

## Step 5 — Invoke f-ui-kit (if selected)

Pass manifest path to `f-ui-kit`:

```
Invoking f-ui-kit with manifest: .figma-import/auth/2026-05-13T10-00/manifest.yaml
```

Use the `Skill` tool to invoke `f-ui-kit`. Wait for completion.

Skip if selection was [3] or [4].

---

## Step 6 — Invoke f-page (if selected)

Pass manifest path to `f-page`:

```
Invoking f-page with manifest: .figma-import/auth/2026-05-13T10-00/manifest.yaml
```

Use the `Skill` tool to invoke `f-page`. Wait for completion.

Skip if selection was [2] or [4].

---

## Step 7 — Final summary

```
## f-import complete

Mode:    hybrid
Module:  auth
Manifest: .figma-import/auth/2026-05-13T10-00/manifest.yaml

UI kit:  5 components added, 1 layout, 1 playground
Pages:   2 pages created (sign-in, sign-up), 1 pending (forgot-password)
Tokens:  12 written to src/styles/tokens.css

Next:
  /f-review auth  → check for future Figma changes vs installed
```

---

## allowed-tools

Read, Write, Bash, Agent, mcp__figma__get_file, mcp__figma__get_file_components, mcp__figma__get_local_variables, mcp__figma__get_file_nodes
