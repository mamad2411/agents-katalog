# /sprint-plan — Analiz Raporlarından Sprint Planı

## Açıklama

Proje analiz raporlarını (`analysis/` klasörü) okuyarak sprint planı oluşturur ve task'lari `forge/sprints/sprint-{N}.json` dosyasina yazar.

## Kullanım

```
/sprint-plan                    # Tam akış: plan oluştur + sprint dosyasina yaz
/sprint-plan plan-only          # Sadece plan oluştur (dosyaya yazma yok)
/sprint-plan sync               # Mevcut sprint dosyasini planla senkronize et
```

## Ön koşul

- `analysis/` klasöründe en az 1 analiz raporu olmalı
- `analysis/MASTER_ANALYSIS.md` varsa öncelikli kaynak

## Akış

### 1. Proje bilgilerini tespit et

`projects.json` ve CLAUDE.md'den proje adini ve path'ini bul. Mevcut `forge/sprints/` altindaki en yuksek sprint numarasini tespit et; yeni sprint bir sonraki numaradir.

### 2. Analiz Raporlarını Oku

```
analysis/*.md dosyalarını oku (MASTER_ANALYSIS.md dahil)
Her rapordan:
  - "Kesin Olmalı" / "Kritik Eksikler" → P0/P1
  - "İyileştirme Önerileri" / "Kesin Değişmeli" → P1/P2
  - "Nice-to-Have" → P2/P3
  - Etki (High/Med/Low) ve Efor (S/M/L/XL) bilgilerini çıkar
```

### 3. Task Çıkarımı

Her bulgu/öneri için:
- **Kısa başlık** (task summary — max 80 karakter, İngilizce)
- **Açıklama** (Türkçe — ne/neden/nasıl + kabul kriterleri checkbox listesi)
- **Label** (security, perf, arch, ui, growth, analytics, data, content, monetization, a11y, seo)
- **Öncelik** (P0/P1/P2/P3)
- **Efor** S=1, M=2, L=3, XL=5 story point
- **Verify kriteri** (mekanik doğrulama komutu — test, curl, dosya varlığı kontrolü, lint)

### 4. Sprint Organizasyonu

| Sprint | Odak | SP Kapasitesi |
|--------|------|---------------|
| 1 | Security & Critical Fixes | 25-35 |
| 2 | Performance & Architecture | 25-35 |
| 3 | UX & Accessibility | 25-35 |
| 4 | Analytics & Growth | 25-35 |
| 5 | Monetization & ASO | 25-35 |

**Kurallar:**
- Sprint 1 daima güvenlik + acil P0 düzeltmelerle başlar
- P0 task'lar atandığı sprint'te kesinlikle yer alır
- Her sprint 2 haftalık

### 4b. Wave Dependency Graph

Sprint içindeki task'lar wave'lere ayrılır:
- Her task'a `depends_on: [KEY-xxx, KEY-yyy]` alanı eklenir
- Bağımlılığı olmayan task'lar Wave 1'e gider
- Bağımlılığı olan task'lar, bağımlılıkları tamamlanınca sonraki wave'e girer
- Wave içi task'lar paralel çalışır, wave'ler sıralı

Örnek:
```
Wave 1 (paralel): KEY-101, KEY-102, KEY-103
Wave 2 (paralel): KEY-104 (depends: 101), KEY-105 (depends: 102)
Wave 3: KEY-106 (depends: 104, 105)
```

SPRINT_PLAN.md'de her task'ın formatı:
```markdown
### KEY-101: Add rate limiting
- Priority: P1
- Effort: M (2 SP)
- Labels: security, backend
- Verify: `curl -w '%{http_code}' localhost:3000/api/test | grep 429`
- Depends: []
- Wave: 1
```

### 5. Doküman Oluştur

Çıktı: `analysis/SPRINT_PLAN.md`

Her task `verify:` alanını içermelidir — mekanik doğrulama komutu (test, curl, dosya varlığı kontrolü, lint). Verify eksik task SPRINT_PLAN.md'ye alınmaz.

### 6. Sprint Dosyasi

Her sprint icin `forge/sprints/sprint-{N}.json` yaz:

```json
{
  "sprint": 1,
  "epic": "Security & Critical Fixes",
  "tasks": [
    {
      "id": "T-001",
      "summary": "Rotate leaked API keys",
      "description": "Ne/neden/nasil + kabul kriterleri",
      "priority": "P0",
      "labels": ["security"],
      "points": 2,
      "verify": "npm run test:secrets",
      "status": "todo"
    }
  ]
}
```

Task ID'leri sprint icinde `T-001`'den baslar. `status` degerleri: `todo` | `in_progress` | `done`.

**Paralel çalışma:** 5 sprint → 5 agent paralel dosya yazabilir (her agent kendi sprint dosyasina).

## Notlar

- Task başlık: **İngilizce**
- Task açıklama + kullanıcı iletişim: **Türkçe**

## When NOT to Use
- Tek satirlik basit soru/cevap ise
- Skill'in scope'u disindaysa
- Riskli/destructive is ise (ayri onay gerekir)

## Red Flags
- Belirsiz hedef/kabul kriteri
- Gerekli dosya/izin/secret eksik
- Ayni adim 2+ kez tekrarlandi

## Error Handling
- Gerekli kaynak yoksa → dur, blocker'i raporla
- Komut/akıs hatasi → en yakin guvenli noktadan devam et
- 3 basarisiz deneme → daha uygun skill/agent'a yonlendir

## Verification
- [ ] Beklenen cikti uretildi
- [ ] Yan etki yok (dosya/ayar)
- [ ] Gerekli log/rapor paylasildi
