---
name: k6-plan
description: Plan deterministic k6 performance tests from goals, SLA, and protocol context. Use when users ask to plan a load test, set up a stress/spike/soak strategy, or request a full k6 test blueprint. Route implementation output requests to k6-builder.
user-invocable: true
disable-model-invocation: false
license: MIT
metadata:
  version: 0.1.0
  category: performance-testing
  protocols: [http, grpc, browser]
---
- User says: "build a complete k6 test plan with SLA"

## Tool Discovery Protocol

At the beginning of the workflow, detect and use interaction tools in this order:

1. If `AskUserQuestion` exists, use it for required inputs.
2. Else if `mcp:sampling` or `create_message` exists, use native IDE modal interaction.
3. Else if `confirm_action` exists, use it for critical confirmations.
4. Else emit the exact fallback and end the turn:

```md
> [?] MISSING REQUIREMENT: Missing target, scenario, SLA, or protocol detail
missing: target, scenario type, SLA requirements, protocol
why: deterministic planning cannot proceed without baseline planning inputs
next_question: What target URL or endpoint should this plan use?
```

Do not continue plan generation after fallback.

## Interoperability Fallback Contract

When fallback is required, always use this portable payload shape:

```md
> [?] MISSING REQUIREMENT: <short missing requirement summary>
missing: <comma-separated missing fields>
why: <why plan generation cannot continue deterministically>
next_question: <single, specific question that unblocks the next step>
```

Do not emit final plan content after this fallback.

## Core Rules

<rules>
1. **Adaptive Question System**: When critical parameters are missing, start with the baseline planning questions and continue in the same question flow with any additional required questions:
   - What is the target URL/endpoint? (if `target` missing)
   - What scenario type do you need? Options: load, stress, spike, soak, smoke (if `scenario` missing)
   - What are your SLA requirements? Example: p95<500ms,error<1% (if `sla` missing)
   - What protocol should this test use? Options: http, grpc, browser (if `protocol` missing)
   
   **Edge case hardening**: When user input is ambiguous or conflicts with best practices:
   - If SLA thresholds conflict (e.g., "p95<100ms" for a high-latency service), ask clarification.
   - If scenario and SLA are mismatched (e.g., "smoke test with SLA p99<50ms"), flag and ask confirmation.
   - For gRPC plans: Always ask about TLS, metadata, and failure handling explicitly.

   Round contract:
   - **Round 1**: one consolidated baseline question block with all minimum required questions.
   - **Round 2**: one optional tie-break block only when a critical ambiguity remains after Round 1.
   - If required inputs are still unresolved after Round 2, emit the interoperability fallback and end the turn.

   **Provisional plan policy:**
   - Default behavior is strict certainty: do not generate provisional assumptions in final plan output.
   - If critical data is missing, return `unknown` for unresolved fields and ask one unblocker question.
   - Only generate provisional plans when the user explicitly asks for assumption-based output.
   - If scenario type is ambiguous, do not generate a provisional plan; ask clarification using the Clarification Output Contract.

   Clarification-mode hard stop:
   - When clarification mode is triggered, emit only the canonical clarification block and stop.
   - Do not append plan scaffolding, executor hints, thresholds, stage ideas, protocol tactics, or builder handoff details.
   - Treat any plan-like token leakage as a contract violation.

   Additional questions must be integrated into the same question system, not handled as a separate side flow:
   - Add an HTTP method question when `protocol=http` and the method cannot be inferred safely.
   - Add one or more authentication questions when auth is required or unknown and executable output depends on it.
   - Add more questions only inside Round 1 or the single Round 2 tie-break block when other critical ambiguities or missing requirements are detected.
   - Do not finalize the plan or builder handoff until all required questions from this same system are resolved.

2. **Load Profile Defaults** (when `profile` is not specified):
   - `minimal`: 5 VUs, 1m duration, smoke testing
   - `standard`: 25 VUs, 9m duration, realistic load
   - `aggressive`: 120 VUs, 14m duration, stress testing

3. **Output Format**: Primary output is a textual execution plan with:
   - Recommended executor type
   - VU count and stages
   - Duration estimate
   - SLA-derived thresholds
   - Protocol-specific recommendations
   - Data integration suggestions (CSV/JSON)
   - Exactly one deterministic `Next recommended step`

4. **Determinism**: Same inputs produce identical outputs every time.

5. **Compact-by-default responses**:
   - Keep plan output concise and practical.
   - Avoid long explanatory prose unless user requests detail.
   - Prefer short verified bullets and direct next action.
</rules>

## Verified Evidence Policy

1. Report only values backed by user-provided inputs or direct runtime/tool evidence.
2. Do not present inferred values as final facts.
3. If unresolved, mark as `unknown` and ask one unblocker question.
4. Keep assumptions out of final summaries unless user explicitly requests assumption-based mode.

## Terminology Contract

- **Scenario type** means the test objective shape (`load`, `stress`, `spike`, `soak`, `smoke`).
- **Profile** means default intensity presets (`minimal`, `standard`, `aggressive`) used when explicit `vus`/`duration` are missing.
- **Round** means one consolidated question block in the adaptive question system; baseline questions are Round 1 and the optional tie-break is Round 2.
- Scenario type selects the executor strategy; profile sets default intensity values.

## Language Policy

1. If user language is explicit, answer in that language.
2. If language is not explicit, default to English.
3. Keep command names, k6 metric keys, and code identifiers in English.

## Cloud Runtime Compatibility Gate

Cloud planning must be version-aware before emitting cloud commands, cloud options, or cloud validation guidance.

Required detection flow:

1. Resolve executable target.
2. Run `k6 version`.
3. Parse semantic version.
4. Classify runtime family deterministically:
   - `V0_53_TO_V1_5` for `>=0.53.0` and `<1.6.0`
   - `V1_6_PLUS_V1_X` for `>=1.6.0` and `<2.0.0`
   - `V2_0_PLUS` for `>=2.0.0`

Gate behavior:

1. If exact version is unknown or parse fails, stop cloud planning and ask for exact k6 version.
2. Do not invent synthetic cloud-family labels.
3. Preserve `k6_version` and `runtime_family` in builder handoff metadata.

## Cloud Planning Inputs

When cloud behavior is requested, ask these inputs in the same active question flow:

1. Execution mode: `cloud-run`, `cloud-streaming-local-execution`, or `local-only`.
2. Routing needs: stack routing, project routing, both, or none.
3. Whether zonal distribution is required.
4. If distribution is required, collect full `{ loadZone, percent }` entries.

## Cloud Authentication Readiness

When cloud execution or cloud-ready handoff is requested, plan for an explicit auth path:

1. Prefer `K6_CLOUD_TOKEN` for non-interactive execution.
2. If token-based auth is not available, require an interactive login path via `k6 cloud login` before execution.
3. Treat missing auth readiness as a blocker for cloud execution handoff, but not for non-executable planning discussion.
4. Keep auth and routing guidance in environment variables or explicit login steps; never assume a live cloud session exists.

## Cloud Version-Gated Behavior

1. `V0_53_TO_V1_5`:
   - Allow only `k6 cloud login`, `k6 cloud run`, and `k6 cloud run --local-execution`.
   - Do not emit stack/project workflow assumptions unless user explicitly targets >= v1.6.0.
   - Do not emit v2-only cloud options.
2. `V1_6_PLUS_V1_X`:
   - Allow the restricted v1 path above plus stack routing via `options.cloud.stackID` and `K6_CLOUD_STACK_ID`.
   - Keep cloud options constrained to proven v1 evidence.
3. `V2_0_PLUS`:
   - Allow verified v2 cloud options and cloud context vars.
   - Require stack routing for cloud command guidance.

## Cloud Distribution Validation

When `options.cloud.distribution` is present:

1. Every entry must include `loadZone` and `percent`.
2. Every `percent` must be an integer.
3. Sum of all `percent` values must be exactly `100`.
4. If any rule fails, stop runnable handoff and emit clarification/validation failure. Do not normalize automatically.

## Dashboard Policy

Apply deterministic recommendation:

1. CI/headless: `K6_WEB_DASHBOARD=false`
2. Local browser troubleshooting: `K6_WEB_DASHBOARD=true`
3. Local non-browser: default `K6_WEB_DASHBOARD=false` unless explicit opt-in
4. Otherwise default `false`

## Dynamic Capacity Protocol

Run this protocol before finalizing any plan that could lead to executable current-host k6 output or validation handoff. For pure `cloud-run`, local host capacity is advisory only and must not block the remote cloud recommendation unless the user also asks for local execution.

Cross-skill required fields:

- `execution_context`
- `machine_profile`
- `projected_load`
- `capacity_estimate`
- `risk_status`
- `safe_limit_recommendation`
- `scale_out_recommendation`

High-risk gate rule (mandatory):

- Before generating or orchestrating any script that projects more than `500` VUs on the current host, run host audit silently with `node skills/k6-plan/scripts/audit-host.js`.
- If Node.js is unavailable, use the Python fallback: `python3 skills/k6-plan/scripts/audit-host.py`.
- Parse stdout JSON and use that as the primary `machine_profile` evidence for this request.

Contextual deterministic formulas:

- `vus_max = (logical_cpu * cpu_factor) + (free_ram_gb * ram_factor)`
- `arrival_rate_max = floor(vus_max / max(projected_load.expected_iteration_duration_seconds, 1))`

Default context factors:

- `local`: `cpu_factor=50`, `ram_factor=10`
- `ci`: `cpu_factor=30`, `ram_factor=6`
- `container`: `cpu_factor=25`, `ram_factor=5`
- `cloud`: `cpu_factor=60`, `ram_factor=12`
- `distributed`: compute per node, then aggregate

Evaluation order:

1. Build `execution_context` from the declared environment (`local`, `ci`, `container`, `cloud`, or `distributed`) plus user constraints.
2. Determine whether the active load generator is the current host or remote cloud-managed infrastructure.
3. Derive `machine_profile` from current evidence only for current-host execution paths: `logical_cpu`, `free_ram_gb`, `fd_limit`, `ephemeral_port_budget`, environment type, and declared user restrictions.
4. If projected load is expected to exceed `500` VUs on the current host, run host audit (`node skills/k6-plan/scripts/audit-host.js`, fallback `python3 skills/k6-plan/scripts/audit-host.py`) and overwrite missing or stale machine evidence with audit output.
5. Add optional telemetry when available: prior k6 saturation, observed memory per VU, prior stable arrival rate, or prior port exhaustion signals.
6. Derive `projected_load` from the requested or defaulted executor shape: target VUs, arrival rate, duration, stages, and `expected_iteration_duration_seconds` for arrival-rate executors.
   - `projected_load.expected_iteration_duration_seconds` must come from explicit user input, prior measured telemetry, or a conservative `[assumption-based]` estimate called out in the plan.
   - If that field is unavailable, do not present `arrival_rate_max` as fully deterministic.
7. Calculate `capacity_estimate.vus_max` and `capacity_estimate.arrival_rate_max` from the current `machine_profile` using the contextual deterministic formulas when the current host generates load. Never use a universal fixed VU ceiling.
8. Classify `risk_status` as `SAFE`, `AT_RISK`, or `HIGH_RISK` against the current estimate for current-host execution.
9. Derive `safe_limit_recommendation` and `scale_out_recommendation`, including `additional_cpu_percent`, `additional_ram_gb`, and `additional_nodes`.
10. If execution mode is pure `cloud-run` and remote worker capacity is not verified, report remote capacity as `unknown` and keep local capacity advisory-only for optional local validation.

Incomplete-data rules:

- If critical machine inputs are missing, ask one clarification question when that is the cheapest unblocker.
- If the scenario is otherwise clear, continue with a conservative `[assumption-based]` estimate instead of inventing a global default capacity.
- Mark every derived field that depends on missing telemetry as `[assumption-based]` and state the missing evidence explicitly.
- For pure `cloud-run`, missing local machine evidence must not block remote execution planning; report remote capacity as `unknown` unless cloud worker constraints are explicitly provided.

Plan-stage behavior:

- Include all required fields above in the final plan.
- If `risk_status` is `AT_RISK` or `HIGH_RISK`, append the canonical alert exactly as written below.
- Do not recommend runnable single-node execution above `safe_limit_recommendation`.
- When projected load exceeds current capacity, recommend either a reduced safe limit or distributed execution.
- If `risk_status` is `HIGH_RISK`, stop local runnable guidance and return only a reduced local limit or distributed recommendation.
- For pure `cloud-run`, local host risk may inform optional dry-run advice but must not block the remote cloud recommendation.

Canonical alert format:

```md
LOAD GENERATOR CAPACITY ALERT
Risk Detected: The requested scenario ([X] VUs) exceeds the load generator operating limit ([Y] VUs).
Impact: Possible metric skew, TCP port exhaustion, or k6 process collapse.
Recommendation: Reduce the scenario to [Z] VUs or use distributed infrastructure with at least [N] additional nodes.
```

Determinism rules:

- `Y` must come from the current `capacity_estimate`.
- `Z` must come from the current `safe_limit_recommendation`.
- `N` must come from the current `scale_out_recommendation.additional_nodes`.
- The same request and machine evidence must produce the same capacity classification.

## HTTP Method Question

Before producing a final HTTP plan, add the method question to the same active question system:

1. Confirm primary method (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`) when endpoint behavior depends on method.
2. If method is missing and cannot be inferred, ask it as an additional required question before finalizing.
3. Reflect confirmed method in scenario steps, checks, and threshold rationale.

## Auth Discovery Questions

Before finalizing plan output or builder handoff parameters, add auth questions to the same active question system:

1. Detect whether authentication is required (Bearer token, API key, basic auth, mTLS, session cookie, or none).
2. If auth is required or still unknown for executable output, ask for auth mechanism and required variable names as additional required questions.
3. Never hard-code credentials in examples or generated scripts.
4. Prefer environment variables (`__ENV`) for auth inputs and list required variables.

## SLA-Scenario Coherence Validation

When both `scenario` and `sla` are available, run this coherence pass before finalizing output. This pass does not block plan generation; it produces explicit warnings and a confirmation prompt when needed.

1. `load` scenario:
   - If p95 target is higher than 500ms, emit INFO about potentially relaxed latency target.
   - If error bound is higher than 5%, emit WARNING about overly permissive failure rate for load tests.
2. `stress` scenario:
   - If latency target is ultra-strict (for example p99<100ms), emit WARNING about unrealistic stress constraints.
   - If error bound is stricter than 1%, emit WARNING because stress tests intentionally probe failure boundaries.
3. `spike` scenario:
   - If planned duration is greater than 10m, emit WARNING that spike tests should be short and abrupt.
4. `soak` scenario:
   - If SLA is stricter than load baseline defaults, emit WARNING that soak validates endurance, not peak latency.
5. `smoke` scenario:
   - If SLA includes strict percentile constraints (for example p99<50ms), emit WARNING that smoke does not validate sustained latency behavior.

After warning emission, ask one confirmation question:
`Do you want to keep these thresholds for this scenario type, or adjust them now?`

If user confirms to proceed, continue with the plan and keep a compact assumptions entry tagged `[provided override]`.

## SLA Consistency Across Multi-Environment

When planning for multiple environments (dev/staging/prod):

- Threshold values MUST BE IDENTICAL across all environments.
- VU counts MAY VARY per environment.
- Duration MAY VARY per environment.
- Performance SLA targets (p95, p99, error bounds) MUST NOT VARY per environment.

Rationale: SLA is a commitment and must remain coherent across environments. Relaxing SLA by environment creates non-comparable results and hides production risk.

Canonical cross-skill warning (must match `k6-builder` exactly):

`WARNING: SLA must be identical across environments to maintain testing coherence.`

Canonical enforcement flow (planning stage):

1. Detect single declared SLA plus per-environment threshold divergence request.
2. Emit the canonical warning string above.
3. Ask one confirmation question:
   - `Do you want to normalize all environment thresholds to the same SLA now?`
4. If user confirms normalization:
   - Continue planning with identical thresholds across dev/staging/prod.
5. If user rejects normalization:
   - Keep the plan as non-runnable planning guidance only.
   - Add assumptions tag `[provided override]` and explicit note:
     - `Builder-stage enforcement will reject runnable artifacts with per-environment SLA relaxation.`
   - Do not present relaxed thresholds as compliant defaults.

## Clarification Output Contract

When required inputs are missing and a clarification response is needed (not a provisional plan), use this exact format and nothing else:

```
missing: <comma-separated list of missing fields>
why: <one sentence explaining why these fields are required to proceed>
next_question: <single, specific question that unblocks the next step>
```

Rules:
- Use exactly these three fields — no additions, no removals.
- Do not mix plan fragments, partial executor recommendations, or scenario guesses into the clarification response. The clarification block must be self-contained.
- Keep `why` strictly unblocker-focused. Do not mention executor names, thresholds, VU counts, stages, protocol tactics, or builder handoff details.
- In clarification mode, avoid plan-like tokens in prose (`executor`, `thresholds`, `stages`, `vus`, `ramping`, `constant-vus`, `arrival-rate`).
- If multiple fields are missing, list them all in `missing` but ask only the single most-blocking question in `next_question`.
- After emitting the clarification block, end the response. Do not add caveats or partial analysis below it.

## Required k6 Invariants

Always enforce these validations before returning the plan:

1. **Thresholds are required**
   - Parse thresholds from SLA if provided.
   - If SLA is not provided, derive profile-based defaults and show them explicitly.
2. **Load profile is required**
   - Plan must include explicit VUs and duration (or explicit stage set with equivalent duration and target VUs).
   - If `vus`/`duration` are missing, derive from profile defaults and state assumptions.
   - When request is multi-environment (dev/staging/prod), VU counts must be explicit and distinct per environment.
3. **Runnable URL hard-coding is forbidden**
   - Do not generate runnable scripts with fixed live target URLs.
   - Require `__ENV.BASE_URL` (or equivalent) for executable output.
   - If target is missing, ask for it instead of using a default live URL.
4. **Parameter coherence is required**
   - Derived or explicit profile values must map to explicit `vus` and `duration`, or explicit staged equivalents.
   - If write methods are planned (`POST`/`PUT`/`PATCH`), payload assumptions and expected status must be explicit.
5. **Secrets and runnable safety are required**
   - Never hard-code credentials or tokens in runnable snippets.
   - Require environment variables (`__ENV`) for auth inputs.

6. **Protocol-specific technical quality is required**
   - gRPC plans must always include: `grpc_req_duration` metric, `client.connect()` in setup or default, and guaranteed `client.close()` on all execution paths (teardown or `try/finally`). Omitting any of these from a gRPC plan is a planning error.
   - HTTP plans must always include: `http_req_duration` threshold, explicit timeout guidance, and `checks` for response validation.
   - Browser plans must always include: page/context lifecycle management and at least one Web Vitals metric recommendation.
   - These are not stylistic preferences — they are required outputs for their respective plan types.
7. **Journey/state fidelity is required**
   - For multi-step user journeys, preserve the full requested sequence in order; do not merge, reorder, or drop steps.
   - Include a session/data-state handling strategy when the journey depends on auth/session, cart state, or correlated user data.
   - If the user provides an end-to-end KPI (for example checkout p95<5s), include it explicitly in Thresholds and map it to the relevant k6 metric.
   - **Correlation map required for flows with 3+ steps that extract data**: For every step that produces a value consumed by a later step, the plan must document it explicitly using this structure:
     ```
     correlation_map:
       - step: login → extracts: access_token → used_by: [createOrder, applyCoupon, pay, verify]
       - step: createOrder → extracts: orderId → used_by: [applyCoupon, pay, verify]
       - step: applyCoupon → extracts: discountApplied → used_by: [pay, verify]
     ```
   - For each extraction: name the variable, its source (JSON field or response header), and every downstream step that consumes it. Generic mention of "correlation" without this level of detail is insufficient — it is a planning error for flows with 3+ chained data dependencies.
8. **Cloud compatibility invariants are required (when cloud mode is requested)**
   - Exact k6 version must be detected and classified before cloud guidance.
   - Output must match runtime family cloud allowlist.
   - Distribution math must pass strict 100% validation.
   - Cloud auth and routing guidance must use environment variables (`K6_CLOUD_TOKEN`, `K6_CLOUD_STACK_ID`, `K6_CLOUD_PROJECT_ID`).

## Output Contract

Every response must include these sections in order:

1. Planning Inputs Summary
2. Executor Recommendation
3. Load Profile (explicit or derived)
4. Thresholds (SLA-derived or defaults)
5. Protocol-Specific Notes
6. Guardrail Validation
7. Next recommended step

Dynamic capacity reporting requirements:

- `Planning Inputs Summary` must include `execution_context`.
- `Load Profile` must include `projected_load` and `machine_profile`.
- `Protocol-Specific Notes` must include `capacity_estimate`, `risk_status`, `safe_limit_recommendation`, and `scale_out_recommendation`.
- When `risk_status` is `AT_RISK` or `HIGH_RISK`, `Protocol-Specific Notes` must include the canonical capacity alert with current calculated values.

Guardrail Validation checklist (minimum):

- [ ] Final summary includes only verified facts or explicit `unknown`
- [ ] Missing critical data is surfaced with one unblocker question
- [ ] No assumption-based values are presented as confirmed

## Scenario to Executor Mapping

<executor-logic>
- **load**: ramping-vus with gradual ramp-up/down
- **stress**: ramping-vus with aggressive progression beyond capacity
- **spike**: ramping-vus with rapid surge to peak
- **soak**: constant-vus or ramping-vus sustained for extended duration
- **smoke**: constant-vus with minimal load
</executor-logic>

## SLA Parsing Rules

<sla-rules>
Parse SLA string to extract threshold conditions. Supported syntax:

### Simple Conditions (single metric)
- `p95<Xms` → 95th percentile latency threshold
- `p99<Xms` → 99th percentile latency threshold
- `error<X%` or `rate<X%` → Error rate threshold

### Comma-Separated Lists (implicit AND)
- `p95<500ms,p99<900ms,error<1%` → All conditions must be met
- Commas separate independent thresholds
- All listed thresholds are combined in final configuration

### Explicit AND Conditions (multiple conditions on same metric)
- `p95<500ms AND p95>100ms` → p95 must be between 100ms and 500ms
- Multiple constraints on the same metric (range validation)
- Translates to multiple threshold entries for the same k6 metric

**Note:** OR logic is not supported in this skill behavior. All conditions are treated as mandatory (AND).

### Parsing Examples
- Input: `p95<400ms,error<1%` → p95 AND error rate thresholds
- Input: `p95<500ms AND p99<900ms` → Both percentiles required
- Input: `p99<200ms` → p99 threshold must be emitted exactly (no conversion to p95-only)
- Input: `p95<2s` → Single threshold with p99 inferred (see sla-defaults.md)

Defaults per profile when SLA is not provided:
- `minimal`: p95<800ms, error<2%
- `standard`: p95<500ms, error<1%
- `aggressive`: p95<300ms, p99<700ms, error<0.5%, checks>99%
</sla-rules>

## Protocol-Specific Generation

<protocol-patterns>
### HTTP
- Use `http.get()`, `http.post()`, `http.batch()` for parallel requests
- Metrics: `http_req_duration`, `http_req_failed`
- Include explicit timeout guidance (baseline `timeout: '30s'`) for executable HTTP examples; missing timeout should be validated as `WARNING`.
- Tag requests: `tags: { name: 'api-call' }`

### gRPC
- Use `grpc.Client()`, `client.load()`, `client.connect()`, `client.invoke()`
- Metrics: `grpc_req_duration`, `grpc_req_failed`
- Always close connections on all execution paths (teardown or `try/finally`)
- Handle metadata for authentication
- Connection lifecycle guidance is mandatory:
   - Create/load client once, outside the hot iteration path.
   - Do not reconnect on every iteration unless explicitly justified.
   - Prefer `teardown()` for `client.close()` to avoid leaked connections.
- TLS guidance must be explicit:
   - Secure endpoints should use TLS-enabled connection options.
   - Non-TLS/plaintext mode must be marked as test-only assumption.
- Metadata guidance must include concrete key examples and env-var-driven token usage.
- Timeout guidance must include both connection timeout and request timeout recommendations.
- Flag anti-pattern: reconnect-per-iteration as a performance and reliability risk.

### Browser
- Use `browser.newContext()`, `context.newPage()`, `page.goto()`, `page.waitForSelector()`
- Always close page/context at iteration end
- Prefer `data-testid` selectors
- Collect Web Vitals when relevant
</protocol-patterns>

## Progressive Disclosure

Keep this file focused on core planning workflow. Place deep guidance in:

- `skills/k6-plan/references/README.md`

## Workflow

When user invokes this skill:

1. Parse provided parameters (`target`, `scenario`, `sla`, `profile`, `protocol`, `duration`, `vus`, `output`).
2. Run Tool Discovery Protocol when critical inputs are missing.
3. Start the Adaptive Question System with baseline questions when `target`, `scenario`, `sla`, or `protocol` are missing.
   - If clarification mode is selected, emit only the canonical `missing`/`why`/`next_question` block and end the response immediately.
   - In clarification mode, reject any appended plan fragments, executor suggestions, threshold snippets, staged load drafts, or builder handoff notes.
4. Apply load profile defaults based on `profile`.
5. Add an HTTP method question to the same question system when protocol is HTTP and the method is still ambiguous.
6. Add auth questions to the same question system when auth is required, unknown, or otherwise blocks executable output.
7. Add more questions in the same system if other critical ambiguities or missing requirements are detected.
8. Select executor based on scenario type.
9. Parse SLA thresholds or apply deterministic defaults.
10. Run the Dynamic Capacity Protocol using current machine evidence and projected workload only when the selected execution path uses the current host as the load generator.
11. If cloud execution or cloud-ready handoff is requested, add explicit cloud auth readiness guidance (`K6_CLOUD_TOKEN` or `k6 cloud login`) before execution advice.
12. For journey-style plans, preserve the full requested sequence and add session/data-state handling strategy.
13. Validate explicit or derived VUs and duration.
14. Generate textual plan with recommendations.
15. Validate output structure using the Output Contract section order.
16. Add exactly one deterministic `Next recommended step` based on first unresolved dependency.
17. If `output=script` or user explicitly requests runnable code, route to k6-builder with accumulated plan parameters (`target`, `scenario`, `sla`, `protocol`, `profile`, `method`, `auth`, `duration`, `vus`) plus the current capacity assessment fields.
18. Return the plan and assumptions summary.

## Local Evaluation Workspace Policy

For official skill evaluation runs in this repository:

- Store artifacts under `skills/k6-plan/k6-plan-workspace/iteration-N/`.
- Keep each run isolated inside its own `iteration-N` directory.
- Treat benchmark outputs, grading files, timing files, and generated responses as non-versioned execution artifacts.
