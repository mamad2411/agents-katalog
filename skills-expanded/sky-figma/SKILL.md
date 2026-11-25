---
name: sky-figma
description: >-
  Figma ile koda köprü: tasarım dosyasını okuma (Dev Mode, ölçüler, değişkenler), Figma
  Variables ↔ CSS token senkronu (Tokens Studio / Style Dictionary), Auto Layout'u flex/grid'e
  çevirme, bileşen ve varyant eşlemesi (Code Connect), Figma MCP ile tasarımdan kod üretme,
  tasarımı birebir uygulama ve sapma kontrolü, handoff kontrol listesi ve tasarımcıyla iş
  akışı. "Figma tasarımını koda dök", "pixel perfect", "token'ları Figma'dan al" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Figma → Kod

## Okuma sırası

1. **Değişkenler/stiller**: renk, tip, boşluk, yarıçap → token'lar var mı? (Yoksa tasarımcıyla kısa bir token seansı.)
2. **Bileşenler**: ana bileşenler ve varyantları (Button: variant × size × state) → mevcut kod bileşenleriyle eşle.
3. **Ekranlar**: breakpoint'ler (mobil/masaüstü kareleri), durumlar (boş/hata/yükleniyor kareleri var mı?).
4. **Prototip bağlantıları**: geçişler ve akış.
Eksik durumları (hata, boş, uzun metin) uygulamaya başlamadan **listele ve sor** — en sık sapma kaynağı.

## Auto Layout → CSS

| Figma | CSS |
|---|---|
| Auto layout yatay/dikey | `display: flex; flex-direction: row/column` |
| Gap | `gap` |
| Padding | `padding` |
| Hug contents | `width: fit-content` / doğal |
| Fill container | `flex: 1` / `width: 100%` |
| Fixed | sabit boyut — gerçekten gerekli mi sorgula (responsive) |
| Space between | `justify-content: space-between` |
| Wrap | `flex-wrap: wrap` |
| Grid (yeni) | `display: grid` |
Ölçüleri token'a yuvarla (13px → `--space-3` 12px); tasarımcı token dışı değer kullandıysa not düş.

## Token senkronu

- Figma Variables → **Tokens Studio** veya Figma REST API → JSON → **Style Dictionary** → `tokens.css` + Tailwind `@theme`.
- Mod'lar (Light/Dark) → CSS'te iki tema bloğu.
- CI'da token JSON değişince CSS yeniden üretilsin; kodda elle token düzenleme yok (tek kaynak).

## Figma MCP / Dev Mode MCP

Figma'nın MCP sunucusu seçili kareyi kod bağlamı olarak verebilir (yapı, değişkenler, görseller). Kullanırken:
- Üretilen kodu **projenin bileşenleriyle** yeniden yaz (ham `div` yığınını kabul etme).
- Değişken adlarını token'larla eşle; mutlak konumlandırmayı flex/grid'e çevir.
- Code Connect tanımlıysa Figma bileşeni doğrudan kod bileşeni adıyla gelir — kuruluma değer.

## Sadakat kontrolü

- Tarayıcıda tasarımla yan yana karşılaştır (aynı genişlikte); **Pixel Perfect / PerfectPixel** eklentisi ile üst üste bindir.
- Kontrol: boşluk ritmi, tipografi (satır yüksekliği, harf aralığı), hizalama, renkler (token), köşe yarıçapları, gölgeler.
- Tasarımda olmayan ama gerçek dünyada olan: uzun Türkçe metin, 0/1/100 öğe, küçük ekran, büyük font ayarı → tasarımcıya göster.
- "Piksel mükemmel" ≠ "sabit piksel": responsive davranışta tasarımın **niyetini** koru.

## Handoff kontrol listesi (tasarımcıdan beklenecekler)

- [ ] Token'lar (değişkenler) tanımlı, bileşenler değişken kullanıyor
- [ ] Mobil + masaüstü kareleri (ve gerekiyorsa tablet)
- [ ] Durumlar: hover, focus, disabled, loading, boş, hata, uzun metin
- [ ] Dark mode (gerekiyorsa)
- [ ] Görseller export ayarlı (SVG ikonlar, 2x raster), illüstrasyonlar SVG
- [ ] Etkileşim notları (animasyon süresi/easing, geçiş türü)
- [ ] Metinler son hali (Türkçe, sen/siz kararı)

## İş akışı

Tasarımcıyla haftalık 15 dk "uygulanmış haliyle tasarım" turu; sapmaları birlikte karara bağla (kod mu
tasarım mı güncellensin). Storybook/`/design` sayfasını tasarımcıya aç (bkz. `sky-design-system`).
