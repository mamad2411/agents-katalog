---
name: nookipedia
description: "Nookipedia API skill. Use when working with Nookipedia for villagers, nh. Covers 32 endpoints."
version: 1.0.0
generator: lapsh
---

# Nookipedia
API version: 1.7.0

## Auth
ApiKey X-API-KEY in header

## Base URL
https://api.nookipedia.com/

## Setup
1. Set your API key in the appropriate header
2. GET /villagers -- verify access

## Endpoints

32 endpoints across 2 groups. See references/api-spec.lap for full details.

### villagers
| Method | Path | Description |
|--------|------|-------------|
| GET | /villagers | Villagers |

### nh
| Method | Path | Description |
|--------|------|-------------|
| GET | /nh/fish | All New Horizons fish |
| GET | /nh/fish/{fish} | Single New Horizons fish |
| GET | /nh/bugs | All New Horizons bugs |
| GET | /nh/bugs/{bug} | Single New Horizons bug |
| GET | /nh/sea | All New Horizons sea creatures |
| GET | /nh/sea/{sea_creature} | Single New Horizons sea creature |
| GET | /nh/events | All New Horizons events |
| GET | /nh/art | All New Horizons artwork |
| GET | /nh/art/{artwork} | Single New Horizons artwork |
| GET | /nh/furniture | All New Horizons furniture |
| GET | /nh/furniture/{furniture} | Single New Horizons furniture |
| GET | /nh/clothing | All New Horizons clothing |
| GET | /nh/clothing/{clothing} | Single New Horizons clothing |
| GET | /nh/interior | All New Horizons interior items |
| GET | /nh/interior/{item} | Single New Horizons interior item |
| GET | /nh/tools | All New Horizons tools |
| GET | /nh/tools/{tool} | Single New Horizons tool |
| GET | /nh/photos | All New Horizons photos and posters |
| GET | /nh/photos/{item} | Single New Horizons photo or poster |
| GET | /nh/items | Miscellaneous New Horizons items |
| GET | /nh/items/{item} | Single New Horizons miscellaneous item |
| GET | /nh/recipes | All New Horizons recipes |
| GET | /nh/recipes/{item} | Single New Horizons recipe |
| GET | /nh/fossils/individuals | All New Horizons fossils |
| GET | /nh/fossils/individuals/{fossil} | Single New Horizons fossil |
| GET | /nh/fossils/groups | All New Horizons fossil groups |
| GET | /nh/fossils/groups/{fossil_group} | Single New Horizons fossil group |
| GET | /nh/fossils/all | All New Horizons fossil groups or individual fossil |
| GET | /nh/fossils/all/{fossil} | Single New Horizons fossil group with individual fossils |
| GET | /nh/gyroids | All New Horizons gyroids |
| GET | /nh/gyroids/{gyroid} | Single New Horizons gyroid |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all villagers?" -> GET /villagers
- "List all fish?" -> GET /nh/fish
- "Get fish details?" -> GET /nh/fish/{fish}
- "List all bugs?" -> GET /nh/bugs
- "Get bug details?" -> GET /nh/bugs/{bug}
- "List all sea?" -> GET /nh/sea
- "Get sea details?" -> GET /nh/sea/{sea_creature}
- "List all events?" -> GET /nh/events
- "List all art?" -> GET /nh/art
- "Get art details?" -> GET /nh/art/{artwork}
- "List all furniture?" -> GET /nh/furniture
- "Get furniture details?" -> GET /nh/furniture/{furniture}
- "List all clothing?" -> GET /nh/clothing
- "Get clothing details?" -> GET /nh/clothing/{clothing}
- "List all interior?" -> GET /nh/interior
- "Get interior details?" -> GET /nh/interior/{item}
- "List all tools?" -> GET /nh/tools
- "Get tool details?" -> GET /nh/tools/{tool}
- "List all photos?" -> GET /nh/photos
- "Get photo details?" -> GET /nh/photos/{item}
- "List all items?" -> GET /nh/items
- "Get item details?" -> GET /nh/items/{item}
- "List all recipes?" -> GET /nh/recipes
- "Get recipe details?" -> GET /nh/recipes/{item}
- "List all individuals?" -> GET /nh/fossils/individuals
- "Get individual details?" -> GET /nh/fossils/individuals/{fossil}
- "List all groups?" -> GET /nh/fossils/groups
- "Get group details?" -> GET /nh/fossils/groups/{fossil_group}
- "List all all?" -> GET /nh/fossils/all
- "Get all details?" -> GET /nh/fossils/all/{fossil}
- "List all gyroids?" -> GET /nh/gyroids
- "Get gyroid details?" -> GET /nh/gyroids/{gyroid}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
