---
name: doqsdev-pdf-filling-api
description: "doqs.dev | PDF filling API skill. Use when working with doqs.dev | PDF filling for pdf-filling, pdf-generator. Covers 4 endpoints."
version: 1.0.0
generator: lapsh
---

# doqs.dev | PDF filling API
API version: 1.0

## Auth
ApiKey x-api-key in header

## Base URL
https://api.doqs.dev/v1

## Setup
1. Set your API key in the appropriate header
2. GET /pdf-filling/templates -- verify access
3. POST /pdf-filling/templates/{id}/fill -- create first fill

## Endpoints

4 endpoints across 2 groups. See references/api-spec.lap for full details.

### pdf-filling
| Method | Path | Description |
|--------|------|-------------|
| POST | /pdf-filling/templates/{id}/fill | Fill |
| GET | /pdf-filling/templates | List |

### pdf-generator
| Method | Path | Description |
|--------|------|-------------|
| POST | /pdf-generator/render | Render Pdf |
| GET | /pdf-generator/submissions | Get Submissions |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a fill?" -> POST /pdf-filling/templates/{id}/fill
- "List all templates?" -> GET /pdf-filling/templates
- "Create a render?" -> POST /pdf-generator/render
- "List all submissions?" -> GET /pdf-generator/submissions
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
