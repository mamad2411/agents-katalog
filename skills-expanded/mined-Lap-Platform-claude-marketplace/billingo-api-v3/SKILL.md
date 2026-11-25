---
name: billingo-api-v3
description: "Billingo API v3 API skill. Use when working with Billingo API v3 for bank-accounts, currencies, document-blocks. Covers 31 endpoints."
version: 1.0.0
generator: lapsh
---

# Billingo API v3
API version: 3.0.7

## Auth
ApiKey X-API-KEY in header

## Base URL
https://api.billingo.hu/v3

## Setup
1. Set your API key in the appropriate header
2. GET /bank-accounts -- verify access
3. POST /bank-accounts -- create first bank-accounts

## Endpoints

31 endpoints across 8 groups. See references/api-spec.lap for full details.

### bank-accounts
| Method | Path | Description |
|--------|------|-------------|
| GET | /bank-accounts | List all bank account |
| POST | /bank-accounts | Create a bank account |
| GET | /bank-accounts/{id} | Retrieve a bank account |
| PUT | /bank-accounts/{id} | Update a bank account |
| DELETE | /bank-accounts/{id} | Delete a bank account |

### currencies
| Method | Path | Description |
|--------|------|-------------|
| GET | /currencies | Get currencies exchange rate. |

### document-blocks
| Method | Path | Description |
|--------|------|-------------|
| GET | /document-blocks | List all document blocks |

### documents
| Method | Path | Description |
|--------|------|-------------|
| GET | /documents | List all documents |
| POST | /documents | Create a document |
| GET | /documents/{id} | Retrieve a document |
| POST | /documents/{id}/cancel | Cancel a document |
| POST | /documents/{id}/create-from-proforma | Create a document from proforma. |
| GET | /documents/{id}/download | Download a document in PDF format. |
| GET | /documents/{id}/online-szamla | Retrieve a document Online Számla status |
| GET | /documents/{id}/payments | Retrieve a payment histroy |
| PUT | /documents/{id}/payments | Update payment history |
| DELETE | /documents/{id}/payments | Delete all payment history on document |
| GET | /documents/{id}/public-url | Retrieve a document download public url. |
| POST | /documents/{id}/send | Send invoice to given email adresses. |

### organization
| Method | Path | Description |
|--------|------|-------------|
| GET | /organization | Retrieve a organization data. |

### partners
| Method | Path | Description |
|--------|------|-------------|
| GET | /partners | List all partners |
| POST | /partners | Create a partner |
| GET | /partners/{id} | Retrieve a partner |
| PUT | /partners/{id} | Update a partner |
| DELETE | /partners/{id} | Delete a partner |

### products
| Method | Path | Description |
|--------|------|-------------|
| GET | /products | List all product |
| POST | /products | Create a product |
| GET | /products/{id} | Retrieve a product |
| PUT | /products/{id} | Update a product |
| DELETE | /products/{id} | Delete a product |

### utils
| Method | Path | Description |
|--------|------|-------------|
| GET | /utils/convert-legacy-id/{id} | Convert legacy ID to v3 ID. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all bank-accounts?" -> GET /bank-accounts
- "Create a bank-account?" -> POST /bank-accounts
- "Get bank-account details?" -> GET /bank-accounts/{id}
- "Update a bank-account?" -> PUT /bank-accounts/{id}
- "Delete a bank-account?" -> DELETE /bank-accounts/{id}
- "List all currencies?" -> GET /currencies
- "List all document-blocks?" -> GET /document-blocks
- "List all documents?" -> GET /documents
- "Create a document?" -> POST /documents
- "Get document details?" -> GET /documents/{id}
- "Create a cancel?" -> POST /documents/{id}/cancel
- "Create a create-from-proforma?" -> POST /documents/{id}/create-from-proforma
- "List all download?" -> GET /documents/{id}/download
- "List all online-szamla?" -> GET /documents/{id}/online-szamla
- "List all payments?" -> GET /documents/{id}/payments
- "List all public-url?" -> GET /documents/{id}/public-url
- "Create a send?" -> POST /documents/{id}/send
- "List all organization?" -> GET /organization
- "List all partners?" -> GET /partners
- "Create a partner?" -> POST /partners
- "Get partner details?" -> GET /partners/{id}
- "Update a partner?" -> PUT /partners/{id}
- "Delete a partner?" -> DELETE /partners/{id}
- "List all products?" -> GET /products
- "Create a product?" -> POST /products
- "Get product details?" -> GET /products/{id}
- "Update a product?" -> PUT /products/{id}
- "Delete a product?" -> DELETE /products/{id}
- "Get convert-legacy-id details?" -> GET /utils/convert-legacy-id/{id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
