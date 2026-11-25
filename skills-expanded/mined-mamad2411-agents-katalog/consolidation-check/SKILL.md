---
name: consolidation-check
description: Wajib dipakai di SEMUA tugas yang menulis atau mengubah kode di proyek ini, dan WAJIB lagi setelah fitur selesai. Sebelum menulis kode, cari dulu pemilik nilai yang sudah ada (status, label, enum, konstanta, aturan) dan jangan pernah membuat salinan kedua. Kalau memang harus membuat, buat SATU pemilik lalu paksa semua pemakai lewatnya. Semua klaim diverifikasi dengan pengukuran, bukan penalaran. Duplikasi diukur dengan "berapa banyak tempat harus sepakat", bukan jumlah baris. Gunakan saat menambah fitur, menambah daftar/label/status, diminta simplify/clean up/remove duplication, me-review, atau membuka PR baru.
---

# Consolidation Check

Kode proyek ini sederhana. Yang mahal adalah **difficult to change safely** — dan itu
disebabkan oleh satu pola yang berulang, bukan oleh file yang rumit.

Pola itu: setiap fitur adalah **delta**. Delta yang benar tidak memberi tahu apakah
objek yang diedit sudah salah sejak sebelumnya. Bukti langsung dari repo ini:

| Tanggal | Commit | Apa yang terjadi |
|---|---|---|
| 2026-08-30 | `23802a3` | Skema dibuat dengan 5 status, termasuk `cancelled_by_user` |
| 2026-09-13 | `727108b` | Fitur dashboard menulis peta status — **salah ketik**: `'cancelled'` |
| 2026-09-25 | `77808b6` | Fitur auto-cancel **benar** menambahkan `cancelled_by_system` ke peta itu |
| 2026-09-25 | `43239f9` | Fitur auto-reject **benar** menambahkan `rejected_by_system` ke peta itu |

Dua penulis berbeda, tiga minggu berselang, keduanya teliti. Tidak ada yang punya alasan
untuk curiga peta itu sudah rusak. Bug-nya bertahan di `main` selama **dua tahun**.

Tiga skill proyek lain sudah mengatur *bagaimana* bekerja. Skill ini mengatur **apa yang
harus diperiksa sebelum dan sesudah** — owner's check dan anti-duplication gate.

---

## 1. Setelah fitur selesai — cek masuk ulang (WAJIB)

Ini bagian yang paling sering terlewat dan paling mahal. Setelah sebuah fitur menyentuh
daftar/label/status, **hitung ulang** berapa banyak tempat harus sepakat:

```bash
# Skop: file yang baru saja berubah
git diff --name-only origin/dev

# Untuk setiap nilai domain yang disentuh, hitung ulang penyebutnya
grep -rn "cancelled_by_"    app resources | wc -l
grep -rn "ruang_kelas"      app resources | wc -l
grep -rn "rejected_by_system" app resources | wc -l
```

Bandingkan dengan angka sebelum fitur. Kalau **naik**, fitur itu menambah duplikasi —
sebutkan ke user, jangan diamkan.

> Dari PR #93: 11 file → 8 file, 54 penyebut → 43. Angka itu terlihat jelas hanya
> karena diukur sebelum dan sesudah.

---

## 2. Sebelum menulis — cari pemilik yang sudah ada

```bash
grep -rn "const \|::LABELS\|::CATEGORIES\|::ORDERED" app/Models/
```

Kalau daftarnya sudah ada di `app/Models/`, **pakai**. Jangan tulis ulang di controller
atau view. Kalau memang harus membuat, buat **satu** pemilik di `app/Models/` atau
`app/Services/`, lalu paksa semua pemakai lewatnya.

**Membangun pemilik saja tidak cukup.** `app/Services/ReservationAvailability.php` sudah
ada dan benar, tapi 14 string di blade tetap menulis `07.00–20.00` dan `26 slot` secara
literal, `RecapService.php:39` menulis `13` sendiri, dan `reservation-form.js:87`
menghitung `count * 0.5`. Pemiliknya ada; **jalur lain juga masih ada**. Dua jalur
berarti keduanya dipakai.

> Deletion test: kalau modul ini dihapus, kompleksitas **terkumpul** di satu tempat
> (bagus) atau **berpindah** ke N pemanggil (jelek, jangan buat).

---

## 3. Verifikasi klaim dengan pengukuran, bukan penalaran

Empat klaim salah yang pernah keluar dari agen di repo ini. Semuanya terdengar meyakinkan:

| Klaim | Kenyataan | Cara membuktikannya |
|---|---|---|
| "`publicScheduleSlots()` dead code" | Dipakai di `FacilityController.php:124` | grep **recursive**; `**` di PowerShell bukan rekursif |
| "Ini net deletion" | Produksi **+81 baris** | `git diff --shortstat`, hitung sendiri |
| "Ada bug timezone di `now()->addHour()`" | `date_default_timezone` = `Asia/Jakarta`; kedua ekspresi **identik** | `php -r "echo date_default_timezone_get();"` lalu bandingkan |
| "Header keamanan hilang di respons error" | **Hanya di `local`/`testing`**, itu memang benar | `assertOk()` + cek header di dalam test, bukan penalaran soal middleware |

Aturan keras:

- **Klaim soal kode harus berasal dari output tool.** Kalau tidak bisa diukur, jangan
  menyatakan sebagai fakta.
- **Output sub-agent adalah petunjuk, bukan temuan.** Verifikasi ulang yang menentukan
  arah keputusan. Di audit terakhir, 1 dari 4 klaim "tinggi" ternyata salah.
- **Default framework adalah asumsi.** `SessionGuard::$rememberDuration` =
  576000 menit selama `config/auth.php` tidak menyetel `remember` — konfirmasi, jangan menebak.
- Angka tidak pernah disalin dari output sub-agent ke laporan. Hitung ulang sendiri.

---

## 4. Dua mode verifikasi — jangan tertukar

| Mode | Kapan | Metode |
|---|---|---|
| **Bug fix** | Perilaku sengaja berubah | Tulis test lebih dulu, **tunjukkan bahwa ia gagal** dengan pesan error asli, baru perbaiki. Test yang hijau di kode yang rusak tidak berguna |
| **Refactor** | Perilaku tidak boleh berubah | Snapshot HTML sebelum/sesudah, lalu diff. Kalau harness-nya belum deterministik, **buktikan dulu** (2× run + 1× setelah full suite) |

Harness byte-diff pernah **tidak deterministik** di repo ini: id auto-increment pada
database MySQL test menggeser antar-run, jadi semua file "berbeda" padahal kode sama.
Semua primary key harus di-pin dan nol factory (yang isinya random). Kalau tidak, diff-nya
bohong.

---

## 5. Kompleksitas = berapa banyak tempat harus sepakat

Bukan jumlah baris. Baris **bertambah** saat duplikasi dipindahkan ke satu pemilik — itu
perdagangan yang benar.

Laporan yang jujur memuat angka yang baru diukur:

```
Files yang harus sepakat:  11 → 8
Total penyebut:            54 → 43
Produksi:                  +81 / -120 baris
```

Kalau tabelnya tidak bisa diisi dengan angka yang **baru saja diukur**, jangan meyakinkan
bahwa refactor itu berhasil.

---

## 6. Gerbang anti-duplikasi (yang paling murah)

Kelas bug di repo ini bertahan karena **tidak ada yang gagal** saat duplikasi kembali
masuk:

- `HomeController::ajaxFacilities` balas 500 selama berbulan-bulan karena **tidak ada
  test** yang menyentuh endpoint yang dipanggil `app.js` dua kali
- `dashboard/index.blade.php` menampilkan `Cancelled_by_user` karena test hanya pernah
  membuat status `pending` dan `approved`
- `RecapService` salah menghitung hari karena `occupancy_rate` punya **nol asersi** di
  seluruh repo

Untuk setiap nilai domain baru: **satu test yang gagal kalau salinannya muncul lagi.**
Itu lebih murah daripada review.

---

## 7. Aturan keras

- Satu nilai domain, satu pemilik. Jangan tambah yang kedua.
- Perubahan aturan bisnis harus punya test. Kalau tidak bisa diuji, laporkan sebagai
  gap — jangan dianggap selesai.
- Jangan menyelesaikan dengan "sudah dirapikan" tanpa angka.
- Jangan menambah abstraksi yang belum punya **dua** pemanggil. Satu = hipotesis, dua = nyata.
- Kalau tidak yakin, tanya. Jangan menebak lalu yakin.
- Semua branch/commit/push/PR mengikuti `git-conventions`: branch baru, conventional
  commit bahasa Inggris, persetujuan user sebelum push.
