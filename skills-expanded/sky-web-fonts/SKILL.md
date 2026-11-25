---
name: sky-web-fonts
description: >-
  Web font mühendisliği ve tipografi eşleşmeleri: font seçimi (Google Fonts, Fontshare,
  dökümhaneler), Türkçe karakter testi, variable font'lar, alt kümeleme, next/font ve
  self-host, font-display ve preload, metrik eşleşen fallback (size-adjust) ile sıfır kayma,
  karaktere göre font eşleştirme tarifleri ve OpenType özellikleri. "Font öner", "font yavaş
  yükleniyor", "Türkçe karakter bozuk", "yazı tipi" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Web Font'lar

## Türkçe testi (her fontta önce bunu yap)

Test cümlesi: **"Pijamalı hasta yağız şoföre çabucak güvendi. İĞÜŞÖÇ ığüşöç"**
Bak: `İ` noktası, `ı` noktasızlığı, `ğ` şapkası, `ş`/`ç` çengelleri düzgün çizilmiş mi, kalın ağırlıkta var mı.
`latin-ext` alt kümesi zorunlu.

## Kaynaklar

- **Google Fonts**: Inter, Geist, Manrope, Plus Jakarta Sans, DM Sans, Outfit, Sora, Space Grotesk,
  Fraunces, Instrument Serif, Newsreader, Bricolage Grotesque.
- **Fontshare** (ücretsiz, karakterli): Satoshi, General Sans, Cabinet Grotesk, Clash Display, Switzer.
- Ücretli dökümhaneler (marka işleri). Lisansta web/self-host izni olsun.

## Eşleştirme tarifleri

| Karakter | Başlık | Gövde |
|---|---|---|
| Modern SaaS, temiz | Geist / Inter Display | Geist / Inter |
| Sıcak, samimi ürün | Bricolage Grotesque | DM Sans |
| Editoryal, dergi | Fraunces / Instrument Serif | Inter / Source Serif |
| Lüks, butik | Cormorant / Playfair Display | Manrope |
| Teknik, geliştirici | Space Grotesk | Inter + JetBrains Mono |
| Oyunbaz, genç | Clash Display / Cabinet Grotesk | Satoshi |
| Klinik/sağlık, güven | Plus Jakarta Sans | Plus Jakarta Sans (tek aile) |

En fazla 2 aile; tek aile + ağırlık/boyut kontrastı çoğu zaman yeter. Gövde fontu **okunaklı** olmalı.

## Next.js (next/font)

```ts
import { Inter, Fraunces } from "next/font/google";
export const sans = Inter({ subsets: ["latin", "latin-ext"], variable: "--font-sans", display: "swap" });
export const display = Fraunces({ subsets: ["latin", "latin-ext"], variable: "--font-display", axes: ["opsz", "SOFT"] });
// layout: <html className={`${sans.variable} ${display.variable}`}>
```
next/font self-host eder, metrik eşleşen fallback üretir (CLS ≈ 0), preload ekler. Yerel dosya: `next/font/local`.

## Self-host

```css
@font-face {
  font-family: "Satoshi"; src: url("/fonts/Satoshi-Variable.woff2") format("woff2");
  font-weight: 300 900; font-display: swap; unicode-range: U+0000-017F, U+20AC, U+2122, U+20BA; /* ₺ dahil */
}
@font-face { font-family: "Satoshi Fallback"; src: local("Arial"); size-adjust: 104%; ascent-override: 96%; descent-override: 24%; }
body { font-family: "Satoshi", "Satoshi Fallback", system-ui, sans-serif; }
```
- Yalnızca **WOFF2**; variable font 3+ ağırlıkta kazançlı.
- Alt kümeleme (`pyftsubset` / `glyphhanger`): 120KB → 35KB. `₺` (U+20BA) unutma.
- `preload` yalnızca LCP metnindeki 1–2 dosya.
- Fallback metrikleri: `fontaine` / `capsize` hesaplar.

## font-display

- `swap`: gövde için varsayılan. `optional`: sıfır kayma, performans öncelikli siteler.
- İkon fontu kullanma — SVG kullan.

## OpenType güzellikleri

```css
.nums  { font-variant-numeric: tabular-nums slashed-zero; }
.title { font-feature-settings: "ss01", "cv11"; }      /* Inter alternatifleri */
.caps  { font-variant-caps: all-small-caps; letter-spacing: 0.04em; }
.frac  { font-variant-numeric: diagonal-fractions; }    /* tarif sitelerinde 1/2 → ½ */
h1     { font-optical-sizing: auto; }
```
Büyük başlıkta negatif harf aralığı (`-0.02em`), küçük büyük harf etiketlerde pozitif (`0.06em`).

## Bütçe

Toplam font ≤ 100KB, ilk yüklemede ≤ 4 dosya. Kullanılmayan ağırlık/italik yükleme.
Panellerde sistem font yığını (`system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`) 0KB ve iyi bir seçim.
