---
name: software-plan-rp
description: "Software Plan RP API skill. Use when working with Software Plan RP for subscriptions, {scope}. Covers 8 endpoints."
version: 1.0.0
generator: lapsh
---

# Software Plan RP
API version: 2019-12-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /{scope}/providers/Microsoft.SoftwarePlan/hybridUseBenefits -- verify access
3. POST /subscriptions/{subscriptionId}/providers/Microsoft.SoftwarePlan/register -- create first register

## Endpoints

8 endpoints across 2 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.SoftwarePlan/register | Register to Microsoft.SoftwarePlan resource provider. |

### {scope}
| Method | Path | Description |
|--------|------|-------------|
| GET | /{scope}/providers/Microsoft.SoftwarePlan/hybridUseBenefits | Get all hybrid use benefits associated with an ARM resource. |
| PUT | /{scope}/providers/Microsoft.SoftwarePlan/hybridUseBenefits/{planId} | Create a new hybrid use benefit under a given scope |
| PATCH | /{scope}/providers/Microsoft.SoftwarePlan/hybridUseBenefits/{planId} | Updates an existing hybrid use benefit |
| GET | /{scope}/providers/Microsoft.SoftwarePlan/hybridUseBenefits/{planId} | Gets a given plan ID |
| DELETE | /{scope}/providers/Microsoft.SoftwarePlan/hybridUseBenefits/{planId} | Deletes a given plan ID |
| GET | /{scope}/providers/Microsoft.SoftwarePlan/hybridUseBenefits/{planId}/revisions | Gets the version history of a hybrid use benefit |
| GET | /{scope}/providers/Microsoft.SoftwarePlan/operations | Get operations. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a register?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.SoftwarePlan/register
- "List all hybridUseBenefits?" -> GET /{scope}/providers/Microsoft.SoftwarePlan/hybridUseBenefits
- "Update a hybridUseBenefit?" -> PUT /{scope}/providers/Microsoft.SoftwarePlan/hybridUseBenefits/{planId}
- "Partially update a hybridUseBenefit?" -> PATCH /{scope}/providers/Microsoft.SoftwarePlan/hybridUseBenefits/{planId}
- "Get hybridUseBenefit details?" -> GET /{scope}/providers/Microsoft.SoftwarePlan/hybridUseBenefits/{planId}
- "Delete a hybridUseBenefit?" -> DELETE /{scope}/providers/Microsoft.SoftwarePlan/hybridUseBenefits/{planId}
- "List all revisions?" -> GET /{scope}/providers/Microsoft.SoftwarePlan/hybridUseBenefits/{planId}/revisions
- "List all operations?" -> GET /{scope}/providers/Microsoft.SoftwarePlan/operations
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
