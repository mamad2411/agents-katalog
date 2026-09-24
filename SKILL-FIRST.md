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
   - **Panduan gaya per kategori (JANGAN cuma pakai skill bintang — daftar LENGKAP per kategori ada di `~/.agents/STYLE-*.md`)**: ngoding → `STYLE-BACKEND-DEVELOPER.md` (6.239) / `STYLE-FRONTEND-DEVELOPER.md` (2.080) / `STYLE-MOBILE-DEVELOPER.md` (706) / `STYLE-FULLSTACK-GENERALIST.md` (272); AI/ML → `STYLE-AI-ENGINEER.md` (1.908); data → `STYLE-DATA-SCIENTIST.md` (1.229) / `STYLE-DATA-ENGINEER.md` (470); infra → `STYLE-DEVOPS-ENGINEER.md` (2.228) / `STYLE-DEVTOOLS-ENGINEER.md` (771) / `STYLE-SECURITY-SPECIALIST.md` (1.091); QA → `STYLE-QA-ENGINEER.md` (1.499); design → `STYLE-DESIGNER.md` (2.926) + `STYLE-DESIGN-QUALITY.md` (44 anti-slop); dokumen PRD/BRD/spec/requirement → `STYLE-DOC-SPEC-PRD-BRD.md` (773); produk → `STYLE-PRODUCT-MANAGER.md` (399) / `STYLE-ARCHITECT.md` (122) / `STYLE-ANALYST.md` (154); tulis-menulis → `STYLE-TECH-WRITER.md` (540); game/kreatif → `STYLE-GAME-DEVELOPER.md` (1.822) / `STYLE-CREATIVE-PRODUCER.md` (1.800); blockchain → `STYLE-BLOCKCHAIN-DEVELOPER.md` (66); produktivitas → `STYLE-PRODUCTIVITY-AUTOMATOR.md` (93); edukasi → `STYLE-EDUCATOR.md` (24)
   - Hemat token → `STYLE-TOKEN-SAVER.md` (108 skill)
   - **Daftar LENGKAP semua skill + path file-nya** (bukan contoh): `~/.agents/SKILLS-ALL-PATHS.md` — kalau butuh isi suatu skill, **baca langsung file SKILL.md di path itu**, tanpa meminta persetujuan user dulu
   - Madhab sumber: `~/.agents/SKILLS-SKILLSH-DIRECTORY.md` (daftar resmi skills.sh) · Detail per repo: `REPO-REF.md` di tiap folder skill
2. **Ada skill cocok → ikuti SKILL.md-nya.** Tidak ada → cek MCP relevan + `~/.agents/repo-refs/` (repo rujukan) → baru tulis sendiri.
3. **Tetap tidak ada** → tambang (`MINER_LIMIT=120 python3 ~/.agents/skill-miner.py`) atau bikin baru (`python3 ~/.agents/skill-factory.py "<topik>" "<deskripsi>"`).
4. **Aturan katalog**: `~/.agents/AGENTS.md` (sumber tunggal skill, MCP ≤20/tool, jangan klon katalog).

## 2. Anti-ngarang protocol (WAJIB — langgar = kerjaan ditolak)

1. Klaim apa pun wajib sebut sumber: skill/MCP/repo/file+baris yang dibaca.
2. Dilarang menulis angka/jumlah/nama dari ingatan — baca dulu, baru tulis.
3. Sumber primer tak bisa diakses (MCP mati/token hilang) → BERHENTI + bilang ke user apa yang kurang, jangan nebak.
4. Setiap file `.md` yang ditulis wajib ada bagian `## Sumber` (daftar sumber primer) — reviewer menolak md tanpa sumber.

