---
name: sky-a11y
description: >-
  Web erişilebilirliği (WCAG 2.2 AA): semantik HTML, klavye ile kullanım, odak yönetimi,
  ARIA kalıpları (dialog, menu, tabs, combobox), form etiketleri, kontrast, ekran okuyucu
  duyuruları, hareket tercihleri ve otomatik test (axe, Playwright). Bileşen yazarken,
  erişilebilirlik denetimi yaparken veya "a11y", "erişilebilir", "klavye" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Erişilebilirlik

## Altın kural

Önce **doğru HTML öğesi**: `<button>` tıklanır, `<a href>` gezinir, `<label>` alanı adlandırır,
`<nav> <main> <header> <footer>` bölgeleri belirler. ARIA yalnızca HTML yetmediğinde.
"ARIA yoksa, kötü ARIA'dan iyidir."

## Kontrol listesi (WCAG 2.2 AA)

**Yapı**
- [ ] Sayfada tek `<h1>`, başlık seviyeleri atlanmıyor
- [ ] `<html lang="tr">` (veya içerik dili)
- [ ] Landmark'lar: `header`, `nav`, `main`, `footer`; "İçeriğe atla" bağlantısı
- [ ] Anlamlı `<title>` her sayfada

**Klavye**
- [ ] Tüm etkileşimler Tab/Shift+Tab, Enter, Space, Esc, ok tuşlarıyla yapılabiliyor
- [ ] Odak sırası görsel sırayla uyumlu; `tabindex` > 0 yok
- [ ] Odak her zaman görünür (2.4.7) ve yapışkan header altında gizlenmiyor (2.4.11)
- [ ] Klavye tuzağı yok (modal hariç, o da Esc ile çıkılıyor)

**Görsel**
- [ ] Metin kontrastı ≥ 4.5:1, büyük metin ≥ 3:1, UI bileşenleri/odak halkası ≥ 3:1
- [ ] Bilgi yalnızca renkle iletilmiyor
- [ ] %200 yakınlaştırmada ve 320px genişlikte içerik kaybı yok
- [ ] Dokunma hedefleri ≥ 24×24px (2.5.8), tercihen 44×44

**İçerik**
- [ ] Anlamlı görsellerde `alt`, dekoratif görsellerde `alt=""`
- [ ] Yalnızca ikon olan butonlarda `aria-label`
- [ ] Bağlantı metni bağlamdan bağımsız anlamlı ("Devamını oku" değil "Fiyatlandırma hakkında devamını oku")
- [ ] Video için altyazı

**Formlar**
- [ ] Her alanın görünür `<label>`ı var (placeholder etiket değildir)
- [ ] Hata mesajı alanla `aria-describedby` ile bağlı, `aria-invalid="true"`
- [ ] Gönderimde hata varsa odak ilk hatalı alana veya hata özetine gider
- [ ] `autocomplete` öznitelikleri (`email`, `name`, `current-password`, `one-time-code`)
- [ ] Sürükle-bırak gerektiren işlemin alternatifi var (2.5.7)

**Dinamik içerik**
- [ ] Toast/durum mesajları `role="status"` (kibar) veya `role="alert"` (acil)
- [ ] Yükleniyor durumu `aria-busy` veya canlı bölgeyle duyuruluyor
- [ ] Route değişiminde odak yeni sayfanın başlığına taşınıyor (SPA)

## ARIA kalıpları (hazır kütüphane tercih et: Radix, React Aria, Headless UI)

| Bileşen | Gereken |
|---|---|
| Dialog | `role="dialog"` + `aria-modal="true"` + `aria-labelledby`; odak içeri, Esc kapatır, kapanınca odak tetikleyiciye döner; arka plan `inert` |
| Menü butonu | `aria-haspopup="menu"`, `aria-expanded`; ok tuşlarıyla gezinme |
| Sekmeler | `role="tablist/tab/tabpanel"`, `aria-selected`, ok tuşları, roving tabindex |
| Akordiyon | `<button aria-expanded aria-controls>`; veya native `<details><summary>` |
| Combobox | `role="combobox"`, `aria-expanded`, `aria-activedescendant`, listbox |
| Toggle | `<button aria-pressed>` veya `role="switch" aria-checked` |
| Tooltip | Yalnızca ek bilgi; odakta da açılır; Esc ile kapanır |

## Hareket

`prefers-reduced-motion` desteği zorunlu (bkz. `sky-motion`).

## Test

- Otomatik: `@axe-core/playwright` ile E2E'de, `vitest-axe`/`jest-axe` ile bileşen testinde.
  Otomatik araçlar sorunların yalnızca bir kısmını yakalar; gerisi manuel.
- Manuel: fareyi bırak, sayfayı yalnızca klavyeyle kullan. macOS VoiceOver (Cmd+F5) ile ana akışı dene.
- Lighthouse erişilebilirlik puanı ≥ 95 hedef (puan tek başına yeterlilik değildir).

```ts
import AxeBuilder from "@axe-core/playwright";
test("ana sayfa a11y", async ({ page }) => {
  await page.goto("/");
  const r = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag22aa"]).analyze();
  expect(r.violations).toEqual([]);
});
```
