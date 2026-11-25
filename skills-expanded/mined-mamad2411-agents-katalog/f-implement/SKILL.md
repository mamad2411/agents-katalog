---
description: Implement UI components and screens from a figma-snapshot.md file. Never calls Figma MCP. Never generates SVG or approximates icons. Tracks missing assets in figma-assets.md and gates on human export before completing.
argument-hint: <snapshot-path> [--plan <plan-path>] [--scope <screen-names>]
allowed-tools: Bash, Read, Write, Edit
---

# f-implement

Implements UI from a `figma-snapshot.md` produced by `f-extract`.

**Core rules — read before every action:**

1. **No MCP calls.** Read the snapshot only. If data is missing, ask — do not re-call Figma.
2. **No asset generation.** Icons, illustrations, images from the Asset Inventory → use
   `ASSET_PLACEHOLDER`. Never generate SVG approximations. Never use an icon library
   substitution without explicit developer confirmation.
3. **No design guessing.** If a screen section has insufficient detail in the snapshot,
   show the Figma link and ask for a PNG. Do not proceed with assumptions.
4. **Placeholders ship with the code.** Commit code with `ASSET_PLACEHOLDER` comments is
   acceptable — better than fake assets. The `figma-assets.md` gate will resolve them.

---

## Input

```
/f-implement <snapshot-path>
/f-implement <snapshot-path> --plan <plan-md-path>
/f-implement <snapshot-path> --scope LoginScreen,SignupScreen
```

- `<snapshot-path>`: path to `figma-snapshot.md` produced by f-extract. Required.
- `--plan <path>`: path to `plan.md` from the task — used to scope which screens to implement.
- `--scope <names>`: comma-separated screen names to implement (subset of snapshot).
  If omitted: implement all screens referenced in plan.md, or all if no plan.

---

## Step 0 — Validate inputs

1. Read `<snapshot-path>`. Error if missing or not in expected format.
2. If `--plan` given: read `plan.md` and extract the list of UI changes/screens mentioned.
3. Build target list: screens to implement (from --scope, or plan.md intersection, or all).
4. Read `.claude/figma.yaml` for output path config (`cfg.output.component_base`, etc.).

---

## Step 1 — Survey snapshot

From `figma-snapshot.md`, build working data:
- `screens`: Map of name → node_id + notes
- `components`: Map of name → node_id + variants + props
- `tokens`: Map of css_var → value
- `assets`: Map of node_id → {name, type, figma_link, status}

Identify which assets are referenced by the target screens (from location field).

Print survey:
```
Snapshot loaded: <path>
Target screens: <list>
Components available: <N>
Assets to resolve: <N> (will create ASSET_PLACEHOLDERs)
```

---

## Step 2 — Implement components

For each shared component referenced by target screens:

1. Check if it already exists in the project (grep for component name in `cfg.output.component_base`).
   If it exists and looks complete: skip, note "using existing".

2. Generate component code from snapshot data:
   - Use variants and props from snapshot
   - Apply token css vars for colors, spacing, typography
   - For each icon/image in the component → insert placeholder:

```tsx
{/* [ASSET_PLACEHOLDER: node_id=7:89 name=icon-close figma=https://figma.com/design/...?node-id=7:89] */}
{/* Replace this comment with the actual asset once exported. Do NOT generate SVG. */}
```

3. **Unclear component gate**: if the snapshot has `Notes` or missing props that make
   implementation ambiguous:
   ```
   ⚠️ Design unclear: <ComponentName>
   Snapshot data is insufficient to implement correctly.
   Figma link: <link>

   Please provide a PNG screenshot of this component, or describe:
   - Expected visual states (hover, active, disabled)
   - Any behavior not captured in the snapshot notes

   Paste the PNG here or reply with a description, then I will continue.
   ```
   Wait for developer reply. Do not implement with guesses.

---

## Step 3 — Implement screens

For each screen in the target list:

1. Read snapshot data: screen node_id, notes, section structure.
2. Read plan.md (if provided) for this screen's acceptance criteria.
3. Generate screen code:
   - Use installed component catalogue (from Step 2 output)
   - Substitute snapshot tokens for hardcoded values
   - For any IMAGE/VECTOR asset in the screen → ASSET_PLACEHOLDER
4. **Unclear screen gate**: if a screen section is described only as a node name with no
   structural data in the snapshot:
   ```
   ⚠️ Design unclear: <ScreenName> § <SectionName>
   The snapshot does not have enough detail for this section.
   Figma link: <screen-scoped link>

   Please take a PNG screenshot of this section and share it here.
   I will pause until you provide the screenshot or a description.
   ```
   Wait. Do not approximate.

---

## Step 4 — Track missing assets

After implementing all screens and components, collect all `ASSET_PLACEHOLDER` comments.

For each placeholder, create an entry in `figma-assets.md`:

```markdown
# Figma Assets Needed

These assets must be exported from Figma before implementation is complete.
The code contains `ASSET_PLACEHOLDER` comments at each usage site.

## Unresolved assets

| Placeholder ID | Node ID | Name | Type | Used in | Figma Export Link | Target path |
|----------------|---------|------|------|---------|-------------------|-------------|
| 1 | 7:89 | icon-close | VECTOR | Header | https://figma.com/design/...?node-id=7:89 | src/assets/icons/icon-close.svg |
| 2 | 8:12 | hero-illustration | IMAGE | HeroSection | https://figma.com/design/...?node-id=8:12 | src/assets/images/hero.png |

## How to export

1. Open the Figma Export Link above.
2. In Figma: right-click the element → Export → choose format (SVG for icons, PNG for images).
3. Save to the Target path shown above.
4. Run `/w-task-v2` to continue — Claude will replace the placeholders with actual imports.

## Resolved assets

(empty — updated when developer provides files)
```

Write to `<state_root>/<task-slug>/figma-assets.md` (or `./figma-assets.md` if no task context).

---

## Step 5 — Asset resolution (interactive)

Show `figma-assets.md` to developer.

If there are unresolved assets:
```
## Assets needed before implementation is complete

<N> assets require export from Figma.
See figma-assets.md for links and target paths.

Once you have exported and placed the files, run /w-task-v2 to continue.
I will then replace the ASSET_PLACEHOLDER comments with actual imports.
```

**GATE (if unresolved):** developer exports assets → runs `/w-task-v2`.

When continuing after gate:
- Read `figma-assets.md`
- For each listed asset, check if file exists at `target_path`
- If found: replace all `ASSET_PLACEHOLDER` comments for that node_id with actual import
- If not found: re-show the missing entry, do not proceed past it
- Update `figma-assets.md § Resolved assets` with each resolved entry

When all assets resolved (or none were needed):
- Output: "All assets resolved. Implementation complete."

---

## Step 6 — Summary

```
## f-implement complete

Screens implemented: <N>
Components implemented: <N>
Assets resolved: <N>/<total>
ASSET_PLACEHOLDERs remaining: 0

Files written:
  <list of created/modified files>
  figma-assets.md (all resolved)
```

---

## Error handling

- Snapshot missing or malformed → stop with clear error, suggest running f-extract.
- No screens in target list → stop: "No UI screens to implement based on plan scope."
- Component already exists and matches: skip without overwrite. Note in summary.
