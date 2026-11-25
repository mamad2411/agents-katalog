---
name: humanizer-id-pendidikan-ajar
description: Use when auditing or editing Indonesian textbooks, learning modules, LKPD worksheets, exam questions, teacher action research (PTK/KTI), or BIPA instructional materials.
version: 2.5.0
author: Hafizh Muzani / Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [writing, editing, bahasa-indonesia, pendidikan, modul, ptk, kti, bipa]
    category: creative
    homepage: https://github.com/apissaj/humanizer-id
    parent: humanizer-id
---

# Humanizer ID — Bahan Ajar, Modul Pendidikan, KTI Guru & BIPA

Sub-kaidah domain Humanizer ID untuk buku teks, modul ajar, lembar kerja peserta didik (LKPD), naskah soal/rubrik penilaian, karya tulis ilmiah guru (KTI/PTK), serta bahan ajar BIPA (*Cerdas Cergas Kelas XI & XII* Kemendikbudristek 2024; *Diklat KTI/PTK*; *Buku Ajar PT* Suyatno dkk. 2017 & Halimah dkk. 2020). Muat berkas ini setelah `humanizer-id` (induk).

---

### A. Bahasa Instruksional Modul, LKPD & Tujuan Pembelajaran

1. **Pola:** tujuan pembelajaran memakai kata kerja non-operasional (*Siswa diharapkan mampu memahami dan mengetahui konsep ekosistem*) atau instruksi LKPD menumpuk 3 perintah dalam satu kalimat panjang → **Perbaikan:** gunakan kata kerja operasional terukur (*Siswa mampu mengidentifikasi tiga komponen biotik dan membandingkan perannya dalam rantai makanan*) dan pecah langkah kerja menjadi daftar bernomor satu aksi per butir — **Sebab:** instruksi ajar wajib terukur dan langsung dapat dikerjakan peserta didik tanpa tafsir ganda.
2. **Pola:** verba ringan dan pembuka bertele-tele dalam uraian materi (*Peserta didik diharapkan dapat melakukan pengamatan terhadap perubahan warna larutan yang mana terjadi...*) → **Perbaikan:** gunakan verba langsung (*Amati perubahan warna larutan yang terjadi...*) — **Sebab:** pemangkasan verba ringan mempercepat pemahaman bacaan belajar (`VRB-001`..`006`).

---

### B. Kaidah Soal, Rubrik & Ejaan Bilangan/Satuan (`BSXI-001`..`003`, `UIN-011`)

1. **Pola:** angka dan lambang satuan ditulis rapat (*50cm*, *15m*, *10kg*, *25km*) atau kalimat soal diawali lambang bilangan angka (*50 siswa mengikuti ujian...*, *3 pemenang menerima hadiah...*) → **Perbaikan:** beri satu spasi antara bilangan dan lambang satuan (*50 cm*, *15 m*, *10 kg*, *25 km*) dan tulis bilangan awal kalimat dengan huruf (*Lima puluh siswa mengikuti ujian...*, *Tiga pemenang menerima hadiah...*) — **Sebab:** kaidah baku penulisan satuan dan lambang bilangan EYD V (`BSXI-001`, `UIN-011`).
2. **Pola:** salah eja serapan sains/sosial di naskah soal (*katagori*, *species*, *karaba*, *obyektif*, *praktek*) atau konjungsi kontaminatif (*Dengan alasan inilah maka...*, *Karena ..., maka ...*, *disebabkan karena*) → **Perbaikan:** gunakan bentuk baku KBBI (*kategori*, *spesies*, *keramba*, *objektif*, *praktik*) dan konjungsi tunggal (*Oleh karena itu,...*, *Karena ..., [klausa utama]*, *disebabkan oleh*) — **Sebab:** naskah pendidikan menjadi model kebahasaan langsung bagi peserta didik (`BSXI-002`, `BSXI-003`, `HKT-016`, `UIN-001`, `UIN-003`).
3. **Pola:** butir soal memakai negasi ganda (*Manakah yang bukan merupakan ketidakbenaran...*) → **Perbaikan:** susun pokok soal (*stem*) secara positif dan langsung (*Manakah pernyataan yang benar tentang...*); bila harus memakai kata *kecuali*, cetak tebal atau kapitalisasi konsisten sesuai standar evaluasi.

---

### C. KTI Guru, PTK & Penjenjangan BIPA (`KTI-001`, `RGM-001`..`002`)

1. **Pola:** rumusan masalah PTK/KTI berbentuk pernyataan umum tanpa kata tanya operasional, keterbatasan tindakan kelas disembunyikan, atau nama penulis Indonesia dibalik seragam tanpa memperhatikan konvensi katalogisasi → **Perbaikan:** susun rumusan masalah sebagai kalimat tanya operasional terukur, paparkan keterbatasan siklus penelitian secara jujur, dan patuhi format daftar pustaka (`Sayektiningsih, Tri dan Amir Ma'ruf`) — **Sebab:** standar evaluasi KTI/PTK Badan Bahasa & Kemendikbud (`KTI-001`).
2. **Penjenjangan BIPA (Bahasa Indonesia bagi Penutur Asing):**
   - **A1–B1 (Pemula–Madya Awal):** prioritaskan kalimat tunggal dan majemuk setara (8–15 kata), hindari penyengauan lisan nonbaku (*nggak*, *gimana*, *nulis*, *nyari* — `RGM-001`, `RGM-002`) kecuali pada sesi khusus ragam cakapan yang diberi label eksplisit.
   - **B2–C2 (Madya Akhir–Mahir):** perkenalkan kalimat kompleks, nominalisasi terkendali, dan pembedaan register formal vs semi-formal tanpa kalke terjemahan mesin.

---

### D. Contoh Selisih Ringkas (*Mini Diff*)

| Draf Bahan Ajar / Soal | Hasil Suntingan | Kaidah |
|---|---|---|
| 25 siswa melakukan pengukuran panjang pita sebesar 50cm. | Dua puluh lima siswa mengukur panjang pita sepanjang 50 cm. | `UIN-011`, `VRB-002`, `BSXI-001` |
| Dengan alasan inilah maka katagori species tersebut dibedakan. | Oleh karena itu, kategori spesies tersebut dibedakan. | `BSXI-003`, `BSXI-002` |

```bash
# Audit modul ajar, LKPD, atau naskah KTI/PTK
python scripts/audit.py modul-ajar.md --preset akademik --report
```
