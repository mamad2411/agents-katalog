---
name: sky-caching
description: >-
  Önbellekleme mühendisliği: hangi katmanda (tarayıcı, CDN, Next Data Cache, uygulama,
  Redis, DB), cache-aside ve stale-while-revalidate kalıpları, Upstash Redis ve Vercel KV,
  anahtar tasarımı ve sürümleme, TTL seçimi, etiket bazlı invalidation, stampede (thundering
  herd) koruması, HTTP Cache-Control başlıkları, kişisel veriyi cache'lememe ve ölçüm.
  "Cache ekle", "Redis", "her istekte DB'ye gidiyor", "yavaş API" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Önbellekleme

## Katman haritası (yukarıdan aşağı, en ucuzdan)

| Katman | Ne için | Araç |
|---|---|---|
| Tarayıcı | statik varlık, kullanıcıya özel GET | `Cache-Control`, Service Worker |
| CDN | herkese aynı HTML/JSON/görsel | `s-maxage`, `stale-while-revalidate`, Vercel/Cloudflare |
| Framework | sayfa/fetch sonuçları | Next Data Cache, `"use cache"`, `unstable_cache` |
| Uygulama | pahalı hesap, üçüncü parti API | Redis (Upstash), bellek içi LRU |
| DB | sorgu planları, materialized view | `materialized view` + `refresh concurrently` |

Önce **ölç**: hangi istek yavaş, ne sıklıkta çağrılıyor, veri ne sıklıkla değişiyor.

## HTTP başlıkları

```
Hash'li statik:      Cache-Control: public, max-age=31536000, immutable
Herkese açık sayfa:  Cache-Control: public, s-maxage=300, stale-while-revalidate=86400
Kişisel veri:        Cache-Control: private, no-store
API (kısa):          Cache-Control: public, s-maxage=30, stale-while-revalidate=300
```
`stale-while-revalidate` kullanıcıya her zaman hızlı yanıt verir, tazelemeyi arka planda yapar — en iyi dost.
`Vary: Accept-Language` gibi başlıklarla varyantları ayır; `Vary: Cookie` CDN önbelleğini öldürür.

## Cache-aside (Redis)

```ts
export async function cached<T>(key: string, ttl: number, fn: () => Promise<T>): Promise<T> {
  const hit = await redis.get<T>(key);
  if (hit !== null) return hit;
  const val = await fn();
  await redis.set(key, val, { ex: ttl + Math.floor(Math.random() * ttl * 0.1) }); // jitter: aynı anda düşmesinler
  return val;
}
const stats = await cached(`v1:org:${orgId}:stats`, 300, () => computeStats(orgId));
```

## Anahtar tasarımı

`{sürüm}:{varlık}:{id}:{alt}` → `v1:org:42:stats`, `v1:product:abc:tr`.
- Sürüm öneki: şema değişince `v2` yap, eskiler TTL ile ölür (toplu silme yok).
- Kiracı/kullanıcı kimliği anahtarda → veri sızıntısı imkânsız.
- Locale/para birimi gibi varyantlar anahtarda.

## Invalidation

"Bilgisayar biliminde iki zor şey" — basit tut:
1. **TTL** ile kabul edilebilir bayatlık (çoğu durumda yeter).
2. **Yazmada sil**: veriyi değiştiren yer ilgili anahtarı siler (`redis.del`).
3. **Etiketler**: Next `revalidateTag("org:42")`; Redis'te etiket → anahtar seti.
Yazma yolunda silmeyi unutmamak için invalidation'ı servis katmanında tek yerde yap.

## Stampede koruması

Popüler anahtar düşünce 1000 istek aynı anda DB'ye gider:
- TTL'e jitter (yukarıda).
- **Tek uçuş (single-flight)**: aynı anahtar için yalnızca bir hesaplama, diğerleri onu bekler.
- **Erken tazeleme**: TTL'in %80'inde arka planda yenile, süresi dolmuş değeri dönmeye devam et (SWR).
- Kısa süreli kilit: `SET lock:key 1 NX EX 10`.

## Ne cache'lenmez

- Yetki kararları (rol değişince anında etki etmeli) — ya da çok kısa TTL + yazmada sil.
- Ödeme durumu, stok sayısı (kritik anda), tek seferlik token'lar.
- Kişisel veri paylaşılan (CDN) önbellekte — asla.

## Rate limit ve diğer Redis kullanımları

- `@upstash/ratelimit` (sliding window) — giriş, OTP, API (bkz. `sky-backend-api`).
- Oturum deposu, kuyruk (bkz. `sky-jobs`), sayaçlar (`INCR`), lider tablosu (`ZADD`), tekilleştirme (`SETNX`).

## Ölçüm

İsabet oranı (hit/miss) logla; < %70 ise anahtar/TTL tasarımını gözden geçir. Gecikme önce/sonra
(bkz. `sky-perf`). Redis bellek kullanımı ve tahliye (eviction) politikası (`allkeys-lru`).
