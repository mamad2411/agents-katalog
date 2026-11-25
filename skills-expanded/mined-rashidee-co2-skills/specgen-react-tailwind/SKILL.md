---
name: specgen-react-tailwind
model: claude-opus-4-8
effort: high
description: >
  Generate a detailed specification document for building a React SPA (Single Page
  Application) using React 19, TypeScript 5, Vite 6, Tailwind CSS v3, Headless UI v2,
  Heroicons, React Router v7, TanStack Query v5, Zustand v5, React Hook Form v7, and
  Zod v3. Components are built utility-first with Tailwind and made accessible with
  Headless UI primitives (no component framework like MUI). Authentication (Keycloak
  OAuth2/OIDC PKCE, generic OIDC, or none), API integration (REST via Axios), and optional
  features (WebSocket, i18n, TanStack Table data grids, Recharts charts, react-day-picker
  date pickers, Tiptap rich text) are configurable based on user input.
  Standardized input: application name (mandatory), version (mandatory), module (optional).
  Use this skill whenever the user asks to create a spec, specification, blueprint, or
  technical design document for a new React SPA or frontend application styled with Tailwind CSS.
  Also trigger when the user says things like "spec out a new React Tailwind project",
  "design a React SPA with Tailwind", "write a technical spec for my new Tailwind frontend app",
  "scaffold spec for a React Tailwind app", or any request for a specification document
  describing a React + Tailwind + TypeScript application. Even if the user only mentions
  a subset of the stack (e.g., "React SPA with Tailwind" or "React + Headless UI" or
  "React Tailwind dashboard"), this skill likely applies — ask and confirm.
---

# React SPA Specification Generator (Tailwind CSS)

This skill generates a comprehensive specification document (Markdown) that serves as a
blueprint for building a React Single Page Application styled with Tailwind CSS. The spec
is intended to be followed by a developer or a coding agent to produce a fully functional
project scaffold.

The specification does NOT generate code. It produces a detailed, opinionated technical
document describing every layer of the application — from Vite configuration to the
Tailwind design-token theme to React Query patterns — so that implementation becomes a
mechanical exercise.

This skill is the Tailwind-CSS sibling of `specgen-react-mui`. It keeps the same React data
stack (React Router, TanStack Query, Zustand, React Hook Form, Zod, Axios) but replaces the
Material UI component framework with a **utility-first Tailwind layer**: components are
hand-built with Tailwind classes and made accessible with **Headless UI** primitives
(Dialog, Menu, Listbox, Combobox, Switch, Tabs, Popover, Transition) and **Heroicons**.

## Technology Stack

### Core Stack (Always Included)

These are the fixed versions the spec targets. Do not deviate unless the user explicitly
requests different versions.

| Component            | Version   |
|----------------------|-----------|
| React                | 19.x      |
| TypeScript           | 5.x       |
| Vite                 | 6.x       |
| Tailwind CSS         | 3.x       |
| PostCSS              | 8.x       |
| Autoprefixer         | 10.x      |
| @tailwindcss/forms   | 0.5.x     |
| Headless UI (`@headlessui/react`) | 2.x |
| Heroicons (`@heroicons/react`)    | 2.x |
| clsx                 | 2.x       |
| tailwind-merge       | 2.x       |
| class-variance-authority | 0.7.x |
| React Router         | 7.x       |
| TanStack Query       | 5.x       |
| Zustand              | 5.x       |
| React Hook Form      | 7.x       |
| Zod                  | 3.x       |
| Axios                | 1.x       |
| Node.js              | 22.x LTS  |

### Optional Integration Versions

Include in the version table only when the corresponding integration is selected.

| Component            | Version   | When Selected          |
|----------------------|-----------|------------------------|
| Keycloak             | 26.x      | Auth = Keycloak        |
| oidc-client-ts       | 3.x       | Auth = Keycloak or OIDC|
| react-oidc-context   | 3.x       | Auth = Keycloak or OIDC|
| @tanstack/react-table| 8.x       | DataGrid = yes         |
| recharts             | 2.x       | Charts = yes           |
| react-day-picker     | 9.x       | DatePickers = yes      |
| date-fns             | 4.x       | DatePickers = yes      |
| Socket.io Client     | 4.x       | WebSocket = yes        |
| react-i18next        | 15.x      | i18n = yes             |
| i18next              | 24.x      | i18n = yes             |
| @tiptap/react + @tiptap/starter-kit | 2.x | RichText = yes |
| @tailwindcss/typography | 0.5.x  | RichText = yes         |

## Core Dependencies (package.json)

The spec must include these in the npm configuration section (always):

**Production dependencies:**
- `react` + `react-dom` — Core React
- `react-router-dom` — Client-side routing
- `@tanstack/react-query` — Server state and data fetching
- `zustand` — Global client state management
- `react-hook-form` — Form state management
- `@hookform/resolvers` — Zod integration for React Hook Form
- `zod` — Schema validation
- `axios` — HTTP client
- `@headlessui/react` — Accessible, unstyled interactive primitives (Dialog, Menu, Listbox, Combobox, Switch, Tabs, Popover, Transition)
- `@heroicons/react` — Icon set (outline + solid)
- `clsx` — Conditional className composition
- `tailwind-merge` — Resolve conflicting Tailwind classes (powers the `cn()` helper)
- `class-variance-authority` — Type-safe component style variants (Button, Badge, etc.)

**Development dependencies:**
- `typescript` — Type checking
- `@types/react` + `@types/react-dom` — React type definitions
- `vite` + `@vitejs/plugin-react` — Build tooling
- `tailwindcss` + `postcss` + `autoprefixer` — Tailwind CSS build pipeline
- `@tailwindcss/forms` — Sensible form-control reset that pairs well with Headless UI inputs
- `@tanstack/react-query-devtools` — Query devtools (dev only)
- `eslint` + `@typescript-eslint/*` — Linting

### Conditional Dependencies

**If Auth = Keycloak or OIDC:**
- `oidc-client-ts` — OAuth2/OIDC PKCE client
- `react-oidc-context` — React context wrapper for oidc-client-ts

**If DataGrid = yes:**
- `@tanstack/react-table` — Headless table/data-grid (sorting, filtering, pagination, row selection) styled with Tailwind

**If Charts = yes:**
- `recharts` — Composable SVG chart components

**If DatePickers = yes:**
- `react-day-picker` — Accessible date/range picker rendered inside a Headless UI `Popover`
- `date-fns` — Date manipulation and formatting

**If WebSocket = yes:**
- `socket.io-client` — WebSocket client

**If i18n = yes:**
- `react-i18next` + `i18next` — Internationalization
- `i18next-browser-languagedetector` — Auto language detection
- `i18next-http-backend` — Lazy translation loading

**If RichText = yes:**
- `@tiptap/react` + `@tiptap/starter-kit` — Headless, extensible WYSIWYG editor (React 19 compatible)
- `@tiptap/extension-link` + `@tiptap/extension-placeholder` — Common editor extensions
- `@tailwindcss/typography` — `prose` classes to style rendered rich-text HTML
- `dompurify` + `@types/dompurify` — HTML sanitization when rendering stored rich-text content

**If Reporting = yes:**
- `xlsx` — Client-side XLSX file generation
- `papaparse` + `@types/papaparse` — Client-side CSV generation
- Report service (Node.js companion): `puppeteer`, `express`, `cors` — server-side HTML-to-PDF via headless Chrome

## When the Skill Triggers

Generate the spec when the user provides an **application name** and **version** that
corresponds to one of the custom applications defined in `CLAUDE.md`. The skill
reads all required inputs from the project's context files — no interactive Q&A is needed
for the core inputs.

The user invokes this skill by specifying the target application and version, for example:
- `/specgen-react-tailwind admin v1.0.4`
- `/specgen-react-tailwind admin v1.0.4 module:Hero Section`
- `/specgen-react-tailwind "Admin Portal" v1.0.4`

The skill then locates the matching context folder and reads all input files automatically.

## Version Gate

Before starting any work, resolve the application folder first (see Input Resolution below), then check `CHANGELOG.md` in the application folder (`<app_folder>/CHANGELOG.md`):

1. If `<app_folder>/CHANGELOG.md` does not exist, skip this check (first-ever execution for this application).
2. If `<app_folder>/CHANGELOG.md` exists, scan all `## vX.Y.Z` headings and determine the **highest version** using semantic versioning comparison.
3. Compare the requested version against the highest version:
   - If requested version **>=** highest version: proceed normally.
   - If requested version **<** highest version: **STOP immediately**. Print: `"Version {requested} is lower than the current application version {highest} recorded in <app_folder>/CHANGELOG.md. Execution rejected."` Do NOT proceed with any work.

## Input Resolution

This skill uses standardized input resolution. Provide:

| Argument | Required | Example | Description |
|----------|----------|---------|-------------|
| `<application>` | Yes | `admin` | Application name to locate the context folder |
| `<version>` | Yes | `v1.0.4` | Version to scope processing |
| `module:<name>` | No | `module:Hero Section` | Limit generation to a single module |

### Application Folder Resolution

The application name is matched against root-level application folders:
1. Strip any leading `<number>_` prefix from folder names (e.g., `1_admin` → `admin`)
2. Match case-insensitively against the provided application name
3. Accept snake_case, kebab-case, or title-case input (all match the same folder)
4. If no match found, list available applications and stop

### Auto-Resolved Paths

| File | Resolved Path |
|------|---------------|
| PRD.md | `<app_folder>/context/PRD.md` |
| Module Models | `<app_folder>/context/model/` |
| HTML Mockups | `<app_folder>/context/mockup/` |
| Output (specification) | `<app_folder>/context/specification/` |

### Version Filtering

When a version is provided, only include user stories, NFRs, and constraints from versions
<= the provided version. For example, if `v1.0.4` is specified:
- Include items tagged `[v1.0.0]`, `[v1.0.1]`, `[v1.0.2]`, `[v1.0.3]`, `[v1.0.4]`
- Exclude items tagged `[v1.0.5]` or later
- Version comparison uses semantic versioning order

### Module Filtering

When `module:<name>` is provided:
- Only generate the `SPEC.md` for that specific module
- Other existing module spec files remain untouched
- `SPECIFICATION.md` (root) gets a partial update — only that module's entry in the TOC
  is added or updated; all other TOC entries are preserved as-is

## Gathering Input

The specification is driven by **six input sources** read from the project's context files.
The skill does NOT ask the user for auth, API backend URL, or optional component choices —
it **determines** these automatically from the context.

### Input 1: Application Name (from CLAUDE.md)

From CLAUDE.md (already loaded in context), locate the target application under the
**Custom Applications** section. Extract:

- **Application name**: The section heading (e.g., "Admin Portal", "Landing Page")
- **Application description**: The description paragraph below the heading
- **Dependencies**: The "Depends on" list — primary source for determining backend API
  base URL, authentication provider, and optional components

The application name is used to derive:
- **Project slug**: Kebab-case of the application name (e.g., `admin-portal`)
- **Vite env prefix**: `VITE_` (standard Vite convention)
- **App title**: Title-case of application name (e.g., "Admin Portal")

### Input 2: User Stories (from PRD.md)

Read `<app_folder>/context/PRD.md`. This file contains all user stories organized by
module. Extract:

- **System modules**: Modules under `# System Module` heading (e.g., Authentication,
  User Management). These become system-level features.
- **Business modules**: Modules under `# Business Module` heading (e.g., Hero Section,
  Product and Service). These become business-level features.
- **User stories per module**: Each `### User Story` section contains tagged items.
  These define the functional requirements for each feature's API hooks, form schemas,
  and page components.

The user stories directly inform:
- Which API calls each feature's hooks must expose
- Which pages and routes are needed
- Which form fields and validation schemas apply
- Which Tailwind/Headless UI components best match the described UI

**Important:** Items with strikethrough (`~~text~~`) are deprecated — do NOT include them
as active requirements. List them in the "Removed / Replaced" subsection of the
traceability table.

- **Version tags per item**: Each `### User Story`, `### Non Functional Requirement`,
  and `### Constraint` section contains one or more version blocks formatted as `[v1.0.x]`.
  The skill must track the version tag for each item and carry it through to the
  generated specification's traceability section.

### Input 3: Non-Functional Requirements (from PRD.md)

Within the same `PRD.md`, each module has a `### Non Functional Requirement` section.
These inform:

- UI layout choices (grid columns, card sizes, image dimensions)
- Data fetching strategies (pagination, filtering, real-time)
- Validation rules (character limits, format requirements)
- Performance constraints (lazy loading, caching)

NFRs should be mapped to specific technical decisions in the spec — for example, an NFR
stating "paginated with 10 items per page" confirms which React Query pagination pattern
to use, while "must support filtering" confirms which Zustand slice manages filter state.

### Input 4: Constraints (from PRD.md)

Within the same `PRD.md`, each module has a `### Constraint` section. These define
hard boundaries that the spec must enforce:

- Status enum values (e.g., "DRAFT, ACTIVE, EXPIRED")
- Business rules (e.g., "category must exist before creating content")
- Access control (e.g., "only ADMIN role can access user management")

Constraints are embedded directly into the relevant module blueprint — they inform
Zod validation schemas, API call parameters, and route guard configurations.

### Input 5: Module Model (from model/ folder)

Read `<app_folder>/context/model/MODEL.md` first as the index, then read the
individual module model files in each module subfolder.

**MODEL.md** provides:
- Summary table of all modules with table/collection counts and design decisions
- Links to each module's detailed model files

**Per-module files** (e.g., `model/hero-section/model.md`):
- Complete field definitions with types and constraints
- Relationships and references
- Table/collection names

**Per-module schema** (e.g., `model/hero-section/schemas.json`):
- JSON schemas defining exact field types, required fields, and validation rules

The module model directly maps to:
- TypeScript interface/type definitions (field-for-field, not placeholder)
- Zod validation schemas
- React Hook Form field configurations
- TanStack Query response type annotations
- API request/response DTOs

### Input 6: HTML Mockup Screens (from mockup/ folder)

Read `<app_folder>/context/mockup/MOCKUP.html` first as the index page, then read the
HTML files organized by role in subfolders.

**MOCKUP.html** provides:
- Application identity (name, version, short name)
- Design tokens: fonts, colors from Tailwind/CSS config or inline styles
- List of user roles and their screen sets

**Role-specific subfolders** (e.g., `mockup/admin/content/`):
- Individual HTML screens for each page in the application
- Screen layout: which components are used (tables, forms, cards, modals, grids)
- Navigation structure from sidebar/header HTML files
- Data display patterns (list pages, detail pages, create/edit forms)

**IMPORTANT — Role folders inform access control, NOT URL paths.** The role-specific
folder structure (e.g., `mockup/admin/content/hero-section.html`) determines:
1. Which role can access the page → `<ProtectedRoute requiredRoles={[Roles.ADMIN]} />`
2. Which navigation items appear for each role
It does NOT determine the URL path. The URL path is always module-based:
- `<Route path="/hero-section" />` — NOT `<Route path="/admin/hero-section" />`

The mockup screens directly map to:
- React page components (one per HTML screen)
- React Router route definitions
- Tailwind/Headless UI component selections (TanStack Table vs simple table, Headless UI
  `Dialog` vs slide-over panel, etc.)
- Form field layouts
- Navigation items per role
- Tailwind design tokens (extract colors, font, radius, spacing from the mockup CSS/config)

## PRD.md Extended Sections

Before determining optional components, check PRD.md for the following extended sections:

### Architecture Principle Extraction

If PRD.md contains an `# Architecture Principle` section, extract patterns that affect frontend decisions:

| Pattern to Extract | How It Influences the Specification |
|---|---|
| "Stateless REST API" | Confirms Axios + TanStack Query pattern for API calls |
| "Event-driven" / "WebSocket" / "real-time" | Include Socket.io client integration and real-time notification component |
| "API gateway" | Configure base URL to point to gateway rather than individual services |
| Backend framework mention | Validate API response format assumptions |

If the section is absent, proceed with existing CLAUDE.md-only detection.

### Design System Extraction

If PRD.md contains a `# Design System` section with a file reference:
1. Resolve and read the referenced file
2. Map design tokens to the Tailwind theme: extend `colors`, `fontFamily`, `borderRadius`,
   `spacing`, and `boxShadow` in `tailwind.config.js`, and seed CSS custom properties in
   `src/index.css` for light/dark token values
3. Include a complete `tailwind.config.js` in SPECIFICATION.md derived from the design system tokens

If the section is absent, derive tokens from the mockup CSS (existing behavior).

### High Level Process Flow Extraction

If PRD.md contains a `# High Level Process Flow` section:
1. Process flows with user-visible states inform which status values appear in list/table filter dropdowns
2. Process flows with real-time updates inform WebSocket subscription patterns
3. Multi-step user flows inform React Router nested route design

If the section is absent, derive UI flow from user stories only (existing behavior).

---

## Determining Optional Components

Instead of asking the user, the skill determines optional components by analyzing the
dependencies listed in `CLAUDE.md`, the `# Architecture Principle` section in PRD.md (if present),
and cross-referencing with PRD.md NFRs and constraints.

### Backend API Detection

Examine the "Depends on" list in CLAUDE.md for the target application:

| Dependency Pattern | API Configuration |
|---|---|
| References another application's REST API | `VITE_API_BASE_URL` set to that app's base URL |
| References a Spring Boot backend | Include Spring Boot CORS headers note |
| No explicit backend | Include mock API / json-server note for development |

### Authentication Detection

| Dependency / PRD Pattern | Auth Selection |
|---|---|
| References "Single Sign On" or "Keycloak" in CLAUDE.md dependencies | Auth = Keycloak |
| PRD.md has login user stories with email/password | Auth = Local (local JWT from API) |
| PRD.md constraint says "public access, no auth required" | Auth = none |
| PRD.md has only public-facing content (landing page) | Auth = none |

If Auth = Keycloak, also extract from CLAUDE.md:
- Keycloak version
- Keycloak realm: Default derived from project name
- Keycloak client ID: Default `<project-slug>-spa`
- Keycloak issuer URI: Default `http://localhost:8180/realms/<realm>`
- Keycloak roles: Infer from mockup role folders (e.g., `admin` → `ADMIN`, `editor` → `EDITOR`)

If Auth = Local (API-managed JWT):
- Login/logout handled by API calls to the backend
- JWT stored in memory (not localStorage) for XSS protection
- Axios interceptor attaches Authorization header
- Zustand auth store manages token and user info

### Optional Component Detection

| PRD.md Pattern | Component Selection |
|---|---|
| NFRs mention "grid", "sortable columns", "bulk select", "export CSV" | DataGrid = yes (TanStack Table) |
| NFRs mention "chart", "bar chart", "pie chart", "graph", "statistics" | Charts = yes (Recharts) |
| NFRs mention "date picker", "date range", "calendar" | DatePickers = yes (react-day-picker) |
| NFRs mention "real-time", "live updates", "push notification", "WebSocket" | WebSocket = yes |
| PRD.md mentions multiple languages or localization | i18n = yes |
| User stories mention "rich text", "WYSIWYG", "formatted content", "HTML content" | RichText = yes (Tiptap) |
| NFRs mention "report", "generate report", "report generation", "PDF report" | Reporting = yes |
| User stories describe generating/downloading PDF, Excel, or CSV reports | Reporting = yes |
| A "Report" module exists in PRD.md with NFRs defining a Report interface | Reporting = yes |

### Summary of Determination

After analyzing all inputs, produce a determination summary before generating the spec.
Present it to the user for confirmation:

```
Optional Component Determination:
- Backend API:    http://localhost:<port>/api (from CLAUDE.md Port Allocation table → depends on backend app)
- Authentication: Keycloak PKCE (from CLAUDE.md → depends on Single Sign On)
- DataGrid:       yes (TanStack Table — from PRD.md → NFR mentions sortable user list with bulk actions)
- Charts:         no
- DatePickers:    yes (react-day-picker — from PRD.md → hero section effective/expiration date fields)
- WebSocket:      no
- i18n:           no
- RichText:       yes (Tiptap — from PRD.md → blog content editor requires rich text)
- Reporting:      yes (from PRD.md → Report module with Report interface NFR)
```

If the user disagrees with any determination, allow them to override before proceeding.

## Required Inputs

After determination, these values are needed. Most are derived automatically:

**Auto-derived from context files:**
- **Application name**: From CLAUDE.md section heading
- **Project slug**: Kebab-case of application name
- **App title**: Title-case used in `<title>` and the topbar
- **Application description**: From CLAUDE.md description
- **Backend API base URL**: From CLAUDE.md dependencies
- **Modules / Features**: From PRD.md module headings + model/MODEL.md
- **Auth type**: Auto-determined (see above)
- **Optional components**: Auto-determined (see above)
- **User roles**: From mockup role folders
- **Design tokens**: Tailwind theme colors/fonts/radius extracted from mockup CSS/inline styles

**Auto-derived from CLAUDE.md (Port Allocation table):**
- **Backend API base URL**: Look up the backend application's port from the `Port Allocation` table in the `Custom Applications` section of `CLAUDE.md`. Construct the base URL as `http://localhost:<port>/api/v1`. Do NOT hardcode `8080` — the port MUST match the allocated port for the backend application this SPA depends on.

**Optional (use sensible defaults if not found in context):**
- **Dev server port**: Default `3000`
- **Default locale**: Default `en`
- **Page size**: Default `10` (from NFRs, or fallback)

## Generating the Specification

Once inputs are gathered from context files and optional components are determined,
generate the specification as a **multi-file output split by module**. Read the spec
template at `references/spec-template.md` for the exact structure and content of each
section. The template is the authoritative guide — follow it closely.

The specification is split into two categories:

1. **Root `SPECIFICATION.md`** — Table of Contents, shared infrastructure, Tailwind
   configuration and design tokens, routing, auth configuration, and application-level
   sections that apply across all modules.
2. **Per-module `<module-name>/SPEC.md`** — Each module gets its own folder with a
   self-contained specification covering that module's complete blueprint.

This split enables a coding agent to:
- First, scaffold the shared infrastructure from `SPECIFICATION.md`
- Then, implement each module independently by picking up its `<module>/SPEC.md`

**Important:** The generated spec must use **real module data** from the context files,
not generic placeholders. Specifically:

- **Modules** must use the actual module names from PRD.md and MODEL.md
  (e.g., `heroSection`, `productService`, `blog` — not `module1`, `module2`)
- **TypeScript types** must match the actual fields defined in the module model files,
  not placeholder `fieldOne`/`fieldTwo`
- **API hooks** must expose functions matching the actual user stories (e.g., if a story
  says "view list of hero sections", the hook needs `useHeroSections()`)
- **Page components** must map to the actual mockup screens (e.g., if
  `admin/content/hero_section.html` exists, there must be a matching route and page
  component). The route path is module-based (e.g., `/hero-section`), NOT role-prefixed
  (e.g., NOT `/admin/hero-section`).
- **Form fields** must match what the mockup screens display
- **Zod schemas** must enforce the constraints from PRD.md (character limits, URL format, etc.)
- **Tailwind theme** must use the design tokens extracted from the mockup (colors, border-radius, font)
- **Version tags**: Every user story ID, NFR ID, constraint ID, and mockup screen in the
  traceability section must include its version tag (e.g., `USA000030 [v1.0.4]`).
  **ALL traceability sub-tables (User Stories, NFRs, AND Constraints) MUST include the
  `| Version |` column.**
- **Removed / Replaced items**: The traceability section must include a "Removed / Replaced"
  subsection listing deprecated items — showing the removed ID, the version that removed it,
  the replacement ID (if any), and a brief reason.

### Output Structure

```
<app_folder>/context/specification/
├── SPECIFICATION.md                    ← TOC + shared/application-level specs
├── hero-section/
│   └── SPEC.md                         ← Module blueprint for Hero Section
├── product-service/
│   └── SPEC.md                         ← Module blueprint for Product and Service
├── blog/
│   └── SPEC.md                         ← Module blueprint for Blog
├── ...                                 ← One folder per module from PRD.md
```

### What Goes in `SPECIFICATION.md` (Root)

The root file contains the TOC and all shared/application-level sections. These are
sections a coding agent implements **first** before any module work:

#### 1. Project Overview
Project metadata, application description, technology stack summary, user roles, module
index table linking to each module's SPEC.md.

#### 2. Package Configuration
Complete `package.json` with all dependencies (core + selected conditional), npm scripts
(`dev`, `build`, `preview`, `lint`, `type-check`), and Vite configuration.

#### 3. Application Configuration
Vite `vite.config.ts` (with proxy for backend API), TypeScript `tsconfig.json`, ESLint
config, Tailwind `tailwind.config.js`, `postcss.config.js`, and `src/index.css`
(Tailwind directives + design-token CSS variables). All environment-sensitive values use
`VITE_` prefix in environment files.

#### 3a. Application Version Configuration
The application MUST include a version value exposed via Vite environment variable with a
default derived from the version argument provided during skill invocation. If multiple
versions were provided, use the highest one.

In `.env.development` and `.env.production`:
```properties
VITE_APP_VERSION=1.0.3
```

The application MUST expose this version in the **footer** of the layout. The shared layout
component (e.g., `src/shared/layouts/Footer.tsx`) must read `import.meta.env.VITE_APP_VERSION`
and render it as: `v{version}` (e.g., `v1.0.3`).

The `package.json` `version` field MUST also be set to the version value (e.g., `1.0.3`).

#### 3b. `.env.development` File Generation from ENVIRONMENT.md
Generate `.env.development` and `.env.production` files at the project root.
The `.env.development` file is populated by reading the project-root credential file,
mapping credential and platform values to `VITE_`-prefixed environment variable names.
The `.env.production` file uses placeholder values for production deployment.

**Credential source resolution:** Read `ENVIRONMENT.md` from the project root — this is the
canonical per-developer credential/platform file generated by `util-projectinit` and
referenced from `CLAUDE.md` (e.g., `See [ENVIRONMENT.md](./ENVIRONMENT.md)`). For backward
compatibility, if `ENVIRONMENT.md` is absent but a legacy `SECRET.md` exists, read that
instead. If neither exists, fall back to sensible local defaults.

**Process:**
1. Read `ENVIRONMENT.md` (or legacy `SECRET.md`) from the project root
2. Extract relevant values:
   - From `# Supporting 3rd Party Applications` → `## Keycloak` (host, HTTP port, realm,
     OIDC issuer, and the **client ID matching this application** in the Clients table) and
     any other 3rd-party service this SPA talks to directly
   - From `# External Services` → values for any external service the SPA calls directly
   - The **backend API base URL** is derived from the `# Port Allocation` table in
     `CLAUDE.md` (the port of the backend application this SPA depends on), NOT from a
     hardcoded port — construct `http://localhost:<port>/api/v1`
3. Map each value to the corresponding `VITE_` environment variable name
4. Generate `.env.development` with actual local values
5. Generate `.env.production` with production placeholder values

**Example `.env.development` output (derived from ENVIRONMENT.md + CLAUDE.md Port Allocation):**
```properties
# Backend API (port from CLAUDE.md Port Allocation table for the backend app this SPA depends on)
VITE_API_BASE_URL=http://localhost:8001/api/v1

# Authentication (Keycloak) — host/port/realm/issuer + the client ID for THIS app
VITE_KEYCLOAK_AUTHORITY=http://127.0.0.1:8180/realms/skf
VITE_KEYCLOAK_CLIENT_ID=skolafund-web
VITE_KEYCLOAK_REDIRECT_URI=http://localhost:3000/auth/callback
```

**Rules:**
- Only include variables that are actually used in the application code via `import.meta.env`
- Use actual values from `ENVIRONMENT.md` — never use placeholders or `TODO`
- Match the **client ID** to this application's row in the Keycloak Clients table (e.g., a
  "School Web" SPA uses client `school-web`), not a generic guess
- If `ENVIRONMENT.md` does not exist or a value is not found, use sensible defaults for local
  development (e.g., `localhost`, default ports)
- Both `.env.development` and `.env.production` are gitignored

#### 4. Directory Structure
The complete source tree under `src/`. The structure follows feature-based architecture
where each PRD module maps to a `src/features/<module>/` folder.
Read `references/routing-patterns.md` for the module folder layout.

#### 5. Tailwind Configuration & Design Tokens
Custom Tailwind theme built from design tokens extracted from mockup screens. Includes:
- `tailwind.config.js` — `darkMode: 'class'`, `content` globs, `theme.extend` with the
  color palette (primary, secondary, danger, warning, success, neutral), font family,
  border-radius, and box-shadow tokens; `plugins: [forms, typography (if RichText)]`
- `src/index.css` — `@tailwind base/components/utilities` directives plus `:root` and
  `.dark` CSS custom properties for semantic tokens
- `src/lib/utils/cn.ts` — the `cn()` helper (`twMerge(clsx(...))`)
- Design token mapping table showing mockup CSS property → Tailwind token
Read `references/component-patterns.md` for the theme/token setup pattern.

#### 6. Authentication Configuration *(conditional — include only if Auth != none)*
**If Auth = Keycloak:** PKCE Authorization Code flow using `oidc-client-ts` +
`react-oidc-context`. `AuthProvider` wraps the app, `useAuthUser()` hook exposes user and
tokens, Axios interceptor attaches Bearer token, protected route component checks
authentication. Read `references/security-patterns.md` for the full auth architecture.

**If Auth = Local (API JWT):** Login form submits to backend API, JWT stored in Zustand
auth store (memory only, not localStorage), Axios interceptor attaches Authorization
header, token refresh interceptor handles 401 responses, protected route component
redirects unauthenticated users.

#### 7. Router Configuration
React Router v7 route tree — lazy-loaded page components, protected routes with role
guards, public routes, 404 fallback.
Read `references/routing-patterns.md` for route patterns.

#### 8. API Client Configuration
Axios instance with `baseURL` from `VITE_API_BASE_URL`, request/response interceptors
for auth token injection, global error handling (toast notifications for 4xx/5xx),
request timeout.

#### 9. Global State (Zustand)
App-level Zustand stores: auth store (user info, token, login/logout actions), UI store
(sidebar open/closed, theme mode, global loading). Feature-level stores defined in each
module's SPEC.md.

#### 10. TanStack Query Setup
`QueryClient` configuration with sensible defaults (staleTime, gcTime, retry logic),
`QueryClientProvider` wrapping the app, React Query DevTools for development,
global error handler for failed queries.

#### 11. Shared Layouts
`DashboardLayout` (sidebar navigation + topbar + content area for authenticated pages),
`PublicLayout` (minimal header/footer for public pages), `AuthLayout` (centered card
for login/callback pages). Each layout is built with Tailwind utility classes.

#### 12. Shared Components
Reusable Tailwind/Headless UI components used across multiple modules: `Button`, `Card`,
`PageHeader`, `DataTable` (wrapper around TanStack Table or a simple Tailwind table),
`ConfirmDialog` (Headless UI `Dialog`), `StatusBadge`, `Modal`/`FormDialog`,
`ImageUpload`, `LoadingOverlay`/`Spinner`, `EmptyState`, `ErrorBoundary`, `SearchInput`,
`FilterBar`, `Pagination`. Each with TypeScript props interface.

#### 13. Navigation Configuration
Sidebar navigation items derived from mockup sidebar files, organized by role. Each item
has label, icon (Heroicons component), path, and required role. Navigation is rendered
dynamically based on the authenticated user's roles.

#### 14. Form Infrastructure
`FormProvider` usage pattern from React Hook Form, Zod schema integration via
`zodResolver`, reusable controlled input components (`TextFieldController`,
`TextAreaController`, `SelectController` (Headless UI `Listbox`), `DatePickerController`
(react-day-picker), `SwitchController` (Headless UI `Switch`), `ComboboxController`
(Headless UI `Combobox`)) that wrap Tailwind-styled inputs with RHF `Controller`.

#### 15. Error Handling Strategy
React `ErrorBoundary` component for rendering errors, Axios response interceptor for
API errors, TanStack Query `onError` callback for query failures, Zod validation error
message extraction utility, toast notifications for user-facing error messages.

#### 16. Notification System
Headless UI `Transition`-animated toast stack styled with Tailwind. Zustand notification
store with `push(type, message)` and `dismiss(id)` actions. `NotificationProvider` renders
the active queue in a fixed viewport corner.

#### 17. Theming & Dark Mode
Tailwind `darkMode: 'class'` strategy. Theme mode (`light`/`dark`) toggled via UI
control, persisted to `localStorage` through the Zustand UI store. An effect syncs the
`dark` class on `document.documentElement`. `useColorMode()` (or the UI store) wraps the
toggle action. Semantic colors are defined as CSS variables in `src/index.css` for both modes.

#### 18. Testing Strategy
Overview: Vitest + React Testing Library for unit/component tests, MSW (Mock Service
Worker) for API mocking in tests, Playwright for E2E tests. Per-feature test conventions
matching the module spec.

#### 19. Build & Deployment
Vite production build (`npm run build`), chunk splitting strategy (vendor chunk, per-
feature lazy chunks), environment variable injection, static hosting notes (nginx config
for SPA routing).

#### 20. Internationalisation *(conditional — include only if i18n = yes)*
`react-i18next` setup, `I18nextProvider` wrapping the app, lazy-loaded translation
namespaces per module (e.g., `heroSection.json`), `useTranslation()` hook usage pattern,
language switcher component (Headless UI `Menu`).

#### 21. WebSocket Integration *(conditional — include only if WebSocket = yes)*
`socket.io-client` setup, connection management Zustand store, custom `useSocket()`
hook, event subscription patterns, reconnection handling.

#### 22. Reporting (Puppeteer) *(conditional — include only if Reporting = yes)*
Client-side report UI components and server-side Puppeteer PDF generation service.
Includes report list page (Tailwind card grid grouped by domain), report parameter
form page (React Hook Form + Zod + Tailwind/Headless UI controls), report preview dialog
(iframe-based HTML preview in a Headless UI `Dialog`), `useReportGeneration()` hook
orchestrating PDF/XLSX/CSV generation, `renderReportHtml()` utility using
`ReactDOMServer.renderToStaticMarkup()` to produce self-contained HTML with Tailwind CDN
for Puppeteer rendering, report layout components (React components rendering
tabular/summary reports as HTML), client-side XLSX export via `xlsx` library, client-side
CSV export via `PapaParse`, lightweight Node.js Express report service using Puppeteer for
HTML-to-PDF conversion (deployed as sidecar or microservice), Vite proxy configuration for
development. Report layouts are fully AI-agent-developed React components — no visual
designers needed. Read `references/reporting-patterns.md` for the full reporting
architecture.

### What Goes in Each `<module>/SPEC.md` (Per-Module)

For EACH module from PRD.md and MODEL.md, create a folder named after the module
(kebab-case, e.g., `hero-section/`) and generate a `SPEC.md` inside it.

Each module `SPEC.md` is a **self-contained** blueprint that a coding agent can pick up
and implement independently (after the shared infrastructure is in place). It must include:

- **Header** with module name and back-reference to root `SPECIFICATION.md`
- **Traceability**: User story IDs, NFR IDs, constraint IDs, table/collection names,
  mockup screen filenames, all with version tags
- **TypeScript Types** — interfaces/types matching the module model fields (field-for-field)
- **Zod Schemas** — validation schemas for create/update forms, derived from PRD constraints
- **API Functions** — Axios-based API calls matching user story data operations
- **TanStack Query Hooks** — `useQuery` and `useMutation` hooks wrapping API functions
- **Zustand Feature Store** (if the module has complex client state beyond server cache)
- **Page Components** — one per mockup screen, using Tailwind/Headless UI components matching the mockup layout
- **Form Components** — create/edit forms with React Hook Form + Zod + Tailwind controllers
- **Route Definitions** — React Router routes for this module
- **Navigation Items** — sidebar nav entries for each role that can access this module
- **Complete code samples** for every component — continuous and copy-pasteable

See `references/spec-template.md` for the exact per-module template structure.

## Changelog Append

After all specification files are successfully generated, append an entry to `CHANGELOG.md` in the application folder (`<app_folder>/CHANGELOG.md`):

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
5. Row format: `| {YYYY-MM-DD} | {application_name} | specgen-react-tailwind | {module or "All"} | Generated React + Tailwind SPA technical specification |`
6. **Never modify or delete existing rows.**

## Output Format

The generated specification is a **folder of files**, not a single document:

```
<app_folder>/context/specification/
├── SPECIFICATION.md                    ← Root: TOC + shared/application-level specs
├── <module-1>/
│   └── SPEC.md                         ← Module blueprint (self-contained)
├── <module-2>/
│   └── SPEC.md
├── <module-N>/
│   └── SPEC.md
```

## Constraints (Non-Negotiable)

These constraints apply to every code sample in the generated spec:

**TypeScript everywhere.** All files use `.tsx` or `.ts` extensions. No `.js` or `.jsx`
(except `tailwind.config.js` / `postcss.config.js`, which are config files). No `any`
type — use `unknown` with type narrowing, or proper type inference.

**Feature-based architecture.** Every module maps to `src/features/<module>/`. Nothing
module-specific leaks into `src/shared/` or `src/lib/`. Shared utilities must be
genuinely reusable across at least two modules.

**No localStorage for tokens.** JWT access tokens are stored in Zustand memory store
only. Refresh tokens may use `httpOnly` cookies (handled by backend). This prevents XSS
token theft.

**TanStack Query for all server state.** Do not use Zustand or component state to cache
API responses. TanStack Query manages all server-side data (fetching, caching, invalidation).
Zustand manages only client-side UI state (filters, selections, modal open/closed).

**React Hook Form + Zod for all forms.** Do not use uncontrolled inputs or manual
`useState` for form fields. Every form uses `useForm()` with `zodResolver()`.

**Tailwind utility-first, Headless UI for interactivity.** Style everything with Tailwind
utility classes. Do NOT introduce a component framework (MUI, Ant Design, Chakra, Bootstrap).
For interactive/accessible widgets that need focus management, keyboard nav, or ARIA
(modals, dropdowns, comboboxes, listboxes, switches, tabs, popovers, transitions), use
**Headless UI** primitives. For icons, use **Heroicons** (`@heroicons/react/24/outline`
and `/24/solid`). Do not embed inline SVG or icon CDNs.

**Compose classes with `cn()`.** Use the `cn()` helper (`tailwind-merge` over `clsx`) for
all conditional/merged className logic. Never concatenate class strings manually with
template literals where conflicts could arise.

**Variants via `cva`.** Components with multiple visual variants (Button, Badge, Alert)
define their classes with `class-variance-authority` and expose typed `variant`/`size` props.

**Dark mode via the `class` strategy.** Use Tailwind `dark:` variants. The `dark` class is
toggled on `document.documentElement` from the Zustand UI store; the preference persists to
`localStorage`. Never hardcode light-only colors — always provide a `dark:` counterpart for
backgrounds, text, and borders.

**Named exports for components.** Use named exports (not default exports) for all
component files to improve tree-shaking and refactoring.

**Lazy loading for all page components.** All route page components use `React.lazy()`
for code splitting. The router uses `<Suspense>` with a loading fallback.

**Consistent file naming:**
- Components: `PascalCase.tsx` (e.g., `HeroSectionList.tsx`)
- Hooks: `camelCase.ts` with `use` prefix (e.g., `useHeroSections.ts`)
- API functions: `camelCase.ts` (e.g., `heroSectionApi.ts`)
- Types: `camelCase.types.ts` (e.g., `heroSection.types.ts`)
- Zod schemas: `camelCase.schema.ts` (e.g., `heroSection.schema.ts`)
- Zustand stores: `camelCase.store.ts` (e.g., `heroSection.store.ts`)
