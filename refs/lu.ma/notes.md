# Referensi: Luma
<https://lu.ma>  ·  dibaca 2026-11-12 16:17

## Ringkasan
- Viewport dianalisa: 1440px · tinggi halaman 2909px · 338 elemen terlihat
- Bahasa: en · background body `#000000`
- Section terdeteksi: 1 · CTA: 2 · gambar: 20

## Tipografi
- Font: -apple-system ×75
- Ukuran dominan: 13px, 14px, 16px, 20px, 80px
- Semua ukuran: 13px, 14px, 16px, 18px, 20px, 40px, 80px
- Rasio antar-step: ~2.62x
- Weight: 500 ×38, 400 ×33, 600 ×4 · line-height: 20.8px ×33, 18.2px ×8, 21px ×7, 73.6px ×6, 30px ×6

## Warna
- Teks: #151515 ×66, #ffffff ×7, #ac894f ×1, #353535 ×1
- Permukaan (bg): #ffffff ×25, #151515 ×1
- Kontras gagal (<4.5:1): 0

## Ritme & bentuk
- Gap: 12px ×5, 8px ×4, 16px ×4, 20px ×2, 4px ×1, 40px ×1
- Padding: 8px ×55, 16px ×20, 4px ×17, 12px ×13, 20px ×9, 9px ×6, 10px ×4, 14px ×3
- Radius: 0px ×270, 12px ×23, 11px ×23, 8px ×12, 24px ×3, 16px ×3
- Shadow: 1 varian
- Container max-width: 100% ×4, 450px ×2, 960px ×2, 600px ×1

## Layout (urut vertikal)
| y | tinggi | bg | isi | grid | heading |
|---|---|---|---|---|---|
| 193 | 274 | `transparent` | media | - | - |

## CTA
- "Skip to Content" · bg `#ffffff` · teks `#151515` · radius 8px · 40×136 · 16px/400
- "Create Your First Event" · bg `#151515` · teks `#ffffff` · radius 100px · 45×224 · 18px/500

## Gambar
- 20 gambar · rasio dominan: 1:1
- 6 gambar tanpa alt (cacat a11y — jangan ditiru)

## Aksesibilitas
- Heading: 7 · urutan: h1, h1, h2, h2, h2, h2, h3
- Target <24px: 5 (contoh: "run clubs")

## Responsive (diukur di 4 lebar)
- 360px: OK · 77 elemen keluar layar
- 768px: OK · 0 elemen keluar layar
- 1024px: OK · 0 elemen keluar layar
- 1440px: OK · 0 elemen keluar layar

## Audit otomatis (axe-core, WCAG 2.1 A/AA)
- 2 jenis pelanggaran · 5 node
  - [serious] color-contrast ×4 — Elements must meet minimum color contrast ratio thresholds
  - [critical] meta-viewport ×1 — Zooming and scaling must not be disabled

## Motion (terukur)
- Durasi: 0.3s ×57, 0.3s, 0s ×3, 1.2s ×3, 0.2s ×1
- Easing: cubic-bezier(0.4, 0, 0.2, 1) ×58, cubic-bezier(0.4, 0, 0.2, 1), ease ×3

## Performa (lab, bukan field)
- TTFB 1929ms · FCP 2188ms · LCP 2188ms · CLS 0
- Ambang: LCP ≤2500ms, CLS ≤0.1. Angka lab bisa lebih baik dari pengguna nyata.

## Prinsip yang bisa dipakai
- Skala tipe 2.62x → bangun token dari skala ini, jangan pilih ukuran per komponen.
- Palet: 1 warna aksi dominan + netral; permukaan dominan `#000000`.
- Ambil grid, density, ritme spacing, dan hierarki. JANGAN copy teks, logo, atau aset.

## Bukti visual
- `/Users/chaali0324/.agents/refs/lu.ma/desktop-hero.png` (desktop-hero)
- `/Users/chaali0324/.agents/refs/lu.ma/desktop.png` (desktop)
- `/Users/chaali0324/.agents/refs/lu.ma/mobile.png` (mobile)
