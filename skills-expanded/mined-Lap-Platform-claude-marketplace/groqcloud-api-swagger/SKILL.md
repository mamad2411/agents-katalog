---
name: groqcloud-api-swagger
description: "GroqCloud API Swagger API skill. Use when working with GroqCloud API Swagger for openai. Covers 7 endpoints."
version: 1.0.0
generator: lapsh
---

# GroqCloud API Swagger
API version: 2.0

## Auth
Bearer bearer

## Base URL
https://api.groq.com

## Setup
1. Set Authorization header with your Bearer token
2. GET /openai/v1/models -- verify access
3. POST /openai/v1/audio/transcriptions -- create first transcriptions

## Endpoints

7 endpoints across 1 groups. See references/api-spec.lap for full details.

### openai
| Method | Path | Description |
|--------|------|-------------|
| POST | /openai/v1/audio/transcriptions | Transcribes audio into the input language. |
| POST | /openai/v1/audio/translations | Translates audio into English. |
| POST | /openai/v1/chat/completions | Creates a model response for the given chat conversation. |
| POST | /openai/v1/embeddings | Creates an embedding vector representing the input text. |
| GET | /openai/v1/models | List models |
| DELETE | /openai/v1/models/{model} | Delete model |
| GET | /openai/v1/models/{model} | Get model |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a transcription?" -> POST /openai/v1/audio/transcriptions
- "Create a translation?" -> POST /openai/v1/audio/translations
- "Create a completion?" -> POST /openai/v1/chat/completions
- "Create a embedding?" -> POST /openai/v1/embeddings
- "List all models?" -> GET /openai/v1/models
- "Delete a model?" -> DELETE /openai/v1/models/{model}
- "Get model details?" -> GET /openai/v1/models/{model}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
