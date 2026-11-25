---
name: sync-for-commerce
description: "Sync for Commerce API skill. Use when working with Sync for Commerce for config, companies, sync. Covers 22 endpoints."
version: 1.0.0
generator: lapsh
---

# Sync for Commerce
API version: 1.1

## Auth
ApiKey Authorization in header

## Base URL
https://api.codat.io

## Setup
1. Set your API key in the appropriate header
2. GET /companies -- verify access
3. POST /companies -- create first companies

## Endpoints

22 endpoints across 5 groups. See references/api-spec.lap for full details.

### config
| Method | Path | Description |
|--------|------|-------------|
| GET | /config/sync/commerce/{commerceKey}/{accountingKey}/start | Start new sync flow |
| GET | /config/companies/{companyId}/sync/commerce | Get company configuration |
| POST | /config/companies/{companyId}/sync/commerce | Set configuration |
| GET | /config/integrations | List integrations |
| GET | /config/integrations/{platformKey}/branding | Get branding for an integration |

### companies
| Method | Path | Description |
|--------|------|-------------|
| GET | /companies | List companies |
| POST | /companies | Create company |
| GET | /companies/{companyId}/connections | List connections |
| POST | /companies/{companyId}/connections | Create connection |
| PATCH | /companies/{companyId}/connections/{connectionId} | Update connection |
| PUT | /companies/{companyId}/connections/{connectionId}/authorization | Update authorization |
| POST | /companies/{companyId}/sync/commerce/latest | Initiate new sync |
| GET | /companies/{companyId}/sync/commerce/syncs/lastSuccessful/status | Last successful sync |
| GET | /companies/{companyId}/sync/commerce/syncs/latest/status | Latest sync status |
| GET | /companies/{companyId}/sync/commerce/syncs/{syncId}/status | Get sync status |
| GET | /companies/{companyId}/sync/commerce/syncs/list/status | List sync statuses |

### sync
| Method | Path | Description |
|--------|------|-------------|
| GET | /sync/commerce/config/ui/text | Get preferences for text fields |
| PATCH | /sync/commerce/config/ui/text | Update preferences for text fields |
| POST | /sync/commerce/config/ui/accounts/platform/{platformKey} | Update visible accounts |

### clients
| Method | Path | Description |
|--------|------|-------------|
| GET | /clients/{clientId}/config/ui/accounts/platform/{platformKey} | List visible accounts |

### meta
| Method | Path | Description |
|--------|------|-------------|
| POST | /meta/companies/{companyId}/sync/commerce/historic | Initiate sync for specific range |
| GET | /meta/companies/{companyId}/sync/commerce/status | Get sync status |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all start?" -> GET /config/sync/commerce/{commerceKey}/{accountingKey}/start
- "Search companies?" -> GET /companies
- "Create a company?" -> POST /companies
- "Search connections?" -> GET /companies/{companyId}/connections
- "Create a connection?" -> POST /companies/{companyId}/connections
- "Partially update a connection?" -> PATCH /companies/{companyId}/connections/{connectionId}
- "List all commerce?" -> GET /config/companies/{companyId}/sync/commerce
- "Create a commerce?" -> POST /config/companies/{companyId}/sync/commerce
- "Search integrations?" -> GET /config/integrations
- "List all branding?" -> GET /config/integrations/{platformKey}/branding
- "List all text?" -> GET /sync/commerce/config/ui/text
- "Get platform details?" -> GET /clients/{clientId}/config/ui/accounts/platform/{platformKey}
- "Create a latest?" -> POST /companies/{companyId}/sync/commerce/latest
- "Create a historic?" -> POST /meta/companies/{companyId}/sync/commerce/historic
- "List all status?" -> GET /meta/companies/{companyId}/sync/commerce/status
- "List all status?" -> GET /companies/{companyId}/sync/commerce/syncs/lastSuccessful/status
- "List all status?" -> GET /companies/{companyId}/sync/commerce/syncs/latest/status
- "List all status?" -> GET /companies/{companyId}/sync/commerce/syncs/{syncId}/status
- "List all status?" -> GET /companies/{companyId}/sync/commerce/syncs/list/status
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
