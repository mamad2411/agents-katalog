# Cache Hit Audit Script

## Summary

**One-sentence:** Daily-cron audit that parses Anthropic API responses, computes per-prompt cache_read_tokens / total_input_tokens ratio, and emits a Markdown report flagging cache-poison prefixes.

**One-paragraph:** Anthropic prompt-cache reuse is fragile: a moved newline, an injected timestamp, or a per-user variable in the system prompt drops the cache hit rate from 92% to 30% with no error message. The recipe for auditing — what prefix is stable, what poisons cache, how to recover the win — sits in tribal knowledge. This methodology codifies the audit into a daily-cron script that parses trace export, computes per-prompt-prefix `cache_read_tokens / total_input_tokens` ratio, clusters prefixes by hash, diffs against the previous run, and emits a Markdown report listing prefixes whose ratio dropped &gt; 20%. Output is consumed by the cost-watch dashboard + alerts when overall ratio dips below 50%.

**Ефективно для:**

- Anthropic API users з prompt-cache enable — щоденний audit вирізняє poisoned prefixes.
- Cost regressions після оновлення system-prompt: report показує який саме prefix дав cache miss.
- RAG / agent loops, де cache_read ratio падає при додаванні per-user змінних.
- Тижневі cost reviews: один Markdown файл = вся cache-economy дашборд.

## Applies If (ALL must hold)

- Project uses Anthropic (or OpenAI) prompt-cache feature.
- Trace store captures `gen_ai.usage.cache_read_tokens` + `gen_ai.usage.input_tokens` per call.
- Monthly LLM bill is large enough that 20-30% cache regression is material.

## Skip If (ANY kills it)

- Project doesn't use prompt caching.
- Trace export doesn't capture cache token fields (instrument first via trajectory-eval-otel).
- Volume too low (&lt; 1000 cached calls / week) — audit overhead exceeds savings.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Trace export | JSONL with gen_ai.* attributes | OTLP backend (Langfuse / Phoenix / etc.) |
| Cron / scheduler | GitHub Actions / systemd timer / Airflow | infra |
| Alert backend | Slack / email / PagerDuty | ops |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[trajectory-eval-otel]] | upstream context required for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: audit-daily-cron, prefix-clustering-by-hash, report-flag-threshold, never-paste-secrets-in-system, alert-on-overall-dip | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for report + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `cluster-by-prefix` | haiku | Hash + group by; deterministic. |
| `compute-deltas` | haiku | Arithmetic over yesterday's table. |
| `scan-variables` | haiku | Regex scan over system prompts. |
| `publish-report` | haiku | Markdown template fill. |

## Templates

| File | Purpose |
|------|---------|
| `templates/daily-report.md.j2` | Markdown report template (overall + prefixes + alerts) |
| `templates/daily-report.md` | Markdown report template (overall + prefixes + alerts) Generated from `templates/daily-report.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cache-hit-audit-script.py` | Validate the report artefact against the schema | CI on each artefact change; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[trajectory-eval-otel]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, eval scores, stakes, noise ratio, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
