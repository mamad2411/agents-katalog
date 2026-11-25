---
name: twilio-sendgrid-statistics-api
description: "Twilio SendGrid Statistics API skill. Use when working with Twilio SendGrid Statistics for browsers, categories, clients. Covers 10 endpoints."
version: 1.0.0
generator: lapsh
---

# Twilio SendGrid Statistics API
API version: 1.0.0

## Auth
Bearer bearer

## Base URL
https://api.sendgrid.com

## Setup
1. Set Authorization header with your Bearer token
2. GET /v3/browsers/stats -- verify access

## Endpoints

10 endpoints across 7 groups. See references/api-spec.lap for full details.

### browsers
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/browsers/stats | Retrieve email statistics by browser. |

### categories
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/categories | Retrieve all categories |
| GET | /v3/categories/stats | Retrieve Email Statistics for Categories |
| GET | /v3/categories/stats/sums | Retrieve sums of email stats for each category. |

### clients
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/clients/stats | Retrieve email statistics by client type. |
| GET | /v3/clients/{client_type}/stats | Retrieve stats by a specific client type. |

### devices
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/devices/stats | Retrieve email statistics by device type. |

### geo
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/geo/stats | Retrieve email statistics by country and state/province. |

### mailbox_providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/mailbox_providers/stats | Retrieve email statistics by mailbox provider. |

### stats
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/stats | Retrieve global email statistics |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all stats?" -> GET /v3/browsers/stats
- "List all categories?" -> GET /v3/categories
- "List all stats?" -> GET /v3/categories/stats
- "List all sums?" -> GET /v3/categories/stats/sums
- "List all stats?" -> GET /v3/clients/stats
- "List all stats?" -> GET /v3/clients/{client_type}/stats
- "List all stats?" -> GET /v3/devices/stats
- "List all stats?" -> GET /v3/geo/stats
- "List all stats?" -> GET /v3/mailbox_providers/stats
- "List all stats?" -> GET /v3/stats
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
