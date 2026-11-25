---
name: aws-migration-hub-config
description: "AWS Migration Hub Config API skill. Use when working with AWS Migration Hub Config for root. Covers 4 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Migration Hub Config
API version: 2019-06-30

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

4 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | This API sets up the home region for the calling account only. |
| POST | / | This operation deletes the home region configuration for the calling account. The operation does not delete discovery or migration tracking data in the home region. |
| POST | / | This API permits filtering on the ControlId and HomeRegion fields. |
| POST | / | Returns the calling account’s home region, if configured. This API is used by other AWS services to determine the regional endpoint for calling AWS Application Discovery Service and Migration Hub. You must call GetHomeRegion at least once before you call any other AWS Application Discovery Service and AWS Migration Hub APIs, to obtain the account's Migration Hub home region. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
