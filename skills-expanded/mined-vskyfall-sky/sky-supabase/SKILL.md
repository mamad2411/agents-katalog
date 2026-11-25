---
name: sky-supabase
description: >-
  Derin Supabase: proje yapısı, @supabase/ssr ile Next.js entegrasyonu, RLS politika kalıpları
  (sahiplik, org üyeliği, rol, herkese açık okuma), security definer fonksiyonlar, Edge
  Functions, Storage ve politikaları, Realtime, veritabanı tipleri üretme, migration ve
  branching, auth hook'ları, pg_cron, maliyet ve sık güvenlik hataları. Supabase kullanan her
  projede, "RLS yazamıyorum", "veri gelmiyor", "service role" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Supabase

## Temel kurulum

- `supabase init` + yerel geliştirme (`supabase start`) — prod'a dokunmadan çalış.
- Şema değişiklikleri **migration** olarak: `supabase migration new add_bookings` → SQL yaz →
  `supabase db reset` (yerelde) → `supabase db push` (bağlı projeye, CI'dan).
- Tipler: `supabase gen types typescript --local > src/lib/database.types.ts`; istemciye ver:
  `createClient<Database>(…)`. Migration sonrası CI'da tip üretip diff kontrolü.
- Next.js: `@supabase/ssr` → `createServerClient` (cookies ile) ve `createBrowserClient`;
  `proxy.ts/middleware.ts`te oturum yenileme.

## RLS: varsayılan kapalı kapı

Her tabloda `alter table x enable row level security;` — politika yoksa **kimse** göremez (iyi).

```sql
-- sahiplik
create policy "kendi kayıtlarını görür" on notes for select using (user_id = (select auth.uid()));
create policy "kendi kaydını ekler"     on notes for insert with check (user_id = (select auth.uid()));
create policy "kendi kaydını günceller" on notes for update using (user_id = (select auth.uid())) with check (user_id = (select auth.uid()));

-- org üyeliği (çok kiracılı)
create function public.is_member(org uuid) returns boolean language sql stable security definer set search_path = '' as $$
  select exists (select 1 from public.memberships m where m.org_id = org and m.user_id = (select auth.uid()));
$$;
create policy "org üyeleri görür" on projects for select using (public.is_member(org_id));

-- herkese açık okuma, sahibi yazar
create policy "herkes okur" on posts for select using (published = true);
```
- `(select auth.uid())` sarmalaması planner'ın değeri bir kez hesaplamasını sağlar → büyük tablolarda çok hızlı.
- Politika kullanılan sütunlara **indeks** (`user_id`, `org_id`).
- `security definer` fonksiyonlarda `set search_path = ''` ve tam nitelikli isimler (güvenlik).
- Test: SQL editöründe `set role authenticated; set request.jwt.claims = '{"sub":"<uuid>"}';` ile kullanıcı gibi sorgula.
- Supabase Dashboard "Security Advisor" ve "Performance Advisor" uyarılarını sıfırla.

## Anahtarlar

| Anahtar | Nerede | Not |
|---|---|---|
| anon / publishable | İstemci | RLS ile korunur; görünmesi normal |
| service_role / secret | **Yalnızca sunucu** | RLS'yi atlar; asla `NEXT_PUBLIC_` değil, asla istemci paketi |

Sunucuda service role'u yalnızca gerçekten gereken iş için (webhook, cron, admin) ve yetkiyi kendin kontrol ederek kullan.

## Auth notları

- Sunucuda yetki için `supabase.auth.getUser()` (sunucuyla doğrular) — `getSession()` çereze güvenir.
- Profil tablosu: `auth.users` insert'ünde trigger ile `public.profiles` oluştur.
- Custom claims (rol) için **Custom Access Token Hook**; RLS'de `auth.jwt() ->> 'user_role'`.
- E-posta şablonlarını Türkçeleştir; SMTP'yi kendi sağlayıcına bağla (varsayılan limitler düşük).

## Storage

- Bucket'lar: `public` (avatar, ürün görseli) ve `private` (fatura, belge).
- Politikalar `storage.objects` üzerinde: `bucket_id = 'docs' and (storage.foldername(name))[1] = (select auth.uid())::text`
  → kullanıcılar yalnızca kendi klasörüne yazar.
- Görsel dönüşümü: `getPublicUrl(path, { transform: { width: 640, quality: 75 } })`.
- Özel dosya: kısa ömürlü `createSignedUrl` (60 sn).

## Edge Functions

Deno; webhook alma (Stripe/iyzico), üçüncü parti API çağrısı, e-posta gönderimi. Sırlar `supabase secrets set`.
`verify_jwt` varsayılan açık; webhook için kapatıp imzayı kendin doğrula.

## Realtime ve cron

- Realtime: tabloyu publication'a ekle; RLS geçerli. Detay: `sky-realtime`.
- `pg_cron` ile zamanlanmış SQL (eski kayıtları temizle, hatırlatma kuyruğu doldur); `pg_net` ile HTTP çağrısı.

## Branching ve ortamlar

- Preview branch'leri (PR başına ayrı DB) — migration'ları güvenle dene.
- Prod'da dashboard'dan şema değiştirme → yerel migration'lar ile drift. Her şey migration'dan.

## Sık hatalar

| Belirti | Sebep |
|---|---|
| Sorgu boş dizi döner, hata yok | RLS politikası yok/yanlış |
| İstemcide her şey görünüyor | RLS kapalı veya `using (true)` |
| Yavaş sorgular | `auth.uid()` select sarmalamasız, politika sütunlarında indeks yok |
| "JWT expired" | Oturum yenileme proxy/middleware'de yok |
| Insert başarısız, select çalışıyor | `with check` politikası eksik |
