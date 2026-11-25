---
name: sky-perf
description: >-
  Web performansı: Core Web Vitals (LCP, INP, CLS), bundle boyutu ve kod bölme, görsel ve
  font optimizasyonu, React render maliyeti, önbellekleme, sunucu yanıt süresi ve ölçüm
  (Lighthouse, Web Vitals, performance trace). Site yavaşsa, bundle büyükse, "hızlandır",
  "optimize et", "Lighthouse puanı düşük" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Performans

## Kural: önce ölç

Tahmine göre optimizasyon yapma. Sırayla:
1. **Lighthouse** (mobil, yavaş 4G simülasyonu) veya Chrome DevTools performance trace.
2. **Bundle analizi:** Next `@next/bundle-analyzer`, Vite `rollup-plugin-visualizer`.
3. **React Profiler** ile gereksiz render'lar.
4. Değişiklikten sonra aynı ölçümü tekrarla; önce/sonra rakamlarını raporla.

## Hedefler

| Metrik | İyi | Başlıca sebepler |
|---|---|---|
| LCP | < 2.5s | büyük hero görseli, render-blocking CSS/font, yavaş TTFB, istemci tarafı render |
| INP | < 200ms | uzun JS görevleri, büyük re-render, ana thread'de ağır iş |
| CLS | < 0.1 | boyutsuz görsel/iframe, geç yüklenen font, sonradan eklenen banner |
| TTFB | < 800ms | yavaş sorgu, önbelleksiz SSR, uzak bölge |

## LCP

- LCP öğesi (genelde hero görseli/başlık) için `fetchpriority="high"`, Next'te `priority`; lazy **değil**.
- Görseller AVIF/WebP, doğru `sizes` ile responsive; hero ≤ ~200KB.
- Kritik CSS küçük; üçüncü parti scriptler `defer`/`async` veya `next/script strategy="lazyOnload"`.
- Fontlar: `next/font` veya self-host + `font-display: swap` + `preload` (yalnızca 1–2 dosya), alt küme (Türkçe için latin + latin-ext).
- İçerik sunucuda render edilsin (SSR/SSG/ISR).

## INP

- Uzun görevleri böl: `await scheduler.yield()` / `setTimeout(0)`, ağır hesapları Web Worker'a.
- Büyük listelerde sanallaştırma (`@tanstack/react-virtual`) — 100+ satırdan itibaren.
- Yazarken filtreleme: `useDeferredValue` veya `useTransition`.
- Olay işleyicide yalnızca görsel geri bildirimi hemen ver, ağır işi ertele.
- Gereksiz re-render: state'i kullanıldığı yere indir, context'i böl, gerekirse `memo`. React Compiler etkinse elle memo'ya gerek azalır.

## CLS

- Tüm `img`/`video`/`iframe` öğelerinde `width/height` veya `aspect-ratio`.
- Sonradan yüklenen içerik için yer ayır (iskelet ekran aynı boyutta).
- Font değişimi kaymasını `size-adjust` / `next/font` otomatik fallback ile azalt.
- Banner/çerez bildirimi içeriği itmesin (overlay olarak).

## Bundle

- Route bazlı kod bölme otomatik (Next/Vite); ağır ve nadir kullanılan bileşenler `dynamic()` / `React.lazy`.
- Ağır kütüphaneleri sorgula: `moment` → `date-fns`/`Intl`, `lodash` → tekil import veya native,
  ikon setlerini tekil import.
- `"use client"` sınırını aşağı it — istemci bundle'ı küçülür.
- Modern tarayıcı hedefi (`browserslist`), gereksiz polyfill yok.

## Önbellekleme & ağ

- Statik varlıklar hash'li ad + `Cache-Control: public, max-age=31536000, immutable`.
- HTML/veri: `stale-while-revalidate`; Next'te `revalidate` / cache tag'leri.
- Kritik üçüncü parti origin'lere `preconnect`.
- API: gereksiz istekleri birleştir, sayfalama, sıkıştırma (br/gzip).
- Veritabanı: bkz. `sky-data` (indeks, N+1).

## Görseller kontrol listesi

- [ ] Doğru format (AVIF/WebP), doğru boyut (2x'ten büyük değil)
- [ ] `loading="lazy"` ekran dışındakilerde, `decoding="async"`
- [ ] Boyutlar/aspect-ratio tanımlı
- [ ] SVG ikonlar sprite veya bileşen; büyük PNG ikon yok

## Rapor biçimi

```
Metrik   Önce    Sonra
LCP      3.8s    1.9s
INP      310ms   140ms
CLS      0.18    0.02
JS (gz)  412KB   188KB
Değişiklikler: …
```
