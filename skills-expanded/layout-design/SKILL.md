---
name: layout-design
description: Generate FileMaker layout objects, preview them in the webviewer, iterate with the developer, then produce output as either XML2 fmxmlsnippet (for paste into FM Layout Mode) or self-contained HTML (for the Web Viewer path). Use when the developer says "design layout", "create layout objects", "build layout", "add fields to layout", "preview layout", or provides a layout spec to implement.
---

# Layout Design

Generate layout objects from a design brief or a specification produced by `layout-spec`. The workflow is preview-first: the agent builds an HTML mock styled with the solution's FM theme CSS, pushes it to the webviewer for the developer to see, iterates on feedback, then produces the final output in the developer's chosen format.

---

## Step 1: Determine the automation tier

Read `agent/config/automation.json` and check `project_tier` (preferred) or `default_tier`:

- **Tier 1** — layout objects go to clipboard with paste instructions
- **Tier 2/3** — agent can deploy via companion server automation

Also read `companion_url` and `webviewer_url` from `automation.json` — these are needed for preview pushes and deployment.

---

## Step 2: Gather context

1. Read `agent/CONTEXT.json` for:
   - `current_layout` — the target layout (name, ID, base TO)
   - `tables` — fields with IDs, types, and TO references
   - `relationships` — related TOs for portals
   - `scripts` — scripts for button wiring
   - `value_lists` — for dropdowns and radio buttons
   - `layouts` — for navigation button targets

2. If CONTEXT.json is absent or scoped to the wrong layout, ask the developer to create the layout shell in FM first, then run **Push Context** on it. The agent cannot generate layout objects without knowing the target layout's TO and the field IDs available in that context.

3. Read the theme data from `agent/context/{solution}/`:
   ```bash
   # Resolve solution name from CONTEXT.json
   cat agent/context/*/theme-manifest.json 2>/dev/null
   cat agent/context/*/theme.css 2>/dev/null
   cat agent/context/*/theme-classes.json 2>/dev/null
   ```

   - `theme.css` — the FM theme's CSS rules, used for HTML preview styling
   - `theme-manifest.json` — color palette and layout builder constants (default margins, field height, label width, row spacing, portal row height)
   - `theme-classes.json` — named style classes available in the solution

4. If no theme data exists, inform the developer and suggest extracting it:

   > No theme data found for this solution. Run `python3 agent/scripts/extract_theme.py` to extract the theme CSS, manifest, and style classes. This enables accurate layout previews and ensures generated objects use valid theme styles.

   Proceed with reasonable defaults if the developer wants to continue without theme data.

---

## Step 3: Design the layout

If a specification from `layout-spec` was provided, use it directly. Otherwise, conduct a brief design conversation:

1. Ask what the layout is for (detail, list, card, dashboard, print)
2. Determine which fields, portals, and buttons are needed
3. Apply the UI/UX principles from the `layout-spec` skill (grouping, hierarchy, alignment)
4. Use the theme manifest's layout builder constants for spacing:
   - Default margins, field heights, label widths, row spacing
   - Portal row heights and padding
   - Button dimensions

### Object positioning

All FM layout objects use absolute pixel positioning via Bounds (top, left, bottom, right). When calculating positions:

- Start from the top-left of each layout part
- Apply consistent margins from the theme manifest (or 20px default)
- Stack fields vertically with consistent row spacing (from manifest or 30px default)
- Arrange columns with consistent gutters
- Portals contain their own coordinate space for child objects — portal column positions are relative to the portal's left edge

---

## Step 4: Generate HTML preview

Build an HTML document that visually represents the layout design. The preview uses the FM theme CSS for accurate styling.

### Preview HTML structure

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Layout Preview: {Layout Name}</title>
  <style>
    /* Inline the theme.css content here */
    {theme_css_content}

    /* Layout preview scaffolding */
    .layout-preview { position: relative; width: {layout_width}px; margin: 0 auto; }
    .layout-part { position: relative; border-bottom: 1px dashed #ccc; }
    .layout-part-label { position: absolute; right: 4px; top: 2px; font-size: 10px; color: #999; }
    .layout-object { position: absolute; box-sizing: border-box; }
  </style>
</head>
<body>
  <div class="layout-preview">
    <!-- One div per layout part, with child objects absolutely positioned -->
  </div>
</body>
</html>
```

Map FM layout object types to HTML elements:

| FM Object | HTML Representation |
|-----------|-------------------|
| Edit Box | `<input type="text">` with field name as placeholder |
| Text Label | `<span>` or `<label>` with the text content |
| Button | `<button>` with the label text |
| Button Bar | `<div>` container with child `<button>` elements |
| Portal | `<table>` with header row and sample data rows |
| Rectangle | `<div>` with border/background styling |
| Line | `<hr>` or `<div>` with border styling |
| Pop-up Menu | `<select>` with value list options |
| Checkbox Set | `<div>` with `<input type="checkbox">` elements |
| Radio Button Set | `<div>` with `<input type="radio">` elements |
| Tab Control | `<div>` with tab headers and content panels |
| Web Viewer | `<div>` with a "Web Viewer" placeholder label |
| Container | `<div>` with a container icon or placeholder |

Apply theme class names as CSS classes on each element so the theme CSS styles them accurately.

### Push to webviewer

Send the preview HTML to the webviewer via the companion server:

```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"type": "layout-preview", "content": "<html content>"}' \
  {companion_url}/webviewer/push
```

If the companion server is not reachable, fall back to writing the preview HTML to `agent/sandbox/{layout-name}-preview.html` and instruct the developer to open it in a browser.

---

## Step 5: Iterate on feedback

Present the preview to the developer:

> The layout preview has been pushed to the webviewer. Review the design and let me know what to change — for example:
> - "Move the portal lower"
> - "Make the name field wider"
> - "Use the strong field style for the total"
> - "Add a status badge in the header"
> - "Switch to a two-column layout for the address fields"

For each revision:
1. Update the object positions, sizes, or styles as requested
2. Regenerate the preview HTML
3. Push the updated preview to the webviewer
4. Report what changed

Continue until the developer approves the design.

---

## Step 6: Choose output path

Once the design is approved, ask the developer:

> The design is approved. How would you like the output?
>
> 1. **FM Layout Objects** — XML2 fmxmlsnippet for paste into Layout Mode (native FileMaker path)
> 2. **Web Viewer HTML** — self-contained HTML/CSS/JS app for a Web Viewer object (web-first path)

### FM path (XML2 fmxmlsnippet)

Generate XML2-formatted layout objects. The developer must have already created the layout shell in FM.

#### XML2 structure reference

Before generating XML2, read an existing layout from `xml_parsed/layouts/` to understand the solution's XML2 structure:

```bash
ls agent/xml_parsed/layouts/{solution}/ 2>/dev/null | head -5
```

Read one layout file to use as a structural reference for object types, attribute patterns, and nesting.

#### Object generation rules

- Wrap all objects in `<fmxmlsnippet type="LayoutObjectList">`
- Each object is a `<LayoutObject>` element with a `type` attribute
- Position every object with `<Bounds top="T" left="L" bottom="B" right="R"/>`
- Apply theme classes with `<LocalCSS name="ClassName"/>` — only use classes from `theme-classes.json`
- Bind fields with `<FieldObj table="TOName" id="FieldID" name="FieldName"/>` — resolve all IDs from CONTEXT.json
- Portal objects contain child `<LayoutObject>` elements for each column field
- Button objects include `<Script id="N" name="ScriptName"/>` for the wired script and optional `<Parameter>` for the script parameter calculation

#### Validation and deployment

After generating XML2:

1. Write to `agent/sandbox/{layout-name}-objects.xml`
2. Run the validator:
   ```bash
   python3 agent/scripts/validate_snippet.py agent/sandbox/{layout-name}-objects.xml
   ```
3. Fix any validation errors
4. Deploy per the current tier:

   **Tier 1** — load to clipboard and present paste instructions:

   ```bash
   python3 agent/scripts/clipboard.py write agent/sandbox/{layout-name}-objects.xml
   ```

   > The layout objects are on your clipboard. To install them:
   >
   > 1. Open **{Layout Name}** in Layout Mode
   > 2. **⌘V** — paste the objects onto the layout
   > 3. Adjust positions as needed — objects are placed at their designed coordinates

   **Tier 2/3** — deploy via `agent/scripts/deploy.py` if layout paste automation is supported.

### Web Viewer path

Generate a self-contained HTML file with the theme CSS, JavaScript data binding, and FM bridge integration. This is the same output as the `webviewer-build` skill — delegate to that skill if the developer chooses this path:

> Switching to the `webviewer-build` skill for the Web Viewer output path.

---

## Step 7: Post-deployment guidance

After deployment, provide guidance based on the output path:

### FM path

> Layout objects have been pasted. In Layout Mode:
>
> 1. Verify field bindings are correct (right-click > Field/Control > inspect the field reference)
> 2. Check that button scripts are wired correctly (right-click > Button Setup)
> 3. Adjust any positions that need fine-tuning
> 4. If conditional formatting is needed, apply it manually — conditional formatting rules cannot be set via clipboard paste
> 5. Save the layout and switch to Browse Mode to test

### Web Viewer path

> The Web Viewer HTML has been generated. To use it:
>
> 1. Add a Web Viewer object to your layout in Layout Mode
> 2. Set its URL to the HTML file path or embed the HTML directly via a calculation
> 3. Install the companion FM scripts (data loader and event handler)
> 4. Test data flow in both directions

---

## Constraints

- The agent **cannot create the layout container** — only objects on it. The developer must create the layout in FM first and run Push Context.
- All field references must resolve to real IDs from CONTEXT.json — never use placeholder or invented IDs.
- All style class names must come from `theme-classes.json` — never invent class names. If no class fits, use the closest match and note the limitation.
- FM layouts are **not responsive** — all objects use fixed pixel positions. The preview must reflect this (no flexbox, no percentage widths).
- Portal child objects are positioned relative to the portal, not the layout.
- The `XML2` clipboard class is auto-detected by `clipboard.py` from `<LayoutObject` elements.
- Conditional formatting rules cannot be included in XML2 clipboard paste — note any conditional formatting in the spec for manual application.
- Tab controls and slide controls have complex nesting — read an existing example from `xml_parsed/layouts/` before generating these object types.
