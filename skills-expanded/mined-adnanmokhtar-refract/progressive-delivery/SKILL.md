---
name: progressive-delivery
description: "Canary gates that cannot fail and flags that cannot be flipped: dead, stale, unsafe default, build-time."
kind: skill
pack: devops
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: progressive-delivery

## Premise

Two mechanisms let a team deploy without releasing: an automated canary gate, and a flag that can be flipped at runtime. Both fail silently, and both look present in a file review:
- an AnalysisTemplate whose `successCondition` is `result[0] >= 0` passes every canary, and so does a `failureLimit` larger than its `count`, a metric listed under `dryRun`, a query on a series that does not exist, or a query on the whole service instead of the canary;
- a flag whose SDK default is `true` turns the risky path **on** for everyone when the provider is down; a flag read once at boot, or inlined by the bundler (`VITE_*`, `NEXT_PUBLIC_*`), cannot be flipped without a deploy; a key the code reads but the registry never declares evaluates to its default forever.

No tool in the ledger reads these. Argo Rollouts and Flagger accept every one of them; the flag SDKs log a warning at most.

This skill owns `ownership.json` row `progressive-delivery` (§1–§9). `@deployment-engineer` (this pack) judges its rows.

**Every finding cites the line `<file:line>` + the object or key (Rollout, AnalysisTemplate metric, Canary, flag key) + the environment it reaches (the render, or the registry's environment block) + the platform or SDK fact it rests on (with its date and tag) + the oracle and its tier + the fix in the project's own syntax.** A pre-flight row is a candidate. "Rollouts are gated" or "flags look healthy" is never printed; the output is the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/devops.md`](../../../../snippets/precedents/devops.md) (deploy § 22–28; § 27 and § 28 are this skill's). The oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § DevOps, V232 (§5) and V233 (§4, §8, §9); §1–§3, §6 and §7 are static facts proven by a two-ended trace (tier S: the declaration and the read, or the two environment values).

## The rule

A candidate is a finding when all four hold (the seven gates as `precedents/devops.md` § Reading the seven gates applies them):

1. **It ships** (gates 1, 7). The Rollout or Canary is in the render of an environment a CD target or deploy unit applies; the flag is read by code a service root runs. A dev overlay, a per-PR preview (precedents § 24) or a test fixture is Hardening or Refuted.
2. **The event happens** (gate 2). A canary that should abort runs (a bad image, a 20 % error rate); the flag provider is unreachable, slow or missing the key; someone needs to flip the flag during an incident.
3. **No control already handles it** (gate 4). A second metric in the same template that can fail; a declared synthetic-load analysis (precedents § 28); a permanent operational flag (precedents § 27); a provider bootstrap that serves a safe value offline; an inverted flag name whose `true` is the old path.
4. **The oracle fired, or both ends are cited** (gate 6). V232 / V233 at their tier; without a run, the two ends (the template line and the render row; the SDK call and the registry entry) and the row is `[report-flagged]`.

## Boundaries

- **Which strategy** (canary, blue-green, rolling) and its rollback command → `@deployment-engineer`. **Watching one rollout** and handing a breach to `/rollback-deploy` → `monitor-deploy`. **A CI deploy with no rollout wait** → `deploy-safety-scan` §4; a GitOps CI that only commits manifests → precedents § 23 and `gitops-audit`.
- **Selector grounding** is observability's technique: `alert-rule-lint` §4 and its `scripts/rule-inventory.py --check=selectors`, when the observability pack is installed (pre-flight 5g runs it on every Prometheus query of §5). Without it, every query row prints `[report-flagged] selector not grounded (owner pack observability not installed)` and §5 never claims a series exists. The PromQL itself (windows, `rate` on a gauge) is not judged here.
- **The Rollout's pod template** (replicas, PDB, probes, resources) → infrastructure `k8s-availability-scan` (it reads the Argo Rollout template), **the GitOps spec** → infrastructure `k8s-render-scan` §4, each when installed; without it, `N/A (owner pack infrastructure not installed)`.
- **A contract migration shipped under a canary** (old and new pods share one schema) → database `migration-safety` §4 when installed, and `deploy-safety-scan` §1d.
- **Config that is not a flag** (a URL, a key) declared per environment → `deploy-safety-scan` §6. **A server image built per environment** → `release-integrity-scan` §4. **A flag SDK key committed in a file** → security `secret-scan-method` when installed.

## Adapt to the codebase — the lanes

Discover every surface (pre-flight 0a, 1); never assume `k8s/`, `flags.yaml` or `src/`. Print the lanes you ran in the header.

| Canary lane | Object | Gate field this skill reads | Never-fails shape |
|---|---|---|---|
| **Argo Rollouts** (v1.10.0 [R]) | `Rollout` + `AnalysisTemplate` / `ClusterAnalysisTemplate` | `strategy.canary.analysis` or an `- analysis:` step; blue-green `prePromotionAnalysis`; per metric `successCondition`, `failureCondition`, `count`, `failureLimit`, `inconclusiveLimit`, `spec.dryRun` | `result[0] >= 0`; no condition at all (evaluates Successful [K]); `failureLimit ≥ count`; `dryRun`; blue-green with `autoPromotionEnabled` left at its default `true` and no `prePromotionAnalysis` [K] |
| **Flagger** (v1.45.0 [R]) | `Canary` + `MetricTemplate` | `analysis.metrics[]`, `thresholdRange`, `threshold`, `skipAnalysis` | `metrics: []` (health checks only [R]); `thresholdRange.min: 0` on a success rate; `skipAnalysis: true` promotes without analysis [K] |
| **Spinnaker / Kayenta** | pipeline JSON stage `kayentaCanary` | `scoreThresholds.marginal`, `.pass` | `marginal: 0` never fails a score [K?]; read-only lane |
| **None** | plain Deployment, rolling | — | §5 prints `N/A (no progressive-delivery object)` |

| Flag lane | Call the pre-flight reads | Default on provider outage or a missing key | Flip without a deploy |
|---|---|---|---|
| **OpenFeature** (spec v0.9.0 [R]) | `getBooleanValue('k', <default>)`, `get*Details` | the default argument [K] | yes (provider) |
| **LaunchDarkly** | `variation('k', ctx, <default>)`, `boolVariation`, Go `BoolVariation` | the default argument [K] | yes |
| **Unleash** | `isEnabled('k', ctx, fallback)`, Python `is_enabled(…, fallback_function=…)` | the fallback [K] | yes |
| **GrowthBook · ConfigCat · Flagsmith · Split** | `isOn`, `getFeatureValue`, `getValue(Async)`, `hasFeature`, `getTreatment` on a flag client | the default argument [K?] | yes |
| **Config file** (flagd, `flags.yaml`) | the registry keys × the SDK keys | the SDK's default | yes, when a provider serves the file at runtime; no, when the app reads it at boot |
| **Environment variable** (`FEATURE_*`, `*_ENABLED`) | `process.env.X`, `os.environ`, `os.Getenv` | whatever the parse gives an unset var | **no**: a change is a restart or a rollout |
| **Build-time public env** (`VITE_*`, `NEXT_PUBLIC_*`, `REACT_APP_*`, `EXPO_PUBLIC_*`) | `import.meta.env.X`, `process.env.X` in client code; `--build-arg` | inlined at build | **no**: a rebuild and a deploy |

## Tool lane and ledger

| Lane | Command | Trap that makes a clean result false |
|---|---|---|
| Render | infrastructure `render.sh` when installed; else `kubectl --kubeconfig=<scratch> kustomize <dir>` and `helm template` into `$SCAN` (offline; a remote base is skipped as `blocked (remote base)`) | A failed render makes that environment's §5 rows `blocked (render failed: <dir>)`; an overlay that patches `failureLimit` exists only in the render |
| Grounding | `python3 -B .claude/skills/alert-rule-lint/scripts/rule-inventory.py <queries> <recording-rule files> --check=selectors --inventory=<names> --format=text --all` (observability pack) | Run **without** `--inventory` it exits 0 and hides the `blocked (no --inventory)` note: always pass the inventory. An inventory of 0 names makes every selector UNGROUNDED: read the count first |
| Registry | the repo's flag files; a SaaS registry (LaunchDarkly, Unleash server) only through its API with a token the user names | No file and no API → §1–§3 and §6 registry side `UNREADABLE (registry not in repo)`, never "no dead flags" |
| Age | `git log --diff-filter=A -S<key> -- <registry>` | A shallow clone dates every key to the clone: say so |
| Live (L) | `kubectl argo rollouts get rollout <r> --kubeconfig=<scratch>` on a throwaway cluster | Never the default context: no scratch cluster → `NO-DATA(rollout)` with the command written out |

## Pre-flight

Run as **one** script from the repo root (shell state does not survive between tool calls; bash 3.2 and zsh print the same rows). Grep **N** feeds **§N**; 0a/0b are the inventory and the render. Every `rg` names its path; an rg exit 2 is a failed grep, never zero hits. The include globs come **before** the exclusion array: in ripgrep the later glob wins, so `-g '*.ts'` after `-g '!**/*.spec.*'` would read the specs again (measured below). Nothing is written in the repo: renders, sets and the scratch rule file go to `$SCAN`.

```bash
X=(--hidden -g '!.git/**' -g '!**/node_modules/**' -g '!**/{dist,build,out,target,vendor,.venv,venv,__pycache__,coverage,.next,.nuxt,.output,.turbo,generated}/**'
   -g '!**/{test,tests,__tests__,spec,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata,examples}/**' -g '!**/*.{spec,test,e2e-spec,stories}.*' -g '!**/*_test.go' -g '!**/test_*.py'
   -g '!**/{docs,ai,.claude}/**' -g '!*.{md,mdx,snap,lock,svg,map}' -g '!**/{locales,i18n,migrations}/**')
CODE=(-g '*.{ts,tsx,js,jsx,mjs,cjs,vue,svelte,astro,py,go,rb,erb,java,kt,cs,php,ex,exs,rs}' -g '!*.d.ts')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(#|//|\*|/\*)')
SCAN="${SCAN:-$(mktemp -d "${TMPDIR:-/tmp}/delivery.XXXXXX")}"; echo "SCAN=$SCAN"
RENDERS() { find "$SCAN" -maxdepth 1 -name 'render-*.yaml' | sort; }
# Flag SDK calls whose first argument is the key; generic method names count only on a flag-ish receiver.
CALL="(?:\bget(?:Boolean|String|Number|Object)(?:Value|Details)|\b(?:bool|string|int|float|json)Variation(?:Detail)?|\b(?:Bool|String|Int|Float|JSON)Variation(?:Detail)?|\bget_(?:boolean|string|integer|float|object)_value|\bis_enabled|\bisOn|\bgetFeatureValue|\bevalFeature|\bhasFeature|\b\w*(?i:flag|feature|toggle|unleash|launchdarkly|ldclient|ld|openfeature|growthbook|configcat|split)\w*\s*\.\s*(?:variation(?:Detail)?|isEnabled|IsEnabled|getValue(?:Async)?|getTreatment))\s*\(\s*['\"\`]([\w.:/-]+)['\"\`]"
ENVF='\b((?:FEATURE|FF|FLAG|TOGGLE|ENABLE|DISABLE|KILL)_[A-Z0-9_]+|[A-Z][A-Z0-9_]*_(?:ENABLED|DISABLED|FLAG|FEATURE|KILLSWITCH))\b'
PUB='\b((?:NEXT_PUBLIC|VITE|REACT_APP|EXPO_PUBLIC|NUXT_PUBLIC|GATSBY|PUBLIC)_\w*(?:FLAG|FEATURE|ENABLE|DISABLE|TOGGLE|KILL)\w*)\b'
echo '# 0a delivery objects (Rollout, AnalysisTemplate, Flagger Canary/MetricTemplate) and Spinnaker/Kayenta stages — discovered, never a guessed dir'
rg -l --pcre2 -g '*.{yml,yaml,tpl}' "${X[@]}" '^\s*kind:\s*(Rollout|AnalysisTemplate|ClusterAnalysisTemplate|Canary|MetricTemplate)\s*$' . | sort > "$SCAN/delivery.txt"; cat "$SCAN/delivery.txt"
rg -l --pcre2 -g '*.{json,yml,yaml}' "${X[@]}" '\bkayentaCanary\b' . | while IFS= read -r f; do rg -n -H --pcre2 '\bkayentaCanary\b|"?(marginal|pass)"?\s*:\s*"?\d+' "$f"; done
echo '# 0b render (offline, isolated kubeconfig): reuse a render already in $SCAN or infrastructure render.sh; else kubectl kustomize / helm template'
if [ -z "$(RENDERS)" ] && [ -s "$SCAN/delivery.txt" ]; then RS=.claude/skills/k8s-render-scan/scripts/render.sh; : > "$SCAN/none.kubeconfig"
  if [ -f "$RS" ]; then bash "$RS" . --out="$SCAN" --quiet; echo "render.sh exit=$?"; else
    rg --files -g '**/kustomization.{yml,yaml}' "${X[@]}" . | sed 's|/[^/]*$||' | while IFS= read -r d; do
      rg -q --pcre2 '^\s*-\s*(https?://|github\.com/|git@)|\?ref=' "$d" -g 'kustomization.{yml,yaml}' && { echo "blocked (remote base): $d"; continue; }
      KUBECONFIG="$SCAN/none.kubeconfig" kubectl --kubeconfig="$SCAN/none.kubeconfig" kustomize "$d" > "$SCAN/render-$(echo "$d" | tr '/.' '__').yaml" 2>>"$SCAN/render.err" || echo "render FAILED: $d"; done
    rg --files -g '**/Chart.yaml' "${X[@]}" . | sed 's|/[^/]*$||' | while IFS= read -r d; do
      KUBECONFIG="$SCAN/none.kubeconfig" helm template x "$d" > "$SCAN/render-$(echo "$d" | tr '/.' '__').yaml" 2>>"$SCAN/render.err" || echo "render FAILED: $d"; done; fi; fi
RENDERS | sed 's|.*/||'
echo '# 5 canary gate rows: source (cited) and render (applied); render-only rows are overlay or values changes'
printf 'groups:\n- name: canary-analysis\n  rules:\n' > "$SCAN/analysis-rules.yaml"
GATE="$SCAN/gate.awk"; cat > "$GATE" <<'AWK'
function ind(t) { match(t, /^ */); return RLENGTH }
function val(t) { sub(/^[^:]*:[ \t]*/, "", t); sub(/[ \t]+#.*$/, "", t); gsub(/^["']|["']$/, "", t); return t }
function rule(nm, ln, e) { if (R == "" || pv != "prometheus" || e == "") return; gsub(/\{\{[^}]*\}\}/, "1m", e); gsub(/\n/, "\n      ", e)
  printf "  - alert: \"%s:%d:%s\"\n    expr: |\n      %s\n", FILENAME, ln, nm, e >> R }
function emit_m(  c, sco) { if (mn == "") return; c = ""
  if (sc ~ /(>=|=>)[ \t]*0(\.0*)?[ \t]*$/ || fc ~ /<[ \t]*0(\.0*)?[ \t]*$/) c = c " NEVER-FAILS"
  if (sc == "" && fc == "" && pv != "job") c = c " NO-CONDITION"
  if (cnt ~ /^[0-9]+$/ && fl ~ /^[0-9]+$/ && fl + 0 >= cnt + 0) c = c " LIMIT>=COUNT"
  if (sc != "" && fc != "" && il == "") c = c " NO-INCONCLUSIVE-LIMIT"
  if ((mn in dry) || dryall) c = c " DRYRUN"
  if (q ~ /or[ \t]+vector\([ \t]*0[ \t]*\)|scalar\(/) c = c " ZERO-FALLBACK"
  sco = (q ~ /rollouts[-_]pod[-_]template[-_]hash/) ? "hash" : (q ~ /\{\{ *args\./) ? "args" : (q == "" ? "-" : "no")
  if (sco == "no") c = c " UNSCOPED"
  printf "%s:%d: %s %s metric=%s provider=%s count=%s failureLimit=%s inconclusiveLimit=%s success=[%s] failure=[%s] scope=%s ->%s\n", FILENAME, ml, k, n, mn, (pv == "" ? "?" : pv), (cnt == "" ? "-" : cnt), (fl == "" ? "0" : fl), (il == "" ? "-" : il), sc, fc, sco, (c == "" ? " ok" : c)
  rule(mn, ml, q); mn = ""; sc = ""; fc = ""; cnt = ""; fl = ""; il = ""; pv = ""; q = "" }
function flush(  c) { emit_m()
  if (k == "Rollout") { c = ""
    if (strat == "canary" && sw > 0 && !an) c = " NO-ANALYSIS"
    if (strat == "blueGreen" && ap != "false" && !pre) c = " BG-AUTO-PROMOTE"
    printf "%s:%d: Rollout %s strategy=%s setWeight=%d analysis=%s autoPromotion=%s prePromotion=%s templates=%s ->%s\n", FILENAME, dl, n, (strat == "" ? "?" : strat), sw, (an ? "yes" : "no"), (ap == "" ? "default" : ap), (pre ? "yes" : "no"), (refs == "" ? "-" : substr(refs, 2)), (c == "" ? " ok" : c) }
  if (k == "Canary" && api ~ /flagger/) { c = ""; if (skip) c = c " SKIP-ANALYSIS"; if (nm <= 0) c = c " NO-METRICS"
    printf "%s:%d: Canary %s metrics=%s threshold=%s interval=%s skipAnalysis=%s ->%s%s\n", FILENAME, dl, n, (nm < 0 ? "absent" : nm), (th == "" ? "-" : th), (iv == "" ? "-" : iv), (skip ? "true" : "false"), (c == "" && fm == "" ? " ok" : c), fm }
  if (k == "MetricTemplate" && api ~ /flagger/) { c = (q ~ /\{\{ *target *\}\}/) ? "target" : "no"
    printf "%s:%d: MetricTemplate %s provider=%s scope=%s ->%s\n", FILENAME, dl, n, pv, c, (c == "no" ? " UNSCOPED" : " ok"); rule(n, dl, q) }
  k = ""; n = ""; api = ""; strat = ""; sw = 0; an = 0; ap = ""; pre = 0; refs = ""; skip = 0; nm = -1; th = ""; iv = ""; fm = ""
  split("", dry); dryall = 0; indry = 0; inm = 0; inq = 0; q = ""; pv = "" }
FNR == 1 { if (NR > 1) flush(); k = ""; nm = -1 }
/^---/ { flush(); next }
/^[ \t]*#/ { next }
{ i = ind($0); s = $0; sub(/^ */, "", s) }
inq { if (s == "" || i > qi) { if (s != "") q = q (q == "" ? "" : "\n") s; next } inq = 0 }
/^apiVersion:/ { api = val($0) }
/^kind:/ { k = val($0); dl = FNR }
/^  name:/ && n == "" { n = val($0) }
k ~ /AnalysisTemplate$/ {
  if (s ~ /^dryRun:/) { indry = 1; di = i; next }
  if (indry && i <= di && s !~ /^- /) indry = 0
  if (indry && s ~ /metricName:/) { v = val(s); if (v ~ /[.*]/) dryall = 1; dry[v] = 1; next }
  if (s ~ /^metrics:/) { emit_m(); inm = 1; mi = i; next }
  if (inm && i <= mi && s !~ /^- /) { emit_m(); inm = 0 }
  if (inm && s ~ /^- / && i <= mi + 2) { emit_m(); mn = "?"; ml = FNR; fi = i + 2; s = substr(s, 3); i = fi }
  if (mn != "" && i == fi) { if (s ~ /^name:/) mn = val(s); else if (s ~ /^successCondition:/) sc = val(s); else if (s ~ /^failureCondition:/) fc = val(s)
    else if (s ~ /^count:/) cnt = val(s); else if (s ~ /^failureLimit:/) fl = val(s); else if (s ~ /^inconclusiveLimit:/) il = val(s) }
  if (mn != "" && i > fi && pv == "" && s ~ /^(prometheus|datadog|newRelic|wavefront|influxdb|cloudWatch|graphite|kayenta|web|job|skywalking|plugin):/) { pv = s; sub(/:.*/, "", pv) }
}
(k ~ /AnalysisTemplate$/ || k == "MetricTemplate") && s ~ /^query:/ { v = val(s); if (v ~ /^[|>][-+]?$/) { inq = 1; qi = i; q = "" } else q = v; next }
k == "MetricTemplate" && s ~ /^type:/ { pv = val(s) }
k == "Rollout" { if (s ~ /^canary:/) strat = "canary"; if (s ~ /^blueGreen:/) strat = "blueGreen"
  if (s ~ /^- setWeight:/) sw++; if (s ~ /^(- )?analysis:/) an = 1; if (s ~ /^prePromotionAnalysis:/) pre = 1
  if (s ~ /^autoPromotionEnabled:/) ap = val(s); if (s ~ /^(- )?templateName:/) { t = s; sub(/^- /, "", t); refs = refs "," val(t) } }
k == "Canary" && api ~ /flagger/ { if (s ~ /^skipAnalysis:[ \t]*true/) skip = 1; if (s ~ /^threshold:/) th = val(s); if (s ~ /^interval:/ && iv == "") iv = val(s)
  if (s ~ /^metrics:/) { nm = 0; fmi = i; next }
  if (nm >= 0 && s ~ /^- / && i <= fmi + 2) { nm++; cm = "?"; ci = i + 2; s = substr(s, 3); i = ci }
  if (nm > 0 && i == ci && s ~ /^name:/) cm = val(s)
  if (nm > 0 && s ~ /^min:/ && val(s) ~ /^0(\.0*)?$/) fm = fm " NEVER-FAILS(" cm ": thresholdRange.min 0)" }
END { flush() }
AWK
while IFS= read -r f; do [ -n "$f" ] && awk -v R="$SCAN/analysis-rules.yaml" -f "$GATE" "$f"; done < "$SCAN/delivery.txt" | tee "$SCAN/gate-src.txt"
RENDERS | while IFS= read -r f; do awk -v R= -f "$GATE" "$f"; done > "$SCAN/gate-render.txt"
awk 'NR == FNR { k = $0; sub(/^[^ ]+ /, "", k); s[k] = 1; next } { k = $0; sub(/^[^ ]+ /, "", k); if (!(k in s)) print "render-only: " $0 }' "$SCAN/gate-src.txt" "$SCAN/gate-render.txt"
echo '# 5g selector grounding: observability rule-inventory.py --check=selectors (when installed) on every Prometheus query above'
RI=.claude/skills/alert-rule-lint/scripts/rule-inventory.py
if ! rg -q 'alert:' "$SCAN/analysis-rules.yaml"; then echo 'grounding: N/A (no Prometheus query)'
elif [ ! -f "$RI" ]; then echo 'grounding: NOT-RUN (owner pack observability not installed) — every query row stays [report-flagged] selector not grounded'
else if [ -z "${INV:-}" ]; then INV="$SCAN/inventory.txt"; NM='([A-Za-z_:][\w.:]*)'   # alert-rule-lint pre-flight step 2, verbatim; that file wins on a difference
  { rg -U --pcre2 -o --no-filename -r '$1' "(?:new\s+(?:\w+\.)?(?:Counter|Gauge|Histogram|Summary)|make(?:Counter|Gauge|Histogram|Summary)Provider)\s*(?:<[^>]*>)?\(\s*\{[^}]*?\bname\s*:\s*['\"]${NM}['\"]" "${CODE[@]}" "${X[@]}" .
    rg -U --pcre2 -o --no-filename -r '$1' "(?:\bprometheus_client\.|(?<![.\w]))(?:Counter|Gauge|Histogram|Summary|Info|Enum)\(\s*['\"]${NM}['\"]" "${CODE[@]}" "${X[@]}" .
    rg -U --pcre2 -o --no-filename -r '$1' "(?:Counter|Gauge|Histogram|Summary)Opts\s*\{[^}]*?\bName:\s*\"${NM}\"" "${CODE[@]}" "${X[@]}" .
    rg -U --pcre2 -o --no-filename -r '$1' "(?:\b(?:Counter|Timer|Gauge|DistributionSummary|LongTaskTimer)\.builder|\bregistry\.(?:counter|timer|gauge|summary)|\b(?:create|Create)(?:Counter|Histogram|UpDownCounter|Gauge|Observable(?:Gauge|Counter|UpDownCounter))(?:<\w+>)?|\bcreate_(?:counter|histogram|up_down_counter|gauge|observable_\w+)|\b(?:Int64|Float64)(?:Counter|Histogram|UpDownCounter|Gauge|Observable(?:Counter|Gauge|UpDownCounter))|\bMetrics\.Create(?:Counter|Gauge|Histogram|Summary))\(\s*['\"]${NM}['\"]" "${CODE[@]}" "${X[@]}" .
  } | sort -u > "$INV"; fi
  RF=(); while IFS= read -r f; do RF+=("$f"); done < <(rg -l --pcre2 -g '*.{yml,yaml}' "${X[@]}" '^\s*-?\s*record:\s*\S' .)
  echo "inventory: $(wc -l < "$INV" | tr -d ' ') names; recording-rule files: ${#RF[@]}"
  python3 -B "$RI" "$SCAN/analysis-rules.yaml" ${RF[@]+"${RF[@]}"} --check=selectors --inventory="$INV" --format=text --all > "$SCAN/grounding.txt"; echo "rule-inventory exit=$?"
  rg -F "$SCAN/analysis-rules.yaml" "$SCAN/grounding.txt"; fi
echo '# 1 flag registries (keys) and SDK call sites (keys read in code)'
rg --files -g '**/*{flag,flags,feature,features,toggle,toggles}*.{yml,yaml,json}' -g '**/*.flagd.json' "${X[@]}" -g '!**/package*.json' . | sort > "$SCAN/registries.txt"; cat "$SCAN/registries.txt"
while IFS= read -r f; do case "$f" in
  *.json) python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); f=d.get("flags") or d.get("features") or {}; [print(k) for k in (f if isinstance(f,dict) else [x.get("name") for x in f if isinstance(x,dict)])]' "$f" ;;
  *) awk '/^(flags|features|toggles):[ \t]*$/ { on = 1; next } on && /^[^ #]/ { on = 0 } on && /^  [A-Za-z0-9_.:\/-]+:/ { k = $1; sub(/:$/, "", k); gsub(/["\x27]/, "", k); print k }' "$f" ;;
esac | sed "s|^|$f	|"; done < "$SCAN/registries.txt" | sort -u > "$SCAN/keys.tsv"; echo "registry keys: $(wc -l < "$SCAN/keys.tsv" | tr -d ' ')"
rg -n -o --pcre2 "${CODE[@]}" "${X[@]}" -r '$1' "$CALL" . | "${NC[@]}" | sort > "$SCAN/calls.txt"; echo "SDK call sites: $(wc -l < "$SCAN/calls.txt" | tr -d ' ')"
cut -d: -f3- "$SCAN/calls.txt" | sort -u > "$SCAN/called.txt"; cut -f2 "$SCAN/keys.tsv" | sort -u > "$SCAN/declared.txt"
echo "called, never declared (evaluates to its default forever): $(comm -23 "$SCAN/called.txt" "$SCAN/declared.txt" | tr '\n' ' ')"
echo '# 1-2 reference count per declared key (quoted literal, and its SCREAMING_SNAKE form), age from git; harness check on keys with a call site'
while IFS="$(printf '\t')" read -r f key; do
  lit=$(rg -c -F "${CODE[@]}" "${X[@]}" -e "'$key'" -e "\"$key\"" -e "\`$key\`" . | awk -F: '{ s += $NF } END { print s + 0 }')
  up=$(printf '%s' "$key" | tr 'a-z.:/-' 'A-Z____'); snake=$(rg -c -F "${CODE[@]}" "${X[@]}" -e "$up" . | awk -F: '{ s += $NF } END { print s + 0 }')
  age=$(git log --diff-filter=A --format=%as -S"$key" -- "$f" 2>/dev/null | tail -1)
  called=$(rg -q -x -F -e "$key" "$SCAN/called.txt" && echo yes || echo no)
  printf '%s\t%s\tliteral=%s\tsnake=%s\tcall-site=%s\tadded=%s\n' "$f" "$key" "$lit" "$snake" "$called" "${age:-unknown}"
done < "$SCAN/keys.tsv" | tee "$SCAN/refs.tsv" | awk -F'\t' '$3 == "literal=0" || $4 != "snake=0" || $5 == "call-site=no"'
awk -F'\t' '$5 == "call-site=yes" && $3 == "literal=0" { bad++ } $5 == "call-site=yes" { n++ } END { print (bad ? "HARNESS BROKEN: " bad " keys with a call site count 0 — fix the globs before any DEAD row" : "harness ok (" n + 0 " keys with a call site all counted)") }' "$SCAN/refs.tsv"
echo '# 2 flags hard-coded in code; 3 registry keys missing an owner, or an expiry on a release flag'
rg -n --pcre2 "${CODE[@]}" "${X[@]}" '^(?:export\s+)?(?:const|let|var)\s+\w*(?i:flag|feature|enable|toggle)\w*\s*(?::\s*\w+\s*)?=\s*(?:true|false)\s*;?\s*(?://.*)?$|^[A-Z][A-Z0-9_]*(?:FLAG|FEATURE|ENABLE|TOGGLE)[A-Z0-9_]*\s*=\s*(?:True|False)\s*(?:#.*)?$|^\s*(?:(?:public|private|protected)\s+)?static\s+final\s+boolean\s+\w*(?i:flag|feature|enable|toggle)\w*\s*=\s*(?:true|false)\s*;' . | "${NC[@]}"
while IFS= read -r f; do case "$f" in *.json) ;; *) awk -v F="$f" 'function out() { if (k != "" && (!o || !(e || p))) print F ":" kl ": " k " missing=" (o ? "" : "owner ") (e || p ? "" : "expiry") }
  /^(flags|features|toggles):/ { on = 1; next } on && /^[^ #]/ { out(); k = ""; on = 0 } on && /^  [A-Za-z0-9_.:\/-]+:/ { out(); k = $1; sub(/:$/, "", k); kl = FNR; o = 0; e = 0; p = 0; next }
  on && /^    owner:/ { o = 1 } on && /^    (expires|expiry|expiration|remove_by|removal|sunset|until|ticket):/ { e = 1 } on && /^    (type|kind):[ \t]*(permanent|ops|operational|kill-?switch|ramp|experiment)/ { p = 1 } END { out() }' "$f" ;; esac; done < "$SCAN/registries.txt"
echo '# 4 kill-switch candidates: env-var flags read at module scope (boot) vs per call; risky keys'
rg -n --pcre2 "${CODE[@]}" "${X[@]}" "(?:process\.env\.|process\.env\[['\"]|os\.(?:environ\[|environ\.get\(|getenv\()['\"]|os\.Getenv\(\"|ENV\[['\"]|System\.getenv\(\")$ENVF" . | "${NC[@]}" | awk -F: '{ l = $0; sub(/^[^:]+:[0-9]+:/, "", l); print ((l ~ /^(export |const |let |var |[A-Z_][A-Z0-9_]* *=|static |final )/) ? "boot-read" : "per-call") "\t" $0 }'
rg -n --pcre2 "${CODE[@]}" "${X[@]}" -i "$CALL" . | rg -i --pcre2 '\b(pay|refund|charge|checkout|billing|invoice|payout|transfer|delete|purge|wipe|migrat|webhook|email|sms|notify)' | "${NC[@]}"
echo '# 6 per-environment values: env-var flags across .env.*, compose, rendered env; registry environments blocks'
rg -n --hidden --pcre2 -g '**/.env*' -g '*compose*.{yml,yaml}' -g '!**/node_modules/**' "^\s*-?\s*$ENVF\s*[=:]\s*\S" . | sort
RENDERS | while IFS= read -r f; do rg -n -A1 --pcre2 "^\s*-\s*name:\s*$ENVF" "$f"; done
while IFS= read -r f; do case "$f" in *.json) ;; *) awk -v F="$f" '
  function chk(  n, i, v, d, nu) { n = split(ev, a, ","); d = 0; nu = 1; for (i = 1; i <= n; i++) { v = a[i]; sub(/^[^:]*:[ \t]*/, "", v); gsub(/[ \t{}"\x27]/, "", v); if (v !~ /^[0-9.]+$/) nu = 0; if (i > 1 && v != f1) d = 1; if (i == 1) f1 = v }
    if (d) print F ":" el ": " k " " (nu ? "RAMP (precedents § 27)" : (ev ~ /prod[a-z]*:[ \t]*(true|on|1)([ \t,]|$)/ && ev ~ /:[ \t]*(false|off|0)([ \t,]|$)/) ? "PROD-AHEAD" : (ev ~ /prod[a-z]*:[ \t]*(false|off|0)([ \t,]|$)/) ? "STAGED" : "DRIFT") " {" ev "}"; ev = "" }
  /^  [A-Za-z0-9_.:\/-]+:/ { if (ev != "") chk(); k = $1; sub(/:$/, "", k); ine = 0; next }
  /^    (environments|envs):/ { el = FNR; v = $0; sub(/^[^:]*:[ \t]*/, "", v); if (v ~ /^\{/) { gsub(/[{}]/, "", v); ev = v; chk() } else { ine = 1; ev = "" } next }
  ine && /^      [A-Za-z0-9_-]+:/ { t = $0; sub(/^ +/, "", t); ev = ev (ev == "" ? "" : ",") t; next }
  ine { ine = 0; if (ev != "") chk() }
  END { if (ev != "") chk() }' "$f" ;; esac; done < "$SCAN/registries.txt"
echo '# 7 a flag that selects config, credentials or routing (call site with a config read within 2 lines)'
rg -n -U --pcre2 "${CODE[@]}" "${X[@]}" "${CALL}[^\n]*\n?(?:[^\n]*\n){0,2}?[^\n]*(?:process\.env|os\.environ|os\.Getenv|config\.get|ConfigService)[^\n]*(?i:host|url|dsn|endpoint|region|bucket|queue|secret|database|db_|key)" . | rg --pcre2 "$CALL" | "${NC[@]}"
echo '# 8 SDK calls whose default (the value on provider outage, a missing key, an uninitialised client) is true'
rg -n --pcre2 "${CODE[@]}" "${X[@]}" "${CALL}[^\n]*,\s*(?:\(\s*\)\s*=>\s*|lambda[^:\n]*:\s*|default(?:_value)?\s*=\s*|fallback(?:_function)?\s*=\s*(?:lambda[^:\n]*:\s*)?)?(?:true|True)\b(?:\s*\)|\s*,)" . | "${NC[@]}"
echo '# 9 build-time flags: public env inlined by the bundler; flag build args'
rg -n --pcre2 "${CODE[@]}" "${X[@]}" "(?:process\.env|import\.meta\.env)\.$PUB" . | "${NC[@]}"
rg -n --hidden --pcre2 -g 'Dockerfile*' -g '*.dockerfile' -g 'Containerfile*' -g '.github/workflows/*.{yml,yaml}' -g '**/.gitlab-ci*.yml' -g '!**/node_modules/**' "^\s*ARG\s+$ENVF|--build-arg[ =]+$ENVF|^\s*ARG\s+$PUB|--build-arg[ =]+$PUB" .
```

How to read it:
- **§5 rows** are one per Rollout, Canary, MetricTemplate and AnalysisTemplate metric, from the source (the citation) and from each render (what applies). `render-only:` marks a row an overlay or values file changed. Codes: `NEVER-FAILS`, `NO-CONDITION`, `LIMIT>=COUNT`, `NO-INCONCLUSIVE-LIMIT`, `DRYRUN`, `UNSCOPED`, `ZERO-FALLBACK` (an empty series reads as 0 and passes), `NO-ANALYSIS`, `BG-AUTO-PROMOTE`, `NO-METRICS`, `SKIP-ANALYSIS`. `scope=hash` means the query selects the canary's pods (`rollouts_pod_template_hash`); `args` means it is templated, so read what the Rollout passes (`podTemplateHashValue: Latest`, the canary Service).
- **5g** prints only the AL-10 rows of the scratch rule file; each `alert` name is `<file>:<line>:<metric>` of the source. Grounding counts code registrations, recording-rule outputs and exporter defaults (observability precedents § 37, § 43); `exporter-default (unverified)` asks whether that exporter runs.
- **1** `called, never declared` is the orphan list. The reference table prints only keys worth reading: no literal, a SCREAMING_SNAKE twin (an env var or a constant: read it), or no SDK call site. `HARNESS BROKEN` voids every DEAD row until the globs are fixed (a `.vue` or `.erb` codebase needs its extension in `CODE`).
- **4** `boot-read` is an env-var flag assigned at module scope: it is not a kill switch. The second list is SDK calls on risky keys; the read decides whether the flag guards the side effect.
- **6** labels a registry environment block `PROD-AHEAD` (prod on, a pre-prod environment off: prod runs a path nothing tested), `STAGED` (pre-prod ahead: the release order working), `DRIFT` (non-boolean values differ: read) or `RAMP` (precedents § 27).

Blind spots, worked around rather than trusted: a key passed through a constant or wrapper (`flags.get(FLAGS.NEW_CHECKOUT)`) has no literal at the call: the SCREAMING_SNAKE column and the wrapper's own call site catch most of it, the read settles the rest. A SaaS registry is invisible offline. ApplicationSet-generated Rollouts are not expanded. A Helm chart rendered with default values only shows the default environment: pass each values file to `helm template` when one exists per environment.

### Measured (2026-10-10)

| Tree | Result |
|---|---|
| Seeded sample (Argo Rollouts ×3 + 2 AnalysisTemplates, Flagger Canary ×3 + MetricTemplate, a Kayenta stage, a kustomize prod overlay, a PrometheusRule, flagd `flags.yaml` with 13 keys, OpenFeature/LaunchDarkly TS, Unleash Python, LaunchDarkly Go, Vite; 27 positives, 12 decoys) | 1.6 s, 0 rg errors; bash 3.2 and zsh identical. **27/27 positives surface**: NEVER-FAILS ×2 (Argo `>= 0`, Flagger `min: 0`), LIMIT>=COUNT ×2 (one **render-only**, from an overlay patch), UNSCOPED ×2, NO-INCONCLUSIVE-LIMIT, DRYRUN, NO-ANALYSIS, BG-AUTO-PROMOTE, NO-METRICS, SKIP-ANALYSIS, Kayenta `marginal: 0`, 1 ungrounded selector via `rule-inventory.py` (8 queries, 2-name inventory, 1 recording rule); a dead key, an orphan key, a hard-coded flag, 6 keys missing an expiry or owner, a boot-read refund flag, PROD-AHEAD ×2, DRIFT, a flag that picks the database host, default-`true` ×2 (OpenFeature, Unleash `fallback_function`), a Vite flag and a flag `--build-arg`. Decoys: a spec file and a fixture never appear; the synthetic-load template (§ 28), the ramp (§ 27), STAGED ×3, the permanent `maintenance-mode`, the inverted `disable-legacy-pricing` default, the recording-rule query (grounded) and the scoped success-rate metric surface and clear on read. Without the observability pack, 5g printed `NOT-RUN (owner pack observability not installed)` |
| `benchmarks/fixtures/*` (16) | 0 delivery objects, 0 registries, 0 SDK calls in all 16; 0 rg errors. One row in quality-mix: `FEATURE_NEW_PRORATION=true` in `.env.example` with no reader (info). The slow-marketplace `isEnabled(` lives in a test file and stays excluded |
| Real NestJS + React monorepo (read-only, `git status` clean before and after) | 1.7 s. No Rollout, Canary or flag SDK; a KEDA ScaledObject and two kustomize `Kustomization` build files are not delivery objects (0 rows). **One FP class fixed before shipping:** the first hard-coded-flag regex printed 20 ORM entity defaults (`isEnabled = true;` class fields); it now needs a module-scope `const`/`let`/`var`, a SCREAMING_SNAKE constant or a `static final boolean`, and prints 0. **One sibling defect measured:** an include glob placed after the exclusion array re-reads `*.spec.ts` (ripgrep's last glob wins), so every code grep here puts `CODE` first. §6: one env-var flag declared in one environment (no drift). Every § prints `N/A` honestly |

## The 3,000-hit path

1. **Intersect** with what ships: §5 rows in a render a CD target applies; flag rows in a service root a rendered workload runs. Dismiss the rest with one read each (a dev overlay, a fixture, a preview).
2. **Group** by unit (precedents § 5): one AnalysisTemplate or ClusterAnalysisTemplate referenced by N Rollouts, one MetricTemplate, one registry file, one SDK wrapper, one key.
3. **Rank:** a prod Rollout or Canary that can never fail; then a default-`true` or boot-read flag on a risky key; then the rest.
4. **Read the top 30 groups.**
5. **Run the bulk oracle once:** one `rule-inventory.py` call grounds every query; one unit test per SDK wrapper with a failing provider settles §8 for every call through it (V233).
6. **Ledger the rest** as `Live, unreviewed (k groups / n rows — <continuing command>)`. Never mark it `checked`.

## Scans for

| § | Classes | Default severity |
|---|---|---|
| 1 | Dead key (declared, never read) · orphan key (read, never declared: the default forever) | L (M when the orphan guards a risky path) |
| 2 | Stale flag: hard-coded in code, or on in every environment past its expiry | L |
| 3 | No owner, or no removal date on a release flag | L |
| 4 | No kill switch on a risky path (payments, refunds, deletes, migrations, outbound side effects): env-var or boot-read flag, or none | M (H on a prod money or data-loss path) |
| 5 | DP-7 canary without a real gate | H |
| 6 | Flag drift across environments (PROD-AHEAD, DRIFT) | M |
| 7 | A flag that rewires config, credentials or routing | M |
| 8 | DP-8 unsafe default on provider outage or a missing key | M (H on a risky path) |
| 9 | DP-8 build-time flag that is treated as runtime | M |

### 1. Dead and orphan keys

```
BAD:   flags.yaml  dead-banner: {…}          (no literal, no SDK call, no env twin anywhere in code)
       getBooleanValue('orders-v3-pagination', false)   (no registry entry: always false, in every environment)
GOOD:  delete the registry entry and the branch together · declare the key, or delete the call
```
**Read the code:** Is the key read by another repo or a mobile client (a shared flagd file)? Through a constant or wrapper? A `literal=0 snake≥1` row is usually an env var or a constant: follow it to §2, §4 or §9. **Finding when** the key has no reader in any repo the registry serves (dead), or the SDK reads a key no registry declares (orphan). The harness line must say `harness ok`. **Proof:** S — both ends cited (the registry line and the empty reference count, or the call and the empty registry).

### 2. Stale flags

```
BAD:   const ENABLE_NEW_SEARCH = true;   // rollout finished      (the flag is gone in all but name)
       enable-new-search: { staging: true, production: true }  added 2025-11, no expiry
GOOD:  remove the flag and the dead branch in one change
```
**Read the code:** Is it a permanent operational flag (kill switch, maintenance mode: precedents § 27)? Is the `added=` date real (a shallow clone)? **Finding when** a release flag is constant in every environment, or replaced by a literal. **Proof:** S.

### 3. No owner or removal date

**Read the code:** `type: permanent` / ops / ramp keys are exempt from the expiry. Does the team track owners elsewhere (a CODEOWNERS block on the registry, the SaaS registry's maintainer)? **Finding when** a release flag has neither. One finding per registry file with N keys (precedents § 5). **Proof:** S.

### 4. No kill switch on a risky path

```
BAD:   const ASYNC_REFUND = process.env.FEATURE_ASYNC_REFUND === 'true';   (module scope: a restart to flip)
GOOD:  await flags.getBooleanValue('async-refund', false, ctx)   evaluated per request, served by the provider
```
**Read the code:** Does the flag guard the side effect itself (the charge, the delete, the outbound call), or only a log line? Is the env var re-read per request (a config service that reloads)? Is there another runtime switch for the same path (a circuit breaker, a queue pause)? **Finding when** a risky path shipped in this change, or reachable in prod, can only be turned off by a deploy or a restart. **Proof (V233):** flip the flag in a scratch provider with the service running: the next request takes the old path, with no deploy.

### 5. Canary without a real gate (DP-7)

```
BAD:   successCondition: result[0] >= 0                        (an error ratio is never negative)
       count: 3, failureLimit: 5                               (3 failures never exceed 5)
       dryRun: [{metricName: experimental-p99}]                (measured, never counted)
       query: …{route="/checkout"}…                            (the whole service: stable traffic dilutes the canary)
       Flagger metrics: []  ·  thresholdRange: {min: 0}  ·  skipAnalysis: true
       strategy.blueGreen with no prePromotionAnalysis and autoPromotionEnabled left at its default
GOOD:  successCondition: result[0] <= 0.01 · failureLimit: 1 of count: 5 · rollouts_pod_template_hash="{{args.canary-hash}}"
       · every selector grounded · blueGreen autoPromotionEnabled: false or a prePromotionAnalysis
```
**Read the code:**
- Can the condition be false for any value the metric can take (a ratio in 0–1, a latency in seconds vs milliseconds, a percentage vs a fraction)?
- Is another metric in the same template able to fail (the gate is the template, not one metric)?
- Does the query select the canary (`scope=hash`; for `args`, what the Rollout passes)? With a traffic-routed canary, does it select the canary Service?
- Does the selector ground (5g)? An ungrounded selector with `or vector(0)` or `scalar(` reads as a perfect canary; without them, Argo records errors until `consecutiveErrorLimit` [K].
- Is the analysis synthetic by design (a `job` provider driving load: precedents § 28)? Is it a preview environment (§ 24)?

**Finding when** no metric of the gate can fail for the values the series can take, the gate never runs (NO-ANALYSIS, BG-AUTO-PROMOTE, SKIP-ANALYSIS, NO-METRICS), or its selector names a series that exists nowhere. **Proof (V232):** the static read shows a value that fails the condition; every selector grounds (observability `rule-inventory.py --check=selectors` when installed); a canary returning 20 % errors on a throwaway cluster aborts within the analysis window (L, isolated kubeconfig), else `NO-DATA(rollout)`.

### 6. Flag drift across environments

**Read the code:** Is it a ramp or a permanent ops flag (precedents § 27)? Is `STAGED` the release order (pre-prod first) — that is not a finding. Is the difference documented next to the key? **Finding when** prod enables a value no pre-prod environment runs (PROD-AHEAD), or a non-boolean value differs with no note. **Proof:** S — the two environment values with their lines.

### 7. A flag that rewires config

**Read the code:** Does flipping it change only a code path, or also a host, a credential, a region or a queue? Is the second target provisioned in every environment the flag can turn on? **Finding when** a flag's branch selects a different backend or secret, so a flip has a blast radius the flag's name does not say. **Proof:** S — the call and the config read it selects.

### 8. Unsafe default on provider outage (DP-8)

```
BAD:   await client.getBooleanValue('new-checkout', true, ctx)        (provider down → the new checkout for everyone)
       client.is_enabled("bulk-refund", ctx, fallback_function=lambda feature_name, context: True)
GOOD:  the default is the old, safe path: getBooleanValue('new-checkout', false, ctx)
```
**Read the code:** Is the name inverted, so `true` is the safe path (`disable-legacy-pricing`)? Does the provider serve a bootstrap file offline? Is the path risky (money, data, outbound side effects)? **Finding when** the default enables the new or risky path. **Proof (V233):** a unit test with a provider that throws (OpenFeature `NOOP`/error provider, an LD client in offline mode, an Unleash client with no toggles) gets the safe value.

### 9. Build-time flags

**Read the code:** Does the registry, a runbook or an incident plan describe this flag as flippable at runtime (`flags.yaml` "flip at runtime" beside a `VITE_FLAG_*`)? Is it a pure build switch the team deploys to change, by design? **Finding when** a flag used as a runtime switch is inlined at build or passed as a `--build-arg`. **Proof (V233):** flipping the registry value leaves the served bundle unchanged (`rg` the value in `dist/`), while a runtime-evaluated flag changes on the next request.

## Proof

The oracles are in [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § DevOps. **Scope: scratch providers, unit tests, `${TMPDIR}` and throwaway kind clusters through an isolated `--kubeconfig=<scratch>` only — never the user's flag service, cluster or default kube context.**

| § | Oracle | Tier | V |
|---|---|---|---|
| 1, 2, 3, 6, 7 | Two-ended static trace (the declaration and the read; the two environment values) | S | — |
| 4, 8, 9 | Provider-error default: a failing provider returns the safe value; the kill switch flips without a deploy; a build-time value does not | R (unit) | V233 |
| 5 | Canary checks: the condition can fail (static), every selector grounds (observability), a 20 %-error canary aborts (L) | S + L | V232 |

## Output

```
progressive-delivery — lanes: argo-rollouts (3 Rollouts, 2 templates; render: base + prod), flagger (3 Canaries), kayenta (read),
  flags: flagd file (13 keys), openfeature, launchdarkly, unleash, env, vite · observability: installed (5g ran) · infrastructure: not installed

Findings: 3 · Unconfirmed: 2

1. deploy/k8s/base/analysis-api.yaml:11                                  [report-with-fix]   high
   §5 DP-7 — AnalysisTemplate api-canary metric error-rate: `successCondition: result[0] >= 0` on an error ratio
   (0–1) cannot fail; Rollout api (prod render) uses it as its only error gate. Proof: static (V232). Fix:
   `successCondition: result[0] <= 0.01`, `failureLimit: 1`.

2. deploy/k8s/overlays/prod/kustomization.yaml:11                       [report-with-fix]   high
   §5 DP-7 — render-only: the prod patch sets success-rate `failureLimit: 9` over `count: 5` (base is 1).
   Proof: render row (V232, static). Fix: drop the patch, or keep `failureLimit` below `count`.

3. apps/api/src/flags.ts:7                                               [report-flagged]    medium
   §8 DP-8 — `getBooleanValue('new-checkout', true, ctx)`: provider down → the new checkout for all users.
   Unproven link: no unit test with a failing provider. Settling test: V233. Fix: default `false`.

Verification: 41 candidates → 3 findings · 2 unconfirmed · 6 hardening · 0 pre-existing · 30 refuted (self-verified)

Class coverage:
  §1 dead / orphan keys        checked (13 keys, 11 calls, harness ok → 2 rows)
  §5 canary gate                checked (14 source rows, 1 render-only; 8 queries → 1 ungrounded)
  §8 unsafe default             checked (11 calls → 3 rows; 1 inverted name refuted)
  …one line for each of §2–§4, §6, §7, §9
```

`[report-with-fix]`: the object, its environment, the platform or SDK fact and the oracle are in hand, and the fix is local. `[report-flagged]`: one link is unproven — the grounding (observability absent), a SaaS registry, a `[K]` semantic, no unit test, a failed render. The row names the link and the settling test.

The coverage block lists **all nine** §s on every run: `checked (k → m)` only when the grep or the awk ran on a lane that is present; `N/A (no progressive-delivery object)` / `N/A (no flag registry or SDK)`; `blocked (<reason>)` for a failed render or `HARNESS BROKEN`; `Unconfirmed (registry not in repo)`; `Live, unreviewed (k groups / n rows)` for a partial review.

## False positives / precedents

The verifier reads [`precedents/devops.md`](../../../../snippets/precedents/devops.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:
- **§ 27** permanent operational flags are not stale, and a percentage ramp that differs across environments is the ramp working. **§ 28** a declared synthetic-load analysis is a real gate when its check can fail. **§ 24** preview environments. **§ 23** a GitOps CI that only commits manifests.
- **§ 5** one finding per template, MetricTemplate, registry file or SDK wrapper. **§ 4** pre-existing lines on a diff run never block. **§ 41** a tool that errored or parsed nothing is NOT-RUN.
- Observability precedents § 37 (a metric name in no inventory is fabricated: a proposed query that names one is Refuted) and § 16 (a mocked promtool test does not prove a series exists).

Read rules measured on the sample (2026-10-10): a `STAGED` difference is the release order, not drift; an inverted flag name whose `true` is the old path is not an unsafe default; a `job`-provider metric has no condition by design.

Rationalizations to reject:
- "The Rollout has an analysis": one that cannot fail is a slower full deploy.
- "We can always roll back": a rollback is a deploy; a kill switch is a flip.
- "The flag defaults to true because the feature is on in prod": the default is what the outage serves.
- "It is a flag, so we can turn it off": not when it is inlined at build or read at boot.

## When to run

- On any diff touching a Rollout, AnalysisTemplate, Canary, MetricTemplate, a Spinnaker pipeline, a flag registry, a flag SDK call, a `FEATURE_*` / `*_ENABLED` env var or a public build-time env var.
- Before a risky change ships behind a flag; quarterly as a flag-hygiene sweep (§1–§3).
- On every whole-repo `/devops-audit`, reporting all nine §s.

## Halt conditions

- **Do not report a critical or high row as confirmed until a separate verifier has refuted it.** That verifier is not the run that found it; it applies [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with `precedents/devops.md`. Under `/devops-audit` that is its verification phase; standalone, run the protocol as a second pass and tag those rows `self-verified`. List the rest as Unconfirmed, Hardening, Pre-existing or Refuted; never drop them.
- **Halt on a finding missing its anchors:** the line, the object or key, the environment, the platform or SDK fact with its tag, and the fix.
- **No DEAD row without `harness ok`.** A broken harness reports every flag dead; "delete these 23 flags" cannot be taken back. A key a SaaS registry holds is `UNREADABLE` offline.
- **No "selector does not exist" without the grounding run**, and no grounding claim without observability's script: without it the row stays `[report-flagged]`.
- **Never run V232 or V233 against the user's flag service, cluster or default kube context.** Every `kubectl` takes an isolated `--kubeconfig=<scratch>`.
- **No proposed fix may weaken a gate to clear a row:** no raised `failureLimit`, no metric moved into `dryRun`, no `skipAnalysis`, no default flipped to `true`.
- **Do not print "rollouts are gated" or "flags are clean" without the coverage block.** **Do not re-derive a class another skill owns** (§ Boundaries); cross-link it.

## Related

- `/devops-audit` dispatches this skill on a flag config, Rollout or AnalysisTemplate and folds its coverage block into the delivery rows; `/devops-fix` closes them with V232 and V233. `/rollback-deploy` asks whether a kill switch exists before it moves an artifact.
- `@deployment-engineer` judges these rows and picks the strategy; `monitor-deploy` watches one rollout; `deploy-safety-scan`, `release-integrity-scan` and `gitops-audit` (this pack) own the neighbouring classes.
- Observability `alert-rule-lint` §4 (the grounding script), infrastructure `k8s-availability-scan` and `k8s-render-scan` §4, database `migration-safety` §4, security `secret-scan-method` — each when its pack is installed.

## Sources

Classes DP-7 and DP-8, the Argo Rollouts v1.10.0 / Flagger v1.45.0 / OpenFeature spec v0.9.0 versions and the `[K]` semantics (Inconclusive pauses, provider defaults) from the devops research catalog (release and deploy reliability notes, 2026-10-10) and the batch-4 devops eval (kept-skill scope). The grounding technique is observability's (`alert-rule-lint` §4, measured there). Rows tagged `[K]`/`[K?]` are settled on the `ci-defects` fixture or a sandbox before a fix relies on them. Paraphrased; no text reproduced beyond identifiers.
