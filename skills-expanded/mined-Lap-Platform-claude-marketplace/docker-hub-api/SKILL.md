---
name: docker-hub-api
description: "Docker HUB API skill. Use when working with Docker HUB for users, auth, access-tokens. Covers 54 endpoints."
version: 1.0.0
generator: lapsh
---

# Docker HUB API
API version: 2-beta

## Auth
Bearer bearer | Bearer bearer

## Base URL
https://hub.docker.com

## Setup
1. Set Authorization header with your Bearer token
2. GET /v2/access-tokens -- verify access
3. POST /v2/users/login -- create first login

## Endpoints

54 endpoints across 9 groups. See references/api-spec.lap for full details.

### users
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/users/login | Create an authentication token |
| POST | /v2/users/2fa-login | Second factor authentication |

### auth
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/auth/token | Create access token |

### access-tokens
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/access-tokens | Create personal access token |
| GET | /v2/access-tokens | List personal access tokens |
| PATCH | /v2/access-tokens/{uuid} | Update personal access token |
| GET | /v2/access-tokens/{uuid} | Get personal access token |
| DELETE | /v2/access-tokens/{uuid} | Delete personal access token |

### auditlogs
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/auditlogs/{account}/actions | List audit log actions |
| GET | /v2/auditlogs/{account} | List audit log events |

### orgs
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/orgs/{name}/settings | Get organization settings |
| PUT | /v2/orgs/{name}/settings | Update organization settings |
| POST | /v2/orgs/{name}/access-tokens | Create access token |
| GET | /v2/orgs/{name}/access-tokens | List access tokens |
| GET | /v2/orgs/{org_name}/access-tokens/{access_token_id} | Get access token |
| PATCH | /v2/orgs/{org_name}/access-tokens/{access_token_id} | Update access token |
| DELETE | /v2/orgs/{org_name}/access-tokens/{access_token_id} | Delete access token |
| GET | /v2/orgs/{org_name}/members | List org members |
| GET | /v2/orgs/{org_name}/members/export | Export org members CSV |
| PUT | /v2/orgs/{org_name}/members/{username} | Update org member (role) |
| DELETE | /v2/orgs/{org_name}/members/{username} | Remove member from org |
| GET | /v2/orgs/{org_name}/invites | List org invites |
| GET | /v2/orgs/{org_name}/groups | Get groups of an organization |
| POST | /v2/orgs/{org_name}/groups | Create a new group |
| GET | /v2/orgs/{org_name}/groups/{group_name} | Get a group of an organization |
| PUT | /v2/orgs/{org_name}/groups/{group_name} | Update the details for an organization group |
| PATCH | /v2/orgs/{org_name}/groups/{group_name} | Update some details for an organization group |
| DELETE | /v2/orgs/{org_name}/groups/{group_name} | Delete an organization group |
| GET | /v2/orgs/{org_name}/groups/{group_name}/members | List members of a group |
| POST | /v2/orgs/{org_name}/groups/{group_name}/members | Add a member to a group |
| DELETE | /v2/orgs/{org_name}/groups/{group_name}/members/{username} | Remove a user from a group |

### namespaces
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/namespaces/{namespace}/repositories/{repository}/tags | List repository tags |
| HEAD | /v2/namespaces/{namespace}/repositories/{repository}/tags | Check repository tags |
| GET | /v2/namespaces/{namespace}/repositories/{repository}/tags/{tag} | Read repository tag |
| HEAD | /v2/namespaces/{namespace}/repositories/{repository}/tags/{tag} | Check repository tag |
| PATCH | /v2/namespaces/{namespace}/repositories/{repository}/immutabletags | Update repository immutable tags |
| POST | /v2/namespaces/{namespace}/repositories/{repository}/immutabletags/verify | Verify repository immutable tags |
| GET | /v2/namespaces/{namespace}/repositories | List repositories in a namespace |
| POST | /v2/namespaces/{namespace}/repositories | Create a new repository |
| GET | /v2/namespaces/{namespace}/repositories/{repository} | Get repository in a namespace |
| HEAD | /v2/namespaces/{namespace}/repositories/{repository} | Check repository in a namespace |

### repositories
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/repositories/{namespace}/{repository}/groups | Assign a group (Team) to a repository for access |

### invites
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /v2/invites/{id} | Cancel an invite |
| PATCH | /v2/invites/{id}/resend | Resend an invite |
| POST | /v2/invites/bulk | Bulk create invites |

### scim
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/scim/2.0/ServiceProviderConfig | Get service provider config |
| GET | /v2/scim/2.0/ResourceTypes | List resource types |
| GET | /v2/scim/2.0/ResourceTypes/{name} | Get a resource type |
| GET | /v2/scim/2.0/Schemas | List schemas |
| GET | /v2/scim/2.0/Schemas/{id} | Get a schema |
| GET | /v2/scim/2.0/Users | List users |
| POST | /v2/scim/2.0/Users | Create user |
| GET | /v2/scim/2.0/Users/{id} | Get a user |
| PUT | /v2/scim/2.0/Users/{id} | Update a user |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a login?" -> POST /v2/users/login
- "Create a 2fa-login?" -> POST /v2/users/2fa-login
- "Create a token?" -> POST /v2/auth/token
- "Create a access-token?" -> POST /v2/access-tokens
- "List all access-tokens?" -> GET /v2/access-tokens
- "Partially update a access-token?" -> PATCH /v2/access-tokens/{uuid}
- "Get access-token details?" -> GET /v2/access-tokens/{uuid}
- "Delete a access-token?" -> DELETE /v2/access-tokens/{uuid}
- "List all actions?" -> GET /v2/auditlogs/{account}/actions
- "Get auditlog details?" -> GET /v2/auditlogs/{account}
- "List all settings?" -> GET /v2/orgs/{name}/settings
- "Create a access-token?" -> POST /v2/orgs/{name}/access-tokens
- "List all access-tokens?" -> GET /v2/orgs/{name}/access-tokens
- "Get access-token details?" -> GET /v2/orgs/{org_name}/access-tokens/{access_token_id}
- "Partially update a access-token?" -> PATCH /v2/orgs/{org_name}/access-tokens/{access_token_id}
- "Delete a access-token?" -> DELETE /v2/orgs/{org_name}/access-tokens/{access_token_id}
- "List all tags?" -> GET /v2/namespaces/{namespace}/repositories/{repository}/tags
- "Get tag details?" -> GET /v2/namespaces/{namespace}/repositories/{repository}/tags/{tag}
- "Create a verify?" -> POST /v2/namespaces/{namespace}/repositories/{repository}/immutabletags/verify
- "Create a group?" -> POST /v2/repositories/{namespace}/{repository}/groups
- "List all repositories?" -> GET /v2/namespaces/{namespace}/repositories
- "Create a repository?" -> POST /v2/namespaces/{namespace}/repositories
- "Get repository details?" -> GET /v2/namespaces/{namespace}/repositories/{repository}
- "List all members?" -> GET /v2/orgs/{org_name}/members
- "List all export?" -> GET /v2/orgs/{org_name}/members/export
- "Update a member?" -> PUT /v2/orgs/{org_name}/members/{username}
- "Delete a member?" -> DELETE /v2/orgs/{org_name}/members/{username}
- "List all invites?" -> GET /v2/orgs/{org_name}/invites
- "Search groups?" -> GET /v2/orgs/{org_name}/groups
- "Create a group?" -> POST /v2/orgs/{org_name}/groups
- "Get group details?" -> GET /v2/orgs/{org_name}/groups/{group_name}
- "Update a group?" -> PUT /v2/orgs/{org_name}/groups/{group_name}
- "Partially update a group?" -> PATCH /v2/orgs/{org_name}/groups/{group_name}
- "Delete a group?" -> DELETE /v2/orgs/{org_name}/groups/{group_name}
- "Search members?" -> GET /v2/orgs/{org_name}/groups/{group_name}/members
- "Create a member?" -> POST /v2/orgs/{org_name}/groups/{group_name}/members
- "Delete a member?" -> DELETE /v2/orgs/{org_name}/groups/{group_name}/members/{username}
- "Delete a invite?" -> DELETE /v2/invites/{id}
- "Create a bulk?" -> POST /v2/invites/bulk
- "List all ServiceProviderConfig?" -> GET /v2/scim/2.0/ServiceProviderConfig
- "List all ResourceTypes?" -> GET /v2/scim/2.0/ResourceTypes
- "Get ResourceType details?" -> GET /v2/scim/2.0/ResourceTypes/{name}
- "List all Schemas?" -> GET /v2/scim/2.0/Schemas
- "Get Schema details?" -> GET /v2/scim/2.0/Schemas/{id}
- "List all Users?" -> GET /v2/scim/2.0/Users
- "Create a User?" -> POST /v2/scim/2.0/Users
- "Get User details?" -> GET /v2/scim/2.0/Users/{id}
- "Update a User?" -> PUT /v2/scim/2.0/Users/{id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
