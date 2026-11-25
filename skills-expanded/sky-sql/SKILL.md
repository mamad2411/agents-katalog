---
name: sky-sql
description: >-
  Ham SQL ustalığı (Postgres): CTE ve recursive sorgular, window fonksiyonları (sıralama,
  hareketli ortalama, önceki satır), upsert (on conflict), jsonb sorgulama ve indeksleme,
  generate_series ile boşluksuz zaman serileri, lateral join ile "her grubun son N kaydı",
  partial/expression indeksler, EXPLAIN ANALYZE okuma, Türkçe collation ve ORM'den kaçış
  kapakları. "Bu sorguyu yaz", "rapor sorgusu", "SQL yavaş", "ORM ile yapamıyorum" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · SQL Ustalığı

ORM günlük işler içindir; raporlar, analizler ve performans kritik yerlerde SQL yaz.
Her ORM'in kaçış kapısı var: Drizzle `sql\`\``, Prisma `$queryRaw` (tagged template — **parametreli**,
asla string birleştirme).

## Window fonksiyonları

```sql
-- her müşterinin randevu sırası ve bir önceki randevudan geçen gün
select client_id, starts_at,
  row_number() over w as nth,
  starts_at - lag(starts_at) over w as since_prev
from bookings window w as (partition by client_id order by starts_at);

-- 7 günlük hareketli ortalama gelir
select day, revenue, avg(revenue) over (order by day rows between 6 preceding and current row) as ma7 from daily_revenue;

-- kategori içi sıralama, ilk 3
select * from (select *, rank() over (partition by category order by sales desc) r from products) t where r <= 3;
```

## Boşluksuz zaman serisi (grafikler için şart)

```sql
select d::date as day, coalesce(count(b.id), 0) as bookings
from generate_series(date_trunc('day', now() - interval '29 days'), date_trunc('day', now()), interval '1 day') d
left join bookings b on b.starts_at >= d and b.starts_at < d + interval '1 day'
group by d order by d;
```
Veri olmayan günler 0 olarak gelir → grafik çökmez (bkz. `sky-dataviz`). Saat dilimi:
`date_trunc('day', starts_at at time zone 'Europe/Istanbul')`.

## Her grubun son N kaydı (lateral)

```sql
select c.id, c.name, last.*
from clients c
cross join lateral (select starts_at, service from bookings b where b.client_id = c.id order by starts_at desc limit 3) last;
```
`(client_id, starts_at desc)` indeksiyle çok hızlı.

## Upsert

```sql
insert into daily_stats (day, org_id, views) values ($1, $2, 1)
on conflict (day, org_id) do update set views = daily_stats.views + 1;
```
Sayaçlar, senkron işler, idempotent içe aktarım için. `returning *` ile sonucu al.

## CTE ve recursive

```sql
-- kategori ağacı (yol ile)
with recursive tree as (
  select id, name, parent_id, name::text as path from categories where parent_id is null
  union all
  select c.id, c.name, c.parent_id, tree.path || ' › ' || c.name from categories c join tree on c.parent_id = tree.id
) select * from tree order by path;
```

## jsonb

```sql
select * from events where payload @> '{"type":"signup"}';           -- içerme (GIN indeksli)
select payload->>'plan' as plan, count(*) from events group by 1;     -- alan çıkarma
create index events_payload on events using gin (payload jsonb_path_ops);
update settings set data = jsonb_set(data, '{notifications,email}', 'false');
```
Sık sorgulanan jsonb alanını **generated column** + B-tree indeksle çıkar.

## İndeks türleri

- B-tree: eşitlik/aralık/sıralama (varsayılan). Bileşikte eşitlik sütunları önce.
- Partial: `create index on bookings (starts_at) where status = 'confirmed';`
- Expression: `create index on users (lower(email));`
- GIN: jsonb, dizi, full-text, trigram. GiST: coğrafya, aralık.
- Covering: `create index on orders (user_id) include (total, status);` → index-only scan.

## EXPLAIN ANALYZE okuma

`explain (analyze, buffers) select …`
- `Seq Scan` büyük tabloda + filtre → indeks eksik.
- `rows=10 (actual rows=50000)` → istatistikler eski: `analyze tablo;`.
- `Nested Loop` + büyük iç döngü → join sırası/indeks.
- `Sort` + `external merge Disk` → `work_mem` veya sıralı indeks.
- En büyük `actual time` düğümüne odaklan.

## Türkçe

- Sıralama: `order by name collate "tr-TR-x-icu"` (ç, ğ, ı, ö, ş, ü doğru yerde).
- Büyük/küçük harf duyarsız karşılaştırma: ICU nondeterministic collation veya normalize sütun (bkz. `sky-search`).

## Güvenlik

- Parametreli sorgu; tablo/sütun adı dinamikse **izinli liste** ile.
- Rapor sorgularını salt okunur rol / replica üzerinde; `statement_timeout` (ör. 5s).
