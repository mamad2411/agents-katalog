---
name: baca-gambar
description: WAJIB OTOMATIS dipakai tanpa slash saat user kirim/lampir gambar, PDF, screenshot, foto teks, atau minta baca isi gambar. OCR tesseract + PyMuPDF lokal, gratis. Trigger: gambar, foto, screenshot, pdf, baca gambar, isi gambar, ocr.
version: 1.0.0
tags: [ocr, gambar, pdf, gratis]
---

# Baca Gambar (OCR lokal, tanpa API)

Ambil teks dari gambar/screenshot/PDF tanpa upload ke layanan luar. Semua jalan lokal.

## Pakai

```bash
python3 ~/.agents/skills-store/baca-gambar/scripts/read.py "/path/ke/file.png"
python3 ~/.agents/skills-store/baca-gambar/scripts/read.py /path/ke/dokumen.pdf
```

Tanpa argumen, skrip memakai path kosong dan gagal — selalu kirim 1 path file.

## Yang didukung

- PNG, JPG, WEBP, TIFF (via tesseract)
- PDF: teks asli dulu (PyMuPDF); halaman hasil scan di-OCR otomatis
- Multi-bahasa: tesseract memakai bahasa yang terpasang (`tesseract --list-langs`)

## Alur kerja AI

1. Terima path dari user (jangan menebak isi gambar).
2. Jalankan skrip, tempel teks hasil apa adanya.
3. Kalau hasil kosong: laporkan "gambar tidak terbaca" + saran (resolusi/contrast),
   jangan mengarang isi.

## Batasan

- Tulisan tangan akurasi rendah; grafik tanpa teks tidak menghasilkan apa pun.
- PDF berpassword gagal → minta versi tanpa password.
- Butuh `tesseract` dan `pymupdf` terpasang (`brew install tesseract`, `pip install pymupdf`).
