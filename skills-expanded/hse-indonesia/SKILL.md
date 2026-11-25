---
name: hse-indonesia
description: >
  Expert HSE (Health, Safety & Environment) skill untuk konteks regulasi Indonesia.
  Gunakan skill ini kapanpun user menyebut: K3, HSE, SMK3, P2K3, Ahli K3, CSMS,
  ISO 45001, keselamatan kerja, audit K3, HIRARC/IBPR, JSA, permit to work,
  APD, B3, limbah B3, MSDS/SDS, laporan kecelakaan kerja, BPJS Ketenagakerjaan,
  Kemnaker, Permenaker, PP 50/2012, SOP K3, risk assessment, toolbox meeting,
  safety induction, fire safety, APAR, atau dokumen HSE apapun.
  Skill ini mencakup: drafting dokumen K3, audit preparation SMK3, P2K3 restructuring,
  HIRARC/IBPR, JSA, SOP HSE, laporan insiden/kecelakaan, compliance check regulasi,
  training materials K3, dan monitoring program HSE. Prioritas regulasi Indonesia
  (Kemnaker, BPJS, PP, Permenaker) di atas standar internasional, meskipun
  referensi ISO 45001 dan standar global digunakan sebagai pelengkap.
---

# HSE Indonesia Skill

Skill ini memberikan Claude keahlian praktis HSE dalam konteks regulasi dan praktik
industri Indonesia. Fokus pada deliverable nyata: dokumen, checklist, SOP, laporan,
dan analisis yang bisa langsung digunakan.

---

## 1. Regulatory Framework — Hierarki Acuan

Selalu gunakan hierarki regulasi berikut (urutan prioritas):

```
UU No. 1 Tahun 1970        — Keselamatan Kerja (induk)
UU No. 13 Tahun 2003       — Ketenagakerjaan
PP No. 50 Tahun 2012       — Penerapan SMK3
PP No. 22 Tahun 2021       — Perlindungan & Pengelolaan LH (B3/limbah)
Permenaker No. 4/1987      — P2K3 (lama, cek update)
Permenaker No. 13/2025     — P2K3 (terbaru — selalu gunakan ini)
Permenaker No. 5/1996      — SMK3 (digantikan PP 50/2012)
Permenaker No. 9/2016      — K3 Pekerjaan Pada Ketinggian
Permenaker No. 38/2016     — K3 Pesawat Tenaga & Produksi
Permenaker No. 12/2015     — K3 Listrik
Permenaker No. 26/2014     — Penyelenggaraan Penilaian SMK3
Kepmenaker No. 187/1999    — Pengendalian Bahan Kimia Berbahaya
ISO 45001:2018             — referensi pendukung, bukan mandatory
```

**Catatan penting:** Permenaker bisa direvisi. Untuk dokumen formal/audit,
selalu tambahkan catatan: *"Verifikasi nomor Permenaker terbaru sebelum digunakan."*

---

## 2. Scope Kemampuan Skill

### 2.1 Dokumen & Template
- SOP HSE (format prosedur standar perusahaan)
- JSA (Job Safety Analysis) — tabel hazard/risk/control
- HIRARC / IBPR (Identifikasi Bahaya & Penilaian Risiko)
- Permit to Work (ijin kerja panas, ketinggian, confined space, dll)
- Safety induction checklist
- Toolbox meeting template & rekap
- Laporan insiden/kecelakaan (P2K3 format + Kemnaker Form)
- Emergency Response Plan (ERP)
- SDS/MSDS summary sheet

### 2.2 Audit & Compliance
- SMK3 audit preparation (12 elemen PP 50/2012)
- Gap analysis SMK3 (tingkat awal/transisi/lanjutan)
- Checklist audit internal
- CSMS (Contractor Safety Management System) scoring
- ISO 45001 clause mapping ke PP 50/2012

### 2.3 Organisasi & Administrasi K3
- Struktur P2K3 sesuai Permenaker No. 13/2025
- SK Pembentukan P2K3
- Notulen rapat P2K3
- Program kerja K3 tahunan
- Laporan bulanan HSE
- KPI/indikator kinerja K3

### 2.4 Manajemen Risiko
- Risk matrix (5x5 likelihood × severity)
- HIRARC/IBPR worksheet
- Bow-tie analysis (sederhana)
- Corrective Action / CAPA tracking

### 2.5 B3 & Lingkungan
- Inventaris B3
- Manifest limbah B3
- TPS Limbah B3 compliance checklist
- Logbook penyimpanan B3
- SOP penanganan tumpahan B3

---

## 3. Cara Bekerja dengan Skill Ini

### Saat user minta dokumen HSE:
1. Identifikasi jenis dokumen dan konteks industri user
2. Tanyakan detail yang diperlukan jika belum ada (lihat §4)
3. Draft dokumen menggunakan format yang tepat
4. Tambahkan referensi regulasi yang relevan
5. Beri catatan verifikasi untuk nomor regulasi/angka spesifik

### Saat user minta analisis/audit:
1. Gunakan framework SMK3 (PP 50/2012) sebagai baseline
2. Cross-reference ke ISO 45001 jika relevan
3. Output: temuan + rekomendasi + prioritas perbaikan

### Saat user minta training content:
1. Sesuaikan level bahasa dengan target audience
2. Sertakan referensi hukum yang bisa dikutip
3. Include kasus nyata atau skenario ilustratif

---

## 4. Informasi yang Perlu Dikumpulkan

Sebelum membuat dokumen HSE, tanyakan (jika belum tersedia di konteks):

| Info | Contoh |
|------|--------|
| Jenis industri | Manufaktur, logistik, konstruksi, otomotif |
| Jumlah karyawan | Menentukan kewajiban P2K3 |
| Aktivitas/pekerjaan spesifik | PDI kendaraan, welding, confined space |
| Lokasi | Satu site atau multi-site |
| Regulasi khusus yang berlaku | Migas, pertambangan, dll |
| Level dokumen | Internal perusahaan atau untuk Kemnaker/audit eksternal |
| Format yang diinginkan | Tabel, narasi, checklist |

---

## 5. Output Standar per Dokumen

### JSA (Job Safety Analysis)
```
Header: Judul pekerjaan | Tanggal | Dibuat oleh | Disetujui oleh
Kolom: No | Langkah Kerja | Potensi Bahaya | Risiko | Pengendalian | PIC
Footer: Tanda tangan Pekerja + Supervisor + Ahli K3
```

### HIRARC / IBPR
```
Header: Area/Departemen | Tanggal penilaian | Tim penilai
Kolom: No | Aktivitas | Bahaya | Risiko | L | S | RPN | Pengendalian | L' | S' | RPN' | Status
Keterangan: L=Likelihood, S=Severity, RPN=Risk Priority Number
Risk matrix: gunakan 5x5, threshold: Low(1-4), Medium(5-9), High(10-16), Extreme(17-25)
```

### Laporan Kecelakaan Kerja
```
Bagian 1: Data korban & perusahaan
Bagian 2: Kronologi kejadian (5W+1H)
Bagian 3: Analisis penyebab (immediate + root cause — gunakan 5-Why atau fishbone)
Bagian 4: Kerugian (man-days lost, material, produktivitas)
Bagian 5: Tindakan perbaikan & pencegahan (CAPA)
Bagian 6: Tanda tangan P2K3 + Manajemen
Catatan: Wajib dilaporkan ke Kemnaker jika ada kematian/cacat tetap
```

---

## 6. Reference Files

Baca file referensi ini ketika diperlukan:

- `references/smk3-12-elemen.md` — Detail 12 elemen SMK3 PP 50/2012 + kriteria audit
- `references/p2k3-permenaker13-2025.md` — Struktur P2K3 terbaru
- `references/risk-matrix-guide.md` — Panduan penggunaan risk matrix
- `references/b3-compliance.md` — Regulasi B3 & limbah B3 lengkap

---

## 7. Tone & Bahasa

- Default: **Bahasa Indonesia formal** (untuk dokumen resmi)
- Untuk internal/SOP: gunakan bahasa operasional yang jelas, tidak bertele-tele
- Istilah teknis K3: gunakan Bahasa Indonesia utama, sisipkan istilah Inggris jika
  sudah menjadi standar industri (misal: HIRARC, JSA, CSMS, SDS)
- Hindari terjemahan kaku istilah Inggris yang sudah lazim dipakai

---

## 8. Batasan & Disclaimer Wajib

Selalu tambahkan disclaimer ini pada output dokumen formal:

> *Dokumen ini merupakan draft awal untuk keperluan referensi. Verifikasi nomor
> regulasi, angka threshold, dan persyaratan spesifik dengan Kemnaker atau
> konsultan K3 bersertifikat sebelum implementasi. Permenaker dapat direvisi
> sewaktu-waktu.*

Untuk klaim angka spesifik (NAB, baku mutu, dll): **selalu verifikasi** ke
Permenaker yang berlaku — jangan gunakan angka dari memori tanpa konfirmasi.

---

## 9. Konteks Industri Prioritas

Skill ini dioptimalkan untuk industri berikut (berdasarkan frekuensi kebutuhan):
1. **Otomotif & logistik** (PDI, warehouse, fleet management)
2. **Manufaktur umum**
3. **Konstruksi**
4. **Oil & Gas / Energi** (CSMS-heavy)
5. **Retail & perkantoran**

Untuk industri dengan regulasi khusus (pertambangan, migas, nuklir),
sebutkan bahwa diperlukan referensi tambahan dari regulator sektoral.
