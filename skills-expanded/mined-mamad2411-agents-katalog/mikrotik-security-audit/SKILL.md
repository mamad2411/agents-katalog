---
name: mikrotik-security-audit
description: Audit hardening keamanan MikroTik — service terbuka (telnet/ftp/api/www/winbox), user & grup, sesi login aktif, sertifikat kedaluwarsa, DNS allow-remote-requests, dan proteksi chain input firewall, lewat tool MikroCLAW. Gunakan saat user minta "audit keamanan mikrotik", "security check router", "hardening mikrotik", "cek celah keamanan", atau "apakah router aman".
---

# MikroTik Security Audit

Orkestrasi tool MikroCLAW (MCP server `mikroclaw`) untuk menilai postur keamanan
router terhadap praktik hardening MikroTik. **Read-only**; remediasi hanya dengan
persetujuan eksplisit + `MIKROCLAW_ALLOW_WRITE=true`.

## Tool yang dipakai
- `mcp__mikroclaw__ip_services` — service IP aktif + batasan `address`
- `mcp__mikroclaw__router_users` + `mcp__mikroclaw__user_groups` — akun & hak akses
- `mcp__mikroclaw__active_sessions` — siapa sedang login
- `mcp__mikroclaw__certificates` — masa berlaku sertifikat
- `mcp__mikroclaw__dns_settings` — allow-remote-requests
- `mcp__mikroclaw__firewall_filter_rules` — proteksi chain input
- `mcp__mikroclaw__ip_cloud` — apakah router terekspos publik
- `mcp__mikroclaw__system_packages` / `routerboard_info` — versi (CVE/patch)

## Daftar periksa
1. **Service berbahaya.** `ip_services`: `telnet`, `ftp`, `www` (HTTP polos),
   `api` (non-TLS) sebaiknya **disabled**. Untuk yang aktif (ssh/winbox/api-ssl/www-ssl),
   cek apakah `address=` membatasi sumber. Service aktif tanpa batasan = 🔴.
2. **User.** `router_users`: adakah user `admin` default masih ada/aktif? Berapa user
   ber-grup `full`? `user_groups`: grup dengan policy berlebih. Soroti.
3. **Sesi aktif.** `active_sessions`: login yang tidak dikenal / dari alamat asing = 🔴.
4. **Sertifikat.** `certificates`: yang `invalid-after` mendekati/lewat = ⚠️/🔴.
5. **DNS.** `dns_settings`: `allow-remote-requests=yes` TANPA firewall yang memblok
   UDP/TCP 53 dari WAN → risiko open resolver/amplifikasi = 🔴.
6. **Firewall input.** `firewall_filter_rules`: pastikan chain `input` punya default
   drop & hanya mengizinkan layanan mgmt dari subnet tepercaya.
7. **Eksposur publik.** `ip_cloud`: jika ada IP publik, manajemen WAN harus tertutup.
8. **Versi.** `routerboard_info`/`system_packages`: versi lama = potensi kerentanan;
   sarankan update.

## Format laporan
```
## Security Audit — <router>
Skor postur: <ringkas, mis. "Perlu perhatian">

### Temuan (urut severity)
- 🔴 [KRITIS] Telnet aktif & terbuka ke semua (ip_services .id=*X) → matikan.
- 🟡 [SEDANG] Sertifikat 'https' kedaluwarsa dalam 12 hari.
- 🟢 [INFO] …

### Rekomendasi hardening (langkah konkret)
1. … (sebut tool remediasi)
```

## Remediasi (opsional, butuh izin)
Hanya bila user setuju & write aktif:
- Matikan service berisiko: `mcp__mikroclaw__set_ip_service_enabled` (enabled=false)
- Perketat firewall: `mcp__mikroclaw__add_firewall_drop` / `add_address_list_entry`
Tampilkan rencana + minta konfirmasi sebelum eksekusi. Jangan pernah mengunci akses
Anda sendiri (mis. memblok subnet tempat sesi audit ini berjalan) — peringatkan user.
