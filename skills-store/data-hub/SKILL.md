---
name: data-hub
description: "Data publik untuk AI: katalog dataset UCI ML + mirror GitHub (konkret/menara, aero-angin, energi gedung, klasifikasi, demografi). Ambil on-demand via data-hub CLI — storage hemat. | EN: public dataset kaggle uci ml data download csv analysis"
version: 1.0.0
category: knowledge-base
lang: id
---

# Data Hub — Dataset Publik untuk Analisis

## CLI
- `data-hub list` — semua dataset + status
- `data-hub search <kata>` — cari (mis. "konstruksi", "klasifikasi")
- `data-hub get <slug>` — unduh ke `~/.agents/datasets/<slug>/` → path file
- `data-hub get <slug> --info` — metadata saja

## Isi katalog
- **Teknik/sipil**: concrete-strength (beton 1030), steel-plates-faults (cacat baja 1941), airfoil-noise (aero/angin 1503), energy-efficiency (HVAC gedung), yacht-hydrodynamics (lambung), auto-mpg (kendaraan)
- **Industrie/maintenance**: hydraulic-systems (2205 sensor), secom (manufaktur), steel-energy (energi baja)
- **Bangunan/smart**: occupancy-detection (sensor gedung 20k), appliances-energy (19k)
- **Lainnya**: traffic-volume (48k), bankruptcy-poland (10k), student-eval, population-world
- **HuggingFace (ribuan dataset lain)**: `data-hub get hf:<owner>/<nama>` → 1000 baris JSONL · `data-hub get openml:<id>` → ARFF · `data-hub get zenodo:<id>` → file pertama ≤50MB (mis. `hf:cornell-movie-review-data/rotten_tomatoes`)
- **ML klasik**: iris, wine-quality, diabetes, bank-marketing (45k, imbalanced), student-performance, breast-cancer, parkinsons
- **Demografi**: population-world (populasi per negara/tahun)

## Alur pakai (WAJIB hemat token)
1. `data-hub search <domain>` → pilih slug → `data-hub get <slug>`
2. **Jangan pernah `cat`/baca seluruh file** — file bisa MB–ratusan MB.
   Pakai pandas dan panggil HANYA agregat:
   `df.head()`, `df.describe()`, `df.dtypes`, `df.isna().sum()`, `df[col].value_counts().head()`
   Untuk JSONL (hf:): `pandas.read_json(path, lines=True)` lalu agregat yang sama.
3. Untuk ML: ikuti skill `data-science-kaggle` (EDA → baseline → CV → model).
   Training pakai script file, output ke terminal — jangan print dataframe utuh.

## Batas ukuran
- `hf:` → maks 1000 baris JSONL (~1-3MB teks) — cukup untuk EDA & baseline.
- `zenodo:` → file pertama ≤50MB; kalau lebih besar, catat slug-nya dan minta user.
- Dataset curated UCI → <1MB, aman.

## Indeks besar (metadata, target 100k+)
- `~/.agents/datasets-index.db` — indeks metadata dataset dari HuggingFace (~1jt+), OpenML (~7rb), Zenodo (~786rb).
- `data-hub search <kata>` — cari di katalog lokal + indeks besar (nama, deskripsi, tag, downloads).
- Fetch dari indeks: `data-hub get hf:<owner>/<nama>` (JSONL 1000 baris) · `data-hub get zenodo:<id>` (file pertama ≤50MB).
- OpenML: metadata saja; download manual via `https://www.openml.org/data/v1/download/<did>`.
- Indexer: `python3 ~/.agents/dataset-indexer.py [hf|openml|zenodo]` — resumable, rebuild FTS otomatis.

## Tambah dataset baru
Edit dict `DATASETS` di `~/.agents/data-hub.py` — format (nama, domain, url, catatan).
Sumber publik tanpa key: archive.ics.uci.edu/static/public/<id>/<nama>.zip · raw.githubusercontent.com/datasets/<repo>/master/data/<file>.csv
