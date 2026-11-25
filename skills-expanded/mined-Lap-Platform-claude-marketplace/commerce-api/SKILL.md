---
name: commerce-api
description: "Commerce API skill. Use when working with Commerce for commerce. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Commerce API
API version: v2

## Auth
ApiKey X-SSL-CERT-UID in header

## Base URL
https://www.ticketmaster.com/commerce/v2

## Setup
1. Set your API key in the appropriate header
2. GET /commerce/v2/events/{eventId}/offers -- verify access

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### commerce
| Method | Path | Description |
|--------|------|-------------|
| GET | /commerce/v2/events/{eventId}/offers | Event Offers |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all offers?" -> GET /commerce/v2/events/{eventId}/offers
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
