# Champion Challenger Pattern for RAG

## Summary

**One-sentence:** Spec for keeping last week's winner running as champion while next week's challenger benches in shadow traffic — without leaking user traffic across arms.

**One-paragraph:** RAG benches happen weekly: chunking, embeddings, reranker, prompt — every component has variants. Without a champion-challenger pattern, teams either deploy untested winners (regression risk) or run parallel UI experiments (slow + user-confusion). This methodology codifies a 7-day cycle: current champion serves 100% of user traffic; challenger reads the same queries in shadow mode (no user-visible answer) and produces parallel responses; an LLM-as-judge or eval rubric compares them; the winner becomes next week's champion. Config artefact specifies arms + traffic allocation + judge + promotion criteria + cleanup cadence; validator enforces no traffic leakage.

**Ефективно для:**

- RAG команди, які weekly bench chunking / embeddings / reranker і хочуть data-driven rollout.
- Системи з high cost-of-error (legal/medical RAG) — shadow eval перед user-facing deploy.
- Multi-component pipelines (retrieval → rerank → generate) — кожен компонент має champion-challenger арм.
- Compliance/audit: tracked promotion history = full decision trail.

## Applies If (ALL must hold)

- RAG system in production with ≥ 1000 queries/day (statistical power).
- Traffic mirror / shadow-mode capability (challenger can read traffic without writing to user).
- Eval rubric or LLM-as-judge exists to score the comparison.

## Skip If (ANY kills it)

- Single-component pipeline (one prompt only) — A/B is cheaper than champion-challenger.
- Volume &lt; 1K queries/day — sample size too small for weekly promotion.
- Greenfield RAG with no champion yet — bootstrap with a static baseline first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Production query log | JSONL of (query, retrieval, response) | trace store |
| Eval rubric or LLM-as-judge | rubric or judge prompt | from ai-feature-eval-set-design |
| Shadow-mode infra | ability to mirror traffic to challenger without user output | infra |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[ai-feature-eval-set-design]] | upstream context required for this methodology |
| [[trajectory-eval-otel]] | upstream context required for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: shadow-no-user-leak, weekly-promotion-cycle, promotion-criteria-explicit, rollback-on-promotion-regression, audit-trail-required | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for config + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `design-challenger` | sonnet | Picks the variable to change with light judgment. |
| `wire-shadow-traffic` | haiku | Infra wiring + leak verification. |
| `run-cycle-and-judge` | haiku | Mechanical scoring loop. |
| `promote-or-bench-again` | sonnet | Decision evaluation against criteria. |

## Templates

| File | Purpose |
|------|---------|
| `templates/cycle-report.md.j2` | Cycle report Markdown template |
| `templates/cycle-report.md` | Cycle report Markdown template Generated from `templates/cycle-report.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-champion-challenger-pattern-rag.py` | Validate the config artefact against the schema | CI on each artefact change; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[ai-feature-eval-set-design]]
- [[auto-rollback-policy-design]]
- [[trajectory-eval-otel]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, eval scores, stakes, noise ratio, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
