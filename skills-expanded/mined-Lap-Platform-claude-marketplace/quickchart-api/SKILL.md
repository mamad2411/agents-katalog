---
name: quickchart-api
description: "QuickChart API skill. Use when working with QuickChart for chart, qr. Covers 4 endpoints."
version: 1.0.0
generator: lapsh
---

# QuickChart API
API version: 1.0.0

## Auth
ApiKey key in query

## Base URL
https://quickchart.io

## Setup
1. Set your API key in the appropriate header
2. GET /chart -- verify access
3. POST /chart -- create first chart

## Endpoints

4 endpoints across 2 groups. See references/api-spec.lap for full details.

### chart
| Method | Path | Description |
|--------|------|-------------|
| GET | /chart | Generate a chart (GET) |
| POST | /chart | Generate a chart (POST) |

### qr
| Method | Path | Description |
|--------|------|-------------|
| GET | /qr | Generate a QR code (GET) |
| POST | /qr | Generate a QR code (POST) |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all chart?" -> GET /chart
- "Create a chart?" -> POST /chart
- "List all qr?" -> GET /qr
- "Create a qr?" -> POST /qr
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
