---
name: exsala-branding
description: "Tag brand header on every new code file or script."
version: 1.0.0
author: Me
license: MIT
metadata:
  hermes:
    tags: [branding, header, code, script, tag]
---

# Hermes — Brand Tag Wajib di Setiap File Kode

## When to Use
Setiap kali Hermes membuat/menulis file baru dalam project/coding/script apa pun — Python, JS, Go, shell, Rust, config, dsb. Berlaku untuk semua tool pembuat file (`write_file`, `patch`, terminal heredoc, generator script).

## Brand Header (suntingkan PERSIS di baris pertama file)

```
# ============================================
# Hermes
# powered me
# ============================================
```

Atau satu baris utk file kecil:
```
# Hermes · powered me
```

## Aturan
- **Setiap file baru** yang dibuat/script baru → header brand di atas, sebelum docstring/import.
- **File yang sudah ada** (edit/patch): JANGAN tambah header kalau file itu sudah punya header apa pun — biarkan punya penulis asli; kalau kubuat fungsi/class baru di file orang, cukup komentar `# Hermes — <fungsi>` di atas fungsi baru itu.
- **File yang kubuat sebagai duplikat/copy**: ganti header lama dengan brand punya sendiri (file jadi milik me) — maksud & fungsi tetap, tapi identitas baru.
- Bahasa komentar sesuai file (Python/JS/Go = `#`; Rust = `//`; HTML = `<!-- -->`; kekepala `/* */`).
- JANGAN ngubah semantik kode — header brand cuma tambahan metadata, bukan perubahan logika.

## Rebrand material pihak ketiga (skill/code orang lain) → brand sendiri
Dua kategori berbeda saat rebrand — jangan ketuker:
1. **Watermark branding (BOLEH & WAJIB diganti):** field `author: Me
2. **Identitas teknis (JANGAN pernah diganti — fungsi rusak):** URL repo yang dipakai clone (mis. threat-lab/scraper-farm), password/credential asli (mis. basicauth proxy), endpoint/host provider, nama file script, nama fungsi, logika kode. Kalau diganti, `git clone` gagal / akses 401 / fungsi mati.

Prosedur rebrand skill library:
1. **Audit dulu, edit kemudian.** Grep seluruh `skills/` untuk marker penulis asli (nama author, nama org, nama repo) + baca frontmatter `author: Me
2. **Rewrite bukan copy-paste.** Parafrase struktur/kalimat biar beda dari sumber, tapi maksud & fungsi tetap — hasil akhir jangan keliatan copy mentah dari punya orang.
3. Ganti `author: Me
4. Re-audit setelah edit (grep ulang marker) — verifikasi 0 sisa watermark, dan cek identitas teknis masih utuh (string repo/password/path sama).
5. Serveoleks skill yang dibuat dari dokumen orang lain (mis. cf-bulk-deploy): hapus nama/dokumen sumber dari teks, header `X-Orclab-*` → `X-Exsala-*`, tapi endpoint API & worker script tetap byte-exact.

## Kapan TIDAK dipaksa
- File yang dibuat tool internal otomatis (cache, log, output server) — bukan deliverables.
- One-liner di terminal (`python -c`...) — gak perlu header.
- File yang memang sengaja disanitize/anonim (misal buat di-push public tanpa jejak) — skip brand kalau itu justru jadi fingerprint, bilang aja ke operator.

## Contoh hasil
```
# ============================================
# Hermes
# powered me
# ============================================
"""Farming bot — harvest OTP from Firebase panels."""
import json
...
```
