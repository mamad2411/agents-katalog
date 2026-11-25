---
name: sky-payments
description: >-
  Ödeme entegrasyonu: iyzico ve PayTR (3D Secure, taksit), Stripe, webhook güvenliği, abonelik, iade,
  e-fatura ve KDV. Ödeme, abonelik veya fiyatlandırma işinde kullan.
---

# Sky · Ödemeler

## Değişmez kurallar

1. **Kart verisi sana hiç gelmez.** Sağlayıcının hosted/embedded formu veya tokenizasyonu; kendi
   `<input name="cardNumber">` yok. Böylece PCI kapsamın SAQ-A seviyesinde kalır.
2. **Gerçeğin kaynağı webhook'tur**, başarı sayfasına yönlenme değil. Kullanıcı sekmeyi kapatabilir.
3. **Erişim hakkı DB'den türetilir.** İstemciden gelen "ödedim" bilgisine güvenilmez; `subscriptions.status`
   sunucuda okunur.
4. **Para tam sayı (kuruş) ve `numeric`**, asla float. Para birimi her kayıtta açık.
5. **Her yazma idempotent.** Aynı webhook iki kez gelir, aynı buton iki kez tıklanır.

## Sağlayıcı seçimi

| | Stripe | iyzico |
|---|---|---|
| Türkiye'de yerleşik şirket | Stripe TR hesabı sınırlı/yok → genelde **kullanılamaz** | ✓ yerel, TL, taksit, BKM |
| Yurt dışı şirket, global müşteri | ✓ abonelik, portal, vergi, çok para birimi | ✗ |
| Abonelik yönetimi | Yerleşik (Billing) | Abonelik ürünü var ama daha dar; çoğu ekip kendi döngüsünü yazar |
| Diğer TR seçenekleri | — | PayTR, Param, Craftgate (çoklu sağlayıcı yönlendirici) |

Türkiye'deki tüzel kişi + TL tahsilat → iyzico (veya PayTR/Craftgate). Yabancı şirket → Stripe.

## Veri modeli (sağlayıcıdan bağımsız)

```
customers        id, user_id, provider, provider_customer_id, created_at
products/prices  id, provider_price_id, amount_minor, currency, interval (month|year|null)
subscriptions    id, customer_id, provider_subscription_id, price_id,
                 status (trialing|active|past_due|canceled|unpaid|incomplete),
                 current_period_end, cancel_at_period_end, created_at, updated_at
payments         id, customer_id, provider_payment_id, amount_minor, currency,
                 status (pending|succeeded|failed|refunded|partially_refunded), metadata jsonb, created_at
webhook_events   id, provider, event_id UNIQUE, type, payload jsonb, processed_at, error
```
Entitlement: `subscriptions.status in ('trialing','active') and current_period_end > now()`
(+ `past_due` için kısa tolerans). Bunu tek bir `getEntitlements(userId)` fonksiyonunda topla.

## Stripe

**Checkout Session (tek seferlik veya abonelik)**
```ts
const session = await stripe.checkout.sessions.create({
  mode: "subscription",
  customer: customerId,                       // önce stripe.customers.create ile eşle, user_id metadata'ya
  line_items: [{ price: priceId, quantity: 1 }],
  success_url: `${APP_URL}/billing?session_id={CHECKOUT_SESSION_ID}`,
  cancel_url: `${APP_URL}/pricing`,
  allow_promotion_codes: true,
  client_reference_id: user.id,
  metadata: { userId: user.id },
}, { idempotencyKey: `checkout:${user.id}:${priceId}:${nonce}` });
```
**Webhook (`/api/webhooks/stripe`)**
```ts
export async function POST(req: Request) {
  const sig = req.headers.get("stripe-signature")!;
  const raw = await req.text();                            // HAM gövde; JSON parse ETMEDEN önce
  let event: Stripe.Event;
  try { event = stripe.webhooks.constructEvent(raw, sig, env.STRIPE_WEBHOOK_SECRET); }
  catch { return new Response("bad signature", { status: 400 }); }

  const inserted = await db.insert(webhookEvents).values({ provider: "stripe", eventId: event.id, type: event.type, payload: event })
    .onConflictDoNothing().returning();
  if (!inserted.length) return new Response("dup", { status: 200 }); // idempotent

  switch (event.type) {
    case "checkout.session.completed":
    case "customer.subscription.created":
    case "customer.subscription.updated":
    case "customer.subscription.deleted":
      await syncSubscriptionFromStripe(event.data.object.customer as string); break;
    case "invoice.paid":
    case "invoice.payment_failed":
      await recordInvoice(event.data.object); break;
  }
  await db.update(webhookEvents).set({ processedAt: new Date() }).where(eq(webhookEvents.eventId, event.id));
  return new Response("ok");
}
```
- `syncSubscriptionFromStripe`: olaydaki veriye değil, **Stripe'tan güncel aboneliği çekip** DB'ye yaz
  (sıra dışı gelen olaylara dayanıklı).
- 2xx'i hızlı dön; ağır iş kuyruğa. Stripe 3 gün boyunca yeniden dener.
- Next.js'te route handler `runtime = "nodejs"`; App Router'da `req.text()` yeter, body parser ayarı gerekmez.
- **Customer Portal** ile plan değiştirme/iptal/kart güncellemeyi Stripe'a bırak; kendi UI'ını yazma.
- Vergi: Stripe Tax açılabilir; fatura ülke/VKN alanları `tax_id_collection`.
- Test: `stripe listen --forward-to localhost:3000/api/webhooks/stripe`; test kartları `4242…`, 3DS için `4000 0025 0000 3155`; `stripe trigger invoice.payment_failed`.

## iyzico

**Checkout Form akışı**
1. Sunucuda `checkoutFormInitialize` → `conversationId` (sipariş ID'n), `price`/`paidPrice`,
   `basketItems`, alıcı/adres bilgileri, `callbackUrl`, `enabledInstallments`.
2. Dönen `checkoutFormContent` (script) sayfada render edilir; kart iyzico iframe'inde girilir; 3DS iyzico'da.
3. iyzico `callbackUrl`'e **POST** eder (`token`). Burada `checkoutForm.retrieve({ token })` ile sonucu
   **sunucuda doğrula**; `paymentStatus === "SUCCESS"` ve `paidPrice` beklenenle eşleşiyorsa siparişi onayla.
4. Callback aynı token ile birden fazla gelebilir → `payments.provider_payment_id` UNIQUE ile idempotent.
5. Callback'te kullanıcı oturumu olmayabilir (POST, farklı site); `conversationId` ile siparişi bul,
   sonra kullanıcıyı başarı sayfasına yönlendir.

- Para `"1234.50"` **string** formatında; `price` (sepet toplamı) ve `paidPrice` (taksit/komisyon dahil) ayrı.
- `basketItems` toplamı `price`e eşit olmalı; yoksa hata.
- Taksit: `installment` seçeneği BIN'e göre; `installmentInfo` servisiyle kartın taksit tablosunu göster.
- Sandbox: `sandbox-api.iyzipay.com`, test kartları dokümanda. Prod anahtarlarını env'de ayrı tut.
- Abonelik için iyzico Subscription API var; esnek fiyatlama/deneme süresi gerekiyorsa kendi döngünü
  (kayıtlı kart + periyodik tahsilat, `cardUserKey/cardToken`) planla ve başarısız tahsilat akışını tasarla.
- Webhook: iyzico'nun bildirim URL'si varsa imzasını/IP'sini doğrula; yoksa callback + periyodik `retrieve` ile uzlaştır.

## Başarısız ödeme ve dunning

- `past_due`: 3–7 gün tolerans, erişimi hemen kesme; e-posta + uygulama içi uyarı "kartını güncelle".
- Stripe Smart Retries açık; iyzico'da kendi yeniden deneme takvimi (1., 3., 7. gün).
- Son denemede `canceled` → erişimi kapat, veriyi sakla (geri dönüş kolay olsun).
- Uygulamada "Faturalandırma" sayfası: plan, dönem sonu, son faturalar, kart güncelle, iptal.

## İade ve iptal

- İade sunucudan sağlayıcı API'siyle; `payments.status` güncellenir; kısmi iade desteklenir.
- İptal: dönem sonunda (`cancel_at_period_end`) varsayılan; anında iptal + orantılı iade istisna.
- Mesafeli satış: dijital hizmette cayma hakkı istisnası sözleşmede açık yazılmalı (hukuki metin işi; sen hatırlat).

## Fatura (Türkiye)

- e-Arşiv/e-Fatura ödeme sağlayıcısının işi değil; entegratör (Paraşüt, BizimHesap, Logo İşbaşı, Uyumsoft API) gerekir.
- Faturada: ad/unvan, VKN/TCKN, adres, KDV oranı (%20 genel), kalemler. Bu alanları ödeme öncesi topla.
- Fiyatları **KDV dahil** göster (tüketiciye), B2B'de "+KDV" belirt.

## Güvenlik kontrol listesi

- [ ] Webhook imzası ham gövde üzerinden doğrulanıyor; `event_id` UNIQUE
- [ ] Fiyat/miktar **sunucuda** belirleniyor; istemciden gelen tutar kullanılmıyor
- [ ] Başarı sayfası yalnızca gösterim; sipariş durumu DB'den
- [ ] Gizli anahtarlar sunucuda; publishable key dışında istemciye hiçbir şey yok
- [ ] Çift tıklama/çift istek idempotency key ile engelli
- [ ] Ödeme logları kart/kişisel veri içermiyor
- [ ] Test ve prod anahtarları karışmıyor (env doğrulamada `sk_test_`/`sk_live_` ön ek kontrolü)
- [ ] Erişim kontrolü `getEntitlements` üzerinden, tek yerde
