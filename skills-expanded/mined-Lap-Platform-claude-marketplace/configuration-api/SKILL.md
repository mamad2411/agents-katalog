---
name: configuration-api
description: "Configuration API skill. Use when working with Configuration for accountHolders, balanceAccounts, balancePlatforms. Covers 79 endpoints."
version: 1.0.0
generator: lapsh
---

# Configuration API
API version: 2

## Auth
ApiKey X-API-Key in header | Bearer basic | ApiKey clientKey in query

## Base URL
https://balanceplatform-api-test.adyen.com/bcl/v2

## Setup
1. Set Authorization header with your Bearer token
2. GET /cardorders -- verify access
3. POST /accountHolders -- create first accountHolders

## Endpoints

79 endpoints across 17 groups. See references/api-spec.lap for full details.

### accountHolders
| Method | Path | Description |
|--------|------|-------------|
| POST | /accountHolders | Create an account holder |
| GET | /accountHolders/{id} | Get an account holder |
| PATCH | /accountHolders/{id} | Update an account holder |
| GET | /accountHolders/{id}/balanceAccounts | Get all balance accounts of an account holder |
| GET | /accountHolders/{id}/taxForms | Get a tax form |
| GET | /accountHolders/{id}/transactionRules | Get all transaction rules for an account holder |
| GET | /accountHolders/{id}/taxFormSummary | Get summary of tax forms for an account holder |

### balanceAccounts
| Method | Path | Description |
|--------|------|-------------|
| POST | /balanceAccounts | Create a balance account |
| GET | /balanceAccounts/{balanceAccountId}/sweeps | Get all sweeps for a balance account |
| POST | /balanceAccounts/{balanceAccountId}/sweeps | Create a sweep |
| GET | /balanceAccounts/{balanceAccountId}/sweeps/{sweepId} | Get a sweep |
| DELETE | /balanceAccounts/{balanceAccountId}/sweeps/{sweepId} | Delete a sweep |
| PATCH | /balanceAccounts/{balanceAccountId}/sweeps/{sweepId} | Update a sweep |
| GET | /balanceAccounts/{id} | Get a balance account |
| PATCH | /balanceAccounts/{id} | Update a balance account |
| GET | /balanceAccounts/{id}/paymentInstruments | Get payment instruments linked to a balance account |
| GET | /balanceAccounts/{id}/transactionRules | Get all transaction rules for a balance account |
| POST | /balanceAccounts/{id}/transferLimits/approve | Approve pending transfer limits |
| GET | /balanceAccounts/{id}/transferLimits | Filter and view the transfer limits |
| POST | /balanceAccounts/{id}/transferLimits | Create a transfer limit |
| GET | /balanceAccounts/{id}/transferLimits/current | Get all current transfer limits |
| GET | /balanceAccounts/{id}/transferLimits/{transferLimitId} | Get the details of a transfer limit |
| DELETE | /balanceAccounts/{id}/transferLimits/{transferLimitId} | Delete a scheduled or pending transfer limit |

### balancePlatforms
| Method | Path | Description |
|--------|------|-------------|
| GET | /balancePlatforms/{id} | Get a balance platform |
| GET | /balancePlatforms/{id}/accountHolders | Get all account holders under a balance platform |
| GET | /balancePlatforms/{id}/transactionRules | Get all transaction rules for a balance platform |
| GET | /balancePlatforms/{balancePlatformId}/webhooks/{webhookId}/settings | Get all balance webhook settings |
| POST | /balancePlatforms/{balancePlatformId}/webhooks/{webhookId}/settings | Create a balance webhook setting |
| GET | /balancePlatforms/{balancePlatformId}/webhooks/{webhookId}/settings/{settingId} | Get a balance webhook setting by id |
| DELETE | /balancePlatforms/{balancePlatformId}/webhooks/{webhookId}/settings/{settingId} | Delete a balance webhook setting by id |
| PATCH | /balancePlatforms/{balancePlatformId}/webhooks/{webhookId}/settings/{settingId} | Update a balance webhook setting by id |
| GET | /balancePlatforms/{id}/transferLimits | Filter and view the transfer limits |
| POST | /balancePlatforms/{id}/transferLimits | Create a transfer limit |
| GET | /balancePlatforms/{id}/transferLimits/{transferLimitId} | Get the details of a transfer limit |
| DELETE | /balancePlatforms/{id}/transferLimits/{transferLimitId} | Delete a scheduled or pending transfer limit |

### cardorders
| Method | Path | Description |
|--------|------|-------------|
| GET | /cardorders | Get a list of card orders |
| GET | /cardorders/{id}/items | Get card order items |

### grantAccounts
| Method | Path | Description |
|--------|------|-------------|
| GET | /grantAccounts/{id} | Get a grant account |

### grantOffers
| Method | Path | Description |
|--------|------|-------------|
| GET | /grantOffers | Get all available grant offers |
| GET | /grantOffers/{grantOfferId} | Get a grant offer |

### networkTokens
| Method | Path | Description |
|--------|------|-------------|
| GET | /networkTokens/{networkTokenId} | Get a network token |
| PATCH | /networkTokens/{networkTokenId} | Update a network token |

### paymentInstrumentGroups
| Method | Path | Description |
|--------|------|-------------|
| POST | /paymentInstrumentGroups | Create a payment instrument group |
| GET | /paymentInstrumentGroups/{id} | Get a payment instrument group |
| GET | /paymentInstrumentGroups/{id}/transactionRules | Get all transaction rules for a payment instrument group |

### paymentInstruments
| Method | Path | Description |
|--------|------|-------------|
| POST | /paymentInstruments | Create a payment instrument |
| POST | /paymentInstruments/reveal | Reveal the data of a payment instrument |
| GET | /paymentInstruments/{id} | Get a payment instrument |
| PATCH | /paymentInstruments/{id} | Update a payment instrument |
| GET | /paymentInstruments/{id}/networkTokenActivationData | Get network token activation data |
| POST | /paymentInstruments/{id}/networkTokenActivationData | Create network token provisioning data |
| GET | /paymentInstruments/{id}/networkTokens | List network tokens |
| GET | /paymentInstruments/{id}/reveal | Get the PAN of a payment instrument |
| GET | /paymentInstruments/{id}/transactionRules | Get all transaction rules for a payment instrument |
| GET | /paymentInstruments/{paymentInstrumentId}/authorisedCardUsers | Get authorized users for a card. |
| POST | /paymentInstruments/{paymentInstrumentId}/authorisedCardUsers | Create authorized users for a card. |
| DELETE | /paymentInstruments/{paymentInstrumentId}/authorisedCardUsers | Delete the authorized users for a card. |
| PATCH | /paymentInstruments/{paymentInstrumentId}/authorisedCardUsers | Update the authorized users for a card. |

### pins
| Method | Path | Description |
|--------|------|-------------|
| POST | /pins/change | Change a card PIN |
| POST | /pins/reveal | Reveal a card PIN |

### publicKey
| Method | Path | Description |
|--------|------|-------------|
| GET | /publicKey | Get an RSA public key |

### registeredDevices
| Method | Path | Description |
|--------|------|-------------|
| GET | /registeredDevices | Get a list of registered SCA devices |
| POST | /registeredDevices | Initiate the registration of an SCA device |
| POST | /registeredDevices/{deviceId}/associations | Initiate an association between an SCA device and a resource |
| PATCH | /registeredDevices/{deviceId}/associations | Complete an association between an SCA device and a resource |
| DELETE | /registeredDevices/{id} | Delete a registration of an SCA device |
| PATCH | /registeredDevices/{id} | Complete the registration of an SCA device |

### transactionRules
| Method | Path | Description |
|--------|------|-------------|
| POST | /transactionRules | Create a transaction rule |
| GET | /transactionRules/{transactionRuleId} | Get a transaction rule |
| DELETE | /transactionRules/{transactionRuleId} | Delete a transaction rule |
| PATCH | /transactionRules/{transactionRuleId} | Update a transaction rule |

### transferRoutes
| Method | Path | Description |
|--------|------|-------------|
| POST | /transferRoutes/calculate | Calculate transfer routes |

### validateBankAccountIdentification
| Method | Path | Description |
|--------|------|-------------|
| POST | /validateBankAccountIdentification | Validate a bank account |

### scaAssociations
| Method | Path | Description |
|--------|------|-------------|
| GET | /scaAssociations | Get a list of devices associated with an entity |
| DELETE | /scaAssociations | Delete association to devices |
| PATCH | /scaAssociations | Approve a pending approval association |

### scaDevices
| Method | Path | Description |
|--------|------|-------------|
| POST | /scaDevices | Begin SCA device registration |
| PATCH | /scaDevices/{deviceId} | Finish registration process for a SCA device |
| POST | /scaDevices/{deviceId}/scaAssociations | Create a new SCA association for a device |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a accountHolder?" -> POST /accountHolders
- "Get accountHolder details?" -> GET /accountHolders/{id}
- "Partially update a accountHolder?" -> PATCH /accountHolders/{id}
- "List all balanceAccounts?" -> GET /accountHolders/{id}/balanceAccounts
- "List all taxForms?" -> GET /accountHolders/{id}/taxForms
- "List all transactionRules?" -> GET /accountHolders/{id}/transactionRules
- "Create a balanceAccount?" -> POST /balanceAccounts
- "List all sweeps?" -> GET /balanceAccounts/{balanceAccountId}/sweeps
- "Create a sweep?" -> POST /balanceAccounts/{balanceAccountId}/sweeps
- "Get sweep details?" -> GET /balanceAccounts/{balanceAccountId}/sweeps/{sweepId}
- "Delete a sweep?" -> DELETE /balanceAccounts/{balanceAccountId}/sweeps/{sweepId}
- "Partially update a sweep?" -> PATCH /balanceAccounts/{balanceAccountId}/sweeps/{sweepId}
- "Get balanceAccount details?" -> GET /balanceAccounts/{id}
- "Partially update a balanceAccount?" -> PATCH /balanceAccounts/{id}
- "List all paymentInstruments?" -> GET /balanceAccounts/{id}/paymentInstruments
- "List all transactionRules?" -> GET /balanceAccounts/{id}/transactionRules
- "Get balancePlatform details?" -> GET /balancePlatforms/{id}
- "List all accountHolders?" -> GET /balancePlatforms/{id}/accountHolders
- "List all transactionRules?" -> GET /balancePlatforms/{id}/transactionRules
- "List all cardorders?" -> GET /cardorders
- "List all items?" -> GET /cardorders/{id}/items
- "Get grantAccount details?" -> GET /grantAccounts/{id}
- "List all grantOffers?" -> GET /grantOffers
- "Get grantOffer details?" -> GET /grantOffers/{grantOfferId}
- "Get networkToken details?" -> GET /networkTokens/{networkTokenId}
- "Partially update a networkToken?" -> PATCH /networkTokens/{networkTokenId}
- "Create a paymentInstrumentGroup?" -> POST /paymentInstrumentGroups
- "Get paymentInstrumentGroup details?" -> GET /paymentInstrumentGroups/{id}
- "List all transactionRules?" -> GET /paymentInstrumentGroups/{id}/transactionRules
- "Create a paymentInstrument?" -> POST /paymentInstruments
- "Create a reveal?" -> POST /paymentInstruments/reveal
- "Get paymentInstrument details?" -> GET /paymentInstruments/{id}
- "Partially update a paymentInstrument?" -> PATCH /paymentInstruments/{id}
- "List all networkTokenActivationData?" -> GET /paymentInstruments/{id}/networkTokenActivationData
- "Create a networkTokenActivationData?" -> POST /paymentInstruments/{id}/networkTokenActivationData
- "List all networkTokens?" -> GET /paymentInstruments/{id}/networkTokens
- "List all reveal?" -> GET /paymentInstruments/{id}/reveal
- "List all transactionRules?" -> GET /paymentInstruments/{id}/transactionRules
- "Create a change?" -> POST /pins/change
- "Create a reveal?" -> POST /pins/reveal
- "List all publicKey?" -> GET /publicKey
- "List all registeredDevices?" -> GET /registeredDevices
- "Create a registeredDevice?" -> POST /registeredDevices
- "Create a association?" -> POST /registeredDevices/{deviceId}/associations
- "Delete a registeredDevice?" -> DELETE /registeredDevices/{id}
- "Partially update a registeredDevice?" -> PATCH /registeredDevices/{id}
- "Create a transactionRule?" -> POST /transactionRules
- "Get transactionRule details?" -> GET /transactionRules/{transactionRuleId}
- "Delete a transactionRule?" -> DELETE /transactionRules/{transactionRuleId}
- "Partially update a transactionRule?" -> PATCH /transactionRules/{transactionRuleId}
- "Create a calculate?" -> POST /transferRoutes/calculate
- "Create a validateBankAccountIdentification?" -> POST /validateBankAccountIdentification
- "List all authorisedCardUsers?" -> GET /paymentInstruments/{paymentInstrumentId}/authorisedCardUsers
- "Create a authorisedCardUser?" -> POST /paymentInstruments/{paymentInstrumentId}/authorisedCardUsers
- "List all settings?" -> GET /balancePlatforms/{balancePlatformId}/webhooks/{webhookId}/settings
- "Create a setting?" -> POST /balancePlatforms/{balancePlatformId}/webhooks/{webhookId}/settings
- "Get setting details?" -> GET /balancePlatforms/{balancePlatformId}/webhooks/{webhookId}/settings/{settingId}
- "Delete a setting?" -> DELETE /balancePlatforms/{balancePlatformId}/webhooks/{webhookId}/settings/{settingId}
- "Partially update a setting?" -> PATCH /balancePlatforms/{balancePlatformId}/webhooks/{webhookId}/settings/{settingId}
- "List all scaAssociations?" -> GET /scaAssociations
- "Create a scaDevice?" -> POST /scaDevices
- "Partially update a scaDevice?" -> PATCH /scaDevices/{deviceId}
- "Create a scaAssociation?" -> POST /scaDevices/{deviceId}/scaAssociations
- "List all taxFormSummary?" -> GET /accountHolders/{id}/taxFormSummary
- "Create a approve?" -> POST /balanceAccounts/{id}/transferLimits/approve
- "List all transferLimits?" -> GET /balanceAccounts/{id}/transferLimits
- "Create a transferLimit?" -> POST /balanceAccounts/{id}/transferLimits
- "List all current?" -> GET /balanceAccounts/{id}/transferLimits/current
- "Get transferLimit details?" -> GET /balanceAccounts/{id}/transferLimits/{transferLimitId}
- "Delete a transferLimit?" -> DELETE /balanceAccounts/{id}/transferLimits/{transferLimitId}
- "List all transferLimits?" -> GET /balancePlatforms/{id}/transferLimits
- "Create a transferLimit?" -> POST /balancePlatforms/{id}/transferLimits
- "Get transferLimit details?" -> GET /balancePlatforms/{id}/transferLimits/{transferLimitId}
- "Delete a transferLimit?" -> DELETE /balancePlatforms/{id}/transferLimits/{transferLimitId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
