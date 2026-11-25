---
name: customer-lockbox
description: "Customer Lockbox API skill. Use when working with Customer Lockbox for providers, subscriptions. Covers 7 endpoints."
version: 1.0.0
generator: lapsh
---

# Customer Lockbox
API version: 2018-02-28-preview

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.CustomerLockbox/operations -- verify access
3. POST /providers/Microsoft.CustomerLockbox/enableLockbox -- create first enableLockbox

## Endpoints

7 endpoints across 2 groups. See references/api-spec.lap for full details.

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.CustomerLockbox/operations | Lists all the available REST API operations. |
| GET | /providers/Microsoft.CustomerLockbox/tenantOptedIn/{tenantId} | Get Customer Lockbox request |
| POST | /providers/Microsoft.CustomerLockbox/enableLockbox | Enable Tenant for Lockbox |
| POST | /providers/Microsoft.CustomerLockbox/disableLockbox | Disable Tenant for Lockbox |

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.CustomerLockbox/requests/{requestId} | Get Customer Lockbox request |
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.CustomerLockbox/requests/{requestId}/updateApproval | Update Customer Lockbox request approval status API |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.CustomerLockbox/requests | Lists all of the Lockbox requests in the given subscription. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all operations?" -> GET /providers/Microsoft.CustomerLockbox/operations
- "Get tenantOptedIn details?" -> GET /providers/Microsoft.CustomerLockbox/tenantOptedIn/{tenantId}
- "Create a enableLockbox?" -> POST /providers/Microsoft.CustomerLockbox/enableLockbox
- "Create a disableLockbox?" -> POST /providers/Microsoft.CustomerLockbox/disableLockbox
- "Get request details?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.CustomerLockbox/requests/{requestId}
- "Create a updateApproval?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.CustomerLockbox/requests/{requestId}/updateApproval
- "List all requests?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.CustomerLockbox/requests
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
