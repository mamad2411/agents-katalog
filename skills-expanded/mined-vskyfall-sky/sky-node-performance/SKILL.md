---
name: sky-node-performance
description: >-
  Node.js/Bun sunucu performansı: event loop gecikmesini ölçme, CPU profilleme (--cpu-prof,
  Chrome DevTools, clinic.js, 0x flame graph), bellek sızıntısı bulma (heap snapshot karşılaştırma),
  sık darboğazlar (senkron JSON/crypto/fs, regex felaketi, büyük JSON, N+1, bağlantı havuzu),
  önbellek, stream kullanımı, cluster/çoklu süreç, Fastify/Hono serileştirme, GC ayarları ve
  yük altında doğrulama. "API yavaş", "bellek sürekli artıyor", "CPU %100" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Node Performansı

Ön yüz performansı `sky-perf`'te. Burada sunucu.

## Önce ölç

1. Hangi uç nokta, hangi yükte yavaş? (APM/trace — bkz. `sky-observability`; ya da `sky-load-testing`)
2. Zaman nerede: DB mi, harici API mi, uygulama CPU'su mu, event loop beklemesi mi?
3. Hipotez → profil → değişiklik → aynı koşulda tekrar ölç.

## Event loop gecikmesi

```ts
import { monitorEventLoopDelay } from "node:perf_hooks";
const h = monitorEventLoopDelay({ resolution: 20 }); h.enable();
setInterval(() => { log.info({ p99ms: h.percentile(99) / 1e6 }, "event loop"); h.reset(); }, 10_000);
```
p99 > 50–100ms → event loop'u bloklayan senkron iş var; tüm istekler etkilenir.

## CPU profili

```bash
node --cpu-prof dist/index.js          # .cpuprofile → Chrome DevTools > Performance'ta aç
node --inspect dist/index.js           # chrome://inspect → Profiler (canlı)
npx clinic doctor -- node dist/index.js   # otomatik teşhis; clinic flame / 0x → flame graph
```
Flame graph'ta en geniş kule = en çok CPU yiyen fonksiyon.

## Bellek sızıntısı

Belirti: RSS/heap zamanla sürekli artıyor, sonunda OOM.
1. `--inspect` ile bağlan, **heap snapshot** al → yük uygula → tekrar snapshot → "Comparison" görünümünde artan nesneler.
2. Sık sebepler: sınırsız büyüyen `Map`/dizi önbelleği (LRU kullan: `lru-cache`), kaldırılmayan event listener'lar, kapanmayan interval'lar,
   global'e takılan istek nesneleri, closure'larda büyük veri tutma, kapanmayan stream/bağlantı.
3. `process.memoryUsage()` periyodik logla; konteyner bellek sınırını `--max-old-space-size` ile uyumlu tut.

## Sık darboğazlar

| Darboğaz | Çözüm |
|---|---|
| `fs.readFileSync`, `crypto.pbkdf2Sync`, `zlib.*Sync` istek yolunda | async sürümler / worker |
| Büyük `JSON.parse/stringify` (MB'lar) | sayfalama, stream, alan seçimi; Fastify şema serileştirme |
| Felaket regex (iç içe nicelik `(a+)+`) | regex'i düzelt, girdi uzunluğu sınırı, `re2` (bkz. `sky-regex`) |
| N+1 sorgu, eksik indeks | bkz. `sky-sql`, `sky-data` |
| Bağlantı havuzu tükenmesi | havuz boyutu, uzun transaction'ları kısalt, pgBouncer |
| Her istekte yeni HTTP istemcisi / DB bağlantısı | tek örnek, keep-alive (undici varsayılanı) |
| Sıralı `await` bağımsız işlerde | `Promise.all` (bkz. `sky-js-async`) |
| Gereksiz log (her istekte büyük nesne) | seviye, örnekleme, pino (async, hızlı) |
| Sıkıştırma uygulamada | CDN/proxy'de sıkıştır |

## Ölçek

- Node tek iş parçacıklı JS → CPU çekirdeği başına bir süreç: konteyner/pod çoğalt (tercih) veya `cluster` / PM2 cluster modu.
- Durumsuz süreçler (oturum/önbellek Redis'te) → yatay ölçek.
- Ağır CPU işi → `worker_threads` havuzu (piscina) veya ayrı servis/kuyruk.

## Önbellek ve stream

Sık ve pahalı hesaplanan yanıtlar → önbellek (bkz. `sky-caching`); büyük dosya/CSV/rapor → stream ile gönder (`pipeline(readStream, res)`), belleğe yükleme.

## Çalışma zamanı

- Güncel LTS Node (her sürüm V8 iyileştirmesi getirir); Bun bazı iş yüklerinde daha hızlı — kendi senaryonda ölç.
- Framework yükü çoğu zaman önemsizdir; darboğaz genelde I/O ve sorgulardır. Yine de yüksek RPS'de Fastify/Hono Express'ten belirgin hızlı.
