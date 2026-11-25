---
name: sky-architecture-patterns
description: >-
  Uygulama mimarisi kalıpları: katmanlı mimari (handler → servis → repository), modüler monolit,
  hexagonal / ports & adapters, clean architecture'ın pragmatik hali, DDD'den işe yarayanlar
  (bounded context, aggregate, value object, ubiquitous language), CQRS ne zaman, bağımlılık
  enjeksiyonu, sık kullanılan tasarım kalıpları (strategy, adapter, factory, observer, state,
  builder, decorator) TypeScript örnekleriyle, SOLID'in aşırıya kaçmayan yorumu ve
  anti-kalıplar. "Mimari nasıl olmalı", "kod nasıl organize edilir", "design pattern" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Mimari Kalıplar

Kural: **en basit yeterli yapı.** Mimari karmaşıklık ekip büyüklüğü ve alanın karmaşıklığıyla orantılı olmalı.

## Seviye seçimi

| Proje | Yapı |
|---|---|
| Küçük site / prototip | route/handler içinde doğrudan ORM — sorun değil |
| Tipik SaaS | **katmanlı**: handler (HTTP) → servis (kurallar, yetki) → repository/ORM |
| Büyüyen ürün, birden çok ekip | **modüler monolit**: alan modülleri, açık arayüzler, modüller arası doğrudan tablo erişimi yok |
| Karmaşık iş kuralları, çok entegrasyon | **hexagonal** (ports & adapters) + DDD öğeleri |
| Bağımsız ölçek/ekip gereksinimi | mikroservisler (bkz. `sky-microservices`) |

## Katmanlı (varsayılan)

```
handler    HTTP/route: girdi parse, kimlik, yanıt biçimi — iş kuralı YOK
service    iş kuralları, yetki, transaction, olay/bildirim tetikleme — HTTP bilmez
repository veri erişimi: sorgular — kural YOK
```
Servis test edilebilir (HTTP olmadan), handler ince, kurallar tek yerde.

## Hexagonal: ports & adapters

```ts
// domain/ports.ts — çekirdeğin ihtiyaç duyduğu arayüzler
export interface PaymentGateway { charge(input: ChargeInput): Promise<ChargeResult>; }
export interface SmsSender { send(to: string, body: string): Promise<void>; }
// adapters/iyzico.ts — dış dünyaya özgü uygulama
export class IyzicoGateway implements PaymentGateway { … }
// test: class FakePayments implements PaymentGateway { … }
```
Çekirdek (alan mantığı) framework'ü, DB'yi, sağlayıcıyı bilmez → sağlayıcı değiştirmek ve test kolay (bkz. `sky-tr-integrations` adaptör kuralı).

## DDD'den işe yarayanlar

- **Ortak dil**: koddaki isimler alan uzmanının kelimeleri (`Appointment` mı `Booking` mı — birini seç, her yerde aynı).
- **Value object**: kimliği olmayan, değerle karşılaştırılan, kendini doğrulayan tipler — `Money`, `PhoneNumber`, `TimeRange`.
- **Aggregate**: birlikte tutarlı kalması gereken nesne kümesi ve kökü (Sipariş + kalemleri); dışarıdan yalnızca kök üzerinden değişiklik.
- **Bounded context**: "Müşteri" faturalamada ve randevuda farklı anlamlar taşıyabilir — modül sınırı.
Ağır DDD törenleri (her şeye factory/repository/specification) çoğu web uygulamasında gereksiz.

## CQRS ne zaman?

Okuma ve yazma modelleri çok farklılaşınca (karmaşık raporlar, farklı ölçek): yazmalar servis/aggregate üzerinden, okumalar optimize edilmiş
sorgular/görünümler (materialized view, ayrı okuma modeli). Küçük ölçekte: okuma sorgularını ayrı `queries/` dosyasında tutmak bile yeter.

## Bağımlılık enjeksiyonu

Konstrüktör veya fonksiyon parametresiyle bağımlılık ver; global singleton'lara gizli bağımlılık yok. TS'de çoğu zaman framework'süz yeter:
```ts
export const createBookingService = (deps: { repo: BookingRepo; sms: SmsSender; clock: () => Date }) => ({
  async create(user: User, input: CreateBooking) { … deps.sms.send(…) … },
});
```
Testte sahte bağımlılıklar, üretimde gerçekleri — bileşim kökünde (composition root) bir kez bağla.

## Sık kalıplar (ne zaman kullanılır)

| Kalıp | Kullanım | Örnek |
|---|---|---|
| Strategy | değiştirilebilir algoritma | kargo ücreti hesaplayıcıları, fiyatlandırma kuralları |
| Adapter | dış API'yi kendi arayüzüne uydurma | SMS sağlayıcıları, ödeme |
| Factory | oluşturma mantığı karmaşık/koşullu | bildirim kanalı seçimi |
| Observer / olay | gevşek bağlı yan etkiler | "randevu oluştu" → e-posta, analitik |
| State machine | durum geçişleri kuralı | sipariş/randevu durumları (bkz. `sky-state`) |
| Builder | çok opsiyonlu nesne | sorgu/rapor oluşturucu |
| Decorator / middleware | çapraz kesen işler | log, cache, retry sarmalayıcıları |
| Result tipi | beklenen hatalar | servis dönüşleri (bkz. `sky-typescript`) |

## SOLID (pragmatik)

Tek sorumluluk = **tek değişme sebebi** (tek fonksiyon değil); açık/kapalı = yeni sağlayıcı eklemek mevcut kodu değiştirmeden (strategy/adapter);
bağımlılıkların tersine çevrilmesi = çekirdek arayüze bağlı. Arayüzü tek uygulaması varken "ileride lazım olur" diye ekleme (YAGNI).

## Anti-kalıplar

Her şeyi bilen "God" servis; anemik model + 15 katman yönlendirme; `utils/` çöplüğü; döngüsel bağımlılık; paylaşılan değiştirilebilir global durum;
erken mikroservis; "esneklik" için yapılandırma cehennemi; iş kuralının UI'da, API'de ve DB tetikleyicisinde üç farklı kopyası.
