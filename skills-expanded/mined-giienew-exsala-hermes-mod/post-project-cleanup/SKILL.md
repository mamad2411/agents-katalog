---
name: post-project-cleanup
description: Use when task done. Kill stray procs, rm temp, verify prod.
---

# Post-Project Cleanup

Setiap project/task SELESAI = wajib cleanup. Jangan tutup kerjaan dengan sampah tertinggal.

## Checklist (urutan)

1. **Kill proses liar** yang dibuat buat kerjaan ini:
   - headless Chrome: `pkill -9 -f chrome`
   - node/CLI spawner yang re-spawn process: `pkill -9 -f '<nama-scraper>'; pkill -9 -f 'index.js'`
   - server test/API lokal yang tidak perlu jalan lagi
   - cek jejak: `pgrep -fa '<nama>'` harus kosong sebelum bilang selesai

2. **Ukur RAM bebas** sebelum & sesudah cleanup:
   `free -m` → bebas harus naik signifikan; kalau masih minus → cari pemakan (`ps aux --sort=-%mem | head`)

3. **Hapus file temp**: isi `~/app/cache/scratch/`, folder project mati di home.
   Hati-hati: cek `du -sh` dulu, jangan hapus folder yang masih dipakai daemon.

4. **Verifikasi layanan produksi AMAN** sebelum tutup:
   - 9router pola: cek `pm2 status` hijau, kalau daemon menjalani live `main` process, jangan diapa-apain.
   - Kalau ada service yang sempat terganggu, confirm jalan normal lagi.

5. **Report jujur**: sebutkan berapa RAM dibebaskan, proses apa yang dibunuh, apa yang masih jalan.

## Pitfall (kejadian nyata)

- **Jangan pernah anggap job CF-clearance-scraper aman**: `createBrowser()`-nya bisa memunculkan ~174 proses Chrome sekaligus (recurcive resspawn) → RAM 1-3MB → OOM → proses lain (misal 9router) ikut di-`kill -9` oleh sistem.
  Gejala: `pgrep -c chrome` > 50 + `free -m` bebas di bawah 200MB.
  Obat: `pkill -9 -f chrome` + `pkill -9 -f 'cf-clearance|index.js'` + verifikasi `pgrep` bersih.
- **pkill -f pakai pola longgar**: `pkill -9 -f 'index.js'` bisa membunuh job node lain — cek `pgrep -fa` dulu sebelum pkill, target pola se-spesifik mungkin.
- **Xvfb & PM2 wajar tersisa**: Xvfb>1 duplikat boleh dibiarkan, PM2 = pengelola layanan produksi, jangan dibunuh.

## Trigger
Kalau user bilang project kelar, dimit, dibatalkan, atau minta "cleanup" — jalankan checklist ini.
