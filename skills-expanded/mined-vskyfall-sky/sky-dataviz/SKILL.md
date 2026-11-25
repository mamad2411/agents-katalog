---
name: sky-dataviz
description: >-
  Web'de veri görselleştirme: soruya göre grafik türü seçimi, Recharts / visx / ECharts /
  Observable Plot tercihi, kategorik-sıralı-ayrışan renk paletleri ve token'larla uyum, renk
  körlüğü ve erişilebilir grafikler (aria, veri tablosu alternatifi), eksen/ölçek/etiket
  kuralları, tooltip ve etkileşim, yükleniyor/boş/hata durumları, responsive ve performans,
  Türkçe biçimlendirme ve sık hatalar. Grafik, chart, sparkline, ısı haritası veya "veriyi
  görselleştir" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Veri Görselleştirme

## Önce soru, sonra grafik

| Soru | Grafik | Kaçın |
|---|---|---|
| Kategoriler arası karşılaştırma | **Yatay bar** (uzun etiketler), dikey bar (≤ 7 kategori, kısa etiket) | pasta |
| Zaman içinde değişim | **Çizgi** (sürekli), bar (ayrık dönemler, az nokta) | alan grafiği çok seride |
| Bütünün parçaları | **Yığılmış bar** veya %100 bar; pasta/halka yalnızca ≤ 3 parça ve tek anlık görüntü | 3D pasta, 6+ dilimli pasta |
| Dağılım | Histogram, kutu grafiği | — |
| İki değişken ilişkisi | Saçılım (+ trend çizgisi) | çift y ekseni |
| Yoğunluk / takvim | Isı haritası | — |
| Tek sayı + bağlam | KPI + sparkline (bkz. `sky-dashboard`) | gösterge (gauge) |
| Sıralama | Sıralı yatay bar, bump chart | — |

Tek grafikte **tek mesaj**. Başlık mesajı söyler ("Mobil siparişler 3 ayda %40 arttı"), ekseni değil.

## Kütüphane

| Durum | Seçim |
|---|---|
| Panel grafikleri, hızlı, SVG, React | **Recharts** (varsayılan) |
| Özel/karmaşık görsel, tam kontrol | **visx** (D3 ilkelleri + React) |
| Büyük veri (10k+ nokta), canvas, zoom/brush | **ECharts** (`echarts-for-react`) veya uPlot |
| Keşifsel/istatistiksel, az kod | **Observable Plot** |
| Sunucuda statik görsel (OG, e-posta) | `@resvg/resvg-js` ile SVG → PNG veya Vega-Lite |

Grafik bileşenlerini `dynamic(() => import(...), { ssr: false })` ile yükle (SSR'da boyut ölçümü sorunlu olabilir)
ve iskelet göster. Tek sarmalayıcı (`components/charts/`) ile kütüphane detayını gizle; tema/renk/tooltip orada.

## Renk

**Kategorik** (seriler): en fazla **6–7**; token'lardan türet (`--chart-1` … `--chart-6`), açık ve koyu
temada ayrı ayarlanmış, renk körlüğüne dayanıklı (mavi/turuncu/yeşil-mavi/mor/kahverengi; kırmızı-yeşil ikilisini
yan yana koyma). Aynı varlık **her grafikte aynı renk** ("Mobil" her yerde `--chart-2`).
**Sıralı** (azdan çoğa): tek renk tonu açıktan koyuya (ısı haritası, choropleth); 5–7 adım.
**Ayrışan** (negatif/pozitif): iki renk + nötr orta (`--chart-neg` / `--chart-pos`); sıfır noktası ortada.
**Anlamsal**: artış/azalış için `--success`/`--danger` ama **yalnızca** anlam gerçekten iyi/kötü ise.
Vurgu: tek seriyi öne çıkar, kalanı `--fg-subtle` ile geri plana at.

```css
:root { --chart-1: oklch(0.55 0.17 255); --chart-2: oklch(0.70 0.15 55); --chart-3: oklch(0.62 0.12 170);
        --chart-4: oklch(0.58 0.18 310); --chart-5: oklch(0.55 0.10 30); --chart-6: oklch(0.65 0.14 120); }
```
Koyu temada açıklığı (L) ~0.05–0.1 artır. Kontrast: bar/çizgi ile arka plan ≥ 3:1.

## Eksen, ölçek, etiket

- Bar grafiği **sıfırdan başlar**; çizgi grafiği başlamayabilir ama kesik eksen işaretlenir.
- Birim eksende veya başlıkta bir kez ("Gelir (₺ bin)"), her tick'te değil.
- Tick biçimi `Intl.NumberFormat("tr-TR", { notation: "compact" })` → "1,2 Mn"; tarih `Intl.DateTimeFormat` kısa ("3 Kas").
- Mobilde tick sayısını azalt (`interval="preserveStartEnd"` / `tickCount`), etiketleri döndürme → yatay bar'a geç.
- Grid çizgileri ince ve `--border`; yalnızca yatay (çoğu grafikte dikey gereksiz).
- Çift y ekseni **kullanma**; iki grafik yan yana yap.
- Lejant: ≤ 3 seri → doğrudan çizgi ucuna etiket; daha fazla → üstte yatay lejant, tıklayınca seriyi gizle/göster.
- Eksik veri: boşluk bırak (`connectNulls={false}`), sıfır çizme; ya da "veri yok" notu.

## Etkileşim

- Tooltip: tüm serileri aynı x'te göster, değerleri biçimli, renk kutucuğu, tarih tam.
  Klavyeyle erişilebilir olmalı (odaklanabilir noktalar veya tablo alternatifi).
- Hover vurgusu: aktif seriyi kalınlaştır, diğerlerini soluklaştır.
- Zoom/brush yalnızca uzun zaman serilerinde; sıfırlama butonu şart.
- Tıkla → filtrele (bar'a tıkla, tablo o kategoriye filtrelenir) panellerde değerli; URL'ye yaz (bkz. `sky-dashboard`).
- Animasyon: ilk çizimde ≤ 400ms, veri güncellemede kısa geçiş; `prefers-reduced-motion`da kapat (`isAnimationActive={false}`).

## Erişilebilirlik

- Kapsayıcı `role="img"` + `aria-label` **özet cümle** ("Son 6 ayda aylık gelir; Ekim en yüksek, ₺124 bin").
- Alternatif: grafiğin altında/`<details>` içinde **veri tablosu** (ekran okuyucu ve kopyalama için) — en sağlam yol.
- Renk tek taşıyıcı olmasın: seriler için farklı nokta şekli veya desen, doğrudan etiketler.
- Metin kontrastı eksen etiketlerinde ≥ 4.5:1 (`--fg-muted` yeter mi kontrol et).
- Odak sırası: başlık → grafik → tablo; tooltip içeriği `aria-live` ile duyurulmasın (gürültü); özet yeter.

## Durumlar

- **Yükleniyor:** grafikle aynı boyutta iskelet (eksen çizgileri + soluk bloklar); boyut zıplamasın (`aspect-ratio` veya sabit `height`).
- **Boş:** "Bu dönemde veri yok" + tarih aralığını genişlet önerisi; boş eksen çizme.
- **Hata:** kısa mesaj + yeniden dene; panelin kalanını etkilemesin.
- **Tek nokta:** çizgi yerine nokta/sayı göster.
- **Çok fazla kategori (>12):** ilk 10 + "Diğer" ya da sıralı yatay bar ile kaydırma.

## Responsive

- `ResponsiveContainer width="100%" height={280}` veya CSS `aspect-ratio: 16/9` kapsayıcı + `ResizeObserver`.
- 375px'te: lejant alta, tick azalt, dikey bar → yatay bar, sparkline'lar KPI'ya iner.
- Container queries ile kapsayıcı genişliğine göre varyant.

## Performans

- Veriyi **sunucuda** topla (günlük/haftalık bucket); istemciye ≤ 500 nokta yolla. LTTB downsampling gerektiğinde.
- `useMemo` ile dönüştürülmüş diziyi sabitle; Recharts her render'da yeniden hesaplar.
- 5k+ nokta SVG'de yavaş → canvas (ECharts/uPlot).
- Çok grafikli panelde her grafik kendi `Suspense`ında.

## Türkçe biçim

`Intl.NumberFormat("tr-TR")` → `1.234,5`; para `{ style: "currency", currency: "TRY" }`; yüzde `{ style: "percent", maximumFractionDigits: 1 }` → `%12,4` (işaret önde — Türkçe'de doğru).
Ay adları `Intl.DateTimeFormat("tr-TR", { month: "short" })` → "Kas". Hafta pazartesi başlar.

## Sık hatalar

- Pasta ile 8 dilim; 3D; gölge/gradyan dolgu; gereksiz gösterge (gauge)
- Kesik y ekseni ile abartılmış fark
- Her grafikte farklı renk ataması
- Tooltip'siz/etiketsiz noktalar; birimsiz eksen
- Mobilde dönmüş etiketler ve 20 tick
- Yükleniyor durumunda boyut zıplaması (CLS)
- Grafikte Türkçe karakter kırılması (font `latin-ext` eksik)

## Kontrol listesi

- [ ] Grafik türü soruya uygun; tek mesaj; başlık mesajı söylüyor
- [ ] Renkler token'dan, ≤ 7 seri, tutarlı, renk körlüğüne dayanıklı, iki temada test edildi
- [ ] Bar sıfırdan; birim var; tick'ler tr-TR
- [ ] `aria-label` özeti + veri tablosu alternatifi
- [ ] Yükleniyor/boş/hata durumları, boyut sabit
- [ ] 375px'te okunur
- [ ] Veri sunucuda toplanmış; ≤ 500 nokta
