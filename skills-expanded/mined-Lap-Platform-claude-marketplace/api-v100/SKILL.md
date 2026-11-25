---
name: api-v100
description: "API v1.0.0 API skill. Use when working with API v1.0.0 for api. Covers 61 endpoints."
version: 1.0.0
generator: lapsh
---

# API v1.0.0
API version: v1

## Auth
ApiKey x-auth-key in header | ApiKey x-auth-secret in header

## Base URL
https://www.envoice.in

## Setup
1. Set your API key in the appropriate header
2. GET /api/client/all -- verify access
3. POST /api/client/new -- create first new

## Endpoints

61 endpoints across 1 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/client/all | Return all clients for the account |
| POST | /api/client/new | Create a client |
| POST | /api/client/update | Update an existing client |
| GET | /api/client/candelete | Check if the provided client can be deleted |
| POST | /api/client/delete | Delete an existing client |
| GET | /api/client/details | Return client details. Activities and invoices included. |
| GET | /api/estimation/all | Return all estimation for the account |
| POST | /api/estimation/new | Create an estimation |
| POST | /api/estimation/update | Update an existing estimation |
| POST | /api/estimation/delete | Delete an existing estimation |
| POST | /api/estimation/changestatus | Change estimation status |
| GET | /api/estimation/status | Retrieve the status of the estimation |
| GET | /api/estimation/details | Return estimation data |
| GET | /api/estimation/uri | Return the unique url to the client's invoice |
| POST | /api/estimation/convert | Convert the estimation to an invoice |
| POST | /api/estimation/sendtoclient | Send the provided estimation to the client |
| GET | /api/general/countries | Return all of the platform supported countries |
| GET | /api/general/currencies | Return all of the platform supported currencies |
| GET | /api/general/uilanguages | Return all of the platform supported UI languages |
| GET | /api/general/dateformats | Return all of the platform supported Date Formats |
| GET | /api/invoice/all | Return all invoices for the account |
| GET | /api/invoice/allcategories | Return all invoice categories for the account |
| POST | /api/invoice/new | Create an invoice |
| POST | /api/invoice/newcategory | Create an invoice category |
| POST | /api/invoice/update | Update an existing invoice |
| POST | /api/invoice/updatecategory | Update an existing invoice category |
| POST | /api/invoice/delete | Delete an existing invoice |
| POST | /api/invoice/deletecategory | Delete an existing invoice category |
| POST | /api/invoice/sendtoclient | Send the provided invoice to the client |
| POST | /api/invoice/sendtoaccountant | Send the provided invoice to the accountant |
| POST | /api/invoice/changestatus | Change invoice status |
| GET | /api/invoice/status | Retrieve the status of the invoice |
| GET | /api/invoice/details | Return invoice data |
| GET | /api/invoice/uri | Return the unique url to the client's invoice |
| GET | /api/invoice/pdf | Return the PDF for the invoice |
| GET | /api/order/all | Return all orders for the account |
| POST | /api/order/new | Create an order |
| POST | /api/order/delete | Delete an existing order |
| POST | /api/order/changeshippingdetails | Change order shipping details |
| POST | /api/order/changestatus | Change order status |
| GET | /api/order/details | Return order details |
| GET | /api/payment/supported | Return all supported payment gateways (no currencies means all are supported) |
| GET | /api/paymentlink/uri | Return the unique url to the client's payment link |
| GET | /api/paymentlink/all | Create a payment link |
| POST | /api/paymentlink/new | Create a payment link |
| POST | /api/paymentlink/delete | Delete an existing payment link |
| GET | /api/product/all | Return all products for the account |
| POST | /api/product/new | Create a product |
| POST | /api/product/update | Update an existing product |
| POST | /api/product/delete | Delete an existing product |
| GET | /api/product/details | Return product details |
| GET | /api/tax/all | Return all taxes for the account |
| POST | /api/tax/new | Create a tax |
| POST | /api/tax/update | Update an existing tax |
| POST | /api/tax/delete | Delete an existing tax |
| GET | /api/worktype/all | Return all work types for the account |
| GET | /api/worktype/search | Return all work types for the account that match the query param |
| POST | /api/worktype/new | Create a work type |
| POST | /api/worktype/update | Update an existing work type |
| POST | /api/worktype/delete | Delete an existing work type |
| GET | /api/worktype/details | Return work type details |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all all?" -> GET /api/client/all
- "Create a new?" -> POST /api/client/new
- "Create a update?" -> POST /api/client/update
- "List all candelete?" -> GET /api/client/candelete
- "Create a delete?" -> POST /api/client/delete
- "List all details?" -> GET /api/client/details
- "List all all?" -> GET /api/estimation/all
- "Create a new?" -> POST /api/estimation/new
- "Create a update?" -> POST /api/estimation/update
- "Create a delete?" -> POST /api/estimation/delete
- "Create a changestatus?" -> POST /api/estimation/changestatus
- "List all status?" -> GET /api/estimation/status
- "List all details?" -> GET /api/estimation/details
- "List all uri?" -> GET /api/estimation/uri
- "Create a convert?" -> POST /api/estimation/convert
- "Create a sendtoclient?" -> POST /api/estimation/sendtoclient
- "List all countries?" -> GET /api/general/countries
- "List all currencies?" -> GET /api/general/currencies
- "List all uilanguages?" -> GET /api/general/uilanguages
- "List all dateformats?" -> GET /api/general/dateformats
- "List all all?" -> GET /api/invoice/all
- "Search allcategories?" -> GET /api/invoice/allcategories
- "Create a new?" -> POST /api/invoice/new
- "Create a newcategory?" -> POST /api/invoice/newcategory
- "Create a update?" -> POST /api/invoice/update
- "Create a updatecategory?" -> POST /api/invoice/updatecategory
- "Create a delete?" -> POST /api/invoice/delete
- "Create a deletecategory?" -> POST /api/invoice/deletecategory
- "Create a sendtoclient?" -> POST /api/invoice/sendtoclient
- "Create a sendtoaccountant?" -> POST /api/invoice/sendtoaccountant
- "Create a changestatus?" -> POST /api/invoice/changestatus
- "List all status?" -> GET /api/invoice/status
- "List all details?" -> GET /api/invoice/details
- "List all uri?" -> GET /api/invoice/uri
- "List all pdf?" -> GET /api/invoice/pdf
- "List all all?" -> GET /api/order/all
- "Create a new?" -> POST /api/order/new
- "Create a delete?" -> POST /api/order/delete
- "Create a changeshippingdetail?" -> POST /api/order/changeshippingdetails
- "Create a changestatus?" -> POST /api/order/changestatus
- "List all details?" -> GET /api/order/details
- "List all supported?" -> GET /api/payment/supported
- "List all uri?" -> GET /api/paymentlink/uri
- "List all all?" -> GET /api/paymentlink/all
- "Create a new?" -> POST /api/paymentlink/new
- "Create a delete?" -> POST /api/paymentlink/delete
- "List all all?" -> GET /api/product/all
- "Create a new?" -> POST /api/product/new
- "Create a update?" -> POST /api/product/update
- "Create a delete?" -> POST /api/product/delete
- "List all details?" -> GET /api/product/details
- "List all all?" -> GET /api/tax/all
- "Create a new?" -> POST /api/tax/new
- "Create a update?" -> POST /api/tax/update
- "Create a delete?" -> POST /api/tax/delete
- "List all all?" -> GET /api/worktype/all
- "List all search?" -> GET /api/worktype/search
- "Create a new?" -> POST /api/worktype/new
- "Create a update?" -> POST /api/worktype/update
- "Create a delete?" -> POST /api/worktype/delete
- "List all details?" -> GET /api/worktype/details
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
