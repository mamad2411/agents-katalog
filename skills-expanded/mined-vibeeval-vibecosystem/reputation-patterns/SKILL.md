---
name: reputation-patterns
description: Agent reputation scoring, performance tier system, trust calibration, and task affinity matching
---

# Reputation Patterns

## Agent Reputation Score (ARS)

```typescript
interface AgentReputation {
  agentId: string
  score: number           // 0-100
  tier: 'S' | 'A' | 'B' | 'C' | 'D'
  totalTasks: number
  successRate: number     // 0-1
  firstPassRate: number   // QA'den ilk seferde geçme oranı
  avgRetries: number
  specialties: string[]   // Başarılı olduğu task tipleri
  weaknesses: string[]    // Başarısız olduğu task tipleri
}

// Score hesaplama
function calculateARS(agent: AgentReputation): number {
  const weights = {
    successRate: 0.35,
    firstPassRate: 0.25,
    consistency: 0.20,    // son 10 task varyansı
    efficiency: 0.20      // ortalama retry sayısı
  }

  return (
    agent.successRate * weights.successRate * 100 +
    agent.firstPassRate * weights.firstPassRate * 100 +
    (1 - agent.avgRetries / 3) * weights.consistency * 100 +
    (agent.totalTasks > 5 ? 1 : 0.5) * weights.efficiency * 100
  )
}
```

## Tier System

| Tier | ARS Range | Yetki | Açıklama |
|------|-----------|-------|----------|
| **S** | 90-100 | Otonom | Her task'ı alabilir, QA skip |
| **A** | 75-89 | Güvenilir | Çoğu task, standart QA |
| **B** | 60-74 | Normal | Standart task, tam QA |
| **C** | 40-59 | İzlemede | Basit task, sıkı QA |
| **D** | 0-39 | Kısıtlı | Cross-training gerekli |

## Decay & Recovery

```
Decay:
- 7 gün inaktif → -2 puan
- 14 gün inaktif → -5 puan
- QA FAIL → -5 puan (severity'ye göre)
- Escalation → -10 puan

Recovery:
- QA PASS (first try) → +3 puan
- QA PASS (retry) → +1 puan
- Complex task başarı → +5 puan
- Cross-training başarı → +2 puan
```

## Task-Type Affinity

```markdown
## Agent Affinity Matrix

| Agent | Frontend | Backend | DB | Security | Score |
|-------|----------|---------|----|---------|----|
| spark | 85 | 70 | 50 | 40 | B |
| kraken | 60 | 90 | 80 | 65 | A |
| frontend-dev | 95 | 30 | 20 | 30 | S(FE) |
| backend-dev | 20 | 92 | 75 | 60 | S(BE) |

Task assignment: Highest affinity agent with available capacity
```

## Reliability Prediction

```python
def predict_success(agent_id: str, task_type: str) -> float:
    """Agent'ın belirli task tipinde başarı olasılığı"""
    agent = get_agent(agent_id)
    base_rate = agent.success_rate
    type_affinity = agent.affinity.get(task_type, 0.5)
    recent_trend = agent.last_5_tasks_success_rate

    return (base_rate * 0.4 + type_affinity * 0.35 + recent_trend * 0.25)
```

## Canavar Integration

```bash
# Skill matrix'ten data çek
cat ~/.claude/canavar/skill-matrix.json | jq '.agents[] | {name, score, tier}'

# Error ledger'dan failure pattern
cat ~/.claude/canavar/error-ledger.jsonl | jq 'select(.agent == "spark")'

# Leaderboard
node ~/.claude/hooks/dist/canavar-cli.mjs leaderboard
```

## Checklist

- [ ] Her agent'ın ARS score'u tracked
- [ ] Tier assignment otomatik
- [ ] Decay/recovery mekanizması aktif
- [ ] Task-type affinity matrisi var
- [ ] Reliability prediction kullanılıyor
- [ ] Cross-training plan (D-tier agent'lar için)
- [ ] Canavar error-ledger entegre

## Anti-Patterns

- Tüm agent'lara eşit güvenme (reputation'a bak)
- Low-tier agent'a kritik task verme
- Score'u sadece success/fail'e dayandırma (context önemli)
- Recovery yolu olmayan punishment
