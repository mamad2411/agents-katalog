---
name: cycatorg-api
description: "CyCAT.org API skill. Use when working with CyCAT.org for child, generate, info. Covers 14 endpoints."
version: 1.0.0
generator: lapsh
---

# CyCAT.org API
API version: 0.9

## Auth
No authentication required.

## Base URL
Not specified.

## Setup
1. No auth setup needed
2. GET /generate/uuid -- verify access
3. POST /propose -- create first propose

## Endpoints

14 endpoints across 10 groups. See references/api-spec.lap for full details.

### child
| Method | Path | Description |
|--------|------|-------------|
| GET | /child/{uuid} | Get child UUID(s) from a specified project or publisher UUID. |

### generate
| Method | Path | Description |
|--------|------|-------------|
| GET | /generate/uuid | Generate an UUID version 4 RFC4122-compliant. |

### info
| Method | Path | Description |
|--------|------|-------------|
| GET | /info | Get information about the CyCAT backend services including status, overall statistics and version. |

### list
| Method | Path | Description |
|--------|------|-------------|
| GET | /list/project/{start}/{end} | List projects registered in CyCAT by pagination (start,end). |
| GET | /list/publisher/{start}/{end} | List publishers registered in CyCAT by pagination (start,end). |

### lookup
| Method | Path | Description |
|--------|------|-------------|
| GET | /lookup/{uuid} | Lookup UUID registered in CyCAT. |

### namespace
| Method | Path | Description |
|--------|------|-------------|
| GET | /namespace/finduuid/{namespace}/{namespaceid} | Get all known UUID for a given namespace id. |
| GET | /namespace/getall | List all known namespaces. |
| GET | /namespace/getid/{namespace} | Get all ID from a given namespace. |

### parent
| Method | Path | Description |
|--------|------|-------------|
| GET | /parent/{uuid} | Get parent UUID(s) from a specified project or item UUID. |

### propose
| Method | Path | Description |
|--------|------|-------------|
| POST | /propose | Propose new resource to CyCAT. |

### relationships
| Method | Path | Description |
|--------|------|-------------|
| GET | /relationships/expanded/{uuid} | Get relationship(s) UUID from a specified UUID including the relationships meta information. |
| GET | /relationships/{uuid} | Get relationship(s) UUID from a specified UUID. |

### search
| Method | Path | Description |
|--------|------|-------------|
| GET | /search/{searchquery} | Full-text search in CyCAT and return matching UUID. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get child details?" -> GET /child/{uuid}
- "List all uuid?" -> GET /generate/uuid
- "List all info?" -> GET /info
- "Get project details?" -> GET /list/project/{start}/{end}
- "Get publisher details?" -> GET /list/publisher/{start}/{end}
- "Get lookup details?" -> GET /lookup/{uuid}
- "Get finduuid details?" -> GET /namespace/finduuid/{namespace}/{namespaceid}
- "List all getall?" -> GET /namespace/getall
- "Get getid details?" -> GET /namespace/getid/{namespace}
- "Get parent details?" -> GET /parent/{uuid}
- "Create a propose?" -> POST /propose
- "Get expanded details?" -> GET /relationships/expanded/{uuid}
- "Get relationship details?" -> GET /relationships/{uuid}
- "Get search details?" -> GET /search/{searchquery}

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
