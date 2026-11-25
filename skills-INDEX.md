# Skills INDEX — 2026-11-23 10:14

Ringkasan katalog `~/.agents`. **Jangan edit file ini** — hasil generate `python3 ~/.agents/skills-index-md.py`.

## Angka pokok

- Total entri: **382703**
- `reference`: **350991** — hasil scraping, punya deskripsi (cari dulu sebelum pakai)
- `junk`: **27864** — BUKAN skill (API doc/HTML/license/terlalu pendek) — jangan di-link
- `curated`: **3848** — skill terpilih — sudah dirawat, layak di-invoke

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
| backend-developer | 101141 | `abp-dapr`, `accelerated-computing-cudf`, `access-control-rbac`, `ad-campaign-analyzer` |
| designer | 51605 | `3dsvg-interactive-react`, `8-bit-orbit-video-template`, `a-b-test-analysis`, `ab-test-setup` |
| devops-engineer | 40817 | `acreadiness-policy`, `add-uint-support`, `adr-critique`, `[replace: skill_name]` |
| creative-producer | 32294 | `absolute-debt`, `absolute-prune`, `absolute-upgrade`, `academic-search` |
| frontend-developer | 31223 | `absolute-deflake`, `accessibility`, `accessibility-auditing`, `accessibility-compliance` |
| game-developer | 30426 | `academy-guide`, `accessibility-auditor`, `add-hf-model`, `adding-api-docs` |
| qa-engineer | 20394 | `absolute-init`, `absolute-simplify`, `access-review`, `adr-backfill` |
| security-specialist | 11748 | `724-office-ai-agent`, `ad-creative`, `agentic-engineering`, `agents-md-senior-engineer` |
| data-scientist | 11455 | `adr-drafting`, `agent-eval`, `agent-self-evaluation`, `agent-setup-maintenance` |
| mobile-developer | 10642 | `adf-master`, `firebase-firestore`, `firebase-remote-config-basics`, `firebase-security-rules-auditor` |
| (kosong) | 7371 | `anyone-to-skill`, `decision-algorithm`, `email-ops`, `healthcare-cdss-patterns` |
| ai-engineer | 5405 | `add-educational-comments`, `agent-platform-prompt-management`, `agents-md`, `ai-prompt-engineering-safety-review` |
| tech-writer | 4463 | `dart-use-primary-constructors`, `asana-automation`, `avoid-ai-writing`, `cmux-ghostty` |
| product-manager | 4311 | `aeris10-plfm-radar`, `bench-read`, `clickup-automation`, `cohort-analysis` |
| data-engineer | 4268 | `aod-plan`, `clawd-code-python-port`, `company-research`, `competitive-ads-extractor` |
| devtools-engineer | 4165 | `aube-package-manager`, `best-of-n-solving`, `configuration`, `conventional-commits` |
| agent-orchestrator | 2076 | `goal-driven-multi-agent`, `swarm`, `linear-context-handover`, `langgraph-human-in-the-loop` |
| productivity-automator | 1865 | `agent-platform-rag-engine-management`, `calendar-automation`, `cc-connect-ai-bridge`, `cinematic-script-writer` |
| analyst | 1790 | `finance-billing-ops`, `lead-qualification` |
| fullstack-generalist | 1639 | `cpanelsniper`, `create-implementation-plan`, `create-spring-boot-java-project`, `create-spring-boot-kotlin-project` |
| blockchain-developer | 1149 | `deck-swiss-international`, `evm-token-decimals`, `oracle-ai-architect`, `safe-greeting` |
| architect | 834 | `debian-linux-triage`, `hexagonal-architecture`, `fedora-linux-triage`, `financial-modeling` |
| agent-ux | 522 | `skill-creator`, `mcp-builder`, `openclaw-local-mac-mini`, `parallel-exploring` |
| agent-memory | 444 | `linkedin-obsidian-memory-graph`, `planning-with-files-manus-workflow`, `trending-skills-planning-with-files-manus-workflow`, `trending-skills-ralph-autonomous-agent-loop` |
| uncategorized | 307 | `golang-patterns`, `python-patterns`, `verification-loop` |

## Kontaminan yang dipisah ke tier `docs`

- Jumlah: **27864** entri → daftar di `skills-junk.txt` (bahan pembersihan P1).
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
