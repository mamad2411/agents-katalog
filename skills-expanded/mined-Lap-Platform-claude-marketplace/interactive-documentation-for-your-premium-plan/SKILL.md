---
name: interactive-documentation-for-your-premium-plan
description: "Interactive documentation for your Premium plan API skill. Use when working with Interactive documentation for your Premium plan for point, find_places, find_places_prefix. Covers 7 endpoints."
version: 1.0.0
generator: lapsh
---

# Interactive documentation for your Premium plan
API version: v1

## Auth
ApiKey Authorization in header

## Base URL
/api/v1/premium

## Setup
1. Set your API key in the appropriate header
2. GET /point -- verify access

## Endpoints

7 endpoints across 7 groups. See references/api-spec.lap for full details.

### point
| Method | Path | Description |
|--------|------|-------------|
| GET | /point | Returns weather data for a single point (geographic name or GPS) |

### find_places
| Method | Path | Description |
|--------|------|-------------|
| GET | /find_places | Search for places. Complete words required. |

### find_places_prefix
| Method | Path | Description |
|--------|------|-------------|
| GET | /find_places_prefix | Prefix search for places. Useful for autocomplete forms. |

### nearest_place
| Method | Path | Description |
|--------|------|-------------|
| GET | /nearest_place | Returns the nearest named location for a given GPS coordinates. |

### map
| Method | Path | Description |
|--------|------|-------------|
| GET | /map | Returns PNG weather map for given area and variable |

### time_machine
| Method | Path | Description |
|--------|------|-------------|
| GET | /time_machine | Returns weather data for a single location and given day in the past |

### air_quality
| Method | Path | Description |
|--------|------|-------------|
| GET | /air_quality | Returns air quality data for a single point (geographic name or GPS) |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all point?" -> GET /point
- "List all find_places?" -> GET /find_places
- "List all find_places_prefix?" -> GET /find_places_prefix
- "List all nearest_place?" -> GET /nearest_place
- "List all map?" -> GET /map
- "List all time_machine?" -> GET /time_machine
- "List all air_quality?" -> GET /air_quality
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
