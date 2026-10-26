# ~/.agents — Katalog Skill & Konfigurasi Agen (entry point)

[![CI](https://github.com/mamad2411/agents-katalog/actions/workflows/ci.yml/badge.svg)](https://github.com/mamad2411/agents-katalog/actions/workflows/ci.yml)

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
| `context-guard.py/.sh` | hook penjaga konteks: 0 token di bawah ambang, 1 baris kalau sesi >10 MB | ✅ aktif |
| `skill-load-lite.sh` | muat skill ringkas (≤80 baris/≤2 KB) — skill tetap dipakai, konteks tetap hemat | ✅ |
| `usage-audit.py/.sh` | ukur token harian/7 hari + sesi terboros dari transcript lokal (read-only) | ✅ |
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

## Status & drift (diverifikasi 2026-10-08)

- **2026-10-08 🎯 TARGET 100K TERCAPAI: index 100.079 entri (dari 69.967).**

  Sumber: **GitHub topic repo-search** (`topic-mine.py`, 5 jilid, 114 topic × 5-15 page,
  ~40rb repo unik) — SEMUA jalan background `nice -n 15` (nggak panas), token `gh auth`
  (keyring, TIDAK ditulis ke file/log). Fetch via raw.githubusercontent (no rate limit).
  - Struktur: curated 3.176 (bersih 99%) · reference ~89rb · junk ~7,9rb · repo-refs 15.929.
  - **Dimensi baru**: `SKILLS-CONCEPTS.md` + `SKILLS-FLOWS.md` (konsep & alur lifecycle,
    generator `concept-flow-map.py`, auto via chain) + 3 role baru (agent-orchestrator/
    agent-memory/agent-ux) + `_override-*` di `_categorize_roles.py` (keyword spesifik
    menang atas backend generik; homonim diverifikasi aman).
  - **Token-hemat**: `TOKEN-SAVER.md` (peta AMAN/MAHAL/RACUN) jadi langkah tangga #1 di
    AGENTS.md; header SKILLS-AVAILABLE larang baca utuh.
  - File pendukung: `mine-chain-100k.sh`, `topic-chain2.sh`, auto-rebuild loop 25 menit
    (`/tmp/mine100k/auto-rebuild.sh`). Backup: `*.bak-20261004`, `*.bak-20261006*`.
  - Catatan: yield unik menipis di akhir (duplikat ~80%) — buat nambah lagi butuh sumber
    BARU lagi (topic tak tersentuh / code-search varian), BUKAN ulang topic lama.

## Status & drift (diverifikasi 2026-09-25)

- **2026-10-03 (2) — PANAS/SSD + subagent & skill per-kategori (pinter, bukan murahan).**

  User minta: hemat + jangan bikin device panas + tetap pinter + rekomendasi subagent
  & skill/MCP/repo per kategori. Audit nyata:
  - 🔴 **Loop mining jalan 8,2 HARI** di tmux (`while true` → GitHub API → tulis
    log/state tiap 10 dtk; log 1,3 MB; mining sudah SATURASI per AGENTS.md sendiri)
    + 2 launchd **KeepAlive 24/7** (`repo-ref-api`, `skill-graph-api` — port-nya sendiri
    didokumentasi mati) + 2 launchd **tiap 30 menit** (`legakan`, `skill-auto-symlink`).
  - ⚠️ **TEMUAN KEAMANAN**: token GitHub (`ghp_…`) **terekspos di cmdline proses**
    (terlihat via `ps` biasa) dan ikut termasuk di log `/tmp/ghchain.log` +
    tmux tmux server. **SARAN: ROTATE token itu sekarang** di GitHub → Settings →
    Developer settings → Personal access tokens, dan jangan export di cmdline
    (pakai file 600). Saya tidak mengulang nilainya di mana pun.
  - **`device-guard.py` (BARU)**: `--report` read-only (CPU/RAM, umur tmux, churn B/s,
    interval launchd, kandidat stop) · `--apply` (opt-in, backup): stop loop saturasi,
    bootout 2 agent 24/7, interval 1800→21600 dtk. Restore: `.device-guard-log.json`.
    Hasil terukur: tmux **kosong**, loop mining **0**, agent 24/7 **0**, legakan
    **21600 s**, CPU idle 46→67% (1 sampel). Yang TIDAK tersentuh: docker, dev-stack,
    cline, 9router (semua masih hidup — diverifikasi).
  - **`wire-skills-role.sh` (BARU)** — "role pack": 12 preset (backend/frontend/fullstack/
    data/ai/design/qa/devops/security/mobile/docs/core) → pilih skill **curated** dari DB
    by `category` (cap `CAP_PER_KAT=10`/kategori) → symlink relatif ke `<repo>/.claude/skills`.
    Alternatif lama ditolak: `role-skill-map.json` ternyata berisi **nama tier expanded
    sampah** (`CODE_OF_CONDUCT-ml`, `CacheStorage`) → tidak layak wiring.
    2 bug ditangkap uji sebelum dipakai nyata: (1) path symlink hardcode `../../../…`
    → salah utk semua lokasi repo; (2) `/tmp` macOS → `/private/tmp` bikin relpath salah
    → pake `realpath` + fallback absolut kalau >6 level. Uji lolos utk repo di dalam HOME
    & di `/tmp`.
  - **AGENTS.md**: (a) §Pakai subagent (default TANPA · maks 3 paralel · 1 tujuan ·
    brief ≤30 baris · satu penulis · model murah utk eksplorasi · verifikasi di penulis
    utama), (b) §Tangga progressive disclosure 7 langkah (FTS cari → kartu 120 B →
    skill-load-lite ≤2 KB → SKILL.md penuh hanya perlu → repo-ref-api search jangan
    klon → MCP on-demand → role pack wiring). Ini konsep "bagus" yang ditanya: satu
    tangga, setiap langkah lebih murah, tidak pernah lompat ke langkah mahal duluan.
  - Dokumentasi: `CHEATSHEET.md` (3 baris baru), `COMMANDS.md` §🔥PANAS & SSD.


- **2026-10-03 (1) — Limit habis KARENA LOOP, bukan pesan panjang (audit tok-tok).**

  User: "Claude sama AI lain masih boros". Audit transcript lokal (bukan tebakan):
  **02 Okt = ±532 jt token dalam 1.223 pesan** (±10× rata-rata harian Sep).
  Pola loop: spawn agent → baca → edit → gagal → validasi → `needs_fixes` → ulangi
  tanpa batas. Opus tidak terlibat (nol pesan opus sejak 24 Sep) dan semua
  agent file tidak memaksa model (default sonnet ikut `settings.json`).
  Tokenisasi/RAG **tidak** direkomendasikan sebagai jawaban: tokenisasi milik
  provider (tidak bisa diubah) + caching tidak mengurangi hitungan limit, dan
  RAG tetap memakan token IN untuk setiap potongan yang dibaca.

  **Perbaikan: `loop-guard.py` (BARU) — penghitung loop per sesi, 0 token saat normal.**
  - Hook **PreToolUse Claude** (via `patch-settings-20261003.py`, idempoten, backup
    `.bak-20261003`) + hook **UserPromptSubmit Cline** — menghitung tool call per
    `session_id` (fallback: transcript aktif <10 menit, aman untuk Cline tanpa id
    berkat TTL state 24 jam).
  - Ambang: **80 tool call/sesi (peringatan lunak, 1× per kelipatan) · 200 tool call
    ATAU 500 pesan riwayat (keras: perintah hentikan agen + tulis STATUS ke file +
    lanjut sesi BARU)**. Di bawah ambang = 0 byte (tidak menambah konteks).
  - Plus **aturan anti-loop keras di `AGENTS.md` §Hemat konteks**: maks 3 spawn
    paralel, 1 tujuan per agen, tanpa rekuris tanpa izin, tanda-tanda loop +
    tindakan wajib (`Esc` → status ke file → sesi baru).
  - Catatan jujur: (a) satu baris `st[sid] = e` sempat hilang → counter tak pernah
    naik; tertangkap uji 200 panggilan (bukan di sesi nyata). (b) Hook Cline hitung
    **per prompt**, bukan per tool call — jadi ambang 80 di Cline ≈ 80 pesan
    (lebih ketat dari Claude; disengaja aman karena Cline CLI limit-nya kecil).
    (c) `transcript_msgs` pesan pakai heuristik string, bukan parse penuh
    (±akurat, tapi murah).
  - Uji: sunyi ke-1–79 → bunyi ke-80 → sunyi 81–159 → bunyi 160 (ulang) → keras 200;
    JSON rusak/stdin kosong → sunyi; hook Cline utuh (skill+guard+loop) = JSON valid.
  - Sisa rekomendasi (belum dikerjakan, butuh keputusan user — bukan otomatis):
    model default turun ke haiku untuk sesi baru, dan `MAX_THINKING_TOKENS` lebih
    rendah (2 hal yang benar-benar turunkan kualitas kalau dipaksa).


- **2026-09-26 (8) — Otomasi arsip mingguan: penumpukan tidak akan terulang.**

  Selama ini semua pembersihan = manual & sekali jalan → riwayat bisa menumpuk lagi
  (kebiasaan = akar masalah). Sekarang otomatis mengikuti pola repo yang sudah ada
  (`mcp-lifecycle --gc-if-due`):
  - `archive-sessions.py` (BARU) — scan Claude/Cline/CodeBuddy, pindah sesi >7 hari
    ke folder arsip masing-masing, manifest append ke `~/ARCHIVE-MANIFEST.txt`;
    gate `.archive-state.json` (**maks 1×/minggu**); dipanggil dari `session-brief.sh`
    dengan `capture_output=True` → **nol token, nol output, 0,2 dtk**.
  - Keamanan diuji 2 arah: (1) dry-run 12 sesi muda → 0 bergerak; (2) file tiruan
    10 hari → tepat 1 itu yang dipindah; sesi aktif & sesi muda utuh dalam kedua uji.
  - Catatan jujur: saat uji pertama, logika `<=`/`>` sempat TERBALIK (sesi aktif masuk
    daftar pindah!) — tertangkap oleh uji dry-run SEBELUM ada penulisan nyata.
    Uji seperti ini wajib untuk setiap skrip yang memindahkan file.
  - Rollback = `mv` balik mengikuti manifest (cara di `COMMANDS.md` §ROLLBACK).
    Ambang bisa diubah: `ARCHIVE_AFTER_DAYS` (bukan hari = kebijakan baru, diskusikan dulu).


- **2026-09-26 (7) — CodeBuddy: rules lama ketinggalan + riwayat 26 MB diarsip.**

  User: "AI CodeBuddy masih boros". Diagnosa `~/.codebuddy` (305 MB — ke-2 terbesar):
  - **Riwayat chat**: 25 sesi / 26,6 MB; 21 sesi berumur >48 jam (25,7 MB) → dipindah ke
    `~/.codebuddy/archived-projects/` (manifest ditambahkan ke `~/ARCHIVE-MANIFEST-20260927.txt`).
    Sisa riwayat aktif **0,9 MB** (4 sesi muda). Nol file dihapus.
  - 🔴 **`AGENTS.md` CodeBuddy ketinggalan dua perbaikan** (drift — file ini tidak masuk
    daftar edit sebelumnya): (a) masih memerintah **"WAJIB baca `SKILL-FLOW.md` penuh"**
    (5.355 B/sesi) → diganti versi on-demand + pakai `skill-load-lite`; (b) angka basi
    **"≈63,436 skill"** → "3.176 skill curated" + peringatan jangan baca
    `SKILLS-AVAILABLE.md` (123 KB). Backup `AGENTS.md.bak-hemat4`.
  - 🔍 **Cek drift serupa ke 16 rules tool**: ketemu 3 tertinggal — `~/.continue/.continuerules`,
    `~/.qwen/QWEN.md` (blok Gaya lama) dan `~/.hermes/AGENTS.md` (angka 63,436) → semua
    diperbaiki (backup `.bak-hemat5`). Setelah ini: **0 rules tersisa blok lama**.
  - Yang ternyata BUKAN lubang: skills CodeBuddy = symlink bersama `skills-store` (otomatis
    ikut dipadatkan; 10 deskripsi sisa 301–338 B → hemat hanya ±150 B, tidak sepadan),
    MCP sudah 2 server, `AGENTS.md` 3,5 KB, memory project kecil (32 KB total), plugin
    Office = penyedia skill (bukan tool-schema) jadi bukan beban konteks per-request.
  - Verifikasi: `install-context-guard --check` tetap **0 perlu** · `skill-flow --eval`
    **31/31** · grep drift `SKILL-FLOW-lama` + `63,436` = **BERSIH** di semua rules.


- **2026-09-26 (6) — Arsip sesi lama: 146,6 MB dipindah (bukan dihapus), nol dampak kualitas.**

  Kebijakan (sesuai syarat user "jangan turunkan kualitas"): hanya PINDAH, sesi aktif
  & sesi <48 jam (Claude) / <24 jam (Cline) tidak disentuh — `--resume` sesi arsip tetap
  bisa dengan mengembalikan file dari manifest.
  - **Claude**: 11 file utama + 11 subagent jsonl → `~/.claude/archived-projects/<proj>/`
    (mtime >48 jam). Total disk sesi **159,5 → 74,5 MB**. Sesi aktif (`dcd21933`, ditulis
    07:44) utuh; sesi kemarin `c2ed1bd9` (**62 MB, 195 gambar**) diarsip MANUAL menyusul
    (rekomendasi tegas disetujui user: 1× resume tidak sengaja = limit mati).
    Audit kini: Claude tersisa 4 sesi / 15 MB, terbesar 7,8 MB (sesi berjalan ini).
  - **Cline**: 5 sesi >24 jam → `~/.cline/archived-sessions/`. **49 → 1,7 MB** tersisa
    (tinggal `svm25` kemarin + `5fqj1` yang sedang aktif).
  - Manifest restore: `~/ARCHIVE-MANIFEST-20260927.txt` (path asal per file).
  - Verifikasi: semua sesi tersisa berumur muda; `ai-context-audit` jalan normal;
    tidak ada file yang dihapus (total arsip = total pindah = 146,6 MB).
  - **Dibatalkan atas syarat user**: `MAX_THINKING_TOKENS` (menurunkan reasoning) &
    kompresi rules agresif (false saving) — tidak dikerjakan.


- **2026-09-26 (5) — Jebakan baca file raksasa + brief sesi yang menyesatkan.**

  - 🔴 **`SKILLS-AVAILABLE.md` (123.273 B ≈ 30 rb token)** dirujuk sebagai "Katalog" di
    `GEMINI.md` → model bisa membaca penuh sekali baca. Rujukan diganti: cari via
    MCP `skill_search`/`skill_for_task` atau `skill-search.sh`, **dilarang baca penuh**
    (perintah eksplisit + ukuran file ditulis di rules).
  - 🟡 `STYLE-TOKEN-SAVER.md` (16.620 B) dirujuk di **6 file rules** tanpa ukuran →
    ditambahi "(16 KB, on-demand)" di ke-6nya (backup `.bak-hemat4`). Trade-off sadar:
    +~45 B/rules × 6 untuk mencegah baca 16,6 KB.
  - 🟡 `session-brief.sh` (SessionStart tiap sesi Claude): **857 → 533 B**; bagian
    Auto-SKILLS yang 100% duplikat dengan `CLAUDE.md` dihapus (bagian Anti-ngarang
    dipertahankan — unik); angka **"MCP: 36 server (semua provider)" yang sudah basi**
    (sesudah slim tinggal 2) diganti angka benar + arah `--on` on-demand; angka
    "1018 skill (curated 3176)" yang kontradiktif → "3176 skill curated".
    Backup `session-brief.sh.bak-20260927`.
  - Verifikasi: `skill-flow --eval` **31/31** · `install-context-guard --check` **0 perlu** ·
    `bash -n` OK · rules 6 file tetap utuh (warna/hemat ±21,7 KB total).


- **2026-09-26 (4) — Mega hemat lanjutan: biaya PER PESAN & sisa rules gemuk.**

  Temuan: rules `~/.claude/CLAUDE.md` §AUTO-SKILLS memaksa model **"route.sh … baca
  SKILL.md-nya, ikuti" untuk 2 skill SETIAP pesan** — kalau dipatuhi literal =
  ±2 × 9 KB = ±18 KB/pesan (100 pesan ≈ 450 rb token). Plus tabel agent 834 B.
  Perbaikan:
  - **§AUTO-SKILLS ditulis ulang** (ringkas + makna utuh): routing cukup SEKALI per
    pesan (pakai kandidat hook `skill-flow` ATAU `route.sh`), muat hasil **wajib lewat
    `skill-load-lite.sh` (≤2 KB), bukan SKILL.md penuh**. Tabel 15 agent → satu baris
    padat. Net CLAUDE.md: 8.467 → **7.959 B, tanpa `@import` guard** (basis awal
    7.910 + 3.784 = 11.694 B).
  - **9 deskripsi skill round-2** (340–450 B) dipadatkan ke ≤300 B: `pdf` 450→281,
    `security-review` 422→293, `git-commit` 437→295, `avoid-ai-writing` 416→298,
    `social-content` 411→294, `email-drafter` 350→299, `seo-audit` 363→298,
    `linkedin-post-formatter` 372→298, `adversarial-reviewer` 370→295. Hemat 940 B.
    Total deskripsi 82 skill: **20.091 → 16.946 B**. Backup `.bak-20260927`.
  - **MCP `skill_load`**: `MAX_LOAD` 6.000 → 4.000 B + pesan potong kini menunjuk
    `skill-load-lite.sh` (mencegah model baca file penuh 9 KB setelahnya).
  - **Rebuild indeks urut (ke-2): curated tetap 3.176** (total 69.620).
  - **Uji recall adil (DB di-salin, limit identik, banding 4 query lama-vs-baru):**
    "pdf buat laporan" / "security review kode" / "git commit pesan" → hasil **identik
    baris demi baris**; "social media konten" → beda 1 posisi di #8 dan justru
    `social-content` (target potongan) yang masuk. **Regresi efektif 0.**
  - Verifikasi: `skill-flow --eval` **31/31**, `install-context-guard --check` **0 perlu**,
    `py_compile` OK.
  - **Akumulasi total sejak awal sesi: konteks tetap Claude 31.785 → 24.905 B
    (hemat ±6,9 KB ≈ 1,7 rb token/sesi)** + potensi hemat baca-SKILL.md-per-pesan +
    Gemini 3,8 KB/sesi + MCP ±25%/panggilan + guard riwayat/gambar (jawaban utama
    limit cepat habis).


- **2026-09-26 (3) — "Mega hemat": konteks TETAP per sesi dipangkas (tanpa menghapus skill/repo-refs).**

  Setelah riwayat/gambar/MCP ditangani di (1)+(2), sisa lubang = konteks yang selalu
  dikirim tiap sesi (bukan riwayat). Terukur & diperbaiki:
  - **`~/.claude/CLAUDE.md`** meng-`@import` penuh `AI_TOKEN_GUARD.md` (3.784 B) padahal
    isinya ~50% tumpang tindih dengan isi CLAUDE.md sendiri → diganti ringkasan 3 baris
    (rules unik dipertahankan: output ≤800 char, no re-read, batch, model murah,
    off-switch, larangan gambar base64). **Hemat 3,2 KB/sesi Claude.**
  - **`~/.gemini/GEMINI.md`** menyuruh "read AI_TOKEN_GUARD.md (read it)" padahal
    ringkasan lengkap sudah inline 6 baris di bawahnya → instruksi baca dibuang.
    **Hemat 3,8 KB/sesi Gemini.** `AI_TOKEN_GUARD.md` tetap ada sebagai dokumen
    (tidak dihapus).
  - **6 deskripsi skill terpanjang dipadatkan** ke ≤300 B: `xlsx` 965→300, `docx` 850→300,
    `pptx` 753→300, `anti-ui-slop` 498→300, `content-humanizer` 484→300,
    `typescript-security-review` 451→300. **Skill TIDAK dihapus/diubah isinya** — hanya
    baris `description:` dipotong (batas kata). Hemat 2.201 B. Backup per-file
    `SKILL.md.bak-20260927` di `skills-store/`.
  - **MCP `skill-catalog`**: hasil `skill_for_task` default 10→8 baris, potongan deskripsi
    per baris 150→120 B (hemat ±25% per panggilan).
  - **Regenerate urut** `build_skills_index.py` → `skills-index-md.py` →
    `skills-router.py` setelah deskripsi berubah: **curated tetap 3.176** (total 69.620,
    DB 56,2 MB, junk 4.538) — tidak ada anjlok.
  - **Uji recall (adil, DB di-salin dulu):** query "spreadsheet excel"/"buat excel"
    hasil identik dengan deskripsi lama (regresi 0); query "spreadsheet" tunggal — `xlsx`
    turun dari posisi 8 ke >8 (8 kandidat relevan lain tetap tampil). Diterima, dicatat.
  - Backup kebijakan: `~/.claude/CLAUDE.md.bak-20260926`, `~/.gemini/GEMINI.md.bak-20260926`.
  - **Total hemat konteks tetap Claude ≈ 5,4 KB/sesi (±1,3 rb token)** + Gemini 3,8 KB +
    MCP ±25%/panggilan. Angka kecil dibanding riwayat (4,42 M token) — jujur: lubang
    terbesar tetap perilaku sesi (sesi >10 MB & gambar base64), yang kini dijaga guard.
  - Opsi LANJUTAN yang sengaja TIDAK dijalankan (butuh keputusan user): (a) arsip sesi
    lama Claude 60 MB + Cline 18 MB (pindah, bukan hapus); (b) `MAX_THINKING_TOKENS`
    lebih rendah (hemat output, turunkan kualitas reasoning); (c) memadatkan 19 sisa
    deskripsi 300–450 B (nilai makin kecil, risiko recall makin besar).


- **2026-09-26 (2) — Cline ikut boros: diperbaiki + aturan hemat ditebar ke SEMUA tool AI.**

  **Diagnosa terukur** (`~/.cline/data/sessions`, 48,8 MB, 6 sesi): total **4.498 M
  token** (estimasi chars/4) — hampir setara Claude. Sesi terbesar 18,3 MB / 944 pesan
  = **2.392 M token kumulatif** (riwayat dikirim ulang tiap request); 2026-09-24 sesi
  1.772 pesan = 1.546 M. **Pemboros #1 = gambar base64 menempel permanen**: pesan
  `user` tunggal terbesar **2,45 JUTA karakter**; sesi itu menampung **46 gambar /
  16 MB** (di sesi Claude terbesar: 195 gambar / 48 MB). Penyebab #2: 5 tool memakai
  8–9 server MCP sekaligus (fixed-cost tools/list per sesi).

  **Perbaikan (baca-saja untuk audit; penulisan rules selalu ber-backup):**
  - `audit-cline.py` (BARU) — token kumulatif per sesi + N pesan/output terbesar.
  - `cline-guard.py` (BARU, 48 ms) → disambungkan ke hook resmi Cline
    `~/.cline/hooks/UserPromptSubmit.py` (jalan bareng `skill-flow`, 0,4 s terukur).
    Peringatan muncul saat sesi >200 pesan / >10 MB / gambar base64 >2 MB
    (ambang `CLINE_GUARD_MSGS`/`_MB`/`_IMG_MB`). Uji nyata: sesi 370 pesan → 1 baris peringatan.
  - `ai-context-audit.py` (BARU) — **satu tabel untuk 13 tool AI** (Claude/Cline/Gemini/
    Qwen/Codex/OpenCode/OpenClaude/iFlow/Aider + Cursor/Roo/Kilo/Cline-ext sqlite):
    jumlah sesi, MB, pesan, jumlah gambar base64. `--json` untuk hook/cron; 0,34 s.
  - `install-context-guard.py` (BARU) — blok aturan "hemat konteks" ke file rules
    **15 tool** (ditandai `context-guard:start/end`, idempoten, backup `.bak-YYYYMMDD`).
    Hasil: 14 ditulis + 2 sudah punya aturan sendiri (Claude/Cursor, tidak ditumpuk) +
    repo dilewati (tidak bikin file baru). Run ke-2 = `0 perlu ditulis` (terbukti idempoten).
  - `mcp-slim-all.py` (BARU) — ramping MCP di **19 tool** → hanya `skill-catalog`
    (+`mcp-router`); sisanya diparkir ke `mcp-parked.json` (hidup on-demand via
    `mcp-lifecycle.py --on <nama>`). Backup `mcp.json.bak-20260926` per tool.
  - `skill-flow.py` — state dipindah ke path stabil + TTL 6 jam (`SKILL_FLOW_STATE_TTL`)
    agar tool tanpa `session_id` (Cline dkk) tetap dapat injeksi berbatas 400 B;
    **`--eval` tetap 31/31 lulus** (routing tidak diubah).
  - Aturan ditulis di: `~/.cline/.clinerules`, `~/.codex/AGENTS.md`, `~/.gemini/GEMINI.md`,
    Cursor/Windsurf/Continue/Roo/Qwen/Aider/OpenCode/CodeBuddy/Hermes/Trae/OpenClaude/iFlow,
    + `AI_TOKEN_GUARD.md` (§Session hygiene no. 12–14).
  - Catatan jujur: (a) estimasi token Cline = chars/4 (tiap model berbeda ±20%);
    (b) penulisan aturan hemat ke 19 `mcp.json` + 14 file rules **pergi ke backup**
    di tool lain yang mungkin sudah punya aturan sendiri — rollback per-file ada di
    `COMMANDS.md` §ROLLBACK; (c) deteksi "sudah punya aturan" memakai heuristik
    ≥2 penanda substansi (`vendor`, `skill-load-lite`, `base64`, dst) — heuristik
    pertama (1 penanda longgar) sempat salah melabeli 9 file sebagai "sudah rapi",
    sudah dikoreksi sebelum `--apply`.
  - Dokumentasi: `CHEATSHEET.md` §Hemat konteks (perintah lintas tool), `COMMANDS.md`
    (+`--apply/--check` kedua installer, +env baru, +ROLLBACK MCP & blok context-guard).


- **2026-09-26 (1) — Audit limit: 4,42 M token terbakar, diperbaiki di akarnya.**

  **Diagnosa terukur** (bukan tebakan) dari `~/.claude/projects` (162 MB jsonl):
  total **4.418 M token**; 3 sesi terbesar @ 59/54/18 MB dengan **konteks ±500.000
  token/pesan** (cache_read 2.525 M ÷ 5.000 pesan). Per hari: 17 Sep **1.846 M**,
  18 Sep 817 M, 19 Sep 835 M, 26 Sep 400 M. Model: sonnet-5 3.804 M + opus-5-5 601 M
  (hanya 1.791 pesan). Penyebab: sesi tidak pernah di-clear → tiap pesan baca ulang
  seluruh konteks. Hook/MCP bukan penyebab (injeksi hook cuma ~4 baris pendek).

  **Perbaikan (skill TETAP diambil — hanya cara memuatnya dihemat):**
  - `context-guard.py|.sh` (BARU) — hook `SessionStart`+`UserPromptSubmit`: 0 token di
    bawah ambang, 1 baris peringatan di >10 MB, instruksi tegas di >25 MB, diingat per
    kenaikan 5 MB (tidak spam). `--report` untuk melihat sesi >10 MB.
  - `skill-flow.py` — routing/skor TIDAK diubah (**`--eval` tetap 31/31 lulus**), tapi
    injeksi jadi idempoten per sesi (`/tmp/voralens-skill-flow/<sesi>.json`) + berbatas
    `SKILL_FLOW_MAX_BYTES` (400 B). Uji nyata: prompt-1 260 B → prompt-2 kategori sama
    28 B ("Kandidat baru: …") → prompt-3 identik **0 B** → tugas beda 219 B. Baris
    pendorong "baca SKILL-FLOW.md" dihapus (5.355 B/sesi terbuang).
  - `skill-load-lite.sh` (BARU) — muat skill ≤80 baris/≤2 KB. Uji: `caveman-token-optimizer`
    **2.277 B vs 8.907 B penuh (±4× lebih hemat)**, esensi tetap.
  - `permissions.deny` (docs resmi Claude Code "large codebases") di `~/.claude/settings.json`
    + repo `.claude/settings.json`: blok `Read` ke `vendor/`, `node_modules/`, `dist/`,
    `public/template/`, `skills-expanded/`, `*.min.js`.
  - `usage-audit.py|.sh` (BARU) — laporan token harian/7 hari/model/sesi terboros.
  - Aturan ditulis di 3 tempat yang sebelumnya justru menyuruh baca SKILL-FLOW.md penuh:
    `AGENTS.md` (§Hemat konteks), `~/.claude/CLAUDE.md`, `AI_TOKEN_GUARD.md` (§Session hygiene).
  - Pemasang idempoten: `patch-settings-20260926.py` (run-2 = "sudah lengkap", terbukti).
    Backup: `skill-flow.py.bak-20260926`, `AGENTS.md.bak-20260926`, `CHEATSHEET.md.bak-20260926`,
    `COMMANDS.md.bak-20260926`, `settings.json.bak-20260926`, `CLAUDE.md.bak-20260926`,
    `AI_TOKEN_GUARD.md.bak-20260926`. Catatan jujur: `README.md` (file ini) diedit langsung
    tanpa backup pra-edit — perubahannya murni aditif (baris tabel + entri status ini);
    snapshot lama yang tersedia: `README.md.bak-20260925`.

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
