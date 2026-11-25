---
name: management-api
description: "Management API skill. Use when working with Management for companies, me, merchants. Covers 130 endpoints."
version: 1.0.0
generator: lapsh
---

# Management API
API version: 1

## Auth
ApiKey X-API-Key in header | Bearer basic

## Base URL
https://management-test.adyen.com/v1

## Setup
1. Set Authorization header with your Bearer token
2. GET /companies -- verify access
3. POST /companies/{companyId}/apiCredentials -- create first apiCredentials

## Endpoints

130 endpoints across 5 groups. See references/api-spec.lap for full details.

### companies
| Method | Path | Description |
|--------|------|-------------|
| GET | /companies | Get a list of company accounts |
| GET | /companies/{companyId} | Get a company account |
| GET | /companies/{companyId}/androidApps | Get a list of Android apps |
| GET | /companies/{companyId}/androidApps/{id} | Get Android app |
| GET | /companies/{companyId}/androidCertificates | Get a list of Android certificates |
| GET | /companies/{companyId}/apiCredentials | Get a list of API credentials |
| POST | /companies/{companyId}/apiCredentials | Create an API credential. |
| GET | /companies/{companyId}/apiCredentials/{apiCredentialId} | Get an API credential |
| PATCH | /companies/{companyId}/apiCredentials/{apiCredentialId} | Update an API credential. |
| GET | /companies/{companyId}/apiCredentials/{apiCredentialId}/allowedOrigins | Get a list of allowed origins |
| POST | /companies/{companyId}/apiCredentials/{apiCredentialId}/allowedOrigins | Create an allowed origin |
| DELETE | /companies/{companyId}/apiCredentials/{apiCredentialId}/allowedOrigins/{originId} | Delete an allowed origin |
| GET | /companies/{companyId}/apiCredentials/{apiCredentialId}/allowedOrigins/{originId} | Get an allowed origin |
| POST | /companies/{companyId}/apiCredentials/{apiCredentialId}/generateApiKey | Generate new API key |
| POST | /companies/{companyId}/apiCredentials/{apiCredentialId}/generateClientKey | Generate new client key |
| GET | /companies/{companyId}/billingEntities | Get a list of billing entities |
| GET | /companies/{companyId}/merchants | Get a list of merchant accounts |
| GET | /companies/{companyId}/shippingLocations | Get a list of shipping locations |
| POST | /companies/{companyId}/shippingLocations | Create a shipping location |
| GET | /companies/{companyId}/terminalActions | Get a list of terminal actions |
| GET | /companies/{companyId}/terminalActions/{actionId} | Get terminal action |
| GET | /companies/{companyId}/terminalLogos | Get the terminal logo |
| PATCH | /companies/{companyId}/terminalLogos | Update the terminal logo |
| GET | /companies/{companyId}/terminalModels | Get a list of terminal models |
| GET | /companies/{companyId}/terminalOrders | Get a list of orders |
| POST | /companies/{companyId}/terminalOrders | Create an order |
| GET | /companies/{companyId}/terminalOrders/{orderId} | Get an order |
| PATCH | /companies/{companyId}/terminalOrders/{orderId} | Update an order |
| POST | /companies/{companyId}/terminalOrders/{orderId}/cancel | Cancel an order |
| GET | /companies/{companyId}/terminalProducts | Get a list of terminal products |
| GET | /companies/{companyId}/terminalSettings | Get terminal settings |
| PATCH | /companies/{companyId}/terminalSettings | Update terminal settings |
| GET | /companies/{companyId}/users | Get a list of users |
| POST | /companies/{companyId}/users | Create a new user |
| GET | /companies/{companyId}/users/{userId} | Get user details |
| PATCH | /companies/{companyId}/users/{userId} | Update user details |
| GET | /companies/{companyId}/webhooks | List all webhooks |
| POST | /companies/{companyId}/webhooks | Set up a webhook |
| DELETE | /companies/{companyId}/webhooks/{webhookId} | Remove a webhook |
| GET | /companies/{companyId}/webhooks/{webhookId} | Get a webhook |
| PATCH | /companies/{companyId}/webhooks/{webhookId} | Update a webhook |
| POST | /companies/{companyId}/webhooks/{webhookId}/generateHmac | Generate an HMAC key |
| POST | /companies/{companyId}/webhooks/{webhookId}/test | Test a webhook |

### me
| Method | Path | Description |
|--------|------|-------------|
| GET | /me | Get API credential details |
| GET | /me/allowedOrigins | Get allowed origins |
| POST | /me/allowedOrigins | Add allowed origin |
| DELETE | /me/allowedOrigins/{originId} | Remove allowed origin |
| GET | /me/allowedOrigins/{originId} | Get allowed origin details |
| POST | /me/generateClientKey | Generate a client key |

### merchants
| Method | Path | Description |
|--------|------|-------------|
| GET | /merchants | Get a list of merchant accounts |
| POST | /merchants | Create a merchant account |
| GET | /merchants/{merchantId} | Get a merchant account |
| POST | /merchants/{merchantId}/activate | Request to activate a merchant account |
| GET | /merchants/{merchantId}/apiCredentials | Get a list of API credentials |
| POST | /merchants/{merchantId}/apiCredentials | Create an API credential |
| GET | /merchants/{merchantId}/apiCredentials/{apiCredentialId} | Get an API credential |
| PATCH | /merchants/{merchantId}/apiCredentials/{apiCredentialId} | Update an API credential |
| GET | /merchants/{merchantId}/apiCredentials/{apiCredentialId}/allowedOrigins | Get a list of allowed origins |
| POST | /merchants/{merchantId}/apiCredentials/{apiCredentialId}/allowedOrigins | Create an allowed origin |
| DELETE | /merchants/{merchantId}/apiCredentials/{apiCredentialId}/allowedOrigins/{originId} | Delete an allowed origin |
| GET | /merchants/{merchantId}/apiCredentials/{apiCredentialId}/allowedOrigins/{originId} | Get an allowed origin |
| POST | /merchants/{merchantId}/apiCredentials/{apiCredentialId}/generateApiKey | Generate new API key |
| POST | /merchants/{merchantId}/apiCredentials/{apiCredentialId}/generateClientKey | Generate new client key |
| GET | /merchants/{merchantId}/billingEntities | Get a list of billing entities |
| GET | /merchants/{merchantId}/paymentMethodSettings | Get all payment methods |
| POST | /merchants/{merchantId}/paymentMethodSettings | Request a payment method |
| GET | /merchants/{merchantId}/paymentMethodSettings/{paymentMethodId} | Get payment method details |
| PATCH | /merchants/{merchantId}/paymentMethodSettings/{paymentMethodId} | Update a payment method |
| POST | /merchants/{merchantId}/paymentMethodSettings/{paymentMethodId}/addApplePayDomains | Add an Apple Pay domain |
| GET | /merchants/{merchantId}/paymentMethodSettings/{paymentMethodId}/getApplePayDomains | Get Apple Pay domains |
| GET | /merchants/{merchantId}/payoutSettings | Get a list of payout settings |
| POST | /merchants/{merchantId}/payoutSettings | Add a payout setting |
| DELETE | /merchants/{merchantId}/payoutSettings/{payoutSettingsId} | Delete a payout setting |
| GET | /merchants/{merchantId}/payoutSettings/{payoutSettingsId} | Get a payout setting |
| PATCH | /merchants/{merchantId}/payoutSettings/{payoutSettingsId} | Update a payout setting |
| GET | /merchants/{merchantId}/shippingLocations | Get a list of shipping locations |
| POST | /merchants/{merchantId}/shippingLocations | Create a shipping location |
| GET | /merchants/{merchantId}/splitConfigurations | Get a list of split configuration profiles |
| POST | /merchants/{merchantId}/splitConfigurations | Create a split configuration profile |
| DELETE | /merchants/{merchantId}/splitConfigurations/{splitConfigurationId} | Delete a split configuration profile |
| GET | /merchants/{merchantId}/splitConfigurations/{splitConfigurationId} | Get a split configuration profile |
| PATCH | /merchants/{merchantId}/splitConfigurations/{splitConfigurationId} | Update the description of the split configuration profile |
| POST | /merchants/{merchantId}/splitConfigurations/{splitConfigurationId} | Create a rule |
| DELETE | /merchants/{merchantId}/splitConfigurations/{splitConfigurationId}/rules/{ruleId} | Delete a rule |
| PATCH | /merchants/{merchantId}/splitConfigurations/{splitConfigurationId}/rules/{ruleId} | Update the split conditions |
| PATCH | /merchants/{merchantId}/splitConfigurations/{splitConfigurationId}/rules/{ruleId}/splitLogic/{splitLogicId} | Update the split logic |
| GET | /merchants/{merchantId}/stores | Get a list of stores |
| POST | /merchants/{merchantId}/stores | Create a store |
| GET | /merchants/{merchantId}/stores/{reference}/terminalLogos | Get the terminal logo |
| PATCH | /merchants/{merchantId}/stores/{reference}/terminalLogos | Update the terminal logo |
| GET | /merchants/{merchantId}/stores/{reference}/terminalSettings | Get terminal settings |
| PATCH | /merchants/{merchantId}/stores/{reference}/terminalSettings | Update terminal settings |
| GET | /merchants/{merchantId}/stores/{storeId} | Get a store |
| PATCH | /merchants/{merchantId}/stores/{storeId} | Update a store |
| GET | /merchants/{merchantId}/terminalLogos | Get the terminal logo |
| PATCH | /merchants/{merchantId}/terminalLogos | Update the terminal logo |
| GET | /merchants/{merchantId}/terminalModels | Get a list of terminal models |
| GET | /merchants/{merchantId}/terminalOrders | Get a list of orders |
| POST | /merchants/{merchantId}/terminalOrders | Create an order |
| GET | /merchants/{merchantId}/terminalOrders/{orderId} | Get an order |
| PATCH | /merchants/{merchantId}/terminalOrders/{orderId} | Update an order |
| POST | /merchants/{merchantId}/terminalOrders/{orderId}/cancel | Cancel an order |
| GET | /merchants/{merchantId}/terminalProducts | Get a list of terminal products |
| GET | /merchants/{merchantId}/terminalSettings | Get terminal settings |
| PATCH | /merchants/{merchantId}/terminalSettings | Update terminal settings |
| GET | /merchants/{merchantId}/users | Get a list of users |
| POST | /merchants/{merchantId}/users | Create a new user |
| GET | /merchants/{merchantId}/users/{userId} | Get user details |
| PATCH | /merchants/{merchantId}/users/{userId} | Update a user |
| GET | /merchants/{merchantId}/webhooks | List all webhooks |
| POST | /merchants/{merchantId}/webhooks | Set up a webhook |
| DELETE | /merchants/{merchantId}/webhooks/{webhookId} | Remove a webhook |
| GET | /merchants/{merchantId}/webhooks/{webhookId} | Get a webhook |
| PATCH | /merchants/{merchantId}/webhooks/{webhookId} | Update a webhook |
| POST | /merchants/{merchantId}/webhooks/{webhookId}/generateHmac | Generate an HMAC key |
| POST | /merchants/{merchantId}/webhooks/{webhookId}/test | Test a webhook |

### stores
| Method | Path | Description |
|--------|------|-------------|
| GET | /stores | Get a list of stores |
| POST | /stores | Create a store |
| GET | /stores/{storeId} | Get a store |
| PATCH | /stores/{storeId} | Update a store |
| GET | /stores/{storeId}/terminalLogos | Get the terminal logo |
| PATCH | /stores/{storeId}/terminalLogos | Update the terminal logo |
| GET | /stores/{storeId}/terminalSettings | Get terminal settings |
| PATCH | /stores/{storeId}/terminalSettings | Update terminal settings |

### terminals
| Method | Path | Description |
|--------|------|-------------|
| GET | /terminals | Get a list of terminals |
| POST | /terminals/scheduleActions | Create a terminal action |
| GET | /terminals/{terminalId}/terminalLogos | Get the terminal logo |
| PATCH | /terminals/{terminalId}/terminalLogos | Update the logo |
| GET | /terminals/{terminalId}/terminalSettings | Get terminal settings |
| PATCH | /terminals/{terminalId}/terminalSettings | Update terminal settings |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all companies?" -> GET /companies
- "Get company details?" -> GET /companies/{companyId}
- "List all androidApps?" -> GET /companies/{companyId}/androidApps
- "Get androidApp details?" -> GET /companies/{companyId}/androidApps/{id}
- "List all androidCertificates?" -> GET /companies/{companyId}/androidCertificates
- "List all apiCredentials?" -> GET /companies/{companyId}/apiCredentials
- "Create a apiCredential?" -> POST /companies/{companyId}/apiCredentials
- "Get apiCredential details?" -> GET /companies/{companyId}/apiCredentials/{apiCredentialId}
- "Partially update a apiCredential?" -> PATCH /companies/{companyId}/apiCredentials/{apiCredentialId}
- "List all allowedOrigins?" -> GET /companies/{companyId}/apiCredentials/{apiCredentialId}/allowedOrigins
- "Create a allowedOrigin?" -> POST /companies/{companyId}/apiCredentials/{apiCredentialId}/allowedOrigins
- "Delete a allowedOrigin?" -> DELETE /companies/{companyId}/apiCredentials/{apiCredentialId}/allowedOrigins/{originId}
- "Get allowedOrigin details?" -> GET /companies/{companyId}/apiCredentials/{apiCredentialId}/allowedOrigins/{originId}
- "Create a generateApiKey?" -> POST /companies/{companyId}/apiCredentials/{apiCredentialId}/generateApiKey
- "Create a generateClientKey?" -> POST /companies/{companyId}/apiCredentials/{apiCredentialId}/generateClientKey
- "List all billingEntities?" -> GET /companies/{companyId}/billingEntities
- "List all merchants?" -> GET /companies/{companyId}/merchants
- "List all shippingLocations?" -> GET /companies/{companyId}/shippingLocations
- "Create a shippingLocation?" -> POST /companies/{companyId}/shippingLocations
- "List all terminalActions?" -> GET /companies/{companyId}/terminalActions
- "Get terminalAction details?" -> GET /companies/{companyId}/terminalActions/{actionId}
- "List all terminalLogos?" -> GET /companies/{companyId}/terminalLogos
- "List all terminalModels?" -> GET /companies/{companyId}/terminalModels
- "List all terminalOrders?" -> GET /companies/{companyId}/terminalOrders
- "Create a terminalOrder?" -> POST /companies/{companyId}/terminalOrders
- "Get terminalOrder details?" -> GET /companies/{companyId}/terminalOrders/{orderId}
- "Partially update a terminalOrder?" -> PATCH /companies/{companyId}/terminalOrders/{orderId}
- "Create a cancel?" -> POST /companies/{companyId}/terminalOrders/{orderId}/cancel
- "List all terminalProducts?" -> GET /companies/{companyId}/terminalProducts
- "List all terminalSettings?" -> GET /companies/{companyId}/terminalSettings
- "List all users?" -> GET /companies/{companyId}/users
- "Create a user?" -> POST /companies/{companyId}/users
- "Get user details?" -> GET /companies/{companyId}/users/{userId}
- "Partially update a user?" -> PATCH /companies/{companyId}/users/{userId}
- "List all webhooks?" -> GET /companies/{companyId}/webhooks
- "Create a webhook?" -> POST /companies/{companyId}/webhooks
- "Delete a webhook?" -> DELETE /companies/{companyId}/webhooks/{webhookId}
- "Get webhook details?" -> GET /companies/{companyId}/webhooks/{webhookId}
- "Partially update a webhook?" -> PATCH /companies/{companyId}/webhooks/{webhookId}
- "Create a generateHmac?" -> POST /companies/{companyId}/webhooks/{webhookId}/generateHmac
- "Create a test?" -> POST /companies/{companyId}/webhooks/{webhookId}/test
- "List all me?" -> GET /me
- "List all allowedOrigins?" -> GET /me/allowedOrigins
- "Create a allowedOrigin?" -> POST /me/allowedOrigins
- "Delete a allowedOrigin?" -> DELETE /me/allowedOrigins/{originId}
- "Get allowedOrigin details?" -> GET /me/allowedOrigins/{originId}
- "Create a generateClientKey?" -> POST /me/generateClientKey
- "List all merchants?" -> GET /merchants
- "Create a merchant?" -> POST /merchants
- "Get merchant details?" -> GET /merchants/{merchantId}
- "Create a activate?" -> POST /merchants/{merchantId}/activate
- "List all apiCredentials?" -> GET /merchants/{merchantId}/apiCredentials
- "Create a apiCredential?" -> POST /merchants/{merchantId}/apiCredentials
- "Get apiCredential details?" -> GET /merchants/{merchantId}/apiCredentials/{apiCredentialId}
- "Partially update a apiCredential?" -> PATCH /merchants/{merchantId}/apiCredentials/{apiCredentialId}
- "List all allowedOrigins?" -> GET /merchants/{merchantId}/apiCredentials/{apiCredentialId}/allowedOrigins
- "Create a allowedOrigin?" -> POST /merchants/{merchantId}/apiCredentials/{apiCredentialId}/allowedOrigins
- "Delete a allowedOrigin?" -> DELETE /merchants/{merchantId}/apiCredentials/{apiCredentialId}/allowedOrigins/{originId}
- "Get allowedOrigin details?" -> GET /merchants/{merchantId}/apiCredentials/{apiCredentialId}/allowedOrigins/{originId}
- "Create a generateApiKey?" -> POST /merchants/{merchantId}/apiCredentials/{apiCredentialId}/generateApiKey
- "Create a generateClientKey?" -> POST /merchants/{merchantId}/apiCredentials/{apiCredentialId}/generateClientKey
- "List all billingEntities?" -> GET /merchants/{merchantId}/billingEntities
- "List all paymentMethodSettings?" -> GET /merchants/{merchantId}/paymentMethodSettings
- "Create a paymentMethodSetting?" -> POST /merchants/{merchantId}/paymentMethodSettings
- "Get paymentMethodSetting details?" -> GET /merchants/{merchantId}/paymentMethodSettings/{paymentMethodId}
- "Partially update a paymentMethodSetting?" -> PATCH /merchants/{merchantId}/paymentMethodSettings/{paymentMethodId}
- "Create a addApplePayDomain?" -> POST /merchants/{merchantId}/paymentMethodSettings/{paymentMethodId}/addApplePayDomains
- "List all getApplePayDomains?" -> GET /merchants/{merchantId}/paymentMethodSettings/{paymentMethodId}/getApplePayDomains
- "List all payoutSettings?" -> GET /merchants/{merchantId}/payoutSettings
- "Create a payoutSetting?" -> POST /merchants/{merchantId}/payoutSettings
- "Delete a payoutSetting?" -> DELETE /merchants/{merchantId}/payoutSettings/{payoutSettingsId}
- "Get payoutSetting details?" -> GET /merchants/{merchantId}/payoutSettings/{payoutSettingsId}
- "Partially update a payoutSetting?" -> PATCH /merchants/{merchantId}/payoutSettings/{payoutSettingsId}
- "List all shippingLocations?" -> GET /merchants/{merchantId}/shippingLocations
- "Create a shippingLocation?" -> POST /merchants/{merchantId}/shippingLocations
- "List all splitConfigurations?" -> GET /merchants/{merchantId}/splitConfigurations
- "Create a splitConfiguration?" -> POST /merchants/{merchantId}/splitConfigurations
- "Delete a splitConfiguration?" -> DELETE /merchants/{merchantId}/splitConfigurations/{splitConfigurationId}
- "Get splitConfiguration details?" -> GET /merchants/{merchantId}/splitConfigurations/{splitConfigurationId}
- "Partially update a splitConfiguration?" -> PATCH /merchants/{merchantId}/splitConfigurations/{splitConfigurationId}
- "Delete a rule?" -> DELETE /merchants/{merchantId}/splitConfigurations/{splitConfigurationId}/rules/{ruleId}
- "Partially update a rule?" -> PATCH /merchants/{merchantId}/splitConfigurations/{splitConfigurationId}/rules/{ruleId}
- "Partially update a splitLogic?" -> PATCH /merchants/{merchantId}/splitConfigurations/{splitConfigurationId}/rules/{ruleId}/splitLogic/{splitLogicId}
- "List all stores?" -> GET /merchants/{merchantId}/stores
- "Create a store?" -> POST /merchants/{merchantId}/stores
- "List all terminalLogos?" -> GET /merchants/{merchantId}/stores/{reference}/terminalLogos
- "List all terminalSettings?" -> GET /merchants/{merchantId}/stores/{reference}/terminalSettings
- "Get store details?" -> GET /merchants/{merchantId}/stores/{storeId}
- "Partially update a store?" -> PATCH /merchants/{merchantId}/stores/{storeId}
- "List all terminalLogos?" -> GET /merchants/{merchantId}/terminalLogos
- "List all terminalModels?" -> GET /merchants/{merchantId}/terminalModels
- "List all terminalOrders?" -> GET /merchants/{merchantId}/terminalOrders
- "Create a terminalOrder?" -> POST /merchants/{merchantId}/terminalOrders
- "Get terminalOrder details?" -> GET /merchants/{merchantId}/terminalOrders/{orderId}
- "Partially update a terminalOrder?" -> PATCH /merchants/{merchantId}/terminalOrders/{orderId}
- "Create a cancel?" -> POST /merchants/{merchantId}/terminalOrders/{orderId}/cancel
- "List all terminalProducts?" -> GET /merchants/{merchantId}/terminalProducts
- "List all terminalSettings?" -> GET /merchants/{merchantId}/terminalSettings
- "List all users?" -> GET /merchants/{merchantId}/users
- "Create a user?" -> POST /merchants/{merchantId}/users
- "Get user details?" -> GET /merchants/{merchantId}/users/{userId}
- "Partially update a user?" -> PATCH /merchants/{merchantId}/users/{userId}
- "List all webhooks?" -> GET /merchants/{merchantId}/webhooks
- "Create a webhook?" -> POST /merchants/{merchantId}/webhooks
- "Delete a webhook?" -> DELETE /merchants/{merchantId}/webhooks/{webhookId}
- "Get webhook details?" -> GET /merchants/{merchantId}/webhooks/{webhookId}
- "Partially update a webhook?" -> PATCH /merchants/{merchantId}/webhooks/{webhookId}
- "Create a generateHmac?" -> POST /merchants/{merchantId}/webhooks/{webhookId}/generateHmac
- "Create a test?" -> POST /merchants/{merchantId}/webhooks/{webhookId}/test
- "List all stores?" -> GET /stores
- "Create a store?" -> POST /stores
- "Get store details?" -> GET /stores/{storeId}
- "Partially update a store?" -> PATCH /stores/{storeId}
- "List all terminalLogos?" -> GET /stores/{storeId}/terminalLogos
- "List all terminalSettings?" -> GET /stores/{storeId}/terminalSettings
- "List all terminals?" -> GET /terminals
- "Create a scheduleAction?" -> POST /terminals/scheduleActions
- "List all terminalLogos?" -> GET /terminals/{terminalId}/terminalLogos
- "List all terminalSettings?" -> GET /terminals/{terminalId}/terminalSettings
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
