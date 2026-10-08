---
name: saas-testing
description: >
  SaaS uygulaması için test stratejisi kur. Vitest ile birim test, Playwright
  ile E2E test, API route testi, webhook mock, Stripe test modu ve CI
  entegrasyonu. Bu skill'i kullanıcı test, test yazma, E2E, birim test,
  Playwright, Vitest, coverage veya kalite güvencesi ile ilgili bir şey
  istediğinde kullan. "Test yaz", "test kur", "E2E ekle", "CI'da test
  çalıştır" gibi ifadeler tetikler.
---

# SaaS Testing — Test Stratejisi ve Kalite Güvencesi

Bu skill, bir SaaS uygulamasının test altyapısını kurar. Test olmadan "production-ready" iddiası eksiktir — ödeme webhook'unun çalıştığını, auth akışının kırılmadığını ve API'nin beklendiği gibi davrandığını sadece testlerle garanti edebilirsin.

**Bağımlılık:** Bu skill **saas-launcher** orkestratör skill'inin Deployment öncesi kalite güvence adımıdır. Bağımsız olarak da kullanılabilir.

**Bağlı skill'ler:**
- **saas-auth** — Giriş/kayıt akışları E2E test edilir.
- **saas-payments** — Webhook handler'lar ve checkout akışı test edilir.
- **saas-api-security** — Rate limiting ve input validation testleri.

---

## Test Piramidi — SaaS İçin

### Hangi Test Türü Ne Zaman

**Birim Test (Unit Test) — Vitest:**
Tekil fonksiyonları ve utility'leri test eder. Hızlı çalışır, dış bağımlılık yok. Kullanım: fiyat hesaplama, plan kontrolü, input validation, helper fonksiyonlar.

**Entegrasyon Test (Integration Test) — Vitest:**
API route'larını test eder. HTTP isteği gönderir, yanıtı doğrular. Kullanım: auth endpoint'leri, checkout API, webhook handler.

**Uçtan Uca Test (E2E Test) — Playwright:**
Gerçek bir tarayıcıda kullanıcı akışlarını test eder. En yavaş ama en güvenilir. Kullanım: kayıt → giriş → plan satın al → dashboard erişimi.

### Başlangıç Önceliği

Day 1'de her şeyi test etmeye çalışma. Öncelik sırası:

1. **Webhook handler testi** — Para alınıp plan aktifleşmezse gelir kaybı
2. **Auth akışı E2E testi** — Giriş yapılamazsa uygulama kullanılamaz
3. **Kritik API route testleri** — Plan kontrolü, kaynak oluşturma
4. **Input validation testleri** — Güvenlik katmanı

---

## Vitest Kurulumu

### Neden Vitest

Jest'e alternatif, modern test runner. Avantajları: Vite tabanlı — çok hızlı, ESM desteği doğal, Jest uyumlu API (geçiş kolay), TypeScript desteği dahili, HMR ile watch mode.

### Kurulum

```
npm install -D vitest @vitejs/plugin-react
```

Proje kökünde `vitest.config.ts` oluştur. Test dosyaları için `__tests__/` klasörü veya dosya adında `.test.ts` / `.spec.ts` uzantısı kullan.

`package.json`'a script ekle:
- `"test": "vitest run"` — tek seferlik çalıştır
- `"test:watch": "vitest"` — watch mode
- `"test:coverage": "vitest run --coverage"` — coverage raporu

### API Route Testi Yaklaşımı

Next.js API route'larını test etmek için route handler fonksiyonunu doğrudan import edip mock Request nesnesi ile çağır. Gerçek HTTP sunucusu ayağa kaldırmaya gerek yok.

Her test:
1. Mock request oluştur (method, headers, body)
2. Route handler'ı çağır
3. Response status ve body'yi doğrula

### Webhook Handler Testi

Webhook testleri en kritik testlerdir. Test stratejisi:

1. **İmza doğrulama testi:** Geçerli imza ile webhook'un işlendiğini, geçersiz imza ile reddedildiğini doğrula.
2. **Event işleme testi:** Her webhook event türü için veritabanı değişikliğini doğrula. Örnek: `checkout.session.completed` → kullanıcı planı "pro" olmalı.
3. **Idempotency testi:** Aynı event'i iki kez gönder, sonucun değişmediğini doğrula.

**Stripe test modu:** Stripe CLI ile webhook'ları localhost'a yönlendir:
```
stripe listen --forward-to localhost:3000/api/stripe/webhook
stripe trigger checkout.session.completed
```

### Mock Stratejisi

Dış servisleri mock'la, kendi kodunu mock'lama:

- **Mock'lanması gerekenler:** Stripe API, Resend API, Supabase client (isteğe bağlı)
- **Mock'lanmaması gerekenler:** Kendi utility fonksiyonların, validation şemaların — bunları gerçek çalıştır

Vitest'in `vi.mock()` fonksiyonu ile modül seviyesinde mock:
- Stripe SDK'yı mock'la — gerçek API çağrısı yapılmasın
- Resend SDK'yı mock'la — test sırasında e-posta gönderilmesin

---

## Playwright E2E Kurulumu

### Neden Playwright

Cypress'e alternatif, modern E2E test aracı. Avantajları: Çoklu tarayıcı desteği (Chromium, Firefox, WebKit), otomatik bekleme (auto-wait), trace viewer ile debugging, headless CI modu.

### Kurulum

```
npm install -D @playwright/test
npx playwright install
```

`playwright.config.ts` oluştur. Temel ayarlar:
- `baseURL`: `http://localhost:3000`
- `webServer`: test öncesi dev server'ı otomatik başlat
- `use.trace`: `on-first-retry` — sadece başarısız testlerde trace kaydet

### Temel E2E Senaryoları

**Auth akışı:**
1. Landing page'e git
2. "Giriş Yap" butonuna tıkla
3. E-posta ile Magic Link giriş formunu doldur (veya test OAuth akışı)
4. Dashboard'a yönlendirildiğini doğrula
5. Korumalı sayfaya erişebildiğini doğrula

**Checkout akışı:**
1. Giriş yap
2. Fiyatlandırma sayfasına git
3. Plan seç
4. Stripe Checkout'a yönlendirildiğini doğrula
5. (Test modunda ödeme yap)
6. Başarı sayfasına dönüşü doğrula

**Landing page:**
1. Ana sayfanın yüklendiğini doğrula
2. Tüm bölümlerin render edildiğini doğrula
3. CTA butonlarının çalıştığını doğrula
4. Mobil görünümde navigasyonun çalıştığını doğrula

### Playwright İpuçları

- **Test izolasyonu:** Her test bağımsız olmalı. Önceki testin state'ine bağımlı olma.
- **Locator kullan, CSS selector değil:** `page.getByRole()`, `page.getByText()`, `page.getByTestId()` — CSS selector'lar kırılgan.
- **Auto-wait'e güven:** `waitForTimeout()` kullanma — Playwright elementlerin görünmesini otomatik bekler.
- **Screenshot on failure:** Başarısız testlerde otomatik screenshot al — CI'da debugging için.

---

## CI Entegrasyonu

### GitHub Actions ile Test

CI pipeline'a test adımlarını ekle:

1. **Birim + entegrasyon testleri:** `vitest run` — her PR'da çalışmalı
2. **E2E testleri:** `npx playwright test` — her PR'da veya sadece main merge öncesinde
3. **Coverage raporu:** PR'a yorum olarak coverage değişimini göster

### CI'da Playwright

Playwright CI'da headless modda çalışır. GitHub Actions'da `playwright install --with-deps` ile tarayıcı bağımlılıklarını kur. Başarısız testlerin trace'ini artifact olarak sakla — debugging için indir ve `npx playwright show-trace` ile aç.

---

## Test Coverage

### Hedefler

- **Webhook handler: %100** — Burası para. Her event türü, her edge case test edilmeli.
- **Auth middleware: %90+** — Güvenlik katmanı yüksek coverage istemeli.
- **API route'ları: %80+** — Temel akışlar ve hata durumları.
- **Utility fonksiyonlar: %80+** — İş mantığı.
- **UI bileşenleri: %50+** — E2E testlerle dolaylı olarak test edilir, birim test önceliği düşük.

**%100 genel coverage hedefleme.** Anlamsız testler yazmak, test yazmamak kadar kötüdür. Kritik yolları yüksek coverage'la koru, geri kalanı pragmatik tut.

---

## Gotchas

- **Stripe webhook testi atlanırsa:** "Production'da çalışır" varsayımı en tehlikeli varsayımdır. Stripe CLI ile her event türünü ayrı ayrı test et.
- **E2E testlerde flaky test sorunu:** Zamanlama bağımlı testler rastgele başarısız olur. `waitForTimeout()` yerine Playwright'ın auto-wait mekanizmasına güven.
- **Test veritabanı izolasyonu:** Testler production veya development veritabanını kullanmamalı. Ayrı bir test veritabanı veya her test öncesi seed + sonrası temizleme stratejisi uygula.
- **Mock'lar gerçeklikten kopar.** Mock'ladığın servisin API'si değişirse testlerin hâlâ geçer ama production'da çöker. Düzenli olarak mock'ları gerçek API ile karşılaştır.
- **CI'da ortam değişkenleri.** Test ortamı için ayrı `.env.test` dosyası veya CI secret'ları kullan. Production anahtarları CI'da olmamalı.
- **E2E testleri yavaştır.** Tüm E2E suite'ini her commit'te çalıştırmak CI'ı yavaşlatır. Kritik akışları her PR'da, tam suite'i main merge öncesinde çalıştır.
