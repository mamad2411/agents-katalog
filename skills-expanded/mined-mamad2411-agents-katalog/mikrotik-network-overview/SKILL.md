---
name: mikrotik-network-overview
description: Snapshot inventaris jaringan MikroTik — identitas perangkat, WAN/IP publik, subnet LAN, interface & VLAN, tabel routing, klien terhubung (DHCP/ARP), dan tetangga, lewat tool MikroCLAW. Gunakan saat user minta "overview jaringan", "peta jaringan mikrotik", "inventaris router", "dokumentasi konfigurasi jaringan", atau "ringkasan topologi".
---

# MikroTik Network Overview

Orkestrasi tool MikroCLAW (MCP server `mikroclaw`) untuk membuat potret menyeluruh
konfigurasi jaringan — berguna untuk dokumentasi & onboarding. **Read-only**.

## Tool yang dipakai
- `mcp__mikroclaw__system_identity` + `mcp__mikroclaw__system_resource` — identitas & versi
- `mcp__mikroclaw__list_interfaces` + `mcp__mikroclaw__ethernet_ports` + `mcp__mikroclaw__vlans` — interface & VLAN
- `mcp__mikroclaw__list_ip_addresses` — subnet & IP
- `mcp__mikroclaw__dhcp_client` + `mcp__mikroclaw__ip_cloud` — WAN/IP publik
- `mcp__mikroclaw__routing_table` — route (default & statis)
- `mcp__mikroclaw__dhcp_servers` + `mcp__mikroclaw__dhcp_leases` — layanan & klien DHCP
- `mcp__mikroclaw__arp_table` + `mcp__mikroclaw__bridge_ports` — L2/host
- `mcp__mikroclaw__neighbors` — perangkat MikroTik/LLDP sekitar
- `mcp__mikroclaw__dns_settings` — DNS

## Prosedur
1. **Identitas.** `system_identity` + `system_resource` → nama, model, RouterOS, uptime.
2. **WAN.** `dhcp_client` + `ip_cloud` → interface WAN, IP WAN, IP publik/DDNS, gateway.
3. **Interface & L2.** `list_interfaces`, `ethernet_ports` (link speed), `bridge_ports`
   (komposisi bridge), `vlans` (vlan-id & induk).
4. **IP/LAN.** `list_ip_addresses` → daftar subnet per interface.
5. **Routing.** `routing_table` → default route & route statis penting.
6. **DHCP & klien.** `dhcp_servers` (scope per interface) + `dhcp_leases` → jumlah &
   daftar klien. Korelasikan dengan `arp_table` untuk MAC/host.
7. **Tetangga.** `neighbors` → perangkat lain di L2.
8. **DNS.** `dns_settings` → resolver.

## Format laporan
```
## Network Overview — <identitas> (RouterOS <versi>)

### WAN
- Interface: …  IP WAN: …  IP publik: …  Gateway: …

### LAN / Subnet
| Interface | IP/CIDR | VLAN | DHCP | # Klien |
|-----------|---------|------|------|---------|

### Interface fisik (link)
…

### Routing utama
- default → … ; route statis: …

### Klien terhubung (ringkas)
- N lease aktif (tabel: IP, MAC, host, expires)

### Tetangga terdeteksi
…
```
Sajikan ringkas namun cukup untuk dipakai sebagai dokumentasi. Tawarkan ekspor ke
file Markdown bila user mau menyimpannya.
