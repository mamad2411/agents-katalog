---
name: identity-api
description: "Identity API skill. Use when working with Identity for track#create-identity, track#identity-create-alias, import. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# Identity API
API version: 1.0.0

## Auth
No authentication required.

## Base URL
https://api.mixpanel.com

## Setup
1. No auth setup needed
3. POST /track#create-identity -- create first track#create-identity

## Endpoints

3 endpoints across 3 groups. See references/api-spec.lap for full details.

### track#create-identity
| Method | Path | Description |
|--------|------|-------------|
| POST | /track#create-identity | Create Identity |

### track#identity-create-alias
| Method | Path | Description |
|--------|------|-------------|
| POST | /track#identity-create-alias | Create Alias |

### import
| Method | Path | Description |
|--------|------|-------------|
| POST | /import | Merge Identities |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a track#create-identity?" -> POST /track#create-identity
- "Create a track#identity-create-alia?" -> POST /track#identity-create-alias
- "Create a import?" -> POST /import

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
