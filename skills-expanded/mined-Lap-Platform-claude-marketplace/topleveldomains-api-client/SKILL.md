---
name: topleveldomains-api-client
description: "TopLevelDomains API Client API skill. Use when working with TopLevelDomains API Client for subscriptions. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# TopLevelDomains API Client
API version: 2018-02-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /subscriptions/{subscriptionId}/providers/Microsoft.DomainRegistration/topLevelDomains -- verify access
3. POST /subscriptions/{subscriptionId}/providers/Microsoft.DomainRegistration/topLevelDomains/{name}/listAgreements -- create first listAgreements

## Endpoints

3 endpoints across 1 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.DomainRegistration/topLevelDomains | Get all top-level domains supported for registration. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.DomainRegistration/topLevelDomains/{name} | Get details of a top-level domain. |
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.DomainRegistration/topLevelDomains/{name}/listAgreements | Gets all legal agreements that user needs to accept before purchasing a domain. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all topLevelDomains?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.DomainRegistration/topLevelDomains
- "Get topLevelDomain details?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.DomainRegistration/topLevelDomains/{name}
- "Create a listAgreement?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.DomainRegistration/topLevelDomains/{name}/listAgreements
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
