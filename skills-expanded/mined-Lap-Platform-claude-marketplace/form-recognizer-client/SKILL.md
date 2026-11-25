---
name: form-recognizer-client
description: "Form Recognizer Client API skill. Use when working with Form Recognizer Client for custom, prebuilt, layout. Covers 12 endpoints."
version: 1.0.0
generator: lapsh
---

# Form Recognizer Client
API version: 2.0-preview

## Auth
ApiKey Ocp-Apim-Subscription-Key in header

## Base URL
Not specified.

## Setup
1. Set your API key in the appropriate header
2. GET /custom/models/{modelId} -- verify access
3. POST /custom/models -- create first models

## Endpoints

12 endpoints across 3 groups. See references/api-spec.lap for full details.

### custom
| Method | Path | Description |
|--------|------|-------------|
| POST | /custom/models | Train Custom Model |
| GET | /custom/models/{modelId} | Get Custom Model |
| DELETE | /custom/models/{modelId} | Delete Custom Model |
| POST | /custom/models/{modelId}/analyze | Analyze Form |
| GET | /custom/models/{modelId}/analyzeResults/{resultId} | Get Analyze Form Result |
| POST | /custom/models/{modelId}/copy | Copy Custom Model |
| GET | /custom/models/{modelId}/copyResults/{resultId} | Get Custom Model Copy Result |
| POST | /custom/models/copyAuthorization | Generate Copy Authorization |

### prebuilt
| Method | Path | Description |
|--------|------|-------------|
| POST | /prebuilt/receipt/analyze | Analyze Receipt |
| GET | /prebuilt/receipt/analyzeResults/{resultId} | Get Analyze Receipt Result |

### layout
| Method | Path | Description |
|--------|------|-------------|
| POST | /layout/analyze | Analyze Layout |
| GET | /layout/analyzeResults/{resultId} | Get Analyze Layout Result |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a model?" -> POST /custom/models
- "Get model details?" -> GET /custom/models/{modelId}
- "Delete a model?" -> DELETE /custom/models/{modelId}
- "Create a analyze?" -> POST /custom/models/{modelId}/analyze
- "Get analyzeResult details?" -> GET /custom/models/{modelId}/analyzeResults/{resultId}
- "Create a copy?" -> POST /custom/models/{modelId}/copy
- "Get copyResult details?" -> GET /custom/models/{modelId}/copyResults/{resultId}
- "Create a copyAuthorization?" -> POST /custom/models/copyAuthorization
- "Create a analyze?" -> POST /prebuilt/receipt/analyze
- "Get analyzeResult details?" -> GET /prebuilt/receipt/analyzeResults/{resultId}
- "Create a analyze?" -> POST /layout/analyze
- "Get analyzeResult details?" -> GET /layout/analyzeResults/{resultId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
