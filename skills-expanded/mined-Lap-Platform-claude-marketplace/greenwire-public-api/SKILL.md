---
name: greenwire-public-api
description: "Greenwire Public API skill. Use when working with Greenwire Public for volunteers, groups, events. Covers 6 endpoints."
version: 1.0.0
generator: lapsh
---

# Greenwire Public API
API version: 1.0.0

## Auth
No authentication required.

## Base URL
https://greenwire.greenpeace.org/api/public

## Setup
1. No auth setup needed
2. GET /volunteers -- verify access

## Endpoints

6 endpoints across 3 groups. See references/api-spec.lap for full details.

### volunteers
| Method | Path | Description |
|--------|------|-------------|
| GET | /volunteers | Gets an array of `Volunteer` object. Mandatory query param of **domain** determines the site / country the volunteers are from. |
| GET | /volunteers/{UUID} | Get one specific `Volunteer` object by specifying its UUID in the url path. |

### groups
| Method | Path | Description |
|--------|------|-------------|
| GET | /groups | Gets an array of `Group` object. Mandatory query param of **domain** determines the site / country the group belongs to. |
| GET | /groups/{UUID} | Get one `Group` object by specifying its UUID in the url path. |

### events
| Method | Path | Description |
|--------|------|-------------|
| GET | /events | Return the upcoming events (e.g. start date >= today). Gets an array of `Event` object. Mandatory query param of **domain** determines the site / country the event belongs to. |
| GET | /events/{UUID} | Get one `Event` object by specifying its UUID in the url path. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all volunteers?" -> GET /volunteers
- "Get volunteer details?" -> GET /volunteers/{UUID}
- "List all groups?" -> GET /groups
- "Get group details?" -> GET /groups/{UUID}
- "List all events?" -> GET /events
- "Get event details?" -> GET /events/{UUID}

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
