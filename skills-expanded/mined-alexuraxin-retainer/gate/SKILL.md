---
name: gate
description: "Full quality gate in one command — linters, types, import contracts, tests. The set of steps lives in the script, not in prose. Trigger words (RU+EN): гейт, прогони гейт, проверки, полный прогон / gate, run the gate, checks, full run."
disable-model-invocation: true
---

# The gate — one command

```bash
bash scripts/gate.sh    # the command comes from <project>/.retainer/config.toml (gate_command):
                        # a path to the script or a build command (make ci, docker compose run …)
```

**The step list is IN THE SCRIPT ITSELF, not in this file and not in the project rules.** Reason:
a list of steps rots — keep the list in prose and it diverges from reality (there was a case of
"nine steps" when there were ten: graph freshness did not make the list). Prose says WHAT the gate
holds; how many steps exactly and in what order — only the script knows.

## What a typical gate holds (Python preset)

- the rule guard (is the regulation not weakened);
- linters and format: `ruff format --check` · `ruff check` · `flake8` (WPS) · templates · JS (biome,
  if present);
- import contracts: `import-linter`;
- types: `mypy` (strict);
- spelling: `codespell`;
- tests: `pytest` with an N+1 detector and a coverage floor;
- migrations (Django module).

## Two levels, one check

The same gate hangs on the **`pre-push` hook** AND in **CI** (a from-scratch environment).

- The hook is faster and catches earlier — the **first line**.
- The guarantee is **CI**: `git push --no-verify` bypasses the hook entirely, and the hook itself is
  not guaranteed to be versioned and may be absent on another machine.

CI on a from-scratch environment catches what the local one does not see (example: `.mo`
translations built by hand only on the developer's machine; a missing config section that silently
disabled CI).

## Acceptance = a GREEN gate, not "done"

"Done" without a green gate means nothing — the machine judges, not the agent's word. The full run
goes locally until green on what leaves the machine, and the claim "done" is made after it; claims
about parts along the way are proven by a targeted run of the subject, not the full suite. This also
requires a working venv with dev dependencies — part of the task, not a separate step.

## How many runs per task

The full run is one, on what leaves the machine. Along the way there is a targeted run of the
subject of the edit and a mutation probe: they answer whether the check guards what is being edited.
The full run answers a different question — is the tree intact — and that answer is needed once,
when the edits are done.

An intermediate "done" is not proven by the full run: it is proven by a targeted run of the subject
(the cost of a full run per hypothesis is named in "When NOT to apply"). What launches the full run
and where the mutation probe lives is known to the project regulation; the step list — the gate
script, as said above.

## When NOT to apply

- **The gate is not a cause finder.** It says "red" and on exactly what; WHY is the subject of
  [[diagnosing]]. Running the gate in circles instead of building a loop means paying with a full
  run for every hypothesis.
- **Not a measure of task readiness.** A green gate means "the tree is not broken", not "the
  declared is done": the acceptance criteria are checked by the task cycle, not the gate.
- **Not a place for a new check one-off.** A step is added to the gate script, not run beside it by
  hand: a check living outside the script runs only while it is remembered.
- **In a foreign tree without a dependency box** the gate reddens on its own environment. That is
  "not checked", not "broken", and the reader must tell them apart.

Related: [[guardrails]] (linter configs under the guard), [[task-cycle]] (the gate is a cycle step
and a DoD item).
