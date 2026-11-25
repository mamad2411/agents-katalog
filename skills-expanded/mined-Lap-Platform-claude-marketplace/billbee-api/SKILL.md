---
name: billbee-api
description: "Billbee API skill. Use when working with Billbee for api. Covers 87 endpoints."
version: 1.0.0
generator: lapsh
---

# Billbee API
API version: V1

## Auth
basic | ApiKey X-Billbee-Api-Key in header

## Base URL
https://app.billbee.io

## Setup
1. Set your API key in the appropriate header
2. GET /api/v1/apiusage -- verify access
3. POST /api/v1/customer-addresses -- create first customer-addresses

## Endpoints

87 endpoints across 1 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/v1/apiusage | Get summarised api usage statistics |
| GET | /api/v1/apiusage/detail | Get detailed api usage statistics |
| GET | /api/v1/cloudstorages | Gets a list of all connected cloud storage devices |
| GET | /api/v1/customer-addresses | Get a list of all customer addresses |
| POST | /api/v1/customer-addresses | Creates a new customer address |
| GET | /api/v1/customer-addresses/{id} | Queries a single customer address by id |
| PUT | /api/v1/customer-addresses/{id} | Updates a customer address by id |
| GET | /api/v1/customers | Get a list of all customers |
| POST | /api/v1/customers | Creates a new customer |
| GET | /api/v1/customers/{id} | Queries a single customer by id |
| PUT | /api/v1/customers/{id} | Updates a customer by id |
| GET | /api/v1/customers/{id}/orders | Queries a list of orders from a customer |
| GET | /api/v1/customers/{id}/addresses | Queries a list of addresses from a customer |
| POST | /api/v1/customers/{id}/addresses | Adds a new address to a customer |
| GET | /api/v1/customers/addresses/{id} | Queries a single address from a customer |
| PUT | /api/v1/customers/addresses/{id} | Updates all fields of an address |
| PATCH | /api/v1/customers/addresses/{id} | Updates one or more fields of an address |
| GET | /api/v1/enums/paymenttypes | Returns a list with all defined paymenttypes |
| GET | /api/v1/enums/shippingcarriers | Returns a list with all defined shippingcarriers |
| GET | /api/v1/enums/accountsyncstate | Returns a list with all defined account sync states |
| GET | /api/v1/enums/shopaccounttype | Returns a list with all defined account types |
| GET | /api/v1/enums/shipmenttypes | Returns a list with all defined shipmenttypes |
| GET | /api/v1/enums/orderstates | Returns a list with all defined orderstates |
| GET | /api/v1/events | Get a list of all events optionally filtered by date. This request is extra throttled to 2 calls per page per hour. |
| POST | /api/v1/orders/createmultiple |  |
| GET | /api/v1/orders | Get a list of all orders optionally filtered by date |
| POST | /api/v1/orders |  |
| PUT | /api/v1/orders/{id}/tags | Sets the tags attached to an order |
| POST | /api/v1/orders/{id}/tags | Attach one or more tags to an order |
| POST | /api/v1/orders/tags | Add one or more tags to multiple orders |
| GET | /api/v1/orders/{id} | Get a single order by its internal billbee id. This request is throttled to 6 calls per order in one minute |
| PATCH | /api/v1/orders/{id} | Updates one or more fields of an order |
| GET | /api/v1/orders/findbyextref/{extRef} | Get a single order by its external order number |
| PUT | /api/v1/orders/{id}/orderstate | Changes the main state of a single order |
| POST | /api/v1/orders/{id}/shipment | Add a shipment to a given order |
| GET | /api/v1/orders/invoices | Get a list of all invoices optionally filtered by date. This request ist throttled to 1 per 1 minute for same page and minInvoiceDate |
| GET | /api/v1/orders/find/{id}/{partner} | Find a single order by its external id (order number) |
| POST | /api/v1/orders/CreateDeliveryNote/{id} | Create an delivery note for an existing order. This request is extra throttled by order and api key to a maximum of 1 per 5 minutes. |
| POST | /api/v1/orders/CreateInvoice/{id} | Create an invoice for an existing order. This request is extra throttled by order and api key to a maximum of 1 per 5 minutes. |
| GET | /api/v1/orders/PatchableFields | Returns a list of fields which can be updated with the orders/{id} patch call |
| POST | /api/v1/orders/{id}/send-message | Sends a message to the buyer |
| POST | /api/v1/orders/{id}/trigger-event | Triggers a rule event |
| POST | /api/v1/orders/{id}/parse-placeholders | Parses a text and replaces all placeholders |
| POST | /api/v1/orders/{id}/message | Adds a message to the order |
| GET | /api/v1/layouts |  |
| POST | /api/v1/search | Search for products, customers and orders. |
| GET | /api/v1/products | Get a list of all products |
| POST | /api/v1/products | Creates a new product |
| GET | /api/v1/products/{id} | Queries a single article by id or by sku |
| DELETE | /api/v1/products/{id} | Deletes a product |
| PATCH | /api/v1/products/{id} | Updates one or more fields of a product |
| GET | /api/v1/products/stocks | Query all defined stock locations |
| GET | /api/v1/products/PatchableFields | Returns a list of fields which can be updated with the patch call |
| GET | /api/v1/products/category | GEts a list of all defined categories |
| POST | /api/v1/products/updatestock | Update the stock qty of an article |
| POST | /api/v1/products/stockmultiple | Retrieve the stock qty for multiple articles at once |
| POST | /api/v1/products/updatestockmultiple | Update the stock qty for multiple articles at once |
| GET | /api/v1/products/reservedamount | Queries the reserved amount for a single article by id or by sku |
| POST | /api/v1/products/updatestockcode | Update the stock code of an article |
| GET | /api/v1/products/custom-fields | Queries a list of all custom fields |
| GET | /api/v1/products/custom-fields/{id} | Queries a single custom field |
| GET | /api/v1/products/{productId}/images | Returns a list of all images of the product |
| PUT | /api/v1/products/{productId}/images | Add multiple images to a product or replace the product images by the given images |
| GET | /api/v1/products/{productId}/images/{imageId} | Returns a single image by id |
| PUT | /api/v1/products/{productId}/images/{imageId} | Add or update an existing image of a product |
| DELETE | /api/v1/products/{productId}/images/{imageId} | Deletes a single image from a product |
| GET | /api/v1/products/images/{imageId} | Returns a single image by id |
| DELETE | /api/v1/products/images/{imageId} | Deletes a single image by id |
| POST | /api/v1/products/images/delete |  |
| POST | /api/v1/automaticprovision/createaccount | Creates a new Billbee user account with the data passed |
| GET | /api/v1/automaticprovision/termsinfo | Returns infos about Billbee terms and conditions |
| POST | /api/v1/shipment/shipmentmultiple | Creates multiple shipments |
| POST | /api/v1/shipment/shipment | Creates a new shipment with the selected Shippingprovider |
| GET | /api/v1/shipment/shippingproviders | Query all defined shipping providers |
| POST | /api/v1/shipment/shipwithlabel | Creates a shipment for an order in billbee |
| POST | /api/v1/shipment/shipwithlabelmultiple | Creates shipments for a list of orders in billbee |
| GET | /api/v1/shipment/shippingcarriers | Queries the currently available shipping carriers. |
| GET | /api/v1/shipment/ping |  |
| GET | /api/v1/shipment/shipments | Get a list of all shipments optionally filtered by date. All parameters are optional. |
| GET | /api/v1/shopaccounts | Queries a list of avaible shop accounts |
| GET | /api/v1/webhooks | Gets all registered WebHooks for a given user. |
| POST | /api/v1/webhooks | Registers a new WebHook for a given user. |
| DELETE | /api/v1/webhooks | Deletes all existing WebHook registrations. |
| GET | /api/v1/webhooks/{id} | Looks up a registered WebHook with the given {id} for a given user. |
| PUT | /api/v1/webhooks/{id} | Updates an existing WebHook registration. |
| DELETE | /api/v1/webhooks/{id} | Deletes an existing WebHook registration. |
| GET | /api/v1/webhooks/filters | Returns a list of all known filters you can use to register webhooks |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all apiusage?" -> GET /api/v1/apiusage
- "List all detail?" -> GET /api/v1/apiusage/detail
- "List all cloudstorages?" -> GET /api/v1/cloudstorages
- "List all customer-addresses?" -> GET /api/v1/customer-addresses
- "Create a customer-address?" -> POST /api/v1/customer-addresses
- "Get customer-address details?" -> GET /api/v1/customer-addresses/{id}
- "Update a customer-address?" -> PUT /api/v1/customer-addresses/{id}
- "List all customers?" -> GET /api/v1/customers
- "Create a customer?" -> POST /api/v1/customers
- "Get customer details?" -> GET /api/v1/customers/{id}
- "Update a customer?" -> PUT /api/v1/customers/{id}
- "List all orders?" -> GET /api/v1/customers/{id}/orders
- "List all addresses?" -> GET /api/v1/customers/{id}/addresses
- "Create a address?" -> POST /api/v1/customers/{id}/addresses
- "Get address details?" -> GET /api/v1/customers/addresses/{id}
- "Update a address?" -> PUT /api/v1/customers/addresses/{id}
- "Partially update a address?" -> PATCH /api/v1/customers/addresses/{id}
- "List all paymenttypes?" -> GET /api/v1/enums/paymenttypes
- "List all shippingcarriers?" -> GET /api/v1/enums/shippingcarriers
- "List all accountsyncstate?" -> GET /api/v1/enums/accountsyncstate
- "List all shopaccounttype?" -> GET /api/v1/enums/shopaccounttype
- "List all shipmenttypes?" -> GET /api/v1/enums/shipmenttypes
- "List all orderstates?" -> GET /api/v1/enums/orderstates
- "List all events?" -> GET /api/v1/events
- "Create a createmultiple?" -> POST /api/v1/orders/createmultiple
- "List all orders?" -> GET /api/v1/orders
- "Create a order?" -> POST /api/v1/orders
- "Create a tag?" -> POST /api/v1/orders/{id}/tags
- "Create a tag?" -> POST /api/v1/orders/tags
- "Get order details?" -> GET /api/v1/orders/{id}
- "Partially update a order?" -> PATCH /api/v1/orders/{id}
- "Get findbyextref details?" -> GET /api/v1/orders/findbyextref/{extRef}
- "Create a shipment?" -> POST /api/v1/orders/{id}/shipment
- "List all invoices?" -> GET /api/v1/orders/invoices
- "Get find details?" -> GET /api/v1/orders/find/{id}/{partner}
- "List all PatchableFields?" -> GET /api/v1/orders/PatchableFields
- "Create a send-message?" -> POST /api/v1/orders/{id}/send-message
- "Create a trigger-event?" -> POST /api/v1/orders/{id}/trigger-event
- "Create a parse-placeholder?" -> POST /api/v1/orders/{id}/parse-placeholders
- "Create a message?" -> POST /api/v1/orders/{id}/message
- "List all layouts?" -> GET /api/v1/layouts
- "Create a search?" -> POST /api/v1/search
- "List all products?" -> GET /api/v1/products
- "Create a product?" -> POST /api/v1/products
- "Get product details?" -> GET /api/v1/products/{id}
- "Delete a product?" -> DELETE /api/v1/products/{id}
- "Partially update a product?" -> PATCH /api/v1/products/{id}
- "List all stocks?" -> GET /api/v1/products/stocks
- "List all PatchableFields?" -> GET /api/v1/products/PatchableFields
- "List all category?" -> GET /api/v1/products/category
- "Create a updatestock?" -> POST /api/v1/products/updatestock
- "Create a stockmultiple?" -> POST /api/v1/products/stockmultiple
- "Create a updatestockmultiple?" -> POST /api/v1/products/updatestockmultiple
- "List all reservedamount?" -> GET /api/v1/products/reservedamount
- "Create a updatestockcode?" -> POST /api/v1/products/updatestockcode
- "List all custom-fields?" -> GET /api/v1/products/custom-fields
- "Get custom-field details?" -> GET /api/v1/products/custom-fields/{id}
- "List all images?" -> GET /api/v1/products/{productId}/images
- "Get image details?" -> GET /api/v1/products/{productId}/images/{imageId}
- "Update a image?" -> PUT /api/v1/products/{productId}/images/{imageId}
- "Delete a image?" -> DELETE /api/v1/products/{productId}/images/{imageId}
- "Get image details?" -> GET /api/v1/products/images/{imageId}
- "Delete a image?" -> DELETE /api/v1/products/images/{imageId}
- "Create a delete?" -> POST /api/v1/products/images/delete
- "Create a createaccount?" -> POST /api/v1/automaticprovision/createaccount
- "List all termsinfo?" -> GET /api/v1/automaticprovision/termsinfo
- "Create a shipmentmultiple?" -> POST /api/v1/shipment/shipmentmultiple
- "Create a shipment?" -> POST /api/v1/shipment/shipment
- "List all shippingproviders?" -> GET /api/v1/shipment/shippingproviders
- "Create a shipwithlabel?" -> POST /api/v1/shipment/shipwithlabel
- "Create a shipwithlabelmultiple?" -> POST /api/v1/shipment/shipwithlabelmultiple
- "List all shippingcarriers?" -> GET /api/v1/shipment/shippingcarriers
- "List all ping?" -> GET /api/v1/shipment/ping
- "List all shipments?" -> GET /api/v1/shipment/shipments
- "List all shopaccounts?" -> GET /api/v1/shopaccounts
- "List all webhooks?" -> GET /api/v1/webhooks
- "Create a webhook?" -> POST /api/v1/webhooks
- "Get webhook details?" -> GET /api/v1/webhooks/{id}
- "Update a webhook?" -> PUT /api/v1/webhooks/{id}
- "Delete a webhook?" -> DELETE /api/v1/webhooks/{id}
- "List all filters?" -> GET /api/v1/webhooks/filters
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
