---
name: sky-css-modern
description: >-
  Modern CSS ile JS'siz büyü: container queries, :has() seçicisi, cascade layers, subgrid,
  anchor positioning, scroll-driven animasyonlar, @starting-style ile giriş/çıkış animasyonu,
  oklch/color-mix/light-dark renk fonksiyonları, CSS nesting, text-wrap balance/pretty,
  field-sizing, scroll-snap carousel ve interpolate-size. "Bunu CSS ile yapabilir miyiz",
  "modern CSS", "JS'siz", "carousel", "scroll animasyonu" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Modern CSS

Felsefe: JS ile yazacağın her UI davranışından önce "bunu CSS yapabilir mi?" sor. Daha hızlı, daha az
hata, daha az bundle. Destek durumunu kontrol et ve **ilerlemeli geliştirme** uygula (`@supports`).

## Container queries

```css
.card-list { container-type: inline-size; }
@container (min-width: 480px) { .card { grid-template-columns: 120px 1fr; } }
```
Bileşen ekrana değil **kapsayıcısına** göre değişir → aynı kart sidebar'da dikey, ana alanda yatay.
`cqi` birimiyle kapsayıcıya göre akışkan tipografi.

## :has() — ebeveyn seçici

```css
.field:has(input:user-invalid) { --ring: var(--danger); }       /* hatalı alanın kutusu */
.card:has(img) { padding-top: 0; }                               /* görselli kartlar */
body:has(dialog[open]) { overflow: hidden; }                     /* modal açıkken kaydırma kilidi */
.grid:has(> :nth-child(5)) { grid-template-columns: repeat(3, 1fr); } /* öğe sayısına göre düzen */
```

## Cascade layers

```css
@layer reset, tokens, base, components, utilities;
@layer components { .btn { … } }
```
Özgüllük savaşları biter; `!important`a gerek kalmaz. Üçüncü parti CSS'i `@import url(lib.css) layer(vendor);`.

## Subgrid

```css
.cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); }
.card  { display: grid; grid-row: span 3; grid-template-rows: subgrid; }
```
Fiyat tablolarında butonların aynı hizada durması — insanların fark etmeden sevdiği şey.

## Anchor positioning

```css
.trigger { anchor-name: --menu; }
.menu { position: fixed; position-anchor: --menu; top: anchor(bottom); left: anchor(left);
        position-try-fallbacks: flip-block, flip-inline; }
```
Tooltip/menü konumlandırma için Floating UI'nin CSS karşılığı; desteklenmiyorsa Floating UI fallback.

## Scroll-driven animasyonlar

```css
@keyframes reveal { from { opacity: 0; translate: 0 24px; } }
.section { animation: reveal linear both; animation-timeline: view(); animation-range: entry 0% cover 30%; }
.progress-bar { animation: grow linear; animation-timeline: scroll(root); transform-origin: left; }
@keyframes grow { from { scale: 0 1; } }
@media (prefers-reduced-motion: reduce) { .section, .progress-bar { animation: none; } }
```
Okuma ilerleme çubuğu, kaydırınca beliren bölümler, paralaks — **sıfır JS**, ana thread dışında.

## Giriş/çıkış animasyonu (display dahil)

```css
.toast { transition: opacity .2s, translate .2s, display .2s allow-discrete; }
.toast[hidden] { opacity: 0; translate: 0 8px; display: none; }
@starting-style { .toast:not([hidden]) { opacity: 0; translate: 0 8px; } }
```

## Renk fonksiyonları

```css
:root { --accent: oklch(0.58 0.2 262); }
.btn:hover { background: oklch(from var(--accent) calc(l - 0.06) c h); }   /* göreli renk */
.badge { background: color-mix(in oklch, var(--accent) 14%, transparent); }
:root { color-scheme: light dark; --bg: light-dark(#fbfbfa, #0f0f12); }    /* tek satır dark mode */
```
oklch algısal olarak düzgün: palet üretimi kolay (bkz. `sky-color`).

## Tipografi ve form ince ayarları

- `text-wrap: balance` başlıklarda, `pretty` paragraflarda.
- `field-sizing: content` → textarea içeriğe göre büyür, JS autosize'a gerek yok.
- `accent-color: var(--accent)` → checkbox/radio/range marka renginde.
- `font-variant-numeric: tabular-nums` sayı sütunlarında.

## Carousel (JS'siz)

```css
.carousel { display: grid; grid-auto-flow: column; grid-auto-columns: 85%; gap: 12px;
            overflow-x: auto; scroll-snap-type: x mandatory; overscroll-behavior-x: contain; scrollbar-width: none; }
.carousel > * { scroll-snap-align: start; }
```
Yeni tarayıcılarda `::scroll-button()` ve `::scroll-marker` ile ok ve noktalar da CSS'te (destek kontrolü).

## Diğer

- Native nesting (`&:hover`, `& .icon`).
- `@property` ile animasyonlanabilir özel özellik (dönen gradyan kenarlık).
- `interpolate-size: allow-keywords` → `height: auto`ya animasyon (akordiyon).
- `scrollbar-gutter: stable` → modal açılınca sayfa zıplamasın.
- `overscroll-behavior: contain` → modal içi kaydırma sayfaya taşmasın.

## Destek stratejisi

`@supports (animation-timeline: view())` ile koşullu; desteklenmeyen yerde içerik **görünür ve
kullanılabilir** kalmalı. Baseline "Widely available" özellikler güvenli.
