---
name: data-resmi-indonesia
description: Use when an app needs Indonesian official data or periodic Indonesian rates — BMKG earthquake/forecast/nowcast alerts, BPS statistics, Bank Indonesia JISDOR & kurs, Bapanas food prices, national holidays & collective leave, Hijriah/Javanese calendar, prayer times, school/hospital/campus directories, and the PPh 21 TER / PTKP / PPN / BPJS / UMP figures that change every year. Triggers on "hari libur nasional", "gempa BMKG", "prakiraan cuaca", "JISDOR", "kurs BI", "harga pangan", "hari kerja", "kalender Hijriah", "jadwal sholat", "UMP 2026", "PPh 21 TER", "BPJS rate", "PTKP".
---

# Data Resmi Indonesia

Menyediakan umpan data resmi Indonesia (BMKG, BPS, Bank Indonesia, Badan Pangan
Nasional, Kemenag) dan aturan berperiode (pajak, BPJS, upah minimum) dalam
registry bertanggal yang digerbangi validator.

## When to Use

Gunakan skill ini saat aplikasi membutuhkan **data resmi Indonesia** atau
**aturan berperiode Indonesia** yang angkanya berubah tiap tahun.

Trigger umum:

- Hari libur / cuti bersama: "hari libur nasional 2026", "cuti bersama", "SKB 3 Menteri"
- BMKG: "gempa BMKG", "prakiraan cuaca", "peringatan dini cuaca", "nowcast"
- Bank Indonesia: "JISDOR", "kurs BI", "kurs acuan", "kurs transaksi"
- BPS: "statistik BPS", "data BPS"
- Bapanas: "harga pangan", "data pangan"
- Kalender: "kalender Hijriah", "kalender Jawa", "1 Ramadhan", "jadwal sholat"
- Direktori: "rumah sakit", "sekolah", "kampus", "PDDikti"
- Aturan: "UMP 2026", "PPh 21 TER", "PTKP", "PPN", "BPJS", "iuran BPJS"

Jika yang dibutuhkan **bukan** data resmi Indonesia atau aturan berperiode
Indonesia, pertimbangkan skill lain.

## Router: Data vs Aturan

| Topik | Berkas |
| --- | --- |
| Gempa bumi BMKG | `references/data/bmkg-gempa.md` |
| Prakiraan cuaca BMKG | `references/data/bmkg-cuaca.md` |
| Peringatan dini / nowcast BMKG | `references/data/bmkg-nowcast.md` |
| Kurs / JISDOR Bank Indonesia | `references/data/bi-kurs.md` |
| Statistik BPS (kunci) | `references/data/bps-statistik.md` |
| Harga pangan Bapanas (kunci) | `references/data/bapanas-pangan.md` |
| Hari libur & cuti bersama | `references/data/hari-libur-cuti-bersama.md` |
| Kalender Hijriah/Jawa | `references/data/kalender-masehi-hijriah-jawa.md` |
| Jadwal sholat (MyQuran mirror) | `references/data/jadwal-sholat.md` |
| Direktori institusi | `references/data/direktori-sekolah-rs-kampus.md` |
| Aturan pajak 2026 (PTKP, PPh 21 TER, PPN) | `references/aturan/pajak-*-2026.json` |
| BPJS & UMP 2026 | `references/aturan/ketenagakerjaan-*-2026.json` |

## Workflow — Bagian Data

1. Identifikasi topik (lihat router di atas).
2. Buka halaman `references/data/<topik>.md`.
3. Catat **kelas sumber**:
   - **Publik tanpa kunci** (BMKG, BI, MyQuran): boleh `curl` + contoh respons
     nyata + klaim `terverifikasi`.
   - **Kunci milik pengguna** (BPS, Bapanas): hanya bentuk + self-check;
     dilarang klaim `terverifikasi`. Kunci dari env var (`BPS_API_KEY`,
     `BAPANAS_API_KEY`), tidak pernah disimpan di repo.
4. Perhatikan **atribusi** (sumber resmi) dan **batas akses** (rate limit,
   zona waktu, jadwal rilis).

## Workflow — Bagian Aturan

1. Petakan tanggal permintaan → periode (tahun).
2. Buka registry JSON `references/aturan/<aturan>-<tahun>.json` yang sesuai.
3. Angka hanya boleh diambil dari JSON; jangan dari ingatan atau dokumen lepas.
4. Hitung & tampilkan jejak keluaran: dasar hukum, tanggal berlaku, sumber.
5. Jika periode **tidak tercakup** registry (mis. belum ada JSON untuk tahun
   itu) → **menolak**, jangan menghitung pakai angka tahun lain.

## Anti-patterns

- Menyalin angka dari dokumen/ingatan (harus dari registry JSON + sumber).
- Menghitung periode di luar cakupan registry.
- Meng-cache data pribadi (mis. dari PDDikti/EMIS).
- Menaruh kunci/kredensial di kode, log, cache, atau contoh.
- Menyalin isi cek-APIPedia (data BMKG yang bukan katalog API publik).
- Mengklaim `terverifikasi` untuk sumber ber-kunci.

## Verification checklist

Sudah memakai data/aturan dari skill ini:

- [ ] Jalankan validator: `node skills/data-resmi-indonesia/scripts/validate-registry.mjs`
- [ ] Pastikan exit code 0.
- [ ] Pastikan setiap angka aturan punya `sumber` + `diverifikasi_pada`.
- [ ] Pastikan tidak ada angka aturan di prosa `SKILL.md` atau `references/aturan/*.md`.

## Rujukan lintas skill

- **Wilayah/kode pos/NIK/NPWP/ongkir** → skill `indonesian-data-forms`.
- **QRIS/rekening/payment gateway** → skill `payment-gateway-indonesia`.
- **Notifikasi (WA/Telegram/email)** untuk peringatan cuaca → skill `notifikasi-indonesia`.
