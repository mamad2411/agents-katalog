---
name: browshot-api
description: "Browshot API skill. Use when working with Browshot for screenshot, batch, account. Covers 17 endpoints."
version: 1.0.0
generator: lapsh
---

# Browshot API
API version: 1.17.0

## Auth
ApiKey key in query

## Base URL
https://api.browshot.com/api/v1

## Setup
1. Set your API key in the appropriate header
2. GET /screenshot/create -- verify access
3. POST /batch/ceate -- create first ceate

## Endpoints

17 endpoints across 5 groups. See references/api-spec.lap for full details.

### screenshot
| Method | Path | Description |
|--------|------|-------------|
| GET | /screenshot/create | Request a screenshot |
| GET | /screenshot/multiple | Request multiple screenshots |
| GET | /screenshot/info | Query screenshot status |
| GET | /screenshot/list | Get information about screenshots |
| GET | /screenshot/search | Search for screenshots |
| GET | /screenshot/host | Host thumbnails on your own S3 account or on Browshot. |
| GET | /screenshot/thumbnail | Retrieve a thumbnail image |
| GET | /screenshot/share | Share a screenshot |
| GET | /screenshot/delete | Delete screenshot data |
| GET | /screenshot/html | Get the HTML code |

### batch
| Method | Path | Description |
|--------|------|-------------|
| POST | /batch/ceate | Requests thousands of screenshtos at once |
| GET | /batch/info | Get the batch status |

### account
| Method | Path | Description |
|--------|------|-------------|
| GET | /account/info | Get information about your account |

### instance
| Method | Path | Description |
|--------|------|-------------|
| GET | /instance/info | Get information about an instance |
| GET | /instance/list | Get all instances |

### browser
| Method | Path | Description |
|--------|------|-------------|
| GET | /browser/info | Get information about a browser |
| GET | /browser/list | Get all browsers |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all create?" -> GET /screenshot/create
- "List all multiple?" -> GET /screenshot/multiple
- "List all info?" -> GET /screenshot/info
- "List all list?" -> GET /screenshot/list
- "List all search?" -> GET /screenshot/search
- "List all host?" -> GET /screenshot/host
- "List all thumbnail?" -> GET /screenshot/thumbnail
- "List all share?" -> GET /screenshot/share
- "List all delete?" -> GET /screenshot/delete
- "List all html?" -> GET /screenshot/html
- "Create a ceate?" -> POST /batch/ceate
- "List all info?" -> GET /batch/info
- "List all info?" -> GET /account/info
- "List all info?" -> GET /instance/info
- "List all list?" -> GET /instance/list
- "List all info?" -> GET /browser/info
- "List all list?" -> GET /browser/list
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
