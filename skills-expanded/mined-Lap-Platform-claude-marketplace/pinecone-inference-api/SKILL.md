---
name: pinecone-inference-api
description: "Pinecone Inference API skill. Use when working with Pinecone Inference for embed, rerank, models. Covers 4 endpoints."
version: 1.0.0
generator: lapsh
---

# Pinecone Inference API
API version: 2025-10

## Auth
ApiKey Api-Key in header

## Base URL
https://api.pinecone.io

## Setup
1. Set your API key in the appropriate header
2. GET /models -- verify access
3. POST /embed -- create first embed

## Endpoints

4 endpoints across 3 groups. See references/api-spec.lap for full details.

### embed
| Method | Path | Description |
|--------|------|-------------|
| POST | /embed | Generate vectors |

### rerank
| Method | Path | Description |
|--------|------|-------------|
| POST | /rerank | Rerank results |

### models
| Method | Path | Description |
|--------|------|-------------|
| GET | /models | List available models |
| GET | /models/{model_name} | Describe a model |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a embed?" -> POST /embed
- "Create a rerank?" -> POST /rerank
- "List all models?" -> GET /models
- "Get model details?" -> GET /models/{model_name}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
