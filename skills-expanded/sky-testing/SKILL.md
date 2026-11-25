---
name: sky-testing
description: >-
  Web uygulamaları için test stratejisi: test piramidi, neyin test edileceği, Vitest +
  Testing Library bileşen testleri, MSW ile ağ taklidi, server action / route handler /
  servis testleri, veritabanı testleri, Playwright E2E (fixture, auth durumu, sayfa nesneleri),
  görsel regresyon, kapsam hedefleri, kararsız (flaky) test tedavisi ve CI'da çalıştırma.
  Test yazarken, "nasıl test edeyim", "test kırılıyor" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Test

## Piramit ve hedefler

| Katman | Araç | Oran | Ne test eder |
|---|---|---|---|
| Birim | Vitest | çok | saf fonksiyonlar, şema/doğrulama, yardımcılar, servis mantığı |
| Bileşen | Vitest + Testing Library + user-event | orta | davranış: tıkla → görünür, form hatası, erişilebilir isimler |
| Entegrasyon | Vitest + test DB / MSW | orta | servis + repository, route handler, server action |
| E2E | Playwright | az | kritik kullanıcı yolları: kayıt, giriş, satın alma, ana akış |

Hedef: kapsam ≥ %80 **anlamlı** satır; ama asıl ölçüt "bu test hangi hatayı yakalar?".
Snapshot testlerini yalnızca küçük, kararlı çıktılar için kullan.

## Ne test edilir, ne edilmez

Test et: iş kuralları, sınır değerleri, hata yolları, yetki (başkasının kaynağı → 403/404),
doğrulama mesajları, erişilebilirlik (axe), para/tarih hesapları, Türkçe karakter işleme.
Test etme: üçüncü parti kütüphanenin kendisi, stil detayları (renk, px), uygulama detayı
(state'in iç yapısı), tek satırlık getter'lar.

## Vitest kurulumu

```ts
// vitest.config.ts
export default defineConfig({
  plugins: [react(), tsconfigPaths()],
  test: {
    environment: "jsdom",          // bileşen testleri; sunucu testleri için "node" (// @vitest-environment node)
    setupFiles: ["./tests/setup.ts"],
    globals: true,
    coverage: { provider: "v8", reporter: ["text", "html"], thresholds: { lines: 80 } },
  },
});
```
`tests/setup.ts`: `@testing-library/jest-dom/vitest`, MSW server `listen/resetHandlers/close`,
`cleanup`. Zaman için `vi.useFakeTimers()` + `vi.setSystemTime()`; rastgelelik için `vi.spyOn(Math, "random")`.

## Bileşen testleri (Testing Library)

- Sorgu önceliği: `getByRole` (erişilebilir isimle) → `getByLabelText` → `getByText` → en son `getByTestId`.
  Bulamıyorsan muhtemelen erişilebilirlik sorunu var.
- Etkileşim `@testing-library/user-event` ile (`await user.click`, `user.type`); `fireEvent` değil.
- Asenkron: `await screen.findByText(...)` / `waitFor`; `act` uyarısı varsa eksik `await` ara.
- Bir test = bir davranış. İsim: "boş gönderimde ad alanı hatası gösterir".

```tsx
test("geçersiz telefonla gönderimde hata gösterir", async () => {
  const user = userEvent.setup();
  render(<AppointmentForm />);
  await user.type(screen.getByLabelText("Telefon"), "123");
  await user.click(screen.getByRole("button", { name: "Randevu oluştur" }));
  expect(await screen.findByText("Geçerli bir cep telefonu girin")).toBeInTheDocument();
});
```

Next.js özel: `next/navigation` (`useRouter`, `usePathname`) ve `next/image`'ı `vi.mock` ile taklit et;
Server Component'leri doğrudan render etmek yerine servis/action testleriyle kapsa, E2E ile bütünle.

## Ağ: MSW

Bileşen ve hook testlerinde gerçek ağ yok; `msw` ile uç noktaları tanımla:
```ts
export const handlers = [
  http.get("/api/posts", () => HttpResponse.json([{ id: "1", title: "Merhaba" }])),
  http.post("/api/posts", async ({ request }) => HttpResponse.json(await request.json(), { status: 201 })),
];
```
Hata senaryosu için testte `server.use(http.get("/api/posts", () => HttpResponse.error()))`.
Playwright'ta da `page.route()` veya MSW tarayıcı modu; ama kritik E2E'ler gerçek backend'e gitsin.

## Sunucu tarafı testleri

- **Servisler:** saf fonksiyon gibi; repository'yi arayüzle enjekte et veya test DB'si kullan.
- **Route handler:** `new Request("http://x/api/posts", { method: "POST", body: ... })` ile çağır,
  `Response` durum kodunu ve gövdesini doğrula.
- **Server action:** doğrudan fonksiyon çağrısı; `cookies()`/`headers()` kullanıyorsa `vi.mock("next/headers")`.
- **Yetki matrisi:** her uç nokta için anonim / sahibi / başka kullanıcı / admin satırlarını test et.

## Veritabanı testleri

- Gerçek bir test DB (Docker Postgres veya SQLite/PGlite): mock ORM yerine gerçek sorgu.
- Her test transaction içinde çalışıp geri alınsın, ya da test başına `TRUNCATE`.
- Fabrika fonksiyonları (`createUser({ role: "admin" })`) ile deterministik veri; `faker` seed'li.
- Migration'lar CI'da sıfır DB'ye uygulanıp testler koşsun.

## Playwright E2E

```ts
// tests/e2e/auth.setup.ts — bir kez giriş yap, durumu sakla
setup("giriş", async ({ page }) => {
  await page.goto("/login");
  await page.getByLabel("E-posta").fill(process.env.E2E_USER!);
  await page.getByLabel("Parola").fill(process.env.E2E_PASS!);
  await page.getByRole("button", { name: "Giriş yap" }).click();
  await expect(page).toHaveURL("/dashboard");
  await page.context().storageState({ path: "tests/.auth/user.json" });
});
```
- Locator'lar rol/etiket tabanlı; `data-testid` yalnızca anlamlı rol olmayan yerlerde.
- `expect(locator).toBeVisible()` gibi **otomatik bekleyen** iddialar; `waitForTimeout` yok.
- Test verisini API/DB ile hazırla, UI'dan değil (hızlı ve kararlı).
- Her test bağımsız: kendi kullanıcısı/kaydı; paylaşılan durumdan kaçın.
- Mobil viewport projesi ekle (375×812) — kritik akışlar orada da geçsin.
- `@axe-core/playwright` ile erişilebilirlik taraması (bkz. `sky-a11y`).
- Görsel regresyon: `toHaveScreenshot()` yalnızca tasarım sistemi bileşenleri ve landing için; animasyonları kapat (`animations: "disabled"`).
- Trace: `trace: "on-first-retry"`; CI'da artifact olarak sakla.

## Kararsız testler

Sebepler: gerçek zaman/zaman aşımı, sıralamaya bağlı paylaşılan durum, ağ, animasyon, `Date`,
yarış (await eksik). Tedavi: fake timers, bağımsız veri, MSW, reduced-motion, otomatik bekleyen
iddialar. **Retry ile gizleme**; retry yalnızca teşhise kadar geçici.

## CI

- Sıra: `typecheck` → `lint` → `test --coverage` → `build` → `test:e2e` (preview URL'sine karşı).
- E2E'de `--shard` ile paralel; `--reporter=github` annotations.
- Başarısız E2E'de trace/video artifact'ı yükle.
- PR'da kapsam düşüşünü raporla ama eşiği sertçe bloke etmeden önce takımla kararlaştır.

## Komutlar (package.json)

```json
"test": "vitest run",
"test:watch": "vitest",
"test:coverage": "vitest run --coverage",
"test:e2e": "playwright test",
"test:e2e:ui": "playwright test --ui"
```
