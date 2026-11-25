---
name: luis-runtime-client
description: "LUIS Runtime Client API skill. Use when working with LUIS Runtime Client for apps. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# LUIS Runtime Client
API version: 2.0

## Auth
ApiKey Ocp-Apim-Subscription-Key in header

## Base URL
Not specified.

## Setup
1. Set your API key in the appropriate header
2. GET /apps/{appId} -- verify access
3. POST /apps/{appId} -- create first apps

## Endpoints

2 endpoints across 1 groups. See references/api-spec.lap for full details.

### apps
| Method | Path | Description |
|--------|------|-------------|
| GET | /apps/{appId} | Gets predictions for a given utterance, in the form of intents and entities. The current maximum query size is 500 characters. |
| POST | /apps/{appId} | Gets predictions for a given utterance, in the form of intents and entities. The current maximum query size is 500 characters. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Search apps?" -> GET /apps/{appId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
