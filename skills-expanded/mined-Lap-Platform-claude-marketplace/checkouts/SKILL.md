---
name: checkouts
description: "Checkouts API skill. Use when working with Checkouts for checkouts. Covers 19 endpoints."
version: 1.0.0
generator: lapsh
---

# Checkouts
API version: 3.0

## Auth
ApiKey X-Auth-Token in header

## Base URL
https://api.bigcommerce.com/stores/{store_hash}/v3

## Setup
1. Set your API key in the appropriate header
2. GET /checkouts/settings -- verify access
3. POST /checkouts/{checkoutId}/discounts -- create first discounts

## Endpoints

19 endpoints across 1 groups. See references/api-spec.lap for full details.

### checkouts
| Method | Path | Description |
|--------|------|-------------|
| GET | /checkouts/{checkoutId} | Get a Checkout |
| PUT | /checkouts/{checkoutId} | Update Customer Messages |
| POST | /checkouts/{checkoutId}/discounts | Add Discount to Checkout |
| POST | /checkouts/{checkoutId}/billing-address | Add Checkout Billing Address |
| PUT | /checkouts/{checkoutId}/billing-address/{addressId} | Update Checkout Billing Address |
| POST | /checkouts/{checkoutId}/consignments | Add Consignment to Checkout |
| PUT | /checkouts/{checkoutId}/consignments/{consignmentId} | Update Checkout Consignment |
| DELETE | /checkouts/{checkoutId}/consignments/{consignmentId} | Delete Checkout Consignment |
| POST | /checkouts/{checkoutId}/coupons | Add Coupon to Checkout |
| DELETE | /checkouts/{checkoutId}/coupons/{couponCode} | Delete Checkout Coupon |
| POST | /checkouts/{checkoutId}/fees | Add order level fees to a checkout |
| PUT | /checkouts/{checkoutId}/fees | Update order level fees in a checkout |
| DELETE | /checkouts/{checkoutId}/fees | Delete order level fees from a checkout. |
| POST | /checkouts/{checkoutId}/orders | Create an Order |
| GET | /checkouts/settings | Get Checkout Settings |
| PUT | /checkouts/settings | Update Checkout Settings |
| GET | /checkouts/settings/channels/{channelId} | Get Channel-Specific Checkout Settings |
| PUT | /checkouts/settings/channels/{channelId} | Update Channel-Specific Checkout Settings |
| POST | /checkouts/{checkoutId}/token | Create Checkout Token |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get checkout details?" -> GET /checkouts/{checkoutId}
- "Update a checkout?" -> PUT /checkouts/{checkoutId}
- "Create a discount?" -> POST /checkouts/{checkoutId}/discounts
- "Create a billing-address?" -> POST /checkouts/{checkoutId}/billing-address
- "Update a billing-address?" -> PUT /checkouts/{checkoutId}/billing-address/{addressId}
- "Create a consignment?" -> POST /checkouts/{checkoutId}/consignments
- "Update a consignment?" -> PUT /checkouts/{checkoutId}/consignments/{consignmentId}
- "Delete a consignment?" -> DELETE /checkouts/{checkoutId}/consignments/{consignmentId}
- "Create a coupon?" -> POST /checkouts/{checkoutId}/coupons
- "Delete a coupon?" -> DELETE /checkouts/{checkoutId}/coupons/{couponCode}
- "Create a fee?" -> POST /checkouts/{checkoutId}/fees
- "Create a order?" -> POST /checkouts/{checkoutId}/orders
- "List all settings?" -> GET /checkouts/settings
- "Get channel details?" -> GET /checkouts/settings/channels/{channelId}
- "Update a channel?" -> PUT /checkouts/settings/channels/{channelId}
- "Create a token?" -> POST /checkouts/{checkoutId}/token
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
