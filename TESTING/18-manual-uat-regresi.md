# 18 — Manual, exploratory, UAT, dan regresi

## 1. Exploratory testing terstruktur (bukan "coba-coba")
Charter 30–60 menit, satu tujuan, hasil dicatat:
```
CHARTER: Jelajahi alur checkout untuk menemukan masalah pembayaran ganda
AREA: /checkout, /cart, /payment/callback
DURASI: 45 menit
HEURISTIK: SFDPOT + CRUD + state transition
CATATAN: waktu, langkah, hasil aneh, screenshot, request-id
```

### Heuristik SFDPOT
| Huruf | Fokus |
|---|---|
| **S**tructure | bagian mana saja dari produk/UI/API? field, parameter, header |
| **F**unction | apa yang dilakukan? fitur, perhitungan, alur |
| **D**ata | input: kosong, batas, unicode, besar, duplikat, urutan |
| **P**latform | browser, OS, device, jaringan (2G/offline), locale, timezone |
| **O**perations | pemakaian nyata: cepat, berulang, paralel, salah urutan, ditinggal |
| **T**ime | tanggal lalu/depan, DST, expire, retry, lama menganggur |

### Tur lain yang cepat menemukan bug
- **CRUD**: Create/Read/Update/Delete tiap entitas + kombinasi (hapus lalu baca).
- **State transition**: pending → paid → refund → refund lagi (harus ditolak).
- **Tour fitur**: keliling semua menu, cek yang kosong/tak selesai.
- **Tour data**: masukkan data aneh (emoji, `<script>`, 10 MB, NUL).
- **Tour jaringan**: offline, lambat, putus di tengah submit (data hilang?).
- **Tour interupsi**: refresh saat proses, tombol back, buka 2 tab, sesi kedaluwarsa.
- **Tour akses**: user biasa mencoba URL admin, ganti id, ganti tenant.

## 2. UAT (acceptance) yang jujur
- Kriteria ditulis **sebelum** dikerjakan (Given/When/Then) dan disetujui pemilik produk.
- Uji dengan data & peran nyata, di lingkungan mirip produksi.
- Bukti: checklist per kriteria + screenshot/angka, bukan "sudah dicek".
- Terima hanya bila semua kriteria P1/P2 lulus; P3 boleh jadi backlog tertulis.
```
Diberikan pengguna dengan langganan aktif
Ketika membuka halaman invoice dan menekan "unduh"
Maka PDF terunduh < 3 detik, nomor invoice sesuai, total = subtotal + pajak
```

## 3. Regresi
- Suite regresi = alur P1 + bug lama yang pernah terjadi (tiap bug → 1 test permanen).
- Jalankan pada tiap PR (subset cepat) dan tiap rilis (subset penuh).
- Seleksi berbasis risiko: file yang berubah → modul terkait + dependennya.
- Jangan pernah menghapus test regresi tanpa alasan tertulis.

## 4. Compatibility matrix
| Dimensi | Minimum |
|---|---|
| Browser | Chrome, Safari, Firefox (2 versi terakhir) |
| OS | macOS, Windows, Linux; iOS & Android |
| Layar | 320, 360, 768, 1024, 1440, 1920 |
| Jaringan | 4G, 3G lambat, offline |
| Input | mouse, sentuh, keyboard, screen reader, zoom 200% |
| Data | baru, kosong, sangat banyak, impor/impor ulang |

## 5. Bug report & triase
- Format wajib: lihat `00-prinsip.md` §6.
- Prioritas: P1 data/uang/keamanan atau layanan mati · P2 fitur utama rusak ·
  P3 gangguan · P4 kosmetik.
- Satu bug satu laporan; sertakan bukti yang bisa direproduksi orang lain.
- Jangan menutup bug karena "tidak bisa direproduksi" tanpa menambah log/instrumentasi.

## 6. Definition of Done manual
- [ ] Charter/checklist tertulis dan hasilnya dicatat (bukan di kepala).
- [ ] Setiap bug punya langkah reproduksi + bukti + prioritas.
- [ ] UAT: kriteria lulus dengan bukti per kriteria.
- [ ] Bug yang ditemukan menghasilkan test otomatis (regresi permanen).
