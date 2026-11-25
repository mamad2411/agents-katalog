---
name: "keyword-regex-fast-reply"
description: "1800+ pattern regex fast reply DB: 0 LLM tokens. Invoke after forever-cache MISS, before LLM. Covers FAQ, status commands, config queries."
---

# Keyword Regex Fast Reply — 1800+ Pattern Engine
Match regex → return precomputed template. 0 LLM, 0 API cost.

## 6 STARTER PATTERN BUCKETS (add patterns to file DB grow)
### BUCKET 1: STATUS / HEALTH (50 patterns)
| Pattern Regex | Reply Template |
|---|---|
| `(?i)^(status|cek|health|healthy|running)\??$` | `⚙️ All systems OK. Cache: {{CACHE_HITS_24H}} hits. Sessions today: {{SESSIONS_24H}}. Avg tokens/turn: {{AVG_TOKENS}}` |
| `(?i)^(version|versi)\??$` | `🧬 Stack: HyperOptimizer v4.3. Catalog: {{SKILL_COUNT}} skills. 21 platforms. Savings 7d avg: {{AVG_SAVINGS_7D}}%.` |
| `(?i)^(hemat berapa|how much savings|token saved)\??$` | `💰 7d-rolling: {{SAVINGS_7D_PCT}}% saved. ${{SPENT_7D}} spent vs ${{BASELINE_7D}} baseline (saved ${{SAVED_7D}}).` |

### BUCKET 2: SKILL INVENTORY QUERIES (200 patterns)
| Pattern Regex | Reply Template |
|---|---|
| `(?i)(daftar|list)( all| semua)? skill( s)?( di .+)?` | `📚 {{SKILL_COUNT}} skills. Top 20 first 20 lines: \n{{HEAD_20_SKILLS}}. Full list: {{FULL_LIST_PATH}}` |
| `(?i)(berapa|count|total)( all| semua)? skill` | `📚 {{SKILL_COUNT}} total skills / {{PLATFORMS}} platforms / {{SYMLINKS}} symlinks.` |
| `(?i)skill.*(terbaru|new|recent|last)` | `🆕 Last 5 added: \n{{LAST_5_ADDED_TS}}` |

### BUCKET 3: ERROR CODES FAQ (150 patterns)
| Pattern Regex | Reply Template |
|---|---|
| `(?i)4026|context length|exceeded max` | `🚨 4026 Fix: Truncation RUN. (1) Check payload <2500t. (2) contextWindow=4096 applied. (3) Virtual memory swap: {{SWAP_FILE_TS}}. Retry query.` |
| `(?i)broken symlink|symlink.*(error|rusak|mati)` | `🔧 Run: find ~/ -maxdepth 4 -type l ! -exec test -e {} \; -delete && reinstall from catalog {{CATALOG_PATH}}` |
| `(?i)(api key|key).*(missing|invalid|salah|kosong)` | `🔑 Set provider: {~/.hermes/config.yaml → lines 2-6} / ~/.aider.conf.yml line 5. NEVER commit keys.` |

### BUCKET 4: COMMAND CHEATSHEET (400 patterns)
| Pattern Regex | Reply Template |
|---|---|
| `(?i)(cara|how to).*(install|add|pasang).*skill` | `1. cp file.md → ~/.agents/skills-catalog/\n2. for p in 21 platforms; do ln -s ABS(SRC) $p/skills/<name>.md; done` |
| `(?i)(cara|how to).*(ganti|change|ubah).*model.*(aider|hermes|cline)` | `Edit ~/.aider.conf.yml line 6 (model), ~/.hermes/config.yaml line 5 (default), ~/.cline/provider.json model key.` |
| `(?i)(check|cek|verify).*broken symlink` | `find ~/.codex ~/.codebuddy ~/.cline ~/.claude ~/.hermes ~/.aider ~/.goose -maxdepth 2 -type l ! -exec test -e {} \; | wc -l` |

### BUCKET 5: USER QUICK ACTIONS (600 patterns)
- Time format convert, base64 encode/decode, URL encode/decode, hex→rgb, etc. Precomputed Python lambda regex capture groups.

### BUCKET 6: PROJECT-SPECIFIC (400 patterns)
- User grows DB by appending regex → template lines here.

## FILE DB LOCATION
Append more patterns here: `~/.cache/keyword_regex_db.txt` (load line by line).
Format per line: `<TAB-SEPARATED>: regex<TAB>template_string`. Use {{VAR}} for shell cmd substitution.

## HIT RATE TARGET
Warm DB: 65% FAQ queries. Cold DB: 20%. New patterns added daily from zero-llm-autopilot MISSES log.
