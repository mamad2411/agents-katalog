---
name: Multi-Agent Orchestration
description: Use when designing multi-agent workflows for TheSearch — specialized agent roles, orchestration patterns, inter-agent communication via MCP, event-driven coordination, and quality control with evaluator-optimizer loops.
---

# Multi-Agent Orchestration

## Overview

Multi-agent orchestration é a coordenação de múltiplos agentes especializados para resolver tarefas complexas de memória. Inspirado em frameworks como AutoGen, CrewAI e LangGraph, mas aplicado especificamente ao pipeline de memória do TheSearch.

**Princípio:** Agentes especializados superam agentes genéricos — mas a orquestração é o desafio real.

## Quando Usar

- Ao projetar pipelines com múltiplas etapas de processamento de memória
- Quando um agente single não tem capacidade para a tarefa
- Ao implementar quality gates com evaluator-optimizer
- Ao coordenar agentes assíncronos via eventos
- Ao escalar processamento paralelo de memórias

## Quando NÃO Usar

- Tarefas simples que um agente resolve em 1-2 steps
- Quando a latência de coordenação supera o benefício
- Protótipos iniciais — comece simples, adicione agentes quando necessário

## Padrões de Orquestração

### Sequential Pipeline

Agentes executam em sequência, output de um é input do próximo:

```python
async def sequential_pipeline(raw_input: str) -> MemoryItem:
    extracted = await extractor.extract(raw_input)
    validated = await validator.validate(extracted)
    consolidated = await consolidator.process(validated)
    stored = await storer.persist(consolidated)
    return stored
```

**Quando:** Dependências claras entre etapas. Cada step precisa do output completo do anterior.

### Parallel Fan-out/Fan-in

Múltiplos agentes processam em paralelo, resultado é mergeado:

```python
async def parallel_extraction(content: str) -> list[MemoryCandidate]:
    tasks = [
        extractor_fact.extract(content),
        extractor_decision.extract(content),
        extractor_insight.extract(content),
    ]
    results = await asyncio.gather(*tasks)
    return merge_and_deduplicate(results)
```

**Quando:** Sub-tarefas independentes. Tempo total = max(individual) ao invés de sum.

### Hierarchical (Orchestrator-Workers)

Orchestrator decomõe tarefa, workers executam, orchestrator sintetiza:

```python
class Orchestrator:
    async def process(self, task: ComplexTask) -> Result:
        subtasks = await self.decompose(task)
        
        assignments = self.assign_workers(subtasks)
        
        results = await asyncio.gather(*[
            worker.execute(subtask)
            for worker, subtask in assignments
        ])
        
        return await self.synthesize(results)
```

**Quando:** Tarefas complexas que requerem decomposição inteligente. Padrão Magentic-One (Microsoft).

### Evaluator-Optimizer Loop

Agent executa, evaluator avalia, feedback loop até qualidade aceitável:

```python
async def evaluator_optimizer(
    task, agent, evaluator, max_iterations=3, threshold=0.8
):
    result = await agent.execute(task)
    
    for i in range(max_iterations):
        evaluation = await evaluator.evaluate(result, task)
        if evaluation.score >= threshold:
            return result
        
        result = await agent.execute(
            task, feedback=evaluation.feedback, previous=result
        )
    
    return result
```

**Quando:** Qualidade é crítica e iteração melhora resultados significativamente. Padrão Anthropic.

## Specialized Agent Roles para TheSearch

### Extractor

Responsável por extrair structured data de conteúdo bruto:

```python
class ExtractorAgent:
    async def extract(self, content: str, context: dict) -> list[MemoryCandidate]:
        raw_extractions = await self.llm.extract(
            content,
            response_model=list[ExtractionResult],
            context=context,
        )
        return [
            MemoryCandidate(
                title=r.title,
                summary=r.summary,
                type=r.memory_type,
                confidence=r.confidence,
                source_content=content,
            )
            for r in raw_extractions
        ]
```

### Validator

Verifica qualidade e consistência das extrações:

```python
class ValidatorAgent:
    async def validate(self, candidate: MemoryCandidate) -> ValidationResult:
        checks = await asyncio.gather(
            self.check_schema(candidate),
            self.check_consistency(candidate),
            self.check_duplicates(candidate),
            self.check_project_relevance(candidate),
        )
        return ValidationResult(
            passed=all(c.passed for c in checks),
            score=min(c.score for c in checks),
            issues=[issue for c in checks for issue in c.issues],
        )
```

### Consolidator

Merge, promote, deprecate — operações de background:

```python
class ConsolidatorAgent:
    async def consolidate(self, scope: str = "all"):
        operations = [
            self.merge_duplicates(),
            self.recalculate_weights(),
            self.promote_proposed(),
            self.deprecate_stale(),
            self.synthesize_insights(),
        ]
        results = {}
        for op in operations:
            try:
                results[op.__name__] = await op()
            except Exception as e:
                results[op.__name__] = {"error": str(e)}
                await self.notify_failure(op.__name__, e)
        return results
```

### Retriever

Busca híbrida com reranking e diversificação:

```python
class RetrieverAgent:
    async def retrieve(self, query: str, project: str, top_k: int = 10):
        vector_results = await self.qdrant.search(query_embedding, project)
        graph_results = await self.neo4j.traverse(query_entities, project)
        
        fused = reciprocal_rank_fusion(
            vector_results, graph_results, k=60
        )
        
        diversified = mmr_diversify(fused, lambda_param=0.7)
        return diversified[:top_k]
```

## MCP como Protocolo Inter-Agent

MCP (Model Context Protocol) pode servir como protocolo de comunicação entre agentes:

```python
from mcp.server import FastMCP

memory_server = FastMCP("thesearch-agents")

@memory_server.tool()
async def extract_memories(content: str, project: str) -> list[dict]:
    """Extractor agent: extract memory candidates from content."""
    return await extractor.extract(content, project)

@memory_server.tool()
async def validate_memory(candidate_id: str) -> dict:
    """Validator agent: validate a memory candidate."""
    return await validator.validate(candidate_id)

@memory_server.tool()
async def retrieve_memories(query: str, project: str, top_k: int = 5) -> list[dict]:
    """Retriever agent: hybrid search across memory stores."""
    return await retriever.retrieve(query, project, top_k)
```

**Benefício MCP:** Agentes são desacoplados — qualquer cliente MCP pode invocar qualquer agente.

### A2A Protocol para Multi-Agent

Para coordenação entre agentes de diferentes sistemas, o A2A (Agent-to-Agent) Protocol oferece padrão aberto:

```python
# A2A: cada agente expõe sua "agent card"
{
    "name": "thesearch-extractor",
    "capabilities": ["extraction", "classification"],
    "input_schema": {...},
    "output_schema": {...},
}
```

**Quando A2A vs MCP:** MCP para tool-calling (agente → ferramenta). A2A para agent-to-agent (agente → agente autônomo).

## Event-Driven Coordination

Agentes comunicam via eventos para desacoplamento temporal:

```python
from dataclasses import dataclass
from enum import Enum

class EventType(Enum):
    MEMORY_CREATED = "memory.created"
    MEMORY_UPDATED = "memory.updated"
    MEMORY_DEPRECATED = "memory.deprecated"
    EXTRACTION_COMPLETED = "extraction.completed"
    VALIDATION_FAILED = "validation.failed"
    CONSOLIDATION_FINISHED = "consolidation.finished"

@dataclass
class Event:
    type: EventType
    payload: dict
    timestamp: datetime
    source: str

class EventBus:
    def __init__(self):
        self._handlers: dict[EventType, list[Callable]] = {}
    
    def subscribe(self, event_type: EventType, handler: Callable):
        self._handlers.setdefault(event_type, []).append(handler)
    
    async def publish(self, event: Event):
        for handler in self._handlers.get(event.type, []):
            try:
                await handler(event)
            except Exception as e:
                await self.dead_letter(event, e)
```

### Reactive Consolidation Pipeline

```python
bus = EventBus()

bus.subscribe(EventType.EXTRACTION_COMPLETED, on_extraction_completed)
bus.subscribe(EventType.VALIDATION_FAILED, on_validation_failed)
bus.subscribe(EventType.MEMORY_CREATED, trigger_consolidation_check)

async def on_extraction_completed(event: Event):
    result = await validator.validate(event.payload["candidate"])
    if result.passed:
        await bus.publish(Event(
            type=EventType.MEMORY_CREATED,
            payload={"candidate": event.payload["candidate"]},
            timestamp=datetime.utcnow(),
            source="validator",
        ))
    else:
        await bus.publish(Event(
            type=EventType.VALIDATION_FAILED,
            payload={"candidate_id": event.payload["candidate"].id, "issues": result.issues},
            timestamp=datetime.utcnow(),
            source="validator",
        ))
```

## Error Handling & Fallback

### Circuit Breaker por Agente

```python
class AgentCircuitBreaker:
    def __init__(self, agent, failure_threshold=3, recovery_timeout=300):
        self.agent = agent
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.last_failure = None
    
    async def execute(self, task):
        if self._is_open:
            return await self.fallback(task)
        try:
            result = await self.agent.execute(task)
            self.failure_count = 0
            return result
        except Exception:
            self.failure_count += 1
            self.last_failure = datetime.utcnow()
            if self.failure_count >= self.failure_threshold:
                return await self.fallback(task)
            raise
    
    @property
    def _is_open(self):
        if self.last_failure is None:
            return False
        elapsed = (datetime.utcnow() - self.last_failure).seconds
        if elapsed > self.recovery_timeout:
            self.failure_count = 0
            return False
        return self.failure_count >= self.failure_threshold
```

### Fallback Strategy Matrix

| Agente Falho | Fallback | Impacto |
|-------------|----------|---------|
| Extractor | Simple regex extraction | Menor qualidade |
| Validator | Skip validation, log warning | Risco controlado |
| Consolidator | Queue para próxima run | Sem impacto imediato |
| Retriever | Vector-only search (sem graph) | Resultados menos ricos |

## Common Mistakes

| Erro | Consequência | Correção |
|------|-------------|----------|
| Orquestração complexa demais para tarefa simples | Overhead > benefício | Comece com 1 agente, adicione quando necessário |
| Sem circuit breaker | Falha em cascata entre agentes | Circuit breaker por agente |
| Comunicação síncrona entre todos | Acoplamento temporal forte | Event-driven para desacoplar |
| Ignorar idempotência | Event replay causa duplicatas | Operações idempotentes por design |
| Sem dead letter queue | Eventos falhos são perdidos | DLQ para debugging |
| Orchestration em hot path | Latência insuportável | Orchestrate apenas em background |
| Agents compartilhando estado mutável | Race conditions, inconsistency | Estado imutável ou CQRS |

## Referências

- **AutoGen:** Wu et al., "Enabling Next-Gen LLM Applications via Multi-Agent Conversation" (2023) — knogdement/03
- **CrewAI:** CrewAI Documentation — knogdement/03
- **LangGraph:** LangGraph Documentation — knogdement/03
- **A2A Protocol:** Google, "Agent2Agent Protocol Specification" — knogdement/03
- **Magentic-One:** Microsoft Research, generalist multi-agent team — knogdement/03
- **Anthropic Agentic Patterns:** "Building Effective Agents" — orchestrator-workers, evaluator-optimizer
- **MCP:** Anthropic, Model Context Protocol — knogdement/03
