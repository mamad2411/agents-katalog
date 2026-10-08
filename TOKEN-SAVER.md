# TOKEN-SAVER — panduan hemat token untuk SEMUA AI (generated, jangan edit manual)
# Prinsip: JANGAN baca file besar utuh. Cari dulu, baca seperlunya, stop kalau cukup.

> **Untuk AI: baca 30 baris ini SEBELUM mengerjakan apa pun.** Ini menghemat
> ±90% token vs baca katalog utuh.

## Aturan hemat (wajib)
1. JANGAN baca `SKILLS-AVAILABLE.md` utuh (123 KB) — pakai `SKILLS-CATEGORIES.md` (4 KB) dulu.
2. JANGAN baca `SKILLS-ALL-PATHS.md` (3,4 MB) — JANGAN PERNAH dibuka utuh.
3. JANGAN baca `STYLE-*.md` (212 file, 6,5 MB) kecuali tugasnya memang butuh style itu.
4. Cari skill: `skill-search.sh "<kata kunci>"` (±1 KB hasil) atau `skill_for_task`.
5. Butuh isi 1 skill: `skill-search.sh --load "<nama>"` (head 60 baris) atau `skill-load-lite.sh`.
6. Butuh tahap alur: `SKILLS-FLOWS.md` (2 KB) → pilih tahap → search.
7. Butuh konsep: `SKILLS-CONCEPTS.md` (2 KB) → pilih konsep → search.
8. Stop kalau sudah cukup — JANGAN baca "sekalian" file lain.
9. Sesi >10 MB → `/clear`, tulis STATUS ke file, lanjut sesi baru (lihat AGENTS.md §Hemat konteks).
10. DILARANG `Read`/grep ke `vendor/ node_modules/ dist/ skills-expanded/ *.min.js`.

## Ukuran file (biar sadar biaya)
- AMAN (<30 KB): CATEGORIES, CONCEPTS, FLOWS, INDEX, skills-index.json, TOKEN-SAVER (ini)
- MAHAL (>100 KB, baca seperlunya): AVAILABLE (123 KB), STYLE-* (80-420 KB tiap file)
- RACUN (>1 MB, JANGAN dibuka): ALL-PATHS (3,4 MB), SKILLSH-DIRECTORY (1,8 MB)
