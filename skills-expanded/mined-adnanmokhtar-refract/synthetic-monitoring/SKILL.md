---
name: synthetic-monitoring
description: "Blackbox journey coverage: unprobed journeys, /health-only probes, single location, no probe-SLO, gated or dead probe alerts."
kind: skill
pack: observability
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: synthetic-monitoring

## Premise

White-box metrics say the server is healthy. They cannot say a user got through checkout. A synthetic probe drives the real journey from outside, on a schedule, and catches "everything green, nobody can log in": a bad static bundle, an expired certificate, a DNS or CDN fault, a downstream the app swallows. That coverage fails in five ways, and the config reads fine in all of them:
- **A critical journey has no probe.** Login, checkout and payment exist as routes; no probe config targets them.
- **The probe pings `/health`.** It proves the process is up, not that login works, and the journey is reported as covered.
- **One location.** A regional network fault looks like an outage, and an outage in that region looks like the ISP's problem.
- **No probe-SLO.** The probe runs and graphs; nothing burns, so nothing pages.
- **The probe cannot page.** Its alert is gated behind a white-box condition, notifies a channel nobody watches, or the probe is disabled.

This skill reads probe configs (k6, Checkly, blackbox exporter and the `Probe` CRD, Grafana Synthetic Monitoring, Datadog, New Relic, CloudWatch canaries, GCP uptime checks, Azure availability tests, uptime pingers, scheduled Playwright or k6 runs) against the journey list taken from the route table. It owns `/obs-audit`'s *Synthetic coverage* row. `@observability-reviewer` (this pack) judges its rows.

**Every finding cites:**
- the journey, by its route `<file:line>` (API) or page file (web);
- the probe config `<file:line>` that covers it, or the absence, shown by the pre-flight's target list;
- for §5, the alert rule or notify line that does or does not page;
- what on-call loses: no page, a page for someone else's network, a page that waits for a white-box signal.

A grep hit is a candidate. "We have synthetics" is never printed; the output is the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/observability.md`](../../../../snippets/precedents/observability.md). §5's oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Observability V204 (fire / blip pair) and V206 (routes matrix).

## The rule

A candidate is a finding when all four hold. These are `precedents/observability.md` § Reading the seven gates, applied to probes.

1. **The journey is real and reachable from outside.** A route a user drives: an internet-facing API route or a rendered page, not an admin-only or internal service, not a webhook receiver (that is a provider callback; its signal is processing alerts, not a probe).
2. **The probe config is what runs.** The Terraform root is applied, the Checkly project is deployed, the scrape job is in the config production Prometheus loads, the scheduled workflow exists. A k6 script with no scheduler is a script, not a probe.
3. **Nothing already covers it:** a vendor probe listed in the vendor's own inventory (most teams create probes in the UI, so absence from the repo is half a proof), a probe on the sibling API route the page calls, or an ADR that scopes the journey out.
4. **The oracle fired:** a two-ended static trace (the route on one end, the probe target list without it on the other) for §1–§4, and for §5 the promtool fire / blip pair or the routes matrix.

## Boundaries

- **Alert-rule hygiene** on a probe alert (`for`, runbook, severity, selector grounding, routing) belongs to `alert-rule-lint` (this pack). §5 reads its rows and asks only whether a probe failure pages *on its own*.
- **Burn arithmetic** on a probe-SLO belongs to `slo-rule-scan` §2 (this pack). §4 reports only that no probe-SLO exists.
- **The registry** `ai/runtime/slos.md` is written by `slo-audit` alone. A §4 finding routes to `/alert-design` Phase 1, which dispatches `slo-audit`; this skill never writes a target.
- **Readiness that lies** (`/readyz` answering 200 with its dependency down) is `metric-hygiene-scan` §7 (this pack). §2 asks only whether a probe *claims* a journey while hitting a health route.
- **Probe traffic polluting RED, traces and logs** is `metric-hygiene-scan` §8 (precedents § 18).
- **Real-user field measurement** (RUM, CWV) belongs to `web-vitals-field`, when the performance pack is installed; without it the row is listed `UNREVIEWED(field)` and never graded here.
- **The route table** comes from `/frontend-audit`'s F2 route map when the frontend pack is installed; without it, step 1's grep and a read of the router config stand in.
- **Liveness probes in manifests** (presence, shape, timings) belong to infrastructure `k8s-availability-scan` §2, when that pack is installed; without it they are listed, never graded here.

## Adapt to the codebase — the probe lanes

Read each tool's version from its lockfile, provider pin or image tag. A location field that is absent means the tool's default, which the row states with its source.

| Lane | Probe config | Journey assertion | Locations read from |
|---|---|---|---|
| **k6** | a script importing `k6/http`, or `k6/browser` (`import { browser } from 'k6/browser'`, scenario `browser.type: 'chromium'`) | `check()` on status and body | wherever the scheduler runs it: a CI cron is one location you did not choose |
| **Checkly** | `checkly.config.ts` (`defineConfig`, `checks.checkMatch`, e.g. `**/*.check.ts`) + `new ApiCheck` / `BrowserCheck` / `MultiStepCheck` | assertions, Playwright steps | `locations: [...]` in the config or on the check |
| **blackbox exporter** | a scrape job with `metrics_path: /probe`, `params: module: [http_2xx]`, relabel to `__param_target`; or `kind: Probe` (`prober`, `module`, `targets`) | `probe_success` | where the exporter runs: one in-cluster exporter is one location, and it is inside |
| **Grafana SM** | `grafana_synthetic_monitoring_check` (`target`, `probes` required, `settings { http \| multihttp \| browser \| scripted }`) | the settings block | `probes = [...]` |
| **Datadog** | `datadog_synthetics_test` (`type` `api` / `browser`, `request_definition.url`, `options_list.tick_every`) | assertions | `locations` (required) |
| **New Relic** | `newrelic_synthetics_*` monitors | the script | `locations_public` / `locations_private` |
| **CloudWatch** | `aws_synthetics_canary`, `AWS::Synthetics::Canary`, CDK `new synthetics.Canary(` | the canary script | one region per canary (`region`, else the provider's) |
| **GCP uptime** | `google_monitoring_uptime_check_config` (`http_check.path`, `period` default 300s) | status, content matcher | `selected_regions`; omitted means all regions |
| **Azure** | `azurerm_application_insights_standard_web_test` / `_web_test` | validation rules | `geo_locations` |
| **Uptime pingers** | `uptimerobot_monitor`, `pingdom_check`, `betteruptime_monitor` | status only | the vendor's |
| **Scheduled runner** | a cron workflow running `playwright test`, `k6 run`, `checkly test` | the suite | the CI runner's region |

An uptime pinger on the bare domain is real reachability coverage and never journey coverage. Credit it in the row and still report the journey.

## Pre-flight

Run as **one** bash script from the repo root (bash 3.2-safe). Grep **N** feeds **§N**; 0 is the probe inventory. Every `rg` names its path; any exit 2 is a failed grep, never zero hits. Files-without-match is `--files-without-match`, never `rg -L` (that is `--follow`).

```bash
T="$(mktemp -d "${TMPDIR:-/tmp}/synth.XXXXXX")"; RI=.claude/skills/alert-rule-lint/scripts/rule-inventory.py
X=(-g '!**/node_modules/**' -g '!**/{dist,build,out,target,vendor,.venv,venv,coverage,.next,.nuxt,.output,.terraform,.git}/**' -g '!**/{docs,ai,.claude}/**' -g '!*.{md,mdx,snap,lock}' -g '!**/*.min.*')
CODE=(-g '*.{ts,tsx,js,jsx,mjs,cjs,py,go,java,kt,cs,rb,php}' -g '!**/{test,tests,__tests__,spec,specs,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata,synthetics,__checks__,k6,load}/**' -g '!**/*.{spec,test,e2e,check}.*' -g '!**/*_test.go' -g '!**/test_*.py')
J='(?:log-?in|sign-?in|sign-?up|register|auth|session|checkout|cart|basket|pay|payment|billing|order|subscri|password|reset|otp|verify)'
# 0 probe-config inventory, one lane per line: k6 · Checkly · blackbox / Probe CRD · vendor and cloud resources · scheduled runners.
{ rg -l --pcre2 "from\s+['\"]k6(?:/[\w/-]+)?['\"]" -g '*.{js,mjs,cjs,ts}' "${X[@]}" . | sed 's/^/k6 /'
  rg -l --pcre2 "from\s+['\"]checkly(?:/constructs)?['\"]|\bnew\s+(?:ApiCheck|BrowserCheck|MultiStepCheck|UrlMonitor|TcpMonitor|CheckGroup(?:V2)?)\s*\(" -g '*.{ts,js,mjs,cjs}' "${X[@]}" . | sed 's/^/checkly /'
  rg -l --pcre2 '^\s*metrics_path:\s*["\x27]?/probe\b|^kind:\s*Probe\s*$|^\s*prober:\s*(?:http|tcp|icmp|dns|grpc)\b' -g '*.{yml,yaml,json,jsonnet,libsonnet}' "${X[@]}" . | sed 's/^/blackbox /'
  rg -l --pcre2 'resource\s+"(?:datadog_synthetics_test|aws_synthetics_canary|google_monitoring_uptime_check_config|azurerm_application_insights_(?:standard_)?web_test|newrelic_synthetics_\w+|grafana_synthetic_monitoring_check|checkly_check|uptimerobot_monitor|pingdom_check|betteruptime_monitor)"|AWS::Synthetics::Canary|\bnew\s+(?:synthetics\.)?Canary\s*\(' -g '*.{tf,json,yml,yaml,ts,js,py}' "${X[@]}" . | sed 's/^/vendor /'
  rg -l --hidden --pcre2 '^\s*-?\s*cron:|^\s*schedule:\s*$' -g '.github/workflows/*.{yml,yaml}' -g '.gitlab-ci.yml' -g '.circleci/config.yml' . | while IFS= read -r f; do rg -q --pcre2 '\bplaywright\s+test\b|\bk6\s+(?:run|cloud)\b|\bcheckly\s+(?:test|trigger)\b' "$f" && echo "scheduled $f"; done
} | tee "$T/lanes.txt"; PROBE_PATHS=(); while read -r _ f; do PROBE_PATHS+=("$f"); done < "$T/lanes.txt"; echo "probe files: ${#PROBE_PATHS[@]}"
# 1 the journey list: critical-keyword route declarations (API) and file-based pages (web). A journey is a read, never a grep row.
rg -n -i --pcre2 "@(?:Get|Post|Put|Patch|Delete|All|Controller)\(\s*['\"][^'\"]*${J}|\b(?:app|router|server|fastify|instance|r|g|e|mux|routes)\.(?i:get|post|put|patch|delete|all|route)\(\s*['\"][^'\"]*${J}|@(?:app|router|bp|api)\.(?:get|post|put|patch|delete|route)\(\s*['\"][^'\"]*${J}|@(?:Get|Post|Put|Patch|Delete|Request)Mapping\(\s*(?:value\s*=\s*)?['\"][^'\"]*${J}|\bHandle(?:Func)?\(\s*\"[^\"]*${J}" "${CODE[@]}" "${X[@]}" . | tee "$T/routes.txt"
rg --files -g '**/{app,pages,routes,views}/**/*.{tsx,jsx,ts,js,vue,svelte}' "${X[@]}" . | rg -i --pcre2 "/[^/]*${J}[^/]*/(?:page|index|\+page)\.\w+$|/(?:pages|routes|views|screens|app)/[^/]*${J}[^/]*\.(?:tsx|jsx|vue|svelte)$" | sed 's/^/page /' | tee -a "$T/routes.txt"; echo "journey candidates: $(wc -l < "$T/routes.txt" | tr -d ' ')"
if [ ${#PROBE_PATHS[@]} -eq 0 ]; then echo "§2–§5: N/A (no probe config in the repo) — every journey is a §1 candidate, [report-flagged] until the vendor inventory is read"; else
# 2 what each probe targets; 2b targets that are a health, status or bare-domain URL.
rg -n -o --pcre2 "https?://[^\s'\"\`)>,\]]+|\b(?:path|url|target)\s*[:=]\s*['\"][^'\"]+['\"]|page\.goto\(\s*['\"\`][^'\"\`]+" "${PROBE_PATHS[@]}" | tee "$T/targets.txt"
rg -n --pcre2 "(?:/(?:health|healthz|livez|readyz|ready|alive|ping|status|_health|actuator/health)\b[^/\s]*|https?://[^/\s'\"]+/?['\"]?|\bpath\s*=\s*\"/\")\s*['\"\]]?\s*$" "$T/targets.txt"
# 3 locations per probe (absent = the tool's default: read it).
rg -n --pcre2 '\blocations?\s*[:=]|\bprobes\s*=|\bselected_regions\b|\bgeo_locations?\b|\blocations_(?:public|private)\b|\bprivateLocations\s*:|^\s*region\s*=|\bdistribution\s*:' "${PROBE_PATHS[@]}"
# 4 probe-SLO: SLO specs, vendor SLO resources and registry rows that read a probe series.
rg -n --pcre2 '\bprobe_(?:success|duration_seconds|http_status_code)\b|resource\s+"(?:datadog_service_level_objective|grafana_slo|newrelic_service_level|google_monitoring_slo)"' -g '*.{yml,yaml,tf,jsonnet,libsonnet}' "${X[@]}" . ; [ -f ai/runtime/slos.md ] && rg -n -i 'probe|synthetic|journey' ai/runtime/slos.md
# 5 the alert path: probes disabled, muted or paused; where each probe notifies; rules on a probe series (gated when they also read a white-box metric).
rg -n --pcre2 '\bactivated\s*:\s*false\b|\bmuted\s*:\s*true\b|\bstatus\s*=\s*"paused"|\bstart_canary\s*=\s*false\b|\benabled\s*[:=]\s*false\b|\bis_paused\s*=\s*true\b' "${PROBE_PATHS[@]}"
rg -n --pcre2 '\balertChannels\s*:|\bnew\s+\w+AlertChannel\s*\(|\bmessage\s*=\s*"[^"]*@[\w-]+|\balert_policy\b|\bnotification_channels\b' "${PROBE_PATHS[@]}"
RULE_DIRS=(); while IFS= read -r d; do RULE_DIRS+=("$d"); done < <(rg -l --pcre2 'probe_success' -g '*.{yml,yaml}' "${X[@]}" . | xargs -n1 dirname 2>/dev/null | sort -u)
[ ${#RULE_DIRS[@]} -gt 0 ] && { if [ -f "$RI" ]; then python3 "$RI" "${RULE_DIRS[@]}" --format=json > "$T/rules.ndjson"; echo "rule-inventory exit $?"; python3 -c 'import json, sys
for l in open(sys.argv[1]):
    r = json.loads(l); m = r.get("metrics") or []
    if r.get("kind") != "alert" or not any(x.startswith("probe_") for x in m): continue
    gate = [x for x in m if not x.startswith("probe_")]
    print("%s:%s %s [%s] %s%s" % (r["file"], r["line"], r["name"], r.get("severity") or "-", " ".join(r["expr"].split()), "  <- also reads " + ",".join(gate) if gate else ""))' "$T/rules.ndjson"; else echo "probe alerts: blocked (rule-inventory.py not found — run alert-rule-lint)"; fi; }
fi; echo "scratch: $T"
```

Then the set-diff, which is a read: for each journey in `routes.txt`, find a target in `targets.txt` that drives it (the API path, or the page that calls it). A journey with none is a §1 candidate; a journey whose only target is a 2b line is a §2 candidate.

Two blind spots are structural, and the row says so:
- **Probes that live only in a vendor UI.** Without the vendor's synthetics inventory (an export or API listing the user pastes), §1 is `[report-flagged]`, and its Unconfirmed half is `NO-DATA(vendor synthetics inventory)`.
- **Hosts.** A probe on `https://api.example.com/auth/login` covers the `auth/login` route only if that host serves this repo's API. Read the deploy config or the ingress host before crediting it.

### Measured (2026-10-10)

| Tree | Hits that matter | Verdict |
|---|---|---|
| Seeded sample: NestJS controllers (`auth/login`, `auth/password/reset`, `checkout`, `orders/:id`, `health`), Next.js pages, a k6 login script run by a 10-minute cron workflow, a k6 load test against staging, Checkly config + one `ApiCheck`, a blackbox scrape job, a Datadog browser test, a GCP uptime check, one probe alert rule, a registry with no probe row; pre-flight 0.16 s | 7 probe files across 5 lanes · 7 journey candidates · 6 targets | Caught: `password/reset` unprobed (§1); the `login-probe` job targets `/health` (§2); Checkly `['us-east-1']`, Datadog `["aws:eu-west-1"]` and the CI-cron k6 run each from one location (§3); no probe-SLO in the registry or rules (§4); the Checkly orders check `activated: false`, the Datadog test notifying only `@slack-synthetics`, and `LoginProbeFailing` ANDed with an `http_requests_total` 5xx rate (§5). **Decoys, not findings:** the k6 ramping-VU load test against staging (a load test, not a probe); the Playwright `tests/e2e` spec run on pull requests (no schedule); the GCP uptime check with no `selected_regions` (all regions, per the provider docs); the `health` route (not a journey) |
| promtool 3.15.0 on the gated rule (§5 proof) | probe failing, 5xx rate 0 | `LoginProbeFailing` **silent** (`got: []`, exit 1). With the white-box clause removed: fires at the failure, silent at a one-sample blip, exit 0 |
| `benchmarks/fixtures/*` (15 trees) | 0 probe files on every tree · journey candidates 0–15 | §2–§5 `N/A (no probe config)` everywhere; §1 rows are `[report-flagged]`. The first journey grep counted client calls (`api.post('/me/cart/lines', …)`, `form.get('password')`): 8 of 13 hits on `a11y-states`, 2 of 7 on `frontend-correctness`. Route receivers are now named (`app`, `router`, `fastify`, `r`, …), and the page lane is held to `pages` / `routes` / `views` / `screens` / `app` directories. After the fix every hit is a route declaration or a routed page, e.g. `slow-marketplace` 15 (`@Post('login')`, `@Post('checkout')`, `CheckoutPage.tsx`) and `vuln-fullstack` 10, where `@Post('payments')` on a webhooks controller is refuted by rule 1 |

## The 3,000-hit path

1. **Intersect** the route list with what is reachable from outside: internet-facing services (ingress hosts, the public API's controllers, rendered pages). Internal and admin-only routes leave with one read.
2. **Group** routes into journeys: `auth/login` + `sign-in/page.tsx` + the session refresh are one login journey. Group probes by config file, Checkly group or Terraform module.
3. **Rank:** payment, checkout, login and signup first, then primary CRUD, then the rest.
4. **Read the top 30 journeys** against the target list.
5. **Run the bulk oracle:** the journey × target set-diff over the whole list, and one promtool fire / blip pass over every probe alert.
6. **Ledger the rest** as `Live, unreviewed (k journeys — the set-diff command)`. Never mark them `checked`.

## Scans for

| § | Class | Oracle | Default |
|---|---|---|---|
| 1 | Critical journey with no probe | journey × target set-diff (S); vendor inventory (L) | high on login, checkout, payment; medium otherwise |
| 2 | A `/health`-only or bare-domain probe claimed as journey coverage | target read (S) | medium; high when it is the only probe on a payment or auth journey |
| 3 | Single-location probe | location field, or the tool's default (S) | medium; low for an internal service |
| 4 | Probe with no probe-SLO | registry, SLO spec, rule reading `probe_success` (S) | medium; low when the probe is ticket-only by design |
| 5 | Probe failure cannot page: white-box-gated, disabled, or a dead route | promtool fire / blip (T, V204); routes matrix (T, V206) | high on a critical journey; medium otherwise |

### 1. Critical journey with no probe

```
BAD:   @Post('login') and app/checkout/page.tsx in the route list; no probe target drives either
       a k6 login script nothing schedules
GOOD:  a Checkly MultiStepCheck that logs in and reaches the order confirmation on a test account
```
**Read the code:**
- Is the journey internet-facing and user-driven, or internal, admin-only or a webhook?
- Does a probe drive the sibling API route the page calls? Then the API half is covered; the rendered half is a browser-probe question for the top journeys only.
- Does the vendor inventory (when given) hold a probe the repo does not?

**Finding when** a reachable critical journey has no probe in the repo and none in the vendor inventory. **Severity** per the table. **Proof:** the two-ended trace: the route `<file:line>` and the target list without it. Without the vendor inventory: `[report-flagged]`, settling input `the vendor's synthetics test list`.

### 2. A `/health`-only probe claimed as journey coverage

```
BAD:   job_name: login-probe  →  targets: ['https://api.example.com/health']
GOOD:  the health probe kept as a liveness check, and a separate probe that posts to /auth/login on a test account
```
**Read the code:** what does the probe's name, group or dashboard claim it covers? A health probe named for itself is correct (precedents § 18) and is no finding. **Finding when** a probe whose name, group or registry row claims a journey only reaches a health, status or bare-domain URL. **Proof:** the target line and the claim side by side (S).

### 3. Single-location probe

```
BAD:   checks: { locations: ['us-east-1'] }   ·   locations = ["aws:eu-west-1"]   ·   a CI cron running k6
GOOD:  two or more locations on different networks   ·   google_monitoring_uptime_check_config with no selected_regions (all regions)
```
**Read the code:** where does the probe actually run? An absent field is the tool's default, read from the lane table, never assumed. One in-cluster blackbox exporter is one location and sits inside the system, so it cannot see DNS, CDN or TLS faults. **Finding when** a probe on a critical journey runs from one location. **Proof:** the location line, or its absence plus the default's source (S).

### 4. Probe with no probe-SLO

```
BAD:   a login probe with no success-rate or latency SLO and no burn alert
GOOD:  a registry row (probe success ratio, owner, origin) and burn alerts on probe_success that slo-rule-scan §2 passes
```
**Read the code:** does the registry or an SLO spec name the probe's series? Is the probe ticket-only on purpose? **Finding when** a probe on a critical journey has no SLO and no burn alert. The fix routes to `/alert-design` Phase 1, which dispatches `slo-audit` to write the row (precedent: never invent the number here). **Proof:** S (the registry and rule files without it).

### 5. Probe failure cannot page

```
BAD:   probe_success{job="login-probe"} == 0 and on() sum(rate(http_requests_total{code=~"5.."}[5m])) > 1
       activated: false  ·  status = "paused"  ·  message = "… @slack-synthetics" on a critical journey with no pager handle
GOOD:  probe_success{job="login-probe"} == 0 for: 3m, severity page, routed to the on-call receiver
```
**Read the code:**
- Does the rule also read a white-box series (the pre-flight prints `also reads`)? A probe page gated on the service's own metrics is silent exactly when internals look fine.
- Is the probe disabled on purpose (a decommissioned journey, a maintenance window in code)?
- Does the notify target reach a pager? The routes matrix answers it for Alertmanager (`alert-rule-lint` §8); a vendor handle is read.

**Finding when** a failing probe on a critical journey produces no page. **Proof:** promtool fire / blip pair (V204 shape): `probe_success = 0` with the white-box series at 0 must fire, and a one-sample blip must not. Measured: the gated rule stayed silent (exit 1). For routing, `amtool config routes test --verify.receivers` with the probe alert's labels (V206).

## Proof

- **Two-ended static trace (S)** for §1–§4: the route or claim on one end, the target, location or registry line on the other.
- **promtool fire / blip (T, V204)** for §5, on the server's Prometheus major: a test that passes on the unfixed rule proves nothing; rebuild it until it fails.
- **Routes matrix (T, V206)** for §5 dead routes.
- **Vendor inventory (L)** for the §1 half the repo cannot show; without it `NO-DATA(vendor synthetics inventory)`.

A fix is accepted only when the probe drives the journey on a test account (never one that places real orders), runs from two or more locations, has a probe-SLO row written by `slo-audit`, and its alert passes the fire / blip pair and the routes matrix. Never accepted: deleting the health probe, gating the probe page on a white-box condition, or a probe-SLO number invented to close §4.

## Output

```
synthetic-monitoring — lanes: checkly 4.x (package.json), datadog provider 3.x (versions.tf), blackbox (prometheus.yml), k6 (CI cron)
Journeys: 6 critical (route list + read) · probes: 5 in repo · vendor inventory: NO-DATA(vendor synthetics inventory)

1. api/src/auth/auth.controller.ts:5  POST auth/password/reset             [report-flagged]    medium
   §1 — no probe target drives the reset journey. Settling: the vendor's synthetics test list.
2. deploy/monitoring/scrape-config.yml:9  job login-probe → /health           [report-with-fix]   high
   §2 — the only login probe reaches a health route. Fix: a probe that posts to /auth/login on a test account; keep /health.
3. deploy/prometheus/rules/synthetic.yml:4  LoginProbeFailing              [report-with-fix]   high
   §5 — ANDed with a 5xx rate: silent while internals are green. Proof: promtool fire test got [] (exit 1). Fix: drop the white-box clause.
4. checkly.config.ts:4  locations ['us-east-1']                          [report-with-fix]   medium
   §3 — every Checkly check runs from one location. Fix: a second location on another network.

Class coverage:
  §1 unprobed journey        checked (6 journeys → 1 flagged) · vendor half NO-DATA(vendor synthetics inventory)
  §2 health-only             checked (6 targets → 1 finding)
  §3 single location         checked (5 probes → 1 finding, 1 unconfirmed: the CI cron's runner)
  §4 no probe-SLO            checked (5 probes → 1 finding: registry has no probe row)
  §5 cannot page             checked (1 rule, 3 notify lines → 2 findings) · routes matrix blocked (lane not installed: amtool@0.34.1)
```

`[report-with-fix]`: both ends of the trace are read and the fix is in the probe, rule or notify config. `[report-flagged]`: one link is unproven (vendor inventory, the host a probe hits, a notify handle's target); the row names it and the settling input.

The coverage block lists **all five** §s on every run: `checked (k → m)` only when the § ran on present surfaces; `N/A (no probe config)` for §2–§5 when the repo has none (§1 still runs); `blocked (<reason>)`; `NO-DATA(<source>)` for the vendor half; `Live, unreviewed` for journeys not yet read.

## False positives / precedents

The verifier reads [`precedents/observability.md`](../../../../snippets/precedents/observability.md) § 15, § 18, § 36 and § 37. Those this skill meets most:
- **§ 18** Health endpoints excluded from tracing, logs and SLIs is right. A health probe kept as a liveness check is right. Only the *claim* that it covers a journey is §2.
- **§ 15** A low-traffic journey is where a probe earns its keep: synthetic traffic is the remedy precedents § 15 names.
- **§ 36** Whether a probe flaps, or whether a channel is watched, is behavioural. Without history or the pager export it is `NO-DATA(<source>)`.
- **§ 37** A probe-SLO selector proposed in a fix must name a series the probe really exports (`probe_success`, the vendor's metric), or it is Refuted.
- A load test (`ramping-vus`, a staging host) and an end-to-end suite run on pull requests are not probes.
- A browser probe is flakier than an API probe; one red run is not an outage. Read the probe-SLO's confirmation window before calling it noisy.
- An internal service with no rendered UI needs an API or TCP probe, not a browser probe.

## When to run

- A new critical journey ships: the probe is part of done.
- After an incident where internal metrics stayed green and users were blocked.
- On a diff touching a probe config, a probe alert, or a route on a critical journey.
- On every whole-repo `/obs-audit` (the *Synthetic coverage* row), and from `/alert-design` Phase 2 when the service owns a critical journey.

## Halt conditions

- **A high or critical row needs a separate refuter.** Do not report it as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 10. Run standalone, apply the protocol as a separate second pass and tag those rows `self-verified`. List the rest as Unconfirmed, Hardening, Pre-existing or Refuted; never drop them.
- Refuse to call a journey covered without a probe that drives it end to end; a health or domain ping does not count.
- Refuse to call a journey uncovered without the target list printed; absent the vendor inventory, the row is `[report-flagged]`.
- Do not print "we have synthetics". Print the coverage block.
- Do not write a probe-SLO target or invent one; `slo-audit` writes the registry.
- Do not propose gating a probe page behind a white-box condition.
- Do not re-grade what `alert-rule-lint`, `slo-rule-scan` or `metric-hygiene-scan` own (§ Boundaries).

## Related

- `alert-rule-lint` (this pack) — probe alert hygiene and the routes matrix; `slo-rule-scan` (this pack) — burn arithmetic on the probe-SLO; `slo-audit` (this pack) — writes the probe-SLO row.
- `metric-hygiene-scan` §7–§8 (this pack) — readiness semantics and probe traffic.
- `@observability-reviewer` judges these rows; `@sre-engineer` owns the probe-SLO policy; `@incident-responder` — a synthetic page is often the first signal.
- `web-vitals-field` (performance pack, when installed) — real-user field measurement, the passive complement.

## Sources

Fetched 2026-10-10: the Terraform `google_monitoring_uptime_check_config` page (omitted `selected_regions` runs from all regions; when set, at least 3 locations; `period` default 300s), `datadog_synthetics_test` (`locations` required; `type` api / browser / mobile / network; `tick_every` 30–604800 s for API tests), `grafana_synthetic_monitoring_check` (`probes` required; `frequency` default 60000), `aws_synthetics_canary` (`region` defaults to the provider's), the Checkly project-structure page (`locations`, `checkMatch`), the k6 browser page (`k6/browser`, `browser.type: 'chromium'`), the blackbox exporter README (`/probe`, `__param_target`, `probe_success`). Measured the same day: the sample above and promtool 3.15.0 (darwin-arm64, checked against the release `sha256sums.txt`). Paraphrased; no text is reproduced beyond identifiers.
