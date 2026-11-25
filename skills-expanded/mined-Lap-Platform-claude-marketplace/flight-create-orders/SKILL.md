---
name: flight-create-orders
description: "Flight Create Orders API skill. Use when working with Flight Create Orders for booking. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Flight Create Orders
API version: 1.10.0

## Auth
No authentication required.

## Base URL
https://test.api.amadeus.com/v1

## Setup
1. No auth setup needed
3. POST /booking/flight-orders -- create first flight-orders

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### booking
| Method | Path | Description |
|--------|------|-------------|
| POST | /booking/flight-orders | Create Order associated to the Flight offers. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a flight-order?" -> POST /booking/flight-orders

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
