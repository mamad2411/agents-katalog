---
name: Memory Consolidation Science
description: Use when implementing or tuning memory consolidation strategies — merge, promotion, deprecation, cross-memory synthesis, scheduling, and decay. Applies when deciding between immediate vs deferred consolidation or evaluating consolidation quality.
---

# Memory Consolidation Science

## Overview

Consolidação de memória é o processo de transformar informações brutas em conhecimento estruturado e duradouro. Inspirado na neurociência (consolidação hipocampal → cortical), TheSearch aplica consolidação em duas fases: **imediata** (durante a tarefa) e **diferida** (background jobs).

**Princípio:** Memória não é armazenamento — é um processo ativo de refino contínuo.

## Quando Usar

- Ao projetar ou modificar pipelines de consolidação
- Ao decidir entre consolidação imediata vs diferida
- Ao implementar promotion/deprecation de memórias
- Ao criar strategies para cross-memory synthesis
- Ao calibrar scheduling de background jobs
- Ao medir qualidade da consolidação

## Fundamentos Científicos

### Ebbinghaus Forgetting Curve

Modelo de decay exponencial — sem reforço, memória decai rapidamente:

```
R(t) = e^(-t/S)
```

- `R` = retenção, `t` = tempo, `S` = força da memória (estabilidade)
- Cada acesso reforça → aumenta `S` → decai mais devagar
- TheSearch implementa isso via `weight_decay` (skill 11)

**Referência:** MemoryBank (Zhong et al., 2023) — aplica Ebbinghaus diretamente em LLM agents.

### Generative Agents — Reflection

Park et al. (Stanford, 2023): agents acumulam observations e periodicamente geram **reflections** — summaries de alto nível que são eles próprios armazenados como memórias.

```
observations diárias → reflection semanal → identity statement mensal
```

Insight-chave: **reflections são mais importantes que observations isoladas** porque capturam padrões.

### Retroformer — Retrospective Memory

Liu et al. (2023): retrospective memory com policy gradient optimization. O agent revisita experiências passadas e otimiza seu comportamento futuro.

**Aplicação em TheSearch:** consolidação diferida pode re-processar memórias com contexto adicional (mais evidências acumuladas desde a criação).

### Self-Reflective LLM Memory

Wang et al. (2024): o sistema de memória se auto-organiza via reflexão. Memórias são periodicamente reavaliadas: ainda relevantes? precisam de merge? devem ser promovidas?

### ExpeL — Experiential Learning

Zhao et al. (2023): agents extraem **insights** de experiências acumuladas. Insights são diferentes das experiências — são generalizações.

```
"O usuário prefere TypeScript para projetos novos"  ← insight (valioso)
"Usuário escolheu TypeScript no projeto X"           ← observation (factual)
```

### Hierarchical Context Merger

Hierarchical summarization: contexts são mergeados progressivamente em níveis de abstração crescente. Similar a como o cérebro consolida memórias episódicas em semânticas.

## Consolidação no TheSearch

### Arquitetura de Duas Fases

```
Fase 1 — Imediata (hot path):
  candidato → admission gates → proposed/active
  Rápido, síncrono, dentro do fluxo do agente

Fase 2 — Diferida (background):
  proposed → merge/recalculate/promote/deprecate
  Assíncrono, não bloqueia o agente
```

### Immediate vs Deferred: Quando Usar Cada Um

| Critério | Imediato | Diferido |
|----------|:--------:|:--------:|
| Latência sensível | ✅ | ❌ |
| Dados suficientes para decisão | ✅ | ❌ |
| Precisa de contexto cruzado | ❌ | ✅ |
| Custo computacional alto | ❌ | ✅ |
| Volume de candidatos alto | ❌ | ✅ |
| Decisão irreversível | ❌ | ✅ (mais seguro) |

**Regra prática:** Se a operação pode ser feita com dados locais em < 100ms, faça imediato. Caso contrário, defer.

### 5 Operações da Consolidação Diferida

#### 1. Merge de Near-Duplicates

Jaro-Winkler similarity para títulos + cosine similarity para conteúdo:

```python
async def merge_duplicates(project: str):
    candidates = await neo4j.find_potential_duplicates(project)
    for pair in candidates:
        title_sim = jaro_winkler_similarity(pair.a.title, pair.b.title)
        content_sim = cosine_similarity(pair.a.embedding, pair.b.embedding)
        combined = 0.4 * title_sim + 0.6 * content_sim
        if combined > 0.90:
            winner = pair.a if pair.a.effective_weight >= pair.b.effective_weight else pair.b
            loser = pair.b if winner == pair.a else pair.a
            await merge_into(winner, loser)
```

#### 2. Recálculo de Pesos

Aplica o modelo composto de 5 componentes (skill 11) com dados atualizados:

```python
async def recalculate_all_weights():
    async for item in neo4j.stream_active_items():
        new_weight = WeightCalculator.compose(
            weight_manual=item.weight_manual,
            weight_confidence=item.weight_confidence,
            weight_usage=await get_usage_signal(item.memory_id),
            weight_feedback=await get_feedback_signal(item.memory_id),
            weight_decay=WeightCalculator.ebbinghaus_decay(
                item.effective_weight, item.last_accessed_at
            ),
        )
        await neo4j.update_effective_weight(item.memory_id, new_weight)
```

#### 3. Promotion: Proposed → Active

Memória candidata se torna canônica quando acumula evidência suficiente:

```python
PROMOTION_RULES = {
    "evidence_count >= 3": "Direct promotion",
    "evidence_count >= 2 AND weight >= 0.5": "Weight-boosted promotion",
    "is_architectural_decision": "Auto-promote (ADRs bypass gates)",
    "age_hours >= 24 AND no_conflicts": "Time-based promotion",
}

async def promote_eligible():
    proposed = await neo4j.get_proposed_items()
    for item in proposed:
        if meets_promotion_criteria(item):
            await neo4j.set_status(item.memory_id, "active")
            await audit_log("promoted", item.memory_id, reason=...#,)
```

**Ciência:** Analogia com memory reconsolidation — cada acesso reativa e potencialmente fortalece a memória (Nader, 2003).

#### 4. Deprecation: Graceful Retirement

Memórias não são deletadas — são deprecadas com trail de auditoria:

```python
async def deprecate_stale():
    candidates = await neo4j.find_deprecation_candidates(
        min_age_days=30,
        max_weight=0.1,
        max_access_count=0,
    )
    for item in candidates:
        has_replacement = await neo4j.has_active_replacement(item.memory_id)
        if has_replacement:
            await neo4j.set_status(item.memory_id, "deprecated")
            await neo4j.create_relationship(
                replacement.memory_id, item.memory_id, "SUPERSEDES"
            )
```

**Regra:** NUNCA delete memórias — deprecate com `SUPERSEDES` para manter lineage.

#### 5. Cross-Memory Synthesis

Extração de insights de múltiplas memórias (inspirado em ExpeL e Generative Agents reflection):

```python
async def synthesize_insights(project: str):
    clusters = await neo4j.find_memory_clusters(project, min_size=3)
    for cluster in clusters:
        memories_text = format_for_synthesis(cluster.members)
        insight = await llm.extract(
            f"Given these related memories, extract a higher-level insight:\n{memories_text}",
            response_model=MemoryInsight,
        )
        if insight.confidence > 0.7:
            candidate = MemoryCandidate(
                title=insight.title,
                summary=insight.summary,
                type="insight",
                sources=[m.memory_id for m in cluster.members],
            )
            await admission_pipeline.process(candidate)
```

**Tipo de memória resultante:** `insight` — diferente de `fact` ou `decision`, representa generalização.

## Scheduling Strategies

### Frequência por Operação

| Operação | Frequência Recomendada | Justificativa |
|----------|:----------------------:|---------------|
| Merge duplicates | 4-6h | Acumula candidatos suficientes |
| Recalculate weights | 6-12h | Uso muda gradualmente |
| Apply decay | 24h | Decay é gradual por natureza |
| Promote proposed | 4-6h | Evita backlog |
| Deprecate stale | 24-48h | Operação conservadora |
| Cross-memory synthesis | 24h | Computacionalmente intensiva |

### Trigger-Based Scheduling

Combinar time-based com event-based:

```python
TRIGGERS = {
    "after_n_insertions": {"count": 10, "ops": ["merge", "promote"]},
    "weight_threshold": {"below": 0.15, "ops": ["deprecate"]},
    "cluster_size": {"above": 5, "ops": ["synthesize"]},
    "scheduled": {"interval": "6h", "ops": ["all"]},
}
```

## Quality Metrics

### Métricas de Consolidação

| Métrica | Como Medir | Target |
|---------|------------|:------:|
| Duplicate rate | `deprecated_by_merge / total_memories` | < 5% |
| Promotion rate | `promoted / proposed` | > 60% |
| Stale ratio | `deprecated / active` | < 20% |
| Insight quality | human feedback on synthesized insights | > 0.7 |
| Merge accuracy | false positive rate of merges | < 2% |
| Weight stability | variance of weights over time | decreasing |

### Health Check

```python
async def consolidation_health() -> dict:
    return {
        "total_active": await neo4j.count("active"),
        "total_proposed": await neo4j.count("proposed"),
        "avg_weight": await neo4j.avg_weight("active"),
        "duplicate_candidates": len(await neo4j.find_potential_duplicates()),
        "stale_candidates": len(await neo4j.find_deprecation_candidates()),
        "last_consolidation": await neo4j.get_last_consolidation_time(),
    }
```

## Common Mistakes

| Erro | Consequência | Correção |
|------|-------------|----------|
| Consolidar no hot path | Latência alta, bloqueia agente | Sempre defer para background |
| Deletar ao invés de deprecar | Perda de lineage e auditoria | Marcar `deprecated` + `SUPERSEDES` |
| Promover sem evidência suficiente | Memórias erradas viram canônicas | Exigir min 2-3 evidências |
| Rodar synthesis com poucas memórias | Insights triviais | Min 3-5 memórias relacionadas |
| Ignorar decay | Memórias obsoletas nunca saem | Aplicar Ebbinghaus decay diariamente |
| Threshold de merge muito baixo | False positives — merge incorreto | Manter > 0.90 com múltiplos sinais |
| Não auditar operações | Impossível debugar quality issues | Log every merge/promote/deprecate |

## Referências

- **Ebbinghaus / MemoryBank:** Zhong et al., "MemoryBank: Enhancing LLMs with Long-Term Memory" (2023) — knogdement/02
- **Generative Agents:** Park et al., "Interactive Simulacra of Human Behavior" (2023) — knogdement/02
- **Retroformer:** Liu et al., "Retrospective LLM Agents with Policy Gradient" (2023) — knogdement/02
- **Self-Reflective Memory:** Wang et al. (2024) — knogdement/02
- **ExpeL:** Zhao et al., "LLM Agents Are Experiential Learners" (2023) — knogdement/02
- **Hierarchical Context Merger** (2023) — knogdement/02
- **Consolidação TheSearch (implementação):** Skill 13 — Consolidation & Background Jobs
- **Weight System:** Skill 11 — Weight System & Decay
