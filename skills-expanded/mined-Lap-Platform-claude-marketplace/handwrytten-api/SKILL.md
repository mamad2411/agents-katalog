---
name: handwrytten-api
description: "Handwrytten API skill. Use when working with Handwrytten for auth, profile, fonts. Covers 30 endpoints."
version: 1.0.0
generator: lapsh
---

# Handwrytten API
API version: 1.0.0

## Auth
No authentication required.

## Base URL
https://api.handwrytten.com/v1

## Setup
1. No auth setup needed
2. GET /fonts/list -- verify access
3. POST /auth/register -- create first register

## Endpoints

30 endpoints across 9 groups. See references/api-spec.lap for full details.

### auth
| Method | Path | Description |
|--------|------|-------------|
| POST | /auth/register | Registers a new account |
| POST | /auth/authorization | Logs in to an existing account |
| POST | /auth/resetPasswordRequest | resets a user's password |
| POST | /auth/changePassword | changes a user's password |
| POST | /auth/logout | logs out a session uid |

### profile
| Method | Path | Description |
|--------|------|-------------|
| POST | /profile/address | gets the user's return address information |
| POST | /profile/updateAddress | update the user's return address information |
| POST | /profile/recipientsList | list the addresses in the user's account |
| POST | /profile/profileAddRecipient | add a new recipient address |
| POST | /profile/updateRecipient | updates an existing new recipient address |
| POST | /profile/deleteRecipient | deletes an existing recipient address |

### fonts
| Method | Path | Description |
|--------|------|-------------|
| GET | /fonts/list | Lists Handwryting styles available for use |
| GET | /fonts/listForCustomizer | Lists fonts available for use with the card customizer |

### cards
| Method | Path | Description |
|--------|------|-------------|
| POST | /cards/uploadCustomLogo | upload logo or cover image for card |
| POST | /cards/createCustomCard | Create a new custom card |
| GET | /cards/list | Lists information on cards |
| POST | /cards/list | Lists information on cards |
| POST | /cards/view | Provides full information on a specific card |

### giftCards
| Method | Path | Description |
|--------|------|-------------|
| POST | /giftCards/view | Lists information on gift cards |
| GET | /giftCards/view | Lists information on gift cards |

### templateCategories
| Method | Path | Description |
|--------|------|-------------|
| GET | /templateCategories/list | List template categories |
| POST | /templateCategories/list | List template categories |

### templates
| Method | Path | Description |
|--------|------|-------------|
| GET | /templates/list | List template categories |
| POST | /templates/list | List template categories |
| POST | /templates/view | Get all info on a template |
| POST | /templates/create | Creates a New Template in the User’s Account |
| POST | /templates/update | Updates an Existing Template in the User’s Account |
| POST | /templates/delete | Deletes a users template |

### countries
| Method | Path | Description |
|--------|------|-------------|
| GET | /countries/list | Lists the countries to which Handwritten can mail, their associated country ID and any costs |

### orders
| Method | Path | Description |
|--------|------|-------------|
| POST | /orders/singleStepOrder | sends an order in a single step.  This is much easier than using other order commands |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a register?" -> POST /auth/register
- "Create a authorization?" -> POST /auth/authorization
- "Create a resetPasswordRequest?" -> POST /auth/resetPasswordRequest
- "Create a changePassword?" -> POST /auth/changePassword
- "Create a logout?" -> POST /auth/logout
- "Create a address?" -> POST /profile/address
- "Create a updateAddress?" -> POST /profile/updateAddress
- "Create a recipientsList?" -> POST /profile/recipientsList
- "Create a profileAddRecipient?" -> POST /profile/profileAddRecipient
- "Create a updateRecipient?" -> POST /profile/updateRecipient
- "Create a deleteRecipient?" -> POST /profile/deleteRecipient
- "List all list?" -> GET /fonts/list
- "Create a uploadCustomLogo?" -> POST /cards/uploadCustomLogo
- "List all listForCustomizer?" -> GET /fonts/listForCustomizer
- "Create a createCustomCard?" -> POST /cards/createCustomCard
- "List all list?" -> GET /cards/list
- "Create a list?" -> POST /cards/list
- "Create a view?" -> POST /cards/view
- "Create a view?" -> POST /giftCards/view
- "List all view?" -> GET /giftCards/view
- "List all list?" -> GET /templateCategories/list
- "Create a list?" -> POST /templateCategories/list
- "List all list?" -> GET /templates/list
- "Create a list?" -> POST /templates/list
- "Create a view?" -> POST /templates/view
- "Create a create?" -> POST /templates/create
- "Create a update?" -> POST /templates/update
- "Create a delete?" -> POST /templates/delete
- "List all list?" -> GET /countries/list
- "Create a singleStepOrder?" -> POST /orders/singleStepOrder

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
