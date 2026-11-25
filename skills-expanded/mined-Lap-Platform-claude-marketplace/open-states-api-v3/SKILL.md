---
name: open-states-api-v3
description: "Open States API v3 API skill. Use when working with Open States API v3 for jurisdictions, people, people.geo. Covers 12 endpoints."
version: 1.0.0
generator: lapsh
---

# Open States API v3
API version: 2021.11.12

## Auth
ApiKey apikey in query

## Base URL
Not specified.

## Setup
1. Set your API key in the appropriate header
2. GET /jurisdictions -- verify access

## Endpoints

12 endpoints across 7 groups. See references/api-spec.lap for full details.

### jurisdictions
| Method | Path | Description |
|--------|------|-------------|
| GET | /jurisdictions | Jurisdiction List |
| GET | /jurisdictions/{jurisdiction_id} | Jurisdiction Detail |

### people
| Method | Path | Description |
|--------|------|-------------|
| GET | /people | People Search |

### people.geo
| Method | Path | Description |
|--------|------|-------------|
| GET | /people.geo | People Geo |

### bills
| Method | Path | Description |
|--------|------|-------------|
| GET | /bills | Bills Search |
| GET | /bills/ocd-bill/{openstates_bill_id} | Bill Detail By Id |
| GET | /bills/{jurisdiction}/{session}/{bill_id} | Bill Detail |

### committees
| Method | Path | Description |
|--------|------|-------------|
| GET | /committees | Committee List |
| GET | /committees/{committee_id} | Committee Detail |

### events
| Method | Path | Description |
|--------|------|-------------|
| GET | /events | Event List |
| GET | /events/{event_id} | Event Detail |

### metrics
| Method | Path | Description |
|--------|------|-------------|
| GET | /metrics | Metrics |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all jurisdictions?" -> GET /jurisdictions
- "Get jurisdiction details?" -> GET /jurisdictions/{jurisdiction_id}
- "List all people?" -> GET /people
- "List all people.geo?" -> GET /people.geo
- "Search bills?" -> GET /bills
- "Get ocd-bill details?" -> GET /bills/ocd-bill/{openstates_bill_id}
- "Get bill details?" -> GET /bills/{jurisdiction}/{session}/{bill_id}
- "List all committees?" -> GET /committees
- "Get committee details?" -> GET /committees/{committee_id}
- "List all events?" -> GET /events
- "Get event details?" -> GET /events/{event_id}
- "List all metrics?" -> GET /metrics
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
