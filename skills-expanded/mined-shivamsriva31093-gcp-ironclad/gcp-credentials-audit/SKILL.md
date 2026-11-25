---
name: gcp-credentials-audit
description: Use to inventory and risk-classify every API key and user-managed service-account key across all accessible GCP projects. READ-ONLY — does not mutate cloud state. Use standalone, or as Phase 1a of the `gcp-ironclad` driver.
---

# GCP Credentials Audit (READ-ONLY)

## Overview

Walks every GCP project the caller can access, lists every API key and every user-managed service-account key, and classifies each by risk. Writes the result as JSON to the session directory. **Does not mutate cloud state.**

## When to Use

- Triggered by the `gcp-ironclad` driver as Phase 1a.
- Or invoked standalone when you want only the audit, without applying any controls.

## Inputs

- `SESSION_DIR` env var: path to the session directory created by the driver (e.g. `/tmp/gcp-ironclad/2026-05-25T10-30-00Z/`). If invoked standalone, default to `/tmp/gcp-ironclad/standalone-$(date -u +%Y-%m-%dT%H-%M-%SZ)/`.
- `LOOKBACK_DAYS` env var (optional): how many days back to look for last-used signal. Default `30`.
- `AUDIT_VERIFY_PARITY` env var (optional): when `1`, also runs the per-project loop over CAI-covered projects and diffs the inventories to prove parity (see "Parity mode"). Off by default.

## Outputs

Writes `${SESSION_DIR}/audit.json` matching `output.schema.json` in this skill's directory.

## Risk classification

| Class | Trigger |
|---|---|
| `CRITICAL` | API key with `restrictions = NONE` (fully unrestricted) |
| `HIGH` | API key restricted to a service the project has never used; SA with ≥3 user-managed keys; SA key older than 365 days |
| `MEDIUM` | API key created >180 days ago AND last-used >90 days ago; SA key older than 90 days |
| `LOW` | API key restricted to ≤1 service and used within the last 30 days |
| `INFO` | Google-managed keys (Firebase browser keys, default compute SAs, `firebase-adminsdk-fbsvc@*`) |

## Execution

### Step A: Establish session directory

```bash
SESSION_DIR="${SESSION_DIR:-/tmp/gcp-ironclad/standalone-$(date -u +%Y-%m-%dT%H-%M-%SZ)}"
mkdir -p "${SESSION_DIR}/raw"
echo "SESSION_DIR=${SESSION_DIR}"
```

### Step B: Discover projects (from driver scope or standalone), then derive the CAI query scopes and the number→id map.

```bash
# Project list (from driver scope, or discover standalone)
if [ -f "${SESSION_DIR}/scope.json" ]; then
  cp "${SESSION_DIR}/scope.json" "${SESSION_DIR}/scope.local.json"
else
  gcloud projects list --format=json > "${SESSION_DIR}/raw-projects.json"
  jq -n --slurpfile p "${SESSION_DIR}/raw-projects.json" '{projects:$p[0]}' \
    > "${SESSION_DIR}/scope.local.json"
fi
jq -r '.projects[].projectId' "${SESSION_DIR}/scope.local.json" > "${SESSION_DIR}/projects.txt"

# Derivations for the CAI fast path:
#  - projnum-to-id.json : project NUMBER -> projectId (CAI returns numbers)
#  - cai-scopes.txt     : distinct org/folder scopes to query
#  - uncovered.txt      : starts with parent-less (standalone) projects; the
#                         fast path appends projects whose scope query failed
jq '[.projects[] | select(.projectNumber) | {(.projectNumber): .projectId}] | add // {}' \
  "${SESSION_DIR}/scope.local.json" > "${SESSION_DIR}/projnum-to-id.json"
jq -r '.projects[] | select(.parent) | "\(.parent.type)s/\(.parent.id)"' \
  "${SESSION_DIR}/scope.local.json" | sort -u > "${SESSION_DIR}/cai-scopes.txt"
jq -r '.projects[] | select(.parent|not) | .projectId' \
  "${SESSION_DIR}/scope.local.json" > "${SESSION_DIR}/uncovered.txt"

echo "projects=$(wc -l < "${SESSION_DIR}/projects.txt") scopes=$(wc -l < "${SESSION_DIR}/cai-scopes.txt") standalone=$(wc -l < "${SESSION_DIR}/uncovered.txt")"
```

### Step C1: CAI fast path (per scope)

For each scope in `cai-scopes.txt`, query the two asset types. A scope that returns cleanly means **every project under it is covered**; a scope that errors sends its projects to the fallback (Step C2) and emits a recommendation.

```bash
export CLOUDSDK_CORE_DISABLE_PROMPTS=1   # an "enable API? (y/N)" prompt would read the scope list as answers (see Step C2)
: > "${SESSION_DIR}/creds.cai.json.parts"
: > "${SESSION_DIR}/covered.txt"
: > "${SESSION_DIR}/cai-errors.json.parts"
while read SCOPE; do
  SAFE=$(echo "$SCOPE" | tr '/' '_')
  ok=1
  for TYPE in apikeys.googleapis.com/Key iam.googleapis.com/ServiceAccountKey; do
    OUT="${SESSION_DIR}/raw/cai.${SAFE}.$(echo "$TYPE" | tr '/.' '__').json"
    if ! gcloud asset search-all-resources --scope="$SCOPE" \
          --asset-types="$TYPE" --read-mask='*' --format=json \
          > "$OUT" 2>"${OUT}.err"; then
      ok=0; break
    fi
  done

  if [ "$ok" = 0 ]; then
    # Scope failed — fall back for its projects, recommend the unlock (READ-ONLY: we never enable).
    REASON=$(tr -d '\n' < "${OUT}.err" | cut -c1-300)
    jq -r --arg s "$SCOPE" '.projects[] | select(.parent) | select(("\(.parent.type)s/\(.parent.id)")==$s) | .projectId' \
      "${SESSION_DIR}/scope.local.json" >> "${SESSION_DIR}/uncovered.txt"
    jq -nc --arg s "$SCOPE" --arg r "$REASON" \
      '{context:"cai_fallback", message:("CAI query failed for \($s): \($r). Falling back to the per-project loop for its projects. To enable the fast path next run: (1) gcloud services enable cloudasset.googleapis.com --project=<quota-project> ; (2) grant your account roles/cloudasset.viewer on \($s).")}' \
      >> "${SESSION_DIR}/cai-errors.json.parts"
    continue
  fi

  # Scope OK — mark its projects covered (complete picture, even if zero keys).
  jq -r --arg s "$SCOPE" '.projects[] | select(.parent) | select(("\(.parent.type)s/\(.parent.id)")==$s) | .projectId' \
    "${SESSION_DIR}/scope.local.json" >> "${SESSION_DIR}/covered.txt"

  AK="${SESSION_DIR}/raw/cai.${SAFE}.apikeys_googleapis_com_Key.json"
  SK="${SESSION_DIR}/raw/cai.${SAFE}.iam_googleapis_com_ServiceAccountKey.json"
  jq --slurpfile map "${SESSION_DIR}/projnum-to-id.json" '
    [ .[] | (.versionedResources[0].resource) as $r
      | select((($r.deleteTime) // "") == "")          # drop soft-deleted keys (Task 1 finding)
      | {
        type:"api_key",
        project:(.project | sub("projects/";"") as $n | ($map[0][$n] // $n)),
        uid:($r.uid // (.name | sub(".*/keys/";""))),
        displayName:($r.displayName // .displayName // ""),
        createTime:($r.createTime // $r.create_time),
        restrictions:($r.restrictions // null),
        lastUsedAt:null } ]' "$AK" >> "${SESSION_DIR}/creds.cai.json.parts"
  jq --slurpfile map "${SESSION_DIR}/projnum-to-id.json" '
    [ .[] | . as $row | ($row.versionedResources[0].resource) as $r
      | ($r.keyType // $r.key_type) as $kt | select($kt=="USER_MANAGED")
      | (($row.displayName // $row.name) | capture("serviceAccounts/(?<sa>[^/]+)/keys/")?) as $m
      | { type:"sa_key",
          project:($row.project | sub("projects/";"") as $n | ($map[0][$n] // $n)),
          serviceAccount:($m.sa // "UNPARSED"),          # email from result-level displayName; never silently drop/null on a malformed name
          keyId:($row.name | sub(".*/keys/";"")),
          createTime:($r.validAfterTime // $r.valid_after_time),
          lastUsedAt:null } ]' "$SK" >> "${SESSION_DIR}/creds.cai.json.parts"
done < "${SESSION_DIR}/cai-scopes.txt"

# Flatten + dedupe (uid for keys, project+serviceAccount+keyId for SA keys) in case scopes overlap.
# stderr is intentionally NOT suppressed: a parse failure here would otherwise silently
# yield zero CAI credentials — a dangerous false-clean for a security audit.
jq -s 'add // [] | unique_by(.uid // "\(.project)/\(.serviceAccount)/\(.keyId)")' \
  "${SESSION_DIR}/creds.cai.json.parts" > "${SESSION_DIR}/creds.cai.json" \
  || { echo "WARN: could not parse creds.cai.json.parts; writing empty CAI set" >&2; \
       echo '[]' > "${SESSION_DIR}/creds.cai.json"; }
# De-dupe uncovered (a project listed standalone won't also be covered, but guard anyway).
sort -u "${SESSION_DIR}/uncovered.txt" -o "${SESSION_DIR}/uncovered.txt"
echo "cai_credentials=$(jq length "${SESSION_DIR}/creds.cai.json") covered_projects=$(sort -u "${SESSION_DIR}/covered.txt" 2>/dev/null | wc -l)"
```

**Resilience:** the live probe confirmed `restrictions` (keys) and `keyType`/`validAfterTime` (SA keys) are present in `versionedResources`, so the `--read-mask='*'` fast form above is the path used. Kept as a defensive note: if for some asset type/org those fields are ever absent, swap that one query for `gcloud asset list --<organization|folder|project>=<id> --content-type=resource --asset-types="$TYPE" --format=json` and read the resource from `.[].resource.data` instead of `.versionedResources[0].resource`.

### Step C2: Per-project fallback (uncovered projects)

For each `$P` in `uncovered.txt` (standalone projects + any scope CAI couldn't read), run the original per-project inventory. This path is unchanged and READ-ONLY.

**Prompts must be off.** When the quota project gcloud resolves doesn't have the API enabled (a `billing/quota_project` setting or `CLOUDSDK_BILLING_QUOTA_PROJECT` pointing at such a project), gcloud asks "Would you like to enable and retry? (y/N)" and reads the answer from stdin. Inside these loops stdin is the project list (or the piped key/SA list), so the prompt eats the *next* lines as answers and those projects are never visited, with no error: a false clean. (Reproduced: 5 projects in, 1 visited.) `CLOUDSDK_CORE_DISABLE_PROMPTS=1` makes gcloud take the default (No) and fail that one call, leaving its error in the project's `.err` file, and the loop goes on.

```bash
export CLOUDSDK_CORE_DISABLE_PROMPTS=1   # see above: a prompt here eats the loop's input
while read P; do
  echo "## $P"
  # API keys
  gcloud services api-keys list --project="$P" --format=json \
    > "${SESSION_DIR}/raw/${P}.apikeys.json" 2>"${SESSION_DIR}/raw/${P}.apikeys.err"
  # Per-key details (restrictions, createTime)
  if jq -e 'length>0' "${SESSION_DIR}/raw/${P}.apikeys.json" >/dev/null 2>&1; then
    jq -r '.[].uid' "${SESSION_DIR}/raw/${P}.apikeys.json" | while read uid; do
      gcloud services api-keys describe "$uid" --project="$P" --format=json \
        > "${SESSION_DIR}/raw/${P}.key.${uid}.json" 2>/dev/null
    done
  fi
  # Service accounts
  gcloud iam service-accounts list --project="$P" --format=json \
    > "${SESSION_DIR}/raw/${P}.sas.json" 2>"${SESSION_DIR}/raw/${P}.sas.err"
  # Per-SA user-managed keys
  if jq -e 'length>0' "${SESSION_DIR}/raw/${P}.sas.json" >/dev/null 2>&1; then
    jq -r '.[].email' "${SESSION_DIR}/raw/${P}.sas.json" | while read sa; do
      gcloud iam service-accounts keys list --iam-account="$sa" --managed-by=user --format=json \
        > "${SESSION_DIR}/raw/${P}.sakeys.${sa}.json" 2>/dev/null
    done
  fi
done < "${SESSION_DIR}/uncovered.txt"
```

If a project errors with `PERMISSION_DENIED` or `API has not been used`, record it in `projectsSkipped` with the reason and move on.

```bash
# Assemble loop raw files into the unified record shape (same as creds.cai.json),
# and record genuinely-unreadable projects (no_access) for scope.projectsSkipped.
# NB: the loop already passed --managed-by=user to `keys list`, so its SA-key files
# are user-managed only — do NOT re-filter on keyType here (the field may be absent
# and would wrongly drop every key).
: > "${SESSION_DIR}/creds.loop.json.parts"
: > "${SESSION_DIR}/skipped.json.parts"
while read P; do
  [ -n "$P" ] || continue
  # no_access = couldn't even list service accounts (a core, always-enabled API)
  if grep -qi "PERMISSION_DENIED" "${SESSION_DIR}/raw/${P}.sas.err" 2>/dev/null \
     && ! jq -e 'length>0' "${SESSION_DIR}/raw/${P}.sas.json" >/dev/null 2>&1; then
    jq -nc --arg p "$P" '{projectId:$p, reason:"no_access"}' >> "${SESSION_DIR}/skipped.json.parts"
  fi
  for KF in "${SESSION_DIR}"/raw/"${P}".key.*.json; do
    [ -e "$KF" ] || continue
    jq --arg p "$P" '[{type:"api_key",project:$p,uid:.uid,
      displayName:(.displayName//""),createTime:.createTime,
      restrictions:(.restrictions//null),lastUsedAt:null}]' "$KF" \
      >> "${SESSION_DIR}/creds.loop.json.parts"
  done
  for SF in "${SESSION_DIR}"/raw/"${P}".sakeys.*.json; do
    [ -e "$SF" ] || continue
    jq --arg p "$P" '[ .[] | {type:"sa_key",project:$p,
         serviceAccount:((.name|capture("serviceAccounts/(?<sa>[^/]+)/keys/")?).sa // "UNPARSED"),
         keyId:(.name|sub(".*/keys/";"")),
         createTime:(.validAfterTime//.valid_after_time),lastUsedAt:null} ]' "$SF" \
      >> "${SESSION_DIR}/creds.loop.json.parts"
  done
done < "${SESSION_DIR}/uncovered.txt"
jq -s 'add // []' "${SESSION_DIR}/creds.loop.json.parts" > "${SESSION_DIR}/creds.loop.json" \
  || echo '[]' > "${SESSION_DIR}/creds.loop.json"
jq -s '.' "${SESSION_DIR}/skipped.json.parts" > "${SESSION_DIR}/skipped.json" \
  || echo '[]' > "${SESSION_DIR}/skipped.json"
```

### Step D: Best-effort last-used signal per API key

For every project that holds API keys, issue ONE Cloud Monitoring `timeSeries.list` query for `serviceruntime.googleapis.com/api/request_count` grouped by `credential_id` over the last `LOOKBACK_DAYS` days; set each API key's `lastUsedAt` to its latest non-zero point (else `null`). SA-key last-used is not tracked by this metric and stays `null`.

**`credential_id` is a *resource* label, not a metric label.** It lives on the `consumed_api` monitored resource (alongside `service`, `method`, `version`); the metric's own labels are only `protocol`, `response_code`, `response_code_class` and `grpc_status_code`. Two details are load-bearing:

- Group by `resource.label.credential_id` and read `.resource.labels.credential_id`. `metric.label.credential_id` does not exist: series come back without it, the `{(.cid): …}` join hits a `null` object key, and every key silently ends up with `lastUsedAt: null`.
- Set `aggregation.crossSeriesReducer`. Without a reducer the API ignores `groupByFields` and returns one series per (method × response code × …), hundreds per busy project, instead of one per credential.

```bash
# ADC first (the documented auth path); fall back to the gcloud user token when ADC
# is missing or needs reauth. Without the fallback every query 401s and every key
# reads as never-used.
TOKEN=$(gcloud auth application-default print-access-token 2>/dev/null \
        || gcloud auth print-access-token)
LOOKBACK_DAYS="${LOOKBACK_DAYS:-30}"
START=$(date -u -v-${LOOKBACK_DAYS}d +%Y-%m-%dT00:00:00Z 2>/dev/null \
        || date -u -d "${LOOKBACK_DAYS} days ago" +%Y-%m-%dT00:00:00Z)
END=$(date -u +%Y-%m-%dT00:00:00Z)

# Merge both inventory paths first (Step E consumes creds.json).
jq -s 'add // []' "${SESSION_DIR}/creds.cai.json" "${SESSION_DIR}/creds.loop.json" \
  > "${SESSION_DIR}/creds.json"

# One Monitoring query per project holding api_key credentials; one series per credential.
echo '{}' > "${SESSION_DIR}/lastused.json"
: > "${SESSION_DIR}/monitoring-errors.json.parts"
for P in $(jq -r '[.[]|select(.type=="api_key")|.project]|unique[]' "${SESSION_DIR}/creds.json"); do
  RESP=$(curl -s -G "https://monitoring.googleapis.com/v3/projects/${P}/timeSeries" \
    -H "Authorization: Bearer ${TOKEN}" \
    --data-urlencode 'filter=metric.type="serviceruntime.googleapis.com/api/request_count" AND resource.type="consumed_api"' \
    --data-urlencode "interval.startTime=${START}" \
    --data-urlencode "interval.endTime=${END}" \
    --data-urlencode 'aggregation.alignmentPeriod=86400s' \
    --data-urlencode 'aggregation.perSeriesAligner=ALIGN_SUM' \
    --data-urlencode 'aggregation.crossSeriesReducer=REDUCE_SUM' \
    --data-urlencode 'aggregation.groupByFields=resource.label.credential_id' 2>/dev/null)
  # An error body or unparseable response is recorded, never silently read as "unused".
  # (A project with no traffic returns `{}` — no timeSeries, no error — and is fine.)
  if ! echo "$RESP" | jq -e 'type=="object" and (has("error")|not)' >/dev/null 2>&1 \
     || ! echo "$RESP" | jq '[ .timeSeries[]?
          | { cid:.resource.labels.credential_id,
              last:([ .points[]? | select(((.value.int64Value // .value.doubleValue // 0)|tonumber)>0)
                      | .interval.endTime ]|sort|last) }
          | select(.cid!=null and .last!=null) ] | map({(.cid):.last}) | add // {}' \
          > "${SESSION_DIR}/lastused.${P}.json"; then
    MSG=$(echo "$RESP" | jq -r '.error.message // empty | sub("[.]+$";"")' 2>/dev/null | tr -d '\n' | cut -c1-200)
    jq -nc --arg p "$P" --arg m "${MSG:-empty or unparseable response}" \
      '{context:"monitoring_last_used", message:("Monitoring last-used query failed for \($p): \($m). API keys in this project keep lastUsedAt=null; treat as unknown, not unused.")}' \
      >> "${SESSION_DIR}/monitoring-errors.json.parts"
    echo '{}' > "${SESSION_DIR}/lastused.${P}.json"
  fi
  jq -s '.[0]*.[1]' "${SESSION_DIR}/lastused.json" "${SESSION_DIR}/lastused.${P}.json" \
    > "${SESSION_DIR}/lastused.tmp" && mv "${SESSION_DIR}/lastused.tmp" "${SESSION_DIR}/lastused.json"
done

# Join: api_key.lastUsedAt = lastused["apikey:"+uid]; sa_key stays null (unchanged behaviour).
jq --slurpfile lu "${SESSION_DIR}/lastused.json" '
  [ .[] | if .type=="api_key"
          then .lastUsedAt = ($lu[0]["apikey:" + .uid] // null)
          else . end ]' "${SESSION_DIR}/creds.json" > "${SESSION_DIR}/creds.enriched.json"
mv "${SESSION_DIR}/creds.enriched.json" "${SESSION_DIR}/creds.json"
```

A failed Monitoring query leaves that project's keys at `lastUsedAt: null` and appends a `monitoring_last_used` entry to `errors[]` (collected in `monitoring-errors.json.parts`, merged in Step E). A key's `null` therefore means "no traffic in the window" only when no error names its project.

### Step E: Classify and write `audit.json`

Load the merged, enriched records from `creds.json`; for each, add `riskClass` + `riskReason` per the taxonomy table above, and **set the shell variable `CREDS_JSON`** to that classified JSON array (the bash block below references `$CREDS_JSON`). Then assemble the final JSON in the schema documented in `output.schema.json` and write atomically:

```bash
# Build scope from the coverage files (Tasks 2–4): scanned = CAI-covered ∪ (loop-attempted − skipped).
USER=$(jq -r '.user // empty' "${SESSION_DIR}/scope.local.json" 2>/dev/null)
[ -n "$USER" ] || USER=$(gcloud config get-value account 2>/dev/null)
SKIPPED=$(cat "${SESSION_DIR}/skipped.json" 2>/dev/null || echo '[]')
SCANNED=$(jq -n --argjson skip "$SKIPPED" \
  --rawfile cov "${SESSION_DIR}/covered.txt" \
  --rawfile unc "${SESSION_DIR}/uncovered.txt" '
  (($cov/"\n") + ($unc/"\n") | map(select(length>0))) as $all
  | ($skip | map(.projectId)) as $sk
  | ($all - $sk) | unique')
SCOPE_JSON=$(jq -n --arg u "$USER" --argjson scanned "$SCANNED" --argjson skipped "$SKIPPED" \
  '{user:$u, projectsScanned:$scanned, projectsSkipped:$skipped}')

# Errors: any the run collected (default none) + the CAI-fallback recommendations from Step C1
# + the Monitoring last-used failures from Step D.
ERRS_JSON="${ERRS_JSON:-[]}"
# cat first: a missing parts file must not throw away the other file's entries.
STEP_ERRS=$(cat "${SESSION_DIR}/cai-errors.json.parts" "${SESSION_DIR}/monitoring-errors.json.parts" 2>/dev/null \
            | jq -s '.' 2>/dev/null || echo '[]')

# $CREDS_JSON = the classified credential array (built above from creds.json, adding
# riskClass + riskReason per the taxonomy table). Assemble + write atomically.
jq -n --argjson creds "$CREDS_JSON" --argjson scope "$SCOPE_JSON" \
      --argjson errs "$ERRS_JSON" --argjson stepErrs "$STEP_ERRS" '
{
  schemaVersion: 1,
  generatedAt: (now | strftime("%Y-%m-%dT%H:%M:%SZ")),
  scope: $scope,
  credentials: $creds,
  errors: ($errs + $stepErrs)
}' > "${SESSION_DIR}/audit.json.tmp" \
  && mv "${SESSION_DIR}/audit.json.tmp" "${SESSION_DIR}/audit.json"
```

### Step F: Inline summary

```bash
# Runtime self-check: the produced audit.json must match output.schema.json.
SCHEMA=""
for c in "skills/gcp-credentials-audit/output.schema.json" \
         "${HOME}/.claude/skills/gcp-credentials-audit/output.schema.json"; do
  [ -f "$c" ] && SCHEMA="$c" && break
done
if [ -n "$SCHEMA" ] && python3 -m jsonschema -i "${SESSION_DIR}/audit.json" "$SCHEMA" >/dev/null 2>&1; then
  echo "audit.json: schema-valid"
else
  # Fallback structural check if the jsonschema CLI isn't installed.
  jq -e '.schemaVersion==1 and (.credentials|type=="array") and (.errors|type=="array")' \
    "${SESSION_DIR}/audit.json" >/dev/null \
    && echo "audit.json: structural check OK (install 'jsonschema' for full validation)" \
    || echo "audit.json: FAILED validation"
fi

CAI_N=$(sort -u "${SESSION_DIR}/covered.txt" 2>/dev/null | wc -l | tr -d ' ')
LOOP_N=$(sort -u "${SESSION_DIR}/uncovered.txt" 2>/dev/null | wc -l | tr -d ' ')
echo "Coverage: ${CAI_N} project(s) via CAI fast path, ${LOOP_N} via per-project fallback."
```

Print a one-paragraph summary:

> Audit complete. Scanned N projects (OK accessible / S skipped). Found A API keys ({{c}} CRITICAL, {{h}} HIGH, {{m}} MEDIUM, {{l}} LOW, {{i}} INFO) and B user-managed SA keys ({{by-risk}}). Output: `${SESSION_DIR}/audit.json`, and the CAI-vs-loop coverage split.

## Error handling

- Project inaccessible (`PERMISSION_DENIED`): record in `scope.projectsSkipped[]` with reason `"no_access"`; continue.
- API Keys API not enabled on a project: record `"apikeys_api_disabled"`; continue.
- CAI not enabled / no `cloudasset.viewer` on a scope: that scope's projects fall back to the per-project loop, and a `cai_fallback` recommendation (with the exact enable/grant commands) is appended to `errors[]`; continue. The audit **never** enables CAI itself (READ-ONLY).
- Monitoring query fails for a project: its keys keep `lastUsedAt = null`; a `monitoring_last_used` entry goes to `errors[]` (Step D).
- Any other unexpected error: append to `errors[]`; do not abort the audit.

## Parity mode (`AUDIT_VERIFY_PARITY=1`)

A one-time correctness check that the CAI fast path and the per-project loop produce the **same raw inventory**. Off by default (it runs both paths, defeating the speedup). When `AUDIT_VERIFY_PARITY=1`:

1. After Step C1, also run the Step C2 loop over the **covered** projects into a separate `creds.loopcheck.json` (do not let it touch `creds.json`).
2. Diff against the CAI records on the raw inventory fields only:

```bash
norm='sort_by(.uid // "\(.project)/\(.serviceAccount)/\(.keyId)")
      | map({type,project,uid,serviceAccount,keyId,createTime,restrictions})'
if diff <(jq -S "$norm" "${SESSION_DIR}/creds.cai.json") \
        <(jq -S "$norm" "${SESSION_DIR}/creds.loopcheck.json"); then
  echo "PARITY OK — CAI inventory matches the loop."
else
  echo "PARITY MISMATCH — investigate the field mapping before trusting the fast path."
fi
```

A mismatch is a real defect in the CAI field mapping; fix before relying on the fast path.
