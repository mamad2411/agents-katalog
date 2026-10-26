# Skills INDEX — 2026-10-26 09:19

Ringkasan katalog `~/.agents`. **Jangan edit file ini** — hasil generate `python3 ~/.agents/skills-index-md.py`.

## Angka pokok

- Total entri: **264892**
- `reference`: **249869** — hasil scraping, punya deskripsi (cari dulu sebelum pakai)
- `junk`: **11752** — BUKAN skill (API doc/HTML/license/terlalu pendek) — jangan di-link
- `curated`: **3271** — skill terpilih — sudah dirawat, layak di-invoke

> **Baca angka dengan benar:** hanya `curated` yang boleh muncul sebagai kandidat
> otomatis (hook/MCP). `reference` = bahan tambang — **wajib** dicek isinya dulu.
> Kalau sebuah katalog atau laporan menampilkan angka jauh lebih besar dari
> `curated` di atas sambil menyebutnya "curated", itu bug pelabelan.

## Cek kesehatan katalog

```bash
python3 ~/.agents/skill-curate.py --report      # angka jujur + kandidat sampah
python3 ~/.agents/skill-curate.py --dry-run      # lihat rencana tanpa ubah apa pun
```

## Cara pakai (ringan, tanpa MCP)

```bash
skill-search.sh "postgres index"            # cari semua tier
skill-search.sh --tier curated "vue page"    # hanya skill terpilih
skill-search.sh -p "docker"                  # tampilkan path SKILL.md
skill-search.sh --load "playwright"          # lihat isi skill teratas
link-skills-min.sh --repo <path>            # project-scope (symlink, bukan klon)
link-skills-min.sh --status                 # cek wiring tiap tool
python3 ~/.agents/build_skills_index.py     # rebuild index (head 4 KB, cepat)
```

## Skill per peran (kategori non-docs)

| Kategori | Jumlah | Contoh |
|---|---|---|
| backend-developer | 71297 | `abp-dapr`, `accelerated-computing-cudf`, `access-control-rbac`, `ad-campaign-analyzer` |
| designer | 35242 | `3dsvg-interactive-react`, `8-bit-orbit-video-template`, `a-b-test-analysis`, `ab-test-setup` |
| frontend-developer | 22504 | `absolute-deflake`, `accessibility`, `accessibility-auditing`, `accessibility-compliance` |
| creative-producer | 21485 | `absolute-debt`, `absolute-prune`, `absolute-upgrade`, `academic-search` |
| game-developer | 21074 | `academy-guide`, `accessibility-auditor`, `add-hf-model`, `adding-api-docs` |
| devops-engineer | 20990 | `acreadiness-policy`, `add-uint-support`, `adr-critique`, `agent-platform-alert-configuration` |
| qa-engineer | 16398 | `absolute-init`, `absolute-simplify`, `access-review`, `adr-backfill` |
| data-scientist | 8952 | `adr-drafting`, `agent-eval`, `agent-self-evaluation`, `agent-setup-maintenance` |
| security-specialist | 8493 | `724-office-ai-agent`, `ad-creative`, `agentic-engineering`, `ai-elements` |
| mobile-developer | 7953 | `adf-master`, `android-clean-architecture`, `android-kotlin-development`, `anubis-android-app-manager` |
| (kosong) | 4783 | `humanize-korean-ai-text` |
| ai-engineer | 4454 | `add-educational-comments`, `agent-platform-prompt-management`, `agents-md`, `ai-prompt-engineering-safety-review` |
| tech-writer | 3655 | `asana-automation`, `avoid-ai-writing`, `cmux-ghostty`, `content-humanizer` |
| devtools-engineer | 3501 | `aube-package-manager`, `best-of-n-solving`, `configuration`, `conventional-commits` |
| product-manager | 3264 | `bench-read`, `clickup-automation`, `cohort-analysis`, `competitor-analysis` |
| data-engineer | 3109 | `aod-plan`, `clawd-code-python-port`, `company-research`, `competitive-ads-extractor` |
| productivity-automator | 1565 | `agent-platform-rag-engine-management`, `calendar-automation`, `cc-connect-ai-bridge`, `encrypted-docs` |
| fullstack-generalist | 1394 | `create-implementation-plan`, `create-spring-boot-java-project`, `create-spring-boot-kotlin-project`, `java-springboot` |
| analyst | 1304 | `lead-qualification` |
| blockchain-developer | 948 | `deck-swiss-international`, `oracle-ai-architect` |
| architect | 657 | `debian-linux-triage`, `ef-core`, `fedora-linux-triage`, `financial-modeling` |
| agent-ux | 463 | `mcp-builder`, `openclaw-local-mac-mini`, `parallel-exploring`, `skill-creator` |
| agent-orchestrator | 407 | `langgraph-human-in-the-loop`, `langgraph-python-quickstart`, `linear-context-handover`, `structured-autonomy-plan` |
| agent-memory | 362 | `linkedin-obsidian-memory-graph` |
| uncategorized | 304 | — |

## Kontaminan yang dipisah ke tier `docs`

- Jumlah: **11752** entri → daftar di `skills-junk.txt` (bahan pembersihan P1).
- Disaring karena: tanpa `description` di frontmatter, atau nama dokumentasi teknis (mis. `Util`, `Pool`, `Client`).

## Maintenance

- Sumber tunggal: `~/.agents/skills-store` (curated). `skills-expanded/` = arsip scraping.
- Jangan klon katalog ke folder tool — pakai `link-skills-min.sh` (symlink).
- MCP: audit dengan `python3 ~/.agents/mcp-hygiene.py` (laporan) / `--apply`.
- **Urutan regenerate yang benar** (jangan dibalik — dua generator terakhir baca DB):
  ```bash
  python3 ~/.agents/build_skills_index.py   # 1. tulis DB dari skills-store + skills-expanded
  python3 ~/.agents/skills-index-md.py      # 2. tulis skills-INDEX.md (baca DB)
  python3 ~/.agents/skills-router.py        # 3. tulis SKILLS-AVAILABLE / CATEGORIES / json
  ```
