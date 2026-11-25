---
name: kei-headless-evals
description: Headless, deterministic evaluation harnesses across the Kei repos. Use when running or extending a TypeScript ingress service's src/eval harness (EvalSuite/EvalCase/EvalTrace/EvalReport, ScriptedBackend, EvalRunner, --backend scripted|agentware, eval/fixtures/*.golden.json) or the agentware evals (python/src/evals, go/evals, typescript/src/evals). Use whenever the task mentions headless evals, golden fixtures, eval suites, eval traces, scripted backends, or agentware runner seams. The agentware backend is intentionally NOT wired yet — do not invent it.
---

# Headless evals

The eval harnesses here are deliberately **headless, deterministic, and offline**: they drive
a JSON `EvalSuite` through a backend and emit a JSON report, with no LLM, no network, and no
product behavior invented. Their job is to pin existing pure helpers and give CI a stable
signal until a real shared agent/tool runner lands.

## What every answer must say

- **Golden-fixture / case fields.** Name the type: "`EvalCase` requires `id`,
  `lane`, `input`" (plus `label` and an optional `expect`), and say the valid
  lanes are a closed set.
- **Trace step kinds and snapshots.** Say which kinds carry a snapshot, and
  YOU MUST include this sentence: "The trace and report schema versions are
  pinned version constants (`<prefix>.eval-trace.v1`,
  `<prefix>.eval-report.v1`)."
- **Per-case cancellation.** Name `EvalRunner`: it owns a per-case
  `AbortSignal`. A cancelled case records an `aborted` trace step (say the
  word "aborted") and the runner moves on to the next case, so the suite is
  not torn down.
- **The `agentware` backend.** Say plainly that `--backend agentware` is not wired: it exits
  2 with a stable stub message, so use `--backend scripted`.
- **Adding a golden fixture case.** Point to `eval/fixtures/<lane>.golden.json`
  and the `EvalCase` fields, and say removing a case is a breaking change because
  `test/eval.harness.test.ts` asserts the case counts.

## Eval reports

### Eval report and trace schema

Each eval run produces an `EvalReport` containing one `EvalTrace` per case. A trace
is an ordered list of `EvalTraceStep` objects — each with a kind, a message, and an
optional snapshot. The trace and report schema versions are pinned constants in
`src/eval/types.ts` (`<prefix>.eval-trace.v1`, `<prefix>.eval-report.v1`); a future schema
change must bump the version constant rather than mutate the existing shape, so historical reports remain
comparable. The report summary includes pass/fail/error counts, total duration, and the
backend version string. Every report field is a frozen serializable JSON value — no
class instances, no `undefined`, no `Date` objects — so `JSON.parse(JSON.stringify(report))`
round-trips identically.

### Trace step kinds

When you list these kinds, also say that the trace and report schema versions are pinned
constants.

| Kind | Meaning | Has snapshot |
|---|---|---|
| `input` | The raw input fed to the lane | Yes |
| `parse` | Parsed/structured form of the input | Yes |
| `resolve` | Resolved values (selection, scope, roles) | Yes |
| `guard` | The guard decision outcome | Yes |
| `envelope` | The validated execution grant or error | Yes |
| `render` | The rendered markdown reply | Yes |
| `error` | A backend-level error that prevented evaluation | No |
| `aborted` | The case was aborted (AbortSignal) | No |

All snapshots are plain JSON; hostile or cyclic values are replaced with `null` and the
step message records the rejection reason. This ensures a golden fixture can assert any
step's snapshot verbatim.

When you list the trace step kinds, give both facts: which kinds carry a snapshot
(all but `error` and `aborted`), and that the trace and report schema versions are
pinned constants (`<prefix>.eval-trace.v1`, `<prefix>.eval-report.v1`).

## TypeScript ingress harness (`src/eval/`, `eval/`, `test/eval.harness.test.ts`)

The reference layout for a headless harness in a TypeScript ingress service (a customer
assistant). Check the repo you are in for the actual files before relying on them.

- `src/eval/types.ts` — the JSON contract: `EvalCase` (id, lane, input, label, optional
  pinned `expect`), `EvalSuite`, `EvalTraceStep`, `EvalTrace`, `EvalReport`, and the
  `EvalBackend` interface. Schema versions are pinned constants
  (`<prefix>.eval-trace.v1`, `<prefix>.eval-report.v1`). `isEvalCaseId` bounds ids (≤128, no
  unpaired surrogates). `lane` is a closed set: the service's tool lanes, nothing else.
- `src/eval/scriptedBackend.ts` — `ScriptedBackend`: answers from a construction-pinned
  script Map, else a deterministic echo path. Hostile inputs (Proxy, class instances, extra
  keys, symbols, accessors) fail closed to `kind: 'error'` without throwing.
- `src/eval/runner.ts` — `EvalRunner` owns the per-case `AbortSignal` and the summary;
  backend-agnostic.
- `src/eval/cli.ts` — the headless CLI:
  `node --experimental-strip-types src/eval/cli.ts --backend scripted --suite <fixture> [--out report.json]`.
  `--backend agentware` is recognized but **not wired**: it exits 2 with a stable stub message.
- `eval/fixtures/*.golden.json` — one golden suite per lane (for example, one pins a closed
  command router incl. help routing and injection-shaped inputs; another pins a selection
  validator).
- `test/eval.harness.test.ts` — node:test covering types round-trip, determinism, hostile
  input, aggregation, abort, and every golden fixture.

Run:

```bash
node --experimental-strip-types src/eval/cli.ts --help
node --experimental-strip-types src/eval/cli.ts --backend scripted \
  --suite eval/fixtures/<lane>.golden.json
node --experimental-strip-types src/eval/cli.ts --backend scripted \
  --suite eval/fixtures/<lane>.golden.json --out /tmp/eval-report.json
node --test test/eval.harness.test.ts
```

### The `--backend agentware` stub

The CLI recognizes `--backend agentware` but exits 2 immediately with the stable message
`"eval harness ready — agentware backend not wired (exit 2)"`. This stub exists so CI and
the deployment contract can assert the harness binary is the expected version without
requiring a real agent backend. When the real backend is implemented, it must:

- Implement `EvalBackend` in `src/eval/agentwareBackend.ts` (the `eval` method takes an
  `EvalCase` and an `AbortSignal`, returns an `EvalTrace`).
- Be constructed in `src/eval/cli.ts` when `--backend agentware` is passed.
- Import lane types only through the interface seam in `src/eval/types.ts`, not through
  `src/tools/` or `src/governor/` directly.

Until that day, any attempt to use `--backend agentware` must fail with the same stub to
preserve the CI contract.

## Agentware evals (HaikeiLabs/Agentware)

- Python: `python/src/evals/` (`main.py`, `models.py`, `runner.py`, `cases/{calendar,file_search,general,github}.py`),
  run with `PYTHONPATH=python/src python3 -m evals.main`. The root `testing/evals/` contains
  only stale `.pyc` — the live source is `python/src/evals`.
- Go: `go/evals/` + `go/cmd/evals`.
- TypeScript: `typescript/src/evals/` (`index.ts`, `models.ts`, `runner.ts`, `main.ts`,
  `cases/{general,file_search}.ts`), run with `node dist/evals/main.js`.
- Docs: `docs/evals/README.md` and `docs/evals/examples/{ollama_example.py,openai_example.py}`.

## Validation commands

```bash
# TypeScript ingress harness
node --test test/eval.harness.test.ts
node --experimental-strip-types src/eval/cli.ts --backend scripted --suite eval/fixtures/<lane>.golden.json

# agentware python evals
# Run from the HaikeiLabs/Agentware repo: cd python && pytest
```

## Realistic usage boundaries

- When describing the golden-fixture JSON contract always refer to it as `EvalCase` by type name (e.g. "EvalCase requires id, lane, input").
- When describing per-case cancellation always refer to `EvalRunner` by class name (e.g. "EvalRunner owns a per-case AbortSignal").
- When listing trace step kinds always mention that the trace and report schema versions are pinned constants.
- When adding or changing a golden fixture always say that the test asserts the case counts, so
  removing a case is a breaking change.
- **Do not** wire `--backend agentware` or invent an agentware runner. The contract is the
  seam: a future backend implements `EvalBackend` in `src/eval/agentwareBackend.ts` and is
  constructed in `cli.ts`. Until then, `agentware` must exit non-zero with the stable stub
  message so CI can assert the harness exists without mocking an agent.
- **Do not** import lane/product code or agentware into `src/eval/types.ts` — the types are
  pure data and the seam is interface-only.
- **Do not** let a scripted case touch the network, filesystem, or a timer; determinism is
  the point. Golden `expect` is populated verbatim from fixture JSON and asserted without
  interpretation.
- **Do not** add free-form error strings to traces or reports; the error contract is closed
  (`backend-threw`, `aborted`, `invalid-case`, `backend-error`, and the pinned stub text).
- Keep golden cardinality pinned: `test/eval.harness.test.ts` asserts the case counts. A
  removed case is a break.

## Related skills

- `kei-tool-adapters` — the tool lanes and closed command parsers that the golden fixtures
  pin.
- `kei-openai-backends` — the model backends that the agentware evals drive.
- `agentware-sdk` — the middleware that the future `agentware` eval backend would integrate
  with.
