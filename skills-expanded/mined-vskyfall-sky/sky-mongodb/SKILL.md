---
name: sky-mongodb
description: >-
  MongoDB ile çalışma: ne zaman doğru seçim (ve ne zaman Postgres daha iyi), doküman modelleme
  (gömme vs referans, erişim kalıbına göre tasarım), şema doğrulama (JSON Schema, Mongoose/Zod),
  indeksler (bileşik, ESR kuralı, TTL, kısmi, metin), aggregation pipeline, transaction'lar,
  sayfalama, Atlas Search ve Vector Search, performans (explain), güvenlik ve Mongoose/resmi
  sürücü kalıpları. MongoDB kullanan projede kullan.
disable-model-invocation: true
---

# Sky · MongoDB

## Doğru seçim mi?

✓ Esnek/değişken şemalı içerik, doküman bazlı erişim (bir sayfa = bir doküman), yüksek yazma, coğrafi/zaman serisi, ekibin uzmanlığı.
✗ Yoğun ilişkisel veri ve çok tablolu join'ler, katı tutarlılık gerektiren finansal defter — Postgres (jsonb ile esnekliği de var) genelde daha iyi.

## Modelleme: erişim kalıbından başla

"Hangi sorgular, hangi sıklıkta?" → dokümanı ona göre şekillendir.
- **Göm** (embed): birlikte okunan, sınırlı sayıda, sahibinden bağımsız yaşamayan veri (siparişin kalemleri, kullanıcının adresleri).
- **Referans**: sınırsız büyüyen (yorumlar, loglar), bağımsız güncellenen, çoklu sahipli veri.
- Sınırsız büyüyen dizi (sonsuz `comments[]`) yok — doküman sınırı 16MB ve performans düşer.
- Kasıtlı **tekrar** (denormalizasyon): randevu dokümanında müşteri adının kopyası — okuma hızlı, güncellemede senkron gerekir.

```js
// bookings
{ _id: ObjectId, orgId: ObjectId, startsAt: ISODate, status: "confirmed",
  client: { _id: ObjectId, name: "Ayşe Yılmaz", phone: "+90532…" },   // okuma için gömülü özet
  service: { _id: ObjectId, name: "Saç kesimi", durationMin: 45, priceMinor: 45000 },
  createdAt: ISODate }
```

## Şema doğrulama

Uygulamada Zod/Mongoose şeması + koleksiyonda `$jsonSchema` validator (son savunma hattı). "Şemasız" = şemanın dağınık olması değil.

## İndeksler

- **ESR kuralı** bileşik indekste: önce **E**şitlik alanları, sonra **S**ıralama, sonra **R**ange (aralık).
  `{ orgId: 1, startsAt: 1 }` → `find({ orgId, startsAt: { $gte } }).sort({ startsAt: 1 })`.
- TTL indeksi (geçici veriler, oturumlar, doğrulama kodları otomatik silinir): `{ expiresAt: 1 }, { expireAfterSeconds: 0 }`.
- Kısmi indeks (`partialFilterExpression: { status: "active" }`), benzersiz indeks (iş kuralı), metin indeksi (basit arama).
- `explain("executionStats")`: `COLLSCAN` büyük koleksiyonda alarm; `totalDocsExamined` / `nReturned` oranı ~1 hedef.

## Aggregation

```js
db.bookings.aggregate([
  { $match: { orgId, startsAt: { $gte: monthStart, $lt: monthEnd }, status: "completed" } },
  { $group: { _id: { $dateToString: { format: "%Y-%m-%d", date: "$startsAt", timezone: "Europe/Istanbul" } },
              revenue: { $sum: "$service.priceMinor" }, count: { $sum: 1 } } },
  { $sort: { _id: 1 } },
]);
```
`$match`'i olabildiğince başa koy (indeks kullanır); `$lookup` join'dir — sık gerekiyorsa modeli yeniden düşün.

## Tutarlılık

Tek doküman güncellemeleri atomiktir (`$inc`, `$set`, `findOneAndUpdate`) — çoğu ihtiyaç buna sığacak şekilde modelle.
Çoklu doküman gerekiyorsa replica set'te transaction (`session.withTransaction`), kısa tut.

## Sayfalama ve sorgu

Cursor: `find({ orgId, _id: { $gt: lastId } }).sort({ _id: 1 }).limit(20)` — `skip` büyük değerlerde yavaş. Projeksiyon ile yalnızca gereken alanlar.

## Atlas özellikleri

**Atlas Search** (Lucene tabanlı tam metin, Türkçe analizör, otomatik tamamlama, bulanık eşleme) ve **Vector Search** (RAG, bkz. `sky-ai`) — ayrı arama motoruna gerek kalmadan.

## Sürücü / ODM

- Resmi Node sürücüsü + Zod (hafif, tip güvenli) veya **Mongoose** (şema, middleware, populate). Bağlantı tek örnek (sunucusuzda modül seviyesinde önbellek).
- Mongoose'da `lean()` okuma sorgularında (çok daha hızlı), `strictQuery`.

## Güvenlik

Kimlik doğrulama açık, ağ erişimi IP/VPC ile sınırlı, en az yetkili kullanıcı; **NoSQL enjeksiyonu**: kullanıcı girdisini doğrudan sorgu nesnesine koyma
(`{ email: req.body.email }` içine `{ "$ne": null }` gelebilir) → şema doğrulama ile yalnızca string kabul et.
