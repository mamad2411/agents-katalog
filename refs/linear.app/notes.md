# Referensi: Linear – The system for product development
<https://linear.app>  ·  dibaca 2026-11-11 17:33

## Ringkasan
- Viewport dianalisa: 1440px · tinggi halaman 9960px · 2219 elemen terlihat
- Bahasa: en · background body `#08090a`
- Section terdeteksi: 10 · CTA: 12 · gambar: 5

## Tipografi
- Font: Inter Variable ×401, Berkeley Mono ×184
- Ukuran dominan: 10px, 11px, 12px, 13px, 14px, 15px, 16px, 18px, 24px
- Semua ukuran: 10px, 11px, 12px, 13px, 14px, 15px, 16px, 18px, 20px, 24px, 32px, 48px, 64px, 72px
- Rasio antar-step: ~1.23x
- Weight: 400 ×442, 510 ×113, 500 ×18, 590 ×8, 300 ×4 · line-height: 24px ×207, 14px ×90, 19.5px ×86, 16px ×72, 16.8px ×42

## Warna
- Teks: #8a8f98 ×149, #62666d ×116, #d0d6e0 ×111, #e2e4e7 ×81, #f79ce0 ×41, #f7bf8b ×22, #f7f8f8 ×20, #ffdf9f ×10
- Permukaan (bg): #0f1011 ×34, #08090a ×6, #161718 ×4, #4ea7fc ×4, #eb5757 ×3, #e5e5e6 ×2, #090a0b ×1, #101112 ×1
- Kontras gagal (<4.5:1): 0

## Ritme & bentuk
- Gap: 8px ×90, 6px ×64, 4px ×64, 12px ×17, 2px ×11, 10px ×5, 16px ×4, 11px ×4
- Padding: 32px ×85, 4px ×54, 6px ×49, 8px ×48, 12px ×38, 7px ×22, 14px ×18, 36px ×15
- Radius: 0px ×1968, 9999px ×82, 8px ×30, 50% ×28, 4px ×22, 12px ×19
- Shadow: 4 varian
- Container max-width: 100% ×40, 1436px ×8, 541.566px ×4, 566.438px ×4, 368px ×3

## Layout (urut vertikal)
| y | tinggi | bg | isi | grid | heading |
|---|---|---|---|---|---|
| 271 | 1024 | `transparent` | media | - | The product development system for teams and agent |
| 1596 | 144 | `transparent` | teks | - | - |
| 1876 | 468 | `transparent` | media | - | - |
| 2546 | 1226 | `transparent` | media | 1 kol × 5 baris · kartu 300px | Intakeand integrations |
| 3782 | 1229 | `transparent` | media | - | Planningand monitoring |
| 5021 | 1232 | `transparent` | media | 4 kol × 1 baris · kartu 400px | AI andautomations |
| 6263 | 1220 | `transparent` | media, form | 2 kol × 4 baris · kartu 1344px | Build, review,and ship |
| 7644 | 422 | `transparent` | teks | 4 kol × 1 baris · kartu 272px | Changelog |
| 8226 | 564 | `transparent` | media | - | - |
| 9014 | 228 | `transparent` | teks | - | Built for the future. Available today. |

## CTA
- "Product" · bg `#000000` · teks `#8a8f98` · radius 9999px · 32×72 · 13px/400
- "Resources" · bg `#000000` · teks `#8a8f98` · radius 9999px · 32×89 · 13px/400
- "Sign up" · bg `#e5e5e6` · teks `#08090a` · radius 9999px · 32×73 · 13px/510
- "Linear" · bg `#000000` · teks `#ffffff` · radius 8px · 28×97 · 13px/400
- "Pulse" · bg `#000000` · teks `#d0d6e0` · radius 8px · 28×208 · 13px/510
- "Inbox" · bg `#000000` · teks `#d0d6e0` · radius 8px · 28×208 · 13px/510

## Gambar
- 5 gambar · rasio dominan: 1.79:1, 1:1
- 1 gambar tanpa alt (cacat a11y — jangan ditiru)

## Aksesibilitas
- Heading: 15 · urutan: h1, h3, h4, h2, h2, h2, h2, h2
- Target <24px: 3 (contoh: "Privacy")

## Responsive (diukur di 4 lebar)
- 360px: OK · 453 elemen keluar layar
- 768px: OK · 829 elemen keluar layar
- 1024px: OK · 598 elemen keluar layar
- 1440px: OK · 222 elemen keluar layar

## Audit otomatis (axe-core, WCAG 2.1 A/AA)
- 1 jenis pelanggaran · 15 node
  - [serious] color-contrast ×15 — Elements must meet minimum color contrast ratio thresholds

## Motion (terukur)
- Durasi: 0.1s ×234, 0.16s ×35, 0.16s, 0.16s ×26, 0.4s ×19, 0.15s ×10
- Easing: cubic-bezier(0.25, 0.46, 0.45, 0.94) ×231, cubic-bezier(0.25, 0.46, 0.45, 0.94), cubic-bezier(0.25, 0.46, 0.45, 0.94) ×34, ease-out ×19, cubic-bezier(0.32, 0.72, 0, 1) ×10

## Performa (lab, bukan field)
- TTFB 1030ms · FCP 2088ms · LCP 8756ms · CLS 0
- Ambang: LCP ≤2500ms, CLS ≤0.1. Angka lab bisa lebih baik dari pengguna nyata.

## Prinsip yang bisa dipakai
- Skala tipe 1.23x → bangun token dari skala ini, jangan pilih ukuran per komponen.
- Palet: 1 warna aksi dominan + netral; permukaan dominan `#08090a`.
- Ambil grid, density, ritme spacing, dan hierarki. JANGAN copy teks, logo, atau aset.

## Bukti visual
- `/Users/chaali0324/.agents/refs/linear.app/desktop-hero.png` (desktop-hero)
- `/Users/chaali0324/.agents/refs/linear.app/desktop.png` (desktop)
- `/Users/chaali0324/.agents/refs/linear.app/mobile.png` (mobile)
