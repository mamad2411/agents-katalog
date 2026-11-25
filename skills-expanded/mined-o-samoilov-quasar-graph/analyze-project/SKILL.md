---
name: analyze-project
description: "Internal skill used by quasar-graph:scan sub-agents. Analyzes ONE project directory and writes its project.md. Do NOT invoke directly — only via the scan orchestrator."
user-invocable: false
---

# /quasar-graph:analyze-project

You analyze ONE project for the quasar-graph scanner. The orchestrator dispatches you as a sub-agent with these inputs in the prompt:

- `project_name` — name from `manifest.json`
- `project_path` — absolute path to the project directory
- `session_dir` — absolute path to `.quasar-graph/<session-id>/`
- `manifest` — full content of `manifest.json` (so you can resolve cross-project links)
- `role` — optional. If `role: environment`, this directory is a **deployment/infrastructure environment**, not an app: capture only its `resources[]` (the backing services it operates, including the `kind: gateway` edge layer) and a topology description; do **NOT** emit `connections`, and do not classify it as `service`/client. (For app projects this input is absent.)
- `output_md` — optional. The absolute path to write the result to. If given, use it verbatim instead of the default path below (the orchestrator passes this for environments, pointing under `scan/environments/`).

## What to read

Read only files relevant for technology, resources, and connections. Do NOT read source code beyond config files.

**Where to look:** these config files may sit at the project root OR in a sub-directory (e.g. the manifest lives in `<project>/mcp/package.json` or `<project>/server/`). Search the whole project tree at depth 1–3 below `project_path`, skipping the usual blacklist (`node_modules`, `.venv`, `vendor`, `dist`, `build`, `target`, `.git`, `.quasar-graph`, …). The exception is `README.md` — read the root one only, do not descend.

**Dependency manifests (for language/framework):**
- `package.json`, `pnpm-lock.yaml` (Node)
- `pyproject.toml`, `requirements.txt`, `Pipfile` (Python)
- `go.mod` (Go)
- `Cargo.toml` (Rust)
- `composer.json` (PHP)
- `pom.xml`, `build.gradle`, `build.gradle.kts` (JVM)
- `pubspec.yaml` (Dart/Flutter)
- `Gemfile` (Ruby)

**Environment & resources:**
- `.env`, `.env.example`, `.env.*`
- `docker-compose.yml`, `docker-compose.*.yml`
- `Dockerfile`

**Schema/migration configs (for DB type):**
- `prisma/schema.prisma`
- `drizzle.config.*`
- `alembic.ini`, `migrations/env.py`
- `ormconfig.*`, `data-source.ts`

**Human context:**
- `README.md` (root only, do not descend)

## How to extract

**`language`** — primary language by the manifest file present (`package.json` → `typescript` if tsconfig exists else `javascript`; `go.mod` → `go`; `pubspec.yaml` → `dart`, etc.).

**`framework`** — derive from top-level dependencies:
- Node: `next` / `nestjs` / `express` / `fastify` / `react` (CRA/Vite) / `vue` / `nuxt`
- Python: `django` / `fastapi` / `flask`
- Dart: `flutter` (if `flutter` in `pubspec.yaml`)
- Go: `gin` / `echo` / `fiber` (presence of import in `go.mod`)

**`role`** — classifies the project as a backend **service**, a shared **library**, an **admin panel**, or a **client** app. Emit `role: service` **only** when the project is clearly a backend that exposes an API / listens on a port; emit `role: library` **only** when it is clearly a shared package/SDK that neither serves nor runs; emit `role: admin_panel` **only** when the project is clearly an administration/back-office UI over other services rather than an end-user product; otherwise OMIT the field (the default is a client `project`). Bias to omitting when unsure — same "better to miss than fabricate" rule.
- `service` signals: a backend web framework (`nestjs` / `express` / `fastify` / `django` / `fastapi` / `flask` / `gin` / `echo` / `fiber` / Spring / Laravel / Symfony / Rails); a `Dockerfile` with `EXPOSE`; a server-port env (`PORT` / `APP_PORT` / `SERVER_PORT`); a compose service that publishes a port.
- `library` signals: a `composer.json` with `"type": "library"`; a `package.json` with no server/CLI entrypoint that sibling projects consume as a dependency; a monorepo package without a `Dockerfile` / compose service.
- `admin_panel` signals: an admin-UI framework/dependency (`react-admin` / `@api-platform/admin` / Filament / EasyAdmin / Django admin-only project); a name/README that says admin panel / back office; an ops-only hostname. It still records its outbound `connections` like any client.
- `client` (omit `role`): frontend / mobile / desktop client — `react` / `vue` / `angular` / `svelte` / `flutter` / React Native / Expo / static sites — and also CLIs that don't serve.
- Fullstack ambiguity (`next` / `nuxt`): default to a client (omit `role`) unless it is clearly API-only.

**`port`** — only when `role: service`. The TCP port the service listens on, as an integer. Detect from compose `ports:` / `expose:`, a `Dockerfile` `EXPOSE`, or a `PORT` / `APP_PORT` / `SERVER_PORT` env value. OMIT if unknown — never guess.

**`package_name`** — only when `role: library`, optional. The registry name of the package (`@scope/name` from `package.json`, `vendor/name` from `composer.json`). OMIT if the manifest declares none.

**`resources`** — derive from:
- **Database** — `DATABASE_URL` / `POSTGRES_*` / `MYSQL_*` / `MONGO_*` env vars; `postgres` / `mysql` / `mongo` services in `docker-compose.yml`; `prisma/schema.prisma` provider.
- **Cache** — `REDIS_URL`, `redis` service in compose.
- **Queue** — `RABBITMQ_*`, `KAFKA_*`, `SQS_*` env; corresponding compose services.
- **Storage** — `S3_*`, `AWS_BUCKET`, `MINIO_*`.
- **External services** — known SDKs in dependencies (`stripe`, `sendgrid`, `twilio`, `algolia`, `posthog`, `sentry`) → `external_service`. ENV like `STRIPE_SECRET_KEY` is also a signal.
- **Auth provider** — `firebase-admin`, `auth0`, `clerk`, env `CLERK_*` / `AUTH0_*`.
- **Search** (`kind: search`) — a search engine: `elasticsearch` / `opensearch` / `meilisearch` / `typesense`. Signals: `ELASTICSEARCH_*` / `OPENSEARCH_*` / `MEILI_*` / `TYPESENSE_*` env vars, a matching compose service, or a client SDK in dependencies. SaaS search (e.g. Algolia) stays `external_service`.
- **Realtime** (`kind: realtime`) — self-hosted realtime / pub-sub infrastructure: `centrifugo`, a websocket server, `mercure`. Signals: `CENTRIFUGO_*` / `MERCURE_*` env vars or a matching compose service. SaaS realtime (Pusher, Ably) stays `external_service`.
- **Gateway** (`kind: gateway`) — the edge / infrastructure layer: a reverse proxy, ingress, API gateway, or web server (`traefik`, `nginx`, `envoy`, `haproxy`, `kong`, `caddy`). Signals: a `traefik` / `nginx` / `envoy` service in `docker-compose.yml`, a `traefik.yml` / `nginx.conf` config file, or a gateway image. Set `type` to the specific tech (`traefik`, `nginx`, …). Capture the proxy **itself** as a gateway resource — distinct from its routing rules (see below, which are NOT connections).
  - **`routes` (routing layer, optional).** On a gateway resource you MAY add a `routes:` list naming the downstream targets it forwards traffic to (`- nginx-acme-api`, or `- { to: acme-api, type: routes }`), read from Traefik `Host(...)` routers / service labels and nginx `upstream` / `proxy_pass`. Each `to` is a node **name**: a peer project/service from `manifest`, or another gateway/resource. This is a separate edge **class** (`routes`), NOT a `connection` — it does not break the outbound-only rule, and it is additive (it never replaces the caller's logical edge). It is consumed only by the ingress overlay; capturing it when visible is always safe.

For each resource fill: `kind` (category), `type` (specific tech), `env` (binding env var), `description` (one sentence on how this resource is used in the project — derived from README, dep names, env naming, or compose config; do not invent), optionally `name` and `admin_url`.

**`env`** — list ALL env variable names you saw across `.env*` files, deduplicated. Include resource-bound and standalone (`JWT_SECRET`, `API_VERSION`, ...). Never include the values.

**`connections`** — **OUTBOUND** calls THIS project initiates to a peer project in `manifest`. Record an edge only when this project is the **caller/client**. Each pairwise relationship is declared by exactly ONE side — the caller — so the peer must NOT also declare the reverse; otherwise the graph gets two opposite edges for one relationship.

Signals that this project calls a peer (record these):
- An API base-URL / endpoint env pointing at a peer's host (e.g. `*_API_URL`, `*_BASE_URL`) consumed by an HTTP client (axios / fetch / guzzle) → `via: rest_api` (or `grpc` / `webhook` as appropriate).
- Hostname `service-name` in compose that matches a peer project's name → link by resource type (`shared_database` / `message_queue`).
- `http://localhost:<port>` references that match a peer's exposed port → `via: rest_api`.
- A dependency name in `package.json` that matches a peer project name (monorepo internal) → `via: client_of`.

Do NOT record a connection from **INBOUND / acceptance** config — it only says who may call THIS project, and the *calling* project records that edge from its own side:
- `CORS_ALLOW_ORIGIN`, `allowed_origins`, CSRF / origin allowlists.
- nginx `server_name`, Traefik routing rules / `Host(...)` labels, reverse-proxy upstreams that point at THIS service. (The proxy/ingress **itself** IS a capturable `kind: gateway` resource — see above; its *routing rules* must not become `connections`, but they MAY be captured as that gateway's `routes:` list — the separate routing/ingress layer, not a connection.)
- Webhook receiver allowlists.

Otherwise — do not invent connections. Better to miss than to fabricate.

## Output schema

Write the file to the **absolute** path `<session_dir>/scan/projects/<project_name>/<project_name>.md` (note the `scan/` segment — the orchestrator and the MCP transform read from `scan/projects/`, not a bare `projects/`). **If `output_md` was given as an input, write to that exact path instead** (environments go to `<session_dir>/scan/environments/<name>/<name>.md`).

`session_dir` is given to you as an absolute path (starts with `/`) and points under the launch directory's `.quasar-graph/`. Use it verbatim. Do NOT build a path relative to `project_path` or the scanned directory, do NOT use a bare `.quasar-graph/...` relative path, and do NOT `cd` anywhere — otherwise the file lands in the wrong place. If `session_dir` is not an absolute path, stop and report that instead of writing.

Write the file at that absolute path, creating intermediate directories as needed.

The file MUST contain valid YAML frontmatter followed by a `# <project_name>` heading and a 1–3 sentence prose description.

```md
---
name: <project_name>
language: <language>
framework: <framework_or_omit>
role: service          # OMIT for client apps (the default); emit only for backend services, shared libraries (role: library), or admin UIs (role: admin_panel)
port: 3000             # OMIT unless role: service AND the port is known
package_name: "@acme/shared"   # OMIT unless role: library AND the manifest declares a registry name
resources:
  - kind: database
    type: postgres
    env: DATABASE_URL
    description: Primary application database — stores users and orders.
  - kind: cache
    type: redis
    env: REDIS_URL
    description: Session store and rate-limit counters.
env:
  - DATABASE_URL
  - REDIS_URL
  - JWT_SECRET
connections:
  - project: <peer-from-manifest>
    via: rest_api
---

# <project_name>

Brief description of what the project does, inferred from README / package description.

## Resources

- **postgres** (`DATABASE_URL`) — Primary application database; stores users and orders.
- **redis** (`REDIS_URL`) — Session store and rate-limit counters.

Reserved space below — user may add manual notes.
```

The `## Resources` section is required when `resources` is non-empty. Each bullet: bolded `type` (or `name` if given), env var in backticks, then a human-readable sentence. Omit the whole section if `resources: []`.

If a field has no value, OMIT it rather than writing empty arrays. `resources: []` is allowed if there are genuinely none.

**Environment variant (`role: environment`).** When the input `role` is `environment`, emit the same file shape but: set `role: environment` in the frontmatter; fill `resources[]` with every backing service the environment operates (databases, realtime, monitoring, and the `kind: gateway` edge layer — Traefik/nginx); **omit `connections` entirely** (an environment makes no outbound app calls — its proxy routes and compose `depends_on` are deployment wiring, not graph edges); on each `kind: gateway` resource, DO capture a `routes:` list of the downstream targets it forwards to (see the Gateway `routes` note above) — this is the routing layer, not a connection; and devote the body to the **deployment topology** (what runs where, public hostnames, TLS, which self-hosted services originate here). The orchestrator treats this file as a resource + context source and does NOT create a node for the environment, so do not worry about a `service`/`project` role.

## What you must NOT do

- Do not update `manifest.json` — the orchestrator handles status changes.
- Do not invent resources or connections not visible in files.
- Do not read source files outside the whitelist above.
- Do not write anything outside `<session_dir>/scan/projects/<project_name>/` (or the given `output_md` path for environments).

## When done

Write the file, then return a short text summary: `Analyzed <project_name>: <N> resources, <M> connections.`
