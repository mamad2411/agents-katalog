---
name: cline-orchestration
description: |
  How to drive the Cline CLI as the coding agent inside a
  loss-function-driven loop. Cline is the *tool surface* the agent
  uses inside the loop. The driver (Hermes or any other orchestrator)
  owns the loop, the loss function, and the verifier runs. Cline
  owns the model call, the per-iteration context, the file edits,
  and the test runs inside its sandbox. Load this skill whenever
  launching, monitoring, or interrupting a Cline session from
  inside a loss-function-driven loop. Also load it when building
  a Cline wrapper script — the verified invocation shape, the
  NDJSON schema, the parser, and the contract the wrapper must
  satisfy all live here.
version: 2.0.0
author: open source
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [cline, acp, agent-client-protocol, agent-orchestration, coding-agents]
    related_skills: [harness-engineering, loss-function-design]
---

# Cline Orchestration

This skill describes how to drive **Cline CLI** as the coding
agent inside a loss-function-driven loop. The pattern is
**agent-agnostic at the driver level** — Hermes is the driver in
the reference build, but any orchestrator (a shell script, CI
runner, another agent) that can spawn a subprocess and read
JSON can use the same wrapper contract.

The split:

- **The driver owns:** the loop, the loss function, the verifier
  runs, the human-facing surface, the stop criterion, the budget.
- **Cline owns:** the model call, the tool surface, the
  per-iteration context, the file edits, the test runs inside
  its sandbox.

## Why Cline

- Native tool surface (file edit, command run, browser, MCP).
- Provider-agnostic. `cline auth` chooses the provider/model; the
  driver never sets it.
- JSON output for headless integration (`--json`).
- ACP support for editor integration (`--acp`).
- Plan mode for read-only exploration (`--plan`).
- Reasoning effort flag (`--thinking none|low|medium|high|xhigh`)
  — provider-dependent; see below.
- Hooks for runtime injection (`--hooks-dir`).

## Locating the `cline` binary

The wrapper resolves the binary at call time. The resolution
order is:

1. The `$CLINE_BIN` environment variable, if set.
2. `$(command -v cline)` — whatever's on `PATH`.
3. A handful of conventional install locations
   (`/usr/local/bin/cline`, `~/.local/bin/cline`,
   `~/.claude/bin/cline` — adjust to your installation).

If none resolve, the wrapper emits a structured JSON error and
exits non-zero. There is no hard-coded path.

## Cline invocation (verified against v3.0.34+)

The working invocation is:

```bash
cline "$TASK" \
  --cwd "$ITER_DIR" \
  --auto-approve true \
  --thinking none \
  --json
```

Where:

- `cline` is the positional prompt. There is **no `-q` flag** in
  v3.0.34+. (Older docs and blog posts still show `-q`; that flag
  is gone. Prompt is positional.)
- `--auto-approve true` is **required** for non-interactive file
  work. With `--auto-approve false` Cline refuses to write files
  non-interactively. Safety is NOT enforced by per-tool approval —
  enforce it with a transcript grep in the safety sub-loss. The
  naive belief "auto-approve false is safer" is wrong for headless
  loops; it just breaks file writes; safety has to live in the
  verifier.
- `--thinking none` is the only level guaranteed to work with
  every provider, including OpenAI-compat endpoints that don't
  pass reasoning tokens through. `--thinking low / medium / high /
  xhigh` produces `"Invalid request Error"` from many upstreams.
  If the model is switched to one that supports reasoning tokens,
  change to `--thinking high`.
- No `--worktree`. The per-cycle `ITER_DIR` is fresh and gives
  isolation. `--worktree` triggers auth failures with providers
  that don't carry their auth into the worktree dir.
- No `--provider` and no `--model`. `cline auth` chose them. The
  driver never overrides.

## Modes of driving Cline

### 1. One-shot headless

```bash
cline "fix the turbo cache globalEnv leak" \
  --cwd /path/to/project \
  --auto-approve true \
  --thinking none \
  --json
```

- `--json` returns NDJSON, one event per line. The authoritative
  final state is the `run_result` event, not the last assistant
  message. Use `scripts/parse_cline_output.py` to extract
  `tokens`, `duration_ms`, `candidate_text`, `model`, `provider`,
  `tool_calls`. Don't hand-roll a parser.
- `--auto-approve true` lets Cline actually write files; see the
  safety note above.
- `--cwd` sets the working directory; matches the verifier's
  contract directory.

This is what the loss-function loop uses for *proposal generation*
when the agent is allowed to run to completion in one shot.

### 2. One-shot headless with per-cycle directory (instead of --worktree)

The Elvis turbo-cache loop's "each experiment = isolated branch"
rule maps to a per-cycle `ITER_DIR`, not `--worktree`:

```bash
mkdir -p "$PROJECT_DIR/.iterations/cycle-1"
cline "hypothesis: NEXT_PUBLIC_VERCEL_URL in globalEnv is \
poisoning the turbo cache hash. Prove or disprove." \
  --cwd "$PROJECT_DIR/.iterations/cycle-1" \
  --auto-approve true \
  --thinking none \
  --json
```

The wrapper script creates `$PROJECT_DIR/.iterations/cycle-N/`
per iteration. The verifier runs against that directory. State
never leaks between cycles.

### 3. Plan mode (read-only exploration)

```bash
cline --plan "design a loss function for the turbo cache \
correctness sub-loss. read the AGENTS.md and the docs/ tree. \
return a rubric and a candidate verifier implementation." \
  --cwd /path/to/project
```

Plan mode is Cline's read-only / thinking-only mode. The output
is a plan, not a diff. Use it for *design* before *iteration*.

### 4. ACP / TUI (interactive / editor integration)

For loops where the human is watching the agent work in real
time:

- `--acp` — Agent Client Protocol, for VS Code / Zed / JetBrains.
- `--tui` — `cline -i` opens the terminal UI for interactive
  sessions.

These are *not* what the loss-function loop uses by default. The
loss-function loop is headless (`--json`). TUI is for the human
debugging a stuck loop.

### 5. Resuming a session

Cline supports resuming an existing session by ID:

```bash
cline --id <session-id> "refine the candidate based on this loss: ..."
```

This is the *cheap* way to iterate. The driver doesn't tear down
the Cline session between iterations; it just re-issues a message
with the new loss and the previous candidate.

For a more disciplined iteration, prefer a fresh `ITER_DIR` per
iteration so each hypothesis is isolated and the verifier's
contract is clean.

### 6. Provider / model override

The user has selected a model for the team's stack. Cline honors
the selected provider/model by default. To force a specific
provider/model for one run:

```bash
cline -P openai -m gpt-5 \
  "..." \
  --cwd /path/to/project
```

The loss-function-developer should *not* hard-code a model. The
model is the team's choice. The loss is model-agnostic. **Do not
embed provider or model flags in the wrapper** — leave the model's
choice to the human's `cline auth`.

## The driver loop (any orchestrator)

A canonical driver loop. The wrapper itself is at
`verifiers/cline-wrapper.sh` in the reference build; this
snippet is the conceptual shape:

```python
# pseudocode for a loss-function-driven driver
import json, subprocess

PROJECT_DIR     = "/path/to/project"
CYCLE_DIR_BASE  = f"{PROJECT_DIR}/.iterations/cycle-{{}}"
LOSS_SCRIPT     = "./verifiers/compute_sub_losses.py"

def run_iteration(hypothesis_prompt: str, iter_id: int) -> dict:
    iter_dir = CYCLE_DIR_BASE.format(f"{iter_id:03d}")
    result = subprocess.run(
        ["./verifiers/cline-wrapper.sh", hypothesis_prompt,
         "--cwd", iter_dir,
         "--timeout", "3600",
         "--cycle", f"cycle-{iter_id:03d}"],
        capture_output=True, text=True, timeout=3700,
    )
    cycle = json.loads(result.stdout)
    loss_result = subprocess.run(
        ["python", LOSS_SCRIPT, f"{iter_dir}/cline.json"],
        capture_output=True, text=True, timeout=1800,
    )
    scores = json.loads(loss_result.stdout)
    return {
        "iteration": iter_id,
        "candidate_text": cycle.get("candidate_text", ""),
        "tokens": cycle.get("tokens", 0),
        "duration_ms": cycle.get("duration_ms", 0),
        "model": cycle.get("model", ""),
        "scores": scores,
    }
```

The driver reads Cline's output via the wrapper, which calls
`scripts/parse_cline_output.py`. The verifier's JSON goes
through the same parsing discipline. Both are agent-legible.

## Hooks and the agent contract

Cline supports runtime hook injection via `--hooks-dir`. For a
loss-function loop, a common pattern is a hook that:

- Logs every tool call to a structured file the verifier reads.
- Intercepts `git commit` and `git push` and routes them through
  a verifier.
- Tags every Cline session with the current iteration ID so the
  verifier can correlate.

This is an *implementation* detail of the loop, not of the loss
function. The loss function only cares that the contract is
honored.

## Compaction

Cline's `--compaction` mode controls how aggressively Cline
compresses its own context.

- `agentic` — Cline drives its own compaction (can be expensive).
- `basic` — Cline uses a deterministic sliding window (default).
- `off` — No compaction; risk of context overflow.

For a loss-function loop, `agentic` is appropriate only if the
loop budget can absorb the compaction cost. `basic` is the safe
default.

## Pitfalls when driving Cline

- **Don't pass `cline` an instruction that contradicts the
  rubric.** If the rubric says "no `as any`" and the prompt says
  "be pragmatic", Cline will follow the prompt.
- **Don't think `--auto-approve false` is the safe default.** It
  is for interactive use. Cline with `--auto-approve false`
  refuses to write files non-interactively. For a headless loop,
  the safe default is `--auto-approve true`, with safety
  enforced by a separate transcript grep (see the `safety`
  sub-loss in `loss-function-design`).
- **Don't assume `--thinking high` works.** It depends on the
  provider. Many OpenAI-compat endpoints fail with `Invalid
  request Error`. Start with `--thinking none` and re-verify per
  provider.
- **Don't use `--worktree` blindly.** It triggers auth failures
  with providers that don't carry auth into the worktree dir.
  Per-cycle `ITER_DIR` is the safer isolation primitive.
- **Don't run multiple Cline sessions against the same
  directory.** The Elvis loop's isolation rule applies to the
  verifier's state, not just the agent's. If two Cline sessions
  share a verifier cache, the loss is broken.
- **Don't hand-roll the NDJSON parser.** Use
  `scripts/parse_cline_output.py`. The schema has changed across
  Cline versions and will change again. Centralize the parser.
  See `references/verifier-script-gotchas.md` for the class-level
  Python/JSON pitfalls (exit_code falsy-zero, json.loads on NDJSON,
  Python 3.9 compat) that bit while building the verifier
  scripts.
- **Don't trust the absence of an error.** `run_result.text`
  containing `"Invalid request Error"` is a failure even though
  `exit_code` is 0 and `finishReason` may be `"error"` or
  `"completed"`. Always read `run_result.finishReason` AND
  `run_result.text` and treat any of {error, refusal string,
  empty candidate} as a non-zero cycle.
- **Don't embed the provider or model in the wrapper.** Leave
  that to `cline auth`. The wrapper is reusable; provider
  settings are per-user.
- **Don't write verifier Python inline in bash heredocs.** Put
  the Python in `scripts/` files. See
  `references/verifier-script-gotchas.md` for the failures this
  caused.
- **Don't claim "the loop is running" from a `delegate_task`
  return value alone.** A successful dispatch returns a
  delegation id synchronously but produces no observable state
  until the result re-enters the conversation. Before reporting a
  dispatched loop as live, require (a) a file the subagent must
  have written that exists, (b) a sub-loss score, or (c) an
  explicit failure message. A dispatch receipt is not evidence
  the work is happening.
- **Don't trust `tokens == 0` from the wrapper JSON.** The
  parser may report 0 tokens for a long-running task. The most
  common cause is that the authoritative
  `run_result.aggregateUsage.totalTokens` field was missing or
  shaped differently than the parser expected. Verify with
  `elapsed_seconds` and `cline.stderr` before drawing
  conclusions.
- **Don't conflate "the wrapper returned a JSON object" with
  "the design set scored the run".** The wrapper emits a JSON
  summary per task; the design-set script runs the per-task
  grader and then writes the aggregate. A cycle that "ran" but
  failed every task is still a 0.0 pass_rate.
- **Don't skip `export CLINE_NO_AUTO_UPDATE=1` in the wrapper.**
  Cline's binary runs a detached auto-updater on every
  invocation that fetches the latest version from npm,
  spawns a detached `npm install`, and RESTARTS the
  background hub that tracks sessions. With back-to-back
  Cline invocations (the loss-function loop runs many in
  a row), the hub restart races with the next invocation's
  session lookup and produces `"session not found: <id>"`
  errors with 286-byte cline.json. Cline reads
  `CLINE_NO_AUTO_UPDATE=1` in its own source and skips the
  auto-updater when set. Without this env var, the loop
  will flake on the second-and-later Cline invocations of
  any batch. See `references/cline-v3-invocation.md` for
  the full story.

## Cline version pinning

The driver should pin the Cline version it drives against. To
check:

```bash
cline --version
```

For a loss-function loop, document the Cline version alongside
the loss rubric. When the Cline version moves, re-run the wrapper
smoke test (a one-line "create hello.txt" task) before trusting
any loop output.

The Cline wrapper contract — what shape the wrapper script must
satisfy, the full annotated worked example, and the on-disk
reference build path — lives at
`references/cline-wrapper-contract.md`. **Treat the contract as
load-bearing:** every loop driver in the project should invoke
the wrapper, never `cline` directly.

## User-style preferences (load these into every reply)

This skill is often loaded for short Q&A. When the user is in
the loop:

- **Default to code, not prose.** When the user asks "what
  would happen" or "give me the prompt," they want a runnable
  artifact. Lead with code, follow with one paragraph of
  context.
- **Don't burn a turn on three setup questions.** Pick
  defaults, state them in `README.md`, just start.
- **Match the answer format to the question format.** A
  one-sentence question gets a one-sentence answer. The
  format the user asks for is binding.
- **Verify before claiming live.** An async-dispatch receipt
  is not proof of work. See
  `references/verification-gate.md`.

## When to load this skill

- The user asks to start, monitor, or interrupt a Cline session.
- The user asks how the loss function integrates with the agent
  runtime.
- The user wants to debug a loop that is stuck.
- The user asks about provider / model switching for a loop run.
- The user is building a Cline wrapper and needs the proven
  invocation shape.
- The user is writing any verifier script that reads JSON
  emitted from a shell pipeline.

## References in this skill

- `references/cline-v3-invocation.md` — verified-good Cline
  v3.0.34+ invocation flags, the table of what broke and why,
  and the parser schema.
- `references/cline-wrapper-contract.md` — what the wrapper
  script must do, plus an annotated worked example.
- `references/verifier-script-gotchas.md` — class-level
  Python/JSON pitfalls hit while building the sub-loss verifier.
- `references/subagent-dispatch-gotchas.md` — the
  fire-and-forget dispatch pattern: synchronous return is a
  receipt, not proof of work.
- `references/compute-sub-losses.py` — the per-cycle sub-loss
  scorer. Drop-in for any Cline-driven loop.
- `references/cline-skills-install.md` — where Cline scans for
  skills on each platform.
- `references/smoke-test-protocol.md` — what to check before
  claiming a cycle is good.
- `scripts/parse_cline_output.py` — the verified NDJSON parser.
  Use this; don't hand-roll.

## Related skills (install separately)

- `harness-engineering` — the harness side: context, tools,
  scaffolding, feedback loops.
- `loss-function-design` — the loss-function side: target,
  constraints, instruments, forced entropy.
