---
name: skill-router
description: Katalog 300k+ skill, 100k repo, MCP, dan agent lokal. Pakai SEBELUM menulis tool/kode baru: cek apakah skill/repo sudah ada, cek dependency siap, scan keamanan, baru pakai.
---

# skill-router — gudang aset lokal (0 token)

Semua aset ada di mesin ini, jangan mengarang nama skill dan jangan langsung menulis
tool baru. Cari dulu lewat shell (tanpa biaya token prompt).

## 1. Cari skill
```bash
sk "<tugas>" -n 5          # cari di 304k skill (FTS)
sk -l <nama>               # cetak SKILL.md lalu IKUTI
sk --design                # khusus skill desain/UI
sk "<tugas>" --repo -n 5   # cari repo, bukan skill
```
Badge `[siap]` = dependency sudah terpasang di device ini.
Badge `[butuh:docker,...]` = CLI belum ada → pasang dulu atau pilih alternatif.

## 2. Kalau skill tidak ada: cek repo (100k terindeks)
```bash
python3 ~/.agents/repo-hub.py search "<kata>" -n 10
python3 ~/.agents/repo-hub.py top -n 20           # repo bintang tertinggi
python3 ~/.agents/repo-hub.py hits -n 20          # trending / disebut komunitas
python3 ~/.agents/repo-hub.py get <owner/name>    # shallow clone (kode asli)
```
Banyak entri di `repo-refs/` hanya stub (LICENSE saja) — ambil kode nyata dengan `get`.

## 3. WAJIB scan sebelum pakai apa pun dari luar
```bash
python3 ~/.agents/repo-hub.py scan <path> --json   # critical = jangan dipakai
python3 ~/.agents/skill-sec-scan.py --quick        # sapu skills-store + expanded
```
Cari pola: reverse shell, exfiltrasi kredensial, prompt injection, auto-execute.

## 4. Tambah aset baru
```bash
python3 ~/.agents/skill-grow.py --target 500000 --minutes 60   # skill dari repo
python3 ~/.agents/crawl-and-scan.py --limit 40                 # SKILL.md GitHub
python3 ~/.agents/skills-ready.py --report                     # cek dependency
```

## 5. Urutan kerja yang benar
1. `sk` cari skill → ada dan `[siap]` → `sk -l <nama>` → jalankan.
2. Tidak ada → cari repo → `get` → `scan` → pakai/bungkus jadi skill.
3. Masih tidak ada → baru tulis sendiri, lalu simpan sebagai SKILL.md baru.

Laporan biaya & aturan MCP: `~/.agents/MCP-COST.md`.
