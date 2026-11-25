---
name: slo-rule-scan
description: "SLO definitions: no burn alert, factor vs objective/period, impossible targets, wrong SLI, bucket edge, retention — arithmetic proved."
kind: skill
pack: observability
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: slo-rule-scan

## Premise

An SLO is a promise that something will page before the error budget is gone. The definition can break that promise before any traffic arrives, in six ways:
- **No burn alert.** The objective is declared, and sloth's `page_alert` and `ticket_alert` are both disabled.
- **A burn rule copied from another SLO.** `14.4 * 0.01` on a 99.9 % objective fires at ten times the intended burn, which in practice means never.
- **One window and no short window.** The page keeps firing for an hour after the incident ends.
- **An impossible objective.** 100 % leaves no budget at all. At 99.999 % over 30 days an outage spends the whole budget in 26 seconds. At 90 % the fast page needs an error ratio above 1, so it can never fire.
- **The wrong SLI.** It counts 404s as failures, or it reads only `code="500"` and misses 502, 503 and 504.
- **A threshold or window with nothing behind it.** A latency threshold of `le="0.25"` names a bucket the code never registered, so the numerator is empty. A 30-day budget sits on 15 days of TSDB retention.

The YAML reads fine in every one of these cases.

**The arithmetic is the rule, not a literal.** The factor must satisfy `factor = budget_fraction × period / long_window`, and the short window must be the long window ÷ 12, or the accepted set's own short window (`THR-OBS-BURN`). That one formula accepts every legitimate set:
- the Workbook 14.4 / 6 / 1;
- sloth `google-30d`'s fourth tier, 3× over 24h/2h;
- Pyrra 14 / 7 / 2 / 1 on windows scaled to the period;
- a 28-day 13.44.

The same formula rejects a factor that was tuned for another objective or another period. A reviewer who checks "must be 14.4" fails every Pyrra rule (precedents § 12).

This skill reads SLO specs (sloth, Pyrra, OpenSLO, Datadog / Honeycomb / New Relic SLO resources), the burn rules generated from them or written by hand, the SLI bucket edges, and TSDB retention. It proves each defect with **regenerate-and-diff and the burn arithmetic**. It owns `/obs-audit`'s SLO definitions row (§1–§6, `ownership.json` row `obs-slo`). `slo-audit` (this pack) keeps attainment, STALE / NO-DATA and the registry write. `@observability-reviewer` judges these rows.

**Every finding cites:**
- the spec or rule `<file:line>` (alert name + tier for burn rules);
- the objective and period it was judged against, and where they were read;
- the arithmetic or diff that shows the defect;
- what on-call loses (no page, a late page, a page on noise, a budget computed on missing data);
- the fix in the spec. Generated rules are regenerated, never hand-edited (precedents § 42).

A grep hit or a `burn-check.py` row is a candidate. "SLOs look fine" is never printed; the output is the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/observability.md`](../../../../snippets/precedents/observability.md). The oracle is [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Observability, *Regenerate, validate and diff*, variants V207 (definition and burn) and V199 (bucket edges).

## The rule

A candidate is a finding when all four hold. These are the protocol's gates as `precedents/observability.md` § Reading the seven gates applies them to SLOs.

1. **The SLO is live.** Its spec is generated into rules that Prometheus loads; the `rule_files` glob or `ruleSelector` match is `alert-rule-lint` §4's. Otherwise the vendor resource is applied, or the registry (`ai/runtime/slos.md`) names it as in force. A spec marked report-only is not SLO-01.
2. **The objective and period are read, never assumed:** from the spec, sloth's metadata recording rules (`slo:objective:ratio`, `slo:time_period:days`), Pyrra's `exhaustion` label, or the registry row passed as `--slo`. A row whose period is unread is a note, never a finding.
3. **Nothing already covers it:**
   - a generator that emits the burn alerts for this spec;
   - a sibling short window;
   - a documented 4xx class counted as bad (precedents § 13);
   - a long-term store behind the TSDB;
   - an ADR that tunes the factor on purpose.
4. **The oracle fired.** Any one of these:
   - `burn-check.py` printed the row and the arithmetic holds when re-done by hand;
   - `sloth generate` / `pyrra generate` from the committed spec diffs non-empty against the committed rules;
   - a two-ended static trace for a static-fact class (an `le` with no matching bucket in the registration, a period over the retention the server runs).

## Boundaries

- **Attainment, budget remaining, too lax / too tight against data, STALE vs NO-DATA, and the registry write** belong to `slo-audit` (this pack, L-tier). This skill never estimates attainment and never writes `ai/runtime/slos.md`.
- **Burn-rule hygiene that is not burn arithmetic** belongs to `alert-rule-lint` (this pack): `for`, runbook and severity (no `for` on a multiwindow burn rule is correct, precedents § 2), selector grounding (AL-10), routing of the burn alert's labels (§8), and integer `le="1"` on Prometheus 3 (AL-21). Burn rules use its `rule-inventory.py` reader too (§ Tool lane), so both skills see the same rows.
- **The histogram registration itself** (units, default buckets, `observe(Date.now()-t)`) belongs to `metric-hygiene-scan` §3 (this pack). §5 here owns only the SLI side, the threshold `T`, and joins on the bucket list. A site both see is reported once, by `<file:line>`.
- **Ingress, load-balancer or mesh request metrics and access-log fields** (whether the edge emits them at all, with a request id and upstream timing) belong to infrastructure `edge-reliability-scan` §15 when that pack is installed; without it the question is listed as `edge telemetry (owner pack infrastructure not installed)`. §4 asks only whether the SLI should read them.
- **The budget-policy text** belongs to `@sre-engineer` (this pack); §6 reports only its absence. **The dollar cost of longer retention** is priced by `@cost-reviewer` (finops pack, when installed; unpriced without it).
- **A page budget** (`THR-OBS-PAGE-BUDGET`, pages per shift) is judged by `alert-audit` against fire history. It is never estimated here.

## Adapt to the codebase — the SLO lanes

Read each generator version from the generated file's header (`# Code generated by Sloth (v0.16.0)`), the CI step or `Makefile` that runs it, or the operator image tag. Read the generate flags too (`--default-slo-period`, `--extra-labels`, Pyrra `--generic-rules` / `--operator-rule`): a diff caused by a flag the repo passes is not drift.

| Lane | Spec | Generated rules | Objective / period read from |
|---|---|---|---|
| **sloth** 0.16.0 | `version: prometheus/v1` + `slos:`, or the `PrometheusServiceLevel` CRD | `slo:sli_error:ratio_rate<w>` records; one page and one ticket alert, each an `or` of two tiers; `sloth_*` labels | `objective` (percent); period 30d unless `--default-slo-period`; metadata records `slo:objective:ratio`, `slo:time_period:days` |
| **Pyrra** 0.10.2 | `kind: ServiceLevelObjective` (`spec.target` percent, `spec.window`) | `<metric>:burnrate<w>` records; four `ErrorBudgetBurn` alerts with labels `long`, `short`, `severity`, `exhaustion`, `slo` | the spec; else `exhaustion` × factor |
| **OpenSLO** | `apiVersion: openslo/v1`, `kind: SLO` (`objectives[].target` fraction, `timeWindow[].duration`) | none of its own (sloth 0.16.0 rejected an `openslo/v1` file, measured) | the spec; `alertPolicies` absent means SLO-01 unless a hand-written burn rule exists |
| **Hand-written** | the registry (`ai/runtime/slos.md`) or a doc | rules with `> factor * (1 - objective)` | the registry row, read by `--registry` (step 2 passes it); `--slo='<alert regex>=<objective>/<period>'` overrides |
| **Vendor** | `datadog_service_level_objective`, `honeycombio_slo`, `newrelic_service_level` | `datadog_monitor` `type = "slo alert"`, `honeycombio_burn_alert`, NR alert conditions | the resource's `target` / `timeframe` |

**Measured generator shapes** (2026-10-10, darwin-arm64 binaries checked against each release's `checksums.txt`, run on the seeded sample):
- **sloth 0.16.0 `generate`:**
  - writes 14.4 × 5m/1h `or` 6 × 30m/6h as the page alert, and 3 × 2h/1d `or` 1 × 6h/3d as the ticket alert. That is the four-tier Workbook set, with the budget written `0.0009999999999999432`.
  - generates **0 alerts** for an SLO whose `page_alert` and `ticket_alert` are both `disable: true`.
  - is deterministic: two runs diff empty.
- **pyrra 0.10.2 `generate`:**
  - on 28d writes 14 × 1h/5m (`for: 2m0s`), 7 × 6h/30m, 2 × 1d/2h and 1 × 4d/6h;
  - on 30d scales the windows and rounds them to the minute: 1h4m/5m, 6h26m/32m, 1d1h43m/2h9m, 4d6h51m/6h26m;
  - sets `exhaustion` (2d on 28d, `2d3h25m42s` on 30d) and wraps long expressions across lines;
  - regenerating the committed sample diffed empty.

## Tool lane

Run in `${TMPDIR:-/tmp}` on **copies**, pinned to the versions above: sloth 0.16.0 and pyrra 0.10.2, downloaded from the `slok/sloth` and `pyrra-dev/pyrra` GitHub releases into the scratch dir and checked against `checksums.txt`. OpenSLO's `oslo` 0.13.0 comes from the research catalog and was not run in this measurement. A generator that cannot install prints `blocked (lane not installed: <tool>@<ver>)` in §2's drift cell; `burn-check.py` still runs.

```bash
"$B/sloth" validate -i <spec dir>; echo "sloth validate exit $?"
"$B/sloth" generate -i <spec> -o "$T/sloth-<name>.yml" <the flags the repo's own generate step passes>; diff -u <committed rules> "$T/sloth-<name>.yml"
"$B/pyrra" generate --config-files='<spec glob>' --prometheus-folder="$T/pyrra/" <the repo's flags>; diff -u <committed rules> "$T/pyrra/<name>.yaml"
"$B/oslo" validate -f <openslo file>
```

`scripts/burn-check.py` (beside this file, installed as `.claude/skills/slo-rule-scan/scripts/burn-check.py`) is the arithmetic. It is Python 3 standard library, read-only, and imports `alert-rule-lint`'s `rule-inventory.py` (`../../alert-rule-lint/scripts/`, or `--rule-inventory=`). So plain rule files, PrometheusRule CRDs and Helm-embedded groups are parsed once, the same way, by both skills, and SLO specs use the same YAML reader. Without `rule-inventory.py` it prints `blocked (rule-inventory.py not found …)` and exits 2. **Co-install:** no pack manifest has a dependency key, so the pairing rests on how the pack installs — standard mode copies every observability skill, and minimal mode's `_essentials.md` lists both. On a project where `alert-rule-lint` was removed, restore it from the observability pack or pass `--rule-inventory=<path>`; never report the burn rows `checked` while burn-check is blocked.

What it does:
- Splits each burn alert into tiers: `or` branches, then `and` conjuncts.
- Reads each comparison's factor and budget: `f * (1 - o)`, `f * b`, or a plain threshold for an alert tied to an SLO.
- Reads each window from a range literal, from the recording rule it names, or from a name suffix (`ratio_rate1h`, `burnrate1h4m`, `avg5m`).
- Checks:
  - a long and a short window are both present (SLO-02);
  - the short window matches the set's own or long ÷ 12, within one minute or 10 % (SLO-02);
  - the budget equals 1 − the read objective (SLO-03, **H**);
  - `factor × budget < 1`, since otherwise an error ratio can never exceed it (SLO-04);
  - the factor equals `budget_fraction × period / long_window` for the accepted tier whose long window matches. Within 1 % is ok; within 10 % is a note (precedents § 12); within 2× is M; beyond 2× is H.
- At the spec level it flags:
  - an objective of 100 %;
  - a budget that a full outage spends before a 5m short window can page;
  - an objective whose generator fast page cannot fire;
  - alerting disabled (SLO-01);
  - a period over `--retention` (SLO-10).

`--self-test` runs these cases:
- Workbook 3-tier;
- Workbook 4-tier, as sloth emits it;
- Pyrra 14/7/2/1, on 28d and on 30d-rounded windows;
- ten negatives.

The self-test fails if any accepted set needs a literal match to pass. Exit codes: 0 none, 1 an H/M/L row, 2 usage, parse or import.

## Pre-flight

Run as **one** bash script from the repo root (bash 3.2-safe). Grep **N** feeds detector **§N**; 0 is context. Every `rg` names its path; any exit 2 is a failed grep, never zero hits. Files-without-match is `--files-without-match`, never `rg -L` (that is `--follow`).

```bash
T="$(mktemp -d "${TMPDIR:-/tmp}/slo.XXXXXX")"; BC=.claude/skills/slo-rule-scan/scripts/burn-check.py
# Rule and spec surfaces keep generated/ (sloth and pyrra output is what Prometheus loads, precedents § 42).
RX=(-g '*.{yml,yaml,jsonnet,libsonnet}' -g '!**/node_modules/**' -g '!**/{vendor,.git,charts/*/charts}/**' -g '!**/{test,tests,__tests__,fixtures,__fixtures__,testdata,e2e}/**' -g '!**/{docs,ai,.claude}/**')
TF=(-g '*.tf' -g '!**/.terraform/**' -g '!**/node_modules/**')
CODE=(-g '*.{ts,tsx,js,mjs,cjs,py,go,java,kt,kts,cs,rb,php}' -g '!**/node_modules/**' -g '!**/{dist,build,vendor,.venv,venv,target,bin,obj,generated,__generated__}/**' -g '!**/{test,tests,__tests__,spec,specs,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata}/**' -g '!**/*.{spec,test,e2e,e2e-spec}.*' -g '!**/*_test.go' -g '!**/test_*.py')
# 0a SLO specs (sloth plain + CRD, Pyrra, OpenSLO) and generator markers; 0b vendor SLOs and their alerts; 0c the registry and a budget policy (SLO-08).
SPECS=(); while IFS= read -r f; do SPECS+=("$f"); done < <(rg -l --pcre2 '^version:\s*["\x27]?prometheus/v1\b|^kind:\s*(?:PrometheusServiceLevel|ServiceLevelObjective)\s*$|^apiVersion:\s*["\x27]?openslo/' "${RX[@]}" .)
echo "specs: ${#SPECS[@]}"; [ ${#SPECS[@]} -gt 0 ] && printf '  %s\n' "${SPECS[@]}"
rg -l --pcre2 'Code generated by Sloth|\bsloth_id\b|\bpyrra\.dev/|:burnrate\d' "${RX[@]}" .
rg -n --pcre2 'resource\s+"(?:datadog_service_level_objective|datadog_monitor|honeycombio_slo|honeycombio_burn_alert|newrelic_service_level|newrelic_nrql_alert_condition|grafana_slo)"|\btype\s*=\s*"slo alert"|\bslo_id\b' "${TF[@]}" .
rg -l --pcre2 -i '^#+\s*(?:error[- ]budget\s+policy|slo\s+policy)\b|\berror[- ]budget\s+policy\b' -g '*.md' -g '!**/node_modules/**' .
ls ai/runtime/slos.md 2>/dev/null
# 1 burn rules: a comparison against factor × budget, in any rule surface (plain, CRD, Helm-embedded, generated).
BURN=(); while IFS= read -r f; do BURN+=("$f"); done < <(rg -l -U --pcre2 '>=?\s*\(?\s*\d+(?:\.\d+)?\s*\*\s*\(?\s*(?:1(?:\.0+)?\s*-\s*0?\.\d+|0?\.0\d+)' "${RX[@]}" .)
echo "burn-rule files: ${#BURN[@]}"; [ ${#BURN[@]} -gt 0 ] && printf '  %s\n' "${BURN[@]}"
# 2 the arithmetic: objective and period from the spec, sloth metadata, or the registry row (--registry ties a hand-written rule to its row).
SP=(); for s in "${SPECS[@]}"; do SP+=("--spec=$s"); done; [ -f ai/runtime/slos.md ] && SP+=("--registry=ai/runtime/slos.md")
if [ $((${#BURN[@]} + ${#SPECS[@]})) -gt 0 ]; then python3 "$BC" "${BURN[@]}" "${SP[@]}" --format=text; echo "burn-check exit $?"; else echo "burn-check: N/A (no burn rule, no spec)"; fi
# 3 objectives on the edge (100, five nines, ≤ 90) and SLOs on admin / cron / batch paths (SLO-09).
rg -n --pcre2 '^\s*-?\s*(?:objective|targetPercent|target_percentage|target)\s*[:=]\s*["\x27]?(?:100(?:\.0+)?|99\.99\d*|[1-8]\d(?:\.\d+)?|90(?:\.0+)?|1(?:\.0+)?|0\.9999\d*|0\.[1-8]\d*|0\.90*)["\x27]?\s*$' -g '*.tf' "${RX[@]}" -g '!**/.terraform/**' .
[ ${#SPECS[@]} -gt 0 ] && rg -n -H --pcre2 -i '^\s*-?\s*name:\s*["\x27]?[\w-]*(?:admin|cron|batch|nightly|backfill|export|report)[\w-]*' "${SPECS[@]}"
# 4 SLI error definitions: 4xx counted as bad, a 200 allow-list, only 500 (precedents § 13); 4b an edge that sees requests the app never does.
rg -n --pcre2 '\b(?:code|status|status_code|http_status|response_code)\s*(?:=~\s*"[^"]*4(?:\.\.|xx|\d\d|\[)|!=\s*"200"|!~\s*"2\.\."|=\s*"500")' "${RX[@]}" -g '!**/{dashboards,grafana}/**' .
rg -l --pcre2 '^kind:\s*(?:Ingress|HTTPRoute|Gateway|VirtualService|IngressRoute)\s*$|ingress-nginx|\bistio\b|\blinkerd\b|traefik|envoyproxy|aws-load-balancer-controller' "${RX[@]}" .
# 5 latency SLI thresholds (le literals in specs and burn/recording rules) vs the bucket lists registered in code (SLO-07).
rg -o -N --no-filename --pcre2 '\ble\s*=~?\s*"\K[^"]+' "${RX[@]}" . | sort -u > "$T/le.txt"; echo "SLI le values: $(paste -sd' ' "$T/le.txt")"
rg -n --pcre2 '\bbuckets\s*(?:[:=]\s*[\[(]\s*\.?\d|:\s*[A-Z][A-Z0-9_]*\b|=\s*[A-Z][A-Z0-9_]*BUCKETS?\b)[^\n]*|\b[A-Z][A-Z0-9_]*BUCKETS?\s*(?::[^=\n]*)?=\s*[\[(]\s*\.?\d[^\n]*|\bBuckets:\s*(?:\[\]float64\{[^}\n]*\}|prometheus\.\w+Buckets\([^)\n]*\)|prometheus\.DefBuckets\b)|\.buckets\([^)\n]*\)|\bserviceLevelObjectives\([^)\n]*\)|ExplicitBucketBoundaries\s*=\s*new\b[^;\n]*' "${CODE[@]}" .
rg -q --pcre2 '\bprometheus\.DefBuckets\b' "${CODE[@]}" . && echo "prometheus.DefBuckets = [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10] (client_golang default)"
# 6 TSDB retention vs the SLO period, and any long-term store (SLO-10).
rg -n --pcre2 'storage\.tsdb\.retention\.(?:time|size)|^\s*retention(?:Size)?:\s*\S+' -g '**/Dockerfile*' -g '*.{sh,tf}' "${RX[@]}" .
rg -l --pcre2 '\bthanos\b|\bmimir\b|\bcortex\b|\bremote_?write\b|\bvictoria-?metrics\b' -g '*.tf' "${RX[@]}" .
echo "scratch: $T"
```

Step 2 ties a hand-written rule to its registry row when the row's `alerts` cell names it, or the row's `rules` cell names the rule's file (the alert name picks between two rows on one file), or, with neither, when the alert name holds every word of the slo name; the row prints as `registry ai/runtime/slos.md:<line> (<slo>)`. Both table shapes read: `slo-audit`'s `| slo | sli | target | window | … | rules |` and a hand-written `| id | SLI | objective (30 days) | … | alerts |`. A tie lends its objective only to a `> factor * budget` comparison, never to a plain depth or lag threshold the row also names. Read the tie. An alert the registry does not tie still prints a 30d / 28d note: re-run step 2 for it with `--slo='<alert regex>=<objective>/<period>'` from the row it implements (that overrides the registry), plus `--retention=<the server's>` for §6, for example `python3 "$BC" deploy/k8s/observability.yaml --registry=ai/runtime/slos.md --slo='ApiLatency.*=99/30d' --retention=15d`.

A finding is a hit **plus** a read of the spec, the rule and the registry row it implements. Two blind spots are structural:
- **Objectives that live only in prose.** When the registry names no objective for a rule, the arithmetic can check internal consistency (both windows, one factor, `factor × budget < 1`), but not the objective. Say so in the row.
- **Bucket constants.** Step 5 lists the bucket lists, the `buckets: CONST` references and Go's `Buckets: prometheus.DefBuckets` (with the default edges printed beside it). Pairing an `le` with its histogram (by metric name, then the constant) is a read; `metric-hygiene-scan`'s inventory does the same join.

### Measured (2026-10-10)

| Tree | Hits that matter | Verdict |
|---|---|---|
| Seeded sample: sloth spec (3 SLOs) + its sloth 0.16.0 output with one hand edit, a Pyrra spec + its pyrra 0.10.2 output, 2 OpenSLO SLOs, 3 hand-written burn rules + 2 latency recording rules, a prom-client bucket list, a Prometheus CR (`retention: 15d`), an nginx Ingress, Datadog and Honeycomb SLO resources; 14 seeds, 6 decoys; pre-flight 0.19 s, `burn-check.py` 0.05 s | every seed caught (14/14) | `burn-check.py` (with `--slo` from the rule comments, `--retention=15d`): 11 burn alerts, 6 specs → SLO-01 ×2 (sloth disabled alerting, OpenSLO no `alertPolicies`), SLO-04 H (`target: 1.0`), SLO-02 (`OrdersSlowBurn` single 6h window), SLO-03 H (`14.4 * 0.01` on a 99.9 objective), SLO-03 M (the hand-edited sloth tier, 5× vs 6×), SLO-10 ×5 (one retention config, so one finding with 5 SLOs). Regenerate-and-diff: sloth 2 changed lines = the hand edit; pyrra empty. Greps: the Datadog SLO with no `slo alert` monitor (§1), `code=~"4..|5.."` and `code="500"` (§4), the Ingress (§4 read), `le="0.25"` against `[0.05, 0.1, 0.3, …]` (§5), the admin export SLO (§3), no policy doc (§6). **Decoys, 0 H/M/L rows:** the Pyrra 14/7/2/1 rules, the sloth 3× ticket tier, `14 * (1 - 0.999)` on 30d (1.94 % vs 2 %: a note, precedents § 12), the Honeycomb SLO with a burn alert, `le="0.3"` with a 0.3 bucket, sloth's `code=~"5.."` |
| `benchmarks/fixtures/*` (15 trees) | 0 specs, 0 burn rules, 0 bucket lists, 0 retention lines | Every § is N/A on every fixture. Two FP classes were removed on the real repo, below. `obs-defects` (eval item 23) is the fixture this skill scores on |
| Real NestJS + Fastify monorepo, read-only, kube-prometheus-stack values under `deploy/`; 0.6 s | 0 specs · 1 burn-rule file (6 alerts, 9 tiers, hand-written in a k8s YAML) · registry `ai/runtime/slos.md` · 0 SLI error-definition hits · Caddy ingress · `le` 0.1 / 0.3 / 1 · retention 30d | `burn-check.py` with the registry's objectives (99.9 / 99 / 99.5, 30d, `--retention=30d`): **0 problems**. Every tier matches the Workbook set by the arithmetic, every budget equals 1 − objective, and every short window is long ÷ 12. §5 refuted: the latency SLI's `le` values sit in `LATENCY_BUCKETS` (0.01 … 10), which step 5 found only after it learned `buckets: CONST`. §6: retention 30d = the 30d period, so a 3d tier has full history; the registry carries the budget policy. **SLO-01 Hardening:** one registry objective (`job-start`) is declared with its SLI missing and an interim depth page, documented. **SLO-05 Unconfirmed (L):** the Caddy edge exports no request metrics, so requests that fail at the edge are outside the app SLI. Two FP classes were fixed on the way: `buckets` matched UI filter models and string-array `*_BUCKETS` constants (now numeric-or-identifier only), and Loki/Tempo `retention_period` lines (dropped from step 6). `git status` was clean after the run |
| Same monorepo, `--registry` (2026-10-10) | its registry is hand-written: `\| id \| SLI \| objective (30 days) \| budget \| alerts \|`, 5 rows | Step 2 now ties all 6 burn alerts by the `alerts` cell, objective and period from the row: **0 problems**, the result the manual `--slo` map gave, with no map. One FP class found and fixed on the way: the rows also name a depth and a lag alert (plain `>` thresholds), which a tie first turned into 4 false SLO-02 / SLO-03 rows; a registry tie now never makes a plain threshold a burn rule |
| `benchmarks/fixtures/obs-defects`, staged copy; 0.2 s | 5 specs · 15 burn alerts · registry 10 rows, 7 hand-written alerts tied by `--registry` · `le` 0.25 / 0.2 vs `[0.1, 0.5, 1, 2]` and `prometheus.DefBuckets` | 12/12 seeds in the verbatim pre-flight (54 lines). Two gaps found and fixed: a burn rule copied from another SLO (`14.4 * (1 - 0.99)` on a 99.9 % row) printed only a hidden note until step 2 passed the registry (now SLO-03 H ×3), and step 5 missed `Buckets: prometheus.DefBuckets` (no call parentheses) |

## The 3,000-hit path

1. **Intersect** with what is loaded or applied: generated rules a `rule_files` glob or `ruleSelector` picks up (`alert-rule-lint` §4), vendor resources in the applied Terraform root, registry rows marked in force.
2. **Group** by spec (one sloth file is one group), generator flag set, retention config and registry row. One generator defect is one finding with N rules (precedents P4, § 42).
3. **Rank:** SLOs with page tiers on payment / auth / checkout paths first, then the rest, then ticket-only and report-only.
4. **Read the top 30 groups.**
5. **Run the bulk oracle:** one `burn-check.py` pass over every burn-rule file with the registry's `--slo` map, and one regenerate-and-diff per generator.
6. **Ledger the rest** as `Live, unreviewed (k groups / n rules — burn-check.py <paths> --format=text)`. Never mark them `checked`.

## Scans for

| § | Classes | Oracle | Default |
|---|---|---|---|
| 1 | SLO-01 SLO with no burn alert | `sloth generate` → 0 `alert:`; spec flags; vendor alert resources | medium |
| 2 | SLO-02 single window / short ≠ long ÷ 12; SLO-03 factor vs objective and period; generated drift | `burn-check.py`; regenerate-and-diff | high (objective mismatch, > 2×); medium (≤ 2×, single window, drift) |
| 3 | SLO-04 impossible target; SLO-09 low-traffic on standard tiers | arithmetic (S) | medium; SLO-09 low |
| 4 | SLO-05 SLI past the edge; SLO-06 wrong error definition | replay (U/L) | medium; SLO-05 low to medium |
| 5 | SLO-07 latency threshold not a bucket edge | registry `count(x_bucket{le="T"}) > 0` (V199) | high |
| 6 | SLO-08 no budget policy; SLO-10 period > retention | S | SLO-08 low; SLO-10 medium |

### 1. SLO with no burn alert (SLO-01)

```
BAD:   sloth page_alert + ticket_alert disable: true  ·  OpenSLO SLO with no alertPolicies and no hand-written burn rule  ·  datadog SLO with no "slo alert" monitor
GOOD:  sloth alerting with page and ticket tiers  ·  Pyrra (generates ErrorBudgetBurn per spec unless spec.alerting.disabled [K?: the key at the installed version])  ·  honeycombio_slo + honeycombio_burn_alert
```
**Read the code:**
- Is the SLO declared report-only (a `description`, an ADR, the registry)? Then it is no finding.
- Does a hand-written burn rule elsewhere implement it? Search the rule files for its SLI metric.
- For OpenSLO and vendor SLOs, which tool evaluates the policy?

**Finding when** an SLO in force has no rule or monitor that notifies on budget burn. **Proof (V207):** `sloth generate` from the spec → 0 `alert:` lines (measured on sloth 0.16.0), or the vendor resource has no alert resource referencing it.

### 2. Single window, factor vs objective or period, generated drift (SLO-02, SLO-03)

```
BAD:   ratio_rate1h > (14.4 * 0.001) alone  ·  > (14.4 * 0.01) on a 99.9 SLO  ·  14.4 on a 7d period (3.36 expected)  ·  1h with a 30m short window
       a committed sloth file whose 6× tier reads 5×  (regenerate diff ≠ ∅)
GOOD:  14.4·5m/1h + 6·30m/6h page, 3·2h/1d + 1·6h/3d ticket on 30d  ·  Pyrra 14/7/2/1 on 28d, windows scaled on other periods
       14 on 30d/1h (1.94 % vs 2 %) or 14.4 on 28d (13.44): a note, never a finding
```
**Read the code:**
- Where were the objective and period read: spec, metadata, `exhaustion`, or `--slo` from the registry? An unread period is a note.
- Is the rule generated? Then the fix is in the spec plus a regeneration, and the finding is the drift (precedents § 42). Diff with the repo's own generate flags before calling it drift.
- Does an ADR tune the factor deliberately?
- Do the long and short windows read the same SLI?

**Finding when** a burn tier pages at a burn other than the one its objective and period imply: the wrong budget, or a factor more than 10 % off the matched tier. A single window counts too, and so does a committed generated rule that differs from its spec's output. **Severity:** H for an objective mismatch or a factor beyond 2× either way; M otherwise. **Proof (V207):** `burn-check.py` row with the arithmetic written out (`f × W / P` against the tier's budget fraction), regenerate-and-diff, and the promtool pair: fast burn fires and a slow leak tickets.

### 3. Impossible target; low traffic on standard tiers (SLO-04, SLO-09)

```
BAD:   objective: 100 / target: 1.0  ·  99.999 % over 30d with burn pages (26 s of budget)  ·  objective 90 with the 14.4× page (needs an error ratio of 1.44)
       an admin export at 99.9 % with a few dozen runs a day on the 14.4×/1h page
GOOD:  99.9 %/30d with Workbook tiers  ·  a 90 % batch SLO that only tickets  ·  low-traffic SLO with synthetic traffic or a longer window (precedents § 15)
```
**Read the code:**
- Does the design rely on burn-rate pages, or only on tickets (precedents § 14)?
- How many events does the SLI see per hour? `burn-check.py` cannot know it; it is `NO-DATA(prometheus)` without a live count. Precedents § 15 makes one-error paging a design issue.

**Finding when** the arithmetic shows a page that cannot fire, or a budget gone before the fastest page can fire, or there is no budget at all. **Proof:** the arithmetic (S): `(1 − o) × P` against the 5m short window, and `factor × (1 − o) ≥ 1`. SLO-09's traffic half is L-tier.

### 4. SLI past the edge; wrong error definition (SLO-05, SLO-06)

```
BAD:   error_query code=~"4..|5.."  ·  code!="200"  ·  only code="500" (misses 502/503/504)  ·  app-only SLI while an ingress / mesh serves every request
GOOD:  code=~"5.."  ·  a documented 429 self-shed counted as bad (precedents § 13)  ·  the SLI on edge metrics, or the app SLI plus an edge-failure SLI
```
**Read the code:**
- Does the team document a 4xx class as a server failure? Then it is no finding (§ 13).
- Does the edge (ingress-nginx, Envoy, ALB, Caddy) export request metrics? If not, the edge half belongs to infrastructure (§ Boundaries).
- Does a traffic-absent rule cover the total-outage case the app SLI cannot see (`alert-rule-lint` §6)?

**Finding when** replaying 404s moves the SLI, or 502 / 503 / 504 do not. For SLO-05, the finding is that failures at the edge are outside every SLI. **Proof (V207):** replay synthetic 404s and assert the SLI does not move (U). SLO-05 is L-tier (app vs edge SLI over 7d), else `NO-DATA(prometheus)` with the static half `[report-flagged]`.

### 5. Latency threshold not a bucket edge (SLO-07)

```
BAD:   …_bucket{le="0.25"} while the histogram registers [0.05, 0.1, 0.3, 0.5, 1]   ·   le="1" on Prometheus 3 (alert-rule-lint AL-21)
GOOD:  le="0.3" with 0.3 in the bucket list (or in the constant it references)   ·   native / exponential histograms (no le)
```
**Read the code:**
- Which histogram does the SLI read? Follow the metric name to its registration and the `buckets` list or constant (step 5).
- Is it an OTel exponential or a native histogram?
- Is the value written the way the server normalizes it (precedents § 45)?

**Finding when** the SLI's `le` names no bucket edge of the histogram it reads, so the numerator is empty and the SLI reads 0 or NaN. **Severity:** H. **Proof (V199):** registry scrape `count(x_bucket{le="T"}) > 0` fails, or a static two-ended trace (the `le` literal and the bucket list), `[report-flagged]` until the scrape.

### 6. No budget policy; window longer than retention (SLO-08, SLO-10)

```
BAD:   SLO specs with no policy doc  ·  a 30d SLO on Prometheus retention: 15d with no Thanos / Mimir / remote read
GOOD:  a policy naming owners and what happens at exhaustion (the registry may carry it)  ·  retention ≥ the longest SLO period, or a long-term store
```
**Read the code:**
- Which retention does the production server run (the Helm values, the Prometheus CR, the compose flag)? A local or dev values file is noise (precedents § 30).
- Does a long-term store answer the SLO queries?

**Finding when** the budget is computed over less data than its period, or no policy says what happens when it is gone. **Proof:** S (the retention line and the SLO period). L: `count_over_time(up[<period>])` against the expected samples.

## Proof

- **Regenerate and diff (V207):** the Tool-lane commands, on copies, with the repo's own generate flags. The output must be empty, or the drift is the finding.
- **Burn arithmetic (V207):** the `burn-check.py` row restated by hand in the finding: `f × W / P` against the tier's budget fraction, and `b` against `1 − o`.
- **promtool pair (V203 shape):** on the server's Prometheus major, a fast burn must fire the page tier, and a slow leak must fire only the ticket tier. A test that passes on the unfixed rule proves nothing; rebuild it until it fails.
- **Error definition (V207):** replay synthetic 404s through the SLI's recording rule in a promtool test; the SLI must not move.
- **Bucket edge (V199):** `count(x_bucket{le="T"}) > 0` on the registry scrape.

A fix is accepted only when all of these hold:
- the spec is fixed and regenerated;
- the diff is empty;
- `burn-check.py` prints nothing for the touched rules;
- the promtool pair is green;
- `alert-rule-lint` shows no new row on the regenerated file.

Never accepted:
- a hand edit to generated rules;
- demoting the page tier to a ticket to make the arithmetic pass;
- deleting the SLO or its alert;
- an objective change without the owner's sign-off (`/obs-fix` STOP rule).

## Output

```
slo-rule-scan — specs: sloth 0.16.0 (header), pyrra 0.10.2 (Dockerfile), OpenSLO v1 · rules: 3 burn-rule files · Prometheus v3.5.0, retention 15d (k8s/prometheus.yaml:8)
Lanes: sloth generate (ran), pyrra generate (ran), oslo (blocked: lane not installed oslo@0.13.0), burn-check.py

Findings: 4 · Unconfirmed: 3 · Hardening: 0

1. prometheus/rules/slo-hand.yml:25  PaymentsFastBurn [1h/5m]                [report-with-fix]   high
   §2 SLO-03 — threshold 14.4 × 0.01 on a 99.9 % / 30d objective (registry row payments): fires at 10× the intended burn.
   Proof: burn-check.py; promtool fast-burn test silent at 14.4 × 0.001 (fails). Fix: (14.4 * (1 - 0.999)) on both windows.

2. slo/generated/checkout.yml:161  ApiAvailability [6h/30m]                    [report-with-fix]   medium
   §2 SLO-03 drift — committed tier reads 5×; `sloth generate -i slo/sloth/api.yml` writes 6× (diff: 2 lines).
   Fix: regenerate from the spec (no hand edit); add the generate + diff step to CI.

3. slo/openslo/login.yaml:29  search-perfect                              [report-with-fix]   high
   §3 SLO-04 — target 1.0: no error budget; no burn rate exists. Fix: an objective the owner signs (STOP: /obs-fix asks).

4. k8s/prometheus.yaml:8  retention 15d (5 SLOs, 28d–30d)                 [report-with-fix]   medium
   §6 SLO-10 — every SLO period exceeds TSDB retention; no long-term store. Fix: retention ≥ 30d or a long-term store.

5. app/src/metrics.ts:7 · prometheus/rules/slo-hand.yml:24               [report-flagged]    high
   §5 SLO-07 — SLI le="0.25" while http_request_duration_seconds registers [0.05, 0.1, 0.3, …]. Settling: V199 scrape.

Verification: 21 candidates → 4 findings · 3 unconfirmed · 0 hardening · 0 pre-existing · 14 refuted / grouped (self-verified)

Class coverage:
  §1 no burn alert (SLO-01)          checked (6 specs + 2 vendor SLOs → 2 unconfirmed; pyrra, honeycomb clean)
  §2 windows / factor / drift        checked (11 alerts, 19 tiers → 2 findings; 1 note § 12) · drift: sloth 1 group, pyrra empty
  §3 impossible / low traffic        checked (1 finding; admin export SLO-09 traffic NO-DATA(prometheus))
  §4 SLI definition / edge           checked (2 rules → 1 unconfirmed; ingress present → SLO-05 NO-DATA(prometheus))
  §5 bucket edge                     checked (2 le values → 1 flagged; 0.3 grounded)
  §6 policy / retention              checked (1 finding; no policy doc → Hardening-level SLO-08 row)
```

`[report-with-fix]`: the objective and period are read, the arithmetic or the diff shows the defect, and the fix is in the spec, the rule's source or the retention config. `[report-flagged]`: one link is unproven (an unread period, a bucket constant not followed, an edge without metrics, no live count); the row names it and the settling command.

The coverage block lists **all six** §s on every run:
- `checked (k → m)` only when the lane ran on present surfaces;
- `N/A (no SLO spec, no burn rule, no vendor SLO)` only when the repo has none;
- `blocked (<reason>)` when a generator, `burn-check.py` or a grep could not run;
- `NO-DATA(<source>)` for an L-tier half;
- `Live, unreviewed` for rows not yet read.

## False positives / precedents

The verifier reads [`precedents/observability.md`](../../../../snippets/precedents/observability.md) § 2, § 5, § 12–§ 16, § 30, § 36–§ 37, § 42 and § 45. The ones this skill meets most:
- **§ 12** Pyrra 14 / 7 / 2 / 1 and the 3× 24h/2h ticket tier are correct. 13.44 on 28d, or 14 on 30d, is a note. The literal `14` vs `14.4` is never the test; the arithmetic is.
- **§ 13** Counting 4xx as good is the Workbook's convention. A documented self-shed 429 counted as bad is right.
- **§ 14** A 100 % SLO is always a finding. 99.999 % is a finding only when burn pages are relied on.
- **§ 15** Low traffic paging on one error is a design issue, not a rule bug.
- **§ 2** A burn rule without `for` is correct; that is `alert-rule-lint`'s ground, not this skill's.
- **§ 42** Generated rules are judged at the spec: drift is the finding, never a hand-edit request.
- **§ 36–37** Attainment and traffic without a backend are `NO-DATA`. An SLI metric named in a proposed fix must resolve in the inventory.
- **§ 30** A local or dev retention value is noise. Only what the production server runs counts.

## When to run

- On any diff that touches an SLO spec, a generated or hand-written burn rule, a registry row, an SLI recording rule, a histogram bucket list behind an SLI, or the TSDB retention. This is `/obs-audit`'s "an SLO spec or burn rule" dispatch signal.
- On every whole-repo `/obs-audit`, reporting all six §s, before `slo-audit` consumes the definition rows.
- When `/alert-design` proposes burn alerts: its gate is `burn-check.py` plus the regenerate diff on the touched spec.

## Halt conditions

- **A high or critical row needs a separate refuter.** Do not report it as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 10.
  - Under `/obs-audit`, that happens in its verification phase.
  - Run standalone, apply the protocol as a separate second pass and tag those rows `self-verified`.
  - List the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- **No factor or objective finding without the objective and period read and printed with their source.** An unread period is a note.
- **Judge every factor by the arithmetic** (`THR-OBS-BURN`), **never by a literal.** A row that says "14 should be 14.4" without `f × W / P` is a defect of this skill.
- **Do not hand-edit generated rules or ask for it.** Diff with the repo's own generate flags before calling it drift.
- **Never run a generator into the project tree.** Every output goes to `${TMPDIR}`, and `git diff --exit-code` proves the tree untouched.
- **Do not estimate attainment, traffic or a page budget.** Those are `slo-audit`, `NO-DATA` and `alert-audit` (§ Boundaries).
- **Do not print "SLOs look fine".** Print the coverage block; a § whose lane did not run is `blocked`, never `checked`.
- **Do not re-derive a class another skill owns** (§ Boundaries). Cross-link it.

## Related

- `slo-audit` (this pack) consumes these rows for attainment and writes the registry. `alert-rule-lint` (this pack) lints the same burn rules for `for`, runbook, selectors and routing, through the same `rule-inventory.py`.
- `metric-hygiene-scan` §3 (this pack) owns the bucket registration §5 joins. `@sre-engineer` writes the budget policy. `@observability-reviewer` judges these rows. `/obs-audit` dispatches, `/obs-fix` closes, and `/alert-design` proposes.
- `edge-reliability-scan` §15 (infrastructure, when installed) for edge request metrics and access-log fields, and `@cost-reviewer` (finops, when installed) for retention cost: § Boundaries.

## Sources

Measured 2026-10-10:
- sloth 0.16.0 `validate` / `generate`: page and ticket alert shape, metadata recordings, 0 alerts with both tiers disabled, determinism, `openslo/v1` rejected.
- pyrra 0.10.2 `generate`: 28d and 30d windows, minute rounding, `exhaustion` / `long` / `short` labels.

Carried from the observability research catalog and the batch-4 eval:
- the SLO-01..SLO-10 class rows;
- the Workbook burn tiers and the 1/12 short window (SRE Workbook *Alerting on SLOs*, CC BY-NC-ND, paraphrased);
- the sloth `google-30d` and Pyrra `Windows()` sets;
- the tool versions.

Paraphrased; no text is reproduced beyond identifiers.
