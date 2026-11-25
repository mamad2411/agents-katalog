---
name: geo
description: >
  GEO Audit Toolkit — evidence-based Generative Engine Optimization audit for
  websites. Diagnostic-only (no commercial framing): produces a multi-page
  audit with per-LLM presence assessment (ChatGPT/Google, Gemini/Google,
  Perplexity/multi, Claude/Brave, Le Chat/Brave), a unified action plan
  with per-LLM impact tags, and technical appendices. Use when the user
  says "geo", "audit", "AI search", "AI visibility", "schema", "BLUF",
  or provides a URL for analysis.
allowed-tools: Read, Grep, Glob, Bash, WebFetch, Write
---

# GEO Audit Toolkit — Claude Code skill

> **Philosophy:** audit-only, evidence-based, no sales framing. Findings are
> reported in `severity × confidence × per-LLM impact`, never in pricing tiers
> or revenue projections.

---

## Single command

```
/geo audit <url> [--positioning "<query>"] [--vs comp1.com,comp2.com] [--output-lang fr|en]
```

Examples:

```
# Audit with positioning + 2 competitors, output in French
/geo audit https://example.com --positioning "agence powerpoint" --vs mprez.fr,laboiteaslides.fr --output-lang fr

# Audit without RRF measurement (on-page only)
/geo audit https://example.com
```

Internally calls `python3 -m scripts.run_audit <url> ...`. The orchestrator is
sequential (not parallel-subagent) and produces a single Markdown audit at
`site-client/<slug>/audits/<date>-audit.md`.

---

## Per-LLM retrieval map (rev. 2026-04-26)

| LLM (in scope) | Backend | Engine in audit |
|---|---|---|
| ChatGPT / SearchGPT | **Google** (OpenAI–Google deal 2025) | `google` (Startpage proxy) |
| Gemini / Google AI Overviews | **Google** | `google` |
| Perplexity | Multi (Google + Brave) | `google` + `brave` |
| Claude | **Brave** (Anthropic–Brave 2025) | `brave` |
| Le Chat (Mistral) | **Brave** (Brave–Mistral 2025) | `brave` |

Bing Copilot, Meta AI, Grok are **out of scope** (user decision, 2026-04-26).
Mapping validated empirically: 80–90% Google SERP similarity vs ~30% Bing
when comparing ChatGPT citations to scraper-baseline. See
[`docs/LLM_RETRIEVAL_ARCHITECTURE.md`](../docs/LLM_RETRIEVAL_ARCHITECTURE.md).

---

## Audit pipeline (5 phases, sequential)

| Phase | What runs | Output |
|---|---|---|
| 1. Locale detection | `scripts/site_locale.py` (HTML lang → Content-Language → TLD → fallback) | `fr-FR`, `en-US`, etc. |
| 2. Multi-page sampling | `scripts/site_crawler.py` (sitemap + strategic diversity: home + service + article + about + case-study) | up to 8 pages |
| 3. Crawler audit (site-level) | `scripts/checks/crawlers.py` (robots.txt parse + 3-category bot taxonomy) | findings |
| 4. Per-page schema + content health | `scripts/checks/schema.py` + `scripts/checks/content_health.py` | findings per page |
| 5. RRF measurement (when `--positioning`) | `scripts/rrf.py` + `scripts/serp/{google,brave}.py` (10 fan-out queries × 2 engines) | per-LLM presence stats |

---

## Audit output structure

```
1. État des lieux par LLM        ← verdict table + 5 detail blocks
2. Plan d'action                  ← unified, per-LLM impact tags + experimental sub-bucket
3. Ce que l'audit ne mesure pas

Annexes techniques:
  A. RRF mesuré (détail)
  B. Politique des crawlers IA
  C. Données structurées (schema)
  D. Content health (BLUF, etc.)
  E. Findings — vue agrégée

Glossaire technique
```

Every audit lands in `site-client/<slug>/audits/<YYYY-MM-DD>-audit.md`. Path
resolved via `scripts/client_paths.py`.

---

## Active sub-skills (6)

| # | Skill | Wraps | Purpose |
|---|---|---|---|
| 1 | `geo-audit` | `scripts/run_audit.py` | Main orchestrator |
| 2 | `geo-schema` | `scripts/checks/schema.py` | Schema.org + Enhanced Entity Pages audit |
| 3 | `geo-content-health` | `scripts/checks/content_health.py` | BLUF + Mount AI anti-patterns |
| 4 | `geo-crawlers` | `scripts/checks/crawlers.py` | robots.txt + 3-category bot taxonomy |
| 5 | `geo-rrf` | `scripts/rrf.py` | Reciprocal Rank Fusion measurement |
| 6 | `geo-client` | `scripts/client_paths.py` | Per-site folder manager (`site-client/<slug>/`) |

The fork dropped 9 upstream skills that did not fit the audit-only pivot
(`geo-prospect`, `geo-proposal`, `geo-brand-mentions`, `geo-citability`,
`geo-llmstxt`, `geo-platform-optimizer`, `geo-technical`, `geo-content`,
`geo-report`, `geo-report-pdf`, `geo-compare`). See `tasks/lessons.md`.

---

## Local-only tooling

`local/` is gitignored. Contains personal scripts that don't ship in the
public toolkit:

- `local/docx_export.py` — convert audit Markdown to a styled `.docx`
  (Google Docs ready). Usage:
  ```
  python3 local/docx_export.py site-client/<slug>/audits/<date>-audit.md
  ```

---

## Quality gates

- **Audit-only**: no pricing tiers, no MRR projections, no "client-ready"
  framing. Findings carry `effort × score-gain × confidence`.
- **Evidence triage**: every finding tagged with confidence (`high` →
  `experimental`). Single-study correlations and emerging patterns are
  flagged, not promoted to critical.
- **Free, no-setup**: pipeline runs without paid APIs or signup. SERP
  scraping uses public interfaces (Google via Startpage proxy, Brave HTML).
- **Output language follows audited site's locale** (override with
  `--output-lang fr|en`).
- **Per-LLM retrieval map re-verified every 6 months** — partnership deals
  change quickly. See `tasks/lessons.md` (2026-04-26 entry).

---

## Reference docs

- [`docs/LLM_RETRIEVAL_ARCHITECTURE.md`](../docs/LLM_RETRIEVAL_ARCHITECTURE.md) — per-LLM backend mapping
- [`docs/CRAWLERS_TAXONOMY.md`](../docs/CRAWLERS_TAXONOMY.md) — 29 AI bots catalogued
- [`docs/STRUCTURED_DATA_BEST_PRACTICES.md`](../docs/STRUCTURED_DATA_BEST_PRACTICES.md) — Schema.org / EEP methodology
- [`docs/CONTENT_HEALTH_PATTERNS.md`](../docs/CONTENT_HEALTH_PATTERNS.md) — Mount AI anti-patterns + BLUF
- [`docs/BRAVE_GRAIL_SIGNALS.md`](../docs/BRAVE_GRAIL_SIGNALS.md) — Brave-rooted LLM evidence (Test #1 result)
- [`docs/sources/`](../docs/sources/) — 8 archived methodology articles with critical-thinking triage
