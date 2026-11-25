---
name: geo-audit
description: >
  Run a full multi-page GEO audit on a website. Sequential pipeline: locale
  detection → multi-page sampling → robots.txt crawler audit → per-page
  schema + content-health checks → optional RRF measurement on Google + Brave
  (when --positioning is supplied) → unified report with per-LLM action plan.
  Output: a single Markdown audit at site-client/<slug>/audits/<date>-audit.md.
  Use when the user asks for a full audit on a URL.
allowed-tools: Bash, Read, Grep, Glob, Write
---

# geo-audit — multi-page GEO audit

The main entry point of the toolkit. One command, one Markdown report.

## Command

```bash
python3 -m scripts.run_audit <url> \
  [--positioning "<query>"] \
  [--vs comp1.com,comp2.com] \
  [--engines google,brave] \
  [--max-pages 8] \
  [--output-lang fr|en]
```

## Pipeline (5 sequential phases)

| Phase | Module | What runs |
|---|---|---|
| 1. Locale detection | `scripts/site_locale.py` | HTML `lang` → `Content-Language` → TLD → fallback `en` |
| 2. Multi-page sampling | `scripts/site_crawler.py` | sitemap-aware + strategic diversity (home + service + article + about + case-study) |
| 3. Crawler audit | `scripts/checks/crawlers.py` | robots.txt parse, 3-category bot taxonomy (training / RAG / user-request) |
| 4. Per-page schema + content health | `scripts/checks/{schema,content_health}.py` | JSON-LD validity + EEP visible-facts coverage; BLUF + Mount AI patterns |
| 5. RRF measurement (optional) | `scripts/rrf.py` + `scripts/serp/{google,brave}.py` | when `--positioning` is supplied, runs 10 fan-out queries × 2 engines |

## Output structure

The audit lands at `site-client/<slug>/audits/<YYYY-MM-DD>-audit.md`. Path
resolved by `scripts/client_paths.py` (per-client folder convention).

```
1. État des lieux par LLM        ← verdict table + 5 LLM detail blocks
2. Plan d'action                  ← unified, per-LLM impact tags
3. Ce que l'audit ne mesure pas

Annexes techniques:
  A. RRF mesuré (détail)
  B. Crawlers IA (robots.txt)
  C. Schema multi-page
  D. Content health multi-page
  E. Findings — vue agrégée

Glossaire technique
```

## When NOT to use this skill

- Single-page schema-only or content-only checks → invoke
  `scripts/checks/schema.py` or `scripts/checks/content_health.py` directly.
- RRF-only measurement on existing fan-out queries → use the `geo-rrf`
  skill or `scripts/rrf.py` directly.
- Per-client folder management (without a fresh audit) → use `geo-client`.

## Examples

```bash
# Full audit, French output, positioning mode
python3 -m scripts.run_audit "https://example.fr/" \
  --positioning "agence de design" \
  --vs concurrent1.fr,concurrent2.fr \
  --output-lang fr

# Audit without RRF (on-page only, no SERP scrapes)
python3 -m scripts.run_audit "https://example.com/"
```

## Dependencies

- `scripts/run_audit.py` (orchestrator)
- All modules under `scripts/checks/`, `scripts/serp/`, plus `scripts/rrf.py`,
  `scripts/fanout.py`, `scripts/llm_impact.py`, `scripts/i18n.py`,
  `scripts/site_crawler.py`, `scripts/site_locale.py`, `scripts/client_paths.py`
- Python deps: `requests`, `beautifulsoup4`, `lxml` (see `requirements.txt`)
