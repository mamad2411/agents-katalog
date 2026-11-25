---
name: telemetry-config-scan
description: "Telemetry config lint: collector, Loki shippers, scrape selection, dashboards."
kind: skill
pack: observability
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: telemetry-config-scan

## Premise

Telemetry is lost between the process that emits it and the person who reads it, and the config that loses it validates clean. A collector whose `batch` runs before `memory_limiter` falls over under the burst it exists to absorb. An exporter with retries switched off drops every span the backend refuses for one second. A tail sampler with no trace-id load balancer in front decides on half a trace. A trace id promoted to a Loki label makes one stream per request, until the tenant's stream limit rejects every push during the incident. A `retention_period` with compactor retention off deletes nothing; Promtail has been end-of-life since 2026-03-02. A ServiceMonitor whose labels miss the Prometheus `serviceMonitorSelector` is never scraped, so every alert on it is silent. A dashboard with a hard-coded `[5m]` goes empty or spiky at the zoom on-call uses.

This skill finds those defects in the telemetry pipeline config a repo ships — OpenTelemetry Collector files (standalone, Helm values, Operator CRs), Alloy, Promtail, Fluent Bit and Vector, Loki, Prometheus scrape config with ServiceMonitor / PodMonitor selection, and Grafana dashboards — and proves each with a tool exit code or a two-ended key trace. It owns `/obs-audit`'s Pipeline (§1–§7) and Dashboards (§8) rows (`ownership.json` row `obs-pipeline`). `@observability-reviewer` (this pack) judges its rows.

**Every finding cites the config component (`file:line` + component id, label, key or panel) + the condition that occurs in production (a burst, a backend 503, a restart, one request per trace id, a zoom-out) + what the pipeline then does (drops, OOMs, decides on a partial trace, rejects the push, keeps forever, never scrapes, shows nothing) + the oracle that showed it + the fix in that file.** The unit is the component (one pipeline, one exporter, one label map, one monitor, one panel), grouped per config file: N defects in one file of one kind are one finding with N sites (precedents P4). A grep hit or a tool message is a candidate; "the pipeline looks fine" is never printed — the output is the class-coverage block (§ Output).

Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/observability.md`](../../../../snippets/precedents/observability.md). The oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Observability: *Pipeline validate + key diff* (**V208**, §1–§3, §5–§7) and, for Loki label cardinality, **V198** (§4). Budgets: `THR-OBS-CARDINALITY` (§4) and `THR-OBS-RATE-WINDOW` (§8), in `templates/governance/thresholds.json`.

## The rule

A candidate is a finding when all four hold (the protocol's gates as `precedents/observability.md` § Reading the seven gates applies them to pipeline config):

1. **Production loads the file** (gate 7). The compose file, Helm release, kustomization or manifest the deploy applies mounts or renders it. A laptop override, a `kind` values file or a dev compose file is precedents § 30: dismissed with that `file:line`.
2. **The condition occurs.** The backend can refuse or stall, the process restarts, traffic bursts, a trace spans more than one collector replica, ids are per-request, a board is zoomed past the window.
3. **Nothing already handles it.** A `memory_limiter` later in the same pipeline does not count; a load balancer tier in front, exporter-side batching, a persistent queue, a per-tenant stream limit with an alert on rejected pushes, structured metadata instead of a label, a provisioned datasource uid.
4. **The oracle fired, on the deployed version** (gate 3). A validator exited non-zero on a scratch copy, or the key diff / label map / selector comparison holds at both ends (`[report-flagged]` until a live check where the class is L-tier). Versions are read from image tags, chart pins or lockfiles, never assumed; an unpinned chart is printed as `unread (no --version)`.

## Boundaries

- **Secrets, PII or tokens written to logs, spans or a telemetry sink**, and a scrub processor's coverage → security `data-exposure-scan` § 6, when the security pack is installed; without it, `telemetry PII (owner pack not installed)`, listed, never graded (precedents P2). §1 here still reports a scrub processor that is *defined but in no pipeline* as an unused component, and routes the redaction verdict.
- **Proxy / ingress access-log format, request-id minting and upstream timing fields** → infrastructure `edge-reliability-scan` §15 (E6, E21), when that pack is installed; without it the hit is listed `edge access-log (owner pack infrastructure not installed)`, never graded here. This skill consumes the request id at the app; `log-signal-scan` (this pack) owns its correlation.
- **Collector and agent RBAC**: privilege breadth (cluster-wide `secrets`, wildcards) → security `iac-scan` § 3; missing or dangling wiring → infrastructure `k8s-wiring-scan` §6, each when installed. §7 reports only the telemetry blast radius as corroboration.
- **PrometheusRule / ServiceMonitor / PodMonitor schema** (kubeconform) → the infrastructure pack, when installed. §7 owns whether a monitor is *selected*.
- **Log, metric and trace retention cost in money** → finops `candidate-pricing` §0 (judged by `@cost-reviewer`), when installed. §6 owns retention that does not do what the config says, and carries the bytes-per-day arithmetic.
- **Metric label cardinality and DogStatsD tags (PL-08)** → `metric-hygiene-scan` §1. **SDK samplers and sampling before span metrics** → `trace-propagation-scan` §9–§10. **Loki / Mimir ruler rules** and **Grafana-managed alerts** → `alert-rule-lint` (this pack). **Prometheus retention vs an SLO window** → `slo-rule-scan` §6. **Probe filters in dashboard selectors** → `metric-hygiene-scan` §8.

## Adapt to the codebase — the pipeline lanes

Read every version from a file and print it in the header: collector, Alloy, Promtail, Loki, Prometheus, Grafana, Fluent Bit and Vector image tags; Helm chart pins (`--version`, `Chart.yaml` dependencies, helmfile); the Prometheus CR `spec.version`. A chart installed without `--version` renders whatever is current on the day of the run: say so, and render with the version the deploy pins when one exists.

| Lane | Surfaces | Tool (T) | No-tool lane |
|---|---|---|---|
| OTel Collector | standalone YAML, `opentelemetry-collector` chart `config:`, Operator `OpenTelemetryCollector` `spec.config` (object, or a string to extract) | otelcol-contrib validate | key diff + order (pre-flight 1) |
| Alloy | `*.alloy` / `*.river`, chart `alloy.configMap.content` (extract the block scalar) | alloy validate | label grep (pre-flight 4) |
| Promtail | `positions:` / `pipeline_stages:` configs, `grafana/promtail` image or chart | alloy validate with the promtail format; alloy convert | EOL is a static fact (§5) |
| Fluent Bit · Vector | `[OUTPUT] Name loki`, fluent-bit YAML; `sinks.*.type: loki` | fluent-bit dry-run; vector validate | label + retry greps |
| Loki | `loki.yaml`, `grafana/loki` chart values (render first: the chart writes the config) | loki -verify-config with env expansion | retention keys (pre-flight 6) |
| Prometheus | `prometheus.yml` scrape config; Prometheus CR and `kube-prometheus-stack` values; ServiceMonitor / PodMonitor / Probe / ScrapeConfig | promtool check config | selector vs labels (pre-flight 7) |
| Grafana | dashboard JSON, ConfigMap-embedded JSON (`grafana_dashboard` label), grafonnet output (render first) | dashboard-linter lint | `dash.py` flags (pre-flight 8) |

## Tool lane

Every tool runs in `${TMPDIR:-/tmp}` on **copies**, pinned to the versions this skill was measured with (2026-10-10, darwin-arm64 release archives checked against each release's published SHA-256 sums): **otelcol-contrib 0.162.0**, **alloy 1.20.1**, **loki / logcli / lokitool 3.7.8**, **promtool 3.15.0** (2.55.1 for a 2.x server — the binary decides what parses), **dashboard-linter 0.3.0**, **vector 0.59.0**. Downloads come from each project's GitHub release page into the scratch dir — never installed globally. **Fluent Bit 5.1.3** publishes no macOS binary: there, its cell prints `blocked (lane not installed: fluent-bit@5.1.3)` and the greps still run. A Helm chart is rendered with `helm template` (with `--kubeconfig` pointing at an empty scratch file and `HELM_CACHE_HOME` / `HELM_CONFIG_HOME` / `HELM_DATA_HOME` in the scratch dir — it never touches a cluster); the block scalar it writes (`config.yaml: |`) is extracted with the pre-flight's `blk.awk`.

Exit codes are read, never assumed (precedents § 53), and these were measured:

- **otelcol-contrib validate** exits 0 on a config with four unused components, `batch` first and `memory_limiter` second, retries off and a `debug` exporter at `detailed` — and prints nothing about them. It is the oracle for undefined references, removed components (the `logging` and `loki` exporters are gone from 0.162.0: exit 1) and syntax, never for §1's order or unused half. An `extensions::file_storage… directory must exist` error is the scratch machine, not the config: point the directory at a scratch path and re-run.
- **alloy validate** exits 1 with the offending `file:line` on a reference to an undefined component; `--config.format=promtail` validates a Promtail file by conversion.
- **loki -verify-config** exits 1 on `${VAR}` without `-config.expand-env=true` (pass the flag when the deploy passes it), exits 0 on `retention_period` with compactor retention off, and exits 1 on `retention_enabled: true` without `delete_request_store`. So §6's mismatch is a key check, and its fix carries both keys.
- **promtool check config** exits 1 on `scrape_timeout` greater than `scrape_interval`, with or without `--syntax-only`.
- **dashboard-linter** exits **0 without `--strict` while printing errors** (13 on the seeded board). With `--strict` it also exits 1 on a datasource-variable *label* warning, so its exit code is not the oracle: count the error rows of the rules §8 names. Its counter rule fires on `sum(orders_total)` but not on `orders_total{job="api"}`, and its rate-interval rule is silent on a board with no datasource template variable — `dash.py` (pre-flight 8) closes both gaps. The v2 rule id is `v2-required-fields-rule`.
- **vector validate --no-environment** checks config and VRL only; a label map is grep-only.
- **Rewrites in place:** `lokitool rules lint` (measured: it added `namespace:`; `--dry-run` and `rules check` leave the file), `mimirtool rules lint` without `-n`, `dashboard-linter lint --fix`.

dashboard-linter keeps only §8's rules through a scratch config (`-c "$T/dl.lint"`): `exclusions:` for `template-job-rule`, `template-instance-rule`, `target-job-rule`, `target-instance-rule`, `template-label-promql-rule`, `template-on-time-change-reload-rule`, `panel-title-description-rule` and `uneditable-dashboard` (style, and noise on multi-datasource boards), each with a `reason:`.

## Pre-flight

Run as **one** bash script from the repo root (`bash <<'EOF' … EOF`; macOS ships bash 3.2, so no `mapfile` or namerefs). Grep **N** feeds **§N**. Every `rg` names its path — `.` or an array guarded non-empty — and any rg exit 2 is a failed grep, never zero hits. Files-without-match is `--files-without-match`, never `rg -L` (`--follow`).

```bash
T="$(mktemp -d "${TMPDIR:-/tmp}/tcs.XXXXXX")"
cat > "$T/keydiff.awk" <<'AWK'
function ind(s){ match(s,/^ */); return RLENGTH }
function key(s){ sub(/^ *(- *)?/,"",s); sub(/:.*/,"",s); return s }
function items(s,  a,n,i){ sub(/^[^[]*\[/,"",s); sub(/\].*/,"",s); gsub(/[ "']/,"",s); n=split(s,a,","); for(i=1;i<=n;i++) if(a[i]!="") add(a[i]) }
function add(c){ if(lk=="extensions"){ ref["extensions",c]=1; return } ref[(lk=="processors")?"processors":(lk=="receivers"?"receivers|connectors":"exporters|connectors"),c]=1; if(lk=="processors") ord[pl]=ord[pl] (ord[pl]==""?"":",") c }
function flush(  n,a){ if(pl=="") return; n=split(ord[pl],a,","); if(n>0 && ord[pl]~/(^|,)memory_limiter/ && a[1]!~/^memory_limiter/) print F":"pln": pipeline "pl": memory_limiter not first ["ord[pl]"]"; if(n>0 && ord[pl]~/(^|,)batch(\/|,|$)/ && a[n]!~/^batch/) print F":"pln": pipeline "pl": batch not last ["ord[pl]"]"; if(ord[pl]!~/(^|,)memory_limiter/) print F":"pln": pipeline "pl": no memory_limiter (uncapped)"; pl="" }
FNR==NR { if($0 ~ /^ *service: *$/ && base=="") base=ind($0); next }
{ line=$0; sub(/[ \t]+#.*$/,"",line) }
line ~ /^ *(#|$)/ { next }
{ i=ind(line); k=key(line) }
base!="" && i==base { flush(); sect=""; svc=0; pi=-1; if(k ~ /^(receivers|processors|exporters|connectors|extensions)$/){ sect=k; ci=-1 } else if(k=="service") { svc=1; si=-1 }; next }
base!="" && i<base { flush(); sect=""; svc=0; next }
sect!="" { if(ci<0) ci=i; if(i==ci && line ~ /:/) def[sect,k]=FNR; next }
svc { if(si<0) si=i
      if(i==si){ flush(); pi=-1; lk=k; inpipes=(k=="pipelines"); if(k=="extensions" && line ~ /\[/) items(line); next }
      if(inpipes){ if(pi<0) pi=i; if(i==pi){ flush(); pl=k; pln=FNR; next }
                   if(line ~ /^ *(receivers|processors|exporters):/){ lk=k; if(line ~ /\[/) items(line); next }
                   if(line ~ /^ *- /){ c=line; sub(/^ *- */,"",c); gsub(/[ "']/,"",c); add(c) } }
      else if(lk=="extensions" && line ~ /^ *- /){ c=line; sub(/^ *- */,"",c); gsub(/[ "']/,"",c); add(c) } }
END{ flush(); if(base=="") exit
  for(x in def){ split(x,p,SUBSEP); s=p[1]; c=p[2]; used=0
    if(s=="receivers") used=ref["receivers|connectors",c]; else if(s=="exporters") used=ref["exporters|connectors",c]
    else if(s=="processors") used=ref["processors",c]; else if(s=="extensions") used=ref["extensions",c]
    else if(s=="connectors") used=(ref["receivers|connectors",c] && ref["exporters|connectors",c])
    if(!used) print F":"def[x]": "s" "c" defined, not referenced in service" } }
AWK
cat > "$T/blk.awk" <<'AWK'
function ind(s){ match(s,/^ */); return RLENGTH }
on && $0 !~ /^ *$/ && ind($0) <= ki { on=0 }
on { if(di<0 && $0 !~ /^ *$/) di=ind($0); print substr($0, di+1); next }
$0 ~ "^ *" K ": *[|>][-+]? *$" { on=1; ki=ind($0); di=-1 }
AWK
cat > "$T/dash.py" <<'PY'
import json, re, sys
LIT = re.compile(r'\[(?:\d+[smhdw]|\$__interval)\]'); CTR = re.compile(r'(?<![\w:])([A-Za-z_:][\w:]*_total)\b')
def walk(ps):
    for p in ps or []:
        if isinstance(p, dict): yield p; yield from walk(p.get('panels'))
for f in sys.argv[1:]:
    try: d = json.load(open(f))
    except Exception as e: print(f'{f}: not JSON ({e})'); continue
    d = d.get('dashboard', d) if isinstance(d, dict) else {}
    dsv = [v for v in (d.get('templating') or {}).get('list', []) if v.get('type') == 'datasource']
    print(f"{f}: {d.get('title')!r} ds-variable={'yes' if dsv else 'no'}")
    for p in walk(d.get('panels')):
        if p.get('type') in ('row', 'text', 'news', 'dashlist'): continue
        ds = p.get('datasource'); uid = ds.get('uid') if isinstance(ds, dict) else ds
        unit = ((p.get('fieldConfig') or {}).get('defaults') or {}).get('unit'); fl = set()
        if uid and not str(uid).startswith('$') and uid not in ('-- Grafana --', '-- Mixed --', '-- Dashboard --'): fl.add(f'ds-uid={uid}')
        if not unit: fl.add('no-unit')
        for t in p.get('targets') or []:
            e = t.get('expr') or ''
            fl.update('window=' + m.group(0) for m in LIT.finditer(e))
            fl.update('counter-no-rate=' + m.group(1) for m in CTR.finditer(e) if not re.search(r'\b(?:rate|irate|increase|resets|changes)\($', e[:m.start()].rstrip()))
        if fl: print(f"  {p.get('title')!r}: {' '.join(sorted(fl))}")
PY
CFG=(-g '*.{yml,yaml,json,alloy,river,conf,toml}' -g '!**/node_modules/**' -g '!**/{vendor,.git,.terraform,charts/*/charts,dist,build,coverage}/**'
     -g '!**/{test,tests,__tests__,spec,fixtures,__fixtures__,testdata,e2e,mocks}/**' -g '!**/{docs,ai,.claude}/**' -g '!**/{package,package-lock,composer,tsconfig}*.json' -g '!**/*.lock')
ID='(?:trace_?id|traceId|span_?id|spanId|request_?id|requestId|req_?id|reqId|user_?id|userId|session_?id|sessionId|tenant_?id|tenantId|order_?id|orderId|customer_?id|email|client_?ip|remote_?addr|ip|path|url|uri)'
# 0 versions (gate 3): image tags, chart installs (runbooks included: a helm line with no --version pins nothing), chart deps.
rg -n --pcre2 '(?:opentelemetry-collector(?:-contrib|-k8s)?|grafana/(?:loki|promtail|alloy|agent|grafana|tempo)|prom/prometheus|prometheus/prometheus|fluent/fluent-bit|timberio/vector)\S*:v?\d[\w.-]*' -g 'Dockerfile*' "${CFG[@]}" .
rg -n --pcre2 '\bhelm\s+(?:upgrade|install|template)\b.*\b(?:loki|promtail|alloy|tempo|opentelemetry-collector|kube-prometheus-stack|fluent-bit|vector)\b' -g '*.{sh,bash,mk,md,yml,yaml}' -g 'Makefile' -g '!**/node_modules/**' .
rg -n -A1 --pcre2 '^\s*-?\s*name:\s*(?:loki|promtail|alloy|tempo|opentelemetry-collector|kube-prometheus-stack|fluent-bit|vector)\s*$' -g 'Chart.yaml' -g 'helmfile*.y*ml' -g '!**/node_modules/**' .
# 1 collector configs (§1–§3, §7): service pipelines + exporters in one file; key diff and processor order per file.
COL=(); while IFS= read -r f; do rg -q --pcre2 '^\s*exporters:\s*$' "$f" && COL+=("$f"); done < <(rg -l --pcre2 '^\s*pipelines:\s*$' "${CFG[@]}" .)
echo "collector configs: ${#COL[@]}"; for f in "${COL[@]}"; do awk -v F="$f" -f "$T/keydiff.awk" "$f" "$f"; done
# 2 retry or queue switched off; queues (read for storage); fail-open shippers with no cap.
[ ${#COL[@]} -gt 0 ] && rg -n -H -U --pcre2 '^[ \t]*(?:retry_on_failure|sending_queue):[ \t]*(?:\{\s*enabled:\s*false|\n\s+enabled:\s*false)|^[ \t]*sending_queue:[ \t]*$' "${COL[@]}"
rg -n -i --pcre2 '^\s*(?:retry_limit\s*[:=]?\s*(?:no_limits|false|-1)\b|storage\.total_limit_size|mem_buf_limit)' -g '*.{conf,yaml,yml}' -g '!**/node_modules/**' .
# 3 tail sampling: the sampler, decision_wait, always_sample, and the trace-id load balancer in front.
[ ${#COL[@]} -gt 0 ] && rg -n -H --pcre2 '^\s*(?:tail_sampling(?:/\S+)?:|decision_wait:|type:\s*always_sample\b|load_?balancing(?:/\S+)?:|routing_key:)' "${COL[@]}"
rg -n --pcre2 '\botelcol\.(?:processor\.tail_sampling|exporter\.loadbalancing)\s+"' -g '*.{alloy,river,yaml,yml}' -g '!**/node_modules/**' .
# 4 Loki stream labels holding ids: Promtail/Vector label maps, Alloy stage.labels, Fluent Bit Labels.
rg -n -U --pcre2 "^[ \t]*-?[ \t]*labels:[ \t]*\n(?:[ \t]+[\w.-]+:.*\n)*?[ \t]+${ID}:" "${CFG[@]}" .
rg -n -U --pcre2 "\bstage\.labels\s*\{[^}]*?\bvalues\s*=\s*\{[^}]*?\b${ID}\s*=" -g '*.{alloy,river,yaml,yml}' -g '!**/node_modules/**' .
rg -n -i --pcre2 "^\s*(?:labels|label_keys)\s*[:=]?\s+.*\b${ID}\b" -g '*.conf' -g '*fluent*.y*ml' -g '!**/node_modules/**' .
# 5 shippers: Promtail (EOL) configs and images; Alloy sources, incl. Helm-embedded River.
rg -l --pcre2 '^\s*positions:\s*$|^\s*pipeline_stages:\s*$' "${CFG[@]}" .
rg -n --pcre2 '^\s*(?:image|repository|chart|-?\s*name):\s*\S*\bpromtail\b' -g '*.{yml,yaml,tf,toml}' -g 'Dockerfile*' -g 'Chart.yaml' -g '!**/node_modules/**' .
ALY=(); while IFS= read -r f; do ALY+=("$f"); done < <(rg --files -g '*.{alloy,river}' -g '!**/node_modules/**' . ; rg -l --pcre2 '^\s+(?:loki|otelcol|prometheus|discovery)\.[\w.]+\s+"[\w-]+"\s*\{' -g '*.{yml,yaml}' -g '!**/node_modules/**' .)
echo "alloy sources: ${#ALY[@]}"; [ ${#ALY[@]} -gt 0 ] && printf '  %s\n' "${ALY[@]}"
# 6 Loki retention: retention_period vs compactor retention_enabled + delete_request_store; unexpanded env.
LOK=(); while IFS= read -r f; do LOK+=("$f"); done < <(rg -l --pcre2 '^\s*(?:limits_config|compactor):\s*$' "${CFG[@]}" .)
[ ${#LOK[@]} -gt 0 ] && rg -n -H --pcre2 '^\s*(?:retention_period|retention_enabled|delete_request_store|retention_stream):|\$\{\w+' "${LOK[@]}"
# 7 debug exporter; monitor metadata labels vs the Prometheus selectors; telemetry DaemonSets (RBAC routed).
[ ${#COL[@]} -gt 0 ] && rg -n -H -U --pcre2 '^[ \t]*(?:debug|logging)(?:/\S+)?:\s*\n\s+(?:verbosity:\s*detailed|loglevel:\s*debug)' "${COL[@]}"
rg -n -A8 --pcre2 '^kind:\s*(?:ServiceMonitor|PodMonitor|Probe|ScrapeConfig)\s*$' -g '*.{yml,yaml}' -g '!**/node_modules/**' . | rg --pcre2 'kind:|-\s{2}(?:name|namespace):|-\s{2}labels:\s*\{|-\s{4}[\w./-]+:\s*\S'
rg -n -A2 --pcre2 '^\s*(?:serviceMonitorSelector|podMonitorSelector|probeSelector|scrapeConfigSelector|\w+NamespaceSelector|\w+SelectorNilUsesHelmValues):' -g '*.{yml,yaml}' -g '!**/node_modules/**' .
while IFS= read -r f; do rg -q --pcre2 'otelcol|alloy|promtail|fluent-bit|vector|grafana-agent' "$f" && echo "telemetry DaemonSet: $f"; done < <(rg -l --pcre2 '^kind:\s*DaemonSet\s*$|^\s*type:\s*daemonset\s*$' -g '*.{yml,yaml}' -g '!**/node_modules/**' .)
# 8 dashboards (i18n catalogs also carry a "panels" key): per-target flags for the no-tool lane.
DSH=(); while IFS= read -r f; do rg -q --pcre2 '"(?:targets|schemaVersion)"\s*:' "$f" && DSH+=("$f"); done < <(rg -l --pcre2 '"panels"\s*:' -g '*.json' -g '!**/node_modules/**' -g '!**/{dist,build,coverage,locales,locale,i18n,translations,messages,lang}/**' .)
echo "dashboards: ${#DSH[@]}"; [ ${#DSH[@]} -gt 0 ] && python3 -I "$T/dash.py" "${DSH[@]}"
echo "scratch: $T"
```

Then the tool lane, on copies (each line prints `blocked (…)` when its binary is absent; `$B` is the scratch bin dir):

```bash
printf 'exclusions:\n' > "$T/dl.lint"; for r in template-job-rule template-instance-rule target-job-rule target-instance-rule template-label-promql-rule \
  template-on-time-change-reload-rule panel-title-description-rule uneditable-dashboard; do printf '  %s: { reason: "style or multi-datasource noise" }\n' "$r" >> "$T/dl.lint"; done
mkdir -p "$T/tree" && tar cf - "${COL[@]}" "${ALY[@]}" "${LOK[@]}" "${DSH[@]}" 2>/dev/null | (cd "$T/tree" && tar xf -)
for f in "${COL[@]}"; do "$B/otelcol-contrib" validate --config="file:$T/tree/$f" >/dev/null 2>"$T/v.err"; echo "otelcol $f exit $? $(tail -1 "$T/v.err")"; done
for f in "${ALY[@]}"; do case "$f" in *.y*ml) awk -v K=content -f "$T/blk.awk" "$f" > "$T/tree/$f.alloy"; f="$f.alloy";; esac; "$B/alloy" validate "$T/tree/$f"; echo "alloy $f exit $?"; done
for f in "${LOK[@]}"; do "$B/loki" -config.file="$T/tree/$f" -verify-config -config.expand-env=true 2>&1 | tail -1; done   # chart values: render, then extract config.yaml
"$B/promtool" check config "$T/tree/${PROM_YML:?the prometheus.yml the deploy mounts}"; echo "promtool exit $?"   # copy it into the tree first
for f in "${DSH[@]}"; do echo "$f errors: $("$B/dashboard-linter" lint -c "$T/dl.lint" "$T/tree/$f" 2>&1 | rg -c '❌' - || echo 0)"; done   # error rows; the exit code is not the oracle
```

### Measured (2026-10-10)

| Tree | Result |
|---|---|
| `benchmarks/fixtures/*` (15 fixtures) | 0 lines, 0 rg errors: no fixture ships collector, shipper, Loki, scrape or dashboard config. `obs-defects` (eval item 23) is the fixture this skill scores on |
| Seeded sample: 5 collector files, Alloy ×2 + Helm-embedded, Promtail, Fluent Bit, Vector, Loki ×2 + chart values, `prometheus.yml`, Prometheus CR + 2 monitors, an agent DaemonSet, 3 dashboards, prod and dev compose | pre-flight 0.22 s, 89 lines. **All 23 seeded positives surface** in their § (§1 ×3, §2 ×3, §3 ×1 with three signals, §4 ×5 — Promtail, Alloy, Helm Alloy, Fluent Bit, Vector — §5 ×2, §6 ×1, §7 ×3, §8 ×5). Decoys that never print: `level` labels, an Alloy `stage.structured_metadata { trace_id }`, `stage.json` fields not promoted, an agent → sampler tier behind `loadbalancing` with `routing_key: traceID`, a correctly ordered agent, a clean board, a business board's `topk(… increase(…[$__range]))`. Decoys that print and clear at read: a dev collector's `debug` exporter and a dev Loki's retention (both mounted only by `docker-compose.dev.yml`, precedents § 30), a `sending_queue` with `storage:`, a chart-values Loki with compactor retention, a selected PodMonitor |
| Same sample, tools | otelcol-contrib: the defect-laden gateway exits 0; the edge file exits 1 (`logging` exporter removed); the sampler exits 1 only for the scratch machine's missing queue directory. alloy: 1 exit 1 (undefined component), 2 exit 0. loki: exit 1 without env expansion, 0 with. promtool: exit 1 (timeout > interval). dashboard-linter: 13 errors at exit 0 non-strict; with the scratch config, 4 error rows on the seeded board (datasource uid, unit, two windows) and 0 on the decoys, but it missed the counter seed (`orders_total{…}`), which `dash.py` reports. vector: exit 0 (labels are grep-only) |
| Real repository, read-only (a NestJS + Fastify monorepo; kube-prometheus-stack, Loki, Tempo and Alloy via Helm values under `deploy/`) | pre-flight 0.48 s, 51 lines, 0 rg errors. **One FP class found and fixed:** the dashboard grep matched two i18n catalogs with a `"panels"` key, and `dash.py` crashed on one — now i18n trees are excluded, a dashboard must carry `targets` or `schemaVersion`, and non-dict panels are skipped. Versions: every chart is installed from a runbook with no `--version` (7 lines) → **unread**; rendered for this run: loki 7.3.0, kube-prometheus-stack 92.3.0 (Prometheus v3.15.0). §1–§3: 0 collector configs (Tempo's `receivers:` has no `pipelines:`). §4: 2 Helm-embedded Alloy configs, `alloy validate` exit 0, labels `level` only — 0 findings. §6: the production render keeps 336h with compactor retention and a delete store (`-verify-config` exit 0); the laptop render has `retention_period: 24h` and no compactor retention → Refuted at gate 7 (precedents § 30). §7: the chart's `*SelectorNilUsesHelmValues: false` renders `serviceMonitorSelector: {}` / `podMonitorSelector: {}` (select all), so the PodMonitor is selected; 2 Alloy DaemonSets → RBAC routed. §8: dashboard-linter 23 errors at exit 0 — 17 datasource-uid rows are Hardening (the chart provisions the Prometheus datasource with uid `prometheus`), 6 unit rows → 3 unitless counts / factors refuted, 3 Low; 0 rate-interval rows (no datasource variable) while `dash.py` lists 13 literal windows → 1 Low finding for the board. `git status` clean after the run |
| `benchmarks/fixtures/obs-defects`, staged copy | 53 lines, 0.2 s, 17/17 seeds, 0 decoy hits. Greps 2, 3 and 7 printed bare `57:` lines on a one-file `COL` (no `-H`), and the multi-line greps could start on the blank line above the key (`^\s*`); both fixed (`-H`, `^[ \t]*`). The seeded sample prints the same 106 lines |

## The 3,000-hit path

1. **Intersect with what is loaded:** the compose files, Helm releases, kustomizations and manifests the deploy applies (gate 7). A config nothing mounts is listed as dead config, one line, not graded.
2. **Group** by config file and by generator (one chart values file, one jsonnet library, one dashboard generator): one template defect is one finding with N sites (P4).
3. **Rank:** gateway and node-agent collectors, the production log shipper and Loki first; then scrape selection for services with page-tier alerts; dashboards last.
4. **Read the top 30 groups.**
5. **Run the bulk oracle:** one validate pass per tool over the copied tree, and one dashboard-linter pass over every board, settle whole groups.
6. **Ledger the rest** as `Live, unreviewed (k files / n hits — <the pre-flight grep>)`. Never mark them `checked`.

## Scans for

| § | Classes | Tool / sketch | Default |
|---|---|---|---|
| 1 | PL-01 processor order; defined-but-unused component; config that does not load | otelcol-contrib validate + key diff | M |
| 2 | PL-02 exporter retry or queue off; fail-open forwarder with no cap | key read; Fluent Bit retry / storage keys | M; **H** uncapped on the only path |
| 3 | PL-03 tail sampling without a trace-id load balancer; short `decision_wait`; `always_sample` | key read | M |
| 4 | PL-04 Loki stream labels holding ids | label maps; logcli series analyze-labels (L) | M–H |
| 5 | PL-05 Promtail EOL; shipper config validity | alloy / vector / fluent-bit validators | M |
| 6 | PL-06 retention that does not delete; compactor off | loki -verify-config + key check | M |
| 7 | PL-07 `debug` exporter in production; agent blast radius; PL-09 monitor not selected; scrape config invalid | key read; selector vs labels; promtool check config | M–H |
| 8 | DB-01..DB-05 dashboards | dashboard-linter (scoped) + `dash.py` | L–M |

### 1. Processor order, unused components, a config that does not load (PL-01)

```
BAD:   processors: [batch, memory_limiter, tail_sampling]  ·  receivers: { zipkin: … } in no pipeline  ·  exporters: [logging] on 0.162.0
GOOD:  [memory_limiter, <droppers/samplers>, k8sattributes, <transformers>, batch]  ·  every defined component referenced  ·  debug exporter
```
**Read the code:** Is batching done exporter-side (`sending_queue` batcher), so a missing `batch` is right (research: the docs now prefer it)? Is the unused component a scrub processor (`attributes`, `transform`, `redaction`) — then the redaction gap is security's (§ Boundaries) and this row reports only that it is not wired? Is an unused `health_check` / `pprof` extension the liveness probe's target (it is not running)? For a chart's `config:`, does the chart merge defaults the values file does not show (render it)? **Finding when** `memory_limiter` is not first or `batch` sits before a processor that needs request context, a component the author meant to run is in no pipeline, or validate exits non-zero. **Severity:** M; H when the unloadable config is the production gateway. **Proof (V208):** validate exits 0/1 on the copy, and the key diff prints the order and the unused set — both ends cited.

### 2. Exporter retry or queue off; fail-open with no cap (PL-02)

```
BAD:   retry_on_failure: { enabled: false } · sending_queue: { enabled: false } · a logs pipeline with no memory_limiter · Retry_Limit no_limits, no storage.total_limit_size
GOOD:  retries and queue on (the default [K]) · sending_queue.storage: file_storage/… where loss on restart matters · memory_limiter on every pipeline · a capped buffer
```
**Read the code:** Is best-effort delivery a recorded decision (a debug exporter, a sampled copy)? Does the endpoint resolve from where the collector runs — a short service name (`http://loki:3100`) only resolves inside the same namespace, so a config copied between environments ships nothing while looking healthy? Is a queue without `storage` acceptable (loss on restart only)? Does the forwarder sit on every node or as the only gateway (precedents § 35)? **Finding when** a backend refusal or stall drops data that a retry would have kept, or the forwarder grows without a cap until it is OOM-killed. **Severity:** M; H — BLOCKER under `/obs-audit` — for an uncapped fail-open forwarder on the only production path (§ 35). A queue with no storage is Hardening. **Proof (V208):** the staged config: point the exporter at a scratch sink that answers 503 for 30 s, then 200, and count what arrives; S where nothing can run.

### 3. Tail sampling without trace-id load balancing (PL-03)

```
BAD:   tail_sampling on a 3-replica gateway fed by a round-robin Service · decision_wait: 2s on traces that last 10s · a policy of type always_sample
GOOD:  an agent tier with exporter loadbalancing, routing_key: traceID → the sampler tier · decision_wait above the p99 trace duration · a status_code ERROR policy
```
**Read the code:** How many replicas run the sampler (compose `replicas`, Deployment, HPA)? One replica needs no balancer (Hardening). What is the p99 trace duration (a span-duration metric, else `[report-flagged]`)? Policies are OR'ed: does `always_sample` make the others moot? Whether errors must be kept at all is `trace-propagation-scan` §10's requirement. **Finding when** spans of one trace can reach different sampler replicas, or the decision is taken before the trace ends. **Severity:** M. **Proof (V208):** S — the replica count, the absent balancer and the policy list, all cited; staged: send one trace's spans to two replicas and observe two decisions.

### 4. Loki stream labels holding ids (PL-04)

```
BAD:   pipeline_stages: - labels: { trace_id: }  ·  stage.labels { values = { user_id = "" } }  ·  Labels job=fb, request_id=$request_id  ·  labels: { request_id: "{{ request_id }}" }
GOOD:  stage.structured_metadata { values = { trace_id = "" } } · labels limited to level, namespace, app, cluster, job · ids stay in the line, parsed at query time
```
**Read the code:** How many distinct values can the label take per day (`THR-OBS-CARDINALITY.loki_dynamic_label_values`: tens)? A per-request id is unbounded; `tenant_id` and `path` need the arithmetic (precedents § 21). Is it promoted to a label, or only parsed (`stage.json` alone is not a label)? A high-cardinality field is right in the line or in structured metadata (§ 19); its *value* policy is security's. **Finding when** a production shipper promotes a per-request, per-user or per-tenant value to a stream label. **Severity:** H for per-request ids (each request a stream; pushes past the tenant stream limit are rejected, so logs drop in the incident); M for tenant or path. **Proof (V198):** L — `logcli series '{job="…"}' --analyze-labels` against the user-given Loki; without one, `NO-DATA(loki)` and the static label map stays `[report-flagged]` with the stream arithmetic written out.

### 5. Promtail end of life; shipper config validity (PL-05)

```
BAD:   image: grafana/promtail:3.0.0 · a promtail chart · an Alloy forward_to an undefined component
GOOD:  Alloy (alloy convert --source-format=promtail, then validate) · every shipper config validates on the deployed version
```
**Read the code:** Is the Promtail config live (mounted by the production compose or chart) or a leftover? Does the Alloy config come from chart values (extract `configMap.content`)? **Finding when** Promtail ships production logs (precedents § 51: on any version), or a validator exits non-zero. **Severity:** M. **Proof (V208, shippers):** alloy / vector / fluent-bit validator exits on the copy; for EOL, the image or chart line.

### 6. Retention that does not delete; compactor off (PL-06)

```
BAD:   limits_config.retention_period: 744h with compactor.retention_enabled: false (or absent)
GOOD:  compactor: { retention_enabled: true, delete_request_store: <store> } with the period the policy states
```
**Read the code:** Does the rendered config (not the values file) set compactor retention? Loki's retention docs (fetched 2026-10-10): without `retention_enabled`, logs live forever; `delete_request_store` is required when it is on; retention needs a 24h index period. Does a stated policy (privacy notice, audit mandate) set the period — log retention past it is a security / compliance question, audit logs below it are `audit-logging`'s (precedents § 31)? Is `-config.expand-env=true` passed where the config holds `${VAR}`? **Finding when** the period the config states is not enforced, or the config cannot load as deployed. **Severity:** M. **Proof (V208, Loki):** `-verify-config` on the rendered copy plus the key pair, both cited; the bytes-per-day × days arithmetic for finops.

### 7. `debug` exporter in production; agent blast radius; monitor not selected; scrape config invalid (PL-07, PL-09)

```
BAD:   exporters: [otlp, debug] with debug.verbosity: detailed in the gateway prod mounts · ServiceMonitor labels release: monitoring vs serviceMonitorSelector release: kps · scrape_timeout: 30s with scrape_interval: 10s
GOOD:  debug only in a dev override · monitor labels ⊇ the selector's matchLabels, in a namespace the namespace selector covers · timeout < interval
```
**Read the code:** Which config does production load (gate 7, § 30)? For selection, read the rendered Prometheus CR: an empty selector `{}` selects all, a null one selects none [K]; kube-prometheus-stack 92.3.0 renders `matchLabels: release: <release>` by default and `{}` when `*SelectorNilUsesHelmValues: false` (measured). Does the monitor's namespace fall under `*NamespaceSelector`? For a node-agent DaemonSet, what does a bad rollout touch (`updateStrategy`, every node at once) and how many API watches does it add (pods × nodes)? **Finding when** detailed debug output runs in production (cost, and every attribute in plain logs — the PII half routed), a monitor with page-tier alerts on its metrics is never scraped, or `promtool check config` exits non-zero. **Severity:** M; H for an unselected monitor whose metrics page-tier rules read (every such rule is never-fire, `alert-rule-lint` §4). RBAC breadth and wiring are routed (§ Boundaries). **Proof (V208):** S — the debug key in the prod-mounted file; the selector and the labels, both cited; promtool exit 1.

### 8. Dashboards (DB-01..DB-05)

```
BAD:   "uid": "P1809F7CD0C75ACF3" · rate(x[5m]) · rate(x[$__interval]) · no fieldConfig unit on a seconds panel · sum(orders_total{…}) with no rate
GOOD:  ${datasource} · rate(x[$__rate_interval]) · unit "s" / "percentunit" / "reqps" · sum(rate(orders_total[$__rate_interval])) · RED on every service board
```
**Read the code:** Is the board loaded (provisioning path, a ConfigMap with the sidecar label)? Is the fixed uid provisioned by the stack (kube-prometheus-stack's Prometheus datasource is uid `prometheus`) — then DB-03 is Hardening, a defect only on import elsewhere? Is the literal window a top-N over the range (`$__range`) or a recording-rule input (DB-04 decoys)? `$__rate_interval` is `max($__interval + scrape, 4 × scrape)`; a literal under `THR-OBS-RATE-WINDOW.min_multiple_of_scrape` is empty at any zoom. Is the panel a unitless count or factor (no unit is right)? Is it a service board (needs rate, errors, duration) or a business board (DB-01 decoy)? Does every selector resolve in the metric inventory (precedents § 37) — and is an integer `le` on a 3.x server empty (§ 45)? **Finding when** a loaded board's panel can show nothing, a wrong scale or a misleading counter on the server it reads. **Severity:** L; M for a service board missing RED or a window under 2× scrape. One finding per board (P4). **Proof (V208, dashboards):** dashboard-linter error rows (T, scoped config) plus `dash.py`'s flags.

## Proof

- **Validate on copies (V208, T):** each tool on the scratch tree, on the deployed major; the exit and the first error line are the row's evidence. A pass is never evidence for §1's order/unused half or §6's retention pair (§ Tool lane).
- **Key diff (V208, S):** the awk's lines plus the pipeline lines they name — both ends cited.
- **Staged config (V208):** for §2 and §3, run the copied collector against scratch sinks (a 503-then-200 HTTP sink; two sampler replicas) and count what arrives. Without a container runtime the row stays `[report-flagged]` with the staged test written out.
- **Live (L):** `logcli series --analyze-labels` (§4, V198), stream and bytes counts (§6), the TSDB's `up{job=…}` for §7 — only with a URL the user gave; else `NO-DATA(<source>)`, and the static half still reports.
- A fix is accepted when the validator exits 0 on the fixed copy, the key diff and `dash.py` print nothing for the touched component, and the staged test keeps what it lost. Never accepted: `debug` swapped for `logging`, a label demoted to a regex at query time while the shipper still labels, `retention_enabled` without `delete_request_store`, a `.lint` exclusion added to make a board pass, a selector widened to `{}` without reading what else it selects.

## Output

```
telemetry-config-scan — otelcol-contrib 0.162.0 (docker-compose.yml:3) · Loki 3.7.8 · Promtail 3.0.0 · Alloy v1.20.1 · Prometheus v3.5.0 · Grafana 12.1.0
Lanes: otelcol-contrib 0.162.0, alloy 1.20.1, loki 3.7.8, promtool 3.15.0, dashboard-linter 0.3.0 (scoped), vector 0.59.0 · fluent-bit blocked (lane not installed: fluent-bit@5.1.3)

Findings: 4 shown (+1 low: dashboards/api-red.json, §8) · Unconfirmed: 1

1. collector/gateway.yaml:58  pipeline traces                       [report-with-fix]   medium
   §1 PL-01 — processors [batch, memory_limiter, tail_sampling]: a burst is batched before the limiter can refuse it; zipkin,
   attributes/scrub, otlphttp/loki and the health_check extension are defined in no pipeline. validate exit 0 (it checks neither).
   Fix: [memory_limiter, tail_sampling, batch]; wire or delete the four (attributes/scrub → security data-exposure-scan § 6).

2. collector/gateway.yaml:41  otlphttp/vendor                       [report-with-fix]   high
   §2 PL-02 — retry_on_failure and sending_queue disabled on the only vendor exporter; the logs pipeline has no memory_limiter.
   Fix: retries + queue on (storage: file_storage/…), memory_limiter first in logs. Staged 503 sink: written out, not run.

3. logging/promtail-config.yaml:22  label trace_id                        [report-flagged]    high
   §4 PL-04 — trace_id promoted to a stream label: one stream per request. Unproven link: live stream count — NO-DATA(loki).
   Fix: stage.structured_metadata for trace_id, labels: level only; and §5 — Promtail is EOL (docker-compose.yml:20) → Alloy.

4. logging/loki-config.yaml:24  retention_period 744h                        [report-with-fix]   medium
   §6 PL-06 — compactor.retention_enabled: false (:28): the period is never enforced. -verify-config exit 0 as is;
   the fix needs delete_request_store too (exit 1 without it).

5. k8s/servicemonitor-api.yaml:7  ServiceMonitor api                [report-with-fix]   high
   §7 PL-09 — labels release: monitoring vs serviceMonitorSelector release: kps (k8s/prometheus.yaml:8): api is never scraped.

Verification: 31 candidates · 15 read → 5 findings · 1 unconfirmed · 5 hardening · 4 refuted (dev overrides, selected PodMonitor, sampler env) · 16 Live, unreviewed

Class coverage:
  §1 order / unused / loads      checked (5 files, 7 key-diff lines → 1 finding; validate 2 exit 1: edge finding, sampler env)
  §2 retry / queue / caps        checked (4 lines → 1 finding; 1 queue without storage Hardening)
  §3 tail sampling               checked (2 samplers → 1 finding; 1 behind loadbalancing)
  §4 Loki labels                 checked (5 label maps → 5 rows) · live streams NO-DATA(loki)
  §5 Promtail / shipper validity checked (1 Promtail + 3 Alloy validated) · fluent-bit blocked (lane not installed: fluent-bit@5.1.3)
  §6 retention                   checked (3 configs → 1 finding; dev override refuted, § 30)
  §7 debug / selection / scrape  checked (2 monitors → 1 finding; promtool exit 1 → 1 finding; 1 DaemonSet routed to RBAC owners)
  §8 dashboards                  checked (3 boards; dashboard-linter 4 error rows + dash.py 1 counter → 1 finding)
```

`[report-with-fix]`: the component, the condition and a fired oracle (or a two-ended static fact) are all present, and the fix is in that file. `[report-flagged]`: one link is unproven (a live stream count, a staged run, the deployed chart version), named with its settling command. The coverage block lists **all eight** sections on every run: `checked (k → m)` only when the lane ran on present surfaces; `N/A (<reason>)` only when the repo has no such surface; `blocked (<reason>)` when a tool or grep could not run; `NO-DATA(<source>)` for an L-tier half; `Live, unreviewed` for rows not yet read.

## False positives / precedents

The verifier reads `precedents/observability.md` § 19–21, § 30–31, § 35–37, § 45, § 51 and § 53, plus P2 and P4. The ones this skill meets most:

- **A dev, laptop or `kind` config** — a debug exporter, short retention, no compactor (§ 30): prove which file production mounts before reporting.
- **A high-cardinality field parsed but not labelled**, or kept in structured metadata (§ 19); `tenant_id` only with the arithmetic (§ 21).
- **A fixed datasource uid the stack provisions**, a unitless count, a top-N over `$__range`: Hardening or Refuted, never a finding.
- **A single-replica tail sampler** needs no balancer (Hardening). **Exporter-side batching** makes a missing `batch` processor right.
- **An uncapped agent is never "just ops"** (§ 35). **"The dashboard shows it"** — from which metric, and does it exist (§ 37)?

## When to run

- On any diff touching a collector, Alloy, Promtail, Fluent Bit, Vector, Loki, Prometheus scrape or monitor file, a telemetry chart's values, or a dashboard — `/obs-audit`'s dispatch signal.
- On every whole-repo `/obs-audit`, reporting all eight sections; before `alert-rule-lint` reads selection (an unselected monitor makes its rules never-fire).
- When `/add-telemetry`, `/add-metrics` or `/add-tracing` adds a pipeline, exporter or board: the touched file's validator plus these rows.

## Halt conditions

- Do not report a high or critical row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 10. Under `/obs-audit` that happens in its verification phase; run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on any finding without the component, its `file:line`, the condition and the fix in that file.
- Do not judge a config production does not load (gate 7); do not judge chart values without rendering them when the chart writes the config.
- Do not take an exit 0 from `otelcol validate`, `loki -verify-config` or non-strict `dashboard-linter` as a pass for the classes they do not check (§ Tool lane).
- Never run `lokitool rules lint`, `mimirtool rules lint`, `dashboard-linter --fix`, `alloy fmt --write` or a helm install in the project tree or against a cluster: copies in `${TMPDIR}`, `helm template` with an empty scratch kubeconfig. `git diff --exit-code` proves the tree untouched.
- Do not print "the pipeline is fine". Print the coverage block; a section whose lane did not run is `blocked`, never `checked`.
- Do not re-derive a class another skill or pack owns (§ Boundaries). Cross-link it.

## Related

- `@observability-reviewer` (this pack) judges these rows in refute mode; `/obs-audit` dispatches, `/obs-fix` closes.
- `alert-rule-lint` (selection makes rules fire or not), `trace-propagation-scan` (samplers), `metric-hygiene-scan` (metric labels, probe filters), `log-signal-scan` (what the shipper carries), `slo-rule-scan` (Prometheus retention) — this pack's neighbours.
- Security `data-exposure-scan` § 6 and `iac-scan` § 3, infrastructure `k8s-wiring-scan` §6, `k8s-api-version-scan` §2 and `edge-reliability-scan` §15, finops `@cost-reviewer` — each when installed (§ Boundaries).
