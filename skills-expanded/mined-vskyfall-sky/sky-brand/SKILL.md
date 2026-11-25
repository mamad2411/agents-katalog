---
name: sky-brand
description: >-
  Markadan tasarım sistemine: marka kişiliği (3 sıfat), logodan renk paleti türetme, tip
  eşleşmesi, ses tonu, logo kullanım kuralları, favicon/app ikonu/OG görsel seti, sosyal medya
  şablonları, marka sayfası (brand guidelines) ve logo yoksa hızlı wordmark üretimi. "Marka
  kimliği", "logomuza göre renk", "favicon seti", "marka rehberi", "yeni marka" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Marka

## 1. Kişilik: 3 sıfat

Her şey buradan türer. Örnek: Klinik → *güven veren, sakin, modern*. Kuaför → *şık, sıcak, cesur*.
Oyun stüdyosu → *oyunbaz, enerjik, tuhaf*. Her tasarım kararını "bu üç sıfata uyuyor mu?" diye test et.

| Sıfat | Görsel karşılığı |
|---|---|
| Güven veren | mavi/yeşil tonlar, bol beyaz alan, düzgün grid, orta ağırlık font |
| Sıcak | turuncu/terrakota, yuvarlak köşeler (12–16px), insan fotoğrafları |
| Lüks | koyu zemin, ince serif, geniş harf aralığı, tek altın vurgu |
| Enerjik | doygun renk, büyük tipografi, eğik açılar, hareket |
| Teknik | mono font detayları, ince çizgiler, keskin köşeler, koyu tema |

## 2. Logodan palet

1. Logonun ana rengini al → oklch'ye çevir (bkz. `sky-color`).
2. Aynı ton (h) ile 11 adımlı ölçek üret (50–950); UI'da vurgu olarak 600 (açık tema) / 400 (koyu tema).
3. Nötrler: saf gri değil, vurgu tonundan çok az renk alan gri (`c ≈ 0.01`) → palet bütünlüklü görünür.
4. İkincil renk gerekiyorsa ton çemberinde ~150–180° karşısı, düşük kullanım.
5. Anlamsal renkler (başarı/hata) markayla çakışıyorsa kaydır (logo kırmızıysa hata rengi daha koyu/bordo).

## 3. Tipografi ve ses

- Font eşleşmesi kişiliğe göre (bkz. `sky-web-fonts` tarif tablosu).
- Ses tonu 3 cümlelik kural: "Biz … gibi konuşuruz, … gibi konuşmayız." + sen/siz kararı (bkz. `sky-ux-writing`).

## 4. Logo yoksa: hızlı wordmark

Karakterli bir fontta marka adı + tek özgün detay (bir harfin rengi, nokta yerine şekil, özel bitişik harf).
SVG olarak çiz, `currentColor` ile tema uyumlu. Simge için adın ilk harfi + basit geometrik form.
Gerçek logo için bir tasarımcıya yönlendir — bu geçici ama düzgün bir başlangıçtır.

## 5. Varlık seti (insanların "profesyonel" dediği kısım)

```
public/
  favicon.ico (32), icon.svg (koyu mod uyumlu: @media prefers-color-scheme içinde), apple-icon.png (180)
  icons/192.png, 512.png, maskable-512.png      # PWA
  og.png (1200×630)                             # paylaşım kartı — logo + slogan + marka rengi
  logo.svg, logo-mark.svg, logo-white.svg
```
- Next.js: `app/icon.svg`, `app/apple-icon.png`, `app/opengraph-image.tsx` (dinamik OG, sayfa başlığıyla).
- SVG favicon'da koyu mod: `<style>@media (prefers-color-scheme: dark){ path{fill:#fff} }</style>`.
- Sosyal medya: profil görseli (daire içinde okunur simge), kapak görselleri (X 1500×500, LinkedIn 1584×396).

## 6. Kullanım kuralları

Logo etrafında boşluk (logo yüksekliğinin %50'si), minimum boyut (24px simge, 80px wordmark), açık/koyu zemin
versiyonları, yasaklar (gerdirme, gölge, döndürme, kontrastsız zemin).

## 7. Marka sayfası

`/marka` veya `/brand` route'u (veya `docs/brand.md`): logo indirme (SVG/PNG), renkler (hex + oklch, kopyala butonu),
fontlar, ses tonu, örnek kullanımlar. Basın ve ortaklar için çok kullanışlı; ekibin tutarlılığını korur.

## 8. Token'a dönüştür

Palet ve fontlar `tokens.css` + Tailwind `@theme`'e (bkz. `sky-ui-craft`, `sky-design-system`). Marka = token'lar;
bileşen kodunda marka rengi yazılmaz.
