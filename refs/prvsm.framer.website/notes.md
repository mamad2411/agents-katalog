# Referensi: PRVSM – Event & Music Framer Template
<https://prvsm.framer.website/>  ·  dibaca 2026-11-10 21:49

## Ringkasan
- Viewport dianalisa: 1440px · tinggi halaman 6839px · 415 elemen terlihat
- Bahasa: en · background body `#640fd4`
- Section terdeteksi: 7 · CTA: 1 · gambar: 12

## Tipografi
- Font: Oswald ×90
- Ukuran dominan: 11px, 16px, 18px, 28px, 32px, 76px, 81px, 178px
- Semua ukuran: 11px, 14px, 16px, 18px, 28px, 32px, 76px, 81px, 178px
- Rasio antar-step: ~1.35x
- Weight: 300 ×36, 400 ×35, 500 ×15, 600 ×4 · line-height: 13.2px ×24, 23.4px ×21, 28px ×13, 19.2px ×11, 76px ×7

## Warna
- Teks: #000000 ×51, #ffffff ×38, #640fd4 ×1
- Permukaan (bg): #ffffff ×38, #640fd4 ×3, #000000 ×2
- Kontras gagal (<4.5:1): 0

## Ritme & bentuk
- Gap: 10px ×70, 16px ×13, 32px ×11, 8px ×9, 40px ×3, 4px ×2, 140px ×1, 64px ×1
- Padding: 12px ×21, 16px ×14, 32px ×9, 20px ×6, 64px ×6, 10px ×2, 8px ×2, 151px ×1
- Radius: 0px ×409, 16px ×3, 20px ×1, 10px ×1, 11px ×1
- Shadow: 2 varian
- Container max-width: 720px ×9, 100% ×2

## Layout (urut vertikal)
| y | tinggi | bg | isi | grid | heading |
|---|---|---|---|---|---|
| 151 | 1084 | `transparent` | media | 2 kol × 2 baris · kartu 312px | ARTIST / UVILEN |
| 1235 | 813 | `transparent` | media | 1 kol × 5 baris · kartu 305px | UPCOMING EVENTS / WARSAW, PL - INDUSTRIAL HALL |
| 2048 | 503 | `transparent` | media | - | TICKETS / NEXT TICKETS DROP IN |
| 2552 | 1892 | `transparent` | media | 1 kol × 5 baris · kartu 656px | EVENTS GALLERY |
| 4444 | 720 | `transparent` | media | - | ONE NIGHT.ONE ROOM.ONE SHIFT IN ENERGY. |
| 5164 | 1263 | `transparent` | media | - | LATEST SIGNALS / PRVSM ANNOUNCES BERLIN EDITION AT |
| 6427 | 412 | `transparent` | media | - | ENTER THE SPECTRUM / Where sound, space, and movem |

## CTA
- "REMIX THIS TEMPLATE" · bg `#ffffff` · teks `#000000` · radius 0px · 48×201 · 12px/400

## Gambar
- 12 gambar · rasio dominan: 1.04:1, 2.19:1, 3.18:1
- 1 gambar tanpa alt (cacat a11y — jangan ditiru)

## Aksesibilitas
- Heading: 45 · urutan: h1, h1, h1, h1, h2, h2, h3, h3
- Target <24px: 6 (contoh: "READ MORE")

## Responsive (diukur di 4 lebar)
- 360px: OK · 43 elemen keluar layar
- 768px: OK · 12 elemen keluar layar
- 1024px: OK · 13 elemen keluar layar
- 1440px: OK · 8 elemen keluar layar

## Audit otomatis (axe-core, WCAG 2.1 A/AA)
- 1 jenis pelanggaran · 8 node
  - [serious] color-contrast ×8 — Elements must meet minimum color contrast ratio thresholds

## Motion (terukur)
- Durasi: 0.2s ×8, 0.3s ×4
- Easing: ease-in-out ×12

## Performa (lab, bukan field)
- TTFB 1914ms · FCP 3196ms · LCP 3880ms · CLS 0.009
- Ambang: LCP ≤2500ms, CLS ≤0.1. Angka lab bisa lebih baik dari pengguna nyata.

## Prinsip yang bisa dipakai
- Skala tipe 1.35x → bangun token dari skala ini, jangan pilih ukuran per komponen.
- Palet: 1 warna aksi dominan + netral; permukaan dominan `#640fd4`.
- Ambil grid, density, ritme spacing, dan hierarki. JANGAN copy teks, logo, atau aset.

## Bukti visual
- `/Users/chaali0324/.agents/refs/prvsm.framer.website/desktop-hero.png` (desktop-hero)
- `/Users/chaali0324/.agents/refs/prvsm.framer.website/desktop.png` (desktop)
- `/Users/chaali0324/.agents/refs/prvsm.framer.website/mobile.png` (mobile)
