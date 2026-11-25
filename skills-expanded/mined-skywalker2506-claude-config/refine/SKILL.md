---
name: refine
description: CLAUDE.md, SKILL.md, settings.json ve diger config dosyalarini rafine et — global, project veya all kapsaminda.
argument-hint: "[global|project|all] [opus|sonnet|haiku]"
---

# /refine — Config & Docs Refiner

Claude Code konfigurasyonunu (CLAUDE.md, SKILL.md, settings.json, hooks, scripts) analiz edip rafine eder. Gereksiz tekrari siler, catismalari cozer, tutarsizliklari duzeltir, icerigi sikilastirir.

## Kullanim

```
/refine                → bulundugun projeyi rafine et (varsayilan = project)
/refine global         → ~/.claude/ + ~/Projects/ kok seviye config
/refine all            → global + ~/Projects/ altindaki TUM projeler
/refine sonnet         → bu projeyi sonnet ile
/refine all haiku      → her seyi haiku ile
```

## Arguman Ayristirma

```
$ARGUMENTS
```

**Kapsam:** `global` veya `all` kelimesi varsa o kapsam. Yoksa `project` (varsayilan).
**Model:** `opus`, `sonnet` veya `haiku` kelimesi varsa o model. Yoksa `opus`.

---

## Calisma Prensibi

### Ne yapar
- Gereksiz tekrari, olu icerigi, cakisan talimatlari tespit eder
- Dosyalari sikilastirir — anlam kaybetmeden boyutu kucultur
- Catisan MCP tanimlarini, permission'lari, hook'lari cozer
- Hardcoded proje referanslarini (path, key, ad) parametrik hale getirir
- Skill'lerde tekrarlanan sablonlari birlestirir veya isaretler
- settings.json tutarsizliklarini duzeltir
- Sonuclari diff olarak gosterir, kullanicidan onay alir, sonra uygular

### Ne yapmaz
- Yeni ozellik / skill / hook eklemez
- Mevcut davranisi degistirmez (sadece ayni seyi daha temiz ifade eder)
- Onaysiz dosya silmez
- Proje koduna (lib/, src/, test/) dokunmaz

---

## Kapsam Dosyalari

### `/refine global`

```
~/.claude/CLAUDE.md
~/.claude/settings.json
~/.claude/settings.local.json
~/.claude/mcp.json
~/.claude/skills/**/SKILL.md
~/Projects/CLAUDE.md
~/Projects/claude-config/projects/MIGRATION_GUIDE.md
~/Projects/claude-config/projects/MIGRATION_VERSION
~/Projects/claude-config/projects/PROJECT_ANALYSIS.md
~/Projects/claude-config/projects/scripts/*.sh
~/.claude/settings.json
~/.claude/settings.local.json
```

### `/refine project`

```
$(pwd)/CLAUDE.md
$(pwd)/.claude/settings.json
$(pwd)/.claude/settings.local.json
$(pwd)/.mcp.json
$(pwd)/.claude/skills/**/SKILL.md  (varsa)
$(pwd)/docs/CLAUDE*.md
$(pwd)/docs/*.md  (Claude/config ile ilgili olanlar)
$(pwd)/scripts/*.sh
$(pwd)/.env.example
$(pwd)/.github/workflows/*.yml
```

### `/refine all`

Global kapsam + `~/Projects/*/` altindaki her projenin project kapsami.

---

## Agent Akisi

Kapsamdaki dosyalari oku, analiz et, rapor sun, onay al, uygula.

### Adim 1 — Tarama (Agent)

Kapsamdaki tum dosyalari oku. Her dosya icin:

| Kontrol | Aciklama |
|---------|----------|
| **Tekrar** | Ayni kural/talimat birden fazla dosyada mi? Hangisi yetkili (single source of truth)? |
| **Catisma** | Iki dosya celisen sey mi soyluyor? (orn. model=opus vs model=sonnet) |
| **Hardcode** | Proje adi, path, Firebase ID gibi degerler sabitlendigi yerler |
| **Olu icerik** | Referans verdigi dosya/fonksiyon artik yok; gecmis karar; TODO/eski tarih |
| **Siskinlik** | Gereksiz uzun aciklama, ornek, tekrar; daha kisa yazilabilir |
| **MCP cakismasi** | Ayni MCP settings.json + mcp.json + .mcp.json'da farkli config ile |
| **Permission tutarsizligi** | allow + ask'ta ayni pattern; deny bos ama ask'ta olmasi gereken var |
| **Hook tekrari** | Ayni hook global + proje seviyesinde |
| **Skill tekrari** | Birden fazla skill neredeyse ayni prompt ile (parametrik olmali) |

### Adim 2 — Rapor

Tarama sonucunu kullaniciya sun:

```
## Refine Raporu — [KAPSAM]

### Ozet
- Taranan dosya: N
- Tespit: N bulgu (K kritik, O orta, B bilgi)

### Bulgular

#### 1. [SEVIYE] Baslik
- **Dosya(lar):** path1, path2
- **Sorun:** ...
- **Oneri:** ...
- **Diff onizleme:**
  ```diff
  - eski satir
  + yeni satir
  ```

#### 2. ...

### Uygulanacak Degisiklikler Ozeti
| # | Dosya | Degisiklik | Geri alinabilir |
|---|-------|-----------|-----------------|
| 1 | ~/.claude/CLAUDE.md | 45 satir → 28 satir | Evet |
| ...
```

### Adim 3 — Onay

```
Bu degisiklikleri uygulamak ister misin?
  [E] Evet, hepsini uygula
  [K] Kismi — numara ile sec (orn. 1,3,5)
  [H] Hayir, sadece raporu kaydet
```

### Adim 4 — Uygulama

Onaylanan degisiklikleri Edit tool ile uygula. Her dosya icin:
1. Degisiklik oncesi yedek: degisiklik buyukse (>50 satir fark) `.backup/refine_<tarih>/` altina kopyala
2. Edit uygula
3. Dogrulama: degisiklik sonrasi dosya gecerli mi (JSON parse, markdown lint vb.)

### Adim 5 — Ozet

```
## Refine Tamamlandi

- Degistirilen: N dosya
- Silinen satir: X | Eklenen satir: Y | Net: Z
- Yedek: .backup/refine_YYYYMMDD/ (buyuk degisiklikler)

Geri almak icin: git checkout -- <dosya> veya yedekten geri yukle.
```

---

## `/refine all` Ozel Kurallari

`all` kapsaminda once global, sonra her proje sirayla islenir. Projeler arasi tutarlilik da kontrol edilir:

| Kontrol | Ornek |
|---------|-------|
| Proje settings.json'da enabledMcpjsonServers var mi? | Eksikse uyar |
| Proje CLAUDE.md global ile celisiyor mu? | Celisirse hangisi oncelikli belirt |
| Proje migration_version guncel mi? | Eski ise uyar (fix degil — /migration'in isi) |
| Projede gereksiz skill kopyasi var mi? | ~/.claude/skills/ varken proje icinde kopya |

**Onemli:** `/refine all` degisiklikleri toplu onaya sunar, tek tek proje icin ayri onay istemez (aksi halde 8 proje = 8 onay turu olur). Kullaniciya tek bir toplam rapor gosterir.

---

## Model Secimi

| Arguman | Kullanilan model |
|---------|-----------------|
| *(belirtilmemis)* | `opus` |
| `opus` | `opus` |
| `sonnet` | `sonnet` |
| `haiku` | `haiku` |

Agent tool `model` parametresi buna gore ayarlanir. Buyuk kapsam (all) + Opus = yuksek maliyet; kullaniciyi uyar ama engelleme.

---

## Ornek Kullanimlar

```
/refine                    → bu projeyi opus ile rafine et
/refine sonnet             → bu projeyi sonnet ile rafine et
/refine global             → global dosyalari opus ile rafine et
/refine global haiku       → global dosyalari haiku ile rafine et
/refine all                → her seyi opus ile rafine et
/refine all haiku          → her seyi haiku ile (hizli/ucuz tarama)
```

---

## Kisitlar

- Max 50 tool call (agent basina)
- Dosya silme onaysiz yapilmaz
- Proje kodu (lib/, src/, test/) kapsam disinda
- `/refine all` 10'dan fazla proje varsa ilk 10'u isler, kalanini raporlar
- JSON dosyalarda (settings.json, mcp.json) degisiklik sonrasi parse kontrolu zorunlu

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
