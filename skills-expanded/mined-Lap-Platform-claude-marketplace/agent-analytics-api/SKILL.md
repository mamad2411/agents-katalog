---
name: agent-analytics-api
description: "Agent Analytics API skill. Use when working with Agent Analytics for track, stats, events. Covers 32 endpoints."
version: 1.0.0
generator: lapsh
---

# Agent Analytics API
API version: 1.0.0

## Auth
ApiKey X-API-Key in header | ApiKey token in query

## Base URL
https://api.agentanalytics.sh

## Setup
1. Set your API key in the appropriate header
2. GET /stats -- verify access
3. POST /track -- create first track

## Endpoints

32 endpoints across 19 groups. See references/api-spec.lap for full details.

### track
| Method | Path | Description |
|--------|------|-------------|
| POST | /track | Track a single event |
| POST | /track/batch | Track multiple events |

### stats
| Method | Path | Description |
|--------|------|-------------|
| GET | /stats | Aggregated stats overview |

### events
| Method | Path | Description |
|--------|------|-------------|
| GET | /events | Raw event log |

### query
| Method | Path | Description |
|--------|------|-------------|
| POST | /query | Flexible analytics query |

### properties
| Method | Path | Description |
|--------|------|-------------|
| GET | /properties | Discover event names and property keys |
| GET | /properties/received | Property keys by event name |

### sessions
| Method | Path | Description |
|--------|------|-------------|
| GET | /sessions | List sessions |
| GET | /sessions/distribution | Session duration histogram |

### breakdown
| Method | Path | Description |
|--------|------|-------------|
| GET | /breakdown | Top property values |

### insights
| Method | Path | Description |
|--------|------|-------------|
| GET | /insights | Period-over-period comparison |

### pages
| Method | Path | Description |
|--------|------|-------------|
| GET | /pages | Entry/exit page stats |

### heatmap
| Method | Path | Description |
|--------|------|-------------|
| GET | /heatmap | Day-of-week x hour traffic grid |

### funnel
| Method | Path | Description |
|--------|------|-------------|
| POST | /funnel | Funnel analysis |

### retention
| Method | Path | Description |
|--------|------|-------------|
| GET | /retention | Cohort retention analysis |

### stream
| Method | Path | Description |
|--------|------|-------------|
| GET | /stream | Live event stream (SSE) |

### live
| Method | Path | Description |
|--------|------|-------------|
| GET | /live | Live snapshot (real-time) |

### projects
| Method | Path | Description |
|--------|------|-------------|
| GET | /projects | List all projects |
| POST | /projects | Create a new project |
| GET | /projects/{id} | Get project details |
| PATCH | /projects/{id} | Update a project |
| DELETE | /projects/{id} | Delete a project |

### account
| Method | Path | Description |
|--------|------|-------------|
| GET | /account | Get account info |
| POST | /account/revoke-key | Revoke and regenerate API key |

### experiments
| Method | Path | Description |
|--------|------|-------------|
| GET | /experiments/config | Get experiment config for tracker.js |
| POST | /experiments | Create an A/B experiment |
| GET | /experiments | List experiments |
| GET | /experiments/{id} | Get experiment with live results |
| PATCH | /experiments/{id} | Update experiment status |
| DELETE | /experiments/{id} | Delete an experiment |

### health
| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Health check |

### tracker.js
| Method | Path | Description |
|--------|------|-------------|
| GET | /tracker.js | JavaScript tracker script |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a track?" -> POST /track
- "Create a batch?" -> POST /track/batch
- "List all stats?" -> GET /stats
- "List all events?" -> GET /events
- "Create a query?" -> POST /query
- "List all properties?" -> GET /properties
- "List all received?" -> GET /properties/received
- "List all sessions?" -> GET /sessions
- "List all breakdown?" -> GET /breakdown
- "List all insights?" -> GET /insights
- "List all pages?" -> GET /pages
- "List all distribution?" -> GET /sessions/distribution
- "List all heatmap?" -> GET /heatmap
- "Create a funnel?" -> POST /funnel
- "List all retention?" -> GET /retention
- "List all stream?" -> GET /stream
- "List all live?" -> GET /live
- "List all projects?" -> GET /projects
- "Create a project?" -> POST /projects
- "Get project details?" -> GET /projects/{id}
- "Partially update a project?" -> PATCH /projects/{id}
- "Delete a project?" -> DELETE /projects/{id}
- "List all account?" -> GET /account
- "Create a revoke-key?" -> POST /account/revoke-key
- "List all config?" -> GET /experiments/config
- "Create a experiment?" -> POST /experiments
- "List all experiments?" -> GET /experiments
- "Get experiment details?" -> GET /experiments/{id}
- "Partially update a experiment?" -> PATCH /experiments/{id}
- "Delete a experiment?" -> DELETE /experiments/{id}
- "List all health?" -> GET /health
- "List all tracker.js?" -> GET /tracker.js
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
