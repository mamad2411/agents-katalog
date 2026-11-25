---
name: storecove-api
description: "Storecove API skill. Use when working with Storecove for invoice_submissions, document_submissions, legal_entities. Covers 37 endpoints."
version: 1.0.0
generator: lapsh
---

# Storecove API
API version: 2.0.1

## Auth
ApiKey Authorization in header

## Base URL
https://api.storecove.com/api/v2

## Setup
1. Set your API key in the appropriate header
2. GET /webhook_instances/ -- verify access
3. POST /invoice_submissions -- create first invoice_submissions

## Endpoints

37 endpoints across 8 groups. See references/api-spec.lap for full details.

### invoice_submissions
| Method | Path | Description |
|--------|------|-------------|
| GET | /invoice_submissions/{guid}/evidence | DEPRECATED. Get InvoiceSubmission Evidence |
| POST | /invoice_submissions | DEPRECATED. Submit a new invoice |
| POST | /invoice_submissions/preflight | DEPRECATED. Preflight an invoice recipient |

### document_submissions
| Method | Path | Description |
|--------|------|-------------|
| POST | /document_submissions | Submit a new document. |
| GET | /document_submissions/{guid}/evidence/{evidence_type} | Get DocumentSubmission Evidence |

### legal_entities
| Method | Path | Description |
|--------|------|-------------|
| POST | /legal_entities | Create a new LegalEntity |
| GET | /legal_entities/{id} | Get LegalEntity |
| DELETE | /legal_entities/{id} | Delete LegalEntity |
| PATCH | /legal_entities/{id} | Update LegalEntity |
| POST | /legal_entities/{legal_entity_id}/peppol_identifiers | Create a new PeppolIdentifier |
| DELETE | /legal_entities/{legal_entity_id}/peppol_identifiers/{superscheme}/{scheme}/{identifier} | Delete PeppolIdentifier |
| POST | /legal_entities/{legal_entity_id}/administrations | DEPRECATED. Create a new Administration |
| GET | /legal_entities/{legal_entity_id}/administrations/{id} | DEPRECATED. Get Administration |
| DELETE | /legal_entities/{legal_entity_id}/administrations/{id} | DEPRECATED. Delete Administration |
| PATCH | /legal_entities/{legal_entity_id}/administrations/{id} | DEPRECATED. Update Administration |
| POST | /legal_entities/{legal_entity_id}/additional_tax_identifiers | Create a new AdditionalTaxIdentifier |
| GET | /legal_entities/{legal_entity_id}/additional_tax_identifiers/{id} | Get AdditionalTaxIdentifier |
| DELETE | /legal_entities/{legal_entity_id}/additional_tax_identifiers/{id} | Delete AdditionalTaxIdentifier |
| PATCH | /legal_entities/{legal_entity_id}/additional_tax_identifiers/{id} | Update AdditionalTaxIdentifier |
| POST | /legal_entities/{legal_entity_id}/received_documents | Receive a new Document |

### purchase_invoices
| Method | Path | Description |
|--------|------|-------------|
| GET | /purchase_invoices/{guid} | DEPRECATED. Get Purchase invoice data as JSON |
| GET | /purchase_invoices/{guid}/{packaging} | DEPRECATED. Get Purchase invoice data in a selectable format |
| GET | /purchase_invoices/{guid}/{packaging}/{package_version} | DEPRECATED. Get Purchase invoice data as JSON with a Base64-encoded UBL string in the specified version |

### webhook_instances
| Method | Path | Description |
|--------|------|-------------|
| GET | /webhook_instances/ | GET a WebhookInstance |
| DELETE | /webhook_instances/{guid} | DELETE a WebhookInstance |

### discovery
| Method | Path | Description |
|--------|------|-------------|
| POST | /discovery/receives | Discover Network Participant Capabilites |
| POST | /discovery/exists | Discover Network Participant Existence |
| GET | /discovery/identifiers | Discover Country Identifiers ** EXPERIMENTAL |

### received_documents
| Method | Path | Description |
|--------|------|-------------|
| GET | /received_documents/{guid}/{format} | Get a new ReceivedDocument |

### api
| Method | Path | Description |
|--------|------|-------------|
| POST | /api/v2/legal_entities/{legal_entity_id}/c5/iras/email/activate | Request a new C5 Email Activation |
| POST | /api/v2/legal_entities/{legal_entity_id}/c5/iras/email/deactivate | Request a new C5 Email Deactivation |
| PUT | /api/v2/legal_entities/{legal_entity_id}/c5/iras/email/cancel | Cancel a C5 email activation or deactivation |
| POST | /api/v2/legal_entities/{legal_entity_id}/c5/iras/redirect/activate | Request a new C5 Redirect Activation |
| POST | /api/v2/legal_entities/{legal_entity_id}/c5/iras/redirect/deactivate | Request a new C5 Redirect Deactivation |
| PUT | /api/v2/legal_entities/{legal_entity_id}/c5/iras/redirect/cancel | Cancel a C5 redirect activation or deactivation |
| POST | /api/v2/legal_entities/{legal_entity_id}/c5_activation/activate | DEPRECATED. Request a new C5 Activation |
| POST | /api/v2/legal_entities/{legal_entity_id}/c5_deactivation/deactivate | DEPRECATED. Request a new C5 Deactivation |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all evidence?" -> GET /invoice_submissions/{guid}/evidence
- "Create a invoice_submission?" -> POST /invoice_submissions
- "Create a document_submission?" -> POST /document_submissions
- "Get evidence details?" -> GET /document_submissions/{guid}/evidence/{evidence_type}
- "Create a preflight?" -> POST /invoice_submissions/preflight
- "Create a legal_entity?" -> POST /legal_entities
- "Get legal_entity details?" -> GET /legal_entities/{id}
- "Delete a legal_entity?" -> DELETE /legal_entities/{id}
- "Partially update a legal_entity?" -> PATCH /legal_entities/{id}
- "Create a peppol_identifier?" -> POST /legal_entities/{legal_entity_id}/peppol_identifiers
- "Delete a peppol_identifier?" -> DELETE /legal_entities/{legal_entity_id}/peppol_identifiers/{superscheme}/{scheme}/{identifier}
- "Create a administration?" -> POST /legal_entities/{legal_entity_id}/administrations
- "Get administration details?" -> GET /legal_entities/{legal_entity_id}/administrations/{id}
- "Delete a administration?" -> DELETE /legal_entities/{legal_entity_id}/administrations/{id}
- "Partially update a administration?" -> PATCH /legal_entities/{legal_entity_id}/administrations/{id}
- "Create a additional_tax_identifier?" -> POST /legal_entities/{legal_entity_id}/additional_tax_identifiers
- "Get additional_tax_identifier details?" -> GET /legal_entities/{legal_entity_id}/additional_tax_identifiers/{id}
- "Delete a additional_tax_identifier?" -> DELETE /legal_entities/{legal_entity_id}/additional_tax_identifiers/{id}
- "Partially update a additional_tax_identifier?" -> PATCH /legal_entities/{legal_entity_id}/additional_tax_identifiers/{id}
- "Get purchase_invoice details?" -> GET /purchase_invoices/{guid}
- "Get purchase_invoice details?" -> GET /purchase_invoices/{guid}/{packaging}
- "Get purchase_invoice details?" -> GET /purchase_invoices/{guid}/{packaging}/{package_version}
- "List all webhook_instances?" -> GET /webhook_instances/
- "Delete a webhook_instance?" -> DELETE /webhook_instances/{guid}
- "Create a receive?" -> POST /discovery/receives
- "Create a exist?" -> POST /discovery/exists
- "List all identifiers?" -> GET /discovery/identifiers
- "Create a received_document?" -> POST /legal_entities/{legal_entity_id}/received_documents
- "Get received_document details?" -> GET /received_documents/{guid}/{format}
- "Create a activate?" -> POST /api/v2/legal_entities/{legal_entity_id}/c5/iras/email/activate
- "Create a deactivate?" -> POST /api/v2/legal_entities/{legal_entity_id}/c5/iras/email/deactivate
- "Create a activate?" -> POST /api/v2/legal_entities/{legal_entity_id}/c5/iras/redirect/activate
- "Create a deactivate?" -> POST /api/v2/legal_entities/{legal_entity_id}/c5/iras/redirect/deactivate
- "Create a activate?" -> POST /api/v2/legal_entities/{legal_entity_id}/c5_activation/activate
- "Create a deactivate?" -> POST /api/v2/legal_entities/{legal_entity_id}/c5_deactivation/deactivate
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
