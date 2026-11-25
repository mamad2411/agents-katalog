---
name: ipinfodb-ip-address-lookup
description: "IPInfoDB IP Address Lookup API skill. Use when working with IPInfoDB IP Address Lookup for ip-city, ip-country. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# IPInfoDB IP Address Lookup
API version: 1.0

## Auth
ApiKey key in query

## Base URL
https://api.ipinfodb.com

## Setup
1. Set your API key in the appropriate header
2. GET /v3/ip-city/ -- verify access

## Endpoints

2 endpoints across 2 groups. See references/api-spec.lap for full details.

### ip-city
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/ip-city/ | Get location of an IP address |

### ip-country
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/ip-country/ | Get country of an IP address |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all ip-city?" -> GET /v3/ip-city/
- "List all ip-country?" -> GET /v3/ip-country/
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
