---
name: mikrotik-sentinel
description: Deteksi perangkat terinfeksi/berperilaku jahat di jaringan MikroTik — botnet IoT (Telnet keluar/Mirai), penambang kripto, bot spam, pemindaian — dari pola koneksi (connection-tracking), tanpa signature, dengan konteks kelas perangkat (kamera/IoT/ponsel/server), lewat tool MikroCLAW. Gunakan saat user minta "ada perangkat terinfeksi?", "cek botnet di jaringan", "kenapa CCTV/IoT ini aneh", "deteksi malware jaringan", "perangkat mencurigakan", atau "ada yang scanning?".
---

# MikroTik Sentinel — Sidik-Jari Perilaku Perangkat

Membangun **profil perilaku tiap klien** dari connection-tracking lalu menilai
deviasi **dalam konteks tipe perangkat** — menangkap perangkat yang dikompromi
tanpa bergantung pada signature. **Read-only.**

## Tool yang dipakai
- `mcp__mikroclaw__analyze_client_behavior` — **inti**: profil per-IP (tujuan unik,
  port, protokol) dari `/ip/firewall/connection`, tebak kelas perangkat via OUI,
  lalu nilai pola jahat (botnet Telnet, miner, spam, scan) berkonteks perangkat.
  Beri `ip` untuk fokus satu klien, atau kosong untuk semua.
- *(konteks opsional)* `dhcp_leases`, `arp_table`, `firewall_connections` untuk
  detail mentah; `address_lists` untuk cek apakah sudah dikarantina.

## Prosedur
1. **Pindai.** Panggil `analyze_client_behavior` (tanpa `ip`) untuk laporan semua
   klien, terurut tingkat keparahan. Perhatikan `keparahan_tertinggi`.
2. **Telaah tiap temuan.** Untuk klien mencurigakan, baca `temuan[]` dan `profil`
   (mis. 30 koneksi Telnet keluar dari sebuah Hikvision = ciri kuat botnet IoT).
   Tekankan **konteks perangkat**: perilaku yang wajar untuk PC bisa sangat
   mencurigakan untuk kamera/IoT.
3. **Verifikasi.** Bila perlu, lihat `firewall_connections` mentah untuk
   mengonfirmasi tujuan/port, dan `arp_table`/`dhcp_leases` untuk identitas fisik.
4. **Rekomendasi berlapis.** Sarankan tindakan: karantina via address-list,
   blokir IP, isolasi VLAN, ganti kredensial default perangkat IoT, update firmware.
5. **Tawarkan remediasi (gated).** Eksekusi nyata (mis. `add_address_list_entry`
   untuk karantina, `add_firewall_drop`) butuh `MIKROCLAW_ALLOW_WRITE=true` dan
   konfirmasi user. Sarankan `config_snapshot` sebelum mengubah.

## Format laporan
```
## Sentinel — Analisis Perilaku Perangkat
**Status:** ⚠️ 2 perangkat mencurigakan (tertinggi: critical)

| IP | Perangkat | Kelas | Keparahan | Temuan utama |
|----|-----------|-------|-----------|--------------|
| 192.168.1.50 | cam1 (Hikvision) | kamera/CCTV | 🔴 critical | 30 koneksi Telnet keluar — rekrutmen botnet |
| 192.168.1.30 | pc-gudang | tak dikenal | 🟠 warning | koneksi ke port pool penambang kripto |

**192.168.1.50 — detail:** profil 30 tujuan unik, semua port 23. Kamera normal
hanya bicara dengan 1 NVR → sangat tidak wajar. **Saran:** karantina segera +
ganti password default + cek firmware.
```

Selalu:
- Jelaskan **mengapa** mencurigakan dalam konteks kelas perangkat, bukan label saja.
- Akui **positif palsu mungkin** (P2P/CDN bisa fan-out tinggi) — minta verifikasi
  sebelum tindakan drastis.
- Jangan mengubah konfigurasi tanpa langkah write eksplisit + konfirmasi user.
