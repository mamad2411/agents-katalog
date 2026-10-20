---
name: Multi-Provider LLM
description: Configuração multi-provider — OpenAI, Z.ai, OpenRouter, Gemini e fallback local. Uma config serve tudo. Como trocar provider, models disponíveis, e env vars.
---

# Multi-Provider LLM

## Quando Usar

- Ao configurar ou trocar o provider de LLM
- Ao debugar erros de API
- Ao adicionar suporte a um novo provider

## Configuração (2 variáveis)

```env
LLM_PROVIDER=zai
LLM_API_KEY=sua-chave
```

Pronto. O sistema detecta `base_url`, modelo de chat e modelo de embedding automaticamente.

## Providers

### Z.ai (GLM-5.1)

```env
LLM_PROVIDER=zai
LLM_API_KEY=sua-chave-zai
# Base URL: https://api.z.ai/api/paas/v4
# Chat: glm-5.1
# Embedding: embedding-3 (1024d)
```

- 100% compatível com OpenAI SDK
- Modelos: GLM-5.1, GLM-5-Turbo, GLM-4.7

### OpenAI

```env
LLM_PROVIDER=openai
LLM_API_KEY=sk-...
# Base URL: https://api.openai.com/v1
# Chat: gpt-4o-mini
# Embedding: text-embedding-3-small (512d)
```

### OpenRouter

```env
LLM_PROVIDER=openrouter
LLM_API_KEY=sk-or-...
# Base URL: https://openrouter.ai/api/v1
# Chat: openai/gpt-4o-mini
# Embedding: openai/text-embedding-3-small (512d)
```

- Acesso a 100+ modelos via um endpoint
- Formato: `provider/model` (ex: `anthropic/claude-3.5-sonnet`)

### Gemini

```env
LLM_PROVIDER=gemini
LLM_API_KEY=AIza...
# Base URL: https://generativelanguage.googleapis.com/v1beta/openai
# Chat: gemini-2.0-flash
# Embedding: text-embedding-004 (768d, API nativa)
```

- Chat via endpoint OpenAI-compatible do Gemini
- Embeddings via API nativa do Google (endpoint separado)

### Local (sem API)

```env
LLM_PROVIDER=local
# Chat: fallback heurístico (regex)
# Embedding: all-MiniLM-L6-v2 (384d, sentence-transformers)
```

- Funciona 100% offline
- Extração vira classificação por palavras-chave
- Sem HyDE

## Prioridade de API Key

```
1. Provider-specific: OPENAI_API_KEY, ZAI_API_KEY, OPENROUTER_API_KEY, GEMINI_API_KEY
2. Genérica: LLM_API_KEY
3. Sem key → fallback local
```

## Override Manual

Qualquer valor automático pode ser sobrescrito:

```env
LLM_PROVIDER=zai
LLM_API_KEY=chave
LLM_CHAT_MODEL=glm-5-turbo          # Override modelo de chat
EMBEDDING_MODEL=embedding-3          # Override modelo de embedding
EMBEDDING_DIMENSIONS=768             # Override dimensões
LLM_BASE_URL=https://custom.api/v1  # Override base URL
```

## O que cada provider afeta

| Componente | Usa LLM? | Provider |
|------------|----------|----------|
| **ExtractionService** | Sim | Chat model (instructor) |
| **HyDEService** | Sim | Chat model (openai SDK) |
| **Embeddings** | Sim | Embedding model |
| **Reranking** | Independente | `RERANKER_PROVIDER` separado |
| **Admission Gates** | Não | Regras determinísticas |
| **Consolidation** | Não | Jaro-Winkler + pesos |

## Arquitetura

```
services/extraction_service.py
├── get_llm_provider()      → lê LLM_PROVIDER
├── get_llm_api_key()       → lê key com fallback
├── get_llm_base_url()      → auto-detecção por provider
├── get_llm_chat_model()    → auto-detecção por provider
└── PROVIDER_CONFIGS        → lookup table de defaults

services/embedding_providers.py
├── OpenAICompatibleEmbeddingProvider  → openai, zai, openrouter
├── GeminiEmbeddingProvider            → API nativa Google
├── LocalMiniLMEmbeddingProvider       → sentence-transformers
└── create_default_embedding_provider() → factory

services/hyde_service.py
└── HyDEService._build_client()  → mesmo provider de chat
```

## Regras

- Trocar provider NÃO requer reiniciar o servidor (lê env vars)
- Trocar modelo de embedding SEMPRE requer reindexar a collection Qdrant
- Todos os providers OpenAI-compatible usam `instructor` para extração estruturada
- Se `instructor` não está instalado, fallback heurístico automático
