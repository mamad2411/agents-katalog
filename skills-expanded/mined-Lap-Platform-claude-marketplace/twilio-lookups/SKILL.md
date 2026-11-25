---
name: twilio-lookups
description: "Twilio - Lookups API skill. Use when working with Twilio - Lookups for PhoneNumbers, batch, RateLimits. Covers 10 endpoints."
version: 1.0.0
generator: lapsh
---

# Twilio - Lookups
API version: 1.0.0

## Auth
Bearer basic

## Base URL
https://lookups.twilio.com

## Setup
1. Set Authorization header with your Bearer token
2. GET /v2/RateLimits -- verify access
3. POST /v2/batch/query -- create first query

## Endpoints

10 endpoints across 3 groups. See references/api-spec.lap for full details.

### PhoneNumbers
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/PhoneNumbers/{PhoneNumber} | Full API documentation: https://www.twilio.com/docs/lookup/v2-api |
| GET | /v2/PhoneNumbers/{PhoneNumber}/Overrides/{Field} | Get Overrides for a Phone Number for a specific field. |
| POST | /v2/PhoneNumbers/{PhoneNumber}/Overrides/{Field} | Create Override for a Phone Number for a specific field |
| PUT | /v2/PhoneNumbers/{PhoneNumber}/Overrides/{Field} | Update Override for a Phone Number for a specific field |
| DELETE | /v2/PhoneNumbers/{PhoneNumber}/Overrides/{Field} | Delete an Override for a Phone Number for a specific field |

### batch
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/batch/query | In Request Bulk |

### RateLimits
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/RateLimits | Get account rate limits |
| GET | /v2/RateLimits/Fields/{Field}/Bucket/{Bucket} | Get rate limit |
| DELETE | /v2/RateLimits/Fields/{Field}/Bucket/{Bucket} | Delete rate limit |
| PUT | /v2/RateLimits/Fields/{Field}/Bucket/{Bucket} | Upsert rate limit |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get PhoneNumber details?" -> GET /v2/PhoneNumbers/{PhoneNumber}
- "Create a query?" -> POST /v2/batch/query
- "List all RateLimits?" -> GET /v2/RateLimits
- "Get Bucket details?" -> GET /v2/RateLimits/Fields/{Field}/Bucket/{Bucket}
- "Delete a Bucket?" -> DELETE /v2/RateLimits/Fields/{Field}/Bucket/{Bucket}
- "Update a Bucket?" -> PUT /v2/RateLimits/Fields/{Field}/Bucket/{Bucket}
- "Get Override details?" -> GET /v2/PhoneNumbers/{PhoneNumber}/Overrides/{Field}
- "Update a Override?" -> PUT /v2/PhoneNumbers/{PhoneNumber}/Overrides/{Field}
- "Delete a Override?" -> DELETE /v2/PhoneNumbers/{PhoneNumber}/Overrides/{Field}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
