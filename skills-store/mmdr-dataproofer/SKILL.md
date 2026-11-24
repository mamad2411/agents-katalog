---
name: mmdr-dataproofer
description: "Dua CLI utilitas: mmdr render diagram Mermaid→PNG/SVG (Rust, tanpa browser); dataproofer audit kualitas CSV/Excel (headers, numerik, statistik, geo). | EN: mermaid diagram render png svg; csv excel data quality proofread audit"
version: 1.0.0
category: devops-engineer
lang: id
---

# mmdr + dataproofer

## mmdr — Mermaid renderer
- `mmdr -i diagram.mmd -o out.png -e png` (svg default; `-` = stdin)
- Theme: `-t dark|forest|neutral|modern` · ukuran `-w/-H`
- Pakai untuk: architecture diagram, flowchart, sequence — cepat, tanpa puppeteer.

## dataproofer — audit data
- `dataproofer file.csv` — test suite default (headers, tipe, empty cells)
- Suite: `-c` core · `-i` info · `-s` stats · `-g` geo · `-t <list>` custom
- `-j` JSON output (CI-friendly) · `-e` exit code error kalau gagal · `-v` verbose
- Pakai SEBELUM analisis dataset atau setelah export CSV/Excel.
