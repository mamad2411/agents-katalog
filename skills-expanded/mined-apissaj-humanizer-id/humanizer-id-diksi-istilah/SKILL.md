---
name: humanizer-id-diksi-istilah
description: Use when fixing diksi, pleonasme, dan padanan istilah.
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

# Humanizer ID — Diksi Istilah

Sub-kaidah Humanizer ID. Muat berkas ini setelah `humanizer-id` (induk) menentukan mode kerja. Aturan integritas ilmiah pada induk tetap mengikat penuh.

---

### K. Kalke AI Slop Khas Indonesia (Rujukan: Ivan Lanin *Xenoglosofilia*, 2018 & *Recehan Bahasa*, 2020; studi Kobak dkk., *Science Advances* 2025)

1. **Pola:** *hiruk pikuk* (kalke "hustle and bustle") → **Perbaikan:** *dinamika, aktivitas padat, keramaian* — **Sebab:** kalke terjemahan klise keluaran LLM yang dikenali penutur asli sebagai "bau ChatGPT"; bersihkan bila naskahnya formal.
2. **Pola:** *menyelami* (kalke "delving into", rasio 28x dalam publikasi medis global) → **Perbaikan:** *menguraikan, menganalisis, meneliti* — **Sebab:** padanan alami penutur asli, bukan kalk Inggris.
3. **Pola:** *merajut* (kalke "weaving / tapestry") → **Perbaikan:** *membangun, mengintegrasikan, menyusun* — **Sebab:** metafora jahit-menjahit khas AI slop; ganti verba tindakan lugas.
4. **Pola:** *lanskap* (kalke "landscape") → **Perbaikan:** *kondisi, peta, situasi, bidang* — **Sebab:** kalk "landscape" mubazir dalam naskah formal.

Konteks buku Lanin (2018, 2020): padanan baku tidak berarti kaku — pilih padanan yang dipakai penutur asli, jangan terjebak mengganti istilah asing dengan padanan yang justru lebih asing (kasus *umpan tekak*, *takarir*).

Catatan penelitian (Kobak dkk., 2025): Studi 15,1 juta abstrak PubMed membuktikan kata AI paling berlebihan antara lain *delves* (28x lebih sering), *underscores* (13,8x), *showcasing* (10,7x). Di teks Indonesia, kata-kata tersebut lazim mengalami kalke menjadi pola di atas.

---

### V. Pedoman Umum Pembentukan Istilah / PUPI (Rujukan Pusat Bahasa 2005 — Keputusan Mendiknas No. 146/U/2004)

1. **Pola:** istilah menyimpang makna, boros suku kata, konotasi buruk, atau melanggar kaidah → **Perbaikan:** pilih istilah paling tepat mengungkap konsep, paling singkat di antara sinonim, bernilai rasa dan eufonik, seturut kaidah bahasa Indonesia — **Sebab:** lima persyaratan istilah yang baik menurut PUPI.
2. **Pola:** *supermarket / merger / factoring / catering / invention / design / science / photocopy* mentah dalam teks Indonesia → **Perbaikan:** *pasar swalayan / gabung usaha* (penerjemahan); *anjak piutang / jasa boga / rekacipta* (perekaan); *desain / sains / fotokopi* (penyerapan dengan penyesuaian ejaan) — **Sebab:** tiga jalur resmi pemadanan istilah asing.
3. **Pola:** *alumni, master of ceremonies, charge d'affaires* (jamak asing) → **Perbaikan:** *lulusan, pengatur acara, kuasa usaha* — **Sebab:** pemarkah jamak asing ditanggalkan: diterjemahkan menjadi tunggal Indonesia.
4. **Pola:** polaritas terbalik (*inorganic → organik; illiterate → literat*) → **Perbaikan:** *takorganik, niraksara* — **Sebab:** keselarasan polaritas penerjemahan: positif → positif, negatif → negatif (*bound form → bentuk terikat*).
5. **Pola:** *in vitro* dicetak tegak / *internet* dicetak miring → **Perbaikan:** *in vitro, status quo, divide et impera* dicetak **miring**; *internet, golf, orbit* dicetak **tegak** — **Sebab:** istilah Latin/asing ilmiah belum terserap dicetak miring; yang telah menjadi kosakata umum dicetak tegak.

---

### AB. Pleonasme & Pilihan Kata (Rujukan Mustakim, *Bentuk dan Pilihan Kata*, Seri Penyuluhan Badan Bahasa, 2014)

1. **Pola:** *agar supaya / demi untuk / lalu kemudian / kalau seandainya / seperti misalnya* → **Perbaikan:** *agar / demi / kemudian / seandainya / misalnya* — **Sebab:** pleonasme pasangan sinonim: dua kata bersinonim berpasangan membuat salah satunya mubazir (hlm. 60-61).
2. **Pola:** *misalnya A, B, dan lain-lain* → **Perbaikan:** buang penutup tak terbatas atau buang pemerinci — **Sebab:** kontradiksi pembatas + penutup: perincian ber-*misalnya/seperti/contohnya/antara lain* dilarang ditutup *dan lain-lain/dan sebagainya/dan seterusnya* (hlm. 62).
3. **Pola:** *saling tolong-menolong / saling tembak-menembak / saling bersalaman* → **Perbaikan:** *saling menolong* atau *tolong-menolong* — **Sebab:** resiprokal ganda: *saling* dan ulang ber-...-an sama-sama menyatakan tindakan berbalasan (hlm. 67-69).
4. **Pola:** *dll., dsb., dst.* dipakai mana suka → **Perbaikan:** *dan sebagainya* (rincian sejenis), *dan lain-lain* (rincian beraneka jenis), *dan seterusnya* (urutan berjenjang) — **Sebab:** ketiganya berfungsi beda (hlm. 63).
5. **Pola:** *sesuai, berkaitan, sehubungan, bergantung* tanpa preposisi lanjutan → **Perbaikan:** *sesuai dengan, berkaitan dengan, sehubungan dengan, bergantung pada, terdiri atas* — **Sebab:** ungkapan idiomatis berpreposisi utuh: preposisi kedua dilarang dihilangkan (hlm. 78).
6. **Pola:** *terbuat daripada kayu / tujuan daripada penelitian ini* → **Perbaikan:** *terbuat dari kayu / tujuan penelitian ini* — **Sebab:** *daripada* khusus perbandingan (*lebih tinggi daripada*); makna asal/sumber memakai *dari*; frasa kepemilikan semu dihapus (hlm. 70, 74-75).

---

### AC. Peristilahan & Ejaan Serapan (Rujukan Adiwimarta dkk., *Tata Istilah Indonesia*, Pusat Bahasa, 1978)

1. **Pola:** *dominant, tolerant, relevant, optimist, manifest* → **Perbaikan:** *dominan, toleran, relevan, optimis, manifes* — **Sebab:** ejaan fonemik serapan: konsonan akhir yang tidak berfungsi digugurkan (hlm. 51-52).
2. **Pola:** *zat lemas, zat air, zat asam, ilmu pasti, ilmu pisah, saran diri* → **Perbaikan:** *nitrogen, hidrogen, oksigen, matematika, kimia, autosugesti* — **Sebab:** istilah klasik dijauhkan: ganti istilah kimia modern (hlm. 49).
3. **Pola:** *non-* dipakai seragam → **Perbaikan:** *tak-* terangkai untuk 'tidak' (*taklinear*); kata lepas *bukan* untuk 'bukan' (*bukan logam*); *nir-* untuk 'tanpa/bebas' (*nirgerak, nirlaba*) — **Sebab:** awalan non- menurut makna (hlm. 56-57).
4. **Pola:** *foki, laboratoria* → **Perbaikan:** *fokus, laboratorium* — **Sebab:** jamak Latin tidak dihidupkan; pakai bentuk lazim Indonesia (hlm. 38).
5. **Pola:** *geologiwan, kosmologiwan* → **Perbaikan:** *ahli geologi, ahli kosmologi* — **Sebab:** akhiran *-wan* hanya untuk akar berakhir /-a/ (*matematikawan, fisikawan*) (hlm. 55).

---

### AD. Paradigma Imbuhan Peristilahan (Rujukan Qodratillah, *Tata Istilah: Seri Penyuluhan Bahasa Indonesia*, Badan Bahasa, 2019)

1. **Pola:** *pemukiman padat/kumuh* → **Perbaikan:** *permukiman padat/kumuh* — **Sebab:** *pemukiman* = proses memukimkan; kawasan tempat tinggal selalu *permukiman* (hlm. 46-48).
2. **Pola:** *pengubahan iklim* → **Perbaikan:** *perubahan iklim* — **Sebab:** *perubahan* = keadaan berubah (paradigma *berubah*); *pengubahan* = tindakan mengubah (paradigma *mengubah*) (hlm. 48-51).
3. **Pola:** *sinergitas, standarisasi, efektifitas, aktifitas* → **Perbaikan:** *sinergi, standardisasi, efektivitas, aktivitas* — **Sebab:** metanalisis palsu: *-itas* hanya pada akar *-ity*, *-isasi* hanya pada akar *-ization* (hlm. 42, 55-56).
4. **Pola:** *ibukota, kerjasama, batubara, anakperusahaan* → **Perbaikan:** *ibu kota, kerja sama, batu bara, anak perusahaan* — **Sebab:** gabungan bentuk bebas ditulis terpisah (hlm. 23, 36).
5. **Pola:** *penterjemah, pengrajin, pensurvei, pembom* → **Perbaikan:** *penerjemah, perajin, penyurvei, pengebom* — **Sebab:** peluluhan peN- baku (hlm. 23).
6. **Pola:** *materiil, moriil, prinsipiil, potensiil* → **Perbaikan:** *materiel, morel, prinsipiel, potensiel* — **Sebab:** serapan Belanda *-eel* menjadi *-el* murni (TIQ-006) (hlm. 14, 17).
7. **Pola:** *pasar beruang / pasar banteng* (untuk bear/bull market) → **Perbaikan:** *pasar lesu/pasar turun / pasar bergairah/pasar naik* — **Sebab:** kalk terjemahan istilah finansial tidak boleh harfiah (TIQ-007) (hlm. 20).
8. **Pola:** *depstor* (untuk department store) → **Perbaikan:** *toko serbaada / toserba* — **Sebab:** padanan toko serbaada resmi (TIQ-008) (hlm. 20).
9. **Pola:** *ke swalayan* → **Perbaikan:** *ke pasar swalayan* — **Sebab:** kalk parsial swalayan: *swalayan* bermakna 'melayani diri sendiri'; sebutan tempat perlu kata yang diterangkan (TIQ-009) (hlm. 20).

---

### AF. Padanan Istilah Linguistik (Rujukan Kridalaksana, *Daftar Istilah Linguistik Asing-Indonesia*, Pusat Bahasa, 1978)

1. **Pola:** *proses pinjaman* → **Perbaikan:** *proses peminjaman* — **Sebab:** proses vs hasil: *peminjaman/pemisahan* = proses; *pinjaman/pisahan* = hasil (hlm. xiv).
2. **Pola:** *linguistic atlas* diterjemahkan *atlas linguistik* → **Perbaikan:** *atlas bahasa*; *linguistic skill → keterampilan bahasa* — **Sebab:** harfiah kaku ditolak (hlm. xiii).
3. **Pola:** *nominatif predikat / terjemah pinjam* → **Perbaikan:** *predikat nominal / pinjam terjemah* — **Sebab:** urutan padanan: unsur kepala di depan (hlm. xiii).
4. **Pola:** *sentum, senematika, apokop* → **Perbaikan:** *kentum, kenematika, apokope* — **Sebab:** alih fonem klasik: /k/ Latin dipertahankan (hlm. xiii).

---

### AI. Diksi Preskriptif Lanjutan (Rujukan Mustakim, *Bentuk dan Pilihan Kata*, Badan Bahasa, 2019)

1. **Pola:** *pada jam 09.00 / jam 14.30* (titik waktu acara) → **Perbaikan:** *pada pukul 09.00, pukul 14.30* — **Sebab:** *jam* khusus durasi (*dua jam perjalanan*) atau alat (*jam tangan*) (hlm. 78).
2. **Pola:** *Algoritma genetika yaitu metode...* → **Perbaikan:** *Algoritma genetika adalah metode...* — **Sebab:** kopula definisi memakai *adalah/ialah*, bukan *yaitu/yakni* (hlm. 81).
3. **Pola:** *mantan kantor pos / bekas rektor* → **Perbaikan:** *bekas kantor pos / mantan rektor* — **Sebab:** *mantan* untuk pemangku jabatan manusia; *bekas* untuk benda/kondisi nonmanusia (konotasi peyoratif bila untuk orang) (hlm. 77).
4. **Pola:** *Ada dua faktor, antara lain A dan B* → **Perbaikan:** *Ada dua faktor, yaitu A dan B* — **Sebab:** pemerinci tuntas (*yaitu/yakni*) untuk seluruh anggota yang sudah dibilang pasti; *antara lain/misalnya* khusus sebagian dari jumlah banyak (hlm. 81-82).
5. **Pola:** *kwalitas, kwantitas, kwitansi, jadual* → **Perbaikan:** *kualitas, kuantitas, kuitansi, jadwal* — **Sebab:** gugus konsonan kw- diserap ku- (BPK-015) (hlm. 68).
6. **Pola:** *prosen, prosentase, presentase, kuisioner, questioner* → **Perbaikan:** *persen, persentase, kuesioner* — **Sebab:** kalk Belanda prosen & kuisioner (BPK-016) (hlm. 68).
7. **Pola:** *sistim, metoda, methode, hipotesa, diagnosa* → **Perbaikan:** *sistem, metode, hipotesis, diagnosis* — **Sebab:** serapan Yunani vokal tertutup: akhiran -is/-os (BPK-017) (hlm. 68).
8. **Pola:** *obyek, subyek* → **Perbaikan:** *objek, subjek* — **Sebab:** konsonan /j/ baku objek-subjek (BPK-018) (hlm. 68).
9. **Pola:** *dirubah, dirobah, merobah, perobahan* → **Perbaikan:** *diubah, mengubah, perubahan* — **Sebab:** kata dasar ubah; *robah* tak ada di kamus, *rubah* = binatang (BPK-019) (hlm. 5-6).
10. **Pola:** *penglepasan, pengrusakan, pengrajin* → **Perbaikan:** *pelepasan, perusakan, perajin* — **Sebab:** peN- pada dasar /l/, /r/ melebur jadi pe- (BPK-020) (hlm. 14).
11. **Pola:** *menyebar luaskan, menyalah gunakan, mengikut sertakan, melipat gandakan* → **Perbaikan:** *menyebarluaskan, menyalahgunakan, mengikutsertakan, melipatgandakan* — **Sebab:** konfiks ganda (awalan + akhiran sekaligus) serangkai (BPK-021) (hlm. 33-34).
12. **Pola:** *mengadudomba, bertandatangan, bertepuktangan* → **Perbaikan:** *mengadu domba, bertanda tangan, bertepuk tangan* — **Sebab:** prefiks tunggal (awalan saja) terpisah (BPK-022) (hlm. 34).
13. **Pola:** *perkembangan sistem oleh peneliti* (kalimat beragen) → **Perbaikan:** *pengembangan sistem oleh peneliti* — **Sebab:** pertalian peng-an/per-an: *pengembangan* transitif berpelaku; *perkembangan* mandiri (BPK-023) (hlm. 22).
14. **Pola:** *kebijaksanaan moneter / kebijakan orang tua* → **Perbaikan:** *kebijakan moneter / kebijaksanaan orang tua* — **Sebab:** kebijakan = strategi institusional; kebijaksanaan = kearifan personal (BPK-024) (hlm. 76).
15. **Pola:** *biaya daripada, pangkal daripada, bagian daripada, hakikat daripada* → **Perbaikan:** *biaya, pangkal, bagian, hakikat* (hapus *daripada*) — **Sebab:** daripada non-komparatif perluasan ditolak; hanya sah untuk perbandingan derajat (BPK-025) (hlm. 79-80).
16. **Pola:** *pesepak bola amatir / pegolf penyuka* → **Perbaikan:** *pemain sepak bola, pemain golf* (amatir); *pesepak bola, pegolf, petenis* khusus profesi — **Sebab:** analogi profesi pe- vs pemain amatir (BPK-026) (hlm. 20-21) [telaah].
17. **Pola:** *produktifitas, kreatifitas, efektifitas* → **Perbaikan:** *produktivitas, kreativitas, efektivitas* — **Sebab:** sufiks serapan -itas (akar *-ity*) (BPK-027) (hlm. 68).
18. **Pola:** *Pebruari, Nopember* → **Perbaikan:** *Februari, November* — **Sebab:** nama bulan Masehi baku (BPK-028) (hlm. 68).
19. **Pola:** *Jum'at, Rabo, Rebo* → **Perbaikan:** *Jumat, Rabu* — **Sebab:** nama hari baku: Jumat tanpa apostrof (BPK-029) (hlm. 68).
20. **Pola:** *tehnik, technik* → **Perbaikan:** *teknik* — **Sebab:** penyerapan teknik baku (BPK-030) (hlm. 68).
21. **Pola:** *photo, photo copi, foto copy* → **Perbaikan:** *foto, fotokopi* — **Sebab:** grafem ph- diserap f (BPK-031) (hlm. 68).

---

### AO. Peristilahan Asesmen & Kurikulum Nasional (Rujukan Panduan Pembelajaran dan Asesmen Pendidikan Anak Usia Dini, Pendidikan Dasar, dan Menengah, BSKAP Kemendikbudristek RI, 2022)

1. **Pola:** campuran istilah kurikulum lintas generasi dalam satu dokumen (*KI/KD* di samping *CP/TP*, *RPP* di samping *Modul Ajar*) → **Perbaikan:** ganti konsisten ke istilah Kurikulum Merdeka: *Kompetensi Inti/Dasar (KI/KD) → Capaian/Tujuan Pembelajaran (CP/TP)*, *Silabus → Alur Tujuan Pembelajaran (ATP)*, *RPP → Modul Ajar (MA)*, *KKM angka tunggal → KKTP* — **Sebab:** keajegan istilah kurikulum dilarang mencampur lintas generasi (BSK-001) (hlm. 11-22).
2. **Pola:** *CP, TP, ATP, KKTP, P5* dipakai tanpa perkenalan → **Perbaikan:** tulis bentuk panjang pada kemunculan pertama sebelum dipakai sebagai akronim mandiri — **Sebab:** pengenalan singkatan resmi (BSK-002).
3. **Pola:** nilai rapor hanya angka agregat tunggal → **Perbaikan:** sertakan narasi deskripsi capaian kompetensi riil (capaian tertinggi dan area bimbingan) — **Sebab:** deskripsi ketercapaian kompetensi wajib bereviden (hlm. 48-52).
4. **Pola:** nilai asesmen formatif dihitung langsung ke akumulasi nilai akhir rapor → **Perbaikan:** gunakan sebagai instrumen perbaikan pembelajaran (*assessment for/as learning*) — **Sebab:** fungsi asesmen formatif, bukan sumatif (hlm. 26-28).

---

### AR. Stilistika Klasik dan Pemurnian Salah Kaprah (Rujukan Gorys Keraf "Diksi dan Gaya Bahasa" 1981; J.S. Badudu "Inilah Bahasa Indonesia yang Benar" 1983; "Bahasa!" Majalah Tempo 2008)

1. **Pola:** *mengenyampingkan / mempersering* → **Perbaikan:** *mengesampingkan / memperkerap (meningkatkan frekuensi)* — **Sebab:** kontaminasi bentuk leksikal: peleburan dua bentuk sah ditolak (KRF-001) (Keraf, Bab Morfologi dan Pilihan Kata).
2. **Pola:** *melakukan upaya peningkatan mutu* → **Perbaikan:** *meningkatkan mutu* — **Sebab:** penumpukan nomina abstrak: rantai nominalisasi kabur diganti verba tindakan langsung; kalimat ilmiah menuntut pelaku dan tindakan terlihat (KRF-002) (Keraf).
3. **Pola:** deretan kalimat berpola S-P identik tanpa variasi → **Perbaikan:** padukan kalimat berkala, inversi keterangan, fusi majemuk — **Sebab:** monotoni ritme sintaksis menghasilkan tempo baca jenuh (KRF-003) (Keraf, Bab Gaya Bahasa) [telaah].
4. **Pola:** *disebabkan karena / disebabkan oleh karena* → **Perbaikan:** *disebabkan oleh [nomina]* atau *terjadi karena [klausa]* — **Sebab:** pleonasme sebab-akibat (BDD-001) (Badudu, Jilid I).
5. **Pola:** *tujuan daripada, hasil daripada, dampak daripada* → **Perbaikan:** *tujuan, hasil, dampak* (gugurkan *daripada*); *daripada* hanya untuk perbandingan (*lebih tinggi daripada*) — **Sebab:** kalk Belanda *van*; daripada non-komparatif (BDD-002) (Badudu).
6. **Pola:** kalimat seluruhnya anak kalimat (*Walaupun...*) tanpa klausa induk → **Perbaikan:** lengkapi induk kalimat — **Sebab:** kalimat buntung tanpa induk (BDD-003) (Badudu) [telaah].
7. **Pola:** *menyolok, menyuci, menyubit, menyulik* → **Perbaikan:** *mencolok, mencuci, mencubit, menculik* — **Sebab:** morfofonemik /c/ tak luluh saat diimbuhi meN- (BDD-004) (Badudu, Jilid I).
8. **Pola:** *tolak ukur / tolak-ukur* → **Perbaikan:** *tolok ukur* — **Sebab:** kata dasarnya *tolok* (standar, tara, imbangan), bukan *tolak* (dorong); salah kaprah leksikal (BDD-005) (Badudu, Jilid II).
9. **Pola:** *mensukseskan, mensuplai, mensurvei* → **Perbaikan:** *menyukseskan, menyuplai, menyurvei* — **Sebab:** peluluhan /s/ serapan meN- menjadi ny- (BDD-006) (Badudu, Jilid I & III).
10. **Pola:** *laboratorium di mana sampel diuji* → **Perbaikan:** *laboratorium tempat sampel diuji* — **Sebab:** kalk relatif lokatif: *di mana* hanya kata tanya; penghubung relatif tempat memakai *tempat* (BDD-007) (Badudu, Jilid IV).
11. **Pola:** *Sehubungan dengan hal tersebut di atas maka... / Dengan ini diberitahukan bahwa... / Dalam rangka untuk dapat...* → **Perbaikan:** langsung ke pokok kalimat atau *Oleh karena itu* — **Sebab:** basa-basi penunda fakta birokratis dihapus (TMP-001) (Bahasa! Tempo, 2008).
12. **Pola:** *gedung yang mana didirikan tahun 1920* → **Perbaikan:** *gedung peninggalan tahun 1920* — **Sebab:** pereduksian klausa berpanjang-panjang: anak kalimat relatif mubazir dipangkas jadi pewatas nomina (TMP-002) (Tempo) [telaah].

---

### BA. Padanan Peristilahan Wacana Resmi (Rujukan "Daftar Istilah Linguistik Asing-Indonesia", Harimurti Kridalaksana, Pusat Bahasa 1978, hlm. xiii-xiv & lema kohesi/koherensi/presupposition/back-reference/deep structure)

1. **Pola:** *koherensitas / kohesifitas* → **Perbaikan:** *koherensi (pertalian) / kohesi (keutuhan)* — **Sebab:** padanan resmi coherence/cohesion; penyerapan akhiran mentah tidak baku (DIL-005).
2. **Pola:** *presuposisi* → **Perbaikan:** *praanggapan* — **Sebab:** padanan resmi presupposition; transkripsi mentah tidak dianjurkan dalam kajian wacana formal (DIL-006).
3. **Pola:** *referensi belakang* → **Perbaikan:** *rujuk balik* / *anafora* — **Sebab:** padanan resmi back-reference; bentuk harfiah tidak baku (DIL-007).
4. **Pola:** *deep structure / surface structure* dibiarkan mentah atau diterjemahkan harfiah → **Perbaikan:** *struktur batin / struktur lahir* — **Sebab:** padanan resmi [telaah kontekstual naskah linguistik] (DIL-008).

---

### BC. Pilihan Kata dan Konsep Kejamakan (Rujukan "Seri Penyuluhan: Bentuk dan Pilihan Kata", Badan Pengembangan dan Pembinaan Bahasa, Bab II hlm. 21-29 & Bab III hlm. 85-99)

1. **Pola:** *ketabrak, ketimpa, keterguling, kejatuhan* → **Perbaikan:** *tertabrak, tertimpa, terguling, terjatuh* — **Sebab:** awalan ke- adversatif salah kaprah; bentukan baku memakai ter- (BPK-011) (hlm. 21-29).
2. **Pola:** *menterapkan, penterapan* → **Perbaikan:** *menerapkan, penerapan* — **Sebab:** peluluhan fonem konfiks: /t/, /k/, /p/, /s/ awal dasar wajib luluh pada meng-...-kan dan peng-...-an (BPK-012).
3. **Pola:** *kita* menggantikan *saya* dalam ragam resmi (penulis tunggal) → **Perbaikan:** *saya / penulis / bentuk pasif* — **Sebab:** kejamakan inklusif [telaah]; *kami* hanya sah untuk penulis kelompok/lembaga (BPK-013, BPK-014) (hlm. 85-99).

---

### BH. Ragam Cakapan dalam Tulisan Formal (Rujukan Kamus Bahasa Indonesia BSE 2008, Pusat Bahasa)

1. **Pola:** *nggak, gimana, cuman, banget, capek* → **Perbaikan:** *tidak, bagaimana, hanya, sangat/amat, lelah/letih* — **Sebab:** kata berlabel cakapan (cak) dilarang masuk naskah formal (RGM-001).

---

### BL. Kehematan Kata & Diksi Karya Ilmiah Perguruan Tinggi (UIN Alauddin, Halimah 2014)

1. **Pola:** *tempat di mana mahasiswa berdiskusi* → **Perbaikan:** *tempat mahasiswa berdiskusi* — **Sebab:** relatif lokatif kalke 'place where/waar': frasa tanya *di mana* dilarang jadi penghubung relatif penjelas tempat (UIN-009) (hlm. 125).
2. **Pola:** *zaman dahulu kala* → **Perbaikan:** *zaman dahulu* atau *dahulu kala* — **Sebab:** pleonasme temporal rangkap tiga: *zaman, dahulu, kala* sama-sama menandai waktu lampau (UIN-010) (hlm. 125).

---

### CD. Diksi Resmi, Ungkapan Kenegaraan & Padanan Istilah (Winarti dkk. 2009 & BPBI 2)

1. **Pola:** *mengacuh pada, hidup-hidupan, membahas dan membicarakan, lain di samping itu, pada antara tahun* → **Perbaikan:** *mengacu pada, hidup-hidup, membahas (atau membicarakan), di samping itu, pada tahun (atau antara tahun)* — **Sebab:** *acuh* bermakna 'peduli' bukan 'merujuk'; akhiran *-an* pada *hidup-hidupan* keliru; *membahas dan membicarakan* sinonim ganda; *lain di samping itu* dan *pada antara tahun* menumpuk penghubung/preposisi mubazir (TMS-046) (Winarti dkk. 2009, hlm. 78–87).
2. **Pola:** *dirgahayu HUT RI ke-79, dirgahayu RI ke-79, HUT RI ke-79, BBWI* → **Perbaikan:** *Dirgahayu RI / Dirgahayu Republik Indonesia, HUT ke-79 RI, WIB* — **Sebab:** *dirgahayu* sudah bermakna 'berumur panjang' sehingga dilarang digabung dengan *HUT* atau *ke-N*; bilangan tingkat menerangkan *HUT*, bukan *RI*; singkatan wilayah waktu resmi ialah *WIB*, *Wita*, dan *WIT* (BPBI-008) (BPBI 2 Bahasa).
3. **Pola:** istilah Inggris bisnis/teknis dibiarkan mentah (*after-sales service, cash flow, overbooking, due diligence, site plan, master plan, standby loan, boarding pass, airworthy, vacuum cleaner*) → **Perbaikan:** *layanan pascajual, arus kas, tempah lajak, uji tuntas, rencana tapak, rencana induk, pinjaman siaga, pas naik, laik terbang, pengisap debu* — **Sebab:** padanan resmi Pusat Bahasa dalam `data/glosarium-lintas-bidang.json` (BPBI 2 Istilah).


---

### CG. Urutan Penyebutan Istilah & Padanan Leksikon Formal (Baharman, UNM; Yahya dkk. 2018; TBBBI Ed. 4)

1. **Pola:** *exposure (paparan risiko)* / *commuter line (kereta komuter)* → **Perbaikan:** *paparan risiko (exposure)* / *kereta komuter (commuter line)* — **Sebab:** `[telaah]` bila padanan Indonesia sudah tersedia, bentuk bahasa Indonesia wajib disebutkan lebih dulu baru diikuti istilah asing bercetak miring dalam tanda kurung (`TMS-048`) (Baharman, UNM, hlm. 9).
2. **Pola:** *tapi, udah, cuma* (di naskah ilmiah/berita) → **Perbaikan:** *tetapi, sudah, hanya* — **Sebab:** kata ragam lisan atau cakapan tidak baku dalam karangan formal wajib diganti bentuk bakunya (`JSK-010`) (Yahya dkk. 2018 hlm. 58, 63; TBBBI Ed. 4 2017, hlm. 523).
3. **Pola:** *gara-gara, mentang-mentang* (di laporan formal) → **Perbaikan:** *akibat, karena, disebabkan oleh* — **Sebab:** penanda sebab ragam lisan tidak baku tidak layak dipakai di tulisan ilmiah atau dinas (`TBB-035`) (TBBBI Ed. 4 2017, hlm. ~437).
4. **Padanan media/ekonomi/TI tambahan (`glosarium-lintas-bidang.json` 150 → 160):** *commuter line* → **kereta komuter**; *busway* → **jalur bus**; *reshuffle* → **perombakan**; *selfie* → **swafoto**; *rising star* → **bintang baru**; *community relation* → **hubungan masyarakat**; *year to date* → **sejauh tahun ini**; *month to month* → **bulan ke bulan**; *online* → **daring / dalam jaringan**; *email* → **pos-el / surat elektronik (surel)**.

---

### CJ. Ragam Cakap `pastinya` & Padanan Jurnalistik/Riset (DiSastra 2021; BRIN 2022; DE_JOURNAL 2023)

1. **Pola:** *pastinya* (di karangan ilmiah/laporan resmi) → **Perbaikan:** *tentu, niscaya*, atau hapus bila penguat mubazir — **Sebab:** ragam cakapan merusak objektif register ilmiah (`JSK-016`) (Uswati & Mardikantoro, *DiSastra* 2021, hlm. 66).
2. **Padanan tambahan (`glosarium-lintas-bidang.json` 160 → 164):** *public figure* → **figur publik / tokoh masyarakat**; *storyteller* → **pencerita / penutur cerita**; *library research* → **penelitian kepustakaan / kajian pustaka**; *hard copy* → **salinan cetak / naskah cetak**.

---

### CM. Padanan Istilah TI Mutakhir (Zaim, UNP 2018, hlm. 2)

- **Padanan tambahan (`glosarium-lintas-bidang.json` 164 → 168):** *download* → **unduh**; *upload* → **unggah**; *offline* → **luring / luar jaringan**; *mouse* → **tetikus** (`teknologi_dan_rekayasa`).

---

### CO. Padanan Sektor Usaha & Perhotelan (Semiloka 2019, hlm. 271–272)

- **Padanan tambahan (`glosarium-lintas-bidang.json` 168 → 170):** *cottage* → **pondok**; *food and beverage* → **makanan dan minuman** (`bisnis_dan_manajemen`).

---

### CR. Padanan Linguistik Baku (Kridalaksana, *Daftar Istilah Linguistik*, 1979)

- **Padanan tambahan (`glosarium-lintas-bidang.json` 170 → 178):** *discourse* → **wacana**; *deep structure* → **struktur batin**; *surface structure* → **struktur lahir**; *paraphrase* → **parafrase**; *ambiguity* → **ketaksaan / ambiguitas**; *redundancy* → **kelimpahan / kelewahan**; *colloquialism* → **ragam tak resmi**; *metalanguage* → **metabahasa** (`linguistik_dan_ilmu_bahasa`).

---

### CU. Padanan Konten Digital & Wacana MABBIM/Kridalaksana (Siklus 35–36)

- **Padanan tambahan (`glosarium-lintas-bidang.json` 178 → 180):** *content creator* → **pencipta konten / kreator konten** (*Buletin MABBIM* Vol. 15, 2024, hlm. 19; `jurnalistik_dan_media`); *tautology* → **tautologi** (Kridalaksana 1979, hlm. 40; `linguistik_dan_ilmu_bahasa`).
