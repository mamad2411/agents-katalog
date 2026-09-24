# AGENTS.md — Aturan Kerja di `~/.agents`

Kamu agen AI yang bekerja di katalog skill bersama. Baca ini dulu (1 menit), lalu
`README.md` untuk peta file.

## Baca dulu (urut)
1. `README.md` — peta cepat + perintah harian + status drift.
2. `skills-INDEX.md` — angka pokok & kategori (generated).
3. `AGENTS.md` (ini) — aturan keras.

## Aturan keras

- **Sumber tunggal:** hanya `skills/<nama>/SKILL.md` yang boleh di-link/di-invoke.
  `skills-expanded/` = arsip scraping; tier `docs` (lihat `skills-junk.txt`) **bukan skill**.
- **Jangan klon katalog.** Wire lewat `link-skills-min.sh` (symlink). Jangan pernah
  menyalin 24k folder ke folder tool apa pun.
- **Jangan edit file generated:** `skills-index.db`, `skills-INDEX.md`, `skills-junk.txt`,
  `mcp-hygiene-report.md`. Regenerate lewat script-nya.
- **Jangan hapus apa pun tanpa izin user.** Script di sini hanya menambah/menautkan;
  penghapusan massal (arsip, `repo-refs/`, farm lama) = keputusan user (P1).
- **Nama file = kanonik.** Saat menambah skill baru, `name:` di frontmatter harus sama
  dengan nama folder (kebab-case, tanpa `--`, tanpa suffix `-skill`).
- **Deskripsi wajib.** Skill tanpa `description:` akan jatuh ke tier `docs` dan tidak
  akan pernah tampil sebagai kandidat. Tulis 1 kalimat "apa + kapan dipakai".
- **MCP jangan ditumpuk.** Kurasi ≤20 server/tool, nama kebab-case, satu file per tool.
  Audit `python3 mcp-hygiene.py`, apply hanya kalau yakin (`--apply`, backup otomatis).
- **Port mati jangan diandalkan:** `:27125` (skill-graph/proxy), `:27126` (repo-ref).
  Untuk pencarian pakai `skill-search.sh` (SQLite FTS5).
- **Selalu UTC & idempotent:** script harus bisa dijalankan 2× tanpa efek samping.
  Setiap perubahan file lama → tulis backup `.bak-YYYYMMDD`.

## Alur kerja standar

```bash
# 0. WAJIB: cari skill dulu (jangan mengarang dari nol)
skill-search.sh --tier curated "<topik>"          # CLI
# atau MCP: skill_for_task(task="...") / skill_search(query="...") / agent_context()

# 1. Baca skill yang relevan
skill-search.sh --load "<nama-skill>"

# 2. Kalau tidak ada yang cocok → tambang komunitas / bikin baru (jangan langsung mengarang)
MINER_LIMIT=120 python3 skill-miner.py             # tambang SKILL.md dari repo komunitas (dedup otomatis)
python3 skill-factory.py "<topik>" "<deskripsi>"   # bikin skill baru meniru struktur referensi curated

# 3. Wire ke tool/repo (symlink, bukan klon)
link-skills-min.sh --repo /path/ke/repo      # untuk project (mis. repo Go/Vue)
link-skills-min.sh --tool ~/.claude/skills   # untuk user-scope

# 4. Kalau katalog berubah, regenerate
python3 build_skills_index.py && python3 skills-index-md.py && python3 skills-router.py

# 5. Audit MCP berkala (1× per beberapa sesi)
python3 mcp-hygiene.py            # statis: nama duplikat, sprawl
python3 mcp-doctor.py             # hidup/mati: handshake nyata per server
python3 mcp-lifecycle.py          # nyala/parkir; --gc-if-due jalan otomatis via session-brief
```

## Definisi "selesai" (untuk perubahan di folder ini)

- [ ] Script bisa dijalankan ulang (idempotent) tanpa error.
- [ ] Perubahan data punya backup dan tercatat di `README.md` §Status.
- [ ] Angka indeks diperbarui: jalankan `build_skills_index.py` + `skills-index-md.py`.
- [ ] Tidak ada skill baru yang jatuh ke tier `docs` (cek `skills-junk.txt`).
- [ ] Tidak menambah server MCP atau duplikasi katalog.
