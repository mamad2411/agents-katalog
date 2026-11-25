---
name: sky-js-async
description: >-
  JavaScript asenkron programlama ustalığı: Promise zincirleri ve async/await, paralel vs sıralı
  çalıştırma (Promise.all, allSettled, any, race), eşzamanlılık sınırı (p-limit), zaman aşımı ve
  iptal (AbortController, AbortSignal.timeout/any), yeniden deneme, event loop (microtask/
  macrotask), unhandled rejection, async iterator ve stream'ler (Web Streams, Node streams),
  Web Worker/worker_threads, debounce/throttle ve yarış durumları. Async kod, "bu neden sırayla
  çalışıyor", "istek iptal edilmiyor" durumlarında kullan.
disable-model-invocation: true
---

# Sky · Asenkron JavaScript

## Sıralı mı, paralel mi?

```ts
// ✗ farkında olmadan sıralı (toplam = a + b)
const user = await getUser(id);
const orders = await getOrders(id);
// ✓ bağımsızsa paralel (toplam = max(a, b))
const [user, orders] = await Promise.all([getUser(id), getOrders(id)]);
```
| API | Davranış |
|---|---|
| `Promise.all` | hepsi başarılı olmalı; ilk hata hepsini reddeder (diğerleri yine çalışmaya devam eder!) |
| `Promise.allSettled` | hepsini bekle, her birinin sonucu/hatası — toplu işlemlerde kısmi başarı |
| `Promise.any` | ilk başarılı (yedekli kaynaklar) |
| `Promise.race` | ilk biten (zaman aşımı için ama AbortSignal daha iyi) |

Döngüde `await` (for…of içinde) bilinçli sıralılık içindir; `array.forEach(async …)` **beklenmez** — `for…of` veya `Promise.all(array.map(…))`.

## Eşzamanlılık sınırı

1000 isteği aynı anda atma (API limiti, bellek): `p-limit`
```ts
const limit = pLimit(5);
const results = await Promise.all(ids.map((id) => limit(() => fetchItem(id))));
```

## İptal ve zaman aşımı

```ts
const res = await fetch(url, { signal: AbortSignal.timeout(5000) });
// kullanıcı iptali + zaman aşımı birlikte
const ctrl = new AbortController();
const signal = AbortSignal.any([ctrl.signal, AbortSignal.timeout(10_000)]);
await doWork({ signal });
// kendi fonksiyonunda iptali destekle
async function doWork({ signal }: { signal: AbortSignal }) {
  for (const item of items) {
    signal.throwIfAborted();
    await process(item, { signal });
  }
}
```
React'te: effect temizliğinde `ctrl.abort()` → bileşen ayrılınca eski istek yarışmaz (TanStack Query bunu yapar).

## Yarış durumları

Arama kutusu: "a" sonra "ab" yazılır, "a"nın yanıtı geç gelir ve "ab"nin üzerine yazar. Çözümler: önceki isteği abort et, istek sırası numarası tut,
ya da Query kütüphanesine bırak. Çift tıklama: işlem sürerken butonu kilitle + sunucuda idempotency.

## Hata yönetimi

- Her promise ya `await` edilir ya `.catch` alır; "yüzen" promise (`void sendEmail()`) bilinçliyse `void` ile işaretle ve hatayı logla.
- Node: `process.on("unhandledRejection", …)` logla (varsayılan davranış süreci sonlandırmak).
- `try/catch` yalnızca `await` edilen hataları yakalar; `setTimeout` içindeki hata dışarı kaçar.
- Hata nesnesine bağlam ekle: `new Error("SMS gönderilemedi", { cause: err })`.

## Event loop

Senkron kod → **microtask**'lar (promise devamları, `queueMicrotask`) → render (tarayıcı) → **macrotask** (setTimeout, I/O, olaylar).
Uzun senkron iş (büyük JSON parse, ağır döngü) her şeyi dondurur → parçala (`await scheduler.yield()` / `setTimeout(0)`) veya Worker'a taşı (bkz. `sky-perf` INP).

## Async iterator ve stream

```ts
for await (const chunk of response.body!) { … }                      // Web stream
for await (const line of readline.createInterface({ input: fs.createReadStream("big.csv") })) { … }  // Node satır satır
async function* paginate(url: string) { let next: string | null = url; while (next) { const r = await (await fetch(next)).json(); yield* r.items; next = r.next; } }
```
Büyük dosyalarda stream → sabit bellek. Node'da `stream.pipeline` (hata ve geri basınç yönetimi). Web Streams: `TransformStream`, `pipeThrough`.

## Worker'lar

Tarayıcı: Web Worker (+ comlink, bkz. `sky-browser-apis`); Node: `worker_threads` CPU yoğun işler için (görsel işleme, şifreleme, büyük hesap) — I/O için gerekmez.

## Debounce / throttle

Debounce: son tetiklemeden X ms sonra bir kez (arama girdisi, otomatik kayıt). Throttle: X ms'de en fazla bir kez (kaydırma, yeniden boyutlandırma).
React'te değer debounce'u: `useDeferredValue` veya küçük bir `useDebounce` hook'u.

## Yeniden deneme

Üstel geri çekilme + jitter, yalnızca idempotent işlemler, iptal sinyalini dinle (bkz. `sky-resilience`).
