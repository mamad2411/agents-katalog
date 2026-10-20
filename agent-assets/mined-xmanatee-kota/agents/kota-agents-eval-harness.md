# Eval Harness Module

Owns autonomy fixture execution, deterministic scoring, regression gates, and
their CLI, HTTP, and cadence surfaces.

## Measurement Contract

- Retain workflow metadata and agent streams, measured usage and activity,
  predicate results, and workspace diffs before clone cleanup. Missing runtime
  evidence remains explicit; projections never manufacture cost or trace facts.
- Record host class, CPU allocation and kill threshold, memory, execution
  backend, requested/observed/enforced profile, timing, and repeat index.
- Host subprocess runs are non-gating without verified CPU and memory facts.
- `pass@k` measures whether any repeat passed; `pass^k` requires every repeat
  and is the regression gate.
- Gate only when baseline and candidate use comparable resources, active
  preset, fixture manifest, source identity, resolved harness/model evidence,
  execution profile, and sufficient equal repeat counts.
- Noise-band drops, profile drift, config drift, or undersized samples produce
  typed non-gating evidence. Calibration is per host class; defaults live in
  code.

## Fixture And Scoring Contract

- Every fixture records either a real failure with its source run id or a
  justified smoke purpose. Anything else fails at load time.
- Fixture ignore rules are stored as `fixture.gitignore`, the package-safe
  canonical name; materialization restores them as `.gitignore` before Git is
  initialized.
- Predicates score final state, never self-report. Initial
  `preRunExpectations` include at least one expected failure.
- Git, shell, agent-verifier, and objective-metric execution uses fail-closed
  offline containers with bounded resources and stripped credentials. Only the
  candidate tree is writable; scorer overlays remain immutable.
- Post-run Git evidence uses that same isolation boundary with the actual
  candidate tree, without scorer overlays, and disables Git's executable helpers.
  Unavailable isolation or failed collection records missing evidence; it never
  falls back to host Git or accepts a partial patch.
- Builder fixtures name `builderTaskId`; the runner resolves its immutable
  dispatch through the production builder task owner after materialization and
  after each round input. Do not copy task digests into fixture data.
- Persistent scenarios use ordered multi-round fixtures.
- Round-input destination writes use verified, pinned directories and atomic
  leaf replacement. Retained candidate symlinks must never redirect host writes;
  lexical path checks alone do not establish filesystem containment.
- Retain a fixture only for a named model-dependent failure and a model/prompt
  decision that deterministic owner checks cannot settle. Record that rationale
  with the fixture. Scorers measure outcomes, not prescribed test names, source
  spelling, implementation paths, or authored reasoning narratives.
- Objective metrics are deterministic evidence, not a second runner. Metric
  errors fail passing runs; failed runs retain diagnostic metrics.
- Scorer self-tests belong to owner verification, never live predicates,
  pre-run expectations, or candidate task completion requirements. Exercise
  shared predicates and runner outcomes with representative inputs; shipped
  fixtures own benchmark difficulty and calibration. Retain fixture-specific
  checks for distinct scorer errors or shortcuts, without duplicating solved
  projects to reprove the shared runner.
- Verifier calibration runs before the workflow and fails as fixture error.
  Accepted alternatives exist only for deterministic, genuinely broad answer
  spaces.
- Code-health diagnostics are opt-in advisory evidence; predicates own pass or
  fail.

@execution.md

## Boundaries

- Keep scoring, runner contracts, cadence baseline, and fixture tooling here.
- Use typed completion/regression events, run artifacts, and one baseline row;
  do not add parallel metrics stores.
- Never leak cost signals into agent context.
- Keep auth behind non-secret adapter locators. Agent replay and binary-call
  shims are unsupported; deterministic product checks belong with their owner.
- Candidate mining is bounded advisory output and never creates fixtures or
  changes regression scores.
- Provider/model evaluations require their declared container, egress policy,
  candidate availability, and artifact evidence; they fail visibly when prerequisites are unavailable.

Native workflow callers use the [contained evaluation surface](contained-evaluation.md).
Host environment profiles bound its scope, scenarios, image, egress and resources;
worker arguments never supply host capabilities. Resolve adapter facts on the
module host, then use the shared blocking worker and run process registry.
Register independent container resources before launch, including verifier and
availability containers. Availability uses the same asynchronous process supervisor
and cancellation signal as candidate execution. Temporary auth snapshots also belong to that cleanup
lifetime. Results remain under the originating run's runtime-owned artifacts.

Deterministic native probes use the same tool and blocking operation, with
host-selected offline profiles. The eval owner collects authorized current-writer
source through anchored reads and sends it over stdin to the existing container
launcher. The task-probe owner retains result semantics; shared runtime cleanup
owns container removal on cancellation and recovery. Candidate code never runs
on the module host or receives host mounts. Source hashes identify the measured
cohort; browser persistence and other consumers retain their own acceptance.

Host grant configuration is exposed through the existing module Setup capability.
The service installer persists operator-reviewed profiles across restarts. The
deployment recipe generates profiles and proxy rules from existing owner catalogs;
configuration readiness never stands in for image/auth/network or live proof.

## Preset Parity

`pnpm build && pnpm test:preset-parity` runs the disposable daemon journey through
single/tool workflow agent turns, capture/recall/answer, a balanced workflow,
and the shipped builder
AgentDef on a read-only task. It does not exercise builder publication or replace
shared runtime recovery tests. The observer is installed only in that disposable
scope and records actual harness and model-client entry calls, including failures.
Single/tool probes explicitly select the balanced tier and require completed
harness turns attributed to their workflow run. Daemon session chat uses
ModelClient and cannot supply harness permission observations. The model sweep
has independent owner tests.

Boot waits for the workflow runtime's loaded-definition observation before
checking probe registration; a reachable control listener establishes liveness
before workflows activate. Required runtime and login-probe errors take precedence
over missing API authentication when qualifying an unexecuted live row.

Per-preset transcripts, calls, workflow selections and cleanup evidence live under
`.kota/runs/<run-id>/preset-parity/` (or the supplied run artifact directory).
Missing authentication is an explicit unexecuted row. Other readiness errors and
provider failures fail the gate. Native adapters' declared rejection of
`canUseTool` is reported alongside their file-read outcome; it is never recorded
as a successful KOTA permission callback.

The disposable scope explicitly configures the API provider for capture/answer.
Codex agent turns use native login, while its capture/answer calls additionally
require `OPENAI_API_KEY`. Gemini's capture/answer calls use Google's compatible
endpoint with an existing Gemini/Google API-key reference. Keys are not copied
into fixture configuration or artifacts.
