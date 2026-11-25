---
name: harness-eval
description: >
  Measure and tune the AI SDLC harness so the pipeline delivers on a cheap model — run
  scenario × model evals against the sandbox fixture, then fix the failing instruction rather
  than raising the model tier. Use when a task only works on the expensive model, when adding
  or changing a playbook or rule, when per-PR cost is climbing, or when writing a new eval
  scenario.
---

# Harness Eval

The economic argument for the whole pipeline: if a well-described harness lets Haiku or Sonnet
produce the same PR as Opus, mass code production becomes affordable and the team stops being
hostage to one provider's top model. If it only works on the best model, the harness is
carrying none of the weight — the model is.

So the eval question is never "is this model good enough". It is **"is our harness explicit
enough for a weaker model to follow"**. Every failure has a fix in a file we control.

## Running it

```bash
make harness-eval MODEL=haiku            # or: evals/harness/run.sh --model haiku
evals/harness/run.sh --model haiku,sonnet
evals/harness/run.sh --model haiku --scenario go-endpoint --keep
```

Each run: fresh sandbox copy of `evals/fixtures/sandbox` in the temp dir → the scenario's
approved spec → `aisdlc add` + `run --once` → assertions scored against the produced branch.
`--keep` leaves the sandbox in place so you can read what the agent actually did.

Every cell is appended to `evals/harness/results.jsonl` (committed, append-only) with the
`harness` digest of the instruction tree and the `inputs` digest of the scenario. The `DELTA`
column compares each cell with the last result for the same scenario, model and inputs on a
*different* harness: `FAIL→PASS improved`, `PASS→FAIL REGRESSED`, `same harness` for a rerun,
`new` when the scenario changed. A run with a missing or duplicated cell reports nothing.

Acceptance bar for a harness change, counted over **graded** cells (the scorer reached a branch):
**Sonnet passes every scenario, Haiku passes all but one.** An ungradeable cell (`ERROR`, `—`
assertions: no task, no branch, pipeline not `done`) is never one of the allowed misses — fix
it and rerun. Below that bar, the harness is not ready — not the model.

## Diagnosing a failure

Work down this list. The answer is almost always in the first three.

| Symptom | Where the defect is |
|---------|--------------------|
| Read the wrong playbook, or several | Router row wording, or the missing closed-world rule (`task-router`) |
| Invented a convention that exists in the repo | The rule file implies it instead of stating it — add the explicit line, with an example |
| Missed a requirement entirely | The UC is not observable enough (`spec-authoring`) — it had nothing to assert on |
| Wrote code with no test, or a test with no UC id | The playbook's test requirements are not imperative enough |
| Weakened or deleted a test to get green | Expected — check the `Stop` guard hook fired; if it did not, the pattern list needs the case |
| Overstepped into unrelated code | The spec's `Out:` scope is thin |
| Ran out of budget mid-run | Too many UCs for one task — split the spec, do not raise the cap |
| Passes on Opus, fails on Haiku | The instruction relies on inference. Replace prose with a command, a table, or an example |

## Writing for the weakest model

What separates instructions a weak model follows from ones it does not:

- **Exact commands, not intentions.** `go test -race ./...`, not "run the tests".
- **One way to do each thing.** Two acceptable patterns in a rule file means a coin flip, and
  the weak model flips it differently each run.
- **Examples over descriptions.** A five-line code sample outperforms a paragraph describing
  the same shape, at a similar token cost.
- **Tables over prose** for anything with cases. Prose lets a model satisfy the clause it
  noticed; a table makes the omission visible.
- **Imperative and unhedged.** "Never delete a test" survives; "tests should generally be
  preserved" does not.
- **Say what not to do**, explicitly. Weak models pattern-match toward the average repo, so
  the local exception has to be stated.
- **Name the file to read.** "Follow the existing conventions" assumes a search the model may
  not run.

## Adding a scenario

`evals/harness/scenarios/<name>/` with `spec.md` (`status: approved`, a real use-case table) and
`scenario.json`:

```json
{
  "name": "go-endpoint", "ticket": "SBX-1", "phases": "implement qa",
  "assert": {
    "commands": ["make verify"],
    "uc_ids": ["UC-1", "UC-2"],
    "test_paths": ["services/ledger"],
    "diff_contains": ["/v1/accounts/\\{id\\}/balance"],
    "diff_absent": ["float64\\(.*Balance"],
    "files_changed": ["api/openapi/ledger.yaml"],
    "min_test_funcs": 7, "no_skips": true, "qa_verdict": "PASS"
  }
}
```

Assert on **behaviour and traceability**, not on filenames or internal structure — an agent
choosing a different-but-valid file layout is not a failure, and a brittle assertion trains you
to ignore red. Good scenarios cover a distinct risk each: a new surface, a contract change that
breaks an existing test, a second stack, a spec whose UCs span both.

Keep the fixture hermetic: no network, no `npm install`, no database. An eval that fails because
a registry was unreachable teaches nothing about the harness.

## When a scenario legitimately cannot pass

Some work genuinely needs the strongest model — dense algorithmic reasoning, a wide refactor,
an ambiguous domain call. Record that in the scenario description and set the model per task
(`aisdlc add --model opus`). What is not acceptable is defaulting everything to the top model
because one class of task needs it.
