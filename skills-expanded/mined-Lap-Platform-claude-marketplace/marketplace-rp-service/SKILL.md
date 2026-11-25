---
name: marketplace-rp-service
description: "Marketplace RP Service API skill. Use when working with Marketplace RP Service for providers, subscriptions. Covers 13 endpoints."
version: 1.0.0
generator: lapsh
---

# Marketplace RP Service
API version: 2020-01-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.Marketplace/privateStores -- verify access
3. POST /providers/Microsoft.Marketplace/privateStores/{privateStoreId}/offers/{offerId} -- create first offers

## Endpoints

13 endpoints across 2 groups. See references/api-spec.lap for full details.

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.Marketplace/privateStores/{privateStoreId}/offers | Get a list of all private offers in the given private store |
| DELETE | /providers/Microsoft.Marketplace/privateStores/{privateStoreId}/offers/{offerId} | Deletes an offer from the given private store. |
| GET | /providers/Microsoft.Marketplace/privateStores/{privateStoreId}/offers/{offerId} | Gets information about a specific offer. |
| PUT | /providers/Microsoft.Marketplace/privateStores/{privateStoreId}/offers/{offerId} | Update or add an offer to the default collection of the private store. |
| POST | /providers/Microsoft.Marketplace/privateStores/{privateStoreId}/offers/{offerId} | Delete Private store offer. This is a workaround. |
| GET | /providers/Microsoft.Marketplace/privateStores | Gets the list of available private stores |
| GET | /providers/Microsoft.Marketplace/privateStores/{privateStoreId} | Get information about the private store |
| DELETE | /providers/Microsoft.Marketplace/privateStores/{privateStoreId} | Deletes the private store. All that is not saved will be lost. |
| PUT | /providers/Microsoft.Marketplace/privateStores/{privateStoreId} | Changes private store properties |
| GET | /providers/Microsoft.Marketplace/operations | Lists all of the available Microsoft.Marketplace REST API operations. |

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Marketplace/privateStores/{privateStoreId}/offers | Get a list of all private offers in the given private store |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Marketplace/privateStores/{privateStoreId}/offers/{offerId} | Gets information about a specific private offer. |
| PUT | /subscriptions/{subscriptionId}/providers/Microsoft.Marketplace/privateStores/{privateStoreId}/offers/{offerId} | Update or add a private offer to the default collection of the private store. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all offers?" -> GET /providers/Microsoft.Marketplace/privateStores/{privateStoreId}/offers
- "List all offers?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Marketplace/privateStores/{privateStoreId}/offers
- "Delete a offer?" -> DELETE /providers/Microsoft.Marketplace/privateStores/{privateStoreId}/offers/{offerId}
- "Get offer details?" -> GET /providers/Microsoft.Marketplace/privateStores/{privateStoreId}/offers/{offerId}
- "Update a offer?" -> PUT /providers/Microsoft.Marketplace/privateStores/{privateStoreId}/offers/{offerId}
- "Get offer details?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Marketplace/privateStores/{privateStoreId}/offers/{offerId}
- "Update a offer?" -> PUT /subscriptions/{subscriptionId}/providers/Microsoft.Marketplace/privateStores/{privateStoreId}/offers/{offerId}
- "List all privateStores?" -> GET /providers/Microsoft.Marketplace/privateStores
- "Get privateStore details?" -> GET /providers/Microsoft.Marketplace/privateStores/{privateStoreId}
- "Delete a privateStore?" -> DELETE /providers/Microsoft.Marketplace/privateStores/{privateStoreId}
- "Update a privateStore?" -> PUT /providers/Microsoft.Marketplace/privateStores/{privateStoreId}
- "List all operations?" -> GET /providers/Microsoft.Marketplace/operations
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
