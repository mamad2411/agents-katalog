---
name: humanizer-id-skripsi-kampus
description: Use when editing Indonesian theses, dissertations, or research proposals with campus presets.
version: 2.5.0
author: Hafizh Muzani / Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [writing, editing, bahasa-indonesia, skripsi, kampus]
    category: creative
    homepage: https://github.com/apissaj/humanizer-id
    parent: humanizer-id
---

# Humanizer ID — Skripsi & Preset Kampus

Sub-kaidah domain Humanizer ID untuk **skripsi, tesis, disertasi, dan proposal riset mahasiswa** sesuai konvensi **18 preset perguruan tinggi & jurnal** di `data/pedoman-kampus.json` serta temuan empiris jurnal kesalahan skripsi. Muat berkas ini setelah `humanizer-id` (induk) bersama preset kampus yang diminta pengguna.

---

### A. Peta 18 Preset Kampus & Konvensi Wajib (`data/pedoman-kampus.json`)

| Kode | Institusi | Gaya Sitasi | Kaidah Teknis & Editorial Khas |
|---|---|---|---|
| `ui` | Universitas Indonesia | APA / IEEE | Abstrak dwibahasa; rujukan tabel/gambar bernomor bab (*Tabel 1.1*) |
| `itb` | Institut Teknologi Bandung | IEEE / Harvard / APA | Persamaan bernomor `(1.1)` di dalam kurung; sampul minimalis |
| `ugm` | Universitas Gadjah Mada | IEEE / APA | Rujukan rumus wajib *Persamaan (nomor)*; Simpulan & Saran dipisah tegas |
| `its` | ITS Surabaya | IEEE | Tinjauan pustaka menekankan *state-of-the-art* 5 tahun terakhir |
| `ipb` | IPB University | Name-Year | **Sub-bab tanpa titik akhir** (`1.1 Latar Belakang`); nama ilmiah miring berautoritas (`*Oryza sativa* L.`) |
| `undip` | Universitas Diponegoro | IEEE / APA / Harvard | Judul bab kapital tebal di tengah; pasif metodologi ketat |
| `unpad` | Universitas Padjadjaran | APA / Chicago | Abstrak maksimal 250 kata, satu paragraf spasi tunggal |
| `unair` | Universitas Airlangga | Vancouver / APA | Sitasi bernomor Vancouver untuk biomedis; APA untuk sosial-humaniora |
| `ub` | Universitas Brawijaya | IEEE / APA | Larangan konjungsi di awal kalimat; paragraf minimal 2 kalimat efektif |
| `telkom` | Telkom University | IEEE | Format artikel IEEE; tautan repositori GitHub & dataset publik di pustaka |
| `udinus` | UDINUS | IEEE / APA | Wajib memuat pengujian *black-box* & uji pengguna; kode *monospace* |
| `uns` | Universitas Sebelas Maret | APA / IEEE | Bab Romawi, sub-bab desimal; abstrak dwibahasa 200–250 kata |
| `unnes` | Universitas Negeri Semarang | APA 7th | Sub-bab desimal tanpa titik akhir; kutipan langsung >40 kata *indent* 1,2 cm |
| `upi` | Universitas Pendidikan Indonesia | APA 7th | Bab Analisis Data & Pembahasan terpisah tegas dari Temuan |
| `unhas` | Universitas Hasanuddin | Harvard / Vancouver / IEEE | Nomor halaman bab di tengah bawah; wajib terjemahan kutipan asing |
| `unand` | Universitas Andalas | APA / Harvard | Abstrak satu paragraf tanpa indentasi; rujukan persamaan `(1.1)` |
| `jurnal-dikbud` | Jurnal Dikbud Kemendikbudristek | Nama-tahun | Judul maks 14 kata; abstrak 150–200 kata tanpa sitasi; 80% pustaka primer |
| `jurnal-jipp` | JIPP Balitbang | Alfabetis-Kronologis | Abstrak dwibahasa 100–150 kata; 5 kata kunci |

---

### B. Penyakit Khas Draf Skripsi Mahasiswa (Empiris 5 Jurnal + Winarti dkk. 2009)

1. **Pola:** *didunia*, *diberbagai*, *disekitar*, *di peroleh*, *di terbitkan* → **Perbaikan:** *di dunia*, *di berbagai*, *di sekitar*, *diperoleh*, *diterbitkan* — **Sebab:** tertukarnya preposisi lokasi (`di` terpisah) dan prefiks pasif (`di-` serangkai) adalah kesalahan ejaan paling masif di abstrak dan bab isi skripsi (`JSK-001`..`004`, `TMS-037`).
2. **Pola:** *tujuan daripada penelitian ini*, *kesimpulan dari penelitian* → **Perbaikan:** *tujuan penelitian ini*, *simpulan/kesimpulan penelitian* — **Sebab:** *daripada* khusus perbandingan; posesif bahasa Indonesia dinyatakan langsung tanpa *dari* (`JSK-016`, `UIN-007`).
3. **Pola:** *penelitian ini adalah merupakan...*, *tempat di mana data diambil*, *beberapa metode-metode*, *sangat amat signifikan* → **Perbaikan:** pilih salah satu (*adalah* atau *merupakan*), *tempat data diambil*, *beberapa metode*, *sangat signifikan* — **Sebab:** kopula ganda, kalke relatif *di mana*, penjamakan ganda, dan superlatif bertumpuk menurunkan bobot ilmiah (`JSK-011`, `JSK-015`, `JSK-017`..`020`).
4. **Pola:** *mungkin/sepertinya hasil ini disebabkan...* pada paparan data empiris → **Perbaikan:** *hasil ini mengindikasikan...* atau *berdasarkan pengujian tercatat...* — **Sebab:** modalitas spekulatif ragam lisan (`JSK-007`) melemahkan objektivitas akademik; tetap jaga batas kepastian klaim sesuai data asli.
5. **Pola:** *Menurut Kim H. Tan (1991), bahwa...* atau *Berdasarkan hasil penelitian menunjukkan bahwa...* → **Perbaikan:** *Menurut Kim H. Tan (1991), ...* / *Hasil penelitian menunjukkan bahwa...* — **Sebab:** subjek tidak boleh didahului *bahwa* dan frasa keterangan *Berdasarkan X* tidak dapat langsung menjadi subjek (`SPK-012`, `SPK-013`).
6. **Pola:** *pengetauan, cendrung, defenisi, kesangupan, dikelas, kejenjang, disana, tapi, udah, cuma* serta fragmen *Yang disebabkan...* atau awal kalimat *Tetapi, ...* → **Perbaikan:** *pengetahuan, cenderung, definisi, kesanggupan, di kelas, ke jenjang, di sana, tetapi, sudah, hanya*, kalimat berinduk *Hal itu disebabkan...*, dan antarkalimat *Akan tetapi, ...* — **Sebab:** temuan empiris korpus proposal/skripsi STAIN Curup (Khair 2018), UNNES/UIR (Saputra & Alber 2021), UMK (Yahya dkk. 2018), serta TBBBI Ed. 4 (`JSK-007`..`011`, `TBB-033`, `TBB-035`).
7. **Pola:** *banyak nya, khusus nya, selesai.., yaitu;, manjemen, sehinnga, pastinya, Menurut (Mulyana 2005:21) menyatakan...* serta pelanggaran binomial (*IPOMOEA BATATAS*) → **Perbaikan:** *banyaknya, khususnya, selesai., yaitu:, manajemen, sehingga, tentu*, `Mulyana (2005:21) menyatakan...`, dan *Ipomoea batatas* miring — **Sebab:** mekanisasi lanjutan temuan KIBASP (2026), JURRIBAH (2026), DEIKTIS (2026), dan DiSastra (2021) (`JSK-012`..`018`).

---

### C. Pemisahan Simpulan vs Saran & Konsistensi Bab Akhir

1. **Bab Metodologi & Hasil:** pertahankan kalimat pasif ilmiah (*Sampel diekstraksi...*, *Pengujian dilakukan...*), jangan diubah ke aktif personal (*kami mengekstraksi*).
2. **Bab Simpulan vs Saran:**
   - **Simpulan** wajib menjawab butir rumusan masalah secara lugas berbasis angka/temuan bab Hasil, **tanpa** menambah data baru atau opini umum.
   - **Saran** khusus memuat keterbatasan teknis penelitian dan rekomendasi terukur bagi penelitian lanjutan atau pengguna sistem.
3. **Rujukan Visual:** ubah penunjuk spasial semu (*tabel di bawah ini*, *grafik di atas*) menjadi nomor eksplisit (*Tabel 4.1*, *Gambar 3.2*) mengikuti konvensi bab kampus aktif.

```bash
# Audit bab skripsi dengan preset akademik dan konvensi kampus spesifik
python scripts/audit.py bab3-metodologi.md --preset akademik --kampus ipb --report
```
