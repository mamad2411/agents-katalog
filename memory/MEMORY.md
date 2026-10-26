# Memory — global

Fakta yang berlaku lintas proyek. Satu baris per fakta: `- YYYY-MM-DD — fakta — kenapa: alasan`

- 2026-10-23 — CLI opencode di mesin ini di-rebrand jadi `mamatagents`; biner ada di `~/.local/share/mamat/bin/mamat-core`, rebuild lewat `mamat reforge` — kenapa: `opencode upgrade` menimpa patch logo.
- 2026-10-23 — Model default gratis: `opencode/deepseek-v4.1-flash-free`; subagent read-only pakai model yang sama biar 0 biaya.
- 2026-10-23 — Skill native DIMATIKAN: opencode scan `~/.agents/skills` DAN `~/.claude/skills` (83, duplikat). Dua-duanya dipindah (`~/.agents/off/skills`, `~/.claude/skills.off`) supaya 0 skill di prompt (~4.300 token/request hemat). Semua skill lewat MCP `skill-catalog` (263.916 skill di `~/.agents/skills-index.db`, 5 tool). Konsekuensi: Claude Code juga kehilangan skill native karena berbagi `~/.claude/skills`.
- User mau semua AI pakai skill dari katalog via sk, 0 token prompt — kenapa: hemat ~4.600 token/request
- pelajaran: repo ini pernah punya secret hardcoded di cfg.js — selalu pakai env
- pelajaran: kalau ubah plugin TUI, wajib cek dengan capture pty — jangan percaya render di kepala
