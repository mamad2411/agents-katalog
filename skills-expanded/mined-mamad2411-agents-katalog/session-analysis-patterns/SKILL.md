---
name: session-analysis-patterns
description: Claude Code session analysis, tool call patterns, efficiency metrics, and anti-pattern detection
---

# Session Analysis Patterns

## Session Metrics

| Metrik | İyi | Orta | Kötü |
|--------|-----|------|------|
| Tokens per task | <50K | 50-100K | >100K |
| Tool calls per task | <20 | 20-40 | >40 |
| Repeated reads | 0-1 | 2-3 | >3 |
| Blind edits | 0 | 1 | >1 |
| Agent spawn efficiency | >80% useful | 50-80% | <50% |

## Anti-Pattern Catalog

| # | Pattern | Tespit | Fix |
|---|---------|--------|-----|
| 1 | **Repeated Read** | Aynı dosya 3+ kez okunmuş | Bilgiyi ilk seferde kaydet |
| 2 | **Wide Grep** | Pattern'siz geniş arama | Spesifik pattern + glob filter |
| 3 | **Blind Edit** | Dosya okumadan edit | Read → Edit sırası zorunlu |
| 4 | **Idle Agent** | Agent spawn edilip sonuç kullanılmamış | Gereksiz spawn etme |
| 5 | **Cascade Fail** | Aynı hata 3+ kez retry | Root cause analiz et |
| 6 | **Context Pollution** | Ana context'te gereksiz büyük dosya okuma | Agent'a delege et |
| 7 | **Premature Agent** | Basit iş için agent spawn | Direkt tool kullan |
| 8 | **Missing Parallel** | Bağımsız işler sıralı | Paralel agent/tool call |
| 9 | **Over-Engineering** | Basit fix için büyük refactoring | Minimal değişiklik |

## Efficiency Scorer (0-100)

```python
def calculate_efficiency(session):
    score = 100

    # Penalties
    score -= session.repeated_reads * 5       # -5 per repeated read
    score -= session.blind_edits * 15         # -15 per blind edit
    score -= session.wide_greps * 3           # -3 per wide grep
    score -= session.idle_agents * 10         # -10 per idle agent
    score -= session.cascade_fails * 8        # -8 per cascade fail

    # Bonuses
    score += session.parallel_calls * 2       # +2 per parallel batch
    score += session.first_pass_success * 5   # +5 per first-try success

    return max(0, min(100, score))
```

## Session Comparison

```markdown
| Metrik | Session A | Session B | Delta |
|--------|-----------|-----------|-------|
| Total tokens | 45,000 | 120,000 | +167% |
| Tool calls | 12 | 38 | +217% |
| Time (min) | 3 | 12 | +300% |
| Tasks completed | 2 | 2 | 0% |
| Efficiency score | 88 | 42 | -52% |
```

## Braintrust Log Analysis

```bash
# Session analizi
btca sessions list --last 7d
btca session <id> --metrics

# Pattern detection
btca session <id> --anti-patterns

# Cost analysis
btca sessions list --sort cost --desc
```

## Checklist

- [ ] Session token usage tracked
- [ ] Anti-pattern detection aktif
- [ ] Efficiency score > 70
- [ ] Repeated reads < 2
- [ ] Blind edits = 0
- [ ] Parallel opportunities exploited
- [ ] Agent spawn ROI positive

## Anti-Patterns

- Her session'ı analiz etmek (sadece outlier'ları analiz et)
- Metric'lere takılıp task quality'yi ihmal etmek
- Hız için correctness'tan ödün vermek
