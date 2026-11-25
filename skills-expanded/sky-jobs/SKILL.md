---
name: sky-jobs
description: >-
  Arka plan işleri ve zamanlanmış görevler: Inngest / Trigger.dev / BullMQ / pg-boss /
  QStash / Vercel Cron seçimi, iş tasarımı (idempotent, küçük adımlar), yeniden deneme ve
  üstel geri çekilme, dead letter, eşzamanlılık ve hız sınırı, uzun süren iş akışları (adım
  adım, bekle, olay bekle), cron ifadeleri ve saat dilimi, ilerleme bildirimi ve iş paneli.
  "Arka planda çalışsın", "her gece", "kuyruk", "cron", "uzun süren işlem" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Arka Plan İşleri

## Ne zaman arka plana?

İstek yolunda > 1 sn sürebilecek veya başarısız olabilecek her şey: e-posta/SMS, PDF, görsel işleme,
üçüncü parti API senkronu, toplu içe aktarım, rapor, webhook teslimi, AI çağrıları, hatırlatmalar.
Kullanıcıya hemen "Hazırlanıyor…" de, bitince bildir.

## Araç seçimi

| Ortam | Seçim |
|---|---|
| Sunucusuz (Vercel), adım adım akışlar, az altyapı | **Inngest** veya **Trigger.dev** |
| Kendi sunucun + Redis | **BullMQ** |
| Yalnızca Postgres var | **pg-boss** / Supabase Queues (pgmq) |
| Basit HTTP tetikleyici + gecikme | **Upstash QStash** |
| Sadece periyodik ping | Vercel Cron / GitHub Actions schedule → route handler |

## İş tasarımı kuralları

1. **Idempotent**: aynı iş iki kez çalışırsa sonuç değişmez (ID ile kontrol, upsert, "zaten gönderildi mi").
2. **Küçük ve tek amaçlı**: "1000 e-posta gönder" değil, 1000 × "bir e-posta gönder" (fan-out).
3. **Girdi = ID'ler**, tam veri değil; iş çalışırken güncel veriyi okur.
4. **Zaman aşımı** ve **yeniden deneme** açık: üstel geri çekilme (10s, 1m, 10m, 1h), maks 5.
5. Kalıcı hata (geçersiz e-posta, 4xx) → yeniden deneme yok, işaretle.
6. **Dead letter**: tükenen işler ayrı listede, panelde görünür, elle yeniden çalıştırılabilir.

## Inngest örneği (adım adım akış)

```ts
export const onboarding = inngest.createFunction(
  { id: "onboarding-drip", concurrency: { limit: 10 } },
  { event: "user/signed.up" },
  async ({ event, step }) => {
    await step.run("hoş geldin e-postası", () => sendWelcome(event.data.userId));
    await step.sleep("1 gün bekle", "1d");
    const activated = await step.run("aktivasyon kontrol", () => hasCreatedFirstBooking(event.data.userId));
    if (!activated) await step.run("ipucu e-postası", () => sendTip(event.data.userId));
    const paid = await step.waitForEvent("ödeme bekle", { event: "billing/paid", timeout: "7d", match: "data.userId" });
    if (!paid) await step.run("deneme bitiyor", () => sendTrialEnding(event.data.userId));
  },
);
```
Her `step` ayrı yeniden denenir ve sonucu saklanır → yarıda kalan akış kaldığı yerden devam eder.

## Zamanlanmış işler

- Cron ifadesi + **saat dilimi** açık: `TZ=Europe/Istanbul 0 9 * * *` (her gün 09:00 İstanbul).
- Randevu hatırlatma gibi "olaydan X önce" işler için cron tarama yerine **gecikmeli iş** (olay oluşunca `sendAt` ile planla; iptal edilirse işi iptal et).
- Uzun cron işi → kendini parçalara böler (sayfa sayfa) ve fan-out yapar.
- Çakışma kilidi: aynı cron iki kez üst üste çalışmasın.

## Eşzamanlılık ve hız sınırı

- Üçüncü parti API limitleri (ör. SMS sağlayıcı saniyede 10) → kuyruk seviyesinde `rateLimit`/`throttle`.
- Kiracı başına eşzamanlılık (`concurrency: { key: "event.data.orgId", limit: 2 }`) → bir müşteri herkesi bekletmez.

## Kullanıcıya ilerleme

- İş tablosu: `jobs(id, type, status, progress, result_url, error, created_by, created_at)`.
- UI: "Rapor hazırlanıyor %45" — polling (2 sn) veya realtime; bitince toast + indirme bağlantısı + bildirim.
- Uzun işlerde "Bitince e-posta gönder" seçeneği — kullanıcılar sekmeyi kapatabilsin.

## Gözlem

- İş paneli (Inngest/Trigger dashboard, BullMQ için Bull Board — yetki arkasında).
- Metrikler: kuyruk derinliği, en eski bekleyen iş yaşı, hata oranı; alarm (bkz. `sky-observability`).
- Cron için heartbeat izleme (çalışmadıysa haber ver).
