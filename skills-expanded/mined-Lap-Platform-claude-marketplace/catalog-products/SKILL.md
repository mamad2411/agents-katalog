---
name: catalog-products
description: "Catalog - Products API skill. Use when working with Catalog - Products for catalog. Covers 53 endpoints."
version: 1.0.0
generator: lapsh
---

# Catalog - Products

## Auth
ApiKey X-Auth-Token in header

## Base URL
https://api.bigcommerce.com/stores/{store_hash}/v3

## Setup
1. Set your API key in the appropriate header
2. GET /catalog/products -- verify access
3. POST /catalog/products -- create first products

## Endpoints

53 endpoints across 1 groups. See references/api-spec.lap for full details.

### catalog
| Method | Path | Description |
|--------|------|-------------|
| GET | /catalog/products | Get All Products |
| PUT | /catalog/products | Update Products (Batch) |
| POST | /catalog/products | Create a Product |
| DELETE | /catalog/products | Delete Products |
| GET | /catalog/products/{product_id} | Get a Product |
| PUT | /catalog/products/{product_id} | Update a Product |
| DELETE | /catalog/products/{product_id} | Delete a Product |
| GET | /catalog/products/{product_id}/images | Get All Product Images |
| POST | /catalog/products/{product_id}/images | Create a Product Image |
| GET | /catalog/products/{product_id}/images/{image_id} | Get a Product Image |
| PUT | /catalog/products/{product_id}/images/{image_id} | Update a Product Image |
| DELETE | /catalog/products/{product_id}/images/{image_id} | Delete a Product Image |
| GET | /catalog/products/{product_id}/videos | Get All Product Videos |
| POST | /catalog/products/{product_id}/videos | Create a Product Video |
| GET | /catalog/products/{product_id}/videos/{id} | Get a Product Video |
| PUT | /catalog/products/{product_id}/videos/{id} | Update a Product Video |
| DELETE | /catalog/products/{product_id}/videos/{id} | Delete a Product Video |
| GET | /catalog/products/{product_id}/complex-rules | Get Complex Rules |
| POST | /catalog/products/{product_id}/complex-rules | Create a Complex Rule |
| GET | /catalog/products/{product_id}/complex-rules/{complex_rule_id} | Get a Product Complex Rule |
| PUT | /catalog/products/{product_id}/complex-rules/{complex_rule_id} | Update a Product Complex Rule |
| DELETE | /catalog/products/{product_id}/complex-rules/{complex_rule_id} | Delete a Product Complex Rule |
| GET | /catalog/products/{product_id}/custom-fields | Get Product Custom Fields |
| POST | /catalog/products/{product_id}/custom-fields | Create a Product Custom Field |
| GET | /catalog/products/{product_id}/custom-fields/{custom_field_id} | Get a Product Custom Field |
| PUT | /catalog/products/{product_id}/custom-fields/{custom_field_id} | Update a Product Custom Field |
| DELETE | /catalog/products/{product_id}/custom-fields/{custom_field_id} | Delete a Product Custom Field |
| POST | /catalog/products/{product_id}/bulk-pricing-rules | Create a Bulk Pricing Rule |
| GET | /catalog/products/{product_id}/bulk-pricing-rules | Get all Bulk Pricing Rules |
| GET | /catalog/products/{product_id}/bulk-pricing-rules/{bulk_pricing_rule_id} | Get a Bulk Pricing Rule |
| PUT | /catalog/products/{product_id}/bulk-pricing-rules/{bulk_pricing_rule_id} | Update a Bulk Pricing Rule |
| DELETE | /catalog/products/{product_id}/bulk-pricing-rules/{bulk_pricing_rule_id} | Delete a Bulk Pricing Rule |
| GET | /catalog/products/{product_id}/metafields | Get Product Metafields |
| POST | /catalog/products/{product_id}/metafields | Create a Product Metafield |
| GET | /catalog/products/{product_id}/metafields/{metafield_id} | Get a Product Metafield |
| PUT | /catalog/products/{product_id}/metafields/{metafield_id} | Update a Product Metafield |
| DELETE | /catalog/products/{product_id}/metafields/{metafield_id} | Delete a Product Metafield |
| GET | /catalog/products/{product_id}/reviews | Get Product Reviews |
| POST | /catalog/products/{product_id}/reviews | Create a Product Review |
| GET | /catalog/products/{product_id}/reviews/{review_id} | Get a Product Review |
| PUT | /catalog/products/{product_id}/reviews/{review_id} | Update a Product Review |
| DELETE | /catalog/products/{product_id}/reviews/{review_id} | Delete a Product Review |
| GET | /catalog/products/channel-assignments | Get Products Channel Assignments |
| PUT | /catalog/products/channel-assignments | Create Products Channel Assignments |
| DELETE | /catalog/products/channel-assignments | Delete Products Channel Assignments |
| GET | /catalog/products/category-assignments | Get Products Category Assignments |
| PUT | /catalog/products/category-assignments | Create Products Category Assignments |
| DELETE | /catalog/products/category-assignments | Delete Products Category Assignments |
| GET | /catalog/summary | Get a Catalog Summary |
| GET | /catalog/products/metafields | Get All Product Metafields |
| POST | /catalog/products/metafields | Create multiple Metafields |
| PUT | /catalog/products/metafields | Update multiple Metafields |
| DELETE | /catalog/products/metafields | Delete Multiple Metafields |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all products?" -> GET /catalog/products
- "Create a product?" -> POST /catalog/products
- "Get product details?" -> GET /catalog/products/{product_id}
- "Update a product?" -> PUT /catalog/products/{product_id}
- "Delete a product?" -> DELETE /catalog/products/{product_id}
- "List all images?" -> GET /catalog/products/{product_id}/images
- "Create a image?" -> POST /catalog/products/{product_id}/images
- "Get image details?" -> GET /catalog/products/{product_id}/images/{image_id}
- "Update a image?" -> PUT /catalog/products/{product_id}/images/{image_id}
- "Delete a image?" -> DELETE /catalog/products/{product_id}/images/{image_id}
- "List all videos?" -> GET /catalog/products/{product_id}/videos
- "Create a video?" -> POST /catalog/products/{product_id}/videos
- "Get video details?" -> GET /catalog/products/{product_id}/videos/{id}
- "Update a video?" -> PUT /catalog/products/{product_id}/videos/{id}
- "Delete a video?" -> DELETE /catalog/products/{product_id}/videos/{id}
- "List all complex-rules?" -> GET /catalog/products/{product_id}/complex-rules
- "Create a complex-rule?" -> POST /catalog/products/{product_id}/complex-rules
- "Get complex-rule details?" -> GET /catalog/products/{product_id}/complex-rules/{complex_rule_id}
- "Update a complex-rule?" -> PUT /catalog/products/{product_id}/complex-rules/{complex_rule_id}
- "Delete a complex-rule?" -> DELETE /catalog/products/{product_id}/complex-rules/{complex_rule_id}
- "List all custom-fields?" -> GET /catalog/products/{product_id}/custom-fields
- "Create a custom-field?" -> POST /catalog/products/{product_id}/custom-fields
- "Get custom-field details?" -> GET /catalog/products/{product_id}/custom-fields/{custom_field_id}
- "Update a custom-field?" -> PUT /catalog/products/{product_id}/custom-fields/{custom_field_id}
- "Delete a custom-field?" -> DELETE /catalog/products/{product_id}/custom-fields/{custom_field_id}
- "Create a bulk-pricing-rule?" -> POST /catalog/products/{product_id}/bulk-pricing-rules
- "List all bulk-pricing-rules?" -> GET /catalog/products/{product_id}/bulk-pricing-rules
- "Get bulk-pricing-rule details?" -> GET /catalog/products/{product_id}/bulk-pricing-rules/{bulk_pricing_rule_id}
- "Update a bulk-pricing-rule?" -> PUT /catalog/products/{product_id}/bulk-pricing-rules/{bulk_pricing_rule_id}
- "Delete a bulk-pricing-rule?" -> DELETE /catalog/products/{product_id}/bulk-pricing-rules/{bulk_pricing_rule_id}
- "List all metafields?" -> GET /catalog/products/{product_id}/metafields
- "Create a metafield?" -> POST /catalog/products/{product_id}/metafields
- "Get metafield details?" -> GET /catalog/products/{product_id}/metafields/{metafield_id}
- "Update a metafield?" -> PUT /catalog/products/{product_id}/metafields/{metafield_id}
- "Delete a metafield?" -> DELETE /catalog/products/{product_id}/metafields/{metafield_id}
- "List all reviews?" -> GET /catalog/products/{product_id}/reviews
- "Create a review?" -> POST /catalog/products/{product_id}/reviews
- "Get review details?" -> GET /catalog/products/{product_id}/reviews/{review_id}
- "Update a review?" -> PUT /catalog/products/{product_id}/reviews/{review_id}
- "Delete a review?" -> DELETE /catalog/products/{product_id}/reviews/{review_id}
- "List all channel-assignments?" -> GET /catalog/products/channel-assignments
- "List all category-assignments?" -> GET /catalog/products/category-assignments
- "List all summary?" -> GET /catalog/summary
- "List all metafields?" -> GET /catalog/products/metafields
- "Create a metafield?" -> POST /catalog/products/metafields
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
