---
name: ingestion-api
description: "Ingestion API skill. Use when working with Ingestion for import, track, engage#profile-set. Covers 20 endpoints."
version: 1.0.0
generator: lapsh
---

# Ingestion API
API version: 1.0.0

## Auth
No authentication required.

## Base URL
https://api.mixpanel.com

## Setup
1. No auth setup needed
2. GET /lookup-tables -- verify access
3. POST /import -- create first import

## Endpoints

20 endpoints across 19 groups. See references/api-spec.lap for full details.

### import
| Method | Path | Description |
|--------|------|-------------|
| POST | /import | Import Events |

### track
| Method | Path | Description |
|--------|------|-------------|
| POST | /track | Track Events |

### engage#profile-set
| Method | Path | Description |
|--------|------|-------------|
| POST | /engage#profile-set | Set Property |

### engage#profile-set-once
| Method | Path | Description |
|--------|------|-------------|
| POST | /engage#profile-set-once | Set Property Once |

### engage#profile-numerical-add
| Method | Path | Description |
|--------|------|-------------|
| POST | /engage#profile-numerical-add | Increment Numerical Property |

### engage#profile-union
| Method | Path | Description |
|--------|------|-------------|
| POST | /engage#profile-union | Union To List Property |

### engage#profile-list-append
| Method | Path | Description |
|--------|------|-------------|
| POST | /engage#profile-list-append | Append to List Property |

### engage#profile-list-remove
| Method | Path | Description |
|--------|------|-------------|
| POST | /engage#profile-list-remove | Remove from List Property |

### engage#profile-unset
| Method | Path | Description |
|--------|------|-------------|
| POST | /engage#profile-unset | Delete Property |

### engage#profile-batch-update
| Method | Path | Description |
|--------|------|-------------|
| POST | /engage#profile-batch-update | Update Multiple Profiles |

### engage#profile-delete
| Method | Path | Description |
|--------|------|-------------|
| POST | /engage#profile-delete | Delete Profile |

### groups#group-set
| Method | Path | Description |
|--------|------|-------------|
| POST | /groups#group-set | Update Property |

### groups#group-set-once
| Method | Path | Description |
|--------|------|-------------|
| POST | /groups#group-set-once | Set Property Once |

### groups#group-unset
| Method | Path | Description |
|--------|------|-------------|
| POST | /groups#group-unset | Delete Property |

### groups#group-remove-from-list
| Method | Path | Description |
|--------|------|-------------|
| POST | /groups#group-remove-from-list | Remove from List Property |

### groups#group-union
| Method | Path | Description |
|--------|------|-------------|
| POST | /groups#group-union | Union To List Property |

### groups#group-batch-update
| Method | Path | Description |
|--------|------|-------------|
| POST | /groups#group-batch-update | Batch Update Group Profiles |

### groups#group-delete
| Method | Path | Description |
|--------|------|-------------|
| POST | /groups#group-delete | Delete Group |

### lookup-tables
| Method | Path | Description |
|--------|------|-------------|
| GET | /lookup-tables | List Lookup Tables |
| PUT | /lookup-tables/{id} | Replace a Lookup Table |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a import?" -> POST /import
- "Create a track?" -> POST /track
- "Create a engage#profile-set?" -> POST /engage#profile-set
- "Create a engage#profile-set-once?" -> POST /engage#profile-set-once
- "Create a engage#profile-numerical-add?" -> POST /engage#profile-numerical-add
- "Create a engage#profile-union?" -> POST /engage#profile-union
- "Create a engage#profile-list-append?" -> POST /engage#profile-list-append
- "Create a engage#profile-list-remove?" -> POST /engage#profile-list-remove
- "Create a engage#profile-unset?" -> POST /engage#profile-unset
- "Create a engage#profile-batch-update?" -> POST /engage#profile-batch-update
- "Create a engage#profile-delete?" -> POST /engage#profile-delete
- "Create a groups#group-set?" -> POST /groups#group-set
- "Create a groups#group-set-once?" -> POST /groups#group-set-once
- "Create a groups#group-unset?" -> POST /groups#group-unset
- "Create a groups#group-remove-from-list?" -> POST /groups#group-remove-from-list
- "Create a groups#group-union?" -> POST /groups#group-union
- "Create a groups#group-batch-update?" -> POST /groups#group-batch-update
- "Create a groups#group-delete?" -> POST /groups#group-delete
- "List all lookup-tables?" -> GET /lookup-tables
- "Update a lookup-table?" -> PUT /lookup-tables/{id}

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
