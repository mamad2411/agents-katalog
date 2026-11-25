---
name: humanizer-id-hukum-regulasi
description: Use when auditing or editing Indonesian legal analyses, policy briefs, regulations, or product claims.
version: 2.5.0
author: Hafizh Muzani / Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [writing, editing, bahasa-indonesia, hukum, regulasi]
    category: creative
    homepage: https://github.com/apissaj/humanizer-id
    parent: humanizer-id
---

# Humanizer ID — Hukum & Regulasi

Sub-kaidah domain Humanizer ID untuk analisis hukum, naskah akademik/kajian regulasi, kebijakan publik, draf peraturan, dan klaim produk (*Hukum dalam Teroka Linguistik*, Penerbit BRIN 2023). Muat berkas ini setelah `humanizer-id` (induk).

---

### A. Batas Zona Terlarang & Kepatuhan Kaidah Bahasa (BRIN 2023, hlm. 40–42)

1. **Pola:** menyunting langsung redaksi klausul kontrak, akta, paten, bunyi pasal undang-undang yang sudah sah berlaku, atau transkrip ujaran/BAP bukti linguistik forensik → **Perbaikan:** **DILARANG** mengubah redaksi dokumen hukum mengikat maupun teks bukti forensik secara sepihak; jalankan **Mode AFTER (`--report`)** untuk memberi catatan temuan bernomor saja tanpa mengubah teks asli — **Sebab:** pengubahan diksi klausul membuka celah sengketa dan merusak keabsahan bukti peradilan (`SKILL.md` Seksi 1.A; `HKT-017`, Juknis KKLP Pembinaan dan Bahasa Hukum 2022, hlm. 19–20).
2. **Pola:** menganggap bahasa hukum bebas dari kaidah EYD V dan KBBI (*kosmetika*, *obyektif*, *praktek*) → **Perbaikan:** *kosmetik* (nomina/adjektiva baku), *objektif*, *praktik* — **Sebab:** bahasa hukum tetap wajib mematuhi kaidah pembentukan kata, ejaan, dan struktur kalimat bahasa Indonesia baku (`HKT-015`, `HKT-016`, hlm. 41–42).

---

### B. Anti-Multimakna, Pasif Normatif & Struktur Pasal (BRIN 2023, hlm. 43, 60–74)

1. **Pola:** kalimat norma/definisi bermakna ganda, konjungsi ganda (*Jika ... maka ...*, *Karena ... maka ...*, *Meskipun ... tetapi/namun ...*), atau pleonasme rujukan (*sebagaimana tersebut di atas*, *para pihak-pihak*) → **Perbaikan:** pecah syarat dan akibat secara tegas, hapus salah satu konjungsi (*Jika X, Y*; *Meskipun X, Y*), dan ringkas rujukan (*tersebut* / *di atas*, *para pihak*) (`SPK-007`, `SPK-008`, `SPK-010`, `UIN-003`, `UIN-004`, `DIN-004`, hlm. 65–67, 74) — **Sebab:** bahasa hukum tidak boleh mengandung multimakna karena menimbulkan ketidakpastian hukum (hlm. 60).
2. **Pola:** mengubah kalimat pasif normatif pasal (*Pemilik nomor notifikasi dikenai sanksi administratif*) dengan alasan "kekurangan objek" → **Perbaikan:** pertahankan struktur `S – P(pasif) – Pel` — **Sebab:** konstituen di sebelah kanan predikat pasif pasal adalah **pelengkap** yang sah secara gramatikal (hlm. 42–43, 63).
3. **Pola:** menyamakan atau membalik urutan frasa istilah hukum berpola DM (*penghinaan ringan*, *pemberitaan palsu*) dan MD (*palsu persangkaan*), atau mengganti kata kerja hipotesis *meng-* (*menyerang*, *menuduhkan*) dalam rumusan pasal → **Perbaikan:** pertahankan urutan inti-penjelas asli dan makna hipotesis *meng-* ('dugaan perbuatan sebelum putusan tetap') — **Sebab:** perubahan struktur istilah KUHP mengubah tafsir unsur delik (hlm. 69–73).
4. **Pola:** kalimat kajian hukum berjela-jela (kalimat majemuk bertingkat >3 klausa, inversi berlapis, pengulangan kata berlebih) → **Perbaikan:** sederhanakan struktur kalimat kajian agar terbaca jelas oleh sasaran publik tanpa menghilangkan presisi norma (hlm. 15–17, 34, 202).

---

### C. Diksi Klaim Produk Realistis & Padanan Hukum Baku (BRIN 2023, hlm. 46, 51–53, 209–213)

1. **Pola:** klaim mutlak atau melampaui batas kategori regulasi (*membunuh kuman 100%*, *menghilangkan ketombe secara permanen*, *menghilangkan kerutan* pada kosmetik) → **Perbaikan:** gunakan verba proses realistis yang sesuai kategori (*melawan kuman*, *membantu mengurangi ketombe*, *mengurangi munculnya kerutan*, *merawat*, *melindungi*) — **Sebab:** perbedaan klausa (*mengurangi* vs *mengurangi munculnya*) menentukan batas hukum obat vs kosmetik serta kebenaran klaim (`HKT-012`, hlm. 46, 51–53).
2. **Padanan istilah hukum baku (`data/glosarium-lintas-bidang.json`):**
   - *legal standing* → **kedudukan hukum**
   - *force majeure* → **keadaan kahar**
   - *dissenting opinion* / *concurring opinion* → **pendapat berbeda** / **pendapat searah**
   - *pro bono* → **bantuan hukum cuma-cuma**
   - *due diligence* → **uji tuntas**
   - *compliance* → **kepatuhan**
   - *non-disclosure agreement (NDA)* → **perjanjian kerahasiaan informasi**
   - *dispute settlement* → **penyelesaian sengketa**
   - *addendum* → **adendum / lampiran tambahan**; *affidavit* → **afidavit / surat pernyataan bersumpah**; *amicus curiae* → **sahabat pengadilan**; *bailout* → **dana talangan**; *class action* → **gugatan perwakilan kelompok**
   - *disclaimer* → **sangkalan / pernyataan pelepasan tanggung jawab**; *injunction* → **putusan sela / perintah larangan pengadilan**; *jurisprudence* → **yurisprudensi**; *power of attorney* → **surat kuasa**; *whistleblower* → **pelapor pelanggaran**
   - *cybercrime* → **kejahatan dunia maya**; *omnibus law* → **undang-undang sapu jagad** (hlm. 58, 211–213).

---

### D. Checklist Audit Mode AFTER Naskah Hukum & Regulasi

- [ ] Apakah naskah berupa kontrak/akta/pasal mengikat? Bila ya, **hanya lapor (`--report`)**, jangan ubah teks asli.
- [ ] Tidak ada konjungsi ganda (`Jika ... maka ...`, `Meskipun ... namun ...`) atau rujukan pleonastis (`sebagaimana tersebut di atas`).
- [ ] Pasif normatif (`S – P(pasif) – Pel`) dan urutan istilah DM/MD pada rumusan delik tetap utuh.
- [ ] Istilah hukum asing dipadankan dengan 20 entri `hukum_dan_regulasi` di `data/glosarium-lintas-bidang.json` (kecuali kutipan langsung).

```bash
# Audit kajian/draf regulasi tanpa mengubah teks asli (Mode AFTER)
python scripts/audit.py naskah-hukum.md --report
```
