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
- **Angka curated jangan ditampilkan menyesatkan.** Aturan: katalog yang dibaca AI
  hanya boleh berisi tier `curated`. Tier `reference` (60k scraping) **wajib**
  dilaporkan sebagai angka terpisah, jangan pernah dilabeli "curated".
  Cek: `python3 skill-curate.py --report` (3176 curated → 3161 bersih, 15 review).
- **Regenerate berurutan**, jangan paralel: `build_skills_index.py` →
  `skills-index-md.py` → `skills-router.py` (dua terakhir membaca DB).
- **Selalu UTC & idempotent:** script harus bisa dijalankan 2× tanpa efek samping.
  Setiap perubahan file lama → tulis backup `.bak-YYYYMMDD`.
- **Sumber katalog WAJIB `skills-store`**, BUKAN `skills/` (itu folder symlink flow,
  hanya ~79 entri). Salah sumber = curated anjlok 3.176 → 79 saat rebuild.
  Berlaku untuk `build_skills_index.py` + `sync-wire.py`.
- **MCP default MATI** (2026-09-25): hanya `skill-catalog` + `mcp-router` (+`skill-graph`
  di Codex) yang terdaftar. Sisanya di `mcp-parked.json` → hidup on-demand via
  `mcp_use(name=..., tool=...)`. Jangan `--on` bulk; cukup hidup saat dipanggil.
- **Mining publik SATURASI** (2026-09-25): yield registry ~2,6%, skills.sh 0%.
  Jangan ulang `skill-miner.py --registry` / `skill-miner-skillsh.py` untuk mengejar
  100k — sumbernya sudah diserap. Butuh sumber baru.
- **Jangan `claude --resume` sesi lama**: file history 53,9 MB = jauh lebih boros
  daripada seluruh fixed-cost. Pakai `claude -c` (sesi terakhir) atau sesi baru.

## Hemat konteks (alasan: limit cepat habis)

Audit 2026-09-26 (transcript nyata): **4,42 miliar token** terpakai, 3 sesi @ 59/54/18 MB
→ tiap pesan membaca ulang **±0,5 juta token**. Penyebabnya bukan model, tapi sesi panjang.

- `/clear` di **setiap batas tugas**. Sesi > 10 MB = wajib ditutup untuk tugas berikutnya
  (hook `context-guard.sh` memperingatkan otomatis; ambang `CONTEXT_WARN_MB`/`CONTEXT_URGENT_MB`).
- **DILARANG `claude --resume`** sesi lama — sesi baru + catatan handoff.
- **LOOP = PEMBOROS #1 (audit 2026-10-03).** 02 Okt: 1.223 pesan/±500 jt token sehari
  karena agen berputar (spawn→baca→edit→gagal→validasi→ulangi). Tanda loop: pesan sama
  berulang, error yang sama >2×, spawn tanpa progres. Tindakan WAJIB saat
  `[loop-guard]` memperingatkan / tanda ini muncul: **HENTIKAN agen (`Esc`),
  tulis STATUS + LANGKAH SELANJUTNYA ke file, tutup sesi, lanjut di sesi BARU**
  yang membaca file itu. DILARANG membiarkan agen berjalan tanpa batas.
  Ambang peringatan: 80 tool call/sesi (lunak), 200 tool call ATAU 500 pesan (keras).
  Sempitkan spawn/subagent: maks 3 paralel, 1 tujuan per agen, tanpa rekuris tanpa izin.
  (`LOOP_WARN_N`/`LOOP_HARD_N`/`LOOP_MSG_N` di `~/.agents/loop-guard.py`.)
- **DILARANG** `Read`/grep ke `vendor/`, `node_modules/`, `dist/`, `public/template/`,
  `skills-expanded/`, `*.min.js` (sudah diblok `permissions.deny` di `~/.claude/settings.json`
  dan `.claude/settings.json` repo). Butuh 1 baris dari sana → `sed -n`/`grep -n` via shell,
  jangan `Read` penuh.
- Alur kerja tetap dijalankan penuh, tapi **baca SKILL-FLOW.md hanya on-demand** (5,3 KB/sesi terbuang).
- **Skill tetap diambil** — hanya cara memuatnya dibuat hemat: `bash ~/.agents/skill-load-lite.sh <nama>`
  (≤80 baris / ≤2 KB). Baca `SKILL.md` penuh hanya kalau lite kurang. Jangan muat ulang skill
  yang sudah dimuat di sesi yang sama.
- Ukur, jangan menebak: `python3 ~/.agents/usage-audit.py` (token 7 hari + sesi terboros)
  dan `python3 ~/.agents/context-guard.py --report`.

## Pakai subagent (pintar, bukan boros)

- **Default TANPA subagent.** Pakai HANYA kalau ketiganya benar: (1) lepas dari tugas
  utama, (2) perkiraan >20 menit, (3) butuh konteks terpisah (eksplorasi besar).
- Maks **3 paralel** · **1 tujuan per agen** · DILARANG subagent memanggil subagent
  tanpa izin user.
- **Brief wajib terbatas**: tujuan + ruang lingkup file + definisi selesai + batas
  keluaran (≤30 baris ringkasan, dilarang dump file besar/daftar panjang).
- Model: eksplorasi/rutin → model murah; reasoning berat → model utama.
- **Satu penulis**, sisanya read-only (hindari konflik edit & edit→gagal→ulangi).
- Agen TIDAK menandai "selesai" untuk perubahan kode produksi — verifikasi ada di
  penulis utama (uji nyata), bukan di agen.
- Tanda loop (error sama >2×, pesan berulang, spawn tanpa progres) → **berhenti**,
  tulis STATUS + LANGKAH SELANJUTNYA ke file, tutup sesi, lanjut di sesi baru.

## Tangga progressive disclosure (skill · MCP · repo) — jangan lompat

1. **Baca `TOKEN-SAVER.md` (2 KB) dulu** — panduan hemat untuk semua AI.
2. **Cari, jangan baca katalog**: DB FTS (`skill-search.sh` / MCP `skill_for_task`).
   JANGAN buka `SKILLS-AVAILABLE.md` (123 KB) / `SKILLS-ALL-PATHS.md` (3,4 MB, RACUN) /
   `SKILLS-SKILLSH-DIRECTORY.md` (1,8 MB, RACUN). Peta aman: `SKILLS-CATEGORIES.md`
   (4 KB) · `SKILLS-CONCEPTS.md` (2 KB) · `SKILLS-FLOWS.md` (2 KB).
2. **Kartu hasil** (8 baris, deskripsi 120 B) → pilih max 2 skill.
3. **Muat ringkas**: `bash ~/.agents/skill-load-lite.sh <nama>` (≤80 baris/≤2 KB).
4. **SKILL.md penuh** hanya kalau lite kurang (3–15 KB → sadar biaya).
5. **Sumber asli**: `REPO-REF.md` atau `python3 ~/.agents/repo-ref-api.py --search "<kata>"`
   (jangan klon/`cat` repo besar; grep baris spesifik).
6. **MCP hemat**: nyala default hanya `skill-catalog` + `mcp-router`; server lain
   on-demand `mcp-use`/`mcp-lifecycle.py --on <nama>` lalu matikan lagi.
7. **Wiring per-repo = role pack**: `bash ~/.agents/wire-skills-role.sh <preset> <repo> --apply`
   (backend/frontend/fullstack/data/ai/design/qa/devops/security/mobile/docs/core).
   Repo Vue+Go tidak perlu skill blockchain/game → konteks lebih ramping tapi tetap pintar.

## Alur kerja standar

```bash
# 0. WAJIB: cari skill dulu (jangan mengarang dari nol)
#    Cheatsheet perintah: ~/.agents/CHEATSHEET.md (36 baris) · lengkap: COMMANDS.md
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
