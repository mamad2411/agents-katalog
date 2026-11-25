---
name: daymet-single-pixel-extraction-tool-api
description: "Daymet Single Pixel Extraction Tool API skill. Use when working with Daymet Single Pixel Extraction Tool for api, preview, send. Covers 4 endpoints."
version: 1.0.0
generator: lapsh
---

# Daymet Single Pixel Extraction Tool API
API version: 1.0.2

## Auth
No authentication required.

## Base URL
https://daymet.ornl.gov/single-pixel

## Setup
1. No auth setup needed
2. GET /api/data -- verify access

## Endpoints

4 endpoints across 4 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/data | Download Daymet Data |

### preview
| Method | Path | Description |
|--------|------|-------------|
| GET | /preview | Preview Daymet Data in a web browser |

### send
| Method | Path | Description |
|--------|------|-------------|
| GET | /send/saveData | Download Daymet Data |

### visualize
| Method | Path | Description |
|--------|------|-------------|
| GET | /visualize | Visualize Daymet Data in a web browser |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all data?" -> GET /api/data
- "List all preview?" -> GET /preview
- "List all saveData?" -> GET /send/saveData
- "List all visualize?" -> GET /visualize

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
