---
name: supabase-api-v1
description: "Supabase API (v1) API skill. Use when working with Supabase API (v1) for branches, projects, organizations. Covers 158 endpoints."
version: 1.0.0
generator: lapsh
---

# Supabase API (v1)
API version: 1.0.0

## Auth
Bearer bearer

## Base URL
Not specified.

## Setup
1. Set Authorization header with your Bearer token
2. GET /v1/projects -- verify access
3. POST /v1/branches/{branch_id_or_ref}/push -- create first push

## Endpoints

158 endpoints across 5 groups. See references/api-spec.lap for full details.

### branches
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/branches/{branch_id_or_ref} | Get database branch config |
| PATCH | /v1/branches/{branch_id_or_ref} | Update database branch config |
| DELETE | /v1/branches/{branch_id_or_ref} | Delete a database branch |
| POST | /v1/branches/{branch_id_or_ref}/push | Pushes a database branch |
| POST | /v1/branches/{branch_id_or_ref}/merge | Merges a database branch |
| POST | /v1/branches/{branch_id_or_ref}/reset | Resets a database branch |
| POST | /v1/branches/{branch_id_or_ref}/restore | Restore a scheduled branch deletion |
| GET | /v1/branches/{branch_id_or_ref}/diff | [Beta] Diffs a database branch |

### projects
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/projects | List all projects |
| POST | /v1/projects | Create a project |
| GET | /v1/projects/available-regions | [Beta] Gets the list of available regions that can be used for a new project |
| GET | /v1/projects/{ref}/actions | List all action runs |
| HEAD | /v1/projects/{ref}/actions | Count the number of action runs |
| GET | /v1/projects/{ref}/actions/{run_id} | Get the status of an action run |
| PATCH | /v1/projects/{ref}/actions/{run_id}/status | Update the status of an action run |
| GET | /v1/projects/{ref}/actions/{run_id}/logs | Get the logs of an action run |
| GET | /v1/projects/{ref}/api-keys | Get project api keys |
| POST | /v1/projects/{ref}/api-keys | Creates a new API key for the project |
| GET | /v1/projects/{ref}/api-keys/legacy | Check whether JWT based legacy (anon, service_role) API keys are enabled. This API endpoint will be removed in the future, check for HTTP 404 Not Found. |
| PUT | /v1/projects/{ref}/api-keys/legacy | Disable or re-enable JWT based legacy (anon, service_role) API keys. This API endpoint will be removed in the future, check for HTTP 404 Not Found. |
| PATCH | /v1/projects/{ref}/api-keys/{id} | Updates an API key for the project |
| GET | /v1/projects/{ref}/api-keys/{id} | Get API key |
| DELETE | /v1/projects/{ref}/api-keys/{id} | Deletes an API key for the project |
| GET | /v1/projects/{ref}/branches | List all database branches |
| POST | /v1/projects/{ref}/branches | Create a database branch |
| DELETE | /v1/projects/{ref}/branches | Disables preview branching |
| GET | /v1/projects/{ref}/branches/{name} | Get a database branch |
| GET | /v1/projects/{ref}/custom-hostname | [Beta] Gets project's custom hostname config |
| DELETE | /v1/projects/{ref}/custom-hostname | [Beta] Deletes a project's custom hostname configuration |
| POST | /v1/projects/{ref}/custom-hostname/initialize | [Beta] Updates project's custom hostname configuration |
| POST | /v1/projects/{ref}/custom-hostname/reverify | [Beta] Attempts to verify the DNS configuration for project's custom hostname configuration |
| POST | /v1/projects/{ref}/custom-hostname/activate | [Beta] Activates a custom hostname for a project. |
| GET | /v1/projects/{ref}/jit-access | [Beta] Get project's just-in-time access configuration. |
| PUT | /v1/projects/{ref}/jit-access | [Beta] Update project's just-in-time access configuration. |
| POST | /v1/projects/{ref}/network-bans/retrieve | [Beta] Gets project's network bans |
| POST | /v1/projects/{ref}/network-bans/retrieve/enriched | [Beta] Gets project's network bans with additional information about which databases they affect |
| DELETE | /v1/projects/{ref}/network-bans | [Beta] Remove network bans. |
| GET | /v1/projects/{ref}/network-restrictions | [Beta] Gets project's network restrictions |
| PATCH | /v1/projects/{ref}/network-restrictions | [Alpha] Updates project's network restrictions by adding or removing CIDRs |
| POST | /v1/projects/{ref}/network-restrictions/apply | [Beta] Updates project's network restrictions |
| GET | /v1/projects/{ref}/pgsodium | [Beta] Gets project's pgsodium config |
| PUT | /v1/projects/{ref}/pgsodium | [Beta] Updates project's pgsodium config. Updating the root_key can cause all data encrypted with the older key to become inaccessible. |
| GET | /v1/projects/{ref}/postgrest | Gets project's postgrest config |
| PATCH | /v1/projects/{ref}/postgrest | Updates project's postgrest config |
| GET | /v1/projects/{ref} | Gets a specific project that belongs to the authenticated user |
| DELETE | /v1/projects/{ref} | Deletes the given project |
| PATCH | /v1/projects/{ref} | Updates the given project |
| GET | /v1/projects/{ref}/secrets | List all secrets |
| POST | /v1/projects/{ref}/secrets | Bulk create secrets |
| DELETE | /v1/projects/{ref}/secrets | Bulk delete secrets |
| GET | /v1/projects/{ref}/ssl-enforcement | [Beta] Get project's SSL enforcement configuration. |
| PUT | /v1/projects/{ref}/ssl-enforcement | [Beta] Update project's SSL enforcement configuration. |
| GET | /v1/projects/{ref}/types/typescript | Generate TypeScript types |
| GET | /v1/projects/{ref}/vanity-subdomain | [Beta] Gets current vanity subdomain config |
| DELETE | /v1/projects/{ref}/vanity-subdomain | [Beta] Deletes a project's vanity subdomain configuration |
| POST | /v1/projects/{ref}/vanity-subdomain/check-availability | [Beta] Checks vanity subdomain availability |
| POST | /v1/projects/{ref}/vanity-subdomain/activate | [Beta] Activates a vanity subdomain for a project. |
| POST | /v1/projects/{ref}/upgrade | [Beta] Upgrades the project's Postgres version |
| GET | /v1/projects/{ref}/upgrade/eligibility | [Beta] Returns the project's eligibility for upgrades |
| GET | /v1/projects/{ref}/upgrade/status | [Beta] Gets the latest status of the project's upgrade |
| GET | /v1/projects/{ref}/readonly | Returns project's readonly mode status |
| POST | /v1/projects/{ref}/readonly/temporary-disable | Disables project's readonly mode for the next 15 minutes |
| POST | /v1/projects/{ref}/read-replicas/setup | [Beta] Set up a read replica |
| POST | /v1/projects/{ref}/read-replicas/remove | [Beta] Remove a read replica |
| GET | /v1/projects/{ref}/health | Gets project's service health status |
| POST | /v1/projects/{ref}/config/auth/signing-keys/legacy | Set up the project's existing JWT secret as an in_use JWT signing key. This endpoint will be removed in the future always check for HTTP 404 Not Found. |
| GET | /v1/projects/{ref}/config/auth/signing-keys/legacy | Get the signing key information for the JWT secret imported as signing key for this project. This endpoint will be removed in the future, check for HTTP 404 Not Found. |
| POST | /v1/projects/{ref}/config/auth/signing-keys | Create a new signing key for the project in standby status |
| GET | /v1/projects/{ref}/config/auth/signing-keys | List all signing keys for the project |
| GET | /v1/projects/{ref}/config/auth/signing-keys/{id} | Get information about a signing key |
| DELETE | /v1/projects/{ref}/config/auth/signing-keys/{id} | Remove a signing key from a project. Only possible if the key has been in revoked status for a while. |
| PATCH | /v1/projects/{ref}/config/auth/signing-keys/{id} | Update a signing key, mainly its status |
| GET | /v1/projects/{ref}/config/auth | Gets project's auth config |
| PATCH | /v1/projects/{ref}/config/auth | Updates a project's auth config |
| POST | /v1/projects/{ref}/config/auth/third-party-auth | Creates a new third-party auth integration |
| GET | /v1/projects/{ref}/config/auth/third-party-auth | Lists all third-party auth integrations |
| DELETE | /v1/projects/{ref}/config/auth/third-party-auth/{tpa_id} | Removes a third-party auth integration |
| GET | /v1/projects/{ref}/config/auth/third-party-auth/{tpa_id} | Get a third-party integration |
| POST | /v1/projects/{ref}/pause | Pauses the given project |
| GET | /v1/projects/{ref}/restore | Lists available restore versions for the given project |
| POST | /v1/projects/{ref}/restore | Restores the given project |
| POST | /v1/projects/{ref}/restore/cancel | Cancels the given project restoration |
| GET | /v1/projects/{ref}/billing/addons | List billing addons and compute instance selections |
| PATCH | /v1/projects/{ref}/billing/addons | Apply or update billing addons, including compute instance size |
| DELETE | /v1/projects/{ref}/billing/addons/{addon_variant} | Remove billing addons or revert compute instance sizing |
| GET | /v1/projects/{ref}/claim-token | Gets project claim token |
| POST | /v1/projects/{ref}/claim-token | Creates project claim token |
| DELETE | /v1/projects/{ref}/claim-token | Revokes project claim token |
| GET | /v1/projects/{ref}/advisors/performance | Gets project performance advisors. |
| GET | /v1/projects/{ref}/advisors/security | Gets project security advisors. |
| GET | /v1/projects/{ref}/analytics/endpoints/logs.all | Gets project's logs |
| GET | /v1/projects/{ref}/analytics/endpoints/usage.api-counts | Gets project's usage api counts |
| GET | /v1/projects/{ref}/analytics/endpoints/usage.api-requests-count | Gets project's usage api requests count |
| GET | /v1/projects/{ref}/analytics/endpoints/functions.combined-stats | Gets a project's function combined statistics |
| POST | /v1/projects/{ref}/cli/login-role | [Beta] Create a login role for CLI with temporary password |
| DELETE | /v1/projects/{ref}/cli/login-role | [Beta] Delete existing login roles used by CLI |
| GET | /v1/projects/{ref}/database/migrations | [Beta] List applied migration versions |
| POST | /v1/projects/{ref}/database/migrations | [Beta] Apply a database migration |
| PUT | /v1/projects/{ref}/database/migrations | [Beta] Upsert a database migration without applying |
| DELETE | /v1/projects/{ref}/database/migrations | [Beta] Rollback database migrations and remove them from history table |
| GET | /v1/projects/{ref}/database/migrations/{version} | [Beta] Fetch an existing entry from migration history |
| PATCH | /v1/projects/{ref}/database/migrations/{version} | [Beta] Patch an existing entry in migration history |
| POST | /v1/projects/{ref}/database/query | [Beta] Run sql query |
| POST | /v1/projects/{ref}/database/query/read-only | [Beta] Run a sql query as supabase_read_only_user |
| POST | /v1/projects/{ref}/database/webhooks/enable | [Beta] Enables Database Webhooks on the project |
| GET | /v1/projects/{ref}/database/context | Gets database metadata for the given project. |
| PATCH | /v1/projects/{ref}/database/password | Updates the database password |
| GET | /v1/projects/{ref}/database/jit | Get user-id to role mappings for JIT access |
| POST | /v1/projects/{ref}/database/jit | Authorize user-id to role mappings for JIT access |
| PUT | /v1/projects/{ref}/database/jit | Updates a user mapping for JIT access |
| GET | /v1/projects/{ref}/database/jit/list | List all user-id to role mappings for JIT access |
| DELETE | /v1/projects/{ref}/database/jit/{user_id} | Delete JIT access by user-id |
| GET | /v1/projects/{ref}/functions | List all functions |
| POST | /v1/projects/{ref}/functions | Create a function |
| PUT | /v1/projects/{ref}/functions | Bulk update functions |
| POST | /v1/projects/{ref}/functions/deploy | Deploy a function |
| GET | /v1/projects/{ref}/functions/{function_slug} | Retrieve a function |
| PATCH | /v1/projects/{ref}/functions/{function_slug} | Update a function |
| DELETE | /v1/projects/{ref}/functions/{function_slug} | Delete a function |
| GET | /v1/projects/{ref}/functions/{function_slug}/body | Retrieve a function body |
| GET | /v1/projects/{ref}/storage/buckets | Lists all buckets |
| GET | /v1/projects/{ref}/config/disk | Get database disk attributes |
| POST | /v1/projects/{ref}/config/disk | Modify database disk |
| GET | /v1/projects/{ref}/config/disk/util | Get disk utilization |
| GET | /v1/projects/{ref}/config/disk/autoscale | Gets project disk autoscale config |
| GET | /v1/projects/{ref}/config/storage | Gets project's storage config |
| PATCH | /v1/projects/{ref}/config/storage | Updates project's storage config |
| GET | /v1/projects/{ref}/config/database/pgbouncer | Get project's pgbouncer config |
| GET | /v1/projects/{ref}/config/database/pooler | Gets project's supavisor config |
| PATCH | /v1/projects/{ref}/config/database/pooler | Updates project's supavisor config |
| GET | /v1/projects/{ref}/config/database/postgres | Gets project's Postgres config |
| PUT | /v1/projects/{ref}/config/database/postgres | Updates project's Postgres config |
| GET | /v1/projects/{ref}/config/realtime | Gets realtime configuration |
| PATCH | /v1/projects/{ref}/config/realtime | Updates realtime configuration |
| POST | /v1/projects/{ref}/config/realtime/shutdown | Shutdowns realtime connections for a project |
| POST | /v1/projects/{ref}/config/auth/sso/providers | Creates a new SSO provider |
| GET | /v1/projects/{ref}/config/auth/sso/providers | Lists all SSO providers |
| GET | /v1/projects/{ref}/config/auth/sso/providers/{provider_id} | Gets a SSO provider by its UUID |
| PUT | /v1/projects/{ref}/config/auth/sso/providers/{provider_id} | Updates a SSO provider by its UUID |
| DELETE | /v1/projects/{ref}/config/auth/sso/providers/{provider_id} | Removes a SSO provider by its UUID |
| GET | /v1/projects/{ref}/database/backups | Lists all backups |
| POST | /v1/projects/{ref}/database/backups/restore-pitr | Restores a PITR backup for a database |
| POST | /v1/projects/{ref}/database/backups/restore-point | Initiates a creation of a restore point for a database |
| GET | /v1/projects/{ref}/database/backups/restore-point | Get restore points for project |
| POST | /v1/projects/{ref}/database/backups/undo | Initiates an undo to a given restore point |

### organizations
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/organizations | List all organizations |
| POST | /v1/organizations | Create an organization |
| GET | /v1/organizations/{slug}/members | List members of an organization |
| GET | /v1/organizations/{slug} | Gets information about the organization |
| GET | /v1/organizations/{slug}/project-claim/{token} | Gets project details for the specified organization and claim token |
| POST | /v1/organizations/{slug}/project-claim/{token} | Claims project for the specified organization |
| GET | /v1/organizations/{slug}/projects | Gets all projects for the given organization |

### oauth
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/oauth/authorize | [Beta] Authorize user through oauth |
| POST | /v1/oauth/token | [Beta] Exchange auth code for user's access and refresh token |
| POST | /v1/oauth/revoke | [Beta] Revoke oauth app authorization and it's corresponding tokens |
| GET | /v1/oauth/authorize/project-claim | Authorize user through oauth and claim a project |

### snippets
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/snippets | Lists SQL snippets for the logged in user |
| GET | /v1/snippets/{id} | Gets a specific SQL snippet |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get branche details?" -> GET /v1/branches/{branch_id_or_ref}
- "Partially update a branche?" -> PATCH /v1/branches/{branch_id_or_ref}
- "Delete a branche?" -> DELETE /v1/branches/{branch_id_or_ref}
- "Create a push?" -> POST /v1/branches/{branch_id_or_ref}/push
- "Create a merge?" -> POST /v1/branches/{branch_id_or_ref}/merge
- "Create a reset?" -> POST /v1/branches/{branch_id_or_ref}/reset
- "Create a restore?" -> POST /v1/branches/{branch_id_or_ref}/restore
- "List all diff?" -> GET /v1/branches/{branch_id_or_ref}/diff
- "List all projects?" -> GET /v1/projects
- "Create a project?" -> POST /v1/projects
- "List all available-regions?" -> GET /v1/projects/available-regions
- "List all organizations?" -> GET /v1/organizations
- "Create a organization?" -> POST /v1/organizations
- "List all authorize?" -> GET /v1/oauth/authorize
- "Create a token?" -> POST /v1/oauth/token
- "Create a revoke?" -> POST /v1/oauth/revoke
- "List all project-claim?" -> GET /v1/oauth/authorize/project-claim
- "List all snippets?" -> GET /v1/snippets
- "Get snippet details?" -> GET /v1/snippets/{id}
- "List all actions?" -> GET /v1/projects/{ref}/actions
- "Get action details?" -> GET /v1/projects/{ref}/actions/{run_id}
- "List all logs?" -> GET /v1/projects/{ref}/actions/{run_id}/logs
- "List all api-keys?" -> GET /v1/projects/{ref}/api-keys
- "Create a api-key?" -> POST /v1/projects/{ref}/api-keys
- "List all legacy?" -> GET /v1/projects/{ref}/api-keys/legacy
- "Partially update a api-key?" -> PATCH /v1/projects/{ref}/api-keys/{id}
- "Get api-key details?" -> GET /v1/projects/{ref}/api-keys/{id}
- "Delete a api-key?" -> DELETE /v1/projects/{ref}/api-keys/{id}
- "List all branches?" -> GET /v1/projects/{ref}/branches
- "Create a branche?" -> POST /v1/projects/{ref}/branches
- "Get branche details?" -> GET /v1/projects/{ref}/branches/{name}
- "List all custom-hostname?" -> GET /v1/projects/{ref}/custom-hostname
- "Create a initialize?" -> POST /v1/projects/{ref}/custom-hostname/initialize
- "Create a reverify?" -> POST /v1/projects/{ref}/custom-hostname/reverify
- "Create a activate?" -> POST /v1/projects/{ref}/custom-hostname/activate
- "List all jit-access?" -> GET /v1/projects/{ref}/jit-access
- "Create a retrieve?" -> POST /v1/projects/{ref}/network-bans/retrieve
- "Create a enriched?" -> POST /v1/projects/{ref}/network-bans/retrieve/enriched
- "List all network-restrictions?" -> GET /v1/projects/{ref}/network-restrictions
- "Create a apply?" -> POST /v1/projects/{ref}/network-restrictions/apply
- "List all pgsodium?" -> GET /v1/projects/{ref}/pgsodium
- "List all postgrest?" -> GET /v1/projects/{ref}/postgrest
- "Get project details?" -> GET /v1/projects/{ref}
- "Delete a project?" -> DELETE /v1/projects/{ref}
- "Partially update a project?" -> PATCH /v1/projects/{ref}
- "List all secrets?" -> GET /v1/projects/{ref}/secrets
- "Create a secret?" -> POST /v1/projects/{ref}/secrets
- "List all ssl-enforcement?" -> GET /v1/projects/{ref}/ssl-enforcement
- "List all typescript?" -> GET /v1/projects/{ref}/types/typescript
- "List all vanity-subdomain?" -> GET /v1/projects/{ref}/vanity-subdomain
- "Create a check-availability?" -> POST /v1/projects/{ref}/vanity-subdomain/check-availability
- "Create a activate?" -> POST /v1/projects/{ref}/vanity-subdomain/activate
- "Create a upgrade?" -> POST /v1/projects/{ref}/upgrade
- "List all eligibility?" -> GET /v1/projects/{ref}/upgrade/eligibility
- "List all status?" -> GET /v1/projects/{ref}/upgrade/status
- "List all readonly?" -> GET /v1/projects/{ref}/readonly
- "Create a temporary-disable?" -> POST /v1/projects/{ref}/readonly/temporary-disable
- "Create a setup?" -> POST /v1/projects/{ref}/read-replicas/setup
- "Create a remove?" -> POST /v1/projects/{ref}/read-replicas/remove
- "List all health?" -> GET /v1/projects/{ref}/health
- "Create a legacy?" -> POST /v1/projects/{ref}/config/auth/signing-keys/legacy
- "List all legacy?" -> GET /v1/projects/{ref}/config/auth/signing-keys/legacy
- "Create a signing-key?" -> POST /v1/projects/{ref}/config/auth/signing-keys
- "List all signing-keys?" -> GET /v1/projects/{ref}/config/auth/signing-keys
- "Get signing-key details?" -> GET /v1/projects/{ref}/config/auth/signing-keys/{id}
- "Delete a signing-key?" -> DELETE /v1/projects/{ref}/config/auth/signing-keys/{id}
- "Partially update a signing-key?" -> PATCH /v1/projects/{ref}/config/auth/signing-keys/{id}
- "List all auth?" -> GET /v1/projects/{ref}/config/auth
- "Create a third-party-auth?" -> POST /v1/projects/{ref}/config/auth/third-party-auth
- "List all third-party-auth?" -> GET /v1/projects/{ref}/config/auth/third-party-auth
- "Delete a third-party-auth?" -> DELETE /v1/projects/{ref}/config/auth/third-party-auth/{tpa_id}
- "Get third-party-auth details?" -> GET /v1/projects/{ref}/config/auth/third-party-auth/{tpa_id}
- "Create a pause?" -> POST /v1/projects/{ref}/pause
- "List all restore?" -> GET /v1/projects/{ref}/restore
- "Create a restore?" -> POST /v1/projects/{ref}/restore
- "Create a cancel?" -> POST /v1/projects/{ref}/restore/cancel
- "List all addons?" -> GET /v1/projects/{ref}/billing/addons
- "Delete a addon?" -> DELETE /v1/projects/{ref}/billing/addons/{addon_variant}
- "List all claim-token?" -> GET /v1/projects/{ref}/claim-token
- "Create a claim-token?" -> POST /v1/projects/{ref}/claim-token
- "List all performance?" -> GET /v1/projects/{ref}/advisors/performance
- "List all security?" -> GET /v1/projects/{ref}/advisors/security
- "List all logs.all?" -> GET /v1/projects/{ref}/analytics/endpoints/logs.all
- "List all usage.api-counts?" -> GET /v1/projects/{ref}/analytics/endpoints/usage.api-counts
- "List all usage.api-requests-count?" -> GET /v1/projects/{ref}/analytics/endpoints/usage.api-requests-count
- "List all functions.combined-stats?" -> GET /v1/projects/{ref}/analytics/endpoints/functions.combined-stats
- "Create a login-role?" -> POST /v1/projects/{ref}/cli/login-role
- "List all migrations?" -> GET /v1/projects/{ref}/database/migrations
- "Create a migration?" -> POST /v1/projects/{ref}/database/migrations
- "Get migration details?" -> GET /v1/projects/{ref}/database/migrations/{version}
- "Partially update a migration?" -> PATCH /v1/projects/{ref}/database/migrations/{version}
- "Create a query?" -> POST /v1/projects/{ref}/database/query
- "Create a read-only?" -> POST /v1/projects/{ref}/database/query/read-only
- "Create a enable?" -> POST /v1/projects/{ref}/database/webhooks/enable
- "List all context?" -> GET /v1/projects/{ref}/database/context
- "List all jit?" -> GET /v1/projects/{ref}/database/jit
- "Create a jit?" -> POST /v1/projects/{ref}/database/jit
- "List all list?" -> GET /v1/projects/{ref}/database/jit/list
- "Delete a jit?" -> DELETE /v1/projects/{ref}/database/jit/{user_id}
- "List all functions?" -> GET /v1/projects/{ref}/functions
- "Create a function?" -> POST /v1/projects/{ref}/functions
- "Create a deploy?" -> POST /v1/projects/{ref}/functions/deploy
- "Get function details?" -> GET /v1/projects/{ref}/functions/{function_slug}
- "Partially update a function?" -> PATCH /v1/projects/{ref}/functions/{function_slug}
- "Delete a function?" -> DELETE /v1/projects/{ref}/functions/{function_slug}
- "List all body?" -> GET /v1/projects/{ref}/functions/{function_slug}/body
- "List all buckets?" -> GET /v1/projects/{ref}/storage/buckets
- "List all disk?" -> GET /v1/projects/{ref}/config/disk
- "Create a disk?" -> POST /v1/projects/{ref}/config/disk
- "List all util?" -> GET /v1/projects/{ref}/config/disk/util
- "List all autoscale?" -> GET /v1/projects/{ref}/config/disk/autoscale
- "List all storage?" -> GET /v1/projects/{ref}/config/storage
- "List all pgbouncer?" -> GET /v1/projects/{ref}/config/database/pgbouncer
- "List all pooler?" -> GET /v1/projects/{ref}/config/database/pooler
- "List all postgres?" -> GET /v1/projects/{ref}/config/database/postgres
- "List all realtime?" -> GET /v1/projects/{ref}/config/realtime
- "Create a shutdown?" -> POST /v1/projects/{ref}/config/realtime/shutdown
- "Create a provider?" -> POST /v1/projects/{ref}/config/auth/sso/providers
- "List all providers?" -> GET /v1/projects/{ref}/config/auth/sso/providers
- "Get provider details?" -> GET /v1/projects/{ref}/config/auth/sso/providers/{provider_id}
- "Update a provider?" -> PUT /v1/projects/{ref}/config/auth/sso/providers/{provider_id}
- "Delete a provider?" -> DELETE /v1/projects/{ref}/config/auth/sso/providers/{provider_id}
- "List all backups?" -> GET /v1/projects/{ref}/database/backups
- "Create a restore-pitr?" -> POST /v1/projects/{ref}/database/backups/restore-pitr
- "Create a restore-point?" -> POST /v1/projects/{ref}/database/backups/restore-point
- "List all restore-point?" -> GET /v1/projects/{ref}/database/backups/restore-point
- "Create a undo?" -> POST /v1/projects/{ref}/database/backups/undo
- "List all members?" -> GET /v1/organizations/{slug}/members
- "Get organization details?" -> GET /v1/organizations/{slug}
- "Get project-claim details?" -> GET /v1/organizations/{slug}/project-claim/{token}
- "Search projects?" -> GET /v1/organizations/{slug}/projects
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
