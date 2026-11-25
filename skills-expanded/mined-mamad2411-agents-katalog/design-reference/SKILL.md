---
name: design-reference
description: Baca referensi UI/UX dari internet secara nyata — Framer, Dribbble, Figma Community, Mobbin, situs produk apa pun, atau screenshot lokal — lalu ukur hasil build sendiri dengan gerbang PASS/FAIL. Menghasilkan screenshot (desktop/mobile), angka terukur (skala tipe, palet + kontras, ritme spacing, radius, grid, section, CTA), audit axe-core WCAG 2.1 AA, LCP/CLS, dan export token Tailwind. Pakai saat user bilang "kayak situs X", "cari referensi", "lihat dribbble/framer/figma", "desainnya bagus kenapa", atau minta UI baru tanpa arah.
license: internal
---

# Design Reference (lensa referensi)

Tujuan: berhenti menebak dari ingatan. Setiap klaim desain harus punya angka atau
screenshot yang benar-benar dibaca. Kalau tidak bisa diukur, jangan diklaim.

## 1. Jalankan lensa (1 perintah)

```bash
dref https://dribbble.com/shots/popular/web-design      # atau framer.com, figma.com/community, linear.app
dref https://situs-target.com --no-shot                 # cepat: angka saja, tanpa screenshot
dref ~/Downloads/moodboard.png                          # screenshot lokal
```

`dref` = `python3 ~/.agents/scripts/design-read.py`. Output ke `~/.agents/refs/<slug>/`:
`desktop.png`, `desktop-hero.png`, `mobile.png`, `tokens.json`, `notes.md`.

Waktu: ±5 s tanpa screenshot, ±10 s dengan screenshot. Exit ≠ 0 = gagal, jangan lanjut.

## 2. Baca hasilnya — dua-duanya wajib

1. `notes.md` → angka: skala tipe + rasio, palet teks/permukaan, kontras gagal,
   gap/padding/radius, tabel section (y, tinggi, bg, isi), CTA, gambar, heading, a11y.
2. **Buka `desktop-hero.png` dengan tool Read (multimodal).** Angka tidak menangkap
   komposisi: alignment, whitespace, berat visual, urutan mata. Screenshot-lah yang
   menjawab "kenapa ini kelihatan mahal". Kalau `mobile.png` ada, buka juga.

Kalau halaman memblokir (captcha), script mencetak `WARN`; screenshot bisa tidak
mewakili. Jangan berpura-pura berhasil — pilih referensi lain.

## 3. Yang diambil (dan yang tidak)

Ambil: grid & container (max-width), density, skala tipe + rasio, ritme spacing
(4/8/12/16/24/32/48/64), bahasa bentuk (border vs shadow vs radius), hierarki CTA,
cara memakai warna aksen, pola section (hero → proof → fitur → CTA).

Jangan: copy teks, logo, foto, ilustrasi, atau nama brand. Jangan tiru cacat yang
terukur (kontras <4.5:1, target <24 px, gambar tanpa alt) — catat sebagai "jangan
diulang".

## 4. Ubah jadi keputusan, bukan ringkasan

Tulis 3–6 baris sebelum koding:

```
Referensi: <url> (skala 1.25x · radius 8/15 · gap 24/32 · bg #08090a · aksen 1 warna)
Ambil  : grid 1200px + hero kiri-teks/kanan-produk, ritme 96px antar section
Buang  : gradient ungu-biru, badge "AI-powered", 3 kartu fitur identik
Token  : --space-*, --text-*, --radius-*, --color-* di DESIGN.md
```

Tanpa blok ini, langkah 5 di `~/.agents/DESIGN-PLAYBOOK.md` (implementasi token-first)
tidak boleh dimulai.

## 5. Beberapa referensi sekaligus

Untuk arah baru, ambil 2–3 sumber berbeda (mis. 1 SaaS, 1 dashboard, 1 editorial),
lalu bandingkan angkanya: mana yang skala tipenya paling dekat, mana density-nya cocok
dengan produk. Jangan campur 5 gaya — pilih satu arah, eksekusi konsisten.

## 6. Setelah kode: ukur build sendiri, jangan diklaim

```bash
dref <url-referensi> --tailwind    # token awal untuk DESIGN.md
dcheck <url-build-sendiri>         # gate PASS/FAIL, exit 1 = belum selesai
dvisual <url-build-sendiri>        # visual regression: baseline vs sekarang (% piksel + peta diff)
dcopy <file|url|->                 # gate copy Indonesia: buzzword, klaim tanpa bukti, pola AI
```

`dcheck` mengukur: scroll horizontal di 360/768/1024/1440, kontras (axe-core WCAG 2.1 AA),
target sentuh <24px, alt gambar, urutan heading, label input, `prefers-reduced-motion`,
drift skala tipe, dan spacing di luar kelipatan 4. LCP/CLS ikut diukur (lab, bukan field).
`dvisual` menyimpan baseline; jalankan `--update` hanya setelah perubahan disengaja.
Gate keras yang FAIL = jangan lapor selesai.

Kontrak desain proyek ditulis di `DESIGN.md` (`cp ~/.agents/templates/DESIGN.md .`).

## 7. Batas

- Halaman butuh login (Mobbin, sebagian Figma) → pakai screenshot yang user kirim,
  jangan mengarang isi halaman.
- Hasil ukur = potret satu viewport 1440px. Perilaku responsive dibaca dari `mobile.png`,
  bukan diasumsikan.
- Referensi ≠ izin menyalin. Yang dipakai prinsipnya; aset dan copy tetap milik pemiliknya.
