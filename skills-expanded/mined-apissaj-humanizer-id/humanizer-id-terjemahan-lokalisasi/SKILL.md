---
name: humanizer-id-terjemahan-lokalisasi
description: Use when editing Indonesian translations, localized software UI/UX copy, bilingual documents, or terminology-heavy adaptations from English.
version: 2.5.0
author: Hafizh Muzani / Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [writing, editing, bahasa-indonesia, terjemahan, lokalisasi, istilah, pupi]
    category: creative
    homepage: https://github.com/apissaj/humanizer-id
    parent: humanizer-id
---

# Humanizer ID — Terjemahan, Lokalisasi & Pemadanan Istilah

Sub-kaidah domain Humanizer ID untuk penyuntingan hasil terjemahan (terutama Inggris → Indonesia), lokalisasi antarmuka aplikasi/web (*UI/UX copy*), dokumen dwibahasa, dan pemadanan istilah lintas bidang (*PUPI Ed. 3*, Baharman UNM, *Buletin MABBIM* Vol. 15/2024, PASTI Kemendikdasmen). Muat berkas ini setelah `humanizer-id` (induk).

---

### A. Eliminasi Kalke Terjemahan Mesin (`KLK-001`..`006`, `SPK-019`)

1. **Pola:** menerjemahkan metafora dan kolokasi Inggris secara harfiah kata demi kata (*menghormati batas memori*, *tidak datang tanpa harga*, *menyelami lebih dalam*, *merangkul perubahan*, *lanskap persaingan*, *ujung tombak*) → **Perbaikan:** alihkan ke kolokasi alami bahasa Indonesia (*selaras dengan batas memori*, *memiliki konsekuensi teknis*, *mengkaji secara mendalam*, *mengadopsi perubahan*, *peta persaingan*, *komponen utama*) — **Sebab:** kalke mempertahankan struktur semantik bahasa sumber yang terasa asing bagi pembaca Indonesia (`KLK-001`..`KLK-006`).
2. **Pola:** mempertahankan struktur klausa relatif dan pengantar ujaran Inggris (*...yang mana hal tersebut sangat membantu*, *Ini Budi melaporkan dari Jakarta*) → **Perbaikan:** ubah menjadi klausa lugas (*...sehingga sangat membantu* / *Kondisi ini sangat membantu*; *Demikian laporan Budi dari Jakarta*) — **Sebab:** *which is* dan *This is X reporting from Y* tidak berpindah harfiah ke sintaksis Indonesia (`SPK-019`, `KLK-007`).

---

### B. Urutan Pemadanan & Penyerapan PUPI/EYD V (`TMS-047`, `TMS-048`, `SPK-007`)

1. **Pola:** mendahulukan istilah asing lalu menaruh padanan Indonesia di dalam kurung (*exposure (paparan)*, *commuter line (kereta komuter)*, *latency (latensi)*) → **Perbaikan:** dahulukan padanan Indonesia baru istilah asing bercetak miring dalam kurung pada kemunculan pertama (*paparan (exposure)*, *kereta komuter (commuter line)*, *latensi (latency)*) — **Sebab:** urutan ini menegaskan bahasa Indonesia sebagai bahasa utama wacana (`TMS-048`, Baharman UNM).
2. **Pola:** salah adaptasi serapan (*frustasi*, *negoisasi*, *konkrit*, *komoditi*, *orisinal* ditulis *orisinil*, *misskoordinasi*, *volantilitas*) atau penjamakan bentuk jamak asing (*data-data*, *kriteria-kriteria*, *alumnus-alumnus* dicampur *para alumni-alumni*) → **Perbaikan:** patuhi adaptasi baku KBBI/EYD V (*frustrasi*, *negosiasi*, *konkret*, *komoditas*, *orisinal*, *miskoordinasi*, *volatilitas*) dan gunakan bentuk tunggal atau penanda jamak non-ganda (*data*, *kriteria*, *para alumni*) — **Sebab:** PUPI melarang penjamakan ulang bentuk yang sudah bermakna jamak atau kolektif (`TMS-001`, `TMS-047`, `SPK-007`).
3. **Rujukan pemadanan resmi:** prioritaskan 210 padanan terverifikasi di `data/glosarium-lintas-bidang.json` (Teknologi 70, Bisnis 66, Linguistik 27, Jurnalistik 26, Hukum 21) dan asas penyerapan selektif Pusat Bahasa (`PKU-001`, Sugono dkk. 2005, hlm. 2–5) sebelum menyerap mentah istilah asing.

---

### C. Lokalisasi UI/UX, Mikro-Teks & Safeguard

1. **Pola:** label tombol/pesan galat hasil terjemahan kaku atau nominalisasi (*Lakukan Penyimpanan*, *Pengiriman Anda telah berhasil dilakukan*, *Kesalahan tidak diketahui telah terjadi*) → **Perbaikan:** gunakan verba aktif ringkas untuk tombol (*Simpan*, *Kirim*, *Lanjutkan*), serta pesan galat yang lugas dan memberi solusi (*Data tersimpan*, *Gagal memuat data. Periksa koneksi internet Anda lalu coba lagi.*) — **Sebab:** antarmuka digital menuntut kejelasan instan dan pemangkasan verba ringan (`VRB-001`..`006`).
2. **Pola:** inkonsistensi sapaan dalam satu aplikasi (*Anda* di halaman masuk, *Kamu* di notifikasi, *Pengguna* di pesan galat) → **Perbaikan:** kunci satu register sapaan sejak awal (*Anda* untuk produk profesional/publik, atau *Kamu* untuk produk kasual/remaja) secara konsisten di seluruh layar.
3. **Safeguard lokalisasi:** **JANGAN** menerjemahkan paksa *placeholder* variabel (`{username}`, `%s`), kunci JSON, *flag* CLI, nama merek terdaftar, atau istilah serapan baku yang sudah mapan (*algoritma*, *server/peladen* sesuai glosarium produk, *enkripsi*).

---

### D. Contoh Selisih Ringkas (*Mini Diff*)

| Teks Terjemahan Kaku | Hasil Lokalisasi Alami | Kaidah |
|---|---|---|
| Mari kita menyelami lebih dalam bagaimana fitur ini menghormati batas privasi Anda. | Berikut uraian cara fitur ini menjaga batas privasi Anda. | `KLK-001`, `KLK-003` |
| Silakan melakukan penyimpanan sebelum keluar. | Simpan perubahan sebelum keluar. | `VRB-001` |
| *Latency* (latensi) tinggi memengaruhi *user experience*. | Latensi (*latency*) tinggi memengaruhi pengalaman pengguna. | `TMS-048`, `GLOS-TEK` |

```bash
# Audit hasil terjemahan atau berkas lokalisasi
python scripts/audit.py terjemahan.md --report
```
