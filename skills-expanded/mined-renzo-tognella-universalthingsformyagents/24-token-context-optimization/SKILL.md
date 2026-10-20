---
name: Token & Context Optimization
description: Use when reducing token costs, optimizing prompt sizes, managing context windows, or implementing compression/caching strategies in TheSearch pipeline stages (extraction, search, consolidation).
---

# Token & Context Optimization

## Overview

O TheSearch gasta tokens em 3 estágios principais: **extração** (LLM extrai conhecimento), **busca** (construção de queries + contexto recuperado), e **consolidação** (merge + refinamento). Cada estágio tem padrões repetitivos que podem ser comprimidos ou cacheados.

**Princípio:** Comprimir onde o modelo já "sabe" o padrão, gastar tokens onde a informação é nova.

## Quando Usar

- Ao analisar custos de tokens do pipeline TheSearch
- Ao implementar prompt caching para patterns repetitivos
- Ao compactar contexto no agent loop (histórico crescente)
- Ao definir token budgets por operação
- Ao avaliar tradeoffs entre compressão e qualidade

## Quando NÃO Usar

- Prompts curtos (<500 tokens) — overhead da compressão supera ganho
- Operações críticas onde perda de informação é inaceitável
- Primeira interação sem contexto repetitivo — sem ganho de cache

## Onde TheSearch Gasta Tokens

| Estágio | Tokens Estimados | Padrão | Otimização |
|---------|:---:|---------|------------|
| Extração | 800-1500 | System prompt + schema + input | Prompt caching, structured output |
| Busca | 500-1200 | Query + resultados + instruções | Compressão de resultados, cache de prefixo |
| Consolidação | 1000-2000 | Contexto + candidatos + regras | Batch, compaction de histórico |
| Agent loop | Acumula | Histórico cresce a cada turno | Context compaction automático |

## Token Budgets (Alvos)

```
Extração (por item):     ≤ 1000 tokens input, ≤ 300 output
Busca (por query):       ≤ 800 tokens input
Consolidação (por run):  ≤ 1500 tokens input, ≤ 500 output
Agent loop turno:        ≤ 2000 tokens (comprimido)
```

## Estratégia 1: Prompt Caching

TheSearch repete os mesmos prefixos em toda chamada LLM: category schemas, extraction rules, project context. O caching automático (OpenAI, Anthropic) salva até 90% do custo desses prefixos.

**Como maximizar cache hits:**

```python
SYSTEM_PREFIX = """You are a knowledge extraction engine for TheSearch.
Categories: {categories}
Schema: {schema}
Rules:
1. Extract factual knowledge only
2. Use exact field names from schema
3. One MemoryItem per distinct concept"""

async def extract_knowledge(input_text: str, project: str) -> MemoryItem:
    messages = [
        {"role": "system", "content": SYSTEM_PREFIX},
        {"role": "user", "content": f"Project: {project}\nInput: {input_text}"}
    ]
    return await llm.call(messages, response_format=MemoryItemSchema)
```

**Regras para cache efetivo:**
- Prefixo do system prompt deve ser **estático** — sem variáveis dinâmicas no início
- Variáveis (project, input) vão no **final** das mensagens
- Mínimo de 1024 tokens no prefixo para ativar cache (OpenAI)
- Manter mesma ordem de mensagens entre chamadas

**Savings estimados:**
- System prompt TheSearch: ~400 tokens fixos → cache hit 90%
- Com 100 extrações/dia: ~36K tokens cached → $0.07/dia salvo

## Estratégia 2: Compressão de Contexto de Busca

Resultados de busca híbrida (Qdrant + Neo4j) podem gerar 2000+ tokens de contexto. Usar LLMLingua ou truncamento inteligente para reduzir.

```python
async def build_search_context(
    results: list[SearchResult],
    max_tokens: int = 600
) -> str:
    ranked = sorted(results, key=lambda r: r.score, reverse=True)
    context_parts = []
    token_count = 0

    for r in ranked:
        entry = f"[{r.memory_id}] {r.title}: {r.summary}"
        entry_tokens = estimate_tokens(entry)
        if token_count + entry_tokens > max_tokens:
            break
        context_parts.append(entry)
        token_count += entry_tokens

    return "\n".join(context_parts)
```

**Approaches por qualidade/custo:**

| Método | Compressão | Perda de Qualidade | Custo |
|--------|:---:|:---:|:---:|
| Truncamento por score | 2-3x | Baixa (top-k) | Zero |
| LLMLingua compressão | 5-10x | Baixa | Extra LLM call |
| Sumarização | 3-5x | Média | Extra LLM call |
| Static embedding pre-filter | 10x | Baixa (coarse→fine) | CPU local |

## Estratégia 3: Context Compaction no Agent Loop

O agente MCP acumula histórico a cada turno. Sem compaction, o contexto explode após 5-10 turnos.

```python
class ContextManager:
    def __init__(self, max_turns_kept: int = 4, max_context_tokens: int = 2000):
        self.max_turns = max_turns_kept
        self.max_tokens = max_context_tokens

    async def compact(self, messages: list[dict]) -> list[dict]:
        if estimate_tokens(messages) <= self.max_tokens:
            return messages

        summary = await llm.call([
            {"role": "system", "content": "Summarize this conversation history concisely, preserving key facts and decisions."},
            {"role": "user", "content": str(messages[:-2])}
        ])

        return [
            {"role": "system", "content": f"Previous context: {summary}"},
            *messages[-2:]
        ]
```

**Quando compactar:**
- Após 4+ turnos sem compactação
- Quando tokens excedem budget do estágio
- Antes de operações custosas (consolidação, busca ampla)

## Estratégia 4: Structured Outputs

Force JSON schema para eliminar tokens desperdiçados com formato livre (markdown, explicações, etc.).

```python
from pydantic import BaseModel

class ExtractedKnowledge(BaseModel):
    title: str
    summary: str
    category: str
    evidence: list[str]
    confidence: float

response = await client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=messages,
    response_format=ExtractedKnowledge,
)
```

**Ganho:** Reduz output tokens em ~40% (sem "Here is the extracted knowledge:" preâmbulos).

## Estratégia 5: DiffuMask / LLMLingua para Batch Processing

Para consolidação em batch (múltiplos candidatos), comprimir inputs não-essenciais:

```python
from llmlingua import PromptCompressor

compressor = PromptCompressor("microsoft/llmlingua-2-bert-base-uncased")

def compress_for_consolidation(context: str, target_ratio: float = 0.4) -> str:
    compressed = compressor.compress_prompt(
        context,
        rate=target_ratio,
        target_token=200
    )
    return compressed["compressed_prompt"]
```

**Quando usar LLMLingua:**
- Batch consolidation com 10+ candidatos
- RAG context > 1000 tokens
- Prompts com muito boilerplate repetitivo

**Quando NÃO usar:** Extração de conhecimento individual — o input do usuário é o payload principal, não comprimível.

## Tradeoffs: Compressão vs Qualidade

```
                       Qualidade
                          ↑
                     ┌────┤
          Sem compressão │    │
                     │    │
               Cache │    │ ← Sweet spot TheSearch
                     │    │   (cache prefixo + truncate resultados)
          LLMLingua  │    │
                     │    │
          Aggressive │    │ ← Perigo: perda de entidades
           compress  └────┴────────────────────→ Economia
```

| Cenário | Compressão Segura | Risco |
|---------|:---:|:---|
| System prompt fixo | Cache 90% | Zero |
| Top-k resultados busca | Truncar após rank 5 | Baixo |
| Histórico agent | Summarize turns antigos | Médio |
| Input do usuário | NÃO comprimir | Alto |
| Regras de consolidação | Cache + reduce | Baixo |

## Common Mistakes

1. **Comprimir o input do usuário** — nunca. O payload principal não deve ser alterado.
2. **Cache com prefixo dinâmico** — variáveis no início do system prompt invalidam cache.
3. **Compaction agressiva no agent loop** — resumo perde decisões recentes. Manter últimos 2 turnos intactos.
4. **Ignorar structured outputs** — `response_format` com Pydantic elimina parsing frágil e tokens de formatação.
5. **LLMLingua em tudo** — overhead do modelo de compressão (>100ms) não compensa para inputs <500 tokens.

## Referências

- `knogdement/05_skills_token_optimization.md` — LLMLingua, LongLLMLingua, TokenDance, DiffuMask, MInference
- OpenAI Prompt Caching: https://platform.openai.com/docs/guides/prompt-caching
- LLMLingua: https://github.com/microsoft/LLMLingua (20x compression)
- TokenDance: 17.5x KV cache reduction for multi-agent (arXiv 2604.03143)
- DiffuMask: diffusion-based parallel pruning (arXiv 2604.06627)
