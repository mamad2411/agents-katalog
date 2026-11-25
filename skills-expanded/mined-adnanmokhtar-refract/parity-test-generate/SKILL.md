---
name: parity-test-generate
description: Generate a parity test suite that runs V1 + V2 against identical inputs and asserts equivalence per the contract's tolerance taxonomy. Combines golden master, record-replay, property-based, and (when applicable) shadow / dual-write audit techniques. Outputs runnable tests and a tolerance configuration file.
kind: skill
pack: migration
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# parity-test-generate

Build the test suite that gates cutover. The suite is V2's spec — V2 is "done" when this suite is green against the pinned V1 commit.

## Premise

The contract is the truth. Mirror; never invent. Every input in the corpus traces to a section of `ai/migration/contracts/<feature>.md` (happy path, error path, business rule, edge case, replay sample) — never a fabricated case to round out coverage. Every entry in `tolerance.yaml` covers a field declared in the contract's Outputs section; "ignore" is a contract decision, not a convenience. Golden snapshots are captured against the pinned V1 commit and never blanket-refreshed with `--update-snapshots`. The parity oracle is V1's actual behaviour at the pinned SHA, not "what the test author thought V1 did".

## Halt conditions

- Halt on corpus inputs that don't map to a contract section (corpus distribution check D1).
- Halt on tolerance.yaml fields not declared in the contract's Outputs (tolerance coverage check D2).
- Halt on parity runs whose `v1_commit` doesn't match the ledger's `v1_commit_pinned` (D4).
- Halt on snapshot updates without a reviewer note + ledger entry (D7); never run blanket `--update-snapshots` to make red green.
- Halt on a comparator that has not passed calibration (step 4b): a control-vs-control run that is not clean, or a seeded mismatch it does not report, means "0 mismatches" proves nothing.
- Halt on a heavy-tier corpus whose V1 branch coverage is below the declared floor (step 2b) — the input COUNT is not the floor.

This skill is the procedural arm of `migration-discipline.md` + `parity-testing.md` + `feature-port.md` Phase 4.

## When to use

- A feature has a contract (`ai/migration/contracts/<feature>.md`) and is in state `In-progress` or transitioning to `V2-shadow`.
- The contract was revised (e.g., parity-test failure surfaced a missing case) — regenerate / extend the suite.
- Cutover deadline approaching and the existing suite has tolerance gaps the auditor flagged.

## When NOT to use (refuse + explain)

- No contract yet — run `extract-v1-contract` first. Without a contract, "parity" has no definition.
- V1 is being modified — pin V1 first; otherwise tests run against a moving oracle.
- The feature has no V1 (greenfield V2 feature on the new system) — there's nothing to be parity-equivalent to. Write regular unit/integration tests.

## Prerequisites

- `ai/migration/contracts/<feature>.md` exists + is reviewed.
- V1 commit pinned in `ai/migration/ledger.md` row for this feature.
- Test framework + parity test root extracted in `_extracted-codebase.md`.
- For record-replay: access to a production traffic sample source (or instructions for capturing one safely with anonymisation).
- For shadow / dual-write: infra is set up (router with mirror, comparison sink, schema for dual-write store).

## Procedure

### 1. Decide the recipe mix

Pick from `parity-testing.md` based on feature shape:

#### Backend / API / job / CLI features

| Feature shape | Recipes |
|---|---|
| Pure / deterministic, well-defined inputs | Golden master + property-based |
| Read-heavy, production-traffic-exposed | Record-replay + shadow |
| Write-heavy, mutating | Record-replay + dual-write audit |
| Mixed read/write | All four (shadow read, dual-write writes) |
| Tiny / utility-shaped | Golden master only |

#### Frontend features (page / component / route / screen)

Frontend ports add specific recipes — generic golden-master alone is insufficient because the contract surface includes DOM affordances, event handlers, accessibility, and reactive lifecycle which generic JSON-output golden master cannot pin.

| Feature shape | Recipes | Tooling |
|---|---|---|
| Page with inline business logic | Page-level mount + driver-test the page's exposed surface (the project's component-instance / imperative-handle / expose primitive — see the project's frontend pack for the concrete API) + DOM assertion | The project's component-test runner |
| Page with shared-logic primitive (hook / composable / mixin / store) extracted | Shared-logic golden master (unit-test the primitive directly) + page-level smoke test | The project's unit-test runner + component-test runner |
| Component (reusable) | Component-level snapshot per render-state + interaction test (click/submit/change) | The project's component-test runner / visual-regression tooling |
| User flow (multi-page) | E2E parity — drive V1 + V2 in parallel; compare DOM / screenshots | The project's E2E browser-driver tool |
| Visual fidelity | Visual regression (pixel-level with tolerance) | The project's visual-regression tool |
| Accessibility | a11y baseline + diff | The project's a11y-audit tool (e.g., axe-core or framework equivalent) |
| Multi-locale | Render in every locale; assert i18n keys + RTL/LTR flip | The project's component-test runner + i18n harness |

**Frontend recipe details:**

- **Page-level mount + driver test**: render the V2 page with mock services; drive interactions; assert the resulting requests / store mutations / route pushes / toast invocations match the V1 contract. Use the project's component-instance / imperative-handle / expose primitive when business logic is inline.
- **Shared-logic golden master**: extract logic to the project's shared-logic primitive (hook / composable / mixin / store helper); test the primitive's exposed API as a unit. The page becomes a thin wrapper — much easier to test. Encouraged by `migration-discipline.md` § Frontend anti-patterns ("Per-page inline business logic" → fix: extract to shared-logic primitive).
- **Component snapshot per state**: render the component with N input states (loading / loaded / empty / error / readonly / etc.); snapshot each. Combine with interaction tests (click button → assert event emitted).
- **E2E parity**: high-confidence but slow + flaky-prone. Reserve for high-traffic flows (auth, checkout, ordering). Drive Playwright against both V1 and V2 hosts; capture and compare.
- **Visual regression**: use a tolerance threshold (e.g., 0.1% pixel diff) to absorb minor anti-aliasing / font-rendering differences. Pin a single browser + viewport.
- **a11y diff**: axe-core baseline against V1; assert V2 has ≤ V1 violations (V2 may be stricter and have *fewer* violations — that's a win, not a regression).
- **Multi-locale**: parameterise tests over the locale list; assert keys resolve in each locale; verify RTL/LTR layout flip; verify date / number / currency formatting per locale.

#### Auto-import test-config requirement (frontend)

Any test that mounts a leaf-component / view-template file from a project that uses any auto-import plugin (build-tool plugin, framework auto-import, IDE-driven import-on-resolve) requires the SAME plugin in the test config. Otherwise auto-imported helpers (i18n hook, router hook, reactive primitives, etc.) resolve in production but not in tests. **First mount fails with `<helper-name> is not defined`-type errors.** This is the named "Auto-import Trip" anti-pattern in `ai/patterns/migration-guardrails.md` § Named anti-patterns; pre-empt it by writing the test config alongside the test files.

#### Route-cache-aware mount (when the project's stack supports route caching)

For pages whose data fetch fires on the project's route-cache reactivate hook (concrete hook varies by stack — see the project's frontend pack rule § Lifecycle), the test mount MUST simulate the cache so the reactivate hook fires:

```pseudo
mount(Page, {
  // wrap the page in the project's route-cache shell
  // so the reactivate hook fires during the test
  wrapper: <project's route-cache wrapper component>,
  options: { /* ... */ }
})
```

Otherwise reactivate-fired API calls don't run and the mock-call assertion fails. This is the named "Wrong Lifecycle Hook on Nested Child" anti-pattern in `ai/patterns/migration-guardrails.md` § Named anti-patterns.

Aim for ≥2 recipes per non-trivial feature so a gap in one is caught by another.

### 2. Build the input corpus (golden master)

`<parity-test-root>/<feature>/inputs/`:

- **Happy paths**: at least one input per documented happy code path.
- **Each error path**: at least one input that triggers it (per the contract's `Outputs § Error path: <name>` sections).
- **Each business rule**: ≥2 inputs — one that triggers the rule, one that doesn't (boundary tests).
- **Each edge case**: from `Edge cases V1 handles` in the contract — empty, null, oversize, malformed, Unicode, concurrent (where representable).
- **Production samples**: 50–100 anonymised inputs from real traffic (if record-replay is in use, reuse the corpus).

**Tier-aware corpus floor** (per ledger row's `tier:` field):
- **Heavy tier**: ≥30 inputs OR a record-replay corpus. This is the historical floor.
- **Standard tier**: ≥10 inputs covering happy + error + at least one edge case per documented contract output path. No record-replay required.
- **Trivial tier**: skip parity tests entirely — the project's standard CI suite is sufficient. Do NOT generate a corpus, tolerance.yaml, or golden snapshots.

If a feature's tier isn't set in the ledger, default to **trivial** — the same default as `extract-v1-contract`, the validator (`validate_feature`) and the rule; an audit promotes it. See `migration-discipline.md` § Required artifacts per feature — tiered floor.

### 2b. Measure what the corpus reaches in V1 (heavy tier; standard when the row has a money or write path)

Thirty files can all walk the same happy path. The file-count floor above stays, and beside it the corpus must reach V1's branches (oracle V387, `proof-oracles.md` § Migration):

1. Run V1 at the pinned SHA under its own coverage tool (Xdebug or PCOV for PHP, coverage.py, SimpleCov, JaCoCo, c8/istanbul, `go test -cover`) while replaying the corpus.
2. Record branch coverage of the feature's V1 files (the contract's cited paths) in `<parity-test-root>/<feature>/v1-coverage.json`, with the V1 SHA.
3. Declare the floor in the ledger row (`v1_branch_floor:`; 80% of the feature's V1 branches unless the audit argues another number). Below it, list every unreached V1 branch as `file:line` and add an input that reaches it, or record why it is unreachable (dead on the six halt-11 axes).
4. When the testing pack is installed, its `mutation-probe` run on **V1** answers the next question: does the parity assertion fail when V1's behaviour changes? Without it, say the oracle strength is unmeasured.

No V1 coverage run (no bootable V1, no tool) → the floor is `UNVERIFIED`, never met.

### 3. Capture V1 outputs (golden snapshots)

Run V1 against the corpus once, in a controlled environment (test DB seeded; deterministic time/random; no external calls real or stubbed):

```bash
# Stack-equivalent capture script (the project's runtime + entry point).
# Examples per common stacks — pick the one matching `_extracted-codebase.md § Stack`:
#   Node:    node   scripts/parity/capture-v1.js  --feature=<feature> --inputs=<inputs> --outputs=<golden>
#   Python:  python scripts/parity/capture_v1.py  --feature=<feature> --inputs=<inputs> --outputs=<golden>
#   Go:      go run scripts/parity/capture_v1.go  --feature=<feature> --inputs=<inputs> --outputs=<golden>
#   Ruby:    ruby   scripts/parity/capture_v1.rb  --feature=<feature> --inputs=<inputs> --outputs=<golden>
#   Java:    ./mvnw exec:java -Dexec.mainClass=parity.CaptureV1 ...
#   .NET:    dotnet run --project tools/Parity.CaptureV1 -- --feature=<feature> ...
<runtime> <capture-script> \
  --feature=<feature> \
  --inputs=<parity-test-root>/<feature>/inputs \
  --outputs=<parity-test-root>/<feature>/__golden__
```

The capture script:
- Resets seed data + time mocks before each input (otherwise non-determinism poisons the snapshots).
- Records V1's output **per the tolerance taxonomy** — strip / normalise volatile fields BEFORE saving, so future diffs surface only the things the contract pins.
- Saves alongside: the V1 commit hash, the captured input, the captured output, the contract revision used.

Commit `__golden__/`. These snapshots are sacred — no `--update-snapshots` blind refresh.

### 4. Build the tolerance file

`<parity-test-root>/<feature>/tolerance.yaml`:

```yaml
exact:
  - $.id
  - $.status
  - $.error.code
structural:
  - $.created_at
numeric_tolerance:
  $.total: 0.01
order_insensitive:
  - $.tags
ignore:
  - $.debug
  - $.x_request_id
```

Generate this from the contract's **Outputs** section. Each field listed in the contract gets a tolerance — `exact` if it's a stable contract value, `structural` if it's volatile-but-shape-pinned, `ignore` if the contract explicitly excludes it.

**These five keys are the only taxonomy** — `exact` · `structural` · `numeric_tolerance` · `order_insensitive` · `ignore`. They are what `check_tolerance_coverage` reads, what `tolerance.json` mirrors, and what `behavior-diff.py` applies. Older prose names other kinds (`timestamp-insensitive`, `dom-equivalent`, `allowed-divergence`); each is one of the five plus a path list (a timestamp is `structural`; a DOM comparison is the frontend recipe's comparator, not a tolerance key; an allowed divergence is an ADR, not a key).

**`structural` never hides presence.** A `structural` field must still be present when V1's is present, absent when V1's is absent, and `null` when V1's is `null`; `[]` and `{}` are different values. A comparator that passes `null` against a missing key is itself a defect (CO-4, presence precedent in `precedents/migration.md`).

### 4b. Calibrate the comparator before trusting it

A comparator that reports "0 mismatches" has proved nothing until it has shown it can see one (oracle V385):

- **Control vs control.** Capture V1 twice on the same corpus (fresh seed, same clock mock) and diff V1 against V1 with the tolerance file. Every difference is noise the capture failed to pin: fix the capture. Only fields that differ between two V1 runs may sit under `structural` or `ignore` (the calibration precedent; Scientist's control-vs-control and Diffy's primary-vs-secondary are the same rule).
- **Seeded mismatch per key.** For each tolerance key in use, mutate one golden output (a changed `exact` value, a dropped `structural` key, a `numeric_tolerance` value just past the bound, a reordered `exact` list) and confirm the comparator FAILS. A key whose seeded mismatch passes is wider than declared.
- **Errors compared, not just status.** Both sides raising counts as a match only when the error class, status and `code` are equal; a status-only compare is a blind spot.

Record both runs beside the suite (`calibration.json`: V1 SHA, keys seeded, result). When the repo has `.claude/scripts/behavior-diff.py` (the repo-baseline gate scripts), it is the comparator for both checks — the same five-key engine G14 runs.

**Tier-aware tolerance scope**:
- **Heavy tier**: every output field across every code path in the 9-section contract gets a tolerance entry. `check_tolerance_coverage` halts on any uncovered field.
- **Standard tier**: every output field declared in the standard-tier 3-section contract (Inputs/Outputs/Known V1 bugs) gets a tolerance entry. The contract has fewer fields by design; coverage is still mandatory for the fields it declares.
- **Trivial tier**: N/A — no parity tests, no tolerance.yaml.

### 5. Author the golden-master test

```pseudo
// Pseudocode — adjust to the project's test framework + path conventions from extraction.
// Concrete syntax depends on stack (xUnit / RSpec / pytest / go test / JUnit / ExUnit / vitest / jest / etc.).
import runParity from "<helpers>/run-parity"

testGroup("feature parity (golden master)") {
  runParity({
    feature:   "feature",
    corpus:    "<parity-test-root>/feature/inputs",
    golden:    "<parity-test-root>/feature/__golden__",
    tolerance: "<parity-test-root>/feature/tolerance.yaml",
    runV2:     (input) => v2.handleFeature(input),
  })
}
```

`runParity()` is a shared helper (one per project) that loads inputs + golden + tolerance, runs V2, applies tolerance-aware diff, asserts equivalence. The skill creates this helper if it doesn't already exist (Phase 4.6 anchors it to the project's test framework).

### 6. Author property-based tests

For each invariant in the contract's **Invariants** section, add a property test using the project's property-based testing library (e.g., fast-check / Hypothesis / PropEr / QuickCheck / jqwik / RapidCheck — pick the one in `_extracted-idioms.md § Test stack`):

```pseudo
property("V1 ≡ V2 totals (within $0.01) — invariant: total = sum(lines) + tax",
  forall(validOrderGen, (order) => {
    v1 = handleV1(order)
    v2 = handleV2(order)
    assert close_to(v2.total, v1.total, 0.01)
  }))
```

Generators (`validOrderGen` here) must reflect prod input distributions — calibrate against the replay corpus's input shapes (sizes, value ranges, locale variations).

### 6b. Side effects and permissions are compared too (write paths and guarded routes)

An output-only suite passes a V2 that returns the right JSON and never sends the email. Two recipes cover what the response cannot show:

- **Side-effect journal (V371).** For each write route in the contract's Side effects section, run V1 and V2 on the same input with every outbound channel captured: outbound mail (Mailpit or the framework's mail fake), outbound HTTP (WireMock or MockServer journal), queue messages (a test consumer on the topic) and row deltas on audit / activity tables. Diff the two **multisets** of (channel, target, kind). Variants: create, update, delete, restore, bulk, queued vs sync. In shadow mode the candidate must emit zero external effects.
- **Permission matrix (V359).** For each guarded route, replay (role × route × resource owner) on V1 and V2: anonymous, each role, owner vs non-owner, another tenant, suspended user, API token vs session, HEAD and OPTIONS. Each cell compares the status class. V2 allowing a cell V1 denies is widening (a blocker; security owns it when that pack is installed); denying a cell V1 allows is narrowing.

Both need a runnable V1. Without one, the row's parity claim for side effects or permissions is `NOT-RUN`, never PASS.

### 7. Build the record-replay harness (when applicable)

```text
1. Capture production traffic samples (input, V1 output) → <parity-test-root>/<feature>/replay/<NNN>.json
   - Anonymise PII at the tap. Don't capture anything that can re-identify a user.
   - Include 1000+ samples for high-traffic features; 100+ for low-traffic.
   - Refresh weekly OR on every V1 deploy that touches the feature.

2. Replay test:
   for sample in replay/*.json:
     v2_output = run_v2(sample.input)
     assert tolerant_equal(v2_output, sample.v1_output, tolerance)
```

The replay corpus is checked in alongside the test, anonymised; raw production data NEVER leaves production. The capture pipeline + anonymiser are themselves audited (see `security/` pack if available).

### 8. Configure shadow / dual-write (for production-stage cutover)

These are infra, not tests — but `parity-test-generate` produces the *comparator* that shadow / dual-write infra runs:

```python
# pseudocode comparator service
def compare(v1_response, v2_response, tolerance):
    diff = tolerant_diff(v1_response, v2_response, tolerance)
    if diff:
        emit_metric('parity_mismatch', tags={'feature': '<feature>', ...})
        log_pair(v1_response, v2_response, diff, anonymised=True)
    else:
        emit_metric('parity_match', ...)
```

Output the comparator code + a Grafana / Datadog dashboard JSON snippet that visualises mismatch_rate over time.

### 9. CI integration

- Golden-master + property-based tests run on every CI push (fast).
- A parity suite gated on V1 being present (`HAS_V1 ? describe : describe.skip`, a `V1_REPO_PATH` check) runs only in a CI job that sets the variable. Confirm one does and that its log shows more than 0 such tests executed; otherwise every claim resting on it is `NOT-RUN`.
- Record-replay tests run nightly OR on `[parity]` PR label (slower; full corpus).
- Dashboard alerts on shadow / dual-write mismatch rate > threshold (≥0.1% sustained for 1h is "wake up an engineer").

### 10. Document tolerance overrides

Every tolerance loosening (e.g., extending `ignore` to a new field, raising numeric tolerance) is a contract change:

- ADR justifying the loosening.
- Ledger note linking the ADR.
- Reviewer signoff (not the person who tightened it).

Tightening tolerance is always allowed without ceremony.

## Output format

```
<parity-test-root>/<feature>/
├── inputs/
│   ├── 001-happy-basic.json
│   ├── 002-happy-with-discount.json
│   ├── 010-error-missing-user.json
│   ├── 011-error-invalid-amount.json
│   ├── 020-edge-empty.json
│   ├── 021-edge-oversize.json
│   ├── 030-rule-001-min-order.json
│   ├── 040-prod-replay-001.json   # anonymised
│   └── ...
├── __golden__/
│   ├── 001-happy-basic.json
│   ├── 002-happy-with-discount.json
│   └── ...
├── replay/                        # if record-replay is in use
│   ├── 2026-04-25/
│   │   ├── 0001.json
│   │   └── ...
├── tolerance.yaml
├── parity.<test-ext>               # golden-master + property-based (extension per project's test stack)
└── replay.<test-ext>               # record-replay
```

Plus, optionally:

```
scripts/parity/
├── capture-v1.<ext>                # extension matches the project's scripting runtime
├── run-comparator.<ext>            # for shadow / dual-write
└── refresh-replay.<ext>            # weekly cron entry point
```

Update the ledger row's `parity_tests` to point at the directory.

## Failure modes

- **Non-deterministic V1**: golden snapshots vary run-to-run because V1 hits real time / random / external state. Strip / mock those at capture time. If V1 is fundamentally non-deterministic, the test is property-based + invariant-checked, not exact-match.
- **Replay corpus PII leak**: the anonymiser missed a field. Treat as an incident; rotate the corpus; audit the anonymiser. Never ship a parity suite whose replay corpus has been sampled but not audited.
- **Tolerance creep**: every parity diff prompts "loosen the tolerance". Reject — investigate the diff first. The default action on a parity diff is "find the V2 bug", not "make the test happy".
- **Mocked dependencies hide bugs (D5)**: V1 calls `getUser`, V2 calls `getUser`, both mocked to return the same fake — parity passes; production diverges. Use real fakes (test DB, test HTTP server) when feasible. The validator's `check_corpus_distribution` will flag suites whose corpus is suspiciously homogeneous.
- **Property generators don't reflect prod**: generators only cover small inputs, prod has 10MB inputs that V2 OOMs on. Calibrate generators against the replay corpus.
- **Tests pass but shadow shows mismatches**: the test corpus didn't cover what production sends. Add the production-divergent sample to the corpus, refresh.
- **Snapshot drift (D7)**: someone runs `--update-snapshots` to "fix CI" — the parity oracle is now wrong. CI rejects snapshot updates without a reviewer + ledger note (lint / hook). NEVER blanket-update snapshots to make red green; that erases the parity signal entirely.

### Validator-enforced failure modes (named D-series)

These fail `scripts/validate-migration-artifacts.sh` and halt the audit:

- **D1 — Corpus distribution missing**: corpus must include happy / error / edge / rule entries. Each input file's name (or a `category` field inside it) declares its bucket so `check_corpus_distribution` can verify all four buckets are populated. Suggested file-naming convention:
  - `001-happy-*.json` — happy paths
  - `010-error-*.json` — documented error paths
  - `020-edge-*.json` — edge cases V1 handles
  - `030-rule-*.json` — business rules (per the contract's named Rule-NNN)
  Or use a JSON `{ "category": "happy" | "error" | "edge" | "rule", "input": ... }` envelope. A corpus of 50 happy-path inputs and zero error/edge/rule inputs FAILS the gate even if total count ≥ 30.
- **D2 — Tolerance coverage incomplete**: every Output field in the contract (across every code path) must have a `tolerance.yaml` entry — `exact` / `structural` / `numeric_tolerance` / `order_insensitive` / `ignore`. `check_tolerance_coverage` cross-references the contract's Outputs sections against the tolerance file. Missing fields halt the gate.
- **D4 — V1 commit not pinned per parity run**: each parity run captures `{ run_id, v1_commit, v2_commit, timestamp }`. `check_parity_run_v1_commit` asserts `v1_commit` matches the ledger row's `v1_commit_pinned`. A parity run against a different V1 SHA is meaningless — the oracle moved.
- **D5 — Mocked-V1-dependency anti-pattern**: see above. Detected indirectly via corpus homogeneity + via reviewer signoff on the test harness setup.
- **D7 — Snapshot drift via blanket update**: see above.

## Baseline registration

This golden-master layout (`inputs/` and `__golden__/` with matching file names, plus the five-key tolerance taxonomy) is the format the testing pack's `characterize` reuses. Once the golden-master test is green against V2, register the feature in the behavioural-baseline registry (`.claude/baselines/main/manifest.json`, proposal §7), so gate G14 guards every later V2 edit against the pinned V1 behaviour:

```bash
bash .claude/scripts/baseline-capture.sh register --id=parity-orders --kind=characterization \
  --engine=migration/parity-test-generate --scope='<v2-root>/orders/**' \
  --command='node scripts/parity/capture-v1.js --feature=orders --inputs=tests/parity/orders/inputs --outputs="$REFRACT_BASELINE_OUT"' \
  --harness=tests/parity/orders/inputs,scripts/parity/capture-v1.js --tolerance=tests/parity/orders/tolerance.json \
  --artifact=tests/parity/orders/__golden__ --compare=golden --cadence=pr --no-capture
```

- The command is step 3's capture script pointed at **this** checkout's entry point (V2), writing one output per input name. `--harness` carries the corpus and the script into the base-sha worktree.
- **`--no-capture` is mandatory.** A capture would replace V1's golden snapshots with V2's own output and erase the oracle (D7).
- **Tolerance as JSON.** The gate scripts are standard-library only and never parse YAML. `tolerance.yaml` stays this skill's file (D2 checks it), and registration mirrors it to `tolerance.json` with the same five keys. Re-mirror it whenever step 10 changes the YAML.
- **Run the comparator.** After registration, `python3 .claude/scripts/behavior-diff.py --gate=G14 --entries=parity-orders` runs the comparison now (exit 0 PASS, 1 FAIL, 3 UNVERIFIED — an entry that could not run is never a pass). Use it for step 4b's calibration and as the parity run whose result and V1 SHA go into the ledger's `parity_runs`.
- **Gate G14**: `characterization` is a quick kind. It re-runs at Stop when in scope and in full in CI. A case that differs on purpose is declared by an acceptance criterion, `changes_baseline: ["parity-orders/<case>"]`. A rewritten `__golden__/` file with no criterion naming it fails `test-integrity.py` (`undeclared-baseline-rewrite`), on top of D7's reviewer and ledger note.

## Related

- `parity-testing.md` — recipe details; its tolerance section maps onto the five keys above.
- `proof-oracles.md` § Migration — V359 (permission matrix), V371 (side-effect journal), V385 (comparator calibration), V386 (V1-pinned tests unmodified), V387 (V1 branch floor).
- `extract-v1-contract.md` — produces the contract this skill consumes.
- `migration-discipline.md` — the rule mandating these tests before cutover.
- `parity-auditor.md` (agent) — verifies the suite covers the contract before cutover.
- `testing/agents/tdd-orchestrator.md` (if pack loaded) — runs the suite as part of broader TDD orchestration.
- `database/skills/migration-rehearsal/SKILL.md` — runs the V2 query plan against prod-sized data; output feeds parity tests' performance assertions.
- `data-cutover-orchestrate.md` (skill) — PORTS + reconciles data across stores; this skill only COMPARES outputs. A green parity suite over an empty V2 store still fails at read-cutover — run both.
