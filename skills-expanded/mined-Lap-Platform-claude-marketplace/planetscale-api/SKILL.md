---
name: planetscale-api
description: "PlanetScale API skill. Use when working with PlanetScale for organizations, regions, user. Covers 148 endpoints."
version: 1.0.0
generator: lapsh
---

# PlanetScale API
API version: v1

## Auth
OAuth2

## Base URL
https://api.planetscale.com/v1

## Setup
1. Configure auth: OAuth2
2. GET /organizations -- verify access
3. POST /organizations/{organization}/databases -- create first databases

## Endpoints

148 endpoints across 3 groups. See references/api-spec.lap for full details.

### organizations
| Method | Path | Description |
|--------|------|-------------|
| GET | /organizations | List organizations |
| GET | /organizations/{organization} | Get an organization |
| PATCH | /organizations/{organization} | Update an organization |
| GET | /organizations/{organization}/audit-log | List audit logs |
| GET | /organizations/{organization}/cluster-size-skus | List available cluster sizes |
| GET | /organizations/{organization}/databases | List databases |
| POST | /organizations/{organization}/databases | Create a database |
| GET | /organizations/{organization}/databases/{database} | Get a database |
| PATCH | /organizations/{organization}/databases/{database} | Update database settings |
| DELETE | /organizations/{organization}/databases/{database} | Delete a database |
| GET | /organizations/{organization}/databases/{database}/branches | List branches |
| POST | /organizations/{organization}/databases/{database}/branches | Create a branch |
| GET | /organizations/{organization}/databases/{database}/branches/{branch} | Get a branch |
| PATCH | /organizations/{organization}/databases/{database}/branches/{branch} | Update a branch |
| DELETE | /organizations/{organization}/databases/{database}/branches/{branch} | Delete a branch |
| GET | /organizations/{organization}/databases/{database}/branches/{branch}/backups | List backups |
| POST | /organizations/{organization}/databases/{database}/branches/{branch}/backups | Create a backup |
| GET | /organizations/{organization}/databases/{database}/branches/{branch}/backups/{id} | Get a backup |
| PATCH | /organizations/{organization}/databases/{database}/branches/{branch}/backups/{id} | Update a backup |
| DELETE | /organizations/{organization}/databases/{database}/branches/{branch}/backups/{id} | Delete a backup |
| GET | /organizations/{organization}/databases/{database}/branches/{branch}/bouncer-resizes | Get bouncer resize requests |
| GET | /organizations/{organization}/databases/{database}/branches/{branch}/bouncers | List bouncers |
| POST | /organizations/{organization}/databases/{database}/branches/{branch}/bouncers | Create a bouncer |
| GET | /organizations/{organization}/databases/{database}/branches/{branch}/bouncers/{bouncer} | Get a bouncer |
| DELETE | /organizations/{organization}/databases/{database}/branches/{branch}/bouncers/{bouncer} | Delete a bouncer |
| GET | /organizations/{organization}/databases/{database}/branches/{branch}/bouncers/{bouncer}/resizes | Get bouncer resize requests |
| PATCH | /organizations/{organization}/databases/{database}/branches/{branch}/bouncers/{bouncer}/resizes | Upsert a bouncer resize request |
| DELETE | /organizations/{organization}/databases/{database}/branches/{branch}/bouncers/{bouncer}/resizes | Cancel a resize request |
| GET | /organizations/{organization}/databases/{database}/branches/{branch}/changes | Get branch change requests |
| PATCH | /organizations/{organization}/databases/{database}/branches/{branch}/changes | Upsert a change request |
| GET | /organizations/{organization}/databases/{database}/branches/{branch}/changes/{id} | Get a branch change request |
| PATCH | /organizations/{organization}/databases/{database}/branches/{branch}/cluster | Change a branch cluster configuration |
| POST | /organizations/{organization}/databases/{database}/branches/{branch}/demote | Demote a branch |
| GET | /organizations/{organization}/databases/{database}/branches/{branch}/extensions | List cluster extensions |
| GET | /organizations/{organization}/databases/{database}/branches/{branch}/keyspaces | Get keyspaces |
| POST | /organizations/{organization}/databases/{database}/branches/{branch}/keyspaces | Create a keyspace |
| GET | /organizations/{organization}/databases/{database}/branches/{branch}/keyspaces/{keyspace} | Get a keyspace |
| PATCH | /organizations/{organization}/databases/{database}/branches/{branch}/keyspaces/{keyspace} | Configure keyspace settings |
| DELETE | /organizations/{organization}/databases/{database}/branches/{branch}/keyspaces/{keyspace} | Delete a keyspace |
| GET | /organizations/{organization}/databases/{database}/branches/{branch}/keyspaces/{keyspace}/rollout-status | Get keyspace rollout status |
| GET | /organizations/{organization}/databases/{database}/branches/{branch}/keyspaces/{keyspace}/vschema | Get the VSchema for the keyspace |
| PATCH | /organizations/{organization}/databases/{database}/branches/{branch}/keyspaces/{keyspace}/vschema | Update the VSchema for the keyspace |
| GET | /organizations/{organization}/databases/{database}/branches/{branch}/parameters | List cluster parameters |
| GET | /organizations/{organization}/databases/{database}/branches/{branch}/passwords | List passwords |
| POST | /organizations/{organization}/databases/{database}/branches/{branch}/passwords | Create a password |
| GET | /organizations/{organization}/databases/{database}/branches/{branch}/passwords/{id} | Get a password |
| PATCH | /organizations/{organization}/databases/{database}/branches/{branch}/passwords/{id} | Update a password |
| DELETE | /organizations/{organization}/databases/{database}/branches/{branch}/passwords/{id} | Delete a password |
| POST | /organizations/{organization}/databases/{database}/branches/{branch}/passwords/{id}/renew | Renew a password |
| POST | /organizations/{organization}/databases/{database}/branches/{branch}/promote | Promote a branch |
| GET | /organizations/{organization}/databases/{database}/branches/{branch}/query-patterns | List generated query patterns reports |
| POST | /organizations/{organization}/databases/{database}/branches/{branch}/query-patterns | Create a new query patterns report |
| GET | /organizations/{organization}/databases/{database}/branches/{branch}/query-patterns/{id} | Show the status of a query patterns report |
| DELETE | /organizations/{organization}/databases/{database}/branches/{branch}/query-patterns/{id} | Delete a query patterns report |
| GET | /organizations/{organization}/databases/{database}/branches/{branch}/query-patterns/{id}/download | Download a finished query patterns report |
| DELETE | /organizations/{organization}/databases/{database}/branches/{branch}/resizes | Cancel a change request |
| GET | /organizations/{organization}/databases/{database}/branches/{branch}/roles | List roles |
| POST | /organizations/{organization}/databases/{database}/branches/{branch}/roles | Create role credentials |
| GET | /organizations/{organization}/databases/{database}/branches/{branch}/roles/default | Get the default postgres role |
| POST | /organizations/{organization}/databases/{database}/branches/{branch}/roles/reset-default | Reset default credentials |
| GET | /organizations/{organization}/databases/{database}/branches/{branch}/roles/{id} | Get a role |
| PATCH | /organizations/{organization}/databases/{database}/branches/{branch}/roles/{id} | Update role name |
| DELETE | /organizations/{organization}/databases/{database}/branches/{branch}/roles/{id} | Delete role credentials |
| POST | /organizations/{organization}/databases/{database}/branches/{branch}/roles/{id}/reassign | Reassign objects owned by one role to another role |
| POST | /organizations/{organization}/databases/{database}/branches/{branch}/roles/{id}/renew | Renew role expiration |
| POST | /organizations/{organization}/databases/{database}/branches/{branch}/roles/{id}/reset | Reset a role's password |
| POST | /organizations/{organization}/databases/{database}/branches/{branch}/safe-migrations | Enable safe migrations for a branch |
| DELETE | /organizations/{organization}/databases/{database}/branches/{branch}/safe-migrations | Disable safe migrations for a branch |
| GET | /organizations/{organization}/databases/{database}/branches/{branch}/schema | Get a branch schema |
| GET | /organizations/{organization}/databases/{database}/branches/{branch}/schema/lint | Lint a branch schema |
| GET | /organizations/{organization}/databases/{database}/cidrs | List IP restriction entries |
| POST | /organizations/{organization}/databases/{database}/cidrs | Create an IP restriction entry |
| GET | /organizations/{organization}/databases/{database}/cidrs/{id} | Get an IP restriction entry |
| PUT | /organizations/{organization}/databases/{database}/cidrs/{id} | Update an IP restriction entry |
| DELETE | /organizations/{organization}/databases/{database}/cidrs/{id} | Delete an IP restriction entry |
| GET | /organizations/{organization}/databases/{database}/deploy-queue | Get the deploy queue |
| GET | /organizations/{organization}/databases/{database}/deploy-requests | List deploy requests |
| POST | /organizations/{organization}/databases/{database}/deploy-requests | Create a deploy request |
| GET | /organizations/{organization}/databases/{database}/deploy-requests/{number} | Get a deploy request |
| PATCH | /organizations/{organization}/databases/{database}/deploy-requests/{number} | Close a deploy request |
| POST | /organizations/{organization}/databases/{database}/deploy-requests/{number}/apply-deploy | Complete a gated deploy request |
| PUT | /organizations/{organization}/databases/{database}/deploy-requests/{number}/auto-apply | Update auto-apply for deploy request |
| PUT | /organizations/{organization}/databases/{database}/deploy-requests/{number}/auto-delete-branch | Update auto-delete branch for deploy request |
| POST | /organizations/{organization}/databases/{database}/deploy-requests/{number}/cancel | Cancel a queued deploy request |
| POST | /organizations/{organization}/databases/{database}/deploy-requests/{number}/complete-deploy | Complete an errored deploy |
| POST | /organizations/{organization}/databases/{database}/deploy-requests/{number}/deploy | Queue a deploy request |
| GET | /organizations/{organization}/databases/{database}/deploy-requests/{number}/deployment | Get a deployment |
| GET | /organizations/{organization}/databases/{database}/deploy-requests/{number}/operations | List deploy operations |
| POST | /organizations/{organization}/databases/{database}/deploy-requests/{number}/revert | Complete a revert |
| GET | /organizations/{organization}/databases/{database}/deploy-requests/{number}/reviews | List deploy request reviews |
| POST | /organizations/{organization}/databases/{database}/deploy-requests/{number}/reviews | Review a deploy request |
| POST | /organizations/{organization}/databases/{database}/deploy-requests/{number}/skip-revert | Skip revert period |
| GET | /organizations/{organization}/databases/{database}/deploy-requests/{number}/throttler | Get deploy request throttler configurations |
| PATCH | /organizations/{organization}/databases/{database}/deploy-requests/{number}/throttler | Update deploy request throttler configurations |
| GET | /organizations/{organization}/databases/{database}/read-only-regions | List read-only regions |
| GET | /organizations/{organization}/databases/{database}/regions | List database regions |
| GET | /organizations/{organization}/databases/{database}/schema-recommendations | List schema recommendations |
| GET | /organizations/{organization}/databases/{database}/schema-recommendations/{number} | Get a schema recommendation |
| POST | /organizations/{organization}/databases/{database}/schema-recommendations/{number}/dismiss | Dismiss a schema recommendation |
| GET | /organizations/{organization}/databases/{database}/throttler | Get database throttler configurations |
| PATCH | /organizations/{organization}/databases/{database}/throttler | Update database throttler configurations |
| GET | /organizations/{organization}/databases/{database}/webhooks | List webhooks |
| POST | /organizations/{organization}/databases/{database}/webhooks | Create a webhook |
| GET | /organizations/{organization}/databases/{database}/webhooks/{id} | Get a webhook |
| PATCH | /organizations/{organization}/databases/{database}/webhooks/{id} | Update a webhook |
| DELETE | /organizations/{organization}/databases/{database}/webhooks/{id} | Delete a webhook |
| POST | /organizations/{organization}/databases/{database}/webhooks/{id}/test | Test a webhook |
| GET | /organizations/{organization}/databases/{database}/workflows | List workflows |
| POST | /organizations/{organization}/databases/{database}/workflows | Create a workflow |
| GET | /organizations/{organization}/databases/{database}/workflows/{number} | Get a workflow |
| DELETE | /organizations/{organization}/databases/{database}/workflows/{number} | Cancel a workflow |
| PATCH | /organizations/{organization}/databases/{database}/workflows/{number}/complete | Complete a workflow |
| PATCH | /organizations/{organization}/databases/{database}/workflows/{number}/cutover | Cutover traffic |
| PATCH | /organizations/{organization}/databases/{database}/workflows/{number}/retry | Retry a failed workflow |
| PATCH | /organizations/{organization}/databases/{database}/workflows/{number}/reverse-cutover | Reverse traffic cutover |
| PATCH | /organizations/{organization}/databases/{database}/workflows/{number}/reverse-traffic | Reverse traffic |
| PATCH | /organizations/{organization}/databases/{database}/workflows/{number}/switch-primaries | Switch primary traffic |
| PATCH | /organizations/{organization}/databases/{database}/workflows/{number}/switch-replicas | Switch replica traffic |
| PATCH | /organizations/{organization}/databases/{database}/workflows/{number}/verify-data | Verify workflow data |
| GET | /organizations/{organization}/invoices | Get invoices |
| GET | /organizations/{organization}/invoices/{id} | Get an invoice |
| GET | /organizations/{organization}/invoices/{id}/line-items | Get invoice line items |
| GET | /organizations/{organization}/members | List organization members |
| GET | /organizations/{organization}/members/{id} | Get an organization member |
| PATCH | /organizations/{organization}/members/{id} | Update organization member role |
| DELETE | /organizations/{organization}/members/{id} | Remove a member from an organization |
| GET | /organizations/{organization}/oauth-applications | List OAuth applications |
| GET | /organizations/{organization}/oauth-applications/{application_id} | Get an OAuth application |
| GET | /organizations/{organization}/oauth-applications/{application_id}/tokens | List OAuth tokens |
| GET | /organizations/{organization}/oauth-applications/{application_id}/tokens/{token_id} | Get an OAuth token |
| DELETE | /organizations/{organization}/oauth-applications/{application_id}/tokens/{token_id} | Delete an OAuth token |
| POST | /organizations/{organization}/oauth-applications/{id}/token | Create or renew an OAuth token |
| GET | /organizations/{organization}/regions | List regions for an organization |
| GET | /organizations/{organization}/service-tokens | List service tokens |
| POST | /organizations/{organization}/service-tokens | Create a service token |
| GET | /organizations/{organization}/service-tokens/{id} | Get a service token |
| DELETE | /organizations/{organization}/service-tokens/{id} | Delete a service token |
| GET | /organizations/{organization}/teams | List teams in an organization |
| POST | /organizations/{organization}/teams | Create an organization team |
| GET | /organizations/{organization}/teams/{team} | Get an organization team |
| PATCH | /organizations/{organization}/teams/{team} | Update an organization team |
| DELETE | /organizations/{organization}/teams/{team} | Delete an organization team |
| GET | /organizations/{organization}/teams/{team}/members | List team members |
| POST | /organizations/{organization}/teams/{team}/members | Add a member to a team |
| GET | /organizations/{organization}/teams/{team}/members/{id} | Get a team member |
| DELETE | /organizations/{organization}/teams/{team}/members/{id} | Remove a member from a team |

### regions
| Method | Path | Description |
|--------|------|-------------|
| GET | /regions | List public regions |

### user
| Method | Path | Description |
|--------|------|-------------|
| GET | /user | Get current user |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all organizations?" -> GET /organizations
- "Get organization details?" -> GET /organizations/{organization}
- "Partially update a organization?" -> PATCH /organizations/{organization}
- "List all audit-log?" -> GET /organizations/{organization}/audit-log
- "List all cluster-size-skus?" -> GET /organizations/{organization}/cluster-size-skus
- "Search databases?" -> GET /organizations/{organization}/databases
- "Create a database?" -> POST /organizations/{organization}/databases
- "Get database details?" -> GET /organizations/{organization}/databases/{database}
- "Partially update a database?" -> PATCH /organizations/{organization}/databases/{database}
- "Delete a database?" -> DELETE /organizations/{organization}/databases/{database}
- "Search branches?" -> GET /organizations/{organization}/databases/{database}/branches
- "Create a branche?" -> POST /organizations/{organization}/databases/{database}/branches
- "Get branche details?" -> GET /organizations/{organization}/databases/{database}/branches/{branch}
- "Partially update a branche?" -> PATCH /organizations/{organization}/databases/{database}/branches/{branch}
- "Delete a branche?" -> DELETE /organizations/{organization}/databases/{database}/branches/{branch}
- "List all backups?" -> GET /organizations/{organization}/databases/{database}/branches/{branch}/backups
- "Create a backup?" -> POST /organizations/{organization}/databases/{database}/branches/{branch}/backups
- "Get backup details?" -> GET /organizations/{organization}/databases/{database}/branches/{branch}/backups/{id}
- "Partially update a backup?" -> PATCH /organizations/{organization}/databases/{database}/branches/{branch}/backups/{id}
- "Delete a backup?" -> DELETE /organizations/{organization}/databases/{database}/branches/{branch}/backups/{id}
- "List all bouncer-resizes?" -> GET /organizations/{organization}/databases/{database}/branches/{branch}/bouncer-resizes
- "List all bouncers?" -> GET /organizations/{organization}/databases/{database}/branches/{branch}/bouncers
- "Create a bouncer?" -> POST /organizations/{organization}/databases/{database}/branches/{branch}/bouncers
- "Get bouncer details?" -> GET /organizations/{organization}/databases/{database}/branches/{branch}/bouncers/{bouncer}
- "Delete a bouncer?" -> DELETE /organizations/{organization}/databases/{database}/branches/{branch}/bouncers/{bouncer}
- "List all resizes?" -> GET /organizations/{organization}/databases/{database}/branches/{branch}/bouncers/{bouncer}/resizes
- "List all changes?" -> GET /organizations/{organization}/databases/{database}/branches/{branch}/changes
- "Get change details?" -> GET /organizations/{organization}/databases/{database}/branches/{branch}/changes/{id}
- "Create a demote?" -> POST /organizations/{organization}/databases/{database}/branches/{branch}/demote
- "List all extensions?" -> GET /organizations/{organization}/databases/{database}/branches/{branch}/extensions
- "List all keyspaces?" -> GET /organizations/{organization}/databases/{database}/branches/{branch}/keyspaces
- "Create a keyspace?" -> POST /organizations/{organization}/databases/{database}/branches/{branch}/keyspaces
- "Get keyspace details?" -> GET /organizations/{organization}/databases/{database}/branches/{branch}/keyspaces/{keyspace}
- "Partially update a keyspace?" -> PATCH /organizations/{organization}/databases/{database}/branches/{branch}/keyspaces/{keyspace}
- "Delete a keyspace?" -> DELETE /organizations/{organization}/databases/{database}/branches/{branch}/keyspaces/{keyspace}
- "List all rollout-status?" -> GET /organizations/{organization}/databases/{database}/branches/{branch}/keyspaces/{keyspace}/rollout-status
- "List all vschema?" -> GET /organizations/{organization}/databases/{database}/branches/{branch}/keyspaces/{keyspace}/vschema
- "List all parameters?" -> GET /organizations/{organization}/databases/{database}/branches/{branch}/parameters
- "List all passwords?" -> GET /organizations/{organization}/databases/{database}/branches/{branch}/passwords
- "Create a password?" -> POST /organizations/{organization}/databases/{database}/branches/{branch}/passwords
- "Get password details?" -> GET /organizations/{organization}/databases/{database}/branches/{branch}/passwords/{id}
- "Partially update a password?" -> PATCH /organizations/{organization}/databases/{database}/branches/{branch}/passwords/{id}
- "Delete a password?" -> DELETE /organizations/{organization}/databases/{database}/branches/{branch}/passwords/{id}
- "Create a renew?" -> POST /organizations/{organization}/databases/{database}/branches/{branch}/passwords/{id}/renew
- "Create a promote?" -> POST /organizations/{organization}/databases/{database}/branches/{branch}/promote
- "List all query-patterns?" -> GET /organizations/{organization}/databases/{database}/branches/{branch}/query-patterns
- "Create a query-pattern?" -> POST /organizations/{organization}/databases/{database}/branches/{branch}/query-patterns
- "Get query-pattern details?" -> GET /organizations/{organization}/databases/{database}/branches/{branch}/query-patterns/{id}
- "Delete a query-pattern?" -> DELETE /organizations/{organization}/databases/{database}/branches/{branch}/query-patterns/{id}
- "List all download?" -> GET /organizations/{organization}/databases/{database}/branches/{branch}/query-patterns/{id}/download
- "List all roles?" -> GET /organizations/{organization}/databases/{database}/branches/{branch}/roles
- "Create a role?" -> POST /organizations/{organization}/databases/{database}/branches/{branch}/roles
- "List all default?" -> GET /organizations/{organization}/databases/{database}/branches/{branch}/roles/default
- "Create a reset-default?" -> POST /organizations/{organization}/databases/{database}/branches/{branch}/roles/reset-default
- "Get role details?" -> GET /organizations/{organization}/databases/{database}/branches/{branch}/roles/{id}
- "Partially update a role?" -> PATCH /organizations/{organization}/databases/{database}/branches/{branch}/roles/{id}
- "Delete a role?" -> DELETE /organizations/{organization}/databases/{database}/branches/{branch}/roles/{id}
- "Create a reassign?" -> POST /organizations/{organization}/databases/{database}/branches/{branch}/roles/{id}/reassign
- "Create a renew?" -> POST /organizations/{organization}/databases/{database}/branches/{branch}/roles/{id}/renew
- "Create a reset?" -> POST /organizations/{organization}/databases/{database}/branches/{branch}/roles/{id}/reset
- "Create a safe-migration?" -> POST /organizations/{organization}/databases/{database}/branches/{branch}/safe-migrations
- "List all schema?" -> GET /organizations/{organization}/databases/{database}/branches/{branch}/schema
- "List all lint?" -> GET /organizations/{organization}/databases/{database}/branches/{branch}/schema/lint
- "List all cidrs?" -> GET /organizations/{organization}/databases/{database}/cidrs
- "Create a cidr?" -> POST /organizations/{organization}/databases/{database}/cidrs
- "Get cidr details?" -> GET /organizations/{organization}/databases/{database}/cidrs/{id}
- "Update a cidr?" -> PUT /organizations/{organization}/databases/{database}/cidrs/{id}
- "Delete a cidr?" -> DELETE /organizations/{organization}/databases/{database}/cidrs/{id}
- "List all deploy-queue?" -> GET /organizations/{organization}/databases/{database}/deploy-queue
- "List all deploy-requests?" -> GET /organizations/{organization}/databases/{database}/deploy-requests
- "Create a deploy-request?" -> POST /organizations/{organization}/databases/{database}/deploy-requests
- "Get deploy-request details?" -> GET /organizations/{organization}/databases/{database}/deploy-requests/{number}
- "Partially update a deploy-request?" -> PATCH /organizations/{organization}/databases/{database}/deploy-requests/{number}
- "Create a apply-deploy?" -> POST /organizations/{organization}/databases/{database}/deploy-requests/{number}/apply-deploy
- "Create a cancel?" -> POST /organizations/{organization}/databases/{database}/deploy-requests/{number}/cancel
- "Create a complete-deploy?" -> POST /organizations/{organization}/databases/{database}/deploy-requests/{number}/complete-deploy
- "Create a deploy?" -> POST /organizations/{organization}/databases/{database}/deploy-requests/{number}/deploy
- "List all deployment?" -> GET /organizations/{organization}/databases/{database}/deploy-requests/{number}/deployment
- "List all operations?" -> GET /organizations/{organization}/databases/{database}/deploy-requests/{number}/operations
- "Create a revert?" -> POST /organizations/{organization}/databases/{database}/deploy-requests/{number}/revert
- "List all reviews?" -> GET /organizations/{organization}/databases/{database}/deploy-requests/{number}/reviews
- "Create a review?" -> POST /organizations/{organization}/databases/{database}/deploy-requests/{number}/reviews
- "Create a skip-revert?" -> POST /organizations/{organization}/databases/{database}/deploy-requests/{number}/skip-revert
- "List all throttler?" -> GET /organizations/{organization}/databases/{database}/deploy-requests/{number}/throttler
- "List all read-only-regions?" -> GET /organizations/{organization}/databases/{database}/read-only-regions
- "List all regions?" -> GET /organizations/{organization}/databases/{database}/regions
- "List all schema-recommendations?" -> GET /organizations/{organization}/databases/{database}/schema-recommendations
- "Get schema-recommendation details?" -> GET /organizations/{organization}/databases/{database}/schema-recommendations/{number}
- "Create a dismiss?" -> POST /organizations/{organization}/databases/{database}/schema-recommendations/{number}/dismiss
- "List all throttler?" -> GET /organizations/{organization}/databases/{database}/throttler
- "List all webhooks?" -> GET /organizations/{organization}/databases/{database}/webhooks
- "Create a webhook?" -> POST /organizations/{organization}/databases/{database}/webhooks
- "Get webhook details?" -> GET /organizations/{organization}/databases/{database}/webhooks/{id}
- "Partially update a webhook?" -> PATCH /organizations/{organization}/databases/{database}/webhooks/{id}
- "Delete a webhook?" -> DELETE /organizations/{organization}/databases/{database}/webhooks/{id}
- "Create a test?" -> POST /organizations/{organization}/databases/{database}/webhooks/{id}/test
- "List all workflows?" -> GET /organizations/{organization}/databases/{database}/workflows
- "Create a workflow?" -> POST /organizations/{organization}/databases/{database}/workflows
- "Get workflow details?" -> GET /organizations/{organization}/databases/{database}/workflows/{number}
- "Delete a workflow?" -> DELETE /organizations/{organization}/databases/{database}/workflows/{number}
- "List all invoices?" -> GET /organizations/{organization}/invoices
- "Get invoice details?" -> GET /organizations/{organization}/invoices/{id}
- "List all line-items?" -> GET /organizations/{organization}/invoices/{id}/line-items
- "Search members?" -> GET /organizations/{organization}/members
- "Get member details?" -> GET /organizations/{organization}/members/{id}
- "Partially update a member?" -> PATCH /organizations/{organization}/members/{id}
- "Delete a member?" -> DELETE /organizations/{organization}/members/{id}
- "List all oauth-applications?" -> GET /organizations/{organization}/oauth-applications
- "Get oauth-application details?" -> GET /organizations/{organization}/oauth-applications/{application_id}
- "List all tokens?" -> GET /organizations/{organization}/oauth-applications/{application_id}/tokens
- "Get token details?" -> GET /organizations/{organization}/oauth-applications/{application_id}/tokens/{token_id}
- "Delete a token?" -> DELETE /organizations/{organization}/oauth-applications/{application_id}/tokens/{token_id}
- "Create a token?" -> POST /organizations/{organization}/oauth-applications/{id}/token
- "List all regions?" -> GET /organizations/{organization}/regions
- "List all service-tokens?" -> GET /organizations/{organization}/service-tokens
- "Create a service-token?" -> POST /organizations/{organization}/service-tokens
- "Get service-token details?" -> GET /organizations/{organization}/service-tokens/{id}
- "Delete a service-token?" -> DELETE /organizations/{organization}/service-tokens/{id}
- "Search teams?" -> GET /organizations/{organization}/teams
- "Create a team?" -> POST /organizations/{organization}/teams
- "Get team details?" -> GET /organizations/{organization}/teams/{team}
- "Partially update a team?" -> PATCH /organizations/{organization}/teams/{team}
- "Delete a team?" -> DELETE /organizations/{organization}/teams/{team}
- "List all members?" -> GET /organizations/{organization}/teams/{team}/members
- "Create a member?" -> POST /organizations/{organization}/teams/{team}/members
- "Get member details?" -> GET /organizations/{organization}/teams/{team}/members/{id}
- "Delete a member?" -> DELETE /organizations/{organization}/teams/{team}/members/{id}
- "List all regions?" -> GET /regions
- "List all user?" -> GET /user
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
