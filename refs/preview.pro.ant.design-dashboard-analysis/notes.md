# Referensi: Analysis - Ant Design Pro
<https://preview.pro.ant.design/dashboard/analysis>  ·  dibaca 2026-11-10 21:50

## Ringkasan
- Viewport dianalisa: 1440px · tinggi halaman 2024px · 671 elemen terlihat
- Bahasa: ? · background body `#000000`
- Section terdeteksi: 4 · CTA: 0 · gambar: 5

## Tipografi
- Font: AlibabaSans ×124, SFMono-Regular ×7
- Ukuran dominan: 11px, 12px, 14px, 16px, 30px
- Semua ukuran: 11px, 12px, 14px, 16px, 18px, 30px
- Rasio antar-step: ~1.88x
- Weight: 400 ×110, 600 ×19, 500 ×1, 700 ×1 · line-height: 22px ×70, 25.1429px ×16, 40px ×13, 20px ×7, 17.2857px ×7

## Warna
- Teks: #000000 ×119, #1677ff ×5, #1890ff ×4, #ffffff ×3
- Permukaan (bg): #ffffff ×18, #fafafa ×4, #000000 ×3, #f5f5f5 ×1, #1890ff ×1
- Kontras gagal (<4.5:1): 0

## Ritme & bentuk
- Gap: 8px ×21, 4px ×3, 8px normal ×1, 12px ×1
- Padding: 8px ×56, 4px ×21, 24px ×18, 16px ×16, 12px ×16, 36px ×10, 6px ×6, 32px ×5
- Radius: 0px ×583, 6px ×45, 8px ×10, 8px 8px 0px 0px ×10, 20px ×7, 0px 0px 8px 8px ×6
- Shadow: 2 varian
- Container max-width: 50% ×24, 100% ×19, 25% ×4, 256px ×2, 66.6667% ×1

## Layout (urut vertikal)
| y | tinggi | bg | isi | grid | heading |
|---|---|---|---|---|---|
| 88 | 261 | `transparent` | media | 4 kol × 1 baris · kartu 282px | - |
| 349 | 412 | `#ffffff` | media, form | - | - |
| 785 | 501 | `transparent` | media, form | - | - |
| 1318 | 600 | `#ffffff` | media | baris horizontal 10 item · 138px | - |

## CTA
- tidak ada tombol dengan latar solid

## Gambar
- 5 gambar · rasio dominan: 1.78:1, 1:1
- 4 gambar tanpa alt (cacat a11y — jangan ditiru)

## Aksesibilitas
- Heading: 2 · urutan: h1, h4
- Target <24px: 6 (contoh: "搜索关键词-0")

## Responsive (diukur di 4 lebar)
- 360px: OK · 97 elemen keluar layar
- 768px: OK · 74 elemen keluar layar
- 1024px: OK · 68 elemen keluar layar
- 1440px: OK · 41 elemen keluar layar

## Audit otomatis (axe-core, WCAG 2.1 A/AA)
- 7 jenis pelanggaran · 21 node
  - [serious] aria-progressbar-name ×1 — ARIA progressbar nodes must have an accessible name
  - [critical] aria-required-children ×2 — Certain ARIA roles must contain particular children
  - [critical] aria-valid-attr-value ×1 — ARIA attributes must conform to valid values
  - [serious] color-contrast ×14 — Elements must meet minimum color contrast ratio thresholds
  - [serious] html-has-lang ×1 — <html> element must have a lang attribute
  - [critical] image-alt ×1 — Images must have alternative text

## Motion (terukur)
- Durasi: 0.3s ×63, 0.2s ×27, 0.2s, 0.2s ×21, 0.2s, 0.3s, 0.3s ×10, 0.3s, 0.3s, 0.2s ×8
- Easing: ease, ease ×24, cubic-bezier(0.215, 0.61, 0.355, 1), cubic-bezier(0.645, 0.045, 0.355, 1), ease ×10, cubic-bezier(0.645, 0.045, 0.355, 1), cubic-bezier(0.645, 0.045, 0.355, 1), cubic-bezier(0.645, 0.045, 0.355, 1) ×8, ease, ease, cubic-bezier(0.215, 0.61, 0.355, 1) ×8

## Performa (lab, bukan field)
- TTFB 2859ms · FCP 6488ms · LCP 6488ms · CLS 0.068
- Ambang: LCP ≤2500ms, CLS ≤0.1. Angka lab bisa lebih baik dari pengguna nyata.

## Prinsip yang bisa dipakai
- Skala tipe 1.88x → bangun token dari skala ini, jangan pilih ukuran per komponen.
- Palet: 1 warna aksi dominan + netral; permukaan dominan `#000000`.
- Ambil grid, density, ritme spacing, dan hierarki. JANGAN copy teks, logo, atau aset.

## Bukti visual
- `/Users/chaali0324/.agents/refs/preview.pro.ant.design-dashboard-analysis/desktop-hero.png` (desktop-hero)
- `/Users/chaali0324/.agents/refs/preview.pro.ant.design-dashboard-analysis/desktop.png` (desktop)
- `/Users/chaali0324/.agents/refs/preview.pro.ant.design-dashboard-analysis/mobile.png` (mobile)
