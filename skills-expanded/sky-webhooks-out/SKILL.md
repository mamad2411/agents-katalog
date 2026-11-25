---
name: sky-webhooks-out
description: >-
  Giden webhook sistemi kurma (kendi kullanıcılarına/ortaklarına olay gönderme): olay
  kataloğu ve yük şeması, abonelik yönetimi UI'ı, HMAC imzalama (Standard Webhooks), teslimat
  kuyruğu, yeniden deneme ve otomatik devre dışı bırakma, teslimat günlüğü ve "tekrar gönder",
  test olayı gönderme, idempotency anahtarı, sürümleme ve Svix gibi hazır servisler. "Webhook
  gönderelim", "Zapier/Make entegrasyonu", "ortaklarımıza olay bildirelim" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Giden Webhook'lar

## Hazır mı, kendin mi?

- **Svix** / **Hookdeck Outpost**: imza, retry, portal UI, günlük hazır — çoğu ekip için en iyisi.
- Kendin: aşağıdaki parçalar; orta ölçekte 2–3 günlük iş.

## Olay kataloğu

```
booking.created   booking.updated   booking.cancelled
client.created    payment.succeeded payment.refunded
```
- Ad: `nesne.geçmiş_zaman`. Her olayın dokümante edilmiş, sürümlü JSON şeması.
- Yük:
```json
{ "id": "evt_01J…", "type": "booking.created", "created_at": "2026-11-04T09:12:00Z", "api_version": "2026-11-01",
  "data": { "id": "bkg_…", "starts_at": "…", "client": { "id": "cli_…", "name": "…" } } }
```
- Kişisel veriyi minimumda tut; gerekiyorsa yalnızca ID gönder, alıcı API'den çeksin ("ince olay").

## İmzalama (Standard Webhooks)

Başlıklar: `webhook-id`, `webhook-timestamp`, `webhook-signature: v1,<base64(hmac_sha256(secret, id.timestamp.body))>`.
- Abonelik başına ayrı gizli anahtar (`whsec_…`), panelden döndürülebilir (eski + yeni bir süre ikisi de geçerli).
- Alıcıya doğrulama örnek kodu ver (Node, PHP, Python) — en çok sorulan şey bu.
- Zaman damgası toleransı 5 dk (replay koruması).

## Teslimat

- Olay oluşunca abonelere teslimat işleri kuyruğa (bkz. `sky-jobs`); asıl isteği bekletme.
- Zaman aşımı 10 sn; 2xx = başarı; diğer her şey = yeniden dene.
- Geri çekilme: 1dk, 5dk, 30dk, 2s, 6s, 12s, 24s (~2 gün).
- Sürekli başarısız uç nokta → 5 gün sonra **otomatik devre dışı** + sahibine e-posta.
- Sıra garantisi verme; alıcı `created_at` ve `id` ile sıralasın/tekilleştirsin.
- SSRF koruması: kullanıcı URL'si iç ağa (10.x, 169.254.x, localhost) çözümlenemez; yalnızca https.

## Kullanıcı arayüzü (insanların sevdiği kısım)

- **Uç nokta ekle**: URL, olay seçimi (onay kutuları), açıklama → gizli anahtarı **bir kez** göster + kopyala.
- **"Test olayı gönder"** butonu → örnek yük gönderir, yanıtı anında gösterir.
- **Teslimat günlüğü**: her deneme — durum kodu, süre, istek/yanıt gövdesi (kısaltılmış), "Tekrar gönder".
- Sağlık rozeti: "Son 24 saatte %98 başarılı".
- Örnek yükler olay kataloğunda kopyalanabilir.

## Veri modeli

```
webhook_endpoints   id, org_id, url, secret_enc, events text[], enabled, disabled_reason, created_at
webhook_deliveries  id, endpoint_id, event_id, attempt, status_code, duration_ms, response_snippet, next_retry_at, created_at
events              id, org_id, type, payload jsonb, created_at
```
Gizli anahtar şifreli saklanır; teslimat günlüğü 30 gün tutulur.

## Sürümleme

- `api_version` olayda; kırıcı değişiklikte yeni sürüm, abonelik kendi sürümünü seçer.
- Alan eklemek kırıcı değil; kaldırmak/ad değiştirmek kırıcı.
