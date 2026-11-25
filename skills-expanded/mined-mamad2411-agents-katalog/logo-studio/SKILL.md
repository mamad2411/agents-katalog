---
name: logo-studio
description: WAJIB OTOMATIS dipakai tanpa slash saat user minta logo, lambang, monogram, wordmark, favicon, atau ikon aplikasi. Mark dibangun dari geometri dan huruf asli yang di-outline, lalu dibuktikan di 16 px sebelum diserahkan.
version: 1.0.0
tags: [design, logo, brand, svg, typography, vector]
---

# Logo Studio

Membuat logo berarti membuat **keputusan yang bisa dipertanggungjawabkan**, bukan
menggambar bentuk yang terlihat enak. Skill ini menutup dua kesalahan yang paling
sering: (1) huruf digambar tangan sehingga proporsinya salah, (2) hasilnya tidak
pernah diuji di ukuran kecil.

## Aturan keras

1. **Jangan pernah menulis `d="..."` sendiri.** Semua path lahir dari `logo.py`
   (rect / circle / polygon / glyph asli) atau dari boolean Skia. Kalau kamu mengetik
   koordinat dengan tangan, kamu sedang menebak, bukan mendesain.
2. **Huruf harus dari typeface asli**, di-outline lewat `fontTools`, bukan huruf yang
   digambar ulang. Boleh pakai font sistem; kalau brand punya font sendiri, beri path
   berkasnya.
3. **Maksimal 3 warna.** Lebih dari itu bukan logo, itu ilustrasi.
4. **Harus lulus `proof.py`** sebelum diserahkan. Exit 1 = belum selesai.
5. **Wajib ada versi satu warna.** Logo yang tidak bisa dicetak satu warna belum jadi.
   Selalu jalankan `--mono`, lalu buktikan file `-mono.svg`-nya juga — bukan cuma yang berwarna.

## Alur (7 langkah)

1. **Brief satu kalimat.** Siapa pemakainya, di mana mark akan dilihat (tab browser?
   header 40 px? seragam?), dan satu hal yang harus diingat orang.
2. **Referensi nyata, bukan selera.** Buka 2–3 merek di industri yang sama:
   `dref https://…` lalu **baca screenshot-nya**, jangan cuma angkanya. Catat satu
   keputusan yang mau kamu tiru dan satu yang mau kamu hindari.
3. **Geometri dulu.** Tentukan grid (biasanya 1000×1000), lalu bentuk dasarnya:
   kotak, lingkaran, potongan 45°. Mark yang benar biasanya bisa dijelaskan dalam
   satu kalimat bentuk.
4. **Bangun lewat spec.** Tulis JSON, jalankan `logo.py`. Iterasi di angka, bukan di
   mata: geser 4 px, jangan "kira-kira agak ke kanan".
5. **Buktikan.** `proof.py` merender 16–256 px di terang dan gelap sekaligus.
6. **Baca proof-nya dengan mata.** Angka lulus belum berarti bagus. Kalau di 16 px
   bentuknya jadi bubur, ulangi langkah 3 — jangan tambah detail.
7. **Serahkan dengan alasan.** Tiap warna dan tiap potongan harus punya kalimat
   "karena…". Kalau tidak ada, itu hiasan.

## Perintah

```bash
S=~/.agents/skills-store/logo-studio/scripts
$S/run.sh fonts list "DIN"              # font apa saja yang terpasang
$S/run.sh fonts path "DIN Alternate" Bold
$S/run.sh build spec.json -o out/ --trim --mono "#ffffff"
$S/run.sh proof out/mark.svg -o out/proof.png --dark "#0a1420" --light "#f2f0ea"
```

Selalu lewat `run.sh`. Dia yang memilih interpreter: `build`/`fonts` ke venv
(`fontTools` + `skia-pathops`), `proof` ke python3 sistem (Playwright). Memanggil
`logo.py` dengan `python3` biasa akan gagal `ModuleNotFoundError` — itu bukan bug.

## Format spec

```json
{
  "name": "genzys",
  "size": [1000, 1000],
  "palette": { "ink": "#0a1420", "gold": "#fdcc3f", "route": "#2f7fd8" },
  "shapes": [
    { "id": "plate", "rect": [0, 0, 1000, 850], "fill": "gold" },
    { "id": "lane",  "rect": [0, 850, 1000, 150], "fill": "route" },
    { "id": "g", "glyph": { "text": "G", "font": "DIN Alternate",
                            "style": "Bold", "height": 480 },
      "center": [500, 425], "fill": "ink" }
  ],
  "ops":   [ { "op": "subtract", "a": "plate", "b": "g", "out": "plate_cut" } ],
  "draw":  ["plate_cut", "lane"]
}
```

- Bentuk: `rect` (+`radius`), `circle`, `polygon`, `glyph` (`text`, `font`, `style`,
  `height` = tinggi kapital, `tracking`).
- Posisi: `center: [x,y]` (optis) atau `at: [x,y]` (kiri-atas tinta).
- Boolean: `union`, `subtract`, `intersect`, `exclude`. Hasil mewarisi warna `a`.
- `draw` menentukan urutan tumpuk (**bawah ke atas**); `--trim` memotong viewBox ke tinta.
- `mono: { "union": [...], "cut": [...] }` — opsional, memaksa cara versi satu warna
  dibentuk. Tanpa ini `--mono` menebak sendiri (lihat di bawah).

## Versi satu warna

`--mono "#f2f0ea"` tidak sekadar mengecat semua path dengan satu warna — itu
menghasilkan blok pejal, hurufnya hilang. Yang dikerjakan: lapisan di atas yang
warnanya beda **dan** berada di dalam siluet dianggap inlay, jadi dilubangi.
Lapisan sewarna atau yang keluar dari siluet di-union. Hasilnya satu path, satu
warna, huruf tetap terbaca.

Kalau tebakan itu salah untuk mark-mu, paksa urutannya:

```json
"mono": { "union": ["plate", "lane"], "cut": ["g"] }
```

## Yang diukur `proof.py`

| cek | arti | gagal kalau |
|---|---|---|
| `colours` | jumlah isi | > 3 |
| `ink-16` | tinta yang selamat di 16 px | 0% (mark hilang total di ukuran tab) |
| `feature-16` | goresan tertipis di 16 px | < 1 px (dan bukan mark penuh) |
| `detail-16` | masih ada struktur di 16 px | 1 warna padahal multi-warna |
| `contrast-*` | kontras vs latar & antar warna | **peringatan saja** — logo dikecualikan WCAG |

`ink-16` diukur dari raster 16×16, bukan dari SVG ukuran penuh: yang dinilai adalah
apakah mark masih meninggalkan bekas di ukuran terkecil, bukan apakah file-nya berisi.

## Larangan (biar tidak jadi AI slop)

- Gradien, bayangan, glow, bevel. Logo harus mati dengan baik dalam satu warna.
- Bentuk yang cuma "keren": panah naik, bola dunia, simpul tak berujung, huruf yang
  dipotong asal-asalan. Kalau tidak bisa dijelaskan, buang.
- Menumpuk tiga ide dalam satu mark. Satu mark, satu gagasan.
- Menyerahkan PNG hasil generator gambar sebagai "logo" — tidak bisa di-scale,
  tidak bisa dicetak, tidak bisa dijadikan favicon.

## Contoh

`examples/badge.json` — pelat emas + G DIN + jalur biru (3 warna, tumpuk).
`examples/knockout.json` — huruf dilubangi dari cakram lewat `subtract` (1 warna).
Jalankan:

```bash
$S/run.sh build $S/../examples/badge.json -o /tmp/logo --trim --mono "#f2f0ea"
$S/run.sh proof /tmp/logo/genzys.svg -o /tmp/logo/proof.png
$S/run.sh proof /tmp/logo/genzys-mono.svg -o /tmp/logo/proof-mono.png
```

Kalau `proof` bilang `LULUS (dengan catatan)` dan catatannya `contrast-dark 1.0:1`,
itu tandanya warna `--mono` yang kamu pilih sama dengan latar. Ganti warnanya.
