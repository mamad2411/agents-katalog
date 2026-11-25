---
name: jumpseller-api
description: "Jumpseller API skill. Use when working with Jumpseller for store, hooks.json, hooks. Covers 182 endpoints."
version: 1.0.0
generator: lapsh
---

# Jumpseller API
API version: 1.0.0

## Auth
Bearer basic | ApiKey login in query | ApiKey authtoken in query | ApiKey partner_code in query | ApiKey auth_token in query

## Base URL
https://api.jumpseller.com/v1

## Setup
1. Set Authorization header with your Bearer token
2. GET /store/info.json -- verify access
3. POST /hooks.json -- create first hooks.json

## Endpoints

182 endpoints across 42 groups. See references/api-spec.lap for full details.

### store
| Method | Path | Description |
|--------|------|-------------|
| GET | /store/info.json | Retrieve Store Information. |
| GET | /store/languages.json | Retrieve Store Languages. |
| POST | /store/create.json | Create a Partnered Store |
| GET | /store/check_status.json | Retrive store creation status. |

### hooks.json
| Method | Path | Description |
|--------|------|-------------|
| GET | /hooks.json | Retrieve all Hooks. |
| POST | /hooks.json | Create a new Hook. |

### hooks
| Method | Path | Description |
|--------|------|-------------|
| GET | /hooks/{id}.json | Retrieve a single Hook. |
| PUT | /hooks/{id}.json | Update a Hook. |
| DELETE | /hooks/{id}.json | Delete an existing Hook. |

### jsapps.json
| Method | Path | Description |
|--------|------|-------------|
| GET | /jsapps.json | Retrieve all the Store's JSApps. |
| POST | /jsapps.json | Create a Store JSApp. |

### jsapps
| Method | Path | Description |
|--------|------|-------------|
| GET | /jsapps/{code}.json | Retrieve a JSApp. |
| DELETE | /jsapps/{code}.json | Delete an existing JSApp. |

### apps
| Method | Path | Description |
|--------|------|-------------|
| GET | /apps/{code}/install_status.json | Retrieve an OauthApplication installation status. |
| GET | /apps/{code}/install_status_by_store_id.json | Retrieve an OauthApplication installation status for a specific Store. |
| GET | /apps/{code}/billing_cycle_dates.json | Retrieve billing cycle start and billing cycle end for an OauthApplication. |
| GET | /apps/{code}/billing_cycle_orders.json | Retrieve billing cycle orders for an OauthApplication. |
| GET | /apps/{code}/check_billing_cycle_order.json | Retrieve a billing cycle order information for an OauthApplication. |

### products.json
| Method | Path | Description |
|--------|------|-------------|
| GET | /products.json | Retrieve all Products. |
| POST | /products.json | Create a new Product. |

### products
| Method | Path | Description |
|--------|------|-------------|
| GET | /products/count.json | Count all Products. |
| GET | /products/after/{id}.json | Retrieves Products after the given id. |
| GET | /products/status/{status}.json | Retrieve Products filtered by status. |
| GET | /products/category/{category_id}.json | Retrieve Products filtered by category. |
| GET | /products/status/{status}/count.json | Count Products filtered by status. |
| GET | /products/category/{category_id}/count.json | Count Products filtered by category. |
| GET | /products/{id}/reviews.json | Retrieve all reviews for a specific Product. |
| GET | /products/reviews/{review_id}.json | Retrieve a single Product Review. |
| GET | /products/reviews.json | Retrieve all Product Reviews. |
| GET | /products/{id}.json | Retrieve a single Product. |
| PUT | /products/{id}.json | Modify an existing Product. |
| DELETE | /products/{id}.json | Delete an existing Product. |
| GET | /products/search.json | Retrieve a Product List from a query. |
| GET | /products/{id}/options.json | Retrieve all Product Options. |
| POST | /products/{id}/options.json | Create a new Product Option. |
| GET | /products/{id}/options/count.json | Count all Product Options. |
| GET | /products/{id}/options/{option_id}.json | Retrieve a single Product Option. |
| PUT | /products/{id}/options/{option_id}.json | Modify an existing Product Option. |
| DELETE | /products/{id}/options/{option_id}.json | Delete a Product Option. |
| GET | /products/{id}/options/{option_id}/values.json | Retrieve all Product Option Values. |
| POST | /products/{id}/options/{option_id}/values.json | Create a new Product Option Value. |
| GET | /products/{id}/options/{option_id}/values/count.json | Count all Product Option Values. |
| GET | /products/{id}/options/{option_id}/values/{value_id}.json | Retrieve a single Product Option Value. |
| PUT | /products/{id}/options/{option_id}/values/{value_id}.json | Modify an existing Product Option Value. |
| DELETE | /products/{id}/options/{option_id}/values/{value_id}.json | Delete a Product Option Value. |
| GET | /products/{id}/variants/{variant_id}.json | Retrieve a single Product Variant. |
| PUT | /products/{id}/variants/{variant_id}.json | Modify an existing Product Variant. |
| GET | /products/{id}/variants.json | Retrieve all Product Variants. |
| POST | /products/{id}/variants.json | Create a new Product Variant. |
| GET | /products/{id}/variants/count.json | Count all Product Variants. |
| GET | /products/{id}/images.json | Retrieve all Product Images. |
| POST | /products/{id}/images.json | Create a new Product Image. |
| PUT | /products/{product_id}/images/{image_id}.json | Update a Product Image position. |
| GET | /products/{id}/images/count.json | Count all Product Images. |
| GET | /products/{id}/images/{image_id}.json | Retrieve a single Product Image. |
| DELETE | /products/{id}/images/{image_id}.json | Delete a Product Image. |
| GET | /products/{id}/attachments.json | Retrieve all Product Attachments. |
| POST | /products/{id}/attachments.json | Create a new Product Attachment. |
| GET | /products/{id}/attachments/count.json | Count all Product Attachments. |
| GET | /products/{id}/attachments/{attachment_id}.json | Retrieve a single Product Attachment. |
| DELETE | /products/{id}/attachments/{attachment_id}.json | Delete a Product Attachment. |
| GET | /products/{id}/digital_products.json | Retrieve all Product DigitalProducts. |
| POST | /products/{id}/digital_products.json | Create a new Product DigitalProduct. |
| GET | /products/{id}/digital_products/count.json | Count all Product DigitalProducts. |
| GET | /products/{id}/digital_products/{digital_product_id}.json | Retrieve a single Product DigitalProduct. |
| DELETE | /products/{id}/digital_products/{digital_product_id}.json | Delete a Product DigitalProduct. |
| GET | /products/{id}/fields.json | Retrieve all Product Custom Fields |
| POST | /products/{id}/fields.json | Add an existing Custom Field to a Product. |
| GET | /products/{id}/fields/count.json | Count all Product Custom Fields. |
| PUT | /products/{product_id}/fields/{field_id}.json | Update value of Product Custom Field |
| DELETE | /products/{product_id}/fields/{field_id}.json | Delete value of Product Custom Field |

### categories.json
| Method | Path | Description |
|--------|------|-------------|
| GET | /categories.json | Retrieve all Categories. |
| POST | /categories.json | Create a new Category. |

### categories
| Method | Path | Description |
|--------|------|-------------|
| GET | /categories/count.json | Count all Categories. |
| GET | /categories/{id}.json | Retrieve a single Category. |
| PUT | /categories/{id}.json | Modify an existing Category. |
| DELETE | /categories/{id}.json | Delete an existing Category. |

### orders.json
| Method | Path | Description |
|--------|------|-------------|
| GET | /orders.json | Retrieve all Orders. |
| POST | /orders.json | Create a new Order. |

### orders
| Method | Path | Description |
|--------|------|-------------|
| GET | /orders/count.json | Count all Orders. |
| GET | /orders/status/{status}.json | Retrieve orders filtered by status. |
| GET | /orders/{id}.json | Retrieve a single Order. |
| PUT | /orders/{id}.json | Modify an existing Order. |
| GET | /orders/search.json | Retrieve an Orders List from a query. |
| GET | /orders/after/{id}.json | Retrieve orders filtered by Order Id. |
| GET | /orders/{id}/history.json | Retrieve all Order History. |
| POST | /orders/{id}/history.json | Create a new Order History Entry. |
| GET | /orders/{id}/documents.json | Retrieve all Documents from an  Order. |
| POST | /orders/{id}/documents.json | Create a new Order Document Entry. |
| PUT | /orders/{id}/documents/{public_id}.json | Update a Document from an Order. |
| DELETE | /orders/{id}/documents/{public_id}.json | Delete a Document from an Order. |

### fulfillments
| Method | Path | Description |
|--------|------|-------------|
| GET | /fulfillments/count.json | Count all Fulfillments. |
| POST | /fulfillments/rates.json | Rates for fulfillment. |
| GET | /fulfillments/{id}/label.json | Retrieve a presigned URL for the Fulfillment label |
| GET | /fulfillments/{id}.json | Retrieve a single Fulfillment. |
| PUT | /fulfillments/{id}.json | Modify an existing Fulfillment. |

### fulfillments.json
| Method | Path | Description |
|--------|------|-------------|
| GET | /fulfillments.json | Retrieve all Fulfillments. |
| POST | /fulfillments.json | Create a new Fulfillment. |

### order
| Method | Path | Description |
|--------|------|-------------|
| GET | /order/{id}/fulfillments.json | Retrieve the Fulfillments associated with the Order. |

### pages.json
| Method | Path | Description |
|--------|------|-------------|
| GET | /pages.json | Retrieve all Pages. |
| POST | /pages.json | Create a new Page. |

### pages
| Method | Path | Description |
|--------|------|-------------|
| GET | /pages/count.json | Count all Pages. |
| GET | /pages/{id}.json | Retrieve a single Page by id. |
| PUT | /pages/{id}.json | Update a Page. |
| DELETE | /pages/{id}.json | Delete an existing Page. |
| GET | /pages/{id}/images.json | Retrieve all Page Images. |
| POST | /pages/{id}/images.json | Create a new Page Image. |
| GET | /pages/{id}/images/count.json | Count all Page Images. |
| GET | /pages/{id}/images/{image_id}.json | Retrieve a single Page Image. |
| PUT | /pages/{id}/images/{image_id}.json | Update a Page Image url. |
| DELETE | /pages/{id}/images/{image_id}.json | Delete a Page Image. |

### customers.json
| Method | Path | Description |
|--------|------|-------------|
| GET | /customers.json | Retrieve all Customers. |
| POST | /customers.json | Create a new Customer. |

### customers
| Method | Path | Description |
|--------|------|-------------|
| GET | /customers/count.json | Count all Customers. |
| GET | /customers/email/{email}.json | Retrieve a single Customer by email. |
| GET | /customers/{id}/orders.json | Retrieve all orders of single Customer |
| GET | /customers/{id}/orders/status/{status}.json | Retrieve all orders of single Customer |
| GET | /customers/{id}.json | Retrieve a single Customer by id. |
| PUT | /customers/{id}.json | Update a new Customer. |
| DELETE | /customers/{id}.json | Delete an existing Customer. |
| GET | /customers/search.json | Retrieve a Customer List from a query. |
| GET | /customers/{id}/fields | Retrieves the Customer Additional Field of a Customer. |
| POST | /customers/{id}/fields | Adds Customer Additional Fields to a Customer. |
| GET | /customers/{id}/fields/{field_id} | Retrieve a single Customer Additional Field. |
| PUT | /customers/{id}/fields/{field_id} | Update a Customer Additional Field. |
| DELETE | /customers/{id}/fields/{field_id} | Delete a Customer Additional Field. |

### customer_categories.json
| Method | Path | Description |
|--------|------|-------------|
| GET | /customer_categories.json | Retrieve all Customer Categories. |
| POST | /customer_categories.json | Create a new CustomerCategory. |

### customer_categories
| Method | Path | Description |
|--------|------|-------------|
| GET | /customer_categories/{id}.json | Retrieve a single CustomerCategory. |
| PUT | /customer_categories/{id}.json | Update a CustomerCategory. |
| DELETE | /customer_categories/{id}.json | Delete an existing CustomerCategory. |
| GET | /customer_categories/{id}/customers.json | Retrieves the customers in a CustomerCategory. |
| POST | /customer_categories/{id}/customers.json | Adds Customers to a CustomerCategory. |
| DELETE | /customer_categories/{id}/customers/{customer_id}.json | Delete Customer from an existing CustomerCategory. |

### promotions.json
| Method | Path | Description |
|--------|------|-------------|
| GET | /promotions.json | Retrieve all Promotions. |
| POST | /promotions.json | Create a new Promotion. |

### promotions
| Method | Path | Description |
|--------|------|-------------|
| GET | /promotions/{id}.json | Retrieve a single Promotion. |
| PUT | /promotions/{id}.json | Update a Promotion. |
| DELETE | /promotions/{id}.json | Delete an existing Promotion. |

### payment_methods.json
| Method | Path | Description |
|--------|------|-------------|
| GET | /payment_methods.json | Retrieve all Store's Payment Methods. |
| POST | /payment_methods.json | Creates an External Payment Method. |

### payment_methods
| Method | Path | Description |
|--------|------|-------------|
| GET | /payment_methods/{id}.json | Retrieve a single Payment Method. |

### shipping_methods.json
| Method | Path | Description |
|--------|------|-------------|
| GET | /shipping_methods.json | Retrieve all Store's Shipping Methods. |
| POST | /shipping_methods.json | Creates a Shipping Method. |

### shipping_methods
| Method | Path | Description |
|--------|------|-------------|
| GET | /shipping_methods/{id}.json | Retrieve a single Shipping Method. |
| PUT | /shipping_methods/{id}.json | Update a Shipping Method. |
| DELETE | /shipping_methods/{id}.json | Delete an existing Shipping Method. |

### locations.json
| Method | Path | Description |
|--------|------|-------------|
| GET | /locations.json | Retrieve all Store's Locations |
| POST | /locations.json | Create a Pickup Location |

### locations
| Method | Path | Description |
|--------|------|-------------|
| GET | /locations/{id}.json | Retrieve a Store's Locations by ID |
| PUT | /locations/{id}.json | Update a Pickup Location |
| DELETE | /locations/{id}.json | Delete a Store's Locations by ID |

### custom_fields.json
| Method | Path | Description |
|--------|------|-------------|
| GET | /custom_fields.json | Retrieve all Store's Custom Fields. |
| POST | /custom_fields.json | Create a new Custom Field. |

### custom_fields
| Method | Path | Description |
|--------|------|-------------|
| GET | /custom_fields/{id}.json | Retrieve a single CustomField. |
| PUT | /custom_fields/{id}.json | Update a CustomField. |
| DELETE | /custom_fields/{id}.json | Delete an existing CustomField. |
| GET | /custom_fields/{id}/select_options.json | Retrieve all Store's Custom Fields. |
| POST | /custom_fields/{id}/select_options.json | Create a new Custom Field Select Option. |
| GET | /custom_fields/{id}/select_options/{custom_field_select_option_id}.json | Retrieve a single SelectOption from a CustomField. |
| PUT | /custom_fields/{id}/select_options/{custom_field_select_option_id}.json | Update a SelectOption from a CustomField. |
| DELETE | /custom_fields/{id}/select_options/{custom_field_select_option_id}.json | Delete an existing CustomFieldSelectOption. |

### checkout_custom_fields.json
| Method | Path | Description |
|--------|------|-------------|
| GET | /checkout_custom_fields.json | Retrieve all Checkout Custom Fields. |
| POST | /checkout_custom_fields.json | Create a new CheckoutCustomField. |

### checkout_custom_fields
| Method | Path | Description |
|--------|------|-------------|
| GET | /checkout_custom_fields/{id}.json | Retrieve a single CheckoutCustomField. |
| PUT | /checkout_custom_fields/{id}.json | Update a CheckoutCustomField. |
| DELETE | /checkout_custom_fields/{id}.json | Delete an existing CheckoutCustomField. |

### countries.json
| Method | Path | Description |
|--------|------|-------------|
| GET | /countries.json | Retrieve all Countries. |

### countries
| Method | Path | Description |
|--------|------|-------------|
| GET | /countries/{country_code}.json | Retrieve a single Country information. |
| GET | /countries/{country_code}/regions.json | Retrieve all Regions from a single Country. |
| GET | /countries/{country_code}/regions/{region_code}/municipalities.json | Retrieve all Municipalities from a single Region. |
| GET | /countries/{country_code}/regions/{region_code}.json | Retrieve a single Region information object. |

### taxes.json
| Method | Path | Description |
|--------|------|-------------|
| GET | /taxes.json | Retrieve all Taxes. |
| POST | /taxes.json | Create a new Tax. |

### taxes
| Method | Path | Description |
|--------|------|-------------|
| GET | /taxes/{id}.json | Retrieve a single Tax information. |

### partners
| Method | Path | Description |
|--------|------|-------------|
| GET | /partners/stores.json | Retrieve statistics. |
| GET | /partners/subscriptions.json | Retrieve subscriptions and transactions. |

### carts
| Method | Path | Description |
|--------|------|-------------|
| GET | /carts/{id}.json | Obtain information for a cart. |

### documents.json
| Method | Path | Description |
|--------|------|-------------|
| GET | /documents.json | Retrieve all Documents from a Store. |

### transaction_ledger
| Method | Path | Description |
|--------|------|-------------|
| GET | /transaction_ledger/balance.json | Store Balance |

### products_locations
| Method | Path | Description |
|--------|------|-------------|
| GET | /products_locations | Stock by Product and Location |
| PUT | /products_locations | Update Stock by Product and Location |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all info.json?" -> GET /store/info.json
- "List all languages.json?" -> GET /store/languages.json
- "List all hooks.json?" -> GET /hooks.json
- "Create a hooks.json?" -> POST /hooks.json
- "Get hook details?" -> GET /hooks/{id}.json
- "Update a hook?" -> PUT /hooks/{id}.json
- "Delete a hook?" -> DELETE /hooks/{id}.json
- "List all jsapps.json?" -> GET /jsapps.json
- "Create a jsapps.json?" -> POST /jsapps.json
- "Get jsapp details?" -> GET /jsapps/{code}.json
- "Delete a jsapp?" -> DELETE /jsapps/{code}.json
- "List all install_status.json?" -> GET /apps/{code}/install_status.json
- "List all install_status_by_store_id.json?" -> GET /apps/{code}/install_status_by_store_id.json
- "List all billing_cycle_dates.json?" -> GET /apps/{code}/billing_cycle_dates.json
- "List all billing_cycle_orders.json?" -> GET /apps/{code}/billing_cycle_orders.json
- "List all check_billing_cycle_order.json?" -> GET /apps/{code}/check_billing_cycle_order.json
- "List all products.json?" -> GET /products.json
- "Create a products.json?" -> POST /products.json
- "List all count.json?" -> GET /products/count.json
- "Get after details?" -> GET /products/after/{id}.json
- "Get status details?" -> GET /products/status/{status}.json
- "Get category details?" -> GET /products/category/{category_id}.json
- "List all count.json?" -> GET /products/status/{status}/count.json
- "List all count.json?" -> GET /products/category/{category_id}/count.json
- "List all reviews.json?" -> GET /products/{id}/reviews.json
- "Get review details?" -> GET /products/reviews/{review_id}.json
- "List all reviews.json?" -> GET /products/reviews.json
- "Get product details?" -> GET /products/{id}.json
- "Update a product?" -> PUT /products/{id}.json
- "Delete a product?" -> DELETE /products/{id}.json
- "Search search.json?" -> GET /products/search.json
- "List all options.json?" -> GET /products/{id}/options.json
- "Create a options.json?" -> POST /products/{id}/options.json
- "List all count.json?" -> GET /products/{id}/options/count.json
- "Get option details?" -> GET /products/{id}/options/{option_id}.json
- "Update a option?" -> PUT /products/{id}/options/{option_id}.json
- "Delete a option?" -> DELETE /products/{id}/options/{option_id}.json
- "List all values.json?" -> GET /products/{id}/options/{option_id}/values.json
- "Create a values.json?" -> POST /products/{id}/options/{option_id}/values.json
- "List all count.json?" -> GET /products/{id}/options/{option_id}/values/count.json
- "Get value details?" -> GET /products/{id}/options/{option_id}/values/{value_id}.json
- "Update a value?" -> PUT /products/{id}/options/{option_id}/values/{value_id}.json
- "Delete a value?" -> DELETE /products/{id}/options/{option_id}/values/{value_id}.json
- "Get variant details?" -> GET /products/{id}/variants/{variant_id}.json
- "Update a variant?" -> PUT /products/{id}/variants/{variant_id}.json
- "List all variants.json?" -> GET /products/{id}/variants.json
- "Create a variants.json?" -> POST /products/{id}/variants.json
- "List all count.json?" -> GET /products/{id}/variants/count.json
- "List all images.json?" -> GET /products/{id}/images.json
- "Create a images.json?" -> POST /products/{id}/images.json
- "Update a image?" -> PUT /products/{product_id}/images/{image_id}.json
- "List all count.json?" -> GET /products/{id}/images/count.json
- "Get image details?" -> GET /products/{id}/images/{image_id}.json
- "Delete a image?" -> DELETE /products/{id}/images/{image_id}.json
- "List all attachments.json?" -> GET /products/{id}/attachments.json
- "Create a attachments.json?" -> POST /products/{id}/attachments.json
- "List all count.json?" -> GET /products/{id}/attachments/count.json
- "Get attachment details?" -> GET /products/{id}/attachments/{attachment_id}.json
- "Delete a attachment?" -> DELETE /products/{id}/attachments/{attachment_id}.json
- "List all digital_products.json?" -> GET /products/{id}/digital_products.json
- "Create a digital_products.json?" -> POST /products/{id}/digital_products.json
- "List all count.json?" -> GET /products/{id}/digital_products/count.json
- "Get digital_product details?" -> GET /products/{id}/digital_products/{digital_product_id}.json
- "Delete a digital_product?" -> DELETE /products/{id}/digital_products/{digital_product_id}.json
- "List all fields.json?" -> GET /products/{id}/fields.json
- "Create a fields.json?" -> POST /products/{id}/fields.json
- "List all count.json?" -> GET /products/{id}/fields/count.json
- "Update a field?" -> PUT /products/{product_id}/fields/{field_id}.json
- "Delete a field?" -> DELETE /products/{product_id}/fields/{field_id}.json
- "List all categories.json?" -> GET /categories.json
- "Create a categories.json?" -> POST /categories.json
- "List all count.json?" -> GET /categories/count.json
- "Get category details?" -> GET /categories/{id}.json
- "Update a category?" -> PUT /categories/{id}.json
- "Delete a category?" -> DELETE /categories/{id}.json
- "List all orders.json?" -> GET /orders.json
- "Create a orders.json?" -> POST /orders.json
- "List all count.json?" -> GET /orders/count.json
- "Get status details?" -> GET /orders/status/{status}.json
- "Get order details?" -> GET /orders/{id}.json
- "Update a order?" -> PUT /orders/{id}.json
- "Search search.json?" -> GET /orders/search.json
- "Get after details?" -> GET /orders/after/{id}.json
- "List all history.json?" -> GET /orders/{id}/history.json
- "Create a history.json?" -> POST /orders/{id}/history.json
- "List all documents.json?" -> GET /orders/{id}/documents.json
- "Create a documents.json?" -> POST /orders/{id}/documents.json
- "Update a document?" -> PUT /orders/{id}/documents/{public_id}.json
- "Delete a document?" -> DELETE /orders/{id}/documents/{public_id}.json
- "List all count.json?" -> GET /fulfillments/count.json
- "Create a rates.json?" -> POST /fulfillments/rates.json
- "List all fulfillments.json?" -> GET /fulfillments.json
- "Create a fulfillments.json?" -> POST /fulfillments.json
- "List all label.json?" -> GET /fulfillments/{id}/label.json
- "Get fulfillment details?" -> GET /fulfillments/{id}.json
- "Update a fulfillment?" -> PUT /fulfillments/{id}.json
- "List all fulfillments.json?" -> GET /order/{id}/fulfillments.json
- "List all pages.json?" -> GET /pages.json
- "Create a pages.json?" -> POST /pages.json
- "List all count.json?" -> GET /pages/count.json
- "Get page details?" -> GET /pages/{id}.json
- "Update a page?" -> PUT /pages/{id}.json
- "Delete a page?" -> DELETE /pages/{id}.json
- "List all images.json?" -> GET /pages/{id}/images.json
- "Create a images.json?" -> POST /pages/{id}/images.json
- "List all count.json?" -> GET /pages/{id}/images/count.json
- "Get image details?" -> GET /pages/{id}/images/{image_id}.json
- "Update a image?" -> PUT /pages/{id}/images/{image_id}.json
- "Delete a image?" -> DELETE /pages/{id}/images/{image_id}.json
- "List all customers.json?" -> GET /customers.json
- "Create a customers.json?" -> POST /customers.json
- "List all count.json?" -> GET /customers/count.json
- "Get email details?" -> GET /customers/email/{email}.json
- "List all orders.json?" -> GET /customers/{id}/orders.json
- "Get status details?" -> GET /customers/{id}/orders/status/{status}.json
- "Get customer details?" -> GET /customers/{id}.json
- "Update a customer?" -> PUT /customers/{id}.json
- "Delete a customer?" -> DELETE /customers/{id}.json
- "Search search.json?" -> GET /customers/search.json
- "List all customer_categories.json?" -> GET /customer_categories.json
- "Create a customer_categories.json?" -> POST /customer_categories.json
- "Get customer_category details?" -> GET /customer_categories/{id}.json
- "Update a customer_category?" -> PUT /customer_categories/{id}.json
- "Delete a customer_category?" -> DELETE /customer_categories/{id}.json
- "List all customers.json?" -> GET /customer_categories/{id}/customers.json
- "Create a customers.json?" -> POST /customer_categories/{id}/customers.json
- "Delete a customer?" -> DELETE /customer_categories/{id}/customers/{customer_id}.json
- "List all fields?" -> GET /customers/{id}/fields
- "Create a field?" -> POST /customers/{id}/fields
- "Get field details?" -> GET /customers/{id}/fields/{field_id}
- "Update a field?" -> PUT /customers/{id}/fields/{field_id}
- "Delete a field?" -> DELETE /customers/{id}/fields/{field_id}
- "List all promotions.json?" -> GET /promotions.json
- "Create a promotions.json?" -> POST /promotions.json
- "Get promotion details?" -> GET /promotions/{id}.json
- "Update a promotion?" -> PUT /promotions/{id}.json
- "Delete a promotion?" -> DELETE /promotions/{id}.json
- "List all payment_methods.json?" -> GET /payment_methods.json
- "Create a payment_methods.json?" -> POST /payment_methods.json
- "Get payment_method details?" -> GET /payment_methods/{id}.json
- "List all shipping_methods.json?" -> GET /shipping_methods.json
- "Create a shipping_methods.json?" -> POST /shipping_methods.json
- "Get shipping_method details?" -> GET /shipping_methods/{id}.json
- "Update a shipping_method?" -> PUT /shipping_methods/{id}.json
- "Delete a shipping_method?" -> DELETE /shipping_methods/{id}.json
- "List all locations.json?" -> GET /locations.json
- "Create a locations.json?" -> POST /locations.json
- "Get location details?" -> GET /locations/{id}.json
- "Update a location?" -> PUT /locations/{id}.json
- "Delete a location?" -> DELETE /locations/{id}.json
- "List all custom_fields.json?" -> GET /custom_fields.json
- "Create a custom_fields.json?" -> POST /custom_fields.json
- "Get custom_field details?" -> GET /custom_fields/{id}.json
- "Update a custom_field?" -> PUT /custom_fields/{id}.json
- "Delete a custom_field?" -> DELETE /custom_fields/{id}.json
- "List all select_options.json?" -> GET /custom_fields/{id}/select_options.json
- "Create a select_options.json?" -> POST /custom_fields/{id}/select_options.json
- "Get select_option details?" -> GET /custom_fields/{id}/select_options/{custom_field_select_option_id}.json
- "Update a select_option?" -> PUT /custom_fields/{id}/select_options/{custom_field_select_option_id}.json
- "Delete a select_option?" -> DELETE /custom_fields/{id}/select_options/{custom_field_select_option_id}.json
- "List all checkout_custom_fields.json?" -> GET /checkout_custom_fields.json
- "Create a checkout_custom_fields.json?" -> POST /checkout_custom_fields.json
- "Get checkout_custom_field details?" -> GET /checkout_custom_fields/{id}.json
- "Update a checkout_custom_field?" -> PUT /checkout_custom_fields/{id}.json
- "Delete a checkout_custom_field?" -> DELETE /checkout_custom_fields/{id}.json
- "List all countries.json?" -> GET /countries.json
- "Get country details?" -> GET /countries/{country_code}.json
- "List all regions.json?" -> GET /countries/{country_code}/regions.json
- "List all municipalities.json?" -> GET /countries/{country_code}/regions/{region_code}/municipalities.json
- "Get region details?" -> GET /countries/{country_code}/regions/{region_code}.json
- "List all taxes.json?" -> GET /taxes.json
- "Create a taxes.json?" -> POST /taxes.json
- "Get taxe details?" -> GET /taxes/{id}.json
- "Create a create.json?" -> POST /store/create.json
- "List all check_status.json?" -> GET /store/check_status.json
- "List all stores.json?" -> GET /partners/stores.json
- "List all subscriptions.json?" -> GET /partners/subscriptions.json
- "Get cart details?" -> GET /carts/{id}.json
- "List all documents.json?" -> GET /documents.json
- "List all balance.json?" -> GET /transaction_ledger/balance.json
- "List all products_locations?" -> GET /products_locations
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
