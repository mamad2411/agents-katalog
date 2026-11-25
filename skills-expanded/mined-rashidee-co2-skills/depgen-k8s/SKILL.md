---
name: depgen-k8s
model: claude-sonnet-4-6
effort: high
description: >
  Generate a Dockerfile and Kubernetes manifests for an application targeting a single
  environment. Supports Spring Boot (Java), Laravel (PHP), and Node.js application stacks.
  Auto-detects the stack from project files (pom.xml, composer.json, package.json), reads
  CLAUDE.md dependencies, SPECIFICATION.md tech stack, and the application's externalized
  environment variables. Generates a Dockerfile in the application root folder and Kubernetes
  manifest YAML files directly in `<app_folder>/k8s/` (no per-environment subfolders — the
  k8s/ folder is gitignored, each machine maintains its own copy).
  Standardized input: application name (mandatory), environment (optional).
  Use this skill whenever the user asks to create deployment artifacts, Dockerfiles,
  Kubernetes manifests, or containerize an application. Also trigger when the user says
  things like "deploy this app", "containerize this", "create a Dockerfile",
  "generate k8s manifests", or any request for deployment-related artifacts.
---

# Deployment Artifact Generator — Kubernetes

This skill generates deployment artifacts for a custom application:

1. **Dockerfile** — A production-ready, multi-stage container build file placed in the
   application root folder.
2. **Kubernetes manifests** — Manifest files stored directly in the application's own
   `k8s/` folder for a **single target environment**. Since the `k8s/` folder is gitignored,
   each machine maintains its own independent copy of the manifests with environment-specific
   ConfigMap/Secret values (hostnames, credentials, resource limits).

**Note:** Only custom applications (from `# Custom Applications` in CLAUDE.md) are processed.
3rd party supporting applications and external services are NOT containerized by this skill.

## Inputs

```
/depgen-k8s <application> [environment]
```

| Argument | Required | Example | Description |
|----------|----------|---------|-------------|
| `<application>` | Yes | `hub_middleware` | Application name — must be a custom application from CLAUDE.md |
| `<environment>` | No | `home_server` | Target environment name — must match a Kubernetes environment in CLAUDE.md |

If `<environment>` is omitted:
- If CLAUDE.md defines exactly **one** Kubernetes environment → auto-select it.
- If CLAUDE.md defines **multiple** Kubernetes environments → list them and ask the user to specify.

The environment name is matched **case-insensitively** against the environment headings in CLAUDE.md, accepting snake_case, kebab-case, or title-case input (e.g., `home_server`, `home-server`, `Home Server`).

No `version:` or `module:` arguments — deployment is application-level.

### Input Resolution

The application name is matched against root-level application folders:
1. Strip any leading `<number>_` prefix from folder names (e.g., `1_hub_middleware` → `hub_middleware`)
2. Match case-insensitively against the provided application name
3. Accept snake_case, kebab-case, or title-case input
4. Verify the application is listed under `# Custom Applications` in CLAUDE.md — reject if it is a 3rd party application or external service
5. If no match found, list available custom applications and stop

### Auto-Resolved Paths

| File | Resolved Path |
|------|---------------|
| CLAUDE.md | Project root `CLAUDE.md` |
| ENVIRONMENT.md | Project root `ENVIRONMENT.md` |
| SPECIFICATION.md | `<app_folder>/context/specification/SPECIFICATION.md` |
| Source code | `<app_folder>/` (pom.xml, composer.json, package.json, etc.) |
| Application config | Stack-dependent (see detection) |
| K8s manifests output | `<app_folder>/k8s/` (gitignored — each machine maintains its own copy) |

## PRD.md Extended Sections

Before generating deployment artifacts, check PRD.md for the following extended sections:

### Architecture Principle

If PRD.md contains an `# Architecture Principle` section, extract patterns that affect deployment:

| Pattern | Deployment Impact |
|---|---|
| "Stateless" | Deployment uses `RollingUpdate` strategy without sticky sessions; no PVC needed for session storage |
| "Container based deployment" | Validates this skill's applicability |
| "Scale out" / "horizontally scalable" | Generate HorizontalPodAutoscaler (HPA) manifest targeting CPU 70% |
| Specific resource constraints (e.g., "max 256Mi per pod") | Use as default resource limits in K8s manifests |
| "Message driven" / "message queue" | Readiness probe should verify message queue connectivity |

If absent, use defaults from SPECIFICATION.md and CLAUDE.md (existing behavior).

### High Level Process Flow

If PRD.md contains a `# High Level Process Flow` section:
- Process flows reveal inter-system dependencies (message queues, external service endpoints)
- Validate that the environment variable list and ConfigMap/Secret values include all dependencies mentioned in process flows
- If a flow references an external system not in the `Depends on` list, log a warning

If absent, derive dependencies from CLAUDE.md only (existing behavior).

---

## Pre-Requisites

Before running this skill, the following must exist:
- **Source code** — The application must be implemented (not just context artifacts)
- **SPECIFICATION.md** — The technical specification must exist (generated by a `specgen-*` skill)
- **Externalized configuration** — The application config must use environment variables
  (e.g., `${ENV_VAR:default}` in Spring Boot, `env('VAR')` in Laravel, `process.env.VAR` in Node.js)

If any are missing, stop and inform the user.

## Workflow

### Phase 0: Validate Inputs

1. Resolve application folder from the provided name
2. Verify the application is a custom application in CLAUDE.md (not 3rd party or external service)
3. Verify source code exists (at least one of: `pom.xml`, `composer.json`, `package.json`)
4. Verify `<app_folder>/context/specification/SPECIFICATION.md` exists
5. Read `CLAUDE.md` (already in context) for project-level information
6. **Detect environments** from CLAUDE.md's `# Environment` section:
   - Each `## <Environment Name>` heading under `# Environment` is an environment
   - For each environment, extract:
     - Environment name (e.g., "Home Server")
     - `Domain` field (e.g., `localhost`, `home.server`)
     - `Deployment Type` field (e.g., `Manual`, `Kubernetes`)
     - `IP` field (from SSH Configuration or direct IP field) if present — needed for `hostAliases` generation in Phase 3
   - If no environments are defined, stop with error: "No environments found in CLAUDE.md `# Environment` section."

7. **Select target environment** — filter to Kubernetes environments and select one:
   1. Filter environments to those with `Deployment Type: Kubernetes`.
   2. If no environment has `Deployment Type: Kubernetes`, stop with error: "No Kubernetes environments found in CLAUDE.md. This skill only generates K8s manifests for environments with Deployment Type: Kubernetes."
   3. If the user provided an `<environment>` argument, match it against the Kubernetes environments (case-insensitively, accepting snake_case, kebab-case, or title-case).
      - If matched → use it as the target environment.
      - If not matched → list available Kubernetes environments and stop.
   4. If no argument was provided:
      - If exactly **one** Kubernetes environment exists → auto-select it.
      - If **multiple** exist → list them and ask the user to specify.
   5. Record the selected environment's Domain and IP for Phase 3.

### Phase 1: Detect Application Stack

#### Step 1 — Identify Stack

Check the application root for build files:

| File Found | Stack | Build Tool |
|---|---|---|
| `pom.xml` | `spring-boot` | Maven |
| `composer.json` | `laravel` | Composer |
| `package.json` (no `pom.xml` or `composer.json`) | `nodejs` | npm / pnpm |

If none found, stop with error: "Cannot determine application stack."

If multiple found (e.g., `pom.xml` + `package.json`), prioritize: `pom.xml` > `composer.json` > `package.json`
(the `package.json` is likely for frontend or E2E tests, not the main app).

#### Step 2 — Extract Stack-Specific Metadata

**If `spring-boot`:**
- Read `pom.xml`:
  - `<java.version>` → JDK version for base image
  - `<artifactId>` → image name
  - `<version>` → image tag
  - `frontend-maven-plugin` presence → has frontend build step
  - `jte-maven-plugin` presence → has JTE precompilation
  - `spring-boot-maven-plugin` → executable JAR packaging
- Read `src/main/resources/application.yml`:
  - Extract all `${ENV_VAR:default}` patterns via regex `\$\{([^:}]+)(?::([^}]*))?\}`
  - `server.port` default → exposed container port
- Read `.env` (if exists) → local dev values for reference

**If `laravel`:**
- Read `composer.json`:
  - `require.php` → PHP version for base image
  - `require.laravel/framework` → Laravel version
  - `name` → image name
- Read `.env.example` or scan `config/*.php`:
  - Extract all `env('VAR', 'default')` patterns via regex `env\('([^']+)'(?:,\s*'?([^')*]*)'?)?\)`
  - `APP_PORT` or default `8000` → exposed container port
- Check for `vite.config.js` or `webpack.mix.js` → has frontend build step
- Check for `package.json` in app root → Node.js needed for frontend build

**If `nodejs`:**
- Read `package.json`:
  - `engines.node` → Node.js version for base image
  - `name` → image name
  - `version` → image tag
  - `scripts.build` → build command (e.g., `tsc`, `tsup`, `vite build`, `next build`)
  - `scripts.start` → start command
- Scan source files or `.env` for `process.env.VAR` patterns
- Check for `tsconfig.json` → TypeScript build step
- Determine framework: Express, Fastify, NestJS, Next.js, etc.

#### Step 3 — Common Detection (All Stacks)

From `CLAUDE.md` → extract the "Depends on" list for the target application:

| Dependency Pattern | External Service |
|---|---|
| References MongoDB | MongoDB required |
| References MySQL / HC Database / SC Database | MySQL required |
| References PostgreSQL | PostgreSQL required |
| References Hub Single Sign On / Keycloak | Keycloak required |
| References RabbitMQ / Message Queue | RabbitMQ required |
| References Redis / Hub Cache | Redis required |
| References SMTP / Mailcatcher | SMTP service required |
| References Meilisearch / Hub Search Engine | Meilisearch required |

From `SPECIFICATION.md` → extract:
- Technology stack table (versions)
- Environment variable reference table (if present)

#### Step 4 — Classify Environment Variables

For each detected environment variable, classify as ConfigMap or Secret:

**Secret** (sensitive — stored in K8s Secret):
- Variable name contains `PASSWORD`, `SECRET`, `KEY`, `TOKEN`, `CREDENTIAL`
- Variable name contains `ADMIN_USERNAME` (admin-level credentials)
- Variable name is a database connection URI containing credentials

**ConfigMap** (non-sensitive — stored in K8s ConfigMap):
- Everything else: hostnames, ports, log levels, feature flags, queue names, CORS origins

#### Step 5 — Determine Health Check

| Stack | Default Health Endpoint | Condition |
|---|---|---|
| Spring Boot | `/actuator/health` | If `spring-boot-starter-actuator` in pom.xml |
| Spring Boot | `/` (HTTP 200/302 check) | If no actuator |
| Laravel | `/health` or `/` | Custom route or root |
| Node.js | `/health` or `/` | Custom route or root |

Check if a health endpoint is explicitly defined in the source code. If not, use the
default for the stack.

#### Step 6 — Present Detection Summary

Before generating, present findings to the user for confirmation:

```
Application Stack Detection:
- Stack:           Spring Boot 3.5.7 (Java 21)
- Artifact:        hub-middleware:1.0.3
- Frontend Build:  Yes (Vite via frontend-maven-plugin)
- JTE Precompile:  Yes (jte-maven-plugin)
- Exposed Port:    8080
- Health Check:    /actuator/health (actuator present)

External Services:
- MongoDB 7.0.6 (Hub Core Database)
- Keycloak 26.5.3 (Hub Single Sign On)
- RabbitMQ 3.11.9 (HC + SC Adapter Message Queues)
- Mailcatcher 0.8.1 (SMTP)

Environment Variables: 25 detected
- ConfigMap: 18 (hostnames, ports, log levels, queue names, flags)
- Secret: 7 (passwords, admin credentials)
```

If the user disagrees, allow overrides before proceeding.

### Phase 2: Generate or Update Dockerfile

1. Check if `<app_folder>/Dockerfile` already exists
2. **If it exists** (UPDATE mode):
   - Read the existing Dockerfile
   - Compare detected values against what the Dockerfile currently has:
     - Base image version (e.g., Java version changed in pom.xml)
     - Exposed port (e.g., server.port default changed)
     - Environment variable defaults (e.g., new env vars added)
     - Build commands (e.g., frontend build step added or removed)
   - Preserve any lines marked with `# CUSTOM:` comments — these are manual overrides
     by the user/DevOps that should not be replaced
   - Update only the parts that changed, keeping the overall structure intact
   - Log what was changed (e.g., "Updated Java version from 17 to 21",
     "Added MAIL_HOST env var")
3. **If it does not exist** (CREATE mode):
   - Select the Dockerfile pattern from `references/dockerfile-<stack>.md`
   - Substitute detected values (Java version, artifact name, port, etc.)
   - Write the Dockerfile to `<app_folder>/Dockerfile`

The Dockerfile MUST:
- Use a **multi-stage build** (build stage + runtime stage)
- Use **specific version tags** for base images (not `latest`)
- Run as a **non-root user** in the runtime stage
- **NOT** copy `.env`, `context/`, `e2e/`, or test files into the image
- Include a `HEALTHCHECK` instruction if a health endpoint is available
- Include comments explaining each significant instruction
- Include a `LABEL version="{version}"` instruction using the application version extracted
  from `pom.xml` (`<version>`), `composer.json` (`version`), or `package.json` (`version`)
- Include a build argument `ARG APP_VERSION={version}` that can be overridden at build time
  via `docker build --build-arg APP_VERSION=1.0.3`

Read `references/dockerfile-spring-boot.md`, `references/dockerfile-laravel.md`, or
`references/dockerfile-nodejs.md` for the complete Dockerfile template per stack.

### Phase 3: Generate or Update Kubernetes Manifests

Kubernetes manifests are stored directly in `<app_folder>/k8s/` (no per-environment
subfolders). Since the `k8s/` folder is gitignored, each machine maintains its own
independent copy with values specific to the target environment selected in Phase 0.

#### 3a. Ensure Folder Structure

1. Check if `<app_folder>/k8s/` exists. If not, create it.

Example folder structure:
```
hub_middleware/
  Dockerfile
  k8s/
    namespace.yaml
    configmap.yaml
    secret.yaml
    deployment.yaml
    service.yaml
    ingress.yaml          (optional)
```

#### 3b. Generate Manifests

Generate individual YAML files inside `<app_folder>/k8s/` using values from the target
environment selected in Phase 0:

1. **`namespace.yaml`** — Namespace resource (use project code from CLAUDE.md in lowercase,
   e.g., `urp`). Shared across all applications — identical content for every environment.
2. **`configmap.yaml`** — Non-sensitive environment variables (from Step 4 classification).
   Values may differ per environment — use defaults from `.env` for local development;
   use `TODO` placeholders for other environments where values are not known.
3. **`secret.yaml`** — Sensitive environment variables (from Step 4 classification),
   base64-encoded. Values use `TODO` placeholders for all non-local environments.
4. **`deployment.yaml`** — Container spec with:
   - Versioned image tag (e.g., `image: hub-middleware:1.0.3`), NOT `latest`
   - `envFrom` referencing ConfigMap and Secret
   - Resource requests/limits (sensible defaults: 256Mi-512Mi memory, 250m-500m CPU)
   - Readiness and liveness probes using the detected health endpoint
   - Non-root `securityContext`
   - `hostAliases` (conditional): If the environment's Domain from CLAUDE.md is referenced
     in ConfigMap values AND is not `localhost`, add `hostAliases` mapping the Domain to
     the environment's IP address. This is needed because K8s pod DNS cannot resolve custom
     domains defined only in the host machine's `/etc/hosts`. See `references/k8s-patterns.md`.
5. **`service.yaml`** — ClusterIP service exposing the application port
6. **`ingress.yaml`** (optional) — if the application is a web application or API with
   external access. Only generate if the environment's CLAUDE.md description suggests
   external access (e.g., mentions domain, IP, or ingress).

Read `references/k8s-patterns.md` for the complete manifest templates per resource type.

#### 3c. Environment-Specific Values

When generating manifests for the target environment:

- **ConfigMap and Secret values**: Read `ENVIRONMENT.md` from the project root. If ENVIRONMENT.md
  contains environment-specific credentials (organized by environment), use the matching
  values for the target environment. If values are not found, use `TODO` as placeholder.
- **Resource limits**: Use sensible defaults. If the CLAUDE.md environment description
  mentions resource constraints, adjust accordingly.
- **Ingress hostnames**: Derive from the target environment description in CLAUDE.md if
  available (e.g., IP address, domain name). Use `TODO` if not specified.

#### 3d. Create or Update Logic

For the `<app_folder>/k8s/` folder:

1. **If a manifest file does not exist** (CREATE mode):
   - Generate the file from the detected values and templates
   - Write to `<app_folder>/k8s/<resource>.yaml`

2. **If it already exists** (UPDATE mode):
   - Read the existing manifest
   - Compare detected values against what the manifest currently has:
     - New or removed environment variables → update configmap.yaml and secret.yaml
     - Image version changed → update deployment.yaml image tag
     - Port changed → update service.yaml and deployment.yaml container port
     - Health endpoint changed → update probes in deployment.yaml
     - New dependencies → add init containers or environment variables
   - Preserve any lines or resources marked with `# CUSTOM:` comments
   - Update only the parts that changed
   - Log what was changed

#### 3e. Namespace Consistency

All manifests use the same namespace (derived from the project code in CLAUDE.md's
`# Project Detail` → Project Code in lowercase, e.g., `urp`).

#### 3f. Docker Build Reference

Include a comment block at the top of `deployment.yaml`:

```yaml
# Application: <Application Name>
# Environment: <Target Environment Name>
# Build: docker build -t <image-name>:<version> <app_folder>/
# Tag:   docker tag <image-name>:<version> <image-name>:latest
# Apply: kubectl apply -f <app_folder>/k8s/
---
```

#### 3g. Update `.gitignore`

The `k8s/` folder contains environment-specific manifests with ConfigMap values,
base64-encoded Secrets, hostnames, and credentials that MUST NOT be committed to
version control. After generating or updating the K8s manifests, ensure the
application's `.gitignore` excludes the `k8s/` folder:

1. Read `<app_folder>/.gitignore`. If it does not exist, create it.
2. Check if `k8s/` (or an equivalent pattern like `k8s/**`) is already listed.
3. If **not already present**, append the following block:

```gitignore

# Kubernetes manifests — environment-specific configs and secrets
k8s/
```

4. If already present, do nothing — do not duplicate the entry.
5. Do NOT remove or modify any other entries in `.gitignore`.

## Constraints

These constraints are non-negotiable:

1. **Custom applications only** — This skill only processes applications listed under
   `# Custom Applications` in CLAUDE.md. 3rd party applications and external services are
   NOT containerized by this skill.

2. **Stack-agnostic output** — The skill must work for Spring Boot, Laravel, and Node.js
   applications. All stack-specific logic is gated behind the detection in Phase 1.

3. **Real values from context** — Every manifest and Dockerfile must use the actual
   application name, port, environment variables, and dependency versions from the project's
   context files. No placeholder `<TODO>` values except for legitimately unknown production
   values (registry URL, domain name).

4. **ConfigMap/Secret separation** — Sensitive values must NEVER appear in ConfigMaps.
   The classification logic in Phase 1 Step 4 must be applied consistently.

5. **Non-root containers** — All Dockerfiles must run the application as a non-root user.

6. **Multi-stage builds** — All Dockerfiles must use multi-stage builds to minimize the
   runtime image size. Build tools (Maven, Composer, npm dev dependencies) must NOT be
   in the final image.

7. **No `.env` in containers** — The `.env` file is for local development only. Container
   environments receive configuration via K8s ConfigMap + Secret injection.

8. **Flat K8s manifest folder** — Kubernetes manifests live directly in `<app_folder>/k8s/`
   with separate YAML files per resource type (no per-environment subfolders). The `k8s/`
   folder is gitignored — each machine maintains its own copy with values specific to
   the target environment. Run the skill once per environment on the target machine.

9. **Idempotent — supports both create and update** — If Dockerfile or manifest already
   exists, read it first, detect what changed, and update only the affected parts. Preserve
   any manual customizations marked with `# CUSTOM:`. If the file does not exist, create
   from scratch. Always log what was created or changed.

10. **Single-pass execution** — This skill completes in one pass (Dockerfile + manifest).
    No Ralph Loop needed.

11. **Production-safe defaults** — Dockerfile and K8s manifests must default to
    production-safe values. Dev-specific settings (JTE dev mode, DevTools, debug logging)
    must be OFF by default in the container, overridden only via explicit environment
    variables.

12. **Versioned image tags** — Kubernetes Deployment manifests must reference versioned
    image tags (e.g., `hub-middleware:1.0.3`), never `latest`.
