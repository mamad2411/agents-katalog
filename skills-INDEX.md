# Skills INDEX — 2026-10-19 10:27

Ringkasan katalog `~/.agents`. **Jangan edit file ini** — hasil generate `python3 ~/.agents/skills-index-md.py`.

## Angka pokok

- Total entri: **192599**
- `reference`: **188288** — hasil scraping, punya deskripsi (cari dulu sebelum pakai)
- `curated`: **3194** — skill terpilih — sudah dirawat, layak di-invoke
- `junk`: **1117** — BUKAN skill (API doc/HTML/license/terlalu pendek) — jangan di-link

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
| backend-developer | 54674 | `absolute-audit`, `accelerated-computing-cudf`, `access-control-rbac`, `ad-campaign-analyzer` |
| designer | 24693 | `3dsvg-interactive-react`, `8-bit-orbit-video-template`, `a-b-test-analysis`, `ab-test-setup` |
| creative-producer | 16740 | `absolute-debt`, `absolute-prune`, `absolute-upgrade`, `academic-search` |
| frontend-developer | 15718 | `absolute-deflake`, `accessibility`, `accessibility-auditing`, `accessibility-compliance` |
| game-developer | 15356 | `academy-guide`, `accessibility-auditor`, `adding-api-docs`, `adding-feature-flags` |
| devops-engineer | 13714 | `acreadiness-policy`, `add-uint-support`, `adding-docker`, `adr-critique` |
| qa-engineer | 11236 | `absolute-docs`, `absolute-init`, `absolute-simplify`, `access-review` |
| data-scientist | 6376 | `adr-drafting`, `agent-eval`, `agent-self-evaluation`, `agent-setup-maintenance` |
| mobile-developer | 5887 | `adf-master`, `android-clean-architecture`, `android-kotlin-development`, `anubis-android-app-manager` |
| security-specialist | 5800 | `724-office-ai-agent`, `ad-creative`, `agentic-engineering`, `aglais-xqvm-quantum-vm` |
| (kosong) | 3698 | `humanize-korean-ai-text` |
| ai-engineer | 3247 | `add-educational-comments`, `agent-platform-prompt-management`, `agents-md`, `ai-prompt-engineering-safety-review` |
| devtools-engineer | 2509 | `aube-package-manager`, `best-of-n-solving`, `configuration`, `conventional-commits` |
| tech-writer | 2467 | `asana-automation`, `avoid-ai-writing`, `cmux-ghostty`, `content-humanizer` |
| data-engineer | 2365 | `clawd-code-python-port`, `company-research`, `competitive-ads-extractor`, `create-technical-spike` |
| product-manager | 2197 | `bench-read`, `clickup-automation`, `cohort-analysis`, `competitor-analysis` |
| productivity-automator | 1419 | `agent-platform-rag-engine-management`, `calendar-automation`, `cc-connect-ai-bridge`, `copaw-ai-assistant` |
| analyst | 1145 | `lead-qualification` |
| fullstack-generalist | 885 | `create-implementation-plan`, `create-spring-boot-java-project`, `create-spring-boot-kotlin-project`, `java-springboot` |
| blockchain-developer | 662 | `deck-swiss-international` |
| architect | 441 | `debian-linux-triage`, `ef-core`, `fedora-linux-triage`, `financial-modeling` |
| agent-ux | 426 | `mcp-builder`, `openclaw-local-mac-mini`, `parallel-exploring`, `skill-creator` |
| uncategorized | 307 | — |
| agent-orchestrator | 278 | `langgraph-human-in-the-loop`, `langgraph-persistence`, `langgraph-python-quickstart`, `linear-context-handover` |
| agent-memory | 277 | `linkedin-obsidian-memory-graph` |

## Kontaminan yang dipisah ke tier `docs`

- Jumlah: **1117** entri → daftar di `skills-junk.txt` (bahan pembersihan P1).
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
