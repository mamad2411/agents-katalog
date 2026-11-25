---
name: llm-ops
description: "Operações de LLM — RAG, embeddings, bancos de dados vetoriais, fine-tuning, prompt engineering avançado, custos de LLM, avaliações de qualidade e arquiteturas de IA para produção."
risk: safe
source: community
date_added: '2026-03-06'
author: renat
tags:
- llm
- rag
- embeddings
- vector-db
- fine-tuning
tools:
- claude-code
- antigravity
- cursor
- gemini-cli
- codex-cli
---

# LLM-OPS — IA de Produção

## Visão Geral

Operações de LLM — RAG, embeddings, bancos de dados vetoriais, fine-tuning, prompt engineering avançado, custos de LLM, avaliações de qualidade e arquiteturas de IA para produção. Ativar para: implementar RAG, criar pipeline de embeddings, Pinecone/Chroma/pgvector, fine-tuning, prompt engineering, redução de custos de LLM, avaliações, cache semântico, streaming, agents.

## Quando Usar Esta Skill

- Quando você precisa de assistência especializada neste domínio

## Quando NÃO Usar Esta Skill

- A tarefa não está relacionada a llm ops
- Uma ferramenta mais simples e específica pode lidar com a solicitação
- O usuário precisa de assistência para fins gerais sem expertise em domínio

## Como Funciona

> A diferença entre um protótipo de IA e um produto de IA é operabilidade.
> LLM-Ops é a engenharia que torna IA confiável, escalável e econômica.

---

## Arquitetura RAG Completa

[Documentos] -> [Chunking] -> [Embeddings] -> [Banco Vetorial]
                                                      |
    [Query] -> [Embed query] -> [Busca Semântica] -> [Top K chunks]
                                                          |
                                           [LLM + Context] -> [Resposta]

## Pipeline de Indexação

```python
from anthropic import Anthropic
import chromadb

client = Anthropic()
chroma = chromadb.PersistentClient(path="./chroma_db")

def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk: chunks.append(chunk)
    return chunks

def index_document(doc_id, content_text, metadata=None):
    chunks = chunk_text(content_text)
    ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
    collection.upsert(ids=ids, documents=chunks)
    return len(chunks)
```

## Pipeline de Query com RAG

```python
def rag_query(query, top_k=5, system=None):
    results = collection.query(
        query_texts=[query], n_results=top_k,
        include=["documents", "metadatas", "distances"])
    context_parts = []
    for doc, meta, dist in zip(results["documents"][0],
                                results["metadatas"][0],
                                results["distances"][0]):
        if dist < 1.5:
            src = meta.get("source", "doc")
            context_parts.append(f"[Fonte: {src}]\n{doc}")
    context = "\n\n---\n\n".join(context_parts)
    response = client.messages.create(
        model="claude-opus-4-20250805", max_tokens=1024,
        system=system or "Responda baseado no contexto.",
        messages=[{"role": "user", "content": f"Contexto:\n{context}\n\n{query}"}])
    return response.content[0].text
```

---

## Escolha do Banco Vetorial

| DB | Melhor Para | Hosting | Custo |
|----|------------|---------|-------|
| Chroma | Desenvolvimento, local | Self-hosted | Grátis |
| pgvector | Já usa PostgreSQL | Self/Cloud | Grátis |
| Pinecone | Produção gerenciada | Cloud | USD 70+/mês |
| Weaviate | Multi-modal | Self/Cloud | Grátis+ |
| Qdrant | Alta performance | Self/Cloud | Grátis+ |

## pgvector

```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE knowledge_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    embedding vector(1536),
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX ON knowledge_embeddings
USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
SELECT content, 1 - (embedding <=> QUERY_VECTOR) AS similarity
FROM knowledge_embeddings ORDER BY similarity DESC LIMIT 5;
```

---

## Estrutura de Prompt de Elite

Componentes do system prompt Auri:

- Identidade: Nome (Auri), Tom (Natural, caloroso, direto), Plataforma (Amazon Alexa)
- Regras: Máximo 3 parágrafos curtos, sem markdown, linguagem conversacional
- Capacidades: análise de negócios, conselho baseado em dados, criatividade
- Limitações: sem internet em tempo real, sem transações financeiras
- Personalização: {user_name}, {user_preferences}, {relevant_history}

## Chain-of-Thought

```python
def cot_analysis(problem: str) -> str:
    steps = [
        "1. O que exatamente está sendo pedido?",
        "2. Que informações são críticas para resolver?",
        "3. Quais abordagens possíveis existem?",
        "4. Qual abordagem é melhor e por quê?",
        "5. Quais riscos ou limitações existem?",
    ]
    prompt = f"Analise passo a passo:\n\nPROBLEMA: {problem}\n\n"
    prompt += "\n".join(steps) + "\n\nResposta final (concisa, para voz):"
    return call_claude(prompt)
```

---

## Cache Semântico

```python
class SemanticCache:
    def __init__(self, similarity_threshold=0.95):
        self.threshold = similarity_threshold
        self.cache = {}

    def get_cached(self, query, embedding):
        for cached_emb, (response, _) in self.cache.items():
            if cosine_similarity(embedding, cached_emb) >= self.threshold:
                return response
        return None

    def set_cache(self, query, embedding, response):
        self.cache[tuple(embedding)] = (response, query)
```

## Estimativa de Custos Claude

```python
PRICING = {
    "claude-opus-4-20250805": {"input": 15.00, "output": 75.00},
    "claude-sonnet-4-5": {"input": 3.00, "output": 15.00},
    "claude-haiku-3-5": {"input": 0.80, "output": 4.00},
}

def estimate_monthly_cost(model, avg_input, avg_output, req_per_day):
    p = PRICING[model]
    daily = (avg_input + avg_output) * req_per_day / 1e6
    monthly = daily * p["input"] * 30
    return {"model": model, "monthly_cost": "USD %.2f" % monthly}
```

---

## Framework de Avaliação

```python
from anthropic import Anthropic
client = Anthropic()

def evaluate_response(question, expected, actual, criteria):
    criteria_text = "\n".join(f"- {c}" for c in criteria)
    eval_prompt = (
        f"Avalie a resposta do assistente de IA.\n\n"
        f"PERGUNTA: {question}\nRESPOSTA ESPERADA: {expected}\n"
        f"RESPOSTA ATUAL: {actual}\n\nCritérios:\n{criteria_text}\n\n"
        "Nota 0-10 e justificativa para cada critério. Formato JSON."
    )
    response = client.messages.create(
        model="claude-haiku-3-5", max_tokens=1024,
        messages=[{"role": "user", "content": eval_prompt}]
    )
    import json
    return json.loads(response.content[0].text)

AURI_EVALS = [
    {
        "question": "Quais são os principais riscos de abrir startup agora?",
        "criteria": ["precisao_factual", "relevancia", "clareza_para_voz"]
    },
]
```

---

## Comandos

| Comando | Ação |
|---------|------|
| /rag-setup | Configura pipeline RAG completo |
| /embed-docs | Indexa documentos no banco vetorial |
| /prompt-optimize | Otimiza prompt para qualidade e custo |
| /cost-estimate | Estima custo mensal do LLM |
| /eval-run | Roda suite de avaliações de qualidade |
| /cache-setup | Configura cache semântico |
| /model-select | Escolhe modelo ideal para o caso de uso |

## Melhores Práticas

- Forneça contexto claro e específico sobre seu projeto e requisitos
- Revise todas as sugestões antes de aplicá-las ao código de produção
- Combine com outras skills complementares para uma análise abrangente

## Armadilhas Comuns

- Usar esta skill para tarefas fora de sua expertise de domínio
- Aplicar recomendações sem entender seu contexto específico
- Não fornecer contexto suficiente do projeto para uma análise precisa