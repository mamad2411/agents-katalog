---
name: selectpdf-html-to-pdf-api
description: "SelectPdf HTML To PDF API skill. Use when working with SelectPdf HTML To PDF for api2. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# SelectPdf HTML To PDF API
API version: 1.0.0

## Auth
No authentication required.

## Base URL
https://selectpdf.com/

## Setup
1. No auth setup needed
3. POST /api2/convert -- create first convert

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### api2
| Method | Path | Description |
|--------|------|-------------|
| POST | /api2/convert | Performs a html to pdf conversion |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a convert?" -> POST /api2/convert

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
