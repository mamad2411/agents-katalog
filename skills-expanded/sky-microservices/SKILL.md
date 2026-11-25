---
name: sky-microservices
description: >-
  Dağıtık sistem ve mikroservis kararları: modüler monolit önce, servis sınırlarını alanlara göre
  çizme, senkron (HTTP/gRPC) ve asenkron (olay/kuyruk) iletişim, olay odaklı mimari, outbox
  kalıbı ile güvenilir olay yayınlama, idempotent tüketiciler, saga ile dağıtık işlemler, servis
  keşfi ve API gateway, sözleşme testleri, dağıtık izleme (OpenTelemetry), veri sahipliği ve
  tutarlılık modelleri. "Mikroservise geçelim mi", "servisler arası iletişim", "event-driven"
  dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Mikroservisler & Dağıtık Sistemler

## Önce: modüler monolit

Çoğu ekip için doğru başlangıç: **tek deploy edilen uygulama, içeride sıkı sınırlı modüller** (her modülün kendi tabloları, açık
arayüzü; diğer modülün tablosuna doğrudan sorgu yok). Mikroservise geçiş sebepleri: bağımsız ölçeklenme ihtiyacı, farklı ekiplerin
bağımsız deploy etmesi, farklı teknoloji gereksinimi, hata izolasyonu. "Moda" bir sebep değildir — dağıtık sistem karmaşıklığı (ağ hataları,
tutarlılık, gözlem, deploy koordinasyonu) gerçek bir maliyettir.

## Sınırlar

- Alan (bounded context) bazlı: Randevu, Faturalama, Bildirim, Kimlik — teknik katman bazlı değil ("veritabanı servisi" yok).
- **Her servis kendi verisinin sahibi**; başka servisin DB'sine erişim yok. Paylaşılan DB = dağıtık monolit (en kötüsü).
- Sohbet eden (chatty) servisler → sınır yanlış çizilmiş olabilir.

## İletişim

| Tür | Ne zaman |
|---|---|
| Senkron HTTP/REST | sorgu, kullanıcı bekliyor, basit |
| gRPC | iç servisler, yüksek hacim, sıkı sözleşme (protobuf), streaming |
| Asenkron olay (Kafka, NATS, RabbitMQ, SQS/SNS, Redis Streams) | "X oldu" bildirimleri, gevşek bağlılık, tamponlama |
| Komut kuyruğu | "şunu yap" işleri (bkz. `sky-jobs`) |
Senkron zincirler (A→B→C→D) toplam erişilebilirliği çarpar ve gecikmeyi toplar → olaylarla kır, zaman aşımı + devre kesici koy (bkz. `sky-resilience`).

## Olaylar

```json
{ "id": "evt_01J…", "type": "booking.confirmed", "version": 1, "occurredAt": "2026-11-04T09:12:00Z",
  "source": "booking-service", "data": { "bookingId": "…", "orgId": "…", "startsAt": "…" } }
```
- Olay geçmiş zamanlı gerçek ("BookingConfirmed"), komut değil.
- Şema sürümlü ve kayıtlı (schema registry / paylaşılan Zod-JSON Schema paketi); alan ekle, kaldırma.
- **En az bir kez** teslim varsay → tüketiciler **idempotent** (işlenen olay ID'leri tablosu).
- Sıra yalnızca bölüm/anahtar içinde garanti (Kafka partition key = `orgId`).

## Outbox kalıbı (en önemli tek kalıp)

Sorun: DB'ye yaz + olay yayınla iki ayrı işlem — biri başarısız olursa tutarsızlık.
```sql
BEGIN;
  INSERT INTO bookings (...) VALUES (...);
  INSERT INTO outbox (id, type, payload) VALUES ('evt_…', 'booking.confirmed', '{…}');
COMMIT;
```
Ayrı bir yayıncı (polling veya CDC — Debezium) outbox'ı okuyup broker'a gönderir, gönderildi işaretler. Olay kaybı yok.
Tüketici tarafında **inbox** (işlenen olay ID'leri) ile çift işleme yok.

## Dağıtık işlemler: saga

Örnek: randevu + ödeme + bildirim. 2PC yerine adım adım yerel işlemler + başarısızlıkta **telafi** (compensation):
ödeme başarısız → randevuyu iptal et. Orkestrasyon (merkezi koordinatör — Temporal, Inngest adımlı akışlar) çoğu zaman koreografiden
(herkes olaylara tepki verir) daha anlaşılırdır. Temporal / Restate gibi dayanıklı iş akışı motorları sagaları çok kolaylaştırır.

## Altyapı parçaları

- API gateway (kimlik doğrulama, rate limit, yönlendirme) — Kong, Envoy, bulut gateway'leri, ya da BFF (backend-for-frontend).
- Servis keşfi: Kubernetes DNS / Consul; servis ağı (Istio, Linkerd) yalnızca gerçekten gerekiyorsa (mTLS, trafik yönetimi).
- **Dağıtık izleme şart**: OpenTelemetry ile trace context (`traceparent`) tüm HTTP çağrılarında ve olay meta verisinde taşınır;
  Jaeger/Tempo/Honeycomb/Sentry'de uçtan uca istek görünümü (bkz. `sky-observability`).
- Korelasyon ID'si loglarda.

## Test

- Servis içi: normal testler. Servisler arası: **sözleşme testleri** (Pact — tüketici beklentilerini sağlayıcı CI'da doğrular) — büyük E2E ortamlarından daha güvenilir.
- Olay şemaları için uyumluluk kontrolü CI'da.
- Kaos: bağımlı servisi kapatınca ne oluyor? (bkz. `sky-resilience`)

## Tutarlılık

Servisler arası **nihai tutarlılık** (eventual consistency) normaldir; UI bunu yansıtsın ("Ödeme işleniyor…"). Güçlü tutarlılık gereken kurallar
tek servisin içinde kalsın (sınırı ona göre çiz).
