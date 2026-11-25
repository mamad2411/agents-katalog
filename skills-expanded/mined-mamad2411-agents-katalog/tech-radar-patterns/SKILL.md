---
name: tech-radar-patterns
description: ThoughtWorks Radar model, technology evaluation framework, ADR format, and stack compatibility analysis
---

# Tech Radar Patterns

## Radar Model (ThoughtWorks)

| Ring | Tanım | Aksiyon |
|------|-------|---------|
| **Adopt** | Production-ready, önerilen | Yeni projelerde varsayılan |
| **Trial** | Değer kanıtlanmış, pilot | Pilot projede dene |
| **Assess** | İlginç, araştır | PoC yap, değerlendir |
| **Hold** | Yeni projelerde KULLANMA | Mevcut kullanımı migre et |

## 4 Quadrant

| Quadrant | İçerik |
|----------|--------|
| Techniques | Practices, patterns, methodologies |
| Platforms | Infrastructure, cloud services |
| Tools | Development tools, frameworks |
| Languages & Frameworks | Programming languages, UI frameworks |

## Technology Evaluation Framework (8 Dimension)

```markdown
## Değerlendirme: [Technology Name]

| Dimension | Score (1-5) | Not |
|-----------|-------------|-----|
| Maturity | | Community, stability, releases |
| Community | | GitHub stars, SO activity, ecosystem |
| Performance | | Benchmarks, latency, throughput |
| Developer Experience | | Learning curve, docs, tooling |
| Security | | CVE history, audit, compliance |
| Scalability | | Horizontal/vertical scaling |
| Integration | | Mevcut stack ile uyum |
| Cost | | License, hosting, maintenance |

**Total Score:** /40
**Ring Recommendation:** Adopt/Trial/Assess/Hold
```

## Architecture Decision Record (ADR)

```markdown
# ADR-001: [Karar Başlığı]

## Status
Accepted | Proposed | Deprecated | Superseded by ADR-XXX

## Context
[Karar verilmesi gereken durum, kısıtlar, driver'lar]

## Decision
[Alınan karar ve gerekçesi]

## Consequences
### Positive
- [Fayda 1]
- [Fayda 2]

### Negative
- [Tradeoff 1]
- [Risk 1]

### Neutral
- [Etki 1]
```

## Stack Compatibility Check

```markdown
| Yeni Tech | Mevcut Stack | Uyumluluk | Risk |
|-----------|-------------|-----------|------|
| [Tech] | Node.js | Uyumlu | Düşük |
| [Tech] | PostgreSQL | Adapter var | Orta |
| [Tech] | Docker | Native support | Düşük |
| [Tech] | CI/CD | Plugin lazım | Orta |
```

## Migration Prioritization

| Kriter | Ağırlık | Score Yöntemi |
|--------|---------|--------------|
| Business impact | 30% | Revenue/user affected |
| Technical debt | 25% | Maintenance burden |
| Security risk | 25% | CVE severity |
| Migration effort | 20% | Engineering weeks |

## Checklist

- [ ] Her büyük tech kararı ADR ile documented
- [ ] Radar quarterly güncelleniyor
- [ ] Hold ring'deki tech'ler migration planında
- [ ] Yeni tech 8-dimension evaluation'dan geçmiş
- [ ] Stack compatibility check yapılmış
- [ ] PoC results documented
- [ ] License uygunluk kontrolü

## Anti-Patterns

- Resume-driven development (CV için tech seçimi)
- Shiny object syndrome (her yeni framework'u deneme)
- Evaluation'sız tech adoption
- ADR yazmadan büyük karar
- Hold'daki tech'i yeni projede kullanma
