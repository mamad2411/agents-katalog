# Skills INDEX — 2026-09-24 15:34

Ringkasan katalog `~/.agents`. **Jangan edit file ini** — hasil generate `python3 ~/.agents/skills-index-md.py`.

## Angka pokok

- Total entri: **67550**
- `reference`: **60275** — hasil scraping, punya deskripsi (cari dulu sebelum pakai)
- `junk`: **4099** — -
- `curated`: **3176** — skill terpilih — sudah dirawat, layak di-invoke

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
| backend-developer | 18776 | `access-control-rbac`, `acreadiness-assess`, `adding-api-docs`, `adding-auth` |
| designer | 9352 | `absolute-ui`, `absolute-work`, `acgti-anime-persona-quiz`, `adobe-illustrator-scripting` |
| frontend-developer | 5803 | `3dsvg-interactive-react`, `accessibility`, `accessibility-auditing`, `accessibility-auditor` |
| creative-producer | 5771 | `8-bit-orbit-video-template`, `absolute-debt`, `absolute-prune`, `absolute-upgrade` |
| game-developer | 5363 | `adf-validation-rules`, `amazon-seller`, `architecture-blueprint-generator`, `asset-inventory` |
| devops-engineer | 4488 | `acquire-codebase-knowledge`, `acreadiness-generate-instructions`, `acreadiness-policy`, `adding-docker` |
| qa-engineer | 3312 | `a-b-test-analysis`, `ab-test-setup`, `ab-testing`, `absolute-audit` |
| ai-engineer | 2649 | `724-office-ai-agent`, `accelerated-computing-cudf`, `ad-campaign-analyzer`, `add-uint-support` |
| data-scientist | 2354 | `adding-analytics`, `adf-ml-analytics`, `agent-eval`, `agent-evals` |
| mobile-developer | 2051 | `adf-master`, `android-clean-architecture`, `android-kotlin-development`, `anubis-android-app-manager` |
| security-specialist | 1937 | `ad-creative`, `agent-supply-chain`, `ai-agent-security`, `ai-first-engineering` |
| devtools-engineer | 1122 | `ado-windows-git-bash-compatibility`, `amc-run-rtsp-calibration`, `amc-run-sample-calibration`, `amc-setup-calibration-stack` |
| tech-writer | 938 | `absolute-docs`, `academy-guide`, `add-educational-comments`, `ads-copywriter` |
| data-engineer | 899 | `academic-search`, `agentforce-2025`, `ai-agent-orchestrator`, `ai-team-orchestration` |
| product-manager | 644 | `absolute-spec`, `adding-feature-flags`, `adr-discovery`, `architecture-advisor` |
| (kosong) | 640 | — |
| fullstack-generalist | 382 | `absolute-init`, `appinsights-instrumentation`, `apple-hig`, `applicant-screening` |
| productivity-automator | 318 | `google-workspace-ops`, `gws-calendar`, `gws-calendar-agenda`, `gws-calendar-insert` |
| analyst | 270 | `add-model-price`, `adding-error-tracking`, `alembic`, `anything-analyzer-cdp` |
| architect | 171 | `adr-backfill`, `adr-critique`, `adr-drafting`, `adr-writer` |
| uncategorized | 139 | `image-annotations`, `suggesting-skills`, `tong-jincheng-relationship-skill`, `ultrathink` |
| blockchain-developer | 132 | `bug-receipt`, `deck-swiss-international`, `define-goal`, `evm-token-decimals` |
| educator | 39 | `anki-connect`, `exam-ready`, `learn` |

## Kontaminan yang dipisah ke tier `docs`

- Jumlah: **4099** entri → daftar di `skills-junk.txt` (bahan pembersihan P1).
- Disaring karena: tanpa `description` di frontmatter, atau nama dokumentasi teknis (mis. `Util`, `Pool`, `Client`).

## Maintenance

- Sumber tunggal: `~/.agents/skills` (curated). `skills-expanded/` = arsip scraping.
- Jangan klon katalog ke folder tool — pakai `link-skills-min.sh` (symlink).
- MCP: audit dengan `python3 ~/.agents/mcp-hygiene.py` (laporan) / `--apply`.
