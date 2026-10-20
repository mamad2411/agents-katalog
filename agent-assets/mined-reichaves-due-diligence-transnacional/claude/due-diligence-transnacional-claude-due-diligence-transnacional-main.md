# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## About this project

CLI pipeline for investigative journalism: cross-references any person with U.S. ties against U.S. public databases (FEC, LDA, FARA, state corporate registries, OpenCorporates, press archives) and produces a source-cited, confidence-scored PDF dossier.

Developed and maintained by Reinaldo Chaves (data journalist in Brazil) — https://br.linkedin.com/in/reinaldochaves

Target user: a Brazilian investigative journalist (default language: Portuguese) or any international journalist (set `investigation_language: en-US` in `target.yaml`).

---

## Development commands

```bash
# Install dependencies (preferred)
pip install uv && uv sync

# Or with pip
pip install -e ".[dev]"

# Run all tests
pytest tests/ -v

# Run a single test file
pytest tests/test_identity_expansion.py -v

# Run a single test by name
pytest tests/test_identity_expansion.py::test_remove_diacritics -v

# Lint
ruff check .

# Type check
mypy skills/ scripts/ tests/

# Smoke-test a script before declaring it done
python -m py_compile skills/expand-brazilian-identity/scripts/expand_identity.py

# CLI entrypoint (installed as `ddt` via pyproject.toml)
python scripts/run_pipeline.py --target examples/case-fictional/target.yaml
python scripts/run_pipeline.py --target target.yaml --skip-search --findings-dir findings/

# Generate PDF dossier (Portuguese default; pass --lang en-US for English)
python skills/generate-dossier-pdf/scripts/generate_report.py \
    --consolidated cases/<slug>/findings-consolidated.json \
    --output cases/<slug>/dossier.pdf \
    --lang pt-BR
```

---

## Slash commands (Claude Code)

Commands live in `.claude/commands/` and are loaded automatically when Claude Code opens in this directory. Both Portuguese and English variants are available:

| Portuguese | English | Description |
|---|---|---|
| `/investigar "Nome"` | `/investigate "Name"` | Full 5-stage pipeline |
| `/consultar-base <base> "Nome"` | `/search-database <db> "Name"` | Single database query |
| `/expandir-nome "Nome"` | `/expand-name "Name"` | Name variation expansion only |
| `/gerar-dossie <findings.json>` | `/generate-dossier <findings.json>` | PDF from existing findings |

> `plugin.json` at the repo root is a legacy artifact — it is **not** read by Claude Code and registers nothing. The only mechanism Claude Code uses is `.claude/commands/`.

---

## Architecture

### Pipeline flow (5 stages)

```
target.yaml → expand-brazilian-identity → [human review] →
parallel searches (FEC / LDA / FARA / state-corps / OpenCorporates / news) →
triangulate-findings → [human review] → generate-dossier-pdf
```

Each stage is a standalone Python script. `scripts/run_pipeline.py` orchestrates them via subprocess. The Claude Code commands invoke the same logic via sub-agents.

### Skills directory structure

Skills live in `skills/<skill-name>/` at the project root. Each skill has:
- `SKILL.md` — instructions loaded by Claude via `CLAUDE.md` context
- `scripts/` — runnable Python scripts (standalone CLIs)
- `references/` — static reference documents

The skill directories use **hyphens** in their names (e.g., `search-lobby-fara`), which makes them non-importable by standard Python `import`. Tests use `importlib.util.spec_from_file_location` to import functions directly from these paths. Follow this pattern when writing new tests.

### FEC search — 3-level execution

`skills/search-fec/SKILL.md` defines a tiered execution strategy:

1. **Level 1** — `mcp__fec-mcp__*` tools (when `fec-mcp` MCP server is active, configured in `.mcp.json`)
2. **Level 2** — `mcp__osint-investigation__*` tools (secondary MCP fallback)
3. **Level 3** — `skills/search-fec/scripts/fec_search.py` (Python script, always available)

Every finding record must include a `methodology_note` stating which level executed the search. See `skills/search-fec/references/mcp-detection.md` for templates.

### Schema validation

All inter-stage JSON files are validated against JSON Schema Draft 2020-12 schemas in `schemas/`. Key schemas:

- `target.schema.json` — input; `nome_completo` + `razao_investigativa` required
- `identity-variations.schema.json` — output of expand stage; `approved_by_human` must be `true` before searches run
- `findings.schema.json` — output of each search sub-skill
- `findings-consolidated.schema.json` — output of triangulate stage
- `confidence-levels.schema.json` — enum: `confirmado` / `provável` / `indício` / `não-encontrado`

### Internationalisation

`target.yaml` accepts `origin_country` (ISO 3166-1 alpha-2, default `"BR"`) and `investigation_language` (`"pt-BR"` or `"en-US"`). The name-expansion algorithm is nationality-agnostic; transliteration coverage is lower for non-Latin names (Chinese, Arabic, Nigerian) — always flag this to the user and request careful review of generated variations.

### PDF generation — language and bilingual output

`generate_report.py` resolves language in this order: `--lang` CLI flag → `investigation_language` in `target.yaml` → `pt-BR`. All section labels, table headers, confidence-level strings, and the disclaimer block are driven by the `STRINGS` dict at the top of that file. Add keys to both `pt-BR` and `en-US` sub-dicts whenever adding new UI text.

### PDF generation — ReportLab word-wrap requirement

**Critical:** ReportLab `Table` cells containing plain Python strings do NOT word-wrap — text overflows the cell boundary. Every cell value must be wrapped with `_cell(text, style)` (defined in `generate_report.py`), which calls `xml.sax.saxutils.escape` and returns a `Paragraph` object. The `cell_key`, `cell_body`, and `cell_conf` styles in `dossier_template.py` all set `wordWrap="LTR"`. If you add a new table section, always use `_cell()` for every data cell.

### Case output directory convention

Live investigation outputs are stored under `cases/<slug>/`:

```
cases/<slug>/
├── target.yaml                  # input
├── identity-variations.json     # approved_by_human: true required
├── findings/                    # one JSON per search sub-skill
│   ├── fec.json
│   ├── lda-fara.json
│   ├── state-corps.json
│   ├── opencorporates.json
│   └── news.json
├── findings-consolidated.json   # output of triangulate stage
├── dossier.pdf                  # Portuguese PDF
└── dossier-en.pdf               # English PDF (optional)
```

`cases/` is gitignored by default — never commit real investigation outputs.

### Known fragile external dependencies

- **Florida Sunbiz** (`florida_sunbiz.py`) — returns HTTP 403 on automated requests. When the script fails, document the failure in findings and direct the user to manual search at sunbiz.org.
- **OpenCorporates** (`opencorporates_search.py`) — requires a valid `OPENCORPORATES_API_KEY`; returns HTTP 401 without one. Fallback: ICIJ Offshore Leaks database (public, no key needed).
- Both failures must be recorded in the findings JSON with `status: "error_403"` / `status: "error_401"` and `confidence: "inconclusivo"` — never silently skip.

---

## Non-negotiable principles

1. **Anti-hallucination above all.** If a database returned nothing, say "not found" — never invent. Every claim in the dossier must have an explicit source (database + ID/URL + retrieval date).

2. **"Not found" is a finding.** The absence of traces is journalistic data when methodology is documented. Always show *what was searched*, not only *what was found*.

3. **Name variations are mandatory.** Before any U.S. database search, expand to at minimum: full name, surname only, inverted order, initials, accent-stripped variants, and direct relatives when known.

4. **Legal context always present.** When a search hits a legal barrier (e.g., 52 U.S.C. § 30121 bars foreign nationals from donating to federal campaigns), explain the barrier in the dossier — it is part of the finding.

5. **Confidence level on every claim.** Scale: `confirmado` / `provável` / `indício` / `não-encontrado`. See `skills/due-diligence-transnacional/references/confidence-levels.md`.

6. **Never expose unnecessary PII.** Residential addresses, birth dates, and CPF/SSNs only appear in the dossier when required for unambiguous identification. Otherwise redact.

---

## Editorial standards

- No speculative adjectives ("supposedly", "apparently") — use confidence levels instead.
- Source citation format: `(Source: FEC Schedule A, ID 202401120300xxx, retrieved DD/MM/YYYY)`
- No emoji, no marketing language, no exclamation marks.
- Dates: `DD/MM/YYYY` in Portuguese output; `MM/DD/YYYY` in English output.
- USD values with approximate BRL parity when relevant; always show USD first.

---

## Secrets and API keys

Never write keys in code. Use `.env` (copy from `.env.example`).

| Key | Service |
|-----|---------|
| `FEC_API_KEY` | api.open.fec.gov — free; raises rate limit from 1k/day to 1k/hour |
| `OPENCORPORATES_API_KEY` | opencorporates.com — free tier 50 req/day; journalist plan free |
| `ANTHROPIC_API_KEY` | Optional — only needed outside Claude Code |

---

## When NOT to use this pipeline

- Private individuals without public relevance (see `docs/ethics.md`)
- Targets with no documented U.S. tie — no U.S. database will have results
- Cases requiring qualitative document analysis — use Claude directly
- Deadlines under 15 minutes — end-to-end pipeline takes 15–30 min
