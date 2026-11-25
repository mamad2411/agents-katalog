---
name: postmark-api
description: "Postmark API skill. Use when working with Postmark for email, deliverystats, bounces. Covers 43 endpoints."
version: 1.0.0
generator: lapsh
---

# Postmark API
API version: 1.0.0

## Auth
No authentication required.

## Base URL
https://api.postmarkapp.com/

## Setup
1. No auth setup needed
2. GET /deliverystats -- verify access
3. POST /email -- create first email

## Endpoints

43 endpoints across 8 groups. See references/api-spec.lap for full details.

### email
| Method | Path | Description |
|--------|------|-------------|
| POST | /email | Send a single email |
| POST | /email/batch | Send a batch of emails |
| POST | /email/withTemplate | Send an email using a Template |
| POST | /email/batchWithTemplates | Send a batch of email using templates. |

### deliverystats
| Method | Path | Description |
|--------|------|-------------|
| GET | /deliverystats | Get delivery stats |

### bounces
| Method | Path | Description |
|--------|------|-------------|
| GET | /bounces | Get bounces |
| GET | /bounces/{bounceid} | Get a single bounce |
| GET | /bounces/{bounceid}/dump | Get bounce dump |
| PUT | /bounces/{bounceid}/activate | Activate a bounce |

### messages
| Method | Path | Description |
|--------|------|-------------|
| GET | /messages/outbound | Outbound message search |
| GET | /messages/outbound/{messageid}/details | Outbound message details |
| GET | /messages/outbound/{messageid}/dump | Outbound message dump |
| GET | /messages/inbound | Inbound message search |
| GET | /messages/inbound/{messageid}/details | Inbound message details |
| PUT | /messages/inbound/{messageid}/bypass | Bypass rules for a blocked inbound message |
| PUT | /messages/inbound/{messageid}/retry | Retry a failed inbound message for processing |
| GET | /messages/outbound/opens | Opens for all messages |
| GET | /messages/outbound/opens/{messageid} | Retrieve Message Opens |
| GET | /messages/outbound/clicks | Clicks for a all messages |
| GET | /messages/outbound/clicks/{messageid} | Retrieve Message Clicks |

### templates
| Method | Path | Description |
|--------|------|-------------|
| GET | /templates | Get the Templates associated with this Server |
| POST | /templates | Create a Template |
| GET | /templates/{templateIdOrAlias} | Get a Template |
| PUT | /templates/{templateIdOrAlias} | Update a Template |
| DELETE | /templates/{templateIdOrAlias} | Delete a Template |
| POST | /templates/validate | Test Template Content |

### stats
| Method | Path | Description |
|--------|------|-------------|
| GET | /stats/outbound | Get outbound overview |
| GET | /stats/outbound/sends | Get sent counts |
| GET | /stats/outbound/bounces | Get bounce counts |
| GET | /stats/outbound/spam | Get spam complaints |
| GET | /stats/outbound/tracked | Get tracked email counts |
| GET | /stats/outbound/opens | Get email open counts |
| GET | /stats/outbound/opens/platforms | Get email platform usage |
| GET | /stats/outbound/opens/emailclients | Get email client usage |
| GET | /stats/outbound/clicks | Get click counts |
| GET | /stats/outbound/clicks/browserfamilies | Get browser usage by family |
| GET | /stats/outbound/clicks/platforms | Get browser plaform usage |
| GET | /stats/outbound/clicks/location | Get clicks by body location |

### triggers
| Method | Path | Description |
|--------|------|-------------|
| POST | /triggers/inboundrules | Create an inbound rule trigger |
| GET | /triggers/inboundrules | List inbound rule triggers |
| DELETE | /triggers/inboundrules/{triggerid} | Delete a single trigger |

### server
| Method | Path | Description |
|--------|------|-------------|
| GET | /server | Get Server Configuration |
| PUT | /server | Edit Server Configuration |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a email?" -> POST /email
- "Create a batch?" -> POST /email/batch
- "List all deliverystats?" -> GET /deliverystats
- "List all bounces?" -> GET /bounces
- "Get bounce details?" -> GET /bounces/{bounceid}
- "List all dump?" -> GET /bounces/{bounceid}/dump
- "List all outbound?" -> GET /messages/outbound
- "List all details?" -> GET /messages/outbound/{messageid}/details
- "List all dump?" -> GET /messages/outbound/{messageid}/dump
- "List all inbound?" -> GET /messages/inbound
- "List all details?" -> GET /messages/inbound/{messageid}/details
- "List all opens?" -> GET /messages/outbound/opens
- "Get open details?" -> GET /messages/outbound/opens/{messageid}
- "List all clicks?" -> GET /messages/outbound/clicks
- "Get click details?" -> GET /messages/outbound/clicks/{messageid}
- "Create a withTemplate?" -> POST /email/withTemplate
- "Create a batchWithTemplate?" -> POST /email/batchWithTemplates
- "List all templates?" -> GET /templates
- "Create a template?" -> POST /templates
- "Get template details?" -> GET /templates/{templateIdOrAlias}
- "Update a template?" -> PUT /templates/{templateIdOrAlias}
- "Delete a template?" -> DELETE /templates/{templateIdOrAlias}
- "Create a validate?" -> POST /templates/validate
- "List all outbound?" -> GET /stats/outbound
- "List all sends?" -> GET /stats/outbound/sends
- "List all bounces?" -> GET /stats/outbound/bounces
- "List all spam?" -> GET /stats/outbound/spam
- "List all tracked?" -> GET /stats/outbound/tracked
- "List all opens?" -> GET /stats/outbound/opens
- "List all platforms?" -> GET /stats/outbound/opens/platforms
- "List all emailclients?" -> GET /stats/outbound/opens/emailclients
- "List all clicks?" -> GET /stats/outbound/clicks
- "List all browserfamilies?" -> GET /stats/outbound/clicks/browserfamilies
- "List all platforms?" -> GET /stats/outbound/clicks/platforms
- "List all location?" -> GET /stats/outbound/clicks/location
- "Create a inboundrule?" -> POST /triggers/inboundrules
- "List all inboundrules?" -> GET /triggers/inboundrules
- "Delete a inboundrule?" -> DELETE /triggers/inboundrules/{triggerid}
- "List all server?" -> GET /server

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
