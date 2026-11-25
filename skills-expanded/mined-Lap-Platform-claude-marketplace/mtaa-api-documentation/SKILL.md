---
name: mtaa-api-documentation
description: "Mtaa API Documentation API skill. Use when working with Mtaa API Documentation for {country}. Covers 5 endpoints."
version: 1.0.0
generator: lapsh
---

# Mtaa API Documentation
API version: 1.0

## Auth
No authentication required.

## Base URL
https://mtaa-api.herokuapp.com/api

## Setup
1. No auth setup needed
2. GET /{country} -- verify access

## Endpoints

5 endpoints across 1 groups. See references/api-spec.lap for full details.

### {country}
| Method | Path | Description |
|--------|------|-------------|
| GET | /{country} | Returns all regions present in Tanzania |
| GET | /{country}/{region} | Returns all districts in region |
| GET | /{country}/{region}/{district} | Returns all wards in a district |
| GET | /{country}/{region}/{district}/{ward} | Returns all streets in a ward |
| GET | /{country}/{region}/{district}/{ward}/{street} | Returns all neighborhood in a street |

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
