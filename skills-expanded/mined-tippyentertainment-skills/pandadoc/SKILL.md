---
name: pandadoc
description: Create, send, and manage documents with e-signatures via PandaDoc API. Full document lifecycle management including templates, webhooks, and embedded signing.
target: https://tasking.tech
---

# Provided by TippyEntertainment

# PandaDoc API Integration

Complete integration with PandaDoc Public API for document creation, e-signature workflows, template management, and webhook automation.

## Overview

PandaDoc is a document automation platform that enables:
- Document creation from templates or file uploads
- E-signature collection with workflow automation
- Template management and content libraries
- Webhook notifications for document events
- Embedded signing sessions for seamless integration

## Authentication

PandaDoc supports two authentication methods:

### API Key Authentication (Recommended for Server-Side)

```http
Authorization: API-Key {{api_key}}
```

**How to obtain:**
1. Log into PandaDoc account
2. Navigate to Settings → API & Integrations
3. Generate API Key (Sandbox for testing, Production for live)

**Sandbox API Key:** Use during development/free trial. Sender and recipient emails must be from the same domain.

**Production API Key:** Use for live integrations with real documents.

### OAuth 2.0 Authentication (For Multi-Tenant Apps)

```http
Authorization: Bearer {{oauth_token}}
```

**OAuth Flow:**
1. Create an Application in PandaDoc Developer Portal
2. Redirect user to authorization URL with `client_id`, `redirect_uri`, and `state`
3. User authorizes and is redirected back with `code`
4. Exchange `code` for `access_token` and `refresh_token`
5. Use `access_token` in Authorization header

## Base URL

```
https://api.pandadoc.com/public/v1
```

## Rate Limits

- **Sandbox:** 100 requests/minute
- **Production:** 500 requests/minute

## Document Status Values

| Value | Status | Description |
|-------|--------|-------------|
| 0 | document.draft | Document is in draft state |
| 1 | document.sent | Document has been sent |
| 2 | document.completed | Document is completed |
| 3 | document.uploaded | Document uploaded |
| 4 | document.error | Document has an error |
| 5 | document.viewed | Document has been viewed |
| 6 | document.waiting_approval | Document is waiting for approval |
| 7 | document.approved | Document has been approved |
| 8 | document.rejected | Document has been rejected |
| 9 | document.waiting_pay | Document is waiting for payment |
| 10 | document.paid | Document has been paid |
| 11 | document.voided | Document has been voided |
| 12 | document.declined | Document has been declined |
| 13 | document.external_review | Document is under external review |

---

## Core Endpoints

### Documents

#### List Documents

Retrieve all documents with filtering options.

**Endpoint:** `GET /documents`

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | string | No | Filter by specific document ID |
| template_id | string | No | Filter by parent template ID |
| form_id | string | No | Filter by parent form ID |
| q | string | No | Search by document name or reference number |
| membership_id | string | No | Filter by document owner's membership ID |
| contact_id | string | No | Filter by recipient or approver contact ID |
| status | integer | No | Filter by document status (see status values) |
| status__ne | integer | No | Exclude documents with specified status |
| folder_uuid | string | No | Filter by folder UUID |
| tag | string | No | Filter by document tag |
| metadata | object | No | Filter by metadata key-value pairs |
| completed_from | datetime | No | Include documents completed after this date |
| completed_to | datetime | No | Include documents completed before this date |
| created_from | datetime | No | Include documents created after this date |
| created_to | datetime | No | Include documents created before this date |
| modified_from | datetime | No | Include documents modified after this date |
| modified_to | datetime | No | Include documents modified before this date |
| deleted | boolean | No | Include only deleted documents when true |
| count | integer | No | Number of results per page (max: 100, default: 50) |
| page | integer | No | Page number (starts from 1) |
| order_by | string | No | Field to order results by |

---

#### Create Document from Template

Create a new document from an existing PandaDoc template.

**Endpoint:** `POST /documents`

**Request Body:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| template_uuid | string | Yes | The ID of the template to use |
| name | string | No | Document name |
| folder_uuid | string | No | Folder UUID to store document |
| owner | object | No | Document owner (email or membership_id) |
| recipients | array | Yes | List of recipients |
| fields | object | No | Field values to pre-fill |
| tokens | array | No | Variables to populate |
| metadata | object | No | Custom key-value data |
| tags | array | No | Document tags |

**Recipient Object:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| email | string | Yes* | Recipient email (*or phone) |
| phone | string | Yes* | Recipient phone (*or email) |
| first_name | string | No | Recipient first name |
| last_name | string | No | Recipient last name |
| role | string | No | Role name from template |
| signing_order | integer | No | Order for sequential signing |

---

#### Send Document

Send a document to recipients for signature.

**Endpoint:** `POST /documents/{id}/send`

**Request Body:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| message | string | No | Email message to recipients |
| subject | string | No | Email subject line |
| silent | boolean | No | If true, disables email notifications |
| sender | object | No | Sender email or membership_id |

**Important Notes:**
- Document must be in `document.draft` status
- After creation, documents remain in `document.uploaded` status for 3-5 seconds
- Use Document Status endpoint or Webhooks to check when ready

---

#### Download Document

Download a document as PDF.

**Endpoint:** `GET /documents/{id}/download`

---

#### Download Completed Document

Download the completed (signed) version.

**Endpoint:** `GET /documents/{id}/download-completed`

---

#### Delete Document

Delete a document.

**Endpoint:** `DELETE /documents/{id}`

---

#### Update Document

Update document properties.

**Endpoint:** `PATCH /documents/{id}`

---

### Templates

#### List Templates

Retrieve all templates.

**Endpoint:** `GET /templates`

---

#### Create Template from File Upload

Create a new template from a PDF or DOCX file.

**Endpoint:** `POST /templates`

---

#### Get Template Details

Retrieve template information.

**Endpoint:** `GET /templates/{id}`

---

#### Delete Template

Delete a template.

**Endpoint:** `DELETE /templates/{id}`

---

### Webhooks

#### List Webhook Subscriptions

Retrieve all webhook subscriptions.

**Endpoint:** `GET /webhook-subscriptions`

---

#### Create Webhook Subscription

Subscribe to document events.

**Endpoint:** `POST /webhook-subscriptions`

**Request Body:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| url | string | Yes | Webhook endpoint URL |
| events | array | Yes | Array of event types to subscribe to |
| shared_key | string | No | Secret key for webhook signature verification |

**Available Events:**

| Event | Description |
|-------|-------------|
| document_created | Document created |
| document_state_changed | Document status changed |
| document_deleted | Document deleted |
| document_updated | Document updated |
| document_creation_failed | Document creation failed |
| recipient_completed | Recipient completed signing |
| document_completed_pdf_ready | Completed PDF available |
| quote_updated | Quote updated |
| template_created | Template created |
| template_updated | Template updated |
| template_deleted | Template deleted |

---

#### Webhook Payload Structure

**Headers:**

```
Content-Type: application/json
X-PandaDoc-Signature: sha256=...
X-PandaDoc-Timestamp: 2024-01-15T10:30:00Z
```

---

#### Verify Webhook Authenticity

**Node.js Example:**

```javascript
const crypto = require('crypto');

function verifyWebhook(payload, signature, sharedKey) {
  const expectedSignature = 'sha256=' + 
    crypto
      .createHmac('sha256', sharedKey)
      .update(JSON.stringify(payload))
      .digest('hex');
  
  return signature === expectedSignature;
}
```

---

### Embedded Signing

#### Create Document Session for Embedded Sign

Create an embedded signing session for in-app signing.

**Endpoint:** `POST /documents/{id}/session/embedded-sign`

**Request Body:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| recipient | string | Yes | Recipient email or ID |
| redirect_url | string | No | URL to redirect after signing |

---

### Document Recipients

#### Add Document Recipient

Add a recipient to a document.

**Endpoint:** `POST /documents/{id}/recipients`

---

#### Update Document Recipient

Update recipient information.

**Endpoint:** `PATCH /documents/{id}/recipients/{recipient_id}`

---

#### Delete Document Recipient

Remove a recipient from a document.

**Endpoint:** `DELETE /documents/{id}/recipients/{recipient_id}`

---

### Folders

#### List Document Folders

**Endpoint:** `GET /documents/folders`

---

#### Create Document Folder

**Endpoint:** `POST /documents/folders`

---

### Contacts

#### List Contacts

**Endpoint:** `GET /contacts`

---

#### Create Contact

**Endpoint:** `POST /contacts`

---

## Step-by-Step Workflows

### Workflow 1: Create and Send Document for E-Signature

1. List available templates: `GET /templates`
2. Create document from template: `POST /documents`
3. Wait for document to be ready (poll status or use webhook)
4. Send document for signature: `POST /documents/{id}/send`
5. Monitor via webhook for completion event
6. Download completed document: `GET /documents/{id}/download-completed`

### Workflow 2: Embedded Signing Integration

1. Create document from template: `POST /documents`
2. Send document silently: `POST /documents/{id}/send` with `silent: true`
3. Create embedded signing session: `POST /documents/{id}/session/embedded-sign`
4. Embed the returned embed_url in an iframe
5. Handle redirect to completion URL
6. Download completed document via API

### Workflow 3: Webhook Integration

1. Create webhook subscription: `POST /webhook-subscriptions`
2. Create server endpoint to receive webhooks
3. Verify webhook signature using shared_key
4. Process webhook payload based on event type

---

## Error Handling

### Common HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request - Invalid parameters |
| 401 | Authentication error - Invalid API key |
| 403 | Permission error - Insufficient permissions |
| 404 | Not found - Resource doesn't exist |
| 409 | Conflict - Resource state conflict |
| 429 | Too Many Requests - Rate limit exceeded |

---

## Best Practices

### Performance

1. Use `date_created` ordering for consistent pagination results
2. Include date ranges when filtering large datasets
3. Limit count to 100 or less per request
4. Use webhooks instead of polling for status changes
5. Cache template IDs to avoid repeated template listing

### Document Creation

1. Wait 3-5 seconds after creation before sending
2. Use Document Status endpoint or webhooks to check readiness
3. Pre-fill fields using the fields parameter for better UX
4. Set signing order for sequential signature workflows

### Webhooks

1. Always verify signatures using the shared_key
2. Return 200 status quickly - process webhooks asynchronously
3. Handle duplicate events - webhooks may be delivered multiple times
4. Use idempotent processing for reliability

### Security

1. Store API keys securely - never expose in client-side code
2. Use OAuth 2.0 for multi-tenant applications
3. Use sandbox keys for development/testing
4. Rotate API keys periodically

---

## SDKs and Libraries

### Official SDKs

- **Python:** `pip install pandadoc-api-client`
- **Node.js:** `npm install @pandadoc/node-client`
- **Ruby:** `gem install pandadoc_api`

### Postman Collection

Import the official PandaDoc Postman collection from the Developer Portal.

---

## Support

- **Documentation:** https://developers.pandadoc.com/
- **API Reference:** https://developers.pandadoc.com/reference/about
- **Support:** Contact via Developer Portal
- **Changelog:** https://developers.pandadoc.com/changelog

---

## Parameters

- **action**: The action to perform (create_document, list_documents, send_document, create_webhook, list_templates, get_document, download_document, create_template, list_contacts, etc.)
- **params**: JSON string of parameters specific to the action (document_id, template_uuid, recipients, fields, webhook_url, events, etc.)

## Returns

- JSON response from PandaDoc API with document IDs, status, download URLs, webhook subscription confirmation, or error messages with details.

## Usage Examples

### Create Document from Template

```
action: create_document
params: {
  "template_uuid": "iMymdDd9XFD3HyxP5VD67Q",
  "name": "NDA - Client",
  "recipients": [{"email": "client@example.com", "role": "Signer"}]
}
```

### Send Document

```
action: send_document
params: {
  "document_id": "xyz789abc",
  "subject": "Please sign",
  "message": "Review and sign the attached document."
}
```

### Create Webhook

```
action: create_webhook
params: {
  "url": "https://your-server.com/webhooks/pandadoc",
  "events": ["document_state_changed", "recipient_completed"]
}
```