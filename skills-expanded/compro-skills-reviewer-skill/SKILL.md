# Reviewer

> **Skill untuk:** Memverifikasi akurasi draf terhadap fakta bisnis, panduan brand, struktur presentasi, dan merumuskan On-Page SEO metadata.

## Tujuan
Memastikan draf company profile berkualitas tinggi, bebas kesalahan faktual, sesuai tone of voice, dan siap dikonversi ke HTML.

## Inputs
- `compros/<slug>/drafts/01-draft.md` (legacy: `artifacts/01-company-profile-draft.md`): Draf draf dari Writer.
- `input/business-knowledge-base.md`: Sumber fakta bisnis.
- `input/business-audit-report.md`: Analisis pasar dan diferensiasi.
- `input/brand-story-guide.md`: Panduan tone of voice dan persona merek.
- `compros/<slug>/reports/selling-points-research.md` *(opsional)*: Laporan research kompetitif — digunakan untuk verifikasi selling points dan zero competitor leak check.

## Outputs
- `compros/<slug>/reports/review-report.md` (legacy: `artifacts/review-report.md`): Laporan evaluasi per kategori dan daftar revisi yang wajib diperbaiki.
- `compros/<slug>/drafts/02-final.md` (legacy: `artifacts/02-company-profile-final.md`): Salinan draf yang telah disetujui (**`APPROVED`**), dilengkapi blok Meta Title & Meta Description di baris awal.

## Checklist Audit Reviewer
1. **Factual Consistency:**
   - Tidak ada angka, nama, harga, atau klaim yang bertentangan dengan `business-knowledge-base.md`.
2. **Brand Voice & Storytelling:**
   - Nada bicara konsisten dengan `brand-story-guide.md`.
   - Alur narasi mengalir logis: Problem -> Solution -> Proof -> Offer -> CTA.
3. **Slide Layout & Capacity:**
   - Setiap slide diawali `# ` (H1).
   - Panjang kata per slide proporsional (85–140 kata). Tidak ada slide yang kepanjangan.
4. **Content SEO & Metadata Formulation:**
   - Judul slide deskriptif dan ramah pencarian.
   - Reviewer menyusun `Meta Title` (maksimal 60 karakter) dan `Meta Description` (150–160 karakter) yang merangkum proposisi nilai perusahaan, disisipkan pada bagian header draf final.
5. **Content Deduplication:**
   - Tidak ada kalimat atau frasa yang diulang verbatim antar elemen pada slide yang sama (tagline ≠ deskripsi, heading ≠ body).
   - Jika repetisi >40% terdeteksi pada slide manapun → REVISION_REQUIRED dengan catatan "Repetisi verbatim pada Slide X: [elemen A] vs [elemen B]".
6. **Contact Information Factual Check:**
   - Semua informasi kontak (nomor telepon, email, website, alamat, nama PIC) WAJIB bersumber langsung dari `business-knowledge-base.md`.
   - Cross-check setiap item kontak di Slide CTA/Contact terhadap data kontak di input docs.
   - Jika input docs TIDAK menyediakan kontak tertentu:
     - Gunakan placeholder eksplisit: `[Nomor WhatsApp]`, `[Email Resmi]`, `[Alamat Kantor]`
     - Tandai di review report: "Kontak X belum tersedia di input docs — menggunakan placeholder"
   - **DILARANG KERAS** mengarang/memfabrikasi nomor telepon, email, atau alamat yang tidak ada di dokumen sumber. Ini merupakan pelanggaran Zero Hallucination yang serius.
7. **Template-Consumability** (template-consumability — output harus langsung bisa
   dirender tema builder `modern` tanpa editing manual):
   - Setiap slide `# ` membawa SATU image directive valid
     (`<!-- image: <slot> -- query: ...; keywords: ...; style: photo -->`).
     image directive hilang/format salah → REVISION_REQUIRED.
   - pricing rows: tabel pricing WAJIB tepat 3 baris data (`| Tier | Harga | Fitur |`,
     baris tengah = Pro). Bukan 3 baris parseable → REVISION_REQUIRED.
   - differentiator columns: tabel pembanding WAJIB 4–5 kolom dengan header kolom menggunakan label kategori/arketipe generik (misal `Solusi Konvensional`, `Agency Tradisional`, `Software Generik`, `Pendekatan Manual`). Header dan isi sel DILARANG menyebut nama merek/brand kompetitor spesifik (Zero Competitor Leak). Kurang dari 4 kolom atau menyebut nama merek kompetitor spesifik → REVISION_REQUIRED.
   - big-number regex: setiap bullet metrik WAJIB cocok dengan big-number regex
     (`%`, `:`, `Rp`, `vX` — misal `~90%`, `20:1`, `Rp10rb`) agar tidak jatuh ke
     default `100%`. Tidak cocok → REVISION_REQUIRED, kecuali bullet
     struktural/prosa yang tidak membawa klaim metrik (misal label pipeline
     seperti `3-tier`).
   - honesty callout: baris `**Intinya:** ...` WAJIB ada bila kompetitor menang di
     satu aspek (misal syarat setup GPU 8 GB). honesty callout hilang padahal ada
     aspek yang dimenangkan kompetitor → REVISION_REQUIRED.
8. **Selling Point Verification & Zero Competitor Leak** *(hanya jika `selling-points-research.md` tersedia)*:
   - Setiap selling point yang diklaim dalam narasi slide harus **traceable** ke entry `SP-N` di `selling-points-research.md`.
   - **Zero Competitor Leak Check:** Scan seluruh `01-draft.md` — TIDAK BOLEH ada nama kompetitor yang muncul. Jika ditemukan → REVISION_REQUIRED dengan catatan "Competitor leak pada Slide X: nama [kompetitor] terdeteksi".
   - **Differentiator Table Headers & Cells Rule:** Tabel pembanding pada Slide 7 WAJIB menggunakan label kategori/arketipe generik (misal: `Solusi Konvensional`, `Agency Tradisional`, `Software Generik`, `Pendekatan Manual`, `Alat Manual / In-House`). Jika nama merek atau brand kompetitor spesifik muncul pada header kolom atau sel tabel pembanding, reviewer WAJIB menerbitkan `REVISION_REQUIRED` untuk competitor leak ("Competitor leak pada tabel Slide 7: nama [kompetitor] terdeteksi di header/sel").
   - Selling points harus dirajut secara natural ke narasi, bukan ditempel sebagai daftar terpisah.
   - Selling points harus konsisten dengan fakta di `business-knowledge-base.md` (overlap check dengan item 1 Factual Consistency).

## Status Review
- **`APPROVED`**: Draf memenuhi semua kriteria checklist. Salin konten ke `compros/<slug>/drafts/02-final.md` (legacy: `artifacts/02-company-profile-final.md`) dan teruskan ke Builder.
- **`REVISION_REQUIRED`**: Tulis rincian perbaikan di `compros/<slug>/reports/review-report.md` (legacy: `artifacts/review-report.md`). Orchestrator akan mengembalikan draf ke Writer (maksimal 3 iterasi loop).