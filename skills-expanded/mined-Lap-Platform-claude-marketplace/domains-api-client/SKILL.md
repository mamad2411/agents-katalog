---
name: domains-api-client
description: "Domains API Client API skill. Use when working with Domains API Client for subscriptions. Covers 15 endpoints."
version: 1.0.0
generator: lapsh
---

# Domains API Client
API version: 2018-02-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /subscriptions/{subscriptionId}/providers/Microsoft.DomainRegistration/domains -- verify access
3. POST /subscriptions/{subscriptionId}/providers/Microsoft.DomainRegistration/checkDomainAvailability -- create first checkDomainAvailability

## Endpoints

15 endpoints across 1 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.DomainRegistration/checkDomainAvailability | Check if a domain is available for registration. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.DomainRegistration/domains | Get all domains in a subscription. |
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.DomainRegistration/generateSsoRequest | Generate a single sign-on request for the domain management portal. |
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.DomainRegistration/listDomainRecommendations | Get domain name recommendations based on keywords. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DomainRegistration/domains | Get all domains in a resource group. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DomainRegistration/domains/{domainName} | Get a domain. |
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DomainRegistration/domains/{domainName} | Creates or updates a domain. |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DomainRegistration/domains/{domainName} | Delete a domain. |
| PATCH | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DomainRegistration/domains/{domainName} | Creates or updates a domain. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DomainRegistration/domains/{domainName}/domainOwnershipIdentifiers | Lists domain ownership identifiers. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DomainRegistration/domains/{domainName}/domainOwnershipIdentifiers/{name} | Get ownership identifier for domain |
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DomainRegistration/domains/{domainName}/domainOwnershipIdentifiers/{name} | Creates an ownership identifier for a domain or updates identifier details for an existing identifier |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DomainRegistration/domains/{domainName}/domainOwnershipIdentifiers/{name} | Delete ownership identifier for domain |
| PATCH | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DomainRegistration/domains/{domainName}/domainOwnershipIdentifiers/{name} | Creates an ownership identifier for a domain or updates identifier details for an existing identifier |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DomainRegistration/domains/{domainName}/renew | Renew a domain. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a checkDomainAvailability?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.DomainRegistration/checkDomainAvailability
- "List all domains?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.DomainRegistration/domains
- "Create a generateSsoRequest?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.DomainRegistration/generateSsoRequest
- "Create a listDomainRecommendation?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.DomainRegistration/listDomainRecommendations
- "List all domains?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DomainRegistration/domains
- "Get domain details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DomainRegistration/domains/{domainName}
- "Update a domain?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DomainRegistration/domains/{domainName}
- "Delete a domain?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DomainRegistration/domains/{domainName}
- "Partially update a domain?" -> PATCH /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DomainRegistration/domains/{domainName}
- "List all domainOwnershipIdentifiers?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DomainRegistration/domains/{domainName}/domainOwnershipIdentifiers
- "Get domainOwnershipIdentifier details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DomainRegistration/domains/{domainName}/domainOwnershipIdentifiers/{name}
- "Update a domainOwnershipIdentifier?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DomainRegistration/domains/{domainName}/domainOwnershipIdentifiers/{name}
- "Delete a domainOwnershipIdentifier?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DomainRegistration/domains/{domainName}/domainOwnershipIdentifiers/{name}
- "Partially update a domainOwnershipIdentifier?" -> PATCH /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DomainRegistration/domains/{domainName}/domainOwnershipIdentifiers/{name}
- "Create a renew?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DomainRegistration/domains/{domainName}/renew
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
