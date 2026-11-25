---
name: framework-fastapi
description: FastAPI security review — validate OpenAPI/docs exposure, auth dependency injection, Pydantic type coercion, SSRF via request parameters, and server configuration with docs-first, read-only checks and no exploitation or data mutation.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# FastAPI security — configuration and surface review

Use this skill to review FastAPI application security posture on authorized in-scope targets. Validate OpenAPI schema and interactive-docs exposure, authentication dependency injection, Pydantic type-coercion risks, SSRF vectors through URL-typed parameters, and server/proxy configuration. All tests are read-only and low-rate. Never bypass authentication dependencies, exploit SSRF to access internal services, inject Pydantic-constructor payloads, or modify application data.

## Required inputs

- Written scope covering the FastAPI application hosts, API routes, `/docs` and `/openapi.json` paths (explicitly), and allowed review methods. Explicit confirmation that auth bypass, SSRF to internal hosts, and data mutation are prohibited unless separately approved.
- FastAPI/Pydantic/Starlette version from: OpenAPI schema `info.version`, response headers, error-page format, or local source code if provided.
- Official FastAPI documentation for the detected version — prefer fastapi.tiangolo.com.
- Valid authorization cache for the target application.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target`.
3. `pentest_agent_check_authorization` before any active probe.
4. `pentest_agent_build_command` for dry-run argv preview.
5. `pentest_agent_execute_tool` for read-only execution — never raw shell.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — OpenAPI schema and interactive docs exposure

1. Check whether the OpenAPI schema is publicly exposed. FastAPI serves the schema at `/openapi.json` by default. Fetch the schema and assess its contents: every route, parameter, request body model, response model, and authentication scheme is documented.
2. Check whether interactive docs are exposed: `/docs` (Swagger UI) and `/redoc` (ReDoc) are enabled by default. Interactive docs allow anyone to execute API requests directly from the browser, including authenticated requests if the browser has a valid session.
3. Assess the schema content risk: does the schema expose internal endpoints not intended for public discovery? Does it reveal parameter names, model field types, enum values, and validation constraints that an attacker could use for parameter fuzzing? Does it document admin, health-check, or debug endpoints?
4. Check whether the schema is restricted: FastAPI allows disabling docs via `docs_url=None` and `openapi_url=None`. If the schema is publicly accessible and contains sensitive endpoint data, flag as information disclosure.
5. Do not execute requests through the interactive docs — only fetch the schema definition and UI pages.

### Phase 2 — authentication dependency and authorization review

1. Identify the authentication mechanism from the OpenAPI schema's `security` and `securitySchemes` sections. FastAPI supports: HTTP Basic, HTTP Bearer (JWT or API key), OAuth2 with password/authorization-code flows, API key in header/query/cookie, and OpenID Connect.
2. For each protected endpoint: send a request without authentication. Confirm the response is 401 or 403, not 200 with data. A protected endpoint returning 200 without authentication is a critical finding.
3. Test authentication dependency bypass techniques: send an empty `Authorization` header, a header with `Bearer` (no token), a header with `Bearer undefined`, a header with `Bearer null`, and a header with a malformed JWT. FastAPI's dependency injection should reject all of these — if any returns 200, flag as an authentication bypass.
4. Check whether the OAuth2 `tokenUrl` (if documented) is protected: the token endpoint should enforce client authentication and rate limiting. An unauthenticated or unthrottled token endpoint allows credential brute-force.
5. Do not submit real credentials, test password guessing, or attempt to forge tokens. Record authentication bypasses only.

### Phase 3 — Pydantic type coercion and validation bypass

1. Collect request-body schemas from the OpenAPI specification. For each schema, identify field types: `string`, `integer`, `boolean`, `array`, `object`, `number`, and `$ref` references.
2. Test Pydantic type-coercion behavior: for boolean fields, submit `1`, `0`, `"true"`, `"false"`, `"yes"`, `"no"`, and `[]`. Pydantic coerces many values to boolean — `"false"` (non-empty string) coerces to `true`, which is a logic bypass if a developer checks `if not field` instead of `if field is False`.
3. For integer fields, submit: floats (`1.5`), strings (`"1"`), booleans (`true`/`false` which coerce to `1`/`0`), arrays, and `null`. FastAPI/Pydantic will coerce or reject based on strictness settings — unexpected coercion may bypass business logic.
4. For `Optional` fields with defaults: submit the field with value `null` explicitly, and omit the field entirely. FastAPI distinguishes `None` (explicit) from missing (default). If an endpoint treats explicit `null` differently from omission, it may be exploitable for partial-update bypasses.
5. Do not exploit type coercion for privilege escalation, data corruption, or unauthorized access. Record coercion behaviors and flag those with security impact.

### Phase 4 — SSRF and URL-parameter injection

1. Identify parameters typed as `HttpUrl`, `AnyUrl`, or `str` with URL validation. These are common in webhook endpoints, file-import endpoints, image-proxy endpoints, and URL-shortening endpoints.
2. Test for SSRF: submit internal URLs (`http://127.0.0.1/`, `http://localhost/`, `http://[::1]/`, `http://0.0.0.0/`), cloud metadata endpoints (`http://169.254.169.254/latest/meta-data/`), and internal hostnames. A response that differs from the normal error response (timeout, different error message, partial content) suggests the server attempted to fetch the URL — flag as potential SSRF.
3. Test URL parsing bypasses: submit URLs with credentials (`http://admin:pass@internal/`), URLs with DNS rebinding characters, and URLs with alternative IP representations (decimal `http://2130706433/` for 127.0.0.1, hex `http://0x7f000001/`).
4. Do not exploit confirmed SSRF to read cloud metadata, access internal services, or scan internal networks. Record the affected parameter and stop further SSRF testing on that endpoint.
5. If a URL parameter is reflected in the response (the server fetches and returns the content), do not request internal resources or sensitive URLs. Use only `/robots.txt` on a host you control for confirmation if in-scope.

### Phase 5 — server configuration and CORS review

1. Inspect CORS configuration: FastAPI uses Starlette's `CORSMiddleware`. Send cross-origin requests with custom `Origin` headers and check `Access-Control-Allow-Origin`. If the origin is reflected, CORS is permissive.
2. Check for server-identity headers: `server: uvicorn` or `server: hypercorn` may appear. Suppressing the server header is recommended but low-severity.
3. Check for HTTPS enforcement: if the application is served over HTTPS, send plain-HTTP requests and verify redirection. Missing HTTPS redirect allows credential interception.
4. Check for rate limiting: does the application enforce rate limits on authentication, token, and sensitive endpoints? FastAPI does not include built-in rate limiting — if missing, flag as a hardening gap.
5. Check for debug or development endpoints: `/docs` interactive API execution in production, `/debug/` endpoints, `/metrics` (Prometheus) without authentication, and health-check endpoints exposing version or dependency details.

## Decision points

- **Escalate on OpenAPI schema publicly accessible with sensitive internal endpoints**: the schema documents admin, management, or internal-only APIs → high.
- **Escalate on authentication bypass**: empty, malformed, or `Bearer undefined` returning 200 on a protected endpoint → critical.
- **Escalate on SSRF via URL parameter**: server fetches attacker-supplied URL with internal network access → critical, stop testing.
- **Escalate on `docs_url` and `openapi_url` enabled in production**: interactive Swagger UI allows unauthenticated API exploration → medium to high depending on endpoint sensitivity.
- **Escalate on Pydantic boolean coercion**: `"false"` (string) coerced to `true` in a security decision (admin flag, access control) → high.
- **Downgrade on server-header disclosure**: informational — UVicorn/Hypercorn `Server` header is low risk.

## Prohibited behavior

- Exploiting SSRF to read cloud metadata, scan internal networks, or access internal services.
- Bypassing authentication dependencies by crafting tokens or forging credentials.
- Injecting Pydantic constructor payloads for object-instantiation attacks.
- Submitting `__init__`, `__class__`, or `__dict__` keys in JSON bodies for prototype/manifestation attacks.
- Running automated fuzzers, parameter-discovery tools, or wordlist scanners.
- Creating, updating, or deleting resources through the API.

## Stop conditions

- SSRF confirmed (server fetches internal URL) → stop, record critical finding, do not enumerate internal network.
- Authentication bypass confirmed → stop, record critical finding, do not access protected data.
- OpenAPI schema reveals secrets, internal IPs, or database connection strings → stop, record finding, redact values.
- `/docs` execution exposes write operations without authentication → stop, record finding.
- Target not in scope or testing impacts production data → stop.

## Evidence — FastAPI security matrix

For each target, record:

```text
Target: <URL> | FastAPI version: <detected from schema | estimated>
Version evidence: <OpenAPI info.version | header | error page>

OpenAPI/docs:
  /openapi.json accessible: <yes — endpoints: <count> | no>
  /docs accessible: <yes — Swagger UI | no>
  /redoc accessible: <yes | no>
  Sensitive endpoints in schema: <admin: yes/no | internal: yes/no | debug: yes/no>
  Restricted in production: <yes — docs disabled | no — docs public>

Authentication:
  Auth mechanism: <HTTP Bearer | OAuth2 | API key | none>
  Protected endpoints: <count>
  Auth bypass (empty): <yes — 200 | no — 401/403>
  Auth bypass (malformed): <yes — type | no — rejected>
  OAuth2 tokenUrl protected: <yes | no — unauthenticated | not applicable>

Pydantic coercion:
  Boolean field coercion: <yes — values: "false"→true etc. | no>
  Integer field coercion: <yes — values: string→int etc. | no>
  Optional/None handling: <differential behavior | consistent>

SSRF:
  URL-typed parameters: <count and endpoints>
  Internal URL fetch: <confirmed — IP | timeout — potential | blocked>
  URL parsing bypass: <successful — method | blocked>

Server config:
  CORS: <Allow-Origin reflects | fixed | not set>
  HTTPS redirect: <yes | no — HTTP served directly>
  Rate limiting: <observed — endpoints | not observed>
  Server header: <uvicorn | hypercorn | suppressed>
  Debug/metrics endpoints: <exposed — paths | not found>

Overall risk: <critical | high | medium | low>
```

Never store: OpenAPI schema with internal endpoint details (summarize counts only), JWT tokens or API keys, response bodies from auth-bypass attempts, SSRF responses containing internal data or cloud metadata, or Pydantic model field values containing PII.

## Report handoff

1. `pentest_agent_record_finding` for: public OpenAPI schema with sensitive endpoints, authentication bypass vectors, confirmed SSRF, Pydantic boolean/integer coercion with security impact, and missing authentication on token/debug endpoints.
2. Reference the FastAPI security matrix.
3. Recommend: disable `/docs` and `/openapi.json` in production or restrict them behind authentication, validate OpenAPI schema does not expose internal-only endpoints, enforce strict Pydantic model validation (reject type coercion for security fields with `StrictBool`/`StrictInt`), validate and restrict URL parameters with allowlist-based URL schemes and hosts, never pass user-supplied URLs to `httpx`/`requests` without strict validation, run FastAPI behind a reverse proxy with rate limiting, enable HTTPS with HSTS, and upgrade FastAPI, Pydantic, and Starlette to supported versions.
