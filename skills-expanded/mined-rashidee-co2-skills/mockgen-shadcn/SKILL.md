---
name: mockgen-shadcn
model: claude-opus-4-8
effort: high
description: >
  Generate React + shadcn/ui mockup screens from PRD.md files for UI/UX human designer review.
  Creates a Vite + React 19 + TypeScript + shadcn/ui mockup application with admin dashboard layout
  (collapsible sidebar navigation, header with logo/notifications/locale/user menu, footer
  with copyright/version) using React Router v7 for client-side navigation, organized by user role
  in a mockup/ folder. The app is BUILT (npm run build) and its dist/ output is served by the
  SINGLE shared Mockup Hub at <root>/mockup — a zero-dependency Node.js server with a landing
  page listing every application and role (unclickable when not ready) and a configurable port
  (PORT env / mockup.config.json). The Vite dev server remains available for design iteration only.
  Input: application name (mandatory), version (mandatory), module (optional).
  Output: mockup/ folder in the application's context folder
  containing MOCKUP.html index page, mockup-manifest.json, Vite + React project files, layout
  components, shadcn/ui components, role-specific page components, and the built dist/ folder;
  plus the shared hub at <root>/mockup if not already present.
  Trigger on keywords: "generate mockup shadcn", "generate shadcn mockup",
  "create shadcn mockup screens", "shadcn UI mockup", "React mockup from user stories",
  "mockup from PRD.md shadcn", "generate shadcn screens", "create shadcn UI screens".
  Accepts application name and version as input
  (e.g., `/mockgen-shadcn hub_middleware v1.0.3`).
  Optionally accepts a module name to limit generation to screens for that module only
  (e.g., `/mockgen-shadcn hub_middleware v1.0.3 module:Location Information`).
  When module is specified, only page components for that module are generated/updated;
  layout components, sidebars, config files, and other module pages are left untouched
  (the manifest is updated and the app is rebuilt).
  Automatically excludes strikethrough (deprecated/removed) items.
---

# Mockgen shadcn/ui

Generate a Vite + React 19 + TypeScript + shadcn/ui mockup application from PRD.md for UI/UX
designer review. Layout uses React components (header, sidebar, footer) composed in a shared
layout route. Pages are React Router routes rendered inside the layout. All navigation is
client-side via React Router `<Link>` and `useNavigate`.

The mockup is generated with `base`/`basename` set to `/{app_slug}/`, **built** with
`npm run build`, and served from its `dist/` folder by the **shared Mockup Hub** — a single
zero-dependency Node.js server at `<root>/mockup/` that serves ALL applications' mockups
(see [references/mockup-hub-template.md](references/mockup-hub-template.md)). The hub renders
a landing page listing every application and role (roles are unclickable until the app is
generated AND built) and listens on a configurable port (`PORT` env var →
`mockup.config.json` → 3000). The Vite dev server (`npm run dev`) remains available for
design iteration only.

## Stack

| Layer | Technology |
|-------|------------|
| Serving | Shared Mockup Hub — `<root>/mockup/server.js` serves the built `dist/` (SPA fallback) |
| Build tool | Vite 6 |
| UI framework | React 19 + TypeScript 5 |
| Component library | shadcn/ui (Radix UI + Tailwind CSS) |
| Routing / navigation | React Router v7 |
| Styling | Tailwind CSS v3 (PostCSS) |
| Icons | Lucide React |
| Dark mode | next-themes |

## Input

This skill uses standardized input resolution. Provide:

| Argument | Required | Example | Description |
|----------|----------|---------|-------------|
| `<application>` | Yes | `hub_middleware` | Application name to locate the context folder |
| `<version>` | Yes | `v1.0.3` | Version to scope processing (filter user stories <= this version) |
| `module:<name>` | No | `module:Location Information` | Limit generation to a single module |

### Application Folder Resolution

The application name is matched against root-level application folders:
1. Strip any leading `<number>_` prefix from folder names (e.g., `1_hub_middleware` â†’ `hub_middleware`)
2. Match case-insensitively against the provided application name
3. Accept snake_case, kebab-case, or title-case input (all match the same folder)
4. If no match found, list available applications and stop

### Auto-Resolved Paths

| File | Resolved Path |
|------|---------------|
| PRD.md | `<app_folder>/context/PRD.md` |
| Module Models | `<app_folder>/context/model/` |
| Output (mockup) | `<app_folder>/context/mockup/` |
| Mockup Hub (shared) | `<root>/mockup/` |

**App slug** (used as the URL base path): the application folder name with the leading
`<number>_` prefix stripped (e.g., `1_hub_middleware` → `hub_middleware`). Record it during
input resolution — it is baked into `vite.config.ts` (`base`), `main.tsx`
(`BrowserRouter basename`), and all MOCKUP.html links.

### Example Invocations

- `/mockgen-shadcn hub_middleware v1.0.3` (all modules, up to v1.0.3)
- `/mockgen-shadcn hub_middleware v1.0.3 module:Location Information` (one module, specific version)
- `/mockgen-shadcn "Hub Middleware" v1.0.3 module:Employer` (title-case app name)

### Version and Module Filtering

- Only include user stories, NFRs, constraints,
  and references from sections whose version tag is **less than or equal to** the target version
- If a module is provided (e.g., `module:Location Information`), only generate/update pages
  for that specific module. All other modules are skipped. Common pages (home, profile,
  account, notifications), layout components (header, footer, sidebars), and config files are
  NOT regenerated when a module filter is active â€” only the module's own page components
  are written (and MOCKUP.html is updated for only that module's cards).
- If no module is provided, process all modules (default behavior)

**Argument parsing**: The `module:` prefix is the canonical form. Also accept:
- `module:"Location Information"` (quoted, with space)
- `module:location_information` (snake_case â€” convert to title-case for matching)
- Natural language: `for Location Information module`, `only Location Information`

## Version Gate

Before starting any work, resolve the application folder first (see Input Resolution below), then check `CHANGELOG.md` in the application folder (`<app_folder>/CHANGELOG.md`):

1. If `<app_folder>/CHANGELOG.md` does not exist, skip this check (first-ever execution for this application).
2. If `<app_folder>/CHANGELOG.md` exists, scan all `## vX.Y.Z` headings and determine the **highest version** using semantic versioning comparison.
3. Compare the requested version against the highest version:
   - If requested version **>=** highest version: proceed normally.
   - If requested version **<** highest version: **STOP immediately**. Print: `"Version {requested} is lower than the current application version {highest} recorded in <app_folder>/CHANGELOG.md. Execution rejected."` Do NOT proceed with any work.

## Workflow

### Step 1: Parse PRD.md

Read the auto-resolved PRD.md file and extract:

1. **Application name**: Derive from the parent folder name containing PRD.md.
   Strip leading number and underscore prefix, then title-case.
   Example: `1_hub_middleware` -> "Hub Middleware"

2. **Application initials**: First letter of each word, uppercase.
   Example: `1_hub_middleware` -> "HM"

3. **Modules**: Each `## Module Name` section under a `# Module Category` heading.
   Record the module name and its description (the line after the heading).

4. **User stories per module**: Lines matching `- [USxx#####] As a {Role} user, I want to...`
   Extract: tag, role, action summary.

5. **Unique roles**: Collect all distinct roles from user stories.
   Example: "Hub Administrator", "Hub Operation Support"

6. **Target version** (from input argument): If a version was provided, record it for
   filtering in the next sub-step.

#### 1a: Version Filtering and Strikethrough Exclusion (MANDATORY)

PRD.md is a version-controlled document. Each section (User Story, Non Functional
Requirement, Constraint, Reference) has a version tag in square brackets, e.g., `[v1.0.1]`.
Items may also be marked with strikethrough (`~~`) to indicate they are deprecated/removed.

**Strikethrough exclusion** (always applied, regardless of version parameter):
- Any line wrapped in `~~strikethrough~~` markup MUST be excluded from processing
- This includes user stories, NFRs, constraints, and references
- Example: `~~[USHM00006] As a Hub Administrator user, I want to...~~` â†’ **SKIP**
- Partially strikethrough lines (where only part is struck) should still be excluded
  if the tag identifier is within the strikethrough

**Version filtering** (applied only when a target version is provided):
- Each section under a module has one or more version tags like `[v1.0.0]` or `[v1.0.1]`
- Items listed under a version tag belong to that version
- When a target version is specified (e.g., `v1.0.1`):
  - **Include** items from sections whose version tag is **<= target version**
  - **Exclude** items from sections whose version tag is **> target version**
- Version comparison uses semantic versioning: compare major, then minor, then patch
- When no target version is specified, include all items from all versions (but still
  exclude strikethrough items)

**Version tracking per section**: Record which version tag each item belongs to, as this
will be used for traceability in the generated pages.

Example parsing of a section with multiple versions:
```markdown
### User Story
[v1.0.0]
- ~~[USHM00006] As a Hub Administrator user, I want to manage...~~
- [USHM00009] As a Hub Administrator user, I want to map...
[v1.0.1]
- [USHM00012] As a Hub Administrator user, I want to manage the list...
```

With target version `v1.0.0`:
- USHM00006 â†’ EXCLUDED (strikethrough)
- USHM00009 â†’ INCLUDED (v1.0.0 <= v1.0.0, not strikethrough)
- USHM00012 â†’ EXCLUDED (v1.0.1 > v1.0.0)

With target version `v1.0.1` (or no version specified):
- USHM00006 â†’ EXCLUDED (strikethrough)
- USHM00009 â†’ INCLUDED
- USHM00012 â†’ INCLUDED

#### 1c: Module Filtering (applied only when a module argument is provided)

When a `module` argument is present, apply module filtering after version filtering:

1. **Match the specified module** against the list of parsed modules (case-insensitive, ignoring
   leading/trailing whitespace). Also accept snake_case input by converting it to title-case
   for comparison (e.g., `location_information` â†’ match "Location Information").
2. **Record the matched module name** for use in Step 3 and beyond.
3. If no module matches, stop and report the available module names to the user before proceeding.
4. **Module filter scope**: the filter only affects **page component generation** (Step 6e).
   All other steps complete normally (parsing, design system, planning) but output is restricted
   to the filtered module's pages.

**Module-filtered generation mode** differs from full generation in these ways:

| Aspect | Full Generation | Module-Filtered |
|--------|----------------|-----------------|
| Common pages (home, profile, account, notifications) | Generate for every role | **SKIP** â€” already exist |
| Layout components (header, footer, sidebar) | Generate | **SKIP** â€” already exist |
| Config files (package.json, vite.config.ts, etc.) | Generate | **SKIP** â€” already exist |
| shadcn/ui component files | Generate | **SKIP** â€” already exist |
| Route config (App.tsx) | Generate | **Update** â€” add routes for new module pages |
| Module page components (target module) | Generate | **Generate / overwrite** |
| Module page components (other modules) | Generate | **SKIP** â€” leave untouched |
| MOCKUP.html | Generate full file | **Update only the target module's cards** |
| Footer version string | Update | **Update** (version may have changed) |
| mockup-manifest.json | Generate | **Update** (version, generatedAt, screen counts) |
| Mockup Hub (`<root>/mockup/`) | Ensure (create/upgrade) | **Ensure** (create/upgrade) |
| `npm run build` (dist/ for hub serving) | Run | **Run** (rebuild required after page changes) |

**MOCKUP.html partial update** (module-filtered mode):
- Read the existing MOCKUP.html
- Locate the screen cards section for the target module (search by module name heading or
  existing card tags)
- Replace only those cards with freshly generated ones reflecting the new pages
- Update the total screen count per role (add net new pages)
- Update the version badge if it changed
- Update the "N new screens added in vX.Y.Z" banner text
- Leave all other role sections and cards unchanged

### Step 1b: Discover and Load Module Models

After parsing PRD.md, look for module models at the auto-resolved model path:
`<app_folder>/context/model/`

For each module extracted in Step 1:

1. Convert the module name to **kebab-case** to derive the model folder name:
   - Lowercase the module name and replace spaces with hyphens
   - Examples: "Location Information" â†’ `location-information`, "Industrial Classification" â†’ `industrial-classification`, "Employer" â†’ `employer`

2. Check for `{model_dir}/{kebab-module}/model.md`

3. If the file exists, parse it and extract the following sections:

   - **Section 2 â€“ Collection Catalog**: collection names and types (Root Collection, Audit Collection, etc.)
   - **Section 5 â€“ Field Detail per Collection**: for each collection â€” field name, type, required, nullable, constraints/notes
   - **Section 6 â€“ Embedded Document Definitions**: embedded type name and its sub-fields
   - **Section 7 â€“ Enum Definitions**: enum name and all allowed values with descriptions
   - **Section 9 â€“ Index Recommendations**: indexed fields (used to identify search/filter parameters)

4. Store this as the **module model** for the module, keyed by module name

**Field classification** (used during page generation in Step 6e):

| Category | Definition | Usage |
|----------|-----------|-------|
| System fields | `_id`, `_audit`, `_version`, `deleted`, `deletedAt`, `deletedBy` | Exclude from user-facing forms |
| Audit-only fields | Fields whose Source is `CONVENTION` and type is `Audit` | Show in detail views only |
| Required form fields | `Required: Yes` AND not a system field | Mandatory inputs in create/edit forms |
| Optional form fields | `Required: No` AND not a system field | Optional inputs in create/edit forms |
| Read-only after creation | Fields marked as unique identity keys (e.g., `companyRegistrationNumber`) | Show in edit forms as readonly |
| Search/filter fields | Fields referenced in Index Recommendations | Render as filter controls in list pages |
| Enum fields | Type matches an entry in Section 7 Enum Definitions | Render as `<Select>` dropdowns |
| Embedded object fields | Type is a custom embedded document type (not a primitive) | Render as grouped `<Card>` sections |
| Embedded array fields | Type ends in `[]` (e.g., `PersonInCharge[]`) | Render as repeatable row with Add/Remove |

**Fallback**: If no `model.md` exists for a module, infer fields from user story text (original behavior).

---

### Step 2: Load Design System

Load the design system using a two-tier resolution strategy:

#### 2a: PRD.md Design System Reference (Primary Source)

Check if PRD.md contains a `# Design System` section. If it does:
1. Extract the referenced file path (e.g., from `[DESIGN_SYSTEM.md](reference/DESIGN_SYSTEM.md)`)
2. Resolve the path relative to PRD.md's location
3. If the referenced file exists, read it and extract:
   - Color palettes (primary, secondary, accent, neutral â€” hex values)
   - Typography (font families, font sizes, weight scale)
   - Spacing scale (if overriding Tailwind defaults)
   - Component patterns (button styles, card styles, form input styles, table styles, badge/chip styles, modal patterns)
   - Layout grid rules
4. Apply extracted tokens to the Tailwind config (`tailwind.config.js`) custom colors/fonts,
   shadcn/ui CSS variables in `src/index.css`, and all generated components

#### 2b: Context Design Folder (Fallback)

If PRD.md does not have a `# Design System` section, or the referenced file does not exist, fall back to the application's `<app_folder>/context/design/` folder. This folder contains pre-defined design tokens and Tailwind component guidelines maintained externally by the UI/UX team.

Read all files in `{app_name}/context/design/` (where `{app_name}` is the resolved application folder name from Step 1). Apply the design tokens and guidelines found there to all generated mockup pages.

**Expected files** (any or all may be present):
- `design-system.md` â€” Colors, typography, spacing, and visual style definitions
- `components.md` â€” Reusable component patterns and Tailwind class conventions
- `guidelines.md` â€” Layout rules, accessibility standards, and stack-specific guidelines

#### 2c: Default Fallback

If neither the PRD reference nor the `{app_name}/context/design/` folder provides design tokens, use the default shadcn/ui "New York" style: zinc/neutral color palette, Inter/Geist font stack, and default shadcn/ui component styling with CSS variables.

#### 2d: Process Flow Status States

If PRD.md contains a `# High Level Process Flow` section, scan it for entity status lifecycle descriptions (e.g., "Received â†’ Validated â†’ Enriched â†’ Active"). For each status lifecycle found:
- Ensure list pages for the corresponding module include a status column with colored `<Badge>` variants for each state
- Use design system color tokens for badge variants (e.g., `default` for active/completed, `secondary` for pending, `destructive` for failed/rejected)

### Step 3: Plan Screen Files

For each role, determine ALL pages to generate. **Every clickable link, tab, or action
in any generated page MUST have a corresponding page component. No link may be a dead end.**

**Module filter applied here**: If a module argument was provided (Step 1c), plan only the
pages for that module across all roles. Skip common pages (home, profile, account,
notifications) and skip all other modules entirely. The screen plan table should list only
the filtered module's pages.

#### 3a: Core Pages (React components)

1. **home.tsx**: Default home/dashboard page with welcome message and summary widgets
2. **profile.tsx**: User profile page (linked from header user dropdown)
3. **account.tsx**: Account settings page (linked from header user dropdown)
4. **notifications.tsx**: Notifications page (linked from header notification bell)
5. **One page per module that has user stories for this role**

#### 3b: Sub-Pages (Detail / Edit / Create)

For each module page, analyze the user stories and identify sub-pages needed:

| User Story Pattern | Sub-Page Required |
|-------------------|-------------------|
| "view details of X" | `{module}-detail.tsx` - Detail view for a single record |
| "add/create/register X" | `{module}-create.tsx` - Create/add form |
| "edit/update/modify X" | `{module}-edit.tsx` - Edit form (pre-filled) |
| "view history/audit of X" | `{module}-history.tsx` - History/audit log view |
| "view associated X of Y" | `{module}-{sub}-list.tsx` - Associated records list |

#### 3f: Report Layout Pages (conditional â€” if PRD.md contains report-related content)

Scan PRD.md for report-related content:
- NFRs mentioning "report", "Report interface", "generate report", "report generation"
- User stories describing generating/downloading PDF, Excel, or CSV reports
- A "Report" module or report-related NFRs defining specific report types

**If report requirements are found**, generate HTML report layout mockups for each
identified report. These layouts serve as draft previews for human designers/stakeholders
to verify the report structure before the AI coding agent implements the actual report
generation code.

For each identified report, create a standalone HTML file in a `public/reports/` subfolder:

| Report Source | File Generated |
|--------------|----------------|
| NFR describes "Staff Allocation Summary report" | `public/reports/staff_allocation_summary.html` |
| User story: "generate Job Demand report by country" | `public/reports/job_demand_by_country.html` |
| Report module NFR: "Monthly Activity Report" | `public/reports/monthly_activity_report.html` |

**Report layout file conventions:**
- Each report layout is a **standalone self-contained HTML document** (not a React component)
  with its own `<html>`, `<head>`, `<body>` tags and Tailwind CDN `<script>` in the head
- Layout simulates a **print-ready A4 page** with appropriate margins and sizing:
  ```html
  <body class="bg-gray-100">
    <div class="mx-auto bg-white shadow" style="width: 210mm; min-height: 297mm; padding: 15mm;">
      <!-- Report content -->
    </div>
  </body>
  ```
- **Report header**: Report title (centered, bold), generation date, filter parameters used
- **Report body**: Data table or summary layout using actual fields from the module model
  (if `model/{module}/model.md` exists, use its field definitions for column headers)
- **Report footer**: Page indicator text ("Page 1 of 1"), generation timestamp
- Use **sample data rows** (5-10 rows) with realistic placeholder values matching model constraints
- Apply the design system colors from Step 2 for header background, borders, and accents
- For landscape reports (wide tables with many columns), use `style="width: 297mm; min-height: 210mm;"`

**Report parameter section**: Above the report data, include a gray-shaded "Parameters" box
showing the filter criteria used to generate the report (e.g., Date Range: 2025-01-01 to
2025-12-31, Department: All, Status: Active).

**Add to MOCKUP.html**: Include a "Reports" section at the bottom of each role's screen cards
(after all module cards) listing the report layout links. Report links open in new tabs
pointing to the hub's static route `/{app_slug}/reports/{report_file}.html`. Also list the
report file names in the manifest's `reports` array.

**Add to sidebar**: If reports are present, add a "Reports" navigation group in each role's
sidebar with links opening report layouts in new tabs.

#### 3c: Tabbed Pages

If a module page contains tabs (e.g., a detail page with Overview, Documents, History tabs),
use shadcn/ui `<Tabs>` component **within the same page component**. Only create separate
page component files for tabs if the tab content is substantial (more than ~100 lines).
Use the naming convention for separate files: `{module}-tab-{tab_name}.tsx`

Example: `employer-tab-overview.tsx`, `employer-tab-documents.tsx`, `employer-tab-history.tsx`

#### 3d: Page File Naming Convention

Convert names to kebab-case for file names, PascalCase for component names.
Example: "Location Information" â†’ file: `location-information.tsx`, component: `LocationInformation`

#### 3e: Build Screen Plan

Build a **complete** screen plan. Every entry must map to a generated file:

| Role | Folder Name | Page File | Source | Description |
|------|-------------|-----------|--------|-------------|
| Hub Administrator | hub-administrator | home.tsx | Common | Dashboard home |
| Hub Administrator | hub-administrator | profile.tsx | Common | User profile |
| Hub Administrator | hub-administrator | account.tsx | Common | Account settings |
| Hub Administrator | hub-administrator | notifications.tsx | Common | Notifications list |
| Hub Administrator | hub-administrator | location-information.tsx | Module | USHM00006, USHM00009 |
| Hub Administrator | hub-administrator | location-information-detail.tsx | Sub-page | View location details |
| Hub Administrator | hub-administrator | location-information-create.tsx | Sub-page | Add new location |
| Hub Operation Support | hub-operation-support | home.tsx | Common | Dashboard home |
| Hub Operation Support | hub-operation-support | profile.tsx | Common | User profile |
| Hub Operation Support | hub-operation-support | account.tsx | Common | Account settings |
| Hub Operation Support | hub-operation-support | notifications.tsx | Common | Notifications list |
| Hub Operation Support | hub-operation-support | employer.tsx | Module | USHM00021-USHM00033 |
| Hub Operation Support | hub-operation-support | employer-detail.tsx | Sub-page | View employer details |
| Hub Operation Support | hub-operation-support | employer-create.tsx | Sub-page | Register new employer |

### Step 4: Create Output Folder Structure

**Module filter**: When a module argument is active, skip this step entirely â€” the folder
structure already exists from a previous full generation. Only page components for the target
module will be written in Step 6e.

Create the mockup folder at the auto-resolved mockup output path (full generation only):

```
<app_folder>/context/
  mockup/
    .gitignore
    package.json
    vite.config.ts
    tsconfig.json
    tsconfig.app.json
    tsconfig.node.json
    tailwind.config.js
    postcss.config.js
    components.json                      # shadcn/ui configuration
    index.html                           # Vite entry HTML
    MOCKUP.html                          # Per-app screen index (served by hub at /{app_slug})
    mockup-manifest.json                 # Hub discovery manifest (app, stack, roles, version)
    dist/                                # Built output served by the hub (npm run build; gitignored)
    public/
      reports/                           # Report layout files (if applicable)
    src/
      main.tsx                           # React entry point
      App.tsx                            # Router configuration
      index.css                          # Tailwind directives + shadcn/ui CSS variables
      lib/
        utils.ts                         # cn() utility
      components/
        ui/                              # shadcn/ui components
          button.tsx
          card.tsx
          table.tsx
          badge.tsx
          input.tsx
          label.tsx
          select.tsx
          dialog.tsx
          dropdown-menu.tsx
          avatar.tsx
          separator.tsx
          tabs.tsx
          switch.tsx
          tooltip.tsx
          breadcrumb.tsx
          pagination.tsx
          sheet.tsx
        layout/
          app-layout.tsx                 # Shared layout with sidebar + header + footer
          app-header.tsx                 # Top header component
          app-sidebar.tsx                # Sidebar nav component (role-aware)
          app-footer.tsx                 # Footer component
          sidebar-config.ts              # Sidebar menu items per role
      pages/
        {role-kebab-case}/
          home.tsx
          profile.tsx
          account.tsx
          notifications.tsx
          {module-kebab-case}.tsx
          {module-kebab-case}-detail.tsx
          {module-kebab-case}-create.tsx
          {module-kebab-case}-edit.tsx
          ...
```

### Step 4b: Generate Project Config Files

**Module filter**: When a module argument is active, skip this step entirely.

Generate all config and entry files using the templates from
[references/admin-layout-template.md](references/admin-layout-template.md).

#### .gitignore

```
node_modules/
dist/
.DS_Store
*.log
*.local
```

Key project setup:
- `package.json` â€” Vite + React 19 + TypeScript + Tailwind CSS + shadcn/ui dependencies
- `vite.config.ts` â€” Vite config with React plugin, path aliases, and
  `base: "/{app_slug}/"` (REQUIRED so the built app is servable by the hub at `/{app_slug}`)
- `tsconfig.json` / `tsconfig.app.json` / `tsconfig.node.json` â€” TypeScript configs with path aliases
- `tailwind.config.js` â€” Tailwind config with shadcn/ui integration and design system tokens
- `postcss.config.js` â€” PostCSS with Tailwind and autoprefixer
- `components.json` â€” shadcn/ui configuration (New York style, zinc base)
- `index.html` â€” Vite entry HTML with Google Fonts
- `src/main.tsx` â€” React root render with `<BrowserRouter basename="/{app_slug}">`
  (REQUIRED to match the Vite `base`)
- `src/App.tsx` â€” React Router configuration with all role/page routes
- `src/index.css` â€” Tailwind directives + shadcn/ui CSS variables (light and dark)
- `src/lib/utils.ts` â€” `cn()` utility (clsx + tailwind-merge)

### Step 4c: Generate shadcn/ui Component Files

**Module filter**: When a module argument is active, skip this step entirely.

Generate the shadcn/ui component files directly into `src/components/ui/`. These follow the
standard shadcn/ui "New York" style patterns. The components are owned by the project â€” they
are NOT imported from npm.

**Required components** (generate all of these):

| Component | File | Primary Usage |
|-----------|------|--------------|
| Button | `button.tsx` | Actions, navigation, form submission |
| Card | `card.tsx` | Content containers, stat cards, detail panels |
| Table | `table.tsx` | Data lists, records, audit logs |
| Badge | `badge.tsx` | Status indicators, tags, enum values |
| Input | `input.tsx` | Text fields, search, filters |
| Label | `label.tsx` | Form field labels |
| Select | `select.tsx` | Dropdowns, enum selectors, page size |
| Dialog | `dialog.tsx` | Delete confirmations, modals |
| DropdownMenu | `dropdown-menu.tsx` | Header user menu, notification dropdown |
| Avatar | `avatar.tsx` | User avatars in header and profile |
| Separator | `separator.tsx` | Visual dividers |
| Tabs | `tabs.tsx` | Detail page sections, notification filters |
| Switch | `switch.tsx` | Boolean toggles, notification preferences |
| Tooltip | `tooltip.tsx` | Field hints, readonly explanations |
| Breadcrumb | `breadcrumb.tsx` | Page navigation trail |
| Pagination | `pagination.tsx` | Table/list pagination |
| Sheet | `sheet.tsx` | Mobile sidebar overlay |

Each component follows the standard shadcn/ui implementation pattern:
- Uses `@radix-ui/*` primitives for accessibility
- Styled with Tailwind CSS utility classes
- Supports `className` prop via `cn()` utility
- Uses `cva` (class-variance-authority) for variants where applicable
- Forwards refs properly

### Step 4d: Write mockup-manifest.json and Ensure the Mockup Hub

**Always runs** (full AND module-filtered generation; in module-filtered mode UPDATE the
existing manifest — version, generatedAt, per-role screen counts).

1. Write `<app_folder>/context/mockup/mockup-manifest.json` following the schema in
   [references/mockup-hub-template.md](references/mockup-hub-template.md):

   ```json
   {
     "app": "{app_slug}",
     "appName": "{App Name}",
     "description": "{short description from PRD.md}",
     "stack": "shadcn",
     "version": "{target version}",
     "generatedAt": "{YYYY-MM-DD}",
     "roles": [
       { "name": "{Role Name}", "slug": "{role-kebab-case}", "screens": {count} }
     ],
     "reports": ["{report_file}.html"]
   }
   ```

   (`reports` only when report layouts were generated.) The hub reads this manifest to
   route the app and render its landing-page card; without it the app shows as "Not
   generated yet" and its roles are unclickable.

2. Ensure the shared hub exists at `<root>/mockup/` per the Ensure-Hub rules in
   [references/mockup-hub-template.md](references/mockup-hub-template.md): create
   `server.js`, `package.json`, `mockup.config.json`, and `.gitignore` if missing;
   upgrade `server.js`/`package.json` only when the existing `HUB_VERSION` is lower;
   never overwrite an existing `mockup.config.json` or `.gitignore`. All hub artifacts
   (config, logs, any `node_modules/`) live inside `<root>/mockup/` and are gitignored
   there.

### Step 5: Generate MOCKUP.html Index

**Module filter**: When a module argument is active, do NOT regenerate the full MOCKUP.html.
Instead, apply a **partial update** as described in Step 1c: update only the target module's
screen cards, the version badge, and the per-role screen count. Leave all other content
unchanged.

Create the index page using the template in [references/mockup-index-template.md](references/mockup-index-template.md).

MOCKUP.html is this app's screen index, served by the hub at `/{app_slug}`. It shows:
- Hub startup banner with instructions (`cd <root>/mockup && npm start` — no install
  needed; port configurable via `PORT` env var or `mockup.config.json`) and a reminder
  that the app must be built (`npm run build`) before screens open
- Application name and description
- **Target version** used for generation
- Number of excluded items for transparency
- For each role: role name, list of screen cards with links
- **ALL screen links use `target="_blank" rel="noopener noreferrer"`** with
  **root-relative** URLs `/{app_slug}/{role}/{page}` (never hardcode
  `http://localhost:<port>` — the hub port is user-configurable) so they open in new
  tabs via the running hub (SPA fallback serves `dist/index.html`, React Router resolves
  the route)
- A "Open Role Dashboard" quick-launch link per role section

### Step 6: Generate Layout Components and Page Components

Use templates from [references/admin-layout-template.md](references/admin-layout-template.md).

**Apply the design system** from Step 2 (colors, typography, spacing) to all components via
the CSS variables in `src/index.css` and the Tailwind config.

**Module filter**: When a module argument is active, skip steps 6aâ€“6d (layout components).
Proceed directly to **6e** for the target module's page components only. Also update the
footer version string in `app-footer.tsx` if the version changed.

#### 6a: Generate src/components/layout/app-layout.tsx

Shared layout component using React Router `<Outlet>`. Contains:
- `<AppHeader>` at the top (fixed)
- `<AppSidebar>` on the left (fixed, collapsible)
- `<Outlet>` for page content (scrollable)
- `<AppFooter>` at the bottom
- ThemeProvider wrapping for dark mode support
- Sidebar state management (expanded/collapsed)

#### 6b: Generate src/components/layout/app-header.tsx

Header component containing:
- Logo + App Name (left) â€” `<Link>` to home
- Notification bell with shadcn/ui `<DropdownMenu>` and `<Badge>` count
- Globe/locale selector with shadcn/ui `<DropdownMenu>`
- Dark mode toggle button using next-themes `useTheme()`
- User `<Avatar>` with `<DropdownMenu>` (Profile, Account, Logout)
- All Profile/Account/Notifications links use React Router `<Link>` / `useNavigate()`
- Lucide React icons throughout (Bell, Globe, Moon, Sun, User, LogOut, Settings)

#### 6c: Generate src/components/layout/app-footer.tsx

Simple footer with copyright year and version string using `<Separator>` divider.

#### 6d: Generate src/components/layout/sidebar-config.ts and app-sidebar.tsx

**sidebar-config.ts**: Export a configuration object mapping each role to its sidebar menu items:
```typescript
export type SidebarItem = {
  title: string;
  path: string;
  icon: string; // Lucide icon name
};

export type SidebarConfig = {
  [role: string]: {
    label: string;
    items: SidebarItem[];
    reports?: { title: string; href: string }[];
  };
};
```

**app-sidebar.tsx**: Sidebar component that:
- Reads the current role from React Router `useParams()`
- Renders menu items from sidebar-config.ts for that role
- Highlights the active menu item using `useLocation().pathname`
- Uses React Router `<Link>` for navigation (not HTMX)
- Uses Lucide React icons dynamically based on config
- Supports collapsed state (icons only) via context/state
- Has a collapsible toggle button

#### 6e: Generate page components (src/pages/{role-kebab-case}/{page}.tsx)

Each page component is a **standard React functional component** that returns JSX.
Pages use shadcn/ui components for all UI elements.

**All navigation within page components uses React Router** `<Link>` or `useNavigate()`.

**Breadcrumbs**: Use shadcn/ui `<Breadcrumb>` component. Home link is a `<Link>`,
module link is a `<Link>`, current page is `<BreadcrumbPage>` (non-interactive).

#### Admin Layout: Screen Content Generation

For each module page, analyze the user stories and generate appropriate UI mockup elements:

| User Story Pattern | UI Element |
|-------------------|------------|
| "search for X based on parameters" | Filter `<Card>` with `<Input>`/`<Select>` + `<Table>` results |
| "view details of X" | Detail `<Card>` with labeled fields in grid layout |
| "manage X" / "configure X" | `<Table>` with Add/Edit/Delete action `<Button>` components |
| "view history/changes" | `<Table>` with timestamps and `<Badge>` change types |
| "map X to Y" | Two-panel mapping interface or matrix `<Table>` |
| "activate/deactivate X" | `<Switch>` toggles in table rows or config panel |
| "view associated X" | Related records `<Table>` or linked `<Card>` sections |

#### Model-Driven Field Usage (MANDATORY when model file exists)

When a module model was loaded in Step 1b, use its actual field definitions â€” not generic placeholders â€” to populate every page. Generic field names like "Field 1" or "Description" are not acceptable when a model is available.

**Field type â†’ shadcn/ui component mapping:**

| Model Type | Form Component | Notes |
|------------|---------------|-------|
| `String` | `<Input type="text">` with `<Label>` | Use `maxLength` if constraints specify length |
| `Number` | `<Input type="number">` with `<Label>` | |
| `Boolean` | `<Switch>` with `<Label>` | |
| `ISODate` | `<Input type="date">` or `<Input type="datetime-local">` | |
| `ObjectId` (reference) | `<Input readOnly>` or lookup widget with `<Tooltip>` | Display as read-only ID reference |
| Enum (Section 7 match) | `<Select>` with all enum values as `<SelectItem>` | Show enum value descriptions as item text |
| Embedded Object | `<Card>` section grouping sub-fields | Title the card with embedded type name |
| Embedded Array (`[]`) | Repeatable `<Card>` section with `<Button>` "+ Add" / "Remove" | Show one pre-filled example row |

**List / Search pages** (`{module}.tsx`):
- **Filter section**: `<Card>` with filter inputs only for fields in Index Recommendations (Section 9). Use the correct component per the mapping above. Enum-indexed fields use `<Select>`. Date-indexed fields use date range pickers.
- **Results table**: shadcn/ui `<Table>` with 5â€“7 most identifying non-system fields as columns. For embedded objects, show as a single column (e.g., "Company Name"). Null/optional fields shown with a dash (`â€”`).
- **Table row actions**: View â†’ `<Link>` to `{module}-detail`, Edit â†’ `<Link>` to `{module}-edit`, Delete â†’ shadcn/ui `<Dialog>` confirm
- **Pagination** (MANDATORY): Every results table MUST include shadcn/ui `<Pagination>` directly below the table. Requirements:
  - Default page size: **10 items per page**
  - Show "Showing Xâ€“Y of Z results" summary text on the left
  - Show page size `<Select>` with options 10, 25, 50 on the right (default 10)
  - Show Previous / Next and page number buttons using `<Pagination>` component
  - Page state managed via React `useState` (`currentPage`, `pageSize`, `totalItems`)
  - Previous/Next buttons are disabled when at first/last page
  - Use sample data: populate exactly 10 visible rows in the table (matching the default page size)

**Detail pages** (`{module}-detail.tsx`):
- Show ALL non-system fields, grouped logically:
  - Basic fields: flat primitive fields in a 2-column grid `<Card>`
  - Embedded objects (e.g., `address`, `contact`): each in its own labeled sub-`<Card>`
  - Embedded arrays (e.g., `personsInCharge`): rendered as a sub-`<Table>` with a row per item
  - Enum fields: display value wrapped in a `<Badge>` with appropriate variant
  - ISODate fields: formatted as `DD MMM YYYY HH:mm` in sample data
  - Boolean fields: show as a `<Badge>` ("Active" variant=default / "Inactive" variant=secondary)
- Include Edit `<Button>`, Delete `<Dialog>` confirm, and Back to List `<Button>` actions

**Create pages** (`{module}-create.tsx`):
- Include ALL `Required: Yes` non-system fields as mandatory inputs (mark with `*` via `<Label>`)
- Include `Required: No` fields as optional inputs where they make sense for initial creation
- Group embedded objects as `<Card>` sections with a title
- For embedded arrays: show one empty repeatable row with a `<Button>` "+ Add"
- Submit `<Button>` and Cancel `<Button>` (Cancel navigates back to `{module}` list via `useNavigate()`)

**Edit pages** (`{module}-edit.tsx`):
- Same structure as create page but with sample data pre-filled in all inputs
- Fields that serve as unique identity keys (e.g., `companyRegistrationNumber`) must be rendered as `<Input readOnly>` with a `<Tooltip>` explaining they cannot be changed
- Save `<Button>` and Cancel `<Button>`

**History / Audit pages** (`{module}-history.tsx`):
- Use fields from the **audit/history collection** (the non-root collection in the Collection Catalog):
  - `changeType` â†’ `<Badge>` using enum values from Section 7 with variant mapping
  - `fieldChanged` â†’ `<code>` styled text
  - `previousValue` / `newValue` â†’ inline diff or truncated display
  - `changedAt` â†’ formatted timestamp
  - `changedBy` â†’ plain text (e.g., "SYSTEM" or username)
- Render as a `<Table>`, newest first
- **Pagination** (MANDATORY): Include `<Pagination>` below the history table. Default 10 items per page.

**Sample data alignment**: Placeholder values in pages must be consistent with field constraints:
- `countryCode` â†’ use actual allowed values (e.g., "MYS", "BHR", "MDV") per constraints if present
- Enum fields â†’ use one of the defined enum values (not arbitrary strings)
- `companyRegistrationNumber` â†’ e.g., "201901012345 (1234567-X)"
- `ISODate` fields â†’ use realistic ISO dates (e.g., "2025-08-15T10:30:00Z")

---

#### Link Integrity Rules (CRITICAL)

**Every clickable element MUST navigate to a real route. No dead-end links allowed.**

1. **Table row actions** (View, Edit, Delete):
   - "View" / "Details" â†’ React Router `<Link to="/{role}/{module}-detail">` 
   - "Edit" â†’ React Router `<Link to="/{role}/{module}-edit">`
   - "Delete" â†’ shadcn/ui `<Dialog>` confirm (no navigation, inline confirm)
   - "Add New" / "Create" â†’ React Router `<Link to="/{role}/{module}-create">`

2. **Tabs within a page**:
   - Use shadcn/ui `<Tabs>` component with `<TabsContent>` for inline tabs
   - If tabs are separate page files, each tab header is a `<Link>` to the tab route

3. **Header links**:
   - Notification bell icon â†’ React Router `<Link>` to `notifications`
   - Notification dropdown "View all notifications" â†’ React Router `<Link>` to `notifications`
   - Locale dropdown options â†’ no-op handler (static language switcher mockup)
   - Dark mode toggle â†’ `useTheme().setTheme()` (no navigation)
   - Profile dropdown â†’ React Router `<Link>` to `profile`
   - Account dropdown â†’ React Router `<Link>` to `account`
   - Logout â†’ plain `<a href="/">` (escapes the SPA to the hub landing page â€” a React
     Router `<Link to="/">` would only reach the app's own root because of the basename)

4. **Sidebar links**: React Router `<Link>` to correct module routes

5. **Breadcrumb links**: shadcn/ui `<Breadcrumb>`
   - Home â†’ `<Link to="/{role}/home">`
   - Module â†’ `<Link to="/{role}/{module}">`
   - Detail / current â†’ `<BreadcrumbPage>` (non-interactive)

6. **Pagination links**: shadcn/ui `<Pagination>` with React `useState` for page state â€” navigation is in-component state, not route-based

7. **Back / Cancel buttons**: React Router `useNavigate()` or `<Link>` to the parent page

8. **Images** (inline previews, thumbnails, etc.):
   - Must open the full image in a **new tab** via `<a href="..." target="_blank" rel="noopener noreferrer">`
   - Use placeholder image URLs like `https://placehold.co/800x600`

9. **PDFs and documents** (download/view links):
   - Must open in a **new tab** via `<a href="..." target="_blank" rel="noopener noreferrer">`
   - Never render PDFs inline within the mockup

**Content guidelines:**
- Use placeholder/sample data that reflects the module context
- Include appropriate form fields based on NFRs and constraints
- Show the user story tags with their version as JSX comments for traceability
  (e.g., `{/* USHM00012 [v1.0.1] */}`)
- All interactive elements use React state and shadcn/ui components
- Use Tailwind utility classes for layout and custom styling
- Use Lucide React icons (`import { IconName } from "lucide-react"`)

#### Common Pages Content

**home.tsx**: Dashboard home page showing:
- Welcome message with user role
- Summary stat `<Card>` grid (one per module: total count, recent activity)
- Recent activity `<Table>` with recent actions across modules

**profile.tsx**: User profile page showing:
- User `<Avatar>`, full name, email, role `<Badge>`
- Personal information `<Card>` (read-only display): Name, Email, Phone, Department
- "Edit Profile" `<Button>` (navigates to self since it's a mockup)

**account.tsx**: Account settings page showing:
- Change Password `<Card>` (current password, new password, confirm password `<Input>` fields)
- Notification Preferences `<Card>` (`<Switch>` toggles for email/SMS)
- Language/Locale `<Select>`
- Session Management `<Card>` (active sessions `<Table>`)

**notifications.tsx**: Notifications list page showing:
- shadcn/ui `<Tabs>`: All, Unread, Read
- List of notification `<Card>` items with: Lucide icon, title, message preview, timestamp, read/unread dot
- Mark all as read `<Button>`
- **Pagination** (MANDATORY): `<Pagination>` below the notification list, default 10 items per page.

#### Sub-Page Content

**{module}-detail.tsx**: Record detail page showing:
- Page title with record identifier
- Back `<Button>` (React Router `<Link>` to `{module}`)
- Detail `<Card>` panels with all relevant fields from user stories
- Action buttons: Edit `<Button>` (`<Link>` to `{module}-edit`), Delete `<Dialog>`, Back to List
- Related data sections if applicable
- If the entity has sub-entities, show them in shadcn/ui `<Tabs>` or sectioned `<Card>` groups

**{module}-create.tsx**: Create/add form page showing:
- Page title: "Add New {Entity}"
- `<Breadcrumb>`: Home > {Module} > Add New
- Form `<Card>` with all required fields derived from user stories
- Submit and Cancel `<Button>` (Cancel: `<Link>` to `{module}`)

**{module}-edit.tsx**: Edit form page showing:
- Page title: "Edit {Entity}"
- `<Breadcrumb>`: Home > {Module} > Edit
- Pre-filled form `<Card>` with sample data
- Save and Cancel `<Button>` (Cancel: `<Link>` to `{module}-detail` or `{module}`)

### Step 6f: Build for Hub Serving (MANDATORY)

The hub serves this app from its built `dist/` folder — an unbuilt app appears on the hub
landing page as "Build required" with unclickable roles.

1. Run in `<app_folder>/context/mockup/`:
   ```bash
   npm install
   npm run build
   ```
2. Verify `dist/index.html` exists and its asset URLs start with `/{app_slug}/`.
3. If the build fails or cannot run (e.g., no network for `npm install`), report it in the
   output summary with the exact command the user must run — the hub landing page will show
   the app as "Build required" until then.
4. **Module-filtered runs**: rebuilding is still REQUIRED — the previous `dist/` does not
   contain the new/updated page components.

The Vite dev server (`npm run dev`) remains available for design iteration; it serves the
app at `http://localhost:5173/{app_slug}/` because of the `base` setting.

### Step 7: Output Summary

After generation, print a summary:

```
Mockup Generation Complete
===========================
Application: {App Name} ({Initials})
Target Version: {version or "latest (all versions)"}
Module Filter: {module name or "all modules"}
Output: {path}/mockup/

Filtering Summary:
- User stories included: {count}
- User stories excluded (strikethrough): {count}
- User stories excluded (version filter): {count}
- User stories excluded (module filter): {count}
- NFRs/Constraints included: {count}
- NFRs/Constraints excluded: {count}

| Role                  | Pages | Page Folder                          |
|-----------------------|-------|--------------------------------------|
| Hub Administrator     | 8     | src/pages/hub-administrator/         |
| Hub Operation Support | 6     | src/pages/hub-operation-support/     |

Files generated:
- Config: .gitignore, package.json, vite.config.ts, tsconfig.json, tailwind.config.js, etc.
- shadcn/ui: {N} component files in src/components/ui/
- Layout: app-layout.tsx, app-header.tsx, app-sidebar.tsx, app-footer.tsx, sidebar-config.ts
- Pages: {N} page component files
- MOCKUP.html (per-app screen index) + mockup-manifest.json
- Build: dist/ {built successfully | BUILD REQUIRED — run npm install && npm run build}
- Mockup Hub: {created at <root>/mockup | upgraded to v{N} | already present}

Total: {N} files

Quick Start
===========
1. cd <root>/mockup
2. npm start          (zero dependencies — no npm install required)
3. Open http://localhost:3000 in your browser
   - Landing page lists ALL applications and roles
   - This app's screen index: http://localhost:3000/{app_slug}
4. Change port: PORT=4000 npm start, or edit <root>/mockup/mockup.config.json

Design iteration (optional): cd {mockup folder path} && npm run dev
→ http://localhost:5173/{app_slug}/
```

### Step 7b: Route Integrity Validation (MANDATORY)

Before finalizing output, perform a route integrity check across ALL generated files:

1. **Scan every generated page and layout component** for all `<Link to="...">`, `useNavigate("...")`,
   and `<a href="...">` references
2. **Build a route registry**: map every route reference to the page component that handles it
3. **Verify each React Router route** has a corresponding page component:
   - `<Link to="/{role}/{page}">` â†’ verify `src/pages/{role}/{page}.tsx` exists
   - plain `<a href="/">` â†’ acceptable for logout (hub landing); a `<Link to="/">` is NOT
     equivalent (basename keeps it inside the app)
   - `target="_blank"` links â†’ acceptable for images, PDFs, external resources
   - `href="#"` or dead-end `<Link>` â†’ **NOT ALLOWED** â€” must be fixed
4. **Verify App.tsx routes**: every page component must have a corresponding route definition
5. **For any missing page file**, either:
   - Generate the missing page component, OR
   - Update the link to point to an existing route
6. **Report any fixes** made during validation in the output summary

If any dead-end link is found in the final output, the generation is **incomplete**.

## Changelog Append

After all mockup files are successfully generated, append an entry to `CHANGELOG.md` in the application folder (`<app_folder>/CHANGELOG.md`):

1. Read `<app_folder>/CHANGELOG.md`. If it does not exist, create it with:
   ```markdown
   # Changelog

   - This file tracks all skill executions by version for this application.
   - The highest version recorded here is the current application version.
   - Skills MUST NOT execute for a version lower than the highest version in this file.

   ---
   ```
2. Search for a `## {version}` heading matching the current version.
3. If the section **exists**: append a new row to its table.
4. If the section **does not exist**: insert a new section after the `---` below the context header and before any existing `## vX.Y.Z` section (newest-first ordering), with a new table header and the first row.
5. Row format: `| {YYYY-MM-DD} | {application_name} | mockgen-shadcn | {module or "All"} | Generated React + shadcn/ui mockup screens |`
6. **Never modify or delete existing rows.**

## Important Rules

- **Module filter is additive, not destructive**: When `module:` is specified, only the named
  module's page components are written/overwritten. All other files (layout components, other module
  pages, config files) remain untouched. If the target module does not exist in PRD.md,
  stop and report available module names before doing any file writes.
- **Version + module are independent axes**: Both may be combined freely. `module:Employer
  v1.0.2` means "generate Employer module pages as they exist at v1.0.2". Version filtering
  and module filtering each apply independently; a story must satisfy BOTH to be included.
- **Base path is mandatory**: `vite.config.ts` MUST set `base: "/{app_slug}/"` and
  `main.tsx` MUST set `<BrowserRouter basename="/{app_slug}">` — without them the built
  app cannot be served by the hub at `/{app_slug}`.
- **No per-app server for viewing**: reviewers use ONLY the shared hub at `<root>/mockup/`
  (ensure it per Step 4d). The Vite dev server is for design iteration only.
- **Manifest is mandatory**: every run writes/updates `mockup-manifest.json` — without it
  the hub cannot route the app and the landing page shows it as not ready.
- **Build is mandatory**: every run ends with `npm run build` (Step 6f) so the hub can
  serve `dist/`; an unbuilt app shows as "Build required" with unclickable roles.
- **Root-relative links only in MOCKUP.html**: never hardcode `http://localhost:<port>` —
  the hub port is user-configurable.
- **ZERO dead links**: Every `<Link>`, `useNavigate()`, and `<a href>` in every file must resolve. No `href="#"`
- **Pagination on every list** (MANDATORY): Every page that renders a `<Table>` of records MUST include
  shadcn/ui `<Pagination>` below it. Default page size is **10 items per page**. Applies to: module list
  pages, history/audit pages, notifications page, and any embedded sub-tables within detail pages
  that may grow unbounded. Use React `useState` for page state. Omitting pagination from any list
  is a generation error.
- **Layout components for structure**: Header, footer, and sidebar are React components composed in a
  shared layout route â€” NOT duplicated inline in each page
- **Page components are content only**: Role page files return only the page content JSX â€” the
  layout wrapper is handled by `AppLayout` via React Router `<Outlet>`
- **React Router for navigation**: All in-app navigation uses `<Link>` or `useNavigate()` â€” no
  `window.location` assignments, no `<a href>` for internal routes
- **shadcn/ui for all UI elements**: Buttons, inputs, tables, dialogs, dropdowns, badges, tabs,
  avatars, etc. MUST use the generated shadcn/ui components â€” not raw HTML elements
- **Lucide React for all icons**: Use `import { IconName } from "lucide-react"` â€” no inline SVG,
  no icon CDN dependencies
- **Images open in new tab**: Any image link or image view action uses `target="_blank"`
- **PDFs open in new tab**: Any PDF/document view link uses `target="_blank" rel="noopener noreferrer"`
- **MOCKUP.html links open in new tab**: All screen card links in the index use `target="_blank"`
- No external image dependencies; use `https://placehold.co/` for placeholder images
- Sidebar navigation must link between pages within the same role using React Router `<Link>`
- Header navigation (notification, profile, account) links use React Router
- Table action buttons (View, Edit, Add) use React Router navigation
- Tabs within pages use shadcn/ui `<Tabs>` component
- Back/Cancel buttons use React Router `useNavigate()` or `<Link>` to the parent page
- Preserve traceability: include user story tags with version as JSX comments in each page
  (e.g., `{/* USHM00012 [v1.0.1] */}`)
- Do not generate pages for modules that have no user stories for a given role
- Common pages (home, profile, account, notifications) are generated for EVERY role
- Use consistent color scheme from the design system via CSS variables and Tailwind config
- The version displayed in footer should be the target version if specified, or the latest version
  found in PRD.md
- **Strikethrough items MUST always be excluded** â€” lines wrapped in `~~` are deprecated/removed
- **Version filtering**: When a target version is provided, only include items from sections
  with version tags <= target version
- **Model-driven pages**: When a module model file exists at `model/{kebab-module}/model.md`,
  use the actual field definitions (field names, types, required/nullable, enums) for all
  form inputs, table columns, and detail panels. Generic placeholder field names are NOT
  acceptable when a model is available. See Step 1b and the "Model-Driven Field Usage" section.
- **Enum accuracy**: Enum `<Select>` options must use the exact values from the model's Enum
  Definitions (Section 7), not inferred strings
- **Constraint-aware sample data**: Sample values must respect field constraints noted in the
  model (e.g., use `MYS`, `BHR`, `MDV` for countryCode fields constrained by CONSHM018)
- **Report layouts**: When PRD.md contains report-related NFRs or user stories, generate
  standalone HTML report layout files in `public/reports/` subfolder. These are self-contained A4
  mockups (not React components) for stakeholder review of report structure before coding.
  Use actual module model fields for column headers and realistic sample data rows. See
  Step 3f for full report layout generation rules.
- **Dark mode support**: All pages and components must support dark mode via next-themes and
  Tailwind `dark:` variant classes. shadcn/ui components handle this automatically through CSS variables.
- **TypeScript**: All generated `.tsx` files must be valid TypeScript. Use proper type annotations
  for component props, state, and event handlers. Avoid `any` types.
