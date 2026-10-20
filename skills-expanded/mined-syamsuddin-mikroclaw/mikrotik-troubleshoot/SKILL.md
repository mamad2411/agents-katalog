---
name: mikrotik-troubleshoot
description: Diagnosa masalah konektivitas MikroTik secara metodis (lapisan fisik → IP → DNS → firewall) memakai ping/traceroute, status WAN, routing, dan DNS lewat tool MikroCLAW. Gunakan saat user bilang "internet mati", "tidak bisa browsing", "router bermasalah", "troubleshoot koneksi mikrotik", "DNS tidak jalan", atau "kenapa tidak konek".
---

# MikroTik Troubleshooting

Orkestrasi tool MikroCLAW (MCP server `mikroclaw`) untuk mendiagnosis gangguan
konektivitas secara berlapis dan menyimpulkan akar masalah. **Read-only**.

Jika user menyebut gejala/target spesifik (mis. "tidak bisa buka youtube",
"klien 192.168.88.50 tak dapat internet"), fokuskan diagnosa ke sana.

## Tool yang dipakai
- `mcp__mikroclaw__list_interfaces` — status fisik/up-down
- `mcp__mikroclaw__dhcp_client` + `mcp__mikroclaw__ip_cloud` — WAN/IP publik
- `mcp__mikroclaw__list_ip_addresses` + `mcp__mikroclaw__routing_table` — IP & default route
- `mcp__mikroclaw__ping` + `mcp__mikroclaw__traceroute` — uji jangkauan & jalur
- `mcp__mikroclaw__dns_settings` + `mcp__mikroclaw__dns_cache` — resolusi nama
- `mcp__mikroclaw__firewall_connections` + `mcp__mikroclaw__firewall_filter_rules` — blokir?
- `mcp__mikroclaw__interface_traffic_live` — apakah ada trafik mengalir
- `mcp__mikroclaw__recent_logs` — petunjuk (link down, DHCP gagal, dst.)

## Alur diagnosa (berhenti di lapisan yang gagal)
1. **L1/L2 — interface.** `list_interfaces`: interface WAN & LAN `running`? Jika WAN
   down → masalah fisik/ISP; cek `recent_logs` untuk "link down".
2. **L3 — alamat WAN.** `dhcp_client`/`ip_cloud`: dapat IP dari ISP? Tidak dapat IP →
   masalah WAN/PPPoE/DHCP ke ISP.
3. **L3 — default route.** `routing_table`: ada default route `0.0.0.0/0` & gateway
   reachable? `ping` ke gateway. Gagal → masalah uplink.
4. **Internet mentah.** `ping 8.8.8.8` (IP, bukan nama). Sukses tapi nama gagal →
   lompat ke DNS. Gagal → `traceroute 8.8.8.8` untuk lihat di hop mana putus.
5. **DNS.** `dns_settings` (server terisi & valid?), lalu `ping` nama domain
   (mis. `google.com`). Domain gagal padahal IP sukses = **masalah DNS**. Cek juga
   `allow-remote-requests` & `dns_cache`.
6. **Firewall.** Bila trafik tertentu terblokir, `firewall_filter_rules` &
   `firewall_connections`: cari aturan drop/reject yang relevan dengan target/klien.
7. **Trafik.** `interface_traffic_live` pada interface terkait untuk konfirmasi
   ada/tidaknya aliran data.

## Format keluaran
```
## Diagnosa Konektivitas
Gejala: <ringkas dari user>

### Hasil per lapisan
- L1/L2 interface: ✅/❌ …
- WAN IP: ✅/❌ …
- Default route + gateway ping: ✅/❌ …
- Ping 8.8.8.8: ✅/❌ …
- Resolusi DNS: ✅/❌ …
- Firewall: …

### Kesimpulan
Akar masalah paling mungkin: **…**

### Langkah perbaikan
1. … (read-only; sarankan perubahan, jangan eksekusi tanpa izin)
```
Simpulkan akar masalah pada lapisan PERTAMA yang gagal — jangan teruskan uji lapisan
di atasnya jika dasar sudah putus. Sebutkan asumsi bila data tidak konklusif.
