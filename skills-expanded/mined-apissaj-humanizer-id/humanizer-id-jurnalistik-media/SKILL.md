---
name: humanizer-id-jurnalistik-media
description: Use when editing Indonesian news, opinion articles, feature essays, or press releases.
version: 2.5.0
author: Hafizh Muzani / Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [writing, editing, bahasa-indonesia, jurnalistik, opini]
    category: creative
    homepage: https://github.com/apissaj/humanizer-id
    parent: humanizer-id
---

# Humanizer ID — Jurnalistik & Media

Sub-kaidah domain Humanizer ID untuk berita, artikel opini, kolom populer, tajuk rencana, dan rilis media (`--preset jurnalistik`). Muat berkas ini setelah `humanizer-id` (induk) untuk menjaga kelugasan, ekonomi kata, dan keterbacaan publik.

---

### A. Tujuh Sifat & Prinsip Bahasa Pers (Badudu 1988; Pusdiklat Kemendikbud 2018, hlm. 17–22)

1. **Pola:** kalimat pasif birokratis bertumpuk, istilah teknis mentah tanpa penjelasan, dan ragam tutur santai di berita/artikel → **Perbaikan:** terapkan 7 sifat bahasa jurnalistik (singkat, padat, sederhana, lugas, menarik, lancar, jelas), utamakan kalimat aktif, terjemahkan istilah teknis ke padanan umum, dan patuhi EYD V (`memercayai` bukan *mempercayai*, `mengampanyekan` bukan *mengkampanyekan*) — **Sebab:** gaya selingkung redaksi tidak boleh melanggar ejaan baku KBBI (`JRN18-001`..`003`, `JRN18-010`) (hlm. 17–18, 22).

---

### B. Ekonomi Kata Tempo & Pemangkasan Basa-Basi Penunda Fakta (Tempo 2008; Pusdiklat 2018, hlm. 19–21)

1. **Pola:** *dapat disampaikan bahwa...*, *sehubungan dengan hal tersebut di atas maka...*, *sementara itu, di tempat yang berbeda...* → **Perbaikan:** hapus pembuka penunda fakta dan langsung nyatakan inti informasi atau gunakan transisi ringkas (*di sisi lain* / *secara terpisah*) — **Sebab:** ekonomi kata jurnalistik menyingkirkan basa-basi birokratis yang memperlambat pembaca (`TMP-001`, `JURNAL-EKONOMI`).
2. **Pola:** frasa memutar (*pada saat ini*, *membubuhkan tanda tangannya*, *melangsungkan pernikahan*, *tidak jauh dari*, *mampu melarikan diri*) → **Perbaikan:** *kini*, *menandatangani*, *menikah/kawin*, *dekat*, *lolos* — **Sebab:** substitusi satu kata kuat menghemat ruang redaksional (`JRN18-004`) (hlm. 19).
3. **Pola:** pleonasme frasa pers (*ramalan masa depan*, *alternatif lain*, *hadiah cuma-cuma*, *kesimpulan akhir*, *maju ke depan*) dan kontaminasi (*demi untuk*, *agar supaya*, *berhubung karena*, *sementara orang*, *untuk sementara waktu*) → **Perbaikan:** *ramalan*, *alternatif*, *hadiah*, *kesimpulan*, *maju*; *demi*/*untuk*, *agar*/*supaya*, *karena*, *beberapa orang*, *untuk sementara* — **Sebab:** kata mubazir dan kontaminasi konjungsi merusak kepadatan berita (`JRN18-005`..`006`) (hlm. 19–20).
4. **Pola:** rantai klausa relatif berpanjang-panjang (*Gedung yang mana didirikan pada tahun 1920 tersebut kini difungsikan...*) → **Perbaikan:** ringkas menjadi pewatas nomina lugas (*Gedung peninggalan tahun 1920 itu kini difungsikan...*) — **Sebab:** `[telaah]` pereduksian anak kalimat memangkas kata tanpa menghapus fakta (`TMP-002`, `JRN18-007`).

---

### C. Batas Panjang Kalimat & Keterpahaman Publik (Pusdiklat 2018, hlm. 20–21)

1. **Pola:** kalimat berita sepanjang 29+ kata berisi beberapa anak kalimat bertumpuk → **Perbaikan:** pecah menjadi kalimat pendek maksimal **17–20 kata** (skala mudah/standar: 8–17 kata) dengan satu gagasan inti per kalimat — **Sebab:** pembaca media massa membutuhkan keterpahaman instan (`JRN18-008`) (hlm. 20).
2. **Pola:** *Ismail menjelaskan bahwa pembinaan...* (pada ragam berita ringkas) → **Perbaikan:** *Ismail menjelaskan, pembinaan...* atau kutipan langsung yang hidup — **Sebab:** penghilangan *bahwa* pascaverba ujaran membuat kalimat berita lebih lincah bila tidak menimbulkan ketaksaan (`JRN18-011`) (hlm. 20).

---

### D. Padanan Istilah Media & Struktur Artikel Opini (`glosarium-lintas-bidang.json` & Modul Opini KD 3.11)

- **Padanan istilah media baku:** *breaking news* → **berita sela / kabar kilat**; *coverage* → **liputan**; *off the record* → **bukan untuk disiarkan / tertutup**; *fact-checking* → **pemeriksaan fakta / verifikasi fakta**; *clickbait* → **umpan klik**; *podcast* → **siniar**; *stand up comedy* → **komedi tunggal**; *commuter line* → **kereta komuter**; *busway* → **jalur bus**; *reshuffle* → **perombakan**; *selfie* → **swafoto**; *rising star* → **bintang baru**; *anchorman* → **penyiar utama**; *byline* → **baris nama penulis**; *deadline* → **tenggat**; *doorstop interview* → **wawancara cegat**; *embargo* → **larangan siar sementara**; *feature* → **karangan khas**; *headline* → **tajuk utama / kepala berita**; *infographic* → **infografik**; *live streaming* → **siaran langsung daring**; *press release* → **siaran pers**; *prime time* → **jam tayang utama** (`glosarium-lintas-bidang.json`, 26 istilah).
- **Kelengkapan 5W+1H & sunting redaksi 4 lapis (`JRN18-014`):** pastikan berita ringkas tetap memuat *What, Who, When* (rinci), *Where* (spesifik), *Why*, dan *How* (kronologi), serta melewati swasunting → editor bahasa → redaktur bidang → redaktur pelaksana sebelum tayang (Ridho dkk., Kemendikbudristek 2021, hlm. 18–20, 36).
- **Urutan penyebutan & serapan berita (Baharman, UNM):** dahulukan padanan Indonesia baru istilah asing bercetak miring dalam kurung (*paparan risiko (exposure)*, bukan *exposure (paparan risiko)*) (`TMS-048`), dan hindari salah adaptasi seperti *misskoordinasi* → **miskoordinasi** atau *volantilitas* → **volatilitas** (`TMS-047`).
- **Struktur artikel opini:** tesis (pernyataan sikap jelas) → argumentasi (berbasis fakta/data terverifikasi, tanpa hiperbola *revolusioner* atau *luar biasa*) → penegasan ulang (simpulan konkret tanpa slogan utopis).

```bash
# Audit artikel opini/berita dengan preset jurnalistik
python scripts/audit.py artikel-opini.md --preset jurnalistik --report
```
