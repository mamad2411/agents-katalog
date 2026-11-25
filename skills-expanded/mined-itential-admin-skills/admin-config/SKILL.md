---
name: admin-config
description: Manage user accounts, groups, roles, OAuth service accounts, SSO configuration, integration models, profiles, and pre-built content packages. Use for user management, access control, and platform configuration.
argument-hint: "[action or user/group name]"
---

# Platform Configuration - Auth, Users, SSO, Integrations & Content

Platform setup and configuration: manage users and access control, configure SSO, create service accounts, set up integrations, and import pre-built content packages. This skill covers everything about who can access what and how the platform connects to external systems.

## Org, team & personal rules

Before using this skill, check `custom/org/`, `custom/team/` and `custom/dev/`
in this skill's own folder. Read every `.md` file found — any folder may be
empty or absent. Apply them on top of everything below; where a file overrides a
specific rule here, follow the override. More specific wins: dev > team > org >
this document. No customization may weaken this skill's safety
rules or put credentials in committed files.

---

## Concepts

- **Account** — a user or service account. Has a username, provenance (where it came from: Pronghorn, SAML, Service Account), group memberships, and role assignments.
- **Group** — a collection of accounts for bulk access control. Used by projects, workflows, LCM, and inventory manager for RBAC.
- **Role** — a set of allowed methods/permissions. Assigned to accounts or groups. Roles control what API methods a user can call.
- **Service Account** — an OAuth client_credentials account for API integration. Has a `client_id` and `client_secret`.
- **SSO Config** — SAML or OIDC configuration for single sign-on. Maps external identity providers to platform accounts.
- **Integration** — a connection model defining how the platform talks to an external system (adapter instance + settings).
- **Profile** — a saved set of adapter/application configurations for an environment. Switch profiles to move between dev/staging/prod settings.
- **Prebuilt** — a packaged set of ready-to-use automations, templates, and configurations that can be imported from a repository.

## Gotchas

- Auth endpoints return `{results: [...], total: N}` — NOT `{data: [...]}` or `{message, data, metadata}`
- Account/group/role IDs are MongoDB ObjectIds (24-char hex)
- `PATCH` for updates (accounts, groups, roles, service accounts), NOT `PUT` — and every one of these PATCH bodies is wrapped in `{updates: {...}}`
- Groups use `{results: [...]}` not a plain array
- Roles have `allowedMethods` — array of `{name, provenance}` objects defining what methods the role can call
- Service account `client_id` IS the account `_id` — they're the same
- Regenerating a service account secret: `PATCH /oauth/serviceAccounts/{client_id}/regenerate` — the old secret is permanently invalidated
- SSO config names are unique identifiers (used in URL paths)
- `DELETE` on accounts is NOT available via API — deactivate instead: `PATCH /authorization/accounts/{id}` with `{updates: {inactive: true}}`
- `forceLogout` requires the account ID, not the username
- Integration `{name}` in URL paths must be URL-encoded (spaces, special chars)
- Prebuilt import uses `POST /prebuilts/import` with the full prebuilt JSON
- **Uploading an integration model auto-creates roles** — one per HTTP method group (admin, get, post, etc.) with `provenance = versionId`
- Integration instances are **codeless** (`virtual: true`) — they do NOT show in `/health/adapters`, only in `/integrations`
- Tasks only appear in palette **after the auto-created role is assigned to a group** the user belongs to
- Group PATCH requires `{updates: {...}}` wrapper — bare fields return "No applicable updates requested"
- Role create requires `{role: {...}}` wrapper, group create `{group: {...}}`, SSO config create/update `{config: {...}}`, prebuilt import `{prebuilt: {...}}`
- `assignedRoles` in group PATCH is a **full replacement** — include ALL existing roles plus new ones
- Default pagination is `limit=25`, API caps at `100` per page — always add `sort=_id&order=-1` when searching for recently-created resources (roles, accounts, groups, models, instances). MongoDB ObjectIds are time-ordered, so descending sort puts the newest items on page 1 instead of buried across hundreds of pages. Apply this to any paginated GET that's hunting for something just created.
- Integration workflow tasks use `app` from `apps/list` (the versionId like `"Cat Facts:1.0.0"`), `adapter_id` is the instance name (like `"cat-facts"`)

## User & Account Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/authorization/accounts` | List all accounts |
| GET | `/authorization/accounts/{accountId}` | Get a single account |
| PATCH | `/authorization/accounts/{accountId}` | Update an account |
| POST | `/authorization/accounts/{accountId}/forceLogout` | Force logout a user |
| GET | `/authorization/csv/export` | Export all accounts as CSV |

**List accounts:**
```
GET /authorization/accounts
```
```json
{
  "results": [
    {
      "_id": "68432681f9597b4178e2f07a",
      "provenance": "Service Account",
      "username": "my-service-account",
      "firstname": "my-service-account",
      "memberOf": [
        {"groupId": "67c85954abe686cf9cb78b2e", "aaaManaged": false}
      ],
      "assignedRoles": [
        {"roleId": "683fb3733324ad98536b8caa"}
      ]
    }
  ],
  "total": 25
}
```

Query parameters: `limit`, `skip`, `sort`, `order`, `equals`, `contains`

**Update account (add to group, assign role):**
```
PATCH /authorization/accounts/{accountId}
```
```json
{
  "updates": {
    "memberOf": [
      {"groupId": "67c85954abe686cf9cb78b2e", "aaaManaged": false}
    ],
    "assignedRoles": [
      {"roleId": "683fb3733324ad98536b8caa"}
    ]
  }
}
```
Note: `memberOf` and `assignedRoles` are full replacements — include ALL memberships. `updates` also accepts `inactive` and `email`.

**Force logout:**
```
POST /authorization/accounts/{accountId}/forceLogout
```
No body required. Invalidates the user's session.

## Group Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/authorization/groups` | List all groups |
| POST | `/authorization/groups` | Create a group |
| GET | `/authorization/groups/{id}` | Get a single group |
| PATCH | `/authorization/groups/{id}` | Update a group |
| DELETE | `/authorization/groups/{id}` | Delete a group |
| GET | `/authorization/groups/list` | Simple group list (names + IDs only) |

**Create a group:**
```
POST /authorization/groups
```
```json
{
  "group": {
    "provenance": "Pronghorn",
    "name": "Network Operations",
    "description": "Network ops team",
    "memberOf": [],
    "assignedRoles": [
      {"roleId": "role-id-for-operations"}
    ],
    "inactive": false
  }
}
```
All six fields are required. `provenance` is where the group is managed — use the same value as the platform's existing groups (`Pronghorn` on a self-hosted platform; Itential Cloud groups show `CloudAAA`).

**Group structure:**
```json
{
  "_id": "67c85954abe686cf9cb78b2e",
  "provenance": "Pronghorn",
  "name": "Solutions Engineering",
  "description": "",
  "memberOf": [{"groupId": "parent-group-id", "aaaManaged": false}],
  "assignedRoles": [{"roleId": "659bdcb2184b7e848bf59d16"}]
}
```

Groups can nest — `memberOf` puts a group inside another group (inherits parent's roles).

## Role Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/authorization/roles` | List all roles |
| POST | `/authorization/roles` | Create a role |
| GET | `/authorization/roles/{id}` | Get a single role |
| PATCH | `/authorization/roles/{id}` | Update a role |
| DELETE | `/authorization/roles/{id}` | Delete a role |

**Create a role:**
```
POST /authorization/roles
```
```json
{
  "role": {
    "provenance": "Custom",
    "name": "device-operator",
    "description": "Can view and backup devices but not modify",
    "allowedMethods": [
      {"name": "getDevicesFiltered", "provenance": "ConfigurationManager"},
      {"name": "getDeviceConfig", "provenance": "ConfigurationManager"},
      {"name": "backUpDevice", "provenance": "ConfigurationManager"},
      {"name": "getJobs", "provenance": "OperationsManager"},
      {"name": "getJob", "provenance": "OperationsManager"},
      {"name": "startJob", "provenance": "OperationsManager"}
    ],
    "allowedViews": []
  }
}
```

All five fields are required. The role's own `provenance` is `Custom` for roles you create. Each `allowedMethods` entry grants access to a specific app method, where `provenance` is the app name; `allowedViews` entries (`{"provenance": "AgentProjects", "path": "/agent-projects/"}`) grant UI pages. To change a role later: `PATCH /authorization/roles/{id}` with `{updates: {description, allowedMethods, allowedViews}}`.

## OAuth Service Accounts

Service accounts for API-based automation (no interactive login, uses client_credentials).

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/oauth/serviceAccounts` | Create a service account |
| GET | `/oauth/serviceAccounts` | List service accounts |
| PATCH | `/oauth/serviceAccounts/{client_id}` | Update the description (`{updates: {description}}`) |
| DELETE | `/oauth/serviceAccounts/{client_id}` | Delete a service account |
| PATCH | `/oauth/serviceAccounts/{client_id}/regenerate` | Regenerate client secret |

**Create a service account:**
```
POST /oauth/serviceAccounts
```
```json
{
  "accountData": {
    "name": "automation-api",
    "description": "Service account for CI/CD pipeline"
  }
}
```

**Response:**
```json
{
  "results": {
    "name": "automation-api",
    "description": "Service account for CI/CD pipeline",
    "client_id": "69a7d8e5f9597b4178e2f123",
    "client_secret": "generated-secret-here"
  }
}
```
**Save the `client_secret` immediately** — it's only returned once on creation.

**Authenticate with service account:**
```
POST /oauth/token
Content-Type: application/x-www-form-urlencoded

client_id={client_id}
client_secret={client_secret}
grant_type=client_credentials
```

**Regenerate secret (invalidates old one):**
```
PATCH /oauth/serviceAccounts/{client_id}/regenerate
```
Returns the new `client_secret`. The old secret stops working immediately.

**Deactivate (without deleting):** the service-account endpoint only updates the description — deactivate through the account itself (`client_id` is its account `_id`):
```
PATCH /authorization/accounts/{client_id}
```
```json
{
  "updates": {
    "inactive": true
  }
}
```

After creating a service account, assign it to groups for permissions:
```
PATCH /authorization/accounts/{client_id}
```
```json
{
  "updates": {
    "memberOf": [
      {"groupId": "group-id", "aaaManaged": false}
    ]
  }
}
```

## SSO Configuration

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/sso/configs` | List SSO configurations |
| POST | `/sso/configs` | Create SSO config |
| GET | `/sso/configs/{name}` | Get SSO config |
| PUT | `/sso/configs/{name}` | Update SSO config |
| DELETE | `/sso/configs/{name}` | Delete SSO config |
| POST | `/sso/configs/{name}/active` | Activate/deactivate SSO config |
| GET | `/sso/enabled` | Check if SSO is enabled |
| GET | `/sso/test/{name}` | Test SSO configuration |

**SAML configuration** (`POST /sso/configs`; `PUT /sso/configs/{name}` takes the same body):
```json
{
  "config": {
    "name": "Okta SAML",
    "ssoType": "saml",
    "settings": {
      "issuer": "Itential",
      "loginURL": "https://idp.example.com/sso/saml",
      "certificate": "-----BEGIN CERTIFICATE-----\n...\n-----END CERTIFICATE-----"
    }
  }
}
```
`name`, `ssoType` and `settings` are required. Activate or deactivate with `POST /sso/configs/{name}/active` and `{"active": true}` (or `false`).

**Test SSO:**
```
GET /sso/test/{name}
```
Validates the configuration can reach the identity provider.

## Codeless Integrations (OpenAPI-based)

Codeless integrations let you connect to any REST API by uploading its OpenAPI spec. No adapter code needed — the platform generates tasks automatically from the spec's paths and operations.

**Two types of adapters on the platform:**
- **Code-based** — npm packages, show in `/health/adapters`, have custom logic
- **Codeless (integrations)** — from OpenAPI specs, `virtual: true`, show in `/integrations` only, auto-generated tasks

### Integration Models

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/integration-models` | Upload OpenAPI spec → creates model + auto-creates roles |
| GET | `/integration-models` | List all integration models |
| GET | `/integration-models/{name}` | Get a model |
| PUT | `/integration-models` | Update a model |
| DELETE | `/integration-models/{name}` | Delete a model |
| GET | `/integration-models/{name}/export` | Export a model |
| PUT | `/integration-models/validation` | Validate a model |
| GET | `/integration-models/{name}/securitySchemes` | Get auth schemes |

### Integration Instances

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/integrations` | Create an instance from a model |
| GET | `/integrations` | List all instances |
| GET | `/integrations/{name}` | Get instance detail |
| PUT | `/integrations/{name}` | Update instance |
| DELETE | `/integrations/{name}` | Delete instance |
| PUT | `/integrations/{name}/properties` | Update connection properties |
| GET | `/schema/integrations/{name}` | Get instance schema |

### Full Integration Flow (tested and confirmed)

**Step 1: Upload OpenAPI spec**
```
POST /integration-models
```
```json
{
  "model": {
    "openapi": "3.0.0",
    "info": {"title": "Cat Facts", "version": "1.0.0"},
    "servers": [{"url": "https://catfact.ninja"}],
    "paths": {
      "/fact": {
        "get": {
          "operationId": "getRandomFact",
          "summary": "Get a random cat fact",
          "responses": {"200": {"description": "A fact", "content": {"application/json": {"schema": {"type": "object"}}}}}
        }
      }
    }
  }
}
```
This creates:
- Model: `@itential/adapter_Cat Facts:1.0.0`
- Auto-created roles with `provenance: "Cat Facts:1.0.0"` containing the API methods

**Step 2: Create instance**
```
POST /integrations
```
```json
{
  "properties": {
    "name": "cat-facts",
    "type": "Adapter",
    "properties": {
      "id": "cat-facts",
      "type": "Cat Facts:1.0.0"
    },
    "virtual": true
  }
}
```
- `name` and `properties.id` must match — this is the instance name
- `properties.type` must match the model's `versionId`
- `virtual: true` marks it as codeless
- Connection config (host, protocol, base_path) is inherited from the model

**Step 3: Find auto-created role**
```
GET /authorization/roles?limit=100&sort=_id&order=-1
```
Sorting by `_id` descending puts the most-recently-created roles first — auto-created roles from an import appear at the top of page 1 rather than scattered across hundreds of pages. Search for roles where `provenance` matches the model's versionId:
```json
{
  "_id": "69a874718d7a2d0139edce14",
  "name": "admin",
  "provenance": "Cat Facts:1.0.0",
  "allowedMethods": [
    {"name": "getRandomFact", "provenance": "Cat Facts:1.0.0"}
  ]
}
```
Note: the API caps results at 100 per page regardless of the `limit` value. With `sort=_id&order=-1`, auto-created roles from a fresh import will be on page 1 — no need to paginate through the full role list.

**Step 4: Assign role to group**
```
PATCH /authorization/groups/{groupId}
```
```json
{
  "updates": {
    "assignedRoles": [
      {"roleId": "existing-role-1"},
      {"roleId": "existing-role-2"},
      {"roleId": "69a874718d7a2d0139edce14"}
    ]
  }
}
```
- Wrapper: `{updates: {assignedRoles: [...]}}` — NOT bare fields
- `assignedRoles` is a **full replacement** — include ALL existing roles plus the new one
- Get existing roles first: `GET /authorization/groups/{id}`

**Step 5: Re-authenticate**

Get a new token so the updated permissions take effect. Tasks now appear in the workflow palette.

**Step 6: Use in workflows**

In workflow tasks:
- `app`: the model versionId from `apps/list` (e.g., `"Cat Facts:1.0.0"`)
- `adapter_id`: the instance name (e.g., `"cat-facts"`)
- `locationType`: same as `app` (the versionId)
- `location`: `"Adapter"`

Response shape from codeless integrations is raw HTTP:
```json
{
  "ok": true,
  "url": "https://catfact.ninja/fact",
  "status": 200,
  "headers": {...},
  "body": "{\"fact\": \"Cats have 32 muscles in each ear.\", \"length\": 38}"
}
```
The actual API data is in `body` (as a JSON string) — use a `query` task to extract it.

## Pre-built Content

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/prebuilts` | List installed prebuilts |
| POST | `/prebuilts/import` | Import a prebuilt |
| GET | `/prebuilts/{id}` | Get prebuilt details |
| DELETE | `/prebuilts/{id}` | Delete a prebuilt |
| PUT | `/prebuilts/{id}` | Update a prebuilt |
| GET | `/prebuilts/{id}/export` | Export a prebuilt |
| PUT | `/prebuilts/import/validation` | Validate before importing |

**Repository (browse available prebuilts):**

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/prebuilts-repository` | Browse available prebuilts |
| POST | `/prebuilts-repository/configs` | Add repository config |
| GET | `/prebuilts-repository/configs` | List repository configs |
| DELETE | `/prebuilts-repository/configs/{name}` | Remove repository |
| PATCH | `/prebuilts-repository/configs/{name}` | Update repository |

**Import a prebuilt:**
```
POST /prebuilts/import
```
```json
{
  "prebuilt": {"metadata": {...}, "manifest": {...}, "bundles": [...], "readme": "..."},
  "options": {"overwrite": false}
}
```
`prebuilt` is the full JSON from `GET /prebuilts/{id}/export` or the repository.

**Validate before import:**
```
PUT /prebuilts/import/validation
```
Same `{"prebuilt": {...}}` body, without `options` — checks for conflicts before importing.

## Profiles

Profiles save adapter/application configurations for different environments.

A profile's `{id}` is its name (the `id` field in its properties).

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/profiles` | List profiles |
| POST | `/profiles` | Create a profile |
| GET | `/profiles/{id}` | Get a profile |
| PUT | `/profiles/{id}` | Update a profile |
| POST | `/profiles/import` | Import a profile |
| DELETE | `/profiles/{id}` | Delete a profile |
| PUT | `/profiles/{id}/active` | Activate a profile |
| GET | `/profiles/{id}/export` | Export a profile |
| GET | `/schema/profiles` | Get profile schema |

**Activate a profile** (switch environment):
```
PUT /profiles/{id}/active
```
No body. This applies the profile's saved adapter/app configurations. Use for switching between dev/staging/prod.

## Admin Scenarios

### 1. Onboard a new team member
```
1. Create a group (if needed): POST /authorization/groups
2. Create a role with needed permissions: POST /authorization/roles
3. Assign role to group: PATCH /authorization/groups/{id}
4. User logs in via SSO → auto-provisioned
5. Add to group: PATCH /authorization/accounts/{id} {updates: {memberOf: [...]}}
```

### 2. Create a service account for CI/CD
```
1. POST /oauth/serviceAccounts → save client_id and client_secret
2. PATCH /authorization/accounts/{client_id} {updates: {memberOf: [...]}} → add to group for permissions
3. Test: POST /oauth/token with client_credentials
4. Use token for API calls
```

### 3. Set up SSO
```
1. POST /sso/configs → create SAML/OIDC config
2. GET /sso/test/{name} → validate connectivity
3. POST /sso/configs/{name}/active → activate
4. GET /sso/enabled → confirm SSO is active
```

### 4. Import pre-built content
```
1. GET /prebuilts-repository → browse available content
2. PUT /prebuilts/import/validation → check for conflicts
3. POST /prebuilts/import → import
4. GET /prebuilts → verify installation
```

### 5. Add a new REST API integration (end-to-end)
```
1. POST /integration-models {model: <OpenAPI spec>}           → model + roles auto-created
2. POST /integrations {properties: {name, type:"Adapter", properties:{id, type:versionId}, virtual:true}}
3. GET /authorization/roles?limit=100&sort=_id&order=-1        → find role with provenance = versionId (newest first)
4. GET /authorization/groups/{id}                              → get current assignedRoles
5. PATCH /authorization/groups/{id} {updates: {assignedRoles: [...existing, {roleId: newRoleId}]}}
6. Re-authenticate                                            → tasks appear in palette
7. Build workflow with app=versionId, adapter_id=instanceName
8. POST /operations-manager/jobs/start                         → run it
```
