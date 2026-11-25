# Referensi: Free Tailwind CSS Admin Dashboard Template - TailAdmin
<https://tailadmin.com/demo>  ·  dibaca 2026-11-14 11:46

## Ringkasan
- Viewport dianalisa: 1440px · tinggi halaman 1502px · 200 elemen terlihat
- Bahasa: en · background body `#ffffff`
- Section terdeteksi: 3 · CTA: 7 · gambar: 1

## Tipografi
- Font: Outfit ×32
- Ukuran dominan: 14px, 16px, 20px
- Semua ukuran: 14px, 16px, 18px, 20px
- Rasio antar-step: ~1.25x
- Weight: 500 ×18, 400 ×13, 700 ×1 · line-height: 24px ×17, 20px ×11, 28px ×4

## Warna
- Teks: #98a2b3 ×20, #344054 ×5, #ffffff ×4, #374151 ×2, #1d2939 ×1
- Permukaan (bg): #ffffff ×7, #f2f4f7 ×2, #465fff ×2, #344054 ×1, #101828 ×1
- Kontras gagal (<4.5:1): 0

## Ritme & bentuk
- Gap: 8px ×13, 12px ×4, 6px ×3, 16px ×2, 28px ×1, 4px ×1, 20px ×1, 5px ×1
- Padding: 8px ×10, 4px ×8, 28px ×5, 12px ×5, 20px ×5, 16px ×3, 24px ×3, 10px ×3
- Radius: 0px ×182, 8px ×11, 3.35544e+07px ×7
- Shadow: 1 varian
- Container max-width: 472px ×1, 100% ×1, 1280px ×1, 388px ×1, 340px ×1

## Layout (urut vertikal)
| y | tinggi | bg | isi | grid | heading |
|---|---|---|---|---|---|
| 16 | 868 | `transparent` | teks | - | - |
| 0 | 900 | `transparent` | media | 1 kol × 4 baris · kartu 244px | ERROR |
| 900 | 602 | `#101828` | media, form | - | - |

## CTA
- "V 2.5" · bg `#f2f4f7` · teks `#667085` · radius 3.35544e+07px · 24×65 · 12px/500
- "Products" · bg `#000000` · teks `#344054` · radius 0px · 24×89 · 16px/500
- "Resources" · bg `#000000` · teks `#344054` · radius 0px · 24×98 · 16px/500
- "2.4k+" · bg `#f2f4f7` · teks `#000000` · radius 3.35544e+07px · 32×79 · 16px/400
- "Live Preview" · bg `#344054` · teks `#ffffff` · radius 8px · 46×140 · 14px/500
- "Pricing & FAQ" · bg `#465fff` · teks `#ffffff` · radius 8px · 44×153 · 14px/500

## Gambar
- 1 gambar · rasio dominan: 2.99:1

## Aksesibilitas
- Heading: 4 · urutan: h1, h4, h4, h4
- Target <24px: 6 (contoh: "Components")

## Responsive (diukur di 4 lebar)
- 360px: OK · 9 elemen keluar layar
- 768px: OK · 0 elemen keluar layar
- 1024px: OK · 0 elemen keluar layar
- 1440px: OK · 0 elemen keluar layar

## Audit otomatis (axe-core, WCAG 2.1 A/AA)
- 2 jenis pelanggaran · 2 node
  - [serious] aria-hidden-focus ×1 — ARIA hidden element must not be focusable or contain focusable element
  - [serious] color-contrast ×1 — Elements must meet minimum color contrast ratio thresholds

## Motion (terukur)
- Durasi: 0.2s ×25, 0.15s ×1
- Easing: cubic-bezier(0.4, 0, 0.2, 1) ×8

## Performa (lab, bukan field)
- TTFB 1044ms · FCP 1720ms · LCP 2328ms · CLS 0.001
- Ambang: LCP ≤2500ms, CLS ≤0.1. Angka lab bisa lebih baik dari pengguna nyata.

## Prinsip yang bisa dipakai
- Skala tipe 1.25x → bangun token dari skala ini, jangan pilih ukuran per komponen.
- Palet: 1 warna aksi dominan + netral; permukaan dominan `#ffffff`.
- Ambil grid, density, ritme spacing, dan hierarki. JANGAN copy teks, logo, atau aset.

## Bukti visual
- `/Users/chaali0324/.agents/refs/tailadmin.com-demo/desktop-hero.png` (desktop-hero)
- `/Users/chaali0324/.agents/refs/tailadmin.com-demo/desktop.png` (desktop)
- `/Users/chaali0324/.agents/refs/tailadmin.com-demo/mobile.png` (mobile)
