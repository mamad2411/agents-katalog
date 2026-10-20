---
name: project-workflow
description: Siklus kerja end-to-end proyek sistem-reservasi — milestone, rencana dulu, verifikasi user sebelum eksekusi/push, bukti kerja, PR. Gunakan skill ini di SETIAP tugas tanpa kecuali.
---

# Workflow Proyek (milik user — jangan dilanggar)

## Prinsip induk

User selalu **memverifikasi sebelum mengizinkan**. Agent mengusulkan, user memutuskan.
Tidak ada aksi permanen (commit, push, PR, merge) tanpa persetujuan eksplisit yang sesuai konteks.

## Fase 1 — Rencana (WAJIB sebelum menulis kode)

Untuk setiap milestone/tugas, presentasikan:

1. **Ruang lingkup**: file apa saja yang dibuat/diubah, referensi bagian spec (§) yang mengikat.
2. **Alasan desain** untuk setiap keputusan (kenapa ENUM ini, kenapa index itu, dst.).
3. **Yang TIDAK dikerjakan** di milestone ini (mencegah scope creep).
4. **Rencana verifikasi** — apa bukti yang akan ditunjukkan (lihat skill quality-verification).
5. **Rencana commit** — pesan conventional commit (Bahasa Inggris) yang diusulkan.

Tunggu persetujuan user (mis. jawaban "lanjut"/"oke") sebelum eksekusi.
Persetujuan sah = jawaban eksplisit seperti itu. Diam atau ganti topik bukan persetujuan.

## Fase 2 — Eksekusi

- Kerja di **branch baru** (lihat skill git-conventions), jangan di `main` — target PR-nya `dev`.
- Ikuti spec `docs/spesifikasi-sistem-reservasi.md` — §4 (DB), §5 (model/middleware), §6 (routes),
  §7 (validasi), §8 (business rules). Setiap keputusan di sana tidak boleh dilanggar.
- Gunakan `php artisan make:*` untuk scaffold; konvensi Laravel 13:
  atribut `#[Fillable([...])]`, `casts(): array`, PHPDoc `@use HasFactory<...>`.
- Model = relasi + scope saja. Logika bisnis di `app/Services/*`. Controller tipis.
- Jalankan verifikasi (Fase 3) SETELAH setiap unit kerja selesai, bukan hanya di akhir.

## Fase 3 — Verifikasi & bukti (lihat skill quality-verification)

- Jalankan seluruh gerbang kualitas dan **tempel output buktinya** ke chat
  (jumlah data seed, hasil uji logika, hasil pint & test). "Sudah dikerjakan" tanpa bukti = belum selesai.

## Fase 4 — Commit & verifikasi user SEBELUM push

1. Commit kecil & logis (satu unit kerja per commit), pesan conventional English.
2. Tampilkan tabel: hash + pesan commit + file yang terlibat.
3. **Tunggu user menyetujui**, baru `git push`.
4. Jika user minta perubahan pesan/struktur commit → `git reset --soft` dan ulangi, jangan amend push lama.

## Fase 5 — Pull Request (alur: fitur → dev → staging → prod)

- PR fitur: `--base dev --head <branch>` (BUKAN ke `main`).
- Promosi antar tingkat hanya via PR: `dev` → `staging` (UAT/demo, harus stabil),
  `staging` → `prod` (versi siap kumpul). Judul promosi:
  `chore: promote <sumber> to <tujuan> (<isi>)`, mis. `chore: promote dev to staging (slot-overlap)`.
- `main` adalah cermin stabil, bukan gerbang kerja harian: disamakan ke `prod` tiap rilis.
- Buat PR via `gh pr create` (atau `& "C:\Program Files\GitHub CLI\gh.exe"` jika PATH belum refresh).
- Body PR berisi: Summary, What's included, Verification (bukti), Commits.
- Judul & body Bahasa Inggris, judul memakai conventional commit style.
- Perubahan docs-only (komentar, skill, README): tetap branch+PR, tetapi boleh merge
  cukup dengan cek suite hijau tanpa review mendalam.
- **User yang merge manual di GitHub.** Agent tidak merge kecuali diminta eksplisit.

## Fase 6 — Sinkronisasi pasca-merge

Setelah user merge PR fitur ke `dev`: `git checkout dev && git pull origin dev`,
verifikasi merge commit ada di log, laporkan status.
Tawarkan pembersihan branch fitur (lokal/remote) secara opsional.
Promosi `dev → staging → prod` dilakukan per PR saat tingkat bawah sudah verified.
Saat rilis: samakan `main` ke `prod` (`git checkout main && git merge prod && git push`)
agar branch default selalu menunjuk versi stabil terakhir.
Perbarui catatan handoff sesi (status, keputusan, kandidat berikutnya) setiap milestone selesai.

## Gaya komunikasi dengan user

- Bahasa Indonesia, ringkas, pakai tabel status ✅/⚠️/❌.
- Selalu tutup laporan dengan **langkah berikutnya** yang diusulkan.
- Jika menemukan temuan menarik (mis. versi EOL, deprekasi), sampaikan dengan tabel perbandingan
  dan tindak lanjut konkret.
- Saat user bertanya konsep (mis. "kenapa BIGINT?"), jawab edukatif berlapis:
  konvensi → alasan teknis → dampak praktis.
