---
name: just-eat-api
description: "Just Eat API skill. Use when working with Just Eat for {tenant}, attempted-delivery-query-resolved, delivery-failed. Covers 98 endpoints."
version: 1.0.0
generator: lapsh
---

# Just Eat API
API version: 1.0.0

## Auth
ApiKey Authorization in header | Bearer basic | Bearer bearer | openIdConnect | Bearer bearer

## Base URL
https://uk.api.just-eat.io

## Setup
1. Set Authorization header with your Bearer token
2. GET /delivery/pools -- verify access
3. POST /{tenant}/orders/{orderId}/queries/attempteddelivery -- create first attempteddelivery

## Endpoints

98 endpoints across 33 groups. See references/api-spec.lap for full details.

### {tenant}
| Method | Path | Description |
|--------|------|-------------|
| POST | /{tenant}/orders/{orderId}/queries/attempteddelivery | Delivery Attempt Failed |
| POST | /{tenant}/orders/{orderId}/queries/attempteddelivery/resolution/redeliverorder | Request Redelivery of the Order |
| DELETE | /v1/{tenant}/restaurants/{id}/event/offline | Delete Offline Event |
| POST | /v1/{tenant}/restaurants/event/offline | Create Offline Event |

### attempted-delivery-query-resolved
| Method | Path | Description |
|--------|------|-------------|
| PUT | /attempted-delivery-query-resolved | Attempted delivery query resolved |

### delivery-failed
| Method | Path | Description |
|--------|------|-------------|
| PUT | /delivery-failed | Delivery Attempt Failed |

### checkout
| Method | Path | Description |
|--------|------|-------------|
| GET | /checkout/{tenant}/{checkoutId} | Get Checkout |
| PATCH | /checkout/{tenant}/{checkoutId} | Update Checkout |
| GET | /checkout/{tenant}/{checkoutId}/fulfilment/availabletimes | Get Available Fulfilment Times |

### orders
| Method | Path | Description |
|--------|------|-------------|
| POST | /orders/{tenant}/{orderId}/consumerqueries/lateorder/restaurantresponse | Response to Late Order Update Request |
| POST | /orders/{tenant}/{orderId}/consumerqueries/lateordercompensation/restaurantresponse | Update late order compensation request with Restaurant response |
| PUT | /orders/{orderId}/accept | Accept order |
| PUT | /orders/{orderId}/cancel | Cancel order |
| POST | /orders/{orderId}/complete | Complete order |
| PUT | /orders/{orderId}/duedate | Update order ETA |
| PUT | /orders/{orderId}/ignore | Ignore order |
| POST | /orders/{orderId}/readyforcollection | Mark order as ready for collection |
| PUT | /orders/{orderId}/reject | Reject order |
| PUT | /orders/{orderId}/deliverystate/atdeliveryaddress | Update order with driver at delivery address details |
| PUT | /orders/{orderId}/deliverystate/atrestaurant | Update order with driver at restaurant details |
| PUT | /orders/{orderId}/deliverystate/atrestauranteta | Update the driver's estimated time to arrive at the Restaurant |
| PUT | /orders/{orderId}/deliverystate/delivered | Update order with delivered details |
| PUT | /orders/{orderId}/deliverystate/driverassigned | Update order with driver assigned details |
| PUT | /orders/{orderId}/deliverystate/driverlocation | Update the driver's current location |
| PUT | /orders/{orderId}/deliverystate/driverunassigned | Update order with driver unassigned details |
| PUT | /orders/{orderId}/deliverystate/onitsway | Update order with driver on its way details |
| PUT | /orders/deliverystate/driverlocation | Update current driver locations (bulk upload) |
| POST | /orders | Create order |
| POST | /orders/{tenant}/{orderId}/restaurantqueries/compensation | Create Compensation requests |

### late-order-compensation-query
| Method | Path | Description |
|--------|------|-------------|
| POST | /late-order-compensation-query | late order compensation query, restaurant response required |

### late-order-query
| Method | Path | Description |
|--------|------|-------------|
| POST | /late-order-query | late order query, restaurant response required |

### consumers
| Method | Path | Description |
|--------|------|-------------|
| POST | /consumers/{tenant} | Create consumer |
| GET | /consumers/{tenant} | Get consumers details |
| GET | /consumers/{tenant}/me/communication-preferences | Get communication preferences |
| GET | /consumers/{tenant}/me/communication-preferences/{type} | Get channel subscriptions for a given consumer's communication preference type |
| PUT | /consumers/{tenant}/me/communication-preferences/{type} | Set only the channel subscriptions for a given consumer's communication preference type |
| POST | /consumers/{tenant}/me/communication-preferences/{type}/subscribedChannels/{channel} | Subscribe to a specific communication preference channel |
| DELETE | /consumers/{tenant}/me/communication-preferences/{type}/subscribedChannels/{channel} | Remove subscription of a specific communication preference channel |

### delivery-fees
| Method | Path | Description |
|--------|------|-------------|
| GET | /delivery-fees/{tenant} | Get restaurant delivery fees |

### delivery
| Method | Path | Description |
|--------|------|-------------|
| GET | /delivery/pools | Get your delivery pools |
| POST | /delivery/pools | Create a new delivery pool |
| GET | /delivery/pools/{deliveryPoolId} | Get an individual delivery pool |
| DELETE | /delivery/pools/{deliveryPoolId} | Delete a delivery pool |
| PATCH | /delivery/pools/{deliveryPoolId} | Modify a delivery pool |
| PUT | /delivery/pools/{deliveryPoolId} | Replace an existing delivery pool |
| GET | /delivery/pools/{deliveryPoolId}/availability/relative | Get availability for pickup |
| PUT | /delivery/pools/{deliveryPoolId}/availability/relative | Set availability for pickup |
| PUT | /delivery/pools/{deliveryPoolId}/hours | Set the delivery pools daily start and end times |
| PUT | /delivery/pools/{deliveryPoolId}/restaurants | Add restaurants to an existing delivery pool |
| DELETE | /delivery/pools/{deliveryPoolId}/restaurants | Remove restaurants from a delivery pool |
| GET | /delivery/estimate | Get delivery estimate |

### acceptance-requested
| Method | Path | Description |
|--------|------|-------------|
| POST | /acceptance-requested | Acceptance requested |

### order-accepted
| Method | Path | Description |
|--------|------|-------------|
| POST | /order-accepted | Order accepted |

### order-cancelled
| Method | Path | Description |
|--------|------|-------------|
| POST | /order-cancelled | Order cancelled |

### order-rejected
| Method | Path | Description |
|--------|------|-------------|
| POST | /order-rejected | Order rejected |

### redelivery-requested
| Method | Path | Description |
|--------|------|-------------|
| PUT | /redelivery-requested | Customer Requested Redelivery |

### driver-assigned-to-delivery
| Method | Path | Description |
|--------|------|-------------|
| PUT | /driver-assigned-to-delivery | Driver Assigned to Delivery |

### driver-at-delivery-address
| Method | Path | Description |
|--------|------|-------------|
| PUT | /driver-at-delivery-address | Driver at delivery address |

### driver-at-restaurant
| Method | Path | Description |
|--------|------|-------------|
| PUT | /driver-at-restaurant | Driver at restaurant |

### driver-has-delivered-order
| Method | Path | Description |
|--------|------|-------------|
| PUT | /driver-has-delivered-order | Driver has delivered order |

### driver-location
| Method | Path | Description |
|--------|------|-------------|
| PUT | /driver-location | Driver Location |

### driver-on-their-way-to-delivery-address
| Method | Path | Description |
|--------|------|-------------|
| PUT | /driver-on-their-way-to-delivery-address | Driver on their way to delivery address |

### order-is-ready-for-pickup
| Method | Path | Description |
|--------|------|-------------|
| PUT | /order-is-ready-for-pickup | Order ready for pickup |

### order-requires-delivery-acceptance
| Method | Path | Description |
|--------|------|-------------|
| PUT | /order-requires-delivery-acceptance | Order requires delivery acceptance |

### order-ready-for-preparation-async
| Method | Path | Description |
|--------|------|-------------|
| POST | /order-ready-for-preparation-async | Order ready for preparation (async) |

### order-ready-for-preparation-sync
| Method | Path | Description |
|--------|------|-------------|
| POST | /order-ready-for-preparation-sync | Order ready for preparation (sync) |

### send-to-pos-failed
| Method | Path | Description |
|--------|------|-------------|
| POST | /send-to-pos-failed | Send to POS failed |

### restaurants
| Method | Path | Description |
|--------|------|-------------|
| GET | /restaurants/{tenant}/{restaurantId}/customerclaims | Get claims |
| GET | /restaurants/{tenant}/{restaurantId}/customerclaims/{id} | Get order claim |
| POST | /restaurants/{tenant}/{restaurantId}/customerclaims/{id}/restaurantresponse | Submit a restaurant response for the claim |
| PUT | /restaurants/{tenant}/{restaurantId}/customerclaims/{id}/restaurantresponse/justification | Add reason and comments to the response |
| GET | /restaurants/{tenant}/{restaurantId}/catalogue | Get product catalogue |
| GET | /restaurants/{tenant}/{restaurantId}/catalogue/availabilities | Get all availabilities |
| GET | /restaurants/{tenant}/{restaurantId}/catalogue/categories | Get all categories |
| GET | /restaurants/{tenant}/{restaurantId}/catalogue/categories/{categoryId}/items | Get all category item IDs |
| GET | /restaurants/{tenant}/{restaurantId}/catalogue/items | Get all menu items |
| GET | /restaurants/{tenant}/{restaurantId}/catalogue/items/{itemId}/dealgroups | Get all menu item deal groups |
| GET | /restaurants/{tenant}/{restaurantId}/catalogue/items/{itemId}/dealgroups/{dealGroupId}/dealitemvariations | Get all deal item variations for a deal group |
| GET | /restaurants/{tenant}/{restaurantId}/catalogue/items/{itemId}/modifiergroups | Get all menu item modifier groups |
| GET | /restaurants/{tenant}/{restaurantId}/catalogue/items/{itemId}/variations | Get all menu item variations |
| GET | /restaurants/{tenant}/{restaurantId}/fees | Get Restaurant Fees |
| PUT | /restaurants/{tenant}/{restaurantId}/fees | Create or Update Restaurant Fees |
| PUT | /restaurants/{tenant}/{restaurantId}/menu | Create or update a menu |
| GET | /restaurants/{tenant}/{restaurantId}/menu | Get the latest version of the restaurant's full menu |
| GET | /restaurants/{tenant}/{restaurantId}/ordertimes | Get the restaurant's delivery and collection lead times |
| PUT | /restaurants/{tenant}/{restaurantId}/ordertimes/{dayOfWeek}/{serviceType} | Update the restaurant's delivery and collection lead times |
| GET | /restaurants/{tenant}/{restaurantId}/servicetimes | Get service times |
| PUT | /restaurants/{tenant}/{restaurantId}/servicetimes | Create or update service times |
| GET | /restaurants/bylatlong | Get restaurants by location |
| GET | /restaurants/bypostcode/{postcode} | Get restaurants by postcode |
| PUT | /restaurants/driver/eta | Set ETA for pickup |

### restaurant-offline-status
| Method | Path | Description |
|--------|------|-------------|
| PUT | /restaurant-offline-status | Restaurant Offline Status |

### restaurant-online-status
| Method | Path | Description |
|--------|------|-------------|
| PUT | /restaurant-online-status | Restaurant Online Status |

### order-eligible-for-restaurant-compensation
| Method | Path | Description |
|--------|------|-------------|
| POST | /order-eligible-for-restaurant-compensation | Order Eligible For Restaurant Compensation |

### menu-ingestion-complete
| Method | Path | Description |
|--------|------|-------------|
| POST | /menu-ingestion-complete | Menu ingestion complete |

### order-time-updated
| Method | Path | Description |
|--------|------|-------------|
| POST | /order-time-updated | Order time updated |

### search
| Method | Path | Description |
|--------|------|-------------|
| GET | /search/autocomplete/{tenant} | Get auto-completed search terms |
| GET | /search/restaurants/{tenant} | Search restaurants |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a attempteddelivery?" -> POST /{tenant}/orders/{orderId}/queries/attempteddelivery
- "Create a redeliverorder?" -> POST /{tenant}/orders/{orderId}/queries/attempteddelivery/resolution/redeliverorder
- "Get checkout details?" -> GET /checkout/{tenant}/{checkoutId}
- "Partially update a checkout?" -> PATCH /checkout/{tenant}/{checkoutId}
- "List all availabletimes?" -> GET /checkout/{tenant}/{checkoutId}/fulfilment/availabletimes
- "Create a restaurantresponse?" -> POST /orders/{tenant}/{orderId}/consumerqueries/lateorder/restaurantresponse
- "Create a restaurantresponse?" -> POST /orders/{tenant}/{orderId}/consumerqueries/lateordercompensation/restaurantresponse
- "Create a late-order-compensation-query?" -> POST /late-order-compensation-query
- "Create a late-order-query?" -> POST /late-order-query
- "Get consumer details?" -> GET /consumers/{tenant}
- "List all communication-preferences?" -> GET /consumers/{tenant}/me/communication-preferences
- "Get communication-preference details?" -> GET /consumers/{tenant}/me/communication-preferences/{type}
- "Update a communication-preference?" -> PUT /consumers/{tenant}/me/communication-preferences/{type}
- "Delete a subscribedChannel?" -> DELETE /consumers/{tenant}/me/communication-preferences/{type}/subscribedChannels/{channel}
- "Get delivery-fee details?" -> GET /delivery-fees/{tenant}
- "List all pools?" -> GET /delivery/pools
- "Create a pool?" -> POST /delivery/pools
- "Get pool details?" -> GET /delivery/pools/{deliveryPoolId}
- "Delete a pool?" -> DELETE /delivery/pools/{deliveryPoolId}
- "Partially update a pool?" -> PATCH /delivery/pools/{deliveryPoolId}
- "Update a pool?" -> PUT /delivery/pools/{deliveryPoolId}
- "List all relative?" -> GET /delivery/pools/{deliveryPoolId}/availability/relative
- "Create a complete?" -> POST /orders/{orderId}/complete
- "Create a readyforcollection?" -> POST /orders/{orderId}/readyforcollection
- "Create a acceptance-requested?" -> POST /acceptance-requested
- "Create a order-accepted?" -> POST /order-accepted
- "Create a order-cancelled?" -> POST /order-cancelled
- "Create a order-rejected?" -> POST /order-rejected
- "List all estimate?" -> GET /delivery/estimate
- "Create a order?" -> POST /orders
- "Create a order-ready-for-preparation-async?" -> POST /order-ready-for-preparation-async
- "Create a order-ready-for-preparation-sync?" -> POST /order-ready-for-preparation-sync
- "Create a send-to-pos-failed?" -> POST /send-to-pos-failed
- "List all customerclaims?" -> GET /restaurants/{tenant}/{restaurantId}/customerclaims
- "Get customerclaim details?" -> GET /restaurants/{tenant}/{restaurantId}/customerclaims/{id}
- "Create a restaurantresponse?" -> POST /restaurants/{tenant}/{restaurantId}/customerclaims/{id}/restaurantresponse
- "Create a offline?" -> POST /v1/{tenant}/restaurants/event/offline
- "Create a compensation?" -> POST /orders/{tenant}/{orderId}/restaurantqueries/compensation
- "Create a order-eligible-for-restaurant-compensation?" -> POST /order-eligible-for-restaurant-compensation
- "List all catalogue?" -> GET /restaurants/{tenant}/{restaurantId}/catalogue
- "List all availabilities?" -> GET /restaurants/{tenant}/{restaurantId}/catalogue/availabilities
- "List all categories?" -> GET /restaurants/{tenant}/{restaurantId}/catalogue/categories
- "List all items?" -> GET /restaurants/{tenant}/{restaurantId}/catalogue/categories/{categoryId}/items
- "List all items?" -> GET /restaurants/{tenant}/{restaurantId}/catalogue/items
- "List all dealgroups?" -> GET /restaurants/{tenant}/{restaurantId}/catalogue/items/{itemId}/dealgroups
- "List all dealitemvariations?" -> GET /restaurants/{tenant}/{restaurantId}/catalogue/items/{itemId}/dealgroups/{dealGroupId}/dealitemvariations
- "List all modifiergroups?" -> GET /restaurants/{tenant}/{restaurantId}/catalogue/items/{itemId}/modifiergroups
- "List all variations?" -> GET /restaurants/{tenant}/{restaurantId}/catalogue/items/{itemId}/variations
- "List all fees?" -> GET /restaurants/{tenant}/{restaurantId}/fees
- "List all menu?" -> GET /restaurants/{tenant}/{restaurantId}/menu
- "List all ordertimes?" -> GET /restaurants/{tenant}/{restaurantId}/ordertimes
- "Update a ordertime?" -> PUT /restaurants/{tenant}/{restaurantId}/ordertimes/{dayOfWeek}/{serviceType}
- "List all servicetimes?" -> GET /restaurants/{tenant}/{restaurantId}/servicetimes
- "List all bylatlong?" -> GET /restaurants/bylatlong
- "Get bypostcode details?" -> GET /restaurants/bypostcode/{postcode}
- "Create a menu-ingestion-complete?" -> POST /menu-ingestion-complete
- "Create a order-time-updated?" -> POST /order-time-updated
- "Get autocomplete details?" -> GET /search/autocomplete/{tenant}
- "Get restaurant details?" -> GET /search/restaurants/{tenant}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
