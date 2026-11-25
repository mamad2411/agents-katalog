---
name: easypdfserver
description: "EasyPDFServer API skill. Use when working with EasyPDFServer for make-pdf. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# EasyPDFServer
API version: 1.0

## Auth
Requires API key (key parameter)

## Base URL
https://api.easypdfserver.com

## Setup
1. Include your API key via the key parameter
3. POST /make-pdf -- create first make-pdf

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### make-pdf
| Method | Path | Description |
|--------|------|-------------|
| POST | /make-pdf | Generate a PDF from HTML or URL. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a make-pdf?" -> POST /make-pdf

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
