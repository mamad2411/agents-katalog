---
name: customers-v3
description: "Customers V3 API skill. Use when working with Customers V3 for customers. Covers 34 endpoints."
version: 1.0.0
generator: lapsh
---

# Customers V3

## Auth
ApiKey X-Auth-Token in header

## Base URL
https://api.bigcommerce.com/stores/{store_hash}/v3

## Setup
1. Set your API key in the appropriate header
2. GET /customers -- verify access
3. POST /customers -- create first customers

## Endpoints

34 endpoints across 1 groups. See references/api-spec.lap for full details.

### customers
| Method | Path | Description |
|--------|------|-------------|
| GET | /customers | Get All Customers |
| POST | /customers | Create Customers |
| PUT | /customers | Update Customers |
| DELETE | /customers | Delete Customers |
| GET | /customers/addresses | Get All Customer Addresses |
| POST | /customers/addresses | Create a Customer Address |
| PUT | /customers/addresses | Update a Customer Address |
| DELETE | /customers/addresses | Delete a Customer Address |
| POST | /customers/validate-credentials | Validate a customer credentials |
| GET | /customers/settings | Get Customer Settings |
| PUT | /customers/settings | Update Customer Settings |
| GET | /customers/settings/channels/{channel_id} | Get Customer Settings per Channel |
| PUT | /customers/settings/channels/{channel_id} | Update Customer Settings per Channel |
| GET | /customers/attributes | Get All Customer Attributes |
| POST | /customers/attributes | Create a Customer Attribute |
| PUT | /customers/attributes | Update a Customer Attribute |
| DELETE | /customers/attributes | Delete Customer Attributes |
| GET | /customers/attribute-values | Get All Customer Attribute Values |
| PUT | /customers/attribute-values | Upsert Customer Attribute Values |
| DELETE | /customers/attribute-values | Delete Customer Attribute Values |
| GET | /customers/form-field-values | Get Customer Form Field Values |
| PUT | /customers/form-field-values | Upsert Customer Form Field Values (Deprecated) |
| GET | /customers/{customerId}/consent | Get Customer Consent |
| PUT | /customers/{customerId}/consent | Update Customer Consent |
| GET | /customers/{customerId}/stored-instruments | Get Stored Instruments |
| GET | /customers/{customerId}/metafields | Get Customer Metafields |
| POST | /customers/{customerId}/metafields | Create Customer Metafields |
| GET | /customers/{customerId}/metafields/{metafieldId} | Get a Customer Metafield |
| PUT | /customers/{customerId}/metafields/{metafieldId} | Update a Metafield |
| DELETE | /customers/{customerId}/metafields/{metafieldId} | Delete a Customer Metafield |
| GET | /customers/metafields | Get All Customer Metafields |
| POST | /customers/metafields | Create Multiple Metafields |
| PUT | /customers/metafields | Update Multiple Metafields |
| DELETE | /customers/metafields | Delete Multiple Metafields |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all customers?" -> GET /customers
- "Create a customer?" -> POST /customers
- "List all addresses?" -> GET /customers/addresses
- "Create a address?" -> POST /customers/addresses
- "Create a validate-credential?" -> POST /customers/validate-credentials
- "List all settings?" -> GET /customers/settings
- "Get channel details?" -> GET /customers/settings/channels/{channel_id}
- "Update a channel?" -> PUT /customers/settings/channels/{channel_id}
- "List all attributes?" -> GET /customers/attributes
- "Create a attribute?" -> POST /customers/attributes
- "List all attribute-values?" -> GET /customers/attribute-values
- "List all form-field-values?" -> GET /customers/form-field-values
- "List all consent?" -> GET /customers/{customerId}/consent
- "List all stored-instruments?" -> GET /customers/{customerId}/stored-instruments
- "List all metafields?" -> GET /customers/{customerId}/metafields
- "Create a metafield?" -> POST /customers/{customerId}/metafields
- "Get metafield details?" -> GET /customers/{customerId}/metafields/{metafieldId}
- "Update a metafield?" -> PUT /customers/{customerId}/metafields/{metafieldId}
- "Delete a metafield?" -> DELETE /customers/{customerId}/metafields/{metafieldId}
- "List all metafields?" -> GET /customers/metafields
- "Create a metafield?" -> POST /customers/metafields
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
