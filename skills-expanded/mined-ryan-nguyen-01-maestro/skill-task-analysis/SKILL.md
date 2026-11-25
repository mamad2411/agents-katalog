---
name: skill-task-analysis
description: Convert HLD, LLD, ticket text, bug reports, or direct user text into a normalized task spec before implementation.
category: workflow
---

# Skill: Task Analysis

Use before any coding task starts.

## Normalize into

```text
intent
business goal
acceptance criteria
out of scope
impacted services
technical requirements
contract changes
risks
blockers
critical checks
dev verification checklist
QC focus
clarifying questions
```

## User Review Gate

After writing task-analysis.yaml, present the full spec to the user for review:

```text
1. Show: intent, acceptance criteria, impacted services, risks, critical checks
2. Ask user: "Task analysis này đã OK chưa? Có cần chỉnh sửa gì không?"
3. If user requests changes → update task-analysis.yaml → re-present
4. If user approves → mark user_approved: true → route to Coder Leader
5. Do NOT proceed to Coder Leader without explicit user approval (R-004-08, R-011-10)
```

## Design Asset Extraction (UI/frontend tasks)

When the task involves UI implementation and Figma URLs are provided:

```text
1. EXTRACT: Use get_design_context or get_metadata on the largest parent frame
   - Prefer 1 call on the parent frame over many calls on individual screens
   - If user provides a single large frame URL → use "Fast Mode" (1 call)

2. SAVE locally to .maestro/work/tasks/<task-id>/assets/:
   - design-context.md        ← Code reference from get_design_context
   - mockup-overview.png      ← Screenshot from get_screenshot
   - design-tokens.json       ← Extracted tokens (colors, spacing, typography)
   - image-assets.yaml        ← Icon/image inventory with export instructions

3. DETECT FIGMA RATE-LIMIT TIER:
   Check project config or ask user for Figma plan:
   - high_tier (200 calls/day — Organization/Enterprise/Professional):
     → figma_tier: high
     → Coders CAN call get_screenshot on individual icon nodes during coding
     → image-assets.yaml records node_ids only, coder exports live
   - low_tier (6 calls/month — Starter/Free):
     → figma_tier: low
     → ALL visual data must be pre-extracted during task-analysis
     → image-assets.yaml must include placeholder_spec for EVERY image slot
     → Coders NEVER call Figma MCP — read local files ONLY
   Record figma_tier in image-assets.yaml header.

4. EXTRACT IMAGE & ICON ASSETS:
   a. From get_design_context response, identify all image/icon nodes:
      - Icons (SVG vectors): logo, search, user, wishlist, arrows, social
      - Product images: placeholder rectangles referencing fills
      - Decorative elements: dividers, borders, background patterns
   b. For each icon/image, record in image-assets.yaml:
      - node_id, node_name, type (icon|image|decorative)
      - size (width × height), format_hint (svg|png|jpg)
      - usage (where in the UI), export_priority (required|nice-to-have)
   c. For LOW TIER — add placeholder_spec for every image/icon slot:
      - exact dimensions (width × height in px)
      - aspect_ratio (e.g., "304:313")
      - object_fit (cover|contain|fill)
      - border (e.g., "1px solid #d7d7d7")
      - border_radius (e.g., "0px" or "8px")
      - background_color (bg of container behind image)
      - alt_text_pattern (e.g., "${product.name} - ${product.category}")
      - loading (lazy|eager)
      → This ensures when real images replace placeholders, they fit 100%.
   d. Export methods vary by tier:
      HIGH TIER: Coders call get_screenshot per icon node during coding.
      LOW TIER: Task-analysis exports all required icons NOW:
        - SVG: Figma REST API GET /v1/images/:file_key?ids=:node_id&format=svg
        - PNG: get_screenshot on icon nodes (batch: comma-separated node_ids)
        - Save to assets/icons/ and assets/images/ immediately
        - Product images: record placeholder_spec only (real images from CMS)
   e. Decorative elements:
      - Prefer CSS equivalents (border, gradient) — skip export
      - Only export if CSS cannot replicate

5. CREATE screen-map.yaml listing all screens:
   - Group screens by user flow (e.g., flow-1-cart, flow-2-shipping)
   - Mark each screen as: primary (has API data) | responsive | state
   - States (loading/error/empty) → describe in text, no API call needed

6. POPULATE design_references in task-analysis.yaml:
   - figma_urls: original URLs from user
   - screenshots: paths to saved local files
   - component_specs: components, states, breakpoints, interactions
   - image_assets: path to image-assets.yaml

7. API BUDGET: Minimize Figma API calls (see figma_tier above)
   - Fast Mode: 1-2 calls (parent frame + 1 detail if needed)
   - Detail Mode: 1 metadata + 1 per flow group (max 5-6 calls)
   - States/responsive variants → text description only
```

After extraction, coders read ONLY local files — zero subsequent Figma API calls.

### Example: TASK-demo-figma

Real example — Fashion e-commerce Home page extracted from Figma:

```text
Figma URL:
  https://www.figma.com/design/7xrPkquBzkRr2HLgTMKqr8/Fashion-Ecommerce-Store?node-id=2-63

Fast Mode (1 MCP call):
  get_design_context(fileKey="7xrPkquBzkRr2HLgTMKqr8", nodeId="2:63")
  → Returns React + Tailwind reference code for full page (1440x3998px)

Assets created:
  .maestro/work/tasks/TASK-demo-figma/assets/
  ├── design-context.md       ← 8 sections breakdown (Header, Hero, Grid, etc.)
  ├── design-tokens.json      ← Colors (#000e8a accent, #f5f5f5 bg), fonts (Beatrice family),
  │                              spacing (32/16/12/8px), component specs (ProductCard 304x313)
  ├── screen-map.yaml         ← 7 screens in flow-1-home, 3 shared components,
  │                              3 states (loading/empty/filter-active)
  └── image-assets.yaml       ← 14 icons + 6 product images inventoried
                                 (Group6=logo, Group45=wishlist, Vector=arrows, etc.)
                                 Export instructions: SVG via REST API, PNG via get_screenshot

task-analysis.yaml design_references:
  figma_urls: [{url: "...", node_id: "2:63", description: "Home page"}]
  component_specs:
    - ProductCard: 2 variants (small 304x313, large 366x376), states [default, hover, loading]
    - FilterTabs: states [active (bold), inactive (#8a8a8a)]
    - SearchBar: states [default, focused]
  local_assets:
    design_context: ".maestro/work/tasks/TASK-demo-figma/assets/design-context.md"
    design_tokens: ".maestro/work/tasks/TASK-demo-figma/assets/design-tokens.json"
    screen_map: ".maestro/work/tasks/TASK-demo-figma/assets/screen-map.yaml"
```

See full example at `.maestro/work/tasks/TASK-demo-figma/`.

## Rules

```text
Do not code during analysis.
Mark ambiguity explicitly.
Prefer task evidence over guesses.
Identify cross-service impact early.
For governed work, do not route to Coder Leader without user approval of task-analysis.yaml.
```
