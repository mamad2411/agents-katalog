# ⚡ SHORTCUT — 90% kebutuhan harian (detail lengkap: COMMANDS.md)

```bash
# 🔍 CARI & MUAT SKILL (WAJIB sebelum kerja apa pun)
python3 ~/.agents/skill-search.sh "<kata kunci>"        # cari skill
python3 ~/.agents/skill-search.sh --load "<nama>"        # baca isi SKILL.md
# atau lewat MCP: skill_for_task(task="<tugas>") → skill_load("<nama>")

# 🔄 SEGARIKAN SEMUA (katalog + wiring + MCP + eval) — idempotent
bash ~/.agents/sync-all.sh --fast                        # ±1 menit

# 🛡️ KEAMANAN & KUALITAS
python3 ~/.agents/skill-sec-scan.py --quick              # scan keamanan (cepat)
python3 ~/.agents/skill-bench.py                         # cek kualitas routing
python3 ~/.agents/skill-eval.py                          # pass@1/pass@3 + health

# 📚 KATALOG
python3 ~/.agents/build_skills_index.py                  # bangun ulang index
python3 ~/.agents/skills-index-md.py && python3 ~/.agents/skills-router.py

# 🔌 MCP & HOOK
bash ~/.agents/session-brief.sh                          # brief konteks sesi
python3 ~/.agents/mcp-hygiene.py                         # audit kebersihan MCP
python3 ~/.agents/mcp-lifecycle.py                       # nyala/parkir MCP
bash ~/.agents/sync-wire.py                              # wiring symlink per tool

# 🧠 KONTRAK SEMUA AI (yang tanpa hook)
python3 ~/.agents/install-skill-contract.py --check      # cek mana sudah punya

# ⛏️ TAMBAH SKILL
python3 ~/.agents/skill-miner-skillsh.py --limit 300     # ambil dari skills.sh
python3 ~/.agents/skill-factory.py "<topik>" "<desc>"    # buat skill baru
bash ~/.agents/mine-daemon.sh status                     # status mining 100k

# 💾 RAM & PERAWATAN
bash ~/.agents/stop-berat.sh                             # matikan proses berat
python3 ~/.agents/sync-all.sh --fast                     # bersihkan lifecycle
```

**Aturan emas:** 1) cari skill dulu · 2) muat yang relevan · 3) kerjakan · 4) verifikasi · 5) lapor jujur.

---

# COMMANDS.md — Daftar Semua Perintah `~/.agents`

Semua perintah aman diulang (idempotent). Sumber tunggal skill: `~/.agents/skills-store`.

---

## ⭐ HARIAN / UTAMA

```bash
# SATU PERINTAH SEGALA HAL: katalog segar + hapus kadaluarsa + symlink semua AI +
# MCP skill-catalog + repo scope + lifecycle + eval kesehatan
bash ~/.agents/sync-all.sh              # full (run pertama ±10 mnt, berikutnya cepat)
bash ~/.agents/sync-all.sh --fast       # ringan: wiring + MCP + eval saja (tanpa rebuild katalog)

# Cari skill (bahasa natural / kata kunci)
~/.agents/skill-search.sh "query lambat di postgres"
~/.agents/skill-search.sh --tier curated "vue page"
~/.agents/skill-search.sh --load "playwright"        # baca isi SKILL.md skill

# Baca brief konteks sesi (yang disuntik ke semua AI)
bash ~/.agents/session-brief.sh
```

## 🧠 HEMAT KONTEKS & LIMIT (audit 2026-09-26 — limit harian/mingguan cepat habis)

Latar terukur: 4,42 **miliar** token terpakai, 3 sesi @ 59/54/18 MB → tiap pesan membaca ulang
**±500.000 token**. Bukan modelnya yang boros — sesinya yang tidak pernah ditutup.

```bash
# Muat skill TANPA membanjiri konteks (≤80 baris / ≤2 KB; tetap dapat esensinya)
bash ~/.agents/skill-load-lite.sh <nama>            # default 80 baris/2 KB
bash ~/.agents/skill-load-lite.sh <nama> --lines 40 # lebih ringkas
bash ~/.agents/skill-load-lite.sh --list "kata kunci"  # cari kandidat dulu (5 baris)
bash ~/.agents/skill-load-lite.sh <nama> --full     # baca penuh (sadar biaya, jarang perlu)

# Ukur, jangan menebak
python3 ~/.agents/ai-context-audit.py               # SEMUA tool AI: ukuran sesi, pesan, gambar base64
python3 ~/.agents/ai-context-audit.py --json        # mesin (untuk hook/cron)
python3 ~/.agents/usage-audit.py                    # token 7 hari + model + sesi terboros (Claude)
python3 ~/.agents/usage-audit.py --days 14 --json   # mesin (idempoten)
python3 ~/.agents/audit-cline.py                    # Cline CLI: token kumulatif + output terbesar
python3 ~/.agents/audit-cline.py --top 15           # 15 pesan terbesar
python3 ~/.agents/context-guard.py --report         # sesi >10 MB (bom waktu limit)

# Aturan hemat ke file rules SEMUA tool (idempoten, backup .bak-YYYYMMDD)
python3 ~/.agents/install-context-guard.py          # dry-run: rencana per tool
python3 ~/.agents/install-context-guard.py --apply  # pasang blok context-guard
python3 ~/.agents/install-context-guard.py --check  # status 17 target

# Ramping MCP lintas tool (hanya skill-catalog + mcp-router yang tersisa)
python3 ~/.agents/mcp-slim-all.py                   # dry-run: daftar file + server dilepas
python3 ~/.agents/mcp-slim-all.py --apply           # tulis + parkir ke mcp-parked.json

# Anti-LOOP (audit 2026-10-03: limit habis karena agen berputar, bukan pesan panjang)
# Loop-guard menghitung tool call per sesi (file kecil /tmp, bukan token).
# Dipasang otomatis: hook PreToolUse Claude (patch-settings-20261003.py) +
# hook UserPromptSubmit Cline — counter per sesi, 80 lunak / 200 atau 500 pesan keras.
# tuning ambang: LOOP_WARN_N / LOOP_HARD_N / LOOP_MSG_N (default 80 / 200 / 500)
# kalau butuh kembalikan hook lama: cp ~/.claude/settings.json.bak-20261003 ~/.claude/settings.json

## 🔥 PANAS & SSD (audit 2026-10-03)
python3 ~/.agents/device-guard.py             # laporan read-only: loop mining, agent 24/7, churn B/s
python3 ~/.agents/device-guard.py --apply     # stop loop saturasi + bootout 24/7 + interval 30mnt→6jam
# restore perubahan: lihat ~/.agents/.device-guard-log.json (kunci "restore")
bash ~/.agents/wire-skills-role.sh --list     # 12 preset role pack (skill curated per kategori)
bash ~/.agents/wire-skills-role.sh <preset> <repo> [--apply]  # symlink relatif, tidak hapus apa pun
# CAP_PER_KAT=20 bash ~/.agents/wire-skills-role.sh backend /repo --apply

# Hook (otomatis; tidak perlu dipanggil manual)
bash ~/.agents/context-guard.sh                     # hook Claude: 0 token di bawah ambang, 1 baris di atasnya
python3 ~/.agents/cline-guard.py                    # hook Cline: deteksi sesi/gambar base64 (48 ms)
python3 ~/.agents/skill-flow.py --stats             # injeksi skill per sesi (batas 400 B, dedupe)
python3 ~/.agents/skill-flow.py --eval              # gerbang mutu routing (harus 31/31 lulus)

# Pemasangan ulang (idempoten; membuat backup .bak-YYYYMMDD)
python3 ~/.agents/patch-settings-20260926.py        # hook context-guard + permissions.deny
```

Ambang bisa diubah lewat env: `CONTEXT_WARN_MB` (default 10), `CONTEXT_URGENT_MB` (25),
`CONTEXT_STEP_MB` (5), `SKILL_FLOW_MAX_BYTES` (400), `SKILL_FLOW_STATE_TTL` (21600 s —
setelah ini, skill diumumkan ulang untuk tool yang tidak kirim `session_id`),
`CLINE_GUARD_MSGS` (200), `CLINE_GUARD_MB` (10), `CLINE_GUARD_IMG_MB` (2),
`AMBANG_MB` (10) dan `AMBANG_PESAN` (200) untuk `ai-context-audit.py`.

Aturan `permissions.deny` yang dipasang (blokir `Read` ke file tak relevan, docs resmi
Claude Code "large codebases"): `./**/vendor/**`, `./**/node_modules/**`, `./**/dist/**`,
`./**/public/template/**`, `./**/skills-expanded/**`, `./**/*.min.js`.
Butuh satu baris dari file itu? `sed -n '120,130p' path` via shell — jangan `Read` penuh.

## EVAL & KUALITAS
```bash
python3 ~/.agents/skill-eval.py         # pass@1/pass@3 + jujur-negatif + health katalog (history otomatis)
cat ~/.agents/skill-evals.json          # test-case-nya (positif + negatif/out-of-domain)
cat ~/.agents/skill-eval-results.json   # riwayat hasil
```

## PASANG KE SEMUA AGEN (MCP + aturan skill-first)
```bash
python3 ~/.agents/install-skill-first.py            # dry-run: lihat apa yang akan ditulis
python3 ~/.agents/install-skill-first.py --apply    # tulis ke 12 provider (backup .bak-YYYYMMDD)
# hasil: MCP skill-catalog + blok <!-- skill-first:start --> di file aturan tiap provider
# angka skill di blok itu AUTO dibaca dari skills-index.json (tidak pernah basi)
```

### Progressive disclosure (biar AI tidak "keberatan" konteksnya)
Blok yang ter-inject sengaja RINGKAS (~7 baris: cari skill + caranya + pointer), detail
tidak di-inject — AI membaca `~/.agents/SKILL-FIRST.md` on-demand saat: skill tak ketemu,
akan menulis file `.md`, atau butuh protokol/anti-ngarang penuh. Total injected:
~5.3 KB / 12 provider (dulu ~10 KB) + brief sesi ~700 B (dulu ~1.2 KB). Jangan panjangkan
blok; tambah detail baru ke `SKILL-FIRST.md` saja.

### Wiring TIERED (biar discovery native juga ringan)
`sync-wire.py` kini hanya men-symlink skill CORE (daftar: `~/.agents/skill-core.json`,
bebas diedit; default = 77 skill flow harian) ke folder `skills` tiap tool. Sisa entri
katalog (3.176 curated / 67.550 total) tetap
bisa dipakai SEMUA AI via MCP (`skill_for_task`/`skill_search`/`skill_load`, ±1–2 KB per
panggilan) atau `skill-search.sh`. Alat yang ikut patuh: `skill-auto-symlink.py` (auto-link
hanya core; `--full` untuk perilaku lama). Pangkas besar pertama: 443.352 symlink (76 s).

### Laptop panas / RAM penuh (8 GB) — pakai `~/.agents/stop-berat.sh`
Auditan 2026-09-20: laptop 8 GB free-nya cuma ~60 MB, swap 29–30 GB, load 25+. Pelaku:
Docker Desktop (VM 4 GB + 17% CPU padahal AutoStart=false), MySQL brew service (jalan
sejak boot), stack dev voralens 18 jam, ±15 MCP yatim, dan **bug launchd**:
`skill-auto-symlink` sempat loop tiap 10 dtk (kombinasi `KeepAlive`+`StartInterval`) —
sudah diperbaiki: `KeepAlive` dihapus dari plist + **kunci anti-loop** di script
(MIN_INTERVAL 1800 dtk via `.symlink-run.lock`, lewat manual pakai `--force`).
Semua pematian REVERSIBLE: data database/container utuh; nyalain balik via
`brew services start mysql`, buka Docker Desktop + `docker start <nama>`, atau
jalankan lagi dev stack voralens (`concurrently ...`).
Rekomendasi Docker Desktop (sekali, dari app-nya): Settings → Resources →
**Memory 4 GB → 2 GB** (laptop 8 GB), dan matikan "Enable Docker AI".

## TAMBAH SKILL BARU (komunitas / buat sendiri)
```bash
MINER_LIMIT=900 python3 ~/.agents/skill-miner.py          # tambang repo komunitas (dedup otomatis)
python3 ~/.agents/skill-miner.py --registry               # dari repo-registry.json (bintang >=100)
REG_MAX_REPOS=80 REG_LIMIT_PER_REPO=100 python3 ~/.agents/skill-miner.py --registry  # batasi
python3 ~/.agents/skill-factory.py "<nama>" "<deskripsi>" # bikin skill baru meniru referensi curated
python3 ~/.agents/skill-factory.py --analyze <nama-referensi>  # bedah struktur referensi
# setelah nambang: bash ~/.agents/sync-all.sh   (auto-rebuild + wire ke semua AI)
```

## KATALOG / INDEX
```bash
python3 ~/.agents/build_skills_index.py   # rebuild DB (FTS5, 3-tier, provenance, dedup)
python3 ~/.agents/skills-router.py        # regen SKILLS-AVAILABLE.md + skills-index.json
python3 ~/.agents/skills-index-md.py      # regen skills-INDEX.md (ringkasan manusiawi)
python3 ~/.agents/_categorize_roles.py    # pemetaan role -> skill (role-skill-map.json)
python3 ~/.agents/skill-graph-api.py      # API graf skill+memory (port 27125, optional, launchd: disabled)
```

## MCP — AUDIT / KURASI / SIKLUS HIDUP / DOKTER
```bash
python3 ~/.agents/mcp-hygiene.py                            # laporan (dry-run)
python3 ~/.agents/mcp-hygiene.py --apply                    # prune junk + backup
python3 ~/.agents/mcp-hygiene.py --keep ~/.agents/mcp-allowlist.txt --apply  # kurasi ke keep-list
python3 ~/.agents/mcp-doctor.py                             # tes handshake semua MCP (ALIVE/DEAD)
python3 ~/.agents/mcp-lifecycle.py                          # status nyala/parkir
python3 ~/.agents/mcp-lifecycle.py --on <nama>              # aktifkan
python3 ~/.agents/mcp-lifecycle.py --off <nama>             # parkir
python3 ~/.agents/mcp-lifecycle.py --gc 14                  # parkir yang >14 hari tak dipakai
python3 ~/.agents/mcp-lifecycle.py --gc-if-due              # GC mingguan (dipanggil session-brief)
```

## WIRING (SYMLINK) MANUAL
```bash
bash ~/.agents/link-skills-min.sh --repo /path/ke/repo    # scope repo → <repo>/.claude/skills
bash ~/.agents/link-skills-min.sh --tool ~/.claude/skills starter  # set ringkas
bash ~/.agents/link-skills-min.sh --tool ~/.roo/skills all-curated # full katalog
bash ~/.agents/link-skills-min.sh --status                # cek kondisi wiring semua tool
python3 ~/.agents/sync-wire.py                            # bagian [2/5] sync-all saja
python3 ~/.agents/install-skill-first.py --apply          # pasang MCP+hook+instruksi ke semua agen
```

## REPO REFERENSI
```bash
python3 ~/.agents/repo-registry.py --fetch    # ambil repo komunitas (awesome-list) → repo-registry.json
bash ~/.agents/clone-repo-refs.sh             # klon/refresh dump repo → ~/.agents/repo-refs
python3 ~/.agents/repo-ref-fetch.py <owner/repo>        # tambah satu repo referensi
curl -s localhost:27126/repos/readme?p=<owner/repo>     # baca dump via API (jika server hidup)
```

## SETUP AWAL / PEMELIHARAAN
```bash
python3 ~/.agents/install-skill-first.py            # pasang skill-first protocol semua agen
bash ~/.agents/cleanup-skill-junk.sh                # hapus dir junk (pakai skills-junk-paths.txt)
python3 ~/.agents/upgrade_demand.py                 # refresh upstream skill (log: upgrade-demand-log.json)
python3 ~/.agents/skill-auto-tuner.py               # tuning parameter (optional)
```

## 🛡️ KEAMANAN & KUALITAS SKILL (2026-09-24)

```bash
# Scan keamanan statis seluruh katalog (tidak menjalankan isi file)
python3 ~/.agents/skill-sec-scan.py                  # penuh (store+expanded+repo-refs)
python3 ~/.agents/skill-sec-scan.py --quick          # tanpa repo-refs (lebih cepat)
python3 ~/.agents/skill-sec-scan.py --since 20260924 # delta: hanya file baru
python3 ~/.agents/skill-sec-scan.py --test           # self-test pola (14 kasus)
# hasil: ~/.agents/security-scan-<UTC>.txt — CRIT/HIGH/MED, TIDAK menghapus apa pun

# Audit katalog curated (nama/deskripsi rusak; buat daftar review, tidak hapus)
python3 ~/.agents/skill-curate.py --report           # 3.176 curated → 3.161 bersih, 15 review
python3 ~/.agents/skill-curate.py --dry-run          # lihat kandidat tanpa menulis
python3 ~/.agents/skill-curate.py --apply            # tulis skills-review.txt + skills-curated-clean.txt

# Benchmark retrieval (precision@k pakai mesin produksi skill-mcp)
python3 ~/.agents/skill-bench.py                     # 12 prompt Indonesia, k=3
python3 ~/.agents/skill-bench.py --k 5 --tier curated --verbose
```

## ⛏️ TAMBUH SKILL MENUJU 100K (2026-09-24)

```bash
# Miner skills.sh: 20.000 entry, pakai raw.githubusercontent (TIDAK kena rate limit API)
python3 ~/.agents/skill-miner-skillsh.py --probe 20  # dry-run: cek hit rate
python3 ~/.agents/skill-miner-skillsh.py --limit 300  # coba 300 entry
python3 ~/.agents/skill-miner-skillsh.py             # semua 20.000 (bg: nohup + log)

# Orkestrator batch: mine → scan delta → rebuild index → cek total
bash ~/.agents/mine-to-100k.sh 1 600 80              # batch 1: 600 repo, 80/repo

# Daemon tmux (loop otomatis ke 100k, lepas dari terminal)
bash ~/.agents/mine-daemon.sh start                  # GH_TOKEN opsional (5.000/jam vs 60/jam)
bash ~/.agents/mine-daemon.sh status | stop
```

## 🧠 KONTRAK SKILL SEMUA AI (yang tidak punya hook)

```bash
python3 ~/.agents/install-skill-contract.py          # pasang kontrak ke 14 file rules
python3 ~/.agents/install-skill-contract.py --check   # audit: mana sudah punya kontrak
# AI tanpa hook (Cursor, Windsurf, Aider, Continue, Trae, Roo, Qwen, OpenCode, Pi, Kilo)
# dapat kontrak "WAJIB cari & muat skill" lewat file rules masing-masing.
```

## 🔌 INTERNAL (dipakai hook; biasanya tidak perlu dipanggil manual)

```bash
python3 ~/.agents/skill-flow.py --test "<prompt>"    # uji routing skill
python3 ~/.agents/skill-flow.py --check              # skill flow hilang?
python3 ~/.agents/skill-flow.py --render             # tulis SKILL-FLOW.md
curl -s localhost:27126/repos/readme?p=<owner/repo>     # baca dump via API (jika server hidup)
python3 ~/.agents/repo-ref-api.py --search <kata>       # cari isi repo via API (server lokal)

python3 ~/.agents/skill-rank.py "<prompt>"           # 3 skill teratas (dipakai hook)
bash ~/.agents/skill-inject.sh                       # output hook (stdin JSON prompt)
python3 ~/.agents/skill-inject-gemini.py             # hook versi Gemini (BeforeAgent)
python3 ~/.agents/mcp-router.py                      # gateway MCP on-demand (3 tool)
python3 ~/.agents/build-mcp-catalog.py               # katalog MCP untuk router
```

## 🧹 PERAWATAN (jarang dipakai, tapi perlu tahu)

```bash
python3 ~/.agents/fix-skill-name-canonical.py        # kanonik nama skill (kebab-case)
python3 ~/.agents/fix-repo-refs.py                   # perbaiki path repo-refs
python3 ~/.agents/skill-learn.py                     # catat skill baru dari pemakaian
python3 ~/.agents/skill-health.py                    # ringkasan kesehatan katalog
python3 ~/.agents/confkit-extract.py                 # ekstrak conf dari repo
python3 ~/.agents/split-style-categories.py          # pecah STYLE-*.md jadi sub-kategori
bash ~/.agents/cleanup-skill-junk.sh                 # bersihkan junk (butuh izin user)
bash ~/.agents/smart-symlink-bridge.sh              # jembatan symlink pintar
python3 ~/.agents/skill-auto-tuner.py                # auto-tune ambang rank
python3 ~/.agents/mass-repo-cloner.py                # clone massal ke repo-refs
python3 ~/.agents/link-skills-repos.py               # link skill ke repo scope
```

## 🔌 MCP PROXY (legacy — router modern lebih disarankan)
```bash
python3 ~/.agents/mcp-proxy-manager.py                # kelola proxy MCP (legacy)
```

## 🔁 UPLOAD / LINK WATCHER (sinkronisasi)

```bash
python3 ~/.agents/upload-links.py                    # upload daftar link
bash ~/.agents/upload-chain.sh                      # rantai upload
bash ~/.agents/upload-link-watcher.sh                # watcher (jarang jalan)
bash ~/.agents/upload-link-watcher2.sh               # watcher v2
```


## ARTIFAK PENTING (jangan edit manual — generated)
```
skills-index.db          DB FTS5 seluruh katalog          build_skills_index.py
skills-index.json        katalog tier-1 untuk MCP         skills-router.py
SKILLS-AVAILABLE.md      daftar skill siap pakai          skills-router.py
SKILLS-CATEGORIES.md     per kategori                     skills-router.py
skills-junk.txt          daftar junk                      build_skills_index.py
mcp-hygiene-report.md    laporan MCP                      mcp-hygiene.py
sync-wire-log.json       audit hapus/wiring               sync-wire.py
mcp-usage.json           pemakaian MCP (untuk GC)         skill-mcp.py (otomatis)
memory/memory.json       graf pengetahuan (persisten)     server 'memory'
```

## ROLLBACK
```bash
# setiap perubahan file config/back-nya dibuat otomatis: *.bak-YYYYMMDD / *.bak-sync / .bak-prune
cp ~/.codex/config.toml.bak-YYYYMMDD ~/.codex/config.toml
cp ~/.agents/skills-junk-paths.txt.bak-YYYYMMDD ~/.agents/skills-junk-paths.txt
# rollback audit hemat konteks 2026-09-26 (kalau perlu kembali ke perilaku lama):
cp ~/.agents/skill-flow.py.bak-20260926 ~/.agents/skill-flow.py
cp ~/.agents/AGENTS.md.bak-20260926 ~/.agents/AGENTS.md
cp ~/.agents/CHEATSHEET.md.bak-20260926 ~/.agents/CHEATSHEET.md
cp ~/.agents/COMMANDS.md.bak-20260926 ~/.agents/COMMANDS.md
cp ~/.claude/settings.json.bak-20260926 ~/.claude/settings.json
cp ~/.claude/CLAUDE.md.bak-20260926 ~/.claude/CLAUDE.md
cp ~/AI_TOKEN_GUARD.md.bak-20260926 ~/AI_TOKEN_GUARD.md
rm -f /Users/chaali0324/receptor/.claude/settings.json   # deny Read repo-level
# rollback ramping MCP 19 tool (kembalikan 8-9 server ke tiap tool):
for f in ~/.aider ~/.antigravity ~/.codebuddy ~/.codeium ~/.codex ~/.continue ~/.copilot \
         ~/.dolphin ~/.gemini ~/.goose ~/.hermes ~/.kiro ~/.mistral ~/.openclaude \
         ~/.opencode ~/.orca ~/.qwen ~/.tabnine ~/.windsurf; do
  [ -f "$f/mcp.json.bak-20260926" ] && cp "$f/mcp.json.bak-20260926" "$f/mcp.json"; done
# atau hidupkan per-server tanpa rollback penuh:
python3 ~/.agents/mcp-lifecycle.py --on playwright
# rollback blok "hemat konteks" di file rules (blok ditandai context-guard:start/end):
for f in ~/.codex/AGENTS.md ~/.gemini/GEMINI.md ~/.cline/.clinerules ~/.windsurf/.windsurfrules \
         ~/.continue/.continuerules ~/.roo/.roorules ~/.qwen/QWEN.md ~/.aider/CONVENTIONS.md \
         ~/.opencode/AGENTS.md ~/.codebuddy/AGENTS.md ~/.hermes/AGENTS.md ~/.trae/AGENTS.md; do
  [ -f "$f.bak-20260926" ] && cp "$f.bak-20260926" "$f"; done
rm -f ~/.openclaude/CLAUDE.md ~/.iflow/AGENTS.md   # dua file yang baru dibuat
rm -f ~/.cline/hooks/UserPromptSubmit.py.bak-20260926 2>/dev/null
# pulihkan hook Cline lama (buang panggilan cline-guard):
#   edit ~/.cline/hooks/UserPromptSubmit.py → hapus blok "cline-guard"
# rollback arsip sesi 2026-09-27 (kembalikan sesi ke daftar resume):
#   daftar path: ~/ARCHIVE-MANIFEST-20260927.txt
mv ~/.claude/archived-projects/-Users-chaali0324-receptor/<uuid>.jsonl ~/.claude/projects/-Users-chaali0324-receptor/
# rollback arsip OTOMATIS mingguan (samakan: pindahkan balik file yang dibutuhkan):
#   lihat ~/ARCHIVE-MANIFEST.txt lalu mv setiap file ke path asalnya (tercantum di manifest)
python3 ~/.agents/archive-sessions.py --dry-run       # dulu lihat kandidatnya
mv ~/.cline/archived-sessions/<session-id> ~/.cline/data/sessions/
# skrip baru (aman dihapus; tidak ada yang memanggil kalau hook dicabut):
#   context-guard.py/.sh · skill-load-lite.sh · usage-audit.py/.sh · patch-settings-20260926.py
#   mcp-slim-all.py · audit-cline.py · cline-guard.py · ai-context-audit.py · install-context-guard.py
```
