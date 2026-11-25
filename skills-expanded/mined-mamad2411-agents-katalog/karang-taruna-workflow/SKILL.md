---
name: karang-taruna-workflow
description: Gunakan saat mengerjakan fitur, perbaikan bug, atau perubahan apa pun pada repositori Sistem Informasi Karang Taruna. Berisi metodologi kerja dan skill inti proyek.
---

# Skill: Karang Taruna Workflow

Skill ini adalah panduan teknik kerja proyek, mengikuti pola `obra/superpowers`. Skill adalah panduan teknik terbukti yang dipakai ulang agar agen bekerja konsisten dan andal. Umumkan di awal saat memakai skill, misalnya "Saya memakai skill karang-taruna-workflow".

## Konvensi Penyimpanan Skill

Mengikuti pola superpowers, setiap skill diletakkan di folder tersendiri dengan berkas `SKILL.md`:

```
skills/
  <nama-skill>/
    SKILL.md        wajib, berisi frontmatter name + description dan isi panduan
    resources/      opsional, contoh kode atau template pendukung
```

Berkas `skill.md` di akar berperan sebagai skill inti sekaligus indeks. Skill proses dipakai lebih dulu, baru skill implementasi.

## Kapan Skill Ini Dipakai

Wajib dibaca sebelum menyentuh kode fitur baru, memperbaiki bug, atau melakukan refactor. Skill ini menetapkan urutan berpikir sebelum implementasi.

## Alur Inti

### Fase 1: Brainstorming
Sebelum kerja kreatif apa pun (membuat fitur, komponen, atau mengubah perilaku), gali dulu maksud dan kebutuhan. Ajukan pertanyaan bila ada yang ambigu. Jangan langsung menulis kode.

### Fase 2: Perencanaan
Tulis rencana langkah demi langkah, tentukan berkas yang disentuh, dan buat daftar tugas untuk pekerjaan besar. Pastikan rencana selaras dengan `PRD.md`.

### Fase 3: Implementasi (TDD)
Terapkan siklus Test-Driven Development bila memungkinkan:
1. RED, tulis test yang gagal lebih dulu.
2. GREEN, tulis kode paling sederhana agar test lolos.
3. REFACTOR, rapikan tanpa mengubah perilaku.
Ikuti pola kode yang sudah ada. Baca berkas terkait sebelum mengubahnya.

### Fase 4: Verifikasi
Jalankan `npm run lint`, `npm run test`, dan `npm run build` bila menyentuh tipe atau rute. Perbaiki error sebelum melapor selesai. Untuk pekerjaan berisiko, verifikasi dengan sub-agen terpisah.

## Skill Pendukung (Katalog)

Skill berikut disarankan hidup di folder `skills/`. Masing-masing mengikuti format `SKILL.md` yang sama.

### systematic-debugging
Gunakan saat menelusuri bug. Empat langkah, yaitu investigasi (kumpulkan bukti dan reproduksi), hipotesis (rumuskan sebab paling mungkin), perbaikan (ubah satu hal terkecil), dan verifikasi (buktikan bug hilang dan tidak ada regresi). Jika satu pendekatan gagal dua kali, berhenti menambal dan cari akar masalahnya.

### prisma-migration
Gunakan saat mengubah skema database. Edit `prisma/schema.prisma`, lalu sinkronkan dengan `npx prisma db push` (pola baseline proyek ini) dan pastikan `npx prisma generate` sukses sebelum menjalankan test. Bila beralih ke alur migrasi penuh, pakai `npx prisma migrate dev --name <deskripsi>` dan jangan mengedit migrasi lama yang sudah diterapkan. Koneksi database disuntikkan lewat driver adapter dan `prisma.config.ts`, bukan lewat baris `url` di schema.

### api-route-pattern
Gunakan saat membuat atau mengubah route handler di `src/app/api`. Pakai `lib/auth-helpers.ts` untuk cek sesi dan peran, `lib/validations.ts` untuk validasi Zod, `lib/api-helpers.ts` untuk format respons, dan `lib/audit.ts` untuk mencatat aksi tulis. Sebelum menambah endpoint baru, cek dulu apakah fitur tersebut sebaiknya memakai Server Action (`actions.ts` dengan `"use server"`) seperti pola yang sudah dipakai luas di area admin.

### content-sanitize
Gunakan saat menangani input rich text dari TipTap. Selalu sanitasi lewat `lib/sanitize.ts` sebelum menyimpan atau menampilkan agar aman dari XSS.

### ui-consistency
Gunakan saat membangun antarmuka. Ikuti token dan komponen di `desain.md`, pakai komponen `ui` dan `shared` yang ada, dan pastikan tampil baik di mode terang dan gelap.

## Aturan Emas

- Utamakan aksi nyata dengan tools dibanding berteori.
- Buat perubahan kecil, terukur, dan mudah dijelaskan (ini proyek skripsi).
- Selalu verifikasi sebelum melapor selesai.
- Jangan menambah dependency, mengganti bahasa domain, atau melakukan refactor yang tidak diminta.
- Jujur menyebut hal yang belum bisa diverifikasi.

## Referensi

Baca `CLAUDE.md` untuk aturan teknis, `AGENTS.md` untuk peran agen, `PRD.md` untuk kebutuhan produk, dan `desain.md` untuk sistem desain.

