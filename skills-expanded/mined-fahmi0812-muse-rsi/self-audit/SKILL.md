---
name: self-audit
description: Checklist audit skill baru sebelum dipasang ke muse-rsi. Wajib lolos semua poin wajib sebelum skill masuk indeks.
---

# self-audit

Skill orisinal `muse-rsi`. Dipakai sebelum skill baru dipasang, dan sebelum skill lama diperbarui.

## Tujuan

Pastikan skill yang masuk `muse-rsi` benar-benar ada, aman, gratis, dan tidak merusak sistem.

## Checklist — poin wajib (semua harus Ya)

| # | Cek | Cara cek | Lolos? |
|---|---|---|---|
| 1 | Repo ada | Buka https://github.com/owner/repo — halaman terbuka, bukan 404 | Ya / Tidak |
| 2 | Ada SKILL.md | Cari file `SKILL.md` di root atau di subfolder `skills/` / `.claude/skills/` | Ya / Tidak — kalau tidak ada, catat sebagai alat, bukan skill |
| 3 | Lisensi jelas | Baca file LICENSE / bagian lisensi di README. Catat jenisnya (MIT, Apache-2.0, AGPL-3.0, GPL-3.0, atau tidak terdeteksi) | Ya / Catatan |
| 4 | Gratis ($0) | Tidak ada biaya wajib, tidak ada API key berbayar yang wajib untuk fungsi dasar | Ya / Tidak |
| 5 | Tidak baca `.env` / vault | Baca SKILL.md dan README: tidak ada instruksi membaca `.env`, `~/.config/muse/vault/`, atau credential | Ya / Tidak |
| 6 | Tidak ada instruksi berbahaya | Tidak ada langkah untuk menyerang, spam, membobol, atau mengelabui deteksi/plagiarisme | Ya / Tidak |
| 7 | Tidak simpan secret | Skill tidak meminta token/password ditulis ke file repo, log, atau chat | Ya / Tidak |
| 8 | Deskripsi jujur | Deskripsi repo cocok dengan isi SKILL.md (bukan clickbait) | Ya / Tidak |

Kalau ada **satu saja** poin wajib jawabannya "Tidak" → **jangan pasang**. Catat alasannya di `docs/verification.md`.

## Checklist — poin catatan (boleh Ya dengan catatan)

- **Repo kecil** (di bawah 500 star): baca isi SKILL.md kata per kata sebelum dipakai produksi.
- **Terakhir update lama** (lebih dari 6 bulan): cek apakah masih cocok dengan versi alat sekarang.
- **Lisensi AGPL-3.0 / GPL-3.0**: boleh dipakai, tapi baca kewajiban lisensinya dulu. Jangan dipakai di proyek tertutup tanpa paham kewajibannya. Contoh yang sudah diketahui: `firecrawl/firecrawl` (AGPL-3.0), `trufflesecurity/trufflehog` (AGPL-3.0), `freqtrade/freqtrade` (GPL-3.0).
- **Layanan pihak ketiga**: contoh `useapi/muse-api` — bukan API resmi Meta. Evaluasi akun dan privasi dulu.
- **Arsip tidak resmi**: contoh `win4r/MuseAI-Skills` — referensi saja, jangan pasang mentah-mentah.

## Langkah audit

1. Buka repo upstream, catat star, bahasa, dan tanggal update terakhir.
2. Buka `SKILL.md` (atau satu subfolder contoh kalau paket besar).
3. Isi tabel checklist di atas.
4. Jalankan secret scan (wajib, lihat bagian "Secret scan" di bawah) pada file yang akan ditambahkan ke repo ini, dan pada seluruh repo sebelum push publik.
5. Kalau lolos → tambahkan ke `skills/index.md` dengan kolom status yang benar.
6. Kalau tidak lolos → tulis di bagian "Yang TIDAK kami pasang" di README, beserta alasannya.

## Secret scan (wajib sebelum push publik)

Alat: `gitleaks` 8.30.1 di `~/workspace/tools/gitleaks/gitleaks`, wrapper `~/workspace/tools/scan-secrets.sh`.

```text
~/workspace/tools/scan-secrets.sh ~/workspace/muse-rsi
~/workspace/tools/scan-secrets.sh --history ~/workspace/muse-rsi
```

Aturan: exit 0 = bersih, lanjut push. Exit 1 = ada kebocoran → **HALT, jangan push**. Hapus secret-nya dari file DAN dari history git (hapus file saja tidak cukup kalau secret sudah masuk commit), scan ulang sampai bersih, baru push. Jangan pernah menulis secret yang ketahuan ke chat, log, atau memory — sebutkan saja jenis dan lokasinya.

## Yang dilarang

- Menyalin isi SKILL.md upstream secara penuh ke repo ini. Cukup link + deskripsi 1 baris.
- Mengklaim skill upstream sebagai milik kami.
- Memasang skill ofensif (pentest, exploit, SMS bomber, jailbreak) dengan alasan apa pun.
- Memasang skill hanya karena star-nya besar, tanpa baca isinya.
