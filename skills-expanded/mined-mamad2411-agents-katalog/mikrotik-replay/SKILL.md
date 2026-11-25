---
name: mikrotik-replay
description: RCA retrospektif MikroTik — jawab "kenapa tadi sore lemot / internet sempat putus?" dengan merekonstruksi telemetri (CPU/mem/RTT/conntrack/firewall-drops/throughput/klien) pada jendela waktu lampau dari riwayat yang dipersist Pulse, menandai anomali, lewat tool MikroCLAW. Gunakan saat user minta "kenapa tadi lemot", "internet putus jam berapa", "analisa insiden", "RCA", "apa yang terjadi 2 jam lalu", "riwayat performa", atau "kenapa ping tinggi tadi".
---

# MikroTik Replay — RCA Retrospektif

Menjawab pertanyaan paling sering operator — *"kenapa tadi sore lemot?"* — yang
tak terjawab oleh monitoring present-tense. Membaca **riwayat telemetri** yang
dipersist MikroCLAW Pulse pada jendela waktu yang diminta, menghitung statistik,
dan menandai anomali untuk merekonstruksi rantai sebab. **Read-only.**

## Prasyarat
Riwayat ditulis oleh **MikroCLAW Pulse** (`uv run mikroclaw-web`) tiap ~30 detik ke
`MIKROCLAW_STATE_DIR/history`. Replay hanya bisa menjelaskan rentang waktu saat
Pulse sedang berjalan. Bila kosong, sarankan menjalankan Pulse agar insiden
berikutnya terekam.

## Tool yang dipakai
- `mcp__mikroclaw__explain_incident` — **inti**: ambil jendela `[mulai_menit_lalu,
  selesai_menit_lalu]`, kembalikan `metrik` (min/max/mean/median per metrik),
  `anomali[]` deterministik (lonjakan RTT, timeout/outage, CPU tinggi
  berkelanjutan, lonjakan conntrack/drops), dan `deret_ringkas`.
- *(konteks live opsional)* `recent_logs` untuk menautkan kejadian, `ping`/
  `traceroute` untuk kondisi sekarang, `firewall_connections` untuk pelaku saat ini.

## Prosedur
1. **Tentukan jendela.** Terjemahkan "tadi sore" / "2 jam lalu" menjadi
   `mulai_menit_lalu`/`selesai_menit_lalu`. Bila ragu, ambil rentang lebih lebar
   dulu lalu persempit.
2. **Tarik telemetri.** Panggil `explain_incident`. Periksa `kosong` (Pulse belum
   jalan?) dan `keparahan_tertinggi`.
3. **Korelasikan anomali.** Hubungkan lonjakan antar-metrik untuk menebak akar
   masalah — mis. "RTT internet 15→480ms BERSAMAAN conntrack melonjak 800→5000 &
   CPU 95% → satu host menjenuhkan conntrack (P2P), bukan gangguan ISP."
4. **Tautkan ke log.** Cek `recent_logs` untuk peristiwa di sekitar waktu itu
   (link down, DHCP, login).
5. **Simpulkan & cegah.** Beri akar masalah + saran agar tak terulang (mis. batasi
   conntrack per-IP, queue untuk host berat, alert).

## Format laporan
```
## Replay — RCA 17:00–18:00
**Data:** 120 sampel · 🟠 2 anomali (tertinggi: warning)

**Anomali:**
- RTT internet melonjak ke 480ms (median 18ms) — saturasi link
- Conntrack melonjak ke 5.000 (median 800) — banyak sesi/flood

**Rekonstruksi:** ~17:32 conntrack & RTT naik bersamaan, CPU firewall ~95%.
Pola khas SATU klien membanjiri sesi (torrent). Bukan gangguan ISP.
**Saran:** batasi conntrack/queue untuk host tersebut; pasang alert dini.
```

Selalu:
- Bila `kosong`, katakan jujur datanya tak ada untuk rentang itu (Pulse tak jalan).
- Pisahkan **temuan dari data** vs **dugaan** — jangan mengarang sebab.
- Read-only; tindakan pencegahan yang mengubah router butuh write-gate + konfirmasi.
