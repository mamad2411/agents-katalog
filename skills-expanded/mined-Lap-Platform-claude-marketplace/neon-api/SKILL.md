---
name: neon-api
description: "Neon API skill. Use when working with Neon for projects, api_keys, consumption_history. Covers 138 endpoints."
version: 1.0.0
generator: lapsh
---

# Neon API
API version: v2

## Auth
Bearer bearer | ApiKey zenith in cookie | ApiKey keycloak_token in cookie

## Base URL
https://console.neon.tech/api/v2

## Setup
1. Set Authorization header with your Bearer token
2. GET /api_keys -- verify access
3. POST /api_keys -- create first api_keys

## Endpoints

138 endpoints across 7 groups. See references/api-spec.lap for full details.

### projects
| Method | Path | Description |
|--------|------|-------------|
| GET | /projects/{project_id}/advisors | Get advisor issues |
| GET | /projects/{project_id}/operations/{operation_id} | Retrieve operation details |
| GET | /projects | List projects |
| POST | /projects | Create project |
| GET | /projects/shared | List shared projects |
| GET | /projects/{project_id} | Retrieve project details |
| PATCH | /projects/{project_id} | Update project |
| DELETE | /projects/{project_id} | Delete project |
| POST | /projects/{project_id}/restore | Restore a deleted project |
| POST | /projects/{project_id}/recover | Recover a deleted project |
| GET | /projects/{project_id}/operations | List operations |
| GET | /projects/{project_id}/permissions | List project access |
| POST | /projects/{project_id}/permissions | Grant project access |
| DELETE | /projects/{project_id}/permissions/{permission_id} | Revoke project access |
| GET | /projects/{project_id}/available_preload_libraries | Return available shared preload libraries |
| POST | /projects/{project_id}/transfer_requests | Create a project transfer request |
| PUT | /projects/{project_id}/transfer_requests/{request_id} | Accept a project transfer request |
| GET | /projects/{project_id}/jwks | List JWKS URLs |
| POST | /projects/{project_id}/jwks | Add JWKS URL |
| DELETE | /projects/{project_id}/jwks/{jwks_id} | Delete JWKS URL |
| POST | /projects/{project_id}/branches/{branch_id}/data-api/{database_name} | Create Neon Data API |
| PATCH | /projects/{project_id}/branches/{branch_id}/data-api/{database_name} | Update Neon Data API |
| DELETE | /projects/{project_id}/branches/{branch_id}/data-api/{database_name} | Delete Neon Data API |
| GET | /projects/{project_id}/branches/{branch_id}/data-api/{database_name} | Get Neon Data API |
| POST | /projects/auth/create | Create Neon Auth integration |
| GET | /projects/{project_id}/branches/{branch_id}/auth | Get details of Neon Auth for the branch |
| POST | /projects/{project_id}/branches/{branch_id}/auth | Enable Neon Auth for the branch |
| DELETE | /projects/{project_id}/branches/{branch_id}/auth | Disables Neon Auth for the branch |
| GET | /projects/{project_id}/auth/domains | List domains in redirect_uri whitelist |
| POST | /projects/{project_id}/auth/domains | Add domain to redirect_uri whitelist |
| DELETE | /projects/{project_id}/auth/domains | Delete domain from redirect_uri whitelist |
| GET | /projects/{project_id}/branches/{branch_id}/auth/domains | List domains in redirect_uri whitelist |
| POST | /projects/{project_id}/branches/{branch_id}/auth/domains | Add domain to redirect_uri whitelist |
| DELETE | /projects/{project_id}/branches/{branch_id}/auth/domains | Delete domain from redirect_uri whitelist |
| POST | /projects/auth/keys | Create Auth Provider SDK keys |
| POST | /projects/auth/user | Create new auth user |
| POST | /projects/{project_id}/branches/{branch_id}/auth/users | Create new auth user |
| DELETE | /projects/{project_id}/branches/{branch_id}/auth/users/{auth_user_id} | Delete auth user |
| PUT | /projects/{project_id}/branches/{branch_id}/auth/users/{auth_user_id}/role | Update auth user role |
| DELETE | /projects/{project_id}/auth/users/{auth_user_id} | Delete auth user |
| POST | /projects/auth/transfer_ownership | Transfer Neon-managed auth project to your own account |
| GET | /projects/{project_id}/auth/integrations | Lists active integrations with auth providers |
| GET | /projects/{project_id}/auth/oauth_providers | List OAuth providers |
| POST | /projects/{project_id}/auth/oauth_providers | Add a OAuth provider |
| GET | /projects/{project_id}/branches/{branch_id}/auth/oauth_providers | List OAuth providers for neon auth for a branch |
| POST | /projects/{project_id}/branches/{branch_id}/auth/oauth_providers | Add a OAuth provider |
| PATCH | /projects/{project_id}/auth/oauth_providers/{oauth_provider_id} | Update OAuth provider |
| DELETE | /projects/{project_id}/auth/oauth_providers/{oauth_provider_id} | Delete OAuth provider |
| PATCH | /projects/{project_id}/branches/{branch_id}/auth/oauth_providers/{oauth_provider_id} | Update OAuth provider |
| DELETE | /projects/{project_id}/branches/{branch_id}/auth/oauth_providers/{oauth_provider_id} | Delete OAuth provider |
| GET | /projects/{project_id}/auth/email_server | Get email server configuration |
| PATCH | /projects/{project_id}/auth/email_server | Update email server configuration |
| POST | /projects/{project_id}/branches/{branch_id}/auth/send_test_email | Send test email |
| GET | /projects/{project_id}/branches/{branch_id}/auth/email_and_password | Get email and password configuration |
| PATCH | /projects/{project_id}/branches/{branch_id}/auth/email_and_password | Update email and password configuration |
| GET | /projects/{project_id}/branches/{branch_id}/auth/email_provider | Get email provider configuration |
| PATCH | /projects/{project_id}/branches/{branch_id}/auth/email_provider | Update email provider configuration |
| DELETE | /projects/{project_id}/auth/integration/{auth_provider} | Delete integration with auth provider |
| GET | /projects/{project_id}/connection_uri | Retrieve connection URI |
| GET | /projects/{project_id}/branches/{branch_id}/auth/allow_localhost | Get allow localhost |
| PATCH | /projects/{project_id}/branches/{branch_id}/auth/allow_localhost | Update allow localhost |
| GET | /projects/{project_id}/branches/{branch_id}/auth/plugins | Get all plugin configurations |
| PATCH | /projects/{project_id}/branches/{branch_id}/auth/plugins/organization | Update organization plugin configuration |
| GET | /projects/{project_id}/branches/{branch_id}/auth/webhooks | Get webhook configuration for Neon Auth |
| PUT | /projects/{project_id}/branches/{branch_id}/auth/webhooks | Update webhook configuration for Neon Auth |
| POST | /projects/{project_id}/branches | Create branch |
| GET | /projects/{project_id}/branches | List branches |
| POST | /projects/{project_id}/branch_anonymized | Create anonymized branch |
| GET | /projects/{project_id}/branches/count | Retrieve number of branches |
| GET | /projects/{project_id}/branches/{branch_id} | Retrieve branch details |
| DELETE | /projects/{project_id}/branches/{branch_id} | Delete branch |
| PATCH | /projects/{project_id}/branches/{branch_id} | Update branch |
| POST | /projects/{project_id}/branches/{branch_id}/restore | Restore branch |
| GET | /projects/{project_id}/branches/{branch_id}/schema | Retrieve database schema |
| GET | /projects/{project_id}/branches/{branch_id}/compare_schema | Compare database schema |
| GET | /projects/{project_id}/branches/{branch_id}/masking_rules | Get masking rules |
| PATCH | /projects/{project_id}/branches/{branch_id}/masking_rules | Update masking rules |
| GET | /projects/{project_id}/branches/{branch_id}/anonymized_status | Get anonymized branch status |
| POST | /projects/{project_id}/branches/{branch_id}/anonymize | Start anonymization |
| POST | /projects/{project_id}/branches/{branch_id}/set_as_default | Set branch as default |
| POST | /projects/{project_id}/branches/{branch_id}/finalize_restore | Finalize restore |
| GET | /projects/{project_id}/branches/{branch_id}/endpoints | List branch endpoints |
| GET | /projects/{project_id}/branches/{branch_id}/databases | List databases |
| POST | /projects/{project_id}/branches/{branch_id}/databases | Create database |
| GET | /projects/{project_id}/branches/{branch_id}/databases/{database_name} | Retrieve database details |
| PATCH | /projects/{project_id}/branches/{branch_id}/databases/{database_name} | Update database |
| DELETE | /projects/{project_id}/branches/{branch_id}/databases/{database_name} | Delete database |
| GET | /projects/{project_id}/branches/{branch_id}/roles | List roles |
| POST | /projects/{project_id}/branches/{branch_id}/roles | Create role |
| GET | /projects/{project_id}/branches/{branch_id}/roles/{role_name} | Retrieve role details |
| DELETE | /projects/{project_id}/branches/{branch_id}/roles/{role_name} | Delete role |
| GET | /projects/{project_id}/branches/{branch_id}/roles/{role_name}/reveal_password | Retrieve role password |
| POST | /projects/{project_id}/branches/{branch_id}/roles/{role_name}/reset_password | Reset role password |
| GET | /projects/{project_id}/vpc_endpoints | List VPC endpoint restrictions |
| POST | /projects/{project_id}/vpc_endpoints/{vpc_endpoint_id} | Set VPC endpoint restriction |
| DELETE | /projects/{project_id}/vpc_endpoints/{vpc_endpoint_id} | Delete VPC endpoint restriction |
| POST | /projects/{project_id}/endpoints | Create compute endpoint |
| GET | /projects/{project_id}/endpoints | List compute endpoints |
| GET | /projects/{project_id}/endpoints/{endpoint_id} | Retrieve compute endpoint details |
| DELETE | /projects/{project_id}/endpoints/{endpoint_id} | Delete compute endpoint |
| PATCH | /projects/{project_id}/endpoints/{endpoint_id} | Update compute endpoint |
| POST | /projects/{project_id}/endpoints/{endpoint_id}/start | Start compute endpoint |
| POST | /projects/{project_id}/endpoints/{endpoint_id}/suspend | Suspend compute endpoint |
| POST | /projects/{project_id}/endpoints/{endpoint_id}/restart | Restart compute endpoint |
| POST | /projects/{project_id}/branches/{branch_id}/snapshot | Create snapshot |
| GET | /projects/{project_id}/snapshots | List project snapshots |
| DELETE | /projects/{project_id}/snapshots/{snapshot_id} | Delete snapshot |
| PATCH | /projects/{project_id}/snapshots/{snapshot_id} | Update snapshot |
| POST | /projects/{project_id}/snapshots/{snapshot_id}/restore | Restore snapshot |
| GET | /projects/{project_id}/branches/{branch_id}/backup_schedule | View backup schedule |
| PUT | /projects/{project_id}/branches/{branch_id}/backup_schedule | Update backup schedule |

### api_keys
| Method | Path | Description |
|--------|------|-------------|
| GET | /api_keys | List API keys |
| POST | /api_keys | Create API key |
| DELETE | /api_keys/{key_id} | Revoke API key |

### consumption_history
| Method | Path | Description |
|--------|------|-------------|
| GET | /consumption_history/account | Retrieve account consumption metrics (legacy plans) |
| GET | /consumption_history/projects | Retrieve project consumption metrics (legacy plans) |
| GET | /consumption_history/v2/projects | Retrieve project consumption metrics |

### organizations
| Method | Path | Description |
|--------|------|-------------|
| GET | /organizations/{org_id} | Retrieve organization details |
| GET | /organizations/{org_id}/api_keys | List organization API keys |
| POST | /organizations/{org_id}/api_keys | Create organization API key |
| DELETE | /organizations/{org_id}/api_keys/{key_id} | Revoke organization API key |
| GET | /organizations/{org_id}/members | Retrieve organization members details |
| GET | /organizations/{org_id}/members/{member_id} | Retrieve organization member details |
| PATCH | /organizations/{org_id}/members/{member_id} | Update role for organization member |
| DELETE | /organizations/{org_id}/members/{member_id} | Remove member from the organization |
| GET | /organizations/{org_id}/invitations | Retrieve organization invitation details |
| POST | /organizations/{org_id}/invitations | Create organization invitations |
| POST | /organizations/{source_org_id}/projects/transfer | Transfer projects between organizations |
| GET | /organizations/{org_id}/vpc/vpc_endpoints | List VPC endpoints across all regions |
| GET | /organizations/{org_id}/vpc/region/{region_id}/vpc_endpoints | List VPC endpoints |
| GET | /organizations/{org_id}/vpc/region/{region_id}/vpc_endpoints/{vpc_endpoint_id} | Retrieve VPC endpoint details |
| POST | /organizations/{org_id}/vpc/region/{region_id}/vpc_endpoints/{vpc_endpoint_id} | Assign or update VPC endpoint |
| DELETE | /organizations/{org_id}/vpc/region/{region_id}/vpc_endpoints/{vpc_endpoint_id} | Delete VPC endpoint |

### regions
| Method | Path | Description |
|--------|------|-------------|
| GET | /regions | List supported regions |

### users
| Method | Path | Description |
|--------|------|-------------|
| GET | /users/me | Retrieve current user details |
| GET | /users/me/organizations | Retrieve current user organizations list |
| POST | /users/me/projects/transfer | Transfer projects from personal account to organization |

### auth
| Method | Path | Description |
|--------|------|-------------|
| GET | /auth | Get request authentication details |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all advisors?" -> GET /projects/{project_id}/advisors
- "List all api_keys?" -> GET /api_keys
- "Create a api_key?" -> POST /api_keys
- "Delete a api_key?" -> DELETE /api_keys/{key_id}
- "Get operation details?" -> GET /projects/{project_id}/operations/{operation_id}
- "Search projects?" -> GET /projects
- "Create a project?" -> POST /projects
- "Search shared?" -> GET /projects/shared
- "Get project details?" -> GET /projects/{project_id}
- "Partially update a project?" -> PATCH /projects/{project_id}
- "Delete a project?" -> DELETE /projects/{project_id}
- "Create a restore?" -> POST /projects/{project_id}/restore
- "Create a recover?" -> POST /projects/{project_id}/recover
- "List all operations?" -> GET /projects/{project_id}/operations
- "List all permissions?" -> GET /projects/{project_id}/permissions
- "Create a permission?" -> POST /projects/{project_id}/permissions
- "Delete a permission?" -> DELETE /projects/{project_id}/permissions/{permission_id}
- "List all available_preload_libraries?" -> GET /projects/{project_id}/available_preload_libraries
- "Create a transfer_request?" -> POST /projects/{project_id}/transfer_requests
- "Update a transfer_request?" -> PUT /projects/{project_id}/transfer_requests/{request_id}
- "List all jwks?" -> GET /projects/{project_id}/jwks
- "Create a jwk?" -> POST /projects/{project_id}/jwks
- "Delete a jwk?" -> DELETE /projects/{project_id}/jwks/{jwks_id}
- "Partially update a data-api?" -> PATCH /projects/{project_id}/branches/{branch_id}/data-api/{database_name}
- "Delete a data-api?" -> DELETE /projects/{project_id}/branches/{branch_id}/data-api/{database_name}
- "Get data-api details?" -> GET /projects/{project_id}/branches/{branch_id}/data-api/{database_name}
- "Create a create?" -> POST /projects/auth/create
- "List all auth?" -> GET /projects/{project_id}/branches/{branch_id}/auth
- "Create a auth?" -> POST /projects/{project_id}/branches/{branch_id}/auth
- "List all domains?" -> GET /projects/{project_id}/auth/domains
- "Create a domain?" -> POST /projects/{project_id}/auth/domains
- "List all domains?" -> GET /projects/{project_id}/branches/{branch_id}/auth/domains
- "Create a domain?" -> POST /projects/{project_id}/branches/{branch_id}/auth/domains
- "Create a key?" -> POST /projects/auth/keys
- "Create a user?" -> POST /projects/auth/user
- "Create a user?" -> POST /projects/{project_id}/branches/{branch_id}/auth/users
- "Delete a user?" -> DELETE /projects/{project_id}/branches/{branch_id}/auth/users/{auth_user_id}
- "Delete a user?" -> DELETE /projects/{project_id}/auth/users/{auth_user_id}
- "Create a transfer_ownership?" -> POST /projects/auth/transfer_ownership
- "List all integrations?" -> GET /projects/{project_id}/auth/integrations
- "List all oauth_providers?" -> GET /projects/{project_id}/auth/oauth_providers
- "Create a oauth_provider?" -> POST /projects/{project_id}/auth/oauth_providers
- "List all oauth_providers?" -> GET /projects/{project_id}/branches/{branch_id}/auth/oauth_providers
- "Create a oauth_provider?" -> POST /projects/{project_id}/branches/{branch_id}/auth/oauth_providers
- "Partially update a oauth_provider?" -> PATCH /projects/{project_id}/auth/oauth_providers/{oauth_provider_id}
- "Delete a oauth_provider?" -> DELETE /projects/{project_id}/auth/oauth_providers/{oauth_provider_id}
- "Partially update a oauth_provider?" -> PATCH /projects/{project_id}/branches/{branch_id}/auth/oauth_providers/{oauth_provider_id}
- "Delete a oauth_provider?" -> DELETE /projects/{project_id}/branches/{branch_id}/auth/oauth_providers/{oauth_provider_id}
- "List all email_server?" -> GET /projects/{project_id}/auth/email_server
- "Create a send_test_email?" -> POST /projects/{project_id}/branches/{branch_id}/auth/send_test_email
- "List all email_and_password?" -> GET /projects/{project_id}/branches/{branch_id}/auth/email_and_password
- "List all email_provider?" -> GET /projects/{project_id}/branches/{branch_id}/auth/email_provider
- "Delete a integration?" -> DELETE /projects/{project_id}/auth/integration/{auth_provider}
- "List all connection_uri?" -> GET /projects/{project_id}/connection_uri
- "List all allow_localhost?" -> GET /projects/{project_id}/branches/{branch_id}/auth/allow_localhost
- "List all plugins?" -> GET /projects/{project_id}/branches/{branch_id}/auth/plugins
- "List all webhooks?" -> GET /projects/{project_id}/branches/{branch_id}/auth/webhooks
- "Create a branche?" -> POST /projects/{project_id}/branches
- "Search branches?" -> GET /projects/{project_id}/branches
- "Create a branch_anonymized?" -> POST /projects/{project_id}/branch_anonymized
- "Search count?" -> GET /projects/{project_id}/branches/count
- "Get branche details?" -> GET /projects/{project_id}/branches/{branch_id}
- "Delete a branche?" -> DELETE /projects/{project_id}/branches/{branch_id}
- "Partially update a branche?" -> PATCH /projects/{project_id}/branches/{branch_id}
- "Create a restore?" -> POST /projects/{project_id}/branches/{branch_id}/restore
- "List all schema?" -> GET /projects/{project_id}/branches/{branch_id}/schema
- "List all compare_schema?" -> GET /projects/{project_id}/branches/{branch_id}/compare_schema
- "List all masking_rules?" -> GET /projects/{project_id}/branches/{branch_id}/masking_rules
- "List all anonymized_status?" -> GET /projects/{project_id}/branches/{branch_id}/anonymized_status
- "Create a anonymize?" -> POST /projects/{project_id}/branches/{branch_id}/anonymize
- "Create a set_as_default?" -> POST /projects/{project_id}/branches/{branch_id}/set_as_default
- "Create a finalize_restore?" -> POST /projects/{project_id}/branches/{branch_id}/finalize_restore
- "List all endpoints?" -> GET /projects/{project_id}/branches/{branch_id}/endpoints
- "List all databases?" -> GET /projects/{project_id}/branches/{branch_id}/databases
- "Create a database?" -> POST /projects/{project_id}/branches/{branch_id}/databases
- "Get database details?" -> GET /projects/{project_id}/branches/{branch_id}/databases/{database_name}
- "Partially update a database?" -> PATCH /projects/{project_id}/branches/{branch_id}/databases/{database_name}
- "Delete a database?" -> DELETE /projects/{project_id}/branches/{branch_id}/databases/{database_name}
- "List all roles?" -> GET /projects/{project_id}/branches/{branch_id}/roles
- "Create a role?" -> POST /projects/{project_id}/branches/{branch_id}/roles
- "Get role details?" -> GET /projects/{project_id}/branches/{branch_id}/roles/{role_name}
- "Delete a role?" -> DELETE /projects/{project_id}/branches/{branch_id}/roles/{role_name}
- "List all reveal_password?" -> GET /projects/{project_id}/branches/{branch_id}/roles/{role_name}/reveal_password
- "Create a reset_password?" -> POST /projects/{project_id}/branches/{branch_id}/roles/{role_name}/reset_password
- "List all vpc_endpoints?" -> GET /projects/{project_id}/vpc_endpoints
- "Delete a vpc_endpoint?" -> DELETE /projects/{project_id}/vpc_endpoints/{vpc_endpoint_id}
- "Create a endpoint?" -> POST /projects/{project_id}/endpoints
- "List all endpoints?" -> GET /projects/{project_id}/endpoints
- "Get endpoint details?" -> GET /projects/{project_id}/endpoints/{endpoint_id}
- "Delete a endpoint?" -> DELETE /projects/{project_id}/endpoints/{endpoint_id}
- "Partially update a endpoint?" -> PATCH /projects/{project_id}/endpoints/{endpoint_id}
- "Create a start?" -> POST /projects/{project_id}/endpoints/{endpoint_id}/start
- "Create a suspend?" -> POST /projects/{project_id}/endpoints/{endpoint_id}/suspend
- "Create a restart?" -> POST /projects/{project_id}/endpoints/{endpoint_id}/restart
- "List all account?" -> GET /consumption_history/account
- "List all projects?" -> GET /consumption_history/projects
- "List all projects?" -> GET /consumption_history/v2/projects
- "Get organization details?" -> GET /organizations/{org_id}
- "List all api_keys?" -> GET /organizations/{org_id}/api_keys
- "Create a api_key?" -> POST /organizations/{org_id}/api_keys
- "Delete a api_key?" -> DELETE /organizations/{org_id}/api_keys/{key_id}
- "List all members?" -> GET /organizations/{org_id}/members
- "Get member details?" -> GET /organizations/{org_id}/members/{member_id}
- "Partially update a member?" -> PATCH /organizations/{org_id}/members/{member_id}
- "Delete a member?" -> DELETE /organizations/{org_id}/members/{member_id}
- "List all invitations?" -> GET /organizations/{org_id}/invitations
- "Create a invitation?" -> POST /organizations/{org_id}/invitations
- "Create a transfer?" -> POST /organizations/{source_org_id}/projects/transfer
- "List all vpc_endpoints?" -> GET /organizations/{org_id}/vpc/vpc_endpoints
- "List all vpc_endpoints?" -> GET /organizations/{org_id}/vpc/region/{region_id}/vpc_endpoints
- "Get vpc_endpoint details?" -> GET /organizations/{org_id}/vpc/region/{region_id}/vpc_endpoints/{vpc_endpoint_id}
- "Delete a vpc_endpoint?" -> DELETE /organizations/{org_id}/vpc/region/{region_id}/vpc_endpoints/{vpc_endpoint_id}
- "List all regions?" -> GET /regions
- "List all me?" -> GET /users/me
- "List all organizations?" -> GET /users/me/organizations
- "Create a transfer?" -> POST /users/me/projects/transfer
- "List all auth?" -> GET /auth
- "Create a snapshot?" -> POST /projects/{project_id}/branches/{branch_id}/snapshot
- "List all snapshots?" -> GET /projects/{project_id}/snapshots
- "Delete a snapshot?" -> DELETE /projects/{project_id}/snapshots/{snapshot_id}
- "Partially update a snapshot?" -> PATCH /projects/{project_id}/snapshots/{snapshot_id}
- "Create a restore?" -> POST /projects/{project_id}/snapshots/{snapshot_id}/restore
- "List all backup_schedule?" -> GET /projects/{project_id}/branches/{branch_id}/backup_schedule
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
