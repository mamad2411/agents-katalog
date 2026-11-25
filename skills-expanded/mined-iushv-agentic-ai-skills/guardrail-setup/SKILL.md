---
name: guardrail-setup
description: Add a defense-in-depth guardrail pipeline — schema validation, prompt-injection detection, SQL and code-execution sandboxing, PII scrubbing, and tests for every layer. Use this whenever the user asks about agent safety, prompt injection, jailbreaks, input validation, output filtering, PII leakage, or hardening an agent after a security review or incident.
---

# Guardrail Setup

Generate a defence-in-depth guardrail package and drop it into an existing
project. Six layers, every one with tests that cover both what must be blocked
and what must still get through.

This skill ships a working generator. Run it rather than pasting snippets.

## When to Use

- Adding guardrails to an agent that has none.
- Filling in missing layers on an agent that has some.
- Hardening after a security review, a jailbreak report, or an incident.

## Generate the package

Pick the layer 5 flags that match the risks the agent actually carries:

```bash
python scripts/add_guardrails.py --out ./myproject/guardrails --sql --files
```

| Flag | Add it when |
|---|---|
| `--sql` | any tool issues SQL |
| `--files` | any tool reads or writes files |
| `--code-exec` | any tool runs model-supplied code |
| `--all-guards` | all three |

Other options: `--package` (importable name, defaults to the directory name),
`--max-query-chars` (layer 1 ceiling, default 5000), `--dry-run`, `--force`.

Then run the tests, which need only `pytest` and `pydantic`:

```bash
pytest ./myproject/guardrails
```

A minimal package is 13 files and 53 tests; with every guard it is 19 files and
108 tests. If they do not pass, stop and fix that before wiring anything up.

## What gets generated

```
guardrails/
├── schema.py           # L1: length, null bytes, unicode normalisation
├── content_filter.py   # L2: injection patterns, untrusted-content fencing
├── classifier.py       # L3: seam + NullClassifier (see below)
├── semantic.py         # L4: exfiltration, escalation, prompt extraction
├── output.py           # L6: PII, prompt-leak, grounding
├── pipeline.py         # Orchestrates 1-4 in, 6 out
├── tool_guards/        # L5: only the guards you asked for
│   ├── sql.py          #     read-only enforcement, LIMIT injection
│   ├── paths.py        #     traversal confinement, executable-write refusal
│   └── sandbox.py      #     sandbox spec assertions, docker flag rendering
└── tests/              # Blocking and passing cases for every layer
```

Templates live in `assets/`. Read one there rather than guessing.

## Wiring it in

```python
from guardrails import GuardrailPipeline, GuardrailBlocked

pipeline = GuardrailPipeline(system_prompt=SYSTEM_PROMPT)

try:
    report = await pipeline.check_input(user_query)
except GuardrailBlocked as exc:
    log.warning("blocked at %s: %s", exc.layer, exc.reasons)
    return "I can't process that request."

answer, tool_outputs = await run_agent(report.validated.query)

out = pipeline.check_output(answer, tool_outputs=tool_outputs)
return out.text
```

Layer 5 is not called from the pipeline. Tool arguments only exist at the call
site, so guards go inside each tool:

```python
from guardrails.tool_guards import validate_sql

safe = validate_sql(query)    # raises ToolBlocked
return await db.fetch(safe)   # execute the returned string, not the original
```

Catch `ToolBlocked` in the agent loop and return it to the model as a tool
error, so it can correct itself instead of seeing an opaque crash.

## Design decisions worth keeping

These are load-bearing. Changing them weakens the pipeline in ways that are not
obvious from reading the code.

- **Order is cheap-to-expensive.** Deterministic checks run before the
  model-backed one, so an obvious attack never costs an inference call. A test
  asserts this.
- **Layer 3 ships inactive and says so.** `NullClassifier` reports
  `active=False`, which surfaces in `InputReport.layers_run`. A stub that
  silently approves everything is worse than no layer, because it looks like
  coverage.
- **Not every flag blocks.** Exfiltration and prompt extraction block;
  escalation wording is advisory, because "who has admin access here" is a
  normal question. Blocking everything produces an outage, not a guardrail.
- **SQL comments are rejected, not stripped.** Stripping would leave the
  validator reasoning about different text than the database executes.
  `validate_sql` returns normalised SQL — execute that, not the original.
- **Output guardrails never raise.** A bad answer is cleaned and reported. A
  dropped answer is an outage.

## After generating

1. **Tune the pattern lists** in `content_filter.py` and `semantic.py` against
   your own traffic. When you add a pattern, add a benign phrase that must
   still pass alongside it.
2. **Implement layer 3** if the agent is exposed to untrusted users. The seam
   is already wired; supply a `Classifier`.
3. **Set alerts** on block rate per layer. A sudden rise is either an attack or
   a regression, and both are worth a page.
4. **Feed incidents back.** Every jailbreak that gets through should leave a
   test behind.

Then run `/agentic-design-review` to check the rest of the agent.

## Extending the templates

Edit `assets/`, not generated output. Templates use `string.Template` syntax
(`${name}`), so a literal dollar sign must be written `$$` — the regex anchors
in `schema.py.tmpl` are the example to copy. After editing, regenerate in both
the minimal and `--all-guards` configurations and run both test suites.
