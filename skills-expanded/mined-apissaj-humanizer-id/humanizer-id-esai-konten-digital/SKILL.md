---
name: humanizer-id-esai-konten-digital
description: Use when editing Indonesian essays, blog posts, newsletters, LinkedIn/social thought leadership, presentation slides, or web/digital content.
version: 2.5.0
author: Hafizh Muzani / Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [writing, editing, bahasa-indonesia, esai, blog, presentasi, konten-digital]
    category: creative
    homepage: https://github.com/apissaj/humanizer-id
    parent: humanizer-id
---

# Humanizer ID — Esai Populer, Blog, Presentasi & Konten Digital

Sub-kaidah domain Humanizer ID untuk esai populer, artikel blog, buletin (*newsletter*), unggahan opini profesional (LinkedIn/Medium), naskah salindia presentasi, dan teks web/media luar ruang (*BPBI 1 Sastra*; *Komunikasi Perusahaan* BRIN 2022; *Buku Saku Istilah Media Luar Ruang* 2015). Muat berkas ini setelah `humanizer-id` (induk) dengan **Mode Esai & Opini Populer**.

---

### A. Pembersihan Klise Blog & Unggahan AI (`RET-001`..`006`, `KLK-003`..`005`)

1. **Pola:** pembuka generik (*Di era digital yang berkembang pesat saat ini...*, *Pertanyaannya sederhana.*, *Bukan rahasia lagi bahwa...*) dan ajakan klise (*Mari kita menyelami lebih dalam...*) → **Perbaikan:** buka langsung dengan pengamatan konkret, adegan singkat, data spesifik, atau pertanyaan tajam yang benar-benar memicu rasa ingin tahu (`RET-002`, `KLK-003`).
2. **Pola:** pujian hampa dan penyangkalan antisipatif (*memegang peranan yang sangat krusial*, *solusi revolusioner*, *Meskipun sederhana, bukan berarti mudah*, *sangat penting sekali*) → **Perbaikan:** ganti pujian abstrak dengan bukti atau dampak terukur, dan nyatakan batas gagasan secara langsung tanpa membantah hal yang tidak ditanyakan (`RET-001`, `RET-004`, `RET-006`).
3. **Pola:** penutup khotbah/utopis (*Pada akhirnya, perubahan dimulai dari kita semua untuk masa depan yang lebih cerah.*) → **Perbaikan:** tutup dengan satu kesimpulan praktis, refleksi jujur, atau langkah konkret yang bisa dicoba pembaca hari ini (`RET-005`).

---

### B. Suara Penulis, Ritme Kalimat & Batas Ragam Semi-Formal (`RGM-001`..`002`, `VRB-001`..`006`)

1. **Pola:** memaksakan sudut pandang impersonal (*penulis berpendapat...*) pada blog/esai pribadi, atau sebaliknya jatuh ke bahasa tutur nonbaku (*nggak*, *gimana*, *cuman*, *banget*, *nulis*, *nyari*, *ketawa*) pada artikel semi-formal → **Perbaikan:** pertahankan pronomina *saya* atau *kita* yang akrab tetapi tetap menggunakan bentuk baku ringan (*tidak*, *bagaimana*, *hanya*, *sangat*, *menulis*, *mencari*, *tertawa*) — **Sebab:** ragam semi-formal memadukan keakraban suara penulis dengan ketertiban morfologi (`RGM-001`, `RGM-002`).
2. **Pola:** ritme patah-patah (*staccato* satu kalimat per baris terus-menerus ala unggahan AI) atau pola tiga serangkai (*triplet*: *cepat, akurat, dan terpercaya*) di setiap paragraf → **Perbaikan:** padukan kalimat pendek sebagai penegas dengan kalimat sedang-panjang yang mengalir; gunakan daftar tiga butir hanya bila ketiganya memang setara dan diperlukan.
3. **Pola:** verba ringan yang melemahkan daya gerak prosa (*melakukan implementasi*, *memberikan pengaruh*, *membuat keputusan*) → **Perbaikan:** gunakan verba aktif langsung (*menerapkan*, *memengaruhi*, *memutuskan*) agar bacaan terasa hidup (`VRB-001`, `VRB-004`, `VRB-006`).

---

### C. Naskah Presentasi, Copy Web & Media Luar Ruang

1. **Pola:** judul salindia (*slide*) berupa label hampa (*Hasil*, *Latar Belakang*) berisi paragraf penuh 80 kata → **Perbaikan:** ubah judul salindia menjadi simpulan inti (*Waktu muat turun 42% setelah pemangkasan kueri*) dengan maksimal 3–5 butir paralel ringkas berverba aktif.
2. **Pola:** istilah digital mentah pada teks publik/web (*download*, *upload*, *link*, *podcast*, *selfie*, *content creator*, *live streaming*, *online/offline*) → **Perbaikan:** gunakan padanan baku yang sudah akrab di publik (*unduh*, *unggah*, *tautan*, *siniar*, *swafoto*, *kreator konten*, *siaran langsung daring*, *daring/luring*) sesuai `data/glosarium-lintas-bidang.json`.

---

### D. Contoh Selisih Ringkas (*Mini Diff*)

| Draf Blog / Unggahan AI | Hasil Suntingan Natural | Kaidah |
|---|---|---|
| Di era digital yang berkembang pesat saat ini, menulis memegang peranan yang sangat krusial. | Menulis dengan jelas menghemat waktu tim lebih banyak daripada rapat satu jam. | `RET-002`, `RET-006` |
| Meskipun singkat, bukan berarti catatan ini nggak penting banget. | Kendati singkat, catatan ini menjadi acuan utama sebelum rilis. | `RET-001`, `RGM-001` |

```bash
# Audit artikel blog, esai, atau naskah konten digital
python scripts/audit.py esai-blog.md --report
```
