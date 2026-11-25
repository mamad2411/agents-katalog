---
name: woocommerce-rest-api
description: "WooCommerce REST API skill. Use when working with WooCommerce REST for customers, products, orders. Covers 122 endpoints."
version: 1.0.0
generator: lapsh
---

# WooCommerce REST API
API version: v3

## Auth
Bearer basic

## Base URL
https://example-woocommerce-shop.com/wp-json/wc/v3

## Setup
1. Set Authorization header with your Bearer token
2. GET /customers -- verify access
3. POST /customers -- create first customers

## Endpoints

122 endpoints across 11 groups. See references/api-spec.lap for full details.

### customers
| Method | Path | Description |
|--------|------|-------------|
| POST | /customers | This API helps you to create a new customer. |
| GET | /customers | This API helps you to view all the customers. |
| GET | /customers/{customerId} | This API lets you retrieve and view a specific customer by ID. |
| PUT | /customers/{customerId} | This API lets you make changes to a customer. |
| DELETE | /customers/{customerId} | This API helps you delete a customer. |
| POST | /customers/batch | Batch create, update, and delete customers |

### products
| Method | Path | Description |
|--------|------|-------------|
| POST | /products | This API helps you to create a new product. |
| GET | /products | This API helps you to view all the products. |
| GET | /products/{productId} | This API lets you retrieve and view a specific product by ID. |
| PUT | /products/{productId} | This API lets you make changes to a product. |
| DELETE | /products/{productId} | This API helps you delete a product. |
| POST | /products/{productId}/duplicate | This API helps you to duplicate a product. |
| POST | /products/batch | Batch create, update, and delete products |
| POST | /products/{productId}/variations | This API helps you to create a new product variation. |
| GET | /products/{productId}/variations | This API helps you to view all the product variations. |
| GET | /products/{productId}/variations/{variationId} | This API lets you retrieve and view a specific product variation by ID. |
| PUT | /products/{productId}/variations/{variationId} | This API lets you make changes to a product variation. |
| DELETE | /products/{productId}/variations/{variationId} | This API helps you delete a product variation. |
| POST | /products/{productId}/variations/batch | Batch create, update, and delete product variations |
| GET | /products/attributes | List all product attributes |
| POST | /products/attributes | Create a product attribute |
| GET | /products/attributes/{attributeId} | Retrieve a product attribute |
| PUT | /products/attributes/{attributeId} | Update a product attribute |
| DELETE | /products/attributes/{attributeId} | Delete a product attribute |
| POST | /products/attributes/batch | Batch update product attributes |
| GET | /products/attributes/{attributeId}/terms | List all terms for a product attribute |
| POST | /products/attributes/{attributeId}/terms | Create an attribute term |
| GET | /products/attributes/{attributeId}/terms/{termId} | Retrieve an attribute term |
| PUT | /products/attributes/{attributeId}/terms/{termId} | Update an attribute term |
| DELETE | /products/attributes/{attributeId}/terms/{termId} | Delete an attribute term |
| POST | /products/attributes/{attributeId}/terms/batch | Batch update attribute terms |
| POST | /products/categories | This API helps you to create a new product category. |
| GET | /products/categories | This API lets you retrieve all product categories. |
| GET | /products/categories/{categoryId} | This API lets you retrieve a product category by ID. |
| PUT | /products/categories/{categoryId} | This API lets you make changes to a product category. |
| DELETE | /products/categories/{categoryId} | This API helps you delete a product category. |
| POST | /products/categories/batch | Batch create, update, and delete product categories |
| GET | /products/shipping-classes | List all shipping classes |
| POST | /products/shipping-classes | Create a shipping class |
| GET | /products/shipping-classes/{classId} | Retrieve a shipping class |
| PUT | /products/shipping-classes/{classId} | Update a shipping class |
| DELETE | /products/shipping-classes/{classId} | Delete a shipping class |
| POST | /products/shipping-classes/batch | Batch update shipping classes |
| POST | /products/tags | This API helps you to create a new product tag. |
| GET | /products/tags | This API lets you retrieve all product tags. |
| GET | /products/tags/{tagId} | This API lets you retrieve a product tag by ID. |
| PUT | /products/tags/{tagId} | This API lets you make changes to a product tag. |
| DELETE | /products/tags/{tagId} | This API helps you delete a product tag. |
| POST | /products/tags/batch | Batch create, update, and delete product tags |
| GET | /products/reviews | List all product reviews |
| POST | /products/reviews | Create a product review |
| GET | /products/reviews/{reviewId} | Retrieve a product review |
| PUT | /products/reviews/{reviewId} | Update a product review |
| DELETE | /products/reviews/{reviewId} | Delete a product review |
| POST | /products/reviews/batch | Batch update product reviews |

### orders
| Method | Path | Description |
|--------|------|-------------|
| POST | /orders | This API helps you to create a new order. |
| GET | /orders | This API helps you to view all the orders. |
| GET | /orders/{orderId} | This API lets you retrieve and view a specific order. |
| PUT | /orders/{orderId} | This API lets you make changes to an order. |
| DELETE | /orders/{orderId} | This API helps you delete an order. |
| POST | /orders/batch | Batch create, update, and delete orders |
| GET | /orders/{orderId}/notes | This API helps you to view all notes for an order. |
| POST | /orders/{orderId}/notes | This API helps you to create a new order note. |
| GET | /orders/{orderId}/notes/{noteId} | This API lets you retrieve and view a specific order note by ID. |
| DELETE | /orders/{orderId}/notes/{noteId} | This API helps you delete an order note. |
| GET | /orders/{orderId}/refunds | This API helps you to view all refunds for an order. |
| POST | /orders/{orderId}/refunds | This API helps you to create a new order refund. |
| GET | /orders/{orderId}/refunds/{refundId} | This API lets you retrieve and view a specific order refund by ID. |
| DELETE | /orders/{orderId}/refunds/{refundId} | This API helps you delete an order refund. |

### reports
| Method | Path | Description |
|--------|------|-------------|
| GET | /reports | List all reports |
| GET | /reports/top_sellers | Retrieve top sellers report |
| GET | /reports/coupons/totals | Retrieve coupons totals report |
| GET | /reports/customers/totals | Retrieve customers totals report |
| GET | /reports/orders/totals | This API lets you retrieve and view orders totals report. |
| GET | /reports/products/totals | Retrieve products totals report |
| GET | /reports/reviews/totals | Retrieve reviews totals report |
| GET | /reports/sales | This API lets you retrieve and view a sales report. |

### coupons
| Method | Path | Description |
|--------|------|-------------|
| GET | /coupons | This API helps you to view all coupons. |
| POST | /coupons | This API helps you to create a new coupon. |
| GET | /coupons/{couponId} | This API lets you retrieve and view a specific coupon by ID. |
| PUT | /coupons/{couponId} | This API helps you to update a coupon. |
| DELETE | /coupons/{couponId} | This API helps you delete a coupon. |
| POST | /coupons/batch | Batch create, update, and delete coupons |

### settings
| Method | Path | Description |
|--------|------|-------------|
| GET | /settings | This API helps you to view all settings groups. |
| GET | /settings/{groupId} | This API helps you to view a specific settings group. |
| GET | /settings/{groupId}/{id} | This API helps you to view a specific setting. |
| PUT | /settings/{groupId}/{id} | This API helps you to update a specific setting. |

### shipping
| Method | Path | Description |
|--------|------|-------------|
| GET | /shipping/zones | This API helps you to view all shipping zones. |
| POST | /shipping/zones | This API helps you to create a new shipping zone. |
| GET | /shipping/zones/{id} | This API lets you retrieve and view a specific shipping zone by ID. |
| PUT | /shipping/zones/{id} | This API helps you to update a shipping zone. |
| DELETE | /shipping/zones/{id} | This API helps you delete a shipping zone. |
| GET | /shipping/zones/{id}/locations | This API helps you to view all locations for a shipping zone. |
| PUT | /shipping/zones/{id}/locations | This API helps you to update locations for a shipping zone. |
| GET | /shipping/zones/{id}/methods | This API helps you to view all shipping methods for a shipping zone. |
| POST | /shipping/zones/{id}/methods | This API helps you to create a new shipping method for a shipping zone. |
| GET | /shipping/zones/{id}/methods/{instanceId} | This API lets you retrieve and view a specific shipping zone method by instance ID. |
| PUT | /shipping/zones/{id}/methods/{instanceId} | This API helps you to update a shipping zone method. |
| DELETE | /shipping/zones/{id}/methods/{instanceId} | This API helps you delete a shipping zone method. |

### payment_gateways
| Method | Path | Description |
|--------|------|-------------|
| GET | /payment_gateways | This API helps you to view all payment gateways. |
| GET | /payment_gateways/{id} | This API lets you retrieve and view a specific payment gateway by ID. |
| PUT | /payment_gateways/{id} | This API helps you to update a payment gateway. |

### taxes
| Method | Path | Description |
|--------|------|-------------|
| GET | /taxes | This API helps you to view all taxes. |
| POST | /taxes | This API helps you to create a new tax. |
| GET | /taxes/{id} | This API lets you retrieve and view a specific tax by ID. |
| PUT | /taxes/{id} | This API helps you to update a tax. |
| DELETE | /taxes/{id} | This API helps you delete a tax. |
| POST | /taxes/batch | Batch create, update, and delete taxes |
| GET | /taxes/classes | This API helps you to view all tax classes. |
| POST | /taxes/classes | This API helps you to create a new tax class. |
| GET | /taxes/classes/{slug} | This API lets you retrieve and view a specific tax class by slug. |
| DELETE | /taxes/classes/{slug} | This API helps you delete a tax class. |

### webhooks
| Method | Path | Description |
|--------|------|-------------|
| GET | /webhooks | This API helps you to view all webhooks. |
| POST | /webhooks | This API helps you to create a new webhook. |
| GET | /webhooks/{id} | This API lets you retrieve and view a specific webhook by ID. |
| PUT | /webhooks/{id} | This API helps you to update a webhook. |
| DELETE | /webhooks/{id} | This API helps you delete a webhook. |
| POST | /webhooks/batch | Batch create, update, and delete webhooks |

### system_status
| Method | Path | Description |
|--------|------|-------------|
| GET | /system_status | This API helps you to view the system status. |
| GET | /system_status/tools | This API helps you to view all system status tools. |
| GET | /system_status/tools/{id} | This API lets you retrieve and view a specific system status tool by ID. |
| PUT | /system_status/tools/{id} | This API helps you to run a system status tool. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a customer?" -> POST /customers
- "Search customers?" -> GET /customers
- "Get customer details?" -> GET /customers/{customerId}
- "Update a customer?" -> PUT /customers/{customerId}
- "Delete a customer?" -> DELETE /customers/{customerId}
- "Create a batch?" -> POST /customers/batch
- "Create a product?" -> POST /products
- "Search products?" -> GET /products
- "Get product details?" -> GET /products/{productId}
- "Update a product?" -> PUT /products/{productId}
- "Delete a product?" -> DELETE /products/{productId}
- "Create a duplicate?" -> POST /products/{productId}/duplicate
- "Create a batch?" -> POST /products/batch
- "Create a variation?" -> POST /products/{productId}/variations
- "Search variations?" -> GET /products/{productId}/variations
- "Get variation details?" -> GET /products/{productId}/variations/{variationId}
- "Update a variation?" -> PUT /products/{productId}/variations/{variationId}
- "Delete a variation?" -> DELETE /products/{productId}/variations/{variationId}
- "Create a batch?" -> POST /products/{productId}/variations/batch
- "List all attributes?" -> GET /products/attributes
- "Create a attribute?" -> POST /products/attributes
- "Get attribute details?" -> GET /products/attributes/{attributeId}
- "Update a attribute?" -> PUT /products/attributes/{attributeId}
- "Delete a attribute?" -> DELETE /products/attributes/{attributeId}
- "Create a batch?" -> POST /products/attributes/batch
- "Search terms?" -> GET /products/attributes/{attributeId}/terms
- "Create a term?" -> POST /products/attributes/{attributeId}/terms
- "Get term details?" -> GET /products/attributes/{attributeId}/terms/{termId}
- "Update a term?" -> PUT /products/attributes/{attributeId}/terms/{termId}
- "Delete a term?" -> DELETE /products/attributes/{attributeId}/terms/{termId}
- "Create a batch?" -> POST /products/attributes/{attributeId}/terms/batch
- "Create a category?" -> POST /products/categories
- "Search categories?" -> GET /products/categories
- "Get category details?" -> GET /products/categories/{categoryId}
- "Update a category?" -> PUT /products/categories/{categoryId}
- "Delete a category?" -> DELETE /products/categories/{categoryId}
- "Create a batch?" -> POST /products/categories/batch
- "Search shipping-classes?" -> GET /products/shipping-classes
- "Create a shipping-class?" -> POST /products/shipping-classes
- "Get shipping-class details?" -> GET /products/shipping-classes/{classId}
- "Update a shipping-class?" -> PUT /products/shipping-classes/{classId}
- "Delete a shipping-class?" -> DELETE /products/shipping-classes/{classId}
- "Create a batch?" -> POST /products/shipping-classes/batch
- "Create a tag?" -> POST /products/tags
- "Search tags?" -> GET /products/tags
- "Get tag details?" -> GET /products/tags/{tagId}
- "Update a tag?" -> PUT /products/tags/{tagId}
- "Delete a tag?" -> DELETE /products/tags/{tagId}
- "Create a batch?" -> POST /products/tags/batch
- "Create a order?" -> POST /orders
- "Search orders?" -> GET /orders
- "Get order details?" -> GET /orders/{orderId}
- "Update a order?" -> PUT /orders/{orderId}
- "Delete a order?" -> DELETE /orders/{orderId}
- "Create a batch?" -> POST /orders/batch
- "List all notes?" -> GET /orders/{orderId}/notes
- "Create a note?" -> POST /orders/{orderId}/notes
- "Get note details?" -> GET /orders/{orderId}/notes/{noteId}
- "Delete a note?" -> DELETE /orders/{orderId}/notes/{noteId}
- "Search reviews?" -> GET /products/reviews
- "Create a review?" -> POST /products/reviews
- "Get review details?" -> GET /products/reviews/{reviewId}
- "Update a review?" -> PUT /products/reviews/{reviewId}
- "Delete a review?" -> DELETE /products/reviews/{reviewId}
- "Create a batch?" -> POST /products/reviews/batch
- "List all reports?" -> GET /reports
- "List all top_sellers?" -> GET /reports/top_sellers
- "List all totals?" -> GET /reports/coupons/totals
- "List all totals?" -> GET /reports/customers/totals
- "List all totals?" -> GET /reports/orders/totals
- "List all totals?" -> GET /reports/products/totals
- "List all totals?" -> GET /reports/reviews/totals
- "List all sales?" -> GET /reports/sales
- "List all refunds?" -> GET /orders/{orderId}/refunds
- "Create a refund?" -> POST /orders/{orderId}/refunds
- "Get refund details?" -> GET /orders/{orderId}/refunds/{refundId}
- "Delete a refund?" -> DELETE /orders/{orderId}/refunds/{refundId}
- "Search coupons?" -> GET /coupons
- "Create a coupon?" -> POST /coupons
- "Get coupon details?" -> GET /coupons/{couponId}
- "Update a coupon?" -> PUT /coupons/{couponId}
- "Delete a coupon?" -> DELETE /coupons/{couponId}
- "Create a batch?" -> POST /coupons/batch
- "List all settings?" -> GET /settings
- "Get setting details?" -> GET /settings/{groupId}
- "Get setting details?" -> GET /settings/{groupId}/{id}
- "Update a setting?" -> PUT /settings/{groupId}/{id}
- "List all zones?" -> GET /shipping/zones
- "Create a zone?" -> POST /shipping/zones
- "Get zone details?" -> GET /shipping/zones/{id}
- "Update a zone?" -> PUT /shipping/zones/{id}
- "Delete a zone?" -> DELETE /shipping/zones/{id}
- "List all locations?" -> GET /shipping/zones/{id}/locations
- "List all methods?" -> GET /shipping/zones/{id}/methods
- "Create a method?" -> POST /shipping/zones/{id}/methods
- "Get method details?" -> GET /shipping/zones/{id}/methods/{instanceId}
- "Update a method?" -> PUT /shipping/zones/{id}/methods/{instanceId}
- "Delete a method?" -> DELETE /shipping/zones/{id}/methods/{instanceId}
- "List all payment_gateways?" -> GET /payment_gateways
- "Get payment_gateway details?" -> GET /payment_gateways/{id}
- "Update a payment_gateway?" -> PUT /payment_gateways/{id}
- "Search taxes?" -> GET /taxes
- "Create a taxe?" -> POST /taxes
- "Get taxe details?" -> GET /taxes/{id}
- "Update a taxe?" -> PUT /taxes/{id}
- "Delete a taxe?" -> DELETE /taxes/{id}
- "Create a batch?" -> POST /taxes/batch
- "List all classes?" -> GET /taxes/classes
- "Create a class?" -> POST /taxes/classes
- "Get class details?" -> GET /taxes/classes/{slug}
- "Delete a class?" -> DELETE /taxes/classes/{slug}
- "Search webhooks?" -> GET /webhooks
- "Create a webhook?" -> POST /webhooks
- "Get webhook details?" -> GET /webhooks/{id}
- "Update a webhook?" -> PUT /webhooks/{id}
- "Delete a webhook?" -> DELETE /webhooks/{id}
- "Create a batch?" -> POST /webhooks/batch
- "List all system_status?" -> GET /system_status
- "List all tools?" -> GET /system_status/tools
- "Get tool details?" -> GET /system_status/tools/{id}
- "Update a tool?" -> PUT /system_status/tools/{id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
