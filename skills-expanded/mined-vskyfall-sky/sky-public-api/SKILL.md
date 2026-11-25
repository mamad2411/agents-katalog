---
name: sky-public-api
description: >-
  Dışa açık API ürünü: API anahtarı oluşturma/döndürme/kapsamları, OAuth uygulamaları, katmanlı
  rate limit ve kota başlıkları, sürümleme (tarih bazlı), OpenAPI şeması ve otomatik dokümantasyon
  (Scalar), SDK üretimi, tutarlı hata ve sayfalama, idempotency, kullanım ölçümü ve geliştirici
  portalı (anahtar yönetimi, kullanım grafiği, örnekler). "API'mizi dışarı açalım", "geliştirici
  dokümantasyonu", "API key" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Dışa Açık API

Genel uç nokta kuralları `sky-backend-api`'de. Burada **ürün olarak API**.

## API anahtarları

- Biçim: `sky_live_<rastgele 32 bayt base62>` / `sky_test_…` — öneki görünce ne olduğu anlaşılır, sır tarayıcıları yakalar.
- DB'de yalnızca **hash** (SHA-256) + ilk/son 4 karakter (`sky_live_…a1b2` gösterimi). Anahtar oluşturulunca **bir kez** gösterilir.
- Kapsamlar: `bookings:read`, `bookings:write`, `clients:read` — anahtar başına seçilir.
- Son kullanım zamanı, oluşturan kişi, isim ("Zapier entegrasyonu"); döndürme (yeni anahtar + eski için geçiş süresi).
- Test modu anahtarları ayrı veri kümesine yazar.

## Kimlik

`Authorization: Bearer sky_live_…`. Kullanıcı adına üçüncü parti uygulamalar → OAuth 2.0 (yetkilendirme kodu + PKCE),
kapsam onay ekranı, uygulama listesi ve iptal.

## Rate limit ve kota

- Anahtar/plan başına: ör. 60 istek/dk (Free), 600/dk (Pro).
- Başlıklar: `RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset`; aşımda `429` + `Retry-After`.
- Aylık kota planla ilişkili (bkz. `sky-metering-quotas`).

## Sürümleme

- Tarih bazlı: `Sky-Version: 2026-11-01` başlığı; hesap varsayılan sürümü sabitlenir.
- Kırıcı değişiklik yalnızca yeni sürümde; değişiklik günlüğü (bkz. `sky-changelog`), kullanımdan kaldırma
  başlığı (`Deprecation`, `Sunset`).

## Tutarlılık

- Kaynak nesnelerinde `id` önekli (`bkg_…`, `cli_…`), `object: "booking"`, `created_at` ISO.
- Liste yanıtı: `{ data: [], has_more, next_cursor }`.
- Hata: `{ error: { type, code, message, param, doc_url } }` — `doc_url` hataya özel doküman sayfası.
- `Idempotency-Key` POST'larda (24 saat saklanan yanıt).
- `expand[]=client` ile ilişkili nesneyi gömme.

## OpenAPI ve dokümantasyon

- Şemayı koddan üret (Zod → `@asteasolutions/zod-to-openapi` veya Hono `@hono/zod-openapi`) — doküman koddan sapmaz.
- Dokümantasyon: **Scalar** / Mintlify / Redocly — "Dene" konsolu, her dilde örnek (cURL, JS, Python, PHP).
- Hızlı başlangıç: 5 dakikada ilk başarılı istek (anahtar al → cURL kopyala → yanıt).
- SDK üretimi: Stainless / Speakeasy / openapi-ts ile TypeScript SDK.

## Geliştirici portalı (insanların sevdiği kısım)

- Anahtar yönetimi, kapsam seçimi, "kopyala".
- **İstek günlüğü**: son 7 gün — yöntem, yol, durum, süre, istek ID'si; tıklayınca gövde (sırlar maskeli).
- Kullanım grafiği ve kota çubuğu.
- Webhook ayarları (bkz. `sky-webhooks-out`).
- Durum sayfası bağlantısı.

## Güvenlik

- Anahtar sızıntısı: GitHub secret scanning ortaklığı (önekli anahtar), sızan anahtarı otomatik iptal.
- IP izin listesi (isteğe bağlı), anahtar başına.
- Audit log: anahtar oluşturma/silme, kapsam değişimi.
