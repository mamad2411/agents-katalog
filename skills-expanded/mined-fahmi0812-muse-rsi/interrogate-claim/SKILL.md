---
name: interrogate-claim
description: Adversarial interrogation — stress-test a claim, artifact, or plan before trusting it.
---

# interrogate-claim

Skill orisinal `muse-rsi`. Bukan salinan skill upstream.

## Tujuan

Klaim yang tidak pernah diserang akan terasa benar padahal belum
terbukti. Skill ini menyerang klaim, artefak, atau rencana dengan
pertanyaan yang dirancang untuk membunuhnya — sebelum Fahmi
memercayainya.

## Kapan dipakai

- Router tidak menemukan skill yang cocok (`NO_MATCH`) atau skor
  tertingginya lemah — sebelum menebak, interogasi dulu permintaannya
  (lihat "Test-time compute" di [router](router/SKILL.md)).
- Seseorang (termasuk agen sendiri) mengklaim "sudah selesai",
  "sudah dicek", atau "pasti benar" tanpa bukti yang bisa dibuka.
- Rencana besar sebelum dieksekusi: migrasi, publish, hapus data.
- **Jangan** dipakai untuk menyerang orang. Targetnya selalu klaim,
  artefak, atau rencana — bukan siapa yang membuatnya.

## Langkah kerja

### 1. Tulis klaimnya dalam 1 kalimat

Kalau klaimnya tidak bisa ditulis dalam 1 kalimat, klaim itu belum
jelas — minta diperjelas dulu, jangan lanjut.

Contoh: "Eval routing lolos 130/130 setelah registry berubah."

### 2. Minta buktinya — yang bisa dibuka

- Bukti harus berupa file, log, URL, atau perintah yang bisa
  dijalankan ulang. "Saya sudah cek" bukan bukti.
- Kalau buktinya tidak bisa dibuka (file tidak ada, link mati,
  log tidak tersimpan) → putusan langsung **unproven**, berhenti
  di sini.

### 3. Cari contoh yang membunuh klaim

- Satu contoh tandingan yang nyata sudah cukup untuk menggugurkan
  klaim umum ("semua X adalah Y").
- Tanya: input apa yang membuat ini gagal? Kasus pinggir apa yang
  belum dicoba? Asumsi apa yang disembunyikan?

### 4. Cari tes termurah yang bisa membunuhnya

- Tes yang paling murah dan paling mematikan jalan dulu, bukan
  yang paling nyaman.
- Contoh: jalankan ulang eval-nya (1 perintah), buka file hasil di
  disk, hitung ulang angkanya dari sumber.
- Kalau tes itu lolos → klaim naik tingkat. Kalau gagal → klaim
  gugur, catat kenapa.

### 5. Putuskan — dengan bar bukti yang jelas

| Putusan | Bar bukti |
|---|---|
| **confirmed** | Bukti bisa dibuka + tes termurah yang mematikan sudah dijalankan dan lolos + tidak ada contoh tandingan yang diketahui. |
| **plausible** | Bukti bisa dibuka, tapi tes yang mematikan belum dijalankan, atau ada asumsi yang belum diperiksa. |
| **unproven** | Tidak ada bukti yang bisa dibuka, atau klaimnya tidak bisa ditulis dalam 1 kalimat. |
| **refuted** | Ada contoh tandingan yang nyata, atau tes yang mematikan gagal. |

## Aturan berhenti

- 3 pertanyaan tanpa jawaban yang bisa diperiksa → berhenti,
  putusan **unproven**. Jangan mengarang jawaban supaya sesi
  selesai.
- 1 contoh tandingan yang nyata → berhenti, putusan **refuted**.
  Tidak perlu 10 contoh.
- Kalau yang diinterogasi adalah permintaan Fahmi sendiri dan
  jawabannya tetap kabur setelah 1 pertanyaan klarifikasi →
  berhenti dan tanyakan langsung ke Fahmi, jangan menebak.

## Format keluaran

```text
Klaim: [1 kalimat]
Putusan: [confirmed / plausible / unproven / refuted]
Bukti yang dibuka: [file/log/URL/perintah — atau "tidak ada"]
Contoh tandingan: [ada/tidak ada — kalau ada, tulis persis]
Tes termurah yang dijalankan: [perintah + hasil]
Yang masih belum diperiksa: [asumsi/tes yang tersisa]
```

## Yang dilarang

- Mengubah putusan `refuted` menjadi `plausible` supaya enak dibaca.
- Mengklaim `confirmed` dari bukti yang tidak bisa dibuka.
- Menginterogasi orang, bukan klaimnya.
- Menjalankan tes berbayar atau merusak sebagai "tes termurah".
