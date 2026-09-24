# COMMANDS.md — Daftar Semua Perintah `~/.agents`

Semua perintah aman diulang (idempotent). Sumber tunggal skill: `~/.agents/skills`.

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
`sync-wire.py` kini hanya men-symlink ~60 skill CORE (daftar: `~/.agents/skill-core.json`,
bebas diedit) ke folder `skills` tiap tool — dulu 3.173/tool. Sisanya 14.916 skill tetap
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
python3 ~/.agents/skill-graph-api.py      # API graf skill+memory (port 27126, optional)
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
```
