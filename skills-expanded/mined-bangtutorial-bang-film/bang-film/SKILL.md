---
name: bang-film
description: "Merancang konsep dan MENULIS PROMPT untuk video AI live-action — microdrama vertikal berseri, short movie, atau scene/trailer tunggal. Skill ini TIDAK menggenerate media apa pun: keluarannya berkas teks berisi konsep cerita, cast bible, shot list, prompt sheet karakter (3 panel: close-up kiri, badan depan dan belakang kanan, nama tercetak di gambar), prompt plate set dan properti, dan prompt video berformat sebelas blok (VIDEO STYLE & FORMAT, LANGUAGE, OPTICS, CAMERA, LIGHTING, CRITICAL, CHARACTERS, LOCATION, AUDIO, MOVEMENT NOTE, SHOT BREAKDOWN) yang tinggal di-copy user ke AI gambar dan AI video mana pun. Tiap prompt video 4–30 detik (satu kali generate); episode yang lebih panjang dipecah mengikuti alur. Rasio, durasi, jumlah episode selalu ditanyakan, tidak pernah dipatok; jumlah shot tidak pernah ditanya. Gunakan saat user minta 'bang-film', bikin microdrama, drama pendek vertikal, short movie, film pendek AI, scene atau trailer, prompt video AI, shot list, sheet karakter, atau melanjutkan episode seri yang sudah ada. Bukan untuk animasi kartun 2D (bang-animation-stickman, bang-animation-horror, bang-animation-milojanes), bukan video 3D three.js (bang-3d-shorts), bukan motion graphic atau kinetic typography (bang-motion)."
license: MIT
metadata:
  author: Bang Tutorial
  author_url: https://youtube.com/bangtutorial
  version: "1.3.0"
  updated: "2026-11-12"
---

# Bang Film — perancang konsep & penulis prompt video AI

**v1.3.0 · by [Bang Tutorial](https://youtube.com/bangtutorial) · MIT.**

Skill ini **asisten rancang, bukan generator**. Tidak ada gambar, video, audio, atau berkas
media yang dibuat di sini. Yang keluar adalah berkas teks: konsep, cast bible, shot list, dan
prompt siap copy-paste. User yang menjalankan generate-nya di AI gambar dan AI video pilihannya
sendiri.

Satu mesin, tiga preset:

| | MICRODRAMA | SHORT MOVIE | SCENE / TRAILER |
|---|---|---|---|
| Bentuk | seri berepisode | satu cerita utuh | satu blok tunggal |
| Struktur naskah | hook keras di awal, cliffhanger di akhir tiap episode | tiga babak, ada resolusi | satu momen, tanpa resolusi |
| Lintas episode | cast, set, properti dipakai ulang | — | — |
| Cocok untuk | cerita bersambung yang bikin orang nunggu episode berikutnya | film pendek, tugas, portofolio | teaser, uji look, satu adegan |

Tulang belakangnya identik untuk ketiganya. Yang berbeda hanya struktur naskah di gerbang 2 dan 4.

## Alur kerja — tujuh gerbang, jangan dilompati

### 0 · Tempat kerja
- Tanyakan folder proyek kalau belum jelas. **Jangan hardcode lokasi mana pun.**
- Proyek baru: salin `assets/template/` ke folder proyek.
- Deteksi dulu: proyek baru, atau lanjut episode dari seri yang sudah ada? Kalau lanjut, baca
  `konsep.md`, `cast.md`, dan `set.md` yang sudah ada lalu **pakai apa adanya** — jangan ditulis
  ulang, karena itu yang menjaga tokoh konsisten lintas episode.

### 1 · BRIEF — tanya dulu, jangan menebak
Baca `references/brief.md`.

Alat tanya pilihan maksimal empat pertanyaan, jadi brief selalu **dua kartu**:
- **Kartu 1:** topik · format · rasio · bahasa dialog
- **Kartu 2:** durasi · jumlah episode · look

Lewati item yang sudah terjawab dari kalimat pertama user. Semua nilai **dikosongkan** — tidak ada
default. Kalau jawaban saling bentrok (misalnya topik "tiap malam", look "siang hari"), sebutkan
bentroknya dan tawarkan resolusi; jangan diam-diam memilih.

**Jumlah shot tidak pernah ditanyakan.** Shot ditentukan naskah dan AI video saat generate.

**Output:** `brief.md`

### 2 · KONSEP → minta persetujuan
Baca `references/konsep.md` dan `references/copywriting.md`.

**Output:** `konsep.md` — logline, premis 3 baris (termasuk satu detail meleset dan satu aturan
tokoh), arc per episode kalau seri, dan **3 hook alternatif dengan rumus berbeda**.

Sebelum setor, periksa dua hal yang paling sering lolos: hook dan arc **tidak bertentangan dengan
premis**, dan **tidak ada beat penting yang bergantung pada tulisan yang harus dibaca** di layar.

Berhenti. Jangan lanjut sebelum user memilih hook dan menyetujui konsep.

### 3 · CAST, SET & PROPERTI → minta persetujuan
Baca `references/cast.md`.

**Output:** `cast.md` dan `set.md`.
- Tokoh: satu blok terkunci dalam dua bentuk — **panjang** (untuk prompt sheet) dan **pendek**
  (untuk blok CHARACTERS di prompt video).
- Set: satu blok per lokasi, termasuk **semua pintu dan jalan masuk** yang dipakai arc.
- Properti: benda atau kendaraan yang muncul berulang dan bisa berubah bentuk antar klip.

Tiap tokoh, set, dan properti berpelat dapat token `[gambar_<nama>]`.

Berhenti. Mengganti deskripsi tokoh setelah prompt ditulis berarti menulis ulang semuanya.

### 4 · NASKAH + SHOT LIST → minta persetujuan
Baca `references/konsep.md` bagian naskah dan `references/copywriting.md`.

**Output:** `epNN/naskah.md` — dialog lengkap supaya bisa dibaca sebagai cerita, rundown per shot,
lalu pembagian scene.

**Pembagian scene:** satu scene = satu prompt video = satu kali generate = **4–30 detik**.
Episode lebih dari 30 detik dipecah mengikuti alur cerita — 60 detik bisa 30:30, 20:20:20, atau
pembagian lain yang pas dengan beat-nya. Pindah lokasi selalu berarti scene baru. Jangan memecah
di tengah dialog.

Cek total durasi ke `brief.md`. Kalau lewat, **lapor dan tawarkan shot mana yang dipotong** —
jangan diam-diam memotong sendiri.

Kalau blocking butuh pintu, jendela, atau elemen ruang yang belum ada di `set.md`, **tambahkan**
— penambahan saja, sebelum prompt ditulis, dan catat sebagai revisi di `set.md`.

**Shot berisiko:** tandai shot yang rawan plot hole di AI video — tempat yang sama dari dua sisi,
shot lewat celah atau kaca, sudut yang tidak ada di plate, ketiadaan benda yang harus terbaca,
benda yang harus bertahan antar potongan, close-up tanpa wajah di dekat dialog. Daftar lengkap
dan alternatifnya ada di `references/konsep.md`. Laporkan bersama shot list; **user yang
memutuskan** mempertahankan atau mengganti.

### 5 · PROMPT ASET
Baca `references/prompt-aset.md`.

**Output:** `epNN/prompt-aset.md` — berisi aset yang **baru muncul di episode itu saja**, plus satu
baris "pakai ulang" untuk aset dari episode sebelumnya. Sheet karakter selalu tiga panel:
**close-up kiri, badan depan tengah, badan belakang kanan, nama tokoh tercetak di gambar.**

### 6 · PROMPT VIDEO
Baca `references/prompt-video.md`. Ini berkas terpenting di skill ini.

**Output:** `epNN/prompt-video.md` — satu judul markdown + satu blok prompt per scene. Prompt
berisi sebelas blok, berakhir di `SHOT BREAKDOWN`. Blok opsional `CONTINUITY` ditambahkan di
antara `LOCATION` dan `AUDIO` kalau ada benda yang harus bertahan antar potongan, atau lebih dari
satu plate lokasi dalam satu generate.

### 7 · VERIFIKASI & SERAH
Baca `references/verifikasi.md`.

Jalankan pengecek dulu:

```
python assets/tools/check_prompts.py <folder proyek>
```

Pengecek memeriksa salinan blok terkunci, sebelas blok, timecode, durasi 4–30 detik, token vs
berkas lampiran, tag lokasi, dan kata terlarang. Perbaiki sampai lolos. Lalu jalankan sisa
checklist yang tidak bisa dicek mesin, dan serahkan daftar berkas plus cara pakainya.

**Kalau user kembali membawa hasil generate yang plot hole**, ikuti bagian "Setelah user
generate" di `references/verifikasi.md`: bedah videonya dulu, perbaiki dengan satu atau dua
kalimat, simpan sebagai versi baru, dan kembali ke versi sebelumnya kalau hasilnya memburuk.

## Aturan dari user (wajib)

1. **Tidak menggenerate apa pun di sini.** Tidak ada gambar, video, audio, atau pemanggilan
   model generator. Keluaran skill ini hanya berkas teks. User generate di AI terpisah.
2. **Jangan hardcode rasio, durasi, atau jumlah episode.** Semuanya ditanyakan di gerbang 1.
   Kalau user mengubahnya di tengah jalan, yang diedit cuma `brief.md`.
3. **Jumlah shot tidak ditanyakan dan tidak dipatok.** Biarkan naskah dan AI video yang menentukan.
4. **Rasio tidak pernah masuk ke dalam prompt video.** Rasio diatur di pengaturan AI video sebelum
   generate. Termasuk kata `vertical` dan `horizontal` — buang.
5. **Header untuk manusia tidak masuk ke dalam prompt.** Judul seperti `=== PROMPT VIDEO · EP01 ===`
   ditulis sebagai judul markdown **di luar** blok kode. AI tidak memahaminya dan bisa
   menganggapnya bagian dari adegan.
6. **Tidak ada subtitle, caption, atau teks di layar.** Skill ini tidak mengurus subtitle sama
   sekali — itu kerjaan editor. Satu-satunya tempat kata subtitle boleh muncul adalah di daftar
   larangan blok `LANGUAGE`, justru supaya AI tidak menempelkan teks ke gambar.
7. **Dialog ditanam di dalam prompt video**, digenerate bersama klipnya seperti AI video pada
   umumnya. Tidak ada berkas audio terpisah, tidak ada TTS. Dialog tetap ditampilkan utuh di
   `naskah.md` supaya ceritanya bisa dibaca sebagai cerita.
8. **Prompt ditulis general**, tidak diikat ke satu tool. Jangan menulis sintaks khusus Seedance,
   Kling, Veo, atau mana pun. Bahasa prompt: **Inggris**; dialog di dalamnya memakai bahasa yang
   dipilih user.
9. **Blok cast, set, dan properti ditulis identik, huruf per huruf.** Jangan pernah meringkas atau
   memparafrase antar berkas. Satu kata berubah, wajahnya ikut berubah.
   **Tokoh tidak diberi tanda di wajah** — bekas luka, tahi lalat, tato, tindik. AI selalu
   melebih-lebihkannya sampai tokoh terlihat aneh. Wajah dikunci oleh gambar sheet; tokoh dibedakan
   lewat usia, rambut, bangun badan, dan wardrobe. Pengecualian hanya untuk tanda yang punya fungsi
   di naskah.
10. **`MOVEMENT NOTE` selalu ada.** Satu tokoh: berisi nada tubuhnya dari `cast.md`. Lebih dari dua
    orang di frame: **wajib** memecah gerak figuran dan melarang gerakan serempak — tanpa itu AI
    video menggerakkan mereka seperti paduan suara.
11. **Sheet karakter: close-up di kiri, detail outfit di kanan**, dan **nama tokoh tercetak di
    gambar** supaya sheet tidak tertukar saat dilampirkan sebagai referensi.
12. **Tiga gerbang persetujuan tidak boleh dilompati**: setelah konsep, setelah cast bible, setelah
    shot list. Lebih murah mengganti satu paragraf daripada empat puluh prompt.
13. **Satu prompt video = satu kali generate = 4–30 detik.** AI video sekarang menerima minimal
    4 detik dan maksimal 30 detik per generate. Episode yang lebih panjang dipecah mengikuti alur
    cerita, bukan dipotong rata.
14. **Beat penting tidak boleh bergantung pada tulisan.** Nama di label, pesan di layar HP, papan
    nama — AI video tidak bisa diandalkan merender tulisan, dan prompt melarang teks di layar.
    Sampaikan lewat gambar atau suara.
15. **Properti yang muncul berulang dikunci seperti tokoh**, dan di prompt video ditulis di blok
    `LOCATION`. Kalau posisinya harus bertahan antar potongan, dikunci di blok `CONTINUITY`.
16. **Lebih dari satu plate lokasi dalam satu generate** wajib memakai tiga hal sekaligus: peta
    referensi di awal `LOCATION`, tag lokasi di tiap baris SHOT, dan posisi tokoh di
    `CONTINUITY`. Tanpa itu, tokoh bocor ke sisi pintu yang salah.
17. **Shot berisiko dilaporkan, tidak disembunyikan.** Tandai di gerbang 4, tawarkan
    alternatifnya, dan biarkan user yang memutuskan. Jangan mengganti diam-diam, jangan menolak
    menulisnya.
18. **Memperbaiki prompt setelah generate: satu atau dua kalimat per masalah**, simpan sebagai
    versi baru, dan kembali ke versi sebelumnya kalau hasilnya memburuk. Prompt yang makin
    panjang tidak membuat model makin patuh.

**Ditolak / dihindari:**
- Memanggil model generator apa pun dari dalam skill ini.
- Menyebut rasio, resolusi, seed, atau nama model di dalam prompt.
- Mengisi sendiri angka durasi atau jumlah episode karena user belum menjawab.
- Prompt video di bawah 4 detik atau di atas 30 detik. Memecah scene di tengah dialog.
- Format prompt video satu blok per shot. Satu blok = satu scene utuh, shot ada di dalamnya.
- Istilah `SCREENPLAY`, `ACTION`, atau `SCENE` sebagai judul bagian. Hanya `SHOT BREAKDOWN`.
- Menyebut tokoh, napasnya, matanya, atau daftar larangan orang (`no face, no head`) di shot
  lewat celah, kaca, atau dari mata tokoh — itu yang menanam wajah di frame.
- Menegaskan benda yang sama berulang-ulang di banyak blok. Benda yang terus disebut justru
  diubah model.
- Menegaskan ketiadaan benda dengan kata kontras (`darker`, `deeper colour`) — dirender jadi
  benda.
- Memberi tokoh bekas luka, tahi lalat, atau tanda wajah lain sebagai "jangkar" tanpa fungsi
  cerita.
- Naskah generik: lihat detektor klise di `references/copywriting.md`.

## Struktur skill

| Berkas | Isi |
|---|---|
| `assets/template/` | kerangka kosong tiap berkas keluaran, disalin ke proyek baru |
| `assets/tools/check_prompts.py` | pengecek gerbang 7 — Python 3, tanpa dependensi |
| `assets/contoh/alamat-yang-sama/` | proyek lengkap hasil skill ini sendiri: microdrama 3 episode × 30 detik, lolos pengecek |
| `assets/contoh/` (berkas lepas) | potongan seri "Unit 7" + sheet karakter RAFA sebagai acuan visual tata letak sheet |

## Referensi

| Berkas | Baca saat |
|---|---|
| `references/brief.md` | gerbang 1: dua kartu pertanyaan, aturan jangan menebak, menangani "terserah" dan jawaban yang bentrok |
| `references/konsep.md` | gerbang 2 & 4: struktur per format, trope microdrama, arc, hook, cliffhanger, beat tanpa teks, shot list, shot berisiko, pembagian scene 4–30 detik |
| `references/copywriting.md` | gerbang 2 & 4: hukum anti-generik, detektor klise, dialog yang tidak sinetron, rubrik |
| `references/cast.md` | gerbang 3: anatomi blok cast, bentuk panjang vs pendek, token gambar, set, properti |
| `references/prompt-aset.md` | gerbang 5: template sheet karakter 3 panel, set plate, plate properti, daftar Avoid wajib |
| `references/prompt-video.md` | gerbang 6: sebelas blok satu per satu, CONTINUITY, peta referensi dan tag lokasi, yang dilarang masuk prompt, format SHOT BREAKDOWN |
| `references/verifikasi.md` | gerbang 7: pengecek, checklist manual, gejala → penyebab, memperbaiki prompt setelah user generate |
