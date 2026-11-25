---
name: hashlookup-circl-api
description: "hashlookup CIRCL API skill. Use when working with hashlookup CIRCL for bulk, children, info. Covers 11 endpoints."
version: 1.0.0
generator: lapsh
---

# hashlookup CIRCL API
API version: 1.3

## Auth
No authentication required.

## Base URL
Not specified.

## Setup
1. No auth setup needed
2. GET /info -- verify access
3. POST /bulk/md5 -- create first md5

## Endpoints

11 endpoints across 7 groups. See references/api-spec.lap for full details.

### bulk
| Method | Path | Description |
|--------|------|-------------|
| POST | /bulk/md5 | Bulk search of MD5 hashes in a JSON array with the key 'hashes'. |
| POST | /bulk/sha1 | Bulk search of SHA1 hashes in a JSON array with the 'hashes'. |

### children
| Method | Path | Description |
|--------|------|-------------|
| GET | /children/{sha1}/{count}/{cursor} | Return children from a given SHA1.  A number of element to return and an offset must be given. If not set it will be the 100 first elements. A cursor must be given to paginate over. The starting cursor is 0. |

### info
| Method | Path | Description |
|--------|------|-------------|
| GET | /info | Info about the hashlookup database |

### lookup
| Method | Path | Description |
|--------|------|-------------|
| GET | /lookup/md5/{md5} | Lookup MD5. |
| GET | /lookup/sha1/{sha1} | Lookup SHA-1. |
| GET | /lookup/sha256/{sha256} | Lookup SHA-256. |

### parents
| Method | Path | Description |
|--------|------|-------------|
| GET | /parents/{sha1}/{count}/{cursor} | Return parents from a given SHA1. A number of element to return and an offset must be given. If not set it will be the 100 first elements. A cursor must be given to paginate over. The starting cursor is 0. |

### session
| Method | Path | Description |
|--------|------|-------------|
| GET | /session/create/{name} | Create a session key to keep search context. The session is attached to a name. After the session is created, the header `hashlookup_session` can be set to the session name. |
| GET | /session/get/{name} | Return set of matching and non-matching hashes from a session. |

### stats
| Method | Path | Description |
|--------|------|-------------|
| GET | /stats/top | Return the top 100 of most queried values. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a md5?" -> POST /bulk/md5
- "Create a sha1?" -> POST /bulk/sha1
- "Get children details?" -> GET /children/{sha1}/{count}/{cursor}
- "List all info?" -> GET /info
- "Get md5 details?" -> GET /lookup/md5/{md5}
- "Get sha1 details?" -> GET /lookup/sha1/{sha1}
- "Get sha256 details?" -> GET /lookup/sha256/{sha256}
- "Get parent details?" -> GET /parents/{sha1}/{count}/{cursor}
- "Get create details?" -> GET /session/create/{name}
- "Get get details?" -> GET /session/get/{name}
- "List all top?" -> GET /stats/top

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
