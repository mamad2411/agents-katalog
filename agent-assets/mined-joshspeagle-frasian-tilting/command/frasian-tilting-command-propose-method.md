---
description: Scaffold a new method end-to-end via the deriver, literature-reviewer, and skeptic agents.
---

Scaffold a new method named `$ARGUMENTS` for the Frasian inference
framework.

The argument should be a snake_case method name plus the *kind*:

  /propose-method fisher_rao tilting
  /propose-method lrt statistic
  /propose-method dynamic_ci experiment

Recognised kinds: `tilting` | `statistic` | `cd` | `experiment` |
`diagnostic`. If the user supplies only a name, ask which kind.

## Workflow

Execute these steps in order. Pause after each for user review.

### 1. Set up

Confirm with the user:
- The exact name (snake_case).
- The kind.
- A one-sentence description of what the method does.
- Whether they want this as `status="stub"` (just registration +
  brief, NotImplementedError on every method) or `status="implemented"`
  (full math + tests).

### 2. Brief skeleton

Copy `docs/methods/_template.md` to `docs/methods/<name>.md`. Fill
in the Summary, Motivation, Definition (the user-supplied one-line
plus a tentative formal statement), and Status. Leave Derivation,
Predicted behavior, Failure modes, Invariants, Literature, and
Links blank with TODO markers.

### 3. Literature

Invoke the `literature-reviewer` subagent with the method name and
the user-supplied description. Paste its output into the brief's
Literature section. Confirm with the user that the citations are
appropriate before continuing.

### 4. Derivation

Invoke the `deriver` subagent with the method name. Paste its
Derivation block into the brief's Derivation section. Use the
deriver's "Invariants" output to populate the brief's Invariants
section.

### 5. Stub source file

Generate `src/frasian/<area>/<name>.py` from the closest existing
stub (e.g. for a tilting, copy the structure of
`src/frasian/tilting/fisher_rao.py`). Adjust the docstring, name, and
status. If `status="implemented"`, emit a TODO marker in each method
body rather than `NotImplementedError`.

Add the import to `src/frasian/_registry_bootstrap.py`.

### 6. Property test file

Generate `tests/properties/test_<name>_invariants.py` with one
skipped test per invariant from step 4. Use the existing stubs as a
template for the skipped-test idiom. If `status="implemented"`, ask
the user which invariants they want to make pass *now* vs leave
skipped for later.

### 7. Illustration (only for status="implemented")

Generate `src/frasian/experiments/illustrations/<name>_demo.py` from
the closest existing demo (e.g. `power_law_demo.py` for a tilting).

### 8. Skeptic pass

Invoke the `skeptic` subagent on the new source file. Relay its
output. If it returns `block`, do not commit — fix the issues and
re-run the skeptic. If it returns `accept-with-caveats`, ask the
user whether to commit anyway.

### 9. Verify

Run:
- `python tools/check_method_completeness.py`
- `python -m pytest tests/properties/test_<name>_invariants.py`
- `python -m frasian.experiments.illustrations.<name>_demo --smoke`
  (only for `status="implemented"`)

Report any failures.

### 10. Commit (ask first)

Stage the new files and write a commit message. Do NOT commit unless
the user explicitly asks. The commit message should follow the
existing convention:

```
Add <kind> '<name>' (status: <status>)

- Brief at docs/methods/<name>.md (sections: ...)
- Implementation: src/frasian/<area>/<name>.py
- Property tests: tests/properties/test_<name>_invariants.py
- Illustration: ...
- Skeptic: <verdict>

Verification:
  python tools/check_method_completeness.py -> N entries OK
  python -m pytest tests/properties/test_<name>_invariants.py
```

## Design notes

- Stubs are first-class citizens. A `status="stub"` proposal is a
  fully valid use of `/propose-method` — the unit of progress is
  flipping `pytest.mark.skip` decorators to passing tests later.
- The skeptic step is mandatory. Any `block` verdict halts the flow.
- The user reviews each section's output before it is pasted; do not
  skip the review prompts.
- Method-completeness CI will fail merge if any required artifact is
  missing. /propose-method's job is to make sure all artifacts exist
  before the user opens a PR.
