# Web Researcher Skill

SENTIENT'nın derin web araştırma yeteneği.

## Özellikler

Bu skill, MindSearch'ın multi-source araştırma pattern'i ve browser-use'ın web otomasyonundan adapte edilmiştir.

### Araştırma Süreci

```
┌─────────────────────────────────────────────────────┐
│  1. Query Decomposition (Sorgu Ayrıştırma)         │
│     └─> Ana sorgu → Alt sorular                    │
├─────────────────────────────────────────────────────┤
│  2. Parallel Search (Paralel Arama)                │
│     └─> Web + Academic + News eşzamanlı            │
├─────────────────────────────────────────────────────┤
│  3. Source Validation (Kaynak Doğrulama)           │
│     └─> Cross-reference + Fact-check               │
├─────────────────────────────────────────────────────┤
│  4. Synthesis (Sentez)                             │
│     └─> AI-powered içerik birleştirme              │
├─────────────────────────────────────────────────────┤
│  5. Report Generation (Rapor Oluşturma)           │
│     └─> Markdown/JSON/PDF çıktı                    │
└─────────────────────────────────────────────────────┘
```

### Desteklenen Kaynaklar

| Kaynak | Açıklama | Limit |
|--------|----------|-------|
| Web | SearXNG üzerinden genel web araması | ∞ |
| Academic | Google Scholar, arXiv, PubMed | 100/gün |
| News | Güncel haber kaynakları | 500/gün |
| Social | Twitter/X, Reddit (opsiyonel) | 1000/gün |

### Kullanım

```bash
# Temel araştırma
sentient skill run web-researcher --query "Rust async programming best practices"

# Derin araştırma
sentient skill run web-researcher \
  --query "quantum computing applications in finance" \
  --depth 5 \
  --sources web,academic,news \
  --output_format pdf
```

### Tarayıcı Entegrasyonu

browser-use pattern'i ile:
- Dinamik JavaScript sayfalarını işleyebilir
- Form doldurma ve oturum yönetimi
- CAPTCHA çözümü (external)
- Screenshot ve PDF export

### Örnek Çıktı

```markdown
# Araştırma Raporu: Rust Async Programming

## Yürütücü Özeti
Rust'ın async/await modeli, zero-cost abstractions ile...

## Metodoloji
- 45 kaynak tarandı
- 12 akademik makale
- 33 blog/article

## Bulgular
1. Tokio runtime en yaygın seçim (%78)
2. Async_trait makrosu yaygın kullanım
...

## Kaynaklar
[1] Tokio Documentation - https://tokio.rs/...
[2] Rust Async Book - https://rust-lang.github.io/...

## Öneriler
- Yeni projelerde Tokio 1.x kullanın
- async_trait yerine native async trait (Rust 1.75+)
```

## Teknik Detaylar

- **Browser Backend**: Lightpanda (9x az RAM)
- **Search Engine**: SearXNG (self-hosted)
- **PDF Processing**: docling/lopdf
- **Rate Limiting**: Token bucket algoritması

---
*SENTIENT - The She-Wolf That Guards Your Empire*
