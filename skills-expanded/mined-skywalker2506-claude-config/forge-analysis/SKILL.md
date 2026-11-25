---
name: forge-analysis
description: "Forge sonrası verimlilik analizi — run metriklerini ölç, pattern'leri tespit et, sistemi optimize et. Her forge sonunda otomatik tetiklenir. Çoklu run'da (forge 5 gibi) tüm run'ları kapsayan final meta-analiz yapar. Triggers: forge-analysis, forge analiz, forge-analysis run, forge verimliliği."
argument-hint: "[run-summary-path | --final N] [proje]"
---

# /forge-analysis — Post-Forge Efficiency Analysis & System Optimization

Forge run bittikten sonra ne kadar verimli çalışıldığını ölç, sistem darboğazlarını tespit et ve claude-config'i optimize et.

**İki mod:**
- **Per-run analiz** (her run sonunda): Tek run'ı değerlendir, küçük optimizasyonlar uygula
- **Final meta-analiz** (`--final N`, tüm run'lar bitince): N run boyunca ne öğrendik, forge yaklaşımı hâlâ mantıklı mı, ne değişmeli?

## Tetiklenme

Bu skill **her forge run'ının Phase 7'si olarak otomatik çalışır**. Çoklu run'da (`/forge 5`) tüm run'lar bitince ek olarak **Final Meta-Analiz** de çalışır.

```
/forge-analysis                         # CWD projesinin son run'ını analiz et
/forge-analysis forge/run-3-summary.md  # Belirli bir run
/forge-analysis CoinHQ                  # Projenin tüm run'larını karşılaştır
/forge-analysis --final 5 CoinHQ        # 5 run'lık final meta-analiz (forge 5 sonu)
```

---

## Phase 7 Akışı

```
━━ Phase 7: Forge Analysis ━━━━━━━━━━━━━━━━━━━━
  [1] Metrikleri hesapla
  [2] Cross-run trend analizi
  [3] Bottleneck tespiti
  [4] Sistem optimizasyonları uygula
  [5] Analysis raporu kaydet
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### Adım 1 — Metrikleri Hesapla

`forge/run-{N}-summary.md` ve `forge/run-{N}-lessons.md` dosyalarını oku.

**Verimlilik metrikleri:**

| Metrik | Hesaplama | Hedef |
|--------|-----------|-------|
| **Task success rate** | completed / total * 100 | ≥ 85% |
| **Fix loop ratio** | fix_iterations / total_prs | ≤ 0.3 |
| **Sprint adherence** | planned_tasks / actual_tasks | ≥ 0.9 |
| **PR merge rate** | merged / opened | ≥ 0.8 |
| **Review pass rate** | first_pass_ok / total_reviews | ≥ 0.7 |
| **Max retry hit rate** | max_retry_tasks / total_tasks | ≤ 0.05 |
| **Phase 0 pass rate** | preflight_ok / preflight_checks | 1.0 (her zaman 100%) |

Her metriği hesapla ve hedefle karşılaştır:
- `✅ Hedef aşıldı` (yeşil)
- `⚠️ Hedefin altında` (sarı — %10'a kadar sapma)
- `🔴 Kritik` (kırmızı — %10'dan fazla sapma)

---

### Adım 2 — Cross-Run Trend Analizi

`forge/` klasöründeki **tüm** run summary ve lessons dosyalarını oku. Run sayısı ≥ 2 ise trend analizi yap.

**Trend metrikleri:**
- Task success rate zaman içinde artıyor mu?
- Fix loop ratio düşüyor mu?
- Hangi task kategorileri sürekli başarısız?
- Hangi sprint'ler düzenli gecikiyor?
- Hangi agent (Sonnet/Opus) bottleneck oluyor?

**Pattern detection:**
```
Tespit edilecek pattern'ler:
- Sürekli başarısız task tipleri (XL task → split gerekiyor)
- Tekrarlayan fix loop konuları (test eksik, lint fail, vb.)
- Phase 0 sıkça fail eden kontroller
- Belirli dosya/modüllerde sürekli çakışma
- Max retry'a düşen task kategorileri
```

---

### Adım 3 — Bottleneck Tespiti

Şu bottleneck'leri sırayla kontrol et:

**Task seviyesi:**
- Hangi task'lar en çok fix loop tüketti?
- Hangi task'lar max retry'a düştü? → Ortak özellik var mı?
- Hangi task'lar en hızlı/yavaş tamamlandı?

**Sprint seviyesi:**
- Hangi sprint'te en fazla başarısızlık var?
- Sprint 1 vs Sprint N başarı oranı farkı?

**Agent seviyesi:**
- Coder (Sonnet) başarısız olduysa → prompt kalitesi mi, task tanımı mı?
- Reviewer (Opus) çok fix istiyorsa → kod kalitesi mi, standartlar mı?

**Sistem seviyesi:**
- Phase 0 kontrolleri fail ettiyse → pre-req eksik mi?
- Git çakışmaları olduysa → worktree isolation yeterli mi?

---

### Adım 4 — Sistem Optimizasyonları Uygula

Tespit edilen bottleneck'lere göre **otomatik düzeltmeler** yap:

#### 4.1 — Forge Skill Optimizasyonu

**XL task pattern tespit edildiyse:**
- `forge/SKILL.md` Phase 2'ye not ekle: hangi task türleri otomatik split edilmeli
- Memory'e kaydet: `forge_split_rules.md`

**Sürekli aynı fix loop konusu varsa (örn. lint):**
- Phase 4'e pre-task lint kontrolü ekle (SKILL.md'ye not olarak)
- Memory'e kaydet: `forge_preflight_additions.md`

**Phase 0 sıkça fail eden bir kontrol varsa:**
- O kontrolün hata mesajını iyileştir
- SKILL.md'deki "Fail durumu" açıklamasını güncelle

#### 4.2 — Memory Optimizasyonu

Aşağıdaki memory dosyalarını oluştur veya güncelle:

```
~/.claude/projects/.../memory/forge_patterns.md
```

Içerik:
```markdown
---
name: Forge Run Patterns
description: Forge çalıştırmalarında tespit edilen verimlilik pattern'leri ve optimizasyonlar
type: project
---

## Başarı Pattern'leri
[Ne çalışıyor — tekrar et]

## Başarısızlık Pattern'leri
[Ne çalışmıyor — kaçın veya farklı yap]

## Sprint Önerileri
[Task büyüklükleri, sprint yapısı için öneriler]

## Son güncelleme: {tarih}, Run {N}
```

#### 4.3 — Agent Config Önerileri

Reviewer (Opus) çok sık reject ediyorsa:
- `forge/SKILL.md` Phase 4'e not ekle: "Review öncesi şu kontrolleri yap: ..."
- Hangi konularda reject geldiğini memory'e kaydet

Coder (Sonnet) fix loop'a giriyorsa:
- Task description kalitesini artırmak için Phase 3'e öneri ekle

#### 4.4 — Sprint Süreç Optimizasyonu

Sprint gecikmesi varsa:
- Sprint plan kapasitesini düşür (velocity hesapla)
- Memory'e velocity kaydet: `forge_velocity.md`

---

### Adım 5 — Analysis Raporu Kaydet

`forge/analysis-{YYYY-MM-DD}-run-{N}.md` dosyasına yaz:

```markdown
# Forge Analysis — {Proje} — Run {N} — {Tarih}

## Verimlilik Skoru: {X}/100

### Metrikler
| Metrik | Değer | Hedef | Durum |
|--------|-------|-------|-------|
| Task success rate | 85% | ≥85% | ✅ |
| Fix loop ratio | 0.4 | ≤0.3 | ⚠️ |
| PR merge rate | 0.9 | ≥0.8 | ✅ |
| ...  | ... | ... | ... |

### Cross-Run Trend (Run 1→{N})
- Task success rate: ↗ 71% → 85% (iyileşiyor)
- Fix loop ratio: → 0.4 stabil (iyileşmiyor)
- Max retry hit rate: ↘ 10% → 3% (iyileşiyor)

### Tespit Edilen Bottleneck'ler
1. **Fix loop yüksek** — Lint hataları tekrarlıyor (3/5 fix loop lint'ten)
2. **XL task'lar başarısız** — KEY-113, KEY-114 scope fazla büyük
3. **Sprint 3 geç kaldı** — Task bağımlılığı beklenmedik

### Uygulanan Optimizasyonlar
- [✓] Memory güncellendi: forge_patterns.md
- [✓] Forge SKILL.md: lint pre-check notu eklendi
- [✓] Memory güncellendi: forge_velocity.md (velocity: 4 task/sprint)
- [~] Öneri: XL task'ları Phase 2'de otomatik split et (manuel onay gerekli)

### Sonraki Run İçin Öneriler
1. Sprint başına max 4 task (mevcut velocity)
2. XL task'ları 2-3 subtask'a böl
3. Phase 4 başında lint çalıştır
4. KEY-113 ve KEY-114 yeniden scope et

## Sistem Sağlığı: {İyi/Orta/Kritik}
```

---

## Verimlilik Skoru Hesaplama

```
Skor = (
  task_success_rate * 40 +       # En kritik metrik
  (1 - fix_loop_ratio) * 25 +    # Kod kalitesi göstergesi
  pr_merge_rate * 20 +           # Süreç uyumu
  review_pass_rate * 15          # Agent kalitesi
) / 100 * 100
```

Skor yorumu:
- **85-100**: Forge çok verimli — minimal müdahale
- **70-84**: İyi — küçük iyileştirmeler yapıldı
- **50-69**: Orta — önemli bottleneck'ler var, uygulanan optimizasyonları kontrol et
- **<50**: Kritik — forge yaklaşımını gözden geçir, kullanıcıyı bildir

---

## Çıktı Özeti (Her Forge'a Eklenir)

Phase 5 sonunda çıktıya bu eklenir:

```
━━ Phase 7: Forge Analysis Complete ━━━━━━━━━━━━━━━━
  Verimlilik Skoru: 78/100 ⚠️
  ✅ Task success rate: 85% (hedef ≥85%)
  ⚠️ Fix loop ratio: 0.40 (hedef ≤0.30) — lint pre-check eklendi
  ✅ PR merge rate: 90% (hedef ≥80%)

  Uygulanan: 3 optimizasyon
  Sonraki run için: 4 öneri

  Rapor: forge/analysis-2026-04-08-run-1.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

---

## Final Meta-Analiz (`/forge N` sonunda — N ≥ 2)

`/forge 5` gibi çoklu run bitince, per-run analizlerin ötesinde **stratejik bir değerlendirme** yapılır. Bu analiz şu soruyu cevaplar: **"N run boyunca forge hâlâ değer üretiyor muydu, yoksa farklı bir şey mi yapılmalı?"**

### 1 — Tüm Run'ları Karşılaştır

`forge/run-{1..N}-summary.md` ve `forge/analysis-*-run-{1..N}.md` dosyalarını toplu oku.

**Karşılaştırma tablosu oluştur:**

```
━━ Cross-Run Comparison — CoinHQ (5 Runs) ━━━━━━━━━━━━━━━━━
  Run  Tasks  Success%  FixLoop  Score  Yeni mi?
  ──   ─────  ────────  ───────  ─────  ────────
  R1   14     71%       0.52     62     İlk run, yüksek baseline
  R2   12     83%       0.38     74     Önceki dersler devreye girdi
  R3   10     90%       0.28     85     Momentum arttı
  R4    8     88%       0.31     82     Küçük regresyon
  R5    6     83%       0.35     78     Task havuzu azaldı
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Trend: ↗ İyileşiyor (R1→R3) → → Plato (R3→R5)
```

### 2 — Return on Forge (RoF) Analizi

Her run'da ne kadar **gerçek değer** üretildi?

| Soru | Veri kaynağı | Sonuç |
|------|-------------|-------|
| Toplam kaç task tamamlandı? | summary dosyaları | ∑ completed |
| Her run'da yeni task mı yoksa tekrar mı yapıldı? | sprint task ID'lerini karşılaştır | yeni vs. tekrar |
| Zamanla task'lar zorlaşıyor mu, kolaylaşıyor mu? | story points trend | ↗/↘/→ |
| Verimlilik skoru platoya girdi mi? | score trend | plato tespiti |
| Son run'da tamamlanan task sayısı ilk run'un <%50'si mi? | R1 vs RN completed | havuz tükeniyor |

**Forge Sağlık Durumu:**

```
✅ Sağlıklı: Her run yeni, farklı task'lar tamamlıyor, score artıyor
⚠️ Plato: Score 3+ run sabit, task'lar azalıyor → forge frekansı düşür
🔴 Diminishing returns: Son run score < ilk run score → yaklaşımı değiştir
🔴 Tekrarlama: Aynı task kategorileri tekrar açılıyor → kök neden çözülmüyor
```

### 3 — Forge Yaklaşımı Hâlâ Doğru mu?

Şu soruları cevapla ve **net bir öneri** ver:

**Devam sinyalleri (forge işe yarıyor):**
- Her run'da %70+ yeni task
- Verimlilik skoru ↗ veya stabil ≥75
- Kritik buglar/güvenlik açıkları kapandı
- Teknik borç azalıyor (proje health iyileşiyor)

**Değiştirme sinyalleri (farklı yaklaşım gerekli):**
- Son 2 run'da tamamlanan task'lar ilk run'un <%40'ı
- Verimlilik skoru 3 run üst üste <60
- Aynı task kategorileri 2+ kez açıldı (kök neden fix edilmedi)
- Sprint plan'da artık yeni task kalmıyor

**Durma sinyalleri (forge'u durdur):**
- Proje task havuzu tükendi (backlog boşaldı)
- Her run'da <%5 tamamlanma
- Max retry'a düşen task oranı >%30

### 4 — Stratejik Öneriler

Yukarıdaki analize göre bir sonuç üret:

```
━━ Final Meta-Analiz Sonucu — CoinHQ — 5 Run ━━━━━━━━━━━━━━━
  Genel Trend: ↗ İyileşti (R1:62 → R3:85) → plato (R3-R5 ~82)
  RoF: Yüksek (R1-R3), Orta (R4-R5 — task havuzu azalıyor)
  Tekrarlama: Yok — her run yeni task'lar
  
  SONUÇ: Forge verimli çalıştı.
  
  Öneri:
  ├─ Forge frekansını düşür (haftalık → 2 haftada bir)
  ├─ Sonraki forge öncesi backlog'u zenginleştir
  └─ R4-R5'teki fix loop yüksekliği → lint pre-check ekle (zaten eklendi)
  
  ALTERNATIF DEĞİL — forge devam edebilir, sadece frekans ayarı yeter.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Eğer "farklı yaklaşım" veya "durma" sinyali varsa, alternatifi de öner:
- **Forge yerine manuel sprint**: Backlog küçüldüyse, /sprint-plan + tek tek task pipeline'i yeterli
- **Daha az otonom**: Sadece yüksek öncelikli task'larda forge, gerisi manuel
- **Temizlik modu**: Yeni feature yerine test coverage, refactor, docs odaklı mini-forge

### 5 — Final Meta-Analiz Raporu Kaydet

`forge/meta-analysis-{YYYY-MM-DD}-runs-1-to-{N}.md` dosyasına yaz:

```markdown
# Forge Meta-Analysis — {Proje} — Run 1 to {N} — {Tarih}

## Özet
- Toplam run: N
- Toplam task: X tamamlandı / Y planlandı
- Ortalama verimlilik skoru: {Z}/100
- Genel trend: {İyileşti / Plato / Geriledi}

## Cross-Run Tablo
[karşılaştırma tablosu]

## Return on Forge
[RoF analizi]

## Forge Sağlık Durumu: {Sağlıklı / Plato / Diminishing Returns}

## Stratejik Sonuç
[Devam / Frekans düşür / Yaklaşım değiştir / Durdur]

## Uygulanan Sistem Optimizasyonları (tüm run'larda)
[Per-run analizlerde yapılan tüm optimizasyonların özeti]
```

---

## Kurallar

1. **Otomatik çalışır** — forge Phase 7 olarak, soru sormaz
2. **Sadece tespit edilen sorunları optimize eder** — spekülatif değişiklik yok
3. **SKILL.md değişiklikleri not olarak eklenir**, kural değil — kullanıcı onayı olmadan zorunlu kural eklenmez
4. **Memory her zaman güncellenir** — lessons kaybolmaz
5. **Verimlilik skoru < 50 ise kullanıcıyı bildir** ve otomatik devam etme
6. **Cross-run trend için min 2 run gerekli** — ilk run'da sadece mevcut metrikleri ölç
7. **Optimizasyon logu** — neyi neden değiştirdiğini `forge/analysis-*.md`'ye yaz

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
