---
name: mikrotik-chronicle
description: Mesin waktu konfigurasi MikroTik — simpan snapshot konfigurasi relevan-keamanan, lalu bandingkan dengan kondisi sekarang untuk mendeteksi PERUBAHAN tak terjadwal & menilai RISIKO-nya (user baru, port manajemen dibuka, scheduler/script persistensi, aturan drop dimatikan, open resolver) lewat tool MikroCLAW. Gunakan saat user minta "apa yang berubah di konfigurasi?", "deteksi perubahan tak terjadwal", "ada backdoor / jejak intrusi?", "audit perubahan config", "bandingkan config dengan kemarin", atau "siapa mengubah firewall".
---

# MikroTik Chronicle — Mesin Waktu Konfigurasi

Mengubah backup pasif menjadi **tata-kelola perubahan aktif**: snapshot konfigurasi
relevan-keamanan, lalu **diff + penilaian risiko** untuk mendeteksi perubahan
tak terjadwal / jejak kompromi. **Read-only terhadap router** (snapshot disimpan
di disk lokal operator).

## Tool yang dipakai
- `mcp__mikroclaw__config_snapshot` — ambil & simpan snapshot kanonik ber-hash
  (firewall/NAT, service, user/grup, scheduler/script, DNS, address-list) ke
  `MIKROCLAW_STATE_DIR/snapshots`. Beri `label` (mis. "sebelum-maintenance").
- `mcp__mikroclaw__config_diff` — bandingkan konfigurasi LIVE vs snapshot terakhir,
  beri `perubahan[]` dengan `risiko` (severity + alasan) per item, `keparahan_tertinggi`.
- *(konteks opsional)* `system_history` (undo RouterOS), `recent_logs`,
  `active_sessions`, `router_users` untuk korelasi "siapa & kapan".

## Prosedur
1. **Tetapkan baseline.** Jika belum ada snapshot, panggil `config_snapshot`
   (mis. label "baseline"). Jelaskan ini titik referensi.
2. **Bandingkan.** Panggil `config_diff`. Bila baru pertama kali, ia membuat
   baseline & memberi tahu untuk dijalankan lagi nanti.
3. **Nilai risiko.** Untuk tiap perubahan, baca `risiko.severity` + `alasan`.
   Fokuskan ke **critical** (user baru, port manajemen 22/8291/dst dibuka ke
   0.0.0.0/0, pembatasan service dihapus) — ini ciri backdoor pasca-kompromi.
4. **Korelasi.** Untuk perubahan mencurigakan, cek `recent_logs` & `active_sessions`
   sekitar waktu itu, dan `system_history`, untuk menebak siapa/kapan/apakah sah.
5. **Rekomendasi.** Untuk perubahan tak sah: sarankan undo (`system/history`),
   nonaktifkan user/aturan asing, dan rotasi kredensial. Untuk yang sah: catat &
   buat snapshot baru sebagai baseline.

## Format laporan
```
## Chronicle — Diff Konfigurasi
**Pembanding:** snapshot 2026-06-27 14:02 (hash a1b2…) → sekarang
**Status:** 🔴 3 perubahan (tertinggi: critical)

| Bagian | Jenis | Identitas | Risiko | Alasan |
|--------|-------|-----------|--------|--------|
| user | ditambah | svc-backup | 🔴 critical | User baru tak terjadwal — bisa backdoor |
| firewall_filter | ditambah | input/accept :8291 | 🔴 critical | Winbox dibuka tanpa batasan sumber |
| ip_service | diubah | www | 🟠 warning | Diaktifkan kembali |

**Korelasi:** perubahan jam 02:14, sesi login dari IP asing → DUGAAN INTRUSI.
**Saran:** isolasi, undo via system/history, rotasi semua kredensial admin.
```

Selalu:
- Tampilkan **alasan risiko**, bukan hanya daftar diff.
- Bedakan perubahan **sah** (maintenance terjadwal) vs **mencurigakan** (di luar jam,
  membuka akses, menambah persistensi).
- Tindakan korektif yang mengubah router butuh `MIKROCLAW_ALLOW_WRITE=true` + konfirmasi.
