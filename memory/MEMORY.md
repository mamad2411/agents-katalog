# Memory — global

Fakta yang berlaku lintas proyek. Satu baris per fakta: `- YYYY-MM-DD — fakta — kenapa: alasan`

- 2026-10-23 — CLI opencode di mesin ini di-rebrand jadi `mamatagents`; biner ada di `~/.local/share/mamat/bin/mamat-core`, rebuild lewat `mamat reforge` — kenapa: `opencode upgrade` menimpa patch logo.
- 2026-10-23 — Model default gratis: `opencode/deepseek-v4.1-flash-free`; subagent read-only pakai model yang sama biar 0 biaya.
- 2026-10-23 — Skill native DIMATIKAN: opencode scan `~/.agents/skills` DAN `~/.claude/skills` (83, duplikat). Dua-duanya dipindah (`~/.agents/off/skills`, `~/.claude/skills.off`) supaya 0 skill di prompt (~4.300 token/request hemat). Semua skill lewat shell `sk`/`skillq.py` (bukan MCP — MCP skill-catalog ON lagi tapi tetap 0-token via shell yang utama). Konsekuensi: Claude Code juga kehilangan skill native karena berbagi `~/.claude/skills`.
- User mau semua AI pakai skill dari katalog via sk, 0 token prompt — kenapa: hemat ~4.600 token/request
- pelajaran: repo ini pernah punya secret hardcoded di cfg.js — selalu pakai env
- pelajaran: kalau ubah plugin TUI, wajib cek dengan capture pty — jangan percaya render di kepala
- 2026-11-24 — katalog skill: 482rb aktif di skills-index.db (634rb mentah - 151rb junk); cari via sk/pow find, muat sk -l — 0 token sampai dipakai
- 2026-11-24 — dataset: data-hub search|get|peek — 957rb indeks (HF/OpenML/Zenodo) + 23 curated; peek = EDA instan ≤40 baris, wajib sebelum analisis file data
- 2026-11-24 — peta semua subsistem AI ada di ~/.agents/SYSTEM-MAP.md — cek dulu sebelum bikin tool/index baru (anti-duplikat)

