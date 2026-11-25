---
name: callfire-api-documentation
description: "CallFire API Documentation API skill. Use when working with CallFire API Documentation for calls, campaigns, contacts. Covers 123 endpoints."
version: 1.0.0
generator: lapsh
---

# CallFire API Documentation
API version: V2

## Auth
basic

## Base URL
https://api.callfire.com/v2

## Setup
1. Configure auth: basic
2. GET /calls -- verify access
3. POST /calls -- create first calls

## Endpoints

123 endpoints across 11 groups. See references/api-spec.lap for full details.

### calls
| Method | Path | Description |
|--------|------|-------------|
| GET | /calls | Find calls |
| POST | /calls | Send calls |
| GET | /calls/broadcasts | Find call broadcasts |
| POST | /calls/broadcasts | Create a call broadcast |
| GET | /calls/broadcasts/{id} | Find a specific call broadcast |
| PUT | /calls/broadcasts/{id} | Update a call broadcast |
| POST | /calls/broadcasts/{id}/archive | Archive voice broadcast |
| GET | /calls/broadcasts/{id}/batches | Find batches in a call broadcast |
| POST | /calls/broadcasts/{id}/batches | Add batches to a call broadcast |
| GET | /calls/broadcasts/{id}/calls | Find calls in a call broadcast |
| POST | /calls/broadcasts/{id}/recipients | Add recipients to a call broadcast |
| POST | /calls/broadcasts/{id}/start | Start voice broadcast |
| GET | /calls/broadcasts/{id}/stats | Get statistics on call broadcast |
| POST | /calls/broadcasts/{id}/stop | Stop voice broadcast |
| POST | /calls/broadcasts/{id}/toggleRecipientsStatus | Disable/enable undialed recipients in broadcast |
| GET | /calls/recordings/{id} | Get call recording by id |
| GET | /calls/recordings/{id}.mp3 | Get call recording in mp3 format |
| GET | /calls/{id} | Find a specific call |
| GET | /calls/{id}/recordings | Get call recordings for a call |
| GET | /calls/{id}/recordings/{name} | Get call recording by name |
| GET | /calls/{id}/recordings/{name}.mp3 | Get call mp3 recording by name |

### campaigns
| Method | Path | Description |
|--------|------|-------------|
| GET | /campaigns/batches/{id} | Find a specific batch |
| PUT | /campaigns/batches/{id} | Update a batch |
| GET | /campaigns/sounds | Find sounds |
| POST | /campaigns/sounds/calls | Add sound via call |
| POST | /campaigns/sounds/files | Add sound via file |
| POST | /campaigns/sounds/tts | Add sound via text-to-speech |
| GET | /campaigns/sounds/{id} | Find a specific sound |
| DELETE | /campaigns/sounds/{id} | Delete a specific sound |
| GET | /campaigns/sounds/{id}.mp3 | Download a MP3 sound |
| GET | /campaigns/sounds/{id}.wav | Download a WAV sound |

### contacts
| Method | Path | Description |
|--------|------|-------------|
| GET | /contacts | Find contacts |
| POST | /contacts | Create contacts |
| GET | /contacts/dncs | Find do not contact (dnc) items |
| POST | /contacts/dncs | Add do not contact (dnc) numbers |
| DELETE | /contacts/dncs/sources/{source} | Delete do not contact (dnc) numbers contained in source. |
| GET | /contacts/dncs/universals/{toNumber} | Find universal do not contacts (udnc) associated with toNumber |
| GET | /contacts/dncs/{number} | Get do not contact (dnc) |
| PUT | /contacts/dncs/{number} | Update an individual do not contact (dnc) number |
| DELETE | /contacts/dncs/{number} | Delete do not contact (dnc) number. If number contains commas treat as list of numbers |
| GET | /contacts/lists | Find contact lists |
| POST | /contacts/lists | Create contact lists |
| POST | /contacts/lists/upload | Create contact list from file |
| GET | /contacts/lists/{id} | Find a specific contact list |
| PUT | /contacts/lists/{id} | Update a contact list |
| DELETE | /contacts/lists/{id} | Delete a contact list |
| GET | /contacts/lists/{id}/items | Find contacts in a contact list |
| POST | /contacts/lists/{id}/items | Add contacts to a contact list |
| DELETE | /contacts/lists/{id}/items | Delete contacts from a contact list |
| DELETE | /contacts/lists/{id}/items/{contactId} | Delete a contact from a contact list |
| GET | /contacts/{id} | Find a specific contact |
| PUT | /contacts/{id} | Update a contact |
| DELETE | /contacts/{id} | Delete a contact |
| GET | /contacts/{id}/history | Find a contact's history |

### keywords
| Method | Path | Description |
|--------|------|-------------|
| GET | /keywords | Find keywords |
| GET | /keywords/leases | Find keyword leases |
| GET | /keywords/leases/configs | Find keyword lease configs |
| GET | /keywords/leases/configs/{keyword} | Find a specific keyword lease config |
| PUT | /keywords/leases/configs/{keyword} | Update a keyword lease config |
| GET | /keywords/leases/id/{id} | Find a keyword by id |
| GET | /keywords/leases/{keyword} | Find a specific lease |
| PUT | /keywords/leases/{keyword} | Update a lease |
| GET | /keywords/{keyword}/available | Check for a specific keyword |

### me
| Method | Path | Description |
|--------|------|-------------|
| GET | /me/account | Find account details |
| GET | /me/api/credentials | Find api credentials |
| POST | /me/api/credentials | Create api credentials |
| GET | /me/api/credentials/{id} | Find a specific api credential |
| DELETE | /me/api/credentials/{id} | Delete api credentials |
| POST | /me/api/credentials/{id}/disable | Disable specified API credentials |
| POST | /me/api/credentials/{id}/enable | Enable specified API credentials |
| GET | /me/billing/credit-usage | Find credit usage |
| GET | /me/billing/credit-usage/grouped/{rollupBinType} | Find credit usage grouped by period |
| GET | /me/billing/plan-usage | Find plan usage |
| GET | /me/callerids | Find caller ids |
| POST | /me/callerids/{callerid} | Create a caller id |
| POST | /me/callerids/{callerid}/verification-code | Verify a caller id |

### media
| Method | Path | Description |
|--------|------|-------------|
| GET | /media | Find media |
| POST | /media | Create media |
| GET | /media/public/{key}.{extension} | Download media by extension |
| GET | /media/{id} | Get a specific media |
| GET | /media/{id}.{extension} | Download media by extension |
| GET | /media/{id}/file | Download a MP3 media |

### numbers
| Method | Path | Description |
|--------|------|-------------|
| GET | /numbers/leases | Find leases |
| GET | /numbers/leases/configs | Find lease configs |
| GET | /numbers/leases/configs/{number} | Find a specific lease config |
| PUT | /numbers/leases/configs/{number} | Update a lease config |
| GET | /numbers/leases/{number} | Find a specific lease |
| PUT | /numbers/leases/{number} | Update a lease |
| GET | /numbers/local | Find local numbers |
| GET | /numbers/regions | Find number regions |
| GET | /numbers/tollfree | Find tollfree numbers |

### orders
| Method | Path | Description |
|--------|------|-------------|
| GET | /orders | Find orders |
| POST | /orders/keywords | Purchase keywords |
| POST | /orders/numbers | Purchase numbers |
| GET | /orders/{id} | Find a specific order |

### reports
| Method | Path | Description |
|--------|------|-------------|
| GET | /reports/delivery | Get delivery reports by ad hoc criteria |

### texts
| Method | Path | Description |
|--------|------|-------------|
| GET | /texts | Find texts |
| POST | /texts | Send texts |
| GET | /texts/auto-replys | Find auto replies |
| POST | /texts/auto-replys | Create an auto reply |
| GET | /texts/auto-replys/{id} | Find a specific auto reply |
| DELETE | /texts/auto-replys/{id} | Delete an auto reply |
| GET | /texts/broadcasts | Find text broadcasts |
| POST | /texts/broadcasts | Create a text broadcast |
| GET | /texts/broadcasts/{id} | Find a specific text broadcast |
| PUT | /texts/broadcasts/{id} | Update a text broadcast |
| POST | /texts/broadcasts/{id}/archive | Archive text broadcast |
| GET | /texts/broadcasts/{id}/batches | Find batches in a text broadcast |
| POST | /texts/broadcasts/{id}/batches | Add batches to a text broadcast |
| POST | /texts/broadcasts/{id}/recipients | Add recipients to a text broadcast |
| POST | /texts/broadcasts/{id}/start | Start text broadcast |
| GET | /texts/broadcasts/{id}/stats | Get statistics on text broadcast |
| POST | /texts/broadcasts/{id}/stop | Stop text broadcast |
| GET | /texts/broadcasts/{id}/texts | Find texts in a text broadcast |
| POST | /texts/broadcasts/{id}/toggleRecipientsStatus | Disable/enable undialed recipients in broadcast |
| GET | /texts/{id} | Find a specific text |

### webhooks
| Method | Path | Description |
|--------|------|-------------|
| GET | /webhooks | Find webhooks |
| POST | /webhooks | Create a webhook |
| GET | /webhooks/resources | Find webhook resources |
| GET | /webhooks/resources/{resource} | Find specific webhook resource |
| GET | /webhooks/{id} | Find a specific webhook |
| PUT | /webhooks/{id} | Update a webhook |
| DELETE | /webhooks/{id} | Delete a webhook |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all calls?" -> GET /calls
- "Create a call?" -> POST /calls
- "List all broadcasts?" -> GET /calls/broadcasts
- "Create a broadcast?" -> POST /calls/broadcasts
- "Get broadcast details?" -> GET /calls/broadcasts/{id}
- "Update a broadcast?" -> PUT /calls/broadcasts/{id}
- "Create a archive?" -> POST /calls/broadcasts/{id}/archive
- "List all batches?" -> GET /calls/broadcasts/{id}/batches
- "Create a batche?" -> POST /calls/broadcasts/{id}/batches
- "List all calls?" -> GET /calls/broadcasts/{id}/calls
- "Create a recipient?" -> POST /calls/broadcasts/{id}/recipients
- "Create a start?" -> POST /calls/broadcasts/{id}/start
- "List all stats?" -> GET /calls/broadcasts/{id}/stats
- "Create a stop?" -> POST /calls/broadcasts/{id}/stop
- "Create a toggleRecipientsStatus?" -> POST /calls/broadcasts/{id}/toggleRecipientsStatus
- "Get recording details?" -> GET /calls/recordings/{id}
- "Get recording details?" -> GET /calls/recordings/{id}.mp3
- "Get call details?" -> GET /calls/{id}
- "List all recordings?" -> GET /calls/{id}/recordings
- "Get recording details?" -> GET /calls/{id}/recordings/{name}
- "Get recording details?" -> GET /calls/{id}/recordings/{name}.mp3
- "Get batche details?" -> GET /campaigns/batches/{id}
- "Update a batche?" -> PUT /campaigns/batches/{id}
- "List all sounds?" -> GET /campaigns/sounds
- "Create a call?" -> POST /campaigns/sounds/calls
- "Create a file?" -> POST /campaigns/sounds/files
- "Create a tt?" -> POST /campaigns/sounds/tts
- "Get sound details?" -> GET /campaigns/sounds/{id}
- "Delete a sound?" -> DELETE /campaigns/sounds/{id}
- "Get sound details?" -> GET /campaigns/sounds/{id}.mp3
- "Get sound details?" -> GET /campaigns/sounds/{id}.wav
- "List all contacts?" -> GET /contacts
- "Create a contact?" -> POST /contacts
- "List all dncs?" -> GET /contacts/dncs
- "Create a dnc?" -> POST /contacts/dncs
- "Delete a source?" -> DELETE /contacts/dncs/sources/{source}
- "Get universal details?" -> GET /contacts/dncs/universals/{toNumber}
- "Get dnc details?" -> GET /contacts/dncs/{number}
- "Update a dnc?" -> PUT /contacts/dncs/{number}
- "Delete a dnc?" -> DELETE /contacts/dncs/{number}
- "List all lists?" -> GET /contacts/lists
- "Create a list?" -> POST /contacts/lists
- "Create a upload?" -> POST /contacts/lists/upload
- "Get list details?" -> GET /contacts/lists/{id}
- "Update a list?" -> PUT /contacts/lists/{id}
- "Delete a list?" -> DELETE /contacts/lists/{id}
- "List all items?" -> GET /contacts/lists/{id}/items
- "Create a item?" -> POST /contacts/lists/{id}/items
- "Delete a item?" -> DELETE /contacts/lists/{id}/items/{contactId}
- "Get contact details?" -> GET /contacts/{id}
- "Update a contact?" -> PUT /contacts/{id}
- "Delete a contact?" -> DELETE /contacts/{id}
- "List all history?" -> GET /contacts/{id}/history
- "List all keywords?" -> GET /keywords
- "List all leases?" -> GET /keywords/leases
- "List all configs?" -> GET /keywords/leases/configs
- "Get config details?" -> GET /keywords/leases/configs/{keyword}
- "Update a config?" -> PUT /keywords/leases/configs/{keyword}
- "Get id details?" -> GET /keywords/leases/id/{id}
- "Get lease details?" -> GET /keywords/leases/{keyword}
- "Update a lease?" -> PUT /keywords/leases/{keyword}
- "List all available?" -> GET /keywords/{keyword}/available
- "List all account?" -> GET /me/account
- "List all credentials?" -> GET /me/api/credentials
- "Create a credential?" -> POST /me/api/credentials
- "Get credential details?" -> GET /me/api/credentials/{id}
- "Delete a credential?" -> DELETE /me/api/credentials/{id}
- "Create a disable?" -> POST /me/api/credentials/{id}/disable
- "Create a enable?" -> POST /me/api/credentials/{id}/enable
- "List all credit-usage?" -> GET /me/billing/credit-usage
- "Get grouped details?" -> GET /me/billing/credit-usage/grouped/{rollupBinType}
- "List all plan-usage?" -> GET /me/billing/plan-usage
- "List all callerids?" -> GET /me/callerids
- "Create a verification-code?" -> POST /me/callerids/{callerid}/verification-code
- "List all media?" -> GET /media
- "Create a media?" -> POST /media
- "Get public details?" -> GET /media/public/{key}.{extension}
- "Get media details?" -> GET /media/{id}
- "Get media details?" -> GET /media/{id}.{extension}
- "List all file?" -> GET /media/{id}/file
- "List all leases?" -> GET /numbers/leases
- "List all configs?" -> GET /numbers/leases/configs
- "Get config details?" -> GET /numbers/leases/configs/{number}
- "Update a config?" -> PUT /numbers/leases/configs/{number}
- "Get lease details?" -> GET /numbers/leases/{number}
- "Update a lease?" -> PUT /numbers/leases/{number}
- "List all local?" -> GET /numbers/local
- "List all regions?" -> GET /numbers/regions
- "List all tollfree?" -> GET /numbers/tollfree
- "List all orders?" -> GET /orders
- "Create a keyword?" -> POST /orders/keywords
- "Create a number?" -> POST /orders/numbers
- "Get order details?" -> GET /orders/{id}
- "List all delivery?" -> GET /reports/delivery
- "List all texts?" -> GET /texts
- "Create a text?" -> POST /texts
- "List all auto-replys?" -> GET /texts/auto-replys
- "Create a auto-reply?" -> POST /texts/auto-replys
- "Get auto-reply details?" -> GET /texts/auto-replys/{id}
- "Delete a auto-reply?" -> DELETE /texts/auto-replys/{id}
- "List all broadcasts?" -> GET /texts/broadcasts
- "Create a broadcast?" -> POST /texts/broadcasts
- "Get broadcast details?" -> GET /texts/broadcasts/{id}
- "Update a broadcast?" -> PUT /texts/broadcasts/{id}
- "Create a archive?" -> POST /texts/broadcasts/{id}/archive
- "List all batches?" -> GET /texts/broadcasts/{id}/batches
- "Create a batche?" -> POST /texts/broadcasts/{id}/batches
- "Create a recipient?" -> POST /texts/broadcasts/{id}/recipients
- "Create a start?" -> POST /texts/broadcasts/{id}/start
- "List all stats?" -> GET /texts/broadcasts/{id}/stats
- "Create a stop?" -> POST /texts/broadcasts/{id}/stop
- "List all texts?" -> GET /texts/broadcasts/{id}/texts
- "Create a toggleRecipientsStatus?" -> POST /texts/broadcasts/{id}/toggleRecipientsStatus
- "Get text details?" -> GET /texts/{id}
- "List all webhooks?" -> GET /webhooks
- "Create a webhook?" -> POST /webhooks
- "List all resources?" -> GET /webhooks/resources
- "Get resource details?" -> GET /webhooks/resources/{resource}
- "Get webhook details?" -> GET /webhooks/{id}
- "Update a webhook?" -> PUT /webhooks/{id}
- "Delete a webhook?" -> DELETE /webhooks/{id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
