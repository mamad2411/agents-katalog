# Skills INDEX — 2026-10-12 18:22

Ringkasan katalog `~/.agents`. **Jangan edit file ini** — hasil generate `python3 ~/.agents/skills-index-md.py`.

## Angka pokok

- Total entri: **103428**
- `reference`: **91258** — hasil scraping, punya deskripsi (cari dulu sebelum pakai)
- `junk`: **8993** — BUKAN skill (API doc/HTML/license/terlalu pendek) — jangan di-link
- `curated`: **3177** — skill terpilih — sudah dirawat, layak di-invoke

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
| backend-developer | 25781 | `absolute-audit`, `accelerated-computing-cudf`, `access-control-rbac`, `ad-campaign-analyzer` |
| designer | 13022 | `3dsvg-interactive-react`, `8-bit-orbit-video-template`, `a-b-test-analysis`, `ab-test-setup` |
| creative-producer | 8545 | `absolute-debt`, `absolute-prune`, `absolute-upgrade`, `academic-search` |
| frontend-developer | 8328 | `absolute-deflake`, `accessibility`, `accessibility-auditing`, `accessibility-compliance` |
| qa-engineer | 8297 | `absolute-docs`, `absolute-init`, `absolute-simplify`, `access-review` |
| game-developer | 8222 | `academy-guide`, `accessibility-auditor`, `adding-api-docs`, `adding-feature-flags` |
| devops-engineer | 7649 | `acreadiness-policy`, `add-uint-support`, `adding-docker`, `adr-critique` |
| data-scientist | 3576 | `adr-drafting`, `agent-eval`, `agent-self-evaluation`, `agent-setup-maintenance` |
| security-specialist | 3147 | `724-office-ai-agent`, `ad-creative`, `agentic-engineering`, `aglais-xqvm-quantum-vm` |
| mobile-developer | 3128 | `adf-master`, `android-clean-architecture`, `android-kotlin-development`, `anubis-android-app-manager` |
| ai-engineer | 2600 | `add-educational-comments`, `agent-platform-prompt-management`, `agents-md`, `ai-prompt-engineering-safety-review` |
| devtools-engineer | 1817 | `aube-package-manager`, `best-of-n-solving`, `configuration`, `conventional-commits` |
| tech-writer | 1588 | `asana-automation`, `avoid-ai-writing`, `cmux-ghostty`, `content-humanizer` |
| data-engineer | 1453 | `clawd-code-python-port`, `company-research`, `competitive-ads-extractor`, `create-technical-spike` |
| product-manager | 1286 | `bench-read`, `clickup-automation`, `cohort-analysis`, `competitor-analysis` |
| (kosong) | 1211 | `humanize-korean-ai-text` |
| productivity-automator | 758 | `agent-platform-rag-engine-management`, `calendar-automation`, `cc-connect-ai-bridge`, `copaw-ai-assistant` |
| fullstack-generalist | 726 | `create-implementation-plan`, `create-spring-boot-java-project`, `create-spring-boot-kotlin-project`, `java-springboot` |
| analyst | 534 | `lead-qualification` |
| blockchain-developer | 433 | `deck-swiss-international` |
| uncategorized | 357 | — |
| architect | 332 | `debian-linux-triage`, `ef-core`, `fedora-linux-triage`, `financial-modeling` |
| agent-ux | 210 | `mcp-builder`, `openclaw-local-mac-mini`, `parallel-exploring`, `skill-creator` |
| agent-orchestrator | 207 | `langgraph-human-in-the-loop`, `langgraph-persistence`, `langgraph-python-quickstart`, `linear-context-handover` |
| agent-memory | 164 | `linkedin-obsidian-memory-graph` |

## Kontaminan yang dipisah ke tier `docs`

- Jumlah: **8993** entri → daftar di `skills-junk.txt` (bahan pembersihan P1).
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
