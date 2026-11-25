---
name: client-spa-endpoints
description: SPA endpoint and route discovery — extract API paths, internal hostnames, and hidden routes from client-side JavaScript bundles, source maps, and framework artifacts without active crawling or exploitation.
disable-model-invocation: true
risk: passive
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: conditional
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# SPA endpoint discovery — passive route and API extraction

Use this skill to extract API endpoints, internal hostnames, route definitions, and hidden paths from client-side JavaScript bundles without active probing. Prefer static analysis of downloaded JS artifacts, source maps, and framework-specific route tables. If active probing is needed to validate discovered endpoints, authorization and scope gates apply before any target contact.

## Required inputs

- Written scope naming the target SPA URLs, allowed JS artifact sources (primary origin, CDN, chunk URLs), and any excluded paths.
- Authorization cache required only if active endpoint validation (HTTP probing) will be performed. Passive extraction from downloaded JS does not require authorization cache.
- The target's primary HTML page or a list of JS bundle URLs. A local directory of downloaded JS files is ideal.
- Known frontend framework (React, Vue, Angular, Svelte, Next.js, Nuxt, etc.) to guide extraction patterns.

## Required gates

1. `pentest_agent_load_config` — read config, check storage dir.
2. `pentest_agent_parse_scope` — validate the target domain is in-scope.
3. `pentest_agent_validate_target` — confirm target normalization.
4. No `pentest_agent_execute_tool` needed for passive extraction from downloaded files.
5. If active validation (HTTP requests to discovered endpoints) is needed, proceed through full auth gates: `pentest_agent_check_authorization` → `pentest_agent_build_command` → `pentest_agent_execute_tool`.
6. `pentest_agent_append_evidence` for extracted endpoint lists.

## Workflow

### Phase 1 — JS bundle collection

Collect all JavaScript files served by the target application:

1. Fetch the main HTML page and extract all `<script src="...">` URLs. Include inline scripts that reference external chunks.
2. Check for build-manifest files: `asset-manifest.json`, `build-manifest.json`, `manifest.json`, `routes-manifest.json` (Next.js). These list all static assets including chunked JS.
3. Check for webpack artifacts: `report.html` (Webpack Bundle Analyzer), `webpack-stats.json`, `stats.json`. If exposed, these reveal every module and chunk.
4. Check for source maps: append `.map` to each JS URL. Source maps expose original source files with full paths, internal comments, and sometimes environment variables.
5. Download all discovered JS files to a local directory under `.pi/pentest-agent/`. Name files by their URL hash or slug for traceability. Never download JS from origins not in scope.

### Phase 2 — API endpoint extraction

From each JS file, extract API endpoint references:

1. **Path patterns**: grep for REST-style paths:
   - `/api/v{1,2}/` followed by resource names.
   - `/graphql`, `/gql`, `/query` — GraphQL endpoints.
   - `/swagger`, `/openapi`, `/docs` — API documentation endpoints.
   - `/internal/`, `/admin/`, `/private/` — hidden API prefixes.
2. **Request calls**: find `fetch(`, `axios.`, `XMLHttpRequest`, `$.ajax(`, `$.get(`, `$.post(` — extract URL arguments. For template literals, extract the base URL and note the variable parts.
3. **Configuration objects**: find `baseURL`, `apiUrl`, `API_BASE`, `API_URL`, `REACT_APP_*`, `VITE_*`, `NEXT_PUBLIC_*`, `VUE_APP_*` — these often contain API hostnames.
4. **GraphQL queries**: find `query`, `mutation`, `subscription` in JS strings — extract operation names and field paths to understand the API surface.
5. **WebSocket URLs**: find `wss://`, `ws://`, `new WebSocket(`, `socket.io` connections.

### Phase 3 — internal hostname and service discovery

Extract references to internal infrastructure:

1. **Internal hostname patterns**: grep for domain-like strings with internal TLDs: `.internal`, `.local`, `.corp`, `.lan`, `.priv`, `.intranet`, `.infra`, `.svc`, `.cluster`.
2. **Cloud metadata endpoints**: grep for cloud metadata URLs: `169.254.169.254` (AWS, GCP, Azure IMDS), `metadata.google.internal`, `100.100.100.200` (Alibaba).
3. **Private IP addresses**: grep for RFC 1918 addresses (`10.`, `172.16.` through `172.31.`, `192.168.`), loopback (`127.`), and link-local (`169.254.`).
4. **Microservice names**: grep for service-name patterns: `user-service`, `payment-api`, `notification-svc`, `auth.internal`. These often appear in environment config or proxy routes.
5. **Database connection strings**: grep for `mongodb://`, `postgres://`, `mysql://`, `redis://`, `amqp://` — redact immediately if found.

### Phase 4 — route and framework artifact analysis

Extract client-side routing information:

1. **React Router**: find `<Route path="`, `path: "`, `createBrowserRouter`, route config arrays with `path` and `element` keys.
2. **Vue Router**: find `path: "`, `routes: [`, `createRouter`.
3. **Angular**: find `path: '`, `loadChildren`, `RouterModule.forRoot`.
4. **Next.js**: inspect the file-based routing from source maps — look for `pages/` and `app/` directory references.
5. **SvelteKit**: find route file references in bundles.
6. For each discovered route, note: the path pattern, whether it requires authentication (by checking for auth guards in the route config), and whether it renders admin or privileged content.
7. Check for hidden or undocumented routes: `/debug`, `/status`, `/health`, `/metrics`, `/env`, `/config`, `/phpinfo`, `/server-status`, `/actuator` (Spring Boot).

### Phase 5 — endpoint validation decision point

After extraction is complete, you have a list of candidate endpoints. Decide:

1. **Purely passive**: record the endpoint list and stop. This is the default safe posture. Endpoints discovered via static analysis may or may not be live — the list is a reconnaissance artifact, not a vulnerability finding.
2. **Passive validation**: check endpoint candidates against a known API schema (OpenAPI, GraphQL introspection) if available without authentication. If the schema confirms the endpoint exists, record as verified passive.
3. **Active validation** (requires authorization): if scope and authorization permit active probing, proceed through full gates to validate each endpoint with a single HEAD or OPTIONS request. Record status codes. Never send data or attempt exploitation during validation.

## Decision points

- **Stop after extraction**: default. The endpoint list is a reconnaissance deliverable. Proceed to active validation only if the engagement scope explicitly includes it.
- **Escalate if internal hostnames found**: internal infrastructure references in client-side JS may indicate information disclosure.
- **Escalate if source maps expose secrets**: environment variables, API keys, or database URLs in source maps → secret-exposure finding.
- **Escalate if admin routes lack auth guards**: route config shows admin pages without authentication wrappers → access-control gap.

## Prohibited behavior

- Probing discovered endpoints with HTTP requests without authorization.
- Accessing `/admin`, `/internal`, or hidden endpoints before scope and authorization validate each path.
- Downloading JS from origins not in scope.
- Extracting and storing authentication tokens, API keys, or database credentials from JS files.
- Running automated crawling or directory brute-forcing at scale.
- Testing discovered endpoints for vulnerabilities (SQLi, XSS, etc.) — this skill covers discovery only.

## Stop conditions

- Internal hostname or cloud metadata URL found → record, do not probe.
- Secrets found in JS or source maps → redact immediately, record finding, do not validate.
- Candidate list exceeds 500 unique endpoints → stop extraction, prioritize by path pattern relevance.
- Active validation required but no authorization cache → stop.

## Evidence — endpoint extraction log

For each JS bundle and the aggregate, record:

```text
Target: <base URL>
JS bundles collected: <count>
Source maps available: <count>

Extraction summary:
  API endpoints (REST): <count>
  GraphQL endpoints: <count>
  WebSocket endpoints: <count>
  Internal hostnames: <count>
  Private IPs: <count>
  Cloud metadata URLs: <count>
  Database connection strings: <count, all redacted>
  Client-side routes: <count>
  Hidden/debug routes: <count>
  Environment config keys: <count>

Per-endpoint detail (sample for high-value candidates):
  Source: <JS bundle URL>
  Pattern: <path or URL>
  Type: <REST | GraphQL | WS | hostname | route>
  In-scope: <yes | no | needs-validation>
  Auth required: <yes | no | unknown>
```

Never store: extracted API keys, tokens, database URLs, cloud credentials, private keys, or unredacted environment variable values. If a secret is found, record its presence, type, and source file, then redact the value from all evidence.

## Report handoff

When endpoint extraction is complete:
1. `pentest_agent_append_evidence` with the endpoint extraction log.
2. If secrets were found: `pentest_agent_record_finding` with secret type, source file, CVSS estimate (7.0–9.0 for API keys/database URLs in client-side JS), and recommendation to rotate immediately.
3. If internal hostnames were found: `pentest_agent_record_finding` with internal architecture exposure, CVSS estimate (4.0–5.0), and recommendation to remove internal references from client bundles.
4. Recommend: remove source maps from production, strip internal hostnames and environment config from client bundles, use build-time constants (not runtime env vars in JS), serve admin routes through a separate authenticated bundle, and audit client bundles for secrets in CI.
