---
name: sky-cloudflare
description: >-
  Cloudflare geliştirici platformu: Workers (edge'de kod), Pages ve statik varlıklar, Hono ile
  Workers API, D1 (SQLite), R2 (S3 uyumlu, çıkış ücretsiz), KV, Durable Objects (durumlu
  gerçek zamanlı), Queues, Cron Triggers, Workers AI, Turnstile (CAPTCHA alternatifi), DNS/SSL/
  önbellek kuralları, WAF ve rate limiting, wrangler ile geliştirme ve dağıtım, Next.js'i
  Workers'ta çalıştırma ve sınırlar. Cloudflare kullanırken kullan.
disable-model-invocation: true
---

# Sky · Cloudflare

## Workers temelleri

```ts
// src/index.ts — Hono ile
import { Hono } from "hono";
type Bindings = { DB: D1Database; BUCKET: R2Bucket; CACHE: KVNamespace; API_KEY: string };
const app = new Hono<{ Bindings: Bindings }>();

app.get("/api/bookings", async (c) => {
  const { results } = await c.env.DB.prepare("select * from bookings where org_id = ? order by starts_at").bind(orgId).all();
  return c.json(results);
});
export default app;
```
```toml
# wrangler.toml
name = "api"
main = "src/index.ts"
compatibility_date = "2026-10-01"
compatibility_flags = ["nodejs_compat"]
[[d1_databases]]
binding = "DB"
database_name = "app"
database_id = "…"
[[r2_buckets]]
binding = "BUCKET"
bucket_name = "uploads"
```
- `wrangler dev` (yerel, gerçek binding'lerin yerel kopyalarıyla), `wrangler deploy`, `wrangler secret put API_KEY`.
- `wrangler types` ile binding tipleri üret.
- Soğuk başlatma neredeyse yok; dünya çapında edge'de çalışır.

## Depolama seçimi

| Servis | Ne için |
|---|---|
| **D1** | SQLite tabanlı ilişkisel DB (migration: `wrangler d1 migrations apply`); küçük-orta veri |
| **R2** | dosyalar, **çıkış ücreti yok**; S3 API uyumlu; public bucket veya presigned URL |
| **KV** | okuma ağırlıklı, nihai tutarlı anahtar-değer (yapılandırma, önbellek, feature flag) |
| **Durable Objects** | güçlü tutarlı tekil durum: sohbet odası, işbirlikli doküman, rate limiter, sayaç; WebSocket hibernation |
| **Hyperdrive** | Workers'tan dış Postgres'e hızlı bağlantı havuzu |
| **Queues** | arka plan işleri, toplu tüketici |
Yüksek yazma yoğunluğu veya büyük ilişkisel veri → Hyperdrive + harici Postgres.

## Diğer parçalar

- **Cron Triggers**: `[triggers] crons = ["0 6 * * *"]` + `scheduled()` handler (UTC!).
- **Workers AI**: edge'de model çalıştırma (embedding, küçük LLM'ler, görsel); **Vectorize** vektör DB; **AI Gateway** LLM çağrıları için önbellek/log/rate limit.
- **Turnstile**: görünmez/az etkileşimli bot koruması, ücretsiz — reCAPTCHA'dan çok daha az sinir bozucu (bkz. `sky-forms`). Token'ı sunucuda `siteverify` ile doğrula.
- **Email Routing / Email Workers**: gelen e-postayı işleme.
- **Images / Stream**: görsel dönüşüm ve video.

## Next.js ve framework'ler

- Next.js → `@opennextjs/cloudflare` adaptörü (Node uyumluluğu ile); Astro, Remix/React Router, SvelteKit, Hono yerel destekli.
- Statik site/SPA → Workers static assets (eski adıyla Pages).

## Sınırlar (bil, tasarla)

CPU süresi istek başına sınırlı (plan bazlı), bellek ~128MB, tam Node API yok (`nodejs_compat` ile çoğu var: Buffer, crypto, stream),
yerel dosya sistemi yok, uzun süreli TCP sınırlı. Ağır iş → Queues + tüketici veya harici servis.

## Ağ katmanı

- DNS + proxy (turuncu bulut) → ücretsiz SSL, DDoS koruması, CDN.
- SSL modu **Full (strict)** (Flexible asla — kaynak ile Cloudflare arası şifresiz kalır).
- Önbellek kuralları: statik yollar uzun TTL, `/api/*` bypass; "Cache Everything" kullanırken kişisel sayfalara dikkat.
- WAF yönetilen kurallar, **Rate Limiting** kuralları (giriş/OTP uç noktaları), Bot Fight Mode; ülke bazlı engelleme gerekiyorsa.
- Redirect Rules ile `www` → apex, eski URL'ler (bkz. `sky-seo`).

## Gözlem

`wrangler tail` canlı log, Workers Logs/Observability, Sentry (`@sentry/cloudflare`), Analytics Engine ile özel metrikler.
