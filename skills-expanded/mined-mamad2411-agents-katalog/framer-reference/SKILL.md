---
name: framer-reference
description: Ambil referensi UI/UX nyata dari site Framer (atau site apa pun) untuk dipakai AI saat membangun UI — scrape HTML, ekstrak design token (font, palet, radius, shadow, gradient), screenshot desktop/mobile, lalu tulis notes.md siap baca. Pakai saat user minta "bikin UI seperti X", "referensi dari Framer", "analisa tampilan site ini", atau butuh contoh layout/palet sebelum menulis kode frontend.
metadata:
  origin: local
  version: "1.0"
---

# Framer Reference — referensi UI/UX yang bisa "dilihat" AI

Framer tidak punya API resmi untuk membaca desain/asset project orang. Yang bisa dipakai:
site Framer yang sudah **publish** (HTML+CSS inline), gallery `framer.com/community/gallery`,
dan asset publik `framerusercontent.com`. Skrip ini mengubah URL jadi bukti visual + token
numerik yang bisa dipakai AI tanpa menebak.

## Kapan dipakai (otomatis)

Aktifkan **sebelum** menulis/mengubah UI ketika user:

- menyebut referensi visual: "Framer", "seperti site ini", "contoh dari Dribbble/Figma/Framer",
  "bikin landing page kayak X", "ambil inspirasi dari …"
- memberi URL dan minta "analisa tampilan/desainnya", "tiru style-nya", "buat yang mirip"
- minta standar visual baru (palet, tipografi, spacing, radius) tanpa menyebut angka

Jangan dipakai untuk: mengubah logic/backend, menyalin brand/teks/aset berhak cipta.

## Perintah

```bash
R=~/.agents/skills-store/framer-reference/scripts/framer-ref.sh

$R <url>                 # analisa 1 site -> ~/.agents/refs/<slug>/
$R <url> --no-shot       # token saja (cepat, tanpa Playwright)
$R --gallery portfolio   # daftar site Framer bagus + live URL
```

Kategori gallery yang **teruji ada isinya**: `portfolio`, `saas`, `agency`, `ecommerce`,
`blog`, `personal`. (`design`, `startup` kosong — jangan dipakai.)

## Output

`~/.agents/refs/<slug>/`

| File | Isi |
|---|---|
| `desktop-hero.png` | viewport atas 1440×900 — **baca ini dulu** |
| `desktop.png` | full page 1440 |
| `mobile.png` | full page 390 (cek perilaku responsif) |
| `tokens.json` | font, skala ukuran, palet+frekuensi, radius, shadow, gradient, CSS vars asli Framer |
| `notes.md` | ringkasan siap baca: palet berlabel, hierarki heading, nav, CTA, aset |
| `page.html` | HTML mentah untuk verifikasi |

## Alur wajib setelah skrip jalan

1. Baca `notes.md` + lihat `desktop-hero.png` (jangan hanya percaya hex code).
2. Ambil **prinsip**: grid/kolom, density spacing, kontras, skala tipografi, radius, hierarki CTA.
3. Cek `mobile.png` → tentukan breakpoint & cara stack.
4. Baru tulis kode. Sebutkan referensi mana yang dipakai (slug) supaya bisa diaudit.
5. Verifikasi hasil: bandingkan screenshot UI baru dengan `desktop-hero.png`.

## Batasan jujur

- Site dengan proteksi bot/Cloudflare bisa gagal → skrip gagal keras (exit 2), jangan
  mengarang token. Coba `--no-shot` dulu, atau pakai URL site Framer lain.
- `--gallery` hanya membaca halaman publik; kalau struktur HTML Framer berubah,
  hasil bisa kosong — laporkan apa adanya, jangan diakali.
- Screenshot butuh Playwright + Chromium lokal (sudah terpasang di mesin ini).
- Aset Framer (`framerusercontent.com`) boleh dilihat untuk referensi; jangan
  redistribusikan sebagai milik sendiri.

## Contoh nyata (teruji)

```
$ framer-ref.sh https://jason-ng.space/
OK https://jason-ng.space/
-> ~/.agents/refs/jason-ng-space
{"sections": 0, "elements": 450, "shots": [desktop.png, desktop-hero.png, mobile.png]}
```
