---
name: text-generation-inference
description: "Text Generation Inference API skill. Use when working with Text Generation Inference for root, chat_tokenize, generate. Covers 12 endpoints."
version: 1.0.0
generator: lapsh
---

# Text Generation Inference
API version: 3.3.6-dev0

## Auth
No authentication required.

## Base URL
Not specified.

## Setup
1. No auth setup needed
2. GET /health -- verify access
3. POST / -- create first resource

## Endpoints

12 endpoints across 12 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Generate tokens if `stream == false` or a stream of token if `stream == true` |

### chat_tokenize
| Method | Path | Description |
|--------|------|-------------|
| POST | /chat_tokenize | Template and tokenize ChatRequest |

### generate
| Method | Path | Description |
|--------|------|-------------|
| POST | /generate | Generate tokens |

### generate_stream
| Method | Path | Description |
|--------|------|-------------|
| POST | /generate_stream | Generate a stream of token using Server-Sent Events |

### health
| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Health check method |

### info
| Method | Path | Description |
|--------|------|-------------|
| GET | /info | Text Generation Inference endpoint info |

### invocations
| Method | Path | Description |
|--------|------|-------------|
| POST | /invocations | Generate tokens from Sagemaker request |

### metrics
| Method | Path | Description |
|--------|------|-------------|
| GET | /metrics | Prometheus metrics scrape endpoint |

### tokenize
| Method | Path | Description |
|--------|------|-------------|
| POST | /tokenize | Tokenize inputs |

### chat
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/chat/completions | Generate tokens |

### completions
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/completions | Generate tokens |

### models
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/models | Get model info |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a chat_tokenize?" -> POST /chat_tokenize
- "Create a generate?" -> POST /generate
- "Create a generate_stream?" -> POST /generate_stream
- "List all health?" -> GET /health
- "List all info?" -> GET /info
- "Create a invocation?" -> POST /invocations
- "List all metrics?" -> GET /metrics
- "Create a tokenize?" -> POST /tokenize
- "Create a completion?" -> POST /v1/chat/completions
- "Create a completion?" -> POST /v1/completions
- "List all models?" -> GET /v1/models

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
