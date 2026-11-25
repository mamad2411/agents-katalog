---
name: sky-data-analysis
description: >-
  Veri analizi (geliştirici için): DuckDB ile CSV/Parquet/JSON üzerinde SQL, Python pandas ve
  polars, Jupyter/marimo defterleri, veri temizleme (eksik değer, tip, tekrar, Türkçe biçimler),
  keşifsel analiz, gruplama/pivot/zaman serisi, görselleştirme (matplotlib, seaborn, plotly),
  ürün metrikleri (huni, cohort, retention), tekrar üretilebilirlik ve sonuçları paylaşma.
  "Bu CSV'yi analiz et", "rapor çıkar", "pandas", "veriden içgörü" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Veri Analizi

## Hızlı yol: DuckDB

Kurulum yok denecek kadar kolay, dosyalar üzerinde doğrudan SQL, milyonlarca satırda hızlı:
```sql
-- duckdb CLI veya Python: import duckdb; duckdb.sql("…").df()
SELECT date_trunc('month', starts_at) AS ay, service, count(*) AS adet, sum(price) / 100.0 AS gelir
FROM read_csv('randevular.csv', delim=';', header=true, dateformat='%d.%m.%Y')
WHERE status = 'completed'
GROUP BY ALL ORDER BY ay, gelir DESC;
```
Parquet, JSON, uzak dosyalar (S3/HTTP), Postgres'e doğrudan bağlanma (`ATTACH`) da var. Geliştiricilerin yeni favorisi.

## Python: pandas / polars

```python
import polars as pl
df = (pl.read_csv("randevular.csv", separator=";", encoding="utf8-lossy")
        .with_columns(pl.col("starts_at").str.strptime(pl.Datetime, "%d.%m.%Y %H:%M"),
                      pl.col("price").str.replace_all(r"\.", "").str.replace(",", ".").cast(pl.Float64)))
summary = (df.filter(pl.col("status") == "completed")
             .group_by(pl.col("starts_at").dt.truncate("1mo").alias("ay"))
             .agg(pl.len().alias("adet"), pl.col("price").sum().alias("gelir"))
             .sort("ay"))
```
polars büyük veride hızlı ve tutarlı API; pandas ekosistemi en geniş. İkisi de DuckDB ile birlikte çalışır.

## Temizleme kontrol listesi

- [ ] Kodlama (UTF-8, gerekirse Windows-1254), ayraç (`;`), ondalık virgül
- [ ] Tipler (tarih, sayı, kategori) doğru; tarih saat dilimi bilinçli
- [ ] Eksik değerler: ne kadar, neden, nasıl ele alınacak (sil / doldur / ayrı kategori)
- [ ] Tekrar eden satırlar, test verileri, iç kullanıcılar ayıklandı
- [ ] Aykırı değerler incelendi (hata mı gerçek mi?)
- [ ] Metin normalizasyonu (büyük/küçük harf `tr` kurallarıyla, boşluk)

## Keşifsel analiz

Satır/sütun sayıları, `describe()`, kategori dağılımları, zaman içinde trend, segment karşılaştırması. Her bulgunun yanında **"bu ne anlama geliyor?"**
cümlesi. Korelasyon ≠ nedensellik; örneklem küçükse belirt.

## Ürün metrikleri

- **Huni**: adım adım dönüşüm (ziyaret → kayıt → ilk randevu → ödeme) ve en büyük düşüş.
- **Cohort retention**: kayıt ayına göre gruplar, sonraki aylarda aktif oranı (ısı haritası tablo).
- **Retention / churn**, ARPU, LTV kabası, aktif kullanıcı (DAU/WAU/MAU) — tanımları yaz (ne "aktif" sayılır?).
Analitik olay verisi büyükse ClickHouse/BigQuery veya PostHog'un SQL'i (bkz. `sky-observability`).

## Görselleştirme

matplotlib/seaborn (statik rapor), plotly (etkileşimli), Altair (bildirimsel). Kurallar `sky-dataviz` ile aynı: soruya uygun grafik, başlık mesajı söyler,
Türkçe biçimler (`ticker.FuncFormatter` ile `1.234,5`), renk körlüğüne dayanıklı palet.

## Defterler ve tekrar üretilebilirlik

- **marimo** (reaktif, `.py` dosyası — Git dostu) veya Jupyter; Jupyter'de "baştan çalıştır" ile hatasız bitmeli.
- Ham veri değiştirilmez; temizleme adımları kodda; bağımlılıklar `uv` ile sabit (bkz. `sky-python`).
- Kişisel veriyi analiz ortamına gereksiz taşıma; anonimleştir (bkz. `sky-privacy-engineering`).

## Paylaşma

Kısa rapor: 3 ana bulgu (rakamla) → her biri için grafik → öneriler → yöntem ve sınırlamalar. Sürekli izlenecekse panoya dönüştür (bkz. `sky-dashboard`).
