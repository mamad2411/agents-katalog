---
name: sky-data
description: >-
  Veritabanı katmanı: şema tasarımı, ilişkiler, migration, indeksleme, sorgu performansı, N+1,
  transaction, soft delete, çok kiracılı (multi-tenant) veri, Prisma/Drizzle/Supabase/Postgres/
  SQLite kalıpları. Tablo/model eklerken, migration yazarken veya yavaş sorguları incelerken kullan.
disable-model-invocation: true
---

# Sky · Veri

## Şema tasarımı

- Birincil anahtar: `uuid` (v7 tercih — sıralı) veya `bigint identity`. Dışa açılan ID tahmin
  edilemez olmalı.
- Her tabloda `created_at timestamptz default now()`, `updated_at timestamptz`.
- Para: `numeric(12,2)` veya kuruş cinsinden `bigint`; **asla float**.
- Zaman: `timestamptz` (UTC sakla, kullanıcı saat diliminde göster).
- Enum'lar için Postgres `enum` veya `check` kısıtı; serbest metin değil.
- `NOT NULL` varsayılan; null'ı bilinçli seç.
- Benzersizlik iş kuralıysa veritabanında `unique` kısıtı — yalnızca uygulamada kontrol yarışa açıktır.
- Yabancı anahtar + `on delete` davranışı açıkça (`cascade` / `restrict` / `set null`).
- E-posta gibi alanlarda büyük/küçük harf duyarsız benzersizlik (`citext` veya `lower()` indeksi).

## İndeksler

- Her yabancı anahtar sütununa indeks.
- `WHERE` + `ORDER BY` birlikte kullanılan sütunlara bileşik indeks (eşitlik sütunları önce).
- Kısmi indeks: `where deleted_at is null`.
- Şüphede `EXPLAIN ANALYZE` çalıştır; `Seq Scan` büyük tabloda alarm.

## Sorgu kalıpları

- **N+1'den kaçın:** listede ilişki gerekiyorsa `include`/`with`/join ya da `IN (...)` toplu sorgu.
- Yalnızca gereken sütunları seç (`select`).
- Sayfalama cursor ile (`where id > $cursor order by id limit 20`); büyük `OFFSET` yavaştır.
- Birden çok yazma tek iş birimiyse **transaction**.
- Sayaç/stok gibi yarışa açık güncellemeler: atomik `update ... set x = x - 1 where x > 0`
  veya satır kilidi (`select ... for update`).

## Migration kuralları

- Her şema değişikliği migration dosyasıyla; elle prod DB'ye dokunma.
- Geriye uyumlu adımlar (expand → migrate → contract):
  1. Yeni sütunu nullable ekle, 2. kodu iki sütunu da yazacak şekilde dağıt,
  3. veriyi doldur, 4. `NOT NULL` yap, 5. eski sütunu kaldır.
- Büyük tabloda indeks: `CREATE INDEX CONCURRENTLY`.
- Migration'ı geri alma planıyla yaz; yıkıcı adımları (drop) ayrı migration'da yap ve kullanıcıya sor.

## Çok kiracılı veri

- Her kiracıya ait tabloda `tenant_id`/`org_id` + indeks.
- Tüm sorgular bu filtreyi içersin — tercihen repository katmanında zorunlu veya Postgres RLS.

## Soft delete

- `deleted_at timestamptz null`; varsayılan sorgular `deleted_at is null` filtresiyle.
- KVKK/GDPR silme talebi için gerçek silme veya anonimleştirme yolu ayrıca olsun.

## ORM notları

**Drizzle:** şema TS'de, `drizzle-kit generate` → migration; ilişkiler için `relations()`.
**Prisma:** `prisma migrate dev` (lokal) / `migrate deploy` (prod); `select` ile alan kısıtla;
seri ortamda tek `PrismaClient` örneği (global singleton).
**Supabase:** her tabloda RLS politikası; `auth.uid()` ile sahiplik; istemci yalnızca anon key.

## Seed & test verisi

- `seed.ts` deterministik; test kullanıcıları ve örnek kayıtlar.
- Testler gerçek bir test DB'sinde (Docker/SQLite) transaction içinde çalışıp geri alınsın.
