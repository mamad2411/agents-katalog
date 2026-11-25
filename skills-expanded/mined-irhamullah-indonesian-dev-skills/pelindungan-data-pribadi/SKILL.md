---
name: pelindungan-data-pribadi
description: Use when an app processes Indonesian users' personal data and you need to comply with UU 27/2022 (UU PDP) and its implementing regulation PP 33/2026 — lawful bases, consent, data subject rights, breach notification within 3x24 hours, processor contracts, cross-border transfer, and sanctions (up to 2% annual revenue). Triggers on "UU PDP", "perlindungan data pribadi", "Pasal 57", "notifikasi kebocoran data", "consent data pribadi", "privacy policy Indonesia", "DPA", "transfer data antarnegara".
---

# Pelindungan Data Pribadi (UU PDP)

## Overview

Setiap aplikasi yang memproses **data pribadi pengguna Indonesia** tunduk pada
**UU No. 27 Tahun 2022** tentang Pelindungan Data Pribadi (UU PDP) dan
pelaksanaannya, **PP No. 33 Tahun 2026** (mulai berlaku 16 Januari 2027).
Skill ini memandu penerapan tata kelola data yang patuh: dasar pemrosesan,
hak subjek data, kewajiban pengendali/prosesor, notifikasi insiden, dan sanksi.

## When to Use

- Melakukan pemrosesan data pribadi pengguna Indonesia (profil, kontak, kesehatan,
  biometrik, keuangan, lokasi, perilaku).
- Membuat halaman privasi, consent flow, atau menu hak subjek data.
- Merancang notifikasi kebocoran data / insiden keamanan.
- Mengontrak pihak ketiga (processor) yang menyentuh data pribadi.
- Mentransfer data pribadi ke luar negeri.
- Menilai risiko sanksi (administratif & pidana) sebuah fitur.

**Jangan pakai kalau:**

- Hanya memproses data non-pribadi (agregat, anonim, statistik).
- Data pengguna di luar yurisdiksi Indonesia, tanpa menyentuh data WNI/pengguna
  Indonesia (pertimbangkan GDPR, PDPA, atau UU lokal).

## Router

| Topik / tugas | Berkas |
| --- | --- |
| Definisi, jenis data & asas; kapan UU berlaku | `references/konsep-dasar.md` |
| Hak subjek data & cara mengimplementasikannya | `references/hak-subjek-data.md` |
| Kewajiban pengendali & prosesor (incl. DPA, transfer lintas negara) | `references/kewajiban-pengendali-prosesor.md` |
| Notifikasi insiden kebocoran data dalam 3×24 jam | `references/notifikasi-insiden.md` |
| Sanksi administratif & pidana; matriks risiko | `references/sanksi.md` |

## Workflow

1. **Identifikasi data** — labeli setiap field: termasuk data pribadi **umum**
   atau **spesifik**? (label pemrosesan lebih ketat.) → `references/konsep-dasar.md`
2. **Tetapkan dasar pemrosesan (lawful basis)** — persetujuan, kontrak,
   kewajiban hukum, kepentingan vital, kepentingan umum, atau kepentingan sah.
   Catat dasar ini per fitur.
3. **Implementasikan hak subjek data** — informasi, akses, perbaikan,
   penghapusan, pembatasan, portabilitas. Sedikan mekanisme yang dapat ditindak
   (formulir, endpoint, dukungan). → `references/hak-subjek-data.md`
4. **Terapkan kewajiban pengendali** — minimisasi data, keamanan teknis &
   administratif, dokumentasi pemrosesan, kontrak dengan prosesor, dan aturan
   transfer lintas negara bila relevan. → `references/kewajiban-pengendali-prosesor.md`
5. **Siapkan rencana respons insiden** — deteksi → mitigasi → notifikasi dalam
   **3×24 jam** ke subjek data dan lembaga. → `references/notifikasi-insiden.md`
6. **Audit risiko sanksi** — pastikan kepatuhan untuk menghindari denda hingga
   **2% pendapatan tahunan** dan sanksi pidana. → `references/sanksi.md`

## Core Principles

1. **Minimisasi data.** Kumpulkan hanya yang diperlukan; jangan simpan lebih
   lama dari tujuan pemrosesan.
2. **Persetujuan (consent) harus nyata dan eksplisit** untuk data spesifik.
   Jangan gunakan opt-out tersembunyi, `pre-checked` checkbox, atau persetujuan
   tunggal untuk banyak tujuan.
3. **Privasi by design.** Pertimbangkan PDP sejak desain fitur, bukan setelah
   jadi. Terapkan enkripsi, kontrol akses, dan audit log.
4. **Dokumentasikan pemrosesan.** Simpan catatan dasar hukum, tujuan, kategori
   data, dan jangka waktu penyimpanan — ini dasar pembuktian kepatuhan.
5. **Jangan pernah menyimpan data pribadi di log, cache, atau dokumen
   pengembangan** (mis. console.log, file dump, contoh).

## Anti-patterns

- Mencampur logika consent ke dalam satu tombol "Setuju" untuk semua tujuan.
- Menyimpan data pribadi di log/error reporter/cache tanpa anonimisasi.
- Menggunakan data untuk tujuan di luar yang dinyatakan di privacy policy.
- Tidak menyediakan jalur penghapusan data meski pengguna memintanya.
- Mentransfer data ke luar negeri tanpa mekanisme (perjanjian, pengecualian).
- Menganggap "sudah ada T&C" = kepatuhan penuh (UU PDP menuntut banyak lagi).

## Verification checklist

- [ ] Seluruh data pribadi telah dilabeli (umum vs spesifik).
- [ ] Setiap fitur pemrosesan punya dasar hukum tertulis.
- [ ] Privacy policy tersedia & dapat diakses, memuat tujuan pemrosesan.
- [ ] Mekanisme hak subjek data (akses/perbaikan/penghapusan) berfungsi.
- [ ] Kontrak dengan prosesor pihak ketiga ada & memuat standar keamanan.
- [ ] Prosedur notifikasi insiden 3×24 jam telah siap & teruji.
- [ ] Tidak ada data pribadi di log/cache/dokumen pengembangan.

## Related Skills

- `security-and-hardening` — kontrol teknis keamanan data.
- `observability-and-instrumentation` — logging aman & audit trail.
- `api-and-interface-design` — desain consent flow & endpoint hak subjek data.
- `database-design` — enkripsi & minimisasi penyimpanan.
