---
name: mikrotik-health-check
description: Laporan kesehatan & maintenance perangkat MikroTik — versi/uptime, CPU/RAM/disk, suhu/tegangan, status firmware & update paket, status interface, status WAN, dan sinkronisasi waktu, lewat tool MikroCLAW. Gunakan saat user minta "cek kesehatan mikrotik", "health check router", "status router", "apakah ada update routeros", atau "kondisi perangkat".
---

# MikroTik Health Check

Orkestrasi tool MikroCLAW (MCP server `mikroclaw`) untuk potret kesehatan router.
**Read-only** (kecuali user minta tindakan). Beri indikator status per area.

## Tool yang dipakai
- `mcp__mikroclaw__system_resource` — versi, uptime, CPU, RAM, disk, board
- `mcp__mikroclaw__system_health` — suhu, tegangan, kipas (jika ada)
- `mcp__mikroclaw__routerboard_info` — firmware terpasang vs tersedia
- `mcp__mikroclaw__check_for_updates` — update RouterOS dari channel
- `mcp__mikroclaw__system_packages` — paket terpasang/disabled
- `mcp__mikroclaw__system_license` — level lisensi/CHR
- `mcp__mikroclaw__list_interfaces` — interface running/down
- `mcp__mikroclaw__ip_cloud` + `mcp__mikroclaw__dhcp_client` — status WAN/IP publik
- `mcp__mikroclaw__ntp_client` — sinkronisasi waktu
- `mcp__mikroclaw__recent_logs` — error/warning terbaru

## Prosedur
1. **Sistem.** `system_resource`: catat versi RouterOS, uptime, free-memory vs
   total, free-hdd-space, cpu-load. Tandai ⚠️ jika cpu-load tinggi, memori/disk < 15%.
2. **Sensor.** `system_health`: suhu/voltase di luar normal → ⚠️/❌. (Kosong = board
   tak punya sensor, tandai informasi saja.)
3. **Firmware & update.** `routerboard_info` (current vs upgrade firmware),
   `check_for_updates` (installed vs latest), `system_packages`. Sarankan upgrade
   bila ada selisih versi.
4. **Lisensi.** `system_license` (relevan untuk CHR).
5. **Interface.** `list_interfaces`: hitung berapa running vs disabled vs down;
   soroti interface penting yang down dan error/drop counter tinggi.
6. **WAN.** `dhcp_client` & `ip_cloud`: pastikan ada IP WAN & IP publik; tandai bila
   tidak dapat IP.
7. **Waktu.** `ntp_client`: pastikan tersinkron (penting untuk log/sertifikat).
8. **Log.** `recent_logs` (limit 50): kutip error/warning yang menonjol.

## Format laporan
```
## Health Check — <identitas router> (RouterOS <versi>, uptime <…>)
| Area        | Status | Catatan |
|-------------|--------|---------|
| CPU/Memori  | ✅/⚠️/❌ | … |
| Penyimpanan | …      | … |
| Suhu/Daya   | …      | … |
| Firmware    | …      | terpasang X, tersedia Y |
| Update OS   | …      | … |
| Interface   | …      | N running / M down |
| WAN         | …      | IP publik … |
| Waktu (NTP) | …      | … |

## Tindakan disarankan
1. …
```
Selalu sebutkan jika suatu data tidak tersedia (mis. sensor/paket tidak ada),
bukan menganggapnya error.
