---
name: humanizer-id-wacana-retorika
description: Use when fixing kohesi paragraf & retorika naskah.
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

# Humanizer ID — Wacana Retorika

Sub-kaidah Humanizer ID. Muat berkas ini setelah `humanizer-id` (induk) menentukan mode kerja. Aturan integritas ilmiah pada induk tetap mengikat penuh.

---

### A. Eliminasi Monotoni Pembuka Antar-Paragraf (*Connector Addiction*)

1. **Pola:** *Selain itu, ...* / *Lebih lanjut, ...* / *Oleh karena itu, ...* / *Di sisi lain, ...* (kata penghubung mekanis di kata pertama setiap awal paragraf) → **Perbaikan:** maksimal satu konjungsi transisi di awal paragraf per halaman teks; buka paragraf baru dengan subjek tematis langsung, frasa nomina fokus, atau kalimat simpulan data terdahulu — **Sebab:** AI memiliki kecenderungan adiktif menaruh kata penghubung mekanis di awal tiap paragraf (*connector addiction*).

---

### B. Eliminasi Transisi Kopong & Ilusi Keterhubungan (*Illusory Cohesion*)

1. **Pola:** *Dengan demikian, hal ini membuktikan bahwa...* / *Konsekuensinya, algoritma ini...* (kata sambung kausalitas padahal kalimat sebelumnya belum memuat premis) → **Perbaikan:** evaluasi apakah kalimat sebelumnya benar-benar memuat premis pembukti; bila bukti belum memadai, hapus transisi kausalitas tiruan dan tampilkan relasi sebagai hubungan koordinatif wajar — **Sebab:** ilusi keterhubungan (*illusory cohesion*): kata sambung kausalitas tanpa data premis yang cukup menyesatkan pembaca.

---

### C. Penertiban Sudut Pandang Aktor (*Agent Drift Consistency*)

1. **Pola:** *Sistem dirancang oleh kami, lalu pengujian dilakukan oleh peneliti, dan laporan disusun oleh penulis* (pelaku tindakan bercampur baur dalam satu bab) → **Perbaikan:** *Sistem dirancang..., pengujian dilakukan..., dan laporan disusun...* (pasif objektif murni) atau konsisten menggunakan sebutan *peneliti* — **Sebab:** pergeseran sudut pandang aktor (*agent drift*) merusak konsistensi pelaku tindakan dalam satu bab.

---

### D. Perajutan Sitasi Ilmiah Alami (*Citation Weaving*)

1. **Pola:** *Menurut Pratama (2021)... Senada dengan itu, Wijaya (2022) menyatakan...* (kutipan nama berulang di awal kalimat) → **Perbaikan:** *Peningkatan akurasi arsitektur berbasis atensi terbukti konsisten pada dataset teks informal (Pratama, 2021; Wijaya, 2022)* — fokuskan kalimat pada sintesis temuan, bukan nama peneliti; tempatkan nama dan tahun di kurung penutup; gabungkan rujukan yang memiliki kesimpulan seirama dalam satu kurung — **Sebab:** kalimat harus menyintesis temuan, bukan mendaftar nama peneliti.

---

### E. Kalibrasi Derajat Kepastian Epistemik (*Epistemic Hedging*)

1. **Pola:** verba kepastian tidak dikalibrasi dengan jenis klaim (verba teruji untuk dugaan; penanda probabilitas untuk fakta empiris) → **Perbaikan:** fakta empiris — *menunjukkan, menghasilkan, membuktikan, mencatatkan*; inferensi & korelasi — *mengindikasikan, berkorelasi dengan, mencerminkan*; hipotesis / prakiraan — penanda probabilitas tunggal *diduga, diproyeksikan, berpotensi* — **Sebab:** kalibrasi derajat kepastian epistemik menuntut verba selaras dengan tingkat kepastian klaim.
2. **Pola:** *data ini mungkin berpotensi dapat diindikasikan bahwa...* → **Perbaikan:** *data ini mengindikasikan bahwa...* — **Sebab:** larangan tumpukan *hedging*: dilarang menumpuk modalitas ganda dalam satu klausa.

---

### F. Rujukan Tabel, Gambar, Persamaan Matematis, & Tipografi Teknis

1. **Pola:** *tabel di bawah ini* / *grafik di atas* → **Perbaikan:** *Tabel 4.2* / *Gambar 3.1* (penunjuk bernomor ilmiah; jangan merekayasa nomor bila belum tersedia) — **Sebab:** hindari penunjuk spasial semu; rujukan tabel & gambar wajib bernomor karena tata letak dapat bergeser.
2. **Pola:** *rumus di atas* / *persamaan berikut* → **Perbaikan:** *Berdasarkan Persamaan (3.1)...* / *...sebagaimana dirumuskan pada Persamaan (2.4)* — **Sebab:** rujukan persamaan matematis informal diganti format baku bernomor (Pedoman Skripsi UGM & UI).
3. **Pola:** perintah terminal, nama berkas, nama fungsi, blok kode, istilah asing, dan istilah berpadanan baku tanpa pembedaan tipografi → **Perbaikan:** `monospace` untuk perintah terminal (`npm run dev`), nama berkas (`config.json`), nama fungsi (`calculateStreaks()`), blok kode; *italic* untuk istilah asing yang belum diserap resmi ke KBBI (*overfitting*, *zero-shot*, *loss function*); tegak untuk istilah berpadanan baku (*basis data*, *tembolok*, *antarmuka*) — **Sebab:** tipografi teknis menandai jenis token secara konsisten.

---

### O. Singkatan Latin Catatan Kaki & Sifat Ragam Ilmiah (Rujukan Buku Bahasa Indonesia IAIN Curup, 2021)

1. **Pola:** *op cit 45* / *loc cit* / *ibidem halaman 23* → **Perbaikan:** *op. cit., hlm. 45* / *loc. cit., hlm. 12* / *ibid., hlm. 23* — **Sebab:** singkatan Latin wajib lengkap dengan titik dan dicetak miring; *ibid.* = karya sama dengan catatan sebelumnya, *op. cit.* = karya yang pernah dikutip (tidak berurutan), *loc. cit.* = halaman sama yang sudah dikutip.
2. **Pola:** ragam penulisan yang meninggalkan tujuh sifat ragam ilmiah (kalimat fragmentaris, bertolak dari penulis, tidak formal-objektif, tidak ringkas-padat, tidak konsisten) → **Perbaikan:** cendekia, lugas-jelas, anti-kalimat fragmentaris, bertolak dari gagasan (bukan penulis → didominasi kalimat pasif), formal-objektif, ringkas-padat, konsisten (istilah & tanda baca seragam sepanjang naskah) — **Sebab:** tujuh sifat tersebut menjadi tolok ukur ragam ilmiah yang sah.
3. **Pola:** nama pengarang ditulis seragam (dibalik) di footnote dan daftar pustaka; nomor halaman diletakkan di daftar pustaka → **Perbaikan:** di footnote urutan normal (nama diri → nama keluarga); di daftar pustaka dibalik (nama keluarga dulu); nomor halaman wajib di footnote, opsional di daftar pustaka — **Sebab:** konvensi nama pengarang dan nomor halaman berbeda antara catatan kaki dan daftar pustaka.

---

### P. Identitas Penulis Ilmiah & Singkatan Halaman (Rujukan Buku Siswa Kelas XI Kemendikbudristek, 2024)

1. **Pola:** *Dr. Ahmad Hidayat, M.Si.* → **Perbaikan:** *Ahmad Hidayat* — **Sebab:** nama penulis artikel ilmiah ditulis tanpa gelar akademik.
2. **Pola:** *Ahmad H* → **Perbaikan:** *Ahmad Hidayat* — **Sebab:** nama belakang dilarang disingkat karena menjadi kunci rujukan sitasi.
3. **Pola:** *hh. 55–67* → **Perbaikan:** *h. 55–67* — **Sebab:** singkatan halaman baku adalah `h.` untuk satu maupun banyak halaman; konvensi Indonesia tidak mengenal pluralisasi singkatan halaman.
4. **Pola:** ragam bahasa yang memuat subjektivitas, konotasi, atau makna ganda → **Perbaikan:** objektif (berbasis data/fakta), reproduktif (makna pembaca = maksud penulis), denotatif murni (bebas konotasi/metafora) — **Sebab:** tiga syarat ragam bahasa ilmiah.

---

### R. Kesatuan Ide Pokok & Pola Pengembangan Paragraf (Rujukan Buku Siswa Kelas XI Kemendikbudristek, 2024)

1. **Pola:** mencampur dua topik berbeda dalam satu paragraf tunggal (mis. membahas latensi model sekaligus membahas struktur dataset) → **Perbaikan:** pecah menjadi dua paragraf tersendiri; setiap paragraf memuat satu kalimat topik (ide pokok) yang dikawal kalimat-kalimat penjelas yang koheren — **Sebab:** satu paragraf wajib memuat satu ide pokok.
2. **Pola:** posisi kalimat topik diacak tanpa pola tetap sehingga pembaca kebingungan menangkap gagasan sentral → **Perbaikan:** deduksi (paling disukai ragam ilmiah) — kalimat pernyataan umum/tesis di awal paragraf, kemudian diuraikan bukti empiris, metrik, atau elaborasi di kalimat-kalimat berikutnya; induksi — sajikan rentetan data pengujian/fakta terperinci, lalu akhiri dengan penarikan simpulan umum pada kalimat pamungkas paragraf — **Sebab:** pola pengembangan paragraf harus konsisten; mencampuradukkan posisi kalimat topik secara acak dilarang.

---

### U. Sindrom Akronim Redundan (RAS) & Keserasian Kohesi Wacana (Rujukan TBBBI Moeliono dkk. 1988/1998 & Haslinda-Thaba 2018)

1. **Pola:** *nomor NIK* / *kartu KIP* / *kartu KTP* / *nomor PIN* / *virus HIV* / *partai PPP* / *partai PDIP* / *partai PAN* / *ATM card* → **Perbaikan:** *NIK* (N = Nomor) / *KIP* / *KTP* (K = Kartu) / *PIN* (N = Number) / *HIV* (V = Virus) / *PPP* / *PDI Perjuangan* / *PAN* (P = Partai) / *kartu ATM* (M = Machine; *card* redundan) — **Sebab:** unsur kepanjangan dalam akronim tidak boleh disebut ulang (larangan Sindrom RAS — Akronim Redundan).
2. **Pola:** *Ratna dan kawannya pergi karena ia harus mendaftar* (taksa: siapa yang mendaftar?) → **Perbaikan:** *Ratna dan kawannya pergi karena Ratna harus mendaftar* — **Sebab:** pronomina anaforis tunggal: pronomina (*ia, dia, mereka, -nya*) wajib punya anteseden tunggal.
3. **Pola:** *Jangankan membeli kursi, satu mebel pun kami tidak punya* → **Perbaikan:** *Jangankan membeli aneka mebel, satu kursi pun kami tidak punya* — **Sebab:** urutan hiponimi–hipernim: kata umum mencakup kata khusus, tidak boleh dibalik.
4. **Pola:** subjek identik diulang di setiap klausa dalam kalimat majemuk → **Perbaikan:** lesapkan subjek yang identik antarklausa (elipsis) — **Sebab:** pelesapan subjek yang sah; pengulangan subjek di setiap klausa melanggar asas ekonomi wacana (TBBBI, hlm. 330–333).

---

### AJ. Kepaduan & Keruntutan Paragraf (Rujukan Suladi, *Paragraf: Seri Penyuluhan Bahasa Indonesia*, Badan Bahasa, 2019)

1. **Pola:** konstruksi kataforis rancu — pronomina muncul sebelum maujud acuannya → **Perbaikan:** pronomina persona dan demonstratif (*itu, ini, ia, dia, -nya*) diletakkan setelah anteseden anaforis yang jelas — **Sebab:** arah referensi & koreferensi wajib anaforis; hindari konstruksi kataforis rancu (hlm. 33–34).
2. **Pola:** *Pertama, Kedua, Ketiga, Ketiga* / *Pertama, Kedua, Keempat* → **Perbaikan:** *Pertama, Kedua, Ketiga, Keempat* — **Sebab:** keruntutan ordinal: penanda perincian berurutan wajib runtut dan konsisten; pengulangan atau lompatan nomor merusak pernalaran paragraf (hlm. 55–56).
3. **Pola:** kalimat topik memuat bilangan pasti (*tiga faktor*) tetapi kalimat penjelas hanya mengembangkan dua faktor → **Perbaikan:** kembangkan ketiga faktor secara lengkap tanpa meninggalkan sisa — **Sebab:** ketuntasan klasifikasi: unsur yang dijanjikan kalimat topik wajib diuraikan seluruhnya (hlm. 55).

---

### AM. Kaidah Penyajian Data Visual & Struktur Observasi (Rujukan Modul Pembelajaran SMA: Teks Tanggapan Tabel-Grafik & Laporan Hasil Observasi, Indri Anatya Permatasari, M.Pd., Direktorat SMA Kemendikbud 2020)

1. **Pola:** *grafik di atas* / *tabel di bawah ini* / *bagan berikut* → **Perbaikan:** *Grafik 2* / *Tabel 4.1* — **Sebab:** rujukan visual bernomor (TBG-001): deiksis spasial relatif dilarang pada naskah ilmiah; rujukan bernomor eksplisit wajib karena tata letak halaman dapat bergeser saat cetak/responsif (KD 3.1, hlm. 12-14).
2. **Pola:** menyebut grafik batang sebagai *bagan batang* → **Perbaikan:** *grafik* untuk data numerik kuantitatif/fluktuasi deret waktu; *bagan* untuk hierarki/komponen struktural; *diagram* untuk prosedur/skema — **Sebab:** terminologi media visual (TBG-002): salah menyebut grafik, bagan, dan diagram adalah kerancuan terminologi (KD 3.1, hlm. 9-11).
3. **Pola:** *Sedangkan, ...* (membuka kalimat mandiri) → **Perbaikan:** *Sementara itu, ...* / *Di sisi lain, ...* atau gabung klausa dengan koma — **Sebab:** konjungsi pertentangan komparasi data (TBG-003): *sedangkan* adalah konjungsi intrakalimat, dilarang membuka kalimat mandiri (KD 3.1, hlm. 16-17; Alwi dkk. 2017).
4. **Pola:** *merupakan salah satu termasuk ...* → **Perbaikan:** pilih satu konstruksi definisi lugas (*merupakan ...* / *salah satu ...* / *termasuk ...*) — **Sebab:** definisi umum LHO (LHO-001): dilarang menumpuk kopula + partitif + verba inklusi (KD 3.1/4.1, hlm. 27).
5. **Pola:** *terbagi dari ...* / *terbagi dalam ...* → **Perbaikan:** *terbagi atas ...* / *dibagi menjadi ...* — **Sebab:** kolokasi taksonomi (LHO-002): *terbagi atas ...* bukan *terbagi dari/dalam* (KD 3.1/4.1, hlm. 24-25).
6. **Pola:** *dan lain sebagainya* → **Perbaikan:** *dan lain-lain* (rincian heterogen) atau *dan sebagainya* (rincian homogen) — **Sebab:** penutup perincian (LHO-003): kontaminasi *dan lain sebagainya* dilarang (KD 3.1/4.1, hlm. 28).

---

### AN. Ragam Opini Epistemik & Pencegahan Interferensi Tuturan Lisan (Rujukan Modul Pembelajaran SMA Artikel Opini KD 3.10, Direktorat SMA Kemendikbud 2020; Widyaparwa Vol. 48 No. 1, Balai Bahasa DIY 2020)

1. **Pola:** *bisa jadi* / *sepertinya* / *kayaknya* → **Perbaikan:** *diduga* / *berpotensi* / *diindikasikan* — **Sebab:** modalitas spekulatif lisan (OPN-002) dilarang di teks formal (KD 3.10, hlm. 12).
2. **Pola:** *eksperimen membuktikan X akan mengeliminasi seluruh Y* → **Perbaikan:** pisahkan klausa verifikasi empiris (*terbukti mereduksi 4,2%*) dari proyeksi masa depan (*diproyeksikan dalam penelitian lanjutan*) — **Sebab:** fakta vs proyeksi (OPN-003): klaim yang mencampur keduanya rancu epistemik [telaah] (KD 3.10, hlm. 12-14).
3. **Pola:** anjuran normatif *seharusnya ...* tanpa bukti → **Perbaikan:** sertakan klausa evidensial berbasis regulasi/parameter/bukti data — **Sebab:** opini berevidensial (OPN-004): opini tanpa bukti adalah opini subjektif mentah [telaah] (KD 3.10, hlm. 16-18).
4. **Pola:** *Menghitung indeks bias...* (kalimat diawali verba aktif transitif tanpa subjek) → **Perbaikan:** *Peneliti menghitung indeks bias...* atau pasif *indeks bias dihitung...* — **Sebab:** pelesapan agen (WDY-001): kalimat ilmiah dilarang diawali langsung verba aktif transitif tanpa subjek; 50% tuturan lisan mengalami *agent deletion* (penghapusan agen), ragam tulis tidak mentolerirnya (Kirana, hlm. 20-21, 25-26).
5. **Pola:** *Laporan ini bendahara telah menyelesaikannya* → **Perbaikan:** selaraskan agen-subjek (*Bendahara telah menyelesaikan laporan ini*) atau gunakan pasif baku (*Laporan ini telah diselesaikan bendahara*) — **Sebab:** hierarki topik (WDY-002): dilarang memajukan objek inanimat sebagai subjek semu lalu mengulang agen dengan pronomina [telaah] (Kirana, hlm. 20-21; Givon 1976; DeLancey 1981).
6. **Pola:** *Katanya...* / *hasilnya menunjukkan...* (tanpa anteseden eksplisit) → **Perbaikan:** *Menurut Hidayat dkk. (2019)...* / *hasil pengujian menunjukkan...* — **Sebab:** enklitik indefinit (WDY-003): *-nya* tanpa anteseden eksplisit ditolak (Kirana, hlm. 22-23).
7. **Pola:** *langkah berikutnya adalah memurnikan.* → **Perbaikan:** *langkah berikutnya adalah memurnikan filtrat hasil maserasi* — **Sebab:** transitivitas tuntas (WDY-004): verba transitif tidak boleh menggantung tanpa objek penderita [telaah] (Kirana, hlm. 24-26; Hopper & Thompson 1980).
8. **Pola:** *kurang mantap* / *cukup oke* / *nge-blend* → **Perbaikan:** *kurang memadai* / *efektif* / *terintegrasi* — **Sebab:** leksikon denotatif formal (WDY-005): slang eufemistis tuturan lisan dilarang di register ilmiah (Permita, hlm. 41-48).
9. **Pola:** *Pada saat melakukan pengambilan sampel darah di puskesmas menemukan...* → **Perbaikan:** *...di puskesmas, petugas medis menemukan...* — **Sebab:** struktur K-P-O (WDY-006): kalimat diawali keterangan temporal/spasial lalu langsung verba tanpa subjek adalah cacat; sisipkan koma lalu subjek eksplisit (Kirana, hlm. 21).

---

### AP. Sindrom Akronim Redundantan, Kohesi Teks, Konversi Monograf, dan Peristilahan Ruang Publik (Rujukan Haslinda & Thaba 2018; Maharani/UI; Istiqomah 2020; Putusan Kongres Bahasa Indonesia VII 1998; Glosarium Linguistik 2002)

1. **Pola:** *Persija Jakarta melawan PSM Makassar* → **Perbaikan:** *Persija melawan PSM* — **Sebab:** akronim-toponimi redundan (RAS-005): nama wilayah sudah terkandung dalam akronim (*Ja*karta pada Persija, *M*akassar pada PSM) (Haslinda & Thaba, hlm. 4-5).
2. **Pola:** *sistem SI* / *nomor ISBN/ISSN/NPWP* / *dosen DPA* / *kode QR code* / *monitor LCD display* / *mesin ATM machine* → **Perbaikan:** *SI* / *ISBN/ISSN/NPWP* / *DPA* / *QR code* / *LCD display* / *ATM machine* — gugurkan spesifikator duplikat — **Sebab:** akronim-spesifikator redundan (RAS-006..009): kata penjelas sudah termuat dalam akronim (Haslinda & Thaba, hlm. 3-6).
3. **Pola:** *Maka, ...* (membuka kalimat mandiri tanpa klausa syarat) → **Perbaikan:** *Oleh karena itu, ...* atau *Jika X, maka Y* — **Sebab:** konjungsi "maka" awal kalimat (KOH-003): *maka* adalah konjungsi konsekuensi intrakalimat, dilarang membuka kalimat mandiri (Maharani, hlm. 17).
4. **Pola:** *2.1.1.1* (penomoran desimal melebihi tiga tingkat) → **Perbaikan:** judul bermakna atau tiga tingkat penuh (*2.1.1*) — **Sebab:** penomoran subbab monograf (MBI-002) dilarang melebihi tiga tingkat (Istiqomah, hlm. 11).
5. **Pola:** judul *... di SMA Negeri 1 Batu Tahun Ajaran 2011/2012* → **Perbaikan:** judul bebas seting administratif; lokasi dan tahun penelitian cukup pada bagian metodologi — **Sebab:** judul bebas latar administratif (MBI-003): judul buku ilmiah dilarang memuat seting administratif (Istiqomah, hlm. 10, 13).
6. **Pola:** *penyesuaian tarif* / *mengamankan* / *dirumahkan* → **Perbaikan:** *kenaikan harga* / *menangkap/menahan* / *PHK* — nyatakan kenyataannya lugas — **Sebab:** eufemisme birokratis (KBI-001): penutupan fakta negatif dengan pembalut halus ditolak dalam ragam resmi (Putusan Kongres VII, hlm. 6, Bagian Khusus B.2).
7. **Pola:** *booking room* / *grand opening* / *meeting room* / *launching* → **Perbaikan:** *ruang pemesanan* / *pembukaan resmi* / *ruang rapat* / *peluncuran* — **Sebab:** istilah asing mentah ruang publik (KBI-002) digantikan padanannya di dokumen resmi (Putusan Kongres VII, hlm. 3, Bagian Khusus A.a.2).
8. **Pola:** *mengacuhkan* (untuk arti 'mengabaikan') / *absensi* (untuk arti 'kehadiran') / *tidak bergeming* (untuk arti 'diam total') → **Perbaikan:** *mengabaikan* / *kehadiran* / bentuk yang tepat sesuai makna — **Sebab:** katakresis paronim (GLS-002): *mengacuhkan* = tidak menggubris dengan sengaja, bukan *mengabaikan* = tidak memedulikan; *absensi* = daftar ketidakhadiran, bukan kehadiran; *tidak bergeming* bukan berarti diam total (Lapoliwa & Nureni, hlm. 51).
9. **Pola:** *sangat mutlak* / *kondisi prasyarat awal* / *saling tolong-menolong satu sama lain* → **Perbaikan:** *mutlak* / *prasyarat* / *saling tolong-menolong* — **Sebab:** tautologi kehematan (GLS-004): gugurkan kelewahan tautologis (Lapoliwa & Nureni, hlm. 50, 71).

---

### AP-Amandemen. Kolokasi Metaforis, Ragam Santai Naskah Resmi, dan Anonimisasi Subjek Penelitian

1. **Pola:** *melahirkan solusi* / *menghidangkan musik* / *mencanangkan pemecahan* → **Perbaikan:** *menghasilkan solusi* / *menyajikan musik* / *merumuskan pemecahan* — **Sebab:** kolokasi verba-nomina metaforis (GLS-003): *melahirkan* hanya untuk makhluk hidup, *menghidangkan* untuk sajian konsumsi, *mencanangkan* untuk program resmi (Lapoliwa & Nureni, hlm. 17).
2. **Pola:** *banget* / *bikin bingung* / *kok* / *sih* → **Perbaikan:** *sangat* / *membingungkan* / hapus partikel — **Sebab:** leksikon percakapan di naskah resmi (KBI-004): partikel dan verba ragam santai dilarang pada buku teks dan naskah dinas (Putusan Kongres VII, hlm. 5-6, Bagian Khusus A.f.2 & B.4) [aspek kontekstual dinilai manual: *telaah* untuk pemakaian figuratif].
3. **Pola:** data identitas responden mentah (*NIK, NIP, nomor KTP*) dalam naskah → **Perbaikan:** samarkan dengan inisial atau kode responden (*narasumber AD*) — **Sebab:** anonimisasi subjek penelitian (MBI-004): digit identitas pribadi mentah dalam naskah melanggar etika penelitian (Istiqomah, hlm. 5) [penilaian konteks naskah: *telaah* untuk kasus non-digit].
4. **Pola:** *tiga jenis mesin* (untuk *piston*, *busi* yang merupakan bagian mesin) → **Perbaikan:** *komponen/bagian* untuk relasi meronimi; *jenis* hanya untuk hiponimi — **Sebab:** rancu taksonomi meronimi-hiponimi (KOH-005): relasi "bagian dari" tidak boleh disebut "jenis" (Maharani, hlm. 8-9, 14) [*telaah*].
5. **Pola:** *aromanya* (menggantikan *aroma kopi*) → **Perbaikan:** ulangi nomina lengkap (*aroma kopi*) atau bentuk padanannya — **Sebab:** pulau anaforis (GLS-001): pronomina (*-nya, ini*) tidak boleh menggantikan nomina turunan utuh (Lapoliwa & Nureni, hlm. 14) [*telaah*].
6. **Pola:** ungkapan berkonotasi vulgar atau sensasional untuk memicu viralitas → **Perbaikan:** gaya lugas berbasis data — **Sebab:** leksikon sensasional naskah resmi (KBI-003) dilarang dalam publikasi dinas (Putusan Kongres VII, hlm. 6, Bagian Khusus B.8) [*telaah*].

---

### BI. Koherensi & Kesatuan Paragraf (Seri Penyuluhan Paragraf, Suladi 2015)

1. **Pola:** *Akhirnya ...* / *Akibatnya ...* / *Oleh karena itu ...* / *Maka dari itu ...* / *Dengan demikian ...* / *Berdasarkan uraian di atas ...* (tanpa koma) → **Perbaikan:** *Akhirnya,* / *Akibatnya,* / *Oleh karena itu,* / *Maka dari itu,* / *Dengan demikian,* / *Berdasarkan uraian di atas,* — **Sebab:** koma konjungsi penumpu simpulan (PRG-001): konjungsi antarkalimat wajib diikuti koma (Suladi, 2015, hlm. 55).
2. **Pola:** satu paragraf memuat lebih dari satu gagasan utama atau memuat kalimat yang menyimpang dari kalimat topik → **Perbaikan:** pisahkan topik baru ke paragraf terpisah; hapus kalimat sumbang — **Sebab:** kesatuan paragraf & kalimat sumbang (PRG-002): tiap paragraf hanya boleh memuat satu gagasan utama `[telaah]` (hlm. 13-14).

---

### BJ. Ragam Baku Bahasa Ilmiah Perguruan Tinggi (Kuntarto UNJA & Suyatno UIN Jakarta)

1. **Pola:** *kesimpulan dari penelitian* → **Perbaikan:** *kesimpulan penelitian* / *tujuan program* / *anak Pak Lurah* — **Sebab:** posesif kalke asing 'dari' (UIN-007): kepemilikan bahasa Indonesia dinyatakan langsung, bukan lewat *dari* yang merupakan kalke struktur asing *van/of* (UNJA hlm. 98).
2. **Pola:** *membelikan untuk adik baju* → **Perbaikan:** *membelikan adik baju* — **Sebab:** verba benefaktif akhiran *-kan* + 'untuk' (UIN-008): sufiks *-kan* sudah mengandung arti 'melakukan untuk orang lain'; *untuk* dilarang ditambahkan di depan penyerta (UNJA hlm. 108).

---

### BV. Kaidah Editorial Taktis Menyunting & Preskripsi Terbitan Ilmiah (Rujukan Bambang Trim Penerbit BRIN 2023 & Winarti dkk. Kantor Bahasa Kaltim 2005)

1. **Pola:** *acuh* (untuk arti cuek) / *bergeming* (untuk arti goyah) / *senonoh* (untuk arti asusila) / *tukasnya* (sebagai varian pewarta netral) → **Perbaikan:** *tidak acuh* / *tidak bergeming* / *tidak senonoh* / *ujarnya* atau *tegasnya* — **Sebab:** preservasi makna kata spesifik: *acuh* = peduli, *bergeming* = diam/kukuh/tidak bergerak, *senonoh* = patut/sopan, *tukas* = menuduh (Penerbit BRIN).
2. **Pola:** tertukarnya pasangan nomina relasional dan waktu: *langganan/pelanggan*, *jam/pukul*, *tiap-tiap/masing-masing*, *pemelajar/pembelajar*, *permukiman/pemukiman*, *persebaran/penyebaran* → **Perbaikan:** *langganan* (pihak penyedia/toko) vs *pelanggan* (konsumen pembeli); *jam* (rentang durasi, mis. *selama dua jam*) vs *pukul* (titik saat spesifik, mis. *pukul 14.00 WIB*); *tiap-tiap* (posisi awal anteseden nomina) vs *masing-masing* (distributif posisi akhir); *pemelajar* (orang yang belajar/siswa/mahasiswa) vs *pembelajar* (pengajar/instruktur yang membelajarkan); *permukiman* (kawasan tempat tinggal) vs *pemukiman* (proses memukimkan); *persebaran* (kondisi/peta tersebarnya objek) vs *penyebaran* (tindakan aktif menyebarkan) — **Sebab:** diferensiasi nomina relasional & waktu (Penerbit BRIN).
3. **Pola:** *sangat sempurna sekali* / *luar biasa sempurna* / *kurang lebih sekitar* / *semata-mata hanya* / *misteri rahasia* / *seperti ..., dan lain-lain* → **Perbaikan:** *sempurna* / *kurang lebih* atau *sekitar* / *semata-mata* atau *hanya* / *misteri* atau *rahasia* / pilih satu (partitif atau enumeratif terbuka) — **Sebab:** pembersihan pleonasme leksikal ekstrem & kontaminasi partitif: frasa pembuka *seperti/di antaranya/misalnya* dilarang diakhiri *dan lain-lain/dan sebagainya* (Penerbit BRIN).
4. **Pola:** *semua lahan-lahan* / *semua faktor-faktor* / *mulai Maret sampai Mei* / *diprioritas* / *menunjukkan bahwa pada persentase N sangat rendah* / *menyatakan, bahwa* / *menemukan, bahwa* → **Perbaikan:** *semua lahan* atau *lahan-lahan* / *dari Maret sampai Mei*, *sejak Maret hingga Mei*, atau *mulai Maret hingga Mei* / *diprioritaskan* (pasif *di-* dari *memprioritaskan*) / *menunjukkan bahwa persentase N sangat rendah* / *menyatakan bahwa* — **Sebab:** kaidah sintaksis & pembentukan kata ilmiah: pleonasme kuantor jamak pada kata ulang dilarang; pasif berawalan *di-* wajib mempertahankan sufiks *-kan*; preposisi pemblokir subjek pada komplemen *bahwa* dihapus; koma sebelum konjungsi komplementer *bahwa* dilarang (Kantor Bahasa Kaltim).

---

### BW. Tanda Tulisan AI (*WP:AISIGNS*) & Tipografi EYD V (`AIS-001`..`AIS-010`)

Rujukan: *Wikipedia:Signs of AI writing* (*WP:AISIGNS*), EYD Edisi V (SK 0424/I/BS.00.01/2022), Gorys Keraf (*Diksi dan Gaya Bahasa*; *Komposisi*), dan Pamusuk Eneste (*Buku Pintar Penyuntingan Naskah*); uraian lengkap di `references/wp-aisigns-indonesia.md`.

1. **Pola:** klausa ekor partisipial kosong di akhir kalimat (*..., menyoroti pentingnya...*, *..., menggarisbawahi peran vital...*, *..., memastikan integrasi yang mulus...*) → **Perbaikan:** hapus klausa ekor atau ganti dengan bukti konkret terukur — **Sebab:** analisis dangkal (*superficial `-ing` analyses*) hanya mengulang klaim umum tanpa data baru (`AIS-001`).
2. **Pola:** atribusi kabur (*para ahli berpendapat*, *banyak pengamat menilai*, *laporan industri menunjukkan*) dan pengantar menggurui (*penting untuk dicatat bahwa*, *perlu diingat bahwa*, *tak dapat dipungkiri bahwa*) → **Perbaikan:** sebutkan peneliti/lembaga/tahun secara eksplisit dan hapus frasa pengantar penunda fakta — **Sebab:** atribusi anonim dan nada didaktis menurunkan kredibilitas ilmiah/jurnalistik (`AIS-002`, `AIS-003`).
3. **Pola:** sisa percakapan asisten (*Tentu, berikut...*, *Pertanyaan yang bagus*, *Semoga membantu!*), inflasi signifikansi (*berdiri sebagai simbol*, *menandai tonggak bersejarah*), paralelisme negatif (*bukan sekadar X, melainkan sebuah Y*), dan templat tantangan/prospek (*Meskipun memiliki banyak kelebihan, X menghadapi sejumlah tantangan*) → **Perbaikan:** bersihkan artefak chatbot dan sajikan fakta serta keterbatasan secara denotatif-spesifik (`AIS-004`..`AIS-007`).
4. **Pola:** tanda pisah em-dash berspasi khas LLM (` — `), *synonym cycling* (mengganti nomina entitas yang sama di tiap kalimat), rentang semu (*mulai dari inovasi teknologi hingga dampak sosial*), *rule of three* mekanis, daftar ber-**boldface** di tiap kepala butir, *Title Case* ala Inggris, atau emoji di naskah formal → **Perbaikan:** tulis tanda pisah EYD V **tanpa spasi** (`kata—kata`) atau ganti koma/kurung (`AIS-008`), jaga konsistensi istilah (`AIS-009`), dan ikuti kapitalisasi judul serta penebalan proporsional EYD V (`AIS-010`).


