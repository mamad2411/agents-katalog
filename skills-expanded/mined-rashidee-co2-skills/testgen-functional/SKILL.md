---
name: testgen-functional
model: claude-opus-4-8
effort: high
description: >
  Generate Playwright E2E test plan and specification documents from project artifacts
  (user stories, module models, mockups, specifications). Produces a TEST_PLAN.md root
  summary and per-module TEST_SPEC.md files containing test scenarios, data seeding
  scripts, and cleanup scripts â€” all as detailed Markdown blueprints, not actual test code.
  Input: application name (mandatory), version (mandatory), module (optional).
  Output: TEST_PLAN.md + per-module TEST_SPEC.md files in the auto-resolved test output folder.
  Trigger on keywords: "generate test plan",
  "generate test spec", "create test specification", "E2E test plan", "Playwright test plan",
  "test plan from user stories", "test spec from PRD.md", "generate test scenarios",
  "create test blueprint". Accepts application name and version as input
  (e.g., `/testgen-functional hub_middleware v1.0.3`).
  Optionally accepts a module name to limit generation to test specs for that module only
  (e.g., `/testgen-functional hub_middleware v1.0.3 module:Location Information`).
  Automatically excludes strikethrough (deprecated/removed) items.
---

# Test Generator

Generate Playwright E2E test plan and specification documents from PRD.md and
related project artifacts. Outputs are **Markdown documents** (TEST_PLAN.md and per-module
TEST_SPEC.md files) that serve as detailed blueprints for a developer or coding agent to
implement actual Playwright test code. This skill does NOT generate Playwright code.

## Core Concept: 4-Layer Data Seeding Strategy

Every module is classified into one of 4 data seeding layers. This classification drives
the seeding strategy, execution order, and test design for each module.

| Layer | Purpose | Detection Heuristic | Seeding Tool |
|-------|---------|---------------------|--------------|
| L1: Auth | Test user setup | Modules about User/Auth; SSO/OAuth references in CLAUDE.md | Auth provider CLI (e.g., Keycloak `kcadm`, Laravel `artisan tinker`, or DB seed) |
| L2: Reference Data | Admin-configured master data | User stories with "manage", "configure" by admin roles; no inbound message queue trigger | Direct DB insert via database CLI (e.g., `mongosh`, `mysql`, `psql`, `artisan tinker`) |
| L3: Transactional Data | Message-driven data | NFRs mentioning "incoming messages", "message queue", "inbound messages"; Reference section linking to MESSAGE_*.md files | Message queue publish via broker CLI (e.g., `rabbitmqadmin`) |
| L4: Side-Effect Data | Data generated as byproduct | NFRs mentioning "auto-generated", "system generated", "automatically"; modules like Activities, Audit Trail, Notifications | No seeding â€” asserted as side effects of L2/L3 operations |

## Input

This skill uses standardized input resolution. Provide:

| Argument | Required | Example | Description |
|----------|----------|---------|-------------|
| `<application>` | Yes | `hub_middleware` | Application name to locate the context folder |
| `<version>` | Yes | `v1.0.3` | Version to scope processing |
| `module:<name>` | No | `module:Location Information` | Limit to a single module |

### Application Folder Resolution

The application name is matched against root-level application folders:
1. Strip any leading `<number>_` prefix from folder names
2. Match case-insensitively
3. Accept snake_case, kebab-case, or title-case input
4. If no match found, list available applications and stop

### Auto-Resolved Paths

| File | Resolved Path |
|------|---------------|
| PRD.md | `<app_folder>/context/PRD.md` |
| Module Models | `<app_folder>/context/model/` |
| Specifications | `<app_folder>/context/specification/` |
| HTML Mockups | `<app_folder>/context/mockup/` |
| References | `<app_folder>/context/reference/` |
| Output (test) | `<app_folder>/context/test/` |

### Example Invocations

- `/testgen-functional hub_middleware v1.0.3` (all modules, up to v1.0.3)
- `/testgen-functional hub_middleware v1.0.3 module:Location Information` (one module)
- `/testgen-functional "Hub Middleware" v1.0.3 module:Employer` (title-case)

### Version and Module Filtering

- Only include user stories, NFRs, constraints, references, test instructions, and bug fixes
  from sections whose version tag is **less than or equal to** the target version
- If a module is provided (e.g., `module:Location Information`), only generate the test spec
  for that specific module. TEST_PLAN.md is still generated but scoped to that module.
- If no module is provided, process all modules (default behavior)

**Argument parsing**: The `module:` prefix is the canonical form. Also accept:
- `module:"Location Information"` (quoted, with space)
- `module:location_information` (snake_case â€” convert to title-case for matching)
- Natural language: `for Location Information module`, `only Location Information`

---

## Version Gate

Before starting any work, resolve the application folder first (see Input Resolution below), then check `CHANGELOG.md` in the application folder (`<app_folder>/CHANGELOG.md`):

1. If `<app_folder>/CHANGELOG.md` does not exist, skip this check (first-ever execution for this application).
2. If `<app_folder>/CHANGELOG.md` exists, scan all `## vX.Y.Z` headings and determine the **highest version** using semantic versioning comparison.
3. Compare the requested version against the highest version:
   - If requested version **>=** highest version: proceed normally.
   - If requested version **<** highest version: **STOP immediately**. Print: `"Version {requested} is lower than the current application version {highest} recorded in <app_folder>/CHANGELOG.md. Execution rejected."` Do NOT proceed with any work.

## Workflow

### Step 1: Parse PRD.md

Read the file and extract:

1. **Application name**: Derive from the parent folder name containing PRD.md.
   Strip leading number and underscore prefix, then title-case.
   Example: `1_hub_middleware` -> "Hub Middleware"

2. **Application initials**: First letter of each word, uppercase.
   Example: `1_hub_middleware` -> "HM"

3. **Module categories and modules**: Each `# Module Category` heading groups related modules.
   Each `## Module Name` section under a category is a module.
   Record the module name, its category, and its description (the line after the heading).

4. **User stories per module**: Lines matching `- [USxx#####] As a {Role} user, I want to...`
   Extract: tag, role, action summary, sub-items (indented lines under the story).

5. **NFRs per module**: Lines matching `- [NFRxx####] ...`
   Extract: tag, full text.

6. **Constraints per module**: Lines matching `- [CONSxx###] ...`
   Extract: tag, full text.

7. **References per module**: Lines matching `- [REFxx####] ...`
   Extract: tag, description, linked file path (if any).

8. **Test instructions per module**: Lines matching `- [TSTxx####] ...` under `### Test`
   sections. These contain human-specified test setup instructions, test data requirements,
   test edge cases, and test user configurations that MUST be incorporated into the test
   plan and specs as **additional context** on top of the standard analysis of User Stories,
   NFRs, Constraints, Module Models, HTML Mockups, and Technical Specs.
   Extract: tag (e.g., `[TSTHM0003]`), version tag, full text of each bullet point
   (including sub-bullets which provide detailed test parameters).
   Test instructions serve as human-guided test scenario hints and edge cases that the
   test spec generator should use to enrich and complement the auto-derived test scenarios.

9. **Bug fixes per module**: Content under `### Bug` sections. These document previously
   fixed bugs from prior development cycles. Each bug entry describes what was broken and
   how it was fixed. Extract: version tag, bug tag (e.g., `[BUG-024]`), description.

10. **Unique roles**: Collect all distinct roles from user stories.

11. **Version tag per item**: Each `### User Story`, `### Non Functional Requirement`,
   `### Constraint`, `### Test`, and `### Bug` section contains version blocks formatted
   as `[v1.0.x]`. Items listed under a version tag belong to that version. Track the
   version for every extracted user story, NFR, constraint, reference, test instruction,
   and bug fix. Carry this version through to the Source Artifacts table, test scenario
   Source fields, and Traceability Matrix.

12. **Deprecated item tracking**: Items marked with strikethrough in a newer version may
    have been replaced by a new item. When an item is removed in version X and replaced by
    item Y, track this replacement. Include a "Removed / Replaced" subsection in the
    Source Artifacts of the TEST_SPEC.md, following the same format used in SPEC.md:
    | ID | Type | Removed In | Replaced By | Reason |

#### 1a: Version Filtering and Strikethrough Exclusion (MANDATORY)

PRD.md is a version-controlled document. Each section has a version tag in square
brackets, e.g., `[v1.0.1]`. Items may also be marked with strikethrough (`~~`).

**Strikethrough exclusion** (always applied, regardless of version parameter):
- Any line wrapped in `~~strikethrough~~` markup MUST be excluded from processing
- This includes user stories, NFRs, constraints, references, test instructions, and bug fixes
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

#### 1b: Module Filtering (applied only when a module argument is provided)

When a `module` argument is present:

1. **Match the specified module** against the list of parsed modules (case-insensitive).
   Also accept snake_case input by converting to title-case for comparison.
2. If no module matches, stop and report the available module names to the user.
3. When module-filtered, generate TEST_PLAN.md scoped to that module and only that module's
   TEST_SPEC.md file.

---

### Step 2: Extract Project Information from CLAUDE.md (Already in Context)

CLAUDE.md is automatically loaded into context. Extract the following from it:

1. **Project name and description**
2. **Infrastructure details**:
   - Database type and version (MongoDB, MySQL, PostgreSQL)
   - Database name(s) and connection info
   - Message Queue type and version (RabbitMQ)
   - Message Queue connection info (host, port, credentials)
   - SSO/Auth type and version (Keycloak)
   - SSO connection info (host, admin credentials, CLI path)
3. **CLI tools available**: Map each infrastructure component to its CLI tool based on
   what CLAUDE.md declares. Common mappings:
   - MongoDB â†’ `mongosh` (connection string from CLAUDE.md)
   - MySQL â†’ `mysql` (host, port, credentials from CLAUDE.md)
   - PostgreSQL â†’ `psql` (host, port, credentials from CLAUDE.md)
   - RabbitMQ â†’ `rabbitmqadmin` (host, port, credentials from CLAUDE.md)
   - Keycloak â†’ `kcadm` (CLI path, host, admin credentials from CLAUDE.md)
   - Laravel artisan â†’ `php artisan` (for seeder commands, tinker, queue management)

   The skill auto-detects which tools apply from CLAUDE.md dependencies. Do not assume
   a specific tech stack â€” read it from the project context.
4. **Application dependencies**: What this application depends on (DB, MQ, SSO)
5. **Environment variable mapping**: Map each infrastructure value from CLAUDE.md to a
   standardized environment variable name. These env vars will be referenced in seeding
   scripts and helper classes so that generated Playwright tests are portable across
   machines. Common mappings:
   - Database connection string â†’ `TEST_DB_URI` (MongoDB) or `TEST_DB_HOST`, `TEST_DB_PORT`,
     `TEST_DB_USER`, `TEST_DB_PASSWORD`, `TEST_DB_NAME` (MySQL/PostgreSQL)
   - Message Queue â†’ `TEST_MQ_HOST`, `TEST_MQ_PORT`, `TEST_MQ_USER`, `TEST_MQ_PASSWORD`,
     `TEST_MQ_VHOST` (or `TEST_MQ_URL` for AMQP URL)
   - SSO/Auth â†’ `TEST_SSO_HOST`, `TEST_SSO_ADMIN_USER`, `TEST_SSO_ADMIN_PASSWORD`,
     `TEST_SSO_CLI_PATH` (e.g., path to `kcadm.bat` or `kcadm.sh`), `TEST_SSO_REALM`
   - Application â†’ `TEST_APP_BASE_URL` (base URL for Playwright navigation)
   - Additional CLI paths â†’ `TEST_PHP_PATH`, `TEST_JAVA_HOME`, `TEST_MAVEN_PATH` (as needed)

   Only include env vars for infrastructure components that actually exist in CLAUDE.md.

---

### Step 2a: Extract PRD.md Extended Sections

After extracting project information, check PRD.md for the following extended sections:

#### Design System

If PRD.md contains a `# Design System` section with a file reference:
1. Resolve and read the referenced `DESIGN_SYSTEM.md` file
2. Extract component patterns and expected visual appearances (e.g., badge styles, button patterns)
3. Use these to generate visual consistency assertions in TEST_SPEC.md (e.g., "Assert status badge has class containing 'bg-green' for Active status", "Assert buttons use rounded-lg class")

If absent, skip visual consistency assertions.

#### Architecture Principle

If PRD.md contains an `# Architecture Principle` section, extract patterns that affect test strategy:

| Pattern | Test Impact |
|---|---|
| "Event-driven" | L3 transactional data may have async propagation delay â€” tests MUST include wait/retry patterns (e.g., `await expect.poll(() => ...).toPass({ timeout: 10000 })`) for eventual consistency assertions |
| "Message driven" | Confirms L3 classification heuristics â€” modules receiving data via message queues are L3 |
| "Stateless" | Tests should handle token refresh/expiry scenarios; include JWT expiry test case |
| ACK/NACK patterns | Generate assertion steps verifying messages published to correct queues with expected correlation IDs |
| "At-least-once delivery" | Include idempotency test â€” send same message twice, verify no duplicate records |

If absent, proceed with existing layer classification heuristics.

#### High Level Process Flow

If PRD.md contains a `# High Level Process Flow` section:
1. Parse all named process flows with their ordered steps
2. Each process flow becomes an **end-to-end test scenario** (or test suite) in TEST_SPEC.md:
   - Happy path: each step â†’ a test step with specific assertions
   - Error paths (if described): each generates a separate error scenario
   - ACK/NACK patterns generate queue assertion steps (verify messages in outbound queues)
3. Process flows are the **primary source for L3 (Transactional Data) test scenarios**
4. Process flows reveal cross-module dependencies that must be included in the test execution order

If absent, derive L3 scenarios from NFRs mentioning "message queue" or "incoming message" only (existing behavior).

---

### Step 3: Load Module Models

For each module, look for `<app_folder>/context/model/{module-kebab}/model.md`

Convert module name to kebab-case:
- Lowercase the module name, replace spaces with hyphens
- Examples: "Location Information" â†’ `location-information`, "Employer" â†’ `employer`

If the model file exists, extract:

1. **Collection Catalog** (Section 2): collection names, DDD types, document types
2. **Field Details** (Section 5): field name, type, nullable, constraints per collection
3. **Embedded Document Definitions** (Section 6): embedded type name and sub-fields
4. **Enum Definitions** (Section 7): enum name and allowed values
5. **Index Recommendations** (Section 9): indexed fields (used for search/filter identification)
6. **Module Prefix**: The prefix used for collections (e.g., `LIN`, `EMP`, `QUO`)

This data is used to:
- Generate realistic sample data for seeding scripts
- Identify searchable/filterable fields for search test scenarios
- Determine collection names for DB insert/cleanup commands
- Map enum values to expected UI dropdown options

---

### Step 4: Load Specifications

For each module, look for `<app_folder>/context/specification/{module-kebab}/SPEC.md`

If found, extract:

1. **Traceability section**: Maps user stories â†’ collections â†’ mockup screens
2. **Public API** (Service Interface): Method signatures showing available operations
3. **DTOs**: Field definitions showing what the API exposes
4. **Validation rules**: Any documented validation logic
5. **Business logic rules**: Documented business rules and constraints
6. **Version tags**: If the SPEC.md traceability section uses versioned tables
   (with ID | Version | Description columns), extract the version for each item.
   Cross-reference with PRD.md version tags for consistency.

This data enriches test scenarios with:
- Expected API behavior for assertions
- Validation rules to test (boundary conditions, required fields)
- Business rule scenarios

---

### Step 5: Load Mockups

For each module, scan `<app_folder>/context/mockup/{role_snake_case}/content/{module_snake_case}*.html`

If mockup files exist, extract:

1. **DOM selectors**: IDs and classes used on key elements (tables, forms, buttons)
2. **Navigation paths**: HTMX `hx-get` routes showing page navigation flow
3. **Form field names**: Input names and types from form elements
4. **Table column headers**: `<th>` content from data tables
5. **Tab structure**: Tab names and their linked content files
6. **Action buttons**: View/Edit/Delete/Create button patterns and their targets
7. **Sidebar navigation**: Menu items and their routes for the module

This data provides:
- Actual CSS selectors for Playwright `page.locator()` calls
- Real navigation paths for `page.goto()` and click sequences
- Form field identifiers for fill operations
- Expected table column names for content assertions

---

### Step 6: Load Message References

Scan `<app_folder>/context/reference/message/MESSAGE_*.md` and `REF_*.md`

For modules classified as L3 (Transactional Data), these files provide:

1. **Message structure**: JSON schema of inbound messages
2. **Sample payloads**: Expanded JSON examples with realistic sample data
3. **Referenced sub-structures**: `$REF_*.md` references that compose the full message
4. **Metadata fields**: correlation ID, origin system, type, command, corridor info

This data is used to generate:
- Sample message JSON payloads for RabbitMQ seeding scripts
- Expected field values for asserting message-driven data in the UI

---

### Step 7: Classify Modules into Layers

For each module, apply the following classification heuristics **in order** (first match wins):

**L1: Auth** â€” Module is classified as L1 if:
- Module name is "User" or contains "Authentication", "Authorization", "SSO"
- User stories reference "profile", "password", "login", "logout"
- NFRs reference "JWT", "SSO", "Keycloak", "token", "authentication"

**L4: Side-Effect Data** â€” Module is classified as L4 if:
- Module name is "Activities", "Audit Trail", "Notification", or similar
- NFRs mention "auto-generated", "system generated", "automatically logged"
- NFRs mention "will be logged", "will be recorded automatically"
- No user stories with "manage" or "configure" actions (only "view" actions)

**L3: Transactional Data** â€” Module is classified as L3 if:
- NFRs mention "incoming messages", "message queue", "inbound messages"
- Reference section links to `MESSAGE_*.md` files
- NFRs mention "unique view ... based on incoming"
- User stories are primarily "view" and "search" (no "manage"/"configure"/"add"/"create")

**L2: Reference Data** â€” Module is classified as L2 if:
- User stories contain "manage", "configure", "add", "create", "edit", "delete"
- Actions are performed by admin roles
- No message queue triggers (no MESSAGE_*.md references)
- Data is master/reference data maintained through the UI

**Record the classification** for each module with the reasoning (which heuristic matched).

---

### Step 8: Determine Dependencies

Build a dependency graph between modules:

1. **Model references**: If a module's model references another module's collection
   (e.g., `countryCode` referencing `lin_countries`), the referencing module depends on
   the referenced module.

2. **NFR references**: If NFRs state data is "based on incoming X messages" and X is
   another module, there is a dependency.

3. **User story references**: If user stories mention "view associated X" where X is
   another module, there is a dependency.

4. **Layer ordering**: L1 â†’ L2 â†’ L3 â†’ L4 (higher layers depend on lower layers implicitly)

5. **Within-layer dependencies**: Within L2, reference data that other L2 modules depend on
   must be seeded first (e.g., Location Information before Employer, since employers have
   country codes).

**Output**: An ordered list of modules for test execution, respecting all dependencies.

---

### Step 9: Generate TEST_PLAN.md

Write `<app_folder>/context/test/TEST_PLAN.md` with the following structure:

```markdown
# E2E Test Plan: {Application Name}

**Generated**: {date}
**Source**: {PRD.md path}
**Version**: {target version or "all versions"}
**Versions Covered**: v1.0.0 â€” v{LATEST_VERSION}
**Module Filter**: {module name or "all modules"}

---

## 1. Application Overview

- **Application**: {Application Name} ({Initials})
- **Description**: {from PRD.md context line or CLAUDE.md}
- **Stack**: {from CLAUDE.md â€” e.g., "Spring Boot 3 + MongoDB + Keycloak + RabbitMQ" or "Laravel 12 + MySQL + Keycloak + RabbitMQ"}

---

## 2. Test Infrastructure

| Component | Type | CLI Tool | Connection |
|-----------|------|----------|------------|
| Database | {type + version from CLAUDE.md} | {CLI tool for that DB} | {connection string} |
| Message Queue | {type + version from CLAUDE.md} | {CLI tool for that MQ} | {AMQP URL} |
| SSO / Auth | {type + version from CLAUDE.md} | {CLI tool or artisan command} | {host URL} |

### CLI Commands Reference

{For each infrastructure component, provide the exact CLI command template with
connection parameters filled in from CLAUDE.md}

---

## 2a. Environment Variables (.env)

{Generate a `.env.example` block listing all environment variables needed by Playwright
test helpers and seeding scripts. Values come from CLAUDE.md. This block serves as the
template for each developer's local `.env` file (which is git-ignored). Only include
variables for infrastructure components that exist in CLAUDE.md.}

```dotenv
# Application
TEST_APP_BASE_URL={base URL from CLAUDE.md, e.g., http://localhost:8080}

# Database ({type from CLAUDE.md})
{If MongoDB:}
TEST_DB_URI={full connection string from CLAUDE.md}
{If MySQL or PostgreSQL:}
TEST_DB_HOST={host}
TEST_DB_PORT={port}
TEST_DB_USER={username}
TEST_DB_PASSWORD={password}
TEST_DB_NAME={database name}

# Message Queue ({type from CLAUDE.md}) â€” include only if MQ exists
TEST_MQ_HOST={host}
TEST_MQ_PORT={port}
TEST_MQ_USER={username}
TEST_MQ_PASSWORD={password}
TEST_MQ_VHOST={vhost}
TEST_MQ_URL={full AMQP URL}

# SSO / Auth ({type from CLAUDE.md}) â€” include only if SSO exists
TEST_SSO_HOST={host URL, e.g., http://localhost:8180}
TEST_SSO_ADMIN_USER={admin username}
TEST_SSO_ADMIN_PASSWORD={admin password}
TEST_SSO_CLI_PATH={absolute path to CLI tool, e.g., /opt/keycloak/bin/kcadm.sh}
TEST_SSO_REALM={test realm name}
```

**Important**: The `.env` file MUST be added to `.gitignore`. The `.env.example` file
(with placeholder descriptions, NOT actual credentials) is committed to the repository
so that other developers know which variables to configure.

---

## 3. Test Users

{Populate this table from TWO sources:
1. `### Test` sections in PRD.md â€” human-specified test users with exact credentials
   and roles. These take precedence and MUST be used as-is (e.g., the Authentication
   module's `### Test` section may specify exact usernames, passwords, and roles).
2. Auto-derived from user story roles â€” for any role NOT already covered by a
   `### Test` section, generate a test user entry.}

| User | Role | Purpose | Seeding Method | Source |
|------|------|---------|----------------|--------|
| {username} | {role} | {what this user tests} | {Keycloak CLI / DB seed} | {PRD.md `### Test` or Auto-derived} |

---

## 4. Layer Classification Summary

| Module | Category | Layer | Seeding Strategy | Versions | Dependencies |
|--------|----------|-------|-----------------|----------|--------------|
| {module} | {System/Business} | {L1/L2/L3/L4} | {strategy} | {versions from PRD.md} | {deps} |

---

## 5. Execution Order

{Ordered list of modules, respecting layer ordering and within-layer dependencies}

1. **L1 â€” Auth Setup**: {modules}
2. **L2 â€” Reference Data**: {modules in dependency order}
3. **L3 â€” Transactional Data**: {modules in dependency order}
4. **L4 â€” Side-Effect Assertions**: {modules}

---

## 6. Table of Contents

{List all test spec files in strict dependency order derived from the dependency graph
built in Step 8. A module only appears after ALL modules it depends on have been listed.
Apply a topological sort within each layer, then order layers L1 â†’ L2 â†’ L3 â†’ L4.
Group by layer in the TOC for readability, but the numbering is globally sequential
and reflects the dependency-resolved execution order throughout.}

### L1 â€” Auth Setup

1. [{Module Name}]({module-kebab}/TEST_SPEC.md) â€” Versions: {comma-separated versions} â€” [Summary](#module-{module-anchor})

### L2 â€” Reference Data

{List L2 modules in topological order: if Module B depends on Module A, Module A comes first.}

2. [{Module Name}]({module-kebab}/TEST_SPEC.md) â€” Versions: {versions} â€” [Summary](#module-{module-anchor})
3. [{Module Name}]({module-kebab}/TEST_SPEC.md) â€” Versions: {versions} â€” [Summary](#module-{module-anchor})

### L3 â€” Transactional Data

{List L3 modules in topological order by their inter-module dependencies.}

4. [{Module Name}]({module-kebab}/TEST_SPEC.md) â€” Versions: {versions} â€” [Summary](#module-{module-anchor})

### L4 â€” Side-Effect Assertions

{List L4 modules after all upstream L1â€“L3 modules they assert against.}

5. [{Module Name}]({module-kebab}/TEST_SPEC.md) â€” Versions: {versions} â€” [Summary](#module-{module-anchor})

---

## 7. Module Summaries

{One subsection per module. The order of subsections MUST follow the topological sort of
the dependency graph (Step 8): a module's subsection only appears after all modules it
depends on have already appeared. This is the same order as the TOC in Section 6.
Each subsection summarizes what the module's TEST_SPEC.md covers, what data it seeds,
what it depends on, and a breakdown of its test scenarios by type.}

### Module: {Module Name} {#module-{module-anchor}}

**Layer**: {L1/L2/L3/L4} â€” {layer purpose}
**Seeding Strategy**: {Keycloak CLI / DB Insert / MQ Publish / No seeding (side effect)}
**Spec File**: [{module-kebab}/TEST_SPEC.md]({module-kebab}/TEST_SPEC.md)

**Dependencies**:

| Prerequisite Module | Layer | Reason |
|--------------------|-------|--------|
| {module name} | {L1/L2/L3} | {why this module must be seeded first} |

_(None â€” this module has no prerequisites.)_ â† use when no deps

**Data Seeded**:

| Collection / Entity | Record Count | Key Sample Fields |
|--------------------|-------------|-------------------|
| {collection} | {count} | {field: value, ...} |

_(No seeding required â€” data is a side effect of upstream operations.)_ â† use for L4

**Test Scenarios Summary**:

| Type | Count | Description |
|------|-------|-------------|
| Navigation | {n} | Verify sidebar link reaches the {Module Name} screen |
| Search | {n} | Search by {param1}, {param2}, ... |
| View / Detail | {n} | View detail of {entity} with tabs: {tab names} |
| CRUD â€” Create | {n} | Create new {entity} with required fields |
| CRUD â€” Edit | {n} | Update {field} of an existing {entity} |
| CRUD â€” Delete | {n} | Delete {entity} with confirmation dialog |
| Validation | {n} | Required fields, {constraint description}, ... |
| Mapping | {n} | Map {entity A} to {entity B} |
| Toggle | {n} | Activate / Deactivate {entity} |
| History / Audit | {n} | View change history of {entity} |
| Raw Message | {n} | View raw inbound message payload |
| Pagination | {n} | Paginate {entity} list, change page size |
| Regression | {n} | Verify previously fixed bugs still hold |
| Test Instruction | {n} | Human-guided scenarios from `### Test` section |
| **Total** | **{total}** | |

_{Omit rows for types with 0 scenarios.}_

**Roles Tested**: {comma-separated list of roles exercised in this module's scenarios}

**Key Assertions**:
- {Brief bullet summarising the most important expected behaviours to verify}
- {e.g., "Dropdown for Country Code is populated from Location Information reference data"}
- {e.g., "Status badge changes colour immediately after toggle without page reload"}

---

{Repeat the Module subsection above for every module, in execution order}

---

## 8. Global Setup

### 8a. Auth Setup (L1)

{Keycloak CLI commands to create test realm, clients, roles, and users}

### 8b. Reference Data Setup (L2)

{Summary of L2 modules and their seeding order}

### 8c. Message Publishing (L3)

{Summary of L3 modules and the messages to publish}

---

## 9. Global Teardown

{Cleanup strategy â€” reverse order of setup}

### 9a. Database Cleanup

{CLI commands to drop test data from each collection/table, in reverse dependency order}

### 9b. Message Queue Cleanup

{CLI commands to purge test queues}

### 9c. Auth Cleanup

{CLI commands to remove test users/realm}
```

---

### Step 10: Generate Per-Module TEST_SPEC.md

For each module (or the filtered module), write `<app_folder>/context/test/{module-kebab}/TEST_SPEC.md`:

```markdown
# TEST_SPEC: {Module Name}

**Application**: {Application Name} ({Initials})
**Module**: {Module Name}
**Category**: {System Module / Business Module}
**Layer**: {L1 / L2 / L3 / L4} â€” {layer purpose}
**Seeding Strategy**: {Keycloak CLI / DB Insert / MQ Publish / No seeding (side effect)}
**Generated**: {date}
**Version**: {target version or "all versions"}
**Versions Covered**: {comma-separated list of versions present in this module}

---

## 1. Module Overview

{Module description from PRD.md}

### Layer Classification Reasoning

{Why this module was classified into its layer â€” which heuristic matched}

### Source Artifacts

| Artifact Type | Reference | Version |
|---------------|-----------|---------|
| User Story    | {USHM tag} | {v1.0.x from PRD.md} |
| NFR           | {NFRHM tag} | {v1.0.x} |
| Constraint    | {CONSHM tag} | {v1.0.x} |
| Test          | {TSTHM tag} | {v1.0.x} |
| Bug Fix       | {BUG tag} | {v1.0.x} |

| Artifact | Path | Status |
|----------|------|--------|
| User Stories | {PRD.md path} | Found |
| Module Model | {model path or "Not found"} | {Found/Not found} |
| Specification | {spec path or "Not found"} | {Found/Not found} |
| Mockup | {mockup path or "Not found"} | {Found/Not found} |
| Message Reference | {message ref path or "Not found"} | {Found/Not found} |

{If any items were deprecated/removed and replaced, include:}

### Removed / Replaced

| ID | Type | Removed In | Replaced By | Reason |
|---|---|---|---|---|
| {old ID} | {User Story/NFR/Constraint} | {version removed} | {new ID or "â€”"} | {reason} |

### Test Instructions (from PRD.md)

{If the module has a `### Test` section in PRD.md, list all tagged test instructions here.
These are human-specified test scenario hints, test edge cases, test data requirements,
and test setup instructions that serve as **additional context** on top of the standard
auto-derived test scenarios from User Stories, NFRs, Constraints, Module Models, HTML
Mockups, and Technical Specs. They MUST be incorporated into the test scenarios in
Section 4.

Test instructions guide the test spec generator on specific scenarios or edge cases that
a human tester has identified as important. They do NOT replace the auto-derived scenarios
but complement them â€” ensuring critical test paths are not missed.

When a test instruction specifies exact test data (e.g., usernames, passwords, field values),
use those values as-is in the relevant seeding scripts and test scenarios.}

| Tag | Version | Instruction |
|-----|---------|-------------|
| {TSTHM tag} | {v1.0.x} | {Full text of the test instruction from PRD.md} |

{Example: `[TSTHM0003]` specifies exact test user credentials and roles for the Auth
module â€” these MUST be used in the L1 Auth seeding script instead of auto-generated
user data. `[TSTHA0006]` describes specific validation edge cases for the Employer
module â€” these should generate additional VAL- test scenarios in Section 4.}

_(No test instructions for this module.)_ â† use when the `### Test` section is empty or has no tagged items

### Bug Fix Regression Coverage

{If the module has a `### Bug` section in PRD.md, list each bug fix and its corresponding
regression test requirement. Each bug fix MUST have at least one test scenario that verifies
the fix still holds â€” preventing the same bug from reappearing.}

| Bug Tag | Version | Description | Regression Scenario |
|---------|---------|-------------|-------------------|
| {BUG-XXX} | {v1.0.x} | {Bug fix description from PRD.md} | {REG-prefix-NNN: scenario ID in Section 4} |

_(No bug fixes recorded for this module.)_ â† use when the `### Bug` section is empty or absent

---

## 2. Prerequisites

{What must exist before tests for this module can run}

| Prerequisite | Module | Layer | How to Verify |
|-------------|--------|-------|--------------|
| {description} | {module name} | {L1/L2/L3} | {verification method} |

---

## 3. Data Seeding

### 3a. Seeding Script

{Based on layer classification, generate appropriate seeding commands}

**IMPORTANT**: All seeding scripts MUST reference environment variables (from Section 2a
of TEST_PLAN.md) instead of hardcoded paths, credentials, or connection strings. This
ensures Playwright tests are portable across developer machines. Use `$ENV_VAR` syntax
in bash command templates and note that the actual Playwright helper code should read
these from `process.env.*` via a `.env` file.

**For L1 (Auth)** â€” use the auth provider's CLI or framework seeder:

*If Keycloak (detected from CLAUDE.md):*
```bash
# Create test user in Keycloak
# Env vars: TEST_SSO_CLI_PATH, TEST_SSO_HOST, TEST_SSO_ADMIN_USER, TEST_SSO_ADMIN_PASSWORD, TEST_SSO_REALM
"$TEST_SSO_CLI_PATH" config credentials --server "$TEST_SSO_HOST" --realm master --user "$TEST_SSO_ADMIN_USER" --password "$TEST_SSO_ADMIN_PASSWORD"
"$TEST_SSO_CLI_PATH" create users -r "$TEST_SSO_REALM" -s username={user} -s enabled=true ...
```

*If Laravel with DB-backed auth (detected from CLAUDE.md):*
```bash
# Seed test users via artisan
# Env vars: TEST_PHP_PATH (optional, defaults to 'php')
php artisan tinker --execute="
    \App\Models\User::factory()->create([
        'name' => '{user}', 'email' => '{email}', 'password' => bcrypt('{pass}')
    ])->assignRole('{role}');
"
```

**For L2 (Reference Data / DB Insert)** â€” use the database CLI matching CLAUDE.md:

*If MongoDB:*
```bash
# Env vars: TEST_DB_URI
mongosh "$TEST_DB_URI" --eval '
db.{collection}.insertMany([
  {sample document based on model fields},
  ...
])
'
```

*If MySQL:*
```bash
# Env vars: TEST_DB_HOST, TEST_DB_PORT, TEST_DB_USER, TEST_DB_PASSWORD, TEST_DB_NAME
mysql -h "$TEST_DB_HOST" -P "$TEST_DB_PORT" -u "$TEST_DB_USER" -p"$TEST_DB_PASSWORD" "$TEST_DB_NAME" -e "
INSERT INTO {table} ({columns}) VALUES
  ({sample row based on model fields}),
  ...;
"
```

*If PostgreSQL:*
```bash
# Env vars: TEST_DB_HOST, TEST_DB_PORT, TEST_DB_USER, TEST_DB_PASSWORD, TEST_DB_NAME
psql "postgresql://$TEST_DB_USER:$TEST_DB_PASSWORD@$TEST_DB_HOST:$TEST_DB_PORT/$TEST_DB_NAME" -c "
INSERT INTO {table} ({columns}) VALUES
  ({sample row based on model fields}),
  ...;
"
```

*If Laravel (alternative to raw CLI):*
```bash
php artisan db:seed --class=Test{Module}Seeder
```

**For L3 (Transactional Data / MQ Publish)** â€” use the message broker CLI:

*If RabbitMQ:*
```bash
# Env vars: TEST_MQ_HOST, TEST_MQ_PORT, TEST_MQ_USER, TEST_MQ_PASSWORD, TEST_MQ_VHOST
rabbitmqadmin -H "$TEST_MQ_HOST" -P "$TEST_MQ_PORT" -u "$TEST_MQ_USER" -p "$TEST_MQ_PASSWORD" -V "$TEST_MQ_VHOST" publish exchange={exchange} routing_key={key} payload='{
  {sample message JSON from MESSAGE_*.md}
}'
```

**For L4 (Side Effect)**:
```
No seeding required â€” data is generated as a side effect of L2/L3 operations.
Assert existence after upstream tests complete.
```

### 3b. Seeded Data Summary

| Collection/Entity | Record Count | Key Fields | Sample Values |
|-------------------|-------------|------------|---------------|
| {collection} | {count} | {key fields from model} | {sample values} |

---

## 4. Test Scenarios

{Derived from user stories, grouped by test type. Each scenario includes:
- Scenario ID (module prefix + sequential number)
- Description
- Source user story tag(s)
- Role performing the test
- Preconditions
- Steps (numbered)
- Expected results
- Selectors (from mockups, if available)}

### 4a. Navigation Tests

{Derived from mockup sidebar links â€” verify the module screen is accessible}

#### NAV-{prefix}-001: Navigate to {Module} screen

- **Source**: Sidebar navigation [v1.0.x]
- **Role**: {role}
- **Preconditions**: User is logged in
- **Steps**:
  1. Click "{Module Name}" in the sidebar navigation
  2. Wait for content area to load
- **Expected**:
  - URL contains `/{role_snake_case}/{module_snake_case}`
  - Page title/heading shows "{Module Name}"
  - {If mockup exists: specific heading selector from mockup}
- **Selectors** (from mockup):
  - Sidebar link: `{selector from sidebar HTML}`
  - Page heading: `{selector from content HTML}`

### 4b. Search Tests

{Derived from user stories matching "search for X based on Y"}

#### SRCH-{prefix}-001: Search {entity} by {parameter}

- **Source**: {user story tag} [v1.0.x]
- **Role**: {role}
- **Preconditions**: {seeded data exists}
- **Steps**:
  1. Navigate to {module} screen
  2. Enter "{sample value}" in the {parameter} filter field
  3. Click "Search" / press Enter
  4. Wait for results to load
- **Expected**:
  - Results table shows matching records
  - Each result row contains the search term in the {parameter} column
  - Result count is displayed (e.g., "Showing 1-N of N results")
- **Selectors** (from mockup):
  - Filter input: `{selector}`
  - Search button: `{selector}`
  - Results table: `{selector}`
  - Result count text: `{selector}`

### 4c. View/Detail Tests

{Derived from user stories matching "view details of X"}

#### VIEW-{prefix}-001: View {entity} details

- **Source**: {user story tag} [v1.0.x]
- **Role**: {role}
- **Preconditions**: {entity exists in system}
- **Steps**:
  1. Navigate to {module} list screen
  2. Click "View" action on a record
  3. Wait for detail page to load
- **Expected**:
  - Detail page shows all expected fields
  - {For each field from model: field label and value are visible}
  - Back button navigates to list
- **Selectors** (from mockup):
  - View button: `{selector}`
  - Detail card: `{selector}`
  - Back button: `{selector}`

### 4d. CRUD Tests

{Derived from user stories matching "manage", "configure", "add/create", "edit/update", "delete"}

#### CRUD-{prefix}-001: Create new {entity}

- **Source**: {user story tag} [v1.0.x]
- **Role**: {role}
- **Preconditions**: User has create permission
- **Steps**:
  1. Navigate to {module} list screen
  2. Click "Add New" button
  3. Fill in required fields:
     {For each required field from model:}
     - {field name}: "{sample value}"
  4. Click "Save" / "Submit"
- **Expected**:
  - Success notification appears
  - Redirected to list or detail screen
  - New record appears in list
- **Form Fields** (from mockup/model):
  | Field | Selector | Type | Required | Sample Value |
  |-------|----------|------|----------|--------------|
  | {field} | {selector} | {input type} | {yes/no} | {value} |

#### CRUD-{prefix}-002: Edit existing {entity}

- **Source**: {user story tag} [v1.0.x]
- **Role**: {role}
- **Preconditions**: {entity exists}
- **Steps**:
  1. Navigate to {module} list or detail screen
  2. Click "Edit" action
  3. Modify field: {field name} = "{new value}"
  4. Click "Save"
- **Expected**:
  - Success notification appears
  - Updated value is reflected in detail/list view
  - {Read-only fields remain unchanged}

#### CRUD-{prefix}-003: Delete {entity}

- **Source**: {user story tag} [v1.0.x]
- **Role**: {role}
- **Preconditions**: {entity exists}
- **Steps**:
  1. Navigate to {module} list screen
  2. Click "Delete" action on a record
  3. Confirm deletion in dialog
- **Expected**:
  - Confirmation dialog appears before deletion
  - Record is removed from list after confirmation
  - {If soft delete: record is flagged, not physically removed}

### 4e. Validation Tests

{Derived from constraints, NFRs, spec validation rules, and model field constraints}

#### VAL-{prefix}-001: Required field validation on {entity} create

- **Source**: {constraint/NFR tag} [v1.0.x]
- **Role**: {role}
- **Preconditions**: None
- **Steps**:
  1. Navigate to create {entity} screen
  2. Leave all required fields empty
  3. Click "Save"
- **Expected**:
  - Form is NOT submitted
  - Validation errors appear for each required field:
    {For each required field from model:}
    - {field name}: shows required error message

#### VAL-{prefix}-002: {Specific constraint validation}

- **Source**: {constraint tag} [v1.0.x]
- **Role**: {role}
- **Steps**: {specific to the constraint}
- **Expected**: {specific validation behavior}

### 4f. Mapping Tests

{Derived from user stories matching "map X to Y"}

### 4g. Toggle Tests

{Derived from user stories matching "activate/deactivate"}

#### TOG-{prefix}-001: Toggle {entity} status

- **Source**: {user story tag}
- **Role**: {role}
- **Steps**:
  1. Navigate to {module} screen
  2. Find an active {entity}
  3. Click the toggle/deactivate control
  4. Confirm if prompted
- **Expected**:
  - Status changes from Active to Inactive (or vice versa)
  - Visual indicator updates (badge color, toggle state)

### 4h. History/Audit Tests

{Derived from user stories matching "view history", "view changes", "audit"}

#### HIST-{prefix}-001: View {entity} change history

- **Source**: {user story tag}
- **Role**: {role}
- **Preconditions**: {entity has been modified at least once}
- **Steps**:
  1. Navigate to {entity} detail screen
  2. Click "History" tab or link
  3. Wait for history records to load
- **Expected**:
  - History table shows chronological list of changes
  - Each entry shows: change type, field changed, old value, new value, timestamp, changed by
  - Most recent changes appear first

### 4i. Raw Message View Tests

{Derived from user stories referencing "view raw message" â€” typically for L3 modules}

#### RAW-{prefix}-001: View raw inbound message

- **Source**: {user story tag}
- **Role**: {role}
- **Steps**:
  1. Navigate to {entity} detail screen
  2. Click "Raw Message" tab
  3. Wait for raw data to load
- **Expected**:
  - Raw JSON message is displayed
  - JSON is formatted/syntax-highlighted
  - Message contains expected fields from MESSAGE_*.md structure

### 4j. Pagination Tests

{Applied to every list screen â€” verify pagination works correctly}

#### PAGE-{prefix}-001: Verify pagination on {entity} list

- **Source**: General requirement (all list screens must paginate)
- **Role**: {role}
- **Preconditions**: More than 10 {entities} exist in system
- **Steps**:
  1. Navigate to {module} list screen
  2. Verify default page shows 10 items
  3. Click "Next" page button
  4. Verify next page loads with different records
  5. Change page size to 25
  6. Verify 25 items are displayed
- **Expected**:
  - "Showing X-Y of Z results" text is accurate
  - Page navigation buttons work correctly
  - Page size selector changes the number of visible rows

### 4k. Regression Tests

{Derived from `### Bug` sections in PRD.md. For each bug fix recorded in the module,
generate a regression test scenario that verifies the fix still holds. This prevents
previously fixed bugs from reappearing during redevelopment.}

#### REG-{prefix}-001: Verify fix for {BUG-XXX}

- **Source**: {BUG-XXX} [v1.0.x] from `### Bug` section
- **Bug Description**: {description of what was broken and how it was fixed}
- **Role**: {role â€” infer from the bug context or use the most common module role}
- **Preconditions**: {relevant seeded data exists}
- **Steps**:
  1. {Steps that would have triggered the original bug}
  2. {Navigate to the affected screen/feature}
  3. {Perform the action that was broken}
- **Expected**:
  - {The corrected behavior as described in the bug fix}
  - {The bug does NOT reappear â€” the fix is still in effect}

{Repeat for each bug fix in the module's `### Bug` section.
If no `### Bug` section exists for this module, omit Section 4k entirely.}

### 4l. Test Instruction Scenarios

{Derived from tagged `### Test` items in PRD.md. These are human-guided test scenarios
and edge cases that complement the auto-derived scenarios above. Each tagged test
instruction (`[TSTxx####]`) should produce one or more test scenarios that cover the
specific test paths, edge cases, or setup requirements described by the human tester.

Test instruction scenarios may overlap with auto-derived scenarios (e.g., a test
instruction about validation edge cases may produce scenarios similar to Section 4e).
When overlap occurs, merge the human-guided details INTO the existing auto-derived
scenario rather than creating a duplicate. Add the TST tag as an additional Source
reference. Only create a NEW scenario in this section when the test instruction describes
a test path not already covered by any auto-derived scenario.}

#### TSTI-{prefix}-001: {Test instruction description}

- **Source**: {TST tag} [v1.0.x] from `### Test` section
- **Instruction**: {Full text of the tagged test instruction}
- **Role**: {role â€” infer from instruction context}
- **Preconditions**: {relevant seeded data or setup}
- **Steps**:
  1. {Steps derived from the human test instruction}
  2. {Include specific values/data mentioned in the instruction}
- **Expected**:
  - {Expected behavior described or implied by the instruction}

{Repeat for each tagged test instruction in the module's `### Test` section.
If no tagged items exist in `### Test`, omit Section 4l entirely.}

---

## 5. Data Cleanup

### 5a. Cleanup Script

{Reverse of seeding â€” remove all test data}

**IMPORTANT**: Cleanup scripts MUST use the same environment variables as seeding scripts
(from Section 2a of TEST_PLAN.md). Never hardcode paths, credentials, or connection strings.

**For L2 (DB cleanup)** â€” use the database CLI matching CLAUDE.md:

*If MongoDB:*
```bash
# Env vars: TEST_DB_URI
mongosh "$TEST_DB_URI" --eval '
db.{collection}.deleteMany({ _testData: true })
'
```

*If MySQL:*
```bash
# Env vars: TEST_DB_HOST, TEST_DB_PORT, TEST_DB_USER, TEST_DB_PASSWORD, TEST_DB_NAME
mysql -h "$TEST_DB_HOST" -P "$TEST_DB_PORT" -u "$TEST_DB_USER" -p"$TEST_DB_PASSWORD" "$TEST_DB_NAME" -e "
DELETE FROM {table} WHERE _test_data = 1;
"
```

*If PostgreSQL:*
```bash
# Env vars: TEST_DB_HOST, TEST_DB_PORT, TEST_DB_USER, TEST_DB_PASSWORD, TEST_DB_NAME
psql "postgresql://$TEST_DB_USER:$TEST_DB_PASSWORD@$TEST_DB_HOST:$TEST_DB_PORT/$TEST_DB_NAME" -c "
DELETE FROM {table} WHERE _test_data = true;
"
```

*If Laravel (alternative):*
```bash
php artisan test:cleanup --module={module}
```

**For L3 (Queue cleanup)** â€” use the message broker CLI:

*If RabbitMQ:*
```bash
# Env vars: TEST_MQ_HOST, TEST_MQ_PORT, TEST_MQ_USER, TEST_MQ_PASSWORD, TEST_MQ_VHOST
rabbitmqadmin -H "$TEST_MQ_HOST" -P "$TEST_MQ_PORT" -u "$TEST_MQ_USER" -p "$TEST_MQ_PASSWORD" -V "$TEST_MQ_VHOST" purge queue name={queue_name}
```

### 5b. Cleanup Order

{Reverse dependency order â€” clean dependents first, then dependencies}

1. {last module in dependency order}
2. ...
3. {first module}

---

## 6. Traceability Matrix

| Test Scenario ID | User Story | Bug Fix | Test Instruction | Version | NFR(s) | Constraint(s) | Test Type |
|-----------------|------------|---------|-----------------|---------|--------|---------------|-----------|
| NAV-{prefix}-001 | â€” | â€” | â€” | â€” | â€” | â€” | Navigation |
| SRCH-{prefix}-001 | {tag} | â€” | â€” | v1.0.x | â€” | â€” | Search |
| VIEW-{prefix}-001 | {tag} | â€” | â€” | v1.0.x | â€” | â€” | View |
| CRUD-{prefix}-001 | {tag} | â€” | â€” | v1.0.x | â€” | â€” | Create |
| CRUD-{prefix}-002 | {tag} | â€” | â€” | v1.0.x | â€” | â€” | Edit |
| CRUD-{prefix}-003 | {tag} | â€” | â€” | v1.0.x | â€” | â€” | Delete |
| VAL-{prefix}-001 | â€” | â€” | {TST tag or â€”} | v1.0.x | â€” | {tag} | Validation |
| TOG-{prefix}-001 | {tag} | â€” | â€” | v1.0.x | â€” | â€” | Toggle |
| HIST-{prefix}-001 | {tag} | â€” | â€” | v1.0.x | â€” | â€” | History |
| RAW-{prefix}-001 | {tag} | â€” | â€” | v1.0.x | â€” | â€” | Raw Message |
| PAGE-{prefix}-001 | â€” | â€” | â€” | â€” | â€” | â€” | Pagination |
| REG-{prefix}-001 | â€” | {BUG-XXX} | â€” | v1.0.x | â€” | â€” | Regression |
| TSTI-{prefix}-001 | â€” | â€” | {TST tag} | v1.0.x | â€” | â€” | Test Instruction |
```

---

### Step 11: Output Summary

After generation, print a summary:

```
Test Specification Generation Complete
=======================================
Application: {App Name} ({Initials})
Target Version: {version or "latest (all versions)"}
Module Filter: {module name or "all modules"}
Output: {output path}/

Filtering Summary:
- User stories included: {count}
- User stories excluded (strikethrough): {count}
- User stories excluded (version filter): {count}
- User stories excluded (module filter): {count}
- NFRs/Constraints included: {count}
- NFRs/Constraints excluded: {count}

Layer Classification:
| Layer | Modules | Count |
|-------|---------|-------|
| L1: Auth | {modules} | {count} |
| L2: Reference Data | {modules} | {count} |
| L3: Transactional Data | {modules} | {count} |
| L4: Side-Effect Data | {modules} | {count} |

Files generated:
- TEST_PLAN.md
- {module-kebab}/TEST_SPEC.md (Ã— {N} modules)

| Module | Layer | Scenarios | Spec File |
|--------|-------|-----------|-----------|
| {module} | {layer} | {count} | {module-kebab}/TEST_SPEC.md |

Total: {N} files, {M} test scenarios
```

---

## Changelog Append

After all test specification files are successfully generated, append an entry to `CHANGELOG.md` in the application folder (`<app_folder>/CHANGELOG.md`):

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
5. Row format: `| {YYYY-MM-DD} | {application_name} | testgen-functional | {module or "All"} | Generated Playwright E2E test specifications |`
6. **Never modify or delete existing rows.**

## Important Rules

### Generic Design
- **No hardcoded module names**: Module names, collection names, prefixes, and message types
  are ALL derived from input artifacts. Never hardcode "Employer", "Quota", etc.
- **No hardcoded collection prefixes**: Read the prefix from the model's Module Prefix Map.
- **No hardcoded message types**: Read message types from MESSAGE_*.md files.
- **Infrastructure from CLAUDE.md**: CLI paths, connection strings, and credentials come
  from CLAUDE.md. Use generic placeholders if CLAUDE.md is not found.
- **Environment variable portability**: All seeding scripts, cleanup scripts, and CLI
  command templates in TEST_PLAN.md and TEST_SPEC.md MUST reference environment variables
  (e.g., `$TEST_DB_URI`, `$TEST_SSO_CLI_PATH`) instead of hardcoded values. The env var
  names and their values from CLAUDE.md are documented in TEST_PLAN.md Section 2a. This
  ensures the generated test blueprints are portable â€” developers configure their local
  `.env` file once and all test helpers work regardless of machine-specific paths.

### Document Quality
- **Documents, not code**: Output is Markdown spec documents. Never generate Playwright
  JavaScript/TypeScript code.
- **Actionable steps**: Each test scenario must have specific enough steps that a developer
  can implement the Playwright test without ambiguity.
- **Real selectors**: When mockup HTML files exist, extract actual CSS selectors, IDs, and
  classes. Do not invent selectors.
- **Real sample data**: When model files exist, use field names, types, enum values, and
  constraints to generate realistic sample data. Do not use generic placeholders.
- **Real message payloads**: When MESSAGE_*.md files exist, use the expanded sample JSON
  as the basis for MQ seeding payloads.

### Parsing Rules
- **Strikethrough items MUST always be excluded**: Lines wrapped in `~~` are deprecated/removed.
- **Version filtering**: When a target version is provided, only include items from sections
  with version tags <= target version. This applies to all section types: User Story, NFR,
  Constraint, Reference, Test, and Bug.
- **Test instructions from PRD.md are authoritative**: When a `### Test` section specifies
  exact test users, credentials, or setup procedures, use them as-is. Do not override with
  auto-generated values. Tagged test instructions (`[TSTxx####]`) provide human-guided
  test scenarios and edge cases that MUST be incorporated into the test spec â€” either by
  merging into existing auto-derived scenarios or by creating new TSTI-* scenarios.
- **Test instructions are additive, not exclusive**: Test instructions complement the
  standard auto-derived scenarios from User Stories, NFRs, Constraints, Models, Mockups,
  and Specs. They do NOT replace or limit the auto-derived scenarios. Think of them as
  "the human tester also wants to make sure these specific things are tested."
- **Bug fixes MUST have regression coverage**: Every bug fix in a `### Bug` section must
  produce at least one REG-* test scenario in the module's TEST_SPEC.md.
- **Version + module are independent axes**: Both may be combined freely. A story must
  satisfy BOTH filters to be included.

### Layer Classification
- **Classification order matters**: Check L1 first, then L4, then L3, then L2 (L2 is the
  default/fallback).
- **One layer per module**: Each module belongs to exactly one layer.
- **Record reasoning**: Always document which heuristic matched for each classification.

### Dependencies
- **Respect execution order**: L1 â†’ L2 â†’ L3 â†’ L4. Within each layer, respect inter-module
  dependencies.
- **Seeding before testing**: All prerequisite data must be seeded before a module's tests run.
- **Cleanup in reverse order**: Clean up in reverse dependency order to avoid foreign key
  or reference violations.

### Traceability
- **Every test scenario maps to at least one source**: User story, NFR, constraint, or
  general requirement (like pagination).
- **Every user story should produce at least one test scenario**: If a user story has no
  corresponding test scenario, flag it in the traceability matrix.
- **Traceability matrix must be complete**: No gaps between user stories and test coverage.

### Mockup Integration
- **Selector accuracy**: Only reference selectors that actually exist in the mockup HTML.
  If no mockup exists, omit the Selectors section from test scenarios.
- **Navigation paths**: Use actual HTMX routes from mockups for navigation steps.
- **Form fields**: Use actual input names and types from mockup forms.

### Version Tracking in Output
- **Version tags in Source Artifacts**: Every user story, NFR, and constraint in the
  Source Artifacts table must include its version from PRD.md.
- **Version tags in test scenarios**: The "Source" field in each test scenario must
  include the version tag (e.g., `USHM00228 [v1.0.3]`).
- **Version column in Traceability Matrix**: The traceability matrix must include a
  Version column showing which version introduced each test scenario's source requirement.
- **Removed / Replaced tracking**: When items are deprecated/removed in a newer version
  and replaced by new items, include a "Removed / Replaced" subsection in Source Artifacts.
- **Versions Covered field**: Both TEST_PLAN.md and TEST_SPEC.md must include a
  "Versions Covered" field showing the range of versions included.

### Following Existing Patterns
- Same frontmatter format as mockgen-tailwind, specgen-spring-jpa-jtehtmx, and specgen-laravel-eloquent-bladehtmx skills
- Same argument parsing conventions (module:, version, path)
- Same version filtering and strikethrough exclusion logic
- Same output summary format (table-based, with file counts)
