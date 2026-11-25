---
name: mikrotik-backup-snapshot
description: Buat backup konfigurasi MikroTik (.backup) dan simpan snapshot konfigurasi penting (JSON, untuk diff/dokumentasi) lewat tool MikroCLAW. Gunakan saat user minta "backup mikrotik", "simpan konfigurasi router", "snapshot config", "ekspor konfigurasi", atau "amankan setting sebelum perubahan".
---

# MikroTik Backup & Snapshot

Orkestrasi tool MikroCLAW (MCP server `mikroclaw`) untuk mengamankan konfigurasi.
Dua keluaran: (1) **backup biner** di router, (2) **snapshot JSON** konfigurasi
kunci ke file lokal (berguna untuk diff antar waktu, karena `/export` penuh tak
tersedia via REST).

## Prasyarat
- Membuat backup biner = operasi write → butuh `MIKROCLAW_ALLOW_WRITE=true`.
- Snapshot JSON murni read-only (selalu bisa dilakukan).
- Jika write nonaktif, lewati langkah backup biner dan lakukan snapshot saja —
  beri tahu user.

## Tool yang dipakai
- `mcp__mikroclaw__create_backup` — buat file .backup (write)
- `mcp__mikroclaw__list_files` — konfirmasi file backup ada + ukuran/waktu
- Snapshot read: `system_identity`, `system_resource`, `list_interfaces`,
  `list_ip_addresses`, `routing_table`, `firewall_filter_rules`,
  `firewall_nat_rules`, `address_lists`, `dhcp_servers`, `dhcp_leases`,
  `dns_settings`, `dns_static`, `ip_services`, `simple_queues`, `vlans`

## Prosedur
1. **Backup biner** (jika write aktif & user setuju): `create_backup` dengan `name`
   bermakna (mis. `pra-perubahan-<konteks>`). Lalu `list_files` untuk verifikasi file
   `.backup` muncul; laporkan nama, ukuran, waktu. Jika tak muncul → laporkan gagal.
2. **Snapshot JSON.** Panggil tool read di atas, gabungkan hasilnya menjadi satu objek
   JSON, dan tulis ke file lokal. Default lokasi: scratchpad atau path yang user minta,
   nama `mikrotik-snapshot-<identitas>.json`. Sertakan metadata (identitas, versi
   RouterOS) di dalamnya. (Catatan: jangan tulis ke repo tanpa diminta; snapshot bisa
   memuat data sensitif seperti static lease & address-list.)
3. **Ringkas.** Tampilkan ringkasan: backup biner (status) + path snapshot + jumlah
   item per kategori.

## Catatan keamanan
- Snapshot bisa berisi data sensitif. JANGAN kirim ke layanan eksternal; simpan lokal.
- `ppp_secrets`/kredensial sengaja TIDAK dimasukkan ke snapshot default; tambahkan
  hanya bila user secara eksplisit memintanya dan paham risikonya.
- Untuk restore penuh, gunakan file `.backup` di router (via Winbox/CLI) — snapshot
  JSON adalah referensi/diff, bukan format restore otomatis.

## Format keluaran
```
## Backup & Snapshot — <router>
- Backup biner: ✅ <nama>.backup (<ukuran>, <waktu>) | ⏭️ dilewati (write nonaktif)
- Snapshot JSON: <path> (<n> kategori, <total item>)

Disarankan: jalankan ini SEBELUM setiap perubahan konfigurasi besar.
```
