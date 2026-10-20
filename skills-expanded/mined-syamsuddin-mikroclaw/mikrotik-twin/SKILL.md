---
name: mikrotik-twin
description: Simulator "what-if" paket MikroTik — telusuri nasib sebuah paket (diteruskan/drop) menembus mangle→NAT→routing→filter, dan uji dampak satu aturan firewall BARU sebelum diterapkan, lewat tool MikroCLAW (read-only, tak menyentuh router). Gunakan saat user minta "kalau klien X akses Y lolos atau diblok", "simulasikan paket", "uji aturan firewall sebelum pasang", "what-if firewall", "kenapa koneksi ini ke-drop", atau "aturan ini bakal blokir apa".
---

# MikroTik Twin — Simulator What-If Paket

Menelusuri perjalanan **paket hipotetis** menembus ruleset LIVE router dan
melaporkan verdict + jejak tiap tahap — serta menguji **dampak aturan firewall
baru SEBELUM diterapkan**. **100% read-only**: tak ada perubahan pada router.

## Tool yang dipakai
- `mcp__mikroclaw__simulate_packet` — **inti**: telusuri satu paket (src, dst,
  protocol, dst_port, in_interface, state) melalui mangle → dst-nat → keputusan
  routing (input vs forward) → filter (ikuti jump/return) → src-nat. Mengembalikan
  `verdict`, `jejak[]`, `dst_efektif`, `dst_nat`, `src_nat`, `chain`.
- `mcp__mikroclaw__simulate_firewall_change` — sisipkan satu `new_rule` hipotetis
  lalu bandingkan verdict **sebelum vs sesudah** (apakah & bagaimana berubah).
- *(konteks opsional)* `firewall_filter_rules`, `firewall_nat_rules`,
  `firewall_mangle`, `routing_table`, `address_lists` untuk mengutip aturan asli.

## Prosedur
1. **Pahami pertanyaan.** Terjemahkan permintaan user menjadi spesifikasi paket:
   siapa sumber (IP klien), tujuan (IP/host), protokol & port, arah (in_interface),
   dan apakah uji koneksi BARU (`state=new`, default) atau balasan (`established`).
2. **Simulasikan.** Panggil `simulate_packet`. Baca `verdict` dan **telusuri
   `jejak[]`** untuk menjelaskan KENAPA — aturan mana (indeks/comment) yang
   memutuskan, apakah lewat dst-nat/src-nat, masuk chain input atau forward.
3. **Uji perubahan (bila diminta).** Untuk "kalau saya pasang rule ini?", panggil
   `simulate_firewall_change` dengan `new_rule` gaya RouterOS dan laporkan
   `berubah` + `dampak` (mis. DITERUSKAN → DI-DROP).
4. **Jelaskan dengan bahasa manusia.** Bukan sekadar verdict — ceritakan alur:
   "paket masuk dari LAN, tak ada dst-nat, diputuskan forward, cocok aturan #4
   (drop port 22) → diblokir."
5. **Saran tindak lanjut.** Bila user ingin menerapkan perubahan yang sudah
   tervalidasi, ingatkan itu butuh `MIKROCLAW_ALLOW_WRITE=true` dan tool write
   (mis. `add_firewall_drop`), serta sarankan `config_snapshot` dulu.

## Format laporan
```
## Twin — Simulasi Paket
**Paket:** 192.168.88.10 → 8.8.8.8 tcp/443 (state=new, masuk ether2)
**Verdict:** ✅ DITERUSKAN (chain forward)

**Jejak:**
1. mangle prerouting — (tak ada mark)
2. dst-nat — tidak ada
3. routing — dst 8.8.8.8 via default route → out ether1 (transit/forward)
4. filter forward — cocok #3 "allow lan-out" (accept) → BERHENTI
5. src-nat — masquerade #1 (out ether1) → disamarkan

**Kesimpulan:** koneksi diizinkan & di-NAT keluar normal.
```
Untuk uji perubahan, tampilkan **Sebelum → Sesudah** dan apakah nasib paket berubah.

Selalu:
- Tunjukkan **jejak & aturan pemicu**, bukan cuma verdict — agar bisa diverifikasi.
- Ingatkan bahwa ini **model yang berguna, bukan replika sempurna** RouterOS
  (fitur tepi seperti interface-list/layer7 diabaikan & ditandai pada jejak).
- Murni read-only; tak pernah mengubah konfigurasi tanpa langkah write eksplisit.
