---
name: ecwid
description: "ecwid API skill. Use when working with ecwid for bulk, customers, objects. Covers 42 endpoints."
version: 1.0.0
generator: lapsh
---

# ecwid
API version: api-v2

## Auth
ApiKey Authorization in header

## Base URL
https://api.cloud-elements.com/elements/api-v2

## Setup
1. Set your API key in the appropriate header
2. GET /bulk/jobs -- verify access
3. POST /bulk/download -- create first download

## Endpoints

42 endpoints across 7 groups. See references/api-spec.lap for full details.

### bulk
| Method | Path | Description |
|--------|------|-------------|
| POST | /bulk/download | Create a new bulk download job (asynchronous) |
| GET | /bulk/jobs | Fetch all the bulk jobs for an instance |
| POST | /bulk/query | Create an asynchronous bulk query job. |
| PUT | /bulk/{id}/cancel | Cancel an asynchronous bulk query job. |
| GET | /bulk/{id}/errors | Retrieve the errors of a bulk job. |
| GET | /bulk/{id}/status | Retrieve the status of a bulk job. |
| GET | /bulk/{id}/{objectName} | Retrieve the results of an asynchronous bulk query. |
| POST | /bulk/{objectName} | Upload a file of objects to be bulk uploaded to the provider. |

### customers
| Method | Path | Description |
|--------|------|-------------|
| POST | /customers | Create a new customer in eCommerce system.With the exception of the 'id' field, the required fields indicated in the 'Customer' model are those required to create a new customer |
| GET | /customers | Find customers in the eCommerce system, using the provided CEQL search expression. If no search expression is provided, all records will be retrieved |
| PATCH | /customers/{id} | Update an customer associated with a given ID in the eCommerce system.The update API uses the PATCH HTTP verb, so only those fields provided in the customer object will be updated, and those fields not provided will be left alone. Updating a customer with a specified ID that does not exist will result in an error response |
| GET | /customers/{id} | Retrieve a customer associated with a given ID from the eCommerce system. Specifying a customer with an ID that does not exist will result in an error response |
| DELETE | /customers/{id} | Delete a customer associated with a given ID from your eCommerce system. Specifying a customer associated with a given ID that does not exist will result in an error message |
| GET | /customers/{id}/orders | Find orders in the customer associated with a given ID. If the customer does not exist, an error response will be returned. If no orders are found in the given customer then an empty array will be returned |

### objects
| Method | Path | Description |
|--------|------|-------------|
| GET | /objects | Get a list of all the available objects. |
| GET | /objects/{objectName}/docs | Get swagger docs for an object. |
| GET | /objects/{objectName}/metadata | Get a list of all the fields for an object. |

### orders
| Method | Path | Description |
|--------|------|-------------|
| POST | /orders | Create an order in the eCommerce system.With the exception of the 'id' field, the required fields indicated in the 'Order' model are those required to create a new order.The paymentStatus can only be AWAITING_PAYMENT or INCOMPLETE.The fulfillmentStatus can only be AWAITING_PROCESSING |
| GET | /orders | Find orders in the eCommerce system, using the provided CEQL search expression. If no search expression is provided, all records will be retrieved |
| PATCH | /orders/{id} | Update an order associated with a given ID in the eCommerce system. The update API uses the PATCH HTTP verb, so only those fields provided in the order object will be updated, and those fields not provided will be left alone. Updating an order with a specified ID that does not exist will result in an error response</strong> |
| GET | /orders/{id} | Retrieve an order associated with a given ID from the eCommerce system. Specifying an order with an ID that does not exist will result in an error response |
| DELETE | /orders/{id} | Delete an order associated with a given ID from your eCommerce system. Specifying an order associated with a given ID that does not exist will result in an error message |
| GET | /orders/{orderId}/payments | Retrieve the payments in the eCommerce system for the specified order |
| GET | /orders/{orderId}/refunds | Retrieve the refunds in the eCommerce system for the specified order |

### ping
| Method | Path | Description |
|--------|------|-------------|
| GET | /ping | Ping the element to confirm that the hub element has a heartbeat.  If the element does not have a heartbeat, an error message will be returned. |

### products
| Method | Path | Description |
|--------|------|-------------|
| POST | /products | Create a new product in eCommerce system.With the exception of the 'id' field, the required fields indicated in the 'Product' model are those required to create a new product |
| GET | /products | Find products in the eCommerce system, using the provided CEQL search expression. The search expression in CEQL is the WHERE clause in a typical SQL query, but without the WHERE keyword.  If no search expression is provided, all records will be retrieved |
| PATCH | /products/{id} | Update a product associated with a given ID in the eCommerce system. The update API uses the PATCH HTTP verb, so only those fields provided in the product object will be updated, and those fields not provided will be left alone. Updating a product with a specified ID that does not exist will result in an error response. <p><strong>Update supports the following fields: sku, quantity, trackQuantity, quantityDelta, warningLimit, name, price, weight, tangible, enabled, fixedShippingRateOnly, fixedShippingRate, description, wholesalePrices, compareAtPrice, productClassId</strong> |
| GET | /products/{id} | Retrieve a product associated with a given ID from the eCommerce system. Specifying a product with an ID that does not exist will result in an error response |
| DELETE | /products/{id} | Delete a product associated with a given ID from your eCommerce system. Specifying a product associated with a given ID that does not exist will result in an error message |

### {objectName}
| Method | Path | Description |
|--------|------|-------------|
| GET | /{objectName} | Search for {objectName} |
| POST | /{objectName} | Create an {objectName} |
| DELETE | /{objectName}/{objectId} | Delete an {objectName} |
| GET | /{objectName}/{objectId} | Retrieve an {objectName} |
| PATCH | /{objectName}/{objectId} | Update an {objectName} |
| PUT | /{objectName}/{objectId} | Update an {objectName} |
| GET | /{objectName}/{objectId}/{childObjectName} | Search for {childObjectName} |
| POST | /{objectName}/{objectId}/{childObjectName} | Create an {objectName} |
| DELETE | /{objectName}/{objectId}/{childObjectName}/{childObjectId} | Delete an {childObjectName} |
| GET | /{objectName}/{objectId}/{childObjectName}/{childObjectId} | Retrieve an {childObjectName} |
| PATCH | /{objectName}/{objectId}/{childObjectName}/{childObjectId} | Update an {childObjectName} |
| PUT | /{objectName}/{objectId}/{childObjectName}/{childObjectId} | Update an {childObjectName} |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a download?" -> POST /bulk/download
- "List all jobs?" -> GET /bulk/jobs
- "Create a query?" -> POST /bulk/query
- "List all errors?" -> GET /bulk/{id}/errors
- "List all status?" -> GET /bulk/{id}/status
- "Get bulk details?" -> GET /bulk/{id}/{objectName}
- "Create a customer?" -> POST /customers
- "List all customers?" -> GET /customers
- "Partially update a customer?" -> PATCH /customers/{id}
- "Get customer details?" -> GET /customers/{id}
- "Delete a customer?" -> DELETE /customers/{id}
- "List all orders?" -> GET /customers/{id}/orders
- "List all objects?" -> GET /objects
- "List all docs?" -> GET /objects/{objectName}/docs
- "List all metadata?" -> GET /objects/{objectName}/metadata
- "Create a order?" -> POST /orders
- "List all orders?" -> GET /orders
- "Partially update a order?" -> PATCH /orders/{id}
- "Get order details?" -> GET /orders/{id}
- "Delete a order?" -> DELETE /orders/{id}
- "List all payments?" -> GET /orders/{orderId}/payments
- "List all refunds?" -> GET /orders/{orderId}/refunds
- "List all ping?" -> GET /ping
- "Create a product?" -> POST /products
- "List all products?" -> GET /products
- "Partially update a product?" -> PATCH /products/{id}
- "Get product details?" -> GET /products/{id}
- "Delete a product?" -> DELETE /products/{id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
