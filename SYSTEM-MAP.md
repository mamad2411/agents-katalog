# SYSTEM-MAP — indeks seluruh ekosistem ~/.agents

Satu peta semua subsistem: apa, di mana, cara AI memanggil, status.
Jangan jalankan ulang yang sudah ada — cek status dulu.

## 1. Katalog Skill (inti)
| Komponen | File/DB | Cara pakai |
|---|---|---|
| Index skill | `skills-index.db` (634rb baris: 482rb aktif + 151rb junk) | `sk "<tugas>" -n 5` |
| Mesin cari | `skillq.py` (FTS5+IDF+sinonim ID+language-aware+feedback skusage) | `sk -l <nama>` muat |
| Builder index | `build_skills_index.py` | rebuild manual/background |
| Peta katalog | `SKILL-CATALOG.md` | baca on-demand (domain→jumlah) |
| Kesiapan dep | `skills-ready.py` | `--report` → skills-readiness.md |
| Scan injeksi | `inject-scan.py` + `inj` | pola berbahaya di skill/repo |
| Dedup/junk | `dedup-skills.py`, `skills-junk-manual.txt` | auto-junk tiap rebuild |
| Auto-tuner | `skill-auto-tuner.py` → `skill-tuned-routes.json` | routing optimal dari efficacy log |

## 2. Repo
| Komponen | File/DB | Cara pakai |
|---|---|---|
| Index repo | `repos.db` (176rb+) | `sk --repo "kata"` |
| Fetch on-demand | `repo-hub.py get <owner/name>` | shallow clone → repo-refs/ |
| Ingest skill | `repo-hub.py ingest` | repo → skills-expanded |
| Scan keamanan | `repo-hub.py scan` / `inj` | sebelum pakai repo asing |
| Trending/top | `repo-hub.py trending|top` | repo naik_daun |

## 3. Dataset
| Komponen | File/DB | Cara pakai |
|---|---|---|
| Index dataset | `datasets-index.db` (957rb+: HF 950rb, OpenML 7rb, Zenodo) | `data-hub search "kata"` |
| Fetch+EDA | `data-hub.py` + `data-eda.py` (test-venv pandas) | `data-hub get|peek <slug>` |
| Indexer | `dataset-indexer.py [hf|openml|zenodo]` | resumable, cursor meta |
| Data lokal | `datasets/` (±2MB curated) | 23 dataset siap pakai |

## 4. MCP
| Komponen | File | Cara pakai |
|---|---|---|
| Katalog MCP | 75 server teregistrasi, semua DISCAN+DISABLED | `pow mcp search|cat|on|off` |
| Guard/hygiene | `mcp-guard.py`, `mcp-hygiene.py`, `mcp-doctor.py` | parkir idle >7 hari |
| Gateway/proxy | `mcp-gateway.py`, `mcp-proxy-manager.py`, `mcp-router.py` | retrieve(query)→cap |
| Aset komunitas | `cap-store/`, `cap-crawler.py`, `retrieve.py`+`retrieve.db` | hybrid BM25+rerank |

## 5. Memori & sesi
| Komponen | Lokasi | Cara pakai |
|---|---|---|
| Memori global | `memory/MEMORY.md`, `memory-store.py` | `memory-store add|recall` |
| Digest sesi | `memory/sessions/` | auto simpan per sesi |
| Mirror Obsidian | `~/mamatXobsidian/00 - Inbox/agent-memory/` | sinkron manual |
| Arsip sesi | `archive-sessions.py` | kompresi sesi lama |

## 6. Tooling dev
| Komponen | File | Fungsi |
|---|---|---|
| project-forge | `project-forge.py` | scaffold+gate project baru |
| testing-forge | `testing-forge.py` + `TESTING/` | 13 lapisan test, generate/audit |
| security-forge | binary di bin/ | audit, headers, TLS, secrets |
| media-forge | `media-forge.py` + media-venv | ffmpeg/imagemagick/manim/lottie |
| repo-map | `repo-map.py` | peta struktur repo sebelum baca |
| tool-install | `tool-install.py` | install tool repo → ~/.agents/tools |

## 7. Desain/UI
| Komponen | File | Fungsi |
|---|---|---|
| Playbook | `DESIGN-PLAYBOOK.md` | kontrak desain wajib |
| Referensi ukur | `dref`, `dcheck`, `dvisual`, `dcopy` | screenshot/metrik/gate a11y |
| Skill desain | `sk --design` + design-skills.json | kurasi UI |
| Anti-slop | skills `anti-ui-slop`, `de-sloppify` | self-check output |

## 8. Observability & guard
| Komponen | Fungsi |
|---|---|
| `mamat-doctor`, `mamat-selftest`, `mamat-usage`, `mamat-sec`, `mamat-net`, `mamat-eval`, `mamat-weekly`, `mamat-snap`, `mamat-mem`, `mamat-backup`, `mamat-sandbox` | monitoring 0-token |
| `ai-context-audit.py`, `token-telemetry.py`, `usage-audit.py`, `opencode-limit-guard.py`, `context-guard.py`, `loop-guard.py`, `cline-guard.py`, `device-guard.py` | anti boros/kebocoran |
| `skill-lint.py`, `skill-scan.py`, `aggressive-scan.py` | kesehatan katalog |

## 9. Integrasi multi-tool
| Komponen | File |
|---|---|
| Sinkron rules | `RULES.md` → `sync-rules.py` → claude/cursor/copilot/cline/codebuddy/gemini/codex |
| Auto-trigger | `AUTO-TRIGGERS.md` (maksud→tool, baca on-demand) |
| Plugin opencode | `skill-inject.ts`, `token-guard.ts`, `mamat-brand` |
| Model routing | `mamat-auto.py` + `model-routing.md` (quick/coding/reasoning/best) |
| Peta command | `COMMANDS.md`, `CHEATSHEET.md`, `TESTING.md` |

## 10. Yang SENGAJA tidak ada / opsional
- **Secrets vault** — tidak dibuat (env/Keychain native sudah cukup; vault custom = risiko).
- **Scheduler umum** — `launchd-backup` ada untuk backup; cron job lain belum perlu.
- **Vector DB lokal** — codebase-memory MCP + retrieve.db FTS sudah cukup; Qdrant MCP ada kalau perlu.
- **Feedback sk→tuner wiring** — `skusage` (skillq) dan efficacy log (auto-tuner) belum disatukan; kandidat perbaikan berikutnya.
- **Zenodo penuh** — indexer jalan background (API limit 25/req), target ~5rb.

## Aturan main
- Cek peta ini dulu sebelum bikin tool/index baru — kemungkinan sudah ada.
- Semua index DB di `~/.agents/*.db` — metadata kecil, data on-demand.
- Update peta ini tiap ada subsistem baru.
