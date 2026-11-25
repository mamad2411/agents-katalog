---
name: geo-rrf
description: SERP-based RRF (Reciprocal Rank Fusion) audit. Measures how a target domain ranks across DuckDuckGo and Brave for a set of fan-out queries derived from a seed, then compares to competitors. Reports per-engine RRF scores and per-LLM citation likelihood signals (ChatGPT/Bing-Copilot via DDG, Claude/Le Chat/Meta AI/Grok/Perplexity via Brave). Free, no API key required.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - Write
---

# RRF (Reciprocal Rank Fusion) — audit module

## Purpose

Measure where a target domain actually ranks on the search backends that LLMs use, expand the user's seed query into ~12-30 fan-out variants, and produce a comparative score against named competitors. This is the toolkit's primary **measured** signal (vs. the **structural** signals from `geo-schema`, `geo-crawlers`, etc.).

Methodology and per-LLM mapping live in [`docs/LLM_RETRIEVAL_ARCHITECTURE.md`](../../docs/LLM_RETRIEVAL_ARCHITECTURE.md). The implementation is in [`scripts/rrf.py`](../../scripts/rrf.py) and [`scripts/serp/`](../../scripts/serp/).

## Output language

By default, the report is written in the **audited site's language**, detected via `scripts/site_locale.py` (HTML `lang` → `Content-Language` header → TLD → fallback `en`). User can override with `--output-lang <iso2>`. See `CLAUDE.md` rule "Output language".

---

## What the audit does

For a target URL/domain `D`, a list of seed queries, and an optional list of competitor domains:

1. **Detect locale** (HTML `<html lang>` → `Content-Language` → TLD → CLI override). Lets the user override via `--lang` and `--country`.
2. **Generate fan-outs** from each seed query via locale-aware templates (FR/EN/DE/ES/IT/PT) plus Google PAA + Related Searches when available. Caps at 30 queries by default.
3. **For each engine and each query**, fetch the SERP (cached on disk under `.serp_cache/` for 24h by default).
4. **Compute per-engine RRF**: $RRF(D, e) = \sum_{q} \frac{1}{60 + rank_q(D)}$. Same formula for each named competitor.
5. **Output**: Markdown report with per-engine scores, comparative strength, per-LLM citation-likelihood mapping, and per-query rank table.

## Engines

| Engine | Status | Covers (per `docs/LLM_RETRIEVAL_ARCHITECTURE.md`) |
|---|---|---|
| `bing` (Bing direct, mobile UA) | ✅ **Primary** for ChatGPT / Bing Copilot | Bing's index is ChatGPT's actual backend — most accurate proxy |
| `brave` (Brave HTML SERP) | ✅ Reliable | Claude, Le Chat (Mistral), Meta AI, Grok agentic, Perplexity historical |
| `ddg` (DuckDuckGo HTML) | ⚠️ Rate-limits aggressively (HTTP 202 after few queries) | Fallback Bing-derived when `bing` fails. Better at low volume than at scale |
| `google` (Google scrape) | ❌ Blocked by anti-bot in 2026 (no-JS redirect) | Gemini, Google AI Overviews — uncertain when blocked |

**Default engine list**: `bing,brave,ddg` (3 engines, covers 6 LLMs reliably). Add `google` to attempt Gemini coverage (will likely fail with a clean "blocked" error).

When an engine fails for a specific query, that query is reported as `n/a` for that engine (distinct from `—` which means "engine answered but domain not in top 100"). No silent degradation; the report includes an "Engine health" section showing the answer rate per engine, and a data-warning banner if any engine has >30% failure rate.

## Command

```bash
/geo rrf <url> [--seed q1,q2,...] [--vs c1,c2,...] [--lang fr] [--country FR] [--engines ddg,brave]
```

If `--seed` is not provided, prompt the user for one or two seed queries (the audit needs anchors — usually the site's most important branded or generic query).

If `--vs` is not provided, the audit runs target-only and reports just the per-engine RRF (no comparative — but still informative).

Per-engine selection: default `ddg,brave`. Add `google` to attempt Gemini coverage (will likely fail with a clean "blocked" error in 2026).

## Implementation steps

When invoked:

1. **Detect locale**:
   ```bash
   python3 ~/.claude/skills/geo/scripts/site_locale.py "<URL>" [--lang <CLI>] [--country <CLI>]
   ```
2. **Resolve client paths** (cache + output):
   ```bash
   eval "$(python3 ~/.claude/skills/geo/scripts/client_paths.py paths '<URL>')"
   # $CLIENT_DIR, $ASSETS_DIR set
   ```
3. **Generate fan-outs** for each seed, dedupe, cap at 30 (configurable):
   ```bash
   python3 -m scripts.fanout "<seed>" --locale "<lang-COUNTRY>"
   ```
4. **Run RRF** with all selected engines:
   ```bash
   python3 -m scripts.rrf "<domain>" \
     --queries "<comma-list>" \
     --vs "<competitors>" \
     --engines ddg,brave \
     --locale "<lang-COUNTRY>"
   ```
5. **Write the markdown report** to `$CLIENT_DIR/audits/<YYYY-MM-DD>-rrf.md`.
6. **Update `info.json`**: append a `rrf_run` entry with the date, the engines used, and the comparative-strength summary. Refresh INDEX:
   ```bash
   python3 ~/.claude/skills/geo/scripts/client_paths.py index
   ```

If user passes `--cwd`, write to `GEO-RRF-AUDIT.md` in current directory and skip the client folder steps.

## Output structure

The Markdown report contains:

```markdown
# RRF Comparative Audit — <domain>
**Locale:** <lang-COUNTRY>
**Queries used:** N
**Engines:** ddg, brave[, google]
**Competitors compared:** <list>

## Per-engine RRF scores
| Domain | ddg RRF | brave RRF | ddg top10/total | brave top10/total |
| ...    | ...     | ...       | ...             | ...               |

## Comparative strength (target / max competitor)
`1.0` = strongest on this engine. `0.0` = absent / weakest.

## Estimated per-LLM citation likelihood
- ChatGPT / Bing Copilot ← ddg
- Claude / Le Chat / Meta AI / Grok ← brave
- Perplexity ← brave + ddg (multi-source fusion)
- Gemini / Google AIO ← google (often blocked from no-setup tools)

## Query-level detail (target only)
| Query | ddg | brave | ... |
```

## Findings produced (severity / confidence / effort)

For each engine that ran successfully:

- If **target's top10 count is 0**: severity High, confidence High. Recommendation: structural work (schema, content, BLUF) for the queries where the target was absent.
- If **target's RRF is much smaller than the strongest competitor (relative_strength < 0.4)**: severity Medium, confidence High. Recommendation: identify which queries the competitor wins on and analyse their structural advantages.
- If **target ranks 11-30 (close to top 10)**: severity Low, confidence High. Quick wins via on-page optimisation likely.
- If **target absent from all queries on Brave specifically**: severity High for Claude/Le Chat/Meta AI/Grok citation likelihood.

## Confidence framing

- **RRF score itself**: high confidence (deterministic algorithm on observed SERP positions).
- **Per-LLM mapping**: medium confidence (architecture cited in `LLM_RETRIEVAL_ARCHITECTURE.md` is the best public knowledge but evolves).
- **Google as proxy for Gemini**: low confidence when Google is blocked; the audit reports "uncertain" rather than a fabricated number.

## What this skill does NOT do

- **No actual LLM citation testing.** That requires paid LLM APIs.
- **No traffic / revenue projections.** Per audit-only philosophy.
- **No fan-out generation via LLM API.** Templates + Google PAA scrape only.
- **No GRAIL signal capture.** Test #1 (`docs/BRAVE_GRAIL_SIGNALS.md`) confirmed Ask Brave is paywalled and SPA-rendered — out of scope for a free, no-setup tool.
