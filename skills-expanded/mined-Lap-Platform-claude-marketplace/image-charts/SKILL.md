---
name: image-charts
description: "Image-Charts API skill. Use when working with Image-Charts for chart, chart.js. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# Image-Charts
API version: 6.1.19

## Auth
No authentication required.

## Base URL
https://image-charts.com/

## Setup
1. No auth setup needed
2. GET /chart -- verify access

## Endpoints

2 endpoints across 2 groups. See references/api-spec.lap for full details.

### chart
| Method | Path | Description |
|--------|------|-------------|
| GET | /chart | Image-Charts API |

### chart.js
| Method | Path | Description |
|--------|------|-------------|
| GET | /chart.js/2.8.0 | Chart.js as image API |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all chart?" -> GET /chart
- "List all 2.8.0?" -> GET /chart.js/2.8.0

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
