---
name: humanizer-id-ejaan-morfologi
description: Use when fixing ejaan, morfologi, dan bentuk baku Indonesia.
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

# Humanizer ID — Ejaan Morfologi

Sub-kaidah Humanizer ID. Muat berkas ini setelah `humanizer-id` (induk) menentukan mode kerja. Aturan integritas ilmiah pada induk tetap mengikat penuh.

---

### G. Kaidah Morfologi Baku (EYD V & TBBBI)

1. **Pola:** *mempengaruhi / merubah / mensintesis / mentargetkan* → **Perbaikan:** *memengaruhi / mengubah / menyintesis / menargetkan* — **Sebab:** peluluhan KTSP pada prefiks *meN-*; gugus konsonan rangkap tetap (*menstabilkan, mentransmisikan, mempraktikkan*) (EYD V).
2. **Pola:** *pasca bencana / antar simpul / multi disiplin / sub bagian / non formal* → **Perbaikan:** *pascabencana, antarsimpul, multidisiplin, subbagian, nonformal* — **Sebab:** bentuk terikat ditulis serangkai.
3. **Pola:** *faktor2 / metode2* → **Perbaikan:** *faktor-faktor / metode-metode* — **Sebab:** reduplikasi wajib tanda hubung, angka 2 adalah gaya pesan instan; bila sudah diawali penanda jamak (*berbagai, beberapa*) hindari perulangan ganda (*berbagai faktor*, bukan *berbagai faktor-faktor*).
4. **Pola:** *BAPPENAS / TILANG* (akronim) → **Perbaikan:** *Bappenas / tilang* — **Sebab:** akronim nama diri > 3 huruf kapital di awal saja; akronim bukan nama diri ditulis kecil seluruhnya.
5. **Pola:** *S.T, M.T, Prof, Dr* → **Perbaikan:** *S.T., M.T., Prof., Dr.* — **Sebab:** singkatan gelar/sapaan diakhiri tanda titik.
6. **Pola:** *apapun / datainipun* → **Perbaikan:** *apa pun / data ini pun* — **Sebab:** partikel *pun* ditulis terpisah, kecuali 12 kata hubung baku leksikal (*meskipun, adapun, maupun, biarpun, walaupun*).
7. **Pola:** *Dalam penelitian ini menunjukkan...* → **Perbaikan:** *Penelitian ini menunjukkan...* / *Dalam penelitian ini ditunjukkan...* — **Sebab:** preposisi pembuka tidak boleh merusak subjek.
8. **Pola:** *analisa, praktek, resiko, standarisasi, efektifitas, metodologi* → **Perbaikan:** *analisis, praktik, risiko, standardisasi, efektivitas, metode* — **Sebab:** bentuk baku KBBI; *metode* untuk rangkaian kerja.
9. **Pola:** *menggaris bawahi / mempertanggung jawabkan* → **Perbaikan:** *menggarisbawahi / mempertanggungjawabkan* — **Sebab:** gabungan kata berkonfiks (awalan+akhiran) wajib serangkai.
10. **Pola:** *50cm / 240MHz* → **Perbaikan:** *50 cm / 240 MHz* — **Sebab:** satuan ukur dipisah spasi setelah angka.
11. **Pola:** *raja hutan* (untuk harimau) → **Perbaikan:** *harimau* — **Sebab:** karya ilmiah wajib makna denotatif, bukan konotatif/kiasan; kata ganti orang pertama menurunkan nilai rubrik resmi buku teks.

> **Rujukan buku teks resmi:** Kaidah di atas diekstrak dari buku *Cerdas Cergas Berbahasa dan Bersastra Indonesia untuk SMA/MA/SMK/MAK Kelas XI* (Edisi Revisi, Kemendikbudristek, 2024; ISBN 978-623-388-439-6), Bab VI hlm. 210–215. Detail contoh salah→benar lengkap tersedia di `references/ekstrak-buku-teks-kemdikbud.md`, dan empat entri baru (`BSE-001`–`BSE-004`) sudah aktif di `data/kalke-indonesia.json` serta terdeteksi oleh `scripts/audit.py`.

---
### I. Kata Tidak Baku dalam Surat Resmi (Teka-Teki Silang Buku Siswa XII, hlm. 33)

1. **Pola:** *ampun, mau, bales, gue, makasih, ngirim, bilang, ngak, pengen, soalnya* → **Perbaikan:** *maaf/tolong, menginginkan, membalas, saya/menurut saya, terima kasih, mengirim, menyatakan, tidak, ingin, karena* — **Sebab:** kata percakapan tidak baku wajib diganti padanan KBBI pada ragam formal.

---
### Q. Ketentuan Tanda Koma pada Konjungsi Intrakalimat & Antarkalimat (Rujukan Buku Kelas XII Kemendikbudristek 2024 & Alwi dkk. 2017)

1. **Pola:** *Model A sangat cepat tetapi membutuhkan memori besar* → **Perbaikan:** *Model A sangat cepat, tetapi membutuhkan memori besar.* — **Sebab:** konjungsi intrakalimat (*tetapi, namun, sedangkan, melainkan, bahkan, padahal, kecuali, kemudian, lalu, lantas*) wajib diawali koma.
2. **Pola:** *Akurasi naik, sehingga efisiensi meningkat / Sistem berhenti, karena kegagalan daya* → **Perbaikan:** *Akurasi naik sehingga efisiensi meningkat / Sistem berhenti karena kegagalan daya* — **Sebab:** konjungsi intrakalimat (*dan, atau, bahwa, karena, sehingga, agar, apabila, jika, maka*) ditulis tanpa koma pendahulu.
3. **Pola:** *Oleh karena itu / Selain itu / Dengan demikian* tanpa koma lanjutan → **Perbaikan:** *Oleh karena itu, / Selain itu, / Dengan demikian,* — **Sebab:** konjungsi antarkalimat selalu di awal kalimat baru, didahului titik dan diikuti koma.

---
### W. Kaidah Huruf Kapital Nama Jenis, Turunan Bangsa, & Jabatan Umum (Rujukan Modul Direktorat SMA Kemendikbud 2020, KD 3.12, hlm. 24–34)

1. **Pola:** *Kunci Inggris, Pisang Ambon, Mesin Diesel, 15 Watt* → **Perbaikan:** *kunci inggris, pisang ambon, mesin diesel, 15 watt* — **Sebab:** nama diri geografi/orang yang menjadi nama jenis atau satuan ukuran ditulis huruf kecil semua.
2. **Pola:** *Peng-Indonesia-an, Keinggris-Inggrisan* → **Perbaikan:** *pengindonesiaan, keinggris-inggrisan* — **Sebab:** bentuk dasar turunan nama bangsa/bahasa ditulis huruf kecil.
3. **Pola:** *Sejumlah Menteri menghadiri rapat Kabinet* → **Perbaikan:** *Sejumlah menteri menghadiri rapat kabinet* — **Sebab:** jabatan/pangkat tanpa nama spesifik ditulis kecil; kapital hanya bila merujuk spesifik (*Menteri Keuangan Republik Indonesia, Gubernur Jawa Barat*).
4. **Pola:** *Kapan bapak berangkat? / rumah Paman dan Bibi* → **Perbaikan:** *Kapan Bapak berangkat? / rumah paman dan bibi* — **Sebab:** sapaan langsung/pengacuan kapital; relasi keluarga umum ditulis kecil.
5. **Pola:** *republik indonesia / Perserikatan Bangsa Bangsa* → **Perbaikan:** *Republik Indonesia / Perserikatan Bangsa-Bangsa* — **Sebab:** nama resmi lembaga/dokumen kapital semua unsur kecuali kata tugas; bentuk ulang sempurna tetap bertanda hubung.
6. **Pola:** *Robin Van Persie* → **Perbaikan:** *Robin van Persie* — **Sebab:** partikel nama asing (Belanda/Jerman/Portugal/Jawa) ditulis huruf kecil.

---
### X. Kalimat Definisi (adalah vs merupakan) & Penulisan Imbuhan di- (Rujukan Buku Siswa Kelas X Edisi Revisi Kemendikbudristek 2022)

1. **Pola:** *Belalang anggrek adalah predator polifagus* → **Perbaikan:** *Belalang anggrek merupakan predator polifagus* — **Sebab:** *adalah* untuk pengertian mutlak (ekuivalensi A = B); *merupakan* untuk penempatan objek dalam kategori.
2. **Pola:** *di analisis, di observasi* → **Perbaikan:** *dianalisis, diobservasi, diteliti, dikembangkan* — **Sebab:** imbuhan pembentuk kata kerja pasif wajib serangkai.
3. **Pola:** *dilaboratorium, dimasa kini* → **Perbaikan:** *di laboratorium, di lapangan, di masa kini* — **Sebab:** preposisi penunjuk tempat/waktu wajib ditulis terpisah.
4. **Pola:** kutipan tidak langsung tanpa halaman → **Perbaikan:** *(Pengarang, tahun: halaman)* atau *Pengarang (tahun: halaman) menyatakan bahwa...* — **Sebab:** format CMS 17; sumber daring wajib frasa *diakses pada <tanggal>*.

---
### Z. Penulisan Gabungan Kata: Terpisah vs Senyawa & Unsur Terikat (Rujukan Seri Penyuluhan 1: Ejaan dalam Bahasa Indonesia, Pusat Bahasa Depdikbud)

1. **Pola:** *tanggungjawab, kerjasama, tandatangan, terimakasih, ujicoba, kantorpos, dutabesar, cagaralam, tatasurya* → **Perbaikan:** *tanggung jawab, kerja sama, tanda tangan, terima kasih, uji coba, kantor pos, duta besar, cagar alam, tata surya* — **Sebab:** gabungan kata yang masih bebas ditulis terpisah.
2. **Pola:** *dari pada, barang kali, pada hal, sekali gus, bila mana, apa bila, mata hari, sapu tangan, bumi putra, segi tiga* → **Perbaikan:** *daripada, barangkali, padahal, sekaligus, bilamana, apabila, matahari, saputangan, bumiputra, segitiga* — **Sebab:** gabungan kata senyawa ditulis serangkai.
3. **Pola:** *sub unit, maha guru, peri laku, antar kota* → **Perbaikan:** *subunit, mahaguru, perilaku, antarkota* — **Sebab:** unsur terikat + kata dasar ditulis serangkai.
4. **Pola:** *non RRC, antar SMA* → **Perbaikan:** *non-RRC, antar-SMA, pan-Afrikanisme* — **Sebab:** pengecualian: diikuti huruf kapital memakai tanda hubung; *maha/peri* + kata berimbuhan terpisah (*maha mengetahui*), + kata dasar serangkai (*mahakasih*).
5. **Pola:** *anak2 / ber-kejar2-an* → **Perbaikan:** *anak-anak / berkejar-kejaran* — **Sebab:** angka 2 dilarang sebagai penanda reduplikasi; tulis lengkap dengan tanda hubung.

---
### AW. Morfofonemik Verba & Klitika Pasif (Rujukan TBBBI Edisi Keempat, Bab IV hlm. 110-118 & Lampiran 1 hlm. 412)

1. **Pola:** *letakan, tunjukan, masukan* (verba) → **Perbaikan:** *letakkan, tunjukkan, masukkan* — **Sebab:** dasar berakhiran /k/ bersufiks *-kan* wajib /k/ ganda (TBB-021); bentuk satu *k* tercadang untuk nomina (*masukan*).
2. **Pola:** *mengisii, memperbaikii* → **Perbaikan:** *mengisi, memperbaiki* — **Sebab:** sufiks *-i* menolak dasar berakhir /i/; bentukan *ii* ganda tidak berterima (TBB-022).
3. **Pola:** *mengulang-i-ulangi* (sufiks ikut direduplikasi) → **Perbaikan:** *mengulang-ulangi / menyulit-nyulitkan* — **Sebab:** reduplikasi verba bersufiks: sufiks tidak ikut diulang; yang diulang bentuk dasar berafiks (TBB-023).
4. **Pola:** *ku kumpulkan / kau pelajari* → **Perbaikan:** *kukumpulkan, kaupelajari* — **Sebab:** klitika pasif *ku-*, *kau-* ditulis serangkai dengan verba (TBB-024).
5. **Pola:** *membom, mencek, mempel, mentik* → **Perbaikan:** *mengebom, mengecek, mengepel, mengetik* — **Sebab:** prefiks *meng-* pada dasar tunggal bersuku satu memerlukan e- (TBB-027) (hlm. 144).
6. **Pola:** *memroduksi, memroses, memrogram, mengredit, menglaim* → **Perbaikan:** *memproduksi, memproses, memprogram, mengkredit, mengklaim* — **Sebab:** gugus /pr/, /pl/, /kl/, /tr/, /kr/ tidak luluh (TBB-028) (hlm. 144).
7. **Pola:** *Tetapi, ...* (memulai kalimat) → **Perbaikan:** *Akan tetapi, ... / Namun, ...* — **Sebab:** konjungsi koordinatif *tetapi* dilarang memulai kalimat (TBB-029) (hlm. 417).
8. **Pola:** *amat sangat / sangat amat* → **Perbaikan:** pilih satu (*amat sangat* → *sangat* atau *amat*) — **Sebab:** penumpukan pewatas elatif: *amat, sangat, sekali* setara; gabungan dilarang ragam baku tulis (TBB-030) (hlm. 229).
9. **Pola:** *membicarakan tentang, membahas mengenai, mengetahui akan* → **Perbaikan:** *membicarakan, membahas, mengetahui* (langsung) — **Sebab:** verba transitif langsung mengikat objek tanpa preposisi pleonastis (TBB-031) (hlm. 129).

---

### AZ. Penyerapan Imbuhan Asing (Rujukan "Tata Istilah Indonesia", Pusat Pembinaan dan Pengembangan Bahasa, Subbab 7.7.1.2 hlm. 55-57)

1. **Pola:** *pointwise, piecewise, stepwise* → **Perbaikan:** *titik demi titik, cebis demi cebis, langkah demi langkah* — **Sebab:** akhiran distributif *-wise* diserap pola reduplikasi bersisipan *demi* (TII-006).
2. **Pola:** *harmonious, analogous* → **Perbaikan:** *berharmoni, beranalog* — **Sebab:** akhiran sifat *-ous* bermakna 'bersifat' diserap prefiks *ber-* (TII-007).
3. **Pola:** *addend, multiplicand* → **Perbaikan:** *bilangan yang ditambah, bilangan yang dikalikan* — **Sebab:** istilah matematika berakhiran *-and/-end* diserap konstruksi pasif penjelas (TII-008).
4. **Pola:** *absorber, analyzer, mixer* → **Perbaikan:** *penyerap/alat serap, penganalisis/alat analisis, pencampur* — **Sebab:** akhiran agen/instrumen *-er/-or* diserap prefiks *pe-* atau gabungan *alat* (TII-009).

---

### BD. Tanda Baca & Gabungan Kata Ejaan Baku (Rujukan "Seri Penyuluhan 1: Ejaan dalam Bahasa Indonesia", Pusat Bahasa Depdikbud, Bab III hlm. 10-12 & Bab IV hlm. 30-39)

1. **Pola:** *ia membatalkan rencana, karena...* → **Perbaikan:** *ia membatalkan rencana karena...* — **Sebab:** koma terlarang sebelum kausal/final bila anak kalimat mengiringi di belakang induk; koma hanya wajib bila anak kalimat mendahului induk (SPE-001).
2. **Pola:** *berterimakasih* → **Perbaikan:** *berterima kasih, bertanda tangan, bersepak bola, membabi buta* — **Sebab:** gabungan berawalan saja tetap terpisah tanpa tanda hubung (SPE-002).
3. **Pola:** *Namun / Bahkan / Kemudian / Lagi pula / Sebenarnya* tanpa koma → **Perbaikan:** *Namun, Bahkan, Kemudian, Lagi pula, Sebenarnya,* — **Sebab:** ungkapan penghubung di awal kalimat wajib diikuti koma (SPE-003).
4. **Pola:** dua klausa setara digabung koma tanpa konjungsi → **Perbaikan:** pisah dengan titik koma — **Sebab:** titik koma memisahkan klausa setara tanpa konjungsi koordinatif [telaah] (SPE-004).

---

### BE. Bentuk Terikat Maha, Kekerabatan Kapital, dan Reduplikasi Resmi (Rujukan "Seri Penyuluhan 9: Ejaan Bahasa Indonesia yang Disempurnakan", Pusat Bahasa Depdikbud, hlm. 34-36)

1. **Pola:** *maha siswa, maha kuasa* → **Perbaikan:** *mahasiswa, mahakuasa, mahaesa, mahaguru* — **Sebab:** unsur terikat *maha* serangkai bila diikuti kata dasar; terpisah hanya bila diikuti kata turunan (*maha mengetahui*); *maha siswa* tidak baku (EYD-023).
2. **Pola:** *buku kakak, surat ibu* (sebagai sapaan/milik) → **Perbaikan:** *buku Kakak, surat Ibu* — **Sebab:** kata kekerabatan kapital bila pronomina sapaan/kemilikan, membedakannya dari nomina umum [telaah] (EYD-024).
3. **Pola:** *orang2, anak2* → **Perbaikan:** *orang-orang, anak-anak* — **Sebab:** angka 2 dilarang untuk reduplikasi dalam naskah resmi (EYD-025).

---

### BF. Ejaan Serapan, Singkatan PT, dan Tanda Hubung Tanggal (Rujukan "Seri Penyuluhan: Ejaan", Sriyanto, Badan Bahasa, 2015, hlm. 14, 17, 50, 91)

1. **Pola:** *da'wah, do'a, taqwa, qalbu* → **Perbaikan:** *dakwah, doa, takwa, kalbu* — **Sebab:** tidak ada kata baku dengan apostrof di tengah; huruf q diganti k (SPE-005) (hlm. 14).
2. **Pola:** *wudhu, bathin, shalat, ashar, shubuh, ustadz, hadits, adzan, dhuha, bhakti, dharma* → **Perbaikan:** *wudu, batin, salat, asar, subuh, ustaz, hadis, azan, duha, bakti, darma* — **Sebab:** digraf baku hanya *kh, ng, ny, sy*; bentuk lain tidak baku; *bhakti/dharma* kecuali nama diri resmi (SPE-006) (hlm. 17).
3. **Pola:** *PT. X* → **Perbaikan:** *PT X* — **Sebab:** singkatan nama badan/lembaga tidak diikuti titik (SPE-007) (hlm. 50).
4. **Pola:** *12-September-2024* → **Perbaikan:** *12 September 2024* — **Sebab:** bila nama bulan dieja huruf, tanda hubung dilarang (SPE-008) (hlm. 91).

---

### BG. Kapitalisasi Turunan Nama Bangsa & Penyerapan Konsonan Ganda (Rujukan PUEBI 2021, SK Kepala Badan Bahasa No. 0321/I/BS.00.00/2021, hlm. 7 & 47)

1. **Pola:** *peng-Indonesia-an, ke-Barat-baratan* → **Perbaikan:** *pengindonesiaan, keinggris-inggrisan, kejawa-jawaan* — **Sebab:** nama bangsa/suku/bahasa sebagai bentuk dasar turunan ditulis kecil tanpa strip (PUE-001) (hlm. 7).
2. **Pola:** *aksesoris* → **Perbaikan:** *aksesori* — **Sebab:** *cc* diserap *ks*; akhiran jamak Belanda tidak diserap (PUE-002) (hlm. 47).
3. **Pola:** *kharisma, kharismatik* → **Perbaikan:** *karisma, karismatik, kolera, karakter* — **Sebab:** *ch* lafal /k/ diserap k tunggal (PUE-003) (hlm. 47).
4. **Pola:** *eschelon, esselon* → **Perbaikan:** *eselon, mesin* — **Sebab:** *ch* lafal /s/ diserap s (PUE-004) (hlm. 47).

---

### BK. Tanda Hubung Prefiks Ejaan Resmi (EYD Lengkap & PUEBI 2016)

1. **Pola:** *seIndonesia, seAsia* → **Perbaikan:** *se-Indonesia, se-Asia, se-Jawa* — **Sebab:** awalan *se-* + kata berawal kapital wajib tanda hubung, bukan serangkai polos (EYD-026) (EYD hlm. 61).
2. **Pola:** *ke2, ke10* → **Perbaikan:** *ke-2, ke-10, ke-100* — **Sebab:** awalan *ke-* + angka ordinal wajib tanda hubung, bukan disatukan polos (EYD-027) (EYD hlm. 61).

---

### BM. Ortografi Morfologis & Gabungan Kata (Seri Penyuluhan Bentuk dan Pilihan Kata 2019)

1. **Pola:** *menunjukan, ditunjukan, mengontrakan* → **Perbaikan:** *menunjukkan, ditunjukkan, mengontrakkan, dikontrakkan* — **Sebab:** dasar berakhiran /k/ + akhiran *-kan* wajib dua huruf /k/ (BPK-032) (hlm. 41).
2. **Pola:** *penunjukkan, pendidikkan* → **Perbaikan:** *penunjukan, pendidikan, kenaikan, kebaikan* — **Sebab:** hiperkoreksi: konfiks *peng-...-an* dan *ke-...-an* berakhiran *-an* (bukan *-kan*); dasar berakhiran /k/ tetap satu huruf /k/ (BPK-033) (hlm. 42).
3. **Pola:** *pertanggungan jawab / pertanggung jawaban* → **Perbaikan:** *pertanggungjawaban* — **Sebab:** gabungan kata dasar *tanggung jawab* diapit konfiks *per-...-an* wajib diserangkaikan penuh (BPK-034) (hlm. 43).

---

### BQ. Bentuk Pasif Morfologis Takbaku & Pleonasme Penggolong Skripsi (Jurnal BB & Retorika)

1. **Pola:** *dikarenakan* → **Perbaikan:** *disebabkan (oleh)* atau *karena* — **Sebab:** *karena* konjungsi subordinatif kausatif, tidak membentuk verba pasif (JRN-005) (Jurnal BB Unmuh Jember 2020, hlm. 58).
2. **Pola:** *112 orang siswa / 40 orang responden* → **Perbaikan:** *112 siswa / 40 responden* — **Sebab:** pleonasme penggolong insani: nomina bernyawa tidak perlu *orang* setelah kardinal dalam penulisan kuantitatif metodologi (JRN-006) (Jurnal Retorika Uniflor 2022, hlm. 56).

---

### BR. Tipografi Tanda Baca & Simbol Logografis Skripsi (Jurnal Jurribah 2026 / EBI Ed. V)

1. **Pola:** *ATP & WTP / tour & travel* → **Perbaikan:** tulis penuh *dan* — **Sebab:** simbol logografis *&* sebagai pengganti konjungsi dalam narasi ilmiah melanggar kaidah akademik (JRN-007) (hlm. 479).
2. **Pola:** *Variabel : data* → **Perbaikan:** *Variabel: data* — **Sebab:** titik dua tidak boleh didahului spasi; tanda baca melekat kata pendahulu (JRN-008) (hlm. 479).

---

### BU. EYD Edisi V (2022), Seri Penyuluhan (2025), & Tata Naskah Dinas (2025)

1. **Pola:** *tuna karya, nara sumber, manca negara, semi permanen, sub tema, multi etnik, dwi bahasa* → **Perbaikan:** *tunakarya, narasumber, mancanegara, semipermanen, subtema, multietnik, dwibahasa* — **Sebab:** bentuk terikat (*tuna-, nara-, manca-, semi-, sub-, multi-, dwi-*) ditulis serangkai (EYD-042..057).
2. **Pola:** *rumahtangga, pertanggung jawaban* → **Perbaikan:** *rumah tangga, rumah sakit, tata bahasa, tata cara* (terpisah); *pertanggungjawaban* (serangkai) — **Sebab:** gabungan kata bebas tanpa konfiks terpisah; berkonfiks penuh serangkai.
3. **Pola:** *garisbawahi, tandatangani, sebarluaskan, lipatgandakan, bebastugaskan, ujicobakan* → **Perbaikan:** *garis bawahi, tanda tangani, sebar luaskan, lipat gandakan, bebas tugaskan, uji cobakan* — **Sebab:** gabungan kata berimbuhan tunggal (awalan/akhiran saja) tetap terpisah (SPE-009..018, BPK-043..045, DIN-005).
4. **Pola:** *penandatangan, penanggungjawab, bekerjabakti* → **Perbaikan:** *penanda tangan, penanggung jawab, bekerja bakti, kami beri tahukan* — **Sebab:** sama — berimbuhan tunggal tetap terpisah; *waswas* tanpa tanda hubung, *dag-dig-dug* bertanda hubung.
5. **Pola:** *angkatan ke-XI* → **Perbaikan:** *angkatan XI* / *angkatan ke-11* — **Sebab:** hindari *ke-* + angka Romawi (SPE-011..012, DIN-006..007).
6. **Pola:** *S1, S2, D3* → **Perbaikan:** *S-1, S-2, S-3, D-3, D-4* — **Sebab:** jenjang wajib bertanda hubung.
7. **Pola:** *NIP. 198204...* → **Perbaikan:** *NIP 198204...* — **Sebab:** *NIP* tidak bertitik sebelum nomor; sedangkan *a.n.*, *Plt.*, *Plh.* wajib bertitik.
8. **Pola:** *mencabut, mencontoh* (bentuk lama) → **Perbaikan:** *mencabut, mencontoh, ditemukan, mengaktifkan, mengesampingkan, mengkritik, mengklasifikasi, berkaitan* — **Sebab:** bentuk baku yang disarankan (BPK-035..042, BPK-046, DIN-008..009, SPK-010..011).
9. **Pola:** *saling berpandangan* → **Perbaikan:** *berpandangan* — **Sebab:** hindari resiprokal *saling ber-...-an*.
10. **Pola:** *memberitahukan kepada ... bahwa / Bagi semua ... menyerahkan* → **Perbaikan:** buang kata hubung berlebih; *... menyerahkan* — **Sebab:** kalimat efektif: hindari *kepada ... bahwa* dan *Bagi ... menyerahkan*.
11. **Pola:** *walaupun/meskipun ..., namun ...* → **Perbaikan:** *walaupun/meskipun X, Y* — **Sebab:** hindari ganda konjungsi konsesif.
12. **Pola:** *disebabkan/dikarenakan terjadinya* → **Perbaikan:** *disebabkan oleh / karena* — **Sebab:** hindari *disebabkan/dikarenakan terjadinya* (tidak baku).

### BV2. Huruf Kapital Khusus EYD V (Rujukan EYD Edisi V, SK Kepala Badan Bahasa No. 0424/I/BS.00.01/2022, Bab I F — transkrip Wikisource)

1. **Pola:** *teori darwin / hukum archimedes / rumus pythagoras* → **Perbaikan:** *teori Darwin / hukum Archimedes / rumus Phytagoras* — **Sebab:** kapital pada nama orang dalam nama teori, hukum, dan rumus (Butir 4 Bab I F, hlm. 8; `EYD-058`).
2. **Pola:** *Fatimah Binti Salim / Charles Adriaan Van Ophuijsen* → **Perbaikan:** *Fatimah binti Salim / Charles Adriaan van Ophuijsen* — **Sebab:** kata bermakna “anak dari” (*bin, binti, boru, van*) nonkapital di tengah nama, kecuali di awal nama atau kata tugas *dari* (Butir 5 Bab I F, hlm. 8; `EYD-059`).
3. **Pola:** *Proklamasi kemerdekaan / Perang Dunia* (peristiwa sejarah generik) → **Perbaikan:** *proklamasi kemerdekaan / perang dunia* — **Sebab:** peristiwa sejarah yang tidak digunakan sebagai nama ditulis nonkapital (Butir 15 Bab I F, hlm. 11; `EYD-060`).
4. **Pola:** *batik cirebon / soto banjar / kopi gayo / bubur manado* → **Perbaikan:** *batik Cirebon / soto Banjar / kopi Gayo / bubur Manado* — **Sebab:** nama geografi yang menyatakan asal daerah ditulis kapital (Butir 19 Bab I F, hlm. 12; `EYD-061`).
5. **Pola:** *buku bahasa dan sastra / majalah bahasa dan sastra* → **Perbaikan:** *buku Bahasa dan Sastra / majalah Bahasa dan Sastra* — **Sebab:** kapital semua kata (termasuk kata ulang sempurna) pada nama buku/majalah/surat kabar/judul karangan, kecuali kata tugas non-awal (EYD 1987 butir 12 Bab II; `EYD-062`).
6. **Pola:** kutipan langsung bahasa asing/daerah tanpa pencetakan miring → **Perbaikan:** cetak miring seluruh kutipan asing — **Sebab:** kalimat/teks asing yang dikutip langsung wajib miring (PUEBI 2015 Bab I hlm. 12; `EYD-063`).
7. **Pola:** *Michael Porter / World Bank* (nama diri asing) ditulis miring → **Perbaikan:** tulis tegak — **Sebab:** nama diri asing/daerah (orang, lembaga, organisasi) tidak ditulis miring (PUEBI 2015 Bab I hlm. 12; `EYD-064`).

> **Sumber verbatim:** teks resmi EYD V tersedia via transkripsi Wikisource Indonesia (`Halaman:SK_EYD_Edisi_V_16082022.pdf`) — detail pemetaan di `references/eyd-v-wikisource-2022.md`. PUEBI (SK 0321/I/BS.00.00/2021) telah dicabut oleh EYD V (Diktum KEEMPAT).

---

### BW. Penyerapan Istilah Asing (Rujukan PUPI, Kepmendiknas 146/U/2004, Bab II.4.2, III.11, IV.2 — transkrip Wikisource)

1. **Pola:** *frekwensi* → **Perbaikan:** *frekuensi* — **Sebab:** sufiks *-ency* diserap menjadi *-ensi* dan gugus *qu* menjadi *ku*, bukan *kw* (`PUPI-002`) (PUPI II.4.2.2.b).
2. **Pola:** *subyektif* → **Perbaikan:** *subjektif* — **Sebab:** *subject* diserap menjadi *subjek*; turunan bersufiks *-ive* menjadi *-if* (`PUPI-003`) (PUPI II.4.2.2.b).
3. **Pola:** *propinsi* → **Perbaikan:** *provinsi* — **Sebab:** penyesuaian ejaan serapan *province*; bentuk dengan *p* ganda tidak baku (`PUPI-004`) (PUPI II.4.2.1).
4. **Pola:** *komplek* → **Perbaikan:** *kompleks* — **Sebab:** gugus konsonan akhir serapan *-x* disesuaikan menjadi *-ks* (`PUPI-005`) (PUPI II.4.2.1).
5. **Pola:** *jaman* → **Perbaikan:** *zaman* — **Sebab:** bentuk baku serapan Arab memakai *z*, bukan *j* (`PUPI-006`) (KBBI).
6. **Pola:** *kaedah* → **Perbaikan:** *kaidah* — **Sebab:** bentuk baku serapan Arab *qa'idah* adalah *kaidah* (`PUPI-007`) (KBBI).
7. **Pola:** *managemen* → **Perbaikan:** *manajemen* — **Sebab:** penyesuaian ejaan serapan *management*; vokal pada suku kedua menjadi *a* (`PUPI-008`) (PUPI II.4.2.1).
8. **Pola:** *ekstrim* → **Perbaikan:** *ekstrem* — **Sebab:** bentuk baku serapan *extreme* adalah *ekstrem* (`PUPI-009`) (KBBI).
9. **Pola:** *pra sekolah / pra kondisi* → **Perbaikan:** *prasekolah / prakondisi* — **Sebab:** bentuk terikat *pra-* (pre-) menempel langsung pada bentuk dasar (`PUPI-010`) (PUPI II.4.2.2.a).
10. **Pola:** *ekstra kurikuler / extra kulikuler* → **Perbaikan:** *ekstrakurikuler* — **Sebab:** prefiks asing *extra-* diserap menjadi *ekstra-* dan ditulis serangkai dengan bentuk dasar (`PUPI-011`) (PUPI II.4.2.2.a).
11. **Pola:** *anti korupsi / anti virus* → **Perbaikan:** *antikorupsi / antivirus* — **Sebab:** prefiks *anti-* tetap *anti-* dan menempel pada bentuk dasar (`PUPI-012`) (PUPI II.4.2.2.a).
12. **Pola:** *multi disiplin / multi fungsi* → **Perbaikan:** *multidisiplin / multifungsi* — **Sebab:** prefiks *multi-* menempel langsung pada bentuk dasar (`PUPI-013`) (PUPI II.4.2.2.a).
13. **Pola:** *globalization / modernization / naturalization* → **Perbaikan:** *globalisasi / modernisasi / naturalisasi* — **Sebab:** sufiks *-isatie/-ization* diserap menjadi *-isasi*, bukan dipertahankan mentah (`TII-010`) (PUPI II.4.2.2.b).
14. **Pola:** *technology / methodology / analogy* → **Perbaikan:** *teknologi / metodologi / analogi* — **Sebab:** sufiks *-logie/-logy* diserap menjadi *-logi* (`TII-011`) (PUPI II.4.2.2.b).
15. **Pola:** *reality / facility / university* → **Perbaikan:** *realitas / fasilitas / universitas* — **Sebab:** sufiks *-iteit/-ity* diserap menjadi *-itas* (`TII-012`) (PUPI II.4.2.2.b).
16. **Pola:** *expressionism / modernism / extremism* → **Perbaikan:** *ekspresionisme / modernisme / ekstremisme* — **Sebab:** sufiks *-isme (Belanda), -ism (Inggris)* diserap menjadi *-isme* (`TII-013`) (PUPI II.4.2.2.b).
17. **Pola:** *hyperglycemia / polyamide / phototherapy* → **Perbaikan:** *hiperglikemia / poliamida / fototerapi* — **Sebab:** prefiks *hyper-, hypo-, poly-, photo-* diserap menjadi *hiper-, hipo-, poli-, foto-* (`TII-014`) (PUPI II.4.2.2.a).
18. **Pola:** *5 Mg / 3 Kg / 10 KM / 5 Newton* → **Perbaikan:** *5 mg / 3 kg / 10 km / 5 newton* — **Sebab:** lambang satuan berhuruf kecil; lambang dari nama orang kapital (N, A, K), bentuk lengkapnya huruf kecil (`TII-015`) (PUPI III.11).
19. **Pola:** [telaah] *antarmuka* di bab kedua, *interface* di bab ketiga, *antar muka* di lampiran → **Perbaikan:** satu istilah baku per konsep, dipakai konsisten — **Sebab:** istilah sinonim dalam satu bidang sebaiknya dibakukan agar naskah tidak membingungkan pembaca (`TII-016`) (PUPI IV.2).

#### Tabel rujukan penyesuaian ejaan serapan (PUPI II.4.2.2)

| Sufiks asing | Serapan Indonesia | Contoh |
|---|---|---|
| *-iteit, -ity* | *-itas* | facility → fasilitas, quality → kualitas |
| *-isatie, -ization* | *-isasi* | naturalization → naturalisasi |
| *-atie, -(a)tion* | *-(a)si* | action → aksi, publication → publikasi |
| *-logie, -logy* | *-logi* | technology → teknologi |
| *-iek, -ic, -ique* | *-ik* | periodic → periodik, unique → unik |
| *-isch, -ic, -ical* | *-is* | optimistic → optimistis |
| *-ance, -ence* | *-ans, -ens* | ambulance → ambulans |
| *-ancy, -ency* | *-ansi, -ensi* | frequency → frekuensi |
| *-teit, -ty* | *-tas* | university → universitas |
| *-eur, -or* | *-ir, -ur* | amateur → amatir, director → direktur |
| *-archie, -archy* | *-arki* | monarchy → monarki |
| *-lyse, -lysis* | *-lisis* | analysis → analisis |

| Prefiks asing | Serapan Indonesia | Contoh |
|---|---|---|
| *cata-* | *kata-* | catalyst → katalis |
| *co-, com-, con-* | *ko-, kom-, kon-* | coordination → koordinasi |
| *contra-* | *kontra-* | contradiction → kontradiksi |
| *eco-* | *eko-* | ecology → ekologi |
| *ex-* | *eks-* | exclusive → eksklusif |
| *extra-* | *ekstra-* | extraterrestrial → ekstraterestrial |
| *hexa-* | *heksa-* | hexagon → heksagon |
| *hyper-, hypo-* | *hiper-, hipo-* | hyperemia → hiperemia |
| *post-* | *pasca-* | — |
| *pre-* | *pra-* | — |

> **Sumber verbatim:** seluruh kaidah di atas bersumber dari `references/pupi-2004-kepmendiknas146.md` (Kepmendiknas 146/U/2004, transkrip Wikisource Indonesia). Bentuk leksikal (*zaman, kaidah, ekstrem, propinsi*) diperiksa silang ke KBBI.

---

### BX. Bentuk Baku Serapan & Morfologi Terbitan Ilmiah (Winarti dkk., *Kesalahan Berbahasa Indonesia dalam Terbitan Ilmiah Perguruan Tinggi di Kalimantan Timur*, Pusat Bahasa, 2009)

1. **Pola:** *salahsatunya, ditindak Ianjuti, unjukrasa, lagipula, non aktif* → **Perbaikan:** *salah satunya, tindak lanjut, unjuk rasa, lagi pula, nonaktif* — **Sebab:** gabungan kata ditulis terpisah, sedangkan bentuk berimbuhan gabung ditulis serangkai; *ditindaklanjuti* dan *menindaklanjuti* tetap sah (TMS-030).
2. **Pola:** *kordinator, kordinasi, mengkomentari* → **Perbaikan:** *koordinator, koordinasi, mengomentari* — **Sebab:** serapan *coordination* mempertahankan vokal *o* ganda; *mengomentari* berpangkal *komentar* sehingga tidak ada fonem luluh (TMS-031).
3. **Pola:** *legalisir, inventarisir, terakomodir, terorganisir, mengkoordinir* → **Perbaikan:** *dilegalisasi, menginventarisasi, terakomodasi, terorganisasi, mengoordinasi* — **Sebab:** akhiran *-ir* warisan Belanda tidak produktif; bentuk baku memakai *-isasi*/*-asi* (TMS-032).
4. **Pola:** *tehknik, enerjik, rejional, aktip, perogram* → **Perbaikan:** *teknik, energik, regional, aktif, program* — **Sebab:** digraf baku hanya *kh, ng, ny, sy*; *j* mewakili /dʒ/ pada *regional*; *-ip* dan *pe-* menyimpang dari bentuk serapan (TMS-033).
5. **Pola:** *akte, beaya, efektip, effektif, effisien* → **Perbaikan:** *akta, biaya, efektif, efisien* — **Sebab:** bentuk baku serapan menetapkan *akta*, *biaya*, dan konsonan tunggal *f/s* (TMS-036).
6. **Pola:** *memposisikan, marjinal, hektar* → **Perbaikan:** *memosisikan, marginal, hektare* — **Sebab:** fonem /p/ luluh setelah awalan *meng-*; *marginal* bukan *marjinal*; *hektare* mempertahankan vokal akhir (TMS-039).
7. **Pola:** *menghasil, diprioritas* → **Perbaikan:** *menghasilkan, diprioritaskan* — **Sebab:** nomina *hasil* dan *prioritas* hanya menerima konfiks *meng-...-kan*, bukan awalan tunggal (TMS-040; KK-004).
8. **Pola:** *respon* → **Perbaikan:** *respons* — **Sebab:** serapan *response* mempertahankan *-s* akhir; *responden* dan *responsif* tetap sah (TMS-041).
9. **Pola:** *teoritis, sekedar* → **Perbaikan:** *teoretis, sekadar* — **Sebab:** *teoretis* diserap dari *theoretical*, bukan teori + *-tis*; *sekadar* berpangkal *kadar* + *se-* (TMS-042).
10. **Pola:** *merubah, mentargetkan, analisa, praktek, mengaktipkan, penanggungjawab, bekerjabakti, tandatangani* → **Perbaikan:** *mengubah, menargetkan, analisis, praktik, mengaktifkan, penanggung jawab, bekerja bakti, menandatangani* — **Sebab:** bentuk dasar berfonem /r/, /t/, /p/ dan gabungan kata yang selama ini belum bermesin sekarang ikut diperiksa (BAK-002, BAK-004, BAK-005, BAK-007, BPK-038, BPK-044, BPK-045, SPE-014).
11. **Pola:** *sudah kumpul, telah jumpa, sampai jumpa* → **Perbaikan:** *sudah berkumpul, telah berjumpa, sampai berjumpa* — **Sebab:** verba berobjek tak langsung menuntut awalan *ber-*; bentuk tanpa awalan tidak baku (TMS-035).
12. **Pola:** *menstimulir, panili, disekitar, diareal, diladang* → **Perbaikan:** *menstimulasi, vanili, di sekitar, di area, di ladang* — **Sebab:** *stimulir* sudah verba sehingga *meng-* ganda; *panili* penyerapan keliru; preposisi *di* ditulis terpisah dari kata yang mengikutinya (TMS-037).

---

### BZ. Kaidah Lengkap EYD Edisi V (SK 0424/I/BS.00.01/2022) & Seri Penyuluhan Ejaan v2

1. **Pola:** *darma bakti, suka rela, sapu tangan, bela sungkawa, mana suka, ada kalanya* → **Perbaikan:** *darmabakti, sukarela, saputangan, belasungkawa, manasuka, adakalanya* — **Sebab:** EYD Edisi V Bab II.B.3.e membakukan gabungan kata padu tersebut ditulis serangkai (EYD-065) (hlm. 20-21).
2. **Pola:** *tandamata, kakitangan, kakilima, orangtua, berpestapora, kerjabaktikan* → **Perbaikan:** *tanda mata, kaki tangan, kaki lima, orang tua, berpesta pora, kerja baktikan* — **Sebab:** gabungan kata bebas dan gabungan kata yang hanya berawalan saja atau berakhiran saja ditulis terpisah (EYD-066) (hlm. 19-20).
3. **Pola:** *menyama ratakan, menganak tirikan, mengambing hitamkan, ketidak tahuan, keputus asaan* → **Perbaikan:** *menyamaratakan, menganaktirikan, mengambinghitamkan, ketidaktahuan, keputusasaan* — **Sebab:** gabungan kata yang mendapat awalan dan akhiran sekaligus (konfiks penuh) ditulis serangkai (EYD-067) (hlm. 20).
4. **Pola:** *Yang Mahakuasa, eka bahasa, nir gagasan, antarjemput* → **Perbaikan:** *Yang Maha Kuasa, ekabahasa, nirgagasan, antar jemput* — **Sebab:** bentuk terikat keilmuan serangkai, *maha-* untuk sifat Tuhan ditulis terpisah berkapital, sedangkan *antar* bermakna 'bawa/kirim' pada *antar jemput* ditulis terpisah (EYD-068) (hlm. 18-19; Ejaan v2 hlm. 39).
5. **Pola:** *a/n, u/p, d/a, Rp. 50.000, Rp 50.000* → **Perbaikan:** *a.n., u.p., d.a., Rp50.000,00* — **Sebab:** singkatan surat dua huruf wajib bertitik per huruf; lambang `Rp` tanpa titik dan tanpa spasi sebelum angka (EYD-069) (hlm. 29, 31).
6. **Pola:** *(a). ..., ...?., ...!., skor 3:1* → **Perbaikan:** *(a) ..., ...?, ...!, skor 3-1* — **Sebab:** huruf/angka perincian berkurung tidak diikuti titik; tanda tanya/seru tidak bersanding dengan titik; skor pertandingan memakai tanda hubung (EYD-070) (hlm. 37, 47).
7. **Pola:** *akommodasi, asesoris, konsekwen, ekivalen, souvenir, diskripsi, stirio, espresso, tentrem* → **Perbaikan:** *akomodasi, aksesori, konsekuen, ekuivalen, suvenir, deskripsi, stereo, espreso, tenteram* — **Sebab:** EYD V Bab IV menyederhanakan konsonan ganda menjadi tunggal dan mempertahankan vokal sumber serta sisipan /e/ serapan daerah (EYD-071) (hlm. 57-75).
8. **Pola:** *tafakkur, ummat, kaffah, tammat, nasehat, hakekat, mahluk, shohih, udzur, dzalim, fikir, nafas* → **Perbaikan:** *tafakur, umat, kafah, tamat, nasihat, hakikat, makhluk, sahih, uzur, zalim, pikir, napas* — **Sebab:** penyerapan kata Arab dalam EYD V Bab IV tanpa konsonan rangkap dan tanpa digraf nonbaku (EYD-072) (hlm. 57-75).
9. **Pola:** kata asing/daerah diapit tanda petik (`"lockdown"`), atau rentang angka/tempat memakai tanda hubung (`1825-1830`) → **Perbaikan:** cetak miring (*lockdown*) dan tanda pisah (`1825—1830`) — **Sebab:** `[telaah]` ketentuan huruf miring, tebal, dan tanda pisah EYD V (EYD-073) (hlm. 14-16, 49).

---

### CA. Morfologi & Serapan Lanjutan Terbitan Ilmiah (Winarti dkk., 2009, Subbab 2.4–2.11)

1. **Pola:** *mengkursuskan, mengsukseskan, mensejahterakan, mempercayai, ditelarkannya* → **Perbaikan:** *mengursuskan, menyukseskan, menyejahterakan, memercayai, ditelurkannya* — **Sebab:** peluluhan fonem /k, p, t, s/ berlaku pada bentuk dasar *kursus, sukses, sejahtera, percaya*; bentuk dasar *telur* menjadi *ditelurkannya* (TMS-043) (hlm. 59-95).
2. **Pola:** *mendiskriditkan, sekertaris, sejogyanya, peraktek, ditolerir, konperensi* → **Perbaikan:** *mendiskreditkan, sekretaris, seyogianya, praktik, ditoleransi, konferensi* — **Sebab:** bentuk serapan baku KBBI tanpa akhiran *-ir* dan tanpa sisipan vokal keliru (TMS-044) (hlm. 81-115).
3. **Pola:** *tenagakerja, semi permeabel, menitik beratkan* → **Perbaikan:** *tenaga kerja, semipermeabel, menitikberatkan* — **Sebab:** gabungan kata bebas terpisah, bentuk terikat *semi-* serangkai, dan gabungan kata berkonfiks penuh serangkai (TMS-045) (hlm. 122-136).


---

### CE. Kesalahan Ejaan Skripsi Empiris & Adaptasi Serapan (Khair 2018; Saputra & Alber 2021; Yahya dkk. 2018; Baharman)

1. **Pola:** *misskoordinasi, volantilitas, investation, illegal* → **Perbaikan:** *miskoordinasi, volatilitas, investasi, ilegal* — **Sebab:** adaptasi istilah asing tidak menggandakan konsonan (`ss`, `ll`) dan tidak menyisipkan fonem *n* (*volantilitas*) (`TMS-047`) (Baharman, UNM, hlm. 11–15).
2. **Pola:** *pengetauan, cendrung, defenisi, kesangupan, alternative* → **Perbaikan:** *pengetahuan, cenderung, definisi, kesanggupan, alternatif* — **Sebab:** penghilangan fonem (*h*/*g*), pertukaran vokal *i*→*e*, dan ejaan Inggris *alternative* lazim muncul di proposal skripsi (`JSK-007`) (Khair 2018, hlm. 47–48).
3. **Pola:** *dikelas, kejenjang, disana, disini, disitu* → **Perbaikan:** *di kelas, ke jenjang, di sana, di sini, di situ* — **Sebab:** kata depan penunjuk lokasi dan arah (*di*, *ke*) wajib ditulis terpisah dari kata yang mengikutinya (`JSK-008`) (Khair 2018 hlm. 49; Saputra & Alber 2021 Data 8; Yahya dkk. 2018 hlm. 63).
4. **Pola:** *kaos, silahkan, membawah* → **Perbaikan:** *kaus, silakan, membawa* — **Sebab:** ejaan baku KBBI memakai *au* pada *kaus* dan tanpa penambahan *h* pada *silakan* maupun *membawa* (`JSK-009`) (Yahya dkk. 2018, hlm. 63–64).

---

### CH. Ejaan Surat Dinas, Kata Ulang, & Mekanisasi Tipografi Skripsi (Pusat Bahasa; KIBASP 2026; JURRIBAH 2026; DEIKTIS 2026)

1. **Pola:** *mempedomani, febuari, transpotasi, himbauan, menghimbau, menimalisir, meminimalisir* → **Perbaikan:** *memedomani, Februari, transportasi, imbauan, mengimbau, meminimalkan* — **Sebab:** peluluhan fonem *p*, kata dasar *imbau* tanpa *h*, ejaan serapan konsisten, dan verba baku *-kan* (`TMS-049`) (Nur Bety, hlm. 81–82; BRIN 2022, hlm. 17; JURRIBAH 2026, hlm. 478).
2. **Pola:** *kearah, didaerah, diluar, disamping, walikota, menindak lanjuti* → **Perbaikan:** *ke arah, di daerah, di luar, di samping, wali kota, menindaklanjuti* — **Sebab:** preposisi penunjuk arah/lokasi terpisah, gabungan kata bebas *wali kota* terpisah, sedangkan gabungan kata berkonfiks penuh serangkai (`TMS-050`, `TMS-051`) (Nur Bety, hlm. 82–84; Mardi Nugroho, hlm. 123).
3. **Pola:** *hal - hal, rata- rata, parameter- parameter, banyak nya, khusus nya, selesai.., yaitu;, Ssos, Msi, Spd, Amd, Mts* → **Perbaikan:** *hal-hal, rata-rata, parameter-parameter, banyaknya, khususnya, selesai., yaitu:, S.Sos., M.Si., S.Pd., A.Md., MTs* — **Sebab:** tanda hubung kata ulang rapat tanpa spasi, klitika *-nya* serangkai, satu titik penutup, titik dua setelah pemerinci, dan kapital awal setiap unsur gelar/lembaga (`EYD-074`, `EYD-075`, `JSK-012`..`014`) (Mardi Nugroho, hlm. 121–123; KIBASP 2026, hlm. 529–531).
4. **Pola:** *manjemen, sehinnga, lingkukngan, Google From, Whatsapp* serta `[telaah]` kapital penuh binomial (*IPOMOEA BATATAS*) dan kata tugas berkapital di tengah judul → **Perbaikan:** *manajemen, sehingga, lingkungan, Google Form, WhatsApp*, penulisan binomial miring berkapital genus (*Ipomoea batatas*), serta huruf kecil kata tugas judul (`JSK-015`, `JSK-018`) (JURRIBAH 2026; DEIKTIS 2026; KIBASP 2026).

---

### CK. Ejaan Surat Kabar, Singkatan Lembaga & Preposisi Lanjutan (Seri Penyuluhan 9 EYD; Prosiding Semiloka 2019)

1. **Pola:** *azasi, muqaddimah, akhlaq, centraal, romadhon, teknologie, kwota, extradiksi, effektiv, psikhologi, alkuran, ke-Tuhan-an, ma'siat, sa'at* → **Perbaikan:** *asasi, mukadimah, akhlak, sentral, Ramadan, teknologi, kuota, ekstradisi, efektif, psikologi, Al-Qur'an, ketuhanan, maksiat, saat* — **Sebab:** penyederhanaan konsonan ganda dan digraf serapan serta penghapusan apostrof palsu (`E9L-026`) (Seri Penyuluhan 9 EYD, hlm. 38–44).
2. **Pola:** *D.P.R., U.U.D., K.B., S.M.A., S.M.P.* → **Perbaikan:** *DPR, UUD, KB, SMA, SMP* — **Sebab:** singkatan gabungan huruf awal nama resmi lembaga, badan, dan dokumen ketatanegaraan ditulis kapital tanpa tanda titik (`E9L-027`) (hlm. 41, 43; EYD V).
3. **Pola:** *diseluruh, ditempat, diantara, ketengah* → **Perbaikan:** *di seluruh, di tempat, di antara, ke tengah* — **Sebab:** kata depan penunjuk tempat dan arah (*di, ke*) wajib dipisah dari nomina pengiringnya (`EYD-076`) (EYD V Bab II.G; Prosiding Semiloka 2019).

---

### CN. Penyuntingan Kebahasaan LIPI Press, Opini KD 3.11 & Ruang Publik (Siklus 31–32)

1. **Pola:** *keluar negeri, keluar kota, keluar daerah* (saat bermakna arah tempat) → **Perbaikan:** *ke luar negeri, ke luar kota, ke luar daerah* — **Sebab:** *ke luar* + keterangan tempat ditulis terpisah (berpasangan dengan *di luar* / *dari luar*), sedangkan *keluar* serangkai khusus aktivitas (`BRN-005`) (LIPI Press, hlm. 67 Butir 24).
2. **Pola:** *di malam hari, di siang hari, di pagi hari, di sore hari* → **Perbaikan:** *pada malam hari, pada siang hari, pada pagi hari, pada sore hari* — **Sebab:** keterangan waktu memakai preposisi *pada*, bukan *di* (`BRN-006`) (LIPI Press, hlm. 67 Butir 23).
3. **Pola:** *bertarap, sekala, sovenir, musholla, mushola, gajih, contemporer, boutique, photocopy, taxi, mall* → **Perbaikan:** *bertaraf, skala, suvenir, musala, gaji, kontemporer, butik, fotokopi, taksi, mal* — **Sebab:** penyesuaian ejaan kata baku KBBI/EYD V (`BRN-007`, `PSB-035`) (LIPI Press hlm. 60; Opini XII hlm. 31; Media Luar Ruang 2015 hlm. 22–89; Semiloka 2019 hlm. 241).
4. **Pola:** `[telaah]` penamaan lokal membalik urutan DM–MD ala Inggris (*East Park*) dan kalimat larangan tanpa `!` (`PSB-036`) (hlm. 110–124; Prosiding Semiloka 2019 hlm. 522–549).

---

### CP. Bentukan `se-`, Spasi Gelar Depan & Verba Lokasi (Latihan Kemahiran Badan Bahasa 2016)

1. **Pola:** *sekabupaten, seprovinsi, sejawa, seindonesia* → **Perbaikan:** *se-Kabupaten, se-Provinsi, se-Jawa, se-Indonesia* — **Sebab:** bentuk terikat *se-* diikuti nama geografis/negara memakai tanda hubung dan huruf awal kapital (`LKB-048`) (Kaniah dkk. 2016, hlm. 16/76).
2. **Pola:** *Prof.Ahmad, Dr.Maman, Ir.Budi* → **Perbaikan:** *Prof. Ahmad, Dr. Maman, Ir. Budi* — **Sebab:** gelar di depan nama wajib diakhiri tanda titik dan dipisahkan satu spasi dari nama (`LKB-049`) (Kaniah dkk. 2016, hlm. 12/71).
3. **Pola:** *mendatangkan lokasi / mendatangkan tempat / mendatangkan gedung* → **Perbaikan:** *mendatangi lokasi / mendatangi tempat / mendatangi gedung* — **Sebab:** verba *-kan* untuk objek yang dibawa/dihadirkan, sedangkan objek tempat statis wajib memakai akhiran *-i* (`LKB-051`) (hlm. 20–21/82).

---

### CS. Salam Surat Resmi, Spasi Satuan Ukur & Bentuk Baku MABBIM/Kemendikbud (Siklus 35–36)

1. **Pola:** *Dengan Hormat / Hormat Saya / Hormat Kami / Salam Takzim* → **Perbaikan:** *Dengan hormat, / Hormat saya, / Hormat kami, / Salam takzim,* — **Sebab:** hanya kata pertama salam surat resmi yang diawali huruf kapital (`SMD-003`) (Pusat Bahasa 1991, hlm. 17–18).
2. **Pola:** *50cm, 15m, 10kg, 25km* → **Perbaikan:** *50 cm, 15 m, 10 kg, 25 km* — **Sebab:** bilangan dan lambang satuan ukuran wajib dipisahkan satu spasi (`BSXI-001`) (*Cerdas Cergas Kelas XI*, hlm. 261).
3. **Pola:** *katagori, species, karaba* → **Perbaikan:** *kategori, spesies, keramba* — **Sebab:** pembakuan KBBI/EYD V dan rubrik *Wisata Kata* MABBIM (`BSXI-002`) (Kelas XI hlm. 260; *Buletin MABBIM* Vol. 15, 2024, hlm. 16–17).

---

### CV. Ragam Tulis Baku PT, Penyengauan Lisan & Bilangan Awal Kalimat (Siklus 37–38)

1. **Pola:** *keikut sertaan, legitimate, cendikia, cendikiawan, memperngaruhi* → **Perbaikan:** *keikutsertaan, legitimasi, cendekia, cendekiawan, memengaruhi* — **Sebab:** konfiks penuh serangkai, serapan baku, vokal *e* kedua pada *cendekia*, serta peluluhan fonem *p* (`TMS-052`) (Karenisa dkk. 2025, hlm. 27, 30; Ifnaldi 2021; UNJA).
2. **Pola:** *ngail, ngantuk, nabrak, nulis, nyubit, nyabut, nyari, nyuap, nolak, nanam, ketawa* → **Perbaikan:** *mengail, mengantuk, menabrak, menulis, mencubit, mencabut, mencari, menyuap, menolak, menanam, tertawa* — **Sebab:** penyengauan ragam tutur lisan tanpa awalan *meN-* maupun awalan daerah *ke-* dilarang masuk tulisan formal (`RGM-002`) (Halimah dkk. 2020, hlm. 110–111).
3. **Pola:** *50 siswa teladan... / 3 pemenang...* di awal kalimat → **Perbaikan:** *Lima puluh siswa teladan... / Tiga pemenang...* — **Sebab:** bilangan satu atau dua kata pada posisi awal kalimat wajib ditulis dengan huruf (`UIN-011`) (Halimah dkk. 2020, hlm. 61; EYD V).

---

### CX. Pedoman Penyuntingan Naskah Badan Bahasa 2023/2024 (Untoro dkk., Siklus 39)

1. **Pola:** tanda tanya dan tanda seru ganda atau berulang (*Apa?!*, *Awas!!!*, *Siapa???*) → **Perbaikan:** pilih satu tanda baca sesuai intonasi (*Apa?*, *Awas!*, *Siapa?*) — **Sebab:** penggabungan dan pengulangan tanda tanya/seru melanggar kaidah tanda baca baku (`PPN-001`, hlm. 64–65).
2. **Pola:** kapitalisasi kata kekerabatan berpewatas (*Pamanku*, *Paman Itu*, *Ibuku*, *Bapaknya* di tengah kalimat) → **Perbaikan:** *pamanku*, *paman itu*, *ibuku*, *bapaknya* — **Sebab:** kata kekerabatan berpewatas posesif/demonstrativa ditulis nonkapital (`PPN-002`, hlm. 60–61; EYD V).
3. **Pola:** kapitalisasi kata sandang *Si* / *Sang* di tengah kalimat/judul bukan unsur Tuhan (*Teladan Si Kambing*, *Rumah Sang Harimau*) → **Perbaikan:** *si Kambing*, *sang Harimau* (kapital hanya untuk *Sang Pencipta* / *Sang Hyang*) — **Sebab:** *si* dan *sang* adalah kata tugas (`PPN-003`, hlm. 62–63).
4. **Pola:** ungkapan terbata-bata memakai tanda hubung (*Si-si-siapa namamu?*) → **Perbaikan:** gunakan elipsis berspasi (*Si ... si ... siapa namamu?*) — **Sebab:** kaidah penyuntingan ungkapan terputus-putus (`PPN-004`, hlm. 65).
5. **Pola:** unsur serapan dan gabungan tidak baku (*khromosom*, *rhetorika*, *thema*, *hidrolik*, *seyogyanya*, *fotocopy*, *transkip*, *ijasah*, *pas photo*, `CV.`/`UD.`/`PD.` bertitik) → **Perbaikan:** *kromosom*, *retorika*, *tema*, *hidraulik*, *seyogianya*, *fotokopi*, *transkrip*, *ijazah*, *pasfoto*, serta `CV`/`UD`/`PD` tanpa titik (`RSN-001`, `SLM-001`, `SLM-002`; Modul SMA XI–XII Kemendikbud 2020).
