---
name: characterize
description: Pin current behaviour before a change — golden-master capture of HTTP endpoints, CLI commands and pure functions on sampled inputs, scoped to a run's design.md files and their _graph.json callers, registered as a behavioural baseline that gate G14 re-runs at HEAD. Runs first in /add-feature P5, /refactor, /optimize, /upgrade-dep and /migrate.
kind: skill
pack: testing
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# characterize

"Behaviour preserved" is the claim every refactor, optimisation, upgrade and port makes, and the
tests that happen to exist are the only thing that checks it. They were written to prove what the
code SHOULD do in the cases someone thought of — not to record what it DOES across the cases it
actually gets. A characterization test records what it does (Feathers' term): run the code as it is
on inputs sampled from where it is really called, store the outputs, and let any later change be
compared against them. Nothing here judges whether the recorded behaviour is right.

## Premise

The recording happens **before the first edit**, at the base sha — a baseline captured after the
change can only confirm the new code agrees with itself. The format is the golden master of
`packs/migration/skills/parity-test-generate` (inputs / `__golden__` / the five-key tolerance
taxonomy), so a port and a refactor are guarded by one comparator: `.claude/scripts/behavior-diff.py`.
Inputs are sampled from real call sites and branch boundaries, never invented to round out a count.
A difference at HEAD is legal only when an acceptance criterion declares it
(`changes_baseline` in `acceptance.json`, proposal §7 rule 2); re-recording the golden files to turn
a diff green is the one move this skill exists to prevent, and `test-integrity.py` fails it.

## Halt conditions

- Halt when the scope cannot be resolved to files that exist at the base sha (a brand-new module has no behaviour to pin — say so, and characterize only its pre-existing callers).
- Halt when the working tree already carries edits to a scoped file: the capture must see the base, so run it on a clean tree or in a worktree at the base sha (`git worktree add --detach <dir> <base>`), never on half-edited code.
- Halt when a target cannot be driven deterministically and the nondeterminism is not seedable (wall clock, network, unordered iteration with no stable key) — record it as `not characterized: <why>`, never a golden file that changes every run.
- Never pass `--update-snapshots`, rewrite a `__golden__/` file, or run `baseline-capture.sh capture --out=main --rebaseline` to make a red G14 green.

## When to run

| Caller | When | Scope |
|---|---|---|
| `/add-feature` P5 (T2/T3) | after `design.md` is approved, before `@implementer`'s first task | the files `design.md` names (§ Interfaces, § Work split) + their importers |
| `/add-feature` P5 (T1) | same point | the files the plan's tasks name |
| `/refactor` | before the first edit | the resolved scope |
| `/optimize` | before the tactical sweep edits an area | the area's files |
| `/upgrade-dep` | while pinning the oracle, on the pre-upgrade tree | the modules that import the dependency |
| `/migrate` · `/port-feature` | V1 golden capture is `parity-test-generate`; for an in-place migration run this first at the pre-migration sha | the feature's V1 entry points |

A scope that an existing registry entry already covers (`bash .claude/scripts/baseline-capture.sh
list`) is captured, not re-characterized.

## Procedure

### 1. Resolve the scope

```bash
# Files the design names (T2/T3) — or pass the plan's / the refactor's paths directly.
grep -oE '`[A-Za-z0-9_./@-]+\.[A-Za-z0-9]+`' ai/runs/<run-id>/design.md | tr -d '`' | sort -u
# Their callers: importers of each file in the import graph (built by /setup-project; absent → say so).
python3 - .claude/_graph.json <file>... <<'PY'
import json, sys
g = json.load(open(sys.argv[1])); want = set(sys.argv[2:])
print("\n".join(sorted({e["from"] for e in g.get("edges", []) if e.get("to") in want})))
PY
```

A target is a **public entry point** inside that set: an exported function, a CLI subcommand, an
HTTP route. The callers decide which entry points matter — characterize the ones they call, with the
arguments they pass. No graph (`.claude/_graph.json` missing or 0 nodes) → grep the call sites by
symbol name and say `callers: grep, not graph`.

### 2. Pick the surface per target

| Surface | Drive it with | Record per case | Normalise (tolerance, not code) |
|---|---|---|---|
| Pure / domain function | a harness that imports it and calls it once per input | the return value as JSON, or `{"error": "<ExceptionType>"}` | float noise → `numeric_tolerance`; unordered collections → `order_insensitive` |
| CLI command | the built binary / script with argv + stdin per case | `{"exit": n, "stdout": …, "stderr_first_line": …}` | timestamps, paths, versions in output → `ignore` / `structural` |
| HTTP endpoint | the project's test server or app factory (in-process client, never a shared environment), seeded DB | `{"status": n, "body": …, "headers": {only the ones the contract names}}` | ids, `createdAt`, request ids → `structural`; trace headers → `ignore` |

Freeze what the harness controls before the first case: the clock (the project's fake-time helper),
random seeds, locale and time zone (`TZ=UTC`), the seed data (reset per case). An exception is
recorded as its type — a case that starts or stops raising IS a behaviour change.

### 3. Sample the inputs

`tests/characterization/<name>/inputs/NNN-<category>-<slug>.json`, each
`{"category": "happy|error|edge|rule", "source": "<where this input came from>", "input": …}` — the
envelope `parity-test-generate` § D1 uses, so its corpus checks apply unchanged.

- **Call sites first.** The literal arguments and argument shapes the callers from step 1 pass (cite `path:line` in `source`).
- **Every branch boundary.** For each conditional on an input in the target: one input on each side, and the boundary value itself (`>=` vs `>` is exactly the bug a refactor introduces).
- **Error paths.** One input per exception / error status the target can produce.
- **Sampled.** A fixed-seed sample from the project's existing factories or fixtures (`source: "sampled (seed 7) from <factory>"`) — never from production data that has not been anonymised.
- **Floor.** ≥ 1 case per branch boundary and per error path; T3 or money / auth / tenant code: ≥ 30 cases (the heavy-tier parity floor). Fewer is allowed when the target has fewer branches — say so.

### 4. Write the harness

`tests/characterization/<name>/run.<ext>` reads every `inputs/*.json`, drives the target, and
writes one file per case, **same file name**, into `$REFRACT_BASELINE_OUT`. Plus
`tolerance.json` (the five keys: `exact`, `structural`, `numeric_tolerance`, `order_insensitive`,
`ignore`; JSONPath-lite `$.ok.items[*].price`). It is JSON because the gate scripts run on the
Python standard library; a `tolerance.yaml` is not read.

```python
# tests/characterization/quote/run.py — the whole harness for a pure function (shape, not a template)
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..")))
from pricing.quote import quote
out = os.environ["REFRACT_BASELINE_OUT"]
for name in sorted(os.listdir(os.path.join(HERE, "inputs"))):
    case = json.load(open(os.path.join(HERE, "inputs", name)))
    try:
        result = {"ok": quote(case["input"])}
    except Exception as e:
        result = {"error": type(e).__name__}
    json.dump(result, open(os.path.join(out, name), "w"), indent=2, sort_keys=True)
```

Same shape per stack: a Node script importing the module, a Go `TestMain`-free `go run` program, a
CLI loop (`for f in inputs/*.json; do jq -r .input.argv[] … | xargs ./bin/tool > "$REFRACT_BASELINE_OUT/$(basename "$f")"; done`),
an HTTP loop through the project's in-process client. Mirror the project's existing test helpers;
the harness is test code and follows the testing rules.

### 5. Register, capture, verify it is deterministic

```bash
bash .claude/scripts/baseline-capture.sh register --id=<name> --kind=characterization \
  --engine=testing/characterize --command='<runtime> tests/characterization/<name>/run.<ext>' \
  --scope='<glob of the target files>' --artifact=tests/characterization/<name>/__golden__ \
  --harness=tests/characterization/<name>/run.<ext>,tests/characterization/<name>/inputs \
  --tolerance=tests/characterization/<name>/tolerance.json --compare=golden
# In a run (P5): a local capture at the base sha — what G14 compares against.
bash .claude/scripts/baseline-capture.sh capture --run=<run-id>      # or --paths=<file>,<file>
```

`register` writes the entry into `.claude/baselines/main/manifest.json` and records the golden files
at the current sha; commit the harness, the inputs, `tolerance.json`, `__golden__/` and the
manifest together. Each capture runs the harness 3 times: outputs that differ between identical runs
mark the entry `nondeterministic` with an owner and an expiry (`THR-WAIVER`) — fix the seed or the
clock, or narrow the tolerance, before relying on it; a quarantined entry is reported, not enforced.

### 6. At HEAD

```bash
python3 .claude/scripts/behavior-diff.py --gate=G14          # gate-check.py runs the same at Stop (quick kinds) and in CI
```

`SAME` — behaviour preserved, with evidence. `DIFF` — either a regression (fix the code) or an
intended change, which the run's `acceptance.json` declares on the criterion that wants it:
`"changes_baseline": ["<name>/<case>"]` (fnmatch; `"<name>"` declares the whole entry). After the
criterion's own test is green, re-record with `baseline-capture.sh capture --out=main --rebaseline
--entries=<name>` in the same change, so the rewrite and its declaration land together (without
`--rebaseline` an existing golden is kept and only checked). A deliberate slowdown on a performance
entry is declared the same way — G4 reads the same `changes_baseline`.

## Output

```
characterize — <name>   scope: <n> file(s) (<m> from design.md, <k> callers via graph|grep)
  targets:   <entry point> (<surface>) …
  cases:     <N> — happy <a> · error <b> · edge <c> · rule <d>   (sources cited per input)
  harness:   tests/characterization/<name>/run.<ext>  tolerance.json (<keys used>)
  baseline:  .claude/baselines/main/manifest.json entry `<name>` · captured ×3 @<sha> (deterministic | QUARANTINED until <date>)
  not characterized: <target> — <why>                        (one line each, never omitted)
```

## False positives / gotchas

- **A diff on a field nobody consumes** (an internal debug key) is still a diff; put the field in `ignore` with the reason in the run's ledger — and only before the change, never to absorb one.
- **Time and locale.** A harness that passes on the author's machine and differs in CI almost always read the wall clock or the machine zone. Freeze both in the harness.
- **Mocks that agree with themselves.** A characterization of code whose collaborator is mocked records the mock (parity-test-generate D5). Prefer the project's real fakes (test DB, in-process server).
- **Coverage is not characterization.** A line executed by a case whose output is not recorded pins nothing; the golden file is the assertion.

## Related

- `packs/migration/skills/parity-test-generate` — the golden-master format and tolerance taxonomy this skill reuses; V1↔V2 parity for ports.
- `.claude/scripts/baseline-capture.sh` (register / capture) · `.claude/scripts/behavior-diff.py` (G14) · `.claude/scripts/perf-compare.py` (G4, performance entries).
- `property-invariants` — properties that must hold for all inputs; characterization records what holds for the sampled ones.
- `coverage-gap` — which code no test executes (a good place to point a characterization first).
