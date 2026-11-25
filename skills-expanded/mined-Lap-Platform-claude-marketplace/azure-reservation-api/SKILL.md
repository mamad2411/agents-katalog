---
name: azure-reservation-api
description: "Azure Reservation API skill. Use when working with Azure Reservation for providers, subscriptions. Covers 16 endpoints."
version: 1.0.0
generator: lapsh
---

# Azure Reservation API
API version: 2019-04-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.Capacity/reservationOrders -- verify access
3. POST /providers/Microsoft.Capacity/reservationOrders/{reservationOrderId}/reservations/{reservationId}/availableScopes -- create first availableScopes

## Endpoints

16 endpoints across 2 groups. See references/api-spec.lap for full details.

### providers
| Method | Path | Description |
|--------|------|-------------|
| POST | /providers/Microsoft.Capacity/reservationOrders/{reservationOrderId}/reservations/{reservationId}/availableScopes | Get Available Scopes for `Reservation`. |
| POST | /providers/Microsoft.Capacity/calculatePrice | Calculate price for a `ReservationOrder`. |
| GET | /providers/Microsoft.Capacity/reservationOrders | Get all `ReservationOrder`s. |
| PUT | /providers/Microsoft.Capacity/reservationOrders/{reservationOrderId} | Purchase `ReservationOrder` |
| GET | /providers/Microsoft.Capacity/reservationOrders/{reservationOrderId} | Get a specific `ReservationOrder`. |
| POST | /providers/Microsoft.Capacity/reservationOrders/{reservationOrderId}/split | Split the `Reservation`. |
| POST | /providers/Microsoft.Capacity/reservationOrders/{reservationOrderId}/merge | Merges two `Reservation`s. |
| GET | /providers/Microsoft.Capacity/reservationOrders/{reservationOrderId}/reservations | Get `Reservation`s in a given reservation Order |
| GET | /providers/Microsoft.Capacity/reservationOrders/{reservationOrderId}/reservations/{reservationId} | Get `Reservation` details. |
| PATCH | /providers/Microsoft.Capacity/reservationOrders/{reservationOrderId}/reservations/{reservationId} | Updates a `Reservation`. |
| GET | /providers/Microsoft.Capacity/reservationOrders/{reservationOrderId}/reservations/{reservationId}/revisions | Get `Reservation` revisions. |
| POST | /providers/Microsoft.Capacity/reservationOrders/{reservationOrderId}/reservations/{reservationId}/archive | Archive a `Reservation`. |
| POST | /providers/Microsoft.Capacity/reservationOrders/{reservationOrderId}/reservations/{reservationId}/unarchive | Unarchive a `Reservation`. |
| GET | /providers/Microsoft.Capacity/operations | Get operations. |

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Capacity/catalogs | Get the regions and skus that are available for RI purchase for the specified Azure subscription. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Capacity/appliedReservations | Get list of applicable `Reservation`s. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a availableScope?" -> POST /providers/Microsoft.Capacity/reservationOrders/{reservationOrderId}/reservations/{reservationId}/availableScopes
- "List all catalogs?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Capacity/catalogs
- "List all appliedReservations?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Capacity/appliedReservations
- "Create a calculatePrice?" -> POST /providers/Microsoft.Capacity/calculatePrice
- "List all reservationOrders?" -> GET /providers/Microsoft.Capacity/reservationOrders
- "Update a reservationOrder?" -> PUT /providers/Microsoft.Capacity/reservationOrders/{reservationOrderId}
- "Get reservationOrder details?" -> GET /providers/Microsoft.Capacity/reservationOrders/{reservationOrderId}
- "Create a split?" -> POST /providers/Microsoft.Capacity/reservationOrders/{reservationOrderId}/split
- "Create a merge?" -> POST /providers/Microsoft.Capacity/reservationOrders/{reservationOrderId}/merge
- "List all reservations?" -> GET /providers/Microsoft.Capacity/reservationOrders/{reservationOrderId}/reservations
- "Get reservation details?" -> GET /providers/Microsoft.Capacity/reservationOrders/{reservationOrderId}/reservations/{reservationId}
- "Partially update a reservation?" -> PATCH /providers/Microsoft.Capacity/reservationOrders/{reservationOrderId}/reservations/{reservationId}
- "List all revisions?" -> GET /providers/Microsoft.Capacity/reservationOrders/{reservationOrderId}/reservations/{reservationId}/revisions
- "Create a archive?" -> POST /providers/Microsoft.Capacity/reservationOrders/{reservationOrderId}/reservations/{reservationId}/archive
- "Create a unarchive?" -> POST /providers/Microsoft.Capacity/reservationOrders/{reservationOrderId}/reservations/{reservationId}/unarchive
- "List all operations?" -> GET /providers/Microsoft.Capacity/operations
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
