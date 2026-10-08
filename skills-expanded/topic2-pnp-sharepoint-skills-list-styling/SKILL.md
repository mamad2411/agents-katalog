---
name: list-styling
description: Apply a visual style theme to any SharePoint list or document library using column formatting, view formatting, row templates, and tile layouts. Use this skill whenever the user asks to style, theme, or visually transform a list or library. The goal is "I can't believe that's SharePoint" impact — not just color swaps, but fully art-directed views. This skill works with any style token file.
---

# List Styling Engine

Transform SharePoint lists and document libraries into fully art-directed views. This is not a color palette swap — it's a complete visual redesign using every formatting capability SharePoint provides.

**The bar: "I can't believe that's SharePoint."**

## Formatting Capabilities — Use ALL of These

SharePoint provides four levels of formatting. A properly styled view uses MULTIPLE levels together. Do not stop at column formatting.

### Level 1: Column Formatting
Per-column rendering. Controls how individual cell values display.
- Status badges, progress bars, date compositions
- Applied via: Column header → Column settings → Format this column → Advanced mode

### Level 2: View Formatting (additionalRowClass)
Adds CSS classes to existing rows. Lightweight — doesn't change layout.
- Alternating row colors, conditional row highlighting (overdue tinting)
- Applied via: View dropdown → Format current view → Advanced mode

### Level 3: Row Template (rowFormatter)
**REPLACES the entire row layout.** This is the power move. Instead of SharePoint's default column grid, you define the complete HTML structure of each row.
- Full card layouts with sidebars, composed metadata, multi-section rows
- Can combine multiple columns into a single visual composition
- Applied via: View dropdown → Format current view → Advanced mode (uses `rowFormatter` key instead of `additionalRowClass`)

### Level 4: Tile Formatting
Gallery/card view layouts. Each item renders as a card instead of a row.
- Standalone card designs with headers, bodies, footers, progress indicators
- Applied via: Gallery view → Format current view → Advanced mode

**Rule: Every style MUST use at least Level 1 + Level 3. Level 3 (rowFormatter) is what creates the "I can't believe it" impact. Column formatting alone is a 3/10.**

---

## The Style Application Workflow

### Step 1: Read the list schema — required before generating any JSON
Know the columns, their internal names, types, and Choice values. Get this from SHAREPOINT.md if available, or ask the user. **Do not generate any JSON until you have the actual column names and Choice values.**

### Step 2: Read the style token file
Load the matching `style-{name}/style-{name}/SKILL.md`. It contains design tokens and a `rowFormatter` reference template. The column names in that template (`[$Status]`, `[$Progress]`, `[$Deadline]`) are **example placeholders** that almost certainly do not match the user's list.

### Step 3: Map the user's columns to the template

The style file's rowFormatter uses reference column names: `[$Title]`, `[$FileLeafRef]`, `[$Status]`, `[$Progress]`, `[$Deadline]`. These are examples — the user's list will likely have different column names.

**Before applying the rowFormatter, you MUST adapt it:**

#### Column-discovery checklist

Run this checklist against the schema you read in Step 1 **before** you start the find-and-replace. If you skip it, the generated JSON will reference columns that don't exist and the view will render blank cells.

- [ ] **List every column** the user's list actually has, with its **internal name** (not display name). Spaces in display names become `_x0020_` in internal names — the rowFormatter uses internal names.
- [ ] **Confirm the four role columns** are present and capture each one:
  - Name/Title role → internal name = `______`
  - Status role (Choice) → internal name = `______`, choices = `______`
  - Progress role (Number 0–100) → internal name = `______`
  - Deadline role (DateTime) → internal name = `______`
- [ ] **Capture the exact Choice values** for the Status column — case-sensitive. "In Progress" ≠ "in progress" ≠ "InProgress".
- [ ] **Note the Number column scale.** SharePoint stores `0.72` for a 72% slider but `72` for a free-entry number column. The rowFormatter must treat the value accordingly — do not assume.
- [ ] **Check the Date column format.** Date-only vs Date-and-time changes which expression to use for overdue comparisons against `@now`.
- [ ] **List any "extra" columns** the user wants surfaced (Owner, Priority, Category, etc.) and decide their slot per Step 3 rule 4 below.
- [ ] **List any "missing" template columns** (e.g. the user has no Deadline) and mark the corresponding rowFormatter section for removal per Step 3 rule 5.

If any item above cannot be filled in from the schema, **stop and ask the user** — do not guess column names or choice values.

1. Identify which column in the user's list serves each role:
   - **Name/Title role**: The item or document name (e.g., `[$Title]`, `[$FileLeafRef]`, `[$ProjectName]`)
   - **Status role**: A Choice column with workflow states (e.g., `[$Status]`, `[$Phase]`, `[$Stage]`)
   - **Progress role**: A Number column 0-100 (e.g., `[$Progress]`, `[$Completion]`, `[$PercentComplete]`)
   - **Deadline role**: A DateTime column (e.g., `[$Deadline]`, `[$DueDate]`, `[$TargetDate]`)

2. Find-and-replace all `[$ReferenceName]` values in the rowFormatter JSON with the actual internal column names.

3. Update the status_colors `if()` expressions to use the actual Choice values from the user's list. If they use "Active" instead of "In Review", or "Complete" instead of "Published", remap accordingly using the same color logic from the style tokens.

4. If the user's list has ADDITIONAL columns not covered by the style template (e.g., Owner, Priority, Category), decide where to surface them:
   - In the sidebar/panel area alongside existing metadata
   - In the main content area replacing the "Open Item" button
   - As additional inline elements in the metadata row

5. If the user's list is MISSING a column the template expects (e.g., no Deadline column), remove that section from the rowFormatter rather than letting it error.

**The style's rowFormatter is a reference implementation. Adapt it to the user's data — do not paste it verbatim.**

### Step 4: Generate formatters — in this order

**A. Row Template (rowFormatter) — DO THIS FIRST**
This is the centerpiece. The style token file defines the row layout structure. Generate the complete `rowFormatter` JSON that composes all columns into the styled row design.

**B. Column Formatters — FOR COLUMNS NOT HANDLED BY rowFormatter**
If the row template covers Status, Progress, and Deadline inline, you may not need separate column formatters for those. But any column NOT included in the rowFormatter still needs its own formatter.

**C. View Formatting — IF the style uses alternating rows or row highlighting**
Add `additionalRowClass` only if the style specifies it AND only if you're NOT using a `rowFormatter` (the two conflict — `rowFormatter` replaces the row entirely, so `additionalRowClass` has no effect when `rowFormatter` is active).

**D. Tile Formatting — IF the user wants a gallery/card view**
Generate tile formatting for card-based layouts.

### Step 5: Create a custom view
Tell the user to create a new view named after the style (e.g., "Neobrutalism") so the formatting doesn't affect the default "All Items" view.

### Step 6: Preview and test before committing

**Never apply formatting to the default view, and never tell the user to skip this step.** A broken `rowFormatter` makes a list look empty and is a frightening experience for anyone who isn't a developer.

1. Confirm the user is on the **new view** created in Step 5 — not "All Items" / "All Documents".
2. Have the user paste the JSON via **Format current view → Advanced mode** and **click Preview**, not Save. The preview pane renders the row template against real data without persisting it.
3. Walk through this checklist against the preview:
   - [ ] Every row renders (no blank rows, no `[$ColumnName]` literals leaking through).
   - [ ] Status pills show the right color for at least one row of each Choice value.
   - [ ] Progress bars show varied widths — not all 0% and not all 100%.
   - [ ] Deadline composition renders both a future date and a past date correctly (overdue treatment fires).
   - [ ] Clickable elements open the item (`customRowAction` with `defaultClick` works).
   - [ ] Resize the browser to ~600 px wide — see Step 7 below.
4. Only after the preview checklist passes, tell the user to click **Save**.
5. If anything in the checklist fails, iterate on the JSON — do not ask the user to save first and fix later. SharePoint will happily save a broken formatter.

### Step 7: Mobile responsiveness

A styled view that looks incredible on a 1920-px monitor and breaks on a phone is half a solution. SharePoint lists are rendered in three places that matter — desktop browser, Teams mobile, and the SharePoint mobile app — and they all hit narrow viewports.

Apply these rules to every `rowFormatter` you generate, regardless of style:

- **No fixed pixel widths greater than 240 px on row sections.** The 280-px sidebar pattern that appears in several style templates clips badly on mobile. Either drop to ≤ 240 px or convert the layout to use `flex` with `flex-basis` and `flex-grow` so the section can shrink.
- **Wrap, don't overflow.** Use `flex-wrap: wrap` on the outer row container so the sidebar drops below the main content on narrow viewports instead of being cut off. Set `min-width: 0` on text children so long titles ellipsis-truncate rather than push their parent wider.
- **Hide secondary metadata under ~480 px**, don't shrink it to unreadable. SharePoint supports `"@window.innerWidth < 480 ? 'none' : 'flex'"` style expressions — use them on tertiary chips (Owner, Category, sublabels) so the row stays scannable on a phone.
- **Hero number sizing.** Progress percentages and status pills that look right at 32 px on desktop are oversized on mobile. Use a step-down expression: `"@window.innerWidth < 480 ? '20px' : '32px'"`.
- **Touch targets.** Anything `customRowAction`-clickable must be at least 44 × 44 px on mobile. Don't ship pill-clicks that only work on a mouse.
- **Test the preview at ~375 px (iPhone), ~600 px (tablet portrait), and ≥ 1024 px (desktop)** before saving — SharePoint's preview pane respects window resizing.

If a style token file is missing responsive breakpoints, fill them in using the rules above and **report this back to the user** so they know the generated formatter is more responsive than the upstream style spec.

### Step 8: Apply and verify

---

## rowFormatter Structure

This is the most powerful tool. It replaces the entire row with a custom layout.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/sp/v2/view-formatting.schema.json",
  "hideSelection": false,
  "hideColumnHeaders": true,
  "rowFormatter": {
    "elmType": "div",
    "style": { ... },
    "children": [ ... ]
  }
}
```

**Key behaviors:**
- `hideColumnHeaders: true` — hides the default column headers since the row template defines its own layout
- Access any column value with `[$InternalColumnName]`
- Can compose multiple columns into a single visual element
- Supports all the same style properties as column formatters
- Can include buttons, links, icons, conditional elements

**Layout patterns the style file can define:**
- **Card row**: Full-width card per item with sidebar + main content
- **Split row**: Left panel (metadata) + right panel (details)
- **Compact row**: Single line with composed inline elements
- **Summary card**: Tile-style card within a list view

---

## SharePoint JSON Formatting Reference

### Supported
- `elmType`: `div`, `span`, `a`, `img`, `svg`, `path`, `button`
- All CSS properties via inline `style` object
- `border-radius`, `text-transform`, `box-shadow`, `overflow`, `gap` — all work
- Colors: hex only (`#ffffff`)
- Emoji in `txtContent` — works for icons
- `customRowAction` with `action: "defaultClick"` — makes elements clickable to open the item
- `forEach` — iterate over multi-value fields
- Expressions: `@currentField`, `[$ColumnName]`, `@now`, `@me`, `@rowIndex`
- `toString()`, `Number()`, `toLocaleDateString()`, `if()`, `indexOf()`, `substring()`

### NOT Supported
- `backdrop-filter`, gradients, `rgb()`/`rgba()`/`hsl()`
- Custom CSS classes in column formatters (only built-in SP classes in `additionalRowClass`)
- CSS variables, hover pseudo-states
- Nested `if()` beyond ~10 levels

### Common Mistakes
- Forgetting `$schema`
- Display names vs internal names (spaces → `_x0020_`)
- Case-sensitivity on Choice values
- Number column stores 0.72 not 72
- Trailing commas (invalid JSON)
- Using `additionalRowClass` WITH `rowFormatter` (they conflict — rowFormatter wins)

---

## What "11/10 Ambition" Looks Like

The difference between "formatted" and "I can't believe that's SharePoint":

| Formatted (3/10) | Styled (7/10) | Art-Directed (11/10) |
|---|---|---|
| Colored status pills | Status badges with style-specific shape/border | Full row template with composed status + progress + deadline in a card layout |
| Default progress bar colors | Styled progress bar (height, border, colors) | Progress bar integrated into the row card with contextual coloring and inline label |
| Date string | Date with overdue coloring | Composed deadline block with icon, date, sublabel, and conditional overdue treatment — all positioned within the row card |
| Default row grid | Alternating row colors | Complete row template that recomposes the entire layout into the style's signature pattern |
| No view changes | Custom view name | Custom view with rowFormatter + style-specific header treatment |

**The token file defines the row template. The engine generates it. RALPH iterates until it hits 11/10.**

---

## Application Instructions

**Creating a styled view:**
1. Go to the list/library
2. Click "Add view" → name it after the style (e.g., "Neobrutalism")
3. Select columns to include: the columns identified in your Step 3 mapping
4. Save the view
5. Click the view dropdown → "Format current view" → "Advanced mode"
6. Paste the rowFormatter JSON
7. For any columns NOT covered by the rowFormatter, apply individual column formatters

**Important:** Always create a new view. Never modify "All Items" or "All Documents" directly.
