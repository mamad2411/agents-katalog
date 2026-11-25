---
name: Episodic & Procedural Memory Tools
description: Memória episódica (experiência de tarefas) e procedural (procedimentos reutilizáveis) — quando criar, quando consultar, como se relacionam com memórias declarativas.
---

# Episodic & Procedural Memory Tools

## Quando Usar

- Ao registrar o resultado de uma tarefa (episódio)
- Ao consultar experiências passadas antes de começar tarefa
- Ao criar ou consultar procedimentos reutilizáveis

## Conceito

O TheSearch tem 3 camadas de memória:

```
Declarativa (MemoryItem)     → "O que" o sistema sabe (regras, padrões, ADRs)
Episódica (EpisodicMemory)   → "O que aconteceu" (outcomes, lições)
Procedural (ProceduralMemory) → "Como fazer" (passos reutilizáveis)
```

## Episodic Memory

### Tool: `memory.episode.create`

```json
{
  "project": "CORE",
  "task_description": "Fix authentication token validation bug",
  "approach": "Added server-side JWT validation middleware",
  "outcome": "completed",
  "lessons": [
    "Always validate tokens server-side, not just client-side",
    "JWT expiration should be checked before signature"
  ],
  "related_memory_ids": ["abc123"],
  "tags": ["auth", "security", "bugfix"]
}
```

**`outcome`:** `completed` | `failed` | `partial`

**Quando criar:**
- Após completar qualquer tarefa não-trivial
- Após tentativa que falhou (registra o que não funcionou)
- Quando aprendeu algo novo durante execução

**Relações automáticas:** `related_memory_ids` cria `(EpisodicMemory)-[:LEARNED_FROM]->(MemoryItem)`

### Tool: `memory.episode.query`

```json
{
  "project": "CORE",
  "outcome": "failed",
  "tag": "auth",
  "limit": 10
}
```

**Casos de uso:**
- Antes de abordar problema similar → consultar episódios com `tag` relevante
- Ver o que falhou recentemente → `outcome=failed`
- Ver lições aprendidas → qualquer query, focar no campo `lessons`

## Procedural Memory

### Tool: `memory.procedure.create`

```json
{
  "project": "CORE",
  "task_type": "bug_fix",
  "steps": [
    "Reproduce the bug with a minimal test case",
    "Write a failing test that demonstrates the bug",
    "Implement the minimal fix",
    "Run the full test suite",
    "Update related documentation"
  ],
  "preconditions": [
    "Test environment is running",
    "Relevant code is understood"
  ],
  "tools_required": ["pytest", "git"],
  "tags": ["bugfix", "workflow"]
}
```

**Quando criar:**
- Após executar um procedimento que funcionou bem
- Quando um padrão de tarefa se repete (3+ vezes)
- Quando o procedimento é complexo o suficiente para esquecer passos

### Tool: `memory.procedure.query`

```json
{
  "project": "CORE",
  "task_type": "bug_fix",
  "limit": 5
}
```

**Retorna** procedimentos ordenados por `success_rate` DESC, `usage_count` DESC.

## Fluxo do Agente

```
1. Antes da tarefa:
   → memory.query(project="CORE", query_text="bug fix procedure")
   → memory.procedure.query(project="CORE", task_type="bug_fix")
   → memory.episode.query(project="CORE", tag="bugfix")

2. Durante a tarefa:
   → Segue os steps do procedimento encontrado
   → memory.query() para consultar regras relevantes

3. Depois da tarefa:
   → memory.reflect(task_description=..., changes=..., project="CORE")
   → memory.episode.create(project="CORE", outcome="completed", lessons=[...])
   → Se procedimento novo → memory.procedure.create(project="CORE", task_type=..., steps=[...])
```

## Modelo de Dados

### EpisodicMemory (Neo4j label: `EpisodicMemory`)

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `episode_id` | str | Hash de project+"episode"+task_description |
| `project` | str | Projeto |
| `task_description` | str | O que foi feito |
| `approach` | str | Como foi abordado |
| `outcome` | enum | completed/failed/partial |
| `lessons` | list[str] | O que aprendeu |
| `related_memory_ids` | list[str] | Memórias declarativas relacionadas |
| `tags` | list[str] | Tags para busca |
| `created_at` | datetime | Quando |

### ProceduralMemory (Neo4j label: `ProceduralMemory`)

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `procedure_id` | str | Hash de project+"procedure"+task_type |
| `project` | str | Projeto |
| `task_type` | str | Categoria da tarefa |
| `steps` | list[str] | Passos ordenados |
| `preconditions` | list[str] | O que precisa antes |
| `tools_required` | list[str] | Ferramentas necessárias |
| `success_rate` | float | 0.0-1.0 (default 1.0) |
| `usage_count` | int | Vezes usado |
| `tags` | list[str] | Tags |

## Regras

- Episódios e procedimentos vivem em labels separados no Neo4j
- Não vão para Qdrant (não têm embeddings)
- `episode_id` é determinístico (hash) — criar duas vezes com mesma descrição = upsert
- Procedimentos são ordenados por sucesso + uso na query
