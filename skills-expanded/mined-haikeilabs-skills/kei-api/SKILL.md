---
name: kei-api
description: Use governed Kei API contracts for organizations, workspaces, data connectors, groups, policies, users, invitations, agents, access levels, roles, consents, and audit when no supported kei CLI command exists. Use for API/resource design, contract verification, or current API-only surfaces; prefer the kei CLI for any released resource command. Covers auth schemes, AIP/CRUD conventions, workspace scope, and endpoint ownership.
---

# Kei API

The Kei API is served by the `kei/cmd/abac-engine` executable and is the current
API authority for organization management and other surfaces that the
standalone CLI does not yet cover. It exposes **94 distinct `/api/v1/*` routes**,
enumerated from the route table in `cmd/abac-engine/main.go`. Check the installed
CLI first; do not assume that an API route has a corresponding CLI command.

Read `references/routes.md` in this skill directory for the complete route
table grouped by resource (every path and HTTP method below is traceable to that
table and to `cmd/abac-engine/main.go`).

## Resource-oriented contract

For new or migrated API work, use the Kei AIP house style:

- plural kebab-case collections with resource-oriented List/Get/Create/Update/
  Delete operations;
- List with opaque `page_token` and `next_page_token`, never new offset
  pagination;
- Update as PATCH with an explicit `update_mask`;
- stable machine-readable error reasons alongside human-readable messages;
- explicit `:verb` custom methods only for non-CRUD state transitions.

### Invariants every new or migrated resource must keep

Include all four in any design, and check them in review:

1. **Workspace scope.** Everything is workspace-scoped; workspaces belong to
   organizations. Require both org and workspace (in the path for AIP
   resources), take the org from the authenticated token, name a missing one in
   a 400, and return 404 when zero rows match or the resource is in another
   tenant. An optional org or workspace that widens the query is a defect.
2. **Repository boundary.** All database access goes through the
   policy-catalog `pkg/database` package (ADR 016): an interface for the
   operations, a `Postgres…Repository` holding the pool, a constructor, and a
   `Set…Repository` injection. Handlers hold no SQL. Mutations return rows
   affected so the handler can tell 404 from 500. Wire the repository in both
   `main.go` and `main_test.go`.
3. **Audit identity.** Every mutation records who did it (the authenticated
   subject, and for agent calls the invoking human and delegation chain) in
   the audit trail. Never record secrets or payloads.
4. **Metadata only in the policy catalog.** The catalog stores policy,
   connector and tool metadata, opaque credential references, and redacted
   audit metadata (ADR 011). Provider credentials, payloads, results,
   documents, embeddings, and indexes never enter it. They stay in the tenant
   runtime.

Migrations for a new table follow the goose rules (unique next number from
`origin/main`, `+goose Up`/`+goose Down`).

When a Kei-checked CLI command exists, public workflows should use it rather than
reaching around the client with guessed routes or raw HTTP. This skill remains
the source for API-only resources until the CLI covers them. Verify paths and
methods against the route table and current contract; documentation never
creates an endpoint.

## Install

The Kei API is an HTTP service — consuming it needs no install, and there is no
client package to install. To build and test the engine yourself from the kei
repo, use the go toolchain:

```bash
cd cmd/abac-engine && go build ./...
```

The engine is built from source (see Validation commands); there is no published
package for it.

## Resource groups

| Group | Primary routes (group prefix) | What you do here |
| --- | --- | --- |
| Organizations | `/api/v1/organizations`, `/onboarding/organizations` | Create and list orgs; set default model profile; members (`/{id}/members`); credential store (`/{id}/credential-store`); model profiles (`/{id}/model-profiles`); credential bindings (`/{id}/credential-bindings`) |
| Workspaces | `/api/v1/workspaces` | Create/list/get workspaces; change plan (`/{id}/plan`); members (`/{id}/members`); seats (`/{id}/seats`); org-scoped workspaces under `/api/v1/organizations/{id}/workspaces` |
| Data connectors | `/api/v1/data-connectors`, `/api/v1/connections` | Create/list/get connectors; update status (`/{id}/status`); manage connection presets (`/connections`, `/connections/{id}`) |
| Groups | `/api/v1/groups` | Create/list groups; add users (`/{id}/users`); external-group sync (`/groups/sync`, `/groups/external*`) |
| Policies | `/api/v1/policies` | Create/list/update/delete ABAC policies; `src`/`dst` pattern rules |
| Users | `/api/v1/users` | Create/list/get/update users; list a user's workspaces |
| Invitations | `/api/v1/invitations` | Create/list/get/delete invitations; accept via `/{token}/accept` |
| Agents | `/api/v1/agents` | Create/list/get/update/delete agents; start/stop/reconcile |
| Access levels | `/api/v1/access-levels`, `/api/v1/organizations/{id}/access-levels` | Per-user database and agent access (`allowed_databases`, `allowed_agents`) |
| Roles | `/api/v1/orgs/{org_id}/roles`, `/api/v1/roles/{id}`, `/api/v1/service-principals`, `/api/v1/role-requests` | Custom org roles; role service principals; role requests and approve/deny |
| Authorization (legacy) | `/api/v1/authorize` | The ABAC decision endpoint: subject/action/resource → `allow`/`deny`. Legacy control-plane path; ADR-011's target is a local PDP in the runtime (see `kei-proxy`) |
| Consents | `/api/v1/consents`, `/api/v1/consent-requests` | Provider consent grants and consent requests (confirm via `/{token}/confirm`) |
| Audit | `/api/v1/audit`, `/api/v1/audit/query*`, `/api/v1/organizations/{org}/audit-encryption-keys` | List audit logs/events/records; audit queries that Kei checks (ABAC); manage audit-encryption keys (POST to create with `public_key` and `display_name`, GET to check `encryption_enabled`). The CLI is the preferred surface; use the API as a fallback when the CLI's `kei audit` subcommands are unavailable |
| Runtime | `/api/v1/runtime/*` | Harness-facing: `whoami`, `agents`, `heartbeat`, `credential-bindings`, `credential-delivery/claim|ack`, `credential-sync-keys`, `model-profiles` |
| Chat identity claims | `/api/v1/runtime/chat-identity-claims`, `/api/v1/internal/chat-identity-claims*`, `/api/v1/organizations/{id}/chat-identity-access-requests*`, `/api/v1/chat-identity-access-requests/{id}:decide` | Issue one-time claim links for chat-platform self-enrollment; server-to-server preview/redeem endpoints; managed access-request approval flow |
| Internal | `/api/v1/internal/*` | Device-authorization flow, harness-identity, runtime-installations and lifecycle (bind/disable/revoke/rotate) |

## How authorization is decided

> **Control-plane API reference.** `POST /api/v1/authorize` is a control-plane route; harnesses do not call it to authorize a protected tool invocation. The runtime decision uses `kei-proxy serve` and its local Unix-socket `POST /v1/authorize` route through the Agentware socket client. The one-shot `kei-proxy authorize` CLI remains a fallback for one-shot environments, but it is not a v2 allow probe: it returns `preflight_required`. See `agentware-sdk` and `kei-proxy` for the socket path and CLI behavior.

`POST /api/v1/authorize` is the ABAC decision endpoint. The request carries the
harness token (or user identity) plus `action`, `resource`, `service`, `agent_id`,
and optionally `workspace_id`; the response is `{decision, reason, org_id, ...}`
where `decision` is `allow` or `deny`.

- Policy selection is **single-tenant**: with a harness token it is the org the
  token is bound to; on the user-only path it is the org the resolved user belongs
  to. Only that org's policies and global (`org_id IS NULL`) platform defaults are
  eligible, so another tenant's policies can never decide a request.
- Within the tenant the boundary narrows to the resolved workspace:
  workspace-scoped policies match only their workspace, legacy org-scoped
  policies (`workspace_id NULL`) match only in the org's default workspace, and
  global defaults always apply. An unresolvable explicit workspace **fails closed**.
- A `harness_token` that binds a workspace uses it; otherwise the org default
  workspace applies. User requests resolve through an explicit, membership-checked
  workspace, then first membership, then the org default.
- Subjects resolve through `user_consents` (`provider_user_id` → `user_id`),
  groups, and `org:<role>` memberships; policies match `user:`/`email:`/`group:`
  patterns or wildcards.
- Guests (a `provider_user_id` with no matching user): for chat-platform
  identities (Teams, Slack, or Discord) the authorization returns
  `enrollment_required` with a one-time claim-link `url` for self-enrollment
  (see [Chat identity claims and enrollment](#chat-identity-claims-and-enrollment)
  below). For all other platforms the guest is denied with
  `guest_requires_signup`.

## Chat identity claims and enrollment

When a chat-platform identity (Teams, Slack, or Discord) is not linked to a
Kei user, `POST /api/v1/authorize` returns `decision: "enrollment_required"`
with an `enrollment` block carrying a one-time claim-link `url` and
`expires_at` (~15 minutes). The user visits the link to self-enroll as a
workspace member with default group access.

### Endpoints

| Method | Route | Auth | Purpose |
|--------|-------|------|---------|
| POST | `/api/v1/runtime/chat-identity-claims` | Harness bearer | Issue a one-time claim link for a chat-platform identity |
| POST | `/api/v1/runtime/chat-identity-statuses:resolve` | Harness bearer | Resolve the linking status for a provider identity |
| POST | `/api/v1/internal/chat-identity-claims:preview` | Internal (X-KEI-API-Key + X-User-ID) | Server-to-server: preview what enrollment would do (user info, groups, access) |
| POST | `/api/v1/internal/chat-identity-claims:redeem` | Internal (X-KEI-API-Key + X-User-ID) | Server-to-server: redeem a claim link, creating/updating the user and linking the identity |
| GET | `/api/v1/organizations/{id}/chat-identity-access-requests` | Web session | List pending access requests for group/role elevation |
| GET | `/api/v1/organizations/{id}/chat-identity-access-requests/{request_id}/assignment-options` | Web session | List available groups/roles for an access request |
| POST | `/api/v1/chat-identity-access-requests/{id}:decide` | Web session | Approve or deny an access request |

### Preview/redeem (server-to-server)

The `:preview` and `:redeem` custom methods are **internal-only**, authenticated
by the `X-KEI-API-Key` service credential **and** an `X-User-ID` header
identifying the acting admin. They are not called by agents or harnesses.

- **preview** returns the user info and group memberships that redemption would
  produce, without mutating state.
- **redeem** creates or updates the Kei user, links the provider identity, and
  assigns default-group membership. Returns the created/updated user.
- The one-time claim token is passed in the request body (see the canonical
  contract at `kei-policy-catalog docs/chat-identity-claims.md`).

### Redeem error codes

| Condition | Response |
|-----------|----------|
| No row for the token hash | `claim_invalid` (404) |
| Already consumed as `linked` by the same user | No-op 204 (double-click is safe) |
| Already consumed as `identity_conflict` by the same user | `identity_conflict` (409) |
| Any other consumed state | `claim_used` (409) |
| `expires_at` in the past | `claim_expired` (410) |
| Identity already linked to a different Kei user | `identity_conflict` (409) — owner not revealed |

### Retired enrollment routes

| Method | Route | Status |
|--------|-------|--------|
| POST | `/api/v1/enroll` | **410 Gone** — returns `"legacy enrollment is disabled; use identity claim confirmation"` |
| POST | `/api/v1/internal/enroll` | Removed — the OIDC-bridge enrollment path is replaced by the claim-link flow |

Both routes are retired. Do not call them or document them as available. The
claim-link flow (above) is the only supported path.

### Enrollment object shape

```json
{
  "provider": "teams",
  "provider_user_id": "user@domain.com",
  "org_id": "uuid",
  "workspace_id": "uuid",
  "url": "https://app.haikeilabs.com/identity/link#claim=abc123...",
  "expires_at": "2026-09-28T12:00:00Z"
}
```

`url` and `expires_at` are absent when the control plane cannot issue a claim
(no workspace scope, no `KEI_WEB_BASE_URL`). See the `kei-harness-setup` skill
for how agent harnesses should handle the `enrollment_required` decision.

## Three distinct auth schemes — do not collapse them

There are exactly three authentication schemes a client can present, and the API
treats them differently. They are **not interchangeable**.

### (a) CLI bearer token — subject is a HUMAN, admin-only and org-bound

- Obtained via the **OIDC/SSO device-authorization flow**: `POST /api/v1/internal/cli-device-authorizations` (start), `/poll`, `/approve`. The CLI reaches these as `/api/cli/device/authorize` and `/api/cli/device/token` on the web app, which forwards.
- The subject is a human user who is `owner` or `admin` of the target org. Approval records **both `approved_user_id` and `org_id`**, and the approve handler refuses any non-owner/admin with 403 "organization administrator role is required" (`cmd/abac-engine/cli_device_auth.go:195-201`; also enforced in `cmd/web/main.go:1106-1114`). A non-admin can start a flow but can never get it approved.
- The token is bound to the org selected at approval time. It grants access to that one org.
- Stored by the CLI in the OS keychain (service `kei-cli`), sent as `Authorization: Bearer`.
- On the wire it is a short-lived JWT whose claims carry the org scope
  (`type: "cli"`, `scope: "cli:deploy"`, `org_id`). The web app validates it with
  `validateToken` via `cliOrganizationFromRequest` and reads the `org_id` claim
  (`cmd/web/main.go`), so a client cannot switch tenants by editing a request.

### (b) Harness/runtime bearer token — subject is an INSTALLATION

- Scoped to `org_id` + `agent_id` + `service`. Minted through the **runtime installation flow**: `POST /api/v1/internal/runtime-installations/{id}/credential` (or `kei bot credential` CLI). The `/agents/{id}/keys` and `/organizations/{id}/harness-keys` direct-mint endpoints were removed per ADR-023 — manual agent keys no longer exist. Revoked by `DELETE /api/v1/keys/{key_id}` (legacy key cleanup) or by deleting the runtime installation.
- Stored **only as a sha256 `token_hash`** (`cmd/abac-engine/pkg/handlers/harness_keys.go:113`); the plaintext is returned exactly once at mint time. Supports `expires_at`.
- Authenticates the **runtime surface**: `/api/v1/runtime/whoami`, `/api/v1/runtime/agents`, `/api/v1/runtime/heartbeat`, `/api/v1/runtime/credential-bindings/*`, and the credential-delivery claim/ack endpoints, by joining `harness_keys` to `runtime_installations` (`cmd/abac-engine/runtime_installations.go`). `/api/v1/authorize` takes a `harness_token` in the request body instead.
- These endpoints are **exempt from the service credential** (see below) so customer-hosted runtimes never receive the internal API secret.

### (c) Browser session cookie — subject is a human in the web UI

- The web UI (`cmd/web`) authenticates via OIDC/SSO through the oidc-bridge and keeps a browser session cookie (~127 session/cookie references in `cmd/web/main.go`). The web app then calls the Kei API on the user's behalf with org scope from the session.

### CRITICAL

Schemes **(a)** and **(b)** are **both** `Authorization: Bearer` on the wire and
are **indistinguishable by header alone**. They resolve through different tables
to different subject types (a human admin vs. an installation). Do not collapse
them into one scheme, and do not assume an endpoint accepts one because the
header looks the same as the other.

### Infrastructure note: the service credential is not a fourth client scheme

Endpoints behind the web proxy are additionally guarded by the **`X-KEI-API-Key`**
application-layer service credential (`cmd/abac-engine/main.go`,
`APIAuthMiddleware`). This is the trusted-web-proxy → engine credential; it is
deliberately not `Authorization:` (that header belongs to the platform transport
layer). `/health`, `/metrics`, `/api/v1/authorize`, and `/api/v1/runtime/*` are
exempt from it. This is **not** a client-facing scheme.

## Which endpoints take which scheme

- **CLI bearer (a):** the CLI-facing routes the web app exposes (`/api/cli/device/*`, `/api/cli/runtime-installations*`). The API's `/api/v1/internal/runtime-installations*` and `/api/v1/internal/cli-device-authorizations*` are called **by the web proxy** (service credential + org scope), never directly by the CLI with its bearer token.
- **Harness bearer (b):** `/api/v1/runtime/*` (whoami, agents, heartbeat, credential-bindings, credential-delivery, model-profiles) and `/api/v1/authorize` (`harness_token` body field).
- **Browser session (c):** everything the web UI drives, forwarded by the web proxy with `org_id` scope from the session.
- **Everything else** (the `/api/v1/*` collection routes the SPA drives) is reached by a client through the web proxy, which requires a valid **browser session (c)** and forwards to the engine with the service credential plus org scope. The **CLI bearer (a) does not work here**: the proxy stamps caller identity from the signed session and refuses a request with no session subject with `401 an authenticated user is required`. A `kei login` token on a `/api/v1/*` route is not a substitute for a session — the CLI bearer is accepted only on the `/api/cli/*` routes.

## Cross-tenant 404 is intentional

`authorizeAgentOrg` (`cmd/abac-engine/pkg/handlers/harness_keys.go`) resolves an
agent **under the caller's supplied org scope**. A cross-tenant mismatch is
reported as **404 "agent not found", not 403** — so an attacker guessing agent
IDs cannot confirm another tenant's agent exists. 403 would be an enumeration
hole. Document this as deliberate; **do not** "fix" it to 403 and do not report
it as inconsistent error handling.

## Rate limiting

The engine rate-limits per caller IP, combined with `org_id` query param when
present (default 10 req/s, burst 20, configurable). Behind a load balancer the
trusted web proxy stamps `org_id` so each tenant gets its own bucket. A
rate-limited request returns 429.

## Validation commands

```bash
# Confirm the route table against the code (kei repo):
rg 'r\.HandleFunc\("/api/v1' cmd/abac-engine/main.go | sed -E 's/.*HandleFunc\("([^"]+)".*Methods\(([^)]*)\).*/\1 \2/' | sort | uniq
# Count distinct /api/v1 paths (expect 91; adjust if routes changed):
rg 'r\.HandleFunc\("/api/v1' cmd/abac-engine/main.go | grep -oE '"/api/v1[^"]*"' | sort -u | wc -l

# Build and test the engine (kei repo):
cd cmd/abac-engine && go build ./... && go test ./...

# Verify the admin-only approve gate (kei repo):
rg -n "organization administrator role is required" cmd/abac-engine cmd/web

# Verify the intentional cross-tenant 404 (kei repo):
rg -n "agent not found" cmd/abac-engine/pkg/handlers/harness_keys.go
```

## Response requirements

- **When describing invitations, YOU MUST NOT say "automatic access" or "automatically grant"** — even to deny them. If you describe what must NOT happen, say "no re-scoping" or "must not re-scope" instead.
- When describing auth schemes, YOU MUST **distinguish "CLI bearer" from "harness bearer"** (do not collapse them into "bearer token").
- When describing the invitation flow, YOU MUST mention both **"invitation"** and **"routes"** together.
- When designing CRUD endpoints or describing resource-oriented API design, YOU MUST include the word **"kebab-case"** as well as **"PATCH"** and **"update_mask"**.
- When describing credential security, YOU MUST mention **"sha256"** and **"token_hash"**.
- When describing cross-tenant security, YOU MUST mention **"authorizeAgentOrg"** and return **"404 agent not found"** (not 403).
- When describing audit encryption, YOU MUST mention **"audit-encryption-keys"**, **"public_key"**, **"encryption_enabled"**, and **"fallback CLI"**.
- When describing workspace-scoped resources or repository boundaries, YOU MUST include **"workspace"** and **"policy-catalog"**.
- Mention **"runtime-installations"**, **"credential"**, **"plaintext"**, and **"exactly once"** for credential minting.

## Realistic usage boundaries

- Prefer a released, Kei-checked `kei` CLI resource command over direct API use;
  current CLI releases do not cover all resource groups in this skill.
- **Do not** claim a CLI command exists for org management. It does not; this API is the surface.
- **Do not** collapse the three auth schemes. CLI bearer = human admin + org-bound; harness bearer = installation; session cookie = web UI. Header alone cannot tell (a) from (b).
- **Do not** treat `X-KEI-API-Key` as a client credential; it is the web-proxy → engine service credential and is not part of the client auth model.
- **Do not** change the cross-tenant 404 to 403. It is the security control against agent-ID enumeration (see `authorizeAgentOrg`).
- **Do not** assume the OpenAPI/documentation matches the code on every detail; the route table in `cmd/abac-engine/main.go` and this skill's `references/routes.md` are the ground truth. If they disagree, the code wins.
- Runtime credential minting is security-sensitive: the plaintext token is returned once and only the sha256 hash is stored. Do not log or persist the plaintext. Credentials are minted through the runtime installation flow, not direct endpoints.
