---
name: aws-marketplace-entitlement-service
description: "AWS Marketplace Entitlement Service API skill. Use when working with AWS Marketplace Entitlement Service for root. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# AWS Marketplace Entitlement Service
API version: 2017-01-11

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | GetEntitlements retrieves entitlement values for a given product. The results can be filtered based on customer identifier or product dimensions. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
