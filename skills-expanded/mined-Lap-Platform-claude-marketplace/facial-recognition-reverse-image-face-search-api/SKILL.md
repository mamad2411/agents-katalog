---
name: facial-recognition-reverse-image-face-search-api
description: "Facial Recognition Reverse Image Face Search API skill. Use when working with Facial Recognition Reverse Image Face Search for api. Covers 4 endpoints."
version: 1.0.0
generator: lapsh
---

# Facial Recognition Reverse Image Face Search API
API version: v1.02

## Auth
ApiKey Authorization in header

## Base URL
Not specified.

## Setup
1. Set your API key in the appropriate header
3. POST /api/upload_pic -- create first upload_pic

## Endpoints

4 endpoints across 1 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| POST | /api/upload_pic |  |
| POST | /api/delete_pic | Remove an image from a search request |
| POST | /api/info | Returns remaining search credits, search engine online status, and number of indexed faces |
| POST | /api/search |  |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a upload_pic?" -> POST /api/upload_pic
- "Create a delete_pic?" -> POST /api/delete_pic
- "Create a info?" -> POST /api/info
- "Create a search?" -> POST /api/search
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
