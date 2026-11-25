---
name: seven
description: "seven API skill. Use when working with seven for analytics, balance, contacts. Covers 51 endpoints."
version: 1.0.0
generator: lapsh
---

# seven
API version: 1.0.0

## Auth
OAuth2

## Base URL
https://gateway.seven.io/api

## Setup
1. Configure auth: OAuth2
2. GET /analytics/country -- verify access
3. POST /contacts -- create first contacts

## Endpoints

51 endpoints across 16 groups. See references/api-spec.lap for full details.

### analytics
| Method | Path | Description |
|--------|------|-------------|
| GET | /analytics/country | Get Analytics By Country |
| GET | /analytics/date | Get Analytics By Date |
| GET | /analytics/label | Get Analytics By Label |
| GET | /analytics/subaccount | Get Analytics By Label |

### balance
| Method | Path | Description |
|--------|------|-------------|
| GET | /balance | Get Balance |

### contacts
| Method | Path | Description |
|--------|------|-------------|
| GET | /contacts | List Contacts |
| POST | /contacts | Create Contact |
| DELETE | /contacts/{id} | Delete Contact |
| GET | /contacts/{id} | Get Contact |
| PATCH | /contacts/{id} | Update Contact |

### groups
| Method | Path | Description |
|--------|------|-------------|
| GET | /groups | List Groups |
| POST | /groups | Create Group |
| DELETE | /groups/{id} | Delete Group |
| GET | /groups/{id} | Get Group |
| PATCH | /groups/{id} | Update Group |

### hooks
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /hooks | Delete Hook |
| GET | /hooks | List Hooks |
| POST | /hooks | Create Hook |

### journal
| Method | Path | Description |
|--------|------|-------------|
| GET | /journal/outbound | Get outbound messages |
| GET | /journal/inbound | Get inbound messages |
| GET | /journal/replies | Get message replies |
| GET | /journal/voice | Get voice journal |

### lookup
| Method | Path | Description |
|--------|------|-------------|
| GET | /lookup/cnam | Lookup Caller Name |
| GET | /lookup/format | Lookup Format |
| GET | /lookup/hlr | Lookup HLR |
| GET | /lookup/mnp | Lookup MNP |
| GET | /lookup/rcs | Lookup RCS Capabilities |

### numbers
| Method | Path | Description |
|--------|------|-------------|
| GET | /numbers/active | List Active Numbers |
| DELETE | /numbers/active/{number} | Delete Number |
| GET | /numbers/active/{number} | Get Number |
| PATCH | /numbers/active/{number} | Update Number |
| GET | /numbers/available | Get Available Numbers |
| POST | /numbers/order | Order Number |

### pricing
| Method | Path | Description |
|--------|------|-------------|
| GET | /pricing | Get Pricing |

### rcs
| Method | Path | Description |
|--------|------|-------------|
| POST | /rcs/events | Trigger RCS Event |
| POST | /rcs/messages | Send RCS |
| DELETE | /rcs/messages/{id} | Delete RCS |

### sms
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /sms | Delete Sms |
| POST | /sms | Send Sms |

### status
| Method | Path | Description |
|--------|------|-------------|
| GET | /status | Get SMS Status |

### subaccounts
| Method | Path | Description |
|--------|------|-------------|
| GET | /subaccounts/list | List Subaccounts |
| POST | /subaccounts/create | Create Subaccount |
| POST | /subaccounts/update | Automatic Balance Transfer |
| POST | /subaccounts/transfer_credits | Manual Credit Transfer |
| POST | /subaccounts/delete | Delete Subaccount |

### validate_for_voice
| Method | Path | Description |
|--------|------|-------------|
| POST | /validate_for_voice | Validate Caller ID for Voice |

### voice
| Method | Path | Description |
|--------|------|-------------|
| POST | /voice | Send text-to-speech Voice Call |
| POST | /voice/{call_id}/hangup | End Voice Call |

### waba
| Method | Path | Description |
|--------|------|-------------|
| POST | /waba/messages | Send WhatsApp Message |
| DELETE | /waba/messages/{id} | Delete WhatsApp Message |
| POST | /waba/events | Trigger WhatsApp Event |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all country?" -> GET /analytics/country
- "List all date?" -> GET /analytics/date
- "List all label?" -> GET /analytics/label
- "List all subaccount?" -> GET /analytics/subaccount
- "List all balance?" -> GET /balance
- "List all contacts?" -> GET /contacts
- "Create a contact?" -> POST /contacts
- "Delete a contact?" -> DELETE /contacts/{id}
- "Get contact details?" -> GET /contacts/{id}
- "Partially update a contact?" -> PATCH /contacts/{id}
- "List all groups?" -> GET /groups
- "Create a group?" -> POST /groups
- "Delete a group?" -> DELETE /groups/{id}
- "Get group details?" -> GET /groups/{id}
- "Partially update a group?" -> PATCH /groups/{id}
- "List all hooks?" -> GET /hooks
- "Create a hook?" -> POST /hooks
- "List all outbound?" -> GET /journal/outbound
- "List all inbound?" -> GET /journal/inbound
- "List all replies?" -> GET /journal/replies
- "List all voice?" -> GET /journal/voice
- "List all cnam?" -> GET /lookup/cnam
- "List all format?" -> GET /lookup/format
- "List all hlr?" -> GET /lookup/hlr
- "List all mnp?" -> GET /lookup/mnp
- "List all rcs?" -> GET /lookup/rcs
- "List all active?" -> GET /numbers/active
- "Delete a active?" -> DELETE /numbers/active/{number}
- "Get active details?" -> GET /numbers/active/{number}
- "Partially update a active?" -> PATCH /numbers/active/{number}
- "List all available?" -> GET /numbers/available
- "Create a order?" -> POST /numbers/order
- "List all pricing?" -> GET /pricing
- "Create a event?" -> POST /rcs/events
- "Create a message?" -> POST /rcs/messages
- "Delete a message?" -> DELETE /rcs/messages/{id}
- "Create a sm?" -> POST /sms
- "List all status?" -> GET /status
- "List all list?" -> GET /subaccounts/list
- "Create a create?" -> POST /subaccounts/create
- "Create a update?" -> POST /subaccounts/update
- "Create a transfer_credit?" -> POST /subaccounts/transfer_credits
- "Create a delete?" -> POST /subaccounts/delete
- "Create a validate_for_voice?" -> POST /validate_for_voice
- "Create a voice?" -> POST /voice
- "Create a hangup?" -> POST /voice/{call_id}/hangup
- "Create a message?" -> POST /waba/messages
- "Delete a message?" -> DELETE /waba/messages/{id}
- "Create a event?" -> POST /waba/events
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
