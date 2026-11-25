---
name: humanizer-id-naskah-resmi
description: Use when fixing naskah dinas, pewara & metadata jurnal.
version: 2.5.0
author: Hafizh Muzani / Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [writing, editing, bahasa-indonesia, akademik, nlp]
    category: creative
    homepage: https://github.com/apissaj/humanizer-id
    parent: humanizer-id
---

# Humanizer ID — Naskah Resmi

Sub-kaidah Humanizer ID. Muat berkas ini setelah `humanizer-id` (induk) menentukan mode kerja. Aturan integritas ilmiah pada induk tetap mengikat penuh.

---

### AK. Bahasa Pewara & Salam Resmi (Rujukan Kurniawan dkk., *Bahasa Indonesia untuk Pewara*, Badan Bahasa, 2019)

1. **Pola:** *Waktu dan tempat kami persilakan* → **Perbaikan:** *Panitia akan menyampaikan waktu dan tempat* — **Sebab:** yang dipersilakan adalah orang, bukan waktu-tempat; frasa pewara harus bernalar (hlm. 10, 90).
2. **Pola:** *Yang kami hormati Kepala Biro, Bapak X* → **Perbaikan:** *Yang kami hormati Bapak X* / *Yang kami hormati Kepala Biro X* — **Sebab:** kata penyapa *Bapak/Ibu* hanya menyertai nama orang, bukan jabatan (*Bapak Kepala Biro* salah) (hlm. 11, 88).
3. **Pola:** *Ibu-ibu / Bapak dan Ibu sekalian / hadirin* → **Perbaikan:** gunakan satu penanda jamak saja — **Sebab:** *para, sekalian,* dan bentuk ulang tidak boleh digabung (hlm. 86–87; selaras `SPB-001`).

---

### AL. Bahasa Dinas & Surat Resmi (Rujukan Mullyana dkk., *Bahasa Indonesia untuk Pejabat Pemerintah*, Badan Bahasa 2019; *Pedoman Surat-Menyurat dalam Bahasa Indonesia*, Pusat Bahasa 1991)

1. **Pola:** *melakukan kunjungan; mengajukan saran; mengeluarkan pemberitahuan* → **Perbaikan:** *berkunjung; menyarankan; memberitahukan* — **Sebab:** verba bentukan lebih hemat daripada nominalisasi verba ringan (Mullyana 2019, hlm. 37).
2. **Pola:** *kami sudah laporkan* → **Perbaikan:** *sudah kami laporkan* — **Sebab:** pronomina diri dan verba pangkal pasif tidak boleh dipisah adverbia (Mullyana 2019, hlm. 48).
3. **Pola:** *Pelaksanaan tugas itu dimulai* → **Perbaikan:** *Tugas itu mulai dilaksanakan* — **Sebab:** nomina tindakan (*pelaksanaan/perencanaan*) tidak sah menjadi penderita verba pasifnya sendiri (Mullyana 2019, hlm. 49).
4. **Pola:** *membahas tentang/mengenai/daripada usulan* → **Perbaikan:** *membahas usulan* — **Sebab:** *tentang/mengenai/daripada* setelah verba transitif mubazir (Mullyana 2019, hlm. 39).
5. **Pola:** *mengejar ketinggalan; bunyi surat* → **Perbaikan:** *mengatasi ketinggalan; isi surat* — **Sebab:** nalar frasa surat: ketinggalan diatasi, bukan dikejar; surat berisi, tidak berbunyi (Pusat Bahasa 1991, hlm. 35–36).
6. **Pola:** *ke-XLV* → **Perbaikan:** *ke-45* atau *XLV* — **Sebab:** awalan *ke-* dilarang menempel angka Romawi; ordinal satu sistem (Pusat Bahasa 1991, hlm. 34).
7. **Pola:** *berkenan dengan* (untuk makna 'sehubungan dengan') → **Perbaikan:** *berkenaan dengan* — **Sebab:** *berkenan* khusus bermakna 'bersedia dengan hormat' (Pusat Bahasa 1991, hlm. 39).

---

### AQ. Pedoman Penerbitan Buku Ilmiah Nasional (Rujukan Author Guidelines Penerbit BRIN, BRIN Publishing, 2024)

1. **Pola:** *penulis menyadari bahwa buku ini masih jauh dari sempurna* / *masih memiliki banyak kekurangan* / *tak luput dari kekurangan* → **Perbaikan:** pernyataan batasan ruang lingkup (*work limitations*) objektif — mis. *Buku ini berfokus pada X dan tidak mencakup Y karena...* — **Sebab:** klise kerendahan hati palsu (BRN-001) dilarang dalam pembuka/prakata (Penerbit BRIN, Bagian Preface).
2. **Pola:** subbab bertitel *Tinjauan Pustaka*, *Metodologi Penelitian*, *Rumusan Masalah*, *Hasil dan Pembahasan*, *Manfaat Penelitian*, *Landasan Teori* → **Perbaikan:** frasa topik substantif yang mencerminkan isi kajian secara langsung — **Sebab:** judul subbab generik (BRN-002) dilarang pada monograf ilmiah (Penerbit BRIN, Bagian Text Matter).
3. **Pola:** penomoran desimal tak berbatas (*2.1.3.4.1*) → **Perbaikan:** *Bab I* (Romawi) → *A.* (Kapital) → *1.* (Arab) → *a.* (Kecil) — **Sebab:** hierarki penomoran monograf (BRN-003) menolak gaya laporan teknis [telaah] (Penerbit BRIN, Bagian Chapters).
4. **Pola:** catatan kaki/endnote dipakai semata-mata untuk sitasi → **Perbaikan:** memuat penjelasan substantif, atau sitasi dialihkan ke sistem pengarang-tahun (APA) dalam badan teks — **Sebab:** catatan kaki konten (BRN-004) wajib substantif [telaah] (Penerbit BRIN, Bagian Chapters & Citations).

---

### AY. Konvensi Naskah Dinas Resmi (Rujukan "Bahasa Indonesia untuk Pejabat Pemerintah", Seri Penyuluhan Badan Bahasa, Bab II hlm. 48-50 & Bab III hlm. 71-76)

1. **Pola:** *Membalas/Merujuk/Menunjuk/Menindaklanjuti surat...* (pembuka verba mentah) → **Perbaikan:** *Sehubungan dengan/Berdasarkan/Berkenaan dengan surat...* atau kalimat lengkap S-P-O — **Sebab:** naskah dinas (DIN-001) dilarang dibuka dengan verba mentah tanpa subjek.
2. **Pola:** *Masalah itu kami sudah laporkan* → **Perbaikan:** *Masalah itu sudah kami laporkan* atau ubah ke aktif — **Sebab:** pasif berklitika (DIN-002) menolak sisipan adverbia.
3. **Pola:** *Atas perhatiannya* / *Harap maklum adanya* → **Perbaikan:** acuan langsung *Saudara/Bapak/Ibu* — **Sebab:** pronomina orang kedua (DIN-003) menyalahi konvensi komunikasi resmi.
4. **Pola:** *Meskipun ... tetapi* → **Perbaikan:** *Meskipun X, Y* atau *X, tetapi Y* — **Sebab:** konsesif tunggal (DIN-004): ganda konjungsi mubazir.

---

### BB. Bahasa Surat-Menyurat Resmi (Rujukan "Surat-Menyurat dalam Bahasa Indonesia", Pusat Bahasa Depdikbud, Bagian D hlm. 28-38)

1. **Pola:** *... yang mana ...* → **Perbaikan:** hilangkan *yang mana* atau ganti dengan *yang* — **Sebab:** bentuk *yang mana* (SUR-001) tidak diperlukan dalam kalimat surat.
2. **Pola:** *Di mana* sebagai kata sambung klausa → **Perbaikan:** ganti *tempat* atau hilangkan — **Sebab:** *di mana* (SUR-002) bukan kata sambung klausa.
3. **Pola:** *sesuai dengan bunyi surat...* → **Perbaikan:** *sesuai dengan surat...* — **Sebab:** surat tidak dapat berbunyi (SUR-003).
4. **Pola:** *sangsi administratif* → **Perbaikan:** *sanksi administratif* — **Sebab:** *sangsi* bermakna 'ragu-ragu'; *sanksi* bermakna 'tindakan penegakan hukum/hukuman' (SUR-004).

---

### BN. Ragam Baku Bahasa Surat Dinas & Komunikasi Resmi (Pusat Bahasa 1985)

1. **Pola:** *kenapa* → **Perbaikan:** *mengapa* — **Sebab:** dalam teks formal, laporan resmi, dan karya ilmiah, kata tanya kausatif baku adalah *mengapa* (SRT-007); *kenapa* ragam percakapan santai (hlm. 55).
2. **Pola:** *haturkan terima kasih* / *menghaturkan puji syukur* → **Perbaikan:** *ucapkan terima kasih* / *sampaikan terima kasih* — **Sebab:** bentuk *haturkan/menghaturkan* (SRT-008) tidak baku dalam bahasa Indonesia resmi (hlm. 52).

---

### BO. Bagian Pelengkap Buku & Penyuntingan Naskah (Untoro dkk., Badan Bahasa 2023/2024, `PPN-005`)

1. **Pola:** menukar penamaan **Kata Pengantar**, **Sambutan**, **Prakata**, dan **Sekapur Sirih** → **Perbaikan:** bedakan sesuai penulisnya: **Kata Pengantar** ditulis orang lain/pimpinan (≤1 hlm.), **Sambutan** ditulis pemangku kepentingan di atas penulis Kata Pengantar, **Prakata** ditulis penulis buku sendiri, dan **Sekapur Sirih** adalah prakata khusus karya sastra (`PPN-005`, hlm. 84–88).
2. **Pola:** judul buku memakai bentuk ulang berimbuhan kapital di kedua unsur (*Saat Lily Berjalan-Jalan*) → **Perbaikan:** hanya bentuk ulang utuh yang dikapitalkan kedua unsurnya (*Orang-Orang Pemberani*), sedangkan bentuk ulang berimbuhan tidak (*Saat Lily Berjalan-jalan*) (`PPN-005`, hlm. 62).
