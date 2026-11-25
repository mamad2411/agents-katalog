# 12 — E2E browser, visual, mobile & desktop

## 1. Prinsip E2E
- **Sedikit tapi berharga**: 3–10 alur yang menghasilkan uang/kepercayaan
  (login, cari, checkout, bayar, unduh invoice, ganti password, hapus akun).
- Satu skenario = satu tujuan bisnis. Jangan menguji 20 variasi form di e2e.
- Data dibuat lewat **API/seed**, bukan lewat UI (cepat & stabil).
- Setiap e2e harus bisa jalan sendiri dan paralel (data unik per worker).

## 2. Playwright — pola yang benar
```ts
// playwright.config.ts
export default defineConfig({
  testDir: "e2e",
  retries: process.env.CI ? 0 : 0,          // 0: flaky harus diperbaiki, bukan diulang
  reporter: [["list"], ["html", { open: "never" }]],
  use: { baseURL: process.env.BASE_URL ?? "http://localhost:3000",
         trace: "on-first-retry", video: "retain-on-failure",
         screenshot: "only-on-failure", locale: "id-ID",
         timezoneId: "Asia/Jakarta" },
  projects: [
    { name: "chromium", use: devices["Desktop Chrome"] },
    { name: "firefox", use: devices["Desktop Firefox"] },
    { name: "webkit", use: devices["Desktop Safari"] },
    { name: "mobile", use: devices["iPhone 15"] },
  ],
})
```
```ts
test("pengguna bisa checkout", async ({ page }) => {
  await page.goto("/")
  await page.getByRole("link", { name: /masuk/i }).click()
  await page.getByLabel("Email").fill("uji@example.com")
  await page.getByLabel("Kata sandi").fill("Rahasia123!")
  await page.getByRole("button", { name: /masuk/i }).click()
  await expect(page.getByRole("heading", { name: /produk/i })).toBeVisible()
  await page.getByRole("button", { name: /tambah ke keranjang/i }).first().click()
  await page.getByRole("link", { name: /keranjang/i }).click()
  await page.getByRole("button", { name: /bayar/i }).click()
  await expect(page.getByText(/pesanan .* diterima/i)).toBeVisible()
})
```
Aturan selector: `getByRole`/`getByLabel`/`getByPlaceholder` → `getByText` → `getByTestId`.
**Dilarang**: XPath struktural, `.nth(3)`, class CSS, `waitForTimeout`, `sleep`.

## 3. Auth sekali, pakai ulang
```ts
// e2e/auth.setup.ts → simpan storageState, dipakai semua test
await page.goto("/login"); await login(page)
await page.context().storageState({ path: "e2e/.auth/user.json" })
// config: projects: [{ name: "setup", testMatch: /auth\.setup\.ts/ },
//                    { name: "chromium", dependencies: ["setup"], use: { storageState: "e2e/.auth/user.json" } }]
```
Jangan login lewat UI di setiap test. Jangan simpan kredensial di repo (pakai env).

## 4. Jaringan & determinisme
- Mock pihak ketiga: `page.route("**/api/analytics/**", r => r.abort())`.
- Tunggu respons nyata: `await page.waitForResponse(r => r.url().includes("/api/items") && r.ok())`.
- Matikan animasi: `page.emulateMedia({ reducedMotion: "reduce" })` + CSS.
- Freeze waktu bila UI menampilkan tanggal relatif.
- Uji kondisi gagal: API 500, offline (`context.setOffline(true)`), lambat (delay 3 s → skeleton).

## 5. Visual regression
```bash
npx playwright test --update-snapshots        # hanya setelah perubahan disengaja
dvisual http://localhost:3000                 # diff % piksel + peta diff
```
- Baseline per viewport (360, 768, 1440) dan per tema (light/dark).
- Mask konten dinamis (tanggal, avatar, iklan) — jangan matikan seluruh halaman.
- Ambang: ≤0.1% piksel; di atas itu review manual.

## 6. Cross-browser, device, dan PWA
- Minimum: Chromium + WebKit (Safari) + Firefox; mobile: 1 iOS, 1 Android.
- Uji: viewport 320–1920, rotasi, zoom 200%, font besar (AX), dark mode.
- PWA: offline setelah cache, install prompt, update service worker (jangan stale forever),
  push notification, simpan form saat offline.
- Sentuh: target ≥24 px, jarak ≥8 px, tidak ada hover-only.

## 7. Desktop (Electron/Tauri)
- Uji paket hasil build, bukan `npm run dev`.
- Jendela: resize minimum, multi-monitor, DPI, menu, shortcut, dialog file.
- Update/rollback, izin filesystem, signature/notarization (macOS).

## 8. Checklist rilis UI
- [ ] 3 alur kritis hijau di 3 browser.
- [ ] Tidak ada error console baru (`page.on("console")` → gagalkan bila `error`).
- [ ] Tidak ada request 4xx/5xx tak terduga.
- [ ] axe: 0 violation serius/kritis.
- [ ] Visual diff ≤ ambang.
- [ ] Waktu muat p95 sesuai anggaran (`14-performa.md`).

## 9. Perintah
```bash
npx playwright test                     # semua project
npx playwright test --project=chromium -g "checkout"
npx playwright test --ui                # debug interaktif
npx playwright show-trace trace.zip     # analisis kegagalan CI
testing-forge generate tests-web w1            # scaffold siap jalan (4/4 lulus)
```
