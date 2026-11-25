---
name: invoices
description: "Invoices API skill. Use when working with Invoices for invoicing. Covers 22 endpoints."
version: 1.0.0
generator: lapsh
---

# Invoices
API version: 2.6

## Auth
OAuth2

## Base URL
https://api-m.sandbox.paypal.com

## Setup
1. Configure auth: OAuth2
2. GET /v2/invoicing/invoices -- verify access
3. POST /v2/invoicing/invoices -- create first invoices

## Endpoints

22 endpoints across 1 groups. See references/api-spec.lap for full details.

### invoicing
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/invoicing/invoices | Create draft invoice |
| GET | /v2/invoicing/invoices | List invoices |
| POST | /v2/invoicing/invoices/{invoice_id}/send | Send invoice |
| POST | /v2/invoicing/invoices/{invoice_id}/remind | Send invoice reminder |
| POST | /v2/invoicing/invoices/{invoice_id}/cancel | Cancel sent invoice |
| POST | /v2/invoicing/invoices/{invoice_id}/payments | Record payment for invoice |
| DELETE | /v2/invoicing/invoices/{invoice_id}/payments/{transaction_id} | Delete external payment |
| POST | /v2/invoicing/invoices/{invoice_id}/refunds | Record refund for invoice |
| DELETE | /v2/invoicing/invoices/{invoice_id}/refunds/{transaction_id} | Delete external refund |
| POST | /v2/invoicing/invoices/{invoice_id}/generate-qr-code | Generate QR code |
| POST | /v2/invoicing/generate-next-invoice-number | Generate invoice number |
| GET | /v2/invoicing/invoices/{invoice_id} | Show invoice details |
| PUT | /v2/invoicing/invoices/{invoice_id} | Fully update invoice |
| DELETE | /v2/invoicing/invoices/{invoice_id} | Delete invoice |
| POST | /v2/invoicing/search-invoices | Search for invoices |
| GET | /v2/invoicing/templates | List templates |
| POST | /v2/invoicing/templates | Create template |
| GET | /v2/invoicing/templates/{template_id} | Show template details |
| PUT | /v2/invoicing/templates/{template_id} | Fully update template |
| DELETE | /v2/invoicing/templates/{template_id} | Delete template |
| GET | /v2/invoicing/accounting-sync/merchant/connections | List Connections. |
| GET | /v2/invoicing/accounting-sync/invoices/{id}/connections | List Connection Status for an Invoice. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a invoice?" -> POST /v2/invoicing/invoices
- "List all invoices?" -> GET /v2/invoicing/invoices
- "Create a send?" -> POST /v2/invoicing/invoices/{invoice_id}/send
- "Create a remind?" -> POST /v2/invoicing/invoices/{invoice_id}/remind
- "Create a cancel?" -> POST /v2/invoicing/invoices/{invoice_id}/cancel
- "Create a payment?" -> POST /v2/invoicing/invoices/{invoice_id}/payments
- "Delete a payment?" -> DELETE /v2/invoicing/invoices/{invoice_id}/payments/{transaction_id}
- "Create a refund?" -> POST /v2/invoicing/invoices/{invoice_id}/refunds
- "Delete a refund?" -> DELETE /v2/invoicing/invoices/{invoice_id}/refunds/{transaction_id}
- "Create a generate-qr-code?" -> POST /v2/invoicing/invoices/{invoice_id}/generate-qr-code
- "Create a generate-next-invoice-number?" -> POST /v2/invoicing/generate-next-invoice-number
- "Get invoice details?" -> GET /v2/invoicing/invoices/{invoice_id}
- "Update a invoice?" -> PUT /v2/invoicing/invoices/{invoice_id}
- "Delete a invoice?" -> DELETE /v2/invoicing/invoices/{invoice_id}
- "Create a search-invoice?" -> POST /v2/invoicing/search-invoices
- "List all templates?" -> GET /v2/invoicing/templates
- "Create a template?" -> POST /v2/invoicing/templates
- "Get template details?" -> GET /v2/invoicing/templates/{template_id}
- "Update a template?" -> PUT /v2/invoicing/templates/{template_id}
- "Delete a template?" -> DELETE /v2/invoicing/templates/{template_id}
- "List all connections?" -> GET /v2/invoicing/accounting-sync/merchant/connections
- "List all connections?" -> GET /v2/invoicing/accounting-sync/invoices/{id}/connections
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
