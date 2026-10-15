---
name: fake-agent-orchestration
description: |
  How to drive the **fake-agent** stub as the inner coding
  agent inside a loss-function-driven loop. The fake agent
  is a deterministic stub: it echoes the cycle prompt back
  as the "candidate text", writes a fixed file to the
  iteration directory, and emits a deterministic JSON
  result. There is no model, no network, no flakiness.
  This adapter exists for **dogfood testing** — verifying
  that the LFD system itself works end-to-end without
  spending tokens or depending on a real coding agent.
  Load this skill when building a deterministic verifier
  (the LFD system verifies itself), or when testing
  the loop / scaffold / parsers in CI. Do NOT use it for
  actual development cycles.
version: 1.0.0
author: open source
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [fake-agent, stub, deterministic, testing, dogfood, agent-orchestration]
    related_skills: [cline-orchestration, claude-code-orchestration, codex-orchestration, hermes-agent-orchestration, opencode-orchestration, harness-engineering, loss-function-design]
---

# Fake-Agent Orchestration

This skill describes how to drive **`fake-agent`** as the
inner coding agent inside a loss-function-driven loop. The
fake agent is a **deterministic stub**: no model, no
network, no flakiness, identical output every run.

The split:

- **The driver owns:** the loop, the loss function, the
  verifier runs, the human-facing surface, the stop
  criterion, the budget.
- **fake-agent owns:** emitting a fixed JSON result,
  writing a fixed file to the iteration dir, returning
  success. The "candidate text" is the cycle prompt
  itself (echoed), so the loop's `legibility_score`
  always sees something. The "tokens" / "duration_ms"
  are zero.

## Why fake-agent exists

The LFD bundle is verified by **dogfooding**: a `/goal`
prompt is run through the full `harness-scaffold` →
`loop-driver` → score → sub-losses chain, and the
output is checked. With a real coding agent this is
non-deterministic (different completions each run) and
expensive (every cycle burns tokens).

`fake-agent` makes the verifier deterministic and free.
It satisfies the same wrapper contract as the other 5
adapters (positional `TASK` + `--cwd` + `--timeout` +
`--cycle`, JSON output on stdout, exit 0 on success) so
it drops in via `--runtime fake` without changing the
loop driver.

## Why you would NOT use it for real work

`fake-agent` produces no actual code changes. The
"candidate skill" it writes to the iteration dir is a
fixed stub (always the same content), so the loop will
never improve past the baseline. It's a test fixture,
not a coding agent.

## Wrapper contract

```bash
verifiers/fake-agent-wrapper.sh "<task-prompt>" --cwd PATH \
    --timeout 60 --cycle cycle-1 > cycle-summary.json
```

Same shape as the other 5 adapter wrappers:

- `<task-prompt>` — **positional**. Echoed into the
  `candidate_text` field of the result.
- `--cwd PATH` — the iteration directory. The wrapper
  writes a fixed `candidate.md` file here.
- `--timeout N` — wall-clock cap. The fake wrapper is
  instant; the timeout is honored for shape-compatibility
  with the other adapters.
- `--cycle NAME` — used to name the per-iteration output
  files. Default: `cycle-0`.

Exit codes:

- `0` — always (the fake agent cannot fail)
- `2` — usage error
- `3` — missing required arg

## Output schema

The wrapper writes `cycle-summary.json` to stdout:

```json
{
  "cycle": "cycle-1",
  "exit_code": 0,
  "elapsed_seconds": 0,
  "claude_duration_ms": 0,
  "tokens": 0,
  "model": "fake",
  "provider": "stub",
  "candidate_text": "<the task prompt, echoed>",
  "tool_calls": [
    {"name": "write_candidate", "args": {"path": "candidate.md"}}
  ],
  "finish_reason": "completed",
  "iterations": 1,
  "raw_output_path": "<CWD>/.iterations/cycle-1/fake.json"
}
```

The 8 required fields (`tokens`, `duration_ms`,
`candidate_text`, `model`, `provider`, `finish_reason`,
`iterations`, `tool_calls`) all match the shared
parser shape, so the loop-driver can read fake-agent
output the same way it reads real adapter output.

## What the wrapper does

1. Resolve args (cycle, cwd, timeout).
2. Echo the task prompt to `candidate_text`.
3. Write a fixed stub `candidate.md` to the iteration
   dir (10 lines, deterministic content).
4. Emit the JSON to stdout.
5. Exit 0.

The stub `candidate.md` content is intentionally
trivial — it doesn't pretend to be a useful skill, it
just gives the loop something to grade. A real
verifier-project overwrites this with the actual
candidate produced by the cycle (the agent still has to
edit the file; the wrapper just provides a starting
scaffold).

## What the wrapper does NOT do

- It does **not** invoke any model.
- It does **not** call the network.
- It does **not** read the LFD bundle's other skills
  (the verifier-project is responsible for loading
  those into the test profile).
- It does **not** vary its output across runs. This is
  the point.

## The skills-dir instrument

```bash
verifiers/fake-agent-skills-dir.sh
```

Prints:

```
FAKE_SKILLS_DIR=<cwd>/.fake-skills
---
Fake agent has no real skills directory. Candidates are
written to <cwd>/.fake-skills/ which the wrapper creates
on demand.
```

The instrument exists for shape-compatibility with the
other adapters' `<agent>-skills-dir.sh`. The cycle.sh
script in loop-driver calls it to learn where to
install the candidate. For fake-agent, that's
`<cwd>/.fake-skills/`.

## Drop-in substitution

Same contract as the other 5 adapters (see
`compatibility.md`):

1. `scripts/parse_fake_output.py` — parser emitting the
   shared 8-key shape.
2. `references/fake-agent-wrapper-contract.md` — this
   file.
3. `references/fake-agent-invocation.md` — the verified
   invocation reference.
4. `references/fake-agent-skills-dir.sh` — the skills-dir
   instrument.

## Building a verifier-project with fake-agent

The pattern (used in
`examples/lfd-system-verifier/`):

1. Write a `/goal` prompt that describes the
   verification task: "verify the LFD system end-to-end".
2. Scaffold a project tree by hand (or use
   `harness-scaffold --runtime fake` once the scaffold
   is updated to accept the `fake` runtime). The tree
   has:
   - `verifiers/fake-agent-wrapper.sh` (the wrapper
     above)
   - `verifiers/run-design-set.sh` (loops over design
     tasks, runs the wrapper + per-task grader)
   - `verifiers/instruments/fake-agent-skills-dir.sh`
     (the skills-dir instrument)
   - `verifiers/instruments/{time-remaining,tokens-remaining,tokens-this-iter}.sh`
     (the standard instruments)
   - `verifiers/instruments/sub-loss-readout.sh` (calls
     the per-cycle sub-loss scorer)
   - `verifiers/compute_sub_losses.py` (per-cycle
     sub-loss scorer; uses the same 7-sub-loss model
     from `cline-orchestration/references/compute-sub-losses.py`)
   - `test-tasks/design/<n>-<name>/prompt.txt` (5
     deterministic design tasks)
   - `test-tasks/design/<n>-<name>/grade.sh` (per-task
     grader; returns 0 on pass, 1 on fail, prints
     `score=<float>` to stdout)
   - `test-tasks/held-out/<n>-<name>/...` (5 tasks the
     agent never sees)
3. Run the loop:
   ```bash
   ./verifiers/loop-driver/scripts/run-loop.sh \
       --project-root . \
       --runtime fake \
       --max-cycles 1 \
       --wrapper-timeout 60
   ```
4. The loop produces `logs/cycle-1/cycle-summary.json`,
   `logs/cycle-1/sub-losses.json`, `logs/best-cycle.json`.
5. The verifier's `run-verification.sh` script:
   - Runs the loop
   - Reads `logs/best-cycle.json` + `logs/cycle-1/sub-losses.json`
   - Reads the per-task grade logs
   - Produces `verification-report.md` and
     `verification-report.json`
   - Cleans all per-cycle artifacts (`.iterations/`,
     `logs/cycle-*/`) keeping only the report

## Determinism guarantees

The fake-agent wrapper is **bit-exact deterministic**:

- Same input → same output, every run
- No real time, no real network, no environment reads
  except `cwd` and the task prompt
- The `cycle-summary.json` differs only in `cycle`
  (taken from the `--cycle` arg) and the
  `raw_output_path` (which contains the cycle name and
  the cwd)

For the verifier to be **end-to-end deterministic**, the
per-task graders must also be deterministic (no
`$(date +%s)` in score files, no model calls, no
network reads). The `examples/lfd-system-verifier/`
shipped graders satisfy this.

## Common pitfalls

1. **Trying to use fake-agent for real work.** It
   doesn't write real code. The candidate is a fixed
   stub. Use a real adapter (Cline, Claude Code, etc.)
   for actual development cycles.

2. **Putting `date` / `$$` / `$RANDOM` in the wrapper.**
   Breaks determinism. Use only `$cwd`, `$cycle`, and
   the task prompt.

3. **Forgetting that the verifier-project needs the LFD
   bundle installed separately.** The fake-agent wrapper
   doesn't load the bundle's skills — that's the test
   profile's job. The verifier's `run-verification.sh`
   script must call `./install.sh <profile> --force`
   before running the loop, or the candidate skill the
   agent is "grading" against won't be the LFD bundle.

4. **Forgetting to clean `.iterations/`.** The cycle
   leaves per-iteration artifacts. The
   `run-verification.sh` script must `rm -rf` these
   before exiting so the verifier's "test artifacts are
   cleaned" rule holds.

## Verification checklist

- [ ] Wrapper resolves `--cycle`, `--cwd`, `--timeout`
      from CLI args; positional `TASK` echoed.
- [ ] Wrapper writes a deterministic `candidate.md` to
      `<cwd>/`.
- [ ] Wrapper emits JSON with the 8 required shared
      fields.
- [ ] Wrapper exits 0 on success, 2 on usage error.
- [ ] Wrapper honors `--timeout` (uses `timeout` and
      SIGKILLs on overrun, even though it should never
      overrun).
- [ ] `parse_fake_output.py` parses the JSON and emits
      the shared 8-key shape.
- [ ] `fake-agent-skills-dir.sh` prints a SKILLS_DIR
      line.
- [ ] No absolute paths, no per-user config baked in.
- [ ] Two consecutive runs of the same input produce
      byte-identical output (modulo the cycle name).
