---
name: specgen-flutter-riverpod
model: claude-opus-4-8
effort: high
description: >
  Generate a detailed specification document for building a Flutter mobile application
  using Flutter 3.x (Dart 3.x), Riverpod 2.x for state management, Hive 2.x for local
  storage, Dio 5.x for REST API with smart retry, Firebase Messaging + flutter_local_notifications
  for push/event notifications, go_router 14.x for navigation, freezed 2.x + json_serializable
  for immutable models, and build_runner for code generation. The spec also covers
  cached_network_image, flutter_svg, pull_to_refresh, font_awesome_flutter, material_design_icons_flutter,
  intl, url_launcher, and flutter_native_splash. Authentication (Keycloak OAuth2/OIDC PKCE
  via flutter_appauth, local JWT, or none) and optional features (WebSocket, i18n via intl)
  are configurable based on user input.
  Standardized input: application name (mandatory), version (mandatory), module (optional).
  Use this skill whenever the user asks to create a spec, specification, blueprint, or
  technical design document for a new Flutter mobile application.
  Also trigger when the user says things like "spec out a new Flutter app", "design a
  Flutter app with Riverpod", "write a technical spec for my new mobile app", "scaffold
  spec for a Flutter Riverpod app", or any request for a specification document describing
  a Flutter + Riverpod + Dio + Hive application. Even if the user only mentions a subset
  of the stack (e.g., "Flutter mobile app" or "Flutter with Firebase notifications"),
  this skill likely applies â€” ask and confirm.
---

# Flutter Mobile Specification Generator

This skill generates a comprehensive specification document (Markdown) that serves as a
blueprint for building a Flutter mobile application. The spec is intended to be followed
by a developer or a coding agent to produce a fully functional project scaffold targeting
both Android and iOS.

The specification does NOT generate code. It produces a detailed, opinionated technical
document describing every layer of the application â€” from `pubspec.yaml` configuration to
Material Theme, from Riverpod providers to Dio retry interceptors â€” so that implementation
becomes a mechanical exercise.

## Technology Stack

### Core Stack (Always Included)

These are the fixed versions the spec targets. Do not deviate unless the user explicitly
requests different versions.

| Component                        | Version   |
|----------------------------------|-----------|
| Flutter SDK                      | 3.24.x    |
| Dart SDK                         | 3.5.x     |
| flutter_riverpod                 | 2.5.x     |
| riverpod_annotation              | 2.3.x     |
| riverpod_generator               | 2.4.x     |
| hooks_riverpod                   | 2.5.x     |
| flutter_hooks                    | 0.20.x    |
| hive                             | 2.2.x     |
| hive_flutter                     | 1.1.x     |
| dio                              | 5.7.x     |
| dio_smart_retry                  | 6.0.x     |
| pretty_dio_logger                | 1.4.x     |
| go_router                        | 14.x      |
| freezed_annotation               | 2.4.x     |
| freezed                          | 2.5.x     |
| json_annotation                  | 4.9.x     |
| json_serializable                | 6.8.x     |
| build_runner                     | 2.4.x     |
| firebase_core                    | 3.6.x     |
| firebase_messaging               | 15.1.x    |
| flutter_local_notifications      | 17.2.x    |
| cached_network_image             | 3.4.x     |
| flutter_svg                      | 2.0.x     |
| pull_to_refresh                  | 2.0.x     |
| font_awesome_flutter             | 10.7.x    |
| material_design_icons_flutter    | 7.0.x     |
| intl                             | 0.19.x    |
| url_launcher                     | 6.3.x     |
| flutter_native_splash            | 2.4.x     |
| flutter_dotenv                   | 5.2.x     |
| path_provider                    | 2.1.x     |
| flutter_secure_storage           | 9.2.x     |

### Optional Integration Versions

Include in the version table only when the corresponding integration is selected.

| Component                | Version   | When Selected               |
|--------------------------|-----------|-----------------------------|
| Keycloak                 | 26.x      | Auth = Keycloak             |
| flutter_appauth          | 8.0.x     | Auth = Keycloak or OIDC     |
| openid_client            | 0.4.x     | Auth = Keycloak or OIDC     |
| web_socket_channel       | 3.0.x     | WebSocket = yes             |
| flutter_localizations    | SDK       | i18n = yes                  |
| share_plus               | 10.0.x    | Sharing = yes               |
| image_picker             | 1.1.x     | ImagePicker = yes           |
| file_picker              | 8.1.x     | FilePicker = yes            |
| permission_handler       | 11.3.x    | Permissions = yes           |
| firebase_analytics       | 11.3.x    | Analytics = yes             |
| firebase_crashlytics     | 4.1.x     | Crashlytics = yes           |

## Core Dependencies (pubspec.yaml)

The spec must include these in the `pubspec.yaml` dependencies section (always):

**Runtime dependencies:**
- `flutter` (sdk: flutter) â€” Core Flutter framework
- `flutter_riverpod` â€” Riverpod for Flutter
- `riverpod_annotation` â€” Annotations for riverpod_generator
- `hooks_riverpod` â€” Riverpod with flutter_hooks integration
- `flutter_hooks` â€” React-style hooks for Flutter
- `hive` + `hive_flutter` â€” Local NoSQL key-value database
- `dio` â€” HTTP client
- `dio_smart_retry` â€” Retry interceptor for Dio
- `pretty_dio_logger` â€” Request/response logging in development
- `go_router` â€” Declarative routing
- `freezed_annotation` â€” Annotations for freezed code generation
- `json_annotation` â€” Annotations for json_serializable
- `firebase_core` â€” Firebase initialization
- `firebase_messaging` â€” Push notification (FCM)
- `flutter_local_notifications` â€” Foreground/scheduled local notifications
- `cached_network_image` â€” Network image with caching and placeholders
- `flutter_svg` â€” SVG rendering
- `pull_to_refresh` â€” Smart pull-to-refresh widget
- `font_awesome_flutter` â€” Font Awesome icons
- `material_design_icons_flutter` â€” Material Design Icons (MDI)
- `intl` â€” Internationalization, date/number formatting
- `url_launcher` â€” Open URLs, dial, mailto, etc.
- `flutter_dotenv` â€” Load `.env` configuration files
- `path_provider` â€” Filesystem paths for Hive init
- `flutter_secure_storage` â€” Encrypted key-value store (keychain/keystore)

**Development dependencies:**
- `flutter_test` (sdk: flutter) â€” Widget test framework
- `build_runner` â€” Code generation runner
- `freezed` â€” Immutable data class generator
- `json_serializable` â€” JSON serialization generator
- `riverpod_generator` â€” Riverpod provider generator
- `hive_generator` â€” Hive type adapter generator
- `flutter_lints` â€” Recommended lint rules
- `flutter_native_splash` â€” Native splash screen generator
- `mocktail` â€” Mock library for unit tests

### Conditional Dependencies

**If Auth = Keycloak or OIDC:**
- `flutter_appauth` â€” Native OAuth2/OIDC PKCE flow (uses AppAuth Android/iOS)
- `openid_client` â€” OIDC discovery and token parsing

**If WebSocket = yes:**
- `web_socket_channel` â€” Cross-platform WebSocket client

**If i18n = yes:**
- `flutter_localizations` (sdk: flutter)
- `intl` is already in core â€” used for ARB-based message localization

**If Analytics = yes:**
- `firebase_analytics`

**If Crashlytics = yes:**
- `firebase_crashlytics`

**If ImagePicker = yes:**
- `image_picker`
- `permission_handler` (for camera/photo permissions)

**If FilePicker = yes:**
- `file_picker`

**If Sharing = yes:**
- `share_plus`

## When the Skill Triggers

Generate the spec when the user provides an **application name** and **version** that
corresponds to one of the custom applications defined in `CLAUDE.md`. The skill
reads all required inputs from the project's context files â€” no interactive Q&A is needed
for the core inputs.

The user invokes this skill by specifying the target application and version, for example:
- `/specgen-flutter-riverpod mobile v1.0.4`
- `/specgen-flutter-riverpod mobile v1.0.4 module:Hero Section`
- `/specgen-flutter-riverpod "Field Worker App" v1.0.4`

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
| `<application>` | Yes | `mobile` | Application name to locate the context folder |
| `<version>` | Yes | `v1.0.4` | Version to scope processing |
| `module:<name>` | No | `module:Hero Section` | Limit generation to a single module |

### Application Folder Resolution

The application name is matched against root-level application folders:
1. Strip any leading `<number>_` prefix from folder names (e.g., `1_mobile` â†’ `mobile`)
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
- `SPECIFICATION.md` (root) gets a partial update â€” only that module's entry in the TOC
  is added or updated; all other TOC entries are preserved as-is

## Gathering Input

The specification is driven by **six input sources** read from the project's context files.
The skill does NOT ask the user for auth, API backend URL, or optional component choices â€”
it **determines** these automatically from the context.

### Input 1: Application Name (from CLAUDE.md)

From CLAUDE.md (already loaded in context), locate the target application under the
**Custom Applications** section. Extract:

- **Application name**: The section heading (e.g., "Mobile App", "Field Worker")
- **Application description**: The description paragraph below the heading
- **Dependencies**: The "Depends on" list â€” primary source for determining backend API
  base URL, authentication provider, and optional components

The application name is used to derive:
- **Project slug**: snake_case of the application name (Dart/Flutter package naming;
  e.g., `mobile_app`, `field_worker`)
- **App bundle ID / Application ID**: Reverse-DNS format (e.g.,
  `com.example.mobile_app`) â€” Android `applicationId` and iOS `CFBundleIdentifier`
- **App display name**: Title-case of application name (e.g., "Mobile App")

### Input 2: User Stories (from PRD.md)

Read `<app_folder>/context/PRD.md`. This file contains all user stories organized by
module. Extract:

- **System modules**: Modules under `# System Module` heading (e.g., Authentication,
  Profile). These become system-level features.
- **Business modules**: Modules under `# Business Module` heading (e.g., Order,
  Catalogue). These become business-level features.
- **User stories per module**: Each `### User Story` section contains tagged items.
  These define the functional requirements for each feature's repositories, providers,
  forms, and screens.

The user stories directly inform:
- Which API calls each feature's repository must expose
- Which screens (Stateful/HookConsumerWidget) and routes are needed
- Which form fields and validation rules apply
- Which Flutter widgets best match the described UI

**Important:** Items with strikethrough (`~~text~~`) are deprecated â€” do NOT include them
as active requirements. List them in the "Removed / Replaced" subsection of the
traceability table.

- **Version tags per item**: Each `### User Story`, `### Non Functional Requirement`,
  and `### Constraint` section contains one or more version blocks formatted as `[v1.0.x]`.
  The skill must track the version tag for each item and carry it through to the
  generated specification's traceability section.

### Input 3: Non-Functional Requirements (from PRD.md)

Within the same `PRD.md`, each module has a `### Non Functional Requirement` section.
These inform:

- UI layout choices (list vs. grid, card sizes, image dimensions)
- Data fetching strategies (pagination, infinite scroll, refresh)
- Validation rules (character limits, format requirements)
- Performance constraints (lazy widgets, image caching, offline support)

NFRs should be mapped to specific technical decisions in the spec â€” for example, an NFR
stating "paginated with 20 items per page" confirms which Riverpod pagination pattern
to use, while "must work offline" confirms which Hive box manages the offline cache.

### Input 4: Constraints (from PRD.md)

Within the same `PRD.md`, each module has a `### Constraint` section. These define
hard boundaries that the spec must enforce:

- Status enum values (e.g., "DRAFT, ACTIVE, EXPIRED")
- Business rules (e.g., "category must exist before creating content")
- Access control (e.g., "only WORKER role can access task management")

Constraints are embedded directly into the relevant module blueprint â€” they inform
freezed model definitions, repository method parameters, and route guard configurations.

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
- Freezed data class definitions (field-for-field, not placeholder)
- Hive type adapters (`@HiveType`/`@HiveField`) for cached entities
- JSON serialization via `json_serializable`
- Dio request/response DTOs
- Riverpod state model

### Input 6: HTML Mockup Screens (from mockup/ folder)

Read `<app_folder>/context/mockup/MOCKUP.html` first as the index page, then read the
HTML files organized by role in subfolders.

**MOCKUP.html** provides:
- Application identity (name, version, short name)
- Design tokens: fonts, colors from Tailwind/CSS config or inline styles
- List of user roles and their screen sets

**Role-specific subfolders** (e.g., `mockup/worker/task/`):
- Individual HTML screens for each page in the application
- Screen layout: which widgets are used (ListView, GridView, Forms, Modals, Cards)
- Navigation structure from drawer/bottom-nav HTML files
- Data display patterns (list pages, detail pages, create/edit forms)

**IMPORTANT â€” Role folders inform access control, NOT route paths.** The role-specific
folder structure (e.g., `mockup/worker/task/task-list.html`) determines:
1. Which role can access the screen â†’ `redirect` guard with role check
2. Which navigation items appear for each role
It does NOT determine the route path. The route path is always module-based:
- `GoRoute(path: '/task', ...)` â€” NOT `GoRoute(path: '/worker/task', ...)`

The mockup screens directly map to:
- Flutter screen widgets (one per HTML screen)
- go_router route definitions
- Widget selections (ListView vs DataTable, BottomSheet vs Drawer, Card vs Tile)
- Form field layouts
- Navigation items per role (drawer / bottom navigation bar)
- ThemeData color tokens (extract from mockup CSS/styles)

## PRD.md Extended Sections

Before determining optional components, check PRD.md for the following extended sections:

### Architecture Principle Extraction

If PRD.md contains an `# Architecture Principle` section, extract patterns that affect mobile decisions:

| Pattern to Extract | How It Influences the Specification |
|---|---|
| "Stateless REST API" | Confirms Dio + Riverpod async provider pattern for API calls |
| "Event-driven" / "WebSocket" / "real-time" | Include web_socket_channel and a stream provider for live data |
| "API gateway" | Configure base URL to point to gateway rather than individual services |
| Backend framework mention | Validate API response format assumptions |
| "Offline-first" / "local cache" | Include Hive cache layer for read paths |

If the section is absent, proceed with existing CLAUDE.md-only detection.

### Design System Extraction

If PRD.md contains a `# Design System` section with a file reference:
1. Resolve and read the referenced file
2. Map design tokens to Flutter `ThemeData` configuration: color scheme, text theme,
   component themes (ElevatedButtonTheme, AppBarTheme, CardTheme, InputDecorationTheme)
3. Include a complete `ThemeData` configuration in SPECIFICATION.md derived from the
   design system tokens

If the section is absent, use a default Material 3 theme (existing behavior).

### High Level Process Flow Extraction

If PRD.md contains a `# High Level Process Flow` section:
1. Process flows with user-visible states inform which status values appear in
   filter chips/dropdowns
2. Process flows with real-time updates inform WebSocket subscription patterns
3. Multi-step user flows inform go_router nested route design and Stepper/PageView usage

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
| References another application's REST API | `API_BASE_URL` set to that app's base URL |
| References a Spring Boot backend | Include Spring Boot CORS headers note |
| No explicit backend | Include mock API / json-server note for development |

### Authentication Detection

| Dependency / PRD Pattern | Auth Selection |
|---|---|
| References "Single Sign On" or "Keycloak" in CLAUDE.md dependencies | Auth = Keycloak |
| PRD.md has login user stories with email/password | Auth = Local (local JWT from API) |
| PRD.md constraint says "public access, no auth required" | Auth = none |
| PRD.md has only public-facing content | Auth = none |

If Auth = Keycloak, also extract from CLAUDE.md:
- Keycloak version
- Keycloak realm: Default derived from project name
- Keycloak client ID: Default `<project-slug>-mobile`
- Keycloak issuer URI: Default `http://localhost:8180/realms/<realm>`
- Keycloak roles: Infer from mockup role folders (e.g., `worker` â†’ `WORKER`, `admin` â†’ `ADMIN`)

If Auth = Local (API-managed JWT):
- Login/logout handled by Dio calls to the backend
- Access token stored in `flutter_secure_storage` (Keychain / Android Keystore)
- Refresh token also in `flutter_secure_storage`
- Dio interceptor attaches `Authorization: Bearer <token>` header
- Token refresh interceptor handles 401 responses

### Optional Component Detection

| PRD.md Pattern | Component Selection |
|---|---|
| NFRs mention "real-time", "live updates", "push notification" | FirebaseMessaging always-on (core); WebSocket = yes if user-driven streams |
| User stories mention "schedule reminder", "local alarm", "background reminder" | Local notifications always-on (core); add scheduled notification helper |
| NFRs mention "share to social", "share link" | Sharing = yes |
| User stories mention "upload photo", "take photo" | ImagePicker = yes |
| User stories mention "attach file", "upload document" | FilePicker = yes |
| PRD.md mentions multiple languages or localization | i18n = yes |
| NFRs mention "track screen views", "user analytics", "conversion funnel" | Analytics = yes |
| NFRs mention "crash reporting", "production error monitoring" | Crashlytics = yes |
| NFRs mention "camera", "gallery", "storage", "location" | Permissions = yes |

### Summary of Determination

After analyzing all inputs, produce a determination summary before generating the spec.
Present it to the user for confirmation:

```
Optional Component Determination:
- Backend API:    http://localhost:<port>/api (from CLAUDE.md Port Allocation table â†’ depends on backend app)
- Authentication: Keycloak PKCE via flutter_appauth (from CLAUDE.md â†’ depends on Single Sign On)
- WebSocket:      no
- i18n:           yes (from PRD.md â†’ English + Bahasa Malaysia required)
- Analytics:      yes (from PRD.md NFR â†’ screen view tracking)
- Crashlytics:    yes (from PRD.md NFR â†’ production error monitoring)
- ImagePicker:    yes (from PRD.md â†’ upload photo of completed task)
- FilePicker:     no
- Sharing:        no
- Permissions:    yes (camera, photo library)
```

If the user disagrees with any determination, allow them to override before proceeding.

## Required Inputs

After determination, these values are needed. Most are derived automatically:

**Auto-derived from context files:**
- **Application name**: From CLAUDE.md section heading
- **Project slug**: snake_case of application name
- **App display name**: Title-case used in `AppBar` title and launcher label
- **App bundle ID**: Reverse-DNS from project slug
- **Application description**: From CLAUDE.md description
- **Backend API base URL**: From CLAUDE.md dependencies
- **Modules / Features**: From PRD.md module headings + model/MODEL.md
- **Auth type**: Auto-determined (see above)
- **Optional components**: Auto-determined (see above)
- **User roles**: From mockup role folders
- **Design tokens**: ThemeData colors extracted from mockup CSS/inline styles

**Auto-derived from CLAUDE.md (Port Allocation table):**
- **Backend API base URL**: Look up the backend application's port from the `Port Allocation` table in the `Custom Applications` section of `CLAUDE.md`. Construct the base URL as `http://10.0.2.2:<port>/api/v1` for Android emulator development (which proxies `localhost`) and `http://localhost:<port>/api/v1` for iOS simulator. Do NOT hardcode `8080` â€” the port MUST match the allocated port for the backend application this mobile app depends on.

**Optional (use sensible defaults if not found in context):**
- **Default locale**: Default `en`
- **Page size**: Default `20` (mobile-appropriate, from NFRs or fallback)
- **Min Android SDK**: Default `23` (Android 6.0)
- **Min iOS deployment target**: Default `13.0`

## Generating the Specification

Once inputs are gathered from context files and optional components are determined,
generate the specification as a **multi-file output split by module**. Read the spec
template at `references/spec-template.md` for the exact structure and content of each
section. The template is the authoritative guide â€” follow it closely.

The specification is split into two categories:

1. **Root `SPECIFICATION.md`** â€” Table of Contents, shared infrastructure, ThemeData,
   routing, auth configuration, Hive/Dio/Firebase init, and application-level sections
   that apply across all modules.
2. **Per-module `<module-name>/SPEC.md`** â€” Each module gets its own folder with a
   self-contained specification covering that module's complete blueprint.

This split enables a coding agent to:
- First, scaffold the shared infrastructure from `SPECIFICATION.md`
- Then, implement each module independently by picking up its `<module>/SPEC.md`

**Important:** The generated spec must use **real module data** from the context files,
not generic placeholders. Specifically:

- **Modules** must use the actual module names from PRD.md and MODEL.md
  (e.g., `task`, `order`, `catalogue` â€” not `module1`, `module2`)
- **Freezed models** must match the actual fields defined in the module model files,
  not placeholder `fieldOne`/`fieldTwo`
- **Repositories** must expose methods matching the actual user stories (e.g., if a story
  says "view list of tasks", the repository needs `fetchTasks()`)
- **Screens** must map to the actual mockup screens (e.g., if
  `worker/task/task-list.html` exists, there must be a matching route and screen
  widget). The route path is module-based (e.g., `/task`), NOT role-prefixed
  (e.g., NOT `/worker/task`).
- **Form fields** must match what the mockup screens display
- **Validation rules** must enforce the constraints from PRD.md (character limits, URL format, etc.)
- **ThemeData** must use the design tokens extracted from the mockup (colors, border-radius, font)
- **Version tags**: Every user story ID, NFR ID, constraint ID, and mockup screen in the
  traceability section must include its version tag (e.g., `USA000030 [v1.0.4]`).
  **ALL traceability sub-tables (User Stories, NFRs, AND Constraints) MUST include the
  `| Version |` column.**
- **Removed / Replaced items**: The traceability section must include a "Removed / Replaced"
  subsection listing deprecated items â€” showing the removed ID, the version that removed it,
  the replacement ID (if any), and a brief reason.

### Output Structure

```
<app_folder>/context/specification/
â”œâ”€â”€ SPECIFICATION.md                    â† TOC + shared/application-level specs
â”œâ”€â”€ task/
â”‚   â””â”€â”€ SPEC.md                         â† Module blueprint for Task
â”œâ”€â”€ order/
â”‚   â””â”€â”€ SPEC.md                         â† Module blueprint for Order
â”œâ”€â”€ catalogue/
â”‚   â””â”€â”€ SPEC.md                         â† Module blueprint for Catalogue
â”œâ”€â”€ ...                                 â† One folder per module from PRD.md
```

### What Goes in `SPECIFICATION.md` (Root)

The root file contains the TOC and all shared/application-level sections. These are
sections a coding agent implements **first** before any module work:

#### 1. Project Overview
Project metadata, application description, technology stack summary, user roles, module
index table linking to each module's SPEC.md, target platforms (Android/iOS) and minimum
OS versions.

#### 2. Package Configuration
Complete `pubspec.yaml` with all dependencies (core + selected conditional),
`build_runner` scripts, and asset/font declarations.

#### 3. Application Configuration
`analysis_options.yaml` (lints), `.gitignore`, Flutter `flavors` if multi-environment
needed, native splash and launcher icon configuration, Android `build.gradle` & iOS
`Info.plist` notes (permissions, deep links, FCM background handler).

#### 3a. Application Version Configuration
The application MUST include a version value derived from the version argument provided
during skill invocation. If multiple versions were provided, use the highest one.

In `pubspec.yaml`:
```yaml
version: 1.0.3+1
```

The first part (`1.0.3`) is the human-readable version; the suffix (`+1`) is the build
number. The build number MUST be incremented manually or via CI on each release.

The application MUST expose this version in a **Settings/About** screen or persistent
drawer footer. Use `package_info_plus` (add as dependency if surfacing programmatically):
```dart
final info = await PackageInfo.fromPlatform();
final versionLabel = 'v${info.version}+${info.buildNumber}';
```

#### 3b. `.env` File Generation from ENVIRONMENT.md
Generate `.env.development` and `.env.production` files at the project root for use with
`flutter_dotenv`. The `.env.development` file is populated by reading `ENVIRONMENT.md` from
the project root, mapping credential and platform values to plain environment variable
names (no `VITE_` prefix â€” Flutter does not use Vite). The `.env.production` file uses
placeholder values for production.

**Process:**
1. Read `ENVIRONMENT.md` from the project root
2. Extract credential values from `ENVIRONMENT.md` (`# Supporting 3rd Party Applications`
   for Keycloak host/realm/client, plus `# External Services` such as Firebase config); the
   backend API host/port comes from the `# Port Allocation` table in `CLAUDE.md`. Read any
   toolchain paths from `DEVTOOL.md`
3. Map each value to the corresponding environment variable name
4. Generate `.env.development` with actual local values
5. Generate `.env.production` with production placeholder values
6. Register both files under `assets:` in `pubspec.yaml`

**Example `.env.development` output (derived from ENVIRONMENT.md):**
```properties
# Backend API
API_BASE_URL=http://10.0.2.2:<port from CLAUDE.md Port Allocation table>/api/v1
API_TIMEOUT_MS=30000
API_RETRY_ATTEMPTS=3

# Authentication (Keycloak)
KEYCLOAK_ISSUER=http://10.0.2.2:8180/realms/urp
KEYCLOAK_CLIENT_ID=urp-mobile
KEYCLOAK_REDIRECT_URI=com.example.mobile_app:/oauth2redirect
```

**Rules:**
- Use plain environment variable names; access via `dotenv.env['API_BASE_URL']`
- Use actual values from ENVIRONMENT.md â€” never use placeholders or `TODO`
- If ENVIRONMENT.md does not exist or a value is not found, use sensible defaults for local
  development (Android emulator uses `10.0.2.2` for host's `localhost`)
- Both `.env.development` and `.env.production` are gitignored, but the **files MUST
  still be declared under `assets:`** in `pubspec.yaml` so `flutter_dotenv` can load them
  at runtime
- Firebase config (`google-services.json`, `GoogleService-Info.plist`) is checked in
  per-flavor but the Firebase project ID/sender ID are read from `.env` if dynamic

#### 4. Directory Structure
The complete source tree under `lib/`. The structure follows feature-based architecture
where each PRD module maps to a `lib/features/<module>/` folder.
Read `references/routing-patterns.md` for the module folder layout.

#### 5. Theme Configuration
Custom Material 3 `ThemeData` built from design tokens extracted from mockup screens.
Includes color scheme (seeded from primary), text theme (Google Fonts or custom font
family), component themes (ElevatedButtonTheme, AppBarTheme, CardTheme, InputDecorationTheme,
FloatingActionButtonTheme), and shape/radius tokens.
Read `references/component-patterns.md` for theme setup patterns.

#### 6. Authentication Configuration *(conditional â€” include only if Auth != none)*
**If Auth = Keycloak:** PKCE Authorization Code flow using `flutter_appauth`. The native
AppAuth library (Android + iOS) handles the system browser redirect. `AuthRepository`
exposes `signIn()`, `signOut()`, `getAccessToken()`. Tokens stored in
`flutter_secure_storage`. Dio interceptor reads access token. Refresh token used to renew
silently. Deep link callback configured for both platforms.
Read `references/security-patterns.md` for the full auth architecture.

**If Auth = Local (API JWT):** Login screen submits to backend API, JWT stored in
`flutter_secure_storage`, Dio interceptor attaches Authorization header, token refresh
interceptor handles 401 responses, route guard via go_router `redirect` callback
redirects unauthenticated users.

#### 7. Router Configuration
go_router v14 route tree â€” top-level routes, nested shell routes for bottom navigation,
route guards via `redirect`, deep link configuration for FCM/Keycloak callbacks,
typed route helpers (optional, via `go_router_builder`).
Read `references/routing-patterns.md` for route patterns.

#### 8. API Client Configuration
Dio instance with `baseUrl` from `dotenv.env['API_BASE_URL']`, request/response
interceptors:
- Auth interceptor (Bearer token injection)
- Retry interceptor (`DioSmartRetry` â€” exponential backoff on 5xx, network errors, retry idempotent methods)
- Logging interceptor (`PrettyDioLogger`, **dev only** â€” guard with `kDebugMode`)
- Error interceptor (transforms `DioException` â†’ typed `ApiFailure` sealed class)

`connectTimeout`, `receiveTimeout`, `sendTimeout` from `.env`.

#### 9. Local Storage (Hive)
`Hive.initFlutter()` in `main()`, type adapters registered for each cached entity,
typed `Box<T>` providers via Riverpod, helper extension methods for upsert/find/clear,
encryption optional (HiveAesCipher with key from `flutter_secure_storage`).
Read `references/storage-patterns.md` for Hive patterns.

#### 10. Riverpod Setup
`ProviderScope` wrapping `MyApp`, code generation via `riverpod_generator`,
`AsyncNotifier`/`Notifier` providers for state, family providers for parameterized
queries, naming convention: `<entity>RepositoryProvider`, `<entity>ListProvider`,
`<entity>ByIdProvider(id)`.
Read `references/state-patterns.md` for Riverpod patterns.

#### 11. Shared Layouts
`AppShellScreen` (bottom navigation + Scaffold body via `ShellRoute`), `AuthShell`
(login/forgot-password scaffolding), `PublicShell` for unauthenticated content (if any).
Each shell uses Material 3 widgets.

#### 12. Shared Widgets
Reusable widgets used across multiple modules: `AppScaffold` (AppBar + body slot),
`LoadingIndicator`, `EmptyState`, `ErrorState`, `ConfirmDialog`, `StatusChip`,
`SearchBarField`, `FormTextField`, `FormDatePickerField`, `FormDropdownField`,
`ImagePickerField` (if ImagePicker = yes), `PullToRefreshList`, `InfiniteScrollList`,
`CachedSvgIcon`, `AppNetworkImage` (wraps `CachedNetworkImage` with placeholder/error).

#### 13. Navigation Configuration
Bottom navigation items (or drawer items) derived from mockup nav files, organized by
role. Each item has label, icon (Material/MDI/FA), path, and required role.
Navigation is rendered dynamically based on the authenticated user's roles.

#### 14. Form Infrastructure
Reusable form-field widgets wrapping `TextFormField` / `DropdownButtonFormField` /
`DatePicker` with consistent decoration, validators (`Validator` static methods:
`required`, `email`, `min/maxLength`, `url`, `compose`), submit button with loading
state (CircularProgressIndicator inside ElevatedButton).

#### 15. Error Handling Strategy
Top-level `FlutterError.onError` and `PlatformDispatcher.instance.onError` for uncaught
errors (route to Crashlytics if enabled), Dio error interceptor mapping `DioException`
â†’ `ApiFailure` sealed class, Riverpod `AsyncValue.when(...)` for screen-level
error/loading states, `ErrorState` widget for full-screen errors with retry button,
`ScaffoldMessenger` (SnackBar) for transient errors.

#### 16. Notification System
**Push notifications (FCM):**
- `firebase_messaging` foreground/background/terminated handlers
- Token registration with backend on first launch and refresh
- Notification permission request (iOS + Android 13+)
- Deep link from notification payload to a specific route via go_router

**Local notifications:**
- `flutter_local_notifications` initialized with platform settings (Android channels,
  iOS categories)
- Used to display FCM messages received in foreground (FCM does not show banners in
  foreground by default on iOS/Android)
- Used for in-app scheduled reminders if PRD requires it

**In-app toasts:**
- `ScaffoldMessenger.of(context).showSnackBar(...)` for non-critical user feedback.

Read `references/notification-patterns.md` for the full notification architecture.

#### 17. Theming & Dark Mode
`MaterialApp.themeMode` toggled via UI control, persisted in Hive `settings` box.
`lightTheme` and `darkTheme` constructed via `ThemeData(colorScheme: ColorScheme.fromSeed(...))`
with brightness override. `ThemeToggle` widget switches mode and writes to Hive.

#### 18. Testing Strategy
Overview: `flutter_test` + `mocktail` for widget/unit tests, `ProviderContainer` for
testing Riverpod providers in isolation, golden tests for critical screens, integration
tests via `integration_test` package. Per-feature test conventions matching the module spec.

#### 19. Build & Distribution
- `flutter build apk --release` / `flutter build appbundle --release` (Android)
- `flutter build ipa --release` (iOS)
- Code signing notes (Android: upload keystore in `~/.gradle/gradle.properties`; iOS:
  Apple Developer team + provisioning profile)
- Native splash via `flutter_native_splash` (`dart run flutter_native_splash:create`)
- Launcher icon via `flutter_launcher_icons` (optional)
- ProGuard rules for Firebase + AppAuth (Android release builds)

#### 20. Internationalisation *(conditional â€” include only if i18n = yes)*
`flutter_localizations` enabled, `intl` for ARB messages, `flutter_gen_l10n` configured
in `pubspec.yaml`, `lib/l10n/app_en.arb` + per-locale ARBs, generated `AppLocalizations`
class, `MaterialApp.localizationsDelegates` and `supportedLocales` wired, locale-switch
provider persisted in Hive.

#### 21. WebSocket Integration *(conditional â€” include only if WebSocket = yes)*
`web_socket_channel` setup, connection management Riverpod provider with auto-reconnect
+ exponential backoff, typed event handler with sealed-class events, lifecycle hook
in `AppShellScreen` to open/close socket on app foreground/background.

#### 22. Firebase Initialization
Always required (push notifications depend on it). Cover:
- `Firebase.initializeApp(options: DefaultFirebaseOptions.currentPlatform)` in `main()`
  before `runApp(...)`
- `google-services.json` (Android) + `GoogleService-Info.plist` (iOS) placement
- `flutterfire configure` CLI workflow (used once during scaffolding)
- Background message handler: top-level `@pragma('vm:entry-point')` function
- Firebase Analytics initialization (if Analytics = yes)
- Firebase Crashlytics setup hook (if Crashlytics = yes)

### What Goes in Each `<module>/SPEC.md` (Per-Module)

For EACH module from PRD.md and MODEL.md, create a folder named after the module
(kebab-case, e.g., `task/`) and generate a `SPEC.md` inside it.

Each module `SPEC.md` is a **self-contained** blueprint that a coding agent can pick up
and implement independently (after the shared infrastructure is in place). It must include:

- **Header** with module name and back-reference to root `SPECIFICATION.md`
- **Traceability**: User story IDs, NFR IDs, constraint IDs, table/collection names,
  mockup screen filenames, all with version tags
- **Freezed Models** â€” `@freezed` data classes matching the module model fields
  (field-for-field), including `fromJson`/`toJson` via `json_serializable`
- **Hive Adapters** *(if module is cached offline)* â€” `@HiveType` adapter with field
  numbers matching the freezed model
- **Validation Rules** â€” Validator static methods or `Form` validator closures derived
  from PRD constraints
- **API Repository** â€” Dio-based API class matching user story data operations
- **Riverpod Providers** â€” `AsyncNotifierProvider` for list, family provider for detail,
  mutation methods on a `Notifier` for CUD operations, cache invalidation pattern via
  `ref.invalidate()`
- **Screens** â€” one per mockup screen, using Material 3 widgets matching the mockup layout
- **Form Widgets** â€” create/edit forms with `Form` + `GlobalKey<FormState>` + reusable
  field widgets
- **Route Definitions** â€” go_router routes for this module with `redirect` guards
  matching the mockup role folder access control
- **Navigation Items** â€” bottom-nav / drawer entries for each role that can access this module
- **Complete code samples** for every widget â€” continuous and copy-pasteable

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
5. Row format: `| {YYYY-MM-DD} | {application_name} | specgen-flutter-riverpod | {module or "All"} | Generated Flutter Riverpod mobile technical specification |`
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

## Constraints (Non-Negotiable)

These constraints apply to every code sample in the generated spec:

**Null-safe Dart everywhere.** Target Dart 3.5+ with sound null safety. No `dynamic`
unless the API genuinely returns unstructured JSON â€” prefer `Object?` with explicit
type checks, or strongly typed `Map<String, dynamic>` only at the JSON boundary.

**Feature-based architecture.** Every module maps to `lib/features/<module>/`. Nothing
module-specific leaks into `lib/shared/` or `lib/core/`. Shared widgets must be
genuinely reusable across at least two modules.

**No tokens in plaintext storage.** JWT access and refresh tokens are stored in
`flutter_secure_storage` (Keychain / Android Keystore), never in `SharedPreferences`,
Hive, or in-memory globals that persist beyond the process. Hive is encrypted (`HiveAesCipher`)
when storing user-sensitive cached data â€” encryption key lives in `flutter_secure_storage`.

**Riverpod for all state.** Do not use `setState` for state that crosses widgets, and
do not use `InheritedWidget` directly â€” use Riverpod providers. `setState` is only
acceptable for purely local widget UI state (animation controllers, hover, focus).

**Freezed for all data models.** No hand-rolled equality / hashCode / copyWith. Every
data class is `@freezed` with `fromJson`/`toJson` if it crosses the API boundary.

**Generated code via build_runner.** Always include the standard commands in the spec:
- `dart run build_runner build --delete-conflicting-outputs` â€” one-shot generation
- `dart run build_runner watch --delete-conflicting-outputs` â€” watch mode for development

**Material 3 only.** `ThemeData(useMaterial3: true)`. Do not mix in Cupertino-only widgets
in cross-platform screens â€” use `Adaptive*` constructors or platform-aware wrappers if
truly necessary.

**go_router for navigation.** Do not use raw `Navigator.push`/`Navigator.pop`. All
navigation is `context.go(...)`, `context.push(...)`, or `context.pop()` via go_router.
Deep link configuration is centralized in `lib/router/app_router.dart`.

**Consistent file naming (Dart conventions):**
- Widgets / classes: `PascalCase` class names in `snake_case.dart` files (e.g.,
  `task_list_screen.dart` defines `class TaskListScreen`)
- Riverpod providers: generated by `riverpod_generator` from `<feature>_providers.dart`
- Repository files: `<feature>_repository.dart` (e.g., `task_repository.dart`)
- Models: `<entity>.dart` for `@freezed` data class, generated `*.freezed.dart` &
  `*.g.dart` are committed
- Test files: `<file>_test.dart` co-located in `test/<feature>/` mirroring `lib/features/`
