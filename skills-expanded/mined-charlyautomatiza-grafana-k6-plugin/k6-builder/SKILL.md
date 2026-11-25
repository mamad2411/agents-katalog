---
name: k6-builder
description: Build runnable k6 artifacts from a plan or direct requirements. Use when users ask to generate k6 scripts, choose/apply executors in runnable options, or create single/multi-environment configs. Prefer this skill for any implementation output request, even if the user also mentions "executor" or "config".
user-invocable: true
disable-model-invocation: false
license: MIT
metadata:
   version: 0.1.0
   category: performance-testing
   protocols: [http, grpc, browser, websocket]
---
- User says: "generate runnable k6 script for this endpoint"
- User says: "build dev/staging/prod config with thresholds"
- User says: "which executor should I use and give me final options"

## Mission

Generate runnable k6 artifacts safely and deterministically:
- script code
- scenario/options configuration
- single and multi-environment setup

Do not switch to planning-only discussion when user asked for implementation output.

## Tool Discovery Protocol

At the beginning of the workflow, detect and use interaction tools in this order:

1. If `AskUserQuestion` exists, use it for required inputs.
2. Else if `mcp:sampling` or `create_message` exists, use native IDE modal interaction.
3. Else if `confirm_action` exists, use it for critical confirmations.
4. Else emit the exact fallback and end the turn:

```md
> [?] MISSING REQUIREMENT: Missing build input for runnable artifacts
missing: target, scenario type, SLA requirements, protocol
why: deterministic generation cannot proceed safely without minimum build inputs
next_question: What target URL or endpoint should this build use?
```

Do not continue generation after fallback.

## Interoperability Fallback Contract

When fallback is required, always use this portable payload shape:

```md
> [?] MISSING REQUIREMENT: <short missing requirement summary>
missing: <comma-separated missing fields>
why: <why generation cannot continue deterministically>
next_question: <single, specific question that unblocks the next step>
```

Do not emit final artifact content after this fallback.

## Core Rules

<rules>
1. **Adaptive Question System**: When critical parameters are missing, start with baseline planning questions and continue in the same question flow with any additional required questions:
   - What is the target URL/endpoint? (if `target` missing)
   - What scenario type do you need? Options: load, stress, spike, soak, smoke (if `scenario` missing)
   - What are your SLA requirements? Example: p95<500ms,error<1% (if `sla` missing)
   - What protocol should this test use? Options: http, grpc, browser (if `protocol` missing)

   Round contract:
   - **Round 1**: one consolidated baseline question block with all minimum required questions.
   - **Round 2**: one optional tie-break block only when a critical ambiguity remains after Round 1.
   - If required inputs are still unresolved after Round 2, emit the interoperability fallback and end the turn.

   **Partial template override for multi-environment requests:**
   - If `target` or `protocol` is missing but the request clearly specifies multiple environments and a scenario, generate a partial script template with `__ENV` placeholders for all missing values.
   - Mark each assumption with `[assumption-based]` in a `pending_questions` block appended at the end of the artifact.
   - The partial template must still satisfy all other invariants (named function, thresholds, load profile via defaults).

   **Partial template override for auth-only edge cases:**
   - If the user explicitly asks for an auth pattern/template and the scenario/protocol is clear but `target` is missing, generate an auth-focused partial template.
   - Use `__ENV.BASE_URL` (or protocol-equivalent env var) placeholder and mark all unresolved values as `[assumption-based]`.
   - Append a `pending_questions` block with one direct question for the unresolved target.

   Additional questions must be integrated into the same question system, not handled as a separate side flow:
   - Add an HTTP method question when `protocol=http` and the method cannot be inferred safely.
   - Add one or more authentication questions when auth is required or unknown and executable output depends on it.
   - Add more questions only inside Round 1 or the single Round 2 tie-break block when other critical ambiguities or missing requirements are detected.
   - Do not finalize artifact generation until all required questions from this same system are resolved.

2. **Load Profile Defaults** (when `profile` is not specified):
   - `minimal`: 5 VUs, 1m duration, smoke testing
   - `standard`: 25 VUs, 9m duration, realistic load
   - `aggressive`: 120 VUs, 14m duration, stress testing

3. **Output Format**: Primary output is runnable artifacts with:
   - Recommended executor type
   - VU count and stages/options
   - Duration estimate
   - SLA-derived thresholds
   - Protocol-specific implementation notes
   - Data integration suggestions (CSV/JSON)
   - Exactly one deterministic `Next recommended step`

4. **Determinism**: Same inputs produce identical outputs every time.

5. **Compact-by-default responses**:
   - Keep generation responses concise and directly actionable.
   - Do not emit long narrative sections when short verified bullets and runnable commands are enough.
   - Default to compact output unless the user explicitly asks for a detailed report.

</rules>

## Verified Evidence Policy

Apply this policy in every builder response:

1. Report only data that is verifiably known from user input or direct tool/runtime evidence in the current task.
2. Do not present inferred values as facts in the final output.
3. If a value is required but not verified, mark it as `unknown` and ask a single unblocker question.
4. Do not fabricate machine/runtime numbers in summaries.

## Terminology Contract

- **Scenario type** means the test objective shape (`load`, `stress`, `spike`, `soak`, `smoke`).
- **Profile** means default intensity presets (`minimal`, `standard`, `aggressive`) used when explicit `vus`/`duration` are missing.
- **Round** means one consolidated question block in the adaptive question system; baseline questions are Round 1 and the optional tie-break is Round 2.
- Scenario type selects the executor strategy; profile sets default intensity values.

## HTTP Method Question

Before producing final HTTP artifacts, add the method question to the same active question system:

1. Confirm primary method (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`) when endpoint behavior depends on method.
2. If method is missing and cannot be inferred, ask it as an additional required question before finalizing.
3. Reflect confirmed method in scenario steps, checks, and threshold rationale.

## Auth Discovery Questions

Before finalizing artifact output, add auth questions to the same active question system:

1. Detect whether authentication is required (Bearer token, API key, basic auth, mTLS, session cookie, or none).
2. If auth is required or still unknown for executable output, ask for auth mechanism and required variable names as additional required questions.
3. Never hard-code credentials in examples or generated scripts.
4. Prefer environment variables (`__ENV`) for auth inputs and list required variables.

## Direct Invocation Behavior

If invoked without prior plan, the same Adaptive Question System above still applies.

Then:

1. Build a minimal internal plan
2. Expose assumptions
3. Generate runnable artifacts
4. Include a mandatory `k6-validate` handoff block with one suggested validation command

## Language Policy

1. If user language is explicit, answer in that language.
2. If language is not explicit, default to English.
3. Keep command names, k6 metric keys, and code identifiers in English.

## Cloud Runtime Compatibility Gate

Cloud artifact generation must be version-aware before emitting cloud commands, cloud options, or cloud-only guidance.

Required detection flow:

1. Resolve executable target.
2. Verify installed binary with `command -v k6`.
3. Run `k6 version`.
4. Parse semantic version.
5. Classify runtime family deterministically:
   - `V0_53_TO_V1_5` for `>=0.53.0` and `<1.6.0`
   - `V1_6_PLUS_V1_X` for `>=1.6.0` and `<2.0.0`
   - `V2_0_PLUS` for `>=2.0.0`

Gate behavior:

1. If `command -v k6` fails, stop cloud generation and ask the user to install k6 first.
2. If exact version is unknown or parse fails, stop cloud generation and ask for exact k6 version.
3. Do not invent synthetic cloud-family labels.
4. Preserve `k6_version` and `runtime_family` in validator handoff metadata.

Deterministic first-attempt rule:

1. When version classification is successful, select command family directly and execute without `--help` discovery.
2. Only consult help output after a blocking CLI error in the first attempt.

## Cloud Artifact Modes

When cloud capability is requested, emit one explicit mode:

1. `cloud-run`
   - Command family: `k6 cloud run <script>`
2. `cloud-streaming-local-execution`
   - Command family: `k6 cloud run --local-execution <script>`
3. `local-only`
   - Command family: `k6 run <script>`

Auth and routing safety:

1. Never hard-code tokens.
2. Prefer `K6_CLOUD_TOKEN` for non-interactive auth.
3. Use `K6_CLOUD_STACK_ID` and `K6_CLOUD_PROJECT_ID` when routing is required.
4. Use `__ENV` for script-consumed cloud-managed values.

## Cloud Command Action Matrix (Installed Version -> Action)

Use this matrix after successful `command -v k6` and parsed `k6 version`:

1. `V2_0_PLUS`
   - First command: `k6 cloud run <script>`
   - Do not use `--project-id` unless proven by current CLI evidence.
2. `V1_6_PLUS_V1_X`
   - First command: `k6 cloud run <script>`
   - Keep routing via environment variables when needed.
3. `V0_53_TO_V1_5`
   - First command: `k6 cloud run <script>`
   - Restrict to v1-compatible cloud guidance only.

Project routing rule:

1. If user provides `project_id`, resolve with `k6 cloud project list --json` before first paid run.
2. If requested `project_id` is default, execute once and report run URL.
3. If requested `project_id` is not default and routing cannot be set with verified syntax, stop and ask for confirmation before any paid run.

Missing project ID routing rule:

1. If user requests cloud execution and does not provide `project_id`, do not execute immediately.
2. Ask this mandatory routing confirmation first:
   - `No project_id was provided. This will run on your default cloud project. Do you want to continue with default project routing?`
3. If user rejects default routing, stop and request explicit `project_id`.
4. If user accepts default routing, require a second explicit paid-run confirmation before executing `k6 cloud run`.

## Cloud v2 Command Resolution

Use this deterministic policy before any cloud execution:

1. Run blocking preflight in this order:
   - `command -v k6`
   - `k6 version`
   - Parse `major.minor.patch` and classify runtime family
2. If preflight fails at any point, stop and ask the user for corrective action. Do not execute cloud commands.
3. Primary remote execution command is `k6 cloud run <script>`.
4. Do not emit or execute `--project-id` unless the detected runtime-family matrix explicitly confirms support.
5. First attempt must run without `--help` discovery once runtime is classified.
6. Consult help only after a real blocking CLI error on the first attempt.
7. If user requires project routing:
   - resolve current/default routing with `k6 cloud project list --json`
   - if requested project id matches default routing, continue without reroute
   - if requested project id does not match default routing, stop and ask for explicit confirmation plus a compatible alternative path before any paid run

## Cloud Authentication Readiness Gate

Before any cloud execution attempt, verify that at least one cloud auth path is available:

1. Prefer non-interactive auth via `K6_CLOUD_TOKEN`.
2. If `K6_CLOUD_TOKEN` is absent, verify active CLI login with `k6 cloud project list --json`.
3. If both checks fail, stop cloud execution and instruct the user to either run `k6 cloud login` interactively or export `K6_CLOUD_TOKEN`.
4. Treat missing cloud auth as a blocking condition for `cloud-run` and `cloud-streaming-local-execution`.
5. When auth is missing, do not attempt a paid cloud run.

## Paid Execution Guardrail

Enforce this block as mandatory for cloud execution:

1. `P1`: maximum one cloud paid execution per task unless user explicitly confirms additional cost.
2. `P2`: any second cloud execution requires explicit user confirmation plus a short reason.
3. `P3`: if run URL exists and status is `Running`, never auto-rerun.
4. `P4`: when terminal output is truncated, recover status from the same run identity; never relaunch automatically.
5. `P5`: when `project_id` is missing, require default-project routing acceptance before the paid-run confirmation.
6. `P6`: default-project routing acceptance does not replace paid-run confirmation; both confirmations are mandatory.

## Run Identity and Idempotency

Track cloud run identity deterministically:

1. Extract and store `run_url` and `run_id` from the first paid execution.
2. Reuse the same run identity for status updates, summaries, and follow-up guidance.
3. Treat rerun as a paid action and require explicit cost confirmation before execution.
4. Report run identity and rerun decisions in the `Cloud Execution Safety` subsection of the output.

## Cloud Version-Gated Output Rules

1. `V0_53_TO_V1_5`:
   - Allow `k6 cloud login`, `k6 cloud run`, and `k6 cloud run --local-execution`.
   - Do not emit `options.cloud.stackID` workflows by default.
   - Do not emit v2-only cloud options.
2. `V1_6_PLUS_V1_X`:
   - Allow restricted v1 path plus `options.cloud.stackID` and `K6_CLOUD_STACK_ID`.
   - Keep cloud options constrained to proven evidence.
3. `V2_0_PLUS`:
   - Allow verified v2 cloud options:
     - `options.cloud.projectID`
     - `options.cloud.stackID`
     - `options.cloud.distribution`
     - `options.cloud.deleteSensitiveData`
     - `options.cloud.staticIPs`
     - `options.cloud.drop_metrics`
     - `options.cloud.drop_tags`
     - `options.cloud.keep_tags`
   - Allow cloud context variables, for example `__ENV.K6_CLOUDRUN_LOAD_ZONE`.
   - Require stack-aware routing guidance for cloud commands.

## Cloud Distribution Validation

When `options.cloud.distribution` is present:

1. Every entry must include `loadZone` and `percent`.
2. Every `percent` must be an integer.
3. Sum of `percent` values must be exactly `100`.
4. If validation fails, stop runnable output instead of normalizing values.

## Dynamic Capacity Protocol

Run this protocol before emitting any runnable artifact that executes load from the current host. For pure `cloud-run`, local host capacity is advisory only and must not block remote cloud execution unless the user also requests a local dry run or `--local-execution`.

Cross-skill required fields:

- `execution_context`
- `machine_profile`
- `projected_load`
- `capacity_estimate`
- `risk_status`
- `safe_limit_recommendation`
- `scale_out_recommendation`

High-risk gate rule (mandatory):

- Before generating or orchestrating any script that projects more than `500` VUs on the current host (`local-only`, `cloud-streaming-local-execution`, CI, or container execution), run host audit silently with `node skills/k6-builder/scripts/audit-host.js`.
- If Node.js is unavailable, use the Python fallback: `python3 skills/k6-builder/scripts/audit-host.py`.
- Parse stdout JSON and use that as the authoritative `machine_profile` for this generation pass.

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
4. If projected load is expected to exceed `500` VUs on the current host, run host audit (`node skills/k6-builder/scripts/audit-host.js`, fallback `python3 skills/k6-builder/scripts/audit-host.py`) and overwrite missing or stale machine evidence with audit output.
5. Add optional telemetry when available: prior k6 saturation, observed memory per VU, prior stable arrival rate, or prior port exhaustion signals.
6. Derive `projected_load` from the runnable executor shape: target VUs, arrival rate, duration, stages, and `expected_iteration_duration_seconds` for arrival-rate executors.
   - `projected_load.expected_iteration_duration_seconds` must come from explicit user input, prior measured telemetry, or a conservative `[assumption-based]` estimate called out in the output.
   - If that field is unavailable, do not present `arrival_rate_max` as fully deterministic.
7. Calculate `capacity_estimate.vus_max` and `capacity_estimate.arrival_rate_max` from the current `machine_profile` using contextual deterministic formulas when the current host generates load. Never use a universal fixed VU ceiling.
8. Classify `risk_status` as `SAFE`, `AT_RISK`, or `HIGH_RISK` for current-host execution paths.
9. Derive `safe_limit_recommendation` and `scale_out_recommendation`, including `additional_cpu_percent`, `additional_ram_gb`, and `additional_nodes`.
10. If execution mode is pure `cloud-run` and remote worker capacity is not directly verified, report remote capacity facts as `unknown` and keep any local host assessment advisory-only for optional local validation.

Incomplete-data rules:

- If critical machine inputs are missing, ask one clarification question when that is the cheapest unblocker.
- If the scenario is otherwise clear, continue with a conservative `[assumption-based]` estimate instead of inventing a global default capacity.
- Mark every derived field that depends on missing telemetry as `[assumption-based]` and state the missing evidence explicitly.
- For pure `cloud-run`, missing local machine evidence must not block remote execution guidance; report remote capacity as `unknown` unless cloud worker constraints are explicitly provided.

Builder-stage gate behavior:

- `cloud-run`: emit runnable artifacts and cloud execution hints even when the local host would be `AT_RISK` or `HIGH_RISK`; local capacity may only restrict optional `k6 run` or `k6 cloud run --local-execution` hints.
- `SAFE`: emit runnable artifacts normally.
- `AT_RISK`: runnable artifacts are allowed only if the output includes the canonical capacity alert, the reduced safe limit, and the distributed mitigation guidance.
- `HIGH_RISK`: block runnable single-node artifact emission only for current-host execution modes. Replace the runnable artifact section with a blocked-output explanation plus a reduced-load or distributed execution path.

When `HIGH_RISK`, the blocked-output explanation must use this exact format:

`Your machine only has [X]GB of available/free RAM. Attempting to run [Y] VUs locally will collapse the load generator. Limit the local test to [Z] VUs or export this design to k6-operator (distributed execution).`

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

## Required k6 Invariants

Always enforce these validations before returning output:

1. **Thresholds are required**
   - Parse from SLA when provided.
   - If SLA missing, derive deterministic defaults and state them.
2. **Load profile is required**
   - Include explicit `vus` and `duration`, or explicit staged/scenario equivalent.
3. **Parameter coherence is required**
   - Arrival-rate executors must satisfy `preAllocatedVUs <= maxVUs`.
   - Time-based executors require explicit duration.
   - Iteration-based executors require explicit `vus` and `iterations`.
4. **Secrets and runnable safety are required**
   - Never hard-code credentials/tokens.
   - Require environment variables (`__ENV`) for auth and base URL.
5. **Multi-environment coherence is required**
   - For `dev/staging/prod`, validate `dev <= staging <= prod` for VU progression.
   - Emit `WARNING` if user override violates VU progression without explicit justification.
   - **SLA thresholds are invariants**: the stated SLA must be identical across dev, staging, and prod. If any environment has relaxed thresholds (e.g., `p99<2s` in dev when the SLA states `p99<1s`), reject the artifact and report under Guardrail Validation.
6. **Named default function is required**
   - The `export default function` must always have a name derived from the active scenario and protocol.
   - Naming convention: `run<Protocol><ScenarioType>` — example: `runHttpLoad`, `runGrpcStress`, `runBrowserSmoke`.
   - If scenario or protocol is not resolved yet, use a generic but named function: `runPerfTest`.
7. **Cloud compatibility invariants are required (when cloud mode is requested)**
   - Exact k6 version must be detected and classified before cloud output.
   - Emitted cloud commands/options must match runtime family allowlist.
   - Reject v2-only cloud options when runtime is below `v2.0.0`.
   - Distribution math must pass strict 100% validation.

### SLA Consistency Across Multi-Environment

When building for multiple environments (dev/staging/prod):

- Threshold values MUST BE IDENTICAL across all environments.
- VU counts MAY VARY per environment.
- Duration MAY VARY per environment.
- Performance SLA targets (p95, p99, error bounds) MUST NOT VARY per environment.

Rationale: SLA is a commitment and must remain coherent across environments. Relaxing SLA by environment creates non-comparable results and hides production risk.

Canonical cross-skill warning (must match `k6-plan` exactly):

`WARNING: SLA must be identical across environments to maintain testing coherence.`

Canonical enforcement flow (builder stage):

1. Detect single declared SLA plus per-environment threshold divergence request.
2. Emit the canonical warning string above.
3. Ask one confirmation question:
   - `Do you want to normalize all environment thresholds to the same SLA now?`
4. If user confirms normalization:
   - Continue generation with identical thresholds across dev/staging/prod.
5. If user rejects normalization:
   - Reject runnable artifact emission and report violation under Guardrail Validation.
   - Do not emit per-environment relaxed thresholds.

## Builder Decision Rules

### Scenario to Executor Mapping

- `load`: `ramping-vus`
- `stress`: `ramping-vus` (aggressive progression)
- `spike`: `ramping-vus` (rapid surge)
- `soak`: `constant-vus` or `ramping-vus` sustained
- `smoke`: `constant-vus`

### Request-Rate Intent

If user explicitly requires rate control, prioritize:
- `constant-arrival-rate` for fixed RPS
- `ramping-arrival-rate` for changing RPS

### Iteration Intent

If user asks for exact iteration accounting:
- `per-vu-iterations` or `shared-iterations`

### Multi-Environment Differentiation Rules

When building multi-environment outputs (dev/staging/prod), apply mandatory differentiation:

1. **VU counts must differ explicitly** across environments — never use identical values. Baseline pattern: dev ≤ staging ≤ prod.
2. **SLA-derived thresholds are invariants across all environments** — never relax or adjust threshold values per environment. The stated SLA (e.g., `p99<1s`) must be applied identically to dev, staging, and prod. Only VU counts, durations, ramp-up stages, and load profiles may differ per environment. Any threshold relaxation (e.g., `p99<2s` in dev when SLA states `p99<1s`) is a hard invariant violation — reject and report under Guardrail Validation.
3. **Target URL must be distinct per environment** — use `__ENV.DEV_BASE_URL`, `__ENV.STAGING_BASE_URL`, `__ENV.PROD_BASE_URL` as named environmental variables.
4. **SLA-derived thresholds must be applied even when the target URL is missing** — use defaults from the stated SLA (e.g., `p99<1s`) with `__ENV` placeholder for the URL.
5. **Structure**: use three distinct scenario blocks or a clearly labeled `profiles` object with per-env overrides — never collapse to a single block relabeled with comments.

## Multi-Environment Architecture Options

When user requests multi-env outputs, offer two architecture options and make the default explicit:

### Option 1: Separate Scripts

- Files: `dev.js`, `staging.js`, `prod.js`
- Pros: Strong isolation per environment
- Cons: Duplication and cross-env maintenance overhead

### Option 2: Single Script with Environment Switcher (recommended default)

- File: `load-test.js`
- Pattern: `__ENV.ENVIRONMENT` selects environment-specific VUs/duration
- Pros: DRY, single source of truth for shared logic and thresholds
- Cons: Slightly more control-flow branching

Default behavior:

- Recommend Option 2 unless user explicitly asks for separate files.
- Still mention Option 1 as an available alternative.
- Keep SLA thresholds identical regardless of selected architecture.

## SLA Parsing Rules

<sla-rules>
Parse SLA string to extract threshold conditions. Supported syntax:

### Simple Conditions (single metric)
- `p95<Xms` -> 95th percentile latency threshold
- `p99<Xms` -> 99th percentile latency threshold
- `error<X%` or `rate<X%` -> Error rate threshold

### Comma-Separated Lists (implicit AND)
- `p95<500ms,p99<900ms,error<1%` -> All conditions must be met
- Commas separate independent thresholds
- All listed thresholds are combined in final configuration

### Explicit AND Conditions (multiple conditions on same metric)
- `p95<500ms AND p95>100ms` -> p95 must be between 100ms and 500ms
- Multiple constraints on the same metric (range validation)
- Translates to multiple threshold entries for the same k6 metric

**Note:** OR logic is not supported in this skill behavior. All conditions are treated as mandatory (AND).

### Parsing Examples
- Input: `p95<400ms,error<1%` -> p95 AND error rate thresholds
- Input: `p95<500ms AND p99<900ms` -> Both percentiles required
- Input: `p95<2s` -> Single threshold with p99 inferred (see sla-defaults.md)

Defaults per profile when SLA is not provided:
- `minimal`: p95<800ms, error<2%
- `standard`: p95<500ms, error<1%
- `aggressive`: p95<300ms, p99<700ms, error<0.5%, checks>99%

### Protocol-to-Threshold Mapping

When generating thresholds, apply the correct metric per protocol. Using `http_req_duration` for non-HTTP protocols is a hard invariant violation.

| Protocol | Required threshold metric |
|---|---|
| HTTP | `http_req_duration: ['p(95)<Nms']` |
| WebSocket | `ws_session_duration: ['p(95)<Nms']` (built-in session duration metric) |
| gRPC | `grpc_req_duration: ['p(99)<Nms']` |
| Browser | `browser_http_req_duration: ['p(95)<Nms']` |

If the inferred protocol does not match `http`, ensure the threshold uses the correct metric above — never substitute `http_req_duration` as a fallback.
</sla-rules>

## Base URL Template Rule

When generating artifacts (single or multi-environment):

**For HTTP/gRPC/Browser protocols:**
- If `target` is explicitly provided (literal URL), wrap it in `__ENV`:
  ```javascript
   if (!__ENV.BASE_URL) {
      throw new Error('BASE_URL environment variable is required');
   }
   const BASE_URL = __ENV.BASE_URL;
  ```
- **Never emit**: `const BASE_URL = 'https://api.example.com';` (hardcoded literal without `__ENV`)
- Exception: Only if user explicitly asks for hardcoded URL (e.g., "quick smoke test for local"), document as assumption.

**For multi-environment outputs:**
- Always use pattern: `__ENV[`${env.toUpperCase()}_BASE_URL`]`
- Append a `.env.example` stub with all required variables.

**Validation**: After artifact generation, scan for violations:
- If protocol in [http, grpc, browser] and artifact contains `= 'https://` or `= "https://` without `__ENV`, **REJECT**.
- Add to guardrail validation checklist: `[ ] Base URL uses __ENV, not hardcoded literals`

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
- Always close connections in teardown
- Handle metadata for authentication

### Browser
- Use `browser.newContext()`, `context.newPage()`, `page.goto()`, `page.waitForSelector()`
- Always close page/context at iteration end
- Prefer `data-testid` selectors
- Collect Web Vitals when relevant
- For requested multi-step user journeys, model the full sequence explicitly in order (do not collapse or skip steps).
- For checkout/browser journeys, include an end-to-end threshold aligned to the requested KPI/SLA (for example `p(95)<4000` when the request states p95<4s).

### WebSocket
- Use `ws.connect()` from `k6/ws` and handle all lifecycle events: `on('open')`, `on('message')`, `on('error')`, `on('close')`.
- Always add a bounded session duration to avoid infinitely hanging connections.
- **WebSocket latency thresholds are required**: `http_req_duration` does not capture WebSocket behavior. Use built-in `ws_session_duration` for session duration and a custom `Trend` for per-message latency:
  ```js
  import { Trend } from 'k6/metrics';
   const wsLatency = new Trend('ws_message_latency');
  // in default function, record per-message timing:
  // wsLatency.add(Date.now() - sentAt);
  // in options.thresholds:
   // ws_session_duration: ['p(95)<1500']
   // ws_message_latency: ['p(95)<150']
  ```
- Add to guardrail checklist: `[ ] WebSocket script includes builtin ws_session_duration and custom ws_message_latency thresholds`.
</protocol-patterns>

## Dashboard Policy

Apply deterministic recommendation:

1. CI/headless: `K6_WEB_DASHBOARD=false`
2. Local browser troubleshooting: `K6_WEB_DASHBOARD=true`
3. Local non-browser: default `K6_WEB_DASHBOARD=false` unless explicit opt-in
4. Otherwise default `false`

## Output Contract

Every response must include these sections in order:

1. Build Inputs Summary
2. Executor and Scenario Configuration
3. Runnable Artifacts
4. Required Environment Variables
5. Guardrail Validation — include this checklist at minimum:
   - [ ] Default export function is named (not anonymous)
   - [ ] SLA thresholds are identical across all environments (no per-env threshold relaxation)
   - [ ] Base URL uses `__ENV`, not hardcoded literals
   - [ ] Final summary includes only verified facts or explicit `unknown`
6. Validation Handoff (required) — include one runnable command for `k6-validate`
   - **For smoke tests specifically**: Append explicit command block:
     ```
     ## k6-validate Recommendation
     
     Run k6-validate to check this smoke artifact:
     
   /k6-validate <your-plan-or-test-config>
     ```
   - **For other scenarios** (load, stress, soak, spike): Include validation recommendation that references k6-validate.
7. Execution Hints (required)
   - Include at least one concrete run command that can be copied as-is.
   - Include required environment variables used by that command using explicit `-e` flags.
   - Do not rely on implicit shell-exported variables for one-shot execution hints.
   - Use deterministic command shape (`k6 run <script>` plus `-e` flags when needed).
   - Keep hints runnable and aligned with the emitted artifact names.
   - Treat `Execution Hints` as a hard companion of `Runnable Artifacts`: if artifact code exists, hints must include the exact script filename and matching env var flags.
   - Never emit conceptual guidance only; include at least one concrete copy-paste command.
8. Cloud Execution Safety (required)
   - `run_count: <integer>`
   - `first_run_url: <url-or-none>`
   - `rerun_requested_by_user: <yes|no>`
   - `cost_confirmation: <yes|no>`
   - `project_id_provided: <yes|no>`
   - `default_project_routing_confirmation: <yes|no|not-applicable>`
9. Next recommended step

Dynamic capacity reporting requirements:

- Include `execution_context` only when explicitly provided or directly measured.
- `Guardrail Validation` must also include these checklist items when capacity evaluation is in scope:
   - [ ] Dynamic capacity gate executed with current `machine_profile`
   - [ ] `capacity_estimate`, `risk_status`, and `safe_limit_recommendation` are present
   - [ ] `scale_out_recommendation` includes `additional_cpu_percent`, `additional_ram_gb`, and `additional_nodes`
   - [ ] Canonical capacity alert emitted when `risk_status` is `AT_RISK` or `HIGH_RISK`

- For pure `cloud-run`, capacity reporting may mark remote cloud-worker capacity as `unknown`; local host capacity remains advisory unless local execution is also requested.

- When `risk_status` is `HIGH_RISK`, `Runnable Artifacts` must not include a single-node runnable artifact.

## Runnable Artifact Rules

- Always prefer `__ENV.BASE_URL` for runnable scripts.
- Include timeout guidance for HTTP (`timeout: '30s'` baseline).
- Include checks and request tags for segmentation.
- Generated script must be portable: the same artifact must run both with `k6 run` and `k6 cloud run`.
- Do not hard-couple the script to cloud-only configuration by default (for example fixed `options.cloud.*` values).
- Cloud routing/auth concerns belong in Execution Hints and environment variables, not as mandatory hardcoded script config.
- Add lightweight traceability support using `__ENV.TRACE_MODE` (`off|basic`) with concise one-line logs only when enabled.
- Default `TRACE_MODE` to `basic` for cloud execution hints unless the user explicitly disables tracing; keep non-cloud hints at `off` unless the user opts in.
- For auth, list required env vars and never place secret literals.
- For multi-env requests, include `.env.example` placeholders only.
- Any output containing URLs, auth headers, or any configurable external value **must** include an explicit `## Required Environment Variables` block listing each `__ENV.VAR_NAME` with a one-line description of its purpose.
- The `## Required Environment Variables` block must be concrete and non-empty; include every required runtime variable and avoid generic placeholders like "add your vars here".
- For multi-env outputs, always include a `.env.example` stub section with three labeled groups (`# dev`, `# staging`, `# prod`) showing the expected variable names as empty placeholders.
- This block is mandatory and must appear even when the target URL is a placeholder — document the placeholder variable name.
- For browser or transaction flows with multiple business steps, emit the full ordered step list in code/comments so the generated artifact preserves the requested journey sequence.

## Code Quality Rules

Generated code must not introduce static-analysis violations. Before emitting any artifact:

1. **Named exports** — `export default function` must be named (see Required k6 Invariants #6).
   - Generate using naming convention: `run<Protocol><ScenarioType>` (e.g., `runHttpLoad()`, `runGrpcSmoke()`).
   - **VALIDATION (MANDATORY)**: After code generation, scan the artifact for `export default function` followed by `(`. 
   - If the pattern matches `export default function\s*\(` (anonymous), **REJECT** the artifact immediately.
   - Add to guardrail violations: "Default export function must be named (e.g., `runHttpLoad`)". Do not emit unless function is named.
   
2. **No `var` declarations** — use `const` or `let` only.
3. **No unguarded logs in hot paths** — inside `export default function` or any function called per iteration.
   - Guarded compact trace logs are allowed only when `__ENV.TRACE_MODE==='basic'`.
   - Prefer one line at iteration start and one line for status/result.
4. **No hardcoded literals for URLs or credentials** — all configurable values must use `__ENV`.
5. **No silent `catch` blocks** — errors must be logged or re-thrown with context.
6. **No unsafe `JSON.parse`** — wrap in try-catch with descriptive error message.

If any generated line would violate a rule above, block the artifact and report the specific violation under `Guardrail Validation` instead of emitting broken code.

## Progressive Disclosure

Keep this file focused on generation workflow. Place deep guidance in:

- `skills/k6-builder/references/README.md`

## Workflow

1. Parse parameters (`target`, `scenario`, `sla`, `protocol`, `profile`, `duration`, `vus`, `environments`, `goal`).
2. Run Tool Discovery Protocol when minimum inputs are missing.
3. Start the Adaptive Question System with baseline questions when `target`, `scenario`, `sla`, or `protocol` are missing.
4. Add an HTTP method question to the same question system when protocol is HTTP and method is still ambiguous.
5. Add auth questions to the same question system when auth is required, unknown, or otherwise blocks executable output.
6. Add more questions in the same system if other critical ambiguities or missing requirements are detected.
7. Build internal minimal plan from inputs.
8. Select executor and derive coherent scenario config.
9. Enforce executor coherence: if scenario type is `load` and the user did not explicitly request rate-based control, recommend and emit `ramping-vus`.
10. Parse SLA thresholds or apply deterministic defaults.
11. If cloud execution is requested, run Cloud Runtime Compatibility Gate and Cloud v2 Command Resolution preflight (`command -v k6`, `k6 version`, runtime classification) before any paid run.
12. If cloud execution is requested, run the Cloud Authentication Readiness Gate before any paid run.
13. If cloud execution is requested and `project_id` is missing, run the Missing project ID routing rule and block execution until routing is confirmed.
14. Run the Dynamic Capacity Protocol using current machine evidence only when the selected execution path uses the current host as the load generator; for pure `cloud-run`, keep local capacity advisory and do not block remote execution.
15. For multi-environment requests, choose architecture using Multi-Environment Architecture Options (default single-script unless explicitly overridden).
16. Generate runnable script/options/config outputs only when the relevant current-host capacity gate allows them.
17. Apply dashboard and secrets safety policies.
18. Enforce Paid Execution Guardrail before any paid run or rerun attempt; require explicit cost confirmation and justification for paid reruns.
19. Validate all required invariants, including: (a) the generated default export function is named — reject anonymous `export default function () {}`; (b) SLA thresholds are identical across all environments — reject any per-environment threshold relaxation. Both are hard invariant violations that block output emission.
20. Return output in Output Contract order.

## Local Evaluation Workspace Policy

For official skill evaluation runs in this repository:

- Store artifacts under `skills/k6-builder/k6-builder-workspace/iteration-N/`.
- Keep each run isolated inside its own `iteration-N` directory.
- Treat benchmark outputs, grading files, timing files, and generated responses as non-versioned execution artifacts.
