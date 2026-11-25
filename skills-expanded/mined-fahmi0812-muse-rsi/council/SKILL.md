---
name: council
description: Blind multi-model council — three judges from three providers decide high-stakes calls.
---

# council

Skill orisinal `muse-rsi`. Bukan salinan skill upstream.

## Tujuan

Satu model bisa salah dengan percaya diri. Tiga model dari tiga provider
yang berbeda, menilai secara buta dan independen, jauh lebih sulit
dibohongi oleh satu sudut pandang. Skill ini dipakai untuk keputusan
yang mahal kalau salah — bukan untuk tugas rutin.

Model dan harga ada di `config/MODELS.yaml` (bagian `council`).
Tidak ada panggilan berbayar tanpa kunci provider yang sudah disiapkan
Fahmi — kalau kuncinya tidak ada, council tidak jalan, dan keputusan
naik ke Fahmi.

## Kapan dipakai

- Keputusan berisiko tinggi: hapus/publish/merge, belanja, kirim ke orang lain.
- Router ragu: dua domain teratas hampir sama skornya (lihat "Test-time
  compute" di [router](router/SKILL.md)).
- Sengketa eval: dua run memberi jawaban berbeda, atau satu klaim
  dipertanyakan.
- **Jangan** dipakai untuk tugas rutin, penulisan biasa, atau apa pun
  yang satu model murah sudah bisa jawab dengan benar.

## Cara kerja

### 1. Tetapkan tiga kursi — lalu kunci

Tiga juri, tiga provider berbeda, dari `config/MODELS.yaml`:

- Anthropic — `claude-opus-5-5`
- OpenAI — `gpt-6.1-sol`
- Google — `gemini-3-pro-preview`

**Aturan anti-substitusi:** kursi yang sudah ditetapkan tidak boleh
diganti diam-diam dengan model provider lain di tengah jalan. Kalau
satu kursi tidak tersedia (kunci tidak ada, provider down, model
pensiun), council **tidak jalan**. Keputusan naik ke Fahmi. Mengganti
juri tanpa mencatatnya adalah pelanggaran protokol — hasilnya tidak
boleh dipakai.

### 2. Putusan independen dulu, diskusi belakangan

- Ketiga juri menerima **pertanyaan yang sama persis**, tanpa tahu
  siapa juri lain dan tanpa melihat draf jawaban satu sama lain.
- Setiap juri menulis putusannya sendiri: setuju / tidak setuju /
  tidak bisa diputuskan, plus 1–3 kalimat alasan dan bukti yang
  dirujuk.
- **Dilarang** membocorkan draf satu juri ke juri lain sebelum semua
  putusan masuk. Juri kedua tidak boleh "melanjutkan" jawaban juri
  pertama.

### 3. Rekam verbatim, baru sintesis

- Semua putusan direkam kata per kata, lengkap dengan nama model
  dan provider.
- Sintesis hanya dibuat **setelah** ketiga putusan masuk.
- Kalau ada juri yang berubah pikiran setelah melihat putusan lain,
  perubahan itu dicatat sebagai revisi — putusan aslinya tetap
  tersimpan, tidak ditimpa.

### 4. Kuorum dan jalan buntu

- Kuorum: **2 dari 3** untuk satu arah yang sama.
- 2–1: mayoritas menang, suara minoritas dicatat sebagai dissent
  (lihat format keluaran).
- 1–1–1 atau 0 putusan yang bisa dipakai: **jalan buntu — naik ke
  Fahmi**. Jangan memaksakan sintesis dari putusan yang tidak
  nyambung.
- Council tidak pernah mengesampingkan aturan repo: $0 cap, larangan
  trading live, larangan kirim tanpa persetujuan, dan guardrail
  kesehatan tetap berlaku apa pun kata mayoritas.

## Format keluaran

```text
Keputusan: [sesuai mayoritas / BUNTU — naik ke Fahmi]
Pertanyaan: [1 kalimat, sama persis untuk ketiga juri]

| Juri | Putusan | Alasan (1 kalimat) |
|---|---|---|
| Anthropic claude-opus-5-5 | Setuju | ... |
| OpenAI gpt-6.1-sol | Setuju | ... |
| Google gemini-3-pro-preview | Tidak setuju | ... |

Dissent: [apa kata suara minoritas, dan kenapa ia mungkin benar]
Bukti yang dirujuk: [file/log/URL, bukan klaim tanpa sumber]
```

## Yang dilarang

- Menjalankan council dengan 1–2 juri dan mengklaim itu "council".
- Menukar juri tanpa mencatatnya di log.
- Membocorkan draf antar-juri sebelum putusan masuk.
- Memakai council untuk membenarkan keputusan yang sudah diambil
  duluan (putusan ditulis setelah hasil diketahui).
- Panggilan berbayar tanpa kunci yang sudah disiapkan Fahmi.
