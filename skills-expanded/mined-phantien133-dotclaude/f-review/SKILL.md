# f-review — Figma Design vs Implementation Diff

Compares the current Figma design state against installed components and applies
selective updates. Solves the update/drift problem: no more full re-imports that
overwrite local customizations.

---

## Input

```
/f-review              → review all modules
/f-review auth         → review auth module only
/f-review auth --export src/exports/auth-v2  → compare against new export folder
```

---

## Step 0 — Validate

Read `.claude/figma.yaml` (error if missing → "Run /f-setup first").

Parse `$ARGUMENTS`:
- Optional module scope
- Optional `--export <folder>` flag

---

## Step 1 — Locate latest manifest

Find manifests in `.figma-import/<module>/` (or all module folders if no scope):

```bash
find .figma-import -name "manifest.yaml" | sort -r | head -20
```

If multiple manifests for the module: use the most recent (sorted by timestamp in path).

If no manifest found:
```
No manifest found for module "<module>".
Run /f-import first to create an initial manifest.
```

Read the manifest. Identify components with non-null `installed_path` values
(these are the ones currently in the project).

---

## Step 2 — Determine comparison source

If `--export` flag provided: use that folder as the new source (export mode, no MCP).

Otherwise, check `cfg.mcp_available`:

```
Compare against:
[1] Current Figma state via MCP  (requires mcp_available: true)
[2] New export folder            (provide path)
```

Wait for selection if not already determined by flags.

---

## Step 3 — Fetch / read new state

### MCP comparison

Use `figma_file_key` from manifest. If null: ask user for Figma URL.

Call:
```
mcp__figma__get_file_components(file_key)   → current component list
mcp__figma__get_local_variables(file_key)   → current tokens
```

For each installed component: find its entry by `figma_id` in the new state.

### Export folder comparison

Read all files in the provided folder. Build ad-hoc manifest using same classification
logic as f-import Step 1 (export mode). Match by filename to installed components.

---

## Step 4 — Generate diff report

For each installed component, compare old manifest entry vs new state:

**Changed component** = any of:
- New variant added or removed
- Prop added, removed, or type changed (MCP mode)
- File content changed significantly (export mode — compare line count + structure)

**New component** = present in new state, not in manifest (not yet in UI kit)

**Removed from Figma** = in manifest + installed, but not in new state (MCP mode only)

**Token changes** = CSS var value changed, new var added, or var removed

Print report:

```
## Figma change report

Module:   auth
Compared: Figma main (fetched 2026-05-13) vs installed (manifest 2026-04-20)

CHANGED components (2):
  Button
    + prop "size" added: "sm" | "md" | "lg"
    ~ token --color-primary: #2563EB → #3B82F6

  Input
    + variant "error" added

NEW components (1):
  Toast — not yet in UI kit (no installed_path)

REMOVED from Figma (0):
  (none)

TOKEN changes (2):
  ~ --color-primary:  #2563EB → #3B82F6
  + --border-radius:  4px  (new)

No changes detected in: Badge, Card, Checkbox, AuthLayout
```

If no changes at all:
```
No changes detected. UI kit is in sync with Figma.
```
Stop here if no changes.

---

## Step 5 — Interactive apply

For each changed or new item, ask individually:

```
[1/3] Button changed — apply update?
  + prop "size": "sm" | "md" | "lg"
  ~ token --color-primary token reference updated

  [y] Apply   [n] Skip   [a] Apply all remaining   [q] Quit
```

**If [y] — apply component update:**

1. Read the source file for this component:
   - MCP mode: fetch generated code via `mcp__figma__get_file_nodes` for this component's `figma_id`
   - Export mode: read from the new export folder file
2. Apply HTML→React transformations inline:
   - `class=` → `className=`
   - `for=` → `htmlFor=`
   - Void elements self-close
   - Inline style strings → object syntax
   - Rewrite imports to project alias
3. Write to `installed_path` from manifest. Existing file is overwritten.
4. Add `// Updated from Figma — <date>` comment at top of file.
5. Update `installed_path` timestamp in manifest.

**If [y] — apply new component:**

Run the same transformation flow. Determine target path using same logic as
f-ui-kit Step 4 (component_base + ui-kit/ + filename).

Write new file. Update manifest entry with `installed_path`.

**If [y] — apply token changes:**

Read `cfg.design_tokens.path`. For each changed/new token, update the CSS var value
or append new var. Preserve existing comments and ordering.

---

## Step 6 — Update manifest

After all applies are done:

Write an updated manifest at `.figma-import/<module>/<new-timestamp>/manifest.yaml`
with updated `installed_path` values, new component entries, and new timestamp.

Do not delete the previous manifest — keep history.

---

## Step 7 — Report

```
## f-review complete

Applied (2):
  Button — updated (src/components/auth/ui-kit/Button.tsx)
  Toast  — added   (src/components/auth/ui-kit/Toast.tsx)

Skipped (1):
  Input — skipped by user

Tokens updated (2):
  --color-primary, --border-radius → src/styles/tokens.css

New manifest: .figma-import/auth/2026-05-13T11-00/manifest.yaml

Manual follow-up:
  - Input: variant "error" was not applied — review manually
  - Button: prop "size" added — existing usages may need size prop specified
```

---

## allowed-tools

Read, Write, Bash, mcp__figma__get_file_components, mcp__figma__get_local_variables, mcp__figma__get_file_nodes
