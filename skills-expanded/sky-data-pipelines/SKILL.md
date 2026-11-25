---
name: sky-data-pipelines
description: >-
  Veri hatları ve analitik altyapı: ETL vs ELT, operasyonel DB'den analitik depoya veri taşıma
  (CDC, toplu yükleme, Airbyte/dlt/Fivetran), ambar seçimi (ClickHouse, BigQuery, Snowflake,
  DuckDB/MotherDuck), dbt ile SQL dönüşümleri ve testler, orkestrasyon (Dagster, Airflow,
  Prefect, basit cron), veri kalitesi kontrolleri, olay verisi şeması, Parquet ve nesne
  depolama, maliyet ve KVKK. "Raporlama altyapısı", "veri ambarı", "ETL", "dbt" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Veri Hatları

## Önce: gerekli mi?

Küçük ölçekte: üretim DB'sinin **okuma replikası** + SQL raporlar veya DuckDB ile dışa aktarılmış veri (bkz. `sky-data-analysis`) yeter.
Ayrı analitik altyapı şunlarda: raporlar üretim DB'sini yavaşlatıyor, birden çok kaynak birleşiyor (ödeme, CRM, analitik olaylar), geçmiş veri ve karmaşık metrikler.

## Mimari (modern, sade)

```
kaynaklar (Postgres, Stripe/iyzico, PostHog, CSV) → yükleme (dlt / Airbyte / CDC) → ham katman (ambar)
   → dbt dönüşümleri (staging → intermediate → marts) → BI / pano / ters ETL
```
ELT: önce ham yükle, ambar içinde SQL ile dönüştür (esnek, tekrar çalıştırılabilir).

## Ambar seçimi

| İhtiyaç | Seçim |
|---|---|
| Hızlı analitik, olay verisi, self-host veya bulut | **ClickHouse** |
| Yönetilen, sunucusuz, Google ekosistemi | BigQuery |
| Kurumsal, çok bulut | Snowflake |
| Küçük-orta, ucuz, tek dosya/S3 üzerinde | **DuckDB** (+ MotherDuck) |
| Zaman serisi metrikler | TimescaleDB / ClickHouse |

## Yükleme

- **dlt** (Python): API/DB kaynaklarından artımlı yükleme, şema evrimi — küçük ekip için harika; Airbyte (hazır konektörler), Fivetran (yönetilen).
- Artımlı: `updated_at` / imleç bazlı; silmeleri yakalamak için CDC (Postgres mantıksal replikasyon, Debezium) veya soft delete.
- Ham veri Parquet olarak nesne depolamada da saklanabilir (ucuz, tekrar işlenebilir).

## dbt

```sql
-- models/marts/fct_bookings.sql
select b.id, b.org_id, b.starts_at::date as booking_date, s.name as service, b.status,
       coalesce(p.amount_minor, 0) / 100.0 as revenue_try
from {{ ref('stg_bookings') }} b
left join {{ ref('stg_services') }} s on s.id = b.service_id
left join {{ ref('stg_payments') }} p on p.booking_id = b.id and p.status = 'succeeded'
```
```yaml
# models/marts/schema.yml
models:
  - name: fct_bookings
    columns:
      - name: id
        tests: [unique, not_null]
      - name: status
        tests: [{ accepted_values: { values: ['pending','confirmed','cancelled','completed','no_show'] } }]
```
Katmanlar: `stg_` (temizleme/yeniden adlandırma, kaynak başına), `int_` (birleştirme), `fct_`/`dim_` (iş tabloları). Testler, dokümantasyon (`dbt docs`), artımlı modeller (büyük tablolar).
**Metrik tanımları tek yerde** (semantic layer veya marts) — "aylık gelir" her panoda aynı hesaplansın.

## Orkestrasyon

Basit: cron + `dbt build` (GitHub Actions schedule bile olur). Büyüyünce: **Dagster** (varlık odaklı, yerel geliştirme iyi), Airflow (yaygın), Prefect. Başarısızlıkta alarm, yeniden deneme, veri tazeliği kontrolü.

## Veri kalitesi

Satır sayısı ani düşüş/artış, null oranı, tekillik, referans bütünlüğü, tazelik ("dün verisi geldi mi?") — dbt testleri + alarm (bkz. `sky-observability`).

## KVKK ve maliyet

Ambarda kişisel veri minimum (hash'li ID, gerekli alanlar), erişim rolleri, saklama süreleri ve silme taleplerinin ambara da yansıması (bkz. `sky-privacy-engineering`). Maliyet: sorgu başına ücretli ambarlarda bölümleme (partition) + kümeleme, gereksiz tam tarama yok.
