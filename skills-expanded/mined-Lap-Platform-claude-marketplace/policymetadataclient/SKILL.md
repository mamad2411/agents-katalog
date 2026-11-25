---
name: policymetadataclient
description: "PolicyMetadataClient API skill. Use when working with PolicyMetadataClient for providers. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# PolicyMetadataClient
API version: 2019-10-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.PolicyInsights/policyMetadata -- verify access

## Endpoints

2 endpoints across 1 groups. See references/api-spec.lap for full details.

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.PolicyInsights/policyMetadata/{resourceName} | Get policy metadata resource. |
| GET | /providers/Microsoft.PolicyInsights/policyMetadata | Get a list of the policy metadata resources. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get policyMetadata details?" -> GET /providers/Microsoft.PolicyInsights/policyMetadata/{resourceName}
- "List all policyMetadata?" -> GET /providers/Microsoft.PolicyInsights/policyMetadata
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
