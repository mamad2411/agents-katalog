---
name: anti-slop-checklist
description: Checklist anti-slop untuk UI, video, dan tulisan — supaya hasil kerja tidak terlihat generik khas AI. Merujuk ke taste-skill, unslop, hallmark, dan anti-slop.
---

# anti-slop-checklist

Skill orisinal `muse-rsi`. Dipakai sebelum hasil kerja dikirim ke Fahmi atau dipublikasikan.

## Tujuan

Hasil AI yang generik mudah dikenali: layout yang itu-itu saja, warna ungu-biru standar, emoji berlebihan, kalimat klise, dan video yang terasa seperti template. Checklist ini mencegah itu.

## Sumber yang dirujuk

Skill-skill ini **bukan** milik kami — baca SKILL.md aslinya di repo upstream sebelum memakai aturannya secara detail:

- [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) — taste / art direction.
- [heydamir/unslop](https://github.com/heydamir/unslop) — mengubah UI yang terlihat hasil AI menjadi desain yang dirancang.
- [Nutlope/hallmark](https://github.com/Nutlope/hallmark) — anti-slop desain.
- [miqdadbadjuber/anti-slop](https://github.com/miqdadbadjuber/anti-slop) — anti-slop untuk kode, copywriting, dan tulisan (cadangan terverifikasi, lihat `docs/critique.md`).
- [adhiprib/humanizer-indonesia](https://github.com/adhiprib/humanizer-indonesia) — tulisan Bahasa Indonesia yang luwes dan natural, bukan untuk mengelabui deteksi AI.

## Checklist UI / Web

- [ ] Ada **satu** gaya visual yang jelas (bukan campur 3 gaya).
- [ ] Warna tidak memakai gradasi ungu-biru standar AI tanpa alasan.
- [ ] Tidak ada emoji sebagai hiasan utama.
- [ ] Jarak, ukuran huruf, dan hierarki konsisten di semua halaman.
- [ ] Ada contoh nyata / data nyata, bukan teks contoh "Lorem ipsum" atau "Contoh Judul".
- [ ] Dicek di layar kecil dan layar besar — tidak ada yang terpotong.

## Checklist video

- [ ] Ada 1 ide utama per video, bukan 5 ide yang dipadatkan.
- [ ] Shot pertama langsung jelas — bukan pembuka generik 5 detik.
- [ ] Tokoh / gaya visual konsisten dari awal sampai akhir.
- [ ] Suara dan subtitle cocok dengan gambar (cek 1 frame acak).
- [ ] Tidak ada template yang sama persis dengan video AI lain.

## Checklist tulisan (Indonesia)

- [ ] Bahasa sederhana, kalimat pendek. Kalau ada jargon, dijelaskan maksimal 3 kata.
- [ ] Tidak ada kalimat klise seperti "di era digital ini", "sangat penting untuk", "dengan demikian".
- [ ] Ada fakta atau angka yang bisa dicek, bukan hanya opini umum.
- [ ] Dibaca keras 1 kali: kalau terdengar seperti mesin, tulis ulang dengan kata sendiri.
- [ ] Untuk Bahasa Indonesia, pakai rujukan [nothinx/naskah-id](https://github.com/nothinx/naskah-id) dan [adhiprib/humanizer-indonesia](https://github.com/adhiprib/humanizer-indonesia) — **dilarang** memakai humanizer untuk mengelabui deteksi AI atau plagiarisme.

## Kalau ada yang tidak lolos

- Perbaiki 1 hal terbesar dulu, jangan perbaiki semuanya sekaligus.
- Kalau sudah diperbaiki 2 kali tapi masih terasa generik, ganti pendekatan (misalnya: ganti referensi visual, atau tulis ulang dari nol dengan 1 contoh nyata).
- Jangan kirim hasil yang gagal checklist ini dengan klaim "sudah bagus".

## Batas

Checklist ini soal kualitas dan rasa, bukan soal menipu. Jangan pakai skill anti-slop atau humanizer untuk menyamar, mengelabui deteksi, atau menghapus jejak plagiarisme.
