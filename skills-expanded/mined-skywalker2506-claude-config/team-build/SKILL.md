---
name: team-build
description: "Multi-agent takım oluştur: Opus tasarlar, agy (Gemini) kodlar, loop ile otonom çalışır. Triggers: team build, takım kur, agent takımı, multi-agent."
user-invocable: true
argument-hint: "[setup|run|status]"
---

# Team Build — Multi-Agent Otonom Geliştirme

> Model yonlendirmesi: global/model-routing.md

Opus agent'lar tasarlar + plan yazar, agy (Gemini) agent'lar kodlar. Loop ile otonom çalışır, her turda commit+push yapar, raporlar üretir.

## Akış

```
Setup → Opus Spec → Loop [ agy (Gemini) Kod → Commit+Push → Opus Review → Sonraki Tur ]
```

## Argümanlar

| Arg | Ne yapar |
|-----|----------|
| *(boş)* veya `setup` | Soru sor → config oluştur → spec yaz → loop başlat |
| `run` | Mevcut config ile loop'u başlat (setup zaten yapılmış) |
| `status` | Mevcut durumu göster (tamamlanan agent'lar, kalan turlar) |

## Çalıştırılınca

Argümana göre aşağıdaki fazlardan birini başlat:

---

## Faz 1: Setup (interaktif — sadece ilk kez)

Kullanıcıya şu soruları sor (cevap yoksa parantez içi varsayılanı kullan):

### Sorular

1. **Proje türü nedir?**
   - Web sitesi / Mobil uygulama / Oyun / CLI aracı / API / Diğer
   - *(Bu cevap agent alanlarını önerecek)*

2. **Projenin kısa açıklaması?**
   - 1-2 cümle (ör: "Güven odaklı proje eşleştirme platformu")

3. **Hangi alanlarda agent istiyorsun?**
   - Proje türüne göre öneriler sun, kullanıcı ekleyip çıkarabilir
   - Varsayılan öneriler:

   | Proje Türü | Önerilen Alanlar |
   |------------|-----------------|
   | Web sitesi | Tasarım Sistemi, Landing Page, Ana Sayfalar, Component Library, Veri Katmanı, Animasyon |
   | Mobil uygulama | UI Kit, Ekranlar, State Management, API Entegrasyonu, Navigation, Test |
   | Oyun | Game Engine, Mekanikler, UI/HUD, Asset Pipeline, Ses, Level Design |
   | API | Schema, Endpoint'ler, Auth, Validation, Test, Dokümantasyon |

4. **Kaç agent? (varsayılan: proje türüne göre 6-10)**

5. **Kaç loop/tur? (varsayılan: 10)**

6. **Sahte/demo veri lazım mı? (varsayılan: hayır)**
   - Evet → ayrı bir "Veri Fabrikası" agent'ı eklenir

7. **Web araştırması yapılsın mı? (ilham, referans site, tasarım trendi)**
   - Evet → Opus spec aşamasında WebSearch/WebFetch kullanır

### Config Çıktısı

Cevaplardan `.team-build/config.json` oluştur:

```json
{
  "project": "Proje Adı",
  "description": "Kısa açıklama",
  "type": "website",
  "agents": [
    {
      "id": "agent-01",
      "name": "Tasarım Sistemi",
      "role": "Renk, font, spacing, animasyon kuralları ve ortak component spec'leri",
      "specFile": ".team-build/specs/agent-01-tasarim-sistemi.md",
      "reportFile": ".team-build/reports/agent-01-report.md",
      "model": "agy",
      "dependsOn": [],
      "priority": 1
    }
  ],
  "loops": 10,
  "mockData": true,
  "webResearch": true,
  "createdAt": "2026-04-01T12:00:00Z"
}
```

Agent model ataması (`model` alanı):
- `"agy"` → **mekanik kodlama / veri / component** (sahte veri, component, spec
  uygulama, UI/state). Loop scripti bunu Bash'ten çalıştırır:
  `~/Projects/ClaudeHQ/scripts/hq agy --file <spec> --dir <proje> --slug <agent-id>`
- `"opus"` → spec yazımı, review, mimari karar. Claude'un `Agent` tool'u ile.
- `"agy"` bir Claude modeli **değildir** — `Agent(model=...)` alanına yazılmaz.

---

## Faz 2: Opus Spec Yazımı (otonom — soru yok)

Her agent için Opus detaylı spec dosyası yazar. **Opus KOD YAZMAZ**, sadece:

- Ne yapılacak (component listesi, sayfa yapısı, davranışlar)
- Tasarım kuralları (renkler, spacing, tipografi — varsa referans sitelerden)
- Dosya yapısı (hangi dosyalar oluşturulacak/düzenlenecek)
- Kabul kriterleri (ne zaman "bitti" sayılır)
- Bağımlılıklar (hangi agent'ın çıktısına ihtiyaç var)
- Sahte veri yapısı (mock data agent'ı varsa)

### Spec dosya formatı

`.team-build/specs/agent-XX-alan-adi.md`:

```markdown
# Agent XX: Alan Adı

## Amaç
Bu agent'ın tek cümlelik görevi.

## Kapsam
- [ ] Yapılacak iş 1
- [ ] Yapılacak iş 2
- [ ] Yapılacak iş 3

## Tasarım Kuralları
(Renkler, spacing, font, animasyon kuralları — agent-01 spec'ine referans ver)

## Dosya Planı
- `src/components/X.tsx` — açıklama
- `src/app/sayfa/page.tsx` — açıklama

## Sahte Veri
(Gerekiyorsa veri yapısı ve örnekler)

## Kabul Kriterleri
- Lint geçer
- Typecheck geçer
- Tarayıcıda görsel doğrulama
- Tasarım sistemiyle uyumlu

## Bağımlılıklar
- agent-01 (tasarım sistemi) tamamlanmış olmalı

## Notlar
(Opus'un özel talimatları, dikkat edilmesi gerekenler)
```

### Spec sırası

1. Bağımlılığı olmayan agent'lar önce (tasarım sistemi, veri fabrikası)
2. Sonra bağımlı olanlar

### Web araştırması

`webResearch: true` ise Opus spec yazarken:
- WebSearch ile ilham/referans ara
- WebFetch ile referans sitelerin tasarımını incele
- Bulguları spec'e "Referanslar" bölümü olarak ekle

Spec'ler yazıldıktan sonra Faz 3'e geç.

---

## Faz 3: Otonom Loop (soru yok — tam otonom)

Shell script'i başlat:

```bash
~/Projects/claude-config/projects/scripts/team-build.sh
```

Script şöyle çalışır (her iterasyon):

### 3a. Kod İterasyonu (agy / Gemini)

1. `.team-build/config.json` oku
2. `.team-build/reports/` altındaki önceki raporları oku
3. `.team-build/review-notes.md` oku (Opus'un önceki turdan notları)
4. Sıradaki agent spec'ini al (priority sırasına göre, tamamlanmamış ilk agent)
5. Spec'e göre kodla
6. `pnpm lint` / typecheck çalıştır (projeye göre)
7. Commit + push
8. `.team-build/reports/agent-XX-report.md`'ye rapor yaz:
   ```markdown
   ## Tur N — Agent XX: Alan Adı
   - Tarih: YYYY-MM-DD HH:mm
   - Durum: tamamlandı / kısmen / başarısız
   - Yapılanlar: ...
   - Değişen dosyalar: ...
   - Sorunlar: ...
   - Öğrenilenler: ...
   ```
9. Config'de agent durumunu güncelle

### 3b. Opus Review (her iterasyon sonunda)

Her kod iterasyonundan sonra Opus (kısa, ucuz bir review):

1. Tüm raporları oku
2. `.team-build/review-notes.md` güncelle:
   ```markdown
   # Review Notları — Tur N

   ## Genel Durum
   - Tamamlanan: X/Y agent
   - Kalan: ...

   ## Sonraki Tur İçin Talimatlar
   - Agent-03: Renk paletini agent-01 ile uyumlu yap, #1a1a2e kullan
   - Agent-05: Filtreleme component'i agent-04'ün card yapısıyla uyumlu olmalı

   ## Uyarılar
   - Agent-02'nin ürettiği veri yapısı agent-06 ile uyumsuz, düzeltilmeli
   ```
3. Gerekirse spec dosyalarını güncelle

### 3c. Context Temizliği

Her commit+push sonrasında:
- Script zaten her iterasyonda yeni Claude oturumu açar (ralph.sh gibi)
- Böylece context otomatik temiz başlar
- Notlar ve raporlar dosyada olduğu için yeni oturum bunları okur

### Döngü Bitişi

Tüm agent'lar tamamlandığında:
1. `.team-build/final-report.md` yaz (özet)
2. Kullanıcıya bildir
3. Script çıkışı

---

## Dosya Yapısı

```
.team-build/
├── config.json          # Proje config'i
├── review-notes.md      # Opus'un tur arası notları
├── final-report.md      # Tüm turlar bitince özet
├── specs/
│   ├── agent-01-tasarim-sistemi.md
│   ├── agent-02-veri-fabrikasi.md
│   └── ...
└── reports/
    ├── agent-01-report.md
    ├── agent-02-report.md
    └── ...
```

## Önemli Kurallar

1. **Opus asla kod yazmaz** — sadece spec, plan, review, not
2. **Mekanik kodlama agy (Gemini) ile yapılır** — component, animasyon, state, sahte veri, spec uygulama
3. **Her iterasyon commit+push** — kesintiye dayanıklı
4. **Raporlar dosyada** — context temizlense bile bilgi kaybolmaz
5. **Proje dışına çıkma** — sadece proje dizininde çalış
6. **Soru sorma** — setup hariç tamamen otonom
7. **Tutarlılık** — her agent tasarım sistemine uymalı

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
