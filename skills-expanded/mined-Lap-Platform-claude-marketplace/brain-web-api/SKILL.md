---
name: brain-web-api
description: "Brain Web API skill. Use when working with Brain Web for authinfo, blobs, events. Covers 77 endpoints."
version: 1.0.0
generator: lapsh
---

# Brain Web API
API version: 2.27.2+0.gd5006bf.dirty

## Auth
ApiKey key in query | ApiKey X-Api-Key in header | ApiKey brain.sid in cookie

## Base URL
https://brain.intellifi.cloud/api

## Setup
1. Set your API key in the appropriate header
2. GET /authinfo -- verify access
3. POST /blobs -- create first blobs

## Endpoints

77 endpoints across 15 groups. See references/api-spec.lap for full details.

### authinfo
| Method | Path | Description |
|--------|------|-------------|
| GET | /authinfo | Authentication information |

### blobs
| Method | Path | Description |
|--------|------|-------------|
| GET | /blobs | Get all binary large objects (blob) |
| POST | /blobs | Create binary large object (blob) metadata |
| GET | /blobs/{id} | Get binary large object (blob) |
| DELETE | /blobs/{id} | Delete binary large object (blob) |
| GET | /blobs/{id}/download/{filename} | Download a binary large object (blob) |
| POST | /blobs/{id}/upload | Create binary large object (blob) |

### events
| Method | Path | Description |
|--------|------|-------------|
| GET | /events | Get all events |
| GET | /events/{id} | Get event |

### items
| Method | Path | Description |
|--------|------|-------------|
| GET | /items | Get all items |
| POST | /items | Create item |
| GET | /items/{id} | Get item |
| PUT | /items/{id} | Update existing item |
| DELETE | /items/{id} | Delete item |

### keys
| Method | Path | Description |
|--------|------|-------------|
| GET | /keys | Get all keys |
| POST | /keys | Create key |
| GET | /keys/{id} | Get key |
| PUT | /keys/{id} | Update existing key |
| DELETE | /keys/{id} | Delete key |

### kvpairs
| Method | Path | Description |
|--------|------|-------------|
| GET | /kvpairs | Get all key-value pairs |
| POST | /kvpairs | Create key-value pair |
| GET | /kvpairs/{id} | Get key-value pair |
| PUT | /kvpairs/{id} | Update existing Key-value pair |
| DELETE | /kvpairs/{id} | Delete key-value pair |

### locations
| Method | Path | Description |
|--------|------|-------------|
| GET | /locations | Get all locations |
| POST | /locations | Create location |
| GET | /locations/{id} | Get location |
| PUT | /locations/{id} | Update existing location |
| DELETE | /locations/{id} | Delete location |

### locationrules
| Method | Path | Description |
|--------|------|-------------|
| GET | /locationrules | Get all location rules |
| POST | /locationrules | Create location rule |
| GET | /locationrules/{id} | Get location rule |
| PUT | /locationrules/{id} | Update existing location rule |
| DELETE | /locationrules/{id} | Delete location rule |

### presences
| Method | Path | Description |
|--------|------|-------------|
| GET | /presences | Get all presences |
| GET | /presences/{id} | Get presence |

### services
| Method | Path | Description |
|--------|------|-------------|
| GET | /services | Get all services |
| GET | /services/{id} | Get service |
| PUT | /services/{id} | Update existing service |

### sets
| Method | Path | Description |
|--------|------|-------------|
| GET | /sets/itemlists | Get all item lists |
| POST | /sets/itemlists | Create item list |
| GET | /sets/itemlists/{id} | Get item list |
| PUT | /sets/itemlists/{id} | Update existing item list |
| DELETE | /sets/itemlists/{id} | Delete item list |
| GET | /sets/itemlists/{id}/ids | Get item ids for this list |
| POST | /sets/itemlists/{id}/ids | Add items to an existing list |
| DELETE | /sets/itemlists/{id}/ids/{itemId} | Delete item from list |
| GET | /sets/spotlists | Get all spot lists |
| POST | /sets/spotlists | Create spot list |
| GET | /sets/spotlists/{id} | Info for a specific spot list |
| PUT | /sets/spotlists/{id} | Update existing spot list |
| DELETE | /sets/spotlists/{id} | Delete spot list |
| GET | /sets/spotlists/{id}/ids | Get spot ids for this list |
| POST | /sets/spotlists/{id}/ids | Add spots to an existing list |
| DELETE | /sets/spotlists/{id}/ids/{itemId} | Delete spot from list |

### spots
| Method | Path | Description |
|--------|------|-------------|
| GET | /spots | Get all spots |
| GET | /spots/{id} | Get spot |
| PUT | /spots/{id} | Update existing spot |
| GET | /spots/{id}/sets | Get spotsets |
| POST | /spots/{id}/sets | Create spotset |
| PUT | /spots/{id}/sets/{setId} | Update existing spotset |
| GET | /spots/{id}/sets/{setId} | Get spotset |

### spotsets
| Method | Path | Description |
|--------|------|-------------|
| GET | /spotsets | Get spotsets |
| POST | /spotsets | Create spotset |
| PUT | /spotsets/{id} | Update existing spotset |
| GET | /spotsets/{id} | Get spotset |

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions | Get all subscriptions |
| POST | /subscriptions | Create subscription |
| GET | /subscriptions/{id} | Get subscription |
| PUT | /subscriptions/{id} | Update existing subscription |
| DELETE | /subscriptions/{id} | Delete subscription |
| GET | /subscriptions/{id}/events | Get subscription events |

### users
| Method | Path | Description |
|--------|------|-------------|
| GET | /users | Get all users |
| POST | /users | Create user |
| GET | /users/{id} | Get user |
| PUT | /users/{id} | Update existing user |
| DELETE | /users/{id} | Delete user |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all authinfo?" -> GET /authinfo
- "List all blobs?" -> GET /blobs
- "Create a blob?" -> POST /blobs
- "Get blob details?" -> GET /blobs/{id}
- "Delete a blob?" -> DELETE /blobs/{id}
- "Get download details?" -> GET /blobs/{id}/download/{filename}
- "Create a upload?" -> POST /blobs/{id}/upload
- "List all events?" -> GET /events
- "Get event details?" -> GET /events/{id}
- "List all items?" -> GET /items
- "Create a item?" -> POST /items
- "Get item details?" -> GET /items/{id}
- "Update a item?" -> PUT /items/{id}
- "Delete a item?" -> DELETE /items/{id}
- "List all keys?" -> GET /keys
- "Create a key?" -> POST /keys
- "Get key details?" -> GET /keys/{id}
- "Update a key?" -> PUT /keys/{id}
- "Delete a key?" -> DELETE /keys/{id}
- "List all kvpairs?" -> GET /kvpairs
- "Create a kvpair?" -> POST /kvpairs
- "Get kvpair details?" -> GET /kvpairs/{id}
- "Update a kvpair?" -> PUT /kvpairs/{id}
- "Delete a kvpair?" -> DELETE /kvpairs/{id}
- "List all locations?" -> GET /locations
- "Create a location?" -> POST /locations
- "Get location details?" -> GET /locations/{id}
- "Update a location?" -> PUT /locations/{id}
- "Delete a location?" -> DELETE /locations/{id}
- "List all locationrules?" -> GET /locationrules
- "Create a locationrule?" -> POST /locationrules
- "Get locationrule details?" -> GET /locationrules/{id}
- "Update a locationrule?" -> PUT /locationrules/{id}
- "Delete a locationrule?" -> DELETE /locationrules/{id}
- "List all presences?" -> GET /presences
- "Get presence details?" -> GET /presences/{id}
- "List all services?" -> GET /services
- "Get service details?" -> GET /services/{id}
- "Update a service?" -> PUT /services/{id}
- "List all itemlists?" -> GET /sets/itemlists
- "Create a itemlist?" -> POST /sets/itemlists
- "Get itemlist details?" -> GET /sets/itemlists/{id}
- "Update a itemlist?" -> PUT /sets/itemlists/{id}
- "Delete a itemlist?" -> DELETE /sets/itemlists/{id}
- "List all ids?" -> GET /sets/itemlists/{id}/ids
- "Create a id?" -> POST /sets/itemlists/{id}/ids
- "Delete a id?" -> DELETE /sets/itemlists/{id}/ids/{itemId}
- "List all spotlists?" -> GET /sets/spotlists
- "Create a spotlist?" -> POST /sets/spotlists
- "Get spotlist details?" -> GET /sets/spotlists/{id}
- "Update a spotlist?" -> PUT /sets/spotlists/{id}
- "Delete a spotlist?" -> DELETE /sets/spotlists/{id}
- "List all ids?" -> GET /sets/spotlists/{id}/ids
- "Create a id?" -> POST /sets/spotlists/{id}/ids
- "Delete a id?" -> DELETE /sets/spotlists/{id}/ids/{itemId}
- "List all spots?" -> GET /spots
- "Get spot details?" -> GET /spots/{id}
- "Update a spot?" -> PUT /spots/{id}
- "List all sets?" -> GET /spots/{id}/sets
- "Create a set?" -> POST /spots/{id}/sets
- "Update a set?" -> PUT /spots/{id}/sets/{setId}
- "Get set details?" -> GET /spots/{id}/sets/{setId}
- "List all spotsets?" -> GET /spotsets
- "Create a spotset?" -> POST /spotsets
- "Update a spotset?" -> PUT /spotsets/{id}
- "Get spotset details?" -> GET /spotsets/{id}
- "List all subscriptions?" -> GET /subscriptions
- "Create a subscription?" -> POST /subscriptions
- "Get subscription details?" -> GET /subscriptions/{id}
- "Update a subscription?" -> PUT /subscriptions/{id}
- "Delete a subscription?" -> DELETE /subscriptions/{id}
- "List all events?" -> GET /subscriptions/{id}/events
- "List all users?" -> GET /users
- "Create a user?" -> POST /users
- "Get user details?" -> GET /users/{id}
- "Update a user?" -> PUT /users/{id}
- "Delete a user?" -> DELETE /users/{id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
