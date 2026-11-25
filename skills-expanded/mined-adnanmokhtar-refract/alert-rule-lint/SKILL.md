---
name: alert-rule-lint
description: "Per-rule alert lint: never-fire, missing for/runbook/severity, window vs scrape, Prom 3 breakage, routing — tool-proved."
kind: skill
pack: observability
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: alert-rule-lint

## Premise

The worst alert is the one that never fires, and an empty query result looks exactly like a healthy service. A selector with a typo, a rate window of one scrape interval, an integer `le` on Prometheus 3, a 0/0 error ratio at zero traffic, `$value` in a label, a rule file no `rule_files` glob loads, a PrometheusRule the operator never selects, a `severity=critical` that the route tree sends to a receiver with no integrations — each of these passes review because the YAML reads fine. The second-worst pages on a one-sample blip, or after the incident is over.

This skill finds those defects in the rule, routing and monitor files a repo ships — Prometheus rule files, PrometheusRule CRDs, Helm-embedded groups, Mimir / Thanos / Loki ruler files, jsonnet mixins, Alertmanager and `AlertmanagerConfig`, Grafana-managed alerts and Datadog / New Relic / Honeycomb monitors — and proves each with a tool exit code. It owns `/obs-audit`'s Alert rules (§1–§6), Alert design (§7), Routing (§8) and Vendor monitors (§9) rows. `@observability-reviewer` (this pack) judges its rows; `alert-audit` (this pack) consumes them and keeps only the behavioural half — fire history, flapping, owner recency.

**Every finding cites the rule (alert name + `file:line`) + the condition that occurs (a sustained failure, a blip, a total outage, a label set the rules emit) + what the rule does then (silent, fires on the blip, routes to a null receiver) + the oracle that showed it + the fix in the rule's own source (the spec or mixin for generated rules, precedents § 42).** The unit is the rule, never the file: a file where one alert of two lacks a runbook is one finding on that alert. A grep hit or a tool message is a candidate; "alerting looks fine" is never printed — the output is the class-coverage block (§ Output).

**Tool first, grep second.** Config defects have deterministic, offline oracles: promtool, pint, amtool, mimirtool. `scripts/rule-inventory.py` (beside this file, installed as `.claude/skills/alert-rule-lint/scripts/rule-inventory.py`; Python 3 standard library, read-only) is the no-tool lane and the inventory every lane grounds against. Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/observability.md`](../../../../snippets/precedents/observability.md); the oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Observability, V203–V206.

## The rule

A candidate is a finding when all four hold (gates 1–7 of the protocol, read for alerts in `precedents/observability.md` § Reading the seven gates):

1. **The rule is loaded.** A `rule_files` glob matches its file, or the Prometheus CR `ruleSelector` selects its PrometheusRule, or the ruler namespace is synced. An unloaded rule is §4's AL-22 candidate — never dismissed as dead code.
2. **The condition occurs.** The failure the rule watches can happen at the rate and duration the expression assumes; the blip exists; traffic can drop to zero.
3. **Nothing already handles it.** A sibling traffic-absent rule (precedents § 5), a generator-emitted `absent` rule, a routes test proving every emitted label set (precedents § 9), a recording rule that smooths the expression.
4. **The oracle fired, on the server's version.** promtool, pint or amtool exited non-zero on the copy, or `rule-inventory.py` produced the row and a two-ended static trace holds (a rule never loaded, `$value` in labels, a selector absent from the inventory — `[report-flagged]` until a live `count()`). The Prometheus and Alertmanager versions are read from files, never assumed (gate 3).

## Boundaries

- **Fire history, flapping, dead-by-behaviour, owner recency** → `alert-audit` (this pack), L-tier with `NO-DATA(<source>)`. This skill never estimates a fire count.
- **Burn-rate arithmetic, SLO specs, regenerate-and-diff** → `slo-rule-scan` §2 (`burn-check.py`, `THR-OBS-BURN`). Here a multiwindow burn rule is recognised only so §1 does not demand a `for` on it (precedents § 2) and §4 still grounds its selectors.
- **Notification secrets inline** (Slack webhook, PagerDuty key) → security `secret-scan-method` when the security pack is installed; without it the row is tagged `secret (owner pack not installed)`, listed, never graded (precedents P2).
- **PrometheusRule / ServiceMonitor schema validity** (kubeconform with local CRD schemas) → infrastructure `k8s-api-version-scan` §2 when that pack is installed; without it the schema is unchecked and says so. This skill owns the PromQL content and whether the rule is *selected* (AL-22).
- **A CI job that runs promtool or pint but is neutered** (`continue-on-error`, `|| true`, path filters) → devops when that pack is installed; `/obs-audit` corroborates with its RULES GATE row.
- **Canary-analysis selectors** (Argo `AnalysisTemplate`) are devops's; they may cite `rule-inventory.py --check=selectors` for grounding.
- **Dashboards and the metric registration itself** → `telemetry-config-scan` §8 and `metric-hygiene-scan` (this pack).

## Adapt to the codebase — the rule lanes

Read each version from a file and print it in the output header: the Prometheus image tag (compose, Helm values, the Prometheus CR `spec.version`, the `kube-prometheus-stack` chart), the Alertmanager image, the pint version CI pins. A Prom-3-only class on an unread version is Unconfirmed (precedents § 17, § 45).

| Lane | Surfaces | Tool (T) | No-tool lane |
|---|---|---|---|
| Prometheus rule files | files matched by the `rule_files` globs in `prometheus.yml` | promtool (check + unit tests), pint | `rule-inventory.py` |
| Kubernetes | PrometheusRule CRDs, Helm `additionalPrometheusRules(Map)`, the Prometheus CR `ruleSelector` | promtool on the `--emit-rules` output; pint with the relaxed parser | `rule-inventory.py --prometheus-cr=` |
| Mimir / Thanos / Loki rulers | namespace rule files; LogQL rules | mimirtool `rules check` (its `rules lint` rewrites without `-n`) | `rule-inventory.py` (PromQL only) |
| jsonnet mixins | `mixin.libsonnet`, `prometheusAlerts` | render with jsonnet into the scratch dir, then the Prometheus lane; fix the source | the rendered file |
| Alertmanager | `alertmanager.yml`, `AlertmanagerConfig`, Helm `alertmanager.config` | amtool (check-config, the routes matrix) | `rule-inventory.py --am=` |
| Grafana-managed | provisioning `alerting/*.yaml`, `grafana_rule_group` | — | §9 read |
| Vendor monitors | `datadog_monitor`, `newrelic_nrql_alert_condition`, `honeycombio_trigger` | — | §9 read |

## Tool lane

Run every tool in `${TMPDIR:-/tmp}` on **copies**, pinned to the versions this skill was measured with (2026-10-10, darwin-arm64 release archives checked against the release `sha256sums.txt`): **promtool 3.15.0** (use **2.55.1** when the server is 2.x — the binary decides what parses), **amtool 0.34.1**, **pint 0.89.2**, **mimirtool 3.2.2**. Downloads come from each project's GitHub release page (`prometheus/prometheus`, `prometheus/alertmanager`, `cloudflare/pint`, `grafana/mimir`) into the scratch dir — never installed globally. A tool that cannot install prints `blocked (lane not installed: <tool>@<ver>)` in its coverage cell; `rule-inventory.py` still runs.

Exit codes are read, never assumed (precedents § 53): promtool 1 = error, 3 = lint (duplicates only with `--lint-fatal`); pint exits 1 when a problem at `--fail-on` (default `bug`) is found; amtool `routes test` **without** `--verify.receivers` exits 0 whatever it resolves (measured: `severity=critical` → `dev-null`, exit 0). Measured on the copies: `pint lint` left every file byte-identical; `mimirtool rules lint` without `-n` rewrote the file (added `namespace:`, re-indented) — so it never runs in the tree.

pint's default config runs few offline checks: on the seeded sample (§ Measured) it reported 4 problems. The rule-level checks need this config, written to the scratch dir (severities from `THR-OBS-ALERT`; replace the vocabulary with the one the routes match on):

```hcl
parser {
  relaxed = [".*"]
}
rule {
  match {
    kind = "alerting"
  }
  label "severity" {
    severity = "bug"
    value    = "(page|critical|ticket|warning|info|none)"
    required = true
  }
  annotation "summary" {
    severity = "warning"
    required = true
  }
}
rule {
  match {
    kind = "alerting"
    label "severity" {
      value = "(page|critical)"
    }
  }
  annotation "runbook_url" {
    severity = "bug"
    required = true
  }
  for {
    severity = "bug"
    min      = "1m"
    max      = "30m"
  }
}
```

With it pint 0.89.2 parsed the CRDs and the Helm values (`relaxed`), applied group-level `labels:`, and reported 15 bugs; 5 of them are `rule/for` on multiwindow burn rules (Pyrra ×2, Workbook ×3), refuted by precedents § 2 — read the `rule-inventory.py` row, which marks burn rules, before reporting a pint `rule/for` hit. pint also warns `alerts/comparison` on a Watchdog `vector(1)`: that is the intended heartbeat (§6), not a finding.

## Pre-flight

Run as **one** bash script from the repo root (`bash <<'EOF' … EOF`: macOS ships bash 3.2, so no `mapfile`; zsh does not split an unquoted `$line` into arguments, which silently turned every amtool case into one label). Every `rg` names its path; any rg exit 2 is a failed grep, never zero hits. Files-without-match is `--files-without-match` — never `rg -L`, which is `--follow`.

```bash
T="$(mktemp -d "${TMPDIR:-/tmp}/arl.XXXXXX")"; RI=.claude/skills/alert-rule-lint/scripts/rule-inventory.py
X=(-g '!**/node_modules/**' -g '!**/{dist,build,out,target,bin,obj,vendor,.venv,venv,__pycache__,coverage,.next,.nuxt,.output,generated,__generated__}/**'
   -g '!**/{test,tests,__tests__,spec,specs,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata,playwright,cypress}/**'
   -g '!**/*.{spec,test,e2e,stories,story}.*' -g '!**/*_test.go' -g '!**/test_*.py' -g '!**/conftest.py' -g '!**/{docs,ai,.claude}/**' -g '!*.{md,mdx,snap,lock}' -g '!**/*.min.*')
# Rule surfaces keep generated/ (sloth and pyrra output is loaded, precedents § 42) and drop only vendored and test trees.
RX=(-g '*.{yml,yaml,jsonnet,libsonnet}' -g '!**/node_modules/**' -g '!**/{vendor,.git,charts/*/charts}/**' -g '!**/{test,tests,__tests__,fixtures,__fixtures__,testdata,e2e}/**' -g '!**/{docs,ai,.claude}/**')
CODE=(-g '*.{ts,tsx,js,mjs,cjs,py,go,java,kt,kts,cs,rb,php}'); NM='([A-Za-z_:][\w.:]*)'
# 0 versions (gate 3): image tags, the kube-prometheus-stack chart, the Prometheus CR (spec.version, ruleSelector).
rg -n --pcre2 '(?:prom/(?:prometheus|alertmanager)|prometheus/(?:prometheus|alertmanager)|cloudflare/pint|grafana/mimir)\S*:v?\d[\w.]*' -g '*.{tf,toml,json}' -g 'Dockerfile*' "${RX[@]}" -g '!**/package*.json' .
rg -n -A3 '\bkube-prometheus-stack\b' -g 'Chart.yaml' -g 'helmfile*.y*ml' -g '*.{tf,sh,bash,mk}' -g 'Makefile' -g '!**/node_modules/**' .   # a helm line with no --version pins nothing
PCR=(); while IFS= read -r f; do PCR+=("$f"); done < <(rg -l --pcre2 '^kind:\s*Prometheus\s*$' "${RX[@]}" .)
[ ${#PCR[@]} -gt 0 ] && rg -n -H --pcre2 '^\s+version:\s*\S+|^\s*(?:ruleSelector|ruleNamespaceSelector|serviceMonitorSelector):|^\s+(?:release|app\.kubernetes\.io/\S+):\s*\S+' "${PCR[@]}"
rg -n --pcre2 '\bruleSelectorNilUsesHelmValues\b|^\s*ruleSelector:' -g '*values*.y*ml' -g '!**/node_modules/**' .
# 1 rule files (§1–§7), rule_files globs (AL-22), scrape intervals (AL-12): prometheus.yml, ServiceMonitor/PodMonitor, Alloy.
RULE_FILES=(); while IFS= read -r f; do RULE_FILES+=("$f"); done < <( { rg -l --pcre2 '^\s*-?\s*(?:alert|record):\s*\S' "${RX[@]}" . ; rg -l --pcre2 '\bkind:\s*PrometheusRule\b|\badditionalPrometheusRules(?:Map)?:|\bprometheus(?:Alerts|Rules)\b' "${RX[@]}" . ; } | sort -u)
echo "rule files: ${#RULE_FILES[@]}"; [ ${#RULE_FILES[@]} -gt 0 ] && printf '  %s\n' "${RULE_FILES[@]}"
rg -n -A6 '^rule_files:' "${RX[@]}" .
rg -n --pcre2 '^\s*(?:scrape_interval|evaluation_interval):\s*\S+|\bscrape_interval\s*=\s*"\d+[smh]"' -g '*.{alloy,river}' "${RX[@]}" .
SM=(); while IFS= read -r f; do SM+=("$f"); done < <(rg -l --pcre2 '^kind:\s*(?:ServiceMonitor|PodMonitor|Probe)\s*$' "${RX[@]}" .)
[ ${#SM[@]} -gt 0 ] && rg -n -H --pcre2 '^\s+(?:-\s*)?interval:\s*\S+' "${SM[@]}"
# 2 the inventory (§4, precedents § 37, § 43): metric names registered in shipped code — prom-client and
#   @willsoto/nestjs-prometheus, prometheus_client, client_golang Opts, Micrometer, OTel meters, prometheus-net.
{ rg -U --pcre2 -o --no-filename -r '$1' "(?:new\s+(?:\w+\.)?(?:Counter|Gauge|Histogram|Summary)|make(?:Counter|Gauge|Histogram|Summary)Provider)\s*(?:<[^>]*>)?\(\s*\{[^}]*?\bname\s*:\s*['\"]${NM}['\"]" "${CODE[@]}" "${X[@]}" .
  rg -U --pcre2 -o --no-filename -r '$1' "(?:\bprometheus_client\.|(?<![.\w]))(?:Counter|Gauge|Histogram|Summary|Info|Enum)\(\s*['\"]${NM}['\"]" "${CODE[@]}" "${X[@]}" .
  rg -U --pcre2 -o --no-filename -r '$1' "(?:Counter|Gauge|Histogram|Summary)Opts\s*\{[^}]*?\bName:\s*\"${NM}\"" "${CODE[@]}" "${X[@]}" .
  rg -U --pcre2 -o --no-filename -r '$1' "(?:\b(?:Counter|Timer|Gauge|DistributionSummary|LongTaskTimer)\.builder|\bregistry\.(?:counter|timer|gauge|summary)|\b(?:create|Create)(?:Counter|Histogram|UpDownCounter|Gauge|Observable(?:Gauge|Counter|UpDownCounter))(?:<\w+>)?|\bcreate_(?:counter|histogram|up_down_counter|gauge|observable_\w+)|\b(?:Int64|Float64)(?:Counter|Histogram|UpDownCounter|Gauge|Observable(?:Counter|Gauge|UpDownCounter))|\bMetrics\.Create(?:Counter|Gauge|Histogram|Summary))\(\s*['\"]${NM}['\"]" "${CODE[@]}" "${X[@]}" .
} | sort -u > "$T/inventory.txt"; echo "inventory: $(wc -l < "$T/inventory.txt" | tr -d ' ') names → $T/inventory.txt"
# 3 routing (§8) and vendor monitors (§9).
rg -l --pcre2 '^\s*receivers:\s*$|\bkind:\s*AlertmanagerConfig\b' "${RX[@]}" .
rg -n --pcre2 '\b(?:noDataState|execErrState|no_data_state|exec_err_state)\b\s*[:=]\s*"?OK\b|\bresource\s+"(?:grafana_rule_group|datadog_monitor|newrelic_nrql_alert_condition|honeycombio_trigger|honeycombio_burn_alert)"' -g '*.{yml,yaml,json,tf}' -g '!**/node_modules/**' -g '!**/.terraform/**' .
# 4 the per-rule rows: pass the version and the configs the steps above printed (one --prometheus-config per server).
python3 "$RI" "${RULE_FILES[@]}" --format=text --inventory="$T/inventory.txt" --prom-major=<2|3 from step 0> \
  --prometheus-config=<prometheus.yml> --prometheus-cr=<prometheus CR file> --am=<alertmanager.yml or Helm values> \
  --emit-rules="$T/plain" --emit-am="$T/am.json"
python3 "$RI" "${RULE_FILES[@]}" --label-sets > "$T/label-sets.txt"
echo "scratch: $T"
```

`rule-inventory.py` flags: `--check=` takes `annotations,for,windows,selectors,prom3,value-in-labels,nan,absent,watchdog,expr,design` (default all); `--scrape=job=30s,*=15s` when intervals live outside a `prometheus.yml`; `--page-severities=` and `--severity-vocab=` when the routes use another vocabulary (`THR-OBS-ALERT`); `--group-labels=no` on a server that ignores them (precedents § 41); `--all` shows Hardening rows in text mode; `--self-test` proves the parser on the § 0.1 shapes (a commented `# runbook_url:`, a group-level `severity` on the next group, a block-scalar `expr`, a CRD, Pyrra and Workbook burn rules, a Watchdog). Exit 0 none, 1 a problem, 2 usage.

Then the tool lane on copies (each line prints `blocked (…)` when its binary is absent):

```bash
B="$T/bin"   # the four binaries downloaded into the scratch dir (§ Tool lane); pint.hcl written beside them
mkdir -p "$T/tree" && tar cf - "${RULE_FILES[@]}" | (cd "$T/tree" && tar xf -)
"$B/promtool" check rules --lint=all --lint-fatal <copied plain rule files> "$T"/plain/*.yml; echo "promtool exit $?"
"$B/pint" -c "$T/pint.hcl" --offline --no-color --show-duplicates lint --min-severity=info "$T/tree"; echo "pint exit $?"
"$B/amtool" check-config "$T/am.json"; echo "amtool exit $?"
while read -ra L; do [ "${L[0]}" = "(no" ] && L=(); printf '%-40s -> %s\n' "${L[*]:-<none>}" "$("$B/amtool" config routes test --config.file="$T/am.json" "${L[@]}" 2>/dev/null)"; done < "$T/label-sets.txt"
```

`--emit-am` writes the Alertmanager config — top level, or embedded in Helm values under `alertmanager.config` — as JSON amtool reads (quoted scalars stay text, plain ones are typed). Add the chart's own label sets by hand when it ships default rules (`alertname=Watchdog`, `severity=critical`, `severity=info`). The matrix prints the receiver each emitted label set reaches; every set that pages is then re-run with `--verify.receivers=<the receiver the design names>` (exit 1 on mismatch). A pager set that resolves to a receiver with no `*_configs` is AM-01.

### Measured (2026-10-10)

| Tree | Result |
|---|---|
| `benchmarks/fixtures/*` (15 fixtures) | 0 rule files, 0 inventory names, 0 alertmanager configs; the version and interval greps print nothing after two FP classes were removed (a `pubspec.yaml` `version:` and a compose healthcheck `interval:` — both greps are now scoped to Prometheus CR / ServiceMonitor files). No fixture ships alert rules: `obs-defects` (eval item 23) is the fixture this skill scores on |
| Seeded sample: 7 rule files, 35 alerts, 15 recording rules, Alertmanager, Prometheus CR, Helm values, code in TS / Python / Go / Java | pre-flight 0.14 s. Inventory 12 names, 0 from tests (a `*.spec.ts` registration is excluded); one FP class removed — the bare `Info(` alternative (prometheus_client) also matched Go `slog.Info("priced", …)`, so it is anchored to `prometheus_client.` or no receiver. `rule-inventory.py`: 34 H/M/L rows covering every seeded class (AL-01, -02, -03, -04, -05, -06, -08, -09, -10 ×2, -12, -13, -16, -17 ×2, -20, -21, -22 ×2, SY-01 ×2, SY-03, SY-04, AM-01, -03, -04, -06, -08); 0 H/M/L rows on the decoys (Pyrra 14/7/2/1, Workbook 3- and 4-tier burn rules without `for`, Watchdog `vector(1)`, a ticket without a runbook, `[1m]` on a 15s job, a 5xx ratio with a zero-traffic sibling) |
| Same sample, the research's corrected awk | 21 lines: it agrees on the page-tier misses but cannot tell tiers or burn rules apart (13 of its lines are precedents § 1 / § 2), and passes `for: 0s` |
| Same sample, promtool 3.15.0 / 2.55.1 | 3.15.0: all 5 plain files and 3 emitted CRD/Helm files parse, and a group-level `labels: {severity: page}` reaches the alert in `promtool test rules`. **2.55.1 rejects the whole file** (`field labels not found in type rulefmt.RuleGroup`) — on a 2.x server a group label is AL-22, not precedents § 41 |
| Same sample, pint 0.89.2 `--offline` | default config: 4 problems (AL-05, AL-06, an `alerts/comparison` warning on the Watchdog, a `promql/fragile` warning on a Workbook burn rule), and the CRD and Helm files fail to parse. With the config above: CRD and Helm parsed, 15 bugs + 5 warnings (`--show-duplicates`) — AL-01 ×4, AL-02, AL-03, AL-04 ×2, AL-05, AL-06, and 5 `rule/for` on burn rules (precedents § 2). Offline pint did not report AL-08, -10, -12, -13, -16, -17, -20, -21, -22 or SY-*: those rows come from `rule-inventory.py` |
| Same sample, mimirtool 3.2.2 | `rules check` exit 0 (it checks recording-rule naming: a `record: errorratio` exits 1); `rules lint -n` changed nothing |
| Same sample, promtool fire/blip pair | `rate(x[30s])` on a 30s series: the sustained-burst test gets `[]` (exactly 1× is empty on 3.x); with `[1m]` it fires. A no-`for` raw-counter page fires on a one-sample blip. A ratio with no traffic-absent sibling stays silent through a total outage |
| Real repository, read-only (a NestJS + Fastify monorepo, kube-prometheus-stack via Helm, one PrometheusRule CRD under `deploy/`) | pre-flight 0.76 s: 1 rule file (26 alerts, 21 recording rules, 3 groups), 0 hits in excluded trees, inventory 21 names; selector groundings: 21 to code, 18 to recording rules, 5 exporter defaults, 0 ungrounded. Versions: the Prometheus chart is installed by a script with no `--version`, so the Prometheus major is **unread** (gate 3). promtool 3.15.0 and 2.55.1 exit 0 on the emitted groups; pint (config above) 0 bugs, 33 warnings (`promql/regexp` on `route!~".*/health/.*"`, one `rule/dependency`). `rule-inventory.py`: 4 rows + 1 note → after reading: **AM-01 Refuted** (root `null`, but `--verify.receivers=telegram` exits 0 for page, ticket, warning and critical — precedents § 9); **AL-18 [report-flagged]** (the chart's Watchdog is routed to `null` and no heartbeat receiver exists, so a dead pipeline is silent); **AL-21 Unconfirmed** (one ticket rule uses `le="1"` where every other selector writes `le="0.1"` / `"0.3"`: empty on 3.x, clean on 2.x — settle by reading `prometheus_build_info`); **2 × AL-16 Hardening** (a job-failure ratio whose stopped-worker case a queue-backlog page covers; an outbound ratio where zero calls affect no one). Two script FPs found and fixed on this tree: a `/` inside `route!~".*/health/.*"` read as a division, and a `node_*` host counter ratio treated as traffic. `git status` clean after the run |
| `benchmarks/fixtures/obs-defects`, staged copy, step 4 filled from step 0 | 69 lines, 0.2 s; inventory 25 names; `rule-inventory.py` 30 H/M/L rows; 23/23 seeds; 0 H/M/L rows on the decoys. The fixture found one FP class, fixed: a black-formatted `Histogram(` with its name on the next line was not inventoried (the `prometheus_client` line ran without `-U`), so both selectors on it were false AL-10 [H]. The Micrometer / OTel line gained `-U` too. The seeded sample's inventory is unchanged (38 names) |

## The 3,000-hit path

1. **Intersect with what is loaded:** rule files a `rule_files` glob or `ruleSelector` picks up, AM configs a deployment mounts. An unloaded rule is AL-22's candidate, not dismissed.
2. **Group** by rule group, generator (sloth / pyrra / mixin source) and Alertmanager root: one generator defect is one finding with N rules (precedents P4, § 42).
3. **Rank:** page-tier rules first, then rules on critical SLOs and payment / auth / consumer paths, then tickets.
4. **Read the top 30 groups**, rule by rule.
5. **Run the bulk oracle:** one `pint --offline lint` and one `promtool test rules` pass over the copies settle whole groups; the routes matrix settles every label set at once.
6. **Ledger the rest** as `Live, unreviewed (k groups / n rules — rule-inventory.py <paths> --format=text)`. Never mark them `checked`.

## Scans for

| § | Classes | Tool rule / flag | Default |
|---|---|---|---|
| 1 | AL-01, AL-02, AL-09 — `for` absent, too long, `keep_firing_for` misuse | pint `rule/for`; `--check=for` | M page, L ticket |
| 2 | AL-03..AL-06 — severity, runbook / summary, a template label the aggregation dropped, `$value` in labels | pint `rule/label`, `alerts/annotation`, `alerts/template`; `--check=annotations,value-in-labels` | L–M; **H** for `$value` |
| 3 | AL-07, AL-08, AL-13, AL-14, AL-15, AL-19, AL-20 — expression cannot express the condition | pint `alerts/comparison`, `promql/counter`, `promql/rate`, `promql/fragile`; `--check=expr` | M |
| 4 | AL-10, AL-11, AL-22 — never fires: missing series, impossible PromQL, rule never loaded | `--check=selectors` + inventory; pint `promql/impossible`; online pint `promql/series` | **H** |
| 5 | AL-12, AL-21 — window vs scrape; Prometheus 3 breakage | `--check=windows,prom3` with the read version; `THR-OBS-RATE-WINDOW` | H (<2×), Hardening (2–4×) |
| 6 | AL-16, AL-17, AL-18 — NaN ratio, `absent` misuse, no dead-man's switch | pint `promql/nan`, `alerts/absent`; `--check=nan,absent,watchdog` | M–H |
| 7 | SY-01..SY-04 — cause pages, no ticket tier, mean latency, per-instance pages | `--check=design` | M |
| 8 | AM-01..AM-09 — routing, inhibition, timers, deprecated keys | amtool matrix; `--am=` | H / M / L |
| 9 | VM-01..VM-06 — Grafana and vendor no-data, recipients | pre-flight 3 + read | M–H |

### 1. `for` absent, too long, or `keep_firing_for` misuse (AL-01, AL-02, AL-09)

```
BAD:   - alert: OrdersFailing  expr: orders_failed_total > 100  (no for)   ·   for: 1h on a page   ·   keep_firing_for: 2h with for: 1h
GOOD:  for: 5m on a threshold page · no for on a Watchdog or a multiwindow burn rule · for of 2+ run cycles on batch staleness
```
**Read the code:** Is it a Watchdog or a burn rule whose short window debounces (precedents § 2; the row's expr has `and` across two windows)? Batch staleness set at two run cycles (§ 3)? A `predict_linear` page? Does `keep_firing_for` outlast the incident on a page? **Finding when** a page fires on one sample, or waits past `THR-OBS-ALERT.page_for_max` (30m) to fire. **Severity:** M page, L ticket. **Proof (V203):** promtool pair — a one-sample blip must stay silent, a sustained failure must fire within the page budget.

### 2. Severity, runbook, template labels, `$value` in labels (AL-03..AL-06)

```
BAD:   labels: { depth: "{{ $value }}" }   ·   sum by (job) (…) with summary "on {{ $labels.instance }}"   ·   a page with no runbook_url
GOOD:  $value in annotations only · the template reads labels the `by (…)` keeps · runbook_url on every page; summary on every alert
```
**Read the code:** Which vocabulary do the routes match on — `severity`, `priority`, `team` (read the AM config first)? Is a runbook injected at build time (a mixin `runbookURLPattern`)? Is the alert a ticket or info (precedents § 1: no runbook needed)? Does the server apply group labels (precedents § 41; a 2.x server rejects the file, § Measured)? **Finding when** a page has no runbook, an alert has no summary, a severity routes nowhere, a template renders empty, or `$value` sits in labels. **Severity:** L–M; H for `$value` (every new value is a new alert, so `for` never completes). **Proof (V203):** pint `alerts/annotation` / `alerts/template`, promtool `exp_annotations`.

### 3. The expression cannot express the condition (AL-07, AL-08, AL-13, AL-14, AL-15, AL-19, AL-20)

```
BAD:   orders_failed_total > 100 · rate(sum(x)[5m:1m]) · histogram_quantile(0.99, sum(rate(b[5m])) by (job)) · irate in a page · increase(x[1h]) == 3
GOOD:  increase(orders_failed_total[5m]) > 100 · sum(rate(x[5m])) · … by (job, le) · rate · round(increase(…)) >= 3
```
**Read the code:** Does a recording rule emit only bad series, so no comparison is needed? Is the counter compared through `changes()` / `resets()` on purpose? Native histograms (no `le`)? **Finding when** the expression is true when the system is healthy, never resolves, or cannot see a counter reset. **Severity:** M. **Proof (V204):** promtool — the healthy series must not fire, the failing one must.

### 4. Never fires: the series is missing, the PromQL impossible, or the rule never loaded (AL-10, AL-11, AL-22)

```
BAD:   http_request_duration_second_bucket (typo) · a rule file outside every rule_files glob · PrometheusRule release: kps vs ruleSelector release: monitoring
GOOD:  every selector resolves in the inventory (code, recording rules, exporter defaults) · every rule file matched · CR labels ⊇ ruleSelector.matchLabels
```
**Read the code:** Is the metric registered lazily, so it appears only after the first event (itself `metric-hygiene-scan` §2)? Is it an exporter default (`up`, `node_`, `kube_`, `probe_` — `exporter-default (unverified)` in the row: is that exporter deployed)? Is it an OTel name translated with unit and `_total` suffixes (precedents § 43, `translated [K?]`)? A client_golang name with a `Namespace` prefix (`suffix-only [K?]`)? Is the PrometheusRule in a namespace `ruleNamespaceSelector` covers? **Finding when** a page selector resolves in no inventory — **HIGH Unconfirmed** until `promtool query instant <url> 'count(<selector>)'` or online pint `promql/series` returns empty (precedents § 16: a promtool test with mocked series never proves a metric exists) — or the rule is never loaded (a two-ended static fact). **Severity:** H. **Proof (V203, V204):** the inventory diff plus the live `count()` (L), else `NO-DATA(prometheus)`; for AL-22, the glob or selector that misses.

### 5. Window under the scrape interval; Prometheus 3 breakage (AL-12, AL-21)

```
BAD:   rate(x{job="api"}[30s]) with api scraped every 30s · le="1" · [5m:5m] · holt_winters( — on a 3.x server
GOOD:  [1m]+ at 30s (≥ 2×, 4× recommended) · le="1.0" · [5m:1m] · double_exponential_smoothing with the feature flag
```
**Read the code:** Which scrape interval applies to this job (`prometheus.yml`, ServiceMonitor `interval`, Alloy)? Which major does the server run (§ Adapt)? **Finding when** the window is under `THR-OBS-RATE-WINDOW.min_multiple_of_scrape` (2×) — exactly 1× is empty on 3.x — or a 3.x-only breakage on a server proven to be 3.x (precedents § 45). **Severity:** H under 2×; 2–4× is Hardening (precedents § 6); on an unread version, Unconfirmed. **Proof (V204):** the promtool sustained-failure test on the server's major (§ Measured: `[30s]` → `[]`, `[1m]` fires).

### 6. NaN ratio, `absent` misuse, no dead-man's switch (AL-16, AL-17, AL-18)

```
BAD:   sum(rate(failed[5m])) / sum(rate(total[5m])) > 0.1 with no zero-traffic sibling · absent(up{job=~"api.*"}) with no for · no vector(1) Watchdog
GOOD:  a sibling `sum(rate(total[5m])) == 0` page for the same job · absent(up{job="api"}) with for: 5m · Watchdog → an external heartbeat receiver
```
**Read the code:** Does a sibling traffic-absent or zero-traffic rule exist for the same job or denominator metric, or does the SLO generator emit one (precedents § 5)? Does the Watchdog route to an external heartbeat (§8 matrix: `alertname=Watchdog`)? Is the evaluator managed (documented)? **Finding when** a total outage turns the ratio into NaN and nothing pages, `absent` fires on a restart or hides a missing target behind a regex, or no heartbeat proves the pipeline alive. **Severity:** M; H on a critical-path ratio page. **Proof (V204):** promtool total-outage test — `exp_alerts` must not be empty at zero traffic.

### 7. Alert design: cause pages, no ticket tier, mean latency, per-instance pages (SY-01..SY-04)

**Read the code:** Is the cause page definite and imminent — `predict_linear` disk-full within hours, certificate expiry before the next business day, quorum loss (precedents § 4)? Is the team one channel by design? Is the service a stateful singleton (per-instance is right)? Low traffic paging on one error is a design issue, not a rule bug (§ 15). **Finding when** a page fires on CPU, memory or a static disk threshold with no user-facing signal, every alert pages, a latency page uses `rate(_sum)/rate(_count)`, or N replicas give N pages. **Severity:** M (SY-03, SY-04: L). **Proof (V206):** the routes matrix for `severity=warning` / ticket sets; S for the rest.

### 8. Routing, inhibition, timers, deprecated keys (AM-01..AM-09)

```
BAD:   root receiver: dev-null (no *_configs) while pyrra emits severity=critical · inhibit equal: [cluster] that no rule emits · group_wait: 10m on a pager
GOOD:  every emitted {severity × team} proven by --verify.receivers · equal labels both sides carry · group_wait ≤ 5m, repeat ≥ 30m on a pager
```
**Read the code:** Which label sets do the rules actually emit (`--label-sets`, including group labels)? Is the null root intentional because every emitted set is proven elsewhere (precedents § 9)? Is `group_by: ['...']` on a self-deduping webhook (§ 8)? Deprecated `match` / `match_re` is Low, never bundled (§ 7). Inhibition and mute timing need a containerised Alertmanager (`amtool alert add` / `query`): without one they are `NO-DATA(alertmanager)`. **Finding when** an emitted page set reaches a null or dev receiver (H), an inhibit rule's `equal` labels are emitted by no rule so it mutes across every scope (H once proven live, M static), or timers after inheritance break `THR-OBS-ALERT` (M / L). **Proof (V206):** `amtool config routes test --verify.receivers=<expected> <labels>` exits 1; `check-config` clean.

### 9. Grafana-managed alerts and vendor monitors (VM-01..VM-06)

**Read the code:** Grafana `noDataState` / `execErrState: OK` on a page (VM-01), unless "keep last state" has a companion rule for datasource loss (precedents § 11). Datadog `notify_no_data` unset on a traffic or heartbeat monitor (VM-02; an error-count monitor is right, § 10), `message` with no `@` handle (VM-03). New Relic with no `expiration_duration`, or `fill_option = "last_value"` on an error rate (VM-04). Honeycomb trigger with no recipients, or an SLO with no burn alert (VM-05). Runbooks naming alerts no repo file defines (VM-06, L: export and diff). **Finding when** a signal that stops produces no alert in the tool that watches it. **Severity:** M–H. **Proof (V205):** the field check per monitor (S), an export diff (L).

## Proof

- **promtool fire / blip pair (V203, V204)**, in a copy, on the server's major. Each case states the correct behaviour, so a failure is the proof:

```yaml
rule_files: [../rules/api.yml]
evaluation_interval: 30s
tests:
  - interval: 30s                       # sustained failure: must fire
    input_series:
      - series: 'http_requests_total{job="api",code="503"}'
        values: '0+60x40'
    alert_rule_test:
      - eval_time: 15m
        alertname: ApiShortWindow
        exp_alerts: [{exp_labels: {severity: page, team: payments}, exp_annotations: {summary: 503 burst, runbook_url: "https://runbooks.example.internal/503"}}]
  - interval: 30s                       # one-sample blip: must stay silent
    input_series: [{series: 'orders_failed_total{job="api"}', values: '0 0 0 150 150 150'}]
    alert_rule_test: [{eval_time: 2m, alertname: OrdersFailing, exp_alerts: []}]
```

- **Total outage (AL-16):** every input series flat at 0; `exp_alerts` names the page that must fire. A test that passes on the unfixed rule proves nothing — rebuild it until it fails.
- **Routes matrix (V206):** `--verify.receivers` per emitted label set; exit 1 on mismatch.
- **Live series (L) for AL-10:** `count(<selector>) > 0` on the running server, only with a URL the user gave; else `NO-DATA(prometheus)` and the row stays HIGH Unconfirmed.
- A fix is accepted when the pair goes green on every rule of the group, the benign control stays silent, `rule-inventory.py` and pint print nothing for the touched rules, and `promtool check rules` exits 0. Never accepted: raising `for` past `THR-OBS-ALERT`, demoting a page to a ticket, deleting the rule or its test, `exp_alerts: []` added to make a test pass, a `# pint disable` comment, a route to `null`.

## Output

```
alert-rule-lint — Prometheus 3.5.0 (deploy/docker-compose.yml:3) · Alertmanager 0.28.1 · lanes: promtool 3.15.0, pint 0.89.2 (scratch .pint.hcl), amtool 0.34.1, rule-inventory.py · pint in CI: absent
Context: 7 rule files (5 plain, 1 CRD file with 2 docs, 1 Helm values) · rule_files: rules/*.yml · scrape 15s global, api 30s · inventory 12 names

Findings: 3 · Unconfirmed: 1

1. deploy/prometheus/rules/api.yml:82  ApiShortWindow                     [report-with-fix]   high
   §5 AL-12 — rate(…{job="api"}[30s]) with api scraped every 30s on Prometheus 3: the sustained-503 test gets [] (exactly 1× is empty).
   Proof: promtool test rules (3.15.0) — fails unfixed, passes with [1m]. Fix: [1m] (≥ 2×, THR-OBS-RATE-WINDOW).

2. deploy/alertmanager/routes.yml:2        root → dev-null                 [report-with-fix]   high
   §8 AM-01 — pyrra's ErrorBudgetBurn emits severity=critical and severity=warning; the routes match only page/ticket, so both resolve to dev-null.
   Proof: amtool config routes test --verify.receivers=pager severity=critical → exit 1. Fix: route on the generator's vocabulary (or set pyrra's severities), re-run the matrix.

3. deploy/prometheus/rules/api.yml:24  PaymentFailureRatio                [report-with-fix]   medium
   §6 AL-16 — ratio of rates with no zero-traffic sibling for payment_attempts_total: the total-outage test stays silent.
   Fix: a sibling `sum(rate(payment_attempts_total[5m])) == 0` page (for: 10m) for the same job.

4. deploy/prometheus/rules/api.yml:132  CheckoutLatency                    [report-flagged]    high
   §4 AL-10 — http_request_duration_second_bucket resolves in no inventory (code registers http_request_duration_seconds).
   Unproven link: the live series. Settling: promtool query instant <url> 'count(http_request_duration_second_bucket)'.

Verification: 34 candidates · 4 read → 3 findings · 1 unconfirmed · 30 Live, unreviewed (rule-inventory.py deploy --format=text) · 10 hardening

Class coverage:
  §1 for / keep_firing_for       Live, unreviewed (7 rows; pint rule/for 10 → 5 refuted: burn rules, precedents § 2)
  §2 severity / runbook / labels Live, unreviewed (6 rows; 10 ticket runbooks Hardening)
  §3 expression                  Live, unreviewed (3 rows)
  §4 never fires                 checked (4 rows → 1 unconfirmed; 3 rows Live, unreviewed) · live series NO-DATA(prometheus)
  §5 window / Prom 3             checked (2 rows → 1 finding; version read: 3.5.0)
  §6 NaN / absent / heartbeat    checked (3 rows → 1 finding; Watchdog present → heartbeat)
  §7 alert design                Live, unreviewed (4 rows)
  §8 routing                     checked (13 label sets; 3 reach dev-null → 1 finding) · inhibition NO-DATA(alertmanager)
  §9 vendor monitors             N/A (no Grafana-managed alerts, no monitor resources)
```

`[report-with-fix]`: the rule, the condition and a failing oracle are all present and the fix is in the rule's own source. `[report-flagged]`: one link is unproven (the live series, the server version, the deployed AM), named with its settling command. The coverage block lists **all nine** sections on every run: `checked (k → m)` only when the lane ran on present surfaces; `N/A (<reason>)` only when the repo has no such surface; `blocked (<reason>)` when a tool or grep could not run; `NO-DATA(<source>)` for an L-tier half; `Live, unreviewed` for rows not yet read.

## False positives / precedents

The verifier reads `precedents/observability.md` § 1–17 (alerts and routing), § 36–37 (verdict discipline), § 41–43 and § 45, § 53 (versions and tool exits). The ones this skill meets most:

- **A ticket or info alert without a runbook** (§ 1) and **no `for` on a Watchdog or multiwindow burn rule** (§ 2) — `rule-inventory.py` marks both; pint does not.
- **Burn factors** 14 / 7 / 2 / 1 (Pyrra) and the 3× 24h/2h ticket (Workbook final rule, sloth `google-30d`) are correct (§ 12, `THR-OBS-BURN`); the arithmetic is `slo-rule-scan`'s.
- **A NaN ratio with a sibling for the same job** (§ 5); **a window of 2–4× scrape** (§ 6); **integer `le` on a 2.x server** (§ 17).
- **A null root receiver** proven safe by a routes test for every emitted set (§ 9); **deprecated `match`** is Low (§ 7).
- **Generated rules** are judged at their spec; a defect in the rendered file is a drift finding (§ 42).
- **A selector naming no inventory entry** in a *proposed* fix is fabricated and Refuted (§ 37).

## When to run

- On any diff touching a rule file, a PrometheusRule, a Helm rules value, a mixin, an Alertmanager config, a Grafana alert or a monitor resource — `/obs-audit`'s dispatch signal.
- On every whole-repo `/obs-audit`, reporting all nine sections; before `alert-audit`, which consumes these rows.
- When `/alert-design` or `/add-telemetry` writes a rule: its gate is promtool + this skill's rows on the touched file.

## Halt conditions

- Do not report a high or critical row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 10. Under `/obs-audit` that happens in its verification phase; run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on any finding without the alert name, its `file:line`, the condition and the fix in the rule's source.
- Do not judge at file granularity: one row per rule. Never `rg -L` (it is `--follow`); never `--files-without-match` for a per-rule key.
- Do not report a Prometheus-3-only class without the server version read from a file; do not run promtool of a different major than the server and call the result proof.
- Do not call a selector "missing" from a promtool test with mocked series (precedents § 16), and do not promote AL-10 past Unconfirmed without a live `count()`.
- Never run `pint`, `mimirtool rules lint` or `lokitool rules lint` in the project tree; every tool runs on copies in `${TMPDIR}`. `git diff --exit-code` proves the tree untouched.
- Do not print "alerting is fine". Print the coverage block; a section whose lane did not run is `blocked`, never `checked`.
- Do not re-derive a class another skill owns (§ Boundaries). Cross-link it.

## Related

- `alert-audit` (this pack) — the behavioural L-tier half; reads this skill's rows and never re-greps rule files.
- `slo-rule-scan` (this pack) — burn arithmetic (`burn-check.py`) and regenerate-and-diff for generated rules.
- `@observability-reviewer` (this pack) — judges these rows in refute mode; `/obs-audit` dispatches, `/obs-fix` closes.
- `/alert-design`, `/add-telemetry` (this pack) — write rules; their alert gate is promtool plus these rows.
- `metric-hygiene-scan`, `telemetry-config-scan` (this pack) — the registrations the inventory reads, and dashboards.
- `secret-scan-method` (security pack, when installed), `k8s-api-version-scan` §2 (infrastructure pack, when installed), devops CI gates (when installed) — § Boundaries.
