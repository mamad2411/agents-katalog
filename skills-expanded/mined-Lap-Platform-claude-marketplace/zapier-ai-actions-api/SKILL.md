---
name: zapier-ai-actions-api
description: "Zapier AI Actions API skill. Use when working with Zapier AI Actions for api. Covers 5 endpoints."
version: 1.0.0
generator: lapsh
---

# Zapier AI Actions API
API version: main_api_v1

## Auth
ApiKey x-api-key in header | ApiKey api_key in query | OAuth2 | ApiKey nlasession in cookie

## Base URL
https://actions.zapier.com

## Setup
1. Set your API key in the appropriate header
2. GET /api/v1/check/ -- verify access
3. POST /api/v1/exposed/{exposed_app_action_id}/execute/ -- create first execute

## Endpoints

5 endpoints across 1 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/v1/check/ | Check |
| GET | /api/v1/configuration-link/ | Get Configuration Link |
| GET | /api/v1/exposed/ | List Exposed Actions |
| POST | /api/v1/exposed/{exposed_app_action_id}/execute/ | Execute App Action Endpoint |
| GET | /api/v1/execution-log/{execution_log_id}/ | Get Execution Log Endpoint |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all check?" -> GET /api/v1/check/
- "List all configuration-link?" -> GET /api/v1/configuration-link/
- "List all exposed?" -> GET /api/v1/exposed/
- "Create a execute?" -> POST /api/v1/exposed/{exposed_app_action_id}/execute/
- "Get execution-log details?" -> GET /api/v1/execution-log/{execution_log_id}/
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
