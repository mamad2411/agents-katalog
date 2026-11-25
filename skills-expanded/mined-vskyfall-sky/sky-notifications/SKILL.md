---
name: sky-notifications
description: >-
  Bildirim: işlemsel e-posta, Türkiye SMS sağlayıcıları (Netgsm, Verimor), OTP, İYS zorunluluğu, push.
  "OTP SMS", "hoş geldin e-postası", "bildirim" dendiğinde kullan.
---

# Sky · Bildirimler

## Mimari

```
olay (sipariş oluştu) → notify("order.created", { userId, orderId })
   → tercih kontrolü (kanal açık mı? sessiz saat?)
   → kuyruk (job)  →  işçi: şablon render (locale) → sağlayıcı API → delivery log
```
- **İstek yolunda gönderme.** Kullanıcıya yanıtı dön, gönderimi kuyruğa at. Kuyruk seçenekleri:
  Inngest / Trigger.dev (sunucusuz dostu), BullMQ (Redis), pg-boss / Supabase Queues (Postgres), QStash.
- Her bildirim bir **`notifications`** satırı: `id, user_id, type, channel, status (queued|sent|delivered|failed|bounced), provider_id, payload, locale, created_at, sent_at, error`.
- **Idempotency anahtarı**: `type:entityId:channel` (ör. `order.created:ord_123:email`) UNIQUE → aynı
  olay iki kez gönderilmez.
- Yeniden deneme: üstel geri çekilme (1m, 5m, 30m, 2h), en fazla 5; kalıcı hatada (geçersiz adres) deneme yok.
- Tek `notify()` giriş noktası; kanala özgü kod `channels/email.ts`, `channels/sms.ts`… içinde.

## Tercihler

```
notification_preferences  user_id, type, email bool, sms bool, push bool, in_app bool
```
- İşlemsel (parola sıfırlama, ödeme makbuzu, güvenlik) **kapatılamaz**; pazarlama/özet kapatılabilir.
- Varsayılanlar temkinli: pazarlama **kapalı** (KVKK/ETK — açık rıza gerekir).
- Sessiz saatler (22:00–08:00 kullanıcı saat dilimi) pazarlama ve özetler için; OTP/güvenlik için değil.
- Toplu/özet (digest): "günde 5 bildirim → tek e-posta" kuralı; `digest_at` ile planla.

## E-posta

**Sağlayıcı:** Resend (varsayılan, basit API), alternatif Postmark (işlemsel), SES (ucuz/ölçek), Brevo.
**Şablon:** `react-email` — bileşenle yaz, HTML'e render et; `@react-email/components` tablolu düzeni halleder.

```tsx
// emails/OrderConfirmed.tsx
export default function OrderConfirmed({ name, orderNo, total, locale }: Props) {
  return (
    <Html lang={locale}>
      <Head /><Preview>Siparişin alındı: #{orderNo}</Preview>
      <Body style={body}><Container>
        <Heading as="h1">Teşekkürler {name}</Heading>
        <Text>#{orderNo} numaralı siparişin alındı. Toplam: {total}</Text>
        <Button href={`${APP_URL}/orders/${orderNo}`}>Siparişi görüntüle</Button>
      </Container></Body>
    </Html>
  );
}
```
```ts
await resend.emails.send({
  from: "Sky <bildirim@mail.example.com>",   // alt alan (mail.) kullan; ana alanın itibarını koru
  to: user.email, replyTo: "destek@example.com",
  subject: `Siparişin alındı: #${orderNo}`,
  react: <OrderConfirmed {...props} />,
  text: renderPlainText(...),                 // düz metin alternatifi
  headers: { "List-Unsubscribe": `<${unsubUrl}>` },  // pazarlama için zorunlu
  tags: [{ name: "type", value: "order.confirmed" }],
});
```
**Teslim edilebilirlik**
- DNS: **SPF**, **DKIM** (sağlayıcı verir), **DMARC** (`p=quarantine` hedefi), gönderen alt alan adı.
- Pazarlama ve işlemsel için **ayrı alt alan** (`news.` / `mail.`) → biri kara listeye girerse diğeri sağ kalır.
- Yeni alan ısıtma: hacmi kademeli artır.
- Bounce ve complaint webhook'larını işle: hard bounce → adresi işaretle, bir daha gönderme.
- Konu satırı ≤ 50 karakter, `Preview` metni anlamlı; tek net CTA; görseller `alt`lı; dark mode'da okunur
  (saydam PNG ve koyu metin tuzağı). Türkçe karakterler UTF-8 — kütüphane halleder, ham header yazma.
- Test: `resend` test adresleri (`delivered@resend.dev`), Mailtrap/Ethereal sandbox; Litmus/Email on Acid istemci önizleme.

## SMS

**Türkiye sağlayıcıları:** Netgsm, İleti Merkezi, Verimor, Mutlucell (yerel, başlık/alfanümerik gönderici);
global: Twilio, Vonage (TR'de başlık tescili gerekir, daha pahalı).
- **İYS (İleti Yönetim Sistemi):** Türkiye'de **ticari** SMS/e-posta için alıcının İYS'de onaylı olması
  zorunlu; sağlayıcılar İYS entegrasyonu sunar. OTP/işlemsel mesajlar kapsam dışı. Pazarlama SMS'i
  göndermeden önce bunu ürün sahibine hatırlat.
- OTP: 6 hane, 5 dk, mesajda uygulama adı + kod + "kimseyle paylaşma"; şablon:
  `"{kod} Sky dogrulama kodunuz. Kimseyle paylasmayin."` — Türkçe karakterler bazı sağlayıcılarda
  mesajı 160 → 70 karakter sınırına düşürüp iki parçaya böler; OTP'de ASCII kullan, maliyet ve teslim için.
- Numara formatı E.164 (`+905xx…`); doğrulama regex `^\+905\d{9}$` (boşluksuz).
- Rate limit: numara başına saatte 3, IP başına 10; abuse için ülke kodu kısıtı.
- Teslim raporu (DLR) webhook'u ile `delivered/failed` güncelle.

## Push

- **Web Push:** VAPID anahtarları, `PushManager.subscribe`, service worker `push` olayı; abonelikler
  `push_subscriptions(user_id, endpoint UNIQUE, keys, user_agent)`; `410 Gone` → sil. Kütüphane: `web-push`.
- **Mobil:** FCM (Android/iOS), APNs; token tablosu benzer; token yenilenmesini işle.
- İzin isteme zamanı: sayfa açılır açılmaz **değil**; bağlamlı ("Siparişin kargoya verildiğinde haber verelim mi?").
- Payload küçük (başlık, gövde, URL, ikon); hassas veri yok (ekranda görünür).
- Tıklama analitiği: `notificationclick` → `clients.openWindow(url)`.

## Uygulama içi bildirimler

```
in_app_notifications  id, user_id, type, title, body, href, read_at, created_at
```
- Zil ikonu + okunmamış sayısı (`aria-label="Bildirimler, 3 okunmamış"`), liste `role="list"`, hepsini okundu işaretle.
- Gerçek zamanlı güncelleme için `sky-realtime` (SSE/Supabase Realtime); yoksa 30–60 sn polling yeter.
- Eski bildirimleri 90 gün sonra arşivle/sil.

## Şablon ve dil

- Şablonlar kullanıcının `locale`ine göre; metinler `messages/{locale}.json`dan (bkz. `sky-i18n`).
- Değişkenler güvenli kaçışlı (HTML enjeksiyonu: kullanıcı adında `<script>` olabilir — react-email kaçışlar, ham string birleştirme kaçışlamaz).
- Tarih/para kullanıcı locale ve saat dilimine göre biçimlendirilmiş gelir.
- Her şablonun **önizleme** sayfası (react-email dev server) ve bir render testi (snapshot küçük tutularak).

## Gözlemlenebilirlik

- `notifications.status` üzerinden pano: gönderilen/teslim/başarısız oranı kanal bazında.
- Başarısız oranı %5'i aşarsa alarm (bkz. `sky-observability`).
- Loglarda e-posta/telefon maskeli (`a***@example.com`).

## Kontrol listesi

- [ ] Gönderim kuyrukta, istek yolunda değil
- [ ] Idempotency anahtarı var; yeniden deneme politikası tanımlı
- [ ] İşlemsel/pazarlama ayrımı; pazarlama için rıza ve abonelikten çık bağlantısı; SMS için İYS
- [ ] SPF/DKIM/DMARC kurulu; bounce webhook'u işleniyor
- [ ] Şablonlar çok dilli, kaçışlı, önizlenebilir, düz metin alternatifi var
- [ ] OTP güvenlik sınırları (süre, deneme, rate limit)
- [ ] Kişisel veri loglanmıyor
