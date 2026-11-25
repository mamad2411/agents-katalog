---
name: sky-observability
description: >-
  Üretimde görünürlük: hata izleme (Sentry — Next.js kurulumu, source map, release, kullanıcı
  bağlamı, replay maskeleme), yapılandırılmış loglama (pino, istek ID'si, PII yok), metrikler
  ve Web Vitals, ürün analitiği (PostHog/Plausible/Umami) ve KVKK/GDPR çerez onayı, olay
  adlandırma, uptime ve sağlık uç noktası, alarm tasarımı ve yorgunluğu, panolar, denetim
  kayıtları, runbook. "Sentry ekle", "log", "analytics", "izleme", "neden çöktüğünü
  göremiyoruz" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Gözlemlenebilirlik

## Dört sinyal, dört araç

| Sinyal | Soru | Varsayılan araç |
|---|---|---|
| **Hatalar** | Ne kırıldı, kimde, hangi sürümde? | Sentry |
| **Loglar** | Ne oldu, hangi sırayla? | pino → platform logları / Axiom / Better Stack |
| **Metrikler** | Ne kadar hızlı, ne kadar sık? | Web Vitals + platform metrikleri (+ OpenTelemetry) |
| **Ürün olayları** | Kullanıcı ne yaptı? | PostHog (zengin) / Plausible-Umami (hafif, çerezsiz) |
| **Uptime** | Ayakta mı? | Better Stack / Checkly / UptimeRobot |

Küçük proje için minimum: Sentry + platform logları + Plausible + uptime. Hepsi 1 günde kurulur.

## Hata izleme: Sentry

```bash
npx @sentry/wizard@latest -i nextjs   # sentry.client/server/edge.config.ts, instrumentation.ts, next.config sarmalayıcı
```
```ts
// sentry.server.config.ts
Sentry.init({
  dsn: env.SENTRY_DSN,
  environment: env.VERCEL_ENV ?? "development",
  release: env.VERCEL_GIT_COMMIT_SHA,          // deploy ile eşleşen sürüm
  tracesSampleRate: 0.1,                       // prod'da %10; dev'de 1.0
  beforeSend(event) {                          // PII temizliği
    if (event.request?.cookies) delete event.request.cookies;
    return event;
  },
  ignoreErrors: ["ResizeObserver loop", /^Loading chunk \d+ failed/],
});
```
- **Source map** yükle (wizard ayarlar; `SENTRY_AUTH_TOKEN` CI'da) — yoksa minified stack işe yaramaz.
- **Kullanıcı bağlamı:** `Sentry.setUser({ id })` — e-posta/isim **değil** (gerekirse hash).
- **Tag/context:** `orgId`, `plan`, `feature` etiketleri; hata gruplamada ve filtrede altın değer.
- **Session Replay:** `maskAllText: true, blockAllMedia: true` ile; form alanları zaten maskeli; replay örnekleme %1–10, hatalarda %100.
- `error.tsx` ve `global-error.tsx` içinde `Sentry.captureException(error)`; route handler'larda `Sentry.captureException` + genel 500 yanıtı.
- Beklenen hatalar (422 doğrulama, 404) Sentry'ye **gitmez**; yalnızca beklenmeyenler.
- Alarm kuralları: yeni hata türü (ilk görülme), hata oranı ani artış, belirli etiket (ödeme) → anında.
- Çözümlenen hata "release X'te düzeltildi" işaretle; regresyonda otomatik yeniden açılır.

Alternatifler: GlitchTip (self-host, Sentry uyumlu), Highlight.io, Bugsnag.

## Loglama

```ts
// lib/logger.ts
import pino from "pino";
export const logger = pino({
  level: env.LOG_LEVEL ?? "info",
  redact: { paths: ["req.headers.authorization", "req.headers.cookie", "*.password", "*.token", "*.email", "*.phone"], censor: "[redacted]" },
  ...(process.env.NODE_ENV !== "production" && { transport: { target: "pino-pretty" } }),
});
// istek bağlamı
export const withRequest = (requestId: string, userId?: string) => logger.child({ requestId, userId });
```
- **JSON** satırları; `level`, `time`, `msg`, `requestId`, `userId`, `durationMs`, `route`.
- `requestId`: gelen `x-request-id` varsa al, yoksa üret; yanıt başlığına koy; Sentry tag'ine ekle → hata ↔ log bağlanır.
- Seviyeler: `error` (müdahale gerek), `warn` (anormal ama tolere), `info` (iş olayı: sipariş oluştu), `debug` (geliştirme).
- **PII yok**: e-posta, telefon, ad, IP (gerekirse kısaltılmış), token, kart. `redact` ile zorla.
- `console.log` prod'da yok (`sky-quality` hook'u uyarır); ya logger ya sil.
- Next.js: sunucu logları Vercel'de otomatik toplanır; kalıcılık ve arama için Log Drain → Axiom / Better Stack / Datadog.
- Edge/istemci: tarayıcıda log yok (gürültü + sızıntı); istemci hatası Sentry'ye.

## Metrikler ve Web Vitals

```tsx
// app/layout.tsx içinde bir client bileşeni
"use client";
import { useReportWebVitals } from "next/web-vitals";
export function WebVitals() {
  useReportWebVitals((m) => analytics.track("web_vital", { name: m.name, value: m.value, rating: m.rating, path: location.pathname }));
  return null;
}
```
- LCP/INP/CLS/TTFB gerçek kullanıcıdan (RUM); Vercel Speed Insights veya kendi analitiğine yolla.
- Sunucu: p50/p95/p99 gecikme route bazında, hata oranı, DB sorgu süresi (Prisma/Drizzle logger'dan yavaş sorgu > 200 ms uyarısı).
- Kuyruk: bekleyen iş sayısı, başarısız iş oranı, en eski işin yaşı.
- İş metrikleri: kayıt, dönüşüm, ödeme başarısızlığı — teknik panoda da görünsün (teknik sorun iş metriğinden fark edilir).
- OpenTelemetry (`@vercel/otel`) ile trace → Sentry/Axiom/Honeycomb; servis sınırlarını geçen istekleri izlemek için.

## Ürün analitiği

**Seçim:** PostHog (olaylar, funnel, feature flag, replay; EU host), Plausible/Umami (sayfa görüntüleme + basit olaylar, **çerezsiz** → onay gerekmez), Vercel Analytics (hafif), GA4 (yaygın ama onay + yurt dışı aktarım sorunları).

**Olay adlandırma:** `nesne_eylem` snake_case, geçmiş zaman yok: `appointment_created`, `checkout_started`,
`plan_upgraded`. Özellikler: `plan`, `source`, `value` — **PII yok**. Bir `events.md` sözlüğü tut.

```ts
// lib/analytics.ts — tek sarmalayıcı; sağlayıcı değişirse burası değişir
export const analytics = {
  track(event: EventName, props?: Record<string, string | number | boolean>) { if (!consent.analytics) return; posthog.capture(event, props); },
  identify(userId: string, traits?: { plan?: string }) { if (!consent.analytics) return; posthog.identify(userId, traits); },
};
```

**KVKK / GDPR:**
- Çerez kullanan analitik, pazarlama pikselleri, replay → **onaydan sonra** yükle (`consent.analytics`).
  Zorunlu çerezler (oturum) onay gerektirmez.
- Onay bileşeni: "Kabul et" / "Reddet" eşit ağırlıkta, ayrıntılı seçim; tercih çerezde + sunucuda kayıt (ne zaman, hangi sürüm).
- Çerezsiz araç (Plausible/Umami) + sunucu tarafı olaylar ile onaysız temel ölçüm mümkün — en az sürtünmeli yol.
- Veri yurt dışına gidiyorsa aydınlatma metninde yaz; mümkünse EU/TR bölge seç.
- Replay'de maskeleme zorunlu; sağlık/finans verisi içeren sayfalarda replay kapalı.

## Uptime ve sağlık

```ts
// app/api/health/route.ts
export const dynamic = "force-dynamic";
export async function GET() {
  const checks = await Promise.allSettled([db.execute(sql`select 1`), redis?.ping()]);
  const ok = checks.every((c) => c.status === "fulfilled");
  return Response.json({ status: ok ? "ok" : "degraded", version: env.APP_VERSION, checks: checks.map((c) => c.status) }, { status: ok ? 200 : 503 });
}
```
- Dış izleyici 1 dk'da bir `GET /api/health` + ana sayfa (içerikte beklenen metin), 2 bölgeden; 2 ardışık hatada alarm.
- Durum sayfası (Better Stack/Instatus) kullanıcıya açık; olaylar oraya yazılır.
- SSL sertifika süresi ve alan adı süresi izlemesi (sık unutulan iki kesinti sebebi).
- Cron/kuyruk işleri için "heartbeat" izleme: iş bitince ping atar, gelmezse alarm (Sentry Crons / Better Stack heartbeat).

## Alarmlar

- Her alarmın **sahibi ve runbook'u** var; yoksa alarm değil gürültü.
- Seviye: **sayfa** (uyandır: site down, ödeme hata oranı > %5, DB bağlantısı yok) / **bildirim** (iş saatinde: hata artışı, p95 > 2 s, kuyruk gecikmesi) / **rapor** (haftalık özet).
- Eşikleri oran ve süreyle ver ("5 dk boyunca hata oranı > %2"), tek olayla değil.
- Yorgunluk kontrolü: ayda alarmların ≥ %80'i eyleme dönmüyorsa eşikleri düzelt veya alarmı sil.
- Kanal: kritik → telefon/SMS/Opsgenie; diğerleri Slack/e-posta.

## Denetim kaydı (audit log)

Hassas işlemler için ayrı tablo: `audit_logs(id, actor_id, action, target_type, target_id, metadata jsonb, ip_trunc, created_at)`.
Giriş, rol değişimi, ödeme/plan değişimi, veri dışa aktarma, silme. Uygulama logundan ayrı; silinmez (append-only); yönetici panelinde görünür.

## Panolar

Tek "sağlık" panosu: istek/sn, hata oranı, p95, CWV, aktif kullanıcı, kuyruk, son deploy işareti. Deploy
işaretleri (Sentry release / Vercel deploy olayı) grafiğe çizilir → "deploy'dan sonra bozuldu" bir bakışta.

## Runbook şablonu (`docs/runbooks/<alarm>.md`)

```
Alarm: ödeme webhook hata oranı > %5
Etki: ödemeler DB'ye işlenmiyor; kullanıcı erişimi gecikir
İlk kontrol: Sentry → tag webhook=stripe; Vercel logs → /api/webhooks/stripe 5xx
Olası sebepler: imza anahtarı değişti, DB bağlantı havuzu dolu, şema değişikliği
Düzeltme: …; Stripe panelinden webhook'ları yeniden gönder
Doğrulama: hata oranı 10 dk içinde < %1
```

## Kontrol listesi

- [ ] Sentry: source map, release, environment, PII temizliği, beklenen hatalar filtrelenmiş
- [ ] Yapılandırılmış log + requestId; PII redact; prod'da console.log yok
- [ ] Web Vitals RUM toplanıyor
- [ ] Analitik tek sarmalayıcı; olay sözlüğü; onay akışı; PII yok
- [ ] `/api/health` + dış uptime + SSL/alan adı izleme
- [ ] Alarmlar sahipli, runbook'lu, eşikleri oran/süre bazlı
- [ ] Hassas işlemler audit log'da
