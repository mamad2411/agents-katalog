---
name: sky-mobile-ux
description: >-
  Mobil web UX: başparmak bölgesi ve alt navigasyon, bottom sheet ve kaydırma jestleri, safe
  area (çentik/home indicator), sanal klavye ile viewport sorunları (dvh, visualViewport),
  yapışkan CTA, dokunma hedefleri ve geri bildirim, input türleri ve otomatik doldurma, mobil
  form akışı, pull-to-refresh, yatay kaydırmalı listeler, iOS/Android farkları ve gerçek cihaz
  testi. "Mobilde kötü görünüyor", "telefonda kullanımı zor", "klavye ekranı kapatıyor"
  dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Mobil UX

Kullanıcıların çoğu telefonda. Mobil "küçültülmüş masaüstü" değil, **başparmakla kullanılan** ayrı bir bağlam.

## Başparmak bölgesi

- Ekranın alt üçte biri kolay, üst köşeler zor. Birincil eylemler **altta**: yapışkan alt çubuk, alt navigasyon, bottom sheet.
- Alt navigasyon: 3–5 öğe, ikon + etiket (yalnızca ikon değil), aktif öğe belirgin; içerik kaydırınca gizlenmesi isteğe bağlı.
- Yıkıcı eylemleri başparmağın en rahat yerine koyma.

## Safe area ve viewport

```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
```
```css
.bottom-bar { padding-bottom: max(12px, env(safe-area-inset-bottom)); }
.full { min-height: 100dvh; }        /* 100vh adres çubuğu yüzünden taşar; dvh dinamik */
```
- `svh` (en küçük), `lvh` (en büyük), `dvh` (dinamik) farkını bil; tam ekran kahraman bölüm için `svh` zıplamaz.
- Sanal klavye: iOS'ta `position: fixed` öğeler klavyeyle kayar → `visualViewport` olayıyla alt çubuğu klavyenin üstüne taşı veya input odaklıyken gizle.
- `interactive-widget=resizes-content` (viewport meta) Android Chrome'da düzeni klavyeye göre küçültür.

## Bottom sheet

- Mobilde modal yerine alttan açılan sayfa: tutamak çizgisi, aşağı kaydırarak kapatma, yarım/tam yükseklik durakları.
- Kütüphane: **Vaul** (shadcn Drawer) — jest fizik ve erişilebilirlik hazır.
- Masaüstünde aynı içerik dialog olarak (`useMediaQuery` ile Drawer/Dialog değiştir).

## Dokunma

- Hedef ≥ 44×44px (görünmez padding ile), öğeler arası ≥ 8px.
- `:active` durumu (basma geri bildirimi) — mobilde hover yok; `@media (hover: hover)` ile hover stillerini sınırla (yapışkan hover sorunu).
- `-webkit-tap-highlight-color: transparent` + kendi `:active` stilin.
- Uzun basma menüsü (context menu) yalnızca gelişmiş eylemler için; görünür alternatif olsun.
- Kaydırarak eylem (sola kaydır → sil/arşivle) liste öğelerinde; erişilebilir menü alternatifiyle.

## Formlar

- Doğru klavye: `type="email"`, `type="tel"`, `inputMode="numeric"` (kod/PIN), `inputMode="decimal"` (tutar), `enterKeyHint="next|send|search"`.
- `autocomplete`: `name`, `tel-national`, `email`, `street-address`, `postal-code`, `one-time-code` (SMS kodu otomatik dolar — insanlar bayılır).
- Font boyutu ≥ 16px inputlarda (iOS daha küçükte zoom yapar).
- Tek sütun, etiket üstte, hata hemen altta; ileri tuşuyla sonraki alana.
- Uzun formu adımlara böl (bkz. `sky-forms`); ilerleme çubuğu üstte.
- Tarih/saat için native seçiciler (bkz. `sky-date-time`).

## Kaydırma

- Yatay kaydırmalı kart listeleri: `scroll-snap`, sonraki kartın bir kısmı görünsün (devamı olduğunu ima eder).
- `overscroll-behavior: contain` modal/sheet içinde.
- Pull-to-refresh yalnızca akış ekranlarında; PWA'da native davranışı bozmadan.
- Yapışkan başlık ince olsun; içerik alanını yemesin.

## Performans hissi

- Dokunuşa 100ms içinde görsel yanıt (`:active`, iyimser UI).
- Sayfa geçişlerinde iskelet; ağır JS'i mobilde ertele (INP, bkz. `sky-perf`).
- Görseller mobil boyutta (`sizes`).

## iOS / Android farkları

- iOS: geri jesti kenardan, rubber-band kaydırma, `position: fixed` + klavye tuhaflıkları, input zoom (16px kuralı), PWA push yalnızca ana ekranda.
- Android: donanım/jest geri tuşu → modal açıkken geri tuşu modalı kapatmalı (history state ile).
- Her ikisinde de sistem dark mode ve yazı boyutu tercihine saygı.

## Test

Gerçek cihaz (en az bir iPhone + bir orta segment Android), Chrome DevTools cihaz modu yetmez. Kontrol:
375px ve 320px genişlik, yatay mod, klavye açıkken form, yavaş 4G, büyük yazı boyutu ayarı.
