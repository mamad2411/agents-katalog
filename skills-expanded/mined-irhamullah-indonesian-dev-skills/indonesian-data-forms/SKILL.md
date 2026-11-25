---
name: indonesian-data-forms
description: Use when building forms, validation, or data handling for Indonesian users - wilayah administratif (provinsi/kota/kecamatan/kelurahan), NIK & NPWP validation, phone number formatting (+62), shipping cost (RajaOngkir, Biteship), and Rupiah currency. Triggers on "validasi NIK", "validasi NPWP", "dropdown provinsi", "format nomor HP Indonesia", "ongkir RajaOngkir", "format Rupiah", "kode pos Indonesia", "waktu Indonesia"
---

# Indonesian Data & Forms

## Overview

Menangani data khas Indonesia di form dan API: wilayah administratif, validasi identitas (NIK/NPWP), nomor HP, ongkir, Rupiah, dan zona waktu. Prinsipnya: validasi dan normalisasi di boundary, simpan dalam bentuk canonical, format saat render.

## When to Use

- Form alamat dengan dropdown wilayah (provinsi → kelurahan): "dropdown provinsi", "kode pos Indonesia"
- Validasi NIK (KTP) atau NPWP (tax ID): "validasi NIK", "validasi NPWP"
- Normalisasi nomor HP Indonesia (+62, 08xx): "format nomor HP Indonesia"
- Integrasi ongkir (RajaOngkir, Biteship): "ongkir RajaOngkir"
- Format atau parsing Rupiah: "format Rupiah"
- Konversi waktu ke WIB/WITA/WIT: "waktu Indonesia"

**Jangan pakai kalau:** form internasional saja (tanpa data Indonesia), atau data sudah validated dan tersimpan canonical (cuma read).

## Router

| Topik / tugas | Berkas |
| --- | --- |
| Strategi & implementasi wilayah administratif (API, local dataset, seeded DB, cascading dropdown) | `references/wilayah-administratif.md` |
| Validasi NIK & NPWP, Zod schema, PII handling | `references/nik-npwp-validation.md` |
| Normalisasi & format nomor HP, WhatsApp link, landline | `references/phone-formatting.md` |
| Integrasi ongkir RajaOngkir/Biteship, abstraction, caching, berat volumetrik | `references/ongkir-integration.md` |
| Format & parsing Rupiah, PPN, diskon, storage integer | `references/rupiah-formatting.md` |
| WIB/WITA/WIT, UTC storage, cron timezone, business hours | `references/timezone-indonesia.md` |

## Core Principles

1. **Canonical form untuk storage.** Simpan nomor HP sebagai E.164, NIK/NPWP sebagai digit saja, dan uang sebagai integer rupiah. Format hanya saat render.

   ```typescript
   // Bad: Simpan as-is (formatted)
   db.user.phone = "+62 812-3456-7890"  // Inconsistent, hard to query
   db.user.nik = "3201 2345 6789 0001"  // With spaces

   // Good: Canonical form
   db.user.phone = "+6281234567890"     // E.164 format
   db.user.nik = "3201234567890001"     // 16 digits, no spaces
   db.user.amount = 100000              // Integer (in smallest unit), not string
   ```

2. **Validasi di boundary input.** Validasi ketat saat input — server-side juga, bukan cuma client — lalu percaya data internal.
3. **Jangan hardcode data wilayah.** Data wilayah berubah karena pemekaran; ambil dari dataset/API yang maintained dan refresh berkala.
4. **Uang tidak pernah float.** Rupiah praktis tanpa sub-unit; simpan integer dan bulatkan eksplisit.

## Workflow

Buka referensi sesuai Router, lalu ikuti langkah berikut:

1. **Wilayah:** pilih strategi (API vs local dataset vs seeded DB); rekomendasi local dataset BPS-based + refresh berkala; dropdown cascade harus reset child saat parent berubah. → detail: `references/wilayah-administratif.md`
2. **NIK:** cek 16 digit, parse DDMMYY (+40 untuk perempuan), validasi tanggal dan kode wilayah. → detail: `references/nik-npwp-validation.md`
3. **NPWP:** normalisasi ke digit; 15 digit legacy atau 16 digit NIK-based (sejak 2024). → detail: `references/nik-npwp-validation.md`
4. **Nomor HP:** normalisasi ke E.164, validasi prefix 8xx dan panjang, format saat display. → detail: `references/phone-formatting.md`
5. **Ongkir:** pakai interface `ShippingProvider` agar bisa switch RajaOngkir ↔ Biteship; cache hasil dengan TTL; hitung berat chargeable. → detail: `references/ongkir-integration.md`
6. **Rupiah:** simpan integer, format dengan `Intl.NumberFormat('id-ID')`, parse sadar separator `.` dan `,`. → detail: `references/rupiah-formatting.md`
7. **Waktu:** simpan UTC, tampilkan sesuai zona user, cron jobs eksplisit timezone. → detail: `references/timezone-indonesia.md`

## Anti-Patterns

- ❌ **Float untuk money** — pakai integer rupiah; decimal library hanya untuk pecahan.
- ❌ **Hardcode daftar wilayah** — pakai dataset/API yang maintained.
- ❌ **Simpan nomor HP dalam format tampilan** — query dan uniqueness jadi sulit.
- ❌ **Validasi hanya di client-side** — bisa di-bypass; validasi juga di server.
- ❌ **Kirim Rupiah sebagai string terformat di API** — kirim integer + `currency: "IDR"`.
- ❌ **Manual offset timezone** — pakai library atau `Intl`, bukan `+7 * 3600 * 1000`.
- ❌ **Hardcode ID destinasi ongkir** — ID berubah antar provider; cari dinamis.
- ❌ **Log NIK/NPWP mentah** — mask atau hash PII.

## Verification

- [ ] Wilayah data source maintained (API atau periodic update)
- [ ] NIK validation check struktur (16 digit, tanggal valid, kode wilayah)
- [ ] NPWP handle both 15 dan 16 digit formats
- [ ] Phone normalization ke E.164 (+62)
- [ ] Ongkir integration dengan provider abstraction
- [ ] Rupiah menggunakan integer (atau decimal library), bukan float
- [ ] Validation di server-side, bukan cuma client
- [ ] Timezone handling correct (WIB/WITA/WIT)
- [ ] Tests untuk edge cases (leap year, invalid date, etc)

## References

- `references/wilayah-administratif.md` — strategi data wilayah, API wilayah.id/emsifa, local dataset, seeding DB, refresh job, cascading dropdown, edge case pemekaran.
- `references/nik-npwp-validation.md` — struktur & algoritma NIK/NPWP, Zod schema, masking/enkripsi PII, testing.
- `references/phone-formatting.md` — normalisasi E.164, prefix operator, format display, WhatsApp link, landline.
- `references/ongkir-integration.md` — interface provider, implementasi RajaOngkir & Biteship, caching, berat volumetrik, API route.
- `references/rupiah-formatting.md` — format/parse Rupiah, compact format, PPN, diskon, storage BIGINT.
- `references/timezone-indonesia.md` — peta WIB/WITA/WIT, konversi UTC, cron, business hours, database.

## Related Skills

- `api-and-interface-design` — untuk design validation interface
- `security-and-hardening` — untuk PII data handling (NIK = sensitive)
- `performance-optimization` — untuk optimize wilayah data loading
- `data-resmi-indonesia` — data resmi & aturan berperiode Indonesia:
  - Hari libur nasional / cuti bersama / hari kerja
  - Kurs BI & JISDOR
  - UMP / upah minimum
  - Aturan pajak (PTKP, PPh 21 TER, PPN) & BPJS
  - Wilayah administratif, kode pos, NIK/NPWP, ongkir, Rupiah, timezone **tetap di skill ini**
