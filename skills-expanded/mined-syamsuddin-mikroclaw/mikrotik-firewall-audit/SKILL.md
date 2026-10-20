---
name: mikrotik-firewall-audit
description: Audit & monitoring firewall MikroTik — tinjau aturan filter/NAT/mangle, address-list, dan koneksi aktif lewat tool MikroCLAW, deteksi aturan berisiko/usang, beri rekomendasi. Gunakan saat user minta "audit firewall", "cek/monitor firewall mikrotik", "firewall monitoring", "review NAT / port forward", atau "firewall security check".
---

# MikroTik Firewall Audit

Orkestrasi tool MikroCLAW (MCP server `mikroclaw`) untuk meninjau postur firewall
router dan menghasilkan laporan temuan + rekomendasi. **Read-only**; jangan
mengubah apa pun tanpa persetujuan eksplisit user.

## Tool yang dipakai
- `mcp__mikroclaw__firewall_filter_rules` — aturan filter (input/forward/output)
- `mcp__mikroclaw__firewall_nat_rules` — NAT (port-forward & masquerade)
- `mcp__mikroclaw__firewall_mangle` — marking
- `mcp__mikroclaw__address_lists` — isi address-list
- `mcp__mikroclaw__firewall_connections` — connection tracking aktif
- `mcp__mikroclaw__ip_services` — service yang terbuka (cross-check)
- `mcp__mikroclaw__recent_logs` — hits drop / indikasi brute force

## Prosedur
1. **Filter rules.** Ambil `firewall_filter_rules`. Periksa:
   - Apakah chain `input` melindungi router (drop default di akhir, izin terbatas
     untuk mgmt: winbox/ssh/api dari subnet tepercaya saja)?
   - Apakah ada aturan `accept` terlalu longgar (src & dst `any`, tanpa batasan)?
   - Aturan `disabled=yes` yang menumpuk (usang) — tandai.
   - Aturan tanpa `comment` (sulit diaudit) — tandai.
   - Urutan: apakah ada accept di atas drop yang membuat drop tak pernah kena?
2. **NAT.** Ambil `firewall_nat_rules`. Daftarkan semua `dstnat` (port-forward):
   port publik → IP/port internal. Soroti yang membuka layanan sensitif (mis. 22,
   3389, 23) ke `dst-address` WAN. Cek `srcnat`/`masquerade` keluar interface mana.
3. **Address-list.** Ambil `address_lists`. Soroti list besar, entri tanpa
   `timeout` yang seharusnya sementara, dan entri tanpa comment.
4. **Koneksi aktif.** Ambil `firewall_connections`. Ringkas top sumber/tujuan &
   protokol; soroti pola mencurigakan (banyak koneksi keluar ke 1 host, port tak lazim).
5. **Konsistensi layanan.** Bandingkan `ip_services` (service enabled + port) dengan
   filter: adakah service aktif yang TIDAK dibatasi firewall maupun `address=`?
6. **Log.** Ambil `recent_logs` (limit 100). Cari lonjakan drop / percobaan login.

## Format laporan
```
## Ringkasan Firewall
- Filter rules: N total (M aktif, K disabled)
- Port-forward (dstnat): ...
- Default-drop input: ya/tidak

## Temuan (urut severity)
- 🔴 [TINGGI] ...  (rule .id, kenapa berisiko, dampak)
- 🟡 [SEDANG] ...
- 🟢 [INFO] ...

## Rekomendasi
1. ... (sebut tool remediasi bila relevan)
```

## Remediasi (opsional, butuh izin)
Hanya jika user setuju DAN `MIKROCLAW_ALLOW_WRITE=true`:
- Nonaktifkan aturan berisiko: `mcp__mikroclaw__set_firewall_rule_enabled`
- Hapus aturan usang: `mcp__mikroclaw__delete_firewall_rule`
- Blokir sumber jahat: `mcp__mikroclaw__add_firewall_drop` / `add_address_list_entry`
Selalu tampilkan rencana perubahan dan minta konfirmasi sebelum mengeksekusi.
