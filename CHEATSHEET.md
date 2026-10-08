# ⚡ CHEATSHEET ~/.agents — semua perintah, format ringkas

WAJIB sebelum kerja: `skill_for_task(task="<tugas>")` → `skill_load("<nama>")` → kerjakan → verifikasi.
Sumber tunggal skill: `~/.agents/skills-store` (3.176 curated). Semua aman diulang (idempotent).
Detail lengkap + penjelasan: `~/.agents/COMMANDS.md`

## SEGALA HAL (sekali jalan, semua beres)
bash ~/.agents/sync-all.sh              # katalog + hapus kadaluarsa + symlink semua AI + MCP + eval
bash ~/.agents/sync-all.sh --fast       # versi ringan (tanpa rebuild katalog)

## Cari & pakai skill
~/.agents/skill-search.sh "kata kunci"            # cari (bahasa natural OK)
~/.agents/skill-search.sh --tier curated "vue"    # filter tier
~/.agents/skill-search.sh -p "playwright"          # lihat PATH file SKILL.md
~/.agents/skill-search.sh --load "playwright"     # baca isi SKILL.md (sadar: bisa 3–15 KB)
bash ~/.agents/skill-load-lite.sh "playwright"    # ⭐ cara hemat: ≤80 baris/≤2 KB, esensi tetap dapat
bash ~/.agents/session-brief.sh                   # konteks sesi (skill+MCP+repo+aturan)

## Hemat konteks & limit (audit 2026-09-26: Claude 4,42 M token · Cline 4,47 M token)
python3 ~/.agents/device-guard.py             # ⭐ PANAS & SSD: loop mining, agent 24/7, churn tulis
python3 ~/.agents/loop-guard.py               # anti-LOOP: 80 tool call lunak / 200 keras
bash ~/.agents/wire-skills-role.sh --list     # role pack: skill relevan saja per repo (12 preset)
python3 ~/.agents/ai-context-audit.py             # ⭐ SEMUA tool AI: ukuran sesi + gambar base64
python3 ~/.agents/usage-audit.py                  # token 7 hari + model + sesi terboros (Claude)
python3 ~/.agents/audit-cline.py                  # Cline: token kumulatif + 20 output terbesar
python3 ~/.agents/context-guard.py --report       # sesi >10 MB (wajib /clear sebelum lanjut)
python3 ~/.agents/install-context-guard.py --check # aturan hemat di file rules semua tool
python3 ~/.agents/mcp-slim-all.py --apply          # ramping MCP 19 tool ke skill-catalog (+router)
python3 ~/.agents/archive-sessions.py --dry-run       # rencana arsip sesi >7 hari (otomatis 1×/minggu)
python3 ~/.agents/skill-flow.py --stats           # injeksi skill per sesi (batas 400 B, dedupe)
python3 ~/.agents/skill-flow.py --eval            # gerbang mutu routing (31/31)
python3 ~/.agents/patch-settings-20260926.py      # pasang ulang hook+deny (idempoten, ada backup)
# aturan: /clear di batas tugas · jangan --resume · jangan read vendor/node_modules/dist
# aturan: JANGAN tempel gambar di sesi panjang (base64 ikut terkirim tiap request, selamanya)

## Kualitas & keamanan
python3 ~/.agents/skill-eval.py                   # pass@1/pass@3 + health katalog
python3 ~/.agents/skill-sec-scan.py --quick        # scan keamanan (cepat, tanpa repo-refs)
python3 ~/.agents/skill-sec-scan.py                # scan penuh (251rb file, ±10 mnt)
python3 ~/.agents/skill-sec-scan.py --since 20260925  # delta: hanya file baru
python3 ~/.agents/skill-sec-scan.py --test         # self-test pola (14 kasus)
python3 ~/.agents/skill-bench.py                   # benchmark routing (precision@k, 12 prompt)
python3 ~/.agents/skill-curate.py --report         # audit curated: 3.176 → 3.161 bersih, 15 review
python3 ~/.agents/skill-curate.py --dry-run        # lihat kandidat, tanpa tulis
python3 ~/.agents/skill-curate.py --apply          # tulis skills-review.txt + skills-curated-clean.txt

## Tambah skill
python3 ~/.agents/skill-miner-skillsh.py --limit 300  # dari skills.sh (20k entry, TANPA rate limit)
python3 ~/.agents/skill-miner-skillsh.py --probe 20   # dry-run: cek hit rate saja
MINER_LIMIT=900 python3 ~/.agents/skill-miner.py      # tambang komunitas (GitHub API, butuh token)
python3 ~/.agents/skill-miner.py --registry           # dari registry (default bintang ≥100)
python3 ~/.agents/skill-factory.py "<nama>" "<desc>"  # bikin skill baru
bash ~/.agents/mine-to-100k.sh 1 600 80               # batch: mine → scan delta → rebuild index
bash ~/.agents/mine-daemon.sh start|status|stop       # daemon tmux menuju 100k (loop otomatis)

## Katalog
python3 ~/.agents/build_skills_index.py   # rebuild DB (WAJIB urut pertama)
python3 ~/.agents/skills-index-md.py      # regen skills-INDEX.md (baca DB)
python3 ~/.agents/skills-router.py        # regen SKILLS-AVAILABLE + CATEGORIES + index.json
python3 ~/.agents/_categorize_roles.py    # pemetaan role (JANGAN jalan saat index dipakai)

## MCP
python3 ~/.agents/mcp-hygiene.py                                   # audit (dry-run)
python3 ~/.agents/mcp-hygiene.py --keep ~/.agents/mcp-allowlist.txt --apply  # kurasi
python3 ~/.agents/mcp-doctor.py                                    # tes ALIVE/DEAD
python3 ~/.agents/mcp-lifecycle.py                                 # status (aktif/parkir)
python3 ~/.agents/mcp-lifecycle.py --on <nama> | --off <nama>      # nyala/parkir 1 server
python3 ~/.agents/mcp-lifecycle.py --gc 14 | --gc-if-due           # parkir idle

## Wiring (symlink) skill ke tool
bash ~/.agents/link-skills-min.sh --repo /path/ke/repo     # scope repo → <repo>/.claude/skills/
bash ~/.agents/link-skills-min.sh --tool ~/.claude/skills starter     # set starter (default)
bash ~/.agents/link-skills-min.sh --tool ~/.claude/skills all-curated  # semua curated (BERAT)
bash ~/.agents/link-skills-min.sh --status                 # cek wiring tiap tool
python3 ~/.agents/sync-wire.py                             # tiered: hanya core (~79), pangkas sisanya
python3 ~/.agents/install-skill-first.py --apply           # pasang blok skill-first ke semua agen
python3 ~/.agents/install-skill-contract.py                # pasang kontrak WAJIB ke 14 file rules
python3 ~/.agents/install-skill-contract.py --check        # audit: mana sudah punya kontrak

## Repo referensi
python3 ~/.agents/repo-registry.py --fetch                 # ambil awesome-list → registry
python3 ~/.agents/repo-ref-fetch.py <owner/repo>           # tambah 1 repo referensi
bash ~/.agents/clone-repo-refs.sh                          # klon/refresh dump repo ke repo-refs/
python3 ~/.agents/repo-ref-api.py --search <kata>          # cari isi repo via API lokal

## RAM &比较好的目录清理
bash ~/.agents/stop-berat.sh                                # matikan proses berat (Docker, stack, MCP yatim)
bash ~/.agents/cleanup-skill-junk.sh                       # bersihkan tier junk (BUTUH izin user)
python3 ~/.agents/skill-health.py                           # ringkasan kesehatan katalog
python3 ~/.agents/fix-skill-name-canonical.py               # kanonik nama skill (kebab-case)
python3 ~/.agents/split-style-categories.py                # pecah STYLE-*.md jadi sub-kategori
python3 ~/.agents/mass-repo-cloner.py                      # clone massal repo ke repo-refs/

## INTERNAL / JARANG DIPAKAI (dipakai hook & sistem; rarely manual)
bash ~/.agents/skill-inject.sh                  # output hook (stdin JSON) — Claude/Cline/Codex
python3 ~/.agents/skill-inject-gemini.py        # hook versi Gemini (BeforeAgent)
python3 ~/.agents/skill-rank.py "<prompt>"      # 3 skill teratas (dipakai hook)
python3 ~/.agents/skill-flow.py --test "<p>"    # uji routing · --check · --render
python3 ~/.agents/skill-mcp.py                  # server MCP skill-catalog (dipanggil AI)
python3 ~/.agents/mcp-router.py                 # gateway MCP on-demand (mcp_list/search/use)
python3 ~/.agents/build-mcp-catalog.py          # katalog MCP untuk router
python3 ~/.agents/skill-learn.py                # catat skill baru dari pemakaian
python3 ~/.agents/fix-repo-refs.py              # perbaiki path repo-refs
python3 ~/.agents/confkit-extract.py            # ekstrak konfigurasi dari repo
python3 ~/.agents/skill-auto-symlink.py         # auto-link core (--full = perilaku lama)
python3 ~/.agents/skill-auto-tuner.py           # auto-tune ambang rank
bash ~/.agents/smart-symlink-bridge.sh          # jembatan symlink pintar
python3 ~/.agents/link-skills-repos.py          # link skill ke repo scope
python3 ~/.agents/skill-graph-api.py            # API skill-graph
python3 ~/.agents/upgrade_demand.py              # proses permintaan upgrade
python3 ~/.agents/upload-links.py               # upload daftar link (sistem)
bash ~/.agents/upload-chain.sh                 # rantai upload
bash ~/.agents/upload-link-watcher.sh           # watcher sinkron link
bash ~/.agents/upload-link-watcher2.sh          # watcher v2
python3 ~/.agents/mcp-proxy-manager.py          # proxy MCP (legacy — pakai mcp-router)
