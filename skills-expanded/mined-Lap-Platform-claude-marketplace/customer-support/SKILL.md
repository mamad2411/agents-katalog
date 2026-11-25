---
name: customer-support
description: "Customer Support API skill. Use when working with Customer Support for customer-support. Covers 5 endpoints."
version: 1.0.0
generator: lapsh
---

# Customer Support
API version: 9.5.0

## Auth
ApiKey Authorization in header

## Base URL
https://unify.apideck.com

## Setup
1. Set your API key in the appropriate header
2. GET /customer-support/customers -- verify access
3. POST /customer-support/customers -- create first customers

## Endpoints

5 endpoints across 1 groups. See references/api-spec.lap for full details.

### customer-support
| Method | Path | Description |
|--------|------|-------------|
| GET | /customer-support/customers | List Customer Support Customers |
| POST | /customer-support/customers | Create Customer Support Customer |
| GET | /customer-support/customers/{id} | Get Customer Support Customer |
| PATCH | /customer-support/customers/{id} | Update Customer Support Customer |
| DELETE | /customer-support/customers/{id} | Delete Customer Support Customer |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all customers?" -> GET /customer-support/customers
- "Create a customer?" -> POST /customer-support/customers
- "Get customer details?" -> GET /customer-support/customers/{id}
- "Partially update a customer?" -> PATCH /customer-support/customers/{id}
- "Delete a customer?" -> DELETE /customer-support/customers/{id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
