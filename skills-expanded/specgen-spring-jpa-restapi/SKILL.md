---
name: specgen-spring-jpa-restapi
model: claude-opus-4-8
effort: high
description: >
  Generate a detailed specification document for building a Spring Boot 3 REST API
  application with Spring Modulith packaging. Database (MongoDB, PostgreSQL, MySQL, or none),
  authentication (Keycloak OAuth2 Resource Server, Spring Security JWT, or none), scheduling
  (Quartz + Spring Batch or none), and messaging (RabbitMQ pub/sub or none) are configurable
  based on user input.
  Standardized input: application name (mandatory), version (mandatory), module (optional).
  Use this skill whenever the user asks to create a spec, specification, blueprint, or
  technical design document for a new Spring Boot REST API application.
  Also trigger when the user says things like "spec out a new REST API project",
  "design a Spring Boot API skeleton", "write a technical spec for my new API",
  "scaffold spec for a REST API", or any request for a specification document
  describing a Spring Boot REST API application. Even if the user only mentions
  a subset of the stack (e.g., "Spring Boot API" or "Spring REST with MySQL" or
  "Spring Boot API with Keycloak"), this skill likely applies â€” ask and confirm.
---

# Spring Boot REST API Specification Generator

This skill generates a comprehensive specification document (Markdown) that serves as a
blueprint for building a Spring Boot 3 REST API application. The spec is intended to be
followed by a developer or a coding agent to produce a fully functional project scaffold.

The specification does NOT generate code. It produces a detailed, opinionated technical
document describing every layer of the application â€” from Maven configuration to controller
endpoints to security filter chains â€” so that implementation becomes a mechanical exercise.

## Technology Stack

### Core Stack (Always Included)

These are the fixed versions the spec targets. Do not deviate unless the user explicitly
requests different versions.

| Component          | Version   |
|--------------------|-----------|
| Java JDK           | 21        |
| Spring Boot        | 3.5.7     |
| Maven              | 4.0.0     |

### Optional Integration Versions

Include in the version table only when the corresponding integration is selected.

| Component          | Version   | When Selected        |
|--------------------|-----------|----------------------|
| MongoDB            | 8.0.19    | Database = MongoDB   |
| PostgreSQL         | 17.x      | Database = PostgreSQL|
| MySQL              | 8.4.x     | Database = MySQL     |
| Keycloak           | 26.5.3    | Auth = Keycloak      |
| RabbitMQ           | 4.x       | Messaging = yes OR Remote Partitioning = yes |

## Core Dependencies

The spec must include these in the Maven configuration section (always):

- Spring Web (starter-web)
- Spring Modulith (core, events-api)
- Lombok
- Spring Boot DevTools
- MapStruct (with annotation processor)
- Jackson (included via starter-web, for JSON serialization)
- SpringDoc OpenAPI (`springdoc-openapi-starter-webmvc-ui`) for API documentation

### Conditional Dependencies

**If Database = MongoDB:**
- Spring Data MongoDB (`spring-boot-starter-data-mongodb`)
- MongoDB Driver
- Spring Modulith starter-mongodb (`spring-modulith-starter-mongodb`)

**If Database = PostgreSQL or MySQL:**
- Spring Data JPA (`spring-boot-starter-data-jpa`)
- PostgreSQL driver (`org.postgresql:postgresql`) or MySQL driver (`com.mysql:mysql-connector-j`)
- Flyway (`org.flywaydb:flyway-core`) for schema migration
- Spring Modulith starter-jpa (`spring-modulith-starter-jpa`)

**If Auth = Keycloak:**
- Spring Security (`spring-boot-starter-security`)
- Spring Security OAuth2 Resource Server (`spring-boot-starter-oauth2-resource-server`)

**If Auth = Spring Security (JWT):**
- Spring Security (`spring-boot-starter-security`)
- `io.jsonwebtoken:jjwt-api`, `jjwt-impl`, `jjwt-jackson` for JWT token generation/validation

**If Scheduling = yes:**
- Spring Quartz (`spring-boot-starter-quartz`)
- If Database = MongoDB: `io.fluidsonic.mirror:fluidsonic-mirror-quartz` (MongoDB job store for Quartz)
- If Database = PostgreSQL/MySQL: Quartz JDBC job store (built-in)

**If Scheduling = yes AND Spring Batch = yes:**
- Spring Batch (`spring-boot-starter-batch`)

**If Scheduling = yes AND Spring Batch = yes AND Remote Partitioning = yes:**
- Spring Batch Integration (`spring-batch-integration`)
- Spring Integration AMQP (`spring-integration-amqp`)
- Spring Boot AMQP Starter (`spring-boot-starter-amqp`)

**If Messaging = yes:**
- Spring Boot AMQP Starter (`spring-boot-starter-amqp`)
  *(shared with Remote Partitioning â€” if both are selected, include the dependency once)*

**If Reporting = yes:**
- JasperReports (`net.sf.jasperreports:jasperreports:7.0.3`) â€” report engine with JRDesign API for programmatic layout
- JasperReports Fonts (`net.sf.jasperreports:jasperreports-fonts:7.0.3`)
- OpenPDF (`com.github.librepdf:openpdf:2.0.4`) â€” PDF export engine for JasperReports 7.x
- Apache POI OOXML (`org.apache.poi:poi-ooxml:5.4.1`) â€” XLSX export support

## When the Skill Triggers

Generate the spec when the user provides an **application name** and **version** that
corresponds to one of the custom applications defined in `CLAUDE.md`. The skill
reads all required inputs from the project's context files â€” no interactive Q&A is needed
for the core inputs.

The user invokes this skill by specifying the target application and version, for example:
- `/specgen-spring-jpa-restapi hc_adapter v1.0.0`
- `/specgen-spring-jpa-restapi hc_adapter v1.0.0 module:Job Demand`
- `/specgen-spring-jpa-restapi "HC Adapter" v1.0.0`

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
| `<application>` | Yes | `hc_adapter` | Application name to locate the context folder |
| `<version>` | Yes | `v1.0.0` | Version to scope processing |
| `module:<name>` | No | `module:Job Demand` | Limit generation to a single module |

### Application Folder Resolution

The application name is matched against root-level application folders:
1. Strip any leading `<number>_` prefix from folder names (e.g., `1_hc_adapter` -> `hc_adapter`)
2. Match case-insensitively against the provided application name
3. Accept snake_case, kebab-case, or title-case input (all match the same folder)
4. If no match found, list available applications and stop

### Auto-Resolved Paths

| File | Resolved Path |
|------|---------------|
| PRD.md | `<app_folder>/context/PRD.md` |
| Module Models | `<app_folder>/context/model/` |
| Output (specification) | `<app_folder>/context/specification/` |

### Example Invocations

- `/specgen-spring-jpa-restapi hc_adapter v1.0.0` (all modules)
- `/specgen-spring-jpa-restapi hc_adapter v1.0.0 module:Job Demand` (one module)
- `/specgen-spring-jpa-restapi "HC Adapter" v1.0.0`

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

The specification is driven by **five input sources** that are read from the project's
context files. The skill does NOT ask the user for database, authentication, scheduling,
or messaging choices â€” it **determines** these automatically from the context.

### Input 1: Application Name (from CLAUDE.md)

From CLAUDE.md (already loaded in context), locate the target application under the **Custom Applications**
section. Extract:

- **Application name**: The section heading (e.g., "HC Adapter", "SC Adapter")
- **Application description**: The description paragraph below the heading
- **Dependencies**: The "Depends on" list â€” this is the primary source for determining
  optional components (see [Determining Optional Components](#determining-optional-components))

The application name is used to derive:
- **Artifact ID**: Kebab-case of the application name (e.g., `hc-adapter`)
- **Group ID**: `com.bestinet.urp` (project-level constant)
- **Base package**: `com.bestinet.urp.<artifactid_no_hyphens>` (e.g., `com.bestinet.urp.hcadapter`)

### Input 2: User Stories (from PRD.md)

Read `<app_folder>/context/PRD.md`. This file contains all user stories
organized by module. Extract:

- **System modules**: Modules under the `# System Module` heading (e.g., User, Notification,
  Activities, Audit Trail). These become system-level modules in the spec.
- **Business modules**: Modules under the `# Business Module` heading (e.g., Location
  Information, Corridor, Employer). These become business-level modules.
- **User stories per module**: Each `### User Story` section contains tagged items like
  `[USHC00108] As a user, I want to...`. These define the functional requirements for
  each module's service interface and API endpoints.

The user stories directly inform:
- Which CRUD operations each module's service must expose
- Which REST API endpoints are needed
- Which request/response DTOs and validation rules apply

**Important:** Items with strikethrough (`~~text~~`) are deprecated â€” do NOT include them
as active requirements. Instead, list them in the "Removed / Replaced" subsection of the
traceability table (see spec-template.md) so that developers can see what was removed and
which version removed it. If a deprecated item has a replacement (e.g., `USHC00015` replaced
by `USHC00222`), note the replacement ID.

- **Version tags per item**: Each `### User Story`, `### Non Functional Requirement`,
  and `### Constraint` section contains one or more version blocks formatted as `[v1.0.x]`.
  Items listed under each version tag belong to that version. The skill must track the
  version tag for each item (user story, NFR, constraint) and carry it through to the
  generated specification's traceability section. When a version block explicitly lists
  "Removed ... from previous version", record those removals in a "Removed / Replaced"
  subsection with the version that removed them and the replacement ID (if any).

### Input 3: Non-Functional Requirements (from PRD.md)

Within the same `PRD.md`, each module has a `### Non Functional Requirement` section
with tagged items like `[NFRHC0120]`. These inform:

- Data storage strategies (e.g., "stored in staging database", "stored in the database")
- Integration patterns (e.g., "API call to external service", "sent asynchronously")
- Performance constraints (e.g., "automatically deleted after 30 days")
- Security requirements (e.g., "API key authentication", "JWT validation")

NFRs should be mapped to specific technical decisions in the spec â€” for example, an NFR
stating "staging database" confirms adapter pattern, while "sent asynchronously" confirms
event-driven processing.

### Input 4: Constraints (from PRD.md)

Within the same `PRD.md`, each module has a `### Constraint` section with tagged
items like `[CONSHC042]`. These define hard boundaries that the spec must enforce:

- Field-level restrictions (e.g., "only accept ISO3 country codes")
- Feature boundaries (e.g., "only 2 message types supported")
- Scope limitations (e.g., "does not manage any user, permissions and roles")

Constraints are embedded directly into the relevant module blueprint â€” they inform
service interface contracts, validation rules, and API endpoint configurations.

### Input 5: Module Model (from model/ folder)

Read `<app_folder>/context/model/MODEL.md` first as the index, then read the
individual module model files in each module subfolder.

**MODEL.md** provides:
- Summary table of all modules with entity counts and design decisions
- Links to each module's detailed model files

**Per-module files** (e.g., `model/job-demand/model.md`):
- Complete entity field definitions with types and constraints
- Embedded vs. referenced relationships
- Table names
- Index specifications
- Audit field patterns

**Per-module schema** (e.g., `model/job-demand/schemas.json`):
- JSON schemas defining exact field types, required fields, and validation rules

**Per-module diagram** (e.g., `model/job-demand/entity-model.mermaid`):
- Visual representation of entity structure and relationships

The module model directly maps to:
- JPA entities (field-for-field, not placeholder) or MongoDB documents
- Repository methods and query patterns
- MapStruct mapper definitions
- DTO structures matching the actual module fields
- Service interface method signatures

- **Version tracking**: The MODEL.md summary table includes a "Versions" column listing
  which versions each module participates in (e.g., "1.0.0, 1.0.1, 1.0.3"). Per-module
  model.md files may also include version annotations on fields and indexes. The skill
  must carry these version tags into the generated specification.

## PRD.md Extended Sections

Before determining optional components, check PRD.md for the following extended sections and extract their content for use throughout specification generation:

### Architecture Principle Extraction

If PRD.md contains an `# Architecture Principle` section, read it and extract architectural patterns as a structured context object. These patterns serve as **primary signals** for optional component determination and specification content:

| Pattern to Extract | How It Influences the Specification |
|---|---|
| Framework mention (e.g., "Spring Boot") | Validates technology stack choice |
| "Stateless" | Confirms stateless REST API â€” no HTTP session, JWT validation only; include in Security section |
| "Event-driven" | Enhances event publishing/subscribing sections with event catalog and explicit listener patterns |
| "Message driven" / "message queue" | Validates RabbitMQ integration; include message flow per module |
| "Document based database" / "MongoDB" | Primary signal for Database = MongoDB |
| "At-least-once delivery" | Add Idempotency section with idempotency key header pattern and deduplication |
| "Container based deployment" | Confirms `${ENV_VAR}` syntax for configuration |
| "API gateway" | Adjust base URL configuration for gateway routing |
| "Scale out" / "horizontally scalable" | Note horizontal scaling considerations in deployment section |

If the section is absent, proceed with existing CLAUDE.md-only detection.

### High Level Process Flow Extraction

If PRD.md contains a `# High Level Process Flow` section:
1. Parse all named process flows and their ordered steps
2. Each process flow is an **authoritative source** for messaging pipeline sections in per-module SPEC.md:
   - Each step maps to a service method, event listener, or message handler
   - Error paths generate exception handlers and dead-letter queue configurations
   - ACK/NACK patterns become outbound message publisher specs with defined schemas
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

Also check `CLAUDE.md`'s database section for the exact database name, host, and
credentials to use in the spec's application configuration. Read `ENVIRONMENT.md` (in the
project root) for host, port, and credentials.

### Authentication Detection

| Dependency Pattern | Auth Selection |
|---|---|
| References "Hub Single Sign On" (Keycloak) | Auth = Keycloak (Resource Server) |
| PRD.md constraint says "does not manage any user, permissions and roles" | Auth = none |
| PRD.md NFRs reference "JWT token" or "Bearer token" | Auth = Keycloak (Resource Server) |
| No SSO/Keycloak dependency but has user management stories | Auth = JWT (self-issued) |

If Auth = Keycloak (Resource Server), also extract from CLAUDE.md:
- Keycloak version from "Hub Single Sign On" section
- Keycloak realm: Default derived from project name
- Keycloak issuer URI: Default `http://localhost:8180/realms/<realm>`
- Keycloak roles: Infer from user stories and NFRs
- The application validates JWT tokens issued by Keycloak (stateless, no session)

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
- **Spring Batch = yes** if NFRs mention "batch processing", "ETL", "bulk import/export",
  or processing large volumes of data with reader/processor/writer patterns
- **Remote Partitioning = yes** if NFRs mention "distributed processing", "horizontal
  scaling", or "partitioned batch jobs"

### Reporting Detection

Reporting is determined from PRD.md content:

| Content Pattern | Reporting Selection |
|---|---|
| NFRs mention "report", "Report interface", "generate report", "report generation" | Reporting = yes |
| User stories describe generating/downloading PDF, Excel, or CSV reports | Reporting = yes |
| A "Report" module exists in PRD.md with NFRs defining a Report interface | Reporting = yes |
| No reporting-related requirements found | Reporting = no |

**If Reporting = yes**, the spec includes:
- JasperReports with JRDesign API for fully programmatic report layout (no .jrxml templates)
- `ReportDefinition` interface with `buildDesign()` method for modules to implement
- `ReportDesignHelper` utility class with static builders for common layout patterns
- `ReportService` orchestrating compile â†’ fill â†’ export via `JRBeanCollectionDataSource`
- Report registry persisted in the database
- REST controller with report list, details, and generation endpoints (JSON + file download)
- Multi-format export: PDF (OpenPDF), XLSX (Apache POI), CSV

### Summary of Determination

After analyzing all inputs, produce a determination summary before generating the spec.
Present it to the user for confirmation:

```
Optional Component Determination:
- Database:      MySQL (from CLAUDE.md -> depends on HC Database)
- Authentication: Keycloak Resource Server (from CLAUDE.md -> depends on Hub Single Sign On)
- Scheduling:    no
- Messaging:     yes (from CLAUDE.md -> depends on Hub to HC Adapter Message Queue)
- Reporting:     yes (from PRD.md â†’ Report module with Report interface NFR)
```

If the user disagrees with any determination, allow them to override before proceeding.

## Required Inputs

After determination, these values are needed. Most are derived automatically:

**Auto-derived from context files:**
- **Application name**: From CLAUDE.md section heading
- **Artifact ID**: Kebab-case of application name
- **Group ID**: `com.bestinet.urp`
- **Base package**: `com.bestinet.urp.<artifactid>`
- **Application description**: From CLAUDE.md description
- **Modules**: From PRD.md module headings + model/MODEL.md
- **Database**: Auto-determined (see above)
- **Authentication**: Auto-determined (see above)
- **Scheduling**: Auto-determined (see above)
- **Messaging**: Auto-determined (see above)
- **Database name/credentials**: From ENVIRONMENT.md (root-level file with local environment credentials)

**Auto-derived from CLAUDE.md (Port Allocation table):**
- **Server port**: Look up the application's port from the `Port Allocation` table in the `Custom Applications` section of `CLAUDE.md`. Do NOT hardcode a default â€” the port MUST match the allocated port for this application.

**Optional (use sensible defaults if not found in context):**
- **API version prefix**: Default `/api/v1`
- **Log level**: Default `INFO` for application, `WARN` for frameworks

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
  (e.g., `jobDemand`, `candidateRegistration`, `employer` â€” not `module1`, `module2`)
- **Entity fields** must match the actual fields defined in the module model
  files (e.g., `model/job-demand/model.md`), not placeholder `fieldOne`/`fieldTwo`
- **Service interfaces** must expose methods matching the actual user stories (e.g., if
  a story says "search job demands by country", the service needs `searchByCountry()`)
- **REST endpoints** must map to the actual user stories (e.g., if a user story says
  "view details of a job demand", there must be a `GET /api/v1/job-demands/{id}` endpoint)
- **Request/Response DTOs** must match what the user stories and module model define
- **Version tags**: Every user story ID, NFR ID, constraint ID in the traceability section
  must include its version tag (e.g., `USHC00228 [v1.0.3]`).
- **Removed / Replaced items**: The traceability section must include a "Removed / Replaced"
  subsection listing any deprecated items from previous versions.

### Output Structure

```
<app_folder>/context/specification/
â”œâ”€â”€ SPECIFICATION.md                    <- TOC + shared/application-level specs
â”œâ”€â”€ job-demand/
â”‚   â””â”€â”€ SPEC.md                         <- Module blueprint for Job Demand
â”œâ”€â”€ candidate-registration/
â”‚   â””â”€â”€ SPEC.md                         <- Module blueprint for Candidate Registration
â”œâ”€â”€ ...                                 <- One folder per module from PRD.md
```

### What Goes in `SPECIFICATION.md` (Root)

The root file contains the TOC and all shared/application-level sections. These are the
sections that a coding agent implements **first** before any module work:

#### 1. Project Overview
Project metadata, application description, technology stack summary, the complete
list of API consumers/roles, and the **Module Index** â€”
a table listing every module with a link to its `<module>/SPEC.md` file.

#### 2. Maven Configuration
Complete `pom.xml` structure with all dependencies (core + selected conditional),
plugin configurations (MapStruct annotation processor, Spring Boot Maven plugin),
and property management.

#### 3. Application Configuration *(conditional content varies)*
A single `application.yml` (no profile-specific files like `application-dev.yml` or
`application-prod.yml`) covering database connection (MongoDB URI or JDBC datasource
depending on selection), auth settings (Keycloak Resource Server JWT validation if
selected, or self-issued JWT if selected), scheduling config (if selected), and logging
configuration. **All environment-sensitive values (ports, hostnames, credentials, URIs)
MUST use Spring's `${ENV_VAR:default}` syntax** to allow externalization via environment
variables while keeping sensible defaults for local development. Do NOT use Spring
profiles or profile-specific YAML files â€” environment differences are handled entirely
through environment variables (e.g., via `.env` file locally or system environment
variables in deployment).

#### 3a. Application-Specific Configuration (`app:` namespace)

All application-owned configuration â€” any config specific to THIS application, as
opposed to the Spring/Java ecosystem â€” MUST live under the top-level `app:` key in
`application.yml`. NEVER place application-specific keys under Spring framework
namespaces (`spring.*`, `server.*`, `management.*`, `logging.*`, `springdoc.*`) â€”
those are reserved for framework configuration.

**Grouping rule.** Organise the `app:` tree by module:
- **Cross-cutting values** (version, shared feature flags, shared timeouts, CORS,
  shared security settings, shared messaging infrastructure, shared object-storage
  settings) sit directly under `app.*` with no module prefix.
- **Per-module values** are grouped under `app.<module-kebab-case>.*`, one block
  per module that needs runtime config. A module with a single config value still
  gets its own block â€” do not flatten.
- **NEVER place module-specific keys at the YAML root** (e.g., top-level
  `notification:`, `batch-job:`, `audit-trail:`). They MUST be nested under `app:`.

**Naming rule.** YAML keys use **kebab-case** (`from-address`, `retry-limit`,
`max-retry`). Spring Boot's relaxed binding maps them to camelCase Java fields
automatically. Do NOT use camelCase or snake_case in YAML.

**Binding rule.** For every `app.*` subtree (cross-cutting OR per-module), bind once
via `@ConfigurationProperties` on a **record** in the corresponding module's `config`
subpackage â€” or, for cross-cutting values, in the application-level `config`
subpackage. **Do NOT** inject individual values via `@Value("${app....}")` scattered
across beans. Bind once at the module boundary and inject the typed record.

**Environment-override rule.** Every `app.*` leaf value MUST use Spring's
`${ENV_VAR:default}` syntax so it can be overridden per environment without editing
YAML. Every referenced `${ENV_VAR}` MUST appear in the `.env` file generated in
section 3b.

**Example structure:**

```yaml
app:
  # Cross-cutting (no module prefix)
  version: ${APP_VERSION:1.0.0}
  cors:
    allowed-origins: ${APP_CORS_ALLOWED_ORIGINS:http://localhost:3000}
  security:
    public-paths:
      - /actuator/health
      - /api/v1/info

  # Per-module blocks â€” one per module with runtime config
  notification:
    email:
      from-address: ${NOTIFICATION_FROM_ADDRESS:noreply@example.com}
      retry-limit: ${NOTIFICATION_RETRY_LIMIT:3}
    cleanup:
      retention-days: ${NOTIFICATION_RETENTION_DAYS:30}
  batch-job:
    cleanup:
      retention-days: ${BATCH_JOB_RETENTION_DAYS:90}
  audit-trail:
    cleanup:
      retention-days: ${AUDIT_TRAIL_RETENTION_DAYS:365}
```

**Example cross-cutting record (`app.*`):**

```java
@ConfigurationProperties(prefix = "app")
public record AppProperties(String version, Cors cors, Security security) {
    public record Cors(List<String> allowedOrigins) {}
    public record Security(List<String> publicPaths) {}
}
```

**Example per-module record (`app.<module>.*`):**

```java
@ConfigurationProperties(prefix = "app.notification")
public record NotificationProperties(
    Email email,
    Cleanup cleanup
) {
    public record Email(String fromAddress, int retryLimit) {}
    public record Cleanup(int retentionDays) {}
}
```

Enable binding at the application root with `@ConfigurationPropertiesScan` on the
main application class, or register each record individually via
`@EnableConfigurationProperties` on a `@Configuration` class in the owning module.

**Mandatory cross-cutting values:**

| Key | Purpose | Binding |
|-----|---------|---------|
| `app.version` | Current application version; must match `pom.xml` `<version>` | `AppProperties.version()` |

Additional cross-cutting keys may be added as the application grows, but
`app.version` is always present.

**`app.version` specifics.** The `.env` file must include `APP_VERSION={version}`
with the actual version value. The `pom.xml` `<version>` element MUST also be set to
the same version value (e.g., `1.0.3`). When multiple versions were provided during
skill invocation, use the highest one. The REST API MUST expose the application
version in:

1. **A health/info endpoint** (e.g., `GET /api/v1/info` or Spring Actuator
   `/actuator/info`) returning `{"version": "1.0.3", ...}`. Inject `AppProperties`
   into the controller and read the version via `appProperties.version()`.
2. **Every API response envelope** â€” if the API uses a standard response wrapper,
   include a `version` field (e.g., `{"version": "1.0.3", "data": {...}}`).

#### 3b. `.env` File Generation from ENVIRONMENT.md
Generate a `.env` file at the project root by reading `ENVIRONMENT.md` from the project root.
The `.env` file maps ENVIRONMENT.md credential and platform values to the environment variable
names referenced in `application.yml`. The spec must define the complete `.env` content
with actual values from ENVIRONMENT.md.

**Process:**
1. Read `ENVIRONMENT.md` from the project root
2. Extract credential values from `ENVIRONMENT.md` (`# Supporting 3rd Party Applications`
   for database hosts, ports, usernames, passwords, plus Keycloak/RabbitMQ); read toolchain
   paths (JDK, Maven) from `DEVTOOL.md`
3. Map each value to the corresponding `${ENV_VAR}` name used in `application.yml`
4. Generate the `.env` file with `KEY=value` pairs

**Example `.env` output (derived from ENVIRONMENT.md):**
```properties
# Database
DB_HOST=localhost
DB_PORT=3306
DB_NAME=hub_supp
DB_USERNAME=root
DB_PASSWORD=B3st1n3t@2025

# Authentication (Keycloak)
KEYCLOAK_HOST=http://localhost:8180
KEYCLOAK_REALM=urp
KEYCLOAK_CLIENT_ID=hub-middleware-api

# Messaging (RabbitMQ)
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USERNAME=guest
RABBITMQ_PASSWORD=guest

# Server
SERVER_PORT=<port from CLAUDE.md Port Allocation table>

# Platform
JAVA_HOME=C:\Users\rashidee.rashid.BESTINET\.jdks\azul-21.0.9
MAVEN_HOME=C:\Users\rashidee.rashid.BESTINET\apache-maven-3.9.12
```

**Rules:**
- Only include variables that are actually referenced in `application.yml`
- Use actual values from ENVIRONMENT.md â€” never use placeholders or `TODO`
- If ENVIRONMENT.md does not exist or a value is not found, use sensible defaults for local
  development (e.g., `localhost`, default ports)
- The `.env` file is gitignored (already covered in `.gitignore`)

#### 4. `.gitignore`
Generate a `.gitignore` file at the project root that excludes all generated, downloaded,
and environment-specific files from version control.

#### 5. Package Structure
The complete directory tree rooted at the base package. The structure follows
Domain-Driven Design with Spring Modulith conventions, adapted for REST API
with `controller` subpackages (not `page`/`fragment`). Use actual module names.
Read `references/modulith-patterns.md` for the detailed module layout and inter-module
communication rules.

#### 6. Security Configuration *(conditional â€” include only if Auth != none)*
**If Auth = Keycloak (Resource Server):** OAuth2 Resource Server setup with JWT validation.
`SecurityFilterChain` with `oauth2ResourceServer(jwt -> ...)`. Keycloak JWT decoder
configuration. Role extraction from JWT claims (`realm_access`, `resource_access`).
Stateless session policy. CORS configuration. Read `references/security-patterns.md`
for the full security architecture.

**If Auth = JWT (self-issued):** Spring Security with custom JWT token provider.
`SecurityFilterChain` with `JwtAuthenticationFilter`. `JwtTokenProvider` for token
generation and validation. Stateless session policy. CORS configuration.

#### 7. REST API Conventions
Standardized REST API patterns including:
- URI naming conventions (plural nouns, kebab-case)
- API versioning strategy (`/api/v1/...` path prefix)
- Request/Response DTO patterns (Java records with Bean Validation)
- Standardized error response envelope (`ApiError` record)
- HTTP status code usage guidelines
- Pagination response structure (Spring Data `Page` serialization)
- HATEOAS considerations (optional, note when applicable)

Read `references/restapi-patterns.md` for the complete REST API patterns.

#### 8. Error Handling & Exceptions
Global `@RestControllerAdvice` exception handler returning standardized JSON error
responses. Base `ApiException` with status/code/message. `ResourceNotFoundException`,
`ValidationException`, `ConflictException` hierarchy. Consistent `ApiError` envelope
across all error responses.

#### 9. Pagination & Filtering Support
Standardized pagination using Spring Data `Pageable`. Sorting support via query
parameters. Dynamic filtering using Spring Data Specifications (JPA) or Query DSL
(MongoDB). Default page size, maximum page size configuration.

#### 10. Data Access *(conditional content varies)*
**If Database = MongoDB:** MongoDB repositories per module with Spring Data MongoRepository.
DTO mapping via MapStruct. All list endpoints paginated. Use actual collection names.

**If Database = PostgreSQL/MySQL:** JPA repositories per module with Spring Data
JpaRepository. JPA entities with `@Entity`/`@Table` annotations extending `BaseEntity`.
`BaseEntity` uses `@UuidGenerator(style = UuidGenerator.Style.TIME)` with
`@Column(columnDefinition = "CHAR(36)")` and `private String id`. Flyway migration scripts.
DTO mapping via MapStruct. All list endpoints paginated. Use actual table names.
**MySQL UUID rule:** All UUID primary keys and foreign keys use `CHAR(36)` in DDL.

**If Database = none:** In-memory data structures or stubs.

#### 11. API Documentation (SpringDoc OpenAPI)
SpringDoc OpenAPI configuration for auto-generating Swagger UI. Controller annotations
(`@Tag`, `@Operation`, `@ApiResponse`). Configuration in `application.yml`.

#### 12. Logging Strategy
SLF4J with Logback configuration, correlation ID filter (`X-Correlation-Id` header),
MDC context filter, per-module log levels.

#### 13. Scheduling and Batch Processing *(conditional â€” include only if Scheduling = yes)*
Quartz scheduler configuration with job store matching the selected database.
Read `references/batch-patterns.md` for the full scaffolding spec.

#### 14. Event-Driven Architecture
Spring Modulith application events for inter-module communication. Read
`references/modulith-patterns.md` for details.

#### 15. Messaging (RabbitMQ Pub/Sub) *(conditional â€” include only if Messaging = yes)*
Standalone RabbitMQ publisher/consumer services for inter-system communication.
Read `references/messaging-patterns.md` for the full messaging architecture.

#### 16. MapStruct Usage
Per-module MapStruct mapper conventions and mapping flow patterns.

#### 17. Testing Strategy
Overview of testing approach â€” unit tests (service layer with Mockito), integration tests
(controller layer with `@WebMvcTest` and MockMvc), security test utilities
(JWT mocking if Keycloak, or `@WithMockUser` if JWT), Spring Modulith module verification.

#### 18. Caching Strategy *(optional â€” include if applicable)*
HTTP caching headers (`Cache-Control`, `ETag`). Application-level caching with
Spring Cache and Caffeine. Cache eviction strategies.

#### 19. Idempotency *(optional â€” include if applicable)*
`Idempotency-Key` header pattern for mutating operations. Duplicate detection
and response replay.

#### 20. Reporting (JasperReports JRDesign API) *(conditional â€” include only if Reporting = yes)*
JasperReports infrastructure with fully programmatic report layout via JRDesign API â€” no
`.jrxml` XML templates. Report layouts are built entirely in Java code using `JasperDesign`,
`JRDesignBand`, `JRDesignStaticText`, `JRDesignTextField`, and `JRDesignField` classes.
Includes `ReportDefinition` interface with `buildDesign()` method for modules to implement,
`ReportDesignHelper` utility with static builders for common patterns (A4 portrait/landscape,
column headers, detail bands, page footers), `ReportService` orchestrating compile â†’ fill â†’
export via `JRBeanCollectionDataSource`, `ReportRegistry` for auto-discovering and persisting
report definitions at startup, REST controller with report list, details, and generation
endpoints (`GET /api/v1/reports`, `POST /api/v1/reports/{id}/generate`), multi-format export
(PDF via OpenPDF, XLSX via Apache POI, CSV). Modules register reports by creating
`@Component` classes implementing `ReportDefinition` â€” each report builds its layout
programmatically and calls module services to produce DTOs (never repositories directly),
preserving Spring Modulith module boundaries. Read `references/reporting-patterns.md` for
the full reporting architecture.

### What Goes in Each `<module>/SPEC.md` (Per-Module)

For EACH module from PRD.md and MODEL.md, create a folder named after the
module (kebab-case, e.g., `job-demand/`) and generate a `SPEC.md` inside it.

Each module `SPEC.md` is a **self-contained** blueprint that a coding agent can pick up
and implement independently (after the shared infrastructure is in place). It must include:

- **Header** with module name and a back-reference to the root `SPECIFICATION.md`
- **Traceability**: User story IDs, NFR IDs, constraint IDs, table/collection names
- **Service interface** with methods derived from user stories
- **Request DTOs** with Bean Validation annotations matching module model fields
- **Response DTOs** as Java records matching module model fields
- **Exception class** for module-specific errors
- **Entity/Document class** with fields from `model/<module>/model.md` and
  `model/<module>/schemas.json`
- **Repository** with query methods matching user stories' data access patterns
- **MapStruct mapper** with mappings matching actual field names
- **Service implementation** with full CRUD logic
- **REST controller** with endpoints matching user stories (`@RestController`)
- **Complete code samples** for every component â€” continuous and copy-pasteable

**Separating REST API Layer from Messaging/Async Pipeline:**

When a module has BOTH user-facing endpoints (user stories) AND async processing NFRs
(e.g., RabbitMQ message consumption, message validation, ACK publishing, forwarding),
the SPEC.md MUST clearly separate these into distinct sections:

1. **REST API sections** â€” service methods for CRUD operations (search, getById, create,
   update, delete), REST controllers, request/response DTOs. These are driven by user
   stories (USHCxxxxx).
2. **Messaging Pipeline sections** â€” message consumer (`@RabbitListener`), message
   validator, ACK publisher, forward publisher, queue configuration, domain events,
   `processIncomingMessage()` service method. These are driven by NFRs (NFRHCxxxx).

> **MQ listener placement (mandatory).** Every `@RabbitListener` class generated for a
> module MUST be placed inside that module's `internal/` package
> (`{{base}}.{{module}}.internal`), package-private, alongside the controller. Shared
> messaging infrastructure (`RabbitMQMessagingConfig`, `RabbitMQPublisher`,
> `MessageConverterConfig`, cross-module event/command DTOs) lives in
> `shared/messaging/`, but that package must contain **no** `@RabbitListener`
> classes. See `references/messaging-patterns.md` Â§ "Consumer Service (module-internal)"
> for the canonical pattern.

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
5. Row format: `| {YYYY-MM-DD} | {application_name} | specgen-spring-jpa-restapi | {module or "All"} | Generated Spring Boot REST API technical specification |`
6. **Never modify or delete existing rows.**

## Output Format

The generated specification is a **folder of files**, not a single document:

```
<app_folder>/context/specification/
â”œâ”€â”€ SPECIFICATION.md                    <- Root: TOC + shared/application-level specs
â”œâ”€â”€ <module-1>/
â”‚   â””â”€â”€ SPEC.md                         <- Module blueprint (self-contained)
â”œâ”€â”€ <module-2>/
â”‚   â””â”€â”€ SPEC.md
â”œâ”€â”€ <module-N>/
â”‚   â””â”€â”€ SPEC.md
```

- **Root folder**: `<app_folder>/context/specification/`
- **Root file**: `SPECIFICATION.md`
- **Module folders**: One folder per module from PRD.md, named in kebab-case
- **Module files**: Each `SPEC.md` is self-contained with full code samples

**Sample code is mandatory.** Every component described in any spec file must include a
complete, self-explanatory code sample inside a fenced code block (Java, YAML, or JSON
as appropriate). The sample code must be continuous (not fragments stitched with "// ..."
gaps) and usable as a direct reference by a coding agent or developer.

## Constraints

These constraints are non-negotiable. Every code sample in the generated spec must
follow them. If any constraint is violated, the spec is incorrect.

### Universal Constraints (Always Apply)

**Do NOT use Lombok's `@Data` annotation â€” anywhere.** Use `@Getter` and `@Setter`
explicitly on every class that needs accessors. `@Data` generates `equals()`, `hashCode()`,
and `toString()` which cause problems with persistent entities, lazy-loaded
collections, and circular references. The spec must use `@Getter @Setter` consistently.

**Do NOT use field injection.** Every Spring-managed bean must use constructor injection.
Use Lombok's `@RequiredArgsConstructor` with `private final` fields. Never use `@Autowired`
on fields. This applies to services, controllers, configurations, filters, and any other
Spring component.

**Use Java records for DTOs.** All request and response DTOs should be Java records
(immutable, auto-generated `equals`/`hashCode`/`toString`). Records with Bean Validation
annotations for request DTOs.

**Use MapStruct for all object mapping.** Define MapStruct mappers per module with
`@Mapper(componentModel = "spring")`. Avoid handwritten mapping beyond simple passthroughs.

**Never expose JPA entities or MongoDB documents directly in API responses.** Always
map to response DTOs via MapStruct.

**All data listings must be paginated.** Every endpoint that returns a list must accept
`Pageable` parameters and return `Page<T>`. Never return unbounded lists.

**Use real module data from context files.** The spec must use actual field names,
collection/table names, module names, and user stories from the context files.

**REST API URI conventions:**
- Use plural nouns for resource names (e.g., `/api/v1/job-demands`, NOT `/api/v1/job-demand`)
- Use kebab-case for multi-word resources (e.g., `/api/v1/job-demands`, NOT `/api/v1/jobDemands`)
- Use `{id}` path variable for single resource access (e.g., `/api/v1/job-demands/{id}`)
- Maximum 2 levels of nesting (e.g., `/api/v1/employers/{id}/contacts`)
- Non-CRUD actions use sub-resource verbs (e.g., `POST /api/v1/orders/{id}/cancel`)

**Return correct HTTP status codes:**
- `200 OK` for successful retrieval and updates
- `201 Created` with `Location` header for resource creation
- `204 No Content` for successful deletion
- `400 Bad Request` for validation errors
- `401 Unauthorized` for missing/invalid credentials
- `403 Forbidden` for insufficient permissions
- `404 Not Found` for non-existent resources
- `409 Conflict` for state conflicts

### Conditional Constraints

**If Auth = Keycloak (Resource Server):**
- **Use OAuth2 Resource Server (not OAuth2 Client).** The application validates JWT tokens
  in the `Authorization: Bearer` header. Stateless â€” no HTTP session.
- **Do NOT manage users and roles in the application.** Keycloak owns user/role management.
  The application only reads roles from JWT claims to enforce access control.

**If Auth = JWT (self-issued):**
- The application manages its own JWT token generation and validation.
- Stateless session policy. Custom `JwtAuthenticationFilter` extracts and validates tokens.

**If Scheduling = yes and Database = MongoDB:**
- **Use `io.fluidsonic.mirror` for Quartz MongoDB job store.**

**If Scheduling = yes and Database = PostgreSQL/MySQL:**
- Use the built-in Quartz JDBC job store with the selected relational database.

**If Messaging = yes:**
- Queue and exchange names for pub/sub messaging (`app.*`) must not collide with batch
  partition queues (`batch.partition.*`). Use distinct prefixes for each concern.

## Principles Embedded in the Spec

These principles should be woven into every section of the spec rather than listed
separately.

### Always-Applicable Principles
- RESTful API design with standardized conventions
- JSON request/response with Jackson serialization
- Bean Validation at controller boundary (`@Valid`)
- Standardized error response envelope
- Event-driven inter-module communication via Spring Modulith events
- Domain-driven package structure (one module per bounded context)
- Separation of concerns (controller -> service -> repository)
- Constructor injection everywhere (`@RequiredArgsConstructor` + `private final`)
- `@Getter @Setter` instead of `@Data` on all entity/document classes
- Java records for all DTOs
- Single `application.yml` with environment variables for all environment-specific values (no profile-specific YAML files)
- Custom exception hierarchy with global error handling via `@RestControllerAdvice`
- Structured logging with correlation IDs
- OpenAPI documentation via SpringDoc
- Pagination on all list endpoints

### Conditional Principles
- **If Auth = Keycloak:** OAuth2 Resource Server with JWT validation for all
  authentication and authorization (stateless). No user/role management â€” external IdP only.
- **If Auth = JWT:** Custom JWT token provider with stateless authentication.
- **If Auth = none:** No security filter chain. All endpoints are publicly accessible.
