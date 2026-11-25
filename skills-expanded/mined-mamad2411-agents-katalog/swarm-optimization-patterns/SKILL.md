---
name: swarm-optimization-patterns
description: Multi-agent coordination, critical path method, dependency DAG, and agent allocation optimization
---

# Swarm Optimization Patterns

## Critical Path Method (CPM)

```
Task A (3min) ─┐
               ├── Task D (5min) ── Task F (2min)
Task B (2min) ─┘        │
                         └── Task E (3min) ── Task G (1min)
Task C (4min) ─────────────────────────────── Task H (2min)

Critical Path: C → H = 6min (longest path)
Zero-slack: C, H (gecikme tüm timeline'ı etkiler)
```

## Dependency DAG Construction

```typescript
interface TaskNode {
  id: string
  agent: string
  estimatedMinutes: number
  dependencies: string[]  // task IDs
  priority: 'critical' | 'high' | 'medium' | 'low'
}

// Topological sort ile execution order
function buildExecutionPlan(tasks: TaskNode[]): TaskNode[][] {
  const layers: TaskNode[][] = []
  const completed = new Set<string>()

  while (completed.size < tasks.length) {
    const ready = tasks.filter(t =>
      !completed.has(t.id) &&
      t.dependencies.every(d => completed.has(d))
    )
    layers.push(ready)  // Bu layer paralel çalışabilir
    ready.forEach(t => completed.add(t.id))
  }
  return layers
}
```

## Agent Allocation Strategy

| Strateji | Ne Zaman | Nasıl |
|----------|----------|-------|
| Specialization | Uzman agent var | Task → matching agent |
| Load Balancing | Eşit workload | Round-robin + capacity |
| Priority-Based | Critical path | Zero-slack task'lara öncelik |
| Affinity | Context reuse | Aynı dosyaları kullanan task'lar aynı agent'a |

## Bottleneck Detection

```markdown
## Bottleneck Tipleri

| Tip | Tespit | Çözüm |
|-----|--------|-------|
| Resource Contention | Aynı dosya birden fazla agent | Sıralı execute veya lock |
| QA Queue | Review bekleyen task yığılması | Paralel reviewer |
| Dependency Chain | Uzun sıralı bağımlılık | Task decomposition |
| Agent Failure | Tekrarlayan fail | Fallback agent, reassign |
```

## Parallel Execution Rules

```
BAĞIMSIZ task'lar → PARALEL
  - Farklı dosyalarda çalışan
  - Birbirine bağımlı olmayan
  - Farklı concern'ler (frontend + backend)

BAĞIMLI task'lar → SIRALI
  - Aynı dosyada çalışan
  - Output → Input ilişkisi olan
  - Schema → Code → Test zinciri
```

## Phase Transition Criteria

| Phase | Geçiş Kriteri |
|-------|--------------|
| Keşif → Geliştirme | Plan onaylandı, task'lar tanımlı |
| Geliştirme → Review | Tüm task'lar QA'den geçti |
| Review → Düzeltme | Review feedback var |
| Düzeltme → Final | Tüm feedback resolved |

## Amdahl's Law

```
Speedup = 1 / ((1-P) + P/N)

P = parallelizable fraction
N = number of agents

Örnek: %80 parallel, 5 agent
Speedup = 1 / (0.2 + 0.8/5) = 1/0.36 = 2.78x
```

## Checklist

- [ ] Dependency DAG oluşturulmuş
- [ ] Critical path tespit edilmiş
- [ ] Paralel task'lar paralel assign
- [ ] Bottleneck detection aktif
- [ ] Agent-task affinity uygun
- [ ] Phase transition kriterleri tanımlı
- [ ] Fallback agent'lar belirlenmiş

## Anti-Patterns

- Tüm task'ları sıralı çalıştırma
- Bağımlı task'ları paralel çalıştırma (conflict)
- Her task'a ayrı agent (overhead)
- Critical path'i optimize etmemek
- Agent fail sonrası retry etmemek
