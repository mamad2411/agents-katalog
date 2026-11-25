---
name: resend
description: "Resend API skill. Use when working with Resend for emails, domains, api-keys. Covers 67 endpoints."
version: 1.0.0
generator: lapsh
---

# Resend
API version: 1.5.0

## Auth
Bearer bearer

## Base URL
https://api.resend.com

## Setup
1. Set Authorization header with your Bearer token
2. GET /emails -- verify access
3. POST /emails -- create first emails

## Endpoints

67 endpoints across 11 groups. See references/api-spec.lap for full details.

### emails
| Method | Path | Description |
|--------|------|-------------|
| POST | /emails | Send an email |
| GET | /emails | Retrieve a list of emails |
| GET | /emails/{email_id} | Retrieve a single email |
| PATCH | /emails/{email_id} | Update a single email |
| POST | /emails/{email_id}/cancel | Cancel the schedule of the e-mail. |
| POST | /emails/batch | Trigger up to 100 batch emails at once. |
| GET | /emails/{email_id}/attachments | Retrieve a list of attachments for a sent email |
| GET | /emails/{email_id}/attachments/{attachment_id} | Retrieve a single attachment for a sent email |
| GET | /emails/receiving | Retrieve a list of received emails |
| GET | /emails/receiving/{email_id} | Retrieve a single received email |
| GET | /emails/receiving/{email_id}/attachments | Retrieve a list of attachments for a received email |
| GET | /emails/receiving/{email_id}/attachments/{attachment_id} | Retrieve a single attachment for a received email |

### domains
| Method | Path | Description |
|--------|------|-------------|
| POST | /domains | Create a new domain |
| GET | /domains | Retrieve a list of domains |
| GET | /domains/{domain_id} | Retrieve a single domain |
| PATCH | /domains/{domain_id} | Update an existing domain |
| DELETE | /domains/{domain_id} | Remove an existing domain |
| POST | /domains/{domain_id}/verify | Verify an existing domain |

### api-keys
| Method | Path | Description |
|--------|------|-------------|
| POST | /api-keys | Create a new API key |
| GET | /api-keys | Retrieve a list of API keys |
| DELETE | /api-keys/{api_key_id} | Remove an existing API key |

### templates
| Method | Path | Description |
|--------|------|-------------|
| POST | /templates | Create a template |
| GET | /templates | Retrieve a list of templates |
| GET | /templates/{id} | Retrieve a single template |
| PATCH | /templates/{id} | Update an existing template |
| DELETE | /templates/{id} | Remove an existing template |
| POST | /templates/{id}/publish | Publish a template |
| POST | /templates/{id}/duplicate | Duplicate a template |

### audiences
| Method | Path | Description |
|--------|------|-------------|
| POST | /audiences | Create a list of contacts |
| GET | /audiences | Retrieve a list of audiences |
| DELETE | /audiences/{id} | Remove an existing audience |
| GET | /audiences/{id} | Retrieve a single audience |

### contacts
| Method | Path | Description |
|--------|------|-------------|
| POST | /contacts | Create a new contact |
| GET | /contacts | Retrieve a list of contacts |
| GET | /contacts/{id} | Retrieve a single contact by ID or email |
| PATCH | /contacts/{id} | Update a single contact by ID or email |
| DELETE | /contacts/{id} | Remove an existing contact by ID or email |
| GET | /contacts/{contact_id}/segments | Retrieve a list of segments for a contact |
| POST | /contacts/{contact_id}/segments/{segment_id} | Add a contact to a segment |
| DELETE | /contacts/{contact_id}/segments/{segment_id} | Remove a contact from a segment |
| GET | /contacts/{contact_id}/topics | Retrieve topics for a contact |
| PATCH | /contacts/{contact_id}/topics | Update topics for a contact |

### broadcasts
| Method | Path | Description |
|--------|------|-------------|
| POST | /broadcasts | Create a broadcast |
| GET | /broadcasts | Retrieve a list of broadcasts |
| DELETE | /broadcasts/{id} | Remove an existing broadcast that is in the draft status |
| GET | /broadcasts/{id} | Retrieve a single broadcast |
| PATCH | /broadcasts/{id} | Update an existing broadcast |
| POST | /broadcasts/{id}/send | Send or schedule a broadcast |

### webhooks
| Method | Path | Description |
|--------|------|-------------|
| POST | /webhooks | Create a new webhook |
| GET | /webhooks | Retrieve a list of webhooks |
| GET | /webhooks/{webhook_id} | Retrieve a single webhook |
| PATCH | /webhooks/{webhook_id} | Update an existing webhook |
| DELETE | /webhooks/{webhook_id} | Remove an existing webhook |

### segments
| Method | Path | Description |
|--------|------|-------------|
| POST | /segments | Create a new segment |
| GET | /segments | Retrieve a list of segments |
| GET | /segments/{id} | Retrieve a single segment |
| DELETE | /segments/{id} | Remove an existing segment |

### topics
| Method | Path | Description |
|--------|------|-------------|
| POST | /topics | Create a new topic |
| GET | /topics | Retrieve a list of topics |
| GET | /topics/{id} | Retrieve a single topic |
| PATCH | /topics/{id} | Update an existing topic |
| DELETE | /topics/{id} | Remove an existing topic |

### contact-properties
| Method | Path | Description |
|--------|------|-------------|
| POST | /contact-properties | Create a new contact property |
| GET | /contact-properties | Retrieve a list of contact properties |
| GET | /contact-properties/{id} | Retrieve a single contact property |
| PATCH | /contact-properties/{id} | Update an existing contact property |
| DELETE | /contact-properties/{id} | Remove an existing contact property |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a email?" -> POST /emails
- "List all emails?" -> GET /emails
- "Get email details?" -> GET /emails/{email_id}
- "Partially update a email?" -> PATCH /emails/{email_id}
- "Create a cancel?" -> POST /emails/{email_id}/cancel
- "Create a batch?" -> POST /emails/batch
- "List all attachments?" -> GET /emails/{email_id}/attachments
- "Get attachment details?" -> GET /emails/{email_id}/attachments/{attachment_id}
- "List all receiving?" -> GET /emails/receiving
- "Get receiving details?" -> GET /emails/receiving/{email_id}
- "List all attachments?" -> GET /emails/receiving/{email_id}/attachments
- "Get attachment details?" -> GET /emails/receiving/{email_id}/attachments/{attachment_id}
- "Create a domain?" -> POST /domains
- "List all domains?" -> GET /domains
- "Get domain details?" -> GET /domains/{domain_id}
- "Partially update a domain?" -> PATCH /domains/{domain_id}
- "Delete a domain?" -> DELETE /domains/{domain_id}
- "Create a verify?" -> POST /domains/{domain_id}/verify
- "Create a api-key?" -> POST /api-keys
- "List all api-keys?" -> GET /api-keys
- "Delete a api-key?" -> DELETE /api-keys/{api_key_id}
- "Create a template?" -> POST /templates
- "List all templates?" -> GET /templates
- "Get template details?" -> GET /templates/{id}
- "Partially update a template?" -> PATCH /templates/{id}
- "Delete a template?" -> DELETE /templates/{id}
- "Create a publish?" -> POST /templates/{id}/publish
- "Create a duplicate?" -> POST /templates/{id}/duplicate
- "Create a audience?" -> POST /audiences
- "List all audiences?" -> GET /audiences
- "Delete a audience?" -> DELETE /audiences/{id}
- "Get audience details?" -> GET /audiences/{id}
- "Create a contact?" -> POST /contacts
- "List all contacts?" -> GET /contacts
- "Get contact details?" -> GET /contacts/{id}
- "Partially update a contact?" -> PATCH /contacts/{id}
- "Delete a contact?" -> DELETE /contacts/{id}
- "Create a broadcast?" -> POST /broadcasts
- "List all broadcasts?" -> GET /broadcasts
- "Delete a broadcast?" -> DELETE /broadcasts/{id}
- "Get broadcast details?" -> GET /broadcasts/{id}
- "Partially update a broadcast?" -> PATCH /broadcasts/{id}
- "Create a send?" -> POST /broadcasts/{id}/send
- "Create a webhook?" -> POST /webhooks
- "List all webhooks?" -> GET /webhooks
- "Get webhook details?" -> GET /webhooks/{webhook_id}
- "Partially update a webhook?" -> PATCH /webhooks/{webhook_id}
- "Delete a webhook?" -> DELETE /webhooks/{webhook_id}
- "Create a segment?" -> POST /segments
- "List all segments?" -> GET /segments
- "Get segment details?" -> GET /segments/{id}
- "Delete a segment?" -> DELETE /segments/{id}
- "Create a topic?" -> POST /topics
- "List all topics?" -> GET /topics
- "Get topic details?" -> GET /topics/{id}
- "Partially update a topic?" -> PATCH /topics/{id}
- "Delete a topic?" -> DELETE /topics/{id}
- "Create a contact-property?" -> POST /contact-properties
- "List all contact-properties?" -> GET /contact-properties
- "Get contact-property details?" -> GET /contact-properties/{id}
- "Partially update a contact-property?" -> PATCH /contact-properties/{id}
- "Delete a contact-property?" -> DELETE /contact-properties/{id}
- "List all segments?" -> GET /contacts/{contact_id}/segments
- "Delete a segment?" -> DELETE /contacts/{contact_id}/segments/{segment_id}
- "List all topics?" -> GET /contacts/{contact_id}/topics
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
