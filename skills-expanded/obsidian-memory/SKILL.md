---
name: obsidian-memory
description: "Memori jangka panjang lintas AI agent via vault Obsidian (PARA) + CLI obsidian-log.py. AI wajib pakai ini untuk mencatat keputusan/progress sesi penting dan untuk mengingat kembali konteks proyek sebelum mulai kerja. Universal: Claude, Cline, Codex, Trae, Hermes, agent lain."
---

# Obsidian Memory (Vault = Memori Lintas AI)

Vault: auto-detect dari `~/Library/Application Support/obsidian/obsidian.json` (vault aktif terbaru). Struktur PARA: `00 - Inbox` · `02 - Notes` · `03 - Projects` · `08 - Daily`.

## CLI (satu entry point untuk semua AI)

`python3 ~/.agents/scripts/obsidian-log.py <cmd>`:

| Cmd | Fungsi |
|---|---|
| `status` | vault + ringkasan note per folder |
| `log <Project> "<summary>"` | append `## 🤖 AI Session Log` di `03 - Projects/<Project>.md` |
| `decision <Project> "<title>" "<body>"` | append `## 🎯 Keputusan` di project note |
| `daily "<text>"` | append inbox di `08 - Daily/YYYY-MM-DD.md` |
| `note "<Title>"` | buat `02 - Notes/<Title>.md` (body via stdin) |
| `recall "<query>"` | grep memori di 02/03/08 — pakai SEBELUM mulai kerja di proyek |

## Protokol Wajib AI (kapan harus manggil)

1. **Sebelum mulai tugas di proyek** → `recall "<nama proyek>"` untuk load konteks.
2. **Setelah milestone/keputusan penting** → `log <Project> "<apa yang selesai>"` + `decision` kalau ada pilihan arsitektural/`scope`.
3. **Handoff antar sesi/AI** → pastikan log terakhir berisi state cukup untuk AI berikutnya lanjut tanpa tanya user.
4. Jangan log trivia (rename variabel, typo fix). Log = keputusan, milestone, blocker, state.

## Aturan

- Output selalu plain Markdown + frontmatter (kompatibel template Obsidian/templater yang sudah ada).
- Jangan pernah menimpa isi note — hanya append/tambah bagian.
- Nama Project = nama proyek repo (mis. `GenZysFleetOps`) supaya `recall` konsisten lintas AI.
