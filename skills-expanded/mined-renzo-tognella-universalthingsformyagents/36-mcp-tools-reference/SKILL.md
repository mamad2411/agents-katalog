---
name: MCP Tools Reference
description: Referência completa de todos os MCP tools disponíveis no TheSearch — parâmetros, retornos, quando usar cada um.
---

# MCP Tools Reference

## Quando Usar

- Ao invocar qualquer tool do TheSearch via MCP
- Ao decidir qual tool usar para uma operação
- Ao debugar chamadas MCP

## Ferramentas Disponíveis (28 tools)

### Busca & Consulta

| Tool | Descrição | Parâmetros |
|------|-----------|------------|
| `memory.query` | Busca híbrida (vetorial + grafo + RRF) | `project, query_text?, category?, top_k?, min_weight?, min_score?` |
| `memory.context` | Carrega contexto pré-tarefa (regras, padrões, ADRs) | `project, domain?` |
| `memory.reflect` | Extrai conhecimento pós-tarefa | `task_description, changes, project` |
| `memory.get` | Busca uma memória por ID | `memory_id` |

**Quando usar o quê:**
- Antes de começar tarefa → `memory.context`
- Para buscar conhecimento → `memory.query`
- Depois de terminar tarefa → `memory.reflect`
- Para ver uma memória específica → `memory.get`

### Criação & Persistência

| Tool | Descrição | Parâmetros |
|------|-----------|------------|
| `memory.upsert` | Cria ou atualiza memória manual | `project, title, summary, details?, category?, domain?, weight?` |
| `memory.ingest_raw` | Ingesta texto bruto e extrai candidatos | `content, project, probable_category?, domain?` |
| `memory.manual_create` | Cria memória com controle total sobre campos | `project, title, summary, category, details?, domain?, weight?` |

### Relacionamentos

| Tool | Descrição | Parâmetros |
|------|-----------|------------|
| `memory.link` | Cria relação entre duas memórias | `from_id, rel, to_id` |
| `memory.deprecate` | Deprecata memória existente | `memory_id` |

### Pesos & Feedback

| Tool | Descrição | Parâmetros |
|------|-----------|------------|
| `memory.set_weight` | Ajusta peso manual de uma memória | `memory_id, weight` |
| `memory.feedback` | Registra feedback positivo/negativo | `memory_id, score, comment?` |

### Consolidação & Manutenção

| Tool | Descrição | Parâmetros |
|------|-----------|------------|
| `memory.consolidate` | Roda consolidação (merge, pesos, promoção) | `scope?` |
| `memory.reconcile` | Verifica consistência Neo4j↔Qdrant | `project?` |
| `memory.list_raw_events` | Lista eventos brutos da landing zone | `project?, limit?` |

### Memória Episódica (experiência)

| Tool | Descrição | Parâmetros |
|------|-----------|------------|
| `memory.episode.create` | Registra outcome de tarefa | `project, task_description, approach?, outcome?, lessons?, related_memory_ids?, tags?` |
| `memory.episode.query` | Consulta episódios por projeto | `project, outcome?, tag?, limit?` |

**outcome:** `completed` | `failed` | `partial`

### Memória Procedural (procedimentos)

| Tool | Descrição | Parâmetros |
|------|-----------|------------|
| `memory.procedure.create` | Cria procedimento reutilizável | `project, task_type, steps, preconditions?, tools_required?, tags?` |
| `memory.procedure.query` | Busca procedimentos por tipo de tarefa | `project, task_type?, limit?` |

### PR Memory

| Tool | Descrição | Parâmetros |
|------|-----------|------------|
| `memory.pr.create` | Cria PR memory | `project, repo, pr_number, changed_files, description, author?` |
| `memory.pr.query` | Consulta PR memories | `project, repo?, pr_number?, changed_file_contains?` |
| `memory.pr.link_memory` | Conecta PR memory a MemoryItem | `pr_memory_id, memory_id, relation_type, rationale?` |
| `memory.pr.query_memories` | Lista memórias linked a um PR | `pr_memory_id` |

### Catálogo (Grafo)

| Tool | Descrição | Parâmetros |
|------|-----------|------------|
| `graph.project.create` | Cria nó projeto | `name, description?` |
| `graph.project.list` | Lista projetos | — |
| `graph.category.create` | Cria nó categoria | `name, description?` |
| `graph.domain.create` | Cria nó domínio | `name, description?` |
| `graph.relation.create` | Cria relação entre nós de catálogo | `source_id, source_kind, relation_type, target_id, target_kind, rationale?` |
| `graph.relation.delete` | Remove relação de catálogo | `source_id, source_kind, relation_type, target_id, target_kind` |
| `graph.catalog.export_csv` | Exporta catálogo como CSV | — |
| `graph.catalog.import_csv` | Importa catálogo de CSV | `csv_content` |

## Relações Válidas

**MemoryItem → MemoryItem:** `RELATED_TO`, `DEPENDS_ON`, `REFINES`, `DEPRECATES`, `CONFLICTS_WITH`, `EVOLVES_FROM`

**Catálogo:** `HAS_CATEGORY`, `HAS_DOMAIN`, `RELATED_TO`, `DEPENDS_ON`, `REFINES`, `DEPRECATES`, `CONFLICTS_WITH`, `EVOLVES_FROM`

**Episódio → MemoryItem:** `LEARNED_FROM` (criado automaticamente via `related_memory_ids`)

## Fluxo Recomendado do Agente

```
1. memory.context(project="CORE")           → O que eu devo saber?
2. ... executa tarefa ...
3. memory.query(project="CORE", query_text="...")  → Precisa consultar durante
4. memory.reflect(task_description="...", changes="...", project="CORE")  → Extrai licoes
5. memory.episode.create(project="CORE", task_description="...", outcome="completed", lessons=["..."])  → Registra experiencia
```

## Retorno de Erro

Todos os tools retornam `{"error": "mensagem"}` em caso de falha.
