---
name: saas-database
description: >
  SaaS uygulaması için Supabase veritabanı altyapısını kur. Proje oluşturma,
  şema tasarımı, Row Level Security (RLS), migration, connection pooling,
  realtime ve edge function yapılandırması. Bu skill'i kullanıcı veritabanı,
  Supabase, tablo, migration, RLS, şema veya veri modeli ile ilgili bir şey
  istediğinde kullan. "Veritabanı kur", "tablo oluştur", "Supabase ayarla",
  "migration yap" gibi ifadeler tetikler.
---

# SaaS Database — Supabase Veritabanı Altyapısı

Bu skill, bir SaaS uygulamasının veritabanı katmanını kurar. Veritabanı uygulamanın belleğidir — şema kararları, güvenlik politikaları ve bağlantı stratejisi ilk günden doğru kurulmalıdır.

**Bağımlılık:** Bu skill **saas-launcher** orkestratör skill'inin Faz 2'sinin derinleştirilmiş versiyonudur. Bağımsız olarak da kullanılabilir.

**Bağlı skill'ler:**
- **saas-auth** — Kullanıcı modeli veritabanında tanımlanır. Auth, kullanıcı kaydını burada oluşturur.
- **saas-payments** — Abonelik ve plan bilgileri veritabanında saklanır.
- **saas-storage** — Dosya metadata'sı veritabanında, dosyanın kendisi Supabase Storage'da saklanır.

---

## Supabase Proje Kurulumu

### İlk Adımlar

1. https://supabase.com adresinden hesap oluştur
2. Yeni proje oluştur — proje adı, veritabanı şifresi ve bölge seç
3. Bölge seçimi: Kullanıcıların çoğunluğuna en yakın bölge. Türkiye için `eu-central-1` (Frankfurt) önerilir
4. Dashboard'dan proje URL'si ve anon key'i al
5. `.env.local` dosyasına ekle:
   - `NEXT_PUBLIC_SUPABASE_URL` — proje URL'si (public, client'ta kullanılır)
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY` — anonim anahtar (public, RLS ile korunur)
   - `SUPABASE_SERVICE_ROLE_KEY` — servis anahtarı (gizli, sadece server-side)

**Kritik:** `SUPABASE_SERVICE_ROLE_KEY` asla `NEXT_PUBLIC_` prefix'i almamalı. Bu anahtar RLS'i bypass eder — client'a sızarsa tüm veriye erişim açılır.

### Supabase Client Kurulumu

İki farklı client oluştur:

**Browser client (client component'ler için):** Anon key ile çalışır, RLS kurallarına tabidir. Kullanıcının kendi verisine erişim için.

**Server client (API route'ları ve server component'ler için):** Service role key ile çalışır, RLS'i bypass eder. Admin işlemleri, webhook handler'lar ve veri migration'ları için.

**Middleware client:** Oturum yenileme ve auth kontrolü için. Edge Runtime uyumlu olmalı.

Her client'ı ayrı bir dosyada tanımla ve projede tek yerden import et. Client'ları her dosyada yeniden oluşturma.

---

## Şema Tasarımı

### Temel Tablolar

Her SaaS'ta olması gereken minimum tablolar:

**users** — Kullanıcı profil bilgileri
- `id` (UUID, primary key — Supabase Auth'un user ID'si ile eşleşmeli)
- `email` (text, unique, not null)
- `full_name` (text)
- `avatar_url` (text, nullable)
- `plan` (text, default: 'free')
- `stripe_customer_id` (text, nullable, unique)
- `stripe_subscription_id` (text, nullable)
- `plan_expires_at` (timestamptz, nullable)
- `created_at` (timestamptz, default: now())
- `updated_at` (timestamptz, default: now())

**Kullanıcı oluşturma tetikleyicisi:** Supabase Auth'a yeni kullanıcı kaydolduğunda `auth.users` tablosuna satır eklenir. Bu olayı dinleyen bir PostgreSQL trigger fonksiyonu yazarak `public.users` tablosuna otomatik kayıt oluştur. Bu sayede Auth ve veritabanı her zaman senkron kalır.

**Ek tablolar (projeye göre):**
- `projects` / `workspaces` — Kullanıcının oluşturduğu kaynaklar
- `subscriptions` — Detaylı abonelik geçmişi
- `api_usage` — API kullanım sayaçları (plan limitleri için)

### Şema Tasarım İlkeleri

- **UUID kullan.** Auto-increment integer yerine UUID — sıralı ID'ler güvenlik riski (tahmin edilebilir) ve multi-tenant uygulamalarda sorun yaratır.
- **Zaman damgası her tabloda olsun.** `created_at` ve `updated_at` her tabloya ekle. Debugging ve analitik için vazgeçilmez.
- **Soft delete düşün.** Kritik tablolarda `deleted_at` alanı ekleyerek silme yerine işaretle. Geri alma imkânı ve yasal uyumluluk (KVKK veri saklama süreleri) için.
- **İlişkileri foreign key ile zorunlu kıl.** Veritabanı seviyesinde ilişki bütünlüğü sağla. Uygulama koduna güvenme.
- **Index'leri erken ekleme.** İlk aşamada sadece foreign key ve sık sorgulanan alanlara index ekle. Geri kalanını sorgu yavaşlayınca ekle.

---

## Row Level Security (RLS)

### Neden Zorunlu

RLS, Supabase'in en önemli güvenlik katmanıdır. Anon key client'ta açıkça görünür — RLS olmadan herhangi biri bu anahtarla tüm veriye erişebilir.

**RLS'i her tabloda aktifleştir.** İstisnasız. RLS aktif değilse tablo herkese açıktır.

### Temel Politika Kalıpları

**Kullanıcı kendi verisini görsün:**
- SELECT: `auth.uid() = user_id` koşulu ile
- INSERT: `auth.uid() = user_id` koşulu ile
- UPDATE: `auth.uid() = user_id` koşulu ile
- DELETE: `auth.uid() = user_id` koşulu ile (veya soft delete kullanıyorsan UPDATE)

**Takım bazlı erişim:**
- Kullanıcının üye olduğu takımların verisine erişim
- `team_members` junction tablosu üzerinden kontrol

**Public okuma, authenticated yazma:**
- Blog yazıları, ürün sayfaları gibi herkesin okuması gereken veriler
- SELECT: herkese açık
- INSERT/UPDATE/DELETE: sadece admin rolü

### RLS Test Etme

RLS politikalarını mutlaka test et:
1. Supabase Dashboard'da SQL Editor'ü aç
2. Farklı kullanıcı rolleri ile sorgu çalıştır
3. Bir kullanıcının başka birinin verisine erişemediğini doğrula
4. Anon (giriş yapmamış) erişimin beklendiği gibi çalıştığını doğrula

---

## Migration Stratejisi

### Supabase CLI ile Migration

Supabase CLI (`npx supabase`) ile migration yönetimi:

1. `npx supabase init` — lokal Supabase projesini başlat
2. `npx supabase migration new <isim>` — yeni migration dosyası oluştur
3. Migration dosyasına SQL yaz (CREATE TABLE, ALTER TABLE vb.)
4. `npx supabase db push` — migration'ları remote veritabanına uygula

### Migration İlkeleri

- **Her değişiklik migration olsun.** Dashboard'dan manuel tablo oluşturma yerine migration dosyası yaz. Tekrarlanabilir, versiyonlanabilir, geri alınabilir.
- **Migration'lar idempotent olsun.** `IF NOT EXISTS` kullan. Aynı migration iki kez çalışsa bile hata vermemeli.
- **Veri kaybetme.** Sütun silme veya tablo kaldırma migration'larında dikkatli ol. Önce verinin yedeklendiğinden emin ol.
- **RLS politikalarını migration'a dahil et.** Tablo oluşturma ile birlikte RLS'i de aynı migration'da aktifleştir.

---

## Connection Pooling

### Serverless Ortamda Neden Kritik

Vercel gibi serverless platformlarda her function invocation yeni bir veritabanı bağlantısı açar. Supabase'in ücretsiz planında bağlantı limiti düşüktür — limit aşılırsa "too many connections" hatası alırsın.

### Çözüm: Supavisor (Supabase Pooler)

Supabase dahili connection pooler sunar (Supavisor). Dashboard'da "Connection Pooling" sekmesinden pooler URL'sini al. Direct connection yerine pooler URL'sini kullan:

- **Direct:** `postgresql://user:pass@host:5432/db` — development için
- **Pooler:** `postgresql://user:pass@host:6543/db` — production için (port farkına dikkat: 6543)

`.env.local`'da iki ayrı URL tut:
- `DATABASE_URL` — pooler URL (uygulama bağlantısı)
- `DIRECT_URL` — direct URL (migration'lar için — migration araçları pooler'dan geçemeyebilir)

---

## Realtime (İleri Seviye)

Supabase Realtime, veritabanı değişikliklerini WebSocket üzerinden canlı olarak client'a iletir. Kullanım alanları: canlı bildirimler, ortak çalışma, chat, canlı dashboard.

**Day 1'de gerekmez.** Çoğu SaaS'ta ilk versiyonda realtime ihtiyacı yoktur. İhtiyaç ortaya çıkınca ekle.

Aktifleştirme: İlgili tablonun "Realtime" özelliğini Dashboard'dan aç. RLS politikaları realtime erişime de uygulanır.

---

## Supabase Edge Functions (İleri Seviye)

Supabase'in Deno tabanlı serverless function'ları. Next.js API route'ları varken genellikle gerekmez. Kullanım alanları: Supabase Webhook tetikleyicileri, CRON job'lar, veritabanına çok yakın işlemler (latency kritikse).

**Çoğu SaaS için Next.js API route'ları yeterlidir.** Edge Function'ları yalnızca spesifik bir ihtiyaç varsa değerlendir.

---

## Gotchas

- **Service role key client'a sızarsa felaket.** Bu anahtar RLS'i bypass eder. `NEXT_PUBLIC_` prefix'i verme, sadece server-side'da kullan.
- **RLS unutulursa veri sızar.** Yeni tablo oluşturunca RLS'i hemen aktifleştir. Dashboard'da tablo oluşturunca RLS varsayılan olarak kapalıdır.
- **Auth trigger olmadan kullanıcı kaydı eksik kalır.** Supabase Auth'a kayıt olan kullanıcı `auth.users`'da oluşur ama `public.users`'da oluşmaz — trigger'ı kur.
- **Pooler port'u farklıdır.** Direct bağlantı 5432, pooler 6543. Yanlış port = bağlantı hatası.
- **Migration'sız dashboard değişikliği kaybolur.** Dashboard'dan yapılan tablo değişiklikleri migration dosyasında değildir — başka bir ortama taşınamaz, `supabase db reset` ile kaybolur.
- **Supabase ücretsiz plan uyku modu.** 7 gün inaktif kalırsa proje duraklatılır. Development'ta düzenli istek göndererek uyandır veya Pro plana geç.
- **TypeScript tipleri üret.** `npx supabase gen types typescript` ile veritabanı şemasından TypeScript tipleri üret. Elle tip tanımlamaya çalışma — şema değişince tipler senkrondan çıkar.
