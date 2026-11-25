---
name: specgen-sdk-java
model: claude-opus-4-8
effort: high
description: >
  Generate a detailed specification document for building a distributable Java SDK
  library packaged as a Multi-Release fat JAR via Maven. Targets JDK 8 baseline with
  JDK 11+ overlay classes (Multi-Release JAR) so a single artifact runs on every
  long-term JDK in production. The SDK is a thin client wrapping a remote REST API
  (and any additional protocols extracted from the PRD's Architecture Principle
  section). REST communication is implemented with OkHttp; everything else
  (JSON parsing, models, builders, retry, logging) is implemented with the JDK and
  in-house code â€” third-party dependencies are kept to the absolute minimum.
  Standardized input: application name (mandatory), version (mandatory), module (optional).
  Use this skill whenever the user asks to create a spec, specification, blueprint, or
  technical design document for a new Java SDK, Java client library, or REST API
  client wrapper. Also trigger when the user says things like "spec out a new Java SDK",
  "design a Java client library for my API", "write a technical spec for an SDK that
  wraps Swagger/OpenAPI", "scaffold spec for a fat-jar Java SDK", or any request
  describing a Java library that wraps a REST/HTTP API for downstream consumers.
  Even if the user only mentions a subset (e.g., "Java wrapper around my API",
  "client library for our microservice", "SDK that supports JDK 8 and 11"), this
  skill likely applies â€” ask and confirm.
---

# Java SDK (Multi-Release Fat JAR) Specification Generator

This skill generates a comprehensive specification document (Markdown) that serves as a
blueprint for building a distributable Java **SDK library**. The library is published as
a **Multi-Release fat JAR** built with Maven, supports JDK 8 as a baseline and uses
JDK 11+ overlays where modern APIs are beneficial, and wraps a remote REST API
(plus any additional protocols defined in the PRD's Architecture Principle section).

The specification does NOT generate code. It produces a detailed, opinionated technical
document describing every layer of the library â€” from the `pom.xml` Multi-Release
configuration, to the OkHttp transport, to the model classes and high-level service
facade â€” so that implementation becomes a mechanical exercise.

## Library-First Mindset

This is **NOT** an application. There is no `main()` (only an optional minimal one for
diagnostics), no Spring, no application server, no scheduler. The output is a JAR that
downstream Java applications add to their classpath and call as a normal API.

Every design decision below is biased toward:

1. **Minimum third-party footprint.** Each transitive dependency the SDK pulls in becomes
   a problem for every downstream consumer. The skill MUST resist adding libraries unless
   the JDK and OkHttp cannot reasonably cover the use case.
2. **Long-lived JDK compatibility.** Consumers may run JDK 8, 11, 17, or 21. The
   Multi-Release JAR layout lets the SDK ship one artifact that runs on all of them.
3. **A fat (uber) JAR as the primary artifact.** Consumers either drop the fat JAR onto
   the classpath or depend on it via Maven; either way they get one self-contained file.

## Technology Stack

### Core Stack (Always Included)

These versions are fixed unless the user explicitly overrides them.

| Component                | Version  | Notes                                         |
|--------------------------|----------|-----------------------------------------------|
| Java baseline (`release`)| 8        | All sources under `src/main/java` target JDK 8|
| Java overlay (`release`) | 11       | Sources under `src/main/java11` target JDK 11 |
| Maven                    | 3.9.x    | Build tool                                    |
| OkHttp                   | 4.12.0   | The ONLY runtime third-party dependency       |
| Okio                     | 3.9.x    | Transitive of OkHttp â€” not declared directly  |
| Kotlin stdlib (OkHttp)   | 1.9.x    | Transitive of OkHttp â€” not declared directly  |

> **Note on OkHttp 4.x vs 5.x:** OkHttp 4.x runs on JDK 8 and is the safe default for an
> SDK that must support legacy consumers. Move to 5.x only if the user explicitly
> requires JDK 11 as the baseline AND no longer needs JDK 8 support.

### Test-Only Dependencies (always included, scope = `test`)

| Component                | Version  | Purpose                                        |
|--------------------------|----------|------------------------------------------------|
| JUnit Jupiter            | 5.10.x   | Unit + integration tests                       |
| OkHttp MockWebServer     | 4.12.0   | Stub the remote API in tests                   |
| AssertJ                  | 3.26.x   | Fluent assertions                              |

These are scoped to `test` and never bundled into the fat JAR.

### Optional Runtime Dependencies (rare â€” only if PRD strictly requires)

The skill MUST default to **NO additional dependencies**. Add a row below ONLY when the
PRD explicitly requires the protocol/format and the JDK has no reasonable equivalent.

| Component                | When Selected                                              |
|--------------------------|------------------------------------------------------------|
| `org.java-websocket`     | WebSocket support AND PRD bans JDK 11 `HttpClient` WS API  |
| `com.rabbitmq:amqp-client` | AMQP/RabbitMQ protocol explicitly listed in Architecture Principle |
| `org.eclipse.paho:paho-mqtt-client` | MQTT protocol explicitly listed in Architecture Principle  |

> **JSON is handled in-house.** Do NOT add Jackson, Gson, Moshi, or org.json. The spec
> describes a tiny hand-written JSON serializer/deserializer (or, if the OpenAPI spec is
> trivial, simple `Map<String, Object>` round-tripping) that operates on the SDK's own
> immutable model classes. This is intentional â€” JSON is one of the largest sources of
> SDK dependency bloat and downstream version conflicts.

## When the Skill Triggers

Generate the spec when the user provides an **application name** and **version** that
corresponds to one of the SDK libraries defined in `CLAUDE.md`. The skill reads all
required inputs from the project's context files â€” no interactive Q&A is needed for the
core inputs.

The user invokes this skill by specifying the target application and version, for example:

- `/specgen-sdk-java my_sdk v1.0.0`
- `/specgen-sdk-java my_sdk v1.0.0 module:Auth`
- `/specgen-sdk-java "My SDK" v1.0.0`

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

| Argument        | Required | Example         | Description                                    |
|-----------------|----------|-----------------|------------------------------------------------|
| `<application>` | Yes      | `my_sdk`        | Application name to locate the context folder  |
| `<version>`     | Yes      | `v1.0.0`        | Version to scope processing                    |
| `module:<name>` | No       | `module:Auth`   | Limit generation to a single module            |

### Application Folder Resolution

The application name is matched against root-level application folders:

1. Strip any leading `<number>_` prefix from folder names (e.g., `1_my_sdk` â†’ `my_sdk`)
2. Match case-insensitively against the provided application name
3. Accept snake_case, kebab-case, or title-case input (all match the same folder)
4. If no match found, list available applications and stop

### Auto-Resolved Paths

| File           | Resolved Path                          |
|----------------|----------------------------------------|
| PRD.md         | `<app_folder>/context/PRD.md`          |
| Module Models  | `<app_folder>/context/model/`          |
| Output         | `<app_folder>/context/specification/`  |

### Version Filtering

When a version is provided, only include user stories, NFRs, constraints, tests, and
references from versions <= the provided version. For example, if `v0.3.0` is specified:

- Include items tagged `[v0.1.0]`, `[v0.2.0]`, `[v0.3.0]`
- Exclude items tagged `[v0.4.0]` or later
- Version comparison uses semantic versioning order

### Module Filtering

When `module:<name>` is provided:

- Only generate the `SPEC.md` for that specific module
- Other existing module spec files remain untouched
- `SPECIFICATION.md` (root) gets a partial update â€” only that module's TOC entry is
  added or updated; all other entries are preserved as-is

## Gathering Input

The specification is driven by **six input sources** that are read from the project's
context files. The skill does NOT ask the user for protocol, packaging, or model
choices â€” it **determines** these automatically from the context.

### Input 1: Application Name (from CLAUDE.md)

From CLAUDE.md (already loaded in context), locate the target SDK under the
**Custom Applications** section. Extract:

- **Application name**: The section heading (e.g., "My SDK", "Hub Client SDK")
- **Application description**: The description paragraph below the heading
- **Target consumers**: The "Used by" or "Consumers" list â€” informs API surface design
- **Dependencies**: The "Depends on" list â€” primary source for identifying the remote
  API (its base URL, auth scheme, etc.)

The application name is used to derive:

- **Artifact ID**: kebab-case of the application name (e.g., `my-sdk`)
- **Group ID**: `com.bestinet.urp` (project-level constant unless CLAUDE.md overrides)
- **Base package**: `com.bestinet.urp.<artifactid_no_hyphens>` (e.g., `com.bestinet.urp.mysdk`)
- **Main facade class name**: PascalCase of the application name with `Client` suffix
  (e.g., `MySdkClient`, `HubClient`)

### Input 2: User Stories (from PRD.md â€” "Library User Stories")

Read `<app_folder>/context/PRD.md`. For an SDK library, user stories describe what
**downstream Java applications** want to do with the SDK â€” NOT what an end user wants to
do with a UI. Phrasing examples:

- "As a consumer application, I want to fetch a paginated list of orders by status."
- "As a consumer application, I want to upload a file with progress callback."

Each story is tagged like `[USSDK00101]` and grouped by module. Extract:

- **Modules**: Each `## <ModuleName>` or `### <ModuleName>` section
- **User stories per module**: Tagged items defining the SDK's public methods

Items with strikethrough (`~~text~~`) are deprecated. List them in the "Removed /
Replaced" subsection of the traceability table. Carry version tags through to the
generated specification.

The user stories directly inform:

- The methods on each module's facade class (e.g., `OrdersService.list(...)`)
- Which request/response model classes are needed
- Which HTTP endpoints the SDK calls (mapping derived together with Input 6)

### Input 3: Non-Functional Requirements (from PRD.md)

Within the same `PRD.md`, each module has a `### Non Functional Requirement` section
with tagged items like `[NFRSDK0120]`. NFRs typical for an SDK:

- "All HTTP calls timeout after 30 seconds by default, configurable per call."
- "Connection pool reuses up to 10 keep-alive connections."
- "All retryable errors retry with exponential backoff up to 3 attempts."
- "Logging is opt-in via SLF4J â€” the SDK ships no SLF4J binding."

These NFRs map directly to the `OkHttpClient` builder configuration, the retry
interceptor design, and the logging strategy in the generated spec.

### Input 4: Constraints (from PRD.md)

Tagged items like `[CONSSDK042]`. For an SDK these usually constrain the public API
surface and dependency footprint, e.g.:

- "Public API must remain backwards compatible within a major version."
- "SDK must run on JDK 8 without modification."
- "SDK must add no more than 5 transitive dependencies."

Constraints are embedded directly into the relevant module blueprint and surface as
explicit rules in the spec's "Constraints" section.

### Input 5: Test Instructions and References (from PRD.md)

Each module's `### Test` and `### References` sections feed:

- **Test**: The test plan section of the module SPEC.md â€” what scenarios MockWebServer
  must cover, what fixtures are needed.
- **References**: The "External Documentation" subsection of the module SPEC.md â€” links
  back to the upstream API docs, RFCs, vendor SDK comparisons, etc. Carry version tags
  through.

### Input 6: Module Model (from model/ folder, if present)

Read `<app_folder>/context/model/MODEL.md` first as the index, then read individual
module files in each module subfolder.

For an SDK, "models" are the request/response Java classes that mirror the remote API's
schema â€” NOT database entities. Per-module model files (e.g.,
`model/auth/model.md`) define:

- The fields, types, and JSON property names for each model class
- Whether a model is a request DTO, response DTO, or both
- Validation rules to enforce client-side before sending the HTTP call
- Enum values and how they map to JSON strings

The model directly maps to:

- Immutable Java model classes (records on JDK 16+; final classes with `Builder` on JDK 8)
- The hand-written JSON serializer field tables
- Argument types of public facade methods

If MODEL.md is absent, derive models entirely from the OpenAPI spec (Input 7) and the
user stories.

## PRD.md Extended Sections

Before determining optional components, check PRD.md for the following extended sections.
**These are critical for SDK generation** â€” they define the protocols the SDK must
support and the design patterns it must follow.

### Input 7: API Surface Source â€” Swagger UI URL or OpenAPI Spec (CRITICAL)

**This is the highest-priority input for the SDK spec.** Before any other determination,
scan the entire `PRD.md` for one of:

| Pattern                                                          | Action                                          |
|------------------------------------------------------------------|-------------------------------------------------|
| A URL ending in `/swagger-ui.html`, `/swagger-ui/index.html`, `/swagger`, or `/api-docs` | Record as `swaggerUiUrl`               |
| A URL ending in `/v3/api-docs`, `/openapi.json`, `/openapi.yaml`, or `/swagger.json` | Record as `openApiSpecUrl`             |
| A relative path to an `openapi.yaml` / `openapi.json` / `swagger.yaml` / `swagger.json` file inside the application folder | Record as `openApiSpecPath` |
| A heading "## Swagger UI", "## OpenAPI Spec", "## API Reference" with a URL/path beneath it | Same as above based on the URL form     |

Scanning order: Architecture Principle section first â†’ "API Reference" / "External APIs"
sections next â†’ fall back to a project-wide grep for `swagger` / `openapi` / `api-docs`.

**Resolution behaviour:**

1. **`openApiSpecUrl` or `openApiSpecPath` found:** This is the authoritative API
   surface. The spec MUST instruct the implementer to read this OpenAPI document and
   generate one model class per schema, one facade method per operation, and one URL
   constant per path. The skill should attempt to fetch the spec at generation time (if
   the URL is reachable) so that the generated SPEC.md can list real operation IDs,
   paths, and schema names â€” NOT placeholders.
2. **Only `swaggerUiUrl` found:** Treat the underlying `/v3/api-docs` (or `/api-docs`)
   as the spec endpoint. Note in the spec that the implementer must derive the spec URL
   by inspecting the Swagger UI page.
3. **Neither found, but PRD lists explicit endpoint tables:** Use those tables as the
   authoritative API surface; mark a `[TODO]` reminding the team to publish an OpenAPI
   document.
4. **Nothing found:** Insert a `[TODO]` at the top of the generated SPECIFICATION.md
   reading: `[TODO] No Swagger UI URL or OpenAPI spec found in PRD.md â€” the SDK API
   surface is inferred from user stories only and may drift from the real API.` Then
   proceed using user stories alone.

The chosen API surface source MUST be summarized in the **Project Overview** section of
SPECIFICATION.md so future readers know which document drove the SDK shape.

See `references/api-extraction-patterns.md` for the full procedure.

### Architecture Principle Extraction

If PRD.md contains an `# Architecture Principle` section, extract patterns that affect
SDK design. Treat this section as **authoritative for protocol selection and design
patterns**:

| Pattern in Architecture Principle              | How It Influences the SDK Spec                                                                                    |
|------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| "REST" / "RESTful API"                         | Confirm OkHttp transport (default)                                                                                |
| "WebSocket" / "real-time"                      | Add WebSocket subsection. Use OkHttp's built-in WebSocket on JDK 8; document JDK 11 `HttpClient` WebSocket option |
| "Server-Sent Events" / "SSE"                   | Add SSE subsection backed by OkHttp `EventSource`                                                                 |
| "gRPC"                                         | Add a `[TODO]` â€” OkHttp does not support gRPC natively. Confirm with user before adding `grpc-java`               |
| "AMQP" / "RabbitMQ" / "message queue"          | Add AMQP subsection backed by `com.rabbitmq:amqp-client` only if user confirms                                    |
| "MQTT"                                         | Add MQTT subsection backed by `paho-mqtt-client` only if user confirms                                            |
| "Stateless"                                    | Confirm no client-side session state; every call carries credentials in headers                                   |
| "OAuth2 / Bearer token"                        | Add `AuthInterceptor` to inject `Authorization: Bearer ...` and refresh on 401                                    |
| "API key authentication"                       | Add `AuthInterceptor` to inject the configured API key header                                                     |
| "mTLS"                                         | Add `OkHttpClient` SSL configuration section with custom `X509TrustManager` and `KeyManager`                      |
| "Idempotency-Key" header                       | Add idempotency key generation utility used by all mutating calls                                                 |
| "Builder pattern"                              | Confirm builder pattern on the client and every request DTO                                                       |
| "Fluent API" / "fluent interface"              | Confirm method chaining on the facade (e.g., `client.orders().forCustomer(id).list()`)                            |
| "Strategy pattern" / "pluggable"               | Add a strategy interface (e.g., `RetryStrategy`, `BackoffStrategy`, `CredentialProvider`) that consumers override |
| "Adapter pattern"                              | Confirm the SDK adapts the remote HTTP API to a typed Java API â€” already the default; document it explicitly     |
| "Decorator pattern"                            | Add a decorator section showing how consumers wrap the facade (e.g., for caching, metrics)                        |
| "Observer pattern" / "event listener"          | Add a listener interface (e.g., `RequestLifecycleListener`) consumers can register                                |
| "Reactive" / "non-blocking"                    | Add an async API surface using `CompletableFuture` (JDK 8+, no extra dep)                                         |
| "Thread-safe" / "concurrent"                   | Confirm immutable models, single shared `OkHttpClient`, document thread-safety in javadoc                         |

Every pattern from Architecture Principle that applies MUST be reflected in:

1. The SPECIFICATION.md "Architecture Patterns" section, as a numbered list with the
   class/interface name and a one-paragraph rationale.
2. The relevant module SPEC.md (e.g., the auth interceptor lives in the auth module).

If the section is absent, default to: REST + Builder pattern + Strategy pattern (for
retry) + Adapter pattern (the SDK itself).

### High Level Process Flow Extraction

If PRD.md contains a `# High Level Process Flow` section:

1. Each named flow informs the orchestration helpers the SDK exposes (e.g., a
   "submit and poll until complete" helper combines `POST /jobs` + `GET /jobs/{id}` +
   polling).
2. Multi-step flows become a `*Flow` class on the facade (e.g., `OrderSubmissionFlow`)
   that returns a `CompletableFuture` and internally calls the relevant module services.
3. Error paths in the flow become specific exception types in the SDK's exception hierarchy.

If absent, derive the API surface from user stories + OpenAPI alone (no flow helpers).

---

## Determining Optional Components

After reading all inputs above, produce a determination summary BEFORE generating the
spec. The defaults are aggressively minimal â€” the skill must justify every "yes".

### Protocol Selection

| Signal                                                       | Selection                |
|--------------------------------------------------------------|--------------------------|
| Default                                                      | REST (OkHttp)            |
| Architecture Principle mentions WebSocket / SSE / AMQP / MQTT/ gRPC | Add the named protocol |

### Authentication Selection

| Signal                                                       | Auth Selection           |
|--------------------------------------------------------------|--------------------------|
| OpenAPI `securitySchemes` includes `bearer` / `oauth2`       | Bearer token             |
| OpenAPI `securitySchemes` includes `apiKey`                  | API key (header or query)|
| Architecture Principle mentions mTLS                         | mTLS (additional, not exclusive) |
| OpenAPI `securitySchemes` includes `basic`                   | HTTP Basic               |
| None of the above                                            | None (caller injects own headers) |

### Async API Surface

| Signal                                                       | Async Selection          |
|--------------------------------------------------------------|--------------------------|
| Architecture Principle mentions "reactive", "non-blocking", "async-first" | Yes â€” every method has both sync and `CompletableFuture` overloads |
| User stories mention long-running operations (`upload`, `export`, `report`) | Yes â€” long ops only      |
| Default                                                       | No â€” synchronous only    |

### Logging Strategy

The default is **SLF4J facade only, no binding**. Consumers add their own SLF4J binding.
Override only if the PRD explicitly forbids SLF4J â€” in which case fall back to JUL
(`java.util.logging`) which is in the JDK and adds zero dependencies.

### Model Style

| JDK Baseline   | Model Style                                                        |
|----------------|--------------------------------------------------------------------|
| 8 (default)    | Final classes with explicit Builder, immutable fields, `equals`/`hashCode`/`toString` |
| 16+ (override) | Records (with builder for fields > 6)                              |

The MR-JAR layout permits records via overlays, but for an SDK the public API must be
identical across JDK versions, so models stay as final classes regardless of overlay.

### Summary of Determination

Print before generating the spec:

```
Optional Component Determination:
- API Surface Source:    {{swagger url|openapi url|openapi path|user stories only}}
- Protocols:             REST{{ + WebSocket/SSE/AMQP/MQTT if any}}
- Authentication:        {{Bearer | API Key | mTLS | Basic | None}}
- Async API:             {{yes (all) | yes (long ops) | no}}
- Logging:               {{SLF4J facade | JUL}}
- Model Style:           Final classes with Builder (JDK 8 baseline)
- Multi-Release JAR:     yes (JDK 8 base + JDK 11 overlay)
- Fat JAR:               yes (Maven Shade Plugin)
- Optional protocol deps:
  - org.java-websocket:  {{yes/no}}
  - amqp-client:         {{yes/no}}
  - paho-mqtt-client:    {{yes/no}}
```

If the user disagrees with any determination, allow them to override before proceeding.

## Required Inputs

After determination, these values are needed. Most are derived automatically:

**Auto-derived from context files:**

- **Application name**: From CLAUDE.md
- **Artifact ID**: kebab-case of application name
- **Group ID**: `com.bestinet.urp`
- **Base package**: `com.bestinet.urp.<artifactid_no_hyphens>`
- **Application description**: From CLAUDE.md
- **Modules**: From PRD.md module headings + `model/MODEL.md`
- **API surface source**: Swagger UI URL or OpenAPI spec (Input 7) â€” MANDATORY summary
- **Default base URL**: From the OpenAPI `servers[0].url`, or from the `# Reference`
  section of CLAUDE.md, or `https://api.example.com` placeholder if neither is present
  (with a `[TODO]`)
- **Auth scheme**: Auto-determined (see above)
- **Optional protocols**: Auto-determined (see above)

**From ENVIRONMENT.md (if present, for the demo/diagnostics `main()`):**

- API host, port, default credential â€” used as default values for the diagnostic
  smoke-test only. Never bundle into the JAR; load from environment at runtime.

## Generating the Specification

Once inputs are gathered and optional components are determined, generate the
specification as a **multi-file output split by module**. Read the spec template at
`references/spec-template.md` for the exact structure and content of each section. The
template is the authoritative guide â€” follow it closely.

The specification is split into two categories:

1. **Root `SPECIFICATION.md`** â€” Shared infrastructure: Maven config (with
   Multi-Release + Shade plugins), source layout, `OkHttpClient` setup, transport
   utilities, JSON support, error model, retry strategy, the top-level `Client` facade,
   and packaging.
2. **Per-module `<module-name>/SPEC.md`** â€” Each module gets its own folder with a
   self-contained specification covering its model classes, service facade,
   request/response payloads, OpenAPI operation mapping, error mapping, and tests.

**Important:** The generated spec must use **real application data** from the context
files:

- **Modules** must use the actual module names from PRD.md / MODEL.md
- **Operation IDs and paths** must come from the OpenAPI spec when available
- **Model fields** must match the OpenAPI schemas (or MODEL.md) â€” never placeholders
- **Public methods** must map to real user stories
- **Version tags** on every user story ID, NFR ID, constraint ID
- **Removed / Replaced items** listed for deprecated items

### Output Structure

```
<app_folder>/context/specification/
â”œâ”€â”€ SPECIFICATION.md              â† Shared infrastructure + TOC
â”œâ”€â”€ auth/
â”‚   â””â”€â”€ SPEC.md                   â† Module blueprint for 'auth'
â”œâ”€â”€ orders/
â”‚   â””â”€â”€ SPEC.md                   â† Module blueprint for 'orders'
â””â”€â”€ ...                           â† One folder per module from PRD.md
```

### What Goes in `SPECIFICATION.md` (Root)

#### 1. Project Overview

Application metadata, description, target consumers, **API Surface Source** (the
recorded Swagger UI URL or OpenAPI path), default base URL, supported JDK range
(8 baseline + 11 overlay), distribution strategy (Maven Central / internal Nexus /
GitHub release attachment), and the complete module list.

#### 2. Maven Configuration (`pom.xml`)

Complete `pom.xml` with:

- `<packaging>jar</packaging>`
- `<groupId>`, `<artifactId>`, `<version>` from inputs
- A single `okhttp` runtime dependency, plus the test-scoped dependencies
- `maven-compiler-plugin` configured TWICE via `<executions>`:
  - **Default execution**: compiles `src/main/java` with `<release>8</release>`
  - **Overlay execution**: compiles `src/main/java11` with `<release>11</release>`,
    output redirected to `target/classes-java11`
- `maven-jar-plugin` configured with `<Multi-Release>true</Multi-Release>` in the manifest
  and an `<archive>` block that copies the JDK 11 overlay into
  `META-INF/versions/11/` of the resulting JAR
- `maven-shade-plugin` configured to build a fat JAR (`<shadedArtifactAttached>false</shadedArtifactAttached>`),
  relocate any internal Kotlin/Okio packages under `<base-package>.shaded.*` to avoid
  classpath collisions, exclude test-scoped artifacts, and **preserve the
  Multi-Release manifest entry** so MR-JAR semantics survive shading
- `maven-source-plugin` and `maven-javadoc-plugin` for source/javadoc JARs
- `maven-surefire-plugin` running JUnit 5
- `<properties>` for versions

The complete sample `pom.xml` MUST appear in this section. No fragments.
See `references/packaging-patterns.md` for the canonical configuration.

#### 3. Source Layout

```
src/
â”œâ”€â”€ main/
â”‚   â”œâ”€â”€ java/                                  â† JDK 8 baseline â€” ALL public API lives here
â”‚   â”‚   â””â”€â”€ com/bestinet/urp/{{artifactid}}/
â”‚   â”‚       â”œâ”€â”€ {{ClientName}}.java            â† Top-level facade + Builder
â”‚   â”‚       â”œâ”€â”€ {{ClientName}}Config.java      â† Immutable config (timeouts, baseUrl, auth)
â”‚   â”‚       â”œâ”€â”€ auth/                          â† Auth interceptor + credential provider
â”‚   â”‚       â”œâ”€â”€ http/                          â† OkHttp wiring, interceptors, retry
â”‚   â”‚       â”œâ”€â”€ json/                          â† Hand-written minimal JSON utility
â”‚   â”‚       â”œâ”€â”€ error/                         â† Exception hierarchy
â”‚   â”‚       â”œâ”€â”€ util/                          â† Internal helpers (no public API)
â”‚   â”‚       â””â”€â”€ {{module1}}/                   â† One package per module
â”‚   â”‚           â”œâ”€â”€ {{Module1}}Service.java    â† Module facade (public)
â”‚   â”‚           â”œâ”€â”€ model/                     â† Request/response models (public)
â”‚   â”‚           â””â”€â”€ internal/                  â† Internals (package-private)
â”‚   â”œâ”€â”€ java11/                                â† JDK 11 overlay â€” same package paths only
â”‚   â”‚   â””â”€â”€ com/bestinet/urp/{{artifactid}}/
â”‚   â”‚       â””â”€â”€ util/
â”‚   â”‚           â””â”€â”€ HttpUtil.java              â† e.g., uses java.net.http.HttpClient
â”‚   â””â”€â”€ resources/
â”‚       â””â”€â”€ META-INF/
â”‚           â””â”€â”€ services/                      â† (only if SPI is exposed)
â””â”€â”€ test/
    â””â”€â”€ java/
        â””â”€â”€ com/bestinet/urp/{{artifactid}}/
            â””â”€â”€ ...                            â† MockWebServer-based tests
```

**Multi-Release JAR rules:**

- Every class under `src/main/java11` MUST also exist under `src/main/java` with an
  identical public signature (the JDK 8 fallback). The JVM picks the JDK 11 version
  automatically when running on JDK 11+.
- Overlay classes are reserved for performance/feature wins on newer JDKs (e.g.,
  `java.net.http.HttpClient`-based fast-path, `String.formatted`, `List.of`). They are
  NOT used to introduce new public API.
- The fat JAR built by Shade preserves `Multi-Release: true` in `META-INF/MANIFEST.MF`
  and copies overlay classes into `META-INF/versions/11/`.

#### 4. OkHttpClient Setup

`http/HttpClientFactory.java` â€” builds a single shared `OkHttpClient` with:

- Connection pool: max idle = 10, keep-alive = 5 min (configurable via `Config`)
- Connect / read / write timeout (default 30 s, configurable)
- `AuthInterceptor` (only if Auth != none)
- `RetryInterceptor` (always, with `RetryStrategy` strategy)
- `CorrelationIdInterceptor` (adds `X-Correlation-Id` if not already set)
- `LoggingInterceptor` (only if SLF4J is on the classpath; otherwise no-op)

The factory is package-private; the `Client.Builder` is the only entry point.
Document thread-safety: a single `OkHttpClient` is safe to share across threads and
must be reused by consumers â€” never create one per request.

See `references/http-client-patterns.md` for the full configuration.

#### 5. JSON Support (Hand-written)

`json/Json.java` â€” a minimal, hand-written JSON parser/writer that handles only what
the SDK's models need: objects, arrays, strings, numbers, booleans, null. No reflection,
no annotations. Each model class implements `toJson(JsonWriter)` and provides a static
`fromJson(JsonReader)`.

This is intentional. JSON is the largest source of dependency conflicts in Java SDKs,
and hand-coded read/write methods make every wire-format change a deliberate, reviewable
edit. If the OpenAPI spec is large enough that hand-writing becomes onerous, document a
codegen step (e.g., a small `JsonModelGenerator` invoked at build time from the OpenAPI
spec) â€” but still emit hand-written-style code, not Jackson annotations.

See `references/spec-template.md` for the exact `Json` class shape and per-model
serializer pattern.

#### 6. Error Model

`error/SdkException.java` (base, unchecked) with subclasses:

- `SdkApiException` â€” non-2xx HTTP response. Carries `int statusCode`, `String body`,
  optional parsed error model, and the original `Request` URL/method.
- `SdkAuthException extends SdkApiException` â€” 401/403.
- `SdkClientException extends SdkException` â€” local I/O, JSON, or validation failure.
- `SdkTimeoutException extends SdkClientException` â€” wraps OkHttp timeout exceptions.
- `SdkRetryExhaustedException extends SdkClientException` â€” retry budget consumed.

All exceptions are `RuntimeException` subclasses â€” checked exceptions in a public Java
SDK API are widely considered an anti-pattern.

#### 7. Retry Strategy

`http/RetryInterceptor.java` invokes `RetryStrategy` (interface) â€” default
implementation `ExponentialBackoffRetryStrategy` retries on connection failure, 502, 503,
504 with `min(maxBackoff, base * 2^attempt + jitter)` delays. The strategy is pluggable
via `Client.Builder#retryStrategy(...)` so consumers can supply their own.

#### 8. Authentication *(conditional)*

If Auth = Bearer token: `auth/BearerCredentialProvider.java` interface +
`StaticBearerCredentialProvider` default. `AuthInterceptor` reads from the provider on
every request; on 401, it calls `provider.refresh()` and replays once.

If Auth = API key: similar but with the configured header name (e.g., `X-API-Key`).

If Auth = mTLS: document `OkHttpClient.Builder#sslSocketFactory` configuration with a
custom `X509TrustManager` + `KeyManager`. Provide a helper that loads a PKCS12 keystore
from a path provided by the consumer.

If Auth = Basic: simple `Credentials.basic(user, pass)` injection.

#### 9. Top-Level Client Facade

`{{ClientName}}.java` â€” the main entry point consumers use:

```java
{{ClientName}} client = {{ClientName}}.builder()
    .baseUrl("https://api.example.com")
    .credentials(BearerCredentialProvider.of("..."))
    .connectTimeout(Duration.ofSeconds(30))
    .build();

OrderDto order = client.orders().getById("ORD-123");
```

The facade is immutable and thread-safe. Each module is exposed as a method
(`client.orders()`, `client.auth()`, `client.users()`) that returns a cached service
instance. The Builder validates required fields (`baseUrl`) before producing the client.

#### 10. Diagnostic Main *(optional, very small)*

If the user explicitly asks, include a `cli/Diagnose.java` with a `public static void
main(String[] args)` that performs a single smoke-test call against the configured base
URL and prints the result. This adds no dependencies (only the SDK itself) and is
useful for `java -jar my-sdk-1.0.0.jar`. The fat-JAR manifest's `Main-Class` points to
this class. Otherwise, omit `Main-Class` so the JAR is library-only.

#### 11. Logging Strategy

If Logging = SLF4J facade: declare `org.slf4j:slf4j-api` as `<scope>provided</scope>` in
Maven so it is NOT bundled into the fat JAR. The SDK uses `LoggerFactory.getLogger(...)`
internally. If no SLF4J binding is on the consumer's classpath, the no-op binding ships
silently â€” this is the standard SLF4J behaviour.

If Logging = JUL: zero dependencies; the SDK uses `java.util.logging.Logger` directly.

#### 12. Testing Strategy

JUnit 5 + AssertJ + OkHttp `MockWebServer`. Each module has a `*ServiceTest.java` that
spins up a `MockWebServer`, configures the SDK to point at it, enqueues canned
responses, and asserts the SDK behavior. Document one full sample in this section.

See `references/spec-template.md` for the canonical test pattern.

#### 13. Packaging & Distribution

Two artifacts are produced:

1. **Thin JAR** (`target/{{artifactId}}-{{version}}.jar`) â€” for Maven consumers. Has
   declared dependencies in `pom.xml`.
2. **Fat JAR** (`target/{{artifactId}}-{{version}}-shaded.jar` â€” but Shade is
   configured with `<finalName>` to overwrite the thin JAR's name when desired) â€” for
   classpath drop-in. Contains all runtime dependencies relocated under
   `com.bestinet.urp.{{artifactid}}.shaded.*` to avoid collisions.

Both artifacts are Multi-Release JARs (MR-JAR layout preserved through Shade).

`mvn package` produces both. The Shade plugin's `Multi-Release: true` manifest entry
is the easiest thing to lose during shading â€” the spec MUST include the explicit
`ManifestResourceTransformer` and `<resource>true</resource>` configuration that
preserves it.

Distribution targets:

- Maven Central: signed (gpg) deploy via `nexus-staging-maven-plugin`.
- Internal Nexus: standard `mvn deploy` to the configured repository.
- GitHub Releases: attach the fat JAR to the release.

See `references/packaging-patterns.md` for the full Maven snippets.

#### 14. Public API Surface & Compatibility

Every public type and method is annotated with `@since 1.0.0` (matching the introducing
version) in javadoc. Removed APIs are marked `@Deprecated` for at least one minor
version before deletion. The spec describes a `revapi` or `japicmp` Maven plugin
configuration to enforce binary compatibility on every release build (optional but
strongly recommended).

#### 15. Fat JAR Verification

After `mvn package`, the spec instructs implementers to run:

```
jar tf target/{{artifactId}}-{{version}}.jar | head -50
unzip -p target/{{artifactId}}-{{version}}.jar META-INF/MANIFEST.MF
jar tf target/{{artifactId}}-{{version}}.jar | grep META-INF/versions/11/
```

â€¦and to verify:

- `META-INF/MANIFEST.MF` contains `Multi-Release: true`
- `META-INF/versions/11/` contains every overlay class
- All OkHttp/Okio/Kotlin classes are present under
  `com/bestinet/urp/{{artifactid}}/shaded/...`
- No unrelocated `okhttp3.*` / `okio.*` / `kotlin.*` packages exist at the JAR root
- The diagnostic main (if present) runs on JDK 8, 11, 17, and 21

### What Goes in Each `<module-name>/SPEC.md` (Per-Module)

For EACH module from PRD.md, create a folder named after the module (kebab-case) and
generate a `SPEC.md` inside it. Each file is **self-contained** â€” a coding agent can
implement the module after the shared infrastructure is in place.

Each module SPEC.md must include:

- **Header** with module name and back-reference to root `SPECIFICATION.md`
- **Traceability**: user story IDs, NFR IDs, constraint IDs, test IDs, reference IDs,
  with version tags
- **OpenAPI Operation Mapping** â€” table mapping each user story to the upstream
  operation ID, HTTP method, path, and OpenAPI schemas (request body, response body)
- **Public API**:
  - Module facade interface and class (`{{Module}}Service`)
  - Request DTOs (final classes with Builder)
  - Response DTOs (final classes with Builder)
  - Module exception class (extends `SdkApiException`)
- **Internal Implementation**:
  - Service implementation (`internal/{{Module}}ServiceImpl`)
  - URL constants
  - JSON serializer methods per model
- **Error Mapping** â€” table mapping HTTP status codes to specific exception subclasses
- **Test Plan** â€” derived from PRD `### Test` section, expressed as MockWebServer scenarios
- **External References** â€” derived from PRD `### References` section
- **Complete code samples** for every component

See `references/spec-template.md` for the canonical module SPEC.md structure and
`references/http-client-patterns.md` for the OkHttp call pattern every service method
must follow.

## Changelog Append

After all specification files are successfully generated, append an entry to
`CHANGELOG.md` in the application folder (`<app_folder>/CHANGELOG.md`):

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
4. If the section **does not exist**: insert a new section after the `---` below the
   context header and before any existing `## vX.Y.Z` section (newest-first ordering),
   with a new table header and the first row.
5. Row format: `| {YYYY-MM-DD} | {application_name} | specgen-sdk-java | {module or "All"} | Generated Java SDK technical specification |`
6. **Never modify or delete existing rows.**

## Output Format

```
<app_folder>/context/specification/
â”œâ”€â”€ SPECIFICATION.md              â† Root: TOC + shared infrastructure
â”œâ”€â”€ <module-1>/
â”‚   â””â”€â”€ SPEC.md                   â† Self-contained module blueprint
â”œâ”€â”€ <module-2>/
â”‚   â””â”€â”€ SPEC.md
â””â”€â”€ <module-N>/
    â””â”€â”€ SPEC.md
```

**Sample code is mandatory.** Every component described in any spec file must include a
complete, self-explanatory code sample. The code must be continuous (no `// ...` gaps)
and usable as a direct reference by a coding agent.

## Constraints

These constraints are non-negotiable. Every code sample in the generated spec must
follow them.

### Universal Constraints

**Library, not application.** No `main()` (except the optional diagnostic), no Spring,
no application server, no static singletons exposed publicly, no global mutable state.

**Minimum dependencies.** OkHttp is the ONLY runtime third-party dependency unless an
optional protocol is selected. JSON, retry, validation, logging facade, builders are
all hand-coded against the JDK. Every additional dependency the spec proposes must
include a one-paragraph justification explaining why the JDK + OkHttp cannot do the job.

**Multi-Release JAR.** Sources under `src/main/java` MUST compile with `--release 8`.
Sources under `src/main/java11` MUST compile with `--release 11` and MUST NOT introduce
new public API â€” they are performance/feature overlays only. The fat JAR's
`META-INF/MANIFEST.MF` MUST contain `Multi-Release: true` and `META-INF/versions/11/`
MUST contain the overlay classes.

**Fat JAR is the headline artifact.** The Shade configuration must produce a fat JAR
with relocated transitive dependencies. The thin JAR with declared dependencies is
also produced for Maven consumers.

**Constructor injection â€” no setters on services.** The facade and every service take
their collaborators (HTTP client, config, JSON utility) via the constructor and store
them in `private final` fields. Builders mutate state during construction but the
resulting object is immutable.

**Immutable models.** Model classes are `final`, all fields are `private final`, no
setters, only a Builder. `equals`, `hashCode`, and `toString` are explicit (or generated
via `Objects.hash` / `String.format`) â€” no Lombok.

**Thread-safe by design.** A single `{{ClientName}}` instance is safe to share across
threads. The shared `OkHttpClient` is the only HTTP transport instance. Services hold
references to the shared client; they do not create new ones.

**No checked exceptions in the public API.** Every public method declares only
`RuntimeException` subclasses (the SDK's own hierarchy). Internal `IOException` is
caught and rewrapped as `SdkClientException` or `SdkApiException`.

**Every public type and method is javadoc'd.** No exceptions. Tools (IDE,
Maven Javadoc plugin) drive consumer adoption.

**No reflection on consumer types.** Models are static; serialization is explicit.

**Deterministic JSON output.** Map iteration order is preserved (`LinkedHashMap`),
booleans serialize as `true`/`false`, numbers without unnecessary trailing zeros.

### Conditional Constraints

**If Auth = Bearer token:**

- Tokens are NEVER logged. The `LoggingInterceptor` MUST redact `Authorization`
  header values to `Bearer ***`.
- Tokens are stored only in the `BearerCredentialProvider` â€” never in `Config` itself.

**If Auth = mTLS:**

- The keystore path and password are read from the `Config` and applied to a fresh
  `SSLSocketFactory` at client-build time. The keystore file is never bundled.

**If Async = yes:**

- Every async method returns `CompletableFuture<T>` and never blocks the calling
  thread. Internal blocking calls are dispatched to OkHttp's dispatcher (which already
  uses its own executor) â€” the SDK never spins up its own thread pool unless the user
  supplies one.

**If WebSocket protocol is selected:**

- Use `OkHttpClient.newWebSocket(...)` on JDK 8. JDK 11 overlay MAY use
  `java.net.http.HttpClient.newWebSocketBuilder()` for performance, but the public API
  surface (`Subscription` interface) MUST be identical across overlays.

**If AMQP / MQTT is selected:**

- The relevant client lib (`amqp-client` / `paho-mqtt-client`) is a runtime dependency
  AND is shaded into the fat JAR with the same relocation rule as OkHttp.

**If a `main()` (diagnostic) is included:**

- It reads `BASE_URL`, `API_TOKEN`, etc. from environment variables only â€” never
  hardcoded.
- The fat JAR's `Main-Class` manifest entry points to `cli.Diagnose`; otherwise omit
  `Main-Class` entirely.

## Principles Embedded in the Spec

### Always-Applicable Principles

- Java 8 source baseline, Multi-Release JDK 11 overlay
- One runtime third-party dependency: OkHttp
- One artifact: a Multi-Release fat JAR; a thin JAR is a side effect of `mvn package`
- Hand-written JSON for every model â€” no reflection-based JSON libraries
- Builder pattern on the client and every request DTO
- Strategy pattern for retry / backoff / credential provider
- Adapter pattern: the SDK adapts the remote HTTP API to a typed Java API
- Constructor injection, immutable services, thread-safe shared transport
- Unchecked exceptions only in the public API
- All modules share one `OkHttpClient`
- Every request goes through the same interceptor chain (auth, retry, correlation, logging)
- OpenAPI is the source of truth for endpoint paths, schemas, and operation IDs
- MockWebServer drives every test â€” no live calls
- Javadoc on every public type and method
- Public API is binary-compatible within a major version (japicmp / revapi enforced)

### Conditional Principles

- **If Auth = Bearer:** 401 triggers a single transparent refresh-and-retry; never two.
- **If Async = yes:** sync methods are convenience wrappers around the async ones â€”
  `Service.foo(...)` calls `Service.fooAsync(...).join()`, not the other way around.
- **If WebSocket:** the public WebSocket API exposes only `connect`, `send`, `close`,
  and a listener interface. No raw `okhttp3.WebSocket` ever escapes the package.
- **If AMQP / MQTT:** these are exposed as separate top-level facades
  (`client.amqp()`, `client.mqtt()`), not mixed into the REST modules.
