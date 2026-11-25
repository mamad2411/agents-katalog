---
name: hotel-booking
description: "Hotel Booking API skill. Use when working with Hotel Booking for booking. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Hotel Booking
API version: 1.1.3

## Auth
No authentication required.

## Base URL
https://test.api.amadeus.com/v1

## Setup
1. No auth setup needed
3. POST /booking/hotel-bookings -- create first hotel-bookings

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### booking
| Method | Path | Description |
|--------|------|-------------|
| POST | /booking/hotel-bookings | Create Orders associated to the Hotel Offers |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a hotel-booking?" -> POST /booking/hotel-bookings

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
