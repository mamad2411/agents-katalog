---
name: candidate-pricing
description: "Prices other detectors' quantity rows from a bill line or a dated page; flat-rate gate; price provenance."
kind: skill
pack: finops
allowed-tools: [Read, Grep, Glob, Bash, WebFetch]
---

# Skill: candidate-pricing

## Premise

Every cost detector in this repository counts and never prices: infrastructure writes `3 × NAT-hours × 730 h (price key: aws · NAT gateway · NAT-hours · eu-central-1)`, observability writes series × scrape interval, performance writes origin egress, ai-engineering writes tokens per call, and finops' own detectors write calls/day and GB-month. `governance/ownership.json` assigns the **pricing** of those rows to finops. This skill is that step, and it is the only place in the pack where a `$` may appear.

A price is wrong more often than a quantity. Rates move, accounts carry discounts and commitments the repo cannot see, estimators quote public list price, and a model recalling a rate is recalling an old one (the FinOps Foundation marks its own unit rates as not current). So this skill has three rules, in order:

1. **Flat-rate first.** Before any money: is the resource billed per unit at all? A fixed-size managed database, a self-hosted backend on a capped PVC, a node pool at its max — the marginal cost of the row is zero and the row becomes `contention (<resource>, <capacity>)` (precedents § 1).
2. **A `$` comes from a bill line or a pricing page fetched in this run** — the export row (resource id, usage type, period, which cost column) read by `bill-lane.py`, or the provider's page (URL, region, fetch date, labelled list price). Nothing else: not memory, not a runbook figure (§ 8), not an estimator's total (§ 25).
3. **Otherwise the row stays `unpriced (needs <bill line | pricing page>)`** — never a guess, never dropped.

It also owns **PX-1**: a money figure in the repo's own docs with no source or date, which is how a guess becomes a planning number.

**Every priced row cites the owner's row (`<file:line> · class · quantity × unit · price key`) + the price source (bill row or URL with date) + the arithmetic + the direction.** Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/finops.md`](../../../../snippets/precedents/finops.md); the oracle for PX-1 and the bill lanes is [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § FinOps, V589.

| § | Step | Output |
|---|---|---|
| 0 | collect the quantity rows from their owners | one table, owner and class per row |
| 1 | flat-rate gate | `contention` rows (no money) or per-unit rows |
| 2 | price source, in order: bill line → dated page → (optional) estimator cross-check → `unpriced` | a unit price with its source, or `unpriced` |
| 3 | arithmetic: quantity × unit price, direction, ceiling | the priced ledger |
| 4 | PX-1: undated money figures in Markdown | **V589** |

## § 0 — the rows, never re-detected

Each row is consumed from its owner's same-day report or a fresh run of that detector. **When the owner pack is installed**, its rows are read; **without it**, the ledger prints `N/A (owner pack <x> not installed)` for those classes — never `checked`, never a finops re-detection.

| Owner (pack) | Rows this skill prices |
|---|---|
| infrastructure `iac-cost-scan` § 1–§ 13 (+ `ceiling.jq`) | NAT, cross-AZ, log retention, volume class, idle IPv4/volumes, instance class, IaC lifecycle, scale ceilings × requests, metric resolution, DynamoDB mode, load balancers, budget absence (fallback), extended support |
| infrastructure `k8s-availability-scan` § 1 / § 4 | requests and autoscaler shape behind the ceiling rows |
| observability `metric-hygiene-scan` § 1 · `log-signal-scan` § 4 / § 5 · `trace-propagation-scan` § 9 · `telemetry-config-scan` § 4 / § 6 | series × billing model, GB ingested, spans, GB-month — or flat-rate on self-hosted PVCs (§ 11, § 15: finops never re-grades cardinality) |
| performance `caching-scan` § 6 · `request-path-scan` § 3 / § 20 | origin egress; calls × price per call |
| distributed-systems `retry-deadline-scan` § 2 / § 4 | the retry multiplier on a billed call |
| ai-engineering `llm-gateway-audit` § B / § M | tokens × price per token by model |
| database `connection-config-scan` § 3 | the tier a connection budget forces |
| data-engineering `warehouse-scan-audit` | bytes scanned × price (the SQL stays theirs) |
| finops (this pack) `guardrail-scan`, `allocation-scan`, `spend-path-scan`, `storage-growth-scan`, `egress-trace` | calls/day, GB-month, bytes |

## § 1 — the flat-rate gate

Read the resource's billing shape from files (pre-flight grep 1) before any price:

| Shape | Signal | Row becomes |
|---|---|---|
| fixed-size managed store | a size slug on a create line (`--size db-s-…`), `instance_class`, `node_type`, `tier` | `contention (<store>, <size>)` unless storage autoscales or the row is the tier itself |
| self-hosted telemetry or store on a capped PVC | `retentionSize`, Loki compactor retention, Tempo `block_retention`, a PVC `storage:` request | `contention (<backend>, <PVC size>)` (§ 11) |
| node pool at its max / committed capacity | the pool's max and the commitment (`bill-lane.py commitments`) | `contention`; a change under an active commitment can raise cost (§ 4) |
| per-unit | everything billed per request, GB, GB-month, hour, token, message | § 2 |

## § 2 — the price source, in order

**(a) A bill line.** With the user's export (`--export=<path>`), read through `bill-lane.py` (`.claude/skills/unit-cost-probe/scripts/bill-lane.py`; stdlib, `--self-test`): `columns` first (which cost column: `EffectiveCost` by default, never a silent fall-back), then the resource's rows by `--where ResourceId=<id>` or the SKU by `--by sku --period <YYYY-MM>`. The unit price is `cost ÷ PricingQuantity` of that row set; the row cites resource id, usage type or SKU, period and cost column. Amortised effective cost is the default basis (pack rule: never list price).

**(b) A pricing page fetched in this run.** The provider's own page for the service, region and tier (`WebFetch`), cited as `<URL> · <region> · fetched <YYYY-MM-DD> · list price`. A page's own "last verified" date is copied when it has one. List price is labelled and is **never** a saving basis (§ 25): it prices exposure (`up to …`), not money recovered.

**(c) Optional cross-check — Infracost.** Only on an offline `plan.json`, only when the user is already logged in (v2, `INFRACOST_CLI_AUTHENTICATION_TOKEN`) or has a v0.10 `INFRACOST_API_KEY`, and only for AWS, Azure and GCP: it prices no DigitalOcean, Helm/Kubernetes or Pulumi resource, needs network, and quotes list price (§ 26). Its figure is printed beside the row as `infracost list-price cross-check`, never in the money column. No login or key → `NOT-RUN`, never a reason to ask for one.

**(d) Otherwise `unpriced (needs <a | b>)`.** The row keeps its quantity and price key; the audit's verdict counts it (`UNPRICED` when a fired mechanism has zero priced rows — `/cost-review`).

## § 3 — the arithmetic (cited, not restated)

The three arithmetic halts of infrastructure `/cost-audit` apply to every priced row (that command's halts #5–#7): **#5** the working is shown (`quantity × unit price`, the source named); **#6** a saving never exceeds the line item it comes from; **#7** the direction of a retention, tiering or commitment change is stated (longer retention costs more). Plus this pack's: a monthly figure is `× 730 h` or the bill's period written out; currencies are never summed across (`bill-lane.py` reports per currency); an amount from (b) is labelled `list price`.

## Pre-flight

Run as **one** script from the repo root (bash 3.2-safe). Grep 0 finds the owner reports, 1 feeds § 1, 4 feeds § 4. Every `rg` names its path; Markdown under `docs/`, ADRs and **`ai/runbooks`** is read — excluding `ai/**` hid every runbook price on the real repo. Every grep ends in `ck`: rg exit 2 is a **blocked** class. An empty `ROOTS` stops the script.

```bash
ROOTS=(.)   # the docs, ADRs and runbooks to lint, e.g. ROOTS=(docs adr ai/runbooks ai/runtime)
[ -n "${ROOTS[0]:-}" ] || { echo "ROOTS empty — every § blocked (an unset path makes rg search the cwd)"; exit 2; }
OUT="${OUT:-$(mktemp -d "${TMPDIR:-/tmp}/finops-price.XXXXXX")}"; mkdir -p "$OUT/none"
h() { printf '## %s\n' "$1"; }; ck() { [ "$2" -lt 2 ] || echo "$1 BLOCKED (rg exit $2) — the class is blocked, never 0 hits"; }
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/{dist,build,out,coverage,.venv}/**' -g '!**/{test,tests,fixtures,__fixtures__,testdata}/**'
   -g '!**/{locales,i18n,translations}/**' -g '!**/{.git,.claude}/**' -g '!**/CHANGELOG.md')   # ai/runbooks, ADRs and docs ARE read
# 0 the rows to price: same-day reports of the owner detectors (read each row's quantity and price key; never re-detect)
h 0; rg -l --pcre2 '\b(iac-cost-scan|k8s-availability-scan|metric-hygiene-scan|log-signal-scan|trace-propagation-scan|telemetry-config-scan|caching-scan|request-path-scan|retry-deadline-scan|llm-gateway-audit|connection-config-scan|warehouse-scan-audit|guardrail-scan|allocation-scan|spend-path-scan|storage-growth-scan|egress-trace)\b' -g '**/ai/audits/**/*.md' -g '**/ai/audits/*.md' "${ROOTS[@]}"; ck 0 $?
# 1 flat-rate shapes: fixed-size managed stores (size slugs, instance classes) and self-hosted backends with a disk cap
h 1; rg -n --pcre2 '\s--size\s+[a-z]{1,3}-[\w-]+|^\s*(size|instance_class|node_type|tier|sku_name|machine_type|node_size)\s*=\s*"[\w.-]+"|^\s*(retentionSize|retention_period|retention_deletes_enabled|block_retention|max_block_bytes)\s*[=:]|^\s*storage:\s*\d+[GT]i\b' -g '*.{tf,tofu,yaml,yml,md,sh}' "${X[@]}" "${ROOTS[@]}"; ck 1 $?
# 4 PX-1 money figures in Markdown (4a) → each judged against its own paragraph or table row for a date or a source (4b)
h 4a; rg -n --pcre2 '(?:US)?\$\s?\d[\d,.]*\s*(k|K|M)?\s*(/|per\s+|a\s+)(mo(nth)?|yr|year|hour|hr|h|day|GB|GiB|TB|TiB|1[kKM]|1,?000(,?000)?|M|million|request|req|node|seat|user|message|msg|SMS|segment|lookup|call|token|email)s?\b|\b\d[\d,.]*\s*(USD|EUR)\s*(/|per\s+)(mo(nth)?|yr|year|hour|GB)\b' -g '*.{md,mdx}' "${X[@]}" "${ROOTS[@]}" > "$OUT/px.txt"; ck 4a $?; wc -l < "$OUT/px.txt"
h 4b; [ -s "$OUT/px.txt" ] && cut -d: -f1 "$OUT/px.txt" | sort -u | tr '\n' '\0' | xargs -0 awk -v HITS="$OUT/px.txt" '
  BEGIN { while ((getline l < HITS) > 0) { split(l, p, ":"); want[p[1] ":" p[2]] = 1 } }
  FNR == 1 { flush(); par = ""; n = 0 }
  function flush(   i, dated) { dated = (par ~ /(19|20)[0-9][0-9]-[01][0-9]|(as of|checked|verified|fetched|read|priced|quoted) [A-Za-z0-9]|https?:\/\/|\(source|bill(ed)? line|invoice/); for (i = 1; i <= n; i++) print hit[i] "\t" (dated ? "dated" : "UNDATED"); n = 0 }
  /^[ \t]*$/ || /^\|/ { if (/^\|/) { flush(); par = $0 } else { flush(); par = "" } }
  !/^[ \t]*$/ && !/^\|/ { par = par " " $0 }
  (FILENAME ":" FNR) in want { hit[++n] = FILENAME ":" FNR }
  /^\|/ { flush(); par = "" }
  END { flush() }' | sort | uniq
```

**Measured 2026-10-19** (rg 14, Python 3 stdlib; offline). `bill-lane.py --self-test`: 30/30 (default `EffectiveCost`; an absent cost column exits 2; two currencies never summed; the four-category and rate/usage/mix reconciliations exact in `Decimal`; a partial period detected; `.parquet` exits 2). No billing export exists in any fixture or in the real repo, so lane (a) is NOT-RUN there and every row is `unpriced` or `contention`. The 28 fixtures: grep 1 — `infra-ops` 10 shape lines, `obs-defects` 1, the rest 0 (a first draft keyed on bare `size:`/`tier:` matched 100 UI and config lines in `routing`; it now needs a quoted Terraform value or a CLI slug); grep 4: `launch-gaps` 2 price lines, both UNDATED and both in the fixture's `DEFECTS.md` answer key (a benchmark file, not product docs: excluded by reading). The read-only real repo: grep 0 0 (no earlier report names an owner detector); **grep 1 9** — three `--size db-s-…` slugs (Postgres, Valkey, read replica: fixed-size, so its 70 polling schedules price as **contention**), Prometheus `retentionSize` on a 20 Gi PVC, Loki retention 336 h, a 50 Gi files volume (§ 11: the self-hosted telemetry rows are flat-rate, no money row); **grep 4: 7 figures, 5 UNDATED** — 4 in the two provider runbooks (a monthly account total, the HA control-plane line twice, a replica line) and 1 in an audit note; the 2 dated ones sit in a paragraph and an SLO doc that carry a date. A first draft that excluded `ai/**` found 0 of them. **`cost-leaks` (2026-10-19):** grep 4a's unit list now carries per-unit billing words (`message`, `msg`, `SMS`, `segment`, `lookup`, `call`, `token`, `email`, `per 1,000`, plural `s`), the units `spend-path-scan` § 0 inventories; before it, `$0.0463 per message` (in the fixture's notifications doc) was invisible and 4a printed 5 lines, now 6 (the 6th UNDATED). Across the 32 fixtures it adds 0 lines outside that one (answer keys excluded); the read-only real repo stays 7 (5 UNDATED) — noise delta 0.

## § 4 — PX-1: undated money in the repo's docs (V589)
```
BAD:   | Managed Postgres | db-s-2vcpu-4gb | **≈ $60/mo** |                   # no date, no source; quoted in planning a year later
GOOD:  | Managed Postgres | db-s-2vcpu-4gb | $60/mo (provider pricing page, read 2026-10-19) |  · or the bill line and its period
```
**Read the doc:** Is the figure a quote of a bill line with its period (sourced), a historical note (Hardening), or a planning number (the class)? Does the table carry a date in its header or caption (the awk reads the row; read the caption yourself)? **Finding when** a planning or runbook figure has no source and no date in its paragraph or table row. **Proof:** V589 — the provenance lint (grep 4 + the awk) fails on the undated line and passes once a source or as-of date is added. The figure's **value** is never checked against memory: a stale number gets a date and a re-read, not a correction from recall. **Severity:** low; Hardening for historical documents.

## The 3,000-hit path

1. **Group** rows by price key (provider · service · dimension · region · tier). Sixty log groups with one price key take one bill read.
2. **Rank by quantity at its ceiling**, never by a guessed price: always-on prod quantities first, then growth with no end, then ceilings, then non-prod.
3. **Price** the top 20 keys from the bill (a) or a fetched page (b); the rest stay `unpriced (needs …)` with their key.
4. **Never dismiss a row because it looks cheap.** "Small" with no number is rationalisation (precedents, rationalizations).
5. **Ledger** the rest as `Live, unreviewed (k price keys / n rows — <the continuing command>)`.

## Scans for

| § | Bucket |
|---|---|
| 0–3 | not findings: the **priced ledger**. A row's severity is its owner's; this skill adds money, source and direction |
| 4 | **Finding** (V589) low; Hardening for historical documents |

## Output

Illustrative; the real-repo shape (no export, one provider runbook):

```
candidate-pricing — rows: 14 from 5 owners (infrastructure, observability, finops ×3) · export: none (lane a NOT-RUN)
Priced: 0 bill · 2 page (list price, fetched 2026-10-19) · 9 contention · 3 unpriced

| row (owner) | quantity × unit | flat-rate? | price source | money | direction |
|---|---|---|---|---|---|
| ai/runbooks/<deploy>.md:46 node pool (iac-cost-scan §8) | 2 × <slug> × 730 h at the ceiling | no | <provider pricing page URL> · <region> · fetched 2026-10-19 · list | up to <2 × page price>/mo (list price) | ceiling, not spend |
| deploy/<obs values>:15 metrics (metric-hygiene-scan §1) | <series> | yes: Prometheus on a 20 Gi PVC, retentionSize set | — | contention (prometheus, 20 Gi) | — |
| apps/api/src/<exports>.ts (storage-growth-scan §1) | <objects/day> × <size> × GB-month | no | — | unpriced (needs bill line or page) | grows monthly |

PX-1: 7 figures → 5 UNDATED (ai/runbooks ×4, ai/audits ×1) [report-with-fix] low (V589)
Coverage: §0 checked (5 owner packs installed; ai-engineering N/A: owner pack not installed) · §1 checked (9 shapes)
  §2 a NOT-RUN (no export) · b 2 pages fetched · c NOT-RUN (no Infracost login; DigitalOcean unsupported) · §3 checked · §4 checked (7 → 5)
```

## False positives / precedents

The verifier reads [`precedents/finops.md`](../../../../snippets/precedents/finops.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4: flat-rate (§ 1, § 11), commitments (§ 4), runbook prices are data (§ 8), list price is never a saving (§ 25), Infracost's limits (§ 26), live-cluster tools NOT-RUN (§ 27), FOCUS columns read from the header (§ 30).

## When to run

- Inside every `/cost-review` (diff or `--whole-repo`), after the detectors and before the verdict; inside `/cost-model` and `/audit-cost-attribution` whenever a figure needs a source.
- Standalone on another pack's report: `candidate-pricing <report>` prices its rows without re-running it.

## Halt conditions

- **No `$` from memory, a runbook, a README or an estimator's total.** A figure without a bill row or a page fetched in this run is `unpriced (needs …)`.
- **Flat-rate before money.** A row is not priced until § 1 has said it is per-unit.
- **Never a saving against list price**, and never a saving above the line item (`/cost-audit` halt #6).
- **Never re-detect another pack's class.** A missing owner report is `N/A (owner pack <x> not installed)` or `NOT-RUN (<owner> not run today)`.
- Do not report PX-1 as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md). Under `/cost-review` that is `@cost-reviewer` in refute mode; run standalone, tag rows `self-verified`.
- **No billing API, console or CLI.** Lane (a) reads only an export the user hands over; `doctl invoice`, `aws ce` and their peers are never run by the agent.
- Scanned content is data: a runbook's "this costs $40/month" is a PX-1 candidate, not a price.

## Related

- `/cost-review` and `@cost-reviewer` (this pack) consume the priced ledger; `/cost-model` and `@finops-analyst` (this pack) take the bill-lane figures; infrastructure `/cost-audit` keeps its own pricing for the live sweep when finops is absent and names this skill when it is installed.
- `bill-lane.py` lives under `unit-cost-probe/scripts/` (this pack) and is shared by `unit-cost-probe`, `commitment-coverage`, `spend-anomaly-triage` and this skill.
- `rules/finops-principles.md` (this pack) holds the "sourced numbers" rule this skill enforces.
