---
name: Weight System & Decay
description: Sistema de pesos compostos com 5 componentes, decadência exponencial (Ebbinghaus), configuração por categoria, e calibração adaptativa.
---

# Weight System & Decay

## Quando Usar

- Ao calcular ou recalcular effective_weight de memórias
- Ao configurar prioridades por categoria
- Ao implementar decadência temporal
- Ao calibrar coeficientes de peso

## Fórmula de Peso Efetivo

```python
effective_weight = (
    α × weight_manual +
    β × weight_confidence +
    γ × weight_usage +
    δ × weight_feedback +
    ε × weight_contextual
) × decay_factor
```

## Componentes de Peso

| Componente | Descrição | Fonte | Range |
|-----------|-----------|-------|:-----:|
| `weight_manual` | Importância definida por humano/arquiteto | Explícito | 0.0-1.0 |
| `weight_confidence` | Força da evidência | `min(evidence_count × 0.25, 1.0)` | 0.0-1.0 |
| `weight_usage` | Frequência de recuperação e uso | Telemetria | 0.0-1.0 |
| `weight_feedback` | Feedback explícito positivo/negativo | EMA | 0.0-1.0 |
| `weight_contextual` | Relevância para query atual | Runtime | 0.0-1.0 |

## Configuração por Categoria

| Categoria | α (manual) | β (confidence) | γ (usage) | δ (feedback) | ε (contextual) |
|-----------|:---:|:---:|:---:|:---:|:---:|
| DesignRule | **0.40** | 0.20 | 0.15 | 0.15 | 0.10 |
| BusinessRule | 0.20 | **0.35** | 0.20 | 0.15 | 0.10 |
| ArchitecturalDecision | **0.35** | 0.25 | 0.10 | 0.20 | 0.10 |
| DesignPattern | 0.25 | 0.25 | **0.25** | 0.15 | 0.10 |

**Lógica:**
- DesignRule: o arquiteto define (α alto)
- BusinessRule: evidência importa mais (β alto)
- ArchitecturalDecision: permanência + feedback (α + δ altos)
- DesignPattern: uso real valida (γ alto)

## Decadência Exponencial (Ebbinghaus)

```python
def calculate_decay(significance: float, last_accessed_at: datetime) -> float:
    days_since = (now() - last_accessed_at).days
    half_life = 30 + (significance * 335)
    return 0.5 ** (days_since / half_life)
```

| Significance | Half-Life | 50% decay em |
|:---:|:---:|:---:|
| 0.0 | 30 dias | 1 mês |
| 0.5 | 197 dias | ~6.5 meses |
| 1.0 | 365 dias | 1 ano |

**Memórias mais significativas decaem mais lentamente.**

## Atualização em Eventos

```python
# Após recuperação
weight_usage = min(current_usage + 0.05 if accepted else 0.01, 1.0)

# Após feedback
weight_feedback = current_feedback * 0.8 + score * 0.2  # EMA
```

## Regras

- Coeficientes (α, β, γ, δ, ε) são parâmetros configuráveis, NUNCA hardcoded como constantes mágicas
- Usar nomes descritivos: `manual_weight_factor` em vez de `alpha`
- Decay só se aplica se `last_accessed_at` existe
- Recalcular pesos na consolidação diferida (batch)
- Calibração adaptativa é meta futura — basear em dados reais de uso
- Soma dos coeficientes DEVE ser 1.0
