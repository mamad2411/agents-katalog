---
name: tcgdex-api
description: "TCGdex API skill. Use when working with TCGdex for cards, sets, series. Covers 33 endpoints."
version: 1.0.0
generator: lapsh
---

# TCGdex API
API version: 2

## Auth
No authentication required.

## Base URL
https://api.tcgdex.net/v2/en

## Setup
1. No auth setup needed
2. GET /cards -- verify access

## Endpoints

33 endpoints across 16 groups. See references/api-spec.lap for full details.

### cards
| Method | Path | Description |
|--------|------|-------------|
| GET | /cards | fetch the list of cards |
| GET | /cards/{cardId} | Find card by ID |

### sets
| Method | Path | Description |
|--------|------|-------------|
| GET | /sets | Get all sets |
| GET | /sets/{set} | Find set by ID |
| GET | /sets/{set}/{cardLocalId} | Find card by set and local ID |

### series
| Method | Path | Description |
|--------|------|-------------|
| GET | /series | Get all series |
| GET | /series/{serie} | Find series by ID |

### categories
| Method | Path | Description |
|--------|------|-------------|
| GET | /categories | Get all categories |
| GET | /categories/{category} | Get cards by category |

### hp
| Method | Path | Description |
|--------|------|-------------|
| GET | /hp | Get all HP values |
| GET | /hp/{hp} | Get cards by HP value |

### illustrators
| Method | Path | Description |
|--------|------|-------------|
| GET | /illustrators | Get all illustrators |
| GET | /illustrators/{illustrator} | Get cards by illustrator |

### rarities
| Method | Path | Description |
|--------|------|-------------|
| GET | /rarities | Get all rarities |
| GET | /rarities/{rarity} | Get cards by rarity |

### retreats
| Method | Path | Description |
|--------|------|-------------|
| GET | /retreats | Get all retreat costs |
| GET | /retreats/{retreat} | Get cards by retreat cost |

### types
| Method | Path | Description |
|--------|------|-------------|
| GET | /types | Get all types |
| GET | /types/{type} | Get cards by type |

### dex-ids
| Method | Path | Description |
|--------|------|-------------|
| GET | /dex-ids | Get all Pokedex IDs |
| GET | /dex-ids/{dexId} | Get cards by Pokedex ID |

### energy-types
| Method | Path | Description |
|--------|------|-------------|
| GET | /energy-types | Get all energy types |
| GET | /energy-types/{energy-type} | Get cards by energy type |

### regulation-marks
| Method | Path | Description |
|--------|------|-------------|
| GET | /regulation-marks | Get all regulation marks |
| GET | /regulation-marks/{regulation-mark} | Get cards by regulation mark |

### stages
| Method | Path | Description |
|--------|------|-------------|
| GET | /stages | Get all Pokemon stages |
| GET | /stages/{stage} | Get cards by stage |

### suffixes
| Method | Path | Description |
|--------|------|-------------|
| GET | /suffixes | Get all card suffixes |
| GET | /suffixes/{suffix} | Get cards by suffix |

### trainer-types
| Method | Path | Description |
|--------|------|-------------|
| GET | /trainer-types | Get all trainer types |
| GET | /trainer-types/{trainer-type} | Get cards by trainer type |

### variants
| Method | Path | Description |
|--------|------|-------------|
| GET | /variants | Get all card variants |
| GET | /variants/{variant} | Get cards by variant |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all cards?" -> GET /cards
- "Get card details?" -> GET /cards/{cardId}
- "List all sets?" -> GET /sets
- "Get set details?" -> GET /sets/{set}
- "Get set details?" -> GET /sets/{set}/{cardLocalId}
- "List all series?" -> GET /series
- "Get sery details?" -> GET /series/{serie}
- "List all categories?" -> GET /categories
- "Get category details?" -> GET /categories/{category}
- "List all hp?" -> GET /hp
- "Get hp details?" -> GET /hp/{hp}
- "List all illustrators?" -> GET /illustrators
- "Get illustrator details?" -> GET /illustrators/{illustrator}
- "List all rarities?" -> GET /rarities
- "Get rarity details?" -> GET /rarities/{rarity}
- "List all retreats?" -> GET /retreats
- "Get retreat details?" -> GET /retreats/{retreat}
- "List all types?" -> GET /types
- "Get type details?" -> GET /types/{type}
- "List all dex-ids?" -> GET /dex-ids
- "Get dex-id details?" -> GET /dex-ids/{dexId}
- "List all energy-types?" -> GET /energy-types
- "Get energy-type details?" -> GET /energy-types/{energy-type}
- "List all regulation-marks?" -> GET /regulation-marks
- "Get regulation-mark details?" -> GET /regulation-marks/{regulation-mark}
- "List all stages?" -> GET /stages
- "Get stage details?" -> GET /stages/{stage}
- "List all suffixes?" -> GET /suffixes
- "Get suffixe details?" -> GET /suffixes/{suffix}
- "List all trainer-types?" -> GET /trainer-types
- "Get trainer-type details?" -> GET /trainer-types/{trainer-type}
- "List all variants?" -> GET /variants
- "Get variant details?" -> GET /variants/{variant}

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
