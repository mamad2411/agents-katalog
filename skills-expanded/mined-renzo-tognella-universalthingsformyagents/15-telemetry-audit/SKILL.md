---
name: Telemetry & Audit
description: Telemetria de uso, feedback loop para weight_usage/weight_feedback, auditoria de tool calls, structured logging, e métricas de qualidade.
---

# Telemetry & Audit

## Quando Usar

- Ao registrar eventos de uso de memória
- Ao implementar feedback loop para calibração de pesos
- Ao configurar auditoria de operações
- Ao analisar qualidade do sistema

## Eventos de Telemetria

| Evento | Trigger | Alimenta | Incremento |
|--------|---------|----------|:----------:|
| `retrieval` | Memória buscada | `weight_usage` | +0.01 |
| `acceptance` | Memória usada pelo agente | `weight_usage` | +0.05 |
| `rejection` | Memória ignorada | Calibração | Ajusta thresholds |
| `feedback` | Score explícito (0-1) | `weight_feedback` | EMA α=0.2 |
| `correction` | Memória corrigida | Política admissão | Calibra gates |

## Implementação

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class TelemetryEvent:
    event_type: str
    memory_id: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    context: dict = field(default_factory=dict)

class TelemetryService:
    def record_retrieval(self, memory_id: str): ...
    def record_acceptance(self, memory_id: str): ...
    def record_rejection(self, memory_id: str, reason: str = ""): ...
    def record_feedback(self, memory_id: str, score: float): ...
    
    def get_usage_stats(self, memory_id: str) -> dict:
        return {
            "total_retrievals": ...,
            "total_acceptances": ...,
            "total_rejections": ...,
            "avg_feedback": ...,
        }
```

## Feedback → Peso (EMA)

Exponential Moving Average para suavizar feedback:

```python
new_feedback = current_feedback * 0.8 + score * 0.2
```

- Score 1.0 repetido → feedback sobe gradualmente
- Score 0.0 repetido → feedback cai gradualmente
- Suaviza flutuações e evita volatilidade

## Auditoria

Toda operação MCP deve ser logada:

```python
class AuditService:
    def log_tool_call(self, tool_name: str, params: dict, result: dict):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": "tool_call",
            "tool": tool_name,
            "params": params,
            "result_status": result.get("status"),
        }
        self._write(entry)
    
    def log_memory_change(self, action: str, memory_id: str, changes: dict, rationale: str):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": "memory_change",
            "action": action,  # create, update, deprecate, weight_change
            "memory_id": memory_id,
            "changes": changes,
            "rationale": rationale,
        }
        self._write(entry)
```

### Formato: JSONL (MVP)

```jsonl
{"timestamp":"2026-03-25T15:00:00","type":"tool_call","tool":"memory_query","params":{"project":"CORE"},"result_status":"ok"}
{"timestamp":"2026-03-25T15:01:00","type":"memory_change","action":"create","memory_id":"abc123","changes":{"title":"X"},"rationale":"Nova regra"}
```

### Produção: Structured Logging

```python
import structlog

logger = structlog.get_logger()
logger.info("tool_call", tool="memory_query", project="CORE", result="ok")
```

## Regras

- TODA tool call MCP deve ter log de auditoria
- TODA mudança de memória (CRUD) deve ter rationale
- Telemetria é in-memory no MVP, persistida em produção
- JSONL para MVP (append-only, fácil de grep)
- Structured logging (structlog) para produção
- Nunca logar conteúdo sensível (payload completo)
