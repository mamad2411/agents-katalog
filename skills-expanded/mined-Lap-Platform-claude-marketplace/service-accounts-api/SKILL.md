---
name: service-accounts-api
description: "Service Accounts API skill. Use when working with Service Accounts for organizations, projects. Covers 7 endpoints."
version: 1.0.0
generator: lapsh
---

# Service Accounts API
API version: 1.0.0

## Auth
No authentication required.

## Base URL
Not specified.

## Setup
1. No auth setup needed
2. GET /organizations/{organizationId}/service-accounts -- verify access
3. POST /organizations/{organizationId}/service-accounts -- create first service-accounts

## Endpoints

7 endpoints across 2 groups. See references/api-spec.lap for full details.

### organizations
| Method | Path | Description |
|--------|------|-------------|
| GET | /organizations/{organizationId}/service-accounts | List Service Accounts |
| POST | /organizations/{organizationId}/service-accounts | Create Service Account |
| GET | /organizations/{organizationId}/service-accounts/{serviceAccountId} | Get Service Account |
| DELETE | /organizations/{organizationId}/service-accounts/{serviceAccountId} | Delete Service Account |
| POST | /organizations/{organizationId}/service-accounts/add-to-project | Add Service Accounts To Projects |
| POST | /organizations/{organizationId}/service-accounts/remove-from-project | Remove Service Accounts From Projects |

### projects
| Method | Path | Description |
|--------|------|-------------|
| GET | /projects/{projectId}/service-accounts | List Service Accounts For Project |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all service-accounts?" -> GET /organizations/{organizationId}/service-accounts
- "Create a service-account?" -> POST /organizations/{organizationId}/service-accounts
- "Get service-account details?" -> GET /organizations/{organizationId}/service-accounts/{serviceAccountId}
- "Delete a service-account?" -> DELETE /organizations/{organizationId}/service-accounts/{serviceAccountId}
- "List all service-accounts?" -> GET /projects/{projectId}/service-accounts
- "Create a add-to-project?" -> POST /organizations/{organizationId}/service-accounts/add-to-project
- "Create a remove-from-project?" -> POST /organizations/{organizationId}/service-accounts/remove-from-project

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
