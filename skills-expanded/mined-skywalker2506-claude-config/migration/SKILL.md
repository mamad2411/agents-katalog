# /migration — Bullet-Proof Project Setup & Health Check

## Açıklama

Proje kurulumunu doğrular, eksikleri tespit eder, düzeltir veya 60 saniye içinde kullanıcıya raporlar. 
Version checking + service health check + auto-recovery. Hiçbir zaman 2 dakikadan fazla döngüye girmez.

## Kullanım

```
/migration              # Tam kurulum + health check
/migration health       # Sadece health check (dosya oluşturmaz)
/migration setup        # Sadece kurulum (sıfırdan setup wizard)
/migration fix          # Tespit edilen sorunları otomatik düzelt
```

## Tetikleme

Bu skill iki şekilde tetiklenir:
1. **Otomatik:** `migration_check.sh` hook'u `MIGRATION_NEEDED` veya `MIGRATION_UPDATE` sinyali verdiğinde
2. **Manuel:** Kullanıcı `/migration` yazınca

## Süre Kısıtları (BULLET-PROOF)

| Aşama | Max Süre | Timeout Davranışı |
|-------|----------|-------------------|
| Version check | 5 sn | Atla, health check'e geç |
| MCP health check | 30 sn | MCP'yi "dead" işaretle, fallback öner |
| Dosya oluşturma | 60 sn | Tamamlananları kaydet, kalanları listele |
| **TOPLAM** | **2 dakika** | Kullanıcıya özet rapor ver, dur |

**KRİTİK KURAL:** Bu skill 2 dakikadan fazla çalışamaz. Timeout'ta ne durumda olursa olsun dur ve rapor ver.

---

## Akış

### Aşama 0 — Ortam Tespiti (5 sn)

```bash
# 1. Migration versiyonları
MASTER=$(cat __PROJECTS_ROOT__/MIGRATION_VERSION 2>/dev/null | tr -d '[:space:]')
PROJECT=$(cat .claude/migration_version 2>/dev/null | tr -d '[:space:]')

# 2. Proje tipi tespit
# package.json → Node/React/Next
# pubspec.yaml → Flutter
# Cargo.toml → Rust
# go.mod → Go
# pyproject.toml / requirements.txt → Python
```

Sonuç: `VERSION_STATUS` = `FRESH` | `OUTDATED` | `CURRENT`

### Aşama 1 — MCP Health Check (30 sn)

**Her MCP için şu kontrolleri yap:**

| MCP | Kontrol Yöntemi | Sağlıklı Kriteri |
|-----|-----------------|-------------------|
| `atlassian` | ToolSearch "atlassian" → tool var mı? | En az 1 atlassian tool bulunur |
| `github` | ToolSearch "github" → tool var mı? | En az 1 github tool bulunur |
| `git` | ToolSearch "git" → tool var mı? | git tool bulunur |
| `firebase` | ToolSearch "firebase" → tool var mı? | firebase tool bulunur |
| `context7` | ToolSearch "context7" → tool var mı? | context7 tool bulunur |
| `jcodemunch` | ToolSearch "jcodemunch" → tool var mı? | jcodemunch tool bulunur |

**Ek kontroller:**
- `~/.claude/settings.json` → `mcpServers` içinde tanımlı mı?
- `.claude/settings.json` → `enabledMcpjsonServers` içinde listelenmiş mi?
- `~/.claude/mcp.json` → çakışma var mı? (aynı MCP farklı config ile tanımlıysa UYAR)

**MCP çakışma tespiti (ÖNEMLİ):**
```
~/.claude/settings.json → mcpServers.atlassian  (KAYNAK A)
~/.claude/mcp.json → mcpServers.atlassian       (KAYNAK B)
.mcp.json → mcpServers.atlassian                (KAYNAK C)

Aynı MCP 2+ kaynakta farklı config ile tanımlıysa → UYAR + hangisinin doğru olduğunu sor
```

### Aşama 2 — Dosya Health Check (15 sn)

| Dosya | Kontrol | Yoksa |
|-------|---------|-------|
| `CLAUDE.md` | Var mı? İçi boş mu? | MIGRATION_GUIDE.md'den şablon oluştur |
| `.claude/settings.json` | `enabledMcpjsonServers` var mı? | MIGRATION_GUIDE.md'den şablon oluştur |
| `.claude/migration_version` | Master ile eşleşiyor mu? | Setup wizard başlat veya delta uygula |
| `.gitignore` | Var mı? `.env` dahil mi? | Framework'e göre oluştur |
| `.env.example` | Var mı? (Firebase vb. servis kullanıyorsa) | Şablon oluştur |

### Aşama 3 — Karar Matrisi

```
Her sorun için:
  SORUN_TIPI = "auto_fix" | "user_action" | "skip"

  auto_fix:
    - Eksik .gitignore → oluştur
    - Eksik .claude/settings.json → şablon oluştur
    - enabledMcpjsonServers eksik → ekle
    - migration_version eski → MIGRATION_GUIDE.md delta uygula
    - MCP çakışması → yanlış kaynağı temizle

  user_action:
    - MCP OAuth tamamlanmamış → "! npx mcp-remote..." komutu ver
    - API token eksik → token alma URL'si ver
    - Credentials placeholder → kullanıcıya doldurmasını söyle

  skip:
    - Kullanmadığı servis (orn. Firebase yok)
    - İsteğe bağlı dosyalar
```

### Aşama 4 — Rapor

**Her durumda** (başarılı veya başarısız) şu formatı kullan:

```
## Migration Raporu — [PROJE_ADI]

### Versiyon
- Master: X.X | Proje: Y.Y | Durum: ✅ Güncel / ⚠️ Eski / 🆕 Yeni

### MCP Durumu
| MCP | Config | Bağlantı | Aksiyon |
|-----|--------|----------|---------|
| atlassian | ✅ settings.json | ❌ Tool yok | OAuth tamamla: `! npx ...` |
| github | ✅ settings.json | ✅ Çalışıyor | - |
| ...

### Dosyalar
| Dosya | Durum | Aksiyon |
|-------|-------|---------|
| CLAUDE.md | ✅ Var | - |
| .claude/settings.json | ⚠️ enabledMcpjsonServers eksik | ✅ Eklendi |
| ...

### Kullanıcı Aksiyonu Gereken
1. Atlassian OAuth: `! npx -y mcp-remote@latest https://mcp.atlassian.com/v1/mcp`
2. ...

### Otomatik Düzeltilen
1. .gitignore oluşturuldu
2. ...
```

---

## MIGRATION_GUIDE.md Referansı

Setup wizard çalıştırırken `__PROJECTS_ROOT__/MIGRATION_GUIDE.md` dosyasını oku:
- **Bölüm 0:** İnteraktif Setup Wizard (yeni proje)
- **Changelog:** Delta adımları (güncelleme)
- **Bölüm 2-12:** Servis-spesifik şablonlar

---

## Anti-Pattern Korumaları

Bu skill aşağıdaki hataları **önler:**

### 1. MCP Yokken Döngüye Girme
```
YANLIŞ: MCP yok → "MCP kurun" de → kullanıcı /sprint-plan → "MCP yok" → tekrarla
DOĞRU:  MCP yok → alternatif öner (curl/script) → hemen ilerle
```

### 2. Credentials Placeholder Bırakma
```
YANLIŞ: Config dosyası yaz, içine "BURAYA_YAZIN" koy → kullanıcı doldurmaz → çalışmaz
DOĞRU:  Config dosyasındaki tüm placeholder'ları tespit et → kullanıcıya tek mesajda listele
```

### 3. Yanlış Paketi Kurma
```
YANLIŞ: settings.json'da mcp-remote var → mcp.json'a mcp-atlassian (PyPI) koy → çakışma
DOĞRU:  Önce settings.json oku → mevcut config'i anla → çakışma yaratma
```

### 4. Sessiz Hata Yutma
```
YANLIŞ: hook: "bash script 2>/dev/null || true" → hata görünmez
DOĞRU:  Hata çıktısını yakala, rapor et, sonra devam et
```

### 5. İş Yapmadan Seçenek Listesi Sunma
```
YANLIŞ: "3 seçenek var, hangisini istersiniz?" × 5 tur
DOĞRU:  En pratik seçeneği seç, yap, sonra söyle. Seçim ancak geri alınamaz konularda.
```

---

## Fallback Zinciri (MCP Yoksa)

Bir MCP bağlı değilse, o servisi kullanan skill'ler şu sırayla dener:

```
1. MCP tool çağrısı → başarılı → devam
2. REST API (curl) → credentials varsa → devam  
3. Script oluştur → kullanıcı credentials ekleyip çalıştırır
4. Kullanıcıya raporla → "Bu servis şu an kullanılamıyor, şunu yapman lazım: ..."
```

**Her adım max 30 sn.** Timeout'ta bir sonraki adıma geç.

---

## Projeye Özel Olmayan (Global)

Bu skill `~/.claude/skills/migration/` altındadır. Tüm projelerde `/migration` komutu ile çağrılabilir.

Proje-spesifik bilgileri (framework, servisler) CLAUDE.md veya setup wizard'dan alır — skill dosyasına hardcode etmez.

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
