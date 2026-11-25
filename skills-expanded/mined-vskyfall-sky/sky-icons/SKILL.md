---
name: sky-icons
description: >-
  İkon sistemi: ikon seti seçimi (Lucide, Phosphor, Tabler, Heroicons, Iconoir), tek set
  kuralı, boyut ve çizgi kalınlığı ölçeği, optik hizalama ve metinle hizalama, ikon butonları
  ve erişilebilirlik, özel ikon çizme kuralları (24px grid), SVGO optimizasyonu, sprite ve
  ağaç sallama, animasyonlu ikonlar ve marka/ödeme logoları. "İkon seç", "ikonlar uyumsuz",
  "özel ikon", "ikon butonu" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · İkonlar

## Set seçimi

| Set | Karakter |
|---|---|
| **Lucide** | temiz, nötr, 1500+, shadcn varsayılanı (varsayılan) |
| **Phosphor** | 6 ağırlık (thin→fill, duotone), sıcak ve esnek — marka karakteri için harika |
| **Tabler** | 5000+, teknik paneller |
| **Heroicons** | Tailwind ekibinden, outline/solid, az ama çok düzgün |
| **Iconoir / Remix** | alternatif karakterler |

**Tek set kuralı**: farklı setleri karıştırma (çizgi kalınlığı, köşe yarıçapı, stil farkı göze batar).
Eksik ikon varsa aynı setin kurallarıyla çiz.

## Ölçek

| Kullanım | Boyut | Çizgi |
|---|---|---|
| Metin içi / küçük buton | 16px | 1.75–2 |
| Varsayılan UI | 20px | 1.75 |
| Navigasyon, kart başlığı | 24px | 1.5–1.75 |
| Boş durum / özellik | 40–48px | 1.25–1.5 |
Büyüdükçe çizgiyi incelt (optik denge). Lucide: `<Calendar size={20} strokeWidth={1.75} />`; ya da global CSS ile `stroke-width`.

## Metinle hizalama

```css
.icon-text { display: inline-flex; align-items: center; gap: 0.5em; }
.icon-text svg { width: 1.25em; height: 1.25em; flex-shrink: 0; }
```
`em` tabanlı boyut → ikon metin boyutuyla ölçeklenir. Optik ortalama: bazı ikonlar (oynat ▶) geometrik
merkezde sola kaymış görünür → 1px kaydır.

## Renk

`currentColor` — ikon metin rengini alır; durum ikonları anlamsal token'lar. İkon tek başına anlam taşımasın
(renk körlüğü, bkz. `sky-color`).

## Erişilebilirlik

- Dekoratif ikon (metnin yanında): `aria-hidden="true"`.
- Yalnızca ikon olan buton: `<button aria-label="Düzenle"><Pencil aria-hidden /></button>` + tooltip ("Düzenle · E").
- Anlam taşıyan tek başına ikon (durum): `role="img" aria-label="Onaylandı"`.
- İkon butonu dokunma hedefi ≥ 40–44px (ikon 20px + padding).

## Özel ikon çizimi

- 24×24 grid, 2px güvenli kenar boşluğu, setin çizgi kalınlığı ve köşe yarıçapı, `stroke-linecap/linejoin: round` (Lucide uyumu).
- Figma'da çiz → SVG export → **SVGO** (`svgo --multipass`) → `fill="none" stroke="currentColor"` kalsın, sabit renkler silinsin.
- React bileşeni: SVGR veya Lucide'ın `createLucideIcon` ile aynı API.

## Performans

- Tekil import (`import { Calendar } from "lucide-react"`) — ağaç sallanır. Tüm seti dinamik import etme.
- Çok sayıda tekrar eden ikon (tablo satırları) → SVG sprite (`<use href="#icon-calendar">`) DOM'u küçültür.
- İkon fontu kullanma (FOIT, erişilebilirlik, bulanıklık).

## Animasyonlu ikonlar

Hover'da küçük hareket (zil sallanır, ok ilerler) — `lucide-animated` / `motion` ile; yalnızca etkileşimde ve
reduced-motion'da kapalı. Başarı ✓ çizilerek belirir (stroke-dashoffset animasyonu) — küçük ama sevilen detay.

## Marka ve ödeme logoları

Sosyal medya/marka logoları ikon setinde olmayabilir (Lucide marka ikonlarını kaldırdı) → **Simple Icons**.
Ödeme logoları (Visa, Mastercard, Troy, iyzico) resmi varlıklardan, marka kurallarına uygun.
