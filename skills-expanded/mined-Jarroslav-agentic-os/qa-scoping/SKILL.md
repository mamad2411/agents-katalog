---
name: qa-scoping
discoverable: false
description: >-
  Plans and reviews QA on a per-feature basis, in three modes that sdlc-engine
  invokes directly: --checklist (Phase 6) turns requirements and QA knowledge into
  qa-checklist.md before implementation starts; --review-tests (Phase 8) reviews
  the tests that were written for quality and completeness; --update (Phase 11)
  refreshes qa-health.md once gate-runner has passed. Not for: direct user
  invocation (sdlc-engine owns its three modes), building the QA foundation
  (qa-baseline), or executing gates (gate-runner).
version: 0.1.0
license: Apache-2.0
---

# qa-scoping

## Shared contract preflight

Before workflow actions, send this JSON request to the installed plugin's
`runtime/run.py` using Python 3.10+ (resolve the plugin root on the current host):

```json
{"api_version":"1.0.0","operation":"policy.resolve","entrypoint":"qa-scoping"}
```

Use the returned policy and `references/runtime-contracts.md` for contract identifiers,
limits and dependency floors. Unknown fields or incompatible versions block startup.
Task envelopes use `contract_version: "1.0.0"` and `task_input`; legacy `raw_input`
is accepted only by the explicit `input.normalize` compatibility adapter with `legacy: true`.
This preflight validates policy; durable lifecycle and host enforcement are separate
capabilities. Never infer those capabilities from a successful policy response.

For a managed run, follow [`references/runtime-authority.md`](../../references/runtime-authority.md):
record QA gate decisions and evidence through runtime operations and use
`legacy.export` for compatibility ledgers. Direct JSONL appends never advance a run.


Everything QA between "we know what we are building" and "the health record is
current": decide what must be tested, judge what was tested, write down what
changed.

**Prerequisites:** `.agentic/guides/testing/qa-strategy.md` and `.agentic/guides/testing/qa-health.md`
must already exist. If either is missing, halt with:
```
[QA GUIDE MISSING] .agentic/guides/testing/qa-strategy.md not found.
Run the `qa-baseline` skill to generate the QA knowledge foundation first.
```

Both documents this skill writes are specified in
`references/qa-artifacts.md`. Follow it exactly — the pipeline and the Phase 7
reviewer parse what comes out.

Every mode takes the same two arguments: `run_dir` (absolute) and `merge_base`
(`origin/main` unless told otherwise).

---

> **Methodology owner.** What a well-shaped test case set covers is defined by the `test-cases`
> blueprint in `agentic-qe`
> (`skills/qe-blueprints/references/catalog/design/test-cases.md`). This skill
> executes; the blueprint is the authority on method. If the two ever disagree,
> the blueprint wins and this file is what gets corrected — one source of truth,
> so two agents cannot follow two different sets of practices.

## Mode: `--checklist` (Phase 6)

Runs before implementation. The output is a claim about what this change has to
get right, made while it is still cheap to disagree.

### Gather the inputs

Read, in this order: `<run_dir>/requirements.md` (required — halt if absent),
`<run_dir>/design.md` (skip if absent), then
`.agentic/guides/testing/qa-strategy.md` and
`.agentic/guides/testing/qa-health.md`.

### Work out what this change touches

From the requirements, name four things:

- **Modules** — the paths, packages or domains the work lands in.
- **Surfaces users meet** — endpoints, screens, commands.
- **Risk flags** — auth, payments, data migration, security, breaking change.
- **Search terms** — three to six words (class, endpoint, domain nouns) good
  enough to find existing tests with.

### Ask what already covers it

Two independent questions, and neither is allowed to stop the run when it cannot
be answered.

*Recorded test cases.* Read
`qa-strategy.md → External Sources → Test Case Management → Adapter`. When an
adapter is configured, query it for cases against those modules using the search
terms, take at most 30, and keep each case's ID, title, kind and status. Sort
them into: a passing automated test (`covered`), a test that exists but fails or
has gone stale (`gap`), or a manual case (`manual`). When there is no adapter, or
it cannot be reached, record the coverage as `unknown` and move on. `unknown` is
a true statement about your knowledge; `gap` is a claim about the code. Do not
substitute one for the other.

*The external harness.* Read `qa-strategy.md → Integration Tests` and
`→ End-to-End Tests`. If a harness path is documented, grep it for each module
and search term and note what you find as
`{module: "<name>", existing_harness_tests: ["<path>::<test_name>", ...]}` — a
hit is `covered` for that module, silence is a `gap`. With no harness path
documented, skip this entirely and generate no harness rows later.

### Turn gaps into candidate scenarios

Walk `qa-health.md → Risky Untested Areas` and keep every entry that overlaps
the modules from above; each becomes a high-risk blocking scenario.

Then, only if the harness scan ran, read the harness coverage areas from
`qa-strategy.md` (`e2e/`, `integration/`, or named feature subdirectories) and
decide for each module whether it falls inside one — by path convention, marker
or description. A module inside a coverage area with no harness test becomes a
deferred harness scenario; one that already has a test is recorded as covered
there.

### Write the checklist

Write `<run_dir>/qa-checklist.md` in the shape given by
`references/qa-artifacts.md`.

**Blocking scenarios** — always present. Earn a row for every surface users
meet, every risk flag, and every overlapping gap found above (those at high
risk). Each row's *first failing assertion* has to name the call, the input and
the result, because the next person's job is to paste it into a failing test.

**Deferred to the harness** — only when qa-strategy.md documents a harness. One
row per module sitting inside a coverage area. `Covered today` is
`covered (<test>)` where the scan found one, `gap` where the area matched but
nothing tests it, `unknown` where the harness could not be read. `Where it goes`
is a real path.

**Deferred to manual** — only when a test case adapter is configured. Stale or
failing manual cases from the adapter, plus new manual scenarios for any
user-facing surface nothing automated reaches. `Where it goes` names the system
and project concretely.

Sections with nothing to say are omitted, not left empty with a "none".

### Check your own work

Before the gate, confirm all four:

- [ ] every acceptance criterion in `requirements.md` shows up in at least one
      blocking scenario
- [ ] every high-risk overlapping gap is a blocking scenario, not a deferred one
- [ ] no blocking scenario is missing its first failing assertion
- [ ] every deferred row says where it goes

Fix what fails here rather than sending it to the gate.

### Gate

Call `gate-arbiter` with:
- `gate_id: "qa-checklist.approved"`
- `artifacts: [{kind: "qa-checklist", path: "<run_dir>/qa-checklist.md", summary: "<N blocking scenarios, M harness backlog, K manual backlog>", signature: "<sha-256>"}]`

HITL: show the checklist and wait. Autonomous: approve when no high-risk
blocking scenario is left unaddressed, escalate otherwise. Deferred rows never
affect this decision — that is what makes them deferred.

**Output:** `<run_dir>/qa-checklist.md`

---

## Mode: `--review-tests` (Phase 8)

Runs after the tests exist. The question is not "are there tests" but "would
these tests have caught it".

### Gather the inputs

Read `<run_dir>/qa-checklist.md` (required) and
`.agentic/guides/testing/qa-strategy.md`. Run
`git diff --name-only <merge_base>...HEAD`, keep the test files — anything under
a directory named in `qa-strategy.md → Test Frameworks`, plus `*.test.*`,
`*_test.*`, `test_*.*`, `*.spec.*` — and read each one.

### Match scenarios to tests

Only blocking scenarios are in scope; deferred rows are out of scope by
construction. For each one, look through the changed tests for the one that
addresses it and record `covered`, `partially-covered` or `missing`. Reach for
`partially-covered` honestly: a test that touches the scenario but asserts less
than the scenario claims is not covered.

### Judge each test

| Ask | It passes when |
|-----|----------------|
| Could this assertion fail? | It pins an actual value or error, so a regression changes the result — not merely that something was returned or nothing threw |
| Does the name survive the failure? | Reading the name in a red CI log tells you what broke, without opening the file |
| Does it stand alone? | No importing from sibling test files, no state shared with its neighbours, no dependence on running order |
| Does it look like its neighbours? | It follows the naming and layout in `qa-strategy.md → Conventions`, so the suite still reads as one thing |

### Write the review

Write `<run_dir>/qa-test-review.md` per `references/qa-artifacts.md`. `PASSED`
requires both: every high- and medium-risk blocking scenario covered, and no
high-severity finding.

### Gate

Call `gate-arbiter` with:
- `gate_id: "qa-tests.approved"`
- `artifacts: [{kind: "qa-test-review", path: "<run_dir>/qa-test-review.md", summary: "<status, covered N/total blocking, H high M medium issues>", signature: "<sha-256>"}]`

Approved, and the pipeline continues. On `request-changes` the pipeline sends a
fix-up task at the high-severity findings and this mode runs once more — once,
not until it passes.

**Output:** `<run_dir>/qa-test-review.md`

---

## Mode: `--update` (Phase 11)

Runs after gate-runner is green, so the health record reflects what this run
actually changed rather than what it intended to.

Find the changed test files exactly as `--review-tests` does. For each, work out
which source modules it covers, from its imports or the path convention in
`qa-strategy.md`.

Then update `.agentic/guides/testing/qa-health.md`:

- a risky untested area that new tests now cover leaves the gap list and joins
  the coverage summary with its new percentage
- a source file this run touched without adding tests joins the risky untested
  areas
- "Last assessed" becomes today

Leave every section this run did not touch exactly as it was.

**Output:** updated `.agentic/guides/testing/qa-health.md`
