# ~/.agents — Katalog Skill & Konfigurasi Agen (entry point)

Satu tempat untuk katalog skill, indeks, dan utilitas lintas-agen.
**Baca `AGENTS.md` di folder ini dulu** kalau kamu agen AI.

## Peta cepat

| Item | Isi | Status |
|---|---|---|
| `skills/` | **3.172 skill curated** (satu folder = satu skill, `SKILL.md` + `REPO-REF.md`) | ✅ sumber tunggal |
| `skills-expanded/` | ±21,4k hasil scraping (tier `reference`) | arsip, jangan di-link |
| `skills-index.db` | SQLite **FTS5** (kolom: name, description, tier, category, path, source) | ✅ generated |
| `SKILLS-AVAILABLE.md` | **katalog "available"**: ~1.090 skill tier-1 per kategori (dibaca AI saat perlu) | ✅ generated |
| `SKILLS-CATEGORIES.md` | peta 22 kategori + contoh skill | ✅ generated |
| `skills-index.json` | versi mesin katalog (dipakai MCP + hook) | ✅ generated |
| `skill-mcp.py` | **MCP server** `skill-catalog`: skill_for_task, skill_search, skill_load, skills_available, agent_context | ✅ aktif |
| `skill-search.sh` | cari skill via CLI (FTS5 + bm25, bahasa natural) | ✅ |
| `session-brief.sh` | brief 720 B disuntik ke tiap sesi (hook SessionStart) | ✅ aktif |
| `install-skill-first.py` | pasang MCP+hook ke semua agen (idempotent, backup) | ✅ |
| `skills-router.py` | generator katalog (cap 60/kategori) | ✅ |
| `link-skills-min.sh` | wiring skill via symlink (repo/user scope) | ✅ |
| `skills-INDEX.md` | ringkasan manusiawi (agregat + contoh) | ✅ generated |
| `skills-junk.txt` | daftar entri tier `docs` (bukan skill) | ✅ generated |
| `repo-refs/` | 14.018 dump README/AGENTS repo rujukan (1,3 GB) | arsip |
| `role-skill-map.json` | 20 peran × keyword → skill (coverage 89%) | data |
| `.skill-lock.json` | provenance 2.454 skill (repo + hash) | 10% cakupan |
| `mcp-hygiene-report.md` | hasil audit MCP terakhir | generated |
| `_symlink-farm-archive/` | arsip farm lama (110 MB) | kandidat hapus (P1) |

## Skill-first: AI harus LIAT dulu, bukan mengarang

Alur wajib untuk agen (semua tool): **cari skill → cek MCP → cek repo ref → baru tulis sendiri.**

| Lapis | Cara akses |
|---|---|
| Katalog "available" | `SKILLS-AVAILABLE.md` (3.176 skill curated, per kategori) |
| Peta kategori | `SKILLS-CATEGORIES.md` |
| Rekomendasi per tugas | MCP `skill_for_task(task="...")` (bahasa natural) |
| Cari kata kunci | MCP `skill_search(query="...")` atau `skill-search.sh "..."` |
| Baca isi skill | MCP `skill_load(name="...")` |
| Lihat semua dulu | MCP `agent_context()` (skill + MCP + repo + aturan) |
| Brief tiap sesi | hook `session-brief.sh` (Claude Code SessionStart) |
| Data mesin | `skills-index.json` (dipakai MCP & hook) |

Instalasi ulang/agen baru: `python3 ~/.agents/install-skill-first.py --apply`
→ memasang MCP `skill-catalog` **+ blok Skill-First (angka auto-refresh)** ke **12 provider**:
claude · codex · gemini · codebuddy · hermes · trae · opencode · aider · cline · windsurf · continue · roo.
(Claude Code: MCP didaftarkan lewat `claude mcp add --scope user skill-catalog -- python3 ~/.agents/skill-mcp.py`.)

**Kenapa ini pernah gagal:** MCP terdaftar tapi hanya claude/codex/gemini punya file aturan — 9 provider lain
tidak punya file aturan sama sekali, jadi AI-nya tidak pernah tahu skill itu ada (tidak pernah muncul teks
"skill tersedia"). Sejak 2026-09-19 semua provider punya blok `<!-- skill-first:start -->` di file aturannya.

## Perintah harian

```bash
skill-search.sh "postgres index"            # cari skill (semua tier)
skill-search.sh --tier curated "vue page"   # hanya skill terpilih
skill-search.sh --load "playwright"         # lihat isi skill teratas
skill-search.sh -p "docker"                 # tampilkan path SKILL.md

link-skills-min.sh --repo <path>            # wire skill repo via symlink (project-scope)
link-skills-min.sh --tool ~/.claude/skills  # wire set "starter" (user-scope)
link-skills-min.sh --status                 # cek: symlink vs klon per tool

python3 build_skills_index.py               # rebuild index (baca head 4 KB, cepat)
python3 skills-index-md.py                  # regenerate skills-INDEX.md
python3 mcp-hygiene.py                      # audit MCP (laporan, tidak menulis)
python3 mcp-hygiene.py --apply              # prune gh_* + nama duplikat (backup otomatis)

python3 skill-auto-symlink.py [--verbose]   # daemon/patch symlink (on-demand juga bisa)
```

## Aturan penting

1. **Sumber tunggal = `skills/`.** Jangan menyalin katalog ke folder tool — pakai
   `link-skills-min.sh` (symlink) supaya perubahan langsung terlihat semua tool.
2. **Tier `docs` bukan skill.** Jangan taruh di `.claude/skills` / `--tool`.
3. **MCP jangan ditumpuk.** Satu file config per tool, nama kebab-case, ≤20 server.
   Audit dulu, apply belakangan.
4. File bertanda *generated* (`skills-index.db`, `skills-INDEX.md`, `skills-junk.txt`,
   `mcp-hygiene-report.md`) **jangan diedit manual**.
5. Semua script di sini idempotent; yang mengubah data selalu menyimpan backup
   (`.bak-YYYYMMDD`).

## Status & drift (diverifikasi 2026-09-25)

- **2026-09-25 (1) — Sesi overhaul: token, keamanan, Obsidian, dan keputusan mining.**

  **A. Token Claude turun ~34%** (18.017 → ~12.000 token sebelum pesan pertama):
  - MCP dipangkas jadi **mati by default**: Claude/Gemini = `skill-catalog` + `mcp-router`,
    Codex = +`skill-graph` (sebelumnya 13/3/7). **13 server diparkir** di `mcp-parked.json`
    → hidup on-demand via `mcp_use(name=..., tool=...)`, auto-mati setelah pakai.
  - `~/.claude/CLAUDE.md` 16.268 → 7.489 B (hantu `store_fr3k`/`md-mcp`/folder `templates/`
    yang tidak pernah ada dihapus; angka 63.436 → 3.176).
  - `SKILLS-AVAILABLE.md` 7,6 MB → 120 KB (cap 55/kategori, sesuai desain docstring).
  - **Nasihat utama:** JANGAN `claude --resume` sesi lama — file 53,9 MB memuat
   /history penuh = jauh lebih boros daripada seluruh fixed-cost.
  - Penyebab build curated salah baca `skills/` (79 symlink flow) → **`skills-store`
    (3.176)**. Bug sama di `sync-wire.py`. curated sempat 3.176 → 79, sudah pulih.

  **B. Scan keamanan (`skill-sec-scan.py`, statis tanpa eksekusi):**
  251.843 file dipindai → 3.556 temuan → **0 malware nyata** (semua false positive:
  installer resmi `curl|bash`, BOM UTF-8, fixture red-team NVIDIA skillspector).
  Nol biner tersembunyi, nol exfiltrasi di curated. 14/14 self-test lulus.

  **C. Obsidian tersambung ke semua AI:**
  - 3 skill Obsidian (`linkedin-obsidian-memory-graph`, `obsidian-automation`,
    `obsidian-llm-bridge`) masuk core → native di Claude/Gemini/Codex/OpenCode/Pi (82 total).
  - Hook kata `obsidian|vault|note|catat` → kategori `memori` → 3 skill itu.
  - `skill-graph` (vault `~/mamatXobsidian`, 11.878 note) diparkir = on-demand.
  - Vault diberi entry point **`Agent Skills.md`** (skill-graph cari node bernama
    persis "Agent Skills" dengan description) + `00-Index.md`; `skill_graph_index`
    kini_ISI bukan "No index note found".

  **D. Kontrak skill untuk 14 AI tanpa hook** (`install-skill-contract.py`):
  Cursor/Windsurf/Aider/Continue/Trae/Roo/Qwen/OpenCode/Pi/Kilo/Cline dapat blok
  "WAJIB cari & muat skill" di file rules masing-masing. Hantu `animation-workflow`
  (MCP tak terdaftar) dibersihkan dari Trae settings.json.

  **E. MINING DIHENTIKAN — sumberjenuh (keputusan sadar).**
  Registry batch: 116 download → **+3** index. Skills.sh batch: 192 download →
  **+0** (191 sudah ada). Keduanya yield 0–2,6% ⇒ sumber publik yang dipakai sudah
  diserap katalog. 100k **tidak realistis** dari sumber ini; batas ±70–80k.
  4 folder duplikat dipindah ke `duplikat-mining-20260925/` (bukan dihapus).
  Miner/daemon dimatikan. Butuh sumber BARU (bukan registry/skills.sh) untuk 100k.

  **F. Dokumentasi:** `COMMANDS.md` 26→54 script + shortcut di atas;
  `CHEATSHEET.md` (97 baris) untuk akses cepat. Semua angka basi dibersihkan.

## Status & drift (sebelum: diverifikasi 2026-09-20)

- **2026-09-20 (11)** — **STYLE dipecah jadi sub-kategori (212 file, verifikasi 26.731/26.731).**
  16 parent besar → ~200 file `STYLE-<CAT>-<SUB>.md` tematik (mis. DESIGNER → UI-UX-DESIGN 225, BRAND-IDENTITY 139, PRESENTATION-DOCUMENT-DESIGN 19, dst; BACKEND → API-REST-GRAPHQL 464, DATABASE-ORM 439, dst) + shard alfabetis GENERAL-<CAT>-A-D/…/U-Z utk sisa tak terpola.
  Kit non-teknis dikeluarkan jadi 4 file mandiri: CONF-ACADEMIC-JOURNAL 1.601 (brycewang-stanford, 1135★), TAX-EINVOICE 103 (openaccountants, 391★), SUEDE-SEO-MARKETING 70, RSUN-WORKFLOW 24 — sumber terverifikasi via GitHub API + REPO-REF, BUKAN sampah.
  Script idempotent: `split-style-categories.py` (guard: parent yg sudah displit dilewati) + `confkit-extract.py`.
  Insiden: run ganda menimpa parent jadi 0 + menghapus 4 file kategori kecil (fullstack/blockchain/productivity-automator/tanpa-kategori) + 720 salinan salah kategori DB + subkat DOC-SPEC cacat (duplikat isi parent) — SEMUA dipulihkan: parent restore dari /tmp/style-backup-20260920, 4 file rebuild dari db, salinan salah dihapus berdasar kategori db, 5 subkat DOC-SPEC cacat dihapus.
  FINAL: unik MD 26.731 = db 26.731, HILANG 0, DUP 0. Miner skills.sh lanjut (746/2569).

- **2026-09-20 (10)** — **Panduan gaya LENGKAP per kategori (bukan cuma token/slop).**
  23 file `STYLE-<KATEGORI>.md` (satu per kategori ngoding/design/data/infra/QA/dsb — tiap file = bintang curated + SEMUA skill kategori itu + path; total ~6,7 MB) + `STYLE-DOC-SPEC-PRD-BRD.md` lintas-kategori (773 skill PRD/BRD/SRS/spec/requirement/user-story/acceptance-criteria, 83 curated).
  `SKILL-FIRST.md` kini menunjuk SEMUA 26 file STYLE (AI wajib baca panduan kategorinya dulu, JANGAN hanya pakai skill bintang).
  Regen: script di log sesi (query db `skills`, bukan hardcode).
  Miner skills.sh lanjut, watchdog v4 aktif.

- **2026-09-20 (9)** — **MD LENGKAP utk semua AI + klarifikasi sumber baru.**
  (a) `SKILLS-ALL-PATHS.md` (3,3 MB — SEMUA 26.731 skill + path file, dari db; regen: script di log) — AI baca skill langsung tanpa minta user.
  (b) `STYLE-TOKEN-SAVER.md` (108 skill hemat token) + `STYLE-DESIGN-QUALITY.md` (44 skill anti-slop/design) — blok Auto-Skill di 12 provider kini menunjuk keduanya (bukan cuma 2 bintang).
  (c) `SKILLS-AIHERO-DIRECTORY.md` (38/38 skill mattpocock terpetakan di katalog).
  (d) `SKILL-FIRST.md` menautkan semua direktori.
  FAKTA: aihero.dev = 1 repo mattpocock/skills (38 SKILL.md — semua SUDAH ada; dedup kemarin sah, tidak ada yang hilang).
  agentskills.io = DOKUMENTASI format skill (0 skill, tidak ada katalog publik; client showcase-nya hanya daftar tool pendukung).
  FIX installer: provider `qwen` + `opencode2` (.config/opencode) didaftarkan; QWEN.md diblok-marker-kan (backup `.bak-20260920`).
  Miner skills.sh lanjut (~124/2569, watchdog v4 aktif).

- **2026-09-20 (7)** — **Ekspansi katalog menuju 30k + mode tarball miner.**
  Target user: 30.000 skill terbaca semua AI tanpa membebani sesi. Miner
  ditemukan bottleneck kuota API anonim (60/jam; 313 repo butuh 313 call
  trees) → `skill-miner.py` dipatch: (a) `get()` token-aware via `GH_TOKEN`
  (gh auth = 5000/jam) + retry 403/429 sekali; (b) mode baru `--tarballs`:
  1 unduhan tar.gz/repo via `codeload.github.com` (bukan kuota API, tahan
  abuse-detection) + ekstrak SKILL.md lokal — teruji (+21 dari RuView).
  Refactor `process()` (dedup md5+nama, REPO-REF.md otomatis per skill =
  AI bisa telusuri repo/workflow sumber). Miner raw lama (PID 40961)
  ternyata masih hidup diam-diam → dibunuh; kini tepat 1 miner jalan.
  Wiring: vscode `mcp.json` +skill-catalog (mcpServers); cek 12 provider
  JSON lain → semua sudah punya skill-catalog ✓. "si slop" = skill
  `anti-ui-slop` — SUDAH ADA di curated, tidak perlu install.
  Backup: `skill-miner.py.bak-20260920`. Katalog saat entri ditulis:
  16.877 (index 14.916) — mining berjalan background, rebuild index +
  INDEX.md + sync-wire SETELAH miner selesai (jangan lupa).
  LANJUTAN (7b) — maksimalkan kualitas: 5 skill penghematan konteks
  (caveman-token-optimizer, token-budget-advisor, anti-ui-slop,
  de-sloppify, talk-normal-llm-prompt) masuk `full_native` di
  skill-core.json (backup `.bak-20260920`) → sync-wire +305 symlink →
  kini 5/5 native di semua provider. Audit kurus: 27/3.174 curated
  <800 byte, mayoritas memang recipe kecil yang sah; review-and-refactor
  dicek = padat, tidak perlu upgrade. Miner mencapai 21.4k+ (81/313).

- **2026-09-20 (6)** — **Doctor round-3: 2 bug baru + verifikasi penuh.** (1) Doctor salah laporkan `skill-catalog` DEAD — probe manual <1 dtk ALIVE; sebab: badai 8 worker di laptop swap-berat melewati deadline lokal 20 dtk. Patch: limit lokal 20→30 + retry serial sekali untuk DEAD "tidak jawab tools/list" (hasil r3: 14 ALIVE — semua 12 server claude + everything + memory-bank; catatan koreksi: memory-bank ternyata ALIVE 5 tools — dedup kemarin tetap valid krn duplikat fungsional dgn `memory`, bukan krn mati). (2) `--only` menimpa seluruh mcp-doctor-result.json dgn 1 server → kini mode merge (tidak merusak bukti). Re-run penuh pasca-patch → hasil final jadi rujukan allowlist. Backup doctor: `.bak-20260920`.

- **2026-09-20 (5)** — **AUDIT GAP RONDE-2 ("apa yang kurang"): 2 bug baru ditemukan & dipatch.** (1) `mcp-doctor.py` menggantung >6 menit tanpa hasil: loop baca pakai `readline()` blokir tanpa batas — deadline 150 dtk tak pernah terevaluasi saat server diam total (figma-mcp). Patch: `select.select` tick 1 dtk + limit 150→60 dtk (backup `.bak-20260920`); anak yatim hasil audit (figma node + wrapper) dibersihkan. (2) `/tmp/legakan.log` 71 KB tumbuh tanpa rotasi → rotasi copy+truncate >500 KB ditambahkan ke legakan.sh (backup `.bak-20260920`; pola mv TIDAK dipakai karena launchd memegang fd ke inode). Lainnya dicek sehat: MCP antar-provider kini 42 server total (claude 12 · codex 10 · windsurf 9 · codebuddy 5 · gemini 2 · trae 1 · vscode 1) vs 132 dulu; skill-graph binary ada; memory persisten OK. Swap naik 0,96→1,98 GB (total 3 GB, grow runtime) → logout/reboot makin layak bila terasa berat.

- **2026-09-20 (4)** — **AUDIT GAP: 3 gap ditemukan & ditutup.** (1) `skills-INDEX.md` basi sejak 18/9 (db 19/9): akar masalah `sync-all.sh` tidak memanggil `skills-index-md.py` → ditambah ke langkah [1/5] + regen sekali. (2) Allowlist ↔ config mismatch: `ddg-search` ada di claude.json tapi tidak di allowlist → tes handshake manual ALIVE ✓ → masuk TIER A utility (backup `.bak2-20260920`). (3) Struktur README: 5 entri drift 09-19 nyempil di header (di atas §Peta cepat) → dipindah ke §Status urutan kronologis (backup README `.bak-20260920b`). Kondisi lain dicek bersih: index db fresh, symlink tiered 60/60 stabil, memory MCP persisten OK (MEMORY_FILE_PATH terpasang, file 3,7 KB), mcp-parked kosong, plist repo-ref-api/skill-graph-api/9router ada tapi tidak loaded (idle, bukan beban). Swap 1,38 GB (naik dr 0,96 — drift pemakaian normal; kandidat logout/reboot saat terasa berat). Sisa `.bak`/`.old` historis dibiarkan (aturan: tidak hapus tanpa izin).

- **2026-09-20 (3)** — **Dedup MCP claude + hygiene re-run + helper dev-stack.**
  Hapus server MCP duplikat `memory-bank` dari `~/.claude.json` (backup
  `.bak-20260920`; dipertahankan `memory` karena server-memory resmi MCP yang
  direferensikan skill `autonomous-agent-harness`) → 13 → 12 server, validasi
  JSON ✓. `mcp-hygiene.py` re-run (dry-run): TOML codex 10 server, 0 `gh_*`,
  0 duplikat → bersih, tidak ada yang perlu `--apply`. `mcp-allowlist.txt`
  di-update (memory-bank dipindah ke TIER C, backup `.bak-20260920`).
  Helper kebiasaan dev: `~/receptor/dev-stack.sh` (start/stop/status/logs/
  restart stack voralens-main; PID-file + sweep jaring pengaman; uji siklus
  start→stop ✓ — detail: stack dev tidak lagi ditinggal hidup semalam).
  Catatan: app ini pakai PostgreSQL (bukan MySQL; .env pgsql 5432 db
  `voralens_v1`). queue:work exit 1 dgn "SQLSTATE[08006] Connection refused"
  saat PG mati — bukan bug script. Solusi uji: `brew services run
  postgresql@16` (run-once) → siklus start HTTP 302 ✓ → stop bersih ✓ →
  PG di-stop lagi. brew mysql service = none, mysqld memang tidak dipakai app ini.


- **2026-09-20 (2)** — **Anti-laptop-panas: bug launchd ditemukan & dimitigasi + `stop-berat.sh`.**
  Audit: RAM 8 GB free ~60 MB, swap 29–30 GB, load 25+. Penyebab campuran (bukan katalog skill):
  Docker Desktop VM 4 GB, MySQL brew service permanen, stack dev voralens 18 jam, MCP yatim,
  dan `skill-auto-symlink` yang **loop tiap 10 detik** karena `KeepAlive`+`StartInterval`
  di plist launchd. Fix: hapus `KeepAlive` (backup `.bak-20260920`) + kunci anti-loop di
  script (`.symlink-run.lock`, MIN_INTERVAL 1800 dtk; manual lewat kunci pakai `--force`;
  uji: run-2 SKIP ✓, `--force` jalan ✓). Tool baru `~/.agents/stop-berat.sh` (REVERSIBLE):
  stop container Up, quit Docker, stop mysql, kill dev stack & MCP yatim (>2 jam / PPID 1).

- **2026-09-20** — **Wiring TIERED: discovery native juga dibikin ringan.** Temuan ukur:
  MCP sudah ringan (`skills_available` 1.2 KB, `skill_search` 2.2 KB, `skill_load` 1 file),
  tapi folder `~/.claude/skills` berisi **3.174 symlink** — Claude Code memindai folder ini
  native (nama+deskripsi semua ikut konteks), dan ada farm ±16,5k symlink/tool di
  codex/gemini/trae/roo dll (total ±463k symlink; tool itu pun tidak support folder skills
  native = percuma + bikin sync berat). Solusi: **tiered wiring** — hanya ~60 skill CORE
  (daftar bisa diedit di `skill-core.json`) yang di-symlink native; sisanya via MCP.
  `sync-wire.py` (opsi `--full` = perilaku lama) + `skill-auto-symlink.py` keduanya patuh
  core-list. Eksekusi: **443.352 symlink dipangkas (76 s)**; sekarang tiap tool punya
  ±60 entri; run ulang idempotent (pangkas:0/baru:0). `skill-core.json` juga dijadikan
  sumber daftar core agar tidak ada daftar ganda.

- **2026-09-19 (4)** — MCP round-2: +desktop-commander(26 tools)+memory-bank (doctor: ALIVE) → Claude = 12 server; memory resmi dibuat PERSISTEN (MEMORY_FILE_PATH → ~/.agents/memory/memory.json). allowlist rev-2 (12 nama, allowlist lama yang 6/20 mati diganti). PANGKAS SEMUA PROVIDER: 73.652 → 191 server (claude 12 · codex 10 · 21 provider lain @9/5/2), masing-masing ada backup .bak-prune. TIER C DEAD (jangan dipakai): sqlite, duckdb, puppeteer, tokz-compress.

- **2026-09-19 (5)** — GAP-EXECUTE: (1) Provenance self-healing di build_skills_index.py (lock → skills-repo-map → heuristik gh-<owner>-<repo>/mined-*): skill dengan source 4.415 → **7.227**. (2) Kategori fallback keyword (nama+deskripsi, sumber: _categorize_roles.py) menimpa 'uncategorized': **2.320 → 252** (aktif 1909 → 152). Keduanya ikut tiap rebuild — tidak hilang lagi. Router+brief+skills-index.json regen sinkron. (3) Batch-3 miner (--registry, 80 repo × 100 skill, gate bintang ≥100) diluncurkan + auto-finalize.

- **2026-09-19 (6)** — JUNK DIHAPUS (izin user): 8.097 dir junk dihapus dari skills-expanded (daftar = logika klasifikasi index builder, dry-run dulu; record: skills-junk-paths.txt + .bak). repo-refs (1,3 GB) TETAP = referensi. Batch-3 selesai: +590 skill → 14.916 siap pakai. Builder dikasih flock (.index-build.lock) — cegah disk I/O error akibat dua build paralel. Batch-4 agresif diluncurkan (322 repo × 200).
- **2026-09-19 (7)** — EVAL HARNESS: skill-evals.json (16 kasus ID) + skill-eval.py (pass@1/3, health check, history). Engine rerank dipindah ke skill-mcp.rank_for_task (sumber tunggal) + sinonim ID→EN. Hasil: 44→75% pass@1, 81→100% pass@3. Arsip 110MB dihapus (user OK). Junk 0. Batch-4: 298 kandidat, 0 baru (sudah ter-tambang).
- **2026-09-19 (8)** — SYNC-ALL: `sync-wire.py` (hapus symlink mati/kadaluarsa, retarget expanded->curated, symlink semua tool AI, ensure MCP skill-catalog, purge mcp-usage basi) + `sync-all.sh` (satu perintah: katalog->wiring->repo->lifecycle->eval). Jalankan ulang: `bash ~/.agents/sync-all.sh` (idempotent).

- **2026-09-19 (6)** — **Progressive disclosure: protokol dibikin RINGKAS (AI tidak keberatan lagi).**
  Keluhan: blok 11 baris × 12 provider (~10 KB) + brief 19 baris (~1.2 KB)/sesi = berat.
  Kini blok selalu-on cuma ~7 baris (~440 B): "ada N skill → cari dulu + caranya + pointer";
  total ter-inject **5.275 B / 12 provider** (dulu 9.919 B, −47%). Brief sesi **9 baris/~700 B**.
  Semua detail (protokol penuh, anti-ngarang 4 poin, cara tambang/buat skill) dipindah ke
  `~/.agents/SKILL-FIRST.md` dan dibaca AI **on-demand** (saat skill tak ketemu / akan menulis
  `.md` / perlu protokol). Eval tetap hijau (pass@1 67% · pass@3 100% · jujur-negatif 86%);
  install idempotent terverifikasi (run ke-2 semua "sudah terbaru"). Prinsip: **jangan
  panjangkan blok — tambah detail ke SKILL-FIRST.md saja.**

- **2026-09-19 (5)** — **MCP + aturan skill-first untuk SEMUA 12 provider.** Akar masalah
  "AI lain tidak bisa memanggil skill": MCP `skill-catalog` memang terdaftar, tapi **9 provider
  tidak punya file aturan** sama sekali (codebuddy, hermes, trae, opencode, aider, cline,
  windsurf, continue, roo) sehingga AI-nya tidak pernah tahu skill itu ada. Dibuat file aturan
  ber-marker `<!-- skill-first:start/end -->` untuk 9 provider itu + perbaiki angka basi
  (~1.090 → **14.916**) di claude/codex/gemini + marker di `~/.claude/CLAUDE.md`.
  `install-skill-first.py` dirombak: 12 provider, kelola file aturan otomatis, **angka dibaca
  live dari indeks** (tidak bisa basi lagi), auto-bikin `mcp.json` yang belum ada (trae/cline/roo
  dibuatkan, MCP ditulis), backup otomatis. Terverifikasi: apply 0 error, **run kedua semuanya
  "sudah terbaru"** (idempotent). Sumber teks: `SKILL-FIRST.md`.

- **2026-09-19 (4)** — **Eval dinaikkan kelasnya + 3 bug rekomendasi diperbaiki.**
  `skill-eval.py` kini punya **kasus negatif** (out-of-domain) + metrik **jujur-negatif**
  (sistem harus *tidak pede* di domain yang tidak ada skillnya) dan gate exit-code.
  Bug nyata yang terbukti dari eval & diperbaiki di `skill-mcp.py`:
  (a) cocok **substring** → `nasi` nyasar ke `nasiko-control-plane` (kini word-boundary);
  (b) token `go` di KEEP_SHORT → task "pokemon go" merekomendasikan `golang-patterns` (token dibuang);
  (c) **teknologi bentrok** → task golang malah dapat `dart-add-unit-test` (kini boost +15 bila
  teknologi cocok, −15 bila bentrok). Ditambah sinonim ID→EN (riset/migrasi/ekstrak/teks/…).
  Skor dipisah: **sinyal** (kecocokan murni) vs **urutan** (+bonus tier), jadi "sok tahu" terukur.
  Hasil: **pass@1 67% · pass@3 100% · jujur-negatif 86%** (sebelum: 43%). 1 kasus negatif sisa
  (`reset password wordpress` → `automated-password-reset-flow`) dinilai wajar karena skill-nya relevan.
  Satu kasus eval lama (`pokemon go`) diperbaiki labelnya — katalog memang punya `pokemon-player`.

- **2026-09-19 (3)** — GAP ditutup: `skill-miner.py` (tambang SKILL.md dari repo komunitas: superpowers/anthropics/awesome-copilot/ComposioHQ + discovery otomatis → registry 322 repo; dedup nama+md5) dan `skill-factory.py` (bikin skill baru meniru struktur referensi curated teratas). `build_skills_index.py` dipatch: scan nested `mined-*` (kedalaman 2). Batch-1: +116 skill baru (13.509 → 13.623 tier-1). Skill baru contoh: `voralens-api-conventions` (dibuat factory dari referensi api-contract-normalizer). Batch-2 jalan di background (MINER_LIMIT=900).

- **2026-09-19 (2)** — `mcp-doctor.py`: probe handshake MCP nyata → 11 ALIVE / 3 DEAD (tokz-compress, sqlite, puppeteer) / 4 BUTUH-KEY (firecrawl, tavily, brave-search, github). Allowlist ditulis ulang berbasis hasil tes; Tier A (10 server) dipasang ke Claude Code user-scope (backup .claude.json.bak-tierA); context7 entri lama rusak diganti npx @upstash/context7-mcp — hasil akhir 10/10 Connected. Puppeteer→playwright, sqlite-archived.

- **2026-09-19** — Skill-first penuh: katalog 13.509 skill aktif (cap dibuka, tier junk 7.304 dipisah); MCP lifecycle manager (`mcp-lifecycle.py`: --on/--off/--gc/--gc-if-due, keep-set core, grace bootstrap, GC maks 1x/minggu 200 server/pass); repo registry komunitas 66 repo dedup (`repo-registry.py --fetch`); skill-catalog MCP terpasang di 6 provider JSON; skill wired ke 9 provider (incl. cline, windsurf); `session-brief.sh` kini menghitung MCP semua provider + memicu gc-if-due. Backup: *.bak-skillfirst, *.bak-lifecycle.

- `mcp-dynamic-proxy.json` (tool MCP `:27125`) → **disabled**: port tidak listening dan
  `skills-catalog/` (gzip yang dibacanya) sudah tidak ada. Pengganti: `skill-search.sh`.
- `skill-graph-api.py` / `repo-ref-api.py` / `skill-auto-tuner.py` / `smart-symlink-bridge.sh`
  semuanya berpatokan ke `skills-catalog/` atau port mati → **jangan diandalkan**.
- launchd: plist `skill-auto-symlink` / `skill-graph-api` / `repo-ref-api` **terpasang tapi
  tidak dimuat**; yang aktif hanya `com.agents.legakan`. Jalankan manual dulu
  (`python3 skill-auto-symlink.py`) sampai keputusan P1.
- Rencana lanjutan: `../../.agents` P1 = backfill provenance, GC arsip 110 MB,
  rapikan 2.694 uncategorized, isi/hapus layer belajar yang masih kosong.

## P0 selesai 2026-09-18 (ringan, reversible)

| Item | Sebelum | Sesudah |
|---|---|---|
| Nama rusak di index | 5.753 (23%) | **0** |
| Deskripsi kosong | 13.996 | 13.955 (dipindah ke tier `docs`, bukan dibuang) |
| Tier | 2 (curated/reference) | **3** (+`docs`, +kolom `category`, `source`) |
| Duplikat nama | 2.025 tidak ter-collapse | **ter-collapse** (total 24.560 → 22.590 kanonik) |
| Skill curated tanpa deskripsi | 21 (`description: ">"`) | **0** (fold + fallback heading) |
| Rebuild index | ~panjang (baca file penuh) | **6 detik** (head 4 KB → fallback 64 KB) |
| MCP codex | 4.334 server / 679 KB | **322 server / 42 KB** (backup ada) |
| `~/.claude/skills` | 0 skill | **12 symlink** |
| repo voralens-v2 | 0 | **11 symlink** relatif |
| Cari skill | port mati `:27125` | **`skill-search.sh`** + **MCP `skill-catalog`** (✔ Connected) |
| Cara AI liat skill | tidak ada | **hook SessionStart** (720 B/sesi) + instruksi di CLAUDE.md/AGENTS.md/GEMINI.md |
| MCP skill tool | 0 | **5 tool** (`skill_for_task` bahasa natural) · terpasang di claude+codex+gemini+codebuddy |
| Relevansi cari | AND (kalimat natural = 0 hasil) | **OR + bm25 + bonus curated + fallback LIKE** |

Catatan kejujuran: dugaan awal "12 tool menyimpan klon penuh" **salah** — farm itu
memang **symlink** (per-skill). Masalah sebenarnya adalah cakupan & kebersihan
(61 tool ter-wire, tapi `.claude` justru kosong), bukan duplikasi disk.

Langkah opsional berikutnya (belum dijalankan, butuh keputusan):
kurasi MCP ke ≤20 server → `python3 mcp-hygiene.py --keep mcp-allowlist.txt --apply`
(dry-run sekarang: 322 → 20).
