---
name: layout-spec
description: Conduct a design conversation and produce a written layout specification for a FileMaker layout — object list, field bindings, section layout, portal configuration, button wiring, and style assignments. No XML output — this is the planning and consulting skill. Use when the developer says "layout spec", "layout blueprint", "spec out layout", "describe layout", or asks what objects a layout should contain.
---

# Layout Spec

Design a complete layout specification through a structured conversation with the developer. The output is a written blueprint — not XML or code — that describes every object, its position, its data binding, and its styling. This spec can be used as a manual build guide or as input to the `layout-design` skill for automated generation.

---

## Step 1: Gather context

1. Check for `agent/CONTEXT.json`. If it exists, read it for:
   - `current_layout` — the layout being designed (name, TO, dimensions if available)
   - `tables` — available fields and their types
   - `relationships` — related TOs available for portals
   - `scripts` — scripts available for button wiring
   - `value_lists` — value lists for dropdowns and radio buttons
   - `layouts` — other layouts for navigation buttons

2. If CONTEXT.json is absent or scoped to the wrong layout, ask the developer to run **Push Context** on the target layout before proceeding.

3. Read the theme manifest and style classes if they exist:
   ```bash
   ls agent/context/*/theme-manifest.json 2>/dev/null
   ls agent/context/*/theme-classes.json 2>/dev/null
   ```
   If theme data exists, read `theme-manifest.json` for the color palette and layout builder constants (default margins, field heights, label widths, portal row heights). Read `theme-classes.json` for available named style classes.

4. If theme data does not exist, note this to the developer and proceed with generic spacing recommendations. Suggest running `python3 agent/scripts/extract_theme.py` to extract theme data from the solution.

---

## Step 2: Determine layout type

Ask the developer what type of layout this is. Common FM layout types:

| Type | Purpose | Key characteristics |
|------|---------|---------------------|
| **Detail view** | View/edit a single record | Fields arranged in sections, possibly with related portals |
| **List view** | Browse multiple records | Repeating body part with summary fields, column headers in header |
| **Card window** | Modal detail or picker | Compact, focused on a single task, fixed dimensions |
| **Dashboard** | Overview with metrics | Summary fields, charts, navigation buttons, minimal data entry |
| **Print layout** | Report output | Precise positioning, sub-summary parts, trailing grand summary |
| **Utility** | Background or data-only | Minimal UI, used by scripts for context switching |

If the developer has already described the purpose, infer the type and confirm.

---

## Step 3: Design conversation

Walk through each design decision with the developer. Apply these UI/UX principles within FileMaker's fixed-position constraints:

### Grouping and sections
- Group related fields together (e.g., contact info, address, financial details)
- Use rectangles or lines as visual separators between sections
- Place section labels as text objects above each group

### Visual hierarchy
- Primary fields (name, title, status) should be larger and positioned at the top
- Secondary fields (dates, codes, internal IDs) can be smaller and positioned lower
- Use bold or larger text styles for section headers
- Status indicators should be visually prominent (conditional formatting)

### Alignment
- Left-align labels with consistent label width across sections
- Align field left edges within a section
- Use a consistent gutter between label and field
- Maintain consistent vertical spacing between field rows

### Portal design
- Portals need a header row (text labels above the portal, not inside it)
- Define visible row count based on available space
- Include a vertical scroll bar for portals with variable record counts
- Consider which fields to show in each portal row — keep it scannable

### Navigation and actions
- Place navigation buttons in the header or top navigation part
- Group action buttons (Save, Cancel, Delete) consistently — typically top-right or bottom
- Wire buttons to specific scripts from CONTEXT.json

### Layout parts
For each part the layout will use, define:
- **Part type**: Header, Body, Footer, Top Navigation, Title Header, Sub-Summary, Trailing Grand Summary
- **Height**: in pixels
- **Background**: fill color or style from the theme

---

## Step 4: Produce the specification

Write the specification in a structured format. Include every object with enough detail for either manual construction or automated generation.

### Specification format

```
# Layout Specification: {Layout Name}

**Based on TO**: {Table Occurrence name}
**Layout type**: {Detail / List / Card / Dashboard / Print}
**Layout width**: {width in pixels}

## Parts

| Part | Height (px) | Background |
|------|-------------|------------|
| Header | 80 | Theme default |
| Body | 600 | White |
| Footer | 40 | Theme default |

## Section: {Section Name}

**Position**: Top-left corner at ({left}, {top}) relative to part

| Object | Type | Field/Value | Position (L, T, R, B) | Style Class | Notes |
|--------|------|-------------|----------------------|-------------|-------|
| Label: Client Name | Text | "Client Name" | (20, 90, 120, 110) | Field Label | |
| Field: ClientName | Edit Box | Clients::ClientName | (130, 90, 400, 110) | Data Field | |
| Label: Email | Text | "Email" | (20, 120, 120, 140) | Field Label | |
| Field: Email | Edit Box | Clients::Email | (130, 120, 400, 140) | Data Field | |

## Section: Related Invoices

**Portal configuration**:
- Related TO: Invoices_by_Client
- Visible rows: 5
- Row height: 22px
- Position: (20, 200, 780, 310)
- Vertical scroll bar: Yes
- Allow creation via relationship: No

| Column | Field | Width | Style Class |
|--------|-------|-------|-------------|
| Invoice # | Invoices_by_Client::InvoiceNumber | 100 | Portal Field |
| Date | Invoices_by_Client::InvoiceDate | 80 | Portal Field |
| Status | Invoices_by_Client::Status | 80 | Portal Field |
| Total | Invoices_by_Client::Total | 100 | Portal Field Right |

## Buttons

| Label | Position (L, T, R, B) | Script | Parameter | Style Class |
|-------|----------------------|--------|-----------|-------------|
| Save | (680, 10, 780, 35) | Save Record | "" | Primary Button |
| Cancel | (580, 10, 670, 35) | Cancel | "" | Secondary Button |
| New Invoice | (20, 310, 140, 335) | New Invoice | JSONSetElement ( "{}" ; "client_id" ; Clients::PrimaryKey ; JSONString ) | Action Button |

## Conditional Formatting

| Object | Condition | Style Change |
|--------|-----------|--------------|
| Field: Status | Status = "Overdue" | Text color: red, Bold |
| Field: Status | Status = "Paid" | Text color: green |

## Notes
- {Any design rationale, constraints, or follow-up items}
```

### Style class validation

When assigning style classes, only use classes that exist in `theme-classes.json`. If no class fits the intended purpose:
- Suggest the closest available class
- Note the limitation and recommend the developer create a custom style in Layout Mode after pasting

---

## Step 5: Review with the developer

Present the specification and ask for feedback:

> Review the layout specification above. You can request changes like:
> - "Move the portal below the address section"
> - "Add a Notes field spanning the full width"
> - "Use a button bar instead of separate buttons"
> - "Add a tab control with Details and History tabs"
>
> Reply with changes or confirm with "looks good" to finalize.

Iterate until the developer approves.

---

## Step 6: Output

The specification is the final deliverable of this skill. Present it in the conversation.

If the developer requests it saved to a file, write to `plans/layouts/{layout-name}-spec.md`.

After approval, suggest next steps:

> The layout specification is complete. Next steps:
>
> 1. **Create the layout shell** in FileMaker — Layout Mode > New Layout > name it **{Layout Name}**, base it on **{TO Name}**
> 2. Run **Push Context** on the new layout to refresh CONTEXT.json
> 3. Use the `layout-design` skill to generate the layout objects from this spec

---

## Constraints

- This skill produces a **written specification only** — no XML, no fmxmlsnippet, no HTML
- The agent cannot create the layout container — only specify what goes on it
- All field references must come from CONTEXT.json or index files — never invent field names or IDs
- All style class references must come from `theme-classes.json` when available — never invent class names
- Portal configurations must reference valid related TOs from CONTEXT.json or `relationships.index`
- Button script references must use script names and IDs from CONTEXT.json or `scripts.index`
