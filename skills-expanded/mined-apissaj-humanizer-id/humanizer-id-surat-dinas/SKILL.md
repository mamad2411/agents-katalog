---
name: humanizer-id-surat-dinas
description: Use when auditing or editing Indonesian official letters, government memos, institutional circulars, official notices, or formal MC/protocol scripts.
version: 2.5.0
author: Hafizh Muzani / Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [writing, editing, bahasa-indonesia, surat-dinas, birokrasi, pewara]
    category: creative
    homepage: https://github.com/apissaj/humanizer-id
    parent: humanizer-id
---

# Humanizer ID — Surat Dinas, Birokrasi & Pewara

Sub-kaidah domain Humanizer ID untuk surat dinas, nota dinas, surat edaran, surat keputusan, undangan resmi, serta naskah pewara/protokol (*Tata Naskah Dinas* 2025, Karenisa dkk.; *Bahasa Indonesia untuk Pejabat Pemerintah*, Mullyana 2019; *Surat-Menyurat*, Pusat Bahasa 1991; *Bahasa Indonesia untuk Pewara*, Kurniawan 2019). Muat berkas ini setelah `humanizer-id` (induk) dengan `--preset dinas`.

---

### A. Alamat, Salam Pembuka & Alinea Pembuka Surat Dinas (TND 2025; Pusat Bahasa 1991)

1. **Pola:** `Kepada Yth. Bapak Kepala Dinas...` atau `Yth. Bapak/Ibu Direktur...` → **Perbaikan:** `Yth. Kepala Dinas...` atau `Yth. Direktur...` (tanpa *Kepada*, tanpa sapaan *Bapak/Ibu* jika langsung diikuti nama jabatan) — **Sebab:** *Kepada* bermakna tujuan yang bertumpuk dengan *Yth.*, sedangkan nama jabatan tidak disapa dengan *Bapak/Ibu* (`SMD-001`, `DIN-005`).
2. **Pola:** `Dengan Hormat,` (H kapital) atau `Dengan hormat.` (titik) → **Perbaikan:** `Dengan hormat,` (`h` kecil, diakhiri koma) — **Sebab:** salam pembuka bukan judul dan diikuti koma sebelum isi surat (`SMD-003`).
3. **Pola:** alinea pembuka berpola non-verba / klise birokratis (*Bersama ini kami sampaikan...*, *Sehubungan dengan surat Saudara nomor..., maka dengan ini kami beritahukan bahwa...*) → **Perbaikan:** gunakan *Dengan ini kami sampaikan...* (tanpa lampiran) atau *Bersama surat ini kami lampirkan...* (bila ada lampiran), serta hapus *maka* pada kalimat bertingkat (`DIN-001`, `DIN-010`, `SPK-001`).
4. **Pola:** kepala surat dinas memakai `Perihal:`, `Lampiran: -` atau `Lampiran: 5 (lima) lembar`, dan `Nomor: .../2018.-` → **Perbaikan:** gunakan `Hal:`, hapus baris `Lampiran` bila kosong (atau tulis `Lampiran: Lima lembar`), dan tulis `Nomor` tanpa titik/hubung akhir (`DIN-011`..`DIN-014`, Sriyanto 2018, hlm. 52–53).

---

### B. Kelugasan Isi, Pasif Diri & Penutup Surat (TND 2025; Mullyana 2019)

1. **Pola:** bentuk pasif diri disisipi unsur lain (*Surat tersebut kami telah terima*, *Usulan ini Bapak harus setujui*) → **Perbaikan:** rapatkan pelaku tepat di depan verba dasar (*Surat tersebut telah kami terima*, *Usulan ini harus Bapak setujui*) — **Sebab:** pada konstruksi pasif pronomina persona (`DIN-002`), aspek/modalitas wajib mendahului pronomina pelaku.
2. **Pola:** sufiks `-nya` rancu pada kalimat penutup (*Atas perhatiannya, kami ucapkan terima kasih*, *Atas kehadirannya, kami sampaikan terima kasih*) → **Perbaikan:** ganti `-nya` dengan sapaan resmi penerima surat (*Atas perhatian Bapak/Ibu, kami ucapkan terima kasih*, *Atas kehadiran Saudara, kami sampaikan terima kasih*) — **Sebab:** `-nya` merujuk persona ketiga yang tidak jelas alamatnya (`DIN-003`).
3. **Pola:** penutup berlebih (*Demikian surat ini kami sampaikan, atas perhatian dan kerja samanya yang baik kami haturkan banyak-banyak terima kasih*) → **Perbaikan:** *Demikian informasi ini kami sampaikan. Atas perhatian Bapak/Ibu, kami ucapkan terima kasih.* — **Sebab:** bahasa dinas menuntut kesantunan yang ringkas, lugas, dan bebas pleonasme (`DIN-004`).

---

### C. Format Penandatanganan, Jabatan & Protokol Pewara (TND 2025; Kurniawan 2019)

1. **Pola:** `NIP.` (pakai titik), `a/n`, `An.`, `Plt:` atau garis bawah nama pejabat yang tidak konsisten → **Perbaikan:** `NIP 198501012010011001` (tanpa titik setelah NIP, tanpa spasi antar-blok jika mengikuti standar kepegawaian atau konsisten format instansi), `a.n.` (atas nama, huruf kecil dengan dua titik), `u.b.` (untuk beliau), `Plt.` (Pelaksana Tugas) — **Sebab:** singkatan resmi tata naskah dinas dibakukan secara ketat (`DIN-006`, `DIN-007`).
2. **Pola:** frasa pewara tidak bernalar (*Waktu dan tempat kami persilakan*, *Untuk menyingkat waktu*, *Hadirin sekalian yang berbahagia*, *Dimohon berdiri* tanpa subjek jelas) → **Perbaikan:** *Kepada Bapak/Ibu [Nama], kami persilakan*, *Untuk menghemat waktu*, *Hadirin yang berbahagia*, *Hadirin dimohon berdiri* — **Sebab:** yang dipersilakan adalah orang/pembicara bukan *waktu dan tempat*, waktu dihemat bukan disingkat, dan *hadirin* sudah bermakna jamak (`PWR-001`, `PWR-002`, `PLE-001`).

```bash
# Audit surat dinas atau naskah resmi instansi
python scripts/audit.py surat-dinas.md --preset dinas --report
```
