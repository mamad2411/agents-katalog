---
name: swagger-api-rest-for-patrowl-engines
description: "Swagger API-REST for Patrowl Engines API skill. Use when working with Swagger API-REST for Patrowl Engines for root, liveness, readiness. Covers 14 endpoints."
version: 1.0.0
generator: lapsh
---

# Swagger API-REST for Patrowl Engines
API version: 1.0.0

## Auth
No authentication required.

## Base URL
http://localhost:5001/engines/nmap/

## Setup
1. No auth setup needed
2. GET / -- verify access
3. POST /startscan -- create first startscan

## Endpoints

14 endpoints across 12 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| GET | / | Index page |

### liveness
| Method | Path | Description |
|--------|------|-------------|
| GET | /liveness | Liveness page |

### readiness
| Method | Path | Description |
|--------|------|-------------|
| GET | /readiness | Readiness page |

### test
| Method | Path | Description |
|--------|------|-------------|
| GET | /test | Test page |

### reloadconfig
| Method | Path | Description |
|--------|------|-------------|
| GET | /reloadconfig | Configuration reloading page |

### info
| Method | Path | Description |
|--------|------|-------------|
| GET | /info | Engine info page |

### clean
| Method | Path | Description |
|--------|------|-------------|
| GET | /clean | Clean all scans |
| GET | /clean/{scanId} | Clean scan |

### status
| Method | Path | Description |
|--------|------|-------------|
| GET | /status | Status on all scans |
| GET | /status/{scanId} | Status of a scan |

### stopscans
| Method | Path | Description |
|--------|------|-------------|
| GET | /stopscans | Stop all scans |

### stop
| Method | Path | Description |
|--------|------|-------------|
| GET | /stop/{scanId} | Stop a scan |

### getfindings
| Method | Path | Description |
|--------|------|-------------|
| GET | /getfindings/{scanId} | Get findings on finished scans |

### startscan
| Method | Path | Description |
|--------|------|-------------|
| POST | /startscan | Start a new scan |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all liveness?" -> GET /liveness
- "List all readiness?" -> GET /readiness
- "List all test?" -> GET /test
- "List all reloadconfig?" -> GET /reloadconfig
- "List all info?" -> GET /info
- "List all clean?" -> GET /clean
- "Get clean details?" -> GET /clean/{scanId}
- "List all status?" -> GET /status
- "Get status details?" -> GET /status/{scanId}
- "List all stopscans?" -> GET /stopscans
- "Get stop details?" -> GET /stop/{scanId}
- "Get getfinding details?" -> GET /getfindings/{scanId}
- "Create a startscan?" -> POST /startscan

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
