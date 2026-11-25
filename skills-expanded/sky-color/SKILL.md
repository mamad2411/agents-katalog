---
name: sky-color
description: >-
  Renk mühendisliği: oklch ile algısal olarak düzgün palet ölçekleri üretme, kontrast hesabı
  (WCAG 2.x ve APCA), açık temadan koyu temayı türetme, anlamsal renk rolleri, vurgu renginin
  dozu, gradyanlar (oklch ile çamursuz), renk körlüğü simülasyonu, grafik paletleri ve
  marka renginin UI'a uyarlanması. "Renk paleti oluştur", "kontrast yetmiyor", "dark mode
  renkleri", "renkler soluk/çamurlu" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Renk

## Neden oklch?

`oklch(L C H)`: L = algılanan açıklık (0–1), C = doygunluk, H = ton (0–360). Aynı L değerindeki farklı tonlar
**aynı parlaklıkta görünür** (HSL'de sarı ve mavi aynı "lightness"ta bambaşka görünür). Palet üretimi tahminden çıkar.

## Ölçek üretimi

```css
/* tek tondan 11 adım; L sabit adımlarla, C kenarlarda düşer */
--brand-50:  oklch(0.97 0.02 262);
--brand-100: oklch(0.93 0.04 262);
--brand-200: oklch(0.87 0.07 262);
--brand-300: oklch(0.78 0.11 262);
--brand-400: oklch(0.68 0.15 262);
--brand-500: oklch(0.60 0.18 262);
--brand-600: oklch(0.53 0.19 262);   /* açık temada vurgu */
--brand-700: oklch(0.46 0.17 262);
--brand-800: oklch(0.38 0.14 262);
--brand-900: oklch(0.30 0.10 262);
--brand-950: oklch(0.22 0.07 262);
```
- Çok yüksek C değerleri sRGB dışına taşar (gamut); tarayıcı kırpar → `@media (color-gamut: p3)` ile geniş gamut varyantı isteğe bağlı.
- Araçlar: oklch.com, Huetone, Leonardo (kontrast hedefli ölçek), Radix Colors (hazır, erişilebilir ölçekler).

## Roller (bileşen ham ölçek kullanmaz)

| Rol | Açık | Koyu |
|---|---|---|
| `--bg` | neutral-50 | neutral-950 |
| `--surface` | white | neutral-900 |
| `--border` | neutral-200 | neutral-800 |
| `--fg` | neutral-900 | neutral-50 |
| `--fg-muted` | neutral-600 | neutral-400 |
| `--accent` | brand-600 | brand-400 |
| `--accent-soft` | brand-50 | brand-950 |
| `--danger` | red-600 | red-400 |

## Kontrast

- WCAG 2.x: normal metin ≥ 4.5:1, büyük metin (24px / 18.66px kalın) ≥ 3:1, UI bileşeni/odak halkası ≥ 3:1.
- APCA (WCAG 3 taslağı) daha algısal: gövde metni Lc ≥ 75, büyük başlık Lc ≥ 60 — ince fontlarda daha doğru sonuç.
- Vurgu rengi üzerinde beyaz metin kontrastını kontrol et (çoğu "güzel mavi" 4.5'i tutturamaz → 1 adım koyulaştır).
- Sky `post-edit` hook'u `tokens.css`/`globals.css` düzenlenince temel çiftlerin kontrastını hesaplar.

## Koyu tema türetme

- Ters çevirme değil **yeniden eşleme**: zemin neutral-950 (saf siyah değil), yüzeyler yükseldikçe açılır (900, 850, 800).
- Vurgu rengi bir-iki adım **açık** (400–500), doygunluk biraz düşük — koyu zeminde göz yormasın.
- Gölge yerine kenarlık ve yüzey açıklığı ile derinlik.
- Görseller/illüstrasyonlar için hafif `filter: brightness(.9)` isteğe bağlı.
- Saf beyaz metin yerine neutral-50 (hafif kırık) — halelenme azalır.

## Doz

60-30-10 sezgisi: %60 nötr zemin, %30 yüzey/ikincil, %10 vurgu. Vurgu yalnızca birincil eylem, aktif durum,
odak ve önemli bilgi. Her şey vurgulu olursa hiçbir şey vurgulu değildir.

## Gradyanlar

```css
background: linear-gradient(in oklch 135deg, oklch(0.65 0.2 290), oklch(0.7 0.18 200));
```
`in oklch` ara renklerin grileşmesini (sRGB'deki "çamurlu orta") engeller. Mesh hissi: 2–3 `radial-gradient` üst üste,
düşük opaklık. Metin üstünde gradyan → kontrastı en kötü noktada ölç.

## Renk körlüğü

- Kırmızı/yeşil tek başına durum taşımasın: ikon + metin ekle.
- DevTools → Rendering → "Emulate vision deficiencies" ile test (protanopia, deuteranopia, tritanopia, achromatopsia).
- Grafik paletleri için `sky-dataviz`.

## Hızlı reçeteler

- Rozet arka planı: `color-mix(in oklch, var(--accent) 12%, var(--surface))`, metin `var(--accent)` (koyu temada kontrol et).
- Hover: `oklch(from var(--accent) calc(l - 0.05) c h)`.
- Devre dışı: `--fg-muted` + %50 opaklık değil — opaklık zeminle karışıp kontrastı öldürür; ayrı soluk renk tanımla.
