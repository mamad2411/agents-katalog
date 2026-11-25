---
name: sheerseo-api
description: "SheerSEO API skill. Use when working with SheerSEO for serp-submit, serp-collect, rank-submit. Covers 4 endpoints."
version: 1.0.0
generator: lapsh
---

# SheerSEO API
API version: 0.0.1

## Auth
ApiKey apiKey in query

## Base URL
https://www.sheerseo.com/seo/api

## Setup
1. Set your API key in the appropriate header
3. POST /serp-submit -- create first serp-submit

## Endpoints

4 endpoints across 4 groups. See references/api-spec.lap for full details.

### serp-submit
| Method | Path | Description |
|--------|------|-------------|
| POST | /serp-submit | Submit serp jobs |

### serp-collect
| Method | Path | Description |
|--------|------|-------------|
| POST | /serp-collect | Submit serp jobs |

### rank-submit
| Method | Path | Description |
|--------|------|-------------|
| POST | /rank-submit | Submit rank jobs |

### rank-collect
| Method | Path | Description |
|--------|------|-------------|
| POST | /rank-collect | Submit serp jobs |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a serp-submit?" -> POST /serp-submit
- "Create a serp-collect?" -> POST /serp-collect
- "Create a rank-submit?" -> POST /rank-submit
- "Create a rank-collect?" -> POST /rank-collect
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
