---
name: turso-platform-api
description: "Turso Platform API skill. Use when working with Turso Platform for organizations, locations, auth. Covers 46 endpoints."
version: 1.0.0
generator: lapsh
---

# Turso Platform API
API version: 0.1.0

## Auth
Bearer bearer

## Base URL
https://api.turso.tech

## Setup
1. Set Authorization header with your Bearer token
2. GET /v1/locations -- verify access
3. POST /v1/organizations/{organizationSlug}/databases -- create first databases

## Endpoints

46 endpoints across 3 groups. See references/api-spec.lap for full details.

### organizations
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/organizations/{organizationSlug}/databases | List Databases |
| POST | /v1/organizations/{organizationSlug}/databases | Create Database |
| GET | /v1/organizations/{organizationSlug}/databases/{databaseName} | Retrieve Database |
| DELETE | /v1/organizations/{organizationSlug}/databases/{databaseName} | Delete Database |
| GET | /v1/organizations/{organizationSlug}/databases/{databaseName}/configuration | Retrieve Database Configuration |
| PATCH | /v1/organizations/{organizationSlug}/databases/{databaseName}/configuration | Update Database Configuration |
| GET | /v1/organizations/{organizationSlug}/databases/{databaseName}/instances | List Database Instances |
| GET | /v1/organizations/{organizationSlug}/databases/{databaseName}/instances/{instanceName} | Retrieve Database Instance |
| POST | /v1/organizations/{organizationSlug}/databases/{databaseName}/auth/tokens | Generate Database Auth Token |
| GET | /v1/organizations/{organizationSlug}/databases/{databaseName}/usage | Retrieve Database Usage |
| GET | /v1/organizations/{organizationSlug}/databases/{databaseName}/stats | Retrieve Database Stats |
| POST | /v1/organizations/{organizationSlug}/databases/{databaseName}/auth/rotate | Invalidate All Database Auth Tokens |
| GET | /v1/organizations/{organizationSlug}/groups | List Groups |
| POST | /v1/organizations/{organizationSlug}/groups | Create Group |
| GET | /v1/organizations/{organizationSlug}/groups/{groupName} | Retrieve Group |
| DELETE | /v1/organizations/{organizationSlug}/groups/{groupName} | Delete Group |
| GET | /v1/organizations/{organizationSlug}/groups/{groupName}/configuration | Retrieve Group Configuration |
| PATCH | /v1/organizations/{organizationSlug}/groups/{groupName}/configuration | Update Group Configuration |
| POST | /v1/organizations/{organizationSlug}/groups/{groupName}/transfer | Transfer Group |
| POST | /v1/organizations/{organizationSlug}/groups/{groupName}/unarchive | Unarchive Group |
| POST | /v1/organizations/{organizationSlug}/groups/{groupName}/locations/{location} | Add Location to Group |
| DELETE | /v1/organizations/{organizationSlug}/groups/{groupName}/locations/{location} | Remove Location from Group |
| POST | /v1/organizations/{organizationSlug}/groups/{groupName}/update | Update Databases in a Group |
| POST | /v1/organizations/{organizationSlug}/groups/{groupName}/auth/tokens | Create Group Auth Token |
| POST | /v1/organizations/{organizationSlug}/groups/{groupName}/auth/rotate | Invalidate All Group Auth Tokens |
| GET | /v1/organizations | List Organizations |
| GET | /v1/organizations/{organizationSlug} | Retrieve Organization |
| PATCH | /v1/organizations/{organizationSlug} | Update Organization |
| GET | /v1/organizations/{organizationSlug}/plans | List Plans |
| GET | /v1/organizations/{organizationSlug}/invoices | List Invoices |
| GET | /v1/organizations/{organizationSlug}/subscription | Current Subscription |
| GET | /v1/organizations/{organizationSlug}/usage | Organization Usage |
| GET | /v1/organizations/{organizationSlug}/members | List Members |
| POST | /v1/organizations/{organizationSlug}/members | Add Member |
| GET | /v1/organizations/{organizationSlug}/members/{username} | Retrieve Member |
| PATCH | /v1/organizations/{organizationSlug}/members/{username} | Update Member Role |
| DELETE | /v1/organizations/{organizationSlug}/members/{username} | Remove Member |
| GET | /v1/organizations/{organizationSlug}/invites | List Invites |
| POST | /v1/organizations/{organizationSlug}/invites | Invite Organization Member |
| DELETE | /v1/organizations/{organizationSlug}/invites/{email} | Delete Invite |
| GET | /v1/organizations/{organizationSlug}/audit-logs | List Audit Logs |

### locations
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/locations | List Locations |

### auth
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/auth/validate | Validate API Token |
| GET | /v1/auth/api-tokens | List API Tokens |
| POST | /v1/auth/api-tokens/{tokenName} | Create API Token |
| DELETE | /v1/auth/api-tokens/{tokenName} | Revoke API Token |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all databases?" -> GET /v1/organizations/{organizationSlug}/databases
- "Create a database?" -> POST /v1/organizations/{organizationSlug}/databases
- "Get database details?" -> GET /v1/organizations/{organizationSlug}/databases/{databaseName}
- "Delete a database?" -> DELETE /v1/organizations/{organizationSlug}/databases/{databaseName}
- "List all configuration?" -> GET /v1/organizations/{organizationSlug}/databases/{databaseName}/configuration
- "List all instances?" -> GET /v1/organizations/{organizationSlug}/databases/{databaseName}/instances
- "Get instance details?" -> GET /v1/organizations/{organizationSlug}/databases/{databaseName}/instances/{instanceName}
- "Create a token?" -> POST /v1/organizations/{organizationSlug}/databases/{databaseName}/auth/tokens
- "List all usage?" -> GET /v1/organizations/{organizationSlug}/databases/{databaseName}/usage
- "List all stats?" -> GET /v1/organizations/{organizationSlug}/databases/{databaseName}/stats
- "Create a rotate?" -> POST /v1/organizations/{organizationSlug}/databases/{databaseName}/auth/rotate
- "List all groups?" -> GET /v1/organizations/{organizationSlug}/groups
- "Create a group?" -> POST /v1/organizations/{organizationSlug}/groups
- "Get group details?" -> GET /v1/organizations/{organizationSlug}/groups/{groupName}
- "Delete a group?" -> DELETE /v1/organizations/{organizationSlug}/groups/{groupName}
- "List all configuration?" -> GET /v1/organizations/{organizationSlug}/groups/{groupName}/configuration
- "Create a transfer?" -> POST /v1/organizations/{organizationSlug}/groups/{groupName}/transfer
- "Create a unarchive?" -> POST /v1/organizations/{organizationSlug}/groups/{groupName}/unarchive
- "Delete a location?" -> DELETE /v1/organizations/{organizationSlug}/groups/{groupName}/locations/{location}
- "Create a update?" -> POST /v1/organizations/{organizationSlug}/groups/{groupName}/update
- "Create a token?" -> POST /v1/organizations/{organizationSlug}/groups/{groupName}/auth/tokens
- "Create a rotate?" -> POST /v1/organizations/{organizationSlug}/groups/{groupName}/auth/rotate
- "List all locations?" -> GET /v1/locations
- "List all organizations?" -> GET /v1/organizations
- "Get organization details?" -> GET /v1/organizations/{organizationSlug}
- "Partially update a organization?" -> PATCH /v1/organizations/{organizationSlug}
- "List all plans?" -> GET /v1/organizations/{organizationSlug}/plans
- "List all invoices?" -> GET /v1/organizations/{organizationSlug}/invoices
- "List all subscription?" -> GET /v1/organizations/{organizationSlug}/subscription
- "List all usage?" -> GET /v1/organizations/{organizationSlug}/usage
- "List all members?" -> GET /v1/organizations/{organizationSlug}/members
- "Create a member?" -> POST /v1/organizations/{organizationSlug}/members
- "Get member details?" -> GET /v1/organizations/{organizationSlug}/members/{username}
- "Partially update a member?" -> PATCH /v1/organizations/{organizationSlug}/members/{username}
- "Delete a member?" -> DELETE /v1/organizations/{organizationSlug}/members/{username}
- "List all invites?" -> GET /v1/organizations/{organizationSlug}/invites
- "Create a invite?" -> POST /v1/organizations/{organizationSlug}/invites
- "Delete a invite?" -> DELETE /v1/organizations/{organizationSlug}/invites/{email}
- "List all validate?" -> GET /v1/auth/validate
- "List all api-tokens?" -> GET /v1/auth/api-tokens
- "Delete a api-token?" -> DELETE /v1/auth/api-tokens/{tokenName}
- "List all audit-logs?" -> GET /v1/organizations/{organizationSlug}/audit-logs
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
