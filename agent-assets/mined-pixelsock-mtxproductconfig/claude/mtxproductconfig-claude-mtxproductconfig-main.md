<!-- OPENSPEC:START -->
# OpenSpec Instructions

These instructions are for AI assistants working in this project.

Always open `@/openspec/AGENTS.md` when the request:
- Mentions planning or proposals (words like proposal, spec, change, plan)
- Introduces new capabilities, breaking changes, architecture shifts, or big performance/security work
- Sounds ambiguous and you need the authoritative spec before coding

Use `@/openspec/AGENTS.md` to learn:
- How to create and apply change proposals
- Spec format and conventions
- Project structure and guidelines

Keep this managed block so 'openspec update' can refresh the instructions.

<!-- OPENSPEC:END -->

## Purpose
This configurator is fully dynamic and Supabase-driven. Agents must read tables (not hard-code logic) to determine:

Which option sets exist and how to render them
Which options are available for a given product
How rules set values/disable options
How to assemble the final SKU deterministically
Golden rule: No fallback logic. If data is missing, surface it; do not guess.

## Data model (source of truth: Supabase)

### Settings (control behavior)

#### rules table
Fields: id (uuid), name (varchar), priority (int|null), if_this (jsonb), then_that (jsonb)
Behavior: when if_this matches, apply then_that. Setting a value disables all other options in that table (see Rules Behavior). Rules do not hide options; only overrides do.

#### configuration_ui table
Fields: id (uuid), collection (varchar), ui_type (varchar), sort (int).
Defines render order and widget type for each option table (e.g., single, multi, grid-2, full-width, size-grid, color-swatch).

#### sku_code_order table
Fields: id (uuid), sku_code_item (varchar), order (int)
Defines SKU segment order. Always starts with products at order:0. If a table doesn't apply to a product, skip it.

### Product taxonomy & options

#### product_lines table
Fields: id, name, sku_code, active, default_options (m2a via junction)
Junction: product_lines_default_options → rows of { product_lines_id, collection, item }.

#### products table
Core fields: id, name, sku_code (base), product_line (m2o), mirror_style (m2o), light_direction (m2o), images (vertical_image, horizontal_image), additional_images (files), options_overrides (m2a)
Overrides via products_options_overrides → { products_id, collection, item }
Typed pointer example: frame_thickness: { \"key\": 2, \"collection\": \"frame_thicknesses\" }

### Option tables (each item has id, name, sku_code, active, sort, plus table-specific fields):

- mirror_styles (e.g., svg_code.variants.vertical/horizontal)
- light_directions (1=Direct d, 2=Indirect i, 3=Both b)
- frame_thicknesses (sku_code exists but not appended; see SKU rules)
- frame_colors (hex_code)
- mounting_options, drivers, light_outputs, color_temperatures
- accessories (multi-select), sizes (width, height)

Removed: mirror_controls is deprecated and should not be referenced by agents or rules.

## Evaluation lifecycle (deterministic)

### 1. Select product 
Load the products record and its product_line.

### 2. Seed availability from product line defaults 
Resolve product_lines.default_options (through product_lines_default_options) into allowed options per table.

### 3. Apply product option overrides 
If a product has overrides for a table, those replace the allowed set for that table (they don't extend).
If a previously selected value is not in the override set, auto-clear the selection.

### 4. Pre-applied product fields 
If the product sets a value (e.g., light_direction: 2), treat it as the current selection (UI should show it locked unless later set by rules).

### 5. Render UI from configuration_ui 
Sort by sort ascending and render each table with the given ui_type.

Hidden vs disabled:
- Hidden only when excluded by overrides (not visible in the list).
- Disabled happens when rules set a value; other options in that table remain visible but disabled.

### 6. Rules processing
- Priority: process all rules with numeric priority first (ascending). After that, process rules with priority: null (order not significant; if you need a tiebreaker, use id ASC for determinism).
- On match, then_that sets fields (e.g., light_output = 2) and disables all other options in that table for the session state.
- Rules may also set product images; when they do, rule images supersede product images.

### 7. SKU assembly
- Start with product's base sku_code (e.g., T03b, W01d).
- Append option sku_codes in the order defined by sku_code_order.
- Skip tables that don't apply to the current product.
- Case matters: preserve each option's sku_code exactly as stored.

Multi-select: currently only Accessories is multi-select, but it ultimately yields a single sku_code via rules:
- If no accessory selected → rules set NA (canonical \"none\").
- If a special combo is selected (e.g., Night Light + Anti-Fog) → rules set a combined code (e.g., AN).
- If future multi-select tables are added without a bespoke rule, default to order of selection for concatenation.

Note: frame_thickness is already encoded into the product's base sku_code and is not appended again.

## Rules behavior (contract)

### Condition operators: 
_eq, _neq, _in, _nin, _and, _or, _empty.

Validation: Disallow _eq: null (data error). Use _empty: true to test \"no selection.\"

### Actions (then_that):

#### Set value: 
e.g., { \"light_output\": { \"_eq\": 2 } }
Effect: select light_output=2 and disable all other light outputs (visible but disabled).

#### Set images: 
e.g.,
```json
{ \"_and\": [
  { \"product\": { \"vertical_image\": { \"_eq\": \"<file-id>\" } } },
  { \"product\": { \"horizontal_image\": { \"_eq\": \"<file-id>\" } } }
]}
```
Rule-driven images override product images for rendering.

#### Set SKU segment: 
e.g., { \"accessory\": { \"sku_code\": { \"_eq\": \"AN\" } } }

Rules do not filter/hide options from the UI; they set values and disable alternatives.

Priority semantics: lower number executes earlier; all numeric priorities run before any null priority rules.

## Option overrides (contract)
- Scope: by product and table.
- Semantics: If overrides exist for a table, they become the only allowed options for that table on that product.
- UI: Non-overridden options are hidden.
- Selections: If a current selection becomes disallowed by overrides, auto-clear and require re-selection.

## SKU assembly (contract)
1. Initialize: sku = product.sku_code
2. For each entry in sku_code_order sorted by order ASC (skipping order:0 which is the product):
   - Resolve the selected option in the given sku_code_item table.
   - If no selection exists (and no rule forces one), skip.
   - Concatenate its sku_code to sku.
   - Preserve exact case of each segment.

Accessories:
- If no selection: rule should set NA.
- If combo present: rule sets the combined code (single segment).
- Future generic multi-select: default to order of selection if no rule provided.

## Example snippets (from live data)

### Option items
- mirror_styles/1 → sku_code: \"01\" (has svg_code.variants)
- light_directions/1 → sku_code: \"d\"
- frame_thicknesses/1 → sku_code: \"W\" (not appended)
- frame_colors/1 → sku_code: \"BF\", hex_code: \"#000000\"
- mounting_options/1 → sku_code: \"W\"
- drivers/1 → sku_code: \"V\"
- light_outputs/1 → sku_code: \"S\"
- color_temperatures/1 → sku_code: \"27\"
- accessories/34 (Night Light) → sku_code: \"NL\"
- sizes/23 → sku_code: \"2436\"

### Configuration UI
configuration_ui/... → { collection: \"light_directions\", ui_type: \"full-width\", sort: 8 }

### Rules
Driver forces light output (sets and disables others):
If driver ∈ {4,5} → light_output = 2

Accessories \"none\":
If accessory _empty: true → set accessory.sku_code = \"NA\"

Polished + Hanging technique sets images:
When conditions match, set both vertical_image and horizontal_image → rule images override product images.

### Product overrides
A product with options_overrides restricting sizes to a subset (e.g., {5,6}) → all other sizes are hidden for that product.
Auto-clear: if user had size 7 selected previously, clear and force re-select from the allowed set.

## UI behavior (for agents)
1. Render tables in configuration_ui.sort order.
2. Respect ui_type to choose widgets.
3. Hidden only via overrides. Disabled via rules.
4. When a rule sets a field, keep the chosen item enabled and disable the rest (still visible).

## Validators & checks (agents should run)

### Schema sanity
- product_lines_default_options: no rows with product_lines_id: null (data issue).
- All tables referenced in configuration_ui.collection exist.

### Rules hygiene
- Disallow _eq: null in conditions or actions (use _empty for checks).
- File IDs referenced in image actions exist.
- If multiple rules target the same field, ensure consistent outcome (priority wins).

### Overrides integrity
- Each products_options_overrides item exists and active: true.
- If overrides exist for a table, selection must be within the override set (else auto-clear).

### SKU integrity
- Every selected option used for SKU has a non-empty sku_code.
- sku_code_order starts with products at order:0; duplicates disallowed.
- frame_thicknesses present? ensure it's not appended (documented exception).

## Do / Don't for agents

### Do
- Drive everything from Supabase reads.
- Apply lifecycle steps in order (defaults → overrides → pre-set product fields → UI → rules → SKU).
- Disable (don't hide) alternatives when rules set a value.
- Preserve SKU segment case and ordering from sku_code_order.
- Auto-clear invalid selections when overrides change availability.

### Don't
- Invent options or fall back when data is missing.
- Append frame_thickness to SKU (it's encoded in product base code).
- Use rules to \"filter/hide\" options; use rules only to set or set & disable.

## Implementation notes (pseudo)
```javascript
// 1) load product + line
const product = getProduct(id)
const line = getProductLine(product.product_line)

// 2) allowed = line defaults per table
const allowed = deriveAllowedFromLine(line.default_options)

// 3) apply product overrides (replace per table)
applyOverrides(allowed, product.options_overrides)

// 4) seed state with product's fixed fields (e.g., light_direction)
const state = seedFromProduct(product)

// 5) render UI from configuration_ui
const ui = getConfigUI().sort(bySort)

// 6) run rules: numeric priorities ASC, then nulls (id ASC as tie-breaker if needed)
const rules = getRules()
applyRules(state, rules)

//   - rule \"set\" behavior: set value + disable all others in that table
//   - rule images override product images

// 7) assemble SKU
const order = getSkuCodeOrder().sort(byOrder)
const sku = buildSku(product.sku_code, state, order, { skipFrameThickness: true })
```

## Dynamic filtering (product-backed availability)

Goal: reflect actual inventory of products within a product line when narrowing user choices, without hard-coding. Dynamic filtering is derived from the products table, per current selections.

### Principles
Mirror Style is the anchor. It determines the set of actual product records available within the chosen product_line.

Example: B05 has two SKUs: B05b (Both) and B05d (Direct). Therefore, both light-direction values are dynamically available for that mirror style.
Example: T22 exists only as T22i. Therefore, only Indirect is available for that mirror style.

Mirror Styles should not be disabled by dynamic filtering. They can only be hidden via product overrides or disabled by rules. Dynamic filtering can disable other tables (e.g., light_direction) based on available product combinations, but mirror_styles remain selectable unless explicitly removed by overrides or rules.

No hard-coded matrices. Availability is computed from products rows that match the current product_line and whatever has already been chosen.

### Algorithm (facet-style)
1. Start scope: all products in the active product_line and active=true.
2. Facet counts by key attributes that are M2O on products (e.g., mirror_style, light_direction, etc.).
3. When user selects mirror_style = X:
   - Filter the product scope to mirror_style = X.
   - Recompute facet availability for other tables from that reduced scope (e.g., show only light directions that exist among remaining products).
   - Do not disable other mirror styles at this step (unless rules/overrides say so); they remain available to switch.
4. When user selects additional facets (e.g., light_direction = Indirect):
   - Filter scope again and recompute availability for remaining tables.
5. No matching products: if a choice combination leads to an empty scope, signal no products available, and guide user to adjust selections (do not fallback).

### UI semantics
Disabled vs hidden:
- Dynamic filtering disables options that have zero matching products in the current scope.
- Overrides hide options (product-specific restriction).
- Rules set a value and disable alternatives.

Switching mirror styles: allowed any time; dynamic filtering immediately recomputes availability for dependent sets (e.g., light_direction).

### Performance notes
- Pre-compute per-product_line facet maps at load (products → counts by { mirror_style, light_direction, … }).
- Cache results in memory; invalidate when product list changes.

## Open items (defaults chosen if unspecified)
- Equal-priority tiebreaker: after numeric priorities, process null priorities in id ASC order for determinism.
- Rule side-effects: value set ⇒ disable others (don't hide).
- Future multi-select tables: If no special combo rule exists, concatenate in order of selection.
- Validation: disallow _eq: null; use _empty for presence checks.

## Supabase-specific notes
- All data access is through direct Supabase  API via SQL like queries
- Use RPC functions for complex queries that require joins across multiple tables
- Leverage Postgres JSONB operators for efficient filtering on JSON fields
- Consider using materialized views for frequently accessed computed data
- Row Level Security (RLS) policies may affect data visibility based on user context
`
}