---
name: agent-mcp-bundle
description: Build and deploy a narrow, authenticated MCP content API for a Wiki or internal app, with scoped short-lived agent tokens, human confirmation before mutation, optimistic concurrency, schema validation, auditability, and fail-safe production gates. Use when an agent must add MCP access to a personal project, CMS, documentation site, or internal tool and the user wants the same read–propose–review–publish pattern used by NineTails Workshop.
---

# Human-Gated Agent MCP Bundle

This skill turns a project’s existing content/CMS path into a small MCP capability. It is a deployment workflow, not a generic “give the agent database access” recipe. Preserve the project’s canonical content model and publication path; expose only named, validated operations; and keep a human in control of credentials, approval, and final publication.

The architecture was cross-checked against the read-only tldraw-online Agent MCP
implementation (`/Users/tinnguyen/tldraw`, branch `develop`). Its canvas-specific
tools are not part of this bundle, but its project/connection binding, capability
lifetimes, revoke-race handling, service injection, and bounded observation rules are
portable. See [references/reference-implementation.md](references/reference-implementation.md)
for the adaptation notes.

## Operating contract

The default capability is intentionally small:

1. `content_list_sections` — discover only manifest/index-backed content.
2. `content_get_section` — read a complete section and return its revision (`baseSha` or equivalent).
3. `content_update_section` — replace one complete validated section after a fresh revision check.

Writes are proposals. In Git-backed projects they should create an agent branch and PR (or equivalent reviewable change), never silently publish to the protected default branch. If the host cannot provide durable Git/database storage, fail closed rather than presenting ephemeral local state as production content.

Read [references/contract.md](references/contract.md) before choosing wire details. Read [references/security.md](references/security.md) before implementing authentication or browser access.

## Workflow

### 1. Assess the target project

Identify, using the project’s repository tools and documentation:

- canonical content source and manifest/index;
- block/schema validator and serializer;
- read path and publication path (Git, database, or CMS API);
- existing human login/edit session and CSRF protections;
- deployment provider, production alias, branch protection, and secret store;
- whether the app is a Wiki, an internal app, or both.

Do not start by adding an arbitrary file editor. If the project has no canonical content boundary, stop and propose one before adding MCP.

Record the exact paths, functions, environment variables, and deployment project in an implementation note. Keep unrelated dirty work untouched.

### 2. Design the narrow boundary

Define a project-specific section identity (for example `chapter` + `section`, or `collection` + `slug`) and a complete typed `Block[]`/record payload. Map only approved manifest entries. Reject unknown identities, unknown fields, oversized bodies, empty destructive replacements, unsafe URLs, and unsupported block types.

Use JSON-RPC 2.0 over Streamable HTTP unless the host already has a compatible MCP transport. Support `initialize`, `ping`, `notifications/initialized`, `tools/list`, and `tools/call`; negotiate a current protocol version plus one documented compatibility version. Return stable application error codes, not stack traces.

Keep review/evidence/canon/governance features additive and separately scoped. They must never silently change effective status or imply human approval.

When the app has a richer interactive domain (canvas, project workspace, dashboard,
or multi-tenant records), carry the same capability discipline used by the tldraw
reference: bind every resolved identity to the requested project/tenant and agent
connection, and issue short-lived context/observation capabilities for scoped reads
and mutations. Read [references/reference-implementation.md](references/reference-implementation.md)
for the composition and revoke-race pattern.

### 3. Implement server-side controls

Implement the following in this order:

1. **Production feature gate.** Require an explicit flag such as `MCP_ENABLED=true`; return a structured `NOT_FOUND`/disabled response when absent. Development/local mode must require an explicit opt-in and must be visibly labeled.
2. **Agent authentication.** Accept only a scoped bearer token on native/server-to-server MCP calls. Never accept a human edit cookie as an agent identity. Hash tokens at rest, show plaintext once, bound expiry (default 30 days, maximum 90), support revocation, and expose metadata without secret material.
3. **Identity binding and revoke races.** Resolve the token against the requested project/tenant and connection ID. For every operation that can touch a slow room/database/upstream call, revalidate the active identity immediately before starting and immediately after it returns. Serialize the final commit behind a per-agent commit/revocation gate so a concurrent revoke cannot produce a usable result or commit after the revoke point.
4. **Human token administration.** Protect issue/list/revoke operations with the existing human edit session, a separate edit secret where needed, same-origin checks, and CSRF proof for mutations. Keep the site-view password, CMS edit password, GitHub/deployment credential, and agent token distinct.
5. **Authorization.** Enforce scopes at the tool boundary (`content:read`, `content:write`, and any future review scopes). Use the narrowest scope; reject malformed or unknown scope records rather than upgrading them to broad access.
6. **Validation.** Reuse the canonical schema validator and serializer. Enforce block count/body byte limits, bounded strings, manifest membership, and complete payload semantics.
7. **Concurrency and capabilities.** In Git mode require a fresh `baseSha`/revision for writes and compare it immediately before commit. For scoped domains, bind context/observation records to project, connection, target page/collection, covered IDs or bounds, expiry, and document revision. On mismatch return `CONFLICT` or a capability-stale error; never overwrite or blindly retry stale content.
8. **Publication.** Write to a dedicated branch/PR or reviewable database change. Return commit/revision and PR/change evidence. A human merge/release action remains the publication gate.
9. **Observability.** Log request ID, tool, actor/capability ID, success/failure code, and duration. Never log article bodies, bearer tokens, passwords, GitHub tokens, or CSRF secrets. Return an `x-request-id` for transport failures as well as JSON-RPC responses.
10. **Rate/resource limits.** Bound request body, blocks, concurrent requests, and per-actor request rate. Release concurrency slots in `finally` blocks and use bounded timeouts for upstream Git/API calls.

For browser-based MCP, implement a same-origin BFF/session adapter instead of placing bearer tokens in JavaScript. Issue an HttpOnly, short-lived session cookie plus a non-HttpOnly CSRF token; require same-origin and CSRF proof on mutating calls. Read the cookie/session details in [references/security.md](references/security.md).

Do not collapse transport, provisioning, capability storage, observation, and mutation
logic into one route handler. Inject domain services from the application composition
root so each seam can be tested with fakes and the transport cannot bypass capability
checks.

### 4. Add the client handoff

Publish an agent-facing article or project instruction that states:

- canonical MCP URL and transport headers;
- how the human issues a scoped token and where the agent stores it;
- exact tools, arguments, and safe edit loop;
- meaning of `404` disabled versus `401` missing/invalid token;
- conflict recovery and publication/merge rules;
- source-audit holds, review status, and non-goals;
- token expiry/revocation instructions.

Do not put a live token, password, GitHub token, or secret-bearing URL in the article. The article must be readable by humans, while the MCP endpoint remains independently gated.

### 5. Configure and deploy

Use the deployment provider’s secret manager; never commit secrets or paste them into build logs. For Vercel/Next.js, the minimum production configuration is typically:

```text
MCP_ENABLED=true
MCP_PUBLIC_ORIGIN=https://<canonical-production-host>
CMS_GITHUB_TOKEN=<server-side repository credential>
EDIT_PASSWORD=<separate human CMS edit secret>
```

Use the project’s actual names if different. `CMS_AGENT_TOKEN` is normally issued at runtime through the token registry and stored in the receiving harness secret store, not as a broad deployment secret. A provider-specific checklist and safe commands are in [references/deploy-vercel.md](references/deploy-vercel.md).

Before changing production configuration, state exactly which variables and deployment will change. If the user has not authorized that production mutation, stop for confirmation. After configuration, redeploy the canonical production alias and verify the deployed commit/environment, not just a preview.

### 6. Verify in layers

Run project checks (typecheck, lint, content/schema checks, build) and the MCP contract harness. Then verify production in this order:

1. no-token request is `401 PERMISSION_DENIED` once the feature gate is on;
2. `initialize` negotiates the advertised protocol;
3. `tools/list` exposes only enabled, scoped tools;
4. list/read return manifest content and a revision;
5. invalid identity, schema, scope, body, and protocol cases fail with stable codes;
6. a valid update produces a branch/PR or equivalent review evidence;
7. a stale revision produces `CONFLICT` and leaves content unchanged;
8. revocation/expiry prevents replay;
9. browser session flows enforce same-origin and CSRF rules;
10. logs and response headers contain correlation IDs but no secrets.

Use the complete acceptance matrix in [references/acceptance.md](references/acceptance.md). Do not call a `mode: local` response durable in hosted production.

## Safe agent behavior after deployment

Agents using the resulting MCP must follow this loop:

`discover → read → explain proposed diff → obtain human confirmation → update with fresh revision → report evidence`

For every write, preserve unrelated blocks, send the complete validated payload, attribute a truthful author, include a concise note, and report revision/commit/PR evidence plus any source-audit hold. On `CONFLICT`, read again and re-apply intent to the new content. Never retry stale blocks blindly.

Agents must not:

- edit arbitrary paths, run shell/raw Git through MCP, or bypass branch protection;
- use a human password or GitHub credential as an agent bearer token;
- expose or echo tokens in prompts, logs, article content, browser bundles, URLs, or commits;
- treat an agent commit/PR as human review, canon promotion, or publication;
- clear a source-audit hold by editing content;
- broaden scopes to “make it work”; or
- claim success when only an ephemeral/local write occurred.

## Completion report

Return a concise deployment handoff containing:

```text
Project: <name>
Production MCP URL: <url>
Transport/protocol: <profile and versions>
Tools: <enabled tool names>
Auth: <token registry + scopes + expiry policy; never include plaintext token>
Environment: <variable names and whether configured; never include values>
Storage/publication: <Git branch/PR or equivalent human gate>
Verification: <commands and production outcomes>
Human action remaining: <token issuance, merge, or none>
Known gaps: <rate limit, browser, observability, etc.>
```

If the user explicitly asks for a ready-to-send agent message, include endpoint and non-secret setup instructions, but deliver any bearer token only through the user’s approved secure secret channel. If a token has appeared in chat, mark it exposed and recommend revocation/rotation.
