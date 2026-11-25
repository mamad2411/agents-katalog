---
name: groundwater-wells-aquifers-and-registry-api
description: "Groundwater Wells, Aquifers and Registry API skill. Use when working with Groundwater Wells, Aquifers and Registry for aquifer-codes, aquifers, cities. Covers 24 endpoints."
version: 1.0.0
generator: lapsh
---

# Groundwater Wells, Aquifers and Registry API
API version: v1

## Auth
ApiKey JWT in header

## Base URL
https://apps.nrs.gov.bc.ca/gwells/api/v1/

## Setup
1. Set your API key in the appropriate header
2. GET /aquifer-codes/demand/ -- verify access

## Endpoints

24 endpoints across 9 groups. See references/api-spec.lap for full details.

### aquifer-codes
| Method | Path | Description |
|--------|------|-------------|
| GET | /aquifer-codes/demand/ | return a list of aquifer demand codes |
| GET | /aquifer-codes/materials/ | return a list of aquifer material codes |
| GET | /aquifer-codes/productivity/ | return a list of aquifer productivity codes |
| GET | /aquifer-codes/quality-concerns/ | return a list of quality concern codes |
| GET | /aquifer-codes/subtypes/ | return a list of aquifer subtype codes |
| GET | /aquifer-codes/vulnerability/ | return a list of aquifer vulnerability codes |
| GET | /aquifer-codes/water-use/ | return a list of water use codes |

### aquifers
| Method | Path | Description |
|--------|------|-------------|
| GET | /aquifers/ | return a list of aquifers |
| GET | /aquifers/names/ | List all aquifers in a simplified format |
| GET | /aquifers/{aquifer_id}/ | return details of aquifers |
| GET | /aquifers/{aquifer_id}/files | list files found for the aquifer identified in the uri |

### cities
| Method | Path | Description |
|--------|------|-------------|
| GET | /cities/drillers/ | returns a list of cities with a qualified, registered operator (driller or installer) |
| GET | /cities/installers/ | returns a list of cities with a qualified, registered operator (driller or installer) |

### config
| Method | Path | Description |
|--------|------|-------------|
| GET | /config | serves general configuration |

### drillers
| Method | Path | Description |
|--------|------|-------------|
| GET | /drillers/ | Returns a list of all person records |
| GET | /drillers/names/ | Search for a person in the Register |
| GET | /drillers/{person_guid}/files/ | list files found for the aquifer identified in the uri |

### keycloak
| Method | Path | Description |
|--------|------|-------------|
| GET | /keycloak | serves keycloak config |

### submissions
| Method | Path | Description |
|--------|------|-------------|
| GET | /submissions/options/ | Options required for submitting activity report forms |

### surveys
| Method | Path | Description |
|--------|------|-------------|
| GET | /surveys/ | returns a list of active surveys |

### wells
| Method | Path | Description |
|--------|------|-------------|
| GET | /wells/ | returns a list of wells |
| GET | /wells/tags/ | seach for wells by tag or owner |
| GET | /wells/{tag}/files | list files found for the well identified in the uri |
| GET | /wells/{well_tag_number} | Return well detail. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all demand?" -> GET /aquifer-codes/demand/
- "List all materials?" -> GET /aquifer-codes/materials/
- "List all productivity?" -> GET /aquifer-codes/productivity/
- "List all quality-concerns?" -> GET /aquifer-codes/quality-concerns/
- "List all subtypes?" -> GET /aquifer-codes/subtypes/
- "List all vulnerability?" -> GET /aquifer-codes/vulnerability/
- "List all water-use?" -> GET /aquifer-codes/water-use/
- "Search aquifers?" -> GET /aquifers/
- "Search names?" -> GET /aquifers/names/
- "Get aquifer details?" -> GET /aquifers/{aquifer_id}/
- "List all files?" -> GET /aquifers/{aquifer_id}/files
- "List all drillers?" -> GET /cities/drillers/
- "List all installers?" -> GET /cities/installers/
- "List all config?" -> GET /config
- "Search drillers?" -> GET /drillers/
- "Search names?" -> GET /drillers/names/
- "List all files?" -> GET /drillers/{person_guid}/files/
- "List all keycloak?" -> GET /keycloak
- "List all options?" -> GET /submissions/options/
- "List all surveys?" -> GET /surveys/
- "List all wells?" -> GET /wells/
- "Search tags?" -> GET /wells/tags/
- "List all files?" -> GET /wells/{tag}/files
- "Get well details?" -> GET /wells/{well_tag_number}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
