---
name: specgen-laravel-eloquent-bladehtmx
model: claude-opus-4-8
effort: high
description: >
  Generate a detailed specification document for building a monolith Laravel 12 web
  application with server-rendered views (Blade), Tailwind CSS, Alpine.js, htmx, and
  nwidart/laravel-modules modular packaging. Database (MongoDB, PostgreSQL, MySQL, or none),
  authentication (Keycloak OAuth2 Client, Laravel Breeze form login, or none), scheduling
  (Laravel Task Scheduling + Queue Batching or none), messaging (RabbitMQ pub/sub or
  none), and internationalisation (multi-locale via Laravel's native translation system,
  or none) are configurable based on user input.
  Standardized input: application name (mandatory), version (mandatory), module (optional).
  Use this skill whenever the user asks to create a spec, specification, blueprint, or
  technical design document for a new Laravel web application with server-side rendering.
  Also trigger when the user says things like "spec out a new Laravel project",
  "design a Laravel web skeleton", "write a technical spec for my new Laravel app",
  "scaffold spec for a monolith Laravel app", or any request for a specification document
  describing a Laravel + Blade + Tailwind application. Even if the user only mentions
  a subset of the stack (e.g., "Laravel web app" or "Laravel with Mongo" or
  "Laravel with Keycloak"), this skill likely applies â€” ask and confirm.
---

# Laravel Web Application Specification Generator

This skill generates a comprehensive specification document (Markdown) that serves as a
blueprint for building a monolith Laravel 12 web application with server-rendered
views. The spec is intended to be followed by a developer or a coding agent to produce
a fully functional project scaffold.

The specification does NOT generate code. It produces a detailed, opinionated technical
document describing every layer of the application â€” from Composer configuration to Blade
layouts to middleware chains â€” so that implementation becomes a mechanical exercise.

## Technology Stack

### Core Stack (Always Included)

These are the fixed versions the spec targets. Do not deviate unless the user explicitly
requests different versions.

| Component          | Version   |
|--------------------|-----------|
| PHP                | 8.3+      |
| Laravel            | 12.x      |
| Composer           | 2.x       |
| Blade              | Built-in  |
| Tailwind CSS       | 4.x       |
| Alpine.js          | 3.x       |
| htmx               | 2.x       |
| Vite               | 6.x       |
| Node.js            | 22.x LTS  |

### Optional Integration Versions

Include in the version table only when the corresponding integration is selected.

| Component          | Version   | When Selected        |
|--------------------|-----------|----------------------|
| MongoDB            | 8.0.x     | Database = MongoDB   |
| PostgreSQL         | 17.x      | Database = PostgreSQL|
| MySQL              | 8.4.x     | Database = MySQL     |
| Keycloak           | 26.5.x    | Auth = Keycloak      |
| RabbitMQ           | 4.x       | Messaging = yes OR Queue driver = rabbitmq |

## Core Dependencies (composer.json)

The spec must include these in the Composer configuration section (always):

- `laravel/framework` â€” Core framework
- `nwidart/laravel-modules` â€” Modular architecture
- `spatie/laravel-data` â€” Typed DTOs with transformation and validation
- `laravel-vite-plugin` â€” Vite integration (npm)

### Conditional Dependencies

**If Database = MongoDB:**
- `mongodb/laravel-mongodb` â€” Official MongoDB Eloquent driver

**If Database = PostgreSQL or MySQL:**
- Built-in Eloquent ORM + PDO driver (no extra package needed)
- Laravel Migrations (built-in) for schema management

**If Auth = Keycloak:**
- `laravel/socialite` â€” OAuth2 abstraction
- `socialiteproviders/keycloak` â€” Keycloak OAuth2 provider

**If Auth = Laravel Breeze (form login):**
- `laravel/breeze` â€” Simple authentication scaffolding

**If Scheduling = yes:**
- Built-in Laravel Task Scheduling (`Illuminate\Console\Scheduling`)

**If Scheduling = yes AND Batch Processing = yes:**
- Built-in `Illuminate\Bus\Batch` (Bus::batch())

**If Messaging = yes:**
- `vladimir-yuldashev/laravel-queue-rabbitmq` â€” RabbitMQ queue driver
- `php-amqplib/php-amqplib` â€” Low-level AMQP for advanced exchange patterns

**If i18n = yes:**
- No extra package â€” uses Laravel's **built-in localization** (`lang/` directory, `__()` /
  `trans()` / `@lang` helpers, `trans_choice()` for pluralization, `app()->setLocale()`).
- Locale is resolved per request by a custom `SetLocale` middleware (session â†’ cookie â†’
  `Accept-Language` header â†’ configured default).
- Each module contributes its own translation namespace via its module service provider
  (`loadTranslationsFrom()`), keeping module strings self-contained.

**If Reporting = yes:**
- `spatie/browsershot` â€” PDF generation via Puppeteer (headless Chrome) with full CSS support
- `maatwebsite/excel` â€” XLSX and CSV export
- Requires `npm install puppeteer` on the server (Node.js + headless Chrome binary)

**Additional cross-cutting packages:**
- `spatie/laravel-permission` â€” RBAC (roles and permissions)
- `owen-it/laravel-auditing` â€” Audit trail (created_by, updated_by, field change history)
- `spatie/laravel-health` â€” Health check endpoints
- `spatie/laravel-view-models` â€” Typed view models for Blade templates

## When the Skill Triggers

Generate the spec when the user provides an **application name** and **version** that
corresponds to one of the custom applications defined in `CLAUDE.md`. The skill
reads all required inputs from the project's context files â€” no interactive Q&A is needed
for the core inputs.

The user invokes this skill by specifying the target application and version, for example:
- `/specgen-laravel-eloquent-bladehtmx hub_middleware v1.0.3`
- `/specgen-laravel-eloquent-bladehtmx hub_middleware v1.0.3 module:Location Information`
- `/specgen-laravel-eloquent-bladehtmx "Hub Middleware" v1.0.3`

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
| `<application>` | Yes | `hub_middleware` | Application name to locate the context folder |
| `<version>` | Yes | `v1.0.3` | Version to scope processing |
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
| HTML Mockups | `<app_folder>/context/mockup/` |
| Output (specification) | `<app_folder>/context/specification/` |

### Example Invocations

- `/specgen-laravel-eloquent-bladehtmx hub_middleware v1.0.3` (all modules)
- `/specgen-laravel-eloquent-bladehtmx hub_middleware v1.0.3 module:Location Information` (one module)
- `/specgen-laravel-eloquent-bladehtmx "Hub Middleware" v1.0.3`

### Version Filtering

When a version is provided, only include user stories, NFRs, and constraints from versions
<= the provided version. For example, if `v1.0.3` is specified:
- Include items tagged `[v1.0.0]`, `[v1.0.1]`, `[v1.0.2]`, `[v1.0.3]`
- Exclude items tagged `[v1.0.4]` or later
- Version comparison uses semantic versioning order

### Module Filtering

When `module:<name>` is provided:
- Only generate the `SPEC.md` for that specific module
- Other existing module spec files remain untouched
- `SPECIFICATION.md` (root) gets a partial update â€” only that module's entry in the TOC
  is added or updated; all other TOC entries are preserved as-is

## Gathering Input

The specification is driven by **six input sources** that are read from the project's
context files. The skill does NOT ask the user for database, authentication, scheduling,
or messaging choices â€” it **determines** these automatically from the context.

### Input 1: Application Name (from CLAUDE.md)

From CLAUDE.md (already loaded in context), locate the target application under the **Custom Applications**
section. Extract:

- **Application name**: The section heading (e.g., "Hub Middleware", "HC Adapter")
- **Application description**: The description paragraph below the heading
- **Dependencies**: The "Depends on" list â€” this is the primary source for determining
  optional components (see [Determining Optional Components](#determining-optional-components))

The application name is used to derive:
- **Project slug**: Kebab-case of the application name (e.g., `hub-middleware`)
- **Namespace root**: `App\Modules` (for nwidart/laravel-modules) or `App` (for core)

### Input 2: User Stories (from PRD.md)

Read `<app_folder>/context/PRD.md`. This file contains all user stories
organized by module. Extract:

- **System modules**: Modules under the `# System Module` heading (e.g., User, Notification,
  Activities, Audit Trail). These become system-level modules in the spec.
- **Business modules**: Modules under the `# Business Module` heading (e.g., Location
  Information, Corridor, Employer). These become business-level modules.
- **User stories per module**: Each `### User Story` section contains tagged items like
  `[USHM00108] As a user, I want to...`. These define the functional requirements for
  each module's service interface and page controllers.

The user stories directly inform:
- Which CRUD operations each module's service must expose
- Which controllers and Blade views are needed
- Which form fields and validation rules apply

**Important:** Items with strikethrough (`~~text~~`) are deprecated â€” do NOT include them
as active requirements. Instead, list them in the "Removed / Replaced" subsection of the
traceability table (see spec-template.md) so that developers can see what was removed and
which version removed it. If a deprecated item has a replacement (e.g., `USHM00015` replaced
by `USHM00222`), note the replacement ID.

- **Version tags per item**: Each `### User Story`, `### Non Functional Requirement`,
  and `### Constraint` section contains one or more version blocks formatted as `[v1.0.x]`.
  Items listed under each version tag belong to that version. The skill must track the
  version tag for each item (user story, NFR, constraint) and carry it through to the
  generated specification's traceability section. When a version block explicitly lists
  "Removed ... from previous version", record those removals in a "Removed / Replaced"
  subsection with the version that removed them and the replacement ID (if any).

### Input 3: Non-Functional Requirements (from PRD.md)

Within the same `PRD.md`, each module has a `### Non Functional Requirement` section
with tagged items like `[NFRHM0120]`. These inform:

- Data storage strategies (e.g., "stored in JWT token", "stored in the database")
- Integration patterns (e.g., "API call to SSO service", "sent asynchronously")
- Performance constraints (e.g., "automatically deleted after 30 days")
- Security requirements (e.g., "require user to relogin")

NFRs should be mapped to specific technical decisions in the spec â€” for example, an NFR
stating "stored in JWT token" confirms stateless auth, while "sent asynchronously" confirms
event-driven processing.

### Input 4: Constraints (from PRD.md)

Within the same `PRD.md`, each module has a `### Constraint` section with tagged
items like `[CONSHM042]`. These define hard boundaries that the spec must enforce:

- Field-level restrictions (e.g., "can only change name and phone number")
- Feature boundaries (e.g., "only 2 delivery channels supported")
- Scope limitations (e.g., "does not manage any user, permissions and roles")

Constraints are embedded directly into the relevant module blueprint â€” they inform
service interface contracts, validation rules, and UI form configurations.

### Input 5: Module Model (from model/ folder)

Read `<app_folder>/context/model/MODEL.md` first as the index, then read the
individual module model files in each module subfolder.

**MODEL.md** provides:
- Summary table of all modules with collection/table counts and design decisions
- Links to each module's detailed model files

**Per-module files** (e.g., `model/location-information/model.md`):
- Complete field definitions with types and constraints
- Embedded vs. referenced relationships
- Collection/table names
- Index specifications
- Audit field patterns

**Per-module schema** (e.g., `model/location-information/schemas.json`):
- JSON schemas defining exact field types, required fields, and validation rules

**Per-module diagram** (e.g., `model/location-information/document-model.mermaid`):
- Visual representation of data structure and relationships

The module model directly maps to:
- Eloquent Models (field-for-field, not placeholder)
- Migration scripts (for SQL databases)
- Repository/query patterns
- spatie/laravel-data DTO structures matching the actual module fields
- Service interface method signatures

- **Version tracking**: The MODEL.md summary table includes a "Versions" column listing
  which versions each module participates in (e.g., "1.0.0, 1.0.1, 1.0.3"). Per-module
  model.md files may also include version annotations on fields and indexes. The skill
  must carry these version tags into the generated specification.

### Input 6: HTML Mockup Screens (from mockup/ folder)

Read `<app_folder>/context/mockup/MOCKUP.html` first as the index page, then
read the HTML files organized by role in subfolders.

**MOCKUP.html** provides:
- Application identity (name, version, short name)
- Design tokens: fonts, colors, spacing from Tailwind config
- List of user roles and their screen sets
- Setup instructions for the shared Mockup Hub (`<root>/mockup`)

**Role-specific subfolders** (e.g., `mockup/hub_administrator/content/`):
- Individual HTML screens for each page in the application
- Screen layout: which components are used (tables, forms, cards, tabs, modals)
- Navigation structure from sidebar HTML files
- Data display patterns (list pages, detail pages, create/edit forms)

**IMPORTANT â€” Role folders inform access control, NOT URL paths.** The role-specific
folder structure (e.g., `mockup/hub_administrator/content/corridor.html`) determines:
1. Which role can access the page â†’ `middleware('role:hub_administrator')`
2. Which sidebar navigation items appear for each role
It does NOT determine the URL path. The URL path is always module-based:
- `Route::get('/corridor', ...)` â€” NOT `Route::get('/hub_administrator/corridor', ...)`
- Fragment URL: `Route::get('/corridor/fragments/...', ...)` â€” NOT role-prefixed

**Shared partials** (e.g., `mockup/partials/`):
- `header.html` â€” Header bar layout and elements
- `footer.html` â€” Footer layout
- `sidebar-<role>.html` â€” Per-role navigation menus
- `shell.html` â€” Page shell/wrapper structure

The mockup screens directly map to:
- Blade page templates (one per HTML screen)
- Blade partial templates (for htmx partial updates)
- Controller endpoints (one per screen)
- View model classes (with fields matching the data shown in each screen)
- Sidebar navigation items per role
- Form field layouts and validation display
- Design tokens for Tailwind configuration (colors, fonts from MOCKUP.html)

- **Version tracking**: The MOCKUP.html index page shows a version tag on each screen
  card (e.g., `v1.0.0`, `v1.0.3`). Individual mockup screens may include version
  annotations. The skill must associate each mockup screen with its version and carry
  this through to the generated specification.

## PRD.md Extended Sections

Before determining optional components, check PRD.md for the following extended sections and extract their content for use throughout specification generation:

### Architecture Principle Extraction

If PRD.md contains an `# Architecture Principle` section, read it and extract architectural patterns as a structured context object. These patterns serve as **primary signals** for optional component determination and specification content:

| Pattern to Extract | How It Influences the Specification |
|---|---|
| Framework mention (e.g., "Laravel") | Validates technology stack choice |
| "Monolithic" / "modular architecture" | Validates nwidart/laravel-modules structure; inter-module via Laravel events |
| "Stateless" | Confirms no server-side session â€” JWT/OAuth2 token-based auth |
| "Event-driven" | Map to Laravel Event Broadcasting and Event Listeners; include event catalog |
| "Message driven" / "message queue" | Map to Laravel Queue Jobs; validate RabbitMQ integration |
| "Document based database" / "MongoDB" | Primary signal for Database = MongoDB |
| "Container based deployment" | Confirms `.env` environment variable configuration |

If the section is absent, proceed with existing CLAUDE.md-only detection.

### Design System Extraction

If PRD.md contains a `# Design System` section with a file reference (e.g., `[DESIGN_SYSTEM.md](reference/DESIGN_SYSTEM.md)`):
1. Resolve the path relative to PRD.md and read the referenced file
2. Extract design tokens: color palettes, typography, component patterns
3. Include a "Design System Integration" subsection in SPECIFICATION.md specifying:
   - Tailwind CSS custom theme configuration (colors, fonts)
   - Blade layout template design token variables
   - CSS variable definitions
4. In per-module SPEC.md, reference which design tokens apply to specific components

If the section is absent, use design tokens from MOCKUP.html Tailwind config (existing behavior).

### High Level Process Flow Extraction

If PRD.md contains a `# High Level Process Flow` section:
1. Parse all named process flows and their ordered steps
2. Each process flow is an **authoritative source** for messaging pipeline sections in per-module SPEC.md:
   - Each step maps to a Laravel Queue Job, Event Listener, or Controller method
   - Error paths generate corresponding exception handlers and failed job configurations
   - ACK/NACK patterns become outbound message publisher specifications
3. Include a "Process Flow Implementation" subsection in each affected module's SPEC.md mapping flow steps to service methods
4. Generate an event catalog in SPECIFICATION.md listing all domain events from process flows

If the section is absent, derive messaging patterns from NFRs only (existing behavior).

---

## Determining Optional Components

Instead of asking the user, the skill determines optional components by analyzing the
dependencies listed in `CLAUDE.md`, the `# Architecture Principle` section in PRD.md (if present),
and cross-referencing with PRD.md NFRs and constraints.

### Database Detection

**First check PRD.md `# Architecture Principle`**: If it explicitly mentions a database type (e.g., "document based database", "MongoDB", "relational database", "MySQL"), use that as the primary signal.

**Fallback to CLAUDE.md**: Examine the "Depends on" list in CLAUDE.md for the target application:

| Dependency Pattern | Database Selection |
|---|---|
| References "Hub Database" (MongoDB) | Database = MongoDB |
| References "HC Database" or "SC Database" (MySQL) | Database = MySQL |
| No database dependency listed | Database = none |

Also check `CLAUDE.md`'s database section for the exact database name, and read
`ENVIRONMENT.md` (in the project root) for host, port, and credentials to use in the
spec's application configuration.

### Authentication Detection

| Dependency Pattern | Auth Selection |
|---|---|
| References "Hub Single Sign On" (Keycloak) | Auth = Keycloak |
| PRD.md constraint says "does not manage any user, permissions and roles" | Auth = none |
| PRD.md NFRs reference "SSO service" or "JWT token" | Auth = Keycloak |
| No SSO/Keycloak dependency but has user management stories | Auth = form |

If Auth = Keycloak, also extract from CLAUDE.md:
- Keycloak version from "Hub Single Sign On" section
- Keycloak realm: Default derived from project name
- Keycloak client ID: Default `<project-slug>-web`
- Keycloak issuer URI: Default `http://localhost:8180/realms/<realm>`
- Keycloak roles: Infer from mockup sidebar roles (e.g., `hub_administrator` â†’ `HUB_ADMINISTRATOR`)

### Messaging Detection

| Dependency Pattern | Messaging Selection |
|---|---|
| References "Hub to HC Adapter Message Queue" or "Hub to SC Adapter Message Queue" (RabbitMQ) | Messaging = yes |
| No message queue dependency listed | Messaging = no |

If Messaging = yes, also extract the RabbitMQ version from the corresponding message
queue section in CLAUDE.md.

### Scheduling Detection

Scheduling is determined from PRD.md content:

| Content Pattern | Scheduling Selection |
|---|---|
| NFRs mention "automatically deleted after X days", "scheduled", "periodic", "batch processing" | Scheduling = yes |
| User stories describe recurring jobs, cleanup tasks, or time-triggered operations | Scheduling = yes |
| No scheduling-related requirements found | Scheduling = no |

**If Scheduling = yes**, further determine:
- **Batch Processing = yes** if NFRs mention "batch processing", "ETL", "bulk import/export",
  or processing large volumes of data with reader/processor/writer patterns

### Reporting Detection

Reporting is determined from PRD.md content:

| Content Pattern | Reporting Selection |
|---|---|
| NFRs mention "report", "Report interface", "generate report", "report generation" | Reporting = yes |
| User stories describe generating/downloading PDF, Excel, or CSV reports | Reporting = yes |
| A "Report" module exists in PRD.md with NFRs defining a Report interface | Reporting = yes |
| No reporting-related requirements found | Reporting = no |

**If Reporting = yes**, the spec includes:
- Puppeteer via Browsershot for PDF generation from Blade templates (full CSS/Tailwind support)
- Laravel Excel for XLSX and CSV export
- `ReportDefinition` interface for modules to implement
- `ReportService` orchestrating render â†’ export
- Report registry persisted in the database
- Report controller with parameter form and download endpoint
- Blade templates for report list, parameter form, and PDF report layouts (Tailwind-styled)

### Internationalisation Detection

Internationalisation is determined from PRD.md content:

| Content Pattern | i18n Selection |
|---|---|
| PRD.md mentions multiple languages or localization (e.g., "English and Bahasa Malaysia", "multilingual", "support multiple locales") | i18n = yes |
| NFRs require translatable UI, locale-specific date/number formatting, or a language switcher | i18n = yes |
| User stories describe choosing/switching the interface language | i18n = yes |
| No language/localization requirements found | i18n = no |

**If i18n = yes**, the spec includes:
- `config/app.php` `locale` / `fallback_locale` + an `app.supported_locales` list
- A `SetLocale` middleware (session â†’ cookie â†’ `Accept-Language` â†’ default) registered on the web group
- Per-locale translation files (`lang/<locale>/...`) plus per-module translation namespaces
- A locale-switch route/controller persisting the choice to session + cookie
- A language switcher partial (Alpine.js dropdown in the header)
- Localized validation messages (`lang/<locale>/validation.php`)

**If i18n = no**, do NOT generate a locale/language switcher or any translation scaffolding â€”
Blade templates use literal copy. Never add a non-functional language switcher "for future use".

### Summary of Determination

After analyzing all inputs, produce a determination summary before generating the spec.
Present it to the user for confirmation:

```
Optional Component Determination:
- Database:      MongoDB (from CLAUDE.md â†’ depends on Hub Database)
- Authentication: Keycloak (from CLAUDE.md â†’ depends on Hub Single Sign On)
- Scheduling:    yes (from PRD.md â†’ NFR mentions automatic deletion)
  - Batch Processing: no
- Messaging:     yes (from CLAUDE.md â†’ depends on Hub to HC/SC Adapter Message Queue)
- Reporting:     yes (from PRD.md â†’ Report module with Report interface NFR)
- Internationalisation: yes (en, ms) (from PRD.md â†’ English + Bahasa Malaysia required)
```

If the user disagrees with any determination, allow them to override before proceeding.

## Required Inputs

After determination, these values are needed. Most are derived automatically:

**Auto-derived from context files:**
- **Application name**: From CLAUDE.md section heading
- **Project slug**: Kebab-case of application name
- **Namespace root**: `App` (core) / `Modules\<ModuleName>` (for modules)
- **Application description**: From CLAUDE.md description
- **Modules**: From PRD.md module headings + model/MODEL.md
- **Database**: Auto-determined (see above)
- **Authentication**: Auto-determined (see above)
- **Scheduling**: Auto-determined (see above)
- **Messaging**: Auto-determined (see above)
- **Database name/credentials**: From ENVIRONMENT.md (root-level file with local environment credentials)
- **User roles**: From mockup sidebar files
- **Design tokens**: From MOCKUP.html Tailwind config

**Auto-derived from CLAUDE.md (Port Allocation table):**
- **Server port**: Look up the application's port from the `Port Allocation` table in the `Custom Applications` section of `CLAUDE.md`. Do NOT hardcode a default â€” the port MUST match the allocated port for this application.

**Optional (use sensible defaults if not found in context):**
- **Default theme**: Default `light` (supports `light`/`dark`)
- **Log level**: Default `info` for application, `warning` for frameworks
- **Default locale**: Default `en` (only relevant if i18n = yes)
- **Supported locales**: Derived from PRD.md language requirements (e.g., `en`, `ms`); default `['en']`

## Generating the Specification

Once inputs are gathered from context files and optional components are determined,
generate the specification as a **multi-file output split by module**. Read the spec
template at `references/spec-template.md` for the exact structure and content of each
section. The template is the authoritative guide â€” follow it closely.

The specification is split into two categories:

1. **Root `SPECIFICATION.md`** â€” Contains the Table of Contents, shared infrastructure,
   and application-level sections that apply across all modules.
2. **Per-module `<module-name>/SPEC.md`** â€” Each module gets its own folder with
   a self-contained specification file covering that module's complete blueprint.

This split enables a coding agent to:
- First, scaffold the shared infrastructure from `SPECIFICATION.md`
- Then, implement each module independently by picking up its `<module>/SPEC.md`

**Important:** The generated spec must use **real module data** from the context files,
not generic placeholders. Specifically:

- **Modules** must use the actual module names from PRD.md and MODEL.md
  (e.g., `LocationInformation`, `Corridor`, `Employer` â€” not `Module1`, `Module2`)
- **Model fields** must match the actual fields defined in the module model
  files (e.g., `model/location-information/model.md`), not placeholder `field_one`/`field_two`
- **Service interfaces** must expose methods matching the actual user stories (e.g., if
  a story says "view provinces by country", the service needs `listProvincesByCountry()`)
- **Controllers** must map to the actual mockup screens (e.g., if
  `hub_administrator/content/location_information.html` exists, there must be a matching
  controller endpoint and Blade page). The controller URL is module-based (e.g.,
  `/location-information`), NOT role-prefixed (e.g., NOT `/hub_administrator/location-information`).
  The mockup's role folder determines `middleware('role:...')` annotations, not URL structure.
- **Sidebar navigation** must match the mockup sidebar files per role. Sidebar hrefs use
  module-based paths (e.g., `/corridor`, `/quota`) â€” the role determines which items
  appear in the sidebar, not the URL prefix
- **Form fields** must match what the mockup screens display
- **Design tokens** (colors, fonts) must match the MOCKUP.html Tailwind configuration
- **Version tags**: Every user story ID, NFR ID, constraint ID, and mockup screen in
  the traceability section must include its version tag (e.g., `USHM00228 [v1.0.3]`).
  This enables incremental implementation by version. **ALL traceability sub-tables
  (User Stories, NFRs, AND Constraints) MUST include the `| Version |` column.** Do not
  omit the Version column from any table â€” even if a module only has v1.0.0 items.
- **Removed / Replaced items**: The traceability section must include a "Removed / Replaced"
  subsection listing any deprecated items from previous versions â€” showing the removed ID,
  the version that removed it, the replacement ID (if any), and a brief reason. This
  ensures developers can see what was removed and understand the evolution of requirements.
  If a module has no removed items, include the subsection with `_None._` to make it
  explicit that nothing was removed.

### Output Structure

```
<app_folder>/context/specification/
â”œâ”€â”€ SPECIFICATION.md                    â† TOC + shared/application-level specs
â”œâ”€â”€ location-information/
â”‚   â””â”€â”€ SPEC.md                         â† Module blueprint for Location Information
â”œâ”€â”€ corridor/
â”‚   â””â”€â”€ SPEC.md                         â† Module blueprint for Corridor
â”œâ”€â”€ employer/
â”‚   â””â”€â”€ SPEC.md                         â† Module blueprint for Employer
â”œâ”€â”€ ...                                 â† One folder per module from PRD.md
```

### What Goes in `SPECIFICATION.md` (Root)

The root file contains the TOC and all shared/application-level sections. These are the
sections that a coding agent implements **first** before any module work:

#### 1. Project Overview
Project metadata, application description, technology stack summary, the complete
list of user roles extracted from mockup sidebar files, and the **Module Index** â€”
a table listing every module with a link to its `<module>/SPEC.md` file.

#### 2. Composer & npm Configuration
Complete `composer.json` structure with all dependencies (core + selected conditional).
Complete `package.json` with Vite, Tailwind CSS, Alpine.js, htmx, and build scripts.

#### 3. Application Configuration *(conditional content varies)*
Full `config/` files covering database connection (MongoDB URI or SQL DSN
depending on selection), auth settings (Keycloak/OAuth2 if selected, or Breeze if selected),
scheduling config (if selected), theme defaults, and logging configuration. **All
environment-sensitive values (ports, hostnames, credentials, URIs) MUST be externalized
using Laravel's `env('VAR', 'default')` helper in config files**, with sensible defaults
for local development. Production overrides via system environment variables or
`.env.production`.

#### 3a. Application Version Configuration
The application configuration MUST include a version value set via environment variable
with a default derived from the version argument provided during skill invocation. If
multiple versions were provided, use the highest one.

In `config/app.php`:
```php
'version' => env('APP_VERSION', '1.0.0'),
```

The application MUST expose this version in the **footer** of every page. The shared footer
Blade partial (`resources/views/partials/footer.blade.php`) must render
`config('app.version')` as: `v{version}` (e.g., `v1.0.3`).

The `.env` file must include `APP_VERSION={version}` with the actual version value.

The `composer.json` `version` field MUST also be set to the version value (e.g., `1.0.3`).

#### 3b. `.env` File Generation from ENVIRONMENT.md
Generate the `.env` file at the project root by reading `ENVIRONMENT.md` from the project root.
The `.env` file maps ENVIRONMENT.md credential and platform values to the environment variable
names referenced in `config/` files via `env()` calls. The spec must define the complete
`.env` content with actual values from ENVIRONMENT.md.

**Process:**
1. Read `ENVIRONMENT.md` from the project root
2. Extract credential values from `ENVIRONMENT.md` (`# Supporting 3rd Party Applications`
   for database hosts, ports, usernames, passwords, plus Keycloak/Mail/RabbitMQ); read
   toolchain paths (Node.js, PHP) from `DEVTOOL.md`
3. Map each value to the corresponding `env('VAR')` name used in Laravel config files
4. Generate the `.env` file with `KEY=value` pairs

**Example `.env` output (derived from ENVIRONMENT.md):**
```properties
APP_NAME="HC Support Portal"
APP_ENV=local
APP_DEBUG=true
APP_URL=http://localhost:<port from CLAUDE.md Port Allocation table>

# Database
DB_CONNECTION=mysql
DB_HOST=localhost
DB_PORT=3306
DB_DATABASE=hc_support_my
DB_USERNAME=root
DB_PASSWORD=B3st1n3t@2025

# Authentication (Keycloak)
KEYCLOAK_BASE_URL=http://localhost:8180
KEYCLOAK_REALM=urp
KEYCLOAK_CLIENT_ID=hc-support-portal-web
KEYCLOAK_CLIENT_SECRET=

# Mail (Mailcatcher)
MAIL_MAILER=smtp
MAIL_HOST=localhost
MAIL_PORT=1025
MAIL_USERNAME=null
MAIL_PASSWORD=null

# Messaging (RabbitMQ)
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest
```

**Rules:**
- Only include variables that are actually referenced in `config/` files via `env()` calls
- Use actual values from ENVIRONMENT.md â€” never use placeholders or `TODO`
- If ENVIRONMENT.md does not exist or a value is not found, use sensible defaults for local
  development (e.g., `localhost`, default ports)
- The `.env` file is gitignored (already covered in `.gitignore`)

#### 4. Build & Tooling
Vite configuration (`vite.config.js`), Tailwind CSS setup (using design tokens from
MOCKUP.html), PostCSS config, and `resources/` directory structure.

#### 4b. `.gitignore`
Generate a `.gitignore` file at the project root. Laravel's default `.gitignore` plus:

```
# Laravel
/vendor/
/node_modules/
/public/build/
/public/hot
/storage/*.key
.env
.env.backup
.env.production

# IDE
.idea/
*.iml
.vscode/
*.swp
*~

# OS
.DS_Store
Thumbs.db

# Testing
/coverage/
.phpunit.result.cache

# E2E
e2e/node_modules/
e2e/test-results/
e2e/playwright-report/
e2e/visual-baselines/

# Logs
*.log
storage/logs/*
!storage/logs/.gitkeep
```

**Conditional additions:**
- **If Reporting = yes:** Add compiled report cache entries if applicable

#### 5. Directory Structure
The complete directory tree rooted at the project. The structure follows
Domain-Driven Design with nwidart/laravel-modules conventions, adapted for server-rendered
web with page and fragment separation. Use actual module names from the context.
Read `references/modulith-patterns.md` for the detailed module layout and inter-module
communication rules.

#### 6. Security Configuration *(conditional â€” include only if Auth != none)*
**If Auth = Keycloak:** OAuth2 Client setup with Keycloak OIDC via Laravel Socialite,
custom `KeycloakGuard`, middleware for role extraction from OIDC ID token claims, CSP
nonce middleware, automatic redirect to Keycloak login, and public route configuration.
Session-based. Read `references/security-patterns.md` for the full security architecture.

**If Auth = form:** Laravel Breeze form login configuration, custom `UserDetailsService`
backed by the selected database, password hashing with bcrypt, role-based access control
via spatie/laravel-permission, CSRF enabled (standard for form login), and remember-me.

#### 7. Layouts (Blade)
Three layouts: `app.blade.php` (header/sidebar/footer for authenticated pages),
`auth.blade.php` (split-screen for login), `error.blade.php` (centered error display).
Each uses Blade component syntax with slots. Layout structure should match the mockup
shell/partials. *Note: If Auth = none, auth layout may be omitted or simplified.*

#### 8. Partials & Includes
Reusable Blade partials: header, sidebar, footer, theme-switcher. Sidebar must include
the actual navigation items from the mockup sidebar files, organized per role.

#### 9. UI Components (Blade + Tailwind)
Pure Tailwind CSS components (no DaisyUI): Alert, Avatar, Badge, Breadcrumb, Button,
Card, Drawer, Dropdown, FormControl/Input/Select/Textarea/Checkbox/Radio/Toggle,
Loading, Menu, Modal, Navbar, Pagination, Progress, Stats, Steps, Table, Tabs,
Toast, Tooltip. Each as an anonymous Blade component with Tailwind utility classes.

#### 10. Frontend JS Structure
Alpine.js stores (toast, modal, drawer, theme), htmx extensions (loading states, toast
errors), ES module organization, and CSP nonce integration.

#### 11. Styles
Tailwind CSS organization: base (reset, typography), components (buttons, forms, cards,
tables, modals, navigation), layouts (sidebar, navbar, footer responsive), themes
(light/dark CSS custom properties). Use the actual design tokens (colors, fonts) from
MOCKUP.html.

#### 12. Authentication Pages *(conditional â€” include only if Auth != none)*
**If Auth = Keycloak:** No custom login page needed. Middleware automatically redirects
unauthenticated users to Keycloak login. Keycloak handles the login form, social login
providers, and credential management. After successful authentication, Keycloak redirects
back with an authorization code which the app exchanges for tokens.

**If Auth = form:** Login page with email/password form, CSRF token, remember-me checkbox.
Logout endpoint. Optionally a registration page if user self-registration is desired.
Provided by Laravel Breeze scaffolding.

#### 13. Data Access *(conditional content varies)*
**If Database = MongoDB:** Eloquent models per module using `mongodb/laravel-mongodb`.
DTO mapping via `spatie/laravel-data`. Pagination via Laravel's built-in `paginate()`.
All list endpoints paginated. Use actual collection names from the module model.

**If Database = PostgreSQL/MySQL:** Eloquent models per module with standard Eloquent ORM.
Laravel Migrations for schema versioning. UUIDs via `$table->uuid('id')->primary()` or
Laravel's built-in `HasUuids` trait. DTO mapping via `spatie/laravel-data`. Pagination
via built-in `paginate()`. All list endpoints paginated. Use actual table names from the
module model.

**If Database = none:** In-memory data structures or stubs. The spec should note that a
database integration can be added later.

#### 14. Error Handling & Exceptions
Base `WebApplicationException` with status/code/userMessage. `Handler.php` returning
error pages for full requests and toast fragments for htmx requests (detected via
`request()->header('HX-Request')`).

#### 15. Theming
Light/dark theme switching via cookie. Server reads cookie via middleware and shares
`$theme` with all views. Alpine store syncs toggle with cookie and `data-theme` attribute.

#### 16. Pagination Support
Laravel's built-in `->paginate()` with custom Blade pagination component matching
the Tailwind design system.

#### 17. Logging Strategy
Laravel Log (Monolog) configuration, correlation ID middleware (from JWT if auth is
enabled, or request-scoped UUID otherwise), contextual logging via `Log::withContext()`,
per-channel log levels.

#### 18. Scheduling and Batch Processing *(conditional â€” include only if Scheduling = yes)*
Laravel Task Scheduling via `routes/console.php` with `Schedule` facade. If Batch
Processing = yes, includes `Bus::batch()` patterns with `Batchable` trait on jobs for
chunk-oriented processing. Read `references/batch-patterns.md` for the full
scaffolding spec.

#### 19. Event-Driven Architecture
Laravel Events & Listeners for inter-module communication. Event classes in module's
public namespace, listeners in internal namespace. `ShouldQueue` for async processing,
`$afterCommit = true` for post-transaction delivery. Read
`references/modulith-patterns.md` for details.

#### 20. Messaging (RabbitMQ Pub/Sub) *(conditional â€” include only if Messaging = yes)*
Standalone RabbitMQ publisher/consumer services for inter-system communication.
Topic exchange for event broadcasting, direct exchange for point-to-point commands.
Read `references/messaging-patterns.md` for the full messaging architecture.

#### 21. DTO & Data Transformation
Per-module `spatie/laravel-data` DTO conventions and mapping flow patterns (Model â†’ DTO
â†’ View, Request â†’ DTO â†’ Model).

#### 22. Testing Strategy
Overview of testing approach â€” unit tests (PHPUnit), feature tests (Laravel HTTP tests),
module isolation tests, security test utilities (Socialite fake for Keycloak, `actingAs()`
for form login), view model tests.

#### 23. Reporting (Puppeteer / Browsershot) *(conditional â€” include only if Reporting = yes)*
Puppeteer via `spatie/browsershot` for PDF generation from Blade templates with full
CSS/Tailwind support (headless Chrome rendering), Laravel Excel for XLSX/CSV export.
Includes `ReportDefinition` interface for modules to implement, `ReportService`
orchestrating HTML render â†’ Browsershot PDF conversion â†’ export, `ReportRegistry` for
auto-discovering and persisting report definitions at startup, report controller with
parameter form and download endpoint, Blade templates for report list, parameter form,
and self-contained PDF report layouts (including Tailwind CDN for standalone rendering),
multi-format export. Report Blade templates are fully AI-agent-developed â€” no visual
designers needed. Read `references/reporting-patterns.md` for the full reporting
architecture.

#### 24. Internationalisation (Localization) *(conditional â€” include only if i18n = yes)*
Laravel's built-in localization. Covers: `config/app.php` `locale`/`fallback_locale` and
the `app.supported_locales` list; a `SetLocale` middleware resolving the active locale
(session â†’ cookie â†’ `Accept-Language` header â†’ default) and calling `app()->setLocale()`,
registered on the `web` middleware group; per-locale translation files under `lang/`
(`lang/<locale>/messages.php`, `lang/<locale>/validation.php`) plus per-module translation
namespaces loaded via each module's service provider (`loadTranslationsFrom()`); a
locale-switch route + controller that validates the requested locale against the supported
list and persists it to session and a long-lived cookie (htmx-aware â€” returns `HX-Refresh`
for partial requests); a language switcher partial (Alpine.js dropdown in the header,
CSRF-protected); and Blade usage conventions (`__('messages.welcome')`, `@lang`,
`trans_choice()` for pluralization, namespaced `__('locationinformation::messages.title')`),
including locale-aware date formatting via `Carbon::setLocale()` / `->translatedFormat()`.
The language switcher is the ONLY locale UI element and MUST NOT be rendered when i18n = no.

### What Goes in Each `<module>/SPEC.md` (Per-Module)

For EACH module from PRD.md and MODEL.md, create a folder named after the
module (kebab-case, e.g., `location-information/`) and generate a `SPEC.md` inside it.

Each module `SPEC.md` is a **self-contained** blueprint that a coding agent can pick up
and implement independently (after the shared infrastructure is in place). It must include:

- **Header** with module name and a back-reference to the root `SPECIFICATION.md`
- **Traceability**: User story IDs, NFR IDs, constraint IDs, collection/table names,
  mockup screen filenames
- **Service interface** with methods derived from user stories
- **DTOs** (spatie/laravel-data) with fields matching the module model fields
- **Exception class** for module-specific errors
- **Eloquent Model** with fields from `model/<module>/model.md` and
  `model/<module>/schemas.json`
- **Migration** (for SQL databases) matching the model schema
- **Repository** (optional pattern) or direct Eloquent queries in service
- **Service implementation** with full CRUD logic
- **Page controllers** with endpoints matching mockup screens for that module
- **Fragment controllers** for htmx partial updates
- **View models** (spatie/laravel-view-models) with fields matching what mockup screens display
- **Blade templates** (list, detail, create, edit, row fragments)
- **Form Request** classes for validation
- **Translation namespace** *(only if i18n = yes)* â€” a module translation file per locale
  (e.g., `Modules/<Module>/lang/<locale>/messages.php`) registered via the module service
  provider's `loadTranslationsFrom(..., '<module-slug>')`, and Blade templates that reference
  keys through the namespace (`__('<module-slug>::messages.<key>')`) instead of literal copy
- **Complete code samples** for every component â€” continuous and copy-pasteable

**Separating UI Layer from Messaging/Async Pipeline:**

When a module has BOTH user-facing screens (user stories) AND async processing NFRs
(e.g., RabbitMQ message consumption, message validation, ACK publishing, forwarding),
the SPEC.md MUST clearly separate these into distinct sections:

1. **UI Layer sections** â€” service methods for read-only queries (search, getById,
   getHistory), page controllers, fragment controllers, Blade templates. These are driven
   by user stories (USHMxxxxx).
2. **Messaging Pipeline sections** â€” message consumer (queue job), message validator,
   ACK publisher, forward publisher, queue configuration, domain events,
   `processIncomingMessage()` service method. These are driven by NFRs (NFRHMxxxx).

This separation enables the implementation orchestrator to track and implement each
concern independently. A module may have its UI layer fully implemented while its
messaging pipeline remains pending.

See `references/spec-template.md` for the exact template structure.

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
5. Row format: `| {YYYY-MM-DD} | {application_name} | specgen-laravel-eloquent-bladehtmx | {module or "All"} | Generated Laravel web application technical specification |`
6. **Never modify or delete existing rows.**

## Output Format

The generated specification is a **folder of files**, not a single document:

```
<app_folder>/context/specification/
â”œâ”€â”€ SPECIFICATION.md                    â† Root: TOC + shared/application-level specs
â”œâ”€â”€ <module-1>/
â”‚   â””â”€â”€ SPEC.md                         â† Module blueprint (self-contained)
â”œâ”€â”€ <module-2>/
â”‚   â””â”€â”€ SPEC.md
â”œâ”€â”€ <module-N>/
â”‚   â””â”€â”€ SPEC.md
```

- **Root folder**: `<app_folder>/context/specification/`
- **Root file**: `SPECIFICATION.md` â€” contains the Table of Contents (with links to
  each module's `SPEC.md`), all shared infrastructure sections (1â€“9), and all
  application-level cross-cutting sections (10â€“24, excluding module blueprints)
- **Module folders**: One folder per module from PRD.md, named in kebab-case
  (e.g., `location-information/`, `corridor/`, `employer/`)
- **Module files**: Each `SPEC.md` is self-contained with full code samples for that
  module's module â€” service, DTOs, model, migration, controller, views, and Blade templates
