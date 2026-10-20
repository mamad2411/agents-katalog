---
name: mikrotik-role-detect
description: Deteksi peran/fungsi yang sedang dijalankan perangkat MikroTik — gateway NAT, firewall, BGP/OSPF router, switch/AP, BRAS PPPoE, konsentrator VPN, DHCP/DNS, QoS, dll — lewat tool MikroCLAW, lalu jelaskan bukti & keyakinannya. Gunakan saat user minta "deteksi peran mikrotik", "router ini berfungsi sebagai apa", "peran perangkat", "fungsi mikrotik ini apa saja", "apakah router ini jadi BGP/firewall/AP", atau "klasifikasikan router".
---

# MikroTik Role Detection

Mengenali **peran apa saja** yang sedang dijalankan sebuah perangkat MikroTik dan
menjelaskan **bukti** di balik tiap kesimpulan. **Read-only.**

## Tool yang dipakai
- `mcp__mikroclaw__detect_roles` — **inti**: mengumpulkan bukti dari banyak menu
  RouterOS lalu mengklasifikasikan peran (nama/kategori/keyakinan/bukti).
- `mcp__mikroclaw__system_resource` & `mcp__mikroclaw__system_identity` — konteks
  perangkat (model, versi, uptime).
- *(opsional, untuk memperdalam temuan)* tool spesifik per peran:
  `bgp_sessions`, `ospf_neighbors`, `firewall_nat_rules`, `firewall_filter_rules`,
  `wifi_interfaces`, `capsman_remote_caps`, `ppp_active`, `wireguard_peers`,
  `ipsec_active_peers`, `dhcp_servers`, `simple_queues`, `vlans`.

## Prosedur
1. **Deteksi.** Panggil `detect_roles`. Ini sudah memberi `peran[]`
   (nama, kategori, keyakinan: tinggi/sedang/rendah, bukti[]) + `ringkasan`.
2. **Konteks.** Sebutkan identitas, model, versi RouterOS (dari `system_resource`/
   `system_identity`) agar laporan jelas merujuk perangkat mana.
3. **Kelompokkan** peran per kategori (Routing & NAT, Keamanan, Switching,
   Wireless, Broadband, Layanan jaringan, VPN & tunnel, QoS, Ketersediaan).
4. **Perdalam bila perlu.** Untuk peran berkeyakinan "sedang", atau bila user minta
   detail, panggil tool spesifiknya (mis. `bgp_sessions` untuk peran BGP) dan kutip
   angka konkret (jumlah peer, sesi aktif, dst.).
5. **Simpulkan peran dominan.** Tebak fungsi utama perangkat (mis. "edge router +
   firewall + gateway NAT", atau "BRAS PPPoE", atau "AP terkelola CAPsMAN").

## Format laporan
```
## Peran MikroTik — <identitas> (RouterOS <versi>, <model>)
**Ringkasan:** <fungsi dominan dalam 1 kalimat>

| Peran | Kategori | Keyakinan | Bukti |
|-------|----------|-----------|-------|
| Gateway internet (NAT) | Routing & NAT | tinggi | 3 aturan masquerade |
| Firewall (stateful)    | Keamanan      | tinggi | 24 aturan, proteksi input |
| BGP router             | Routing dinamis | tinggi | 2 sesi BGP |
| …                      | …             | …         | … |

**Catatan:** <peran berkeyakinan sedang / yang perlu dikonfirmasi manual>
```

Selalu:
- Tampilkan **bukti**, bukan hanya label — agar kesimpulan bisa diverifikasi.
- Bedakan **keyakinan tinggi** (bukti kuat) vs **sedang** (indikasi tak langsung).
- Bila `detect_roles` mengembalikan 0 peran, nyatakan perangkat kemungkinan masih
  minimal/baru — jangan menebak-nebak.
- Jangan mengubah konfigurasi (skill ini murni read-only).
