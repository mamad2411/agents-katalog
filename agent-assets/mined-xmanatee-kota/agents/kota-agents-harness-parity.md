# Harness Parity Module

This module owns the operator-facing surface for capturing paired coding-task
artifacts across every registered `AgentHarness`. Its job is to turn the
`AgentHarness.run` contract into comparable evidence — same prompt, same
initial state, same verification predicate, every registered adapter — so the
"general-purpose coding agent across pluggable harnesses" claim can be
judged against real runs rather than aspiration.

## Scope

- Scenarios are self-contained: `scenarios/<id>/scenario.json` plus an
  `initial/` tree that defines the starting repo state. Single-stage
  scenarios declare one prompt and verifier; staged scenarios declare two or
  three ordered stages, each with its own prompt and verifier. Both input
  shapes normalize to the same stage list; consumers read stage fields, with
  no duplicate top-level prompt, verifier, or preview aliases.
- The runner reuses `runAgentHarness` — the same entry point the main `kota
  run` path calls. No parallel benchmarking framework lives here.
- Every harness runs against a fresh `tmpdir` copy of the scenario's
  `initial/` tree. The scenario source is never mutated. With no explicit scope,
  harness session state belongs under the stage artifact directory so runtime
  bookkeeping does not become candidate changes.
- Paired artifacts land under a single operator-chosen output directory with
  one subdirectory per harness, plus a top-level `parity.json` summarizing
  the comparison.
- This module also owns the `harnessParity` `KotaClient` namespace
  (`harness-parity-operations.ts`). CLI action handlers consume
  `ctx.client.harnessParity.<method>()`; the local handler and the
  daemon-control routes (`controlRoutes` at `/harness-parity/*`) call the
  same shared helpers, so daemon-up and daemon-down callers see the same
  scenario list and run summary.

## Model Matrices

Matrix defaults resolve each model through the shipped preset and provider
owners. An explicit harness list is a pool: only compatible declared routes
execute, and a model with no compatible route rejects the matrix before any
agent launches. Scenario and eval targets share admission; provider-qualified
ids stay on ModelClient routes and native adapters receive native ids.
Provider defaults apply unless an effort is requested; unsupported local effort
rejects before launch. Scenario and eval execution carry configured output-token
limits, and eval subprocesses resolve candidate auth in the original scope.
Eval isolation settings use the eval-harness backend schema, keyed by resolved
provider in `evalIsolationBackends` (CLI: `--eval-isolation-backends <json>`).
Every runnable eval route preflights before matrix inference; missing backend,
image, verifier isolation, or enforced egress stops execution with attributable
preflight evidence. Provider policies must match their row's resolved provider.
OpenRouter container candidates require provider egress; omitted or offline
network policies reject before inference.
Candidates use the shared subprocess executor and scoring stays offline. Native
container login uses an adapter-declared credential file locator: the executor
snapshots only that file outside the candidate tree and mounts the snapshot
read-only. Host homes, configuration and session stores do not cross this boundary.
Public and contained matrices retain explicitly unavailable native login/capability rows as
unexecuted evidence while preparing independent compatible routes. Invalid grants,
malformed login locators, isolation failures and unexpected errors still reject;
file readability does not
establish authentication or entitlement. Local providers require their matching
internal proxy policy and the model-client owner's contained endpoint. Proxy
readiness, positive inference, and denied unintended access still need live proof;
network labels and launch arguments alone do not establish those outcomes.
Runnable non-gating egress remains non-gating.
Cost prefers complete runtime usage; otherwise complete tokens with shipped flat
rates yield an uncached-token estimate. Unknown pricing and tiered aggregate
usage remain unavailable rather than becoming zero-cost evidence.

Shadow evidence pairs each baseline with each candidate for the same target,
including different harnesses, and names both harnesses in the report. Shared
scenario snapshots and run options are fixed within an invocation. Missing
capability, repeat, verification, cost, or eval configuration/resource evidence
keeps a comparison incompatible. These artifacts never authorize promotion;
eval-harness owns regression and consistency gates.

## Scenario Portfolio

Keep the smallest representative set that distinguishes materially different
harness capabilities: tool-loop editing, recovery from feedback, workspace
navigation, rendered output, staged maintenance, and read-only investigation.
Before adding a scenario, name the distinct failure it catches and check
whether an existing scenario can carry that example. Merge or remove scenarios
whose outcomes overlap; scenario identity and fixture count are not contracts.
The current catalog is discoverable from `scenario.json` files and should not
be copied into this instruction file. Decode the shipped portfolio once for
readiness and exercise runner behavior with representative scenarios. Keep
custom verifier checks for evidence, scope and invalid-result rejection;
manually solving every shipped project does not establish live harness parity.

## Capability Gap Handling

Harnesses differ in capability. A text-only adapter (e.g. `thin`) cannot
apply file edits, so a coding-task scenario will record a verification
failure with an empty diff rather than a successful fix. That is not a bug
in the harness or the scenario — it is the capability boundary the task
exists to measure.

- When the boundary is inherent (text-only adapter on a coding task), the
  artifact is the evidence and the gap is recorded in `trace-summary.md`.
- When the gap is a KOTA bug against a capable adapter, convert it to a
  follow-up task rather than suppressing the artifact.

## What Does Not Belong Here

- Scoring, regression gates, and standalone aggregated pass@k/pass^k metrics
  are eval-harness concerns; harness-parity may record model-matrix parity
  evidence, but it is not a rollout gate.
- Provider credentials, model discovery, or adapter registration. Harnesses
  register themselves through their own modules; this module resolves them
  by name.
- Live execution without an operator authorization step. The autonomous
  builder may capture artifacts when the owner has authorized live validation,
  using the runtime's permitted execution boundary. Authorization does not
  grant candidate code host credentials or broader filesystem/network access.

@running-routes.md
