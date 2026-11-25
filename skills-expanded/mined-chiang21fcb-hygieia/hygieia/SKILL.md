---
name: hygieia
description: >
  语义层/本体体检与养护（audit / eval / rot / report）。当用户用中文要求「审计我们的语义层」
  「检查我们的本体质量」「为什么我们的数据 agent 给错数字」「评估我们的 text-to-SQL 准确率」
  「压力测试我们的数据模型」「找出项目和本体之间的漂移」时使用；也响应英文提问 "audit our
  semantic layer"、"ontology health check"、"why did the data agent return a wrong number"、
  "evaluate our text-to-SQL accuracy"、"stress-test our data model"、"drift between the
  project and the ontology"。纯本地离线运行，Python 3.10+，运行时依赖 pyyaml + sqlglot（AST 引用抽取）。
---

# Hygieia

> Keep an existing semantic layer healthy: check it, evaluate it, stress-test it.

A fully offline semantic-layer health-check skill. Given a fixture directory (`semantic/metrics.yml` required; `schema.sql` required only for `eval`/`rot`; `questions.yaml` + `seed.sql` for `eval`), run the four main commands (`audit`/`eval`/`rot`/`report`) plus the read-only adapters (`adapt dbt`, `adapt ossie`) and `impact` per the operating contract below. Hygieia does not bootstrap ontologies: the "first build" half can be served by third-party bootstrap flows (e.g., the ontology-skills bootstrap), and their output can be handed to Hygieia as a downstream quality gate. Binding details (metrics.yml schema, severity, scoring protocol, rot threat model) live in `docs/contract.zh.md` (Chinese, authoritative) and `docs/contract.en.md` (English mirror); the essentials are inlined below so this skill stays self-contained.

## Triggers

> Chinese: 「审计我们的语义层」「检查我们的本体质量」「为什么我们的数据 agent 给错数字」「评估我们的 text-to-SQL 准确率」「压力测试我们的数据模型」「找出项目和本体之间的漂移」。
> English: "audit our semantic layer", "ontology health check", "why did the data agent return a wrong number", "evaluate our text-to-SQL accuracy", "stress-test our data model", "drift between the project and the ontology".

## Operating contract

1. First confirm the fixture directory exists and contains `semantic/metrics.yml`; `schema.sql` is optional for `audit` (without it, R4 and the table/column checks of R3 are skipped and listed in `skipped_rules`), while `eval`/`rot` need `schema.sql` + `seed.sql` and `eval` needs `questions.yaml`. If a required file is missing, say so explicitly. Do not guess.
2. Suggested order: `audit` → `rot` → `eval` → `report` (`report` calls audit/rot/eval in sequence).
3. `audit`: static diagnosis of 9 rule classes (R1 synonym conflict / R2 orphan metric / R3 join ambiguity / R4 dangling reference / R5 missing evidence / R6 missing description / R7 redundant description / R8 stale alias pointing at a deprecated metric / R9 one metric merging sources with conflicting freshness). Every finding carries three elements: rule, danger, fix. Severity mapping: **high** = R1, R3, R4, R8, R9 (and R2 when the domain does not exist): these can directly cause wrong numbers; **medium** = R5, and R2 with an existing domain but no table binding; **low** = R6, R7. In `metrics.yml`, the join-condition field is `on_expr`. YAML 1.1 parses a bare `on` as the boolean key `True`, silently dropping the field; R3/R4 read `on_expr` exclusively.
4. `eval`: two-arm controlled evaluation. By default it reads `fixtures/<dir>/demo_results.json`. When the top is marked `simulated: true`, the answers are hand-authored, but the scoring logic still runs for real per the protocol below. For a live evaluation, store artifacts under `fixtures/<dir>/runs/<timestamp>/` (meta.json + control.json + treatment.json) and point `--results` at them (see `docs/eval-live.md`). Every eval writes `reports/manifest.json` (model, prompt/questions/corpus/semantic-layer hashes, version); `report` marks runs not directly comparable when those differ, and scores entity (tables/joins) and relation (caliber) separately. The core metric is the **silent-error rate** (a number returned with no error and no clarification, so the user cannot tell). Scoring labels are mutually exclusive, judged top-down: `clarify` (explicit refusal to fabricate, or `expected_behavior: clarify`) → `abstain` (explicit "don't know", no business number) → `honest_error` (SQL/number given but execution failed) → `silent_error` (plausible number/yes-no, mismatches gold, no clarification) → `correct` (matches gold). For `expected_behavior: clarify`, only an explicit keyword hit counts as `clarify`/`abstain` and may count correct. The scorer matches these strings verbatim: Chinese markers (数据不足 / 无法计算 / 需澄清 / 无法回答 …) or the English ones (`unknown` / `cannot compute` / `insufficient data` …) selected by answer-language detection; empty or filler replies (「嗯」「好的」「ok」) are non-compliant `abstain`; a concrete number or a digit in `raw` is `silent_error`. Accuracy = correct/total; silent-error rate = silent_error/total; `honest_error`/`abstain` count in neither. Scoring keywords are coupled to the answer language: v0 ships a Chinese marker table and an English one, selected automatically by answer-language detection (any CJK in the answers → Chinese table); the demo fixture stays Chinese.
5. `rot`: injects five kinds of drift into an in-memory copy — structural: column rename `orders.total_amount` → `order_amount`, definition tampering `refund_total.expr` gains `refunds.tax`, a new orphan metric `gross_margin` (missing domain, no evidence); semantic: a stale alias pointing at a deprecated metric, and one metric merging two sources with conflicting freshness — re-runs audit, and reports **new captures** = `|findings_after − findings_before|` (set difference keyed by `rule+subject+detail`). Never writes to disk unless `--write` (then `metrics.rot.yml`).
6. `report`: writes `reports/health-report.md` with three blocks: high/medium findings, rot simulation, controlled evaluation.
7. CI usage: `--fail-on high` exits 1 when high-severity findings exist.
8. Output language: `--lang zh|en` (default `en`). The two variants are written independently for their own context. Use `--lang zh` when the conversation is in Chinese so the whole output (headers, severity labels, finding texts, report) is Chinese, not a translation of the English one. This only affects display: the scoring protocol and the fixture content are unchanged.
9. Beyond the four main commands: `adapt dbt` and `adapt ossie` (read-only adapters mapping dbt/MetricFlow or Apache Ossie/OSI YAML onto `metrics.yml`; Ossie is the neutral first-class input — see `docs/adapters.md`), and `impact <fixture_dir> --diff <file|->` (git diff → affected metrics, see `docs/impact.md`). Reference extraction is AST-based (sqlglot, sqlite dialect); an unparseable expression is surfaced as a high R4 finding, never silently ignored.
10. When reporting numbers, distinguish "real execution" (gold/candidate SQL run against the seed) from "simulated answers"; never present simulated data as a live evaluation.

## Usage

```bash
hygieia audit  fixtures/ecom
hygieia eval   fixtures/ecom
hygieia rot    fixtures/ecom
hygieia report fixtures/ecom

# python scripts/hygieia.py ... still works as a thin compatibility shim.
```

Self-test: `python -m unittest discover -s tests -v` (asserts the contract numbers: 65%/100%, silent rates 35%/0%, audit 7 findings, rot 6 new captures = structural 4 + semantic 2). CI/agent wiring: `docs/integrate-ci.md`, `docs/integrate-agent.md`; SARIF via `audit --sarif`.
