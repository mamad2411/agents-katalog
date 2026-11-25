---
name: vercel-api
description: "Vercel API skill. Use when working with Vercel for access-groups, artifacts, billing. Covers 281 endpoints."
version: 1.0.0
generator: lapsh
---

# Vercel API
API version: 0.0.1

## Auth
Bearer bearer | OAuth2

## Base URL
https://api.vercel.com

## Setup
1. Set Authorization header with your Bearer token
2. GET /v1/access-groups -- verify access
3. POST /v1/access-groups/{idOrName} -- create first access-groups

## Endpoints

281 endpoints across 26 groups. See references/api-spec.lap for full details.

### access-groups
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/access-groups/{idOrName} | Reads an access group |
| POST | /v1/access-groups/{idOrName} | Update an access group |
| DELETE | /v1/access-groups/{idOrName} | Deletes an access group |
| GET | /v1/access-groups/{idOrName}/members | List members of an access group |
| GET | /v1/access-groups | List access groups for a team, project or member |
| POST | /v1/access-groups | Creates an access group |
| GET | /v1/access-groups/{idOrName}/projects | List projects of an access group |
| POST | /v1/access-groups/{accessGroupIdOrName}/projects | Create an access group project |
| GET | /v1/access-groups/{accessGroupIdOrName}/projects/{projectId} | Reads an access group project |
| PATCH | /v1/access-groups/{accessGroupIdOrName}/projects/{projectId} | Update an access group project |
| DELETE | /v1/access-groups/{accessGroupIdOrName}/projects/{projectId} | Delete an access group project |

### artifacts
| Method | Path | Description |
|--------|------|-------------|
| POST | /v8/artifacts/events | Record an artifacts cache usage event |
| GET | /v8/artifacts/status | Get status of Remote Caching for this principal |
| PUT | /v8/artifacts/{hash} | Upload a cache artifact |
| GET | /v8/artifacts/{hash} | Download a cache artifact |
| HEAD | /v8/artifacts/{hash} | Check if a cache artifact exists |
| POST | /v8/artifacts | Query information about an artifact |

### billing
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/billing/charges | List FOCUS billing charges |
| GET | /v1/billing/contract-commitments | List FOCUS contract commitments |

### bulk-redirects
| Method | Path | Description |
|--------|------|-------------|
| PUT | /v1/bulk-redirects | Stages new redirects for a project. |
| GET | /v1/bulk-redirects | Gets project-level redirects. |
| DELETE | /v1/bulk-redirects | Delete project-level redirects. |
| PATCH | /v1/bulk-redirects | Edit a project-level redirect. |
| POST | /v1/bulk-redirects/restore | Restore staged project-level redirects to their production version. |
| GET | /v1/bulk-redirects/versions | Get the version history for a project's redirects. |
| POST | /v1/bulk-redirects/versions | Promote a staging version to production or restore a previous production version. |

### projects
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/projects/{projectIdOrName}/checks | List all checks for a project |
| POST | /v2/projects/{projectIdOrName}/checks | Create a check |
| GET | /v2/projects/{projectIdOrName}/checks/{checkId} | Get a check |
| PATCH | /v2/projects/{projectIdOrName}/checks/{checkId} | Update a check |
| DELETE | /v2/projects/{projectIdOrName}/checks/{checkId} | Delete a check |
| GET | /v2/projects/{projectIdOrName}/checks/{checkId}/runs | List runs for a check |
| GET | /v1/projects/{projectIdOrName}/feature-flags/flags | List flags |
| PUT | /v1/projects/{projectIdOrName}/feature-flags/flags | Create a flag |
| GET | /v1/projects/{projectIdOrName}/feature-flags/flags/{flagIdOrSlug} | Get a flag |
| PATCH | /v1/projects/{projectIdOrName}/feature-flags/flags/{flagIdOrSlug} | Update a flag |
| DELETE | /v1/projects/{projectIdOrName}/feature-flags/flags/{flagIdOrSlug} | Delete a flag |
| GET | /v1/projects/{projectIdOrName}/feature-flags/flags/{flagIdOrSlug}/versions | List flag versions |
| GET | /v1/projects/{projectIdOrName}/feature-flags/settings | Get project flag settings |
| PATCH | /v1/projects/{projectIdOrName}/feature-flags/settings | Update project flag settings |
| PUT | /v1/projects/{projectIdOrName}/feature-flags/segments | Create a segment |
| GET | /v1/projects/{projectIdOrName}/feature-flags/segments | List segments |
| GET | /v1/projects/{projectIdOrName}/feature-flags/segments/{segmentIdOrSlug} | Get a segment |
| DELETE | /v1/projects/{projectIdOrName}/feature-flags/segments/{segmentIdOrSlug} | Delete a segment |
| PATCH | /v1/projects/{projectIdOrName}/feature-flags/segments/{segmentIdOrSlug} | Update a segment |
| GET | /v1/projects/{projectIdOrName}/feature-flags/sdk-keys | Get all SDK keys |
| PUT | /v1/projects/{projectIdOrName}/feature-flags/sdk-keys | Create an SDK key |
| DELETE | /v1/projects/{projectIdOrName}/feature-flags/sdk-keys/{hashKey} | Delete an SDK key |
| GET | /v1/projects/{projectId}/deployments/{deploymentId}/runtime-logs | Get logs for a deployment |
| GET | /v1/projects/{idOrName}/members | List project members |
| POST | /v1/projects/{idOrName}/members | Adds a new member to a project. |
| DELETE | /v1/projects/{idOrName}/members/{uid} | Remove a Project Member |
| GET | /v10/projects | Retrieve a list of projects |
| POST | /v11/projects | Create a new project |
| GET | /v9/projects/{idOrName} | Find a project by id or name |
| PATCH | /v9/projects/{idOrName} | Update an existing project |
| DELETE | /v9/projects/{idOrName} | Delete a Project |
| PATCH | /v1/projects/{idOrName}/shared-connect-links | Configures Static IPs for a project |
| POST | /v9/projects/{idOrName}/custom-environments | Create a custom environment for the current project. |
| GET | /v9/projects/{idOrName}/custom-environments | Retrieve custom environments |
| GET | /v9/projects/{idOrName}/custom-environments/{environmentSlugOrId} | Retrieve a custom environment |
| PATCH | /v9/projects/{idOrName}/custom-environments/{environmentSlugOrId} | Update a custom environment |
| DELETE | /v9/projects/{idOrName}/custom-environments/{environmentSlugOrId} | Remove a custom environment |
| GET | /v9/projects/{idOrName}/domains | Retrieve project domains by project by id or name |
| GET | /v9/projects/{idOrName}/domains/{domain} | Get a project domain |
| PATCH | /v9/projects/{idOrName}/domains/{domain} | Update a project domain |
| DELETE | /v9/projects/{idOrName}/domains/{domain} | Remove a domain from a project |
| POST | /v10/projects/{idOrName}/domains | Add a domain to a project |
| POST | /v1/projects/{idOrName}/domains/{domain}/move | Move a project domain |
| POST | /v9/projects/{idOrName}/domains/{domain}/verify | Verify project domain |
| GET | /v10/projects/{idOrName}/env | Retrieve the environment variables of a project by id or name |
| POST | /v10/projects/{idOrName}/env | Create one or more environment variables |
| GET | /v1/projects/{idOrName}/env/{id} | Retrieve the decrypted value of an environment variable of a project by id |
| DELETE | /v9/projects/{idOrName}/env/{id} | Remove an environment variable |
| PATCH | /v9/projects/{idOrName}/env/{id} | Edit an environment variable |
| DELETE | /v1/projects/{idOrName}/env | Batch remove environment variables |
| GET | /v1/projects/{idOrName}/rolling-release/billing | Get rolling release billing status |
| GET | /v1/projects/{idOrName}/rolling-release/config | Get rolling release configuration |
| DELETE | /v1/projects/{idOrName}/rolling-release/config | Delete rolling release configuration |
| PATCH | /v1/projects/{idOrName}/rolling-release/config | Update the rolling release settings for the project |
| GET | /v1/projects/{idOrName}/rolling-release | Get the active rolling release information for a project |
| POST | /v1/projects/{idOrName}/rolling-release/approve-stage | Update the active rolling release to the next stage for a project |
| POST | /v1/projects/{idOrName}/rolling-release/complete | Complete the rolling release for the project |
| POST | /projects/{idOrName}/transfer-request | Create project transfer request |
| PUT | /projects/transfer-request/{code} | Accept project transfer request |
| PATCH | /v1/projects/{idOrName}/protection-bypass | Update Protection Bypass for Automation |
| POST | /v1/projects/{projectId}/rollback/{deploymentId} | Points all production domains for a project to the given deploy |
| PATCH | /v1/projects/{projectId}/rollback/{deploymentId}/update-description | Updates the description for a rollback |
| POST | /v10/projects/{projectId}/promote/{deploymentId} | Points all production domains for a project to the given deploy |
| GET | /v1/projects/{projectId}/promote/aliases | Gets a list of aliases with status for the current promote |
| POST | /v1/projects/{projectId}/pause | Pause a project |
| POST | /v1/projects/{projectId}/unpause | Unpause a project |

### deployments
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/deployments/{deploymentId}/check-runs | List check runs for a deployment |
| POST | /v2/deployments/{deploymentId}/check-runs | Create a check run |
| GET | /v2/deployments/{deploymentId}/check-runs/{checkRunId} | Get a check run |
| PATCH | /v2/deployments/{deploymentId}/check-runs/{checkRunId} | Update a check run |
| POST | /v1/deployments/{deploymentId}/checks | Creates a new Check |
| GET | /v1/deployments/{deploymentId}/checks | Retrieve a list of all checks |
| GET | /v1/deployments/{deploymentId}/checks/{checkId} | Get a single check |
| PATCH | /v1/deployments/{deploymentId}/checks/{checkId} | Update a check |
| POST | /v1/deployments/{deploymentId}/checks/{checkId}/rerequest | Rerequest a check |
| GET | /v3/deployments/{idOrUrl}/events | Get deployment events |
| PATCH | /v1/deployments/{deploymentId}/integrations/{integrationConfigurationId}/resources/{resourceId}/actions/{action} | Update deployment integration action |
| GET | /v13/deployments/{idOrUrl} | Get a deployment by ID or URL |
| POST | /v13/deployments | Create a new deployment |
| PATCH | /v12/deployments/{id}/cancel | Cancel a deployment |
| GET | /v1/deployments/{deploymentId}/feature-flags | Retrieve the feature flags of a deployment |
| GET | /v2/deployments/{id}/aliases | List Deployment Aliases |
| POST | /v2/deployments/{id}/aliases | Assign an Alias |
| GET | /v6/deployments/{id}/files | List Deployment Files |
| GET | /v8/deployments/{id}/files/{fileId} | Get Deployment File Contents |
| GET | /v6/deployments | List deployments |
| DELETE | /v13/deployments/{id} | Delete a Deployment |

### connect
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/connect/networks | List Secure Compute networks |
| POST | /v1/connect/networks | Create a Secure Compute network |
| DELETE | /v1/connect/networks/{networkId} | Delete a Secure Compute network |
| PATCH | /v1/connect/networks/{networkId} | Update a Secure Compute network |
| GET | /v1/connect/networks/{networkId} | Read a Secure Compute network |

### domains
| Method | Path | Description |
|--------|------|-------------|
| GET | /v4/domains/{domain}/records | List existing DNS records |
| POST | /v2/domains/{domain}/records | Create a DNS record |
| PATCH | /v1/domains/records/{recordId} | Update an existing DNS record |
| DELETE | /v2/domains/{domain}/records/{recordId} | Delete a DNS record |
| GET | /v6/domains/{domain}/config | Get a Domain's configuration |
| GET | /v5/domains/{domain} | Get Information for a Single Domain |
| GET | /v5/domains | List all the domains |
| POST | /v7/domains | Add an existing domain to the Vercel platform |
| PATCH | /v3/domains/{domain} | Update or move apex domain |
| DELETE | /v6/domains/{domain} | Remove a domain by name |

### registrar
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/registrar/tlds/supported | Get supported TLDs |
| GET | /v1/registrar/tlds/{tld} | Get TLD |
| GET | /v1/registrar/tlds/{tld}/price | Get TLD price data |
| GET | /v1/registrar/domains/{domain}/availability | Get availability for a domain |
| GET | /v1/registrar/domains/{domain}/price | Get price data for a domain |
| POST | /v1/registrar/domains/availability | Get availability for multiple domains |
| GET | /v1/registrar/domains/{domain}/auth-code | Get the auth code for a domain |
| POST | /v1/registrar/domains/{domain}/buy | Buy a domain |
| POST | /v1/registrar/domains/buy | Buy multiple domains |
| POST | /v1/registrar/domains/{domain}/transfer | Transfer-in a domain |
| GET | /v1/registrar/domains/{domain}/transfer | Get a domain's transfer status |
| POST | /v1/registrar/domains/{domain}/renew | Renew a domain |
| PATCH | /v1/registrar/domains/{domain}/auto-renew | Update auto-renew for a domain |
| PATCH | /v1/registrar/domains/{domain}/nameservers | Update nameservers for a domain |
| GET | /v1/registrar/domains/{domain}/contact-info/schema | Get contact info schema |
| GET | /v1/registrar/orders/{orderId} | Get a domain order |

### log-drains
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/log-drains/{id} | Retrieves a Configurable Log Drain (deprecated) |
| DELETE | /v1/log-drains/{id} | Deletes a Configurable Log Drain (deprecated) |
| GET | /v1/log-drains | Retrieves a list of all the Log Drains (deprecated) |
| POST | /v1/log-drains | Creates a Configurable Log Drain (deprecated) |

### drains
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/drains | Create a new Drain |
| GET | /v1/drains | Retrieve a list of all Drains |
| DELETE | /v1/drains/{id} | Delete a drain |
| GET | /v1/drains/{id} | Find a Drain by id |
| PATCH | /v1/drains/{id} | Update an existing Drain |
| POST | /v1/drains/test | Validate Drain delivery configuration |

### edge-cache
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/edge-cache/invalidate-by-tags | Invalidate by tag |
| POST | /v1/edge-cache/dangerously-delete-by-tags | Dangerously delete by tag |
| POST | /v1/edge-cache/invalidate-by-src-images | Invalidate by source image |
| POST | /v1/edge-cache/dangerously-delete-by-src-images | Dangerously delete by source image |

### edge-config
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/edge-config | Get Edge Configs |
| POST | /v1/edge-config | Create an Edge Config |
| GET | /v1/edge-config/{edgeConfigId} | Get an Edge Config |
| PUT | /v1/edge-config/{edgeConfigId} | Update an Edge Config |
| DELETE | /v1/edge-config/{edgeConfigId} | Delete an Edge Config |
| GET | /v1/edge-config/{edgeConfigId}/items | Get Edge Config items |
| PATCH | /v1/edge-config/{edgeConfigId}/items | Update Edge Config items in batch |
| GET | /v1/edge-config/{edgeConfigId}/schema | Get Edge Config schema |
| POST | /v1/edge-config/{edgeConfigId}/schema | Update Edge Config schema |
| DELETE | /v1/edge-config/{edgeConfigId}/schema | Delete an Edge Config's schema |
| GET | /v1/edge-config/{edgeConfigId}/item/{edgeConfigItemKey} | Get an Edge Config item |
| GET | /v1/edge-config/{edgeConfigId}/tokens | Get all tokens of an Edge Config |
| DELETE | /v1/edge-config/{edgeConfigId}/tokens | Delete one or more Edge Config tokens |
| GET | /v1/edge-config/{edgeConfigId}/token/{token} | Get Edge Config token meta data |
| POST | /v1/edge-config/{edgeConfigId}/token | Create an Edge Config token |
| GET | /v1/edge-config/{edgeConfigId}/backups/{edgeConfigBackupVersionId} | Get Edge Config backup |
| GET | /v1/edge-config/{edgeConfigId}/backups | Get Edge Config backups |

### env
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/env | Create one or more shared environment variables |
| GET | /v1/env | Lists all Shared Environment Variables for a team |
| PATCH | /v1/env | Updates one or more shared environment variables |
| DELETE | /v1/env | Delete one or more Env Var |
| GET | /v1/env/{id} | Retrieve the decrypted value of a Shared Environment Variable by id. |
| PATCH | /v1/env/{id}/unlink/{projectId} | Disconnects a shared environment variable for a given project |

### events
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/events | List User Events |
| GET | /v1/events/types | List Event Types |

### teams
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/teams/{teamId}/feature-flags/settings | List team project flag settings |
| GET | /v1/teams/{teamId}/feature-flags/flags | List all flags for a team |
| GET | /v3/teams/{teamId}/members | List team members |
| POST | /v2/teams/{teamId}/members | Invite a user |
| POST | /v1/teams/{teamId}/request | Request access to a team |
| GET | /v1/teams/{teamId}/request/{userId} | Get access request status |
| POST | /v1/teams/{teamId}/members/teams/join | Join a team |
| PATCH | /v1/teams/{teamId}/members/{uid} | Update a Team Member |
| DELETE | /v1/teams/{teamId}/members/{uid} | Remove a Team Member |
| GET | /v2/teams/{teamId} | Get a Team |
| PATCH | /v2/teams/{teamId} | Update a Team |
| GET | /v2/teams | List all teams |
| POST | /v1/teams | Create a Team |
| POST | /v1/teams/{teamId}/dsync-roles | Update Team Directory Sync Role Mappings |
| DELETE | /v1/teams/{teamId} | Delete a Team |
| DELETE | /v1/teams/{teamId}/invites/{inviteId} | Delete a Team invite code |

### integrations
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/integrations/git-namespaces | List git namespaces by provider |
| GET | /v1/integrations/search-repo | List git repositories linked to namespace by provider |
| GET | /v1/integrations/integration/{integrationIdOrSlug}/products/{productIdOrSlug}/plans | List integration billing plans |
| POST | /v1/integrations/installations/{integrationConfigurationId}/resources/{resourceId}/connections | Connect integration resource to project |
| GET | /v1/integrations/configurations | Get configurations for the authenticated user or team |
| GET | /v1/integrations/configuration/{id} | Retrieve an integration configuration |
| DELETE | /v1/integrations/configuration/{id} | Delete an integration configuration |
| GET | /v1/integrations/configuration/{id}/products | List products for integration configuration |
| POST | /v1/integrations/sso/token | SSO Token Exchange |
| GET | /v2/integrations/log-drains | Retrieves a list of Integration log drains (deprecated) |
| POST | /v2/integrations/log-drains | Creates a new Integration Log Drain (deprecated) |
| DELETE | /v1/integrations/log-drains/{id} | Deletes the Integration log drain with the provided `id` (deprecated) |

### installations
| Method | Path | Description |
|--------|------|-------------|
| PATCH | /v1/installations/{integrationConfigurationId} | Update Installation |
| GET | /v1/installations/{integrationConfigurationId}/account | Get Account Information |
| GET | /v1/installations/{integrationConfigurationId}/member/{memberId} | Get Member Information |
| POST | /v1/installations/{integrationConfigurationId}/events | Create Event |
| GET | /v1/installations/{integrationConfigurationId}/resources | Get Integration Resources |
| GET | /v1/installations/{integrationConfigurationId}/resources/{resourceId} | Get Integration Resource |
| DELETE | /v1/installations/{integrationConfigurationId}/resources/{resourceId} | Delete Integration Resource |
| PUT | /v1/installations/{integrationConfigurationId}/resources/{resourceId} | Import Resource |
| PATCH | /v1/installations/{integrationConfigurationId}/resources/{resourceId} | Update Resource |
| POST | /v1/installations/{integrationConfigurationId}/billing | Submit Billing Data |
| POST | /v1/installations/{integrationConfigurationId}/billing/invoices | Submit Invoice |
| POST | /v1/installations/{integrationConfigurationId}/billing/finalize | Finalize Installation |
| GET | /v1/installations/{integrationConfigurationId}/billing/invoices/{invoiceId} | Get Invoice |
| POST | /v1/installations/{integrationConfigurationId}/billing/invoices/{invoiceId}/actions | Invoice Actions |
| POST | /v1/installations/{integrationConfigurationId}/billing/balance | Submit Prepayment Balances |
| PUT | /v1/installations/{integrationConfigurationId}/products/{integrationProductIdOrSlug}/resources/{resourceId}/secrets | Update Resource Secrets (Deprecated) |
| PUT | /v1/installations/{integrationConfigurationId}/resources/{resourceId}/secrets | Update Resource Secrets |
| POST | /v1/installations/{integrationConfigurationId}/resources/{resourceId}/experimentation/items | Create one or multiple experimentation items |
| PATCH | /v1/installations/{integrationConfigurationId}/resources/{resourceId}/experimentation/items/{itemId} | Patch an existing experimentation item |
| DELETE | /v1/installations/{integrationConfigurationId}/resources/{resourceId}/experimentation/items/{itemId} | Delete an existing experimentation item |
| HEAD | /v1/installations/{integrationConfigurationId}/resources/{resourceId}/experimentation/edge-config | Get the data of a user-provided Edge Config |
| GET | /v1/installations/{integrationConfigurationId}/resources/{resourceId}/experimentation/edge-config | Get the data of a user-provided Edge Config |
| PUT | /v1/installations/{integrationConfigurationId}/resources/{resourceId}/experimentation/edge-config | Push data into a user-provided Edge Config |

### sandboxes
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/sandboxes | List sandboxes |
| POST | /v1/sandboxes | Create a sandbox |
| GET | /v1/sandboxes/snapshots | List snapshots |
| GET | /v1/sandboxes/{sandboxId} | Get a sandbox |
| GET | /v1/sandboxes/{sandboxId}/cmd | List commands |
| POST | /v1/sandboxes/{sandboxId}/cmd | Execute a command |
| POST | /v1/sandboxes/{sandboxId}/{cmdId}/kill | Kill a command |
| POST | /v1/sandboxes/{sandboxId}/stop | Stop a sandbox |
| POST | /v1/sandboxes/{sandboxId}/extend-timeout | Extend sandbox timeout |
| POST | /v1/sandboxes/{sandboxId}/network-policy | Update network policy |
| GET | /v1/sandboxes/{sandboxId}/cmd/{cmdId} | Get a command |
| GET | /v1/sandboxes/{sandboxId}/cmd/{cmdId}/logs | Stream command logs |
| POST | /v1/sandboxes/{sandboxId}/fs/read | Read a file |
| POST | /v1/sandboxes/{sandboxId}/fs/mkdir | Create a directory |
| POST | /v1/sandboxes/{sandboxId}/fs/write | Write files |
| GET | /v1/sandboxes/snapshots/{snapshotId} | Get a snapshot |
| DELETE | /v1/sandboxes/snapshots/{snapshotId} | Delete a snapshot |
| POST | /v1/sandboxes/{sandboxId}/snapshot | Create a snapshot |

### security
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/security/attack-mode | Update Attack Challenge mode |
| PUT | /v1/security/firewall/config | Put Firewall Configuration |
| PATCH | /v1/security/firewall/config | Update Firewall Configuration |
| GET | /v1/security/firewall/config/{configVersion} | Read Firewall Configuration |
| GET | /v1/security/firewall/attack-status | Read active attack data |
| GET | /v1/security/firewall/bypass | Read System Bypass |
| POST | /v1/security/firewall/bypass | Create System Bypass Rule |
| DELETE | /v1/security/firewall/bypass | Remove System Bypass Rule |
| GET | /v1/security/firewall/events | Read Firewall Actions by Project |

### storage
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/storage/stores/integration/direct | Create integration store (free and paid plans) |

### files
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/files | Upload Deployment Files |

### user
| Method | Path | Description |
|--------|------|-------------|
| GET | /v5/user/tokens | List Auth Tokens |
| POST | /v3/user/tokens | Create an Auth Token |
| GET | /v5/user/tokens/{tokenId} | Get Auth Token Metadata |
| DELETE | /v3/user/tokens/{tokenId} | Delete an authentication token |
| GET | /v2/user | Get the User |
| DELETE | /v1/user | Delete User Account |

### webhooks
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/webhooks | Creates a webhook |
| GET | /v1/webhooks | Get a list of webhooks |
| GET | /v1/webhooks/{id} | Get a webhook |
| DELETE | /v1/webhooks/{id} | Deletes a webhook |

### aliases
| Method | Path | Description |
|--------|------|-------------|
| GET | /v4/aliases | List aliases |
| GET | /v4/aliases/{idOrAlias} | Get an Alias |
| DELETE | /v2/aliases/{aliasId} | Delete an Alias |
| PATCH | /aliases/{id}/protection-bypass | Update the protection bypass for a URL |

### certs
| Method | Path | Description |
|--------|------|-------------|
| GET | /v8/certs/{id} | Get cert by id |
| DELETE | /v8/certs/{id} | Remove cert |
| POST | /v8/certs | Issue a new cert |
| PUT | /v8/certs | Upload a cert |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get access-group details?" -> GET /v1/access-groups/{idOrName}
- "Delete a access-group?" -> DELETE /v1/access-groups/{idOrName}
- "Search members?" -> GET /v1/access-groups/{idOrName}/members
- "Search access-groups?" -> GET /v1/access-groups
- "Create a access-group?" -> POST /v1/access-groups
- "List all projects?" -> GET /v1/access-groups/{idOrName}/projects
- "Create a project?" -> POST /v1/access-groups/{accessGroupIdOrName}/projects
- "Get project details?" -> GET /v1/access-groups/{accessGroupIdOrName}/projects/{projectId}
- "Partially update a project?" -> PATCH /v1/access-groups/{accessGroupIdOrName}/projects/{projectId}
- "Delete a project?" -> DELETE /v1/access-groups/{accessGroupIdOrName}/projects/{projectId}
- "Create a event?" -> POST /v8/artifacts/events
- "List all status?" -> GET /v8/artifacts/status
- "Update a artifact?" -> PUT /v8/artifacts/{hash}
- "Get artifact details?" -> GET /v8/artifacts/{hash}
- "Create a artifact?" -> POST /v8/artifacts
- "List all charges?" -> GET /v1/billing/charges
- "List all contract-commitments?" -> GET /v1/billing/contract-commitments
- "Search bulk-redirects?" -> GET /v1/bulk-redirects
- "Create a restore?" -> POST /v1/bulk-redirects/restore
- "List all versions?" -> GET /v1/bulk-redirects/versions
- "Create a version?" -> POST /v1/bulk-redirects/versions
- "List all checks?" -> GET /v2/projects/{projectIdOrName}/checks
- "Create a check?" -> POST /v2/projects/{projectIdOrName}/checks
- "Get check details?" -> GET /v2/projects/{projectIdOrName}/checks/{checkId}
- "Partially update a check?" -> PATCH /v2/projects/{projectIdOrName}/checks/{checkId}
- "Delete a check?" -> DELETE /v2/projects/{projectIdOrName}/checks/{checkId}
- "List all runs?" -> GET /v2/projects/{projectIdOrName}/checks/{checkId}/runs
- "List all check-runs?" -> GET /v2/deployments/{deploymentId}/check-runs
- "Create a check-run?" -> POST /v2/deployments/{deploymentId}/check-runs
- "Get check-run details?" -> GET /v2/deployments/{deploymentId}/check-runs/{checkRunId}
- "Partially update a check-run?" -> PATCH /v2/deployments/{deploymentId}/check-runs/{checkRunId}
- "Create a check?" -> POST /v1/deployments/{deploymentId}/checks
- "List all checks?" -> GET /v1/deployments/{deploymentId}/checks
- "Get check details?" -> GET /v1/deployments/{deploymentId}/checks/{checkId}
- "Partially update a check?" -> PATCH /v1/deployments/{deploymentId}/checks/{checkId}
- "Create a rerequest?" -> POST /v1/deployments/{deploymentId}/checks/{checkId}/rerequest
- "Search networks?" -> GET /v1/connect/networks
- "Create a network?" -> POST /v1/connect/networks
- "Delete a network?" -> DELETE /v1/connect/networks/{networkId}
- "Partially update a network?" -> PATCH /v1/connect/networks/{networkId}
- "Get network details?" -> GET /v1/connect/networks/{networkId}
- "List all events?" -> GET /v3/deployments/{idOrUrl}/events
- "Partially update a action?" -> PATCH /v1/deployments/{deploymentId}/integrations/{integrationConfigurationId}/resources/{resourceId}/actions/{action}
- "Get deployment details?" -> GET /v13/deployments/{idOrUrl}
- "Create a deployment?" -> POST /v13/deployments
- "List all records?" -> GET /v4/domains/{domain}/records
- "Create a record?" -> POST /v2/domains/{domain}/records
- "Partially update a record?" -> PATCH /v1/domains/records/{recordId}
- "Delete a record?" -> DELETE /v2/domains/{domain}/records/{recordId}
- "List all supported?" -> GET /v1/registrar/tlds/supported
- "Get tld details?" -> GET /v1/registrar/tlds/{tld}
- "List all price?" -> GET /v1/registrar/tlds/{tld}/price
- "List all availability?" -> GET /v1/registrar/domains/{domain}/availability
- "List all price?" -> GET /v1/registrar/domains/{domain}/price
- "Create a availability?" -> POST /v1/registrar/domains/availability
- "List all auth-code?" -> GET /v1/registrar/domains/{domain}/auth-code
- "Create a buy?" -> POST /v1/registrar/domains/{domain}/buy
- "Create a buy?" -> POST /v1/registrar/domains/buy
- "Create a transfer?" -> POST /v1/registrar/domains/{domain}/transfer
- "List all transfer?" -> GET /v1/registrar/domains/{domain}/transfer
- "Create a renew?" -> POST /v1/registrar/domains/{domain}/renew
- "List all schema?" -> GET /v1/registrar/domains/{domain}/contact-info/schema
- "Get order details?" -> GET /v1/registrar/orders/{orderId}
- "List all config?" -> GET /v6/domains/{domain}/config
- "Get domain details?" -> GET /v5/domains/{domain}
- "List all domains?" -> GET /v5/domains
- "Create a domain?" -> POST /v7/domains
- "Partially update a domain?" -> PATCH /v3/domains/{domain}
- "Delete a domain?" -> DELETE /v6/domains/{domain}
- "Get log-drain details?" -> GET /v1/log-drains/{id}
- "Delete a log-drain?" -> DELETE /v1/log-drains/{id}
- "List all log-drains?" -> GET /v1/log-drains
- "Create a log-drain?" -> POST /v1/log-drains
- "Create a drain?" -> POST /v1/drains
- "List all drains?" -> GET /v1/drains
- "Delete a drain?" -> DELETE /v1/drains/{id}
- "Get drain details?" -> GET /v1/drains/{id}
- "Partially update a drain?" -> PATCH /v1/drains/{id}
- "Create a test?" -> POST /v1/drains/test
- "Create a invalidate-by-tag?" -> POST /v1/edge-cache/invalidate-by-tags
- "Create a dangerously-delete-by-tag?" -> POST /v1/edge-cache/dangerously-delete-by-tags
- "Create a invalidate-by-src-image?" -> POST /v1/edge-cache/invalidate-by-src-images
- "Create a dangerously-delete-by-src-image?" -> POST /v1/edge-cache/dangerously-delete-by-src-images
- "List all edge-config?" -> GET /v1/edge-config
- "Create a edge-config?" -> POST /v1/edge-config
- "Get edge-config details?" -> GET /v1/edge-config/{edgeConfigId}
- "Update a edge-config?" -> PUT /v1/edge-config/{edgeConfigId}
- "Delete a edge-config?" -> DELETE /v1/edge-config/{edgeConfigId}
- "List all items?" -> GET /v1/edge-config/{edgeConfigId}/items
- "List all schema?" -> GET /v1/edge-config/{edgeConfigId}/schema
- "Create a schema?" -> POST /v1/edge-config/{edgeConfigId}/schema
- "Get item details?" -> GET /v1/edge-config/{edgeConfigId}/item/{edgeConfigItemKey}
- "List all tokens?" -> GET /v1/edge-config/{edgeConfigId}/tokens
- "Get token details?" -> GET /v1/edge-config/{edgeConfigId}/token/{token}
- "Create a token?" -> POST /v1/edge-config/{edgeConfigId}/token
- "Get backup details?" -> GET /v1/edge-config/{edgeConfigId}/backups/{edgeConfigBackupVersionId}
- "List all backups?" -> GET /v1/edge-config/{edgeConfigId}/backups
- "Create a env?" -> POST /v1/env
- "Search env?" -> GET /v1/env
- "Get env details?" -> GET /v1/env/{id}
- "Partially update a unlink?" -> PATCH /v1/env/{id}/unlink/{projectId}
- "List all events?" -> GET /v3/events
- "List all types?" -> GET /v1/events/types
- "Search flags?" -> GET /v1/projects/{projectIdOrName}/feature-flags/flags
- "Get flag details?" -> GET /v1/projects/{projectIdOrName}/feature-flags/flags/{flagIdOrSlug}
- "Partially update a flag?" -> PATCH /v1/projects/{projectIdOrName}/feature-flags/flags/{flagIdOrSlug}
- "Delete a flag?" -> DELETE /v1/projects/{projectIdOrName}/feature-flags/flags/{flagIdOrSlug}
- "List all versions?" -> GET /v1/projects/{projectIdOrName}/feature-flags/flags/{flagIdOrSlug}/versions
- "List all settings?" -> GET /v1/projects/{projectIdOrName}/feature-flags/settings
- "List all settings?" -> GET /v1/teams/{teamId}/feature-flags/settings
- "Search flags?" -> GET /v1/teams/{teamId}/feature-flags/flags
- "List all segments?" -> GET /v1/projects/{projectIdOrName}/feature-flags/segments
- "Get segment details?" -> GET /v1/projects/{projectIdOrName}/feature-flags/segments/{segmentIdOrSlug}
- "Delete a segment?" -> DELETE /v1/projects/{projectIdOrName}/feature-flags/segments/{segmentIdOrSlug}
- "Partially update a segment?" -> PATCH /v1/projects/{projectIdOrName}/feature-flags/segments/{segmentIdOrSlug}
- "List all feature-flags?" -> GET /v1/deployments/{deploymentId}/feature-flags
- "List all sdk-keys?" -> GET /v1/projects/{projectIdOrName}/feature-flags/sdk-keys
- "Delete a sdk-key?" -> DELETE /v1/projects/{projectIdOrName}/feature-flags/sdk-keys/{hashKey}
- "List all git-namespaces?" -> GET /v1/integrations/git-namespaces
- "Search search-repo?" -> GET /v1/integrations/search-repo
- "List all plans?" -> GET /v1/integrations/integration/{integrationIdOrSlug}/products/{productIdOrSlug}/plans
- "Create a connection?" -> POST /v1/integrations/installations/{integrationConfigurationId}/resources/{resourceId}/connections
- "Partially update a installation?" -> PATCH /v1/installations/{integrationConfigurationId}
- "List all account?" -> GET /v1/installations/{integrationConfigurationId}/account
- "Get member details?" -> GET /v1/installations/{integrationConfigurationId}/member/{memberId}
- "Create a event?" -> POST /v1/installations/{integrationConfigurationId}/events
- "List all resources?" -> GET /v1/installations/{integrationConfigurationId}/resources
- "Get resource details?" -> GET /v1/installations/{integrationConfigurationId}/resources/{resourceId}
- "Delete a resource?" -> DELETE /v1/installations/{integrationConfigurationId}/resources/{resourceId}
- "Update a resource?" -> PUT /v1/installations/{integrationConfigurationId}/resources/{resourceId}
- "Partially update a resource?" -> PATCH /v1/installations/{integrationConfigurationId}/resources/{resourceId}
- "Create a billing?" -> POST /v1/installations/{integrationConfigurationId}/billing
- "Create a invoice?" -> POST /v1/installations/{integrationConfigurationId}/billing/invoices
- "Create a finalize?" -> POST /v1/installations/{integrationConfigurationId}/billing/finalize
- "Get invoice details?" -> GET /v1/installations/{integrationConfigurationId}/billing/invoices/{invoiceId}
- "Create a action?" -> POST /v1/installations/{integrationConfigurationId}/billing/invoices/{invoiceId}/actions
- "Create a balance?" -> POST /v1/installations/{integrationConfigurationId}/billing/balance
- "List all configurations?" -> GET /v1/integrations/configurations
- "Get configuration details?" -> GET /v1/integrations/configuration/{id}
- "Delete a configuration?" -> DELETE /v1/integrations/configuration/{id}
- "List all products?" -> GET /v1/integrations/configuration/{id}/products
- "Create a token?" -> POST /v1/integrations/sso/token
- "List all log-drains?" -> GET /v2/integrations/log-drains
- "Create a log-drain?" -> POST /v2/integrations/log-drains
- "Delete a log-drain?" -> DELETE /v1/integrations/log-drains/{id}
- "List all runtime-logs?" -> GET /v1/projects/{projectId}/deployments/{deploymentId}/runtime-logs
- "Create a item?" -> POST /v1/installations/{integrationConfigurationId}/resources/{resourceId}/experimentation/items
- "Partially update a item?" -> PATCH /v1/installations/{integrationConfigurationId}/resources/{resourceId}/experimentation/items/{itemId}
- "Delete a item?" -> DELETE /v1/installations/{integrationConfigurationId}/resources/{resourceId}/experimentation/items/{itemId}
- "List all edge-config?" -> GET /v1/installations/{integrationConfigurationId}/resources/{resourceId}/experimentation/edge-config
- "Search members?" -> GET /v1/projects/{idOrName}/members
- "Create a member?" -> POST /v1/projects/{idOrName}/members
- "Delete a member?" -> DELETE /v1/projects/{idOrName}/members/{uid}
- "Search projects?" -> GET /v10/projects
- "Create a project?" -> POST /v11/projects
- "Get project details?" -> GET /v9/projects/{idOrName}
- "Partially update a project?" -> PATCH /v9/projects/{idOrName}
- "Delete a project?" -> DELETE /v9/projects/{idOrName}
- "Create a custom-environment?" -> POST /v9/projects/{idOrName}/custom-environments
- "List all custom-environments?" -> GET /v9/projects/{idOrName}/custom-environments
- "Get custom-environment details?" -> GET /v9/projects/{idOrName}/custom-environments/{environmentSlugOrId}
- "Partially update a custom-environment?" -> PATCH /v9/projects/{idOrName}/custom-environments/{environmentSlugOrId}
- "Delete a custom-environment?" -> DELETE /v9/projects/{idOrName}/custom-environments/{environmentSlugOrId}
- "List all domains?" -> GET /v9/projects/{idOrName}/domains
- "Get domain details?" -> GET /v9/projects/{idOrName}/domains/{domain}
- "Partially update a domain?" -> PATCH /v9/projects/{idOrName}/domains/{domain}
- "Delete a domain?" -> DELETE /v9/projects/{idOrName}/domains/{domain}
- "Create a domain?" -> POST /v10/projects/{idOrName}/domains
- "Create a move?" -> POST /v1/projects/{idOrName}/domains/{domain}/move
- "Create a verify?" -> POST /v9/projects/{idOrName}/domains/{domain}/verify
- "List all env?" -> GET /v10/projects/{idOrName}/env
- "Create a env?" -> POST /v10/projects/{idOrName}/env
- "Get env details?" -> GET /v1/projects/{idOrName}/env/{id}
- "Delete a env?" -> DELETE /v9/projects/{idOrName}/env/{id}
- "Partially update a env?" -> PATCH /v9/projects/{idOrName}/env/{id}
- "List all billing?" -> GET /v1/projects/{idOrName}/rolling-release/billing
- "List all config?" -> GET /v1/projects/{idOrName}/rolling-release/config
- "List all rolling-release?" -> GET /v1/projects/{idOrName}/rolling-release
- "Create a approve-stage?" -> POST /v1/projects/{idOrName}/rolling-release/approve-stage
- "Create a complete?" -> POST /v1/projects/{idOrName}/rolling-release/complete
- "Create a transfer-request?" -> POST /projects/{idOrName}/transfer-request
- "Update a transfer-request?" -> PUT /projects/transfer-request/{code}
- "List all aliases?" -> GET /v1/projects/{projectId}/promote/aliases
- "Create a pause?" -> POST /v1/projects/{projectId}/pause
- "Create a unpause?" -> POST /v1/projects/{projectId}/unpause
- "List all sandboxes?" -> GET /v1/sandboxes
- "Create a sandboxe?" -> POST /v1/sandboxes
- "List all snapshots?" -> GET /v1/sandboxes/snapshots
- "Get sandboxe details?" -> GET /v1/sandboxes/{sandboxId}
- "List all cmd?" -> GET /v1/sandboxes/{sandboxId}/cmd
- "Create a cmd?" -> POST /v1/sandboxes/{sandboxId}/cmd
- "Create a kill?" -> POST /v1/sandboxes/{sandboxId}/{cmdId}/kill
- "Create a stop?" -> POST /v1/sandboxes/{sandboxId}/stop
- "Create a extend-timeout?" -> POST /v1/sandboxes/{sandboxId}/extend-timeout
- "Create a network-policy?" -> POST /v1/sandboxes/{sandboxId}/network-policy
- "Get cmd details?" -> GET /v1/sandboxes/{sandboxId}/cmd/{cmdId}
- "List all logs?" -> GET /v1/sandboxes/{sandboxId}/cmd/{cmdId}/logs
- "Create a read?" -> POST /v1/sandboxes/{sandboxId}/fs/read
- "Create a mkdir?" -> POST /v1/sandboxes/{sandboxId}/fs/mkdir
- "Create a write?" -> POST /v1/sandboxes/{sandboxId}/fs/write
- "Get snapshot details?" -> GET /v1/sandboxes/snapshots/{snapshotId}
- "Delete a snapshot?" -> DELETE /v1/sandboxes/snapshots/{snapshotId}
- "Create a snapshot?" -> POST /v1/sandboxes/{sandboxId}/snapshot
- "Create a attack-mode?" -> POST /v1/security/attack-mode
- "Get config details?" -> GET /v1/security/firewall/config/{configVersion}
- "List all attack-status?" -> GET /v1/security/firewall/attack-status
- "List all bypass?" -> GET /v1/security/firewall/bypass
- "Create a bypass?" -> POST /v1/security/firewall/bypass
- "List all events?" -> GET /v1/security/firewall/events
- "Create a direct?" -> POST /v1/storage/stores/integration/direct
- "Search members?" -> GET /v3/teams/{teamId}/members
- "Create a member?" -> POST /v2/teams/{teamId}/members
- "Create a request?" -> POST /v1/teams/{teamId}/request
- "Get request details?" -> GET /v1/teams/{teamId}/request/{userId}
- "Create a join?" -> POST /v1/teams/{teamId}/members/teams/join
- "Partially update a member?" -> PATCH /v1/teams/{teamId}/members/{uid}
- "Delete a member?" -> DELETE /v1/teams/{teamId}/members/{uid}
- "Get team details?" -> GET /v2/teams/{teamId}
- "Partially update a team?" -> PATCH /v2/teams/{teamId}
- "List all teams?" -> GET /v2/teams
- "Create a team?" -> POST /v1/teams
- "Create a dsync-role?" -> POST /v1/teams/{teamId}/dsync-roles
- "Delete a team?" -> DELETE /v1/teams/{teamId}
- "Delete a invite?" -> DELETE /v1/teams/{teamId}/invites/{inviteId}
- "Create a file?" -> POST /v2/files
- "List all tokens?" -> GET /v5/user/tokens
- "Create a token?" -> POST /v3/user/tokens
- "Get token details?" -> GET /v5/user/tokens/{tokenId}
- "Delete a token?" -> DELETE /v3/user/tokens/{tokenId}
- "List all user?" -> GET /v2/user
- "Create a webhook?" -> POST /v1/webhooks
- "List all webhooks?" -> GET /v1/webhooks
- "Get webhook details?" -> GET /v1/webhooks/{id}
- "Delete a webhook?" -> DELETE /v1/webhooks/{id}
- "List all aliases?" -> GET /v2/deployments/{id}/aliases
- "Create a aliase?" -> POST /v2/deployments/{id}/aliases
- "List all aliases?" -> GET /v4/aliases
- "Get aliase details?" -> GET /v4/aliases/{idOrAlias}
- "Delete a aliase?" -> DELETE /v2/aliases/{aliasId}
- "Get cert details?" -> GET /v8/certs/{id}
- "Delete a cert?" -> DELETE /v8/certs/{id}
- "Create a cert?" -> POST /v8/certs
- "List all files?" -> GET /v6/deployments/{id}/files
- "Get file details?" -> GET /v8/deployments/{id}/files/{fileId}
- "List all deployments?" -> GET /v6/deployments
- "Delete a deployment?" -> DELETE /v13/deployments/{id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
