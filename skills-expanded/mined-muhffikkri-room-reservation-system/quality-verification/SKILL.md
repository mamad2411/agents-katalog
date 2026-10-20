---
name: quality-verification
description: Gerbang kualitas wajib proyek sistem-reservasi sebelum commit/push — pint, test suite, migrate:fresh --seed, skrip bukti logika bisnis, dan cara membuktikan bukan sekadar mengklaim.
---

# Quality Verification Gates

Pekerjaan dinyatakan "selesai" hanya jika semua gerbang relevan lulus dan **bukti output
ditempel ke chat**. Klaim tanpa bukti dianggap belum selesai.

## Gerbang 1 — Formatting (wajib jika ada file PHP berubah)

```bash
vendor/bin/pint --dirty --format agent
```

- `--dirty` hanya menyentuh file yang berubah. Wajib dijalankan, bukan `--test`.

## Gerbang 2 — Test suite

```bash
php artisan test --compact
```

- Semua test harus lulus. Milestone 2+ wajib menambah test fitur baru
  (skenario ada di spec §14.1–14.3; gunakan factory yang tersedia).
- Test Feature memakai `RefreshDatabase` dengan database `reservasi_kampus_testing`
  (lihat `phpunit.xml`); pastikan MySQL berjalan sebelum test.
- Format bukti minimal: perintah + ringkasan hasil (jumlah test, assertions) ditempel verbatim.

## Gerbang 3 — Database & seeder (jika menyentuh migrasi/seeder/model)

```bash
php artisan migrate:fresh --seed --no-interaction --force
```

- Harus sukses dari nol. Lalu buktikan isi data (jumlah baris per tabel, distribusi role/status).

## Gerbang 4 — Bukti logika bisnis (jika menyentuh business rules BR-1..BR-20)

Tulis skrip verifikasi sementara di `scripts/` (bootstrap Laravel, jalankan query/fungsi,
print hasil), jalankan, **tempel output**, lalu **hapus skripnya** — jangan di-commit.
Contoh yang sudah pernah dilakukan: membuktikan `scopeOverlap`
(09:00–09:30 vs approved 08:00–10:00 → true; 10:00–11:00 → false).

> Alasan skrip PHP, bukan `php artisan tinker --execute`: quoting PowerShell merusak
> string bersarang (error `Unexpected end of input`). Template bootstrap ada di
> `scripts/create-database.php`.

## Jebakan testing yang SUDAH PERNAH TERJADI — jangan ulangi

- `config()` di dalam `try/catch` pada Rule objects: error konfigurasi tertelan dan rule
  lolos diam-diam. Baca timezone/konfigurasi di luar `try`; hanya parsing tanggal
  yang boleh masuk `try`.
- Test Unit yang menyentuh helper Laravel (`config()`, `now()`, dsb.) wajib
  `uses(Tests\TestCase::class)`, karena suite Unit tidak mem-boot aplikasi secara default.

## Gerbang 5 — Cek kebocoran (wajib sebelum commit)

```bash
git status --short        # tidak boleh ada .env, vendor/, node_modules/, storage logs
```

`.gitignore` sudah mengatur `.env`, `/vendor`, `/node_modules` — jangan pernah memodifikasi
`.gitignore` untuk memasukkannya.

## Checklist "Definition of Done" per tugas

- [ ] Kode mengikuti spec (bagian § yang relevan dikutip di laporan)
- [ ] Pint bersih
- [ ] Test lulus (test baru untuk fitur baru)
- [ ] `migrate:fresh --seed` lulus (jika ada perubahan skema/seeder)
- [ ] Bukti logika bisnis ditampilkan (jika menyentuh BR)
- [ ] Tidak ada file sensitif ter-stage
- [ ] Daftar commit tampil dan disetujui user
