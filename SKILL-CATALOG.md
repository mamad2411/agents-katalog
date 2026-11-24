# Peta Katalog Skill (ringkas, on-demand)

Total: **634.493 skill** (558.685 aktif / 75rb junk) di `~/.agents/skills-index.db` (bertambah otomatis oleh miner).
Jangan load massal — cukup tahu coverage ini, lalu cari via `sk "<tugas>" -n 5` → `sk -l <nama>`.

## Category resmi (skills.category)
| Category | Jumlah |
|---|---|
| backend-developer | 144.135 |
| game-developer | 110.186 |
| designer | 78.926 |
| creative-producer | 55.280 |
| devops-engineer | 51.979 |
| frontend-developer | 43.610 |
| qa-engineer | 32.620 |
| security-specialist | 19.083 |
| data-scientist | 17.602 |
| mobile-developer | 15.388 |
| tech-writer | 7.443 |
| ai-engineer | 7.441 |
| data-engineer | 6.435 |
| product-manager | 6.192 |
| devtools-engineer | 6.189 |
| productivity-automator | 3.197 |
| analyst | 2.720 |
| agent-orchestrator | 2.665 |
| blockchain-developer | 1.758 |
| architect / agent-ux / agent-memory | ~2.800 |

## Domain (cocok di nama/desc skill)
- mobile/game/3D: ~115rb (iOS, Android, Unity, Unreal, Godot, Blender)
- AI/ML/LLM: ~44rb (RAG, fine-tune, agent, prompt, MCP, diffusion, whisper)
- sains/edu: ~43rb (math, research, course, medical, bahasa)
- bisnis/finance: ~41rb (trading, crypto, akuntansi, pajak, legal, marketing, real-estate)
- media/kreatif: ~36rb (video, musik, foto, desain, font, subtitle, CAD)
- backend/data: ~33rb (DB, API, cloud, devops, semua bahasa)
- web/frontend: ~30rb (React, Vue, CSS, SEO, web3)
- otomasi/agent: ~19rb (n8n, scraping, bot, browser, webhook)
- security/CTF: ~13rb (pentest, forensik, OSINT, bug-bounty, malware)
- produktivitas/dokumen: ~13rb (docx/xlsx/pdf, resume, notion, email)
- bahasa/niche: ~10rb (30+ bahasa, masak, travel, fitness, drone, IoT, embedded)

## Sumber terbesar
nb-ecosystem 76rb · agents-katalog 62rb · ra-skills 59rb · learn-skills.dev 39rb ·
legal-skills-open 17rb · openclaw-marketplace 13rb · claude-skill-registry 13rb ·
+ ratusan sumber mined-* dari 24.800+ repo GitHub.

## Cara pakai (0 token sampai dipanggil)
- `sk "<tugas>" -n 5` — cari skill (badge [siap]/[butuh:x])
- `sk -l <nama>` — muat SKILL.md · `sk --design` / `sk --repo` — filter khusus
- `pow find "<tugas>"` — cari skill+repo+tool sekaligus
- Skill dari repo: `repo-hub.py get <owner/name>` lalu `repo-hub.py ingest`

## Data & dataset (tambahan)
- `data-hub list|search|get|peek` — 23 dataset curated siap pakai + indeks
  **957rb+ dataset** (`~/.agents/datasets-index.db`: HuggingFace 950rb,
  OpenML 7rb, Zenodo) — metadata saja, file di-fetch on-demand.
- Fetch: `data-hub get hf:<owner>/<nama>` / `openml:<id>` / `zenodo:<id>`
- EDA instan: `data-hub peek <slug>` (auto-download + shape/stats/sample ≤40 baris)
- Menara/teknik: concrete-strength, steel-plates-faults, airfoil-noise,
  energy-efficiency, yacht-hydrodynamics + skill fisika-dasar, struktur-menara,
  antena-telekomunikasi, meteorologi-cuaca, geodesi-survei, statistika-data,
  data-science-kaggle.
