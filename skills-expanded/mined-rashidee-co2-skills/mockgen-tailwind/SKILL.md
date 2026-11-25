---
name: mockgen-tailwind
model: claude-opus-4-8
effort: high
description: >
  Generate HTML mockup screens from PRD.md files for UI/UX human designer review.
  Creates Alpine.js + HTMX mockup assets with admin dashboard layout
  (left sidebar navigation, header with logo/notifications/locale/user menu, footer
  with copyright/version) served as partials, organized by user role in a mockup/ folder.
  All mockups are served by the SINGLE shared Mockup Hub at <root>/mockup — a
  zero-dependency Node.js server with a landing page listing every application and role
  (unclickable when not ready) and a configurable port (PORT env / mockup.config.json).
  Input: application name (mandatory), version (mandatory), module (optional).
  Output: mockup/ folder in the application's context folder
  containing MOCKUP.html index page, mockup-manifest.json, partials/, and role-specific
  content subfolders (assets only — no per-app server); plus the shared hub at
  <root>/mockup if not already present. Trigger on keywords: "generate mockup", "generate mockups",
  "create mockup screens", "HTML mockup", "UI mockup from user stories",
  "mockup from PRD.md", "generate screens", "create UI screens".
  Accepts application name and version as input
  (e.g., `/mockgen-tailwind hub_middleware v1.0.3`).
  Optionally accepts a module name to limit generation to screens for that module only
  (e.g., `/mockgen-tailwind hub_middleware v1.0.3 module:Location Information`).
  When module is specified, only content files for that module are generated/updated
  (plus the manifest); partials, sidebars, the shared hub, and other module screens are
  left untouched.
  Automatically excludes strikethrough (deprecated/removed) items.
---

# Mockgen HTML

Generate HTMX + Alpine.js mockup assets from PRD.md for UI/UX designer review.
Header, footer, and sidebar are served as partials. Content pages are HTMX fragments
swapped into a shell layout. All image/PDF links open in new tabs.

The application's mockup folder contains **assets only** — no server. All applications'
mockups are served by the **shared Mockup Hub**, a single zero-dependency Node.js server
at `<root>/mockup/` (see [references/mockup-hub-template.md](references/mockup-hub-template.md)).
The hub assembles pages at `/{app_slug}/{role}/{page}`, renders a landing page listing
every application and role (roles are unclickable until their mockups are ready), and
listens on a configurable port (`PORT` env var → `mockup.config.json` → 3000).

## Stack

| Layer | Technology |
|-------|------------|
| Server | Shared Mockup Hub — `<root>/mockup/server.js` (zero-dependency Node.js) |
| Partial loading / navigation | HTMX 2.x |
| Interactive UI (dropdowns, dark mode) | Alpine.js 3.x |
| Styling | Tailwind CSS (CDN) |
| Icons | Inline Heroicons SVG |

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

**App slug** (used in all generated routes): the application folder name with the leading
`<number>_` prefix stripped (e.g., `1_hub_middleware` → `hub_middleware`). Record it during
input resolution — every generated link is prefixed with `/{app_slug}`.

### Example Invocations

- `/mockgen-tailwind hub_middleware v1.0.3` (all modules, up to v1.0.3)
- `/mockgen-tailwind hub_middleware v1.0.3 module:Location Information` (one module, specific version)
- `/mockgen-tailwind "Hub Middleware" v1.0.3 module:Employer` (title-case app name)

### Version and Module Filtering

- Only include user stories, NFRs, constraints,
  and references from sections whose version tag is **less than or equal to** the target version
- If a module is provided (e.g., `module:Location Information`), only generate/update screens
  for that specific module. All other modules are skipped. Common screens (home, profile,
  account, notifications) and partials (shell, header, footer, sidebars) are
  NOT regenerated when a module filter is active â€” only the module's own content fragments
  are written (plus MOCKUP.html updated for only that module's cards and
  mockup-manifest.json refreshed).
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
will be used for traceability in the generated screens.

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
4. **Module filter scope**: the filter only affects **content fragment generation** (Step 6e).
   All other steps complete normally (parsing, design system, planning) but output is restricted
   to the filtered module's screens.

**Module-filtered generation mode** differs from full generation in these ways:

| Aspect | Full Generation | Module-Filtered |
|--------|----------------|-----------------|
| Common screens (home, profile, account, notifications) | Generate for every role | **SKIP** â€” already exist |
| Partials (shell, header, footer) | Generate | **SKIP** â€” already exist |
| Sidebar per role | Generate | **SKIP** â€” already exist |
| mockup-manifest.json | Generate | **Update** (version, generatedAt, screen counts) |
| Mockup Hub (`<root>/mockup/`) | Ensure (create/upgrade) | **Ensure** (create/upgrade) |
| Module content files (target module) | Generate | **Generate / overwrite** |
| Module content files (other modules) | Generate | **SKIP** â€” leave untouched |
| MOCKUP.html | Generate full file | **Update only the target module's cards** |
| footer.html version string | Update | **Update** (version may have changed) |

**MOCKUP.html partial update** (module-filtered mode):
- Read the existing MOCKUP.html
- Locate the screen cards section for the target module (search by module name heading or
  existing card tags)
- Replace only those cards with freshly generated ones reflecting the new screens
- Update the total screen count per role (add net new screens)
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

**Field classification** (used during content generation in Step 6e):

| Category | Definition | Usage |
|----------|-----------|-------|
| System fields | `_id`, `_audit`, `_version`, `deleted`, `deletedAt`, `deletedBy` | Exclude from user-facing forms |
| Audit-only fields | Fields whose Source is `CONVENTION` and type is `Audit` | Show in detail views only |
| Required form fields | `Required: Yes` AND not a system field | Mandatory inputs in create/edit forms |
| Optional form fields | `Required: No` AND not a system field | Optional inputs in create/edit forms |
| Read-only after creation | Fields marked as unique identity keys (e.g., `companyRegistrationNumber`) | Show in edit forms as readonly |
| Search/filter fields | Fields referenced in Index Recommendations | Render as filter controls in list screens |
| Enum fields | Type matches an entry in Section 7 Enum Definitions | Render as `<select>` dropdowns |
| Embedded object fields | Type is a custom embedded document type (not a primitive) | Render as `<fieldset>` sub-group |
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
4. Apply extracted tokens to the Tailwind CDN `<script>` config block in `shell.html` (custom colors, fonts), all generated partials (consistent color classes), and component rendering

#### 2b: Context Design Folder (Fallback)

If PRD.md does not have a `# Design System` section, or the referenced file does not exist, fall back to the application's `<app_folder>/context/design/` folder. This folder contains pre-defined design tokens and Tailwind component guidelines maintained externally by the UI/UX team.

Read all files in `{app_name}/context/design/` (where `{app_name}` is the resolved application folder name from Step 1). Apply the design tokens and guidelines found there to all generated mockup screens.

**Expected files** (any or all may be present):
- `design-system.md` â€” Colors, typography, spacing, and visual style definitions
- `components.md` â€” Reusable component patterns and Tailwind class conventions
- `guidelines.md` â€” Layout rules, accessibility standards, and stack-specific guidelines

#### 2c: Default Fallback

If neither the PRD reference nor the `{app_name}/context/design/` folder provides design tokens, use sensible defaults: a neutral color palette, Inter/system font stack, and standard Tailwind utility classes for spacing and layout.

#### 2d: Process Flow Status States

If PRD.md contains a `# High Level Process Flow` section, scan it for entity status lifecycle descriptions (e.g., "Received â†’ Validated â†’ Enriched â†’ Active"). For each status lifecycle found:
- Ensure list screens for the corresponding module include a status column with colored badges for each state
- Use design system color tokens for badge colors (e.g., success color for active/completed states, warning for pending, danger for failed/rejected)

### Step 3: Plan Screen Files

For each role, determine ALL screens to generate. **Every clickable link, tab, or action
in any generated screen MUST have a corresponding content fragment file. No link may point
to `#` or be a dead end.**

**Module filter applied here**: If a module argument was provided (Step 1c), plan only the
screens for that module across all roles. Skip common screens (home, profile, account,
notifications) and skip all other modules entirely. The screen plan table should list only
the filtered module's screens.

#### 3a: Core Screens (content fragments)

1. **home.html**: Default home/dashboard page with welcome message and summary widgets
2. **profile.html**: User profile page (linked from header user dropdown)
3. **account.html**: Account settings page (linked from header user dropdown)
4. **notifications.html**: Notifications page (linked from header notification bell)
5. **One screen per module that has user stories for this role**

#### 3b: Sub-Screens (Detail / Edit / Create)

For each module screen, analyze the user stories and identify sub-screens needed:

| User Story Pattern | Sub-Screen Required |
|-------------------|---------------------|
| "view details of X" | `{module}_detail.html` - Detail view for a single record |
| "add/create/register X" | `{module}_create.html` - Create/add form |
| "edit/update/modify X" | `{module}_edit.html` - Edit form (pre-filled) |
| "view history/audit of X" | `{module}_history.html` - History/audit log view |
| "view associated X of Y" | `{module}_{sub}_list.html` - Associated records list |

#### 3f: Report Layout Screens (conditional â€” if PRD.md contains report-related content)

Scan PRD.md for report-related content:
- NFRs mentioning "report", "Report interface", "generate report", "report generation"
- User stories describing generating/downloading PDF, Excel, or CSV reports
- A "Report" module or report-related NFRs defining specific report types

**If report requirements are found**, generate HTML report layout mockups for each
identified report. These layouts serve as draft previews for human designers/stakeholders
to verify the report structure before the AI coding agent implements the actual report
generation code (JasperReports JRDesign API for Java, Puppeteer for Laravel/React).

For each identified report, create a standalone HTML file in a `reports/` subfolder:

| Report Source | File Generated |
|--------------|----------------|
| NFR describes "Staff Allocation Summary report" | `reports/staff_allocation_summary.html` |
| User story: "generate Job Demand report by country" | `reports/job_demand_by_country.html` |
| Report module NFR: "Monthly Activity Report" | `reports/monthly_activity_report.html` |

**Report layout file conventions:**
- Each report layout is a **standalone self-contained HTML document** (not a content fragment)
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

#### 3c: Tabbed Screens

If a module screen contains tabs (e.g., a detail page with Overview, Documents, History tabs),
**each tab MUST be a separate content fragment file** unless the tab content is trivially small.
Use the naming convention: `{module}_tab_{tab_name}.html`

Example: `employer_tab_overview.html`, `employer_tab_documents.html`, `employer_tab_history.html`

#### 3d: Screen File Naming Convention

Convert names to snake_case, no `.html` extension in HTMX route references.
Example: "Location Information" -> `location_information`

#### 3e: Build Screen Plan

Build a **complete** screen plan. Every entry must map to a generated file:

| Role | Folder Name | Screen File | Source | Description |
|------|-------------|-------------|--------|-------------|
| Hub Administrator | hub_administrator | home | Common | Dashboard home |
| Hub Administrator | hub_administrator | profile | Common | User profile |
| Hub Administrator | hub_administrator | account | Common | Account settings |
| Hub Administrator | hub_administrator | notifications | Common | Notifications list |
| Hub Administrator | hub_administrator | location_information | Module | USHM00006, USHM00009 |
| Hub Administrator | hub_administrator | location_information_detail | Sub-screen | View location details |
| Hub Administrator | hub_administrator | location_information_create | Sub-screen | Add new location |
| Hub Operation Support | hub_operation_support | home | Common | Dashboard home |
| Hub Operation Support | hub_operation_support | profile | Common | User profile |
| Hub Operation Support | hub_operation_support | account | Common | Account settings |
| Hub Operation Support | hub_operation_support | notifications | Common | Notifications list |
| Hub Operation Support | hub_operation_support | employer | Module | USHM00021-USHM00033 |
| Hub Operation Support | hub_operation_support | employer_detail | Sub-screen | View employer details |
| Hub Operation Support | hub_operation_support | employer_create | Sub-screen | Register new employer |

### Step 4: Create Output Folder Structure

**Module filter**: When a module argument is active, skip this step entirely â€” the folder
structure already exists from a previous full generation. Only content files for the target
module will be written in Step 6e.

Create the mockup folder at the auto-resolved mockup output path (full generation only).
The folder contains **assets only** â€” no server files (the shared hub at `<root>/mockup/`
serves them):

```
<app_folder>/context/
  mockup/
    mockup-manifest.json             # Hub discovery manifest (app, stack, roles, version)
    MOCKUP.html                      # Per-app screen index (served by hub at /{app_slug})
    partials/
      shell.html                     # Page shell (assembled server-side)
      header.html                    # Top header with Alpine.js dropdowns
      footer.html                    # Footer partial
      sidebar-{role_snake_case}.html # One sidebar per role with HTMX nav
    {role_snake_case}/
      content/
        home.html                    # Content fragment (no layout wrapper)
        profile.html
        account.html
        notifications.html
        {module_snake_case}.html
        {module_snake_case}_detail.html
        {module_snake_case}_create.html
        {module_snake_case}_edit.html
        ...
```

### Step 4b: Write mockup-manifest.json

**Module filter**: When a module argument is active, UPDATE the existing manifest
(version, generatedAt, per-role screen counts) instead of regenerating it.

Write `<app_folder>/context/mockup/mockup-manifest.json` following the schema in
[references/mockup-hub-template.md](references/mockup-hub-template.md):

```json
{
  "app": "{app_slug}",
  "appName": "{App Name}",
  "description": "{short description from PRD.md}",
  "stack": "tailwind",
  "version": "{target version}",
  "generatedAt": "{YYYY-MM-DD}",
  "roles": [
    { "name": "{Role Name}", "slug": "{role_snake_case}", "screens": {count} }
  ],
  "reports": ["{report_file}.html"]
}
```

(`reports` only when report layouts were generated.) The hub reads this manifest to route
the app and to render its landing-page card; without it the app shows as "Not generated
yet" and its roles are unclickable.

### Step 4c: Ensure the Mockup Hub

**Always runs** (full AND module-filtered generation).

Ensure the shared hub exists at `<root>/mockup/` per the Ensure-Hub rules in
[references/mockup-hub-template.md](references/mockup-hub-template.md):

1. `<root>/mockup/server.js` missing â†’ create `server.js`, `package.json`,
   `mockup.config.json`, and `.gitignore` from the templates.
2. Exists â†’ compare the `HUB_VERSION` marker; overwrite `server.js` + `package.json` only
   when the existing version is lower. Never overwrite an existing `mockup.config.json`
   or `.gitignore`.
3. All hub artifacts (config, logs, any `node_modules/`) live inside `<root>/mockup/` and
   are covered by its `.gitignore`.

Key behaviours of the hub (for reference):
- `GET /` â†’ landing page listing ALL applications and roles (unclickable when not ready)
- `GET /{app_slug}` â†’ serves this app's `MOCKUP.html`
- `GET /{app_slug}/{role}` â†’ redirects to `/{app_slug}/{role}/home`
- `GET /{app_slug}/{role}/{page}` â†’ assembles shell + header + sidebar + content + footer
- `GET /api/content/{app_slug}/{role}/{page}` â†’ content fragment only (HTMX swaps)
- `GET /{app_slug}/static/*` and `GET /{app_slug}/reports/*` â†’ static assets
- Injects `{{ROLE}}` into the header partial before responding
- Port: `PORT` env var â†’ `mockup.config.json` â†’ 3000

### Step 5: Generate MOCKUP.html Index

**Module filter**: When a module argument is active, do NOT regenerate the full MOCKUP.html.
Instead, apply a **partial update** as described in Step 1c: update only the target module's
screen cards, the version badge, and the per-role screen count. Leave all other content
unchanged.

Create the index page using the template in [references/mockup-index-template.md](references/mockup-index-template.md).

MOCKUP.html is this app's screen index, served by the hub at `/{app_slug}`. It shows:
- Hub startup banner with instructions (`cd <root>/mockup && npm start` â€” no install
  needed; port configurable via `PORT` env var or `mockup.config.json`)
- Application name and description
- **Target version** used for generation
- Number of excluded items for transparency
- For each role: role name, list of screen cards with links
- **ALL screen links use `target="_blank" rel="noopener noreferrer"`** with
  **root-relative** URLs `/{app_slug}/{role}/{page}` (never hardcode `http://localhost:<port>`
  â€” the port is user-configurable) so they open in new tabs via the running hub
- A "Open Role Dashboard" quick-launch link per role section

### Step 6: Generate Partials and Content Fragments

Use templates from [references/admin-layout-template.md](references/admin-layout-template.md).

**Apply the design system** from Step 2 (colors, typography, spacing) to all templates.

**Module filter**: When a module argument is active, skip steps 6aâ€“6d (shell, header,
footer, sidebars). Proceed directly to **6e** for the target module's content fragments only.
Also update `partials/footer.html` if the version string changed (the footer version badge
must always reflect the current target version).

#### 6a: Generate partials/shell.html

Single shared shell file. The server replaces `{{HEADER}}`, `{{SIDEBAR}}`, `{{CONTENT}}`,
and `{{FOOTER}}` at request time. Includes HTMX, Alpine.js, and Tailwind CDN.

#### 6b: Generate partials/header.html

One header partial (or one per role if HTMX links differ per role). Contains:
- Logo + App Name (left)
- Notification bell with Alpine.js dropdown (`x-data`, `@click`, `@click.outside`)
- Globe/locale selector with Alpine.js dropdown
- Dark mode toggle button (dispatches to parent `appShell()` Alpine context)
- User avatar with Alpine.js dropdown (Profile, Account, Logout)
- All notification/profile/account navigation links use HTMX (`hx-get`, `hx-target="#content-area"`)

#### 6c: Generate partials/footer.html

Simple footer with copyright year and version string.

#### 6d: Generate partials/sidebar-{role}.html (one per role)

Each sidebar contains HTMX-powered navigation links. `{{APP_SLUG}}` is replaced with the
app slug **at generation time** (it is constant for the whole mockup folder):
```html
<a href="/{{APP_SLUG}}/{{ROLE}}/{{PAGE}}"
   hx-get="/api/content/{{APP_SLUG}}/{{ROLE}}/{{PAGE}}"
   hx-target="#content-area"
   hx-swap="innerHTML"
   hx-push-url="/{{APP_SLUG}}/{{ROLE}}/{{PAGE}}"
   ...>
```
Alpine.js `:class` binding highlights the active menu item based on `window.location.pathname`.

#### 6e: Generate content fragments ({role}/content/{page}.html)

Each content fragment contains **only** the page content â€” no `<html>`, `<head>`, `<body>`,
no Tailwind config, no CDN scripts. Structure:

```
[breadcrumb bar div]
[main content div with padding]
```

**All navigation links within content fragments use HTMX** (same pattern as sidebar).

**Breadcrumbs**: Home link uses HTMX; module link uses HTMX; current page is plain text.

#### Admin Layout: Screen Content Generation

For each module screen, analyze the user stories and generate appropriate UI mockup elements:

| User Story Pattern | UI Element |
|-------------------|------------|
| "search for X based on parameters" | Search form with filter fields + results table |
| "view details of X" | Detail view with labeled fields in card/panel layout |
| "manage X" / "configure X" | CRUD table with Add/Edit/Delete actions |
| "view history/changes" | Timeline or audit log table with timestamps |
| "map X to Y" | Two-panel mapping interface or matrix table |
| "activate/deactivate X" | Alpine.js toggle switches in table rows or config panel |
| "view associated X" | Related records table or linked cards section |

#### Model-Driven Field Usage (MANDATORY when model file exists)

When a module model was loaded in Step 1b, use its actual field definitions â€” not generic placeholders â€” to populate every screen. Generic field names like "Field 1" or "Description" are not acceptable when a model is available.

**Field type â†’ HTML input mapping:**

| Model Type | Form Input | Notes |
|------------|-----------|-------|
| `String` | `<input type="text">` | Use `maxlength` if constraints specify length |
| `Number` | `<input type="number">` | |
| `Boolean` | Alpine.js toggle (`x-data`, `@click`) | |
| `ISODate` | `<input type="date">` or `<input type="datetime-local">` | |
| `ObjectId` (reference) | `<input type="text" readonly>` or lookup widget | Display as read-only ID reference |
| Enum (Section 7 match) | `<select>` with all enum values as `<option>` | Show enum value descriptions as option text |
| Embedded Object | `<fieldset>` grouping sub-fields | Label the fieldset with the embedded type name |
| Embedded Array (`[]`) | Repeatable section with "+ Add" / "Remove" buttons | Show one pre-filled example row |

**List / Search screens** (`{module}.html`):
- **Filter form**: render filter inputs only for fields that appear in Index Recommendations (Section 9). Use the correct input type per the mapping above. Enum-indexed fields use `<select>`. Date-indexed fields use date range pickers.
- **Results table**: choose 5â€“7 of the most identifying non-system fields as columns. For embedded objects, show them as a single column (e.g., "Company Name" rather than expanding all sub-fields). Null/optional fields can be shown with a dash (`â€”`) in sample data.
- **Table row actions**: View â†’ `{module}_detail`, Edit â†’ `{module}_edit`, Delete â†’ Alpine.js confirm
- **Pagination** (MANDATORY): Every results table MUST include a pagination bar directly below the table. Requirements:
  - Default page size: **10 items per page**
  - Show "Showing Xâ€“Y of Z results" summary text on the left
  - Show page size selector (`<select>`) with options 10, 25, 50 on the right (default 10)
  - Show Previous / Next buttons and page number buttons in the centre
  - Page number buttons: show first page, last page, current page Â± 1, with `...` ellipsis for gaps
  - Use Alpine.js `x-data="{ currentPage: 1, pageSize: 10, totalItems: 47 }"` (sample total) to drive display state
  - Page buttons use HTMX `hx-get` linking to the same route (self-referential) â€” acceptable per Link Integrity Rule 6
  - Previous/Next buttons are disabled (visual only with `opacity-50 cursor-not-allowed`) when at first/last page
  - Use sample data: populate exactly 10 visible rows in the table (matching the default page size)

**Detail screens** (`{module}_detail.html`):
- Show ALL non-system fields, grouped logically:
  - Basic fields: flat primitive fields in a 2-column grid card
  - Embedded objects (e.g., `address`, `contact`): each in its own labelled sub-card
  - Embedded arrays (e.g., `personsInCharge`): rendered as a sub-table with a row per item
  - Enum fields: display value wrapped in a colored badge/chip
  - ISODate fields: formatted as `DD MMM YYYY HH:mm` in sample data
  - Boolean fields: show as a green/red badge ("Active" / "Inactive")
- Include Edit, Delete (Alpine.js confirm), and Back to List action buttons

**Create screens** (`{module}_create.html`):
- Include ALL `Required: Yes` non-system fields as mandatory inputs (mark with `*`)
- Include `Required: No` fields as optional inputs where they make sense for initial creation
- Group embedded objects as `<fieldset>` sections with a legend
- For embedded arrays: show one empty repeatable row with an "+ Add" button
- Submit and Cancel buttons; Cancel navigates back to `{module}` list screen

**Edit screens** (`{module}_edit.html`):
- Same structure as create screen but with sample data pre-filled in all inputs
- Fields that serve as unique identity keys (e.g., `companyRegistrationNumber`) must be rendered as `<input readonly>` with a tooltip explaining they cannot be changed
- Save and Cancel buttons

**History / Audit screens** (`{module}_history.html`):
- Use fields from the **audit/history collection** (the non-root collection in the Collection Catalog):
  - `changeType` â†’ colored badge using enum values from Section 7
  - `fieldChanged` â†’ code-styled text (`<code>`)
  - `previousValue` / `newValue` â†’ inline diff or truncated JSON display
  - `changedAt` â†’ formatted timestamp
  - `changedBy` â†’ plain text (e.g., "SYSTEM" or username)
- Render as a chronological table, newest first
- **Pagination** (MANDATORY): Include pagination bar below the history table. Default 10 items per page. Same Alpine.js + HTMX pattern as list screens (see above).

**Sample data alignment**: Placeholder values in screens must be consistent with field constraints:
- `countryCode` â†’ use actual allowed values (e.g., "MYS", "BHR", "MDV") per CONSHM constraints if present in model notes
- Enum fields â†’ use one of the defined enum values (not arbitrary strings)
- `companyRegistrationNumber` â†’ e.g., "201901012345 (1234567-X)"
- `ISODate` fields â†’ use realistic ISO dates (e.g., "2025-08-15T10:30:00Z")

---

#### Link Integrity Rules (CRITICAL)

**Every clickable element MUST navigate to a real route. No `href="#"` allowed anywhere.**

1. **Table row actions** (View, Edit, Delete):
   - "View" / "Details" â†’ HTMX link to `/{app_slug}/{role}/{module}_detail`
   - "Edit" â†’ HTMX link to `/{app_slug}/{role}/{module}_edit`
   - "Delete" â†’ Alpine.js inline confirm dialog (`href="javascript:void(0)"`)
   - "Add New" / "Create" â†’ HTMX link to `/{app_slug}/{role}/{module}_create`

2. **Tabs within a screen**:
   - Each tab MUST HTMX-link to its corresponding content file
   - The current tab is visually active; other tabs link to their respective content pages

3. **Header links**:
   - Notification bell icon â†’ HTMX nav to `notifications`
   - Notification dropdown "View all notifications" â†’ HTMX nav to `notifications`
   - Locale dropdown options â†’ `javascript:void(0)` (static language switcher mockup)
   - Night mode toggle â†’ Alpine.js `@click="toggleDark()"` (no href)
   - Profile dropdown â†’ HTMX nav to `profile`
   - Account dropdown â†’ HTMX nav to `account`
   - Logout â†’ `href="/"` (returns to the hub landing page)

4. **Sidebar links**: HTMX links to correct module screen routes (already enforced)

5. **Breadcrumb links**: HTMX links
   - Home â†’ `/{app_slug}/{role}/home`
   - Module â†’ `/{app_slug}/{role}/{module}`
   - Detail / current â†’ plain text, no link

6. **Pagination links**: HTMX `hx-get` links to the same route (self-referential) are acceptable. Pagination is MANDATORY on every list â€” page buttons must use `hx-get` with the same route, not `href="#"`

7. **Back / Cancel buttons**: HTMX link to the parent screen

8. **Images** (inline previews, thumbnails, etc.):
   - Must open the full image in a **new tab** via `<a href="..." target="_blank" rel="noopener noreferrer">`
   - Use placeholder image URLs like `https://placehold.co/800x600`

9. **PDFs and documents** (download/view links):
   - Must open in a **new tab** via `<a href="..." target="_blank" rel="noopener noreferrer">`
   - Never render PDFs inline within the mockup

**Content guidelines:**
- Use placeholder/sample data that reflects the module context
- Include appropriate form fields based on NFRs and constraints
- Show the user story tags with their version as HTML comments for traceability
  (e.g., `<!-- USHM00012 [v1.0.1] -->`)
- All interactive elements use Alpine.js (`x-data`, `x-show`, `@click`, `:class`)
- Use Tailwind utility classes for all styling
- Use inline Heroicons SVG (no external icon dependencies)

#### Common Screens Content

**profile.html**: User profile page showing:
- User avatar, full name, email, role badge
- Personal information form (read-only display): Name, Email, Phone, Department
- "Edit Profile" button (HTMX links to self since it's a mockup)

**account.html**: Account settings page showing:
- Change Password section (current password, new password, confirm password fields)
- Notification Preferences (Alpine.js email/SMS toggles)
- Language/Locale selector (Alpine.js)
- Session Management (active sessions table)

**notifications.html**: Notifications list page showing:
- Alpine.js filter tabs: All, Unread, Read
- List of notification cards with: icon, title, message preview, timestamp, read/unread dot
- Mark all as read button
- **Pagination** (MANDATORY): Pagination bar below the notification list, default 10 items per page. Same Alpine.js + HTMX pattern as list screens.

#### Sub-Screen Content

**{module}_detail.html**: Record detail page showing:
- Page title with record identifier
- Back button (HTMX link to `{module}`)
- Detail cards/panels with all relevant fields from user stories
- Action buttons: Edit (HTMX to `{module}_edit`), Delete (Alpine.js confirm), Back to List
- Related data sections if applicable
- If the entity has sub-entities, show them in HTMX-linked tabs or sections

**{module}_create.html**: Create/add form page showing:
- Page title: "Add New {Entity}"
- Breadcrumb: Home > {Module} > Add New
- Form with all required fields derived from user stories
- Submit and Cancel buttons (Cancel: HTMX link to `{module}`)

**{module}_edit.html**: Edit form page showing:
- Page title: "Edit {Entity}"
- Breadcrumb: Home > {Module} > Edit
- Pre-filled form with sample data
- Save and Cancel buttons (Cancel: HTMX link to `{module}_detail` or `{module}`)

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

| Role                  | Screens | Content Folder                    |
|-----------------------|---------|-----------------------------------|
| Hub Administrator     | 8       | hub_administrator/content/        |
| Hub Operation Support | 6       | hub_operation_support/content/    |

Files generated:
- mockup-manifest.json
- MOCKUP.html
- partials/shell.html, header.html, footer.html
- partials/sidebar-hub_administrator.html
- partials/sidebar-hub_operation_support.html
- {N} content fragment files
- Mockup Hub: {created at <root>/mockup | upgraded to v{N} | already present}

Total: {N} files

Quick Start
===========
1. cd <root>/mockup
2. npm start          (zero dependencies â€” no npm install required)
3. Open http://localhost:3000 in your browser
   - Landing page lists ALL applications and roles
   - This app's screen index: http://localhost:3000/{app_slug}
4. Change port: PORT=4000 npm start, or edit <root>/mockup/mockup.config.json
```

### Step 7b: Link Integrity Validation (MANDATORY)

Before finalizing output, perform a link integrity check across ALL generated files:

1. **Scan every generated file** for all `href`, `hx-get`, and `hx-push-url` attribute values
2. **Build a link registry**: map every route reference to the file that should exist
3. **Verify each HTMX route** resolves to an existing content fragment:
   - `hx-get="/api/content/{app_slug}/{role}/{page}"` â†’ verify `{role}/content/{page}.html` exists
   - Every internal route MUST start with `/{app_slug}/` (or `/api/content/{app_slug}/`)
     â€” un-prefixed routes like `/{role}/{page}` are dead links under the hub
   - `href="javascript:void(0)"` â†’ acceptable for delete confirm, locale switcher
   - `href="/"` â†’ acceptable for logout
   - `target="_blank"` links â†’ acceptable for images, PDFs, external resources
   - `href="#"` â†’ **NOT ALLOWED** â€” dead link, must be fixed
4. **For any missing target file**, either:
   - Generate the missing content fragment, OR
   - Update the link to point to an existing route
5. **Report any fixes** made during validation in the output summary

If any `href="#"` is found in the final output (excluding anchor-only usage), the generation
is **incomplete**.

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
5. Row format: `| {YYYY-MM-DD} | {application_name} | mockgen-tailwind | {module or "All"} | Generated HTML mockup screens |`
6. **Never modify or delete existing rows.**

## Important Rules

- **Module filter is additive, not destructive**: When `module:` is specified, only the named
  module's content files are written/overwritten (plus manifest/MOCKUP.html updates). All
  other files (partials, other module content) remain untouched. If the target module does
  not exist in PRD.md, stop and report available module names before doing any file writes.
- **No per-app server**: NEVER generate `server.js`/`package.json` inside the application's
  mockup folder. All serving is done by the shared hub at `<root>/mockup/` (ensure it per
  Step 4c). All npm/machine artifacts stay inside `<root>/mockup/` and are gitignored there.
- **Manifest is mandatory**: every run writes/updates `mockup-manifest.json` â€” without it
  the hub cannot route the app and the landing page shows it as not ready.
- **Root-relative links only**: never hardcode `http://localhost:<port>` in any generated
  file â€” the hub port is user-configurable.
- **Version + module are independent axes**: Both may be combined freely. `module:Employer
  v1.0.2` means "generate Employer module screens as they exist at v1.0.2". Version filtering
  and module filtering each apply independently; a story must satisfy BOTH to be included.
- **ZERO dead links**: Every `href` and `hx-get` in every file must resolve. No `href="#"`
- **Pagination on every list** (MANDATORY): Every screen that renders a table or card list of records MUST include a pagination bar below it. Default page size is **10 items per page**. Applies to: module list screens, history/audit screens, notifications screen, and any embedded sub-tables within detail screens that may grow unbounded. Use Alpine.js `x-data` for page state and HTMX `hx-get` (self-referential) for page navigation. Omitting pagination from any list is a generation error.
- **Partials for layout**: Header, footer, and sidebar are partial files, NOT duplicated inline
- **Content fragments only**: Role screen files contain only page content â€” no `<html>/<head>/<body>`
- **HTMX navigation**: All in-app navigation uses HTMX (`hx-get`, `hx-target`, `hx-push-url`)
- **Alpine.js for interactivity**: Dropdowns, toggles, confirm dialogs use Alpine.js
- **Images open in new tab**: Any `<img>` link or image view action uses `target="_blank"`
- **PDFs open in new tab**: Any PDF/document view link uses `target="_blank" rel="noopener noreferrer"`
- **MOCKUP.html links open in new tab**: All screen card links in the index use `target="_blank"`
- No external image dependencies; use `https://placehold.co/` for placeholder images
- Use inline SVG Heroicons only; no icon CDN dependencies
- Sidebar navigation must link between screens within the same role using HTMX
- Header navigation (notification, profile, account) links use HTMX
- Table action buttons (View, Edit, Add) use HTMX navigation
- Tabs within screens each link to a corresponding content fragment via HTMX
- Back/Cancel buttons use HTMX to navigate to the parent list or detail screen
- Preserve traceability: include user story tags with version as HTML comments in each screen
  (e.g., `<!-- USHM00012 [v1.0.1] -->`)
- Do not generate screens for modules that have no user stories for a given role
- Common screens (home, profile, account, notifications) are generated for EVERY role
- Use consistent color scheme from the design system across all partials and content fragments
- The version displayed in footer should be the target version if specified, or the latest version
  found in PRD.md
- **Strikethrough items MUST always be excluded** â€” lines wrapped in `~~` are deprecated/removed
- **Version filtering**: When a target version is provided, only include items from sections
  with version tags <= target version
- **Model-driven screens**: When a module model file exists at `model/{kebab-module}/model.md`,
  use the actual field definitions (field names, types, required/nullable, enums) for all
  form inputs, table columns, and detail panels. Generic placeholder field names are NOT
  acceptable when a model is available. See Step 1b and the "Model-Driven Field Usage" section.
- **Enum accuracy**: Enum select options must use the exact values from the model's Enum
  Definitions (Section 7), not inferred strings
- **Constraint-aware sample data**: Sample values must respect field constraints noted in the
  model (e.g., use `MYS`, `BHR`, `MDV` for countryCode fields constrained by CONSHM018)
- **Report layouts**: When PRD.md contains report-related NFRs or user stories, generate
  standalone HTML report layout files in `reports/` subfolder. These are self-contained A4
  mockups (not content fragments) for stakeholder review of report structure before coding.
  Use actual module model fields for column headers and realistic sample data rows. See
  Step 3f for full report layout generation rules.
