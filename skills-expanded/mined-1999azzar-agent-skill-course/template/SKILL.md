---
name: template-skill
description: >
  Deskripsi lengkap tentang apa yang dilakukan skill ini.
  Sertakan teknologi yang dipakai dan contoh trigger (kata kunci user).
  Contoh: Generate images using SDXL API.
  Use when user asks to 'generate image', 'make a picture', or 'draw this'.
---

# Template Skill

## Setup
<!-- Hapus section ini jika tidak ada setup yang diperlukan -->
1. Install dependencies: `pip install requests`
2. Set environment variable: `export MY_API_KEY=xxx`

## Usage
<!-- Instruksi utama penggunaan skill -->

### Basic
```bash
python3 scripts/main.py "input"
```

### Advanced
See [references/advanced-usage.md](references/advanced-usage.md) for detailed options.

## Environment Variables
| Variable | Required | Description |
| :--- | :---: | :--- |
| `MY_API_KEY` | Yes | API key for the service |

## Notes
<!-- Catatan penting, edge cases, atau batasan -->
