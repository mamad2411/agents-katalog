---
name: mikrotik-concierge
description: Laporan bisnis untuk operator RT-RW net / hotspot / warnet berbasis MikroTik — terjemahkan telemetri jaringan menjadi keputusan bisnis: jumlah & status pelanggan PPPoE/hotspot, akun menganggur (bisa ditagih/dicabut), perangkat tak terotentikasi (dugaan pencurian bandwidth), utilisasi WAN vs kapasitas paket (kapan upgrade), dan top talkers, lewat tool MikroCLAW. Gunakan saat user minta "laporan bisnis", "berapa pelanggan aktif", "ada yang nyolong bandwidth?", "perlu upgrade paket internet?", "akun mana yang nganggur", "siapa pemakai terbesar", atau "kapasitas WAN cukup tidak".
---

# MikroTik Concierge — Penerjemah Jaringan → Bisnis

Menjembatani telemetri teknis dan **keputusan bisnis** untuk operator kecil
(RT-RW net, hotspot desa, warnet, UMKM) yang sering non-teknis. **Read-only.**

## Tool yang dipakai
- `mcp__mikroclaw__business_report` — **inti**: kumpulkan ppp secret/active/profile,
  hotspot user/active, DHCP lease, queue; hitung `pelanggan` (terdaftar/aktif/
  nonaktif/belum-konek + distribusi profil), `perangkat_tak_terotentikasi` (dugaan
  pencuri bandwidth), `utilisasi_wan` (% vs kapasitas + level), `top_talkers`, dan
  `saran[]` berprioritas. Beri `plan_down_mbps`/`plan_up_mbps` (kapasitas paket dari
  ISP) & `wan_interface` agar utilisasi akurat.
- *(konteks opsional)* `simple_queues`, `ppp_active`, `hotspot_active`,
  `interface_traffic_live` untuk angka real-time.

## Prosedur
1. **Kumpulkan kapasitas.** Tanyakan/atau gunakan kapasitas paket WAN operator
   (mis. 100 Mbps) sebagai `plan_down_mbps`, dan `wan_interface` untuk throughput
   live. Tanpa ini, utilisasi ditebak dari link speed (kurang akurat).
2. **Tarik laporan.** Panggil `business_report`. Baca `ringkasan` lalu tiap blok.
3. **Terjemahkan ke bahasa pemilik usaha.** Hindari jargon. Contoh: bukan
   "utilisasi 92%", tapi "internet Anda hampir penuh di jam sibuk — pelanggan
   kemungkinan mengeluh lambat".
4. **Soroti peluang & risiko bisnis:**
   - **Akun nganggur/nonaktif** → tagih tunggakan atau cabut (rapikan basis pelanggan).
   - **Perangkat tak terotentikasi** → dugaan pemakaian tak tertagih; verifikasi.
   - **Utilisasi tinggi** → estimasi kapan & untung-rugi upgrade paket.
   - **Top talkers** → siapa penyedot terbesar (untuk fair-usage / paket khusus).
5. **Beri rekomendasi terukur** dengan estimasi sederhana (mis. potensi pendapatan
   dari mengaktifkan kembali N akun), tapi **tandai sebagai estimasi**, bukan janji.

## Format laporan
```
## Concierge — Laporan Bisnis Jaringan
**Ringkasan:** 42/50 pelanggan PPPoE aktif · utilisasi WAN 92% (kritis) · 3 perangkat tak terotentikasi

**Pelanggan**
- Aktif sekarang: 42 dari 50 terdaftar
- Dinonaktifkan (tertahan): 5 → 💰 tagih/cabut
- Belum pernah konek: 3 → tindak lanjuti pemasangan

**Kapasitas WAN:** 92 Mbps dari 100 Mbps (kritis) → ⬆️ pertimbangkan upgrade;
saat jam sibuk pelanggan kemungkinan mengeluh lambat.

**Dugaan pencurian bandwidth:** 3 perangkat memakai jaringan tanpa akun PPPoE/hotspot
(192.168.1.77, …) → verifikasi & amankan; potensi pemakaian tak tertagih.

**Top talkers:** 1) 10.0.0.3 (ani) 20 Mbps · 2) …
```

Selalu:
- Bahasa **ramah-awam**, fokus keputusan (tagih, cabut, upgrade, amankan).
- Tandai angka monetisasi sebagai **estimasi**.
- "Pencuri bandwidth" = **dugaan** berbasis tak-terotentikasi; minta verifikasi
  sebelum menuduh (bisa perangkat operator sendiri / IP statis sah).
- Read-only; perubahan (blokir, queue) butuh `MIKROCLAW_ALLOW_WRITE=true` + konfirmasi.
