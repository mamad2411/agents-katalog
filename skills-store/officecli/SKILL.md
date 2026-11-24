---
name: officecli
description: "Buat PPTX/DOCX/XLSX/gambar dari prompt bahasa natural via officecli (100 kredit hosted gratis; External Mode = LLM sendiri). | EN: powerpoint word excel slides document spreadsheet generate office"
version: 1.0.0
category: productivity-automator
lang: id
---

# OfficeCLI — Dokumen Office dari Prompt

## CLI
- `officecli new pptx "Judul" --prompt "..."` — slide deck
- `officecli new docx "Judul" --prompt "..."` — dokumen Word
- `officecli new xlsx "Judul" --prompt "..."` — workbook Excel
- `officecli doctor` — cek environment
- `officecli` — TUI interaktif

## Catatan
- Butuh login 1x (`officecli` → login) untuk 100 kredit hosted gratis.
- External Mode: pakai LLM endpoint sendiri (mis. omniroute lokal) tanpa kredit.
- Untuk report/doc panjang → tetap bisa pakai skill pptx/docx biasa; officecli untuk hasil cepat.
