---
name: k6-validate
description: Validate k6 scripts against structural, performance, and reliability standards. Use when users ask to validate a k6 script, review k6 test quality, or detect anti-patterns before execution.
user-invocable: true
disable-model-invocation: false
license: MIT
metadata:
  version: 0.1.0
  category: performance-testing
---
- User says: "find issues in my k6 scenario"
- User says: "check if my thresholds and load profile are correct"

## Tool Discovery Protocol

At the beginning of the workflow, detect and use interaction tools in this order:

1. If `AskUserQuestion` exists, use it for required inputs.
2. Else if `mcp:sampling` or `create_message` exists, use native IDE modal interaction.
3. Else if `confirm_action` exists, use it for critical confirmations.
4. Else emit the exact fallback and end the turn:

```md
> [?] MISSING REQUIREMENT: Missing script path or validation scope
missing: script path, validation scope
why: deterministic validation report cannot run without target and scope
next_question: Which script should be validated?
```

Do not continue validation after fallback.

## Interoperability Fallback Contract

When fallback is required, always use this portable payload shape:

```md
> [?] MISSING REQUIREMENT: <short missing requirement summary>
missing: <comma-separated missing fields>
why: <why validation cannot continue deterministically>
next_question: <single, specific question that unblocks the next step>
```

Do not emit final validation findings after this fallback.

## Verified Evidence Policy

1. Report only findings supported by direct script evidence, explicit user context, or direct runtime/tool evidence.
2. Do not state inferred conditions as facts in `Validation Summary`.
3. If a required fact cannot be verified, mark it `unknown` and include a single unblocker question in `Scope and Assumptions`.
4. Keep language compact and action-oriented; avoid narrative repetition.
5. Never reproduce credential material from input scripts. For tokens, passwords, API keys, cookies, auth headers, connection strings, or secret query values, use redacted placeholders plus line references. Preferred placeholders: `******` (default) or `<REDACTED_SECRET>` when typed labeling is needed.

## Language Policy

1. If user language is explicit, answer in that language.
2. If language is not explicit, default to English.
3. Keep command names, k6 metric keys, and code identifiers in English.

## Cloud Compatibility Validation

When a target artifact declares cloud execution, validator must enforce version-safe behavior.

Required runtime classification for cloud checks:

1. Parse or receive exact k6 version from context/handoff.
2. Classify runtime family deterministically:
   - `V0_53_TO_V1_5` for `>=0.53.0` and `<1.6.0`
   - `V1_6_PLUS_V1_X` for `>=1.6.0` and `<2.0.0`
   - `V2_0_PLUS` for `>=2.0.0`

Validation rules:

1. Reject artifacts claiming v2 cloud behavior when runtime family is below `v2.0.0`.
2. Verify cloud auth/routing variables when cloud mode is declared:
   - `K6_CLOUD_TOKEN`
   - `K6_CLOUD_STACK_ID` when stack routing is required
   - `K6_CLOUD_PROJECT_ID` when project routing is required
3. Flag hard-coded tokens as `ERROR`.
4. Flag undocumented cloud options/flags as `ERROR`.
5. Enforce cloud option allowlist parity with builder:
   - `options.cloud.projectID`
   - `options.cloud.stackID`
   - `options.cloud.distribution`
   - `options.cloud.deleteSensitiveData`
   - `options.cloud.staticIPs`
   - `options.cloud.drop_metrics`
   - `options.cloud.drop_tags`
   - `options.cloud.keep_tags`
6. Validate cloud distribution entries:
   - every entry includes `loadZone` and `percent`
   - `percent` values are integers
   - total percent equals `100`

## Cloud Paid Execution Compliance

When validating cloud execution guidance or run procedures, enforce cost/idempotency guardrails:

1. Flag `ERROR` if output proposes more than one cloud execution without explicit user confirmation.
2. Flag `ERROR` if output proposes rerun while an existing run URL is present with `Running` status.
3. Flag `ERROR` if output uses truncated terminal output as a reason to relaunch instead of checking the same run identity.
4. Require `Cloud Execution Safety` evidence:
   - `run_count`
   - `first_run_url`
   - `rerun_requested_by_user`
   - `cost_confirmation`
5. Flag `ERROR` when rerun is requested by user but `cost_confirmation` is missing or `no`.
6. Flag `WARNING` when cloud mode is declared but run identity (`run_url`/`run_id`) is not traceable.

## Terminology Contract

- **Scenario type** means the test objective shape (`load`, `stress`, `spike`, `soak`, `smoke`) used to select executor intent.
- **Profile** means the expected intensity preset (`minimal`, `standard`, `aggressive`) used to evaluate whether `vus`, `duration`, and thresholds fit the intended load level.
- **Recommended profile** in validation references is advisory mapping from scenario type to default intensity, not a replacement for explicit user-provided values.
- When both scenario type and profile are provided, validate executor fit against scenario type first and threshold/load intensity fit against profile second.

## Dashboard Policy

Apply deterministic recommendation:

1. CI/headless: `K6_WEB_DASHBOARD=false`
2. Local browser troubleshooting: `K6_WEB_DASHBOARD=true`
3. Local non-browser: default `K6_WEB_DASHBOARD=false` unless explicit opt-in
4. Otherwise default `false`

## Dynamic Capacity Protocol

Audit this protocol whenever the input is an executable k6 artifact, a runnable plan, or a validation request that includes capacity claims. For pure `cloud-run`, missing local host capacity evidence must not by itself fail validation unless the artifact also claims local execution capacity.

Cross-skill required fields:

- `execution_context`
- `machine_profile`
- `projected_load`
- `capacity_estimate`
- `risk_status`
- `safe_limit_recommendation`
- `scale_out_recommendation`

High-risk gate audit expectation:

- If projected load exceeds `500` VUs on the current host, validation must expect evidence that host audit was executed before generation (`node skills/k6-validate/scripts/audit-host.js`, or `python3 skills/k6-validate/scripts/audit-host.py` when Node.js is unavailable).
- Missing pre-generation audit evidence for `>500` VU current-host scenarios is a validation failure for executable artifacts.

Contextual deterministic formulas (audit target):

- `vus_max = (logical_cpu * cpu_factor) + (free_ram_gb * ram_factor)`
- `arrival_rate_max = floor(vus_max / max(projected_load.expected_iteration_duration_seconds, 1))`

Default context factors to validate:

- `local`: `cpu_factor=50`, `ram_factor=10`
- `ci`: `cpu_factor=30`, `ram_factor=6`
- `container`: `cpu_factor=25`, `ram_factor=5`
- `cloud`: `cpu_factor=60`, `ram_factor=12`
- `distributed`: per-node estimate aggregated

Validation expectations:

1. `execution_context` must identify whether the run is `local`, `ci`, `container`, `cloud`, or `distributed`, and whether the active load generator is current-host or remote cloud-managed.
2. `machine_profile` must reflect current evidence when the current host generates load: `logical_cpu`, `free_ram_gb`, `fd_limit`, `ephemeral_port_budget`, environment type, and declared user restrictions.
3. `projected_load` must reflect the actual executor shape being reviewed: target VUs, arrival rate, duration, stages, and `expected_iteration_duration_seconds` for arrival-rate executors.
   - `projected_load.expected_iteration_duration_seconds` must come from explicit user input, prior measured telemetry, or a conservative `[assumption-based]` estimate.
   - If that field is missing, validation must treat `arrival_rate_max` as non-deterministic and report the gap.
4. `capacity_estimate.vus_max` and `capacity_estimate.arrival_rate_max` must be tied to the current `machine_profile`, not to a universal fixed threshold.
5. `risk_status` must be coherent with the numeric relationship between `projected_load` and `capacity_estimate`.
6. `safe_limit_recommendation` and `scale_out_recommendation` must include `additional_cpu_percent`, `additional_ram_gb`, and `additional_nodes` when risk is present.
7. For `projected_load.target_vus > 500` on the current host, pre-generation host audit evidence must be present and consistent with `machine_profile`.
8. For pure `cloud-run`, remote cloud-worker capacity may remain `unknown`; local host capacity is advisory unless the artifact also includes local execution guidance.

Required formula checks:

- VU-driven: `additional_nodes = ceil(projected_load.target_vus / capacity_estimate.vus_max) - 1`
- Rate-driven: `additional_nodes = ceil(projected_load.target_arrival_rate / capacity_estimate.arrival_rate_max) - 1`
- Clamp `additional_nodes` at `0` minimum.

Canonical alert requirement when risk exists:

```md
LOAD GENERATOR CAPACITY ALERT
Risk Detected: The requested scenario ([X] VUs) exceeds the load generator operating limit ([Y] VUs).
Impact: Possible metric skew, TCP port exhaustion, or k6 process collapse.
Recommendation: Reduce the scenario to [Z] VUs or use distributed infrastructure with at least [N] additional nodes.
```

Incomplete-data rules:

- If a field is missing, accept a conservative `[assumption-based]` substitute only when the missing evidence is called out explicitly.
- If executable output claims `SAFE` without enough machine evidence, report that as a validation failure.
- If executable output claims `AT_RISK` or `HIGH_RISK` with incomplete machine evidence, report that the risk assessment is unreliable until missing evidence is provided.
- If runtime latency indicates overload (for example heavy tail growth, timeout spikes, or saturation signals), warn about potential coordinated omission even when pre-generation capacity evidence exists.
- For pure `cloud-run`, do not fail validation solely because local machine evidence is absent; fail only when the artifact incorrectly presents local-capacity facts as verified or blocks remote execution on local limits.

## Validation Rules

<validation-rules>
1. **Syntax and Structure**:
   - `export const options` correctly defined
   - `export default function` present
   - Thresholds configured
   - Import statements valid using explicit usage-based minimum checklist:
     - require `k6/http` when `http.*` is used
     - require `k6` when `check` or `sleep` is used
     - require `k6/grpc` when gRPC APIs are used
     - require `k6/browser` when browser automation APIs are used
   - For broader module compatibility and allowed import coverage, cross-check `references/goja-k6-compatibility-matrix.md`.

2. **Performance Best Practices**:
   - Sleep between iterations (avoid tight loops); if missing, report at least `WARNING`
   - Checks implemented for assertions; if absent, report `WARNING`
   - Timeouts set on requests
   - Tagged requests for metric segmentation; if missing for multi-endpoint flows, report `WARNING`
   - Profile/load-context clarity present (scenario type and expected profile intensity are inferable); if missing, report `WARNING`
   - Capacity-assessment clarity present for executable or near-executable outputs; if missing, report at least `WARNING`
   - Runtime-risk awareness present: when high latency tail or error bursts appear, include a coordinated-omission caution tied to runtime stress vs agent-time audit.

3. **Protocol-Specific**:
   - HTTP: timeouts set, checks included
   - gRPC: connections properly closed
   - gRPC: flag `client.connect()` outside `default function`, `setup()`, or `teardown()` as `WARNING` (connection lifecycle leakage risk)
   - Browser: page/context closure in all execution paths (success, catch, finally, and early return paths)
   - WebSocket: socket lifecycle hygiene (`on('open')`, `on('error')`, graceful close path, and bounded session duration)
   - Browser: if page/context closure is missing in any iteration path, report `WARNING`
   - Browser lifecycle path analysis is mandatory:
     - Track each `newPage()` / `newContext()` creation.
     - Evaluate all exits after creation (normal completion, `return`, `throw`, catch branches).
     - If any path lacks corresponding `.close()`, emit `WARNING` with path evidence.
     - Prefer `try/finally` remediation in `Suggested Fixes`.

4. **Anti-Patterns to Flag**:
   - Hard-coded credentials
   - Hard-coded production URLs (for example `https://api.prod...`) in runnable scripts without `__ENV` control
   - Insecure hard-coded environment defaults/fallbacks in runnable scripts (without `__ENV` fallback)
   - Unbounded loops
   - Synchronous waits without reason
   - Silent `catch` blocks that swallow errors
   - Unsafe parsing without guarded failure handling
   - Quality violations mapped to static-analysis concerns (including S7726-class findings)
   - **Anonymous default export function** — `export default function() {}` without a name is a quality violation. Flag as `WARNING`: "Default export function should be named for traceability and debuggability. Example: `export default function runLoad() {}`". The naming convention is `run<ScenarioType>` or `run<Protocol><ScenarioType>`.
</validation-rules>

## Required k6 Invariants

Always enforce these validations as mandatory checks:

1. **Thresholds are required**
   - Flag as error when thresholds are missing.
   - If user provides explicit SLA values in the validation prompt/context, compare thresholds against that SLA.
   - Flag as warning when thresholds exist but are more lax than stated SLA.
   - For multi-environment artifacts with one declared SLA, threshold divergence across environments is `ERROR` because it violates cross-env SLA coherence expected by `k6-builder`.
2. **Load profile is required**
   - Flag as error when no explicit load profile exists.
   - Require explicit `vus` and `duration` for time-based cases, or clear equivalent (`stages`, `iterations` + `vus`) for scenario-based definitions.
3. **Parameter coherence is required**
   - If arrival-rate parameters exist, validate `preAllocatedVUs <= maxVUs`.
   - If staged scenarios exist, validate non-empty stages with explicit duration per stage.
4. **Secrets and runnable safety are required**
   - Flag hard-coded credentials/tokens as error.
   - Flag insecure runnable defaults for secrets as error or warning based on impact.
   - Flag hard-coded production URLs without `__ENV` control as at least `WARNING` (elevate to `ERROR` when credentials or sensitive paths are coupled).
5. **Lifecycle hygiene is required**
   - Browser scripts must close `page`/`context` in all execution paths.
   - gRPC scripts must show connect/invoke/close lifecycle consistency.
   - WebSocket scripts must include open/message/error/close handling and an explicit bounded lifetime.
6. **Dynamic capacity assessment is required for executable outputs**
   - Flag as error when `execution_context`, `machine_profile`, `projected_load`, or `capacity_estimate` is missing without explicit `[assumption-based]` justification for current-host execution artifacts.
   - Flag as error when `risk_status` contradicts the numeric comparison between projected load and current capacity.
   - Flag as error when `AT_RISK` or `HIGH_RISK` outputs omit the canonical capacity alert.
   - Flag as error when `additional_nodes` does not match the required formula for VU-driven or rate-driven execution.
   - Flag as warning when additional CPU or RAM guidance is omitted for `AT_RISK` or `HIGH_RISK` outputs.
   - For pure `cloud-run`, treat remote capacity as `unknown` unless verified cloud-worker evidence exists; local capacity becomes advisory-only.
7. **Cloud compatibility is required for cloud artifacts**
   - Flag as error when cloud runtime family is unknown for cloud artifact claims.
   - Flag as error when cloud options exceed the runtime-family allowlist.
   - Flag as error when cloud distribution math is invalid.
   - Flag as error when cloud mode is declared without explicit auth path (`K6_CLOUD_TOKEN` or `k6 cloud login` guidance).
8. **Cloud paid execution guardrail compliance is required when cloud runs are present**
   - Flag as error when multiple paid cloud runs are proposed without explicit user confirmation.
   - Flag as error when rerun is proposed despite an existing running run URL.
   - Flag as error when rerun is proposed for truncated output instead of same-run status recovery.
   - Flag as error when `Cloud Execution Safety` evidence is missing for cloud run flows.

## Severity Assignment Rules

- `ERROR`: mandatory invariant failures, hard safety/security violations, or incoherent capacity math.
- `WARNING`: quality/performance hygiene gaps that do not invalidate core correctness.
- `INFO`: optional non-blocking improvements.
- Every finding row must carry exactly one severity label from `ERROR`, `WARNING`, or `INFO`.
- A report may contain one, two, or three severity levels depending on findings; do not force all three levels to appear.

## Output Contract

Every validation response must include these sections in order:

Output artifact requirements:

- Use a single stable output artifact name: `validation-report.md`.
- Use Markdown as the required output format.
- Use exactly these H2 section headers in this order — no sections may be added, removed, reordered, or renamed:
   1. `## Validation Summary`
   2. `## Scope and Assumptions`
   3. `## Mandatory Invariant Results`
   4. `## Detailed Findings`
   5. `## Suggested Fixes`
   6. `## Next Step`
- `## Validation Summary` must always begin with a status badge on its own line: `**Status: PASS**`, `**Status: WARN**`, or `**Status: FAIL**`.
- `## Mandatory Invariant Results` must include a checklist item for each invariant from `Required k6 Invariants`, even if the result is ✅ pass.
- `## Detailed Findings` must group entries by severity in this order: 🔴 CRITICAL (`ERROR`) → 🟡 WARNING → ℹ️ INFO.
- In each severity group, sort by impact first, then line order.
- Every reported finding must include exactly one valid severity label (`ERROR`, `WARNING`, or `INFO`).
- Do not require all three severity levels to appear in the same report.
- For dynamic-capacity audits with missing machine evidence in `AT_RISK`/`HIGH_RISK` outputs, include the term `unreliable` explicitly in the relevant finding text.
- `## Suggested Fixes` must include a compact fix-priority matrix with counts and estimated time-to-fix per severity.

**Output budget:**
- Sections `Validation Summary` + `Mandatory Invariant Results` + `Detailed Findings` combined must target ≤ 600 tokens total.
- Use a compact findings table with these columns: `#` · `Severity` · `Finding` · `Recommended Fix` (one-liner max).
- Keep `Validation Summary` to verified facts only; unresolved items must be `unknown`.
- Extended explanations, code examples, and multi-step remediation instructions belong exclusively in `Suggested Fixes`. Each fix should include:
  - `issue`: The problem detected
  - `severity`: ERROR, WARNING, or INFO
  - `evidence`: Sanitized code snippet or line reference showing the issue (must redact secrets/sensitive literals)
  - `fix_snippet`: Executable corrected code (when applicable) that uses safe placeholders or `__ENV` variables; never copy credential literals from the input
   - `estimated_time`: short estimate (for example `~5 min`)
- Do not repeat finding descriptions between `Detailed Findings` and `Suggested Fixes` — `Detailed Findings` identifies; `Suggested Fixes` remediates.
- For credential findings, identify secret type + location and keep values fully redacted in all sections.
- **Token budget rule**: If combined findings exceed token budget, deprioritize INFO-level findings; ERROR and WARNING must always be reported.
- **Compactness rule**: If section content is already actionable, do not add explanatory filler.

For common anti-patterns, point to `skills/k6-validate/references/remediation-playbooks.md` and include the matching playbook name.

**Findings table format:**

| # | Severity | Finding | Recommended Fix |
|---|---|---|---|
| 1 | ERROR | Missing thresholds | Add `thresholds` block to `options` |
| 2 | WARNING | Anonymous default function | Rename to `export default function runLoad()` |

Under the table, include this compact template:

```md
### 🔴 CRITICAL (Fix Immediately)
- <highest-impact findings only>

### 🟡 WARNING (Fix Soon)
- <quality/perf risks>

### ℹ️ INFO (Optional)
- <non-blocking improvements>
```

In `Suggested Fixes`, append:

```md
## Fix Priority Matrix

| Priority | Category | Count | Estimated Time |
|---|---|---:|---|
| 🔴 CRITICAL | Security/Safety/Correctness | <n> | <total> |
| 🟡 WARNING | Quality/Performance | <n> | <total> |
| ℹ️ INFO | Best Practice | <n> | <total> |
```

## Progressive Disclosure

Keep this file focused on validation workflow. Place deep guidance in:

- `skills/k6-validate/references/README.md`

## Workflow

1. Parse validation target (`script`) and optional context (`protocol`, `sla`, scenario type, profile).
2. Run Tool Discovery Protocol if required input is missing.
3. Validate syntax and structure.
4. Validate performance best practices and protocol-specific rules.
5. Enforce required threshold, load-profile, and lifecycle-hygiene invariants.
6. Audit the Dynamic Capacity Protocol and verify formula coherence when current-host capacity claims are present or required, including mandatory pre-generation host-audit evidence for current-host projected loads above 500 VUs.
7. Audit Cloud Compatibility Validation: version-family match, cloud allowlist, auth/routing completeness, blocking login readiness, and distribution math.
8. Audit Cloud Paid Execution Compliance: single paid run policy, rerun confirmation, same-run recovery, and `Cloud Execution Safety` traceability.
9. If explicit SLA is present, compare script thresholds against the declared SLA and emit `WARNING` for more lax thresholds.
10. For browser scripts, run path-based closure analysis for `page/context` resources and flag any non-closed path.
11. Run quality-hardening checks (silent catch, unsafe parse, static-analysis signals, hard-coded production URLs, missing checks/sleep/tags).
12. Reference remediation playbooks for every fixable finding that matches a known anti-pattern.
13. Return deterministic report in `validation-report.md` using Markdown and the Output Contract section order.

## Local Evaluation Workspace Policy

For official skill evaluation runs in this repository:

- Store artifacts under `skills/k6-validate/k6-validate-workspace/iteration-N/`.
- Keep each run isolated inside its own `iteration-N` directory.
- Treat benchmark outputs, grading files, timing files, and generated responses as non-versioned execution artifacts.
