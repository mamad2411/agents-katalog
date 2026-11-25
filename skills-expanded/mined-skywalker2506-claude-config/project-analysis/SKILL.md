# /project-analysis [-focus]

> Model yonlendirmesi: global/model-routing.md

**Focus modları** (isteğe bağlı, `-` ile):
```
/project-analysis                   # Tüm kategoriler (12 lead)
/project-analysis -backend          # API, DB, Arch, Security
/project-analysis -frontend         # UI/UX, Content, A11y
/project-analysis -security         # Sadece Security (SecLead/Opus)
/project-analysis -optimize         # Perf, Arch, Data
/project-analysis -feature          # Growth, Biz, Content
/project-analysis -test             # Tüm kategorilerde test boşlukları
/project-analysis -refactor         # Arch, Perf — teknik borç
/project-analysis -backend -security  # Kombinasyon
```

**Focus → Lead mapping:**

| Focus | Çalışan Lead'ler | Atlanan Lead'ler |
|-------|-----------------|-----------------|
| `-backend` | CodeLead, SecLead | ArtLead, GrowthLead, BizLead |
| `-frontend` | ArtLead | CodeLead, GrowthLead, BizLead, SecLead |
| `-security` | SecLead | ArtLead, CodeLead, GrowthLead, BizLead |
| `-optimize` | CodeLead (Perf+Arch+Data) | ArtLead, GrowthLead, BizLead, SecLead |
| `-feature` | GrowthLead, BizLead | ArtLead, CodeLead, SecLead |
| `-test` | Tüm Lead'ler (test gaps modu) | — |
| `-refactor` | CodeLead (Arch+Perf) | ArtLead, GrowthLead, BizLead, SecLead |
| `-docs` | ArtLead (Content) | CodeLead, GrowthLead, BizLead, SecLead |

Focus varsa dispatch tablosunda atlanan lead'ler `(atlandı)` olarak gösterilir.
Focus flag'leri forge'dan geçilebilir — forge Phase 1'de `/project-analysis -backend` gibi çağırır.

---

> **ÖNEMLİ — skill başlamadan önce:**
> Kullanıcıya şunu göster:
>
> ```
> Analiz başlamadan önce /compact önerilir (agent'lar çok token tüketir).
>
>   1) /compact çalıştır, sonra devam et
>   2) Geç ve devam et
> ```
>
> Kullanıcı "1" yazarsa → yanıt olarak **sadece şunu yaz, başka hiçbir şey ekleme:**
>
> /compact
> Kullanıcı "2" veya sadece Enter basarsa → direkt devam et.

## Başlamadan Önce ZORUNLU Oku

`PROJECT_ANALYSIS.md` dosyasını oku — özellikle şu bölümler:
- **§2** — Lead hiyerarşisi ve "dispatches" ne anlama geldiği (Lead ayrı process başlatmaz, bizzat analiz eder)
- **§4** — Agent registry ve model mapping tablosu (Claude Code Model kolonu dahil)
- **§5** — Lead prompt şablonu (birebir uygula, kendi yorumunu katma)

Bu okuma yapılmadan Lead prompt'ları yazılmaz.

---

Bu skill tetiklendiğinde aşağıdaki adımları izle:

## Referans

Tam protokol: `__PROJECTS_ROOT__/PROJECT_ANALYSIS.md`

O dosyayı oku ve içindeki talimatlara **harfiyen** uy.

---

## Adım -1 — Agent Erişilebilirlik Kontrolü (HER ZAMAN İLK ÇALIŞIR)

`scripts/check-agent-availability.sh` çalıştır (Bash tool ile).

Çıktıdaki her `UNAVAILABLE:` satırı için formatı parse et:
```
UNAVAILABLE: <model_tipi> | <neden> | <kurulum_talimatı> | <fallback>
```

Her ulaşılamayan agent için kullanıcıya sor:
```
⚠️  [MODEL_TIPI] ulaşılamıyor — [NEDEN]

Ne yapalım?
  1) Kurulum yap   — [KURULUM_TALİMATI]
  2) Alternatif kullan — [FALLBACK] modeli ile devam et
  3) Bu agent'ı atla
  4) Tüm ulaşılamazlara alternatif uygula (bu oturum)
```

Tam protokol: `PROJECT_ANALYSIS.md §7`

Tüm seçimler alındıktan sonra → **Adım 0'a geç**

---

## Adım 0 — Proje Tespiti (YENİ — HER ZAMAN İLK ÇALIŞIR)

Mevcut proje dizinini tara:
```
Glob: **/* (max depth 2)
Kontrol et: kaynak kod var mı? (lib/, src/, app/, pubspec.yaml, package.json, vb.)
```

### Senaryo A — Boş / Yeni Proje (kod yok, sadece README veya hiçbir şey yok)

```
Bu proje henüz kurulmamış. Analiz yapabilmem için önce projeyi anlamam gerekiyor.

Sana birkaç soru soracağım — cevaplarından bir proje brief'i oluşturacağım.
Sonra istersen tech stack tavsiyesi de verebilirim.

Devam edelim mi? (enter = evet)
```

**A14 DiscoveryAgent** başlat — `PROJECT_ANALYSIS.md §0`'daki soruları kullanır.
Discovery tamamlanınca kullanıcıya sor:
```
Brief hazır. Şimdi ne yapalım?
  1) Tech stack tavsiyesi al (A15 TechLead)
  2) Direkt projeyi kur (kurulum adımlarına geç)
  3) İkisi de — önce stack karar ver, sonra kur
```

### Senaryo B — Mevcut Proje (kod var)

`project-brief.md` var mı kontrol et:
- Varsa → brief'i oku, analiz moduna geç
- Yoksa → "Proje hakkında kısa bir brief oluşturalım mı? (Y/N)" sor
  - Y → A14 çalıştır (hızlı mod, 3 soru), sonra analiz moduna geç
  - N → direkt analiz moduna geç

---

### Paralel Research Phase (Phase 1'den önce)

Analysis başlamadan önce 4 paralel research agent çalıştırılır. Her biri farklı açıdan projeyi araştırır:

| Researcher | Odak | Çıktı |
|-----------|------|-------|
| **Stack Researcher** | Tech stack, versiyon, bağımlılıklar, uyumluluk | `analysis/research-stack.md` |
| **Feature Researcher** | Mevcut özellikler, eksikler, rakip karşılaştırma | `analysis/research-features.md` |
| **Architecture Researcher** | Kod yapısı, pattern'ler, coupling, complexity | `analysis/research-architecture.md` |
| **Risk Researcher** | Güvenlik açıkları, performans darboğazları, teknik borç | `analysis/research-risks.md` |

**Çalışma şekli:**
1. 4 agent paralel `run_in_background: true` ile başlatılır
2. Her agent kendi dosyasına yazar (max 3-5KB)
3. Tüm research tamamlanınca Lead'lere context olarak verilir
4. Lead'ler research çıktılarını okuyarak daha derin analiz yapar

**Focus modu etkisi:**
- `-backend`: Stack + Architecture + Risk researcher çalışır (Feature atlanır)
- `-frontend`: Stack + Feature researcher çalışır (Architecture + Risk atlanır)  
- `-security`: Risk researcher tek başına, detaylı (Opus modeli ile)
- Diğer focus'lar: 4'ü de çalışır, sonuçlar focus'a göre filtrelenir

Research phase max 3 dakika sürer. Timeout olan researcher atlanır, lead'ler onsuz devam eder.

---

## Adım 1 — Agent atama modunu sor

```
Analiz için ajan atama modunu seç:
  1) Lead Orchestrator — A1 projeyi inceler, her departman için Lead + ajan atar
  2) Manuel            — her kategori için ajan ve modeli kendim seçerim
  3) Hızlı             — tüm kategoriler agy (Gemini) ile, standart agent'lar

Seçiminiz (1/2/3):
```

**1 seçilirse (Lead Orchestrator):**
- A1 (Lead Orchestrator) kısa bir proje taraması yapar
- Her Lead departmanı için: hangi kategoriler, hangi worker agent'lar, hangi modeller → bir atama haritası çıkarır
- Kullanıcıya haritayı göster, onay al
- Leads'leri paralel başlat (`run_in_background=true`)

**2 seçilirse (Manuel):**
- Her kategori için sırayla sor: `Evet / Hayır / Kısmen`
- Kabul edilen her kategori için: hangi agent ID? hangi model?
- `PROJECT_ANALYSIS.md` §3'teki kategori + agent eşleşme tablosuna bak, öner

**3 seçilirse (Hızlı):**
- Tüm 12 kategoriyi agy (Gemini) modeli + varsayılan agent'larla başlat (kategori seçimi yok)

## Adım 2 — Lead'leri başlat (paralel, background)

Her Lead departmanı için bir Agent başlat (`run_in_background=true`).

Lead agent prompt şablonu (`PROJECT_ANALYSIS.md` §5'teki şablonu kullan):
- Lead rolü ve sorumlu kategoriler
- Her kategori için atanan worker agent ve model
- Proje kökü
- Çıktı: `[PROJE]/analysis/[NN_kategori].md`

Lead yapısı:
- **ArtLead**    → UI/UX (#1), Content (#8), Accessibility (#11)
- **CodeLead**   → Performance (#2), Data (#4), Architecture (#10)
- **GrowthLead** → SEO (#3), Growth (#6), Analytics (#9)
- **BizLead**    → Monetization (#5), Competitive (#12)
- **SecLead**    → Security (#7)

### Agent Dispatch Tablosu

Lead'ler başlatılmadan önce kullanıcıya dispatch tablosunu göster:

```
━━ Agent Dispatch ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Agent        Model          Kategoriler
  ─────────    ───────────    ──────────────────────────
  ArtLead      agy (Gemini)   UI/UX, Content, A11y
  CodeLead     agy (Gemini)   Perf, Data, Arch
  GrowthLead   agy (Gemini)   SEO, Growth, Analytics
  BizLead      agy (Gemini)   Monetization, Competitive
  SecLead      Opus 4.6       Security
  Master       Opus 4.6       Final report (Phase 4)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Bu tablo her zaman gösterilir — kullanıcı hangi agent'ın hangi modelle çalıştığını bilmeli.

## Adım 3 — Watchdog

Her 3 dakikada bir durum göster (model bilgisi dahil):
```
Analiz durumu (X/Y tamamlandı):
✅ ArtLead   [agy (Gemini)] 3m 12s — UI/UX ✅, Content ✅, A11y ✅
✅ SecLead   [Opus 4.6]     2m 30s — Security ✅
⏳ CodeLead  [agy (Gemini)] 4m 45s — Perf ✅, Data ✅, Arch ⏳
⏳ GrowthLead[agy (Gemini)] 3m 50s — SEO ✅, Growth ⏳, Analytics ⏳
⏳ BizLead   [agy (Gemini)] 2m 10s — Monetization ⏳, Competitive ⏳
```
8 dakika geçen lead → kullanıcıya sor, onay gelirse yeniden başlat.

## Adım 4 — Master rapor

Tüm Lead'ler tamamlanınca bir **Opus agent** başlat:
- Tüm kategori raporlarını oku
- `[PROJE]/analysis/MASTER_ANALYSIS.md` oluştur
- `PROJECT_ANALYSIS.md` §6'daki master rapor yapısını kullan
- Cross-cutting insights + top 20 aksiyon listesi + maliyet tablosu

## Adım 5 — Kullanıcıya göster

1. Agent execution özeti (her agent: model, süre, çıktı sayısı)
2. Master rapor özeti
3. Dosya konumları
4. En kritik 5 aksiyon

```
━━ Execution Summary ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Agent        Model          Süre      Çıktı
  ─────────    ───────────    ──────    ─────
  ArtLead      agy (Gemini)   3m 12s    3 reports
  CodeLead     agy (Gemini)   4m 45s    3 reports
  GrowthLead   agy (Gemini)   3m 50s    3 reports
  BizLead      agy (Gemini)   2m 10s    2 reports
  SecLead      Opus 4.6       2m 30s    1 report
  Master       Opus 4.6       1m 45s    MASTER_ANALYSIS.md
  ─────────    ───────────    ──────    ─────
  Total        6 agents       18m 12s   13 files
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

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
