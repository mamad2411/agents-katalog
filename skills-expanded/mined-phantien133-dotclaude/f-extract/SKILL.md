---
description: Extract all Figma design data (nodes, components, tokens, assets) in one MCP round and write a persistent figma-snapshot.md. Run once per task — downstream steps read the snapshot, never call MCP again.
argument-hint: <figma-url> [--task <task-slug>] [--out <path>]
allowed-tools: Bash, Read, Write, mcp__figma__get_file, mcp__figma__get_file_nodes, mcp__figma__get_file_components, mcp__figma__get_local_variables
---

# f-extract

Exhaustive one-shot Figma extractor. Calls all relevant MCP tools once, classifies every
node, and writes `figma-snapshot.md` — a persistent cache that lets all downstream steps
(f-implement, Phase 4c verify, etc.) work without ever re-calling Figma MCP.

**Rule:** after this skill completes, no other skill or phase may call `mcp__figma__*`
for this task. Read the snapshot instead.

---

## Input

```
/f-extract <figma-url>
/f-extract <figma-url> --task <task-slug>
/f-extract <figma-url> --out <custom-output-path>
```

- `<figma-url>`: required. Must start with `https://figma.com/` or `https://www.figma.com/`.
- `--task <task-slug>`: write snapshot to `<state_root>/<task-slug>/figma-snapshot.md`.
- `--out <path>`: write to explicit path (overrides --task).
- If neither `--task` nor `--out`: write to `./figma-snapshot.md` in current dir.

---

## Step 0 — Validate

Read `.claude/figma.yaml`. If missing: output "Run /f-setup first." Stop.

Check `cfg.mcp_available == true`. If false:
```
Figma MCP not configured.
To enable: claude mcp add figma -- npx -y @figma/mcp
Then re-run /f-extract.
```
Stop.

Parse `$ARGUMENTS`:
- Extract `figma-url` (first arg not starting with `--`)
- Extract `--task <slug>` and `--out <path>` flags
- Resolve output path:
  - `--out` → use as-is
  - `--task` → `<state_root from workflow.yaml>/<slug>/figma-snapshot.md`
  - neither → `./figma-snapshot.md`

---

## Step 1 — Parse Figma URL

Extract from URL:
```
file_key: path segment after /design/ or /file/
node_id:  query param node-id (replace - with :)

Examples:
  https://figma.com/design/AbCdEfGh/MyApp?node-id=1-23  → file_key=AbCdEfGh, node_id=1:23
  https://figma.com/design/AbCdEfGh/MyApp               → file_key=AbCdEfGh, node_id=null
```

---

## Step 2 — MCP extraction (single round)

Call in order. Collect all results before processing. If a call fails, note the error
in the snapshot and continue — partial data is better than stopping.

### 2a. File overview
```
mcp__figma__get_file(file_key)
```
Collect:
- `name`: file display name
- `document.children`: top-level pages
- For each page: `children` = top-level frames/components

### 2b. Published components
```
mcp__figma__get_file_components(file_key)
```
Collect: `meta.components[]` → `{node_id, name, description, containing_frame.name}`

### 2c. Design tokens / variables
```
mcp__figma__get_local_variables(file_key)
```
Collect: `meta.variables[]` → `{id, name, resolvedType, valuesByMode}`
Collect: `meta.variableCollections[]` → `{id, name, modes}`

### 2d. Focused node subtree (if node_id present)
```
mcp__figma__get_file_nodes(file_key, ids=[node_id])
```
Collect: `nodes[node_id].document` → full subtree of the scoped frame/component.

If no node_id: use the page-level children from 2a as the scope.

---

## Step 3 — Node classification

Walk the node tree (depth-first, max depth 6 to avoid token overflow).
For each node, record:

| Node type | Classification | Notes |
|---|---|---|
| COMPONENT, COMPONENT_SET | `component` | Collect variants if COMPONENT_SET |
| FRAME (top-level of page) | `screen` | These are the main screens/pages |
| FRAME (nested) | `section` | Sub-frames inside a screen |
| TEXT | `text-content` | Collect text value + style name |
| RECTANGLE/ELLIPSE with fills[].type == "IMAGE" | `image-asset` | Needs export |
| VECTOR, BOOLEAN_OPERATION, STAR, POLYGON | `vector-icon` | Needs export — never generate |
| INSTANCE | `component-usage` | Record component reference + overrides |
| GROUP | traverse children only | Not recorded separately |

**Asset detection rule:** any node where the primary visual content is:
- A rasterized fill (IMAGE type fill)
- A vector path (VECTOR, BOOLEAN_OPERATION)
- A component named like `/icon|logo|illustration|avatar/i`

→ mark as `needs-export`. Record `node_id`, `name`, `parent_name`, direct Figma link.

---

## Step 4 — Token classification

For each variable from 2c:
```
resolvedType == "COLOR"  → category: color
  css_var: --color-<kebab(name)>
  value: hex/rgba from default mode value

resolvedType == "FLOAT" with name matching /spacing|gap|margin|padding|size|radius/i
  → category: spacing
  css_var: --<kebab(name)>

resolvedType == "FLOAT" with name matching /font|text|line|letter/i
  → category: typography
  css_var: --<kebab(name)>

otherwise → category: other
```

---

## Step 5 — Write figma-snapshot.md

Write to resolved output path. Format:

```markdown
# Figma Snapshot

**Source:** <figma-url>  
**File:** <file-name>  
**File key:** <file_key>  
**Scope:** <node_id — "full file" if none>  
**Extracted:** <ISO-8601 timestamp>  
**MCP status:** get_file ✅ | get_file_components ✅ | get_local_variables ✅ | get_file_nodes ✅/skipped

---

## Screens / Frames

| Node ID | Name | Page | Notes |
|---------|------|------|-------|
| 1:23 | LoginScreen | Auth | ... |

---

## Components

| Node ID | Name | Variants | Props | Used in screens |
|---------|------|----------|-------|-----------------|
| 4:56 | Button | primary, secondary, ghost, disabled | label, size, onClick | LoginScreen, SignupScreen |

---

## Text Content

| Node ID | Screen / Section | Text | Style |
|---------|-----------------|------|-------|
| 2:10 | LoginScreen > Header | "Welcome back" | Heading/32/Bold |

---

## Design Tokens

| Variable | CSS Variable | Value | Category |
|----------|-------------|-------|----------|
| color/primary | --color-primary | #3B82F6 | color |
| spacing/4 | --spacing-4 | 16px | spacing |

---

## Asset Inventory

Assets that MUST be exported from Figma — do NOT generate or approximate.

| Node ID | Name | Type | Location | Figma Export Link | Status |
|---------|------|------|----------|-------------------|--------|
| 7:89 | icon-close | VECTOR | Header > CloseButton | https://figma.com/design/<key>?node-id=7:89 | ⚠️ needs-export |
| 8:12 | hero-illustration | IMAGE | HeroSection | https://figma.com/design/<key>?node-id=8:12 | ⚠️ needs-export |

---

## Figma Reference Links

- File: https://figma.com/design/<file_key>
- Scoped frame: <url with node-id if scoped>

---

## Extraction notes

<any errors or partial data warnings>
```

Output:
```
figma-snapshot.md written: <output-path>

Summary:
  Screens: <N>
  Components: <N>
  Tokens: <N>
  Assets needing export: <N>

Next: run /f-implement <output-path> to generate code from this snapshot.
```

---

## Error handling

- MCP call fails → write `⚠️ FAILED: <error>` in the relevant section, continue.
- URL parse fails → stop with "Cannot parse Figma URL. Expected format: https://figma.com/design/<key>/...".
- Output path unwritable → stop with path error.
