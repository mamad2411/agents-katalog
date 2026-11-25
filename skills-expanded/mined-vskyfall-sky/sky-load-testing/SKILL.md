---
name: sky-load-testing
description: >-
  Yük ve performans testi: hedef belirleme (RPS, eşzamanlı kullanıcı, p95 gecikme, hata oranı),
  k6 ile senaryo yazma (aşamalar, eşikler, kontroller, gerçekçi kullanıcı akışı), Artillery ve
  autocannon, test verisi ve kimlik doğrulama, yük türleri (smoke, load, stress, spike, soak),
  sonuçları okuma ve darboğaz bulma (DB, bağlantı havuzu, CPU, harici API), CI'da performans
  regresyonu ve üretimi yanlışlıkla yıkmamak. "Kaç kullanıcı kaldırır", "yük testi",
  "lansmanda çöker mi" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Yük Testi

## 1. Hedefi sayıyla yaz

"Lansman günü saatte 20.000 ziyaretçi, en yoğun dakikada ~150 istek/sn, %5'i randevu oluşturur.
Hedef: p95 < 500ms, hata < %1." Sayısız yük testi yorumsuz grafik üretir.

## 2. Test türleri

| Tür | Amaç | Profil |
|---|---|---|
| **Smoke** | senaryo çalışıyor mu | 1–2 VU, 1 dk |
| **Load** | beklenen yükte hedefler tutuyor mu | hedef VU, 10–30 dk |
| **Stress** | kırılma noktası nerede | kademeli artır, çökene kadar |
| **Spike** | ani dalgalanma (lansman, kampanya) | saniyeler içinde 10× |
| **Soak** | saatler boyunca sızıntı/bozulma | orta yük, 2–8 saat |

## 3. k6 senaryosu

```js
import http from "k6/http";
import { check, sleep, group } from "k6";

export const options = {
  stages: [
    { duration: "2m", target: 50 },
    { duration: "5m", target: 50 },
    { duration: "2m", target: 200 },   // zirve
    { duration: "3m", target: 200 },
    { duration: "2m", target: 0 },
  ],
  thresholds: {
    http_req_failed: ["rate<0.01"],
    http_req_duration: ["p(95)<500"],
    "http_req_duration{name:create_booking}": ["p(95)<800"],
  },
};

const BASE = __ENV.BASE_URL;
export function setup() {
  const res = http.post(`${BASE}/api/test/login`, JSON.stringify({ email: "load@test.local" }), { headers: { "Content-Type": "application/json" } });
  return { token: res.json("token") };
}
export default function ({ token }) {
  const headers = { Authorization: `Bearer ${token}`, "Content-Type": "application/json" };
  group("rezervasyon akışı", () => {
    const slots = http.get(`${BASE}/api/slots?date=2026-12-01`, { headers, tags: { name: "slots" } });
    check(slots, { "slots 200": (r) => r.status === 200 });
    sleep(Math.random() * 3 + 1);                       // düşünme süresi: gerçekçi kullanıcı
    if (Math.random() < 0.05) {
      const r = http.post(`${BASE}/api/bookings`, JSON.stringify({ slotId: slots.json("0.id") }), { headers, tags: { name: "create_booking" } });
      check(r, { "booking 201/409": (x) => x.status === 201 || x.status === 409 });
    }
  });
}
```
`k6 run -e BASE_URL=https://staging.site.com load.js`. Dinamik URL'leri `tags: { name }` ile grupla (yoksa her ID ayrı metrik).

## 4. Kurallar

- **Üretimde değil**, üretime benzer staging'de (aynı boyut DB, aynı bölge, gerçekçi veri hacmi). Üretimde test gerekiyorsa küçük, duyurulu, düşük trafik saatinde.
- Üçüncü parti servisleri (ödeme, SMS, e-posta) **sahte** moda al — yoksa fatura ve kara liste.
- Yük üreticisi darboğaz olmasın (CPU'su %80 altında); büyük testlerde k6 Cloud / dağıtık çalıştırma.
- Önbellek ısınması: ilk dakikaları ayrı değerlendir.
- Rate limit'ler test kullanıcıları için gevşetilmeli veya testin bir parçası olarak ölçülmeli.

## 5. Sonuçları okuma

- p50 iyi ama p95/p99 kötü → kuyruklanma, kilit beklemesi, GC duraklamaları, soğuk başlatma.
- Hata oranı belli bir VU'dan sonra sıçrıyor → bağlantı havuzu dolması (DB, HTTP istemcisi), dosya tanımlayıcı sınırı, bellek.
- Gecikme yükle doğrusal artıyor → CPU sınırı veya tek darboğaz kaynak.
Eşzamanlı olarak izle: uygulama CPU/bellek, DB CPU + aktif bağlantılar + yavaş sorgu logu, kuyruk derinliği, harici çağrı süreleri (bkz. `sky-observability`).
Tipik darboğazlar ve çözümler: N+1 ve eksik indeks (`sky-sql`), bağlantı havuzu (pgBouncer/Hyperdrive), önbellek (`sky-caching`), ağır işi kuyruğa alma (`sky-jobs`).

## 6. Diğer araçlar

- **autocannon** / **oha**: tek uç noktaya hızlı yük (`npx autocannon -c 100 -d 30 http://localhost:3000/api/x`).
- **Artillery**: YAML senaryolar, Playwright ile tarayıcı bazlı yük.
- **Lighthouse CI** ön yüz performansı için (bkz. `sky-perf`) — yük testi değil.

## 7. CI'da regresyon

PR'da kısa smoke + temel eşikler (p95 belirli uç noktalarda), gece staging'de load testi; sonuçları önceki çalıştırmayla karşılaştır, eşik aşılırsa uyarı.
