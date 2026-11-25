---
name: humanizer-id-bisnis-korporat
description: Use when editing Indonesian corporate, executive, proposal, memo, or press release prose.
version: 2.5.0
author: Hafizh Muzani / Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [writing, editing, bahasa-indonesia, bisnis, korporat]
    category: creative
    homepage: https://github.com/apissaj/humanizer-id
    parent: humanizer-id
---

# Humanizer ID — Bisnis & Korporat

Sub-kaidah domain Humanizer ID untuk **Mode Bisnis & Eksekutif** (laporan manajemen, memo internal, proposal klien, surat instruksi kerja, dan siaran pers). Muat berkas ini setelah `humanizer-id` (induk). Aturan integritas angka dan fakta pada induk tetap mengikat penuh.

---

### A. Prinsip KISS & Kejelasan Komunikasi Korporat (Rahman, Penerbit BRIN 2022, hlm. 16–20)

1. **Pola:** verba ringan + nomina abstrak dalam memo/proposal (*memberikan informasi*, *membuat perusahaan tumbuh dan berkembang*, *melakukan peninjauan terhadap*, *melakukan implementasi*, *membuat keputusan*) → **Perbaikan:** verba derivasional langsung (*menginformasikan*, *menumbuhkembangkan perusahaan*, *meninjau*, *menerapkan*, *memutuskan*) — **Sebab:** efisiensi kata prinsip KISS (*Keep It Simple*): pembaca bisnis menuntut pesan inti cepat tanpa lapisan verba kosong (`KPT-016`, `VRB-001`..`006`) (hlm. 16, 19).
2. **Pola:** pembuka klise AI & kalke korporat (*Di era digital yang berkembang pesat saat ini...*, *memegang peranan yang sangat krusial*, *merangkul perubahan*, *lanskap persaingan*, *Sehubungan dengan hal tersebut di atas maka...*) → **Perbaikan:** langsung nyatakan konteks bisnis dan metrik kunci (*peta persaingan*, *mengadopsi pembaruan*, *Oleh karena itu,...*) — **Sebab:** eksekutif membaca untuk mengambil keputusan, bukan membaca basa-basi (`RET-002`, `RET-006`, `KLK-004`, `KLK-005`, `TMP-001`).
3. **Pola:** kalimat pasif berbelit pada instruksi kerja atau proposal tindakan → **Perbaikan:** utamakan kalimat aktif berorientasi tindakan (*Tim operasional meninjau laporan setiap Senin*) — **Sebab:** ragam korporat menuntut kejelasan penanggung jawab aksi; berbeda dari bab metodologi skripsi yang mewajibkan pasif (hlm. 19).
4. **Pola:** penutup rincian malas *dll.* dan *dsb.* dalam dokumen bisnis resmi, atau salam/penutup surat korporat yang salah eja (*Dengan Hormat,*, *Atas perhatiannya...*) → **Perbaikan:** sebutkan butir rincian yang relevan secara tuntas, serta gunakan `Dengan hormat,` dan `Atas perhatian Bapak/Ibu,` (`SMD-003`, `DIN-003`) — **Sebab:** *dll.*/*dsb.* terkesan menggantung, sedangkan penutup `-nya` rancu dalam surat resmi (hlm. 19).
5. **Pola:** nama merek ditulis miring seperti istilah asing biasa (*"searching di google"* / *Microsoft*) atau kata tugas pada judul ditulis kapital (*Strategi Pemasaran Di Era Digital*) → **Perbaikan:** nama merek cukup huruf kapital tegak (*melalui Google*), sedangkan kata tugas non-awal judul (*di, dari, ke, yang, dan, atau, untuk*) ditulis huruf kecil — **Sebab:** kaidah kapitalisasi nama merek dan judul EYD V (hlm. 17, 20).

---

### B. Struktur Surat Instruksi Kerja & Siaran Pers (Rahman, Penerbit BRIN 2022, hlm. 94–99)

1. **Pola:** surat instruksi program kerja tanpa kelengkapan unsur operasional atau diakhiri frasa berbunga → **Perbaikan:** pastikan memuat **5W1H** lengkap (nama kegiatan, alasan/latar belakang, lokasi, pelaksana/pemantau/evaluator, jadwal, dan juklak/juknis), nomor kontak koordinasi, serta penutup lugas (*Demikian disampaikan, atas perhatian dan kerja sama Saudara, kami ucapkan terima kasih.*) — **Sebab:** surat instruksi korporat harus langsung dapat dieksekusi tanpa rapat klarifikasi ulang (hlm. 94–96).
2. **Pola:** siaran pers (*press release*) dibuka dengan latar belakang sejarah perusahaan panjang sebelum inti berita → **Perbaikan:** terapkan struktur **piramida terbalik** (fakta terpenting + 5W1H di paragraf pertama, diikuti rincian pendukung dan rencana tindak lanjut), bernada netral-positif, bebas kesalahan ejaan — **Sebab:** editor media dan pembaca publik memindai nilai berita di dua kalimat pertama (hlm. 96–99).

---

### C. Pembersihan Jargon Bisnis & Padanan Baku (`data/glosarium-lintas-bidang.json`)

Ganti istilah Inggris mentah dengan padanan resmi bahasa Indonesia (kecuali istilah khusus dalam kutipan kontrak):

| Istilah Asing | Padanan Baku Indonesia | Catatan Editorial |
|---|---|---|
| *after-sales service* | **layanan pascajual** | Standar Pusat Bahasa (BPBI 2) |
| *customer service* | **layanan pelanggan / layanan nasabah** | Gunakan *nasabah* untuk perbankan/asuransi |
| *cash flow* | **arus kas** | Laporan keuangan & proyeksi |
| *overbooking* | **tempah lajak** | Perhotelan & transportasi |
| *due diligence* | **uji tuntas** | Akuisisi, kepatuhan, kontrak |
| *site plan* / *master plan* | **rencana tapak** / **rencana induk** | Properti, tata ruang, proyek |
| *standby loan* | **pinjaman siaga** | Pembiayaan korporat |
| *showroom* | **ruang pamer / ruang peraga** | Ritel & otomotif |
| *boarding pass* | **pas naik** | Penerbangan & pelayaran |
| *stakeholder* | **pemangku kepentingan** | Tata kelola & CSR |
| *synergy* | **keselarasan kerja / kolaborasi terpadu** | Hindari *sinergitas* tanpa ukuran keluaran |

---

### D. Contoh Selisih Ringkas (*Mini Diff*) & Perintah Audit CLI

| Draf Korporat Kaku | Hasil Eksekutif Lugas | Kaidah |
|---|---|---|
| Sehubungan dengan hal tersebut di atas maka kami melakukan implementasi *cash flow* baru untuk merangkul perubahan lanskap persaingan. | Oleh karena itu, kami menerapkan pengelolaan arus kas baru agar siap menghadapi peta persaingan. | `TMP-001`, `VRB-001`, `KLK-004`, `KLK-005`, `GLOS-BIS` |
| Dengan Hormat, atas perhatiannya kami ucapkan terima kasih. | Dengan hormat, atas perhatian Bapak/Ibu, kami ucapkan terima kasih. | `SMD-003`, `DIN-003` |

```bash
# Audit proposal/laporan bisnis (deteksi jargon & verba ringan)
python scripts/audit.py naskah-bisnis.md

# Audit surat dinas/memo resmi instansi
python scripts/audit.py surat-keputusan.md --preset dinas --report
```
