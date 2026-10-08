---
name: adyen-recurring-api
description: "Adyen Recurring API skill. Use when working with Adyen Recurring for createPermit, disable, disablePermit. Covers 6 endpoints."
version: 1.0.0
generator: lapsh
---

# Adyen Recurring API
API version: 68

## Auth
ApiKey X-API-Key in header | Bearer basic

## Base URL
https://paltokenization-test.adyen.com/paltokenization/servlet/Recurring/v68

## Setup
1. Set Authorization header with your Bearer token
3. POST /createPermit -- create first createPermit

## Endpoints

6 endpoints across 6 groups. See references/api-spec.lap for full details.

### createPermit
| Method | Path | Description |
|--------|------|-------------|
| POST | /createPermit | Create new permits linked to a recurring contract. |

### disable
| Method | Path | Description |
|--------|------|-------------|
| POST | /disable | Disable stored payment details |

### disablePermit
| Method | Path | Description |
|--------|------|-------------|
| POST | /disablePermit | Disable an existing permit. |

### listRecurringDetails
| Method | Path | Description |
|--------|------|-------------|
| POST | /listRecurringDetails | Get stored payment details |

### notifyShopper
| Method | Path | Description |
|--------|------|-------------|
| POST | /notifyShopper | Ask issuer to notify the shopper |

### scheduleAccountUpdater
| Method | Path | Description |
|--------|------|-------------|
| POST | /scheduleAccountUpdater | Schedule running the Account Updater |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a createPermit?" -> POST /createPermit
- "Create a disable?" -> POST /disable
- "Create a disablePermit?" -> POST /disablePermit
- "Create a listRecurringDetail?" -> POST /listRecurringDetails
- "Create a notifyShopper?" -> POST /notifyShopper
- "Create a scheduleAccountUpdater?" -> POST /scheduleAccountUpdater
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
