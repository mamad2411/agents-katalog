---
name: color-name-api
description: "Color Name API skill. Use when working with Color Name for root, health, docs. Covers 7 endpoints."
version: 1.0.0
generator: lapsh
---

# Color Name API
API version: 1.1.0

## Auth
No authentication required.

## Base URL
https://api.color.pizza/

## Setup
1. No auth setup needed
2. GET / -- verify access

## Endpoints

7 endpoints across 7 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| GET | / | Get API metadata and discovery information |

### health
| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Health check endpoint |

### docs
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/docs/ | Get API Documentation |

### v1
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/ | Get color names for specific hex values |

### names
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/names/ | Search for colors by name |

### lists
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/lists/ | Get available color name lists |

### swatch
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/swatch/ | Generate a color swatch for any color |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all health?" -> GET /health
- "List all docs?" -> GET /v1/docs/
- "List all names?" -> GET /v1/names/
- "List all lists?" -> GET /v1/lists/
- "List all swatch?" -> GET /v1/swatch/

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
