---
name: flight-order-management
description: "Flight Order Management API skill. Use when working with Flight Order Management for booking. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# Flight Order Management
API version: 1.10.0

## Auth
No authentication required.

## Base URL
https://test.api.amadeus.com/v1

## Setup
1. No auth setup needed
2. GET /booking/flight-orders/{flight-orderId} -- verify access

## Endpoints

2 endpoints across 1 groups. See references/api-spec.lap for full details.

### booking
| Method | Path | Description |
|--------|------|-------------|
| GET | /booking/flight-orders/{flight-orderId} | Retrieve a given flight order |
| DELETE | /booking/flight-orders/{flight-orderId} | Cancel a given flight order |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get flight-order details?" -> GET /booking/flight-orders/{flight-orderId}
- "Delete a flight-order?" -> DELETE /booking/flight-orders/{flight-orderId}

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
