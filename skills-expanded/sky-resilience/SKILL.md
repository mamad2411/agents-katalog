---
name: sky-resilience
description: >-
  Dayanıklılık kalıpları: zaman aşımı (timeout) her dış çağrıda, akıllı yeniden deneme
  (üstel geri çekilme + jitter, idempotency), devre kesici (circuit breaker), bulkhead
  (izolasyon), fallback ve zarif bozulma (graceful degradation), kuyrukla tamponlama, sağlık
  kontrolleri, kaos denemeleri ve "üçüncü parti çökerse ne olur" haritası. "SMS servisi
  çökünce her şey duruyor", "dış API yavaş", "sistem kırılgan" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Dayanıklılık

Soru her zaman: **"Bu bağımlılık çökerse/yavaşlarsa kullanıcı ne görür?"** Cevap "beyaz sayfa" olmamalı.

## Bağımlılık haritası

| Bağımlılık | Çökerse | Davranış |
|---|---|---|
| Veritabanı | kritik | bakım sayfası, salt okunur önbellek |
| Ödeme sağlayıcı | kritik akış | "Ödeme şu an alınamıyor, sepetin saklandı" + durum |
| SMS / e-posta | kritik değil | kuyrukta bekler, sonra gönderilir |
| AI servisi | kritik değil | özellik gizlenir/elle akış |
| Harita / analitik / chat widget | kozmetik | sessizce yok, sayfa çalışır |
Bu tabloyu proje dokümanına koy; yeni entegrasyonda doldur.

## Zaman aşımı: her dış çağrıda

```ts
const res = await fetch(url, { signal: AbortSignal.timeout(5000) });
```
Varsayılan "sonsuz bekle" bir yavaş servisin tüm sunucu kaynaklarını tüketmesine yol açar. Kullanıcı
isteği yolundaki çağrılar ≤ 3–5 sn; arka plan işleri daha uzun ama yine sınırlı. DB'de `statement_timeout`.

## Yeniden deneme

```ts
async function retry<T>(fn: () => Promise<T>, { tries = 3, base = 300 } = {}): Promise<T> {
  for (let i = 0; ; i++) {
    try { return await fn(); }
    catch (e) {
      if (i >= tries - 1 || !isRetryable(e)) throw e;          // 4xx (429 hariç) yeniden denenmez
      await sleep(base * 2 ** i + Math.random() * base);        // üstel + jitter
    }
  }
}
```
- Yalnızca **idempotent** işlemleri (veya idempotency anahtarıyla) yeniden dene — yoksa çift ödeme/çift SMS.
- `429` → `Retry-After` başlığına uy.
- İstek yolunda en fazla 1–2 deneme; gerisini kuyruğa bırak.
- Katmanlar arasında iç içe retry'dan kaçın (3 × 3 × 3 = 27 istek).

## Devre kesici

Ardışık hatalar eşiği aşınca (ör. 30 sn'de %50) devre **açılır**: çağrı yapmadan hemen fallback dön; 30 sn sonra
**yarı açık**: bir deneme isteği, başarılıysa kapan. Kütüphane: `opossum`; ya da Redis'te basit sayaç.
Yavaş servisi dövmeyi bırakır, kullanıcı beklemeden fallback görür.

## Bulkhead

Bir bağımlılığın eşzamanlı çağrı sayısını sınırla (`p-limit`), ayrı kuyruk/işçi havuzu ver → yavaş PDF servisi
randevu API'sini aç bırakmaz. Kiracı bazlı eşzamanlılık (bkz. `sky-jobs`).

## Zarif bozulma örnekleri

- Öneriler servisi çöktü → "Popüler hizmetler" statik listesi.
- Arama motoru çöktü → Postgres ILIKE ile basit arama.
- Görsel CDN yavaş → bulanık yer tutucu kalır, sayfa kullanılabilir.
- Döviz kuru API'si yok → son bilinen kur + "güncelleme gecikti" notu.
- Bileşen seviyesinde hata sınırları (bkz. `sky-rsc-streaming`): bir widget düşer, sayfa yaşar.

## Kuyrukla tamponlama

Kullanıcı eylemi ile yan etkiyi ayır: sipariş kaydedilir (DB), e-posta/SMS/fatura/webhook kuyruğa. Sağlayıcı
saatlerce çöksse de sipariş akışı etkilenmez; servis dönünce kuyruk erir.

## Sağlık ve bakım modu

- `/api/health` bağımlılıkları ayrı raporlar (bkz. `sky-observability`); yük dengeleyici yalnızca kritik olanlara bakar.
- Bakım modu bayrağı (bkz. `sky-feature-flags`): planlı DB bakımında güzel bir sayfa + tahmini süre.
- Salt okunur mod: yazma kapalı, okuma açık — göçler sırasında hayat kurtarır.

## Kaos denemesi (küçük ölçekte)

Staging'de bir bağımlılığı bilerek kapat (env ile sahte adaptörü "her zaman hata" moduna al) ve kullanıcı yolunu
dene. Ayda bir 30 dakika — üretimde sürprizleri bitirir.

## Kontrol listesi

- [ ] Her dış çağrıda timeout
- [ ] Retry yalnızca idempotent işlemlerde, jitter'lı, sınırlı
- [ ] Kritik olmayan yan etkiler kuyrukta
- [ ] Her bağımlılığın fallback davranışı tanımlı
- [ ] Bakım ve salt okunur mod var
