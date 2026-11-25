---
name: humanizer-id-jurnal
description: Skill humanizer-id untuk menulis, menyunting, dan mengaudit naskah jurnal ilmiah bereputasi (Scopus, SINTA, IEEE, Springer, Elsevier).
version: 1.0.0
author: Hafizh Muzani (apissaj)
license: MIT
---

# Humanizer ID — Modul Jurnal Ilmiah Bereputasi

Modul khusus (sub-skill) dari humanizer-id untuk menulis, menyunting, dan mengaudit naskah
artikel jurnal ilmiah bereputasi: Scopus, Web of Science, SINTA 1-2, IEEE, Springer, Elsevier,
Taylor & Francis, dan Emerald. Modul ini dipisah jalurnya dari humanizer umum agar tidak
mengganggu kaidah umum, tetapi tetap memakai mesin audit, dataset kalke, dan prompt yang sama.

## Kapan Dipakai
- Menulis artikel hasil penelitian untuk jurnal terindeks Scopus/SINTA 1-2.
- Menyunting (proofreading) naskah submission sebelum dikirim ke editor.
- Mengaudit draf yang ditulis AI agar lolos desk check editor dan tidak terdeteksi slop.
- Menyiapkan abstrak, cover letter, dan response to reviewer.

## Kapan TIDAK Dipakai
- Skripsi/tesis/proposal internal kampus -> pakai preset pedoman-kampus.json di humanizer-id utama.
- Artikel opini/populer/media massa -> pakai kaidah artikel opini KD 3.11 di SKILL.md induk.
- Surat dinas/aparatur -> pakai referensi buku-aparatur-pemerintah-pusat-bahasa.md.

## Prinsip Dasar Naskah Jurnal Bereputasi
1. Ragam baku formal, impersonal (penulis/peneliti atau kalimat pasif) — MKI-001.
2. Denotatif murni; dilarang makna konotatif/hiperbolis ("revolusioner", "sangat krusial") — RET-006, RET-008.
3. Satu paragraf satu gagasan pokok dengan kalimat topik eksplisit — ARG-001.
4. Denotasi istilah konsisten sepanjang naskah (keajegan istilah) — TBBBI hlm. 42.
5. Abstrak TANPA sitasi, TANPA singkatan/akronim yang belum didefinisikan, TANPA referensi silang — Pedoman Jurnal Pendidikan dan Kebudayaan Kemendikbud.
6. Judul artikel maksimal 14 kata, spesifik, memuat kata kunci — Pedoman Jurnal Dikbud.
7. Nama penulis tanpa gelar, pangkat, atau jabatan — Pedoman Jurnal Dikbud.
8. Semua kaidah kebahasaan humanizer-id (740 entri) berlaku di sini juga.

## Struktur IMRaD Standar Scopus
1. Title & Abstract (150-250 kata, satu paragraf, tujuan-metode-hasil-simpulan)
2. Introduction: latar belakang -> gap penelitian -> novelty -> tujuan (funnel structure)
3. Literature Review / Related Work: posisi penelitian terhadap state-of-the-art
4. Methods: desain, data/sampel, instrumen, prosedur, analisis (replikabel)
5. Results: temuan murni tanpa interpretasi, dilengkapi tabel/gambar bernomor
6. Discussion: interpretasi, perbandingan dengan literatur, implikasi, keterbatasan
7. Conclusion: menjawab tujuan, tanpa informasi baru
8. References: gaya sitasi konsisten (IEEE/APA/Vancouver) sesuai jurnal target

## Prosedur Penggunaan

### Fase 1 - Pemetaan Jurnal Target
1. Tentukan jurnal target (kuartil, penerbit, scope).
2. Baca Guide for Authors resmi jurnal (batas kata, template, gaya sitasi, jumlah referensi).
3. Catat parameter ke jurnal/target-jurnal.md.

### Fase 2 - Drafting per Bagian
1. Susun kerangka IMRaD sesuai struktur di atas.
2. Tulis per bagian dengan ragam baku impersonal.
3. Pahami bahwa kalimat topik tiap paragraf wajib eksplisit (kesatuan paragraf).

### Fase 3 - Humanisasi & Audit Otomatis
1. Jalankan audit mesin dengan preset jurnal:
   python scripts/audit.py <naskah.md> --kampus jurnal-dikbud
2. Perbaiki semua temuan sampai bersih.
3. Cek manual entri [telaah] (kesatuan paragraf, gagasan ganda, kelogisan).

### Fase 4 - Audit Jurnal Spesifik
1. Jalankan checklist checklist.md (30 poin).
2. Verifikasi batas kata, jumlah referensi, gaya sitasi, kelengkapan bagian.
3. Pastikan zero AI-slop: tidak ada "delve", "leverage", "in the realm of", "plays a crucial role".

## Checklist Kualitas Naskah (28 Poin)
Lihat checklist.md untuk rincian lengkap. Poin utama:
1. Judul <= 14 kata, tanpa singkatan, tanpa rumus.
2. Abstrak 150-250 kata, satu paragraf, tanpa sitasi/akronim.
3. Kata kunci 4-6 istilah, urut abjad, sesuai thesaurus bidang.
4. Novelty dinyatakan eksplisit di akhir Introduction.
5. Tabel/gambar bernomor dan diberi keterangan mandiri (self-contained caption).
6. Sitasi in-text konsisten dengan daftar pustaka (100% match).
7. Tidak ada kalimat > 40 kata.
8. Tidak ada konjungsi awal kalimat informal (Dan, Lalu, Terus).
9. Verba mental pasif ilmiah (diduga, dianalisis) bukan aktif personal (kami berasumsi).
10. Angka satuan SI konsisten; desimal pakai titik; ribuan pakai koma (atau sesuai jurnal).

## Pitfalls
1. Jangan pakai kaidah kampus (preset pedoman-kampus.json) untuk jurnal internasional — formatnya beda.
2. Jangan melanggar keajegan istilah: satu istilah satu padanan sepanjang naskah.
3. Jangan sertakan data mentah di Results; taruh di Lampiran atau repositori data.
4. Self-plagiarism: pastikan tidak ada salinan verbatim dari artikel sendiri sebelumnya.
5. Abstrak yang memuat sitasi/akronim tak didefinisikan = desk check reject.

## Verification
1. audit.py lulus tanpa temuan pada naskah final.
2. Checklist 28 poin semua tercentang.
3. Batas kata tiap bagian sesuai Guide for Authors jurnal target.
