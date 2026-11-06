# DESIGN.md — kontrak desain <nama halaman/produk>

> Salin ke root proyek (`cp ~/.agents/templates/DESIGN.md ./DESIGN.md`), isi sebelum menulis kode.
> Semua angka di sini harus berasal dari pengukuran (`dref`), bukan perasaan.
> AI wajib membaca file ini sebelum mengubah UI, dan memperbaruinya kalau keputusan berubah.

## 1. Brief
- Pengguna utama: <!-- siapa, dalam satu kalimat -->
- 1 aksi utama halaman ini: <!-- mis. "assign kendaraan ke trip" -->
- Suasana yang dituju: <!-- tenang-padat / editorial / teknis / hangat -->
- Ukuran sukses: <!-- mis. paham kondisi armada ≤3 detik; konversi form ≥x% -->

## 2. Referensi (terukur)
| Sumber | Yang diambil | Angka kunci |
|---|---|---|
| <!-- url --> | <!-- grid/density/hierarki --> | <!-- skala 1.25x, radius 8/15, gap 24/32 --> |

Perintah yang dipakai: `dref <url>` → `~/.agents/refs/<slug>/notes.md` + `desktop-hero.png` (dibuka, bukan cuma dibaca angkanya).

Yang **tidak** diambil: <!-- gradient ungu-biru, 3 kartu identik, badge "AI-powered", copy pujian diri -->

## 3. Token (satu sumber)
```css
/* hasil awal: dref <url> --tailwind, lalu dirapikan */
@theme {
  --color-bg-1: ;
  --color-text-1: ;
  --color-accent: ;
  --font-sans: ;
  --text-1: ;
  --radius-1: ;
  --spacing-1: ;
}
```
- Skala spacing: 4/8/12/16/24/32/48/64 (tidak ada nilai di luar skala)
- Skala tipe: <!-- rasio + daftar ukuran -->
- Radius: <!-- px -->
- Motion: <!-- 120–240ms mikro, easing -->

## 4. Struktur & state
| Bagian | Default | Loading | Empty | Error | Sukses |
|---|---|---|---|---|---|
| <!-- header --> | | | | | |

- Dark mode: <!-- token diatur ulang, bukan inversi -->
- Mobile: <!-- apa yang berubah di <768px -->

## 5. Keputusan a11y
- Kontras teks: <!-- angka hasil dcheck -->
- Target sentuh: ≥24×24 px, jarak ≥8 px
- Keyboard: <!-- urutan fokus, Esc untuk overlay -->
- `prefers-reduced-motion`: <!-- apa yang dimatikan -->

## 6. Bukti (diisi saat selesai)
- `dcheck <url>` → <!-- LULUS / gate yang masih gagal -->
- Screenshot: <!-- desktop + mobile, path -->
- Catatan jujur: <!-- yang belum selesai / sengaja ditunda -->
