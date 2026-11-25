---
name: product-prototype-design
description: Generate standardized enterprise product prototypes from business requirements, prototype references, `.pen` files, HTML mockups, or design files. Defaults to Element Plus-style admin UI, supports query/add/edit/delete state pages, right-drawer workflows, full-page overlays, true table structures, pagination, business logic notes, and page-state consistency validation. Use when building or normalizing backend management prototypes with Pencil MCP.
---

# Product Prototype Design

## Purpose

Turn business requirements or existing prototype material into consistent, implementation-guiding product prototype pages for enterprise backend systems.

This skill is optimized for:

- Pencil MCP `.pen` generation
- admin CRUD pages
- page-state prototype systems
- Element Plus-style information architecture
- traditional admin-console visual shells
- business-logic-aware prototype review

Default desktop canvas:

- `1920 x 1080`

## Core Rules

### 1. Default to Element Plus

Unless the user explicitly overrides the design system:

- use Element Plus visual language
- use Element Plus component semantics
- use enterprise admin density, spacing, and hierarchy
- default to a traditional backend-management-system look, not a marketing-style or dashboard-hero look
- do not ask again for style reference when the request is a normal admin prototype
- use Element Plus to keep visible component styling consistent, not just to choose structure
- if a reference `.pen` is provided, extract layout structure, information hierarchy, note format, and content organization from it
- do not blindly inherit a reference `.pen` color palette or typography if it conflicts with Element Plus defaults

Read:

- `./references/element-plus-components-full.md`
- `./references/element-plus-prototype-mapping.md`
- `./references/element-plus-layout-rules.md`
- `./references/reference-pen-patterns.md`
- `./references/traditional-admin-visual-tokens.md`
- `./references/traditional-admin-shell-rules.md`
- `./references/traditional-admin-checklist.md`

### 2. Use page-state modeling for CRUD

For backend CRUD pages, generate these state pages separately:

1. 查询页
2. 新增页
3. 修改页
4. 删除页

### 3. Query page is the base page

The query page is the canonical base.

- build the query page first
- verify it first
- copy it into add/edit/delete state pages

Do not generate four unrelated pages independently.

### 4. Add/Edit are overlays, not rebuilt pages

For 新增页 and 修改页:

- keep the query-page base layout unchanged
- add a full-page mask
- add a right drawer above the mask
- do not change sidebar, header, filter area, or list layout

### 5. Delete is a confirmation state

For 删除页:

- keep the query-page base layout unchanged
- add a full-page mask
- add a centered confirmation layer or warning panel

### 6. Tables must be real

CRUD list pages must use real table structure.

At minimum:

- toolbar row
- header row
- body rows
- cell frames
- visible pagination

Never use a single text line to fake a table.

Visible pagination is mandatory for query/list pages.

### 7. Query page must occupy the full usable width

- do not leave a fake drawer lane on the query page
- filter card and table module should occupy the full usable right-side content width
- compute width from main content width minus page-body horizontal padding
- on `1920x1080`, keep content visually controlled so it does not feel over-stretched
- keep the shell stable: top nav, left navigation, page title, then the main work area
- if the reference `.pen` uses denser list-page composition, absorb its structural hierarchy without copying its non-Element visual tokens directly
- prefer the traditional admin order:
  top system bar -> left nav -> tabs or breadcrumb strip -> query toolbar -> action buttons -> table -> bottom-right pagination
- the result should look like a classic operations/admin system, not a stylized SaaS landing page or card-heavy dashboard
- query conditions should default to `text label + input component` pairs
- do not render bare search/select/date components without a visible preceding label unless the user explicitly asks for placeholder-only search

### 8. Business logic belongs in notes

If a page contains core business rules:

- add a page-external business note
- keep it secondary to the primary action flow
- place it outside the page canvas, typically to the right side
- use it to explain validation, permissions, status transitions, side effects, and save/delete impact
- do not move it into the page content area unless the user explicitly asks for that
- use Pencil `note` as the default annotation component
- keep the note outside the page frame, not inside the page layout
- for a single page, place the note in the right-side annotation lane
- when no better reference exists, follow the reference `.pen` note pattern:
  page title line + 核心逻辑 + 主操作 + 关键校验
- prefer compact note blocks around `250 x 240` unless the content genuinely needs more space
- if existing note content is trivial or placeholder text, ignore it instead of treating it as a rule source
- do not place page-level instruction text, rule summaries, helper paragraphs, or explanatory description cards inside the page canvas by default
- keep the page itself focused on layout, controls, data, statuses, and interaction states
- move all non-essential explanatory text to external `note` nodes
- only keep labels, placeholders, state text, and business data that are necessary to understand the UI structure

### 9. Validation is visual, not assumed

Always validate by screenshot:

- whole page
- filter card
- table card
- drawer state
- delete confirmation state

If a page still looks wrong, keep iterating.

### 10. Defaults that should not need repeating in prompts

Unless the user overrides them, assume:

- Element Plus style
- traditional admin-console shell
- compact controls and dense information layout
- reference `.pen` files contribute structure and copywriting patterns, not mandatory visual tokens
- query/list pages use real tables
- query/list pages have visible pagination
- query pages occupy the full usable width
- query/list modules keep controlled field widths and balanced spacing
- generation proceeds iteratively by section
- output should target the current active editor `.pen` file
- business logic is explained with a page-external note

## Workflow

1. Read the business request and classify the page type.
2. Choose the page shell and navigation.
3. If a reference `.pen` exists, extract reusable page-shell, note, table, drawer-content, and copy patterns from it.
4. Load the relevant Element Plus references.
5. Load the traditional admin-shell references and treat them as the default visual-shape constraint.
6. Reconcile the three layers:
   - structure and hierarchy from the reference `.pen`
   - visual language and component semantics from Element Plus
   - shell density, control scale, and classic admin appearance from the traditional-admin references
7. Build the query page first.
8. Verify:
   - filter structure
   - table structure
   - full-width layout
   - visible pagination
   - traditional admin visual density
9. Copy the query page into state pages.
10. Apply overlay states:
   - add/edit: full-page mask + right drawer
   - delete: full-page mask + confirm layer
11. Add business logic notes.
12. Screenshot each state page and verify consistency against the traditional-admin checklist.

## Required References

- `./references/element-plus-components-full.md`
- `./references/element-plus-prototype-mapping.md`
- `./references/element-plus-layout-rules.md`
- `./references/reference-pen-patterns.md`
- `./references/traditional-admin-visual-tokens.md`
- `./references/traditional-admin-shell-rules.md`
- `./references/traditional-admin-checklist.md`
- `./references/crud-state-page-rules.md`
- `./references/pencil-mcp-execution-rules.md`

## Quality Bar

The result is acceptable only if:

- query page is complete and independently reviewable
- add/edit states preserve the query-page base layout
- overlay mask covers the full page
- drawer is topmost
- table is structurally real
- pagination is visibly present
- no unnecessary right-side whitespace remains on the query page
- business logic notes explain key behavior
- reference `.pen` structure cues are absorbed where useful, without overriding the Element Plus visual baseline
- the page reads visually as a traditional backend management system without requiring extra prompt correction
- explanatory descriptions are not embedded inside the page canvas unless the user explicitly asks for them

## Prompt Shortcuts

In normal use, the user should only need one of these:

Minimal page:

```text
Use the product-prototype-design skill to generate a [业务页面名称] backend prototype.
```

CRUD page:

```text
Use the product-prototype-design skill to generate a [业务对象] management prototype with query/add/edit/delete states.
```

Strong-constraint version:

```text
Use the product-prototype-design skill to generate a [业务对象] backend CRUD prototype.
Default to a traditional admin-console shell.
Use Element Plus semantics.
Generate 查询页、新增页、修改页、删除页.
Use the query page as the base.
Add/edit must use full-page mask + right drawer.
Delete must use full-page mask + centered confirmation.
Use a real table and visible pagination.
Place business logic in page-external notes.
Canvas size 1920x1080.
```

These should already be implied and should not require repetition unless the user wants to override them:

- traditional backend-management shell
- Element Plus semantics
- real table
- visible pagination
- query page as base page
- add/edit right drawer overlays
- page-external business note
- `1920 x 1080` canvas
