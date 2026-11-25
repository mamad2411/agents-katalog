# Competitor Analyzer Skill

SENTIENT'nın rekabet analizi yeteneği.

## Özellikler

Bu skill, agency-agents'ın persona pattern'inden ve MindSearch'ın derin araştırma metodolojisinden adapte edilmiştir.

### Analiz Boyutları

| Boyut | Açıklama | Çıktı |
|-------|----------|-------|
| **Features** | Özellik karşılaştırması | Feature matrix |
| **Pricing** | Fiyat analizi | Pricing table |
| **Market** | Pazar konumu | Market share data |
| **Strengths** | Güçlü yönler | Strengths list |
| **Weaknesses** | Zayıf yönler | Weaknesses list |

### SWOT Analizi

```
┌─────────────────────────────────────────────────────┐
│                    SWOT MATRIX                      │
├──────────────────────┬──────────────────────────────┤
│   STRENGTHS          │   WEAKNESSES                 │
│   • ...              │   • ...                      │
│   • ...              │   • ...                      │
├──────────────────────┼──────────────────────────────┤
│   OPPORTUNITIES      │   THREATS                    │
│   • ...              │   • ...                      │
│   • ...              │   • ...                      │
└──────────────────────┴──────────────────────────────┘
```

### Kullanım

```bash
# Temel analiz
sentient skill run competitor-analyzer --target "Notion"

# Derin analiz
sentient skill run competitor-analyzer \
  --target "Linear" \
  --aspects features,pricing,market \
  --depth 5
```

### Örnek Çıktı

```markdown
# Rakip Analiz: Linear

## Yürütücü Özeti
Linear, modern yazılım ekipleri için tasarlanmış bir proje yönetim aracı...

## Özellik Karşılaştırması
| Özellik | Linear | Jira | Asana |
|---------|--------|------|-------|
| Sprint Planning | ✅ | ✅ | ✅ |
| Time Tracking | ❌ | ✅ | ❌ |

## Fiyat Analizi
- Free: $0 (5 kullanıcıya kadar)
- Standard: $8/kullanıcı/ay
- Plus: $14/kullanıcı/ay

## SWOT Analizi
**Strengths:** Hızlı UI, keyboard shortcuts, git entegrasyonu
**Weaknesses:** Zaman takibi yok, raporlama zayıf
**Opportunities:** Enterprise market, AI features
**Threats:** Jira'yı kullanan büyük şirketler

## Öneriler
1. Zaman takibi özelliği eklenmeli
2. Enterprise segment'e odaklanılmalı
```

---
*SENTIENT - The She-Wolf That Guards Your Empire*
