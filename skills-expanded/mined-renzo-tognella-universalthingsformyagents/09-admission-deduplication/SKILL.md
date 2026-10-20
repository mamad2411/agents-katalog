---
name: Admission & Deduplication
description: Política de admissão inteligente com 5 gates sequenciais, deduplicação por similaridade vetorial, e fluxo de decisão para candidatos de memória.
---

# Admission & Deduplication

## Quando Usar

- Ao processar candidatos de memória para admissão
- Ao ajustar thresholds de similaridade
- Ao implementar novos gates ou regras de admissão

## Conceito Fundamental

> **Nada entra direto na memória final.**

```
dado bruto → candidato → gates de admissão → memória canônica ✅
dado bruto → embedding → memória final      ❌ POLUI O SISTEMA
```

## Os 5 Gates

```
MemoryCandidate
  │
  ├─ Gate A: tem project? ─── NÃO → ❌ rejected
  │
  ├─ Gate B: tem evidence? ── NÃO → 📎 evidence_only
  │
  ├─ Gate C: é similar a existente?
  │   ├─ score ≥ 0.92 ────── SIM → 🔄 update (atualiza existente)
  │   ├─ score 0.80-0.92 ─── SIM → 🔗 refine (cria com REFINES)
  │   └─ score < 0.80 ────── NÃO → continua...
  │
  ├─ Gate D: peso ≥ 0.3? (ou ADR?) ── NÃO → ❌ rejected
  │
  └─ ✅ ADMITIDO → create nova memória
```

## Thresholds

| Threshold | Valor | Significado |
|-----------|:-----:|------------|
| `SIMILARITY_THRESHOLD` | 0.92 | Score acima = duplicata (atualiza) |
| `REFINEMENT_THRESHOLD` | 0.80 | Score entre 0.80-0.92 = refinamento |
| `MIN_WEIGHT_DEFAULT` | 0.30 | Peso mínimo para admissão |

## Gate C — Deduplicação Vetorial

```python
text = f"{candidate.title} | {candidate.summary}"
embedding = await embeddings.embed(text)
similar = qdrant.find_similar(
    embedding, candidate.project, candidate.type, threshold=0.92
)
```

### Decisões do Gate C

| Score | Ação | Relação no Grafo |
|:-----:|------|:----------------:|
| ≥ 0.92 | Update existente (merge) | Nenhuma |
| 0.80-0.92 | Criar novo + link | `REFINES` |
| < 0.80 | Considerar novo | — |

## Estados de Saída

| Status | Significado | Ação |
|--------|------------|------|
| `rejected` | Não passou nos gates | Descartado |
| `evidence_only` | Sem valor de memória | Salva como evidência |
| `proposed` | Aceito, aguarda confirmação | Pendente de promoção |
| `active` | Memória canônica ativa | Persistido |
| `deprecated` | Substituída por versão nova | Marcado DEPRECATES |

## Padrão Chain of Responsibility (Recomendado)

Para extensibilidade, cada gate pode ser uma classe:

```python
from abc import ABC, abstractmethod

class AdmissionGate(ABC):
    def __init__(self, next_gate: "AdmissionGate | None" = None):
        self.next_gate = next_gate
    
    @abstractmethod
    async def evaluate(self, candidate) -> AdmissionResult | None:
        ...
    
    async def handle(self, candidate) -> AdmissionResult:
        result = await self.evaluate(candidate)
        if result:
            return result
        if self.next_gate:
            return await self.next_gate.handle(candidate)
        return AdmissionResult("active", "create", reason="Passed all gates")

class ProjectGate(AdmissionGate):
    async def evaluate(self, candidate):
        if not candidate.project:
            return AdmissionResult("rejected", "reject", reason="Sem projeto")
        return None

# Montar chain
chain = ProjectGate(EvidenceGate(DuplicateGate(WeightGate())))
result = await chain.handle(candidate)
```

## Regras

- A ordem dos gates importa: Projeto → Evidência → Duplicata → Peso
- ADRs (ArchitecturalDecision) bypass o Gate D de peso mínimo
- Similar ≥ 0.92 SEMPRE atualiza, nunca cria duplicata
- evidence_only = informação útil mas não canônica
- Thresholds são configuráveis e devem ser calibrados com dados reais
