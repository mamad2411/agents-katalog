# SKILL-FIRST.md — protokol lengkap (dibaca on-demand, TIDAK di-inject penuh)

Blok yang dipasang ke file aturan provider sengaja RINGKAS (progressive disclosure):
yang selalu-on cuma "ada N skill → cari dulu + caranya". Detail di bawah ini dibaca
AI saat dibutuhkan: skill tak ketemu, akan menulis file `.md`, atau perlu tambang/buat skill.
Angka terkini selalu di `~/.agents/SKILLS-AVAILABLE.md` (refresh: `python3 ~/.agents/build_skills_index.py`).

## 1. Skill-First Protocol (WAJIB — sebelum mengerjakan apa pun)

1. **Cari skill dulu** (pilih salah satu):
   - MCP `skill-catalog` → `skill_for_task(task="tambah endpoint Go Gin + test")` ← bahasa natural, paling cepat
   - MCP lainnya: `skill_search(query="...")` · `skill_load(name="...")` · `skills_available()` · `agent_context()`
   - CLI: `~/.agents/skill-search.sh "kata kunci"` · Katalog: `~/.agents/SKILLS-AVAILABLE.md` · Peta: `~/.agents/SKILLS-CATEGORIES.md`
   - Panduan gaya per kategori → `STYLE-*.md` **HANYA on-demand** (jangan baca massal; pilih 1 file yang relevan tugas). Ringkas: ngoding → `STYLE-BACKEND-DEVELOPER.md`/`STYLE-FRONTEND-DEVELOPER.md`; hemat token → `STYLE-TOKEN-SAVER.md`; anti-slop UI → `STYLE-DESIGN-QUALITY.md`
   - ⛔ **JANGAN pernah baca `SKILLS-ALL-PATHS.md` / `SKILLS-SKILLSH-DIRECTORY.md` utuh** (3,4 MB & 1,9 MB = ±1 juta token, membakar seluruh context). Cari path skill via `skill-search.sh -p "<nama>"` atau `sqlite3 ~/.agents/skills-index.db "select path from skills where name='<nama>'"` — baca 1 `SKILL.md` yang dicari saja.
   - Madhab sumber: `~/.agents/SKILLS-SKILLSH-DIRECTORY.md` (daftar resmi skills.sh) · Detail per repo: `REPO-REF.md` di tiap folder skill
2. **Ada skill cocok → ikuti SKILL.md-nya.** Tidak ada → cek MCP relevan + `~/.agents/repo-refs/` (repo rujukan) → baru tulis sendiri.
3. **Tetap tidak ada** → tambang (`MINER_LIMIT=120 python3 ~/.agents/skill-miner.py`) atau bikin baru (`python3 ~/.agents/skill-factory.py "<topik>" "<deskripsi>"`).
4. **Aturan katalog**: `~/.agents/AGENTS.md` (sumber tunggal skill, MCP ≤20/tool, jangan klon katalog).

## 2. Anti-ngarang protocol (WAJIB — langgar = kerjaan ditolak)

1. Klaim apa pun wajib sebut sumber: skill/MCP/repo/file+baris yang dibaca.
2. Dilarang menulis angka/jumlah/nama dari ingatan — baca dulu, baru tulis.
3. Sumber primer tak bisa diakses (MCP mati/token hilang) → BERHENTI + bilang ke user apa yang kurang, jangan nebak.
4. Setiap file `.md` yang ditulis wajib ada bagian `## Sumber` (daftar sumber primer) — reviewer menolak md tanpa sumber.

