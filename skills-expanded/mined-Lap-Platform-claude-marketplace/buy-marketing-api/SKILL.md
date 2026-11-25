---
name: buy-marketing-api
description: "Buy Marketing API skill. Use when working with Buy Marketing for merchandised_product. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Buy Marketing API
API version: v1_beta.2.0

## Auth
OAuth2

## Base URL
https://api.ebay.com/buy/marketing/v1_beta

## Setup
1. Configure auth: OAuth2
2. GET /merchandised_product -- verify access

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### merchandised_product
| Method | Path | Description |
|--------|------|-------------|
| GET | /merchandised_product | This method returns an array of products based on the category and metric specified. This includes details of the product, such as the eBay product ID (EPID), title, and user reviews and ratings for the product. You can use the <code>epid</code> returned by this method in the Browse API <b>search</b> method to retrieve items for this product. <h3><b>Restrictions </b></h3> <ul><li>To test <b> getMerchandisedProducts</b> in Sandbox, you must use category ID 9355 and the response will be mock data.  </li>   <li>For a list of supported sites and other restrictions, see <a href="/api-docs/buy/marketing/overview.html#API">API Restrictions</a>.</li>  </ul> |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all merchandised_product?" -> GET /merchandised_product
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
