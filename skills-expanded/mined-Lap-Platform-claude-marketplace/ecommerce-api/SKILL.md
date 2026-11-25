---
name: ecommerce-api
description: "Ecommerce API skill. Use when working with Ecommerce for ecommerce. Covers 7 endpoints."
version: 1.0.0
generator: lapsh
---

# Ecommerce API
API version: 10.24.0

## Auth
ApiKey Authorization in header

## Base URL
https://unify.apideck.com

## Setup
1. Set your API key in the appropriate header
2. GET /ecommerce/orders -- verify access

## Endpoints

7 endpoints across 1 groups. See references/api-spec.lap for full details.

### ecommerce
| Method | Path | Description |
|--------|------|-------------|
| GET | /ecommerce/orders | List Orders |
| GET | /ecommerce/orders/{id} | Get Order |
| GET | /ecommerce/products | List Products |
| GET | /ecommerce/products/{id} | Get Product |
| GET | /ecommerce/customers | List Customers |
| GET | /ecommerce/customers/{id} | Get Customer |
| GET | /ecommerce/store | Get Store |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all orders?" -> GET /ecommerce/orders
- "Get order details?" -> GET /ecommerce/orders/{id}
- "List all products?" -> GET /ecommerce/products
- "Get product details?" -> GET /ecommerce/products/{id}
- "List all customers?" -> GET /ecommerce/customers
- "Get customer details?" -> GET /ecommerce/customers/{id}
- "List all store?" -> GET /ecommerce/store
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
