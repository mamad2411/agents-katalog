---
name: sky-redis
description: >-
  Redis (ve Valkey/Upstash/Dragonfly) derinlemesine: veri yapıları ve doğru kullanım (string,
  hash, list, set, sorted set, stream, HyperLogLog, bitmap, geo), anahtar tasarımı ve TTL,
  atomik işlemler ve Lua betikleri, dağıtık kilit (doğru ve yanlış yolları), rate limiting
  algoritmaları, pub/sub vs Streams (tüketici grupları), oturum deposu, lider tablosu, bellek ve
  tahliye politikaları, kalıcılık (RDB/AOF), kümeleme ve sunucusuz Redis. Redis ile çalışırken kullan.
disable-model-invocation: true
---

# Sky · Redis

Önbellek kalıpları `sky-caching`'de; burada Redis'in kendisi.

## Veri yapısı → kullanım

| Yapı | Kullanım | Komutlar |
|---|---|---|
| String | önbellek, sayaç, bayrak | `SET k v EX 300 NX`, `INCR`, `GETEX` |
| Hash | nesne alanları (profil, sepet) | `HSET`, `HINCRBY`, `HGETALL` |
| List | basit kuyruk, son N öğe | `LPUSH` + `LTRIM 0 99`, `BRPOP` |
| Set | tekil üyeler, etiketler, "kim gördü" | `SADD`, `SISMEMBER`, `SINTER` |
| Sorted set | **lider tablosu**, zaman sıralı, öncelik kuyruğu, sliding window | `ZADD`, `ZINCRBY`, `ZREVRANGE … WITHSCORES`, `ZREMRANGEBYSCORE` |
| Stream | olay günlüğü, tüketici grupları, güvenilir kuyruk | `XADD`, `XREADGROUP`, `XACK`, `XAUTOCLAIM` |
| HyperLogLog | yaklaşık tekil sayım (günlük tekil ziyaretçi) | `PFADD`, `PFCOUNT` |
| Bitmap | günlük aktiflik, özellik bayrakları | `SETBIT`, `BITCOUNT` |
| Geo | yakınlık | `GEOADD`, `GEOSEARCH` |

## Anahtar tasarımı

`{uygulama}:{varlık}:{id}:{alt}` (`sky:org:42:stats`), kiracı ID'si anahtarda; her geçici anahtarda TTL; `KEYS *` üretimde **asla** (bloklar) → `SCAN`. Büyük anahtar (MB'larca değer, milyonlarca elemanlı koleksiyon) performansı öldürür.

## Atomiklik

Tek komutlar atomik; çok adımlı işlem → `MULTI/EXEC` (koşulsuz) veya **Lua betiği** (koşullu mantık, tek atomik birim):
```lua
-- stok düş: yeterliyse azalt, değilse -1 dön
local s = tonumber(redis.call('GET', KEYS[1]) or '0')
if s >= tonumber(ARGV[1]) then return redis.call('DECRBY', KEYS[1], ARGV[1]) else return -1 end
```

## Dağıtık kilit

`SET lock:job:42 <rastgele-token> NX PX 30000` → işi yap → **yalnızca token eşleşiyorsa** sil (Lua ile kontrol+sil). Kilit süresi işten uzun olmalı veya yenilenmeli.
Doğruluk kritikse (para, çift işlem) yalnızca Redis kilidine güvenme: DB kısıtı / idempotency anahtarı / fencing token (bkz. `sky-payments`, `sky-scheduling`).

## Rate limiting

Sabit pencere (`INCR` + `EXPIRE` — basit), kayan pencere (sorted set + zaman damgaları — doğru), token bucket (Lua). Hazır: `@upstash/ratelimit`, `rate-limiter-flexible`.

## Pub/Sub vs Streams

- **Pub/Sub**: anlık yayın, bağlı olmayan kaçırır, kalıcılık yok — gerçek zamanlı bildirim dağıtımı (bkz. `sky-realtime`).
- **Streams**: kalıcı, tüketici grupları, onay (`XACK`), bekleyenleri devralma — güvenilir iş/olay kuyruğu. Uzunluğu sınırla (`XADD … MAXLEN ~ 100000`).

## Bellek ve kalıcılık

- `maxmemory` + tahliye politikası: saf önbellekte `allkeys-lru`/`allkeys-lfu`; kalıcı veri de tutuyorsan `volatile-lru` (yalnızca TTL'liler silinir) — karıştırma, ayrı örnek kullan.
- Kalıcılık: RDB (anlık görüntü), AOF (her yazma — `everysec`), ikisi birden; saf önbellekte kapalı olabilir.
- `INFO memory`, `MEMORY USAGE key`, `--bigkeys`, `SLOWLOG GET` ile teşhis.

## Dağıtım

Yönetilen (Upstash — sunucusuz/HTTP, ElastiCache, Redis Cloud), uyumlu alternatifler (Valkey — açık kaynak çatal, Dragonfly — çok çekirdekli); kümede çoklu anahtar işlemleri aynı hash slot'ta olmalı (`{org:42}:a`, `{org:42}:b`). Sunucusuzda bağlantı yerine HTTP istemcisi (Upstash) bağlantı patlamasını önler.
