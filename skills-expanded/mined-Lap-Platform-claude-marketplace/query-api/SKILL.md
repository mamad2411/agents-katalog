---
name: query-api
description: "Query API skill. Use when working with Query for insights, funnels, retention. Covers 19 endpoints."
version: 1.0.0
generator: lapsh
---

# Query API
API version: 1.0.0

## Auth
No authentication required.

## Base URL
https://mixpanel.com/api/query

## Setup
1. No auth setup needed
2. GET /insights -- verify access
3. POST /cohorts/list -- create first list

## Endpoints

19 endpoints across 9 groups. See references/api-spec.lap for full details.

### insights
| Method | Path | Description |
|--------|------|-------------|
| GET | /insights | Query Saved Report |

### funnels
| Method | Path | Description |
|--------|------|-------------|
| GET | /funnels | Query Saved Report |
| GET | /funnels/list | List Saved Funnels |

### retention
| Method | Path | Description |
|--------|------|-------------|
| GET | /retention | Query Retention Report |
| GET | /retention/addiction | Query Frequency Report |

### segmentation
| Method | Path | Description |
|--------|------|-------------|
| GET | /segmentation | Query Segmentation Report |
| GET | /segmentation/numeric | Numerically Bucket |
| GET | /segmentation/sum | Numerically Sum |
| GET | /segmentation/average | Numerically Average |

### stream
| Method | Path | Description |
|--------|------|-------------|
| GET | /stream/query | Profile Event Activity |

### cohorts
| Method | Path | Description |
|--------|------|-------------|
| POST | /cohorts/list | List Saved Cohorts |

### engage
| Method | Path | Description |
|--------|------|-------------|
| POST | /engage | Query Profiles |

### events
| Method | Path | Description |
|--------|------|-------------|
| GET | /events | Aggregate Event Counts |
| GET | /events/top | Today's Top Events |
| GET | /events/names | Top Events |
| GET | /events/properties | Aggregrated Event Property Values |
| GET | /events/properties/top | Top Event Properties |
| GET | /events/properties/values | Top Event Property Values |

### jql
| Method | Path | Description |
|--------|------|-------------|
| POST | /jql | Custom JQL Query |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all insights?" -> GET /insights
- "List all funnels?" -> GET /funnels
- "List all list?" -> GET /funnels/list
- "List all retention?" -> GET /retention
- "List all addiction?" -> GET /retention/addiction
- "List all segmentation?" -> GET /segmentation
- "List all numeric?" -> GET /segmentation/numeric
- "List all sum?" -> GET /segmentation/sum
- "List all average?" -> GET /segmentation/average
- "List all query?" -> GET /stream/query
- "Create a list?" -> POST /cohorts/list
- "Create a engage?" -> POST /engage
- "List all events?" -> GET /events
- "List all top?" -> GET /events/top
- "List all names?" -> GET /events/names
- "List all properties?" -> GET /events/properties
- "List all top?" -> GET /events/properties/top
- "List all values?" -> GET /events/properties/values
- "Create a jql?" -> POST /jql

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
