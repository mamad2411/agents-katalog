---
name: Agent Loop Integration
description: Fluxo pré/durante/pós tarefa do agente IA, pre-task context loading, contextual queries, post-task knowledge extraction, e feedback loop.
---

# Agent Loop Integration

## Quando Usar

- Ao integrar o sistema de memória com o workflow do agente
- Ao configurar quais resources/tools usar em cada fase
- Ao implementar o resumo pós-tarefa

## O Loop de 3 Fases

```
┌─────────────────────────────────────────────┐
│                 Agent Loop                   │
│                                              │
│  PRÉ  → Carregar contexto essencial         │
│  DUR  → Consultar sob demanda               │
│  PÓS  → Extrair, admitir, persistir         │
└─────────────────────────────────────────────┘
```

## Fase 1: PRÉ-TAREFA (Before)

O agente carrega contexto **antes** de começar qualquer implementação:

```python
async def pre_task_context(project: str, domain: str | None = None) -> dict:
    context = {
        "design_rules": await search.search(
            "design rules conventions", project, category="DesignRule", top_k=5
        ),
        "patterns": await search.search(
            "design patterns", project, category="DesignPattern", top_k=5
        ),
    }
    if domain:
        context["domain_rules"] = await search.search(
            f"business rules {domain}", project, category="BusinessRule", top_k=5
        )
    return context
```

**Resources MCP usados nesta fase:**
- `mem://project/CORE/top-design-rules`
- `mem://project/CORE/top-patterns`
- `mem://domain/RETUSD/rules`

## Fase 2: DURANTE A TAREFA (During)

Consulta contextual quando surge dúvida:

```python
async def during_task_query(question: str, project: str) -> list[dict]:
    return await search.search(question, project, top_k=5)
```

**Tool MCP usado:**
- `memory.query(project="CORE", query_text="como sazonalizar?")`

## Fase 3: PÓS-TAREFA (After)

Extrair conhecimento, avaliar, e persistir:

```python
async def post_task_summary(task_description: str, changes: str, project: str) -> dict:
    full_text = f"TAREFA: {task_description}\n\nMUDANÇAS: {changes}"
    
    # 1. Extrair candidatos via LLM
    candidates = await extraction.extract_candidates(full_text, project)
    
    # 2. Avaliar cada candidato nos 5 gates
    results = []
    for candidate in candidates:
        admission_result = await admission.evaluate(candidate)
        
        # 3. Persistir se admitido
        if admission_result.status in ("active", "proposed"):
            item = await persistence.persist(candidate, admission_result)
            results.append({
                "memory_id": item.memory_id,
                "title": item.title,
                "action": admission_result.action,
                "status": admission_result.status,
            })
    
    return {
        "candidates_extracted": len(candidates),
        "memories_created": sum(1 for r in results if r["action"] == "create"),
        "memories_updated": sum(1 for r in results if r["action"] == "update"),
        "rejected": len(candidates) - len(results),
    }
```

**Tools/Prompts MCP usados:**
- `prompt://summarize_work_item`
- `memory.upsert(...)` ou pipeline completo de ingestão

## Diagrama de Integração

```
PRÉ ──→ Resources (leitura pronta, sem latência de busca)
         ↓
DURANTE → Tools (busca sob demanda, contextual)
         ↓
PÓS ──→ Prompts (extração) → Admission → Persistence → Telemetria
```

## Regras

- PRÉ-TAREFA é obrigatório — agente DEVE carregar contexto antes de agir
- DURANTE: usar apenas quando surgir dúvida contextual (não spammar)
- PÓS-TAREFA: extrair APENAS conhecimento durável, não detalhes efêmeros
- O retorno do pós-tarefa deve incluir métricas (criados, atualizados, rejeitados)
- Registrar feedback telemetria em cada fase
