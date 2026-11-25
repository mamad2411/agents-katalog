---
name: account-management-overview
description: "Account Management Overview API skill. Use when working with Account Management Overview for resources. Covers 25 endpoints."
version: 1.0.0
generator: lapsh
---

# Account Management Overview

## Auth
Bearer bearer

## Base URL
https://api.frontegg.com/tenants

## Setup
1. Set Authorization header with your Bearer token
2. GET /resources/tenants/v2 -- verify access
3. POST /resources/tenants/v1 -- create first tenants

## Endpoints

25 endpoints across 1 groups. See references/api-spec.lap for full details.

### resources
| Method | Path | Description |
|--------|------|-------------|
| GET | /resources/tenants/v1/{tenantId} | Get account (tenant) by ID |
| PUT | /resources/tenants/v1/{tenantId} | Update account (tenant) |
| DELETE | /resources/tenants/v1/{tenantId} | Delete account (tenant) |
| POST | /resources/tenants/v1 | Create an account (tenant) |
| DELETE | /resources/tenants/v1 | Delete current account (tenant) |
| POST | /resources/tenants/v1/{tenantId}/metadata | Add account (tenant) metadata |
| DELETE | /resources/tenants/v1/{tenantId}/metadata/{key} | Delete account (tenant) metadata |
| GET | /resources/tenants/v2 | Get accounts (tenants) |
| GET | /resources/tenants/v2/alias/{alias} | Get account (tenant) by alias |
| GET | /resources/tenants/v2/{tenantId} | Get an account (tenant) |
| PUT | /resources/tenants/v2/{tenantId} | Update an account (tenant) |
| POST | /resources/sub-tenants/v1 | Create sub-account |
| PUT | /resources/sub-tenants/v1/{tenantId}/management | Update sub-account (tenant) management |
| PUT | /resources/sub-tenants/v1/{tenantId}/hierarchy-settings | Update sub-account hierarchy settings |
| DELETE | /resources/sub-tenants/v1/{tenantId} | Delete a sub-account by ID |
| GET | /resources/account-settings/v1 | Get account settings |
| PUT | /resources/account-settings/v1 | Update account settings |
| GET | /resources/account-settings/v1/public | Get public settings |
| POST | /resources/migrations/v1/tenants | Migrate accounts (tenants) |
| GET | /resources/migrations/v1/tenants/status/{migrationId} | Accounts (tenants) migration status |
| GET | /resources/hierarchy/v1 | Get sub-accounts (tenants) |
| POST | /resources/hierarchy/v1 | Create sub-account (tenant) |
| DELETE | /resources/hierarchy/v1 | Delete sub-account (tenant) |
| GET | /resources/hierarchy/v1/parents | Get parent accounts (tenants) |
| GET | /resources/hierarchy/v1/tree | Get sub-accounts (tenanants) hierarchy tree |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get tenant details?" -> GET /resources/tenants/v1/{tenantId}
- "Update a tenant?" -> PUT /resources/tenants/v1/{tenantId}
- "Delete a tenant?" -> DELETE /resources/tenants/v1/{tenantId}
- "Create a tenant?" -> POST /resources/tenants/v1
- "Create a metadata?" -> POST /resources/tenants/v1/{tenantId}/metadata
- "Delete a metadata?" -> DELETE /resources/tenants/v1/{tenantId}/metadata/{key}
- "List all tenants?" -> GET /resources/tenants/v2
- "Get alia details?" -> GET /resources/tenants/v2/alias/{alias}
- "Get tenant details?" -> GET /resources/tenants/v2/{tenantId}
- "Update a tenant?" -> PUT /resources/tenants/v2/{tenantId}
- "Create a sub-tenant?" -> POST /resources/sub-tenants/v1
- "Delete a sub-tenant?" -> DELETE /resources/sub-tenants/v1/{tenantId}
- "List all account-settings?" -> GET /resources/account-settings/v1
- "List all public?" -> GET /resources/account-settings/v1/public
- "Create a tenant?" -> POST /resources/migrations/v1/tenants
- "Get status details?" -> GET /resources/migrations/v1/tenants/status/{migrationId}
- "List all hierarchy?" -> GET /resources/hierarchy/v1
- "Create a hierarchy?" -> POST /resources/hierarchy/v1
- "List all parents?" -> GET /resources/hierarchy/v1/parents
- "List all tree?" -> GET /resources/hierarchy/v1/tree
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object
- Error responses use types: When

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
